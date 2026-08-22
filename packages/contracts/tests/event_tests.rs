//! Tests for event types.

use atlas_contracts::{Channel, Event, EventBusStats, EventPriority, SubscriptionHandle};
use uuid::Uuid;

#[test]
fn test_event_creation() {
    let event = Event::new(
        Channel::new("test.channel"),
        "TestEvent",
        serde_json::json!({"key": "value"}),
    );
    assert_eq!(event.event_type, "TestEvent");
    assert_eq!(event.priority, EventPriority::Normal);
    assert_eq!(event.channel.0, "test.channel");
}

#[test]
fn test_event_priority_override() {
    let event = Event::new(Channel::new("test"), "Test", serde_json::json!({}))
        .with_priority(EventPriority::Critical);
    assert_eq!(event.priority, EventPriority::Critical);
}

#[test]
fn test_subscription_handle() {
    let handle = SubscriptionHandle(Uuid::new_v4().to_string());
    assert!(!handle.0.is_empty());
}

#[test]
fn test_event_bus_stats_defaults() {
    let stats = EventBusStats::default();
    assert_eq!(stats.total_published, 0);
    assert_eq!(stats.total_subscribed, 0);
    assert_eq!(stats.total_failed, 0);
    assert_eq!(stats.dlq_size, 0);
}

#[test]
fn test_channel_new() {
    let ch = Channel::new("runtime.state");
    assert_eq!(ch.0, "runtime.state");
}
