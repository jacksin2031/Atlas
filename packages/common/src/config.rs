//! Configuration data model.
//!
//! See RFC-0010 §9 (Standard Manifest Schema) and the configuration loader
//! contract. The [`Configuration`] type is the parsed, immutable
//! representation of a runtime configuration document. Configuration MUST be
//! immutable after the Runtime reaches the Running state (RFC-0010 §4).
//!
//! The model is intentionally a flat key/value document with strongly typed
//! sections so that business logic never depends on raw parsing details.

use serde::{Deserialize, Serialize};

/// Runtime configuration document (RFC-0010 §9).
///
/// Loaded from a JSON/TOML/YAML source and validated against the
/// configuration schema before boot. Once frozen, the document is immutable.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct Configuration {
    /// Schema version of the configuration document.
    #[serde(default)]
    pub schema_version: String,
    /// Path to the runtime manifest (RFC-0010 §12).
    #[serde(default)]
    pub manifest_path: Option<String>,
    /// Tunable runtime parameters.
    #[serde(default)]
    pub runtime: RuntimeConfig,
    /// Health-monitor tuning.
    #[serde(default)]
    pub health: HealthConfig,
    /// Scheduler tuning.
    #[serde(default)]
    pub scheduler: SchedulerConfig,
    /// Metrics tuning.
    #[serde(default)]
    pub metrics: MetricsConfig,
    /// Storage tuning.
    #[serde(default)]
    pub storage: StorageConfig,
    /// Free-form extension section for subsystem-specific keys.
    #[serde(default)]
    pub extensions: serde_json::Map<String, serde_json::Value>,
}

/// Runtime-level tuning parameters.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct RuntimeConfig {
    /// Health-check interval in milliseconds (RFC-0003 §10.1).
    #[serde(default)]
    pub health_check_interval_ms: Option<u64>,
    /// Maximum number of health-check retries before disabling a service
    /// (RFC-0003 §13).
    #[serde(default)]
    pub max_health_retries: Option<u32>,
    /// Graceful-shutdown timeout in milliseconds (RFC-0002 §32).
    #[serde(default)]
    pub shutdown_timeout_ms: Option<u64>,
}

/// Health-monitor configuration.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct HealthConfig {
    /// Periodic check interval in milliseconds.
    #[serde(default)]
    pub check_interval_ms: Option<u64>,
    /// Consecutive failures before a service is disabled.
    #[serde(default)]
    pub failure_threshold: Option<u32>,
}

/// Scheduler configuration.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct SchedulerConfig {
    /// Number of worker threads in the pool.
    #[serde(default)]
    pub worker_count: Option<u32>,
    /// Maximum queue depth before backpressure is applied.
    #[serde(default)]
    pub max_queue_depth: Option<u64>,
}

/// Metrics configuration.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct MetricsConfig {
    /// Whether the metrics service is enabled.
    #[serde(default)]
    pub enabled: Option<bool>,
    /// Default histogram bucket upper bounds.
    #[serde(default)]
    pub default_buckets: Vec<f64>,
}

/// Storage configuration.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct StorageConfig {
    /// Default provider ID to prefer for operations.
    #[serde(default)]
    pub default_provider: Option<String>,
    /// Opaque, provider-specific connection configuration.
    #[serde(default)]
    pub providers: Vec<ProviderConfig>,
}

/// Per-provider configuration block.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct ProviderConfig {
    /// Provider identifier (RFC-0403).
    pub id: String,
    /// Provider implementation type (backend-agnostic key).
    #[serde(default)]
    pub backend: String,
    /// Capabilities the provider declares (RFC-0403 §6.1).
    #[serde(default)]
    pub capabilities: Vec<String>,
    /// Opaque backend-specific options.
    #[serde(default)]
    pub options: serde_json::Map<String, serde_json::Value>,
}
