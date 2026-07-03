//! Error type hierarchy.
//!
//! Re-exports from atlas-contracts and defines composite errors.

pub use atlas_contracts::{
    ServiceError, EventBusError, SchedulerError, StateTransitionError, MetricsError, StorageError,
};
use thiserror::Error;

/// Error from manifest operations.
#[derive(Error, Debug, PartialEq, Clone)]
pub enum ManifestError {
    #[error("validation failed: {0}")]
    ValidationError(String),
    #[error("capability unsupported: {0}")]
    CapabilityUnsupported(String),
    #[error("version mismatch: {0}")]
    VersionMismatch(String),
    #[error("parse error: {0}")]
    ParseError(String),
    #[error("file not found: {0}")]
    FileNotFound(String),
    #[error("schema error: {0}")]
    SchemaError(String),
}

/// Error from configuration operations.
#[derive(Error, Debug, PartialEq, Clone)]
pub enum ConfigError {
    #[error("parse error: {0}")]
    ParseError(String),
    #[error("file not found: {0}")]
    FileNotFound(String),
    #[error("invalid value for {key}: {value}")]
    InvalidValue { key: String, value: String },
    #[error("immutable: configuration is frozen after runtime reaches Running")]
    Frozen,
    #[error("missing required key: {0}")]
    MissingKey(String),
}

/// Error from health checks.
#[derive(Error, Debug, PartialEq, Clone)]
pub enum HealthError {
    #[error("health check failed for {0}: {1}")]
    CheckFailed(String, String),
    #[error("interval enforcement violation")]
    IntervalViolation,
    #[error("service not registered: {0}")]
    NotRegistered(String),
}

/// Error from dependency resolution.
#[derive(Error, Debug, PartialEq, Clone)]
pub enum DependencyError {
    #[error("circular dependency detected: {0}")]
    CircularDependency(String),
    #[error("missing dependency: {0}")]
    MissingDependency(String),
}

/// Top-level Atlas error enum.
#[derive(Error, Debug)]
pub enum AtlasError {
    #[error("service error: {0}")]
    Service(#[from] ServiceError),
    #[error("event bus error: {0}")]
    Event(#[from] EventBusError),
    #[error("scheduler error: {0}")]
    Scheduler(#[from] SchedulerError),
    #[error("state transition error: {0}")]
    Lifecycle(#[from] StateTransitionError),
    #[error("manifest error: {0}")]
    Manifest(#[from] ManifestError),
    #[error("config error: {0}")]
    Config(#[from] ConfigError),
    #[error("health error: {0}")]
    Health(#[from] HealthError),
    #[error("dependency error: {0}")]
    Dependency(#[from] DependencyError),
    #[error("metrics error: {0}")]
    Metrics(#[from] MetricsError),
    #[error("storage error: {0}")]
    Storage(#[from] StorageError),
}
