//! Manifest Service.
//!
//! Implements the Runtime Service Contract (RFC-0003 §9) for the manifest
//! subsystem (RFC-0010). The Manifest System consists of a Parser, a Schema
//! Validator, and a Capability Registry (RFC-0010 §8).
//!
//! Parsing and validation are **independent of business logic**: this service
//! only reads, parses, validates, and exposes manifest data. It does not
//! instantiate services or execute workflows.
//!
//! The manifest is immutable once loaded (RFC-0010 §4).

use atlas_common::manifest::{Capability, Manifest, ServiceDeclaration};
use atlas_common::{HealthStatus, ManifestError};
use atlas_contracts::{ServiceContract, ServiceError, ServiceId, ServiceName};
use std::path::Path;
use std::sync::Mutex;

use crate::config::ConfigService;

/// Stable service identifier for the Manifest Service.
pub const SERVICE_ID: &str = "srv-manifest";

/// Manifest Service — parses, validates, and exposes runtime manifests.
pub struct ManifestService {
    id: ServiceId,
    name: ServiceName,
    dependencies: Vec<ServiceId>,
    priority: u8,
    required: bool,
    state: Mutex<ManifestState>,
}

#[derive(Debug, Default)]
struct ManifestState {
    /// Parsed and validated manifest.
    manifest: Option<Manifest>,
    /// Whether `initialize` has run.
    initialized: bool,
    /// Whether `start` has run.
    started: bool,
}

impl ManifestService {
    /// Create a new, uninitialised Manifest Service that depends on the
    /// Configuration Service for manifest-path resolution.
    pub fn new() -> Self {
        Self {
            id: SERVICE_ID.to_string(),
            name: "Manifest Service".to_string(),
            dependencies: vec![crate::config::SERVICE_ID.to_string()],
            priority: 1,
            required: true,
            state: Mutex::new(ManifestState::default()),
        }
    }

    /// Load and validate a manifest from a JSON file at `path` (RFC-0010 §12).
    pub fn load_from_path(&self, path: &str) -> Result<Manifest, ManifestError> {
        if !Path::new(path).exists() {
            return Err(ManifestError::FileNotFound(path.to_string()));
        }
        let bytes =
            std::fs::read(path).map_err(|e| ManifestError::ParseError(e.to_string()))?;
        let manifest: Manifest =
            serde_json::from_slice(&bytes).map_err(|e| ManifestError::ParseError(e.to_string()))?;
        Self::validate(&manifest)?;
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        state.manifest = Some(manifest.clone());
        Ok(manifest)
    }

    /// Load a manifest from an already-parsed [`Manifest`] value, validating it.
    pub fn load_value(&self, manifest: Manifest) -> Result<(), ManifestError> {
        Self::validate(&manifest)?;
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        state.manifest = Some(manifest);
        Ok(())
    }

    /// Load the manifest using the manifest path declared in the configuration.
    pub fn load_from_config(&self, config: &ConfigService) -> Result<Manifest, ManifestError> {
        let cfg = config
            .get()
            .map_err(|e| ManifestError::ParseError(e.to_string()))?;
        let path = cfg
            .manifest_path
            .ok_or(ManifestError::ValidationError("manifest_path not set".to_string()))?;
        self.load_from_path(&path)
    }

    /// Return a clone of the loaded manifest, or an error if not loaded.
    pub fn manifest(&self) -> Result<Manifest, ManifestError> {
        self.state
            .lock()
            .expect("manifest state mutex poisoned")
            .manifest
            .clone()
            .ok_or(ManifestError::ValidationError("manifest not loaded".to_string()))
    }

    /// Discover service declarations from the loaded manifest.
    pub fn discover_services(&self) -> Result<Vec<ServiceDeclaration>, ManifestError> {
        Ok(self.manifest()?.services)
    }

    /// Return all declared capabilities (RFC-0010 §10).
    pub fn capabilities(&self) -> Result<Vec<Capability>, ManifestError> {
        Ok(self.manifest()?.capabilities)
    }

