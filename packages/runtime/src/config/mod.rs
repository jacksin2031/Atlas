//! Configuration Service.
//!
//! Implements the Runtime Service Contract (RFC-0003 §9) for the configuration
//! subsystem (RFC-0010 §9). The service loads, parses, and validates a runtime
//! configuration document and exposes it as an immutable [`Configuration`].
//!
//! Immutability rule (RFC-0010 §4): configuration MUST be immutable after the
//! Runtime reaches the Running state. [`ConfigService::freeze`] enforces this;
//! any mutating call after freezing returns [`ConfigError::Frozen`].
//!
//! The service uses interior mutability so it is [`Send`] + [`Sync`] and can be
//! shared via dependency injection without global mutable state.

use atlas_common::config::Configuration;
use atlas_common::{ConfigError, HealthStatus};
use atlas_contracts::{ServiceContract, ServiceError, ServiceId, ServiceName};
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;

/// Stable service identifier for the Configuration Service.
pub const SERVICE_ID: &str = "srv-config";

/// Configuration Service — loads and exposes immutable runtime configuration.
pub struct ConfigService {
    id: ServiceId,
    name: ServiceName,
    dependencies: Vec<ServiceId>,
    priority: u8,
    required: bool,
    state: Mutex<ConfigState>,
    frozen: AtomicBool,
}

#[derive(Debug, Default)]
struct ConfigState {
    /// Path the configuration was loaded from, if any.
    path: Option<String>,
    /// Parsed configuration document.
    config: Option<Configuration>,
    /// Whether `initialize` has run.
    initialized: bool,
    /// Whether `start` has run.
    started: bool,
}

impl ConfigService {
    /// Create a new, uninitialised Configuration Service.
    pub fn new() -> Self {
        Self {
            id: SERVICE_ID.to_string(),
            name: "Configuration Service".to_string(),
            dependencies: Vec::new(),
            priority: 0,
            required: true,
            state: Mutex::new(ConfigState::default()),
            frozen: AtomicBool::new(false),
        }
    }

    /// Load and parse a configuration document from `path` (JSON).
    pub fn load(&self, path: &str) -> Result<Configuration, ConfigError> {
        if self.frozen.load(Ordering::Acquire) {
            return Err(ConfigError::Frozen);
        }
        if !Path::new(path).exists() {
            return Err(ConfigError::FileNotFound(path.to_string()));
        }
        let bytes = std::fs::read(path).map_err(|e| ConfigError::ParseError(e.to_string()))?;
        let config: Configuration =
            serde_json::from_slice(&bytes).map_err(|e| ConfigError::ParseError(e.to_string()))?;
        let mut state = self.state.lock().expect("config state mutex poisoned");
        state.path = Some(path.to_string());
        state.config = Some(config.clone());
        Ok(config)
    }

    /// Load a configuration from an already-parsed [`Configuration`] value.
    pub fn load_value(&self, config: Configuration) -> Result<(), ConfigError> {
        if self.frozen.load(Ordering::Acquire) {
            return Err(ConfigError::Frozen);
        }
        let mut state = self.state.lock().expect("config state mutex poisoned");
        state.config = Some(config);
        Ok(())
    }

    /// Return a clone of the loaded configuration, or an error if not loaded.
    pub fn get(&self) -> Result<Configuration, ConfigError> {
        let state = self.state.lock().expect("config state mutex poisoned");
        state
            .config
            .clone()
            .ok_or(ConfigError::MissingKey("configuration".to_string()))
    }

    /// Return the path the configuration was loaded from, if any.
    pub fn path(&self) -> Option<String> {
        self.state
            .lock()
            .expect("config state mutex poisoned")
            .path
            .clone()
    }

    /// Freeze the configuration so it can no longer be mutated.
    pub fn freeze(&self) {
        self.frozen.store(true, Ordering::Release);
    }

    /// Whether the configuration is frozen (immutable).
    pub fn is_frozen(&self) -> bool {
        self.frozen.load(Ordering::Acquire)
    }
}

impl Default for ConfigService {
    fn default() -> Self {
        Self::new()
    }
}

impl ServiceContract for ConfigService {
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
        let state = self.state.lock().expect("config state mutex poisoned");
        if state.config.is_some() {
            HealthStatus::Healthy
        } else {
            HealthStatus::Degraded("configuration not loaded".to_string())
        }
    }

    fn initialize(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("config state mutex poisoned");
        if state.initialized {
            return Err(ServiceError::InvalidState("already initialized".to_string()));
        }
        state.initialized = true;
        Ok(())
    }

    fn start(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("config state mutex poisoned");
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
        let mut state = self.state.lock().expect("config state mutex poisoned");
        state.started = false;
        Ok(())
    }

    fn deinitialize(&mut self) -> Result<(), ServiceError> {
        let mut state = self.state.lock().expect("config state mutex poisoned");
        state.started = false;
        state.initialized = false;
        Ok(())
    }

    fn dispose(&mut self) {
        let mut state = self.state.lock().expect("config state mutex poisoned");
        state.config = None;
        state.path = None;
        state.initialized = false;
        state.started = false;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_load_missing_file_returns_file_not_found() {
        let svc = ConfigService::new();
        let err = svc.load("/nonexistent/path.json").unwrap_err();
        assert!(matches!(err, ConfigError::FileNotFound(_)));
    }

    #[test]
    fn test_load_valid_config() {
        let dir = std::env::temp_dir();
        let path = dir.join("atlas_config_test_valid.json");
        {
            let mut f = std::fs::File::create(&path).unwrap();
            f.write_all(
                br#"{"schema_version":"1.0","manifest_path":"manifest.json","runtime":{"health_check_interval_ms":5000}}"#,
            )
            .unwrap();
        }
        let svc = ConfigService::new();
        let config = svc.load(path.to_str().unwrap()).unwrap();
        assert_eq!(config.schema_version, "1.0");
        assert_eq!(config.runtime.health_check_interval_ms, Some(5000));
        let _ = std::fs::remove_file(&path);
    }

    #[test]
    fn test_get_before_load_errors() {
        let svc = ConfigService::new();
        assert!(svc.get().is_err());
    }

    #[test]
    fn test_freeze_prevents_mutation() {
        let svc = ConfigService::new();
        svc.load_value(Configuration::default()).unwrap();
        svc.freeze();
        assert!(svc.is_frozen());
        let err = svc.load_value(Configuration::default()).unwrap_err();
        assert!(matches!(err, ConfigError::Frozen));
    }

    #[test]
    fn test_service_contract_lifecycle() {
        let mut svc = ConfigService::new();
        assert!(!svc.health_check().is_healthy());
        svc.load_value(Configuration::default()).unwrap();
        svc.initialize().unwrap();
        svc.start().unwrap();
        assert!(svc.health_check().is_healthy());
        svc.stop().unwrap();
        svc.deinitialize().unwrap();
        svc.dispose();
        assert!(!svc.health_check().is_healthy());
    }

    #[test]
    fn test_double_initialize_rejected() {
        let mut svc = ConfigService::new();
        svc.initialize().unwrap();
        assert!(svc.initialize().is_err());
    }

    #[test]
    fn test_start_before_initialize_rejected() {
        let mut svc = ConfigService::new();
        assert!(svc.start().is_err());
    }
}
