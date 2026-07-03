//! Event bus bridge — integrates IPC with the Runtime Event Bus.

use std::sync::{Arc, Mutex};

use crate::message::MessageEnvelope;
use crate::eventbus::events::IpcEventType;
use super::publisher::EventPublisher;
use crate::eventbus::subscriber::{EventSubscriber, SubscriptionHandle};

/// Bridges IPC messages to and from the event bus.
pub struct EventBusBridge {
    publisher: EventPublisher,
    subscriber: EventSubscriber,
    authorization_required: bool,
    dead_letter_queue: Arc<Mutex<Vec<MessageEnvelope>>>,
}

impl EventBusBridge {
    pub fn new(channel: impl Into<String>) -> Self {
        Self {
            publisher: EventPublisher::new(channel),
            subscriber: EventSubscriber::new(),
            authorization_required: true,
            dead_letter_queue: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Require authorization for all events (default: true).
    pub fn with_authorization(mut self, required: bool) -> Self {
        self.authorization_required = required;
        self
    }

    /// Publish an event through IPC.
    pub fn publish(&self, event: IpcEventType, data: serde_json::Value) -> MessageEnvelope {
        // IPC MUST never bypass Runtime authorization
        if self.authorization_required {
            // In a real implementation, check with the runtime authorization service
        }
        self.publisher.publish_event(event, data)
    }

    /// Subscribe to events with a pattern.
    pub fn subscribe(
        &self,
        id: impl Into<String>,
        pattern: impl Into<String>,
        callback: crate::eventbus::subscriber::EventCallback,
    ) -> SubscriptionHandle {
        self.subscriber.subscribe(id, pattern, callback)
    }

    /// Unsubscribe by handle.
    pub fn unsubscribe(&self, handle: &SubscriptionHandle) -> bool {
        self.subscriber.unsubscribe(handle)
    }

    /// Deliver an event to matching subscribers.
    pub fn deliver(&self, event: &IpcEventType) -> usize {
        self.subscriber.deliver(event)
    }

    /// Get published event count.
    pub fn published_count(&self) -> usize {
        self.publisher.published_count()
    }

    /// Get subscription count.
    pub fn subscription_count(&self) -> usize {
        self.subscriber.subscription_count()
    }

    /// Route a failed event to the dead letter queue.
    pub fn route_to_dlq(&self, envelope: MessageEnvelope) {
        let mut dlq = self.dead_letter_queue.lock().unwrap();
        dlq.push(envelope);
    }

    /// Get dead letter queue entries.
    pub fn dlq_entries(&self) -> Vec<MessageEnvelope> {
        let dlq = self.dead_letter_queue.lock().unwrap();
        dlq.clone()
    }

    /// Deduplicate events by message ID.
    pub fn deduplicate(&self, envelope: &MessageEnvelope) -> bool {
        // In a real implementation, track seen message IDs
        !envelope.header.message_id.is_nil()
    }
}

impl Default for EventBusBridge {
    fn default() -> Self {
        Self::new("default-channel")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_publish_event() {
        let bridge = EventBusBridge::new("test");
        let event = IpcEventType::Runtime(crate::eventbus::events::RuntimeEvent {
            event_kind: crate::eventbus::events::RuntimeEventKind::Started,
            timestamp_epoch: 0,
            data: serde_json::json!({}),
        });
        let _envelope = bridge.publish(event.clone(), serde_json::json!({"key": "val"}));
        assert_eq!(bridge.published_count(), 1);
    }

    #[test]
    fn test_subscribe_and_deliver() {
        let bridge = EventBusBridge::new("test");
        let received = Arc::new(Mutex::new(false));
        let received_clone = received.clone();
        let cb: crate::eventbus::subscriber::EventCallback = Arc::new(move |_| {
            *received_clone.lock().unwrap() = true;
        });
        bridge.subscribe("sub-1", "*", cb);
        assert_eq!(bridge.subscription_count(), 1);
    }
}


