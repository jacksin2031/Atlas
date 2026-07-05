//! Delivery guarantees — AtMostOnce, AtLeastOnce, ExactlyOnce.

use serde::{Deserialize, Serialize};

/// Delivery guarantee levels.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DeliveryGuarantee {
    /// Message may be lost but never duplicated.
    AtMostOnce,
    /// Message is delivered at least once (may be duplicated).
    AtLeastOnce,
    /// Message is delivered exactly once.
    ExactlyOnce,
}

impl Default for DeliveryGuarantee {
    fn default() -> Self {
        Self::AtLeastOnce
    }
}

impl DeliveryGuarantee {
    pub fn label(&self) -> &'static str {
        match self {
            Self::AtMostOnce => "at-most-once",
            Self::AtLeastOnce => "at-least-once",
            Self::ExactlyOnce => "exactly-once",
        }
    }

    /// Returns true if acknowledgments are required.
    pub fn requires_ack(&self) -> bool {
        matches!(self, Self::AtLeastOnce | Self::ExactlyOnce)
    }

    /// Returns true if deduplication is needed.
    pub fn requires_deduplication(&self) -> bool {
        matches!(self, Self::ExactlyOnce)
    }
}

/// Enforces delivery guarantees for a channel.
#[derive(Clone)]
pub struct DeliveryGuaranteeEnforcer {
    guarantee: DeliveryGuarantee,
    /// For ExactlyOnce: tracks sent message IDs for deduplication.
    sent_ids: std::sync::Arc<std::sync::Mutex<std::collections::HashSet<String>>>,
    /// For AtLeastOnce: tracks unacknowledged messages.
    unacked:
        std::sync::Arc<std::sync::Mutex<std::collections::HashMap<String, std::time::Instant>>>,
}

impl DeliveryGuaranteeEnforcer {
    pub fn new(guarantee: DeliveryGuarantee) -> Self {
        Self {
            guarantee,
            sent_ids: std::sync::Arc::new(std::sync::Mutex::new(std::collections::HashSet::new())),
            unacked: std::sync::Arc::new(std::sync::Mutex::new(std::collections::HashMap::new())),
        }
    }

    /// Check if a message has already been sent (for ExactlyOnce).
    pub fn is_duplicate(&self, message_id: &str) -> bool {
        let ids = self.sent_ids.lock().unwrap();
        ids.contains(message_id)
    }

    /// Record a message as sent.
    pub fn record_sent(&self, message_id: &str) {
        let mut ids = self.sent_ids.lock().unwrap();
        ids.insert(message_id.to_string());
        if self.guarantee.requires_ack() {
            let mut unacked = self.unacked.lock().unwrap();
            unacked.insert(message_id.to_string(), std::time::Instant::now());
        }
    }

    /// Acknowledge a message.
    pub fn acknowledge(&self, message_id: &str) {
        let mut ids = self.sent_ids.lock().unwrap();
        ids.remove(message_id);
        let mut unacked = self.unacked.lock().unwrap();
        unacked.remove(message_id);
    }

    /// Get unacknowledged message IDs.
    pub fn unacked_messages(&self) -> Vec<String> {
        let unacked = self.unacked.lock().unwrap();
        unacked.keys().cloned().collect()
    }

    /// Get the guarantee level.
    pub fn guarantee(&self) -> DeliveryGuarantee {
        self.guarantee
    }
}
