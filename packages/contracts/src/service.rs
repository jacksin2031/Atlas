//! Service contract trait.
//!
//! Every service registered with the Service Registry MUST implement this trait.
//! See RFC-0003 §9 (Service Lifecycle Contracts).

use serde::{Deserialize, Serialize};

/// Unique service identifier.
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

/// Error from service operations.
#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum ServiceError {
    #[error("service not found: {0}")]
    NotFound(String),
    #[error("duplicate registration: {0}")]
    DuplicateRegistration(String),
    #[error("initialization failed: {0}")]
    InitializationFailed(String),
    #[error("deinitialization failed: {0}")]
    DeinitializationFailed(String),
    #[error("service is not in the expected state: {0}")]
    InvalidState(String),
}

/// The lifecycle contract that every service must implement.
pub trait ServiceContract: Send + Sync {
    fn id(&self) -> &ServiceId;
    fn name(&self) -> &ServiceName;
    fn dependencies(&self) -> &[ServiceId];
    fn priority(&self) -> u8;
    fn required(&self) -> bool;
    fn health_check(&self) -> HealthStatus;
    fn initialize(&mut self) -> Result<(), ServiceError>;
    fn start(&mut self) -> Result<(), ServiceError>;
    fn pause(&mut self) -> Result<(), ServiceError>;
    fn resume(&mut self) -> Result<(), ServiceError>;
    fn stop(&mut self) -> Result<(), ServiceError>;
    fn deinitialize(&mut self) -> Result<(), ServiceError>;
    fn dispose(&mut self);
}
