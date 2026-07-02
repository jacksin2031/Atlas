//! Service identity types.

use serde::{Deserialize, Serialize};

/// Unique service identifier (UUID).
pub type ServiceId = String;

/// Human-readable service name.
pub type ServiceName = String;

/// Service health status.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum HealthStatus {
    Healthy,
    Degraded(String),
    Unhealthy(String),
    Disabled,
}

impl HealthStatus {
    /// Check if the service is considered operational.
    pub fn is_healthy(&self) -> bool {
        matches!(self, HealthStatus::Healthy)
    }
}
