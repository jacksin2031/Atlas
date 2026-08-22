//! Plugin subsystem error types.
//!
//! Defines the complete error hierarchy for the Plugin Runtime (RFC-0201,
//! RFC-0202, RFC-0203, RFC-0204, RFC-0205, RFC-0226). All plugin operations
//! surface failures through [`PluginError`], which composes the per-domain
//! error enums defined alongside each module.

use thiserror::Error;

/// Error from plugin manifest parsing or validation (RFC-0202).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum ManifestError {
    #[error("manifest validation failed: {0}")]
    ValidationError(String),
    #[error("manifest parse error: {0}")]
    ParseError(String),
    #[error("manifest file not found: {0}")]
    FileNotFound(String),
    #[error("duplicate plugin id: {0}")]
    DuplicatePluginId(String),
    #[error("incompatible: {0}")]
    Incompatible(String),
    #[error("invalid semantic version: {0}")]
    InvalidVersion(String),
    #[error("unsupported capability: {0}")]
    UnsupportedCapability(String),
}

/// Error from plugin lifecycle state machine (RFC-0203).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum LifecycleError {
    #[error("illegal plugin state transition from {from:?} to {to:?}")]
    IllegalTransition {
        from: crate::lifecycle::PluginState,
        to: crate::lifecycle::PluginState,
    },
    #[error("lifecycle operation failed for plugin {0}: {1}")]
    OperationFailed(String, String),
    #[error("plugin not in expected state: expected {expected:?}, actual {actual:?}")]
    InvalidState {
        expected: crate::lifecycle::PluginState,
        actual: crate::lifecycle::PluginState,
    },
}

/// Error from plugin dependency resolution (RFC-0226).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum DependencyError {
    #[error("version parse error: {0}")]
    VersionParse(String),
    #[error("circular dependency detected: {0}")]
    CircularDependency(String),
    #[error("missing required dependency: {0}")]
    MissingDependency(String),
    #[error("version conflict for {plugin}: required {constraint}, found {version}")]
    VersionConflict {
        plugin: String,
        constraint: String,
        version: String,
    },
    #[error("capability dependency not satisfied: plugin {0} requires capability {1}")]
    CapabilityNotSatisfied(String, String),
}

impl From<ManifestError> for DependencyError {
    fn from(e: ManifestError) -> Self {
        Self::VersionParse(e.to_string())
    }
}

/// Error from the plugin registry (RFC-0205).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum RegistryError {
    #[error("plugin already registered: {0}")]
    AlreadyRegistered(String),
    #[error("plugin not found: {0}")]
    NotFound(String),
    #[error("plugin is disabled: {0}")]
    Disabled(String),
    #[error("plugin cannot be unloaded in current state: {0}")]
    CannotUnload(String),
}

/// Error from the plugin loader (RFC-0204).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum LoaderError {
    #[error("discovery failed: {0}")]
    DiscoveryFailed(String),
    #[error("manifest invalid: {0}")]
    ManifestInvalid(String),
    #[error("dependency resolution failed: {0}")]
    DependencyResolutionFailed(String),
    #[error("activation failed for plugin {0}: {1}")]
    ActivationFailed(String, String),
    #[error("deactivation failed for plugin {0}: {1}")]
    DeactivationFailed(String, String),
    #[error("plugin provider not available for: {0}")]
    ProviderUnavailable(String),
}

/// Error from the plugin sandbox (RFC-0208).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum SandboxError {
    #[error("permission denied: {0}")]
    PermissionDenied(String),
    #[error("resource limit exceeded: {0}")]
    ResourceLimitExceeded(String),
    #[error("security validation failed: {0}")]
    SecurityValidationFailed(String),
    #[error("sandbox lifecycle violation: {0}")]
    LifecycleViolation(String),
}

/// Error from plugin configuration (RFC-0222).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum ConfigError {
    #[error("configuration validation failed: {0}")]
    ValidationError(String),
    #[error("configuration is frozen and cannot be modified")]
    Frozen,
    #[error("missing required configuration key: {0}")]
    MissingKey(String),
    #[error("invalid configuration value for {key}: {value}")]
    InvalidValue { key: String, value: String },
}

/// Error from plugin health (RFC-0210 §14).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum HealthError {
    #[error("health check failed for plugin {0}: {1}")]
    CheckFailed(String, String),
    #[error("plugin not registered for health monitoring: {0}")]
    NotMonitored(String),
}

/// Error from plugin capability registry (RFC-0206).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum CapabilityError {
    #[error("capability not registered: {0}")]
    NotRegistered(String),
    #[error("capability already registered by plugin {0}")]
    AlreadyRegistered(String),
}

/// Top-level plugin runtime error.
///
/// Composes every per-domain error so callers can handle plugin failures
/// uniformly or match on the specific domain.
#[derive(Error, Debug, Clone)]
pub enum PluginError {
    #[error("manifest error: {0}")]
    Manifest(#[from] ManifestError),
    #[error("lifecycle error: {0}")]
    Lifecycle(#[from] LifecycleError),
    #[error("dependency error: {0}")]
    Dependency(#[from] DependencyError),
    #[error("registry error: {0}")]
    Registry(#[from] RegistryError),
    #[error("loader error: {0}")]
    Loader(#[from] LoaderError),
    #[error("sandbox error: {0}")]
    Sandbox(#[from] SandboxError),
    #[error("config error: {0}")]
    Config(#[from] ConfigError),
    #[error("health error: {0}")]
    Health(#[from] HealthError),
    #[error("capability error: {0}")]
    Capability(#[from] CapabilityError),
    #[error("event bus error: {0}")]
    EventBus(#[from] atlas_common::EventBusError),
    #[error("storage error: {0}")]
    Storage(#[from] atlas_common::StorageError),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_manifest_error_display() {
        let e = ManifestError::ValidationError("bad field".to_string());
        assert!(e.to_string().contains("bad field"));
    }

    #[test]
    fn test_plugin_error_from_manifest() {
        let me = ManifestError::DuplicatePluginId("p1".to_string());
        let pe: PluginError = me.into();
        assert!(matches!(pe, PluginError::Manifest(_)));
    }

    #[test]
    fn test_dependency_error_version_conflict() {
        let e = DependencyError::VersionConflict {
            plugin: "a".to_string(),
            constraint: ">=1.0.0".to_string(),
            version: "0.9.0".to_string(),
        };
        assert!(e.to_string().contains("0.9.0"));
    }
}
