//! Metrics recorder contract.
//!
//! Defines the abstract interface for the system diagnostic time-series
//! collector (SRV-METRICS, RFC-0003 §8) and the Health and Metrics Contract
//! (RFC-0003 §16). Every Metrics service implementation MUST satisfy this
//! contract.
//!
//! The model supports the three metric primitives referenced by the storage
//! observability model (RFC-0414) and the platform metrics catalogue:
//! - [`MetricKind::Counter`] — monotonically increasing value.
//! - [`MetricKind::Gauge`] — point-in-time value that can go up or down.
//! - [`MetricKind::Histogram`] — distribution of observations grouped into
//!   explicit buckets.

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// The kind of a registered metric.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum MetricKind {
    /// Monotonically increasing counter.
    Counter,
    /// Value that can arbitrarily increase or decrease.
    Gauge,
    /// Distribution of observed values across explicit buckets.
    Histogram,
}

/// Static descriptor for a registered metric.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MetricDescriptor {
    /// Unique metric name (e.g. `runtime.events.published`).
    pub name: String,
    /// Metric primitive kind.
    pub kind: MetricKind,
    /// Optional unit of measurement (e.g. `ms`, `bytes`, `ops`).
    pub unit: Option<String>,
    /// Human-readable description of what the metric measures.
    pub description: String,
}

/// A single histogram bucket upper bound and its cumulative count.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HistogramBucket {
    /// Inclusive upper bound of the bucket (`f64::INFINITY` for the overflow bucket).
    pub upper_bound: f64,
    /// Number of observations that fell into this bucket.
    pub count: u64,
}

/// The current value of a metric.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum MetricValue {
    /// Counter value.
    Counter(u64),
    /// Gauge value.
    Gauge(f64),
    /// Histogram aggregation: total count, sum of observations, and buckets.
    Histogram {
        count: u64,
        sum: f64,
        buckets: Vec<HistogramBucket>,
    },
}

/// A point-in-time snapshot of a single metric.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct MetricSnapshot {
    /// Descriptor of the metric.
    pub descriptor: MetricDescriptor,
    /// Current value.
    pub value: MetricValue,
    /// Monotonic timestamp (milliseconds since UNIX epoch) of the snapshot.
    pub timestamp_ms: u64,
}

/// Error from metrics operations.
#[derive(Error, Debug, Clone, PartialEq)]
pub enum MetricsError {
    /// The requested metric is not registered.
    #[error("metric not found: {0}")]
    NotFound(String),
    /// A metric with the same name is already registered.
    #[error("metric already registered: {0}")]
    AlreadyRegistered(String),
    /// An operation was attempted against a metric of the wrong kind.
    #[error("metric kind mismatch for {name}: expected {expected:?}, got {actual:?}")]
    KindMismatch {
        name: String,
        expected: MetricKind,
        actual: MetricKind,
    },
    /// A generic metric operation failure.
    #[error("metric operation failed: {0}")]
    OperationFailed(String),
}

/// The metrics recorder contract.
///
/// Implementations MUST be [`Send`] + [`Sync`] and MUST NOT use global mutable
/// state. All mutations are performed through `&self` using interior
/// mutability so that the recorder can be shared across services via
/// dependency injection.
pub trait MetricsRecorder: Send + Sync {
    /// Register a monotonically increasing counter.
    fn register_counter(&self, name: &str, description: &str) -> Result<(), MetricsError>;
    /// Register a gauge that can move up or down.
    fn register_gauge(&self, name: &str, description: &str) -> Result<(), MetricsError>;
    /// Register a histogram with the given explicit bucket upper bounds.
    fn register_histogram(
        &self,
        name: &str,
        description: &str,
        buckets: Vec<f64>,
    ) -> Result<(), MetricsError>;
    /// Increment a counter by `by`. Returns `NotFound` if unregistered or
    /// `KindMismatch` if the metric is not a counter.
    fn increment(&self, name: &str, by: u64) -> Result<(), MetricsError>;
    /// Set a gauge to `value`.
    fn set_gauge(&self, name: &str, value: f64) -> Result<(), MetricsError>;
    /// Observe a single value against a histogram.
    fn observe(&self, name: &str, value: f64) -> Result<(), MetricsError>;
    /// Return a snapshot of every registered metric.
    fn snapshot(&self) -> Vec<MetricSnapshot>;
    /// Return the descriptors of every registered metric.
    fn list_metrics(&self) -> Vec<MetricDescriptor>;
}
