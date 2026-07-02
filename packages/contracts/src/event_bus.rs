//! Event Bus trait definitions.

use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Channel identifier for event routing.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Channel(pub String);

impl Channel {
    pub fn new(name: impl Into<String>) -> Self {
        Self(name.into())
    }
}

/// Event priority levels.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[repr(u8)]
pub enum EventPriority {
    Critical = 0,
    High = 1,
    Normal = 2,
    Low = 3,
    Background = 4,
}

/// Standard event payload.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Event {
    pub event_id: Uuid,
    pub correlation_id: Uuid,
    pub trace_id: Uuid,
    pub channel: Channel,
    pub priority: EventPriority,
    pub event_type: String,
    pub payload: serde_json::Value,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

impl Event {
    pub fn new(channel: Channel, event_type: impl Into<String>, payload: serde_json::Value) -> Self {
        Self {
            event_id: Uuid::new_v4(),
            correlation_id: Uuid::new_v4(),
            trace_id: Uuid::new_v4(),
            channel,
            priority: EventPriority::Normal,
            event_type: event_type.into(),
            payload,
            timestamp: chrono::Utc::now(),
        }
    }

    pub fn with_priority(mut self, priority: EventPriority) -> Self {
        self.priority = priority;
        self
    }
}

/// Subscription handle.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct SubscriptionHandle(pub String);

/// Event bus statistics.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct EventBusStats {
    pub total_published: u64,
    pub total_subscribed: u64,
    pub total_failed: u64,
    pub dlq_size: usize,
}

/// Error from event bus operations.
#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum EventBusError {
    #[error("channel not found: {0}")]
    ChannelNotFound(String),
    #[error("subscription not found: {0}")]
    SubscriptionNotFound(String),
    #[error("event dispatch failed: {0}")]
    DispatchFailed(String),
    #[error("dead letter queue full")]
    DlqFull,
}

/// The event bus interface.
pub trait EventBus: Send + Sync {
    fn publish(&self, channel: Channel, event: Event) -> Result<(), EventBusError>;
    fn subscribe<F>(&self, pattern: String, handler: F) -> SubscriptionHandle
    where
        F: Fn(&Event) + Send + Sync + 'static;
    fn unsubscribe(&self, handle: &SubscriptionHandle) -> Result<(), EventBusError>;
    fn get_stats(&self) -> EventBusStats;
}

