//! Tests for service types.

use atlas_contracts::{HealthStatus, ServiceError};

#[test]
fn test_health_status_is_healthy() {
    assert!(HealthStatus::Healthy.is_healthy());
    assert!(!HealthStatus::Degraded("slow".to_string()).is_healthy());
    assert!(!HealthStatus::Unhealthy("crashed".to_string()).is_healthy());
    assert!(!HealthStatus::Disabled.is_healthy());
}

#[test]
fn test_service_errors_display() {
    let err = ServiceError::NotFound("svc1".to_string());
    assert!(format!("{}", err).contains("svc1"));

    let err = ServiceError::DuplicateRegistration("svc2".to_string());
    assert!(format!("{}", err).contains("svc2"));
}
