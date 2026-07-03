//! Message priority levels.
//!
//! Priorities are numeric values 0-4 where lower numbers indicate higher urgency.
//! The runtime uses these values for scheduling and back-pressure decisions.

use serde::{Deserialize, Serialize};

/// Message priority levels, ordered from highest to lowest urgency.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[repr(u8)]
pub enum MessagePriority {
    /// Critical - must be delivered immediately; bypasses normal queues.
    Critical = 0,
    /// High - prioritised over normal traffic.
    High = 1,
    /// Normal - default scheduling tier.
    Normal = 2,
    /// Low - deferred when the queue is back-pressured.
    Low = 3,
    /// Background - processed only when the system is idle.
    Background = 4,
}

impl MessagePriority {
    /// Returns the numeric priority value (0-4).
    pub fn value(self) -> u8 {
        self as u8
    }

    /// Returns a human-readable label.
    pub fn label(self) -> &'static str {
        match self {
            Self::Critical => "critical",
            Self::High => "high",
            Self::Normal => "normal",
            Self::Low => "low",
            Self::Background => "background",
        }
    }
}

impl Default for MessagePriority {
    fn default() -> Self {
        Self::Normal
    }
}

impl core::fmt::Display for MessagePriority {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}({})", self.label(), self.value())
    }
}

/// Construct a priority from a raw byte value.
impl TryFrom<u8> for MessagePriority {
    type Error = InvalidPriorityError;

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        match value {
            0 => Ok(Self::Critical),
            1 => Ok(Self::High),
            2 => Ok(Self::Normal),
            3 => Ok(Self::Low),
            4 => Ok(Self::Background),
            _ => Err(InvalidPriorityError(value)),
        }
    }
}

/// Error returned when an invalid priority byte is encountered.
#[derive(Debug, Clone, PartialEq, thiserror::Error)]
#[error("invalid priority value: {0}; expected 0-4")]
pub struct InvalidPriorityError(pub u8);
