//! Health Service tests.

use atlas_common::HealthStatus;
use atlas_contracts::HealthChecker;
use atlas_runtime::health::HealthService;

#[test]
fn test_health_service_empty() {
    let svc = HealthService::new();
    assert_eq!(svc.aggregate_health(), HealthStatus::Healthy);
    assert!(svc.all_health().is_empty());
}

#[test]
fn test_record_and_query_health() {
    let svc = HealthService::new();

    svc.record_health(&"svc-1".to_string(), HealthStatus::Healthy);
    svc.record_health(
        &"svc-2".to_string(),
        HealthStatus::Degraded("high cpu".to_string()),
    );

    let health = svc.all_health();
    assert_eq!(health.len(), 2);

    assert_eq!(
        svc.service_health(&"svc-1".to_string()),
        Some(HealthStatus::Healthy)
    );
    assert!(matches!(
        svc.service_health(&"svc-2".to_string()),
        Some(HealthStatus::Degraded(_))
    ));
    assert_eq!(svc.service_health(&"nonexistent".to_string()), None);
}
