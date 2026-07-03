//! Dead letter queue for undeliverable messages.

use std::collections::VecDeque;
use serde::{Deserialize, Serialize};
use crate::message::MessageEnvelope;

/// Epoch-based timestamp for serialization.
type EpochTime = u64;

/// Entries in the dead letter queue.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DlqEntry {
    pub original_message: MessageEnvelope,
    pub failure_reason: String,
    pub attempted_epoch: EpochTime,
    pub retry_count: u32,
    pub max_retries: u32,
}

/// Dead letter queue with configurable capacity and retention.
#[derive(Debug, Clone)]
pub struct DeadLetterQueue {
    entries: VecDeque<DlqEntry>,
    max_capacity: usize,
    notification_enabled: bool,
    total_diverted: u64,
}

impl DeadLetterQueue {
    pub fn new(max_capacity: usize) -> Self {
        Self {
            entries: VecDeque::with_capacity(max_capacity),
            max_capacity,
            notification_enabled: true,
            total_diverted: 0,
        }
    }

    pub fn add(&mut self, message: MessageEnvelope, reason: impl Into<String>, retry_count: u32, max_retries: u32) {
        if self.entries.len() >= self.max_capacity {
            self.entries.pop_front();
        }
        let epoch = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        self.entries.push_back(DlqEntry {
            original_message: message,
            failure_reason: reason.into(),
            attempted_epoch: epoch,
            retry_count,
            max_retries,
        });
        self.total_diverted += 1;
    }

    pub fn peek(&self) -> Option<&DlqEntry> {
        self.entries.front()
    }

    pub fn remove(&mut self) -> Option<DlqEntry> {
        self.entries.pop_front()
    }

    pub fn entries_list(&self) -> Vec<&DlqEntry> {
        self.entries.iter().collect()
    }

    pub fn is_full(&self) -> bool {
        self.entries.len() >= self.max_capacity
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn clear(&mut self) {
        self.entries.clear();
    }

    pub fn set_notifications(&mut self, enabled: bool) {
        self.notification_enabled = enabled;
    }

    pub fn stats(&self) -> DlqStats {
        DlqStats {
            current_size: self.entries.len(),
            max_capacity: self.max_capacity,
            total_diverted: self.total_diverted,
        }
    }
}

impl Default for DeadLetterQueue {
    fn default() -> Self {
        Self::new(10000)
    }
}

/// DLQ statistics.
#[derive(Debug, Clone)]
pub struct DlqStats {
    pub current_size: usize,
    pub max_capacity: usize,
    pub total_diverted: u64,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessagePayload, MessageMetadata, MessageType};

    fn sample_msg() -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender", "receiver", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"test": true})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_add_and_remove() {
        let mut dlq = DeadLetterQueue::new(100);
        dlq.add(sample_msg(), "delivery failed", 0, 3);
        assert_eq!(dlq.len(), 1);
        let entry = dlq.remove().unwrap();
        assert_eq!(entry.failure_reason, "delivery failed");
    }

    #[test]
    fn test_eviction_on_overflow() {
        let mut dlq = DeadLetterQueue::new(3);
        for i in 0..5 {
            dlq.add(sample_msg(), format!("failure {}", i), 0, 3);
        }
        assert_eq!(dlq.len(), 3);
    }

    #[test]
    fn test_clear() {
        let mut dlq = DeadLetterQueue::new(100);
        dlq.add(sample_msg(), "fail", 0, 3);
        dlq.clear();
        assert!(dlq.is_empty());
    }

    #[test]
    fn test_stats() {
        let mut dlq = DeadLetterQueue::new(100);
        dlq.add(sample_msg(), "fail", 0, 3);
        dlq.add(sample_msg(), "fail2", 0, 3);
        let stats = dlq.stats();
        assert_eq!(stats.current_size, 2);
        assert_eq!(stats.total_diverted, 2);
    }
}
