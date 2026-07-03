//! Plugin event integration (RFC-0210).
//!
//! Plugins communicate exclusively through the event bus (RFC-0210 §4). This
//! module defines the plugin event catalog, typed event payloads, and an
//! in-memory event bus implementing the standard [`atlas_contracts::EventBus`]
//! contract so that the Runtime and Workflow Engine can subscribe to plugin
//! events.
//!
//! Event catalog (Plugin Runtime scope): `PluginRegistered`, `PluginLoaded`,
//! `PluginStarted`, `PluginStopped`, `PluginPaused`, `PluginResumed`,
//! `PluginFailed`, `PluginRecovered`, `PluginRemoved`, `PluginUpdated`.

use atlas_contracts::{Channel, Event, EventBusError, EventBusStats, EventPriority, SubscriptionHandle};
use atlas_contracts::EventBus;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fmt;
use std::sync::Mutex;
use uuid::Uuid;

/// The plugin event channel used for all plugin lifecycle/registry events.
pub const PLUGIN_CHANNEL: &str = "plugin";

/// Plugin event types (RFC-0210 §9).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PluginEventType {
    PluginRegistered,
    PluginLoaded,
    PluginStarted,
    PluginStopped,
    PluginPaused,
    PluginResumed,
    PluginFailed,
    PluginRecovered,
    PluginRemoved,
    PluginUpdated,
}

impl PluginEventType {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::PluginRegistered => "PluginRegistered",
            Self::PluginLoaded => "PluginLoaded",
            Self::PluginStarted => "PluginStarted",
            Self::PluginStopped => "PluginStopped",
            Self::PluginPaused => "PluginPaused",
            Self::PluginResumed => "PluginResumed",
            Self::PluginFailed => "PluginFailed",
            Self::PluginRecovered => "PluginRecovered",
            Self::PluginRemoved => "PluginRemoved",
            Self::PluginUpdated => "PluginUpdated",
        }
    }
}

impl fmt::Display for PluginEventType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// Typed plugin event payload (RFC-0210 §18).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PluginEvent {
    pub event_type: PluginEventType,
    pub plugin_id: String,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub payload: serde_json::Value,
}

impl PluginEvent {
    /// Create a new plugin event of `event_type` for `plugin_id`.
    pub fn new(event_type: PluginEventType, plugin_id: impl Into<String>, payload: serde_json::Value) -> Self {
        Self {
            event_type,
            plugin_id: plugin_id.into(),
            timestamp: chrono::Utc::now(),
            payload,
        }
    }

    /// Convert this typed event into a bus [`Event`] on the plugin channel.
    pub fn to_event(&self) -> Event {
        let mut event = Event::new(
            Channel::new(PLUGIN_CHANNEL),
            self.event_type.as_str(),
            serde_json::to_value(self).unwrap_or(serde_json::Value::Null),
        );
        event = event.with_priority(EventPriority::Normal);
        event
    }

    /// Build a registered event.
    pub fn registered(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginRegistered, plugin_id, serde_json::json!({}))
    }
    /// Build a loaded event.
    pub fn loaded(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginLoaded, plugin_id, serde_json::json!({}))
    }
    /// Build a failed event with a reason.
    pub fn failed(plugin_id: impl Into<String>, reason: &str) -> Self {
        Self::new(PluginEventType::PluginFailed, plugin_id, serde_json::json!({ "reason": reason }))
    }
    /// Build a started event.
    pub fn started(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginStarted, plugin_id, serde_json::json!({}))
    }
    /// Build a stopped event.
    pub fn stopped(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginStopped, plugin_id, serde_json::json!({}))
    }
    /// Build a paused event.
    pub fn paused(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginPaused, plugin_id, serde_json::json!({}))
    }
    /// Build a resumed event.
    pub fn resumed(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginResumed, plugin_id, serde_json::json!({}))
    }
    /// Build a recovered event.
    pub fn recovered(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginRecovered, plugin_id, serde_json::json!({}))
    }
    /// Build a removed event.
    pub fn removed(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginRemoved, plugin_id, serde_json::json!({}))
    }
    /// Build an updated event.
    pub fn updated(plugin_id: impl Into<String>) -> Self {
        Self::new(PluginEventType::PluginUpdated, plugin_id, serde_json::json!({}))
    }
}

struct Subscriber {
    handle: String,
    handler: Box<dyn Fn(&Event) + Send + Sync>,
}

/// In-memory plugin event bus implementing [`atlas_contracts::EventBus`].
///
/// Dispatches events to subscribers registered for a channel. Uses interior
/// mutability so it is [`Send`] + [`Sync`] and can be shared via dependency
/// injection as `Arc<dyn EventBus>` without global mutable state.
pub struct PluginEventBusImpl {
    subscribers: Mutex<HashMap<String, Vec<Subscriber>>>,
    stats: Mutex<EventBusStats>,
}

impl PluginEventBusImpl {
    pub fn new() -> Self {
        Self {
            subscribers: Mutex::new(HashMap::new()),
            stats: Mutex::new(EventBusStats::default()),
        }
    }

    /// Publish a typed plugin event on the plugin channel.
    pub fn publish_plugin_event(&self, event: &PluginEvent) -> Result<(), EventBusError> {
        self.publish(Channel::new(PLUGIN_CHANNEL), event.to_event())
    }
}