    /// Whether a capability is declared and enabled.
    pub fn has_capability(&self, name: &str) -> Result<bool, ManifestError> {
        Ok(self
            .manifest()?
            .capabilities
            .iter()
            .any(|c| c.name == name && c.enabled))
    }

    /// Return required-but-disabled capabilities (missing required caps).
    pub fn missing_required_capabilities(&self) -> Result<Vec<Capability>, ManifestError> {
        Ok(self
            .manifest()?
            .capabilities
            .iter()
            .filter(|c| c.required && !c.enabled)
            .cloned()
            .collect())
    }
}

impl Default for ManifestService {
    fn default() -> Self {
        Self::new()
    }
}

impl ManifestService {
    /// Validate a manifest against the standard schema (RFC-0010 §9, §19).
    ///
    /// Checks performed (independent of business logic):
    /// - `schema_version` and `runtime_version` are non-empty.
    /// - No duplicate capability names; capability names are non-empty.
    /// - No duplicate service IDs; service IDs are non-empty.
    pub fn validate(manifest: &Manifest) -> Result<(), ManifestError> {
        if manifest.schema_version.is_empty() {
            return Err(ManifestError::ValidationError(
                "schema_version must not be empty".to_string(),
            ));
        }
        if manifest.runtime_version.is_empty() {
            return Err(ManifestError::ValidationError(
                "runtime_version must not be empty".to_string(),
            ));
        }

        let mut seen_caps = std::collections::HashSet::new();
        for cap in &manifest.capabilities {
            if cap.name.is_empty() {
                return Err(ManifestError::ValidationError(
                    "capability name must not be empty".to_string(),
                ));
            }
            if !seen_caps.insert(cap.name.clone()) {
                return Err(ManifestError::ValidationError(format!(
                    "duplicate capability: {}",
                    cap.name
                )));
            }
        }

        let mut seen_ids = std::collections::HashSet::new();
        for svc in &manifest.services {
            if svc.id.is_empty() {
                return Err(ManifestError::ValidationError(
                    "service id must not be empty".to_string(),
                ));
            }
            if !seen_ids.insert(svc.id.clone()) {
                return Err(ManifestError::ValidationError(format!(
                    "duplicate service id: {}",
                    svc.id
                )));
            }
        }
        Ok(())
    }
}

impl ServiceContract for ManifestService {
    fn id(&self) -> &ServiceId {
        &self.id
    }

    fn name(&self) -> &ServiceName {
        &self.name
    }

    fn dependencies(&self) -> &[ServiceId] {
        &self.dependencies
    }

    fn priority(&self) -> u8 {
        self.priority
    }

    fn required(&self) -> bool {
        self.required
    }

    fn health_check(&self) -> HealthStatus {
        let state = self.state.lock().expect("manifest state mutex poisoned");
        if state.manifest.is_some() {
            HealthStatus::Healthy
        } else {
            HealthStatus::Degraded("manifest not loaded".to_string())
        }
    }

    fn initialize(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        if state.initialized {
            return Err(ServiceError::InvalidState("already initialized".to_string()));
        }
        state.initialized = true;
        Ok(())
    }

    fn start(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        if !state.initialized {
            return Err(ServiceError::InvalidState("not initialized".to_string()));
        }
        state.started = true;
        Ok(())
    }

    fn pause(&mut self) -> Result<(), ServiceError> {
        Ok(())
    }

    fn resume(&mut self) -> Result<(), ServiceError> {
        Ok(())
    }

    fn stop(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        state.started = false;
        Ok(())
    }

    fn deinitialize(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        state.started = false;
        state.initialized = false;
        Ok(())
    }

