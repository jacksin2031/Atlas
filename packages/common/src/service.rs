//! Service identity types.

/// Unique service identifier (UUID).
pub type ServiceId = String;

/// Human-readable service name.
pub type ServiceName = String;

/// Service health status — re-exported from `atlas-contracts` so that
/// `atlas_common::HealthStatus` and `atlas_contracts::HealthStatus` are the
/// same type, satisfying the `ServiceContract` and `HealthChecker` traits.
pub use atlas_contracts::HealthStatus;
