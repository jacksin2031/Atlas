//! Event Bus implementation.

use atlas_contracts::{
    Channel, Event, EventBusError, EventBusStats, EventPriority, SubscriptionHandle,
};
use std::collections::HashMap;
use uuid::Uuid;

struct Subscriber {
    pattern: String,
    handler: Box<dyn Fn(&Event) + Send + Sync>,
}

/// Event Bus implementation.
pub struct EventBusImpl {
    subscribers: HashMap<String, Vec<Subscriber>>,
    stats: EventBusStats,
}

impl EventBusImpl {
    pub fn new() -> Self {
        Self {
            subscribers: HashMap::new(),
            stats: EventBusStats::default(),
        }
    }

    pub fn publish(&mut self, channel: Channel, event: Event) -> Result<(), EventBusError> {
        self.stats.total_published += 1;
        if let Some(sub_list) = self.subscribers.get(&channel.0) {
            for sub in sub_list {
                (sub.handler)(&event);
            }
        }
        Ok(())
    }

    pub fn subscribe<F>(&mut self, pattern: String, handler: F) -> SubscriptionHandle
    where
        F: Fn(&Event) + Send + Sync + 'static,
    {
        let handle = SubscriptionHandle(Uuid::new_v4().to_string());
        self.subscribers
            .entry(pattern)
            .or_default()
            .push(Subscriber {
                pattern: handle.0.clone(),
                handler: Box::new(handler),
            });
        self.stats.total_subscribed += 1;
        handle
    }

    pub fn unsubscribe(&mut self, handle: &SubscriptionHandle) -> Result<(), EventBusError> {
        for sub_list in self.subscribers.values_mut() {
            sub_list.retain(|s| s.pattern != handle.0);
        }
        Ok(())
    }

    pub fn get_stats(&self) -> EventBusStats {
        self.stats.clone()
    }

    pub fn publish_ready(&mut self) -> Result<(), EventBusError> {
        let event = Event::new(Channel::new("lifecycle"), "Ready", serde_json::json!({}))
            .with_priority(EventPriority::Critical);
        self.publish(Channel::new("lifecycle"), event)
    }

    pub fn publish_running(&mut self) -> Result<(), EventBusError> {
        let event = Event::new(Channel::new("lifecycle"), "Running", serde_json::json!({}))
            .with_priority(EventPriority::Critical);
        self.publish(Channel::new("lifecycle"), event)
    }

    pub fn publish_shutdown(&mut self) -> Result<(), EventBusError> {
        let event = Event::new(
            Channel::new("lifecycle"),
            "ShutdownRequested",
            serde_json::json!({}),
        )
        .with_priority(EventPriority::Critical);
        self.publish(Channel::new("lifecycle"), event)
    }

    pub fn publish_terminated(&mut self) -> Result<(), EventBusError> {
        let event = Event::new(
            Channel::new("lifecycle"),
            "Terminated",
            serde_json::json!({}),
        )
        .with_priority(EventPriority::Critical);
        self.publish(Channel::new("lifecycle"), event)
    }
}

impl Default for EventBusImpl {
    fn default() -> Self {
        Self::new()
    }
}
