//! Plugin manifest model, parsing, validation, and compatibility checking
//! (RFC-0202).
//!
//! The manifest is the declarative definition of a plugin: metadata,
//! capabilities, dependencies, permissions, compatibility, and resource
//! limits. Parsing and validation are **independent of plugin execution**
//! (RFC-0202 §1): this module never instantiates plugins.
//!
//! Once validated, a manifest is immutable. Compatibility checking against the
//! runtime version and API version is performed before loading (RFC-0218 §17).

use crate::capability::{CapabilityDeclaration, PluginCapability};
use crate::error::ManifestError;
use crate::version::{SemanticVersion, VersionConstraint};
use serde::{Deserialize, Serialize};
use std::fmt;

/// Maximum permitted length of `plugin_name` (AC-0202-003).
pub const MAX_PLUGIN_NAME_LEN: usize = 256;

/// The primary role a plugin fulfils (RFC-0202, `PT-` prefixed types).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Default)]
pub enum PluginType {
    #[default]
    Extension,
    Service,
    Provider,
    Agent,
    Tool,
    Theme,
    Driver,
    Integration,
    #[serde(untagged)]
    Custom(String),
}

impl fmt::Display for PluginType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Extension => write!(f, "extension"),
            Self::Service => write!(f, "service"),
            Self::Provider => write!(f, "provider"),
            Self::Agent => write!(f, "agent"),
            Self::Tool => write!(f, "tool"),
            Self::Theme => write!(f, "theme"),
            Self::Driver => write!(f, "driver"),
            Self::Integration => write!(f, "integration"),
            Self::Custom(name) => write!(f, "{name}"),
        }
    }
}

/// Six discrete permission levels (RFC-0219 §9), ordered least to most
/// privileged. The sandbox maps each level to an isolation boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize, Default)]
pub enum PermissionLevel {
    Restricted,
    Low,
    #[default]
    Normal,
    Elevated,
    Privileged,
    Trusted,
}

/// A declared permission (RFC-0219 §10).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PluginPermission {
    pub name: String,
    pub level: PermissionLevel,
    #[serde(default)]
    pub required: bool,
}

/// The strength of a plugin dependency (RFC-0226 §9).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
pub enum DependencyType {
    /// Hard dependency: plugin fails to load if missing or incompatible.
    #[default]
    Required,
    /// Optional dependency: plugin loads without it; presence improves function.
    Optional,
    /// Soft dependency: plugin loads with degraded function if missing.
    Soft,
}

/// A declared plugin dependency (RFC-0226).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PluginDependency {
    pub plugin_id: String,
    pub version: String,
    #[serde(default)]
    pub dependency_type: DependencyType,
    #[serde(default)]
    pub capability: Option<PluginCapability>,
}

/// Runtime/API compatibility range (RFC-0218, RFC-0202).
#[derive(Debug, Clone, PartialEq, Eq, Default, Serialize, Deserialize)]
pub struct PluginCompatibility {
    #[serde(default)]
    pub minimum_runtime_version: Option<String>,
    #[serde(default)]
    pub maximum_runtime_version: Option<String>,
    #[serde(default)]
    pub api_version: Option<String>,
}

/// Resource limits declared by a plugin (RFC-0208 §11, RFC-0221).
#[derive(Debug, Clone, PartialEq, Eq, Default, Serialize, Deserialize)]
pub struct PluginResourceLimits {
    #[serde(default)]
    pub max_memory_mb: Option<u64>,
    #[serde(default)]
    pub max_cpu_cores: Option<u32>,
    #[serde(default)]
    pub max_vram_mb: Option<u64>,
    #[serde(default)]
    pub max_filesystem_mb: Option<u64>,
    #[serde(default)]
    pub max_threads: Option<u32>,
    #[serde(default)]
    pub timeout_ms: Option<u64>,
}

/// The plugin manifest (RFC-0202).
///
/// Parsed and validated independently of execution. Stored as an immutable
/// value once validated.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct PluginManifest {
    /// Manifest schema version, matching the pattern MAJOR.MINOR.PATCH (AC-0202-001).
    pub manifest_version: String,
    /// Globally-unique plugin identifier (AC-0202-002).
    pub plugin_id: String,
    /// Human-readable name, at most 256 characters (AC-0202-003).
    pub plugin_name: String,
    /// Plugin semantic version, SemVer 2.0.0 (AC-0202-004).
    pub version: String,
    #[serde(default)]
    pub description: String,
    #[serde(default)]
    pub author: String,
    /// SPDX identifier or non-empty license text (AC-0202-005).
    #[serde(default)]
    pub license: String,
    #[serde(default)]
    pub plugin_type: PluginType,
    /// Entry point identifier resolved by the plugin provider.
    #[serde(default)]
    pub entry_point: String,
    #[serde(default)]
    pub capabilities: Vec<CapabilityDeclaration>,
    #[serde(default)]
    pub dependencies: Vec<PluginDependency>,
    #[serde(default)]
    pub permissions: Vec<PluginPermission>,
    #[serde(default)]
    pub compatibility: PluginCompatibility,
    #[serde(default)]
    pub resource_limits: PluginResourceLimits,
}

