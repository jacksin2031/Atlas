//! Ordering guarantees — FIFO, PartialOrder, Unordered.

use serde::{Deserialize, Serialize};

/// Message ordering modes.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum MessageOrdering {
    /// Strict FIFO ordering per sender per channel.
    Fifo,
    /// Partial ordering: messages from the same sender are ordered.
    PartialOrder,
    /// No ordering guarantee.
    Unordered,
}

impl Default for MessageOrdering {
    fn default() -> Self {
        Self::Unordered
    }
}

impl MessageOrdering {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Fifo => "fifo",
            Self::PartialOrder => "partial-order",
            Self::Unordered => "unordered",
        }
    }
}

/// Enforces ordering guarantees per channel.
#[derive(Clone, Default)]
pub struct OrderingEnforcer {
    /// Last sequence number seen per (sender, channel) pair.
    last_sequence: std::sync::Arc<std::sync::Mutex<
        std::collections::HashMap<(String, String), u64>,
    >>,
    ordering: MessageOrdering,
}

impl OrderingEnforcer {
    pub fn new(ordering: MessageOrdering) -> Self {
        Self {
            last_sequence: std::sync::Arc::new(std::sync::Mutex::new(
                std::collections::HashMap::new(),
            )),
            ordering,
        }
    }

    /// Validate that a message's sequence number is in order.
    pub fn validate_sequence(
        &self,
        sender: &str,
        channel: &str,
        sequence: u64,
    ) -> Result<(), OrderingError> {
        if self.ordering == MessageOrdering::Unordered {
            return Ok(());
        }

        let mut last = self.last_sequence.lock().unwrap();
        let key = (sender.to_string(), channel.to_string());
        let prev = *last.get(&key).unwrap_or(&0);

        match self.ordering {
            MessageOrdering::Fifo => {
                if sequence != prev + 1 {
                    return Err(OrderingError::OutOfOrder {
                        expected: prev + 1,
                        got: sequence,
                    });
                }
            }
            MessageOrdering::PartialOrder => {
                if sequence <= prev {
                    return Err(OrderingError::DuplicateOrReorder {
                        last_seen: prev,
                        got: sequence,
                    });
                }
            }
            MessageOrdering::Unordered => {}
        }

        last.insert(key, sequence);
        Ok(())
    }

    /// Get the ordering mode.
    pub fn ordering(&self) -> MessageOrdering {
        self.ordering
    }
}

/// Ordering errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum OrderingError {
    #[error("out of order: expected {expected}, got {got}")]
    OutOfOrder { expected: u64, got: u64 },
    #[error("duplicate or reorder: last seen {last_seen}, got {got}")]
    DuplicateOrReorder { last_seen: u64, got: u64 },
}
