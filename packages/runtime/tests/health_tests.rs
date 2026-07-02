//! Health monitor tests.

use atlas_runtime::health::HealthMonitor;
use atlas_common::HealthStatus;
use atlas_runtime::eventbus::EventBusImpl;

#[test]
fn test_health_monitor_empty() {
    let bus = EventBusImpl::new();
    let monitor = HealthMonitor::new(&bus);
    let health = monitor.aggregate_health();
    assert!(health.is_empty());
}

#[test]
fn test_record_and_query_health() {
    let bus = EventBusImpl::new();
    let mut monitor = HealthMonitor::new(&bus);

    monitor.record_health("svc-1".to_string(), HealthStatus::Healthy);
    monitor.record_health("svc-2".to_string(), HealthStatus::Degraded("high cpu".to_string()));

    let health = monitor.aggregate_health();
    assert_eq!(health.len(), 2);

    assert_eq!(monitor.service_health("svc-1"), Some(HealthStatus::Healthy));
    assert!(matches!(monitor.service_health("svc-2"), Some(HealthStatus::Degraded(_))));
    assert_eq!(monitor.service_health("nonexistent"), None);
}
