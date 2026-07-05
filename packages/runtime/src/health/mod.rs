//! Health Service.
//!
//! Implements the Runtime Service Contract (RFC-0003 §9) and the
//! [`HealthChecker`] contract (RFC-0003 §16) for health monitoring.
//!
//! Responsibilities:
//! - Record per-service health status.
//! - Aggregate overall runtime health (worst-case semantics).
//! - Enforce degradation escalation: a service that fails its health check
//!   repeatedly is escalated to `Disabled` after `failure_threshold`
//!   consecutive failures (RFC-0003 §13: Degraded → Disabled after max
//!   retries).
//! - Expose the configured health-check interval (RFC-0003 §10.1).
//!
//! The service uses interior mutability so it is [`Send`] + [`Sync`] and can be
//! shared via dependency injection without global mutable state.

use atlas_common::HealthStatus;
use atlas_contracts::{HealthChecker, ServiceContract, ServiceError, ServiceId, ServiceName};
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;

/// Stable service identifier for the Health Service.
pub const SERVICE_ID: &str = "srv-health";

/// Default consecutive-failure threshold before a service is disabled.
pub const DEFAULT_FAILURE_THRESHOLD: u32 = 3;
/// Default health-check interval in milliseconds (RFC-0003 §10.1).
pub const DEFAULT_CHECK_INTERVAL_MS: u64 = 5000;

/// Health Service — monitors and aggregates service health.
pub struct HealthService {
    id: ServiceId,
    name: ServiceName,
    dependencies: Vec<ServiceId>,
    priority: u8,
    required: bool,
    health_map: Mutex<HashMap<String, HealthStatus>>,
    failure_counts: Mutex<HashMap<String, u32>>,
    failure_threshold: u32,
    check_interval_ms: u64,
    initialized: AtomicBool,
    started: AtomicBool,
}

impl HealthService {
    /// Create a new Health Service with default tuning.
    pub fn new() -> Self {
        Self::with_config(DEFAULT_FAILURE_THRESHOLD, DEFAULT_CHECK_INTERVAL_MS)
    }

    /// Create a new Health Service with explicit tuning.
    pub fn with_config(failure_threshold: u32, check_interval_ms: u64) -> Self {
        Self {
            id: SERVICE_ID.to_string(),
            name: "Health Service".to_string(),
            dependencies: Vec::new(),
            priority: 0,
            required: true,
            health_map: Mutex::new(HashMap::new()),
            failure_counts: Mutex::new(HashMap::new()),
            failure_threshold,
            check_interval_ms,
            initialized: AtomicBool::new(false),
            started: AtomicBool::new(false),
        }
    }

    /// The configured consecutive-failure threshold.
    pub fn failure_threshold(&self) -> u32 {
        self.failure_threshold
    }

    /// The configured health-check interval in milliseconds.
    pub fn check_interval_ms(&self) -> u64 {
        self.check_interval_ms
    }

    /// Return all recorded health entries as `(service_id, status)` pairs.
    pub fn all_health(&self) -> Vec<(String, HealthStatus)> {
        self.health_map
            .lock()
            .expect("health map mutex poisoned")
            .iter()
            .map(|(id, status)| (id.clone(), status.clone()))
            .collect()
    }
}

impl Default for HealthService {
    fn default() -> Self {
        Self::new()
    }
}

impl HealthChecker for HealthService {
    fn aggregate_health(&self) -> HealthStatus {
        let map = self.health_map.lock().expect("health map mutex poisoned");
        let mut has_degraded = false;
        for status in map.values() {
            match status {
                HealthStatus::Unhealthy(_) => {
                    return HealthStatus::Unhealthy("at least one service unhealthy".to_string());
                }
                HealthStatus::Disabled => {
                    return HealthStatus::Unhealthy("at least one service disabled".to_string());
                }
                HealthStatus::Degraded(_) => has_degraded = true,
                HealthStatus::Healthy => {}
            }
        }
        if has_degraded {
            HealthStatus::Degraded("at least one service degraded".to_string())
        } else {
            HealthStatus::Healthy
        }
    }

    fn service_health(&self, service_id: &ServiceId) -> Option<HealthStatus> {
        self.health_map
            .lock()
            .expect("health map mutex poisoned")
            .get(service_id)
            .cloned()
    }

    fn record_health(&self, service_id: &ServiceId, status: HealthStatus) {
        let mut map = self.health_map.lock().expect("health map mutex poisoned");
        let mut counts = self
            .failure_counts
            .lock()
            .expect("failure counts mutex poisoned");
        match &status {
            HealthStatus::Healthy => {
                counts.remove(service_id);
                map.insert(service_id.clone(), status);
            }
            HealthStatus::Degraded(_) | HealthStatus::Unhealthy(_) => {
                let count = counts.entry(service_id.clone()).or_insert(0);
                *count += 1;
                if *count >= self.failure_threshold {
                    map.insert(service_id.clone(), HealthStatus::Disabled);
                    counts.remove(service_id);
                } else {
                    map.insert(service_id.clone(), status);
                }
            }
            HealthStatus::Disabled => {
                counts.remove(service_id);
                map.insert(service_id.clone(), status);
            }
        }
    }
}

impl ServiceContract for HealthService {
    fn id(&self) -> &ServiceId {
        &self.id
    }

