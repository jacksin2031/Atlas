//! Metrics Service.
//!
//! Implements the Runtime Service Contract (RFC-0003 §9) and the
//! [`MetricsRecorder`] contract (RFC-0003 §16) for the system diagnostic
//! time-series collector (SRV-METRICS).
//!
//! Supports counters, gauges, and histograms with explicit buckets. The
//! service uses interior mutability so it is [`Send`] + [`Sync`] and can be
//! shared via dependency injection without global mutable state.

use atlas_common::{
    HealthStatus, HistogramBucket, MetricDescriptor, MetricKind, MetricSnapshot, MetricValue,
    MetricsError, MetricsRecorder,
};
use atlas_contracts::{ServiceContract, ServiceError, ServiceId, ServiceName};
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use std::time::{SystemTime, UNIX_EPOCH};

/// Stable service identifier for the Metrics Service.
pub const SERVICE_ID: &str = "srv-metrics";

/// A stored metric: its descriptor plus current value.
struct StoredMetric {
    descriptor: MetricDescriptor,
    value: MetricValue,
}

fn now_ms() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_millis() as u64
}

/// Metrics Service — collects and exports runtime metrics.
pub struct MetricsService {
    id: ServiceId,
    name: ServiceName,
    dependencies: Vec<ServiceId>,
    priority: u8,
    required: bool,
    metrics: Mutex<HashMap<String, StoredMetric>>,
    initialized: AtomicBool,
    started: AtomicBool,
}

impl MetricsService {
    /// Create a new, uninitialised Metrics Service.
    pub fn new() -> Self {
        Self {
            id: SERVICE_ID.to_string(),
            name: "Metrics Service".to_string(),
            dependencies: Vec::new(),
            priority: 0,
            required: false,
            metrics: Mutex::new(HashMap::new()),
            initialized: AtomicBool::new(false),
            started: AtomicBool::new(false),
        }
    }
}

impl Default for MetricsService {
    fn default() -> Self {
        Self::new()
    }
}

impl MetricsRecorder for MetricsService {
    fn register_counter(&self, name: &str, description: &str) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        if metrics.contains_key(name) {
            return Err(MetricsError::AlreadyRegistered(name.to_string()));
        }
        metrics.insert(
            name.to_string(),
            StoredMetric {
                descriptor: MetricDescriptor {
                    name: name.to_string(),
                    kind: MetricKind::Counter,
                    unit: None,
                    description: description.to_string(),
                },
                value: MetricValue::Counter(0),
            },
        );
        Ok(())
    }

    fn register_gauge(&self, name: &str, description: &str) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        if metrics.contains_key(name) {
            return Err(MetricsError::AlreadyRegistered(name.to_string()));
        }
        metrics.insert(
            name.to_string(),
            StoredMetric {
                descriptor: MetricDescriptor {
                    name: name.to_string(),
                    kind: MetricKind::Gauge,
                    unit: None,
                    description: description.to_string(),
                },
                value: MetricValue::Gauge(0.0),
            },
        );
        Ok(())
    }

    fn register_histogram(
        &self,
        name: &str,
        description: &str,
        buckets: Vec<f64>,
    ) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        if metrics.contains_key(name) {
            return Err(MetricsError::AlreadyRegistered(name.to_string()));
        }
        let mut hist_buckets: Vec<HistogramBucket> = buckets
            .into_iter()
            .map(|ub| HistogramBucket {
                upper_bound: ub,
                count: 0,
            })
            .collect();
        hist_buckets.sort_by(|a, b| {
            a.upper_bound
                .partial_cmp(&b.upper_bound)
                .unwrap_or(std::cmp::Ordering::Equal)
        });
        // Append the overflow bucket.
        hist_buckets.push(HistogramBucket {
            upper_bound: f64::INFINITY,
            count: 0,
        });
        metrics.insert(
            name.to_string(),
            StoredMetric {
                descriptor: MetricDescriptor {
                    name: name.to_string(),
                    kind: MetricKind::Histogram,
                    unit: None,
                    description: description.to_string(),
                },
                value: MetricValue::Histogram {
                    count: 0,
                    sum: 0.0,
                    buckets: hist_buckets,
                },
            },
        );
        Ok(())
    }

    fn increment(&self, name: &str, by: u64) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        let entry = metrics
            .get_mut(name)
            .ok_or(MetricsError::NotFound(name.to_string()))?;
        match &mut entry.value {
            MetricValue::Counter(v) => {
                *v = v.saturating_add(by);
                Ok(())
            }
            other => Err(MetricsError::KindMismatch {
                name: name.to_string(),
                expected: MetricKind::Counter,
                actual: metric_kind_of(other),
            }),
        }
    }

    fn set_gauge(&self, name: &str, value: f64) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        let entry = metrics
            .get_mut(name)
            .ok_or(MetricsError::NotFound(name.to_string()))?;
        match &mut entry.value {
            MetricValue::Gauge(v) => {
                *v = value;
                Ok(())
            }
            other => Err(MetricsError::KindMismatch {
                name: name.to_string(),
                expected: MetricKind::Gauge,
                actual: metric_kind_of(other),
            }),
        }
    }

    fn observe(&self, name: &str, value: f64) -> Result<(), MetricsError> {
        let mut metrics = self.metrics.lock().expect("metrics mutex poisoned");
        let entry = metrics
            .get_mut(name)
            .ok_or(MetricsError::NotFound(name.to_string()))?;
        match &mut entry.value {
            MetricValue::Histogram {
                count,
                sum,
                buckets,
            } => {
                *count += 1;
                *sum += value;
                for b in buckets.iter_mut() {
                    if value <= b.upper_bound {
                        b.count += 1;
                    }
                }
                Ok(())
            }
            other => Err(MetricsError::KindMismatch {
                name: name.to_string(),
                expected: MetricKind::Histogram,
                actual: metric_kind_of(other),
            }),
        }
    }

    fn snapshot(&self) -> Vec<MetricSnapshot> {
        let metrics = self.metrics.lock().expect("metrics mutex poisoned");
        let ts = now_ms();
        metrics
            .values()
            .map(|m| MetricSnapshot {
                descriptor: m.descriptor.clone(),
                value: m.value.clone(),
                timestamp_ms: ts,
            })
            .collect()
    }

    fn list_metrics(&self) -> Vec<MetricDescriptor> {
        let metrics = self.metrics.lock().expect("metrics mutex poisoned");
        metrics.values().map(|m| m.descriptor.clone()).collect()
    }
}