impl PluginManifest {
    /// Parse a manifest from a JSON string and validate it.
    pub fn from_json(json: &str) -> Result<Self, ManifestError> {
        let manifest: PluginManifest =
            serde_json::from_str(json).map_err(|e| ManifestError::ParseError(e.to_string()))?;
        manifest.validate()?;
        Ok(manifest)
    }

    /// Parsed semantic version of the plugin.
    pub fn semantic_version(&self) -> SemanticVersion {
        SemanticVersion::parse(&self.version).unwrap_or(SemanticVersion {
            major: 0,
            minor: 0,
            patch: 0,
            pre_release: None,
            build_metadata: None,
        })
    }

    /// The capability identifiers this plugin provides (enabled only).
    pub fn provided_capabilities(&self) -> Vec<PluginCapability> {
        self.capabilities
            .iter()
            .filter(|d| d.enabled)
            .map(|d| d.capability.clone())
            .collect()
    }

    /// Build the immutable [`PluginMetadata`] view of this manifest.
    pub fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            id: self.plugin_id.clone(),
            name: self.plugin_name.clone(),
            version: self.version.clone(),
            description: self.description.clone(),
            author: self.author.clone(),
            license: self.license.clone(),
            plugin_type: self.plugin_type.clone(),
            entry_point: self.entry_point.clone(),
        }
    }
}

fn is_dotted_triple(s: &str) -> bool {
    let parts: Vec<&str> = s.split('.').collect();
    parts.len() == 3
        && parts
            .iter()
            .all(|p| !p.is_empty() && p.chars().all(|c| c.is_ascii_digit()))
}

/// Immutable plugin metadata view (RFC-0209 PluginMetadata).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PluginMetadata {
    pub id: String,
    pub name: String,
    pub version: String,
    pub description: String,
    pub author: String,
    pub license: String,
    pub plugin_type: PluginType,
    pub entry_point: String,
}

impl PluginManifest {
    /// Validate the manifest against RFC-0202 acceptance criteria.
    pub fn validate(&self) -> Result<(), ManifestError> {
        if !is_dotted_triple(&self.manifest_version) {
            return Err(ManifestError::ValidationError(format!(
                "manifest_version must be MAJOR.MINOR.PATCH: '{}'",
                self.manifest_version
            )));
        }
        if self.plugin_id.trim().is_empty() {
            return Err(ManifestError::ValidationError(
                "plugin_id must not be empty".to_string(),
            ));
        }
        if self.plugin_name.chars().count() > MAX_PLUGIN_NAME_LEN {
            return Err(ManifestError::ValidationError(format!(
                "plugin_name must not exceed {MAX_PLUGIN_NAME_LEN} characters"
            )));
        }
        let _ = SemanticVersion::parse(&self.version)?;
        if self.license.trim().is_empty() {
            return Err(ManifestError::ValidationError(
                "license must not be empty".to_string(),
            ));
        }
        // No duplicate capabilities.
        let mut seen: Vec<&PluginCapability> = Vec::new();
        for decl in &self.capabilities {
            if seen.contains(&&decl.capability) {
                return Err(ManifestError::ValidationError(format!(
                    "duplicate capability '{}' in manifest",
                    decl.capability
                )));
            }
            seen.push(&decl.capability);
        }
        // No duplicate / empty / self dependencies; constraints must parse.
        let mut dep_ids: Vec<&str> = Vec::new();
        for dep in &self.dependencies {
            if dep.plugin_id.trim().is_empty() {
                return Err(ManifestError::ValidationError(
                    "dependency plugin_id must not be empty".to_string(),
                ));
            }
            let _ = VersionConstraint::parse(&dep.version)?;
            if dep_ids.contains(&dep.plugin_id.as_str()) {
                return Err(ManifestError::ValidationError(format!(
                    "duplicate dependency '{}'",
                    dep.plugin_id
                )));
            }
            dep_ids.push(dep.plugin_id.as_str());
        }
        if self
            .dependencies
            .iter()
            .any(|d| d.plugin_id == self.plugin_id)
        {
            return Err(ManifestError::ValidationError(format!(
                "plugin '{}' depends on itself",
                self.plugin_id
            )));
        }
        Ok(())
    }