impl Default for PluginEventBusImpl {
    fn default() -> Self {
        Self::new()
    }
}

impl atlas_contracts::EventBus for PluginEventBusImpl {
    fn publish(&self, channel: Channel, event: Event) -> Result<(), EventBusError> {
        {
            let mut stats = self.stats.lock().expect("plugin event bus stats mutex poisoned");
            stats.total_published += 1;
        }
        let subscribers = self.subscribers.lock().expect("plugin event bus subscribers mutex poisoned");
        if let Some(list) = subscribers.get(&channel.0) {
            for sub in list {
                (sub.handler)(&event);
            }
        }
        Ok(())
    }

    fn subscribe(&self, pattern: String, handler: Box<dyn Fn(&Event) + Send + Sync>) -> SubscriptionHandle {
        let handle = SubscriptionHandle(Uuid::new_v4().to_string());
        let subscriber = Subscriber { handle: handle.0.clone(), handler: Box::new(handler) };
        self.subscribers
            .lock()
            .expect("plugin event bus subscribers mutex poisoned")
            .entry(pattern)
            .or_default()
            .push(subscriber);
        let mut stats = self.stats.lock().expect("plugin event bus stats mutex poisoned");
        stats.total_subscribed += 1;
        handle
    }

    fn unsubscribe(&self, handle: &SubscriptionHandle) -> Result<(), EventBusError> {
        let mut subscribers =
            self.subscribers.lock().expect("plugin event bus subscribers mutex poisoned");
        for list in subscribers.values_mut() {
            list.retain(|s| s.handle != handle.0);
        }
        Ok(())
    }

    fn get_stats(&self) -> EventBusStats {
        self.stats.lock().expect("plugin event bus stats mutex poisoned").clone()
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use atlas_contracts::EventBus;
    use std::sync::Arc;
    use std::sync::atomic::{AtomicUsize, Ordering};

    #[test]
    fn test_event_type_str() {
        assert_eq!(PluginEventType::PluginStarted.as_str(), "PluginStarted");
        assert_eq!(PluginEventType::PluginFailed.to_string(), "PluginFailed");
    }

    #[test]
    fn test_plugin_event_to_event() {
        let pe = PluginEvent::failed("p1", "boom");
        let event = pe.to_event();
        assert_eq!(event.channel.0, PLUGIN_CHANNEL);
        assert_eq!(event.event_type, "PluginFailed");
    }

    #[test]
    fn test_publish_and_subscribe() {
        let bus = Arc::new(PluginEventBusImpl::new());
        let counter = Arc::new(AtomicUsize::new(0));
        let c2 = counter.clone();
        let _handle = bus.subscribe(
            PLUGIN_CHANNEL.to_string(),
            Box::new(move |_event| {
                c2.fetch_add(1, Ordering::SeqCst);
            }),
        );
        bus.publish_plugin_event(&PluginEvent::loaded("p1")).unwrap();
        bus.publish_plugin_event(&PluginEvent::started("p1")).unwrap();
        assert_eq!(counter.load(Ordering::SeqCst), 2);
    }

    #[test]
    fn test_stats_track_publish_and_subscribe() {
        let bus = PluginEventBusImpl::new();
        let _h = bus.subscribe(PLUGIN_CHANNEL.to_string(), Box::new(|_| {}));
        bus.publish_plugin_event(&PluginEvent::registered("p1")).unwrap();
        let stats = bus.get_stats();
        assert_eq!(stats.total_published, 1);
        assert_eq!(stats.total_subscribed, 1);
    }

    #[test]
    fn test_unsubscribe_removes_handler() {
        let bus = Arc::new(PluginEventBusImpl::new());
        let counter = Arc::new(AtomicUsize::new(0));
        let c2 = counter.clone();
        let handle = bus.subscribe(PLUGIN_CHANNEL.to_string(), Box::new(move |_| { c2.fetch_add(1, Ordering::SeqCst); }));
        bus.publish_plugin_event(&PluginEvent::loaded("p1")).unwrap();
        bus.unsubscribe(&handle).unwrap();
        bus.publish_plugin_event(&PluginEvent::loaded("p1")).unwrap();
        assert_eq!(counter.load(Ordering::SeqCst), 1);
    }

    #[test]
    fn test_event_constructors() {
        let _ = PluginEvent::registered("p1");
        let _ = PluginEvent::loaded("p1");
        assert_eq!(PluginEvent::failed("p1", "x").event_type, PluginEventType::PluginFailed);
    }

    #[test]
    fn test_all_event_types_distinct() {
        let all = [
            PluginEventType::PluginRegistered,
            PluginEventType::PluginLoaded,
            PluginEventType::PluginStarted,
            PluginEventType::PluginStopped,
            PluginEventType::PluginPaused,
            PluginEventType::PluginResumed,
            PluginEventType::PluginFailed,
            PluginEventType::PluginRecovered,
            PluginEventType::PluginRemoved,
            PluginEventType::PluginUpdated,
        ];
        let names: Vec<&str> = all.iter().map(|e| e.as_str()).collect();
        let unique: std::collections::HashSet<&str> = names.iter().copied().collect();
        assert_eq!(unique.len(), all.len());
    }
}