fn metric_kind_of(value: &MetricValue) -> MetricKind {
    match value {
        MetricValue::Counter(_) => MetricKind::Counter,
        MetricValue::Gauge(_) => MetricKind::Gauge,
        MetricValue::Histogram { .. } => MetricKind::Histogram,
    }
}

impl ServiceContract for MetricsService {
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
            HealthStatus::Degraded("metrics service not initialized".to_string())
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
        self.metrics.lock().expect("metrics mutex poisoned").clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_counter_register_and_increment() {
        let svc = MetricsService::new();
        svc.register_counter("events.total", "total events")
            .unwrap();
        svc.increment("events.total", 5).unwrap();
        svc.increment("events.total", 3).unwrap();
        let snap = svc.snapshot();
        assert_eq!(snap.len(), 1);
        match &snap[0].value {
            MetricValue::Counter(v) => assert_eq!(*v, 8),
            _ => panic!("expected counter"),
        }
    }

    #[test]
    fn test_gauge_register_and_set() {
        let svc = MetricsService::new();
        svc.register_gauge("cpu.usage", "cpu usage").unwrap();
        svc.set_gauge("cpu.usage", 0.75).unwrap();
        let snap = svc.snapshot();
        match &snap[0].value {
            MetricValue::Gauge(v) => assert!((v - 0.75).abs() < f64::EPSILON),
            _ => panic!("expected gauge"),
        }
    }

    #[test]
    fn test_histogram_observe_buckets() {
        let svc = MetricsService::new();
        svc.register_histogram("latency", "request latency", vec![0.1, 0.5, 1.0])
            .unwrap();
        svc.observe("latency", 0.05).unwrap();
        svc.observe("latency", 0.3).unwrap();
        svc.observe("latency", 2.0).unwrap();
        let snap = svc.snapshot();
        match &snap[0].value {
            MetricValue::Histogram {
                count,
                sum,
                buckets,
            } => {
                assert_eq!(*count, 3);
                assert!((sum - 2.35).abs() < 1e-9);
                // bucket <=0.1: 1 observation (0.05)
                assert_eq!(buckets[0].count, 1);
                // bucket <=0.5: 2 observations (0.05, 0.3)
                assert_eq!(buckets[1].count, 2);
                // bucket <=1.0: 2 observations
                assert_eq!(buckets[2].count, 2);
                // overflow: 3
                assert_eq!(buckets[3].count, 3);
            }
            _ => panic!("expected histogram"),
        }
    }

    #[test]
    fn test_increment_unknown_returns_not_found() {
        let svc = MetricsService::new();
        assert!(matches!(
            svc.increment("nope", 1).unwrap_err(),
            MetricsError::NotFound(_)
        ));
    }

    #[test]
    fn test_kind_mismatch_on_counter() {
        let svc = MetricsService::new();
        svc.register_gauge("g", "g").unwrap();
        assert!(matches!(
            svc.increment("g", 1).unwrap_err(),
            MetricsError::KindMismatch { .. }
        ));
    }

    #[test]
    fn test_duplicate_registration_rejected() {
        let svc = MetricsService::new();
        svc.register_counter("c", "c").unwrap();
        assert!(matches!(
            svc.register_counter("c", "c").unwrap_err(),
            MetricsError::AlreadyRegistered(_)
        ));
    }

    #[test]
    fn test_list_metrics() {
        let svc = MetricsService::new();
        svc.register_counter("a", "a").unwrap();
        svc.register_gauge("b", "b").unwrap();
        let names: Vec<_> = svc.list_metrics().into_iter().map(|d| d.name).collect();
        assert_eq!(names.len(), 2);
        assert!(names.contains(&"a".to_string()));
        assert!(names.contains(&"b".to_string()));
    }

    #[test]
    fn test_service_contract_lifecycle() {
        let mut svc = MetricsService::new();
        svc.initialize().unwrap();
        svc.start().unwrap();
        assert!(svc.health_check().is_healthy());
        svc.stop().unwrap();
        svc.deinitialize().unwrap();
        svc.dispose();
        assert!(svc.snapshot().is_empty());
    }
}