    /// Check compatibility against the runtime version and API version
    /// (RFC-0218 §17). Returns `Ok(())` if compatible.
    pub fn check_compatibility(
        &self,
        runtime_version: &SemanticVersion,
        api_version: &SemanticVersion,
    ) -> Result<(), ManifestError> {
        if let Some(min) = &self.compatibility.minimum_runtime_version {
            let min = SemanticVersion::parse(min)?;
            if runtime_version < &min {
                return Err(ManifestError::Incompatible(format!(
                    "runtime {} below minimum {}",
                    runtime_version, min
                )));
            }
        }
        if let Some(max) = &self.compatibility.maximum_runtime_version {
            let max = SemanticVersion::parse(max)?;
            if runtime_version > &max {
                return Err(ManifestError::Incompatible(format!(
                    "runtime {} above maximum {}",
                    runtime_version, max
                )));
            }
        }
        if let Some(req_api) = &self.compatibility.api_version {
            let req = SemanticVersion::parse(req_api)?;
            if !api_version.is_compatible_with(&req) {
                return Err(ManifestError::Incompatible(format!(
                    "api version {} incompatible with required {}",
                    api_version, req
                )));
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn valid_manifest() -> PluginManifest {
        PluginManifest {
            manifest_version: "1.0.0".to_string(),
            plugin_id: "com.atlas.vision".to_string(),
            plugin_name: "Vision Plugin".to_string(),
            version: "1.2.3".to_string(),
            description: "desc".to_string(),
            author: "Atlas".to_string(),
            license: "MIT".to_string(),
            plugin_type: PluginType::Extension,
            entry_point: "main".to_string(),
            capabilities: vec![CapabilityDeclaration::new(PluginCapability::Vision)],
            dependencies: vec![PluginDependency {
                plugin_id: "com.atlas.storage".to_string(),
                version: "^1.0.0".to_string(),
                dependency_type: DependencyType::Required,
                capability: None,
            }],
            permissions: vec![PluginPermission {
                name: "screen.capture".to_string(),
                level: PermissionLevel::Normal,
                required: true,
            }],
            compatibility: PluginCompatibility {
                minimum_runtime_version: Some("1.0.0".to_string()),
                maximum_runtime_version: None,
                api_version: Some("1.0.0".to_string()),
            },
            resource_limits: PluginResourceLimits::default(),
        }
    }

    #[test]
    fn test_valid_manifest_passes() {
        assert!(valid_manifest().validate().is_ok());
    }

    #[test]
    fn test_rejects_bad_manifest_version() {
        let mut m = valid_manifest();
        m.manifest_version = "1.0".to_string();
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_empty_plugin_id() {
        let mut m = valid_manifest();
        m.plugin_id = "  ".to_string();
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_long_plugin_name() {
        let mut m = valid_manifest();
        m.plugin_name = "x".repeat(MAX_PLUGIN_NAME_LEN + 1);
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_bad_semver() {
        let mut m = valid_manifest();
        m.version = "1.2".to_string();
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_accepts_pre_release_version() {
        let mut m = valid_manifest();
        m.version = "1.0.0-beta".to_string();
        assert!(m.validate().is_ok());
    }

    #[test]
    fn test_rejects_empty_license() {
        let mut m = valid_manifest();
        m.license = "".to_string();
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_duplicate_capability() {
        let mut m = valid_manifest();
        m.capabilities
            .push(CapabilityDeclaration::new(PluginCapability::Vision));
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_duplicate_dependency() {
        let mut m = valid_manifest();
        m.dependencies.push(PluginDependency {
            plugin_id: "com.atlas.storage".to_string(),
            version: "^1.0.0".to_string(),
            dependency_type: DependencyType::Required,
            capability: None,
        });
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_rejects_self_dependency() {
        let mut m = valid_manifest();
        m.dependencies.push(PluginDependency {
            plugin_id: m.plugin_id.clone(),
            version: "*".to_string(),
            dependency_type: DependencyType::Optional,
            capability: None,
        });
        assert!(m.validate().is_err());
    }

    #[test]
    fn test_compatibility_passes() {
        let m = valid_manifest();
        let rt = SemanticVersion::parse("1.5.0").unwrap();
        let api = SemanticVersion::parse("1.0.0").unwrap();
        assert!(m.check_compatibility(&rt, &api).is_ok());
    }

    #[test]
    fn test_compatibility_rejects_below_min() {
        let m = valid_manifest();
        let rt = SemanticVersion::parse("0.9.0").unwrap();
        let api = SemanticVersion::parse("1.0.0").unwrap();
        assert!(m.check_compatibility(&rt, &api).is_err());
    }

    #[test]
    fn test_compatibility_rejects_api_mismatch() {
        let m = valid_manifest();
        let rt = SemanticVersion::parse("1.5.0").unwrap();
        let api = SemanticVersion::parse("2.0.0").unwrap();
        assert!(m.check_compatibility(&rt, &api).is_err());
    }

    #[test]
    fn test_from_json_valid() {
        let json = r#"{
            "manifest_version":"1.0.0","plugin_id":"p1","plugin_name":"P1",
            "version":"1.0.0","license":"MIT","entry_point":"main"
        }"#;
        let m = PluginManifest::from_json(json).unwrap();
        assert_eq!(m.plugin_id, "p1");
        assert!(m.capabilities.is_empty());
    }

    #[test]
    fn test_from_json_invalid() {
        let json = r#"{"manifest_version":"1.0","plugin_id":"p1","plugin_name":"P1","version":"1.0.0","license":"MIT"}"#;
        assert!(PluginManifest::from_json(json).is_err());
    }

    #[test]
    fn test_metadata_and_capabilities() {
        let m = valid_manifest();
        let md = m.metadata();
        assert_eq!(md.id, m.plugin_id);
        assert_eq!(m.provided_capabilities(), vec![PluginCapability::Vision]);
    }
}
