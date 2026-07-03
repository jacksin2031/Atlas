//! IPC metrics service — collects all IPC-related metrics.

use std::sync::{Arc, Mutex};
use serde::{Deserialize, Serialize};

/// Individual metric values.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MetricPoint {
    pub name: String,
    pub value: f64,
    pub kind: MetricKind,
    pub labels: std::collections::HashMap<String, String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MetricKind {
    Counter,
    Gauge,
    Histogram,
}

/// Aggregate IPC metrics snapshot.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct IpcMetricsSnapshot {
    pub messages_sent: u64,
    pub messages_received: u64,
    pub avg_latency_ms: f64,
    pub max_latency_ms: f64,
    pub serialization_time_avg_ms: f64,
    pub queue_size: usize,
    pub dropped_messages: u64,
    pub timeout_count: u64,
    pub retry_count: u64,
    pub error_count: u64,
}

impl IpcMetricsSnapshot {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_messages_sent(mut self, count: u64) -> Self {
        self.messages_sent = count;
        self
    }

    pub fn with_messages_received(mut self, count: u64) -> Self {
        self.messages_received = count;
        self
    }

    pub fn with_latency(mut self, avg: f64, max: f64) -> Self {
        self.avg_latency_ms = avg;
        self.max_latency_ms = max;
        self
    }

    pub fn with_queue_size(mut self, size: usize) -> Self {
        self.queue_size = size;
        self
    }

    pub fn with_dropped(mut self, count: u64) -> Self {
        self.dropped_messages = count;
        self
    }

    pub fn with_timeouts(mut self, count: u64) -> Self {
        self.timeout_count = count;
        self
    }

    pub fn with_retries(mut self, count: u64) -> Self {
        self.retry_count = count;
        self
    }

    pub fn with_errors(mut self, count: u64) -> Self {
        self.error_count = count;
        self
    }
}

/// IPC metrics service.
#[derive(Clone)]
pub struct IpcMetricsService {
    snapshot: Arc<Mutex<IpcMetricsSnapshot>>,
}

impl IpcMetricsService {
    pub fn new() -> Self {
        Self {
            snapshot: Arc::new(Mutex::new(IpcMetricsSnapshot::new())),
        }
    }

    /// Record a sent message.
    pub fn record_sent(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.messages_sent += 1;
    }

    /// Record a received message.
    pub fn record_received(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.messages_received += 1;
    }

    /// Record message latency.
    pub fn record_latency(&self, latency_ms: f64) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.max_latency_ms = snap.max_latency_ms.max(latency_ms);
        // Simple average update
        let total = snap.messages_sent + snap.messages_received;
        if total > 0 {
            snap.avg_latency_ms = (snap.avg_latency_ms * ((total - 1) as f64) + latency_ms) / total as f64;
        }
    }

    /// Record serialization time.
    pub fn record_serialization_time(&self, time_ms: f64) {
        let mut snap = self.snapshot.lock().unwrap();
        // Similar averaging
        snap.serialization_time_avg_ms = time_ms;
    }

    /// Record a dropped message.
    pub fn record_dropped(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.dropped_messages += 1;
    }

    /// Record a timeout.
    pub fn record_timeout(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.timeout_count += 1;
    }

    /// Record a retry.
    pub fn record_retry(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.retry_count += 1;
    }

    /// Record an error.
    pub fn record_error(&self) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.error_count += 1;
    }

    /// Set queue size.
    pub fn set_queue_size(&self, size: usize) {
        let mut snap = self.snapshot.lock().unwrap();
        snap.queue_size = size;
    }

    /// Get the current snapshot.
    pub fn snapshot(&self) -> IpcMetricsSnapshot {
        let snap = self.snapshot.lock().unwrap();
        snap.clone()
    }
}

impl Default for IpcMetricsService {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_record_metrics() {
        let svc = IpcMetricsService::new();
        svc.record_sent();
        svc.record_sent();
        svc.record_received();
        svc.record_latency(5.0);
        svc.record_error();
        let snap = svc.snapshot();
        assert_eq!(snap.messages_sent, 2);
        assert_eq!(snap.messages_received, 1);
        assert_eq!(snap.error_count, 1);
        assert_eq!(snap.max_latency_ms, 5.0);
    }
}