    fn dispose(&mut self) {
        let mut state = self.state.lock().expect("manifest state mutex poisoned");
        state.manifest = None;
        state.initialized = false;
        state.started = false;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use atlas_common::manifest::{Capability, Manifest, ServiceDeclaration};
    use std::io::Write;

    fn valid_manifest() -> Manifest {
        Manifest {
            schema_version: "1.0".to_string(),
            runtime_version: "1.0.0".to_string(),
            name: "atlas".to_string(),
            version: "1.0.0".to_string(),
            capabilities: vec![Capability {
                name: "vision".to_string(),
                enabled: true,
                required: false,
            }],
            services: vec![ServiceDeclaration {
                id: "svc-1".to_string(),
                name: "S1".to_string(),
                version: "1.0".to_string(),
                dependencies: vec![],
                required: true,
                priority: 0,
            }],
            ..Default::default()
        }
    }

    #[test]
    fn test_validate_accepts_valid_manifest() {
        assert!(ManifestService::validate(&valid_manifest()).is_ok());
    }

    #[test]
    fn test_validate_rejects_empty_schema_version() {
        let mut m = valid_manifest();
        m.schema_version = String::new();
        assert!(ManifestService::validate(&m).is_err());
    }

    #[test]
    fn test_validate_rejects_duplicate_capability() {
        let mut m = valid_manifest();
        m.capabilities.push(Capability {
            name: "vision".to_string(),
            enabled: false,
            required: false,
        });
        assert!(ManifestService::validate(&m).is_err());
    }

    #[test]
    fn test_validate_rejects_duplicate_service_id() {
        let mut m = valid_manifest();
        m.services.push(ServiceDeclaration {
            id: "svc-1".to_string(),
            name: "Dup".to_string(),
            version: "1.0".to_string(),
            dependencies: vec![],
            required: false,
            priority: 1,
        });
        assert!(ManifestService::validate(&m).is_err());
    }

    #[test]
    fn test_load_from_path_missing_file() {
        let svc = ManifestService::new();
        assert!(svc.load_from_path("/nonexistent/manifest.json").is_err());
    }

    #[test]
    fn test_load_from_path_valid_file() {
        let dir = std::env::temp_dir();
        let path = dir.join("atlas_manifest_test_valid.json");
        {
            let mut f = std::fs::File::create(&path).unwrap();
            f.write_all(br#"{"schema_version":"1.0","runtime_version":"1.0.0","name":"atlas","version":"1.0.0"}"#).unwrap();
        }
        let svc = ManifestService::new();
        let m = svc.load_from_path(path.to_str().unwrap()).unwrap();
        assert_eq!(m.schema_version, "1.0");
        assert!(svc.has_capability("vision").unwrap() == false);
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_discover_services_and_capabilities() {
        let svc = ManifestService::new();
        svc.load_value(valid_manifest()).unwrap();
        assert_eq!(svc.discover_services().unwrap().len(), 1);
        assert_eq!(svc.capabilities().unwrap().len(), 1);
        assert!(svc.has_capability("vision").unwrap());
    }

    #[test]
    fn test_missing_required_capabilities() {
        let mut m = valid_manifest();
        m.capabilities.push(Capability {
            name: "gpu".to_string(),
            enabled: false,
            required: true,
        });
        let svc = ManifestService::new();
        svc.load_value(m).unwrap();
        let missing = svc.missing_required_capabilities().unwrap();
        assert_eq!(missing.len(), 1);
        assert_eq!(missing[0].name, "gpu");
    }

    #[test]
    fn test_manifest_service_lifecycle() {
        let mut svc = ManifestService::new();
        svc.load_value(valid_manifest()).unwrap();
        svc.initialize().unwrap();
        svc.start().unwrap();
        assert!(svc.health_check().is_healthy());
        svc.stop().unwrap();
        svc.deinitialize().unwrap();
        svc.dispose();
        assert!(!svc.health_check().is_healthy());
    }

    #[test]
    fn test_load_from_config_without_manifest_path() {
        let cfg = ConfigService::new();
        cfg.load_value(atlas_common::config::Configuration::default())
            .unwrap();
        let svc = ManifestService::new();
        assert!(svc.load_from_config(&cfg).is_err());
    }
}
