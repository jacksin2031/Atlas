//! Health checker trait definitions.
//!
//! See RFC-0003 §16 (Health and Metrics Contract).

use crate::service::{HealthStatus, ServiceId};

/// Health checker interface.
pub trait HealthChecker: Send + Sync {
    fn aggregate_health(&self) -> HealthStatus;
    fn service_health(&self, service_id: &ServiceId) -> Option<HealthStatus>;
    fn record_health(&self, service_id: &ServiceId, status: HealthStatus);
}
