//! Dead letter queue manager — capacity limits, retention, inspection.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

use crate::message::MessageEnvelope;

/// Entry in the DLQ manager.
#[derive(Debug, Clone)]
pub struct DlqManagerEntry {
    pub message: MessageEnvelope,
    pub reason: String,
    pub retry_count: u32,
    pub max_retries: u32,
    pub created_at: std::time::Instant,
}

type NotificationCallback = Box<dyn Fn(&DlqManagerEntry) + Send + Sync>;

/// Dead letter queue manager with capacity and retention policies.
pub struct DeadLetterQueueManager {
    entries: Arc<Mutex<VecDeque<DlqManagerEntry>>>,
    max_capacity: usize,
    retention_period: std::time::Duration,
    notification_callback: Option<NotificationCallback>,
}

impl DeadLetterQueueManager {
    pub fn new(max_capacity: usize, retention_period: std::time::Duration) -> Self {
        Self {
            entries: Arc::new(Mutex::new(VecDeque::with_capacity(max_capacity))),
            max_capacity,
            retention_period,
            notification_callback: None,
        }
    }

    /// Set a notification callback for new DLQ entries.
    pub fn set_notification<F>(&mut self, callback: F)
    where
        F: Fn(&DlqManagerEntry) + Send + Sync + 'static,
    {
        self.notification_callback = Some(Box::new(callback));
    }

    /// Add an entry to the DLQ.
    pub fn add(
        &self,
        message: MessageEnvelope,
        reason: impl Into<String>,
        retry_count: u32,
        max_retries: u32,
    ) {
        let mut entries = self.entries.lock().unwrap();

        // Evict oldest if at capacity
        while entries.len() >= self.max_capacity {
            entries.pop_front();
        }

        let entry = DlqManagerEntry {
            message,
            reason: reason.into(),
            retry_count,
            max_retries,
            created_at: std::time::Instant::now(),
        };

        entries.push_back(entry.clone());

        // Notify
        if let Some(ref cb) = self.notification_callback {
            cb(&entry);
        }
    }

    /// Peek at the oldest entry.
    pub fn peek(&self) -> Option<DlqManagerEntry> {
        let entries = self.entries.lock().unwrap();
        entries.front().cloned()
    }

    /// Remove and return the oldest entry.
    pub fn remove(&self) -> Option<DlqManagerEntry> {
        let mut entries = self.entries.lock().unwrap();
        entries.pop_front()
    }

    /// Get all entries.
    pub fn entries(&self) -> Vec<DlqManagerEntry> {
        let entries = self.entries.lock().unwrap();
        entries.iter().cloned().collect()
    }

    /// Clean up expired entries (older than retention period).
    pub fn cleanup_expired(&self) -> usize {
        let mut entries = self.entries.lock().unwrap();
        let before = entries.len();
        entries.retain(|e| e.created_at.elapsed() < self.retention_period);
        before - entries.len()
    }

    /// Get the current size.
    pub fn len(&self) -> usize {
        let entries = self.entries.lock().unwrap();
        entries.len()
    }

    /// Return whether the queue contains no entries.
    pub fn is_empty(&self) -> bool {
        self.entries.lock().unwrap().is_empty()
    }

    /// Check if the DLQ is full.
    pub fn is_full(&self) -> bool {
        let entries = self.entries.lock().unwrap();
        entries.len() >= self.max_capacity
    }

    /// Clear all entries.
    pub fn clear(&self) {
        let mut entries = self.entries.lock().unwrap();
        entries.clear();
    }

    /// Get statistics.
    pub fn stats(&self) -> DlqManagerStats {
        let entries = self.entries.lock().unwrap();
        DlqManagerStats {
            current_size: entries.len(),
            max_capacity: self.max_capacity,
            utilization: if self.max_capacity > 0 {
                entries.len() as f64 / self.max_capacity as f64
            } else {
                0.0
            },
        }
    }
}

impl Default for DeadLetterQueueManager {
    fn default() -> Self {
        Self::new(10000, std::time::Duration::from_secs(86400 * 7)) // 7 days retention
    }
}

/// DLQ manager statistics.
#[derive(Debug, Clone)]
pub struct DlqManagerStats {
    pub current_size: usize,
    pub max_capacity: usize,
    pub utilization: f64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessageMetadata, MessagePayload, MessageType};

    fn sample_msg() -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender", "receiver", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"test": true})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_add_and_remove() {
        let mgr = DeadLetterQueueManager::new(100, std::time::Duration::from_secs(3600));
        mgr.add(sample_msg(), "test failure", 0, 3);
        assert_eq!(mgr.len(), 1);
        let entry = mgr.remove().unwrap();
        assert_eq!(entry.reason, "test failure");
    }

    #[test]
    fn test_capacity_limit() {
        let mgr = DeadLetterQueueManager::new(3, std::time::Duration::from_secs(3600));
        for _ in 0..5 {
            mgr.add(sample_msg(), "fail", 0, 3);
        }
        assert_eq!(mgr.len(), 3);
    }

    #[test]
    fn test_stats() {
        let mgr = DeadLetterQueueManager::new(100, std::time::Duration::from_secs(3600));
        mgr.add(sample_msg(), "fail", 0, 3);
        let stats = mgr.stats();
        assert_eq!(stats.current_size, 1);
        assert_eq!(stats.utilization, 0.01);
    }
}
