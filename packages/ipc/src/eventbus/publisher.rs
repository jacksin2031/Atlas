//! Event publisher for the IPC event bus bridge.

use std::sync::{Arc, Mutex};

use crate::message::{MessageEnvelope, MessageHeader, MessagePayload, MessageMetadata, MessageType};
use super::events::{IpcEventType, RuntimeEvent, RuntimeEventKind};

/// Published event record.
#[derive(Debug, Clone)]
pub struct PublishedEvent {
    pub event_type: IpcEventType,
    pub channel: String,
    pub priority: crate::message::MessagePriority,
    pub published_at: std::time::Instant,
}

/// Publishes IPC events as messages.
#[derive(Clone)]
pub struct EventPublisher {
    events: Arc<Mutex<Vec<PublishedEvent>>>,
    channel: String,
}

impl EventPublisher {
    pub fn new(channel: impl Into<String>) -> Self {
        Self {
            events: Arc::new(Mutex::new(Vec::new())),
            channel: channel.into(),
        }
    }

    /// Publish a runtime event.
    pub fn publish_runtime_event(
        &self,
        kind: RuntimeEventKind,
        data: serde_json::Value,
    ) -> MessageEnvelope {
        let event = RuntimeEvent {
            event_kind: kind,
            timestamp_epoch: std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap_or_default().as_secs(),
            data: data.clone(),
        };
        let ipc_event = IpcEventType::Runtime(event);
        self.publish_event(ipc_event, data)
    }

    /// Publish any IPC event type.
    pub fn publish_event(
        &self,
        ipc_event: IpcEventType,
        data: serde_json::Value,
    ) -> MessageEnvelope {
        let envelope = MessageEnvelope::fire_and_forget(
            "event-bus",
            &self.channel,
            MessageType::Event,
            data,
        ).unwrap_or_else(|_| MessageEnvelope {
            header: MessageHeader::new("event-bus", "*", MessageType::Event, 60),
            payload: MessagePayload::new(serde_json::json!({"event": format!("{:?}", ipc_event)})).unwrap_or_default(),
            metadata: MessageMetadata::default(),
        });

        let mut events = self.events.lock().unwrap();
        events.push(PublishedEvent {
            event_type: ipc_event,
            channel: self.channel.clone(),
            priority: crate::message::MessagePriority::Normal,
            published_at: std::time::Instant::now(),
        });

        envelope
    }

    /// Get all published events.
    pub fn published_events(&self) -> Vec<PublishedEvent> {
        let events = self.events.lock().unwrap();
        events.clone()
    }

    /// Get the count of published events.
    pub fn published_count(&self) -> usize {
        let events = self.events.lock().unwrap();
        events.len()
    }
}


