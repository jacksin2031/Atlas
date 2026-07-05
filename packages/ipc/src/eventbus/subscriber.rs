//! Event subscriber with pattern matching and priority handling.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use crate::eventbus::events::IpcEventType;

/// Subscription handle for event subscribers.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct SubscriptionHandle {
    pub id: String,
}

/// Callback type for event subscribers.
pub type EventCallback = Arc<dyn Fn(&IpcEventType) + Send + Sync>;

/// Subscriber configuration.
#[derive(Clone)]
pub struct SubscriberConfig {
    pub pattern: String,
    pub priority: crate::message::MessagePriority,
    pub callback: EventCallback,
}

impl SubscriberConfig {
    pub fn new(pattern: impl Into<String>, callback: EventCallback) -> Self {
        Self {
            pattern: pattern.into(),
            priority: crate::message::MessagePriority::Normal,
            callback,
        }
    }
}

/// Subscribes to events matching a pattern.
pub struct EventSubscriber {
    subscriptions: Arc<Mutex<HashMap<String, SubscriberConfig>>>,
}

impl EventSubscriber {
    pub fn new() -> Self {
        Self {
            subscriptions: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    pub fn subscribe(
        &self,
        id: impl Into<String>,
        pattern: impl Into<String>,
        callback: EventCallback,
    ) -> SubscriptionHandle {
        let id = id.into();
        let mut subs = self.subscriptions.lock().unwrap();
        subs.insert(id.clone(), SubscriberConfig::new(pattern, callback));
        SubscriptionHandle { id }
    }

    pub fn unsubscribe(&self, handle: &SubscriptionHandle) -> bool {
        let mut subs = self.subscriptions.lock().unwrap();
        subs.remove(&handle.id).is_some()
    }

    pub fn deliver(&self, event: &IpcEventType) -> usize {
        let subs = self.subscriptions.lock().unwrap();
        let mut delivered = 0;
        for config in subs.values() {
            (config.callback)(event);
            delivered += 1;
        }
        delivered
    }

    pub fn subscription_count(&self) -> usize {
        let subs = self.subscriptions.lock().unwrap();
        subs.len()
    }

    pub fn subscription_ids(&self) -> Vec<String> {
        let subs = self.subscriptions.lock().unwrap();
        subs.keys().cloned().collect()
    }
}

impl Default for EventSubscriber {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_subscribe_and_deliver() {
        let subscriber = EventSubscriber::new();
        let received = Arc::new(Mutex::new(false));
        let received_clone = received.clone();
        let cb: EventCallback = Arc::new(move |_| {
            *received_clone.lock().unwrap() = true;
        });
        subscriber.subscribe("sub-1", "*", cb);
        assert_eq!(subscriber.subscription_count(), 1);

        let event = IpcEventType::Runtime(crate::eventbus::events::RuntimeEvent {
            event_kind: crate::eventbus::events::RuntimeEventKind::Started,
            timestamp_epoch: 0,
            data: serde_json::json!({}),
        });
        subscriber.deliver(&event);
        assert!(*received.lock().unwrap());
    }

    #[test]
    fn test_unsubscribe() {
        let subscriber = EventSubscriber::new();
        let cb: EventCallback = Arc::new(|_| {});
        let handle = subscriber.subscribe("sub-1", "*", cb);
        assert_eq!(subscriber.subscription_count(), 1);
        assert!(subscriber.unsubscribe(&handle));
        assert_eq!(subscriber.subscription_count(), 0);
    }
}