    fn name(&self) -> &ServiceName {
        &self.name
    }

    fn dependencies(&self) -> &[ServiceId] {
        &self.dependencies
    }

    fn priority(&self) -> u8 {
        self.priority
    }

    fn required(&self) -> bool {
        self.required
    }

    fn health_check(&self) -> HealthStatus {
        if self.initialized.load(Ordering::Acquire) {
            HealthStatus::Healthy
        } else {
            HealthStatus::Degraded("health service not initialized".to_string())
        }
    }

    fn initialize(&mut self) -> Result<(), ServiceError> {
        if self.initialized.swap(true, Ordering::AcqRel) {
            return Err(ServiceError::InvalidState(
                "already initialized".to_string(),
            ));
        }
        Ok(())
    }

    fn start(&mut self) -> Result<(), ServiceError> {
        if !self.initialized.load(Ordering::Acquire) {
            return Err(ServiceError::InvalidState("not initialized".to_string()));
        }
        self.started.store(true, Ordering::Release);
        Ok(())
    }

    fn pause(&mut self) -> Result<(), ServiceError> {
        Ok(())
    }

    fn resume(&mut self) -> Result<(), ServiceError> {
        Ok(())
    }

    fn stop(&mut self) -> Result<(), ServiceError> {
        self.started.store(false, Ordering::Release);
        Ok(())
    }

    fn deinitialize(&mut self) -> Result<(), ServiceError> {
        self.started.store(false, Ordering::Release);
        self.initialized.store(false, Ordering::Release);
        Ok(())
    }

    fn dispose(&mut self) {
        self.started.store(false, Ordering::Release);
        self.initialized.store(false, Ordering::Release);
        self.health_map
            .lock()
            .expect("health map mutex poisoned")
            .clear();
        self.failure_counts
            .lock()
            .expect("failure counts mutex poisoned")
            .clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_aggregate_is_healthy() {
        let svc = HealthService::new();
        assert_eq!(svc.aggregate_health(), HealthStatus::Healthy);
    }

    #[test]
    fn test_record_and_query_health() {
        let svc = HealthService::new();
        svc.record_health(&"svc-1".to_string(), HealthStatus::Healthy);
        svc.record_health(
            &"svc-2".to_string(),
            HealthStatus::Degraded("high cpu".to_string()),
        );
        assert_eq!(
            svc.service_health(&"svc-1".to_string()),
            Some(HealthStatus::Healthy)
        );
        assert!(matches!(
            svc.service_health(&"svc-2".to_string()),
            Some(HealthStatus::Degraded(_))
        ));
        assert_eq!(svc.all_health().len(), 2);
    }

    #[test]
    fn test_aggregate_worst_case() {
        let svc = HealthService::new();
        svc.record_health(&"a".to_string(), HealthStatus::Healthy);
        svc.record_health(&"b".to_string(), HealthStatus::Degraded("slow".to_string()));
        assert!(matches!(svc.aggregate_health(), HealthStatus::Degraded(_)));

        svc.record_health(
            &"c".to_string(),
            HealthStatus::Unhealthy("down".to_string()),
        );
        assert!(matches!(svc.aggregate_health(), HealthStatus::Unhealthy(_)));
    }

    #[test]
    fn test_degradation_escalation_to_disabled() {
        let svc = HealthService::with_config(2, 1000);
        svc.record_health(
            &"flaky".to_string(),
            HealthStatus::Degraded("retry 1".to_string()),
        );
        assert!(matches!(
            svc.service_health(&"flaky".to_string()),
            Some(HealthStatus::Degraded(_))
        ));
        svc.record_health(
            &"flaky".to_string(),
            HealthStatus::Degraded("retry 2".to_string()),
        );
        assert_eq!(
            svc.service_health(&"flaky".to_string()),
            Some(HealthStatus::Disabled)
        );
    }

    #[test]
    fn test_healthy_resets_failure_count() {
        let svc = HealthService::with_config(3, 1000);
        svc.record_health(
            &"svc".to_string(),
            HealthStatus::Degraded("once".to_string()),
        );
        svc.record_health(&"svc".to_string(), HealthStatus::Healthy);
        svc.record_health(
            &"svc".to_string(),
            HealthStatus::Degraded("again".to_string()),
        );
        assert!(matches!(
            svc.service_health(&"svc".to_string()),
            Some(HealthStatus::Degraded(_))
        ));
    }

    #[test]
    fn test_unhealthy_aggregates_to_unhealthy() {
        let svc = HealthService::new();
        svc.record_health(&"x".to_string(), HealthStatus::Healthy);
        svc.record_health(&"y".to_string(), HealthStatus::Disabled);
        assert!(matches!(svc.aggregate_health(), HealthStatus::Unhealthy(_)));
    }

    #[test]
    fn test_service_contract_lifecycle() {
        let mut svc = HealthService::new();
        svc.initialize().unwrap();
        svc.start().unwrap();
        assert!(svc.health_check().is_healthy());
        svc.stop().unwrap();
        svc.deinitialize().unwrap();
        svc.dispose();
        assert!(svc.all_health().is_empty());
    }

    #[test]
    fn test_interval_and_threshold_config() {
        let svc = HealthService::with_config(5, 2000);
        assert_eq!(svc.failure_threshold(), 5);
        assert_eq!(svc.check_interval_ms(), 2000);
    }
}
