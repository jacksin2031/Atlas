//! Event Bus implementation tests.

use atlas_runtime::eventbus::EventBusImpl;
use atlas_contracts::{Event, Channel};
use std::sync::{Arc, Mutex};

#[test]
fn test_event_bus_creation() {
    let bus = EventBusImpl::new();
    let stats = bus.get_stats();
    assert_eq!(stats.total_published, 0);
    assert_eq!(stats.total_subscribed, 0);
}

#[test]
fn test_publish_and_subscribe() {
    let mut bus = EventBusImpl::new();
    let received = Arc::new(Mutex::new(Vec::new()));
    let received_clone = received.clone();

    bus.subscribe("test".to_string(), move |event: &Event| {
        received_clone.lock().unwrap().push(event.event_type.clone());
    });

    let event = Event::new(Channel::new("test"), "Hello", serde_json::json!({}));
    bus.publish(Channel::new("test"), event).unwrap();

    assert_eq!(received.lock().unwrap().len(), 1);
    assert_eq!(received.lock().unwrap()[0], "Hello");
}

#[test]
fn test_unsubscribe() {
    let mut bus = EventBusImpl::new();
    let handle = bus.subscribe("chan".to_string(), |_| {});
    bus.unsubscribe(&handle).unwrap();

    let stats = bus.get_stats();
    assert_eq!(stats.total_subscribed, 1);
}

#[test]
fn test_stats_tracking() {
    let mut bus = EventBusImpl::new();
    let event = Event::new(Channel::new("test"), "Test", serde_json::json!({}));
    bus.publish(Channel::new("test"), event).unwrap();

    let stats = bus.get_stats();
    assert_eq!(stats.total_published, 1);
}

#[test]
fn test_publish_ready() {
    let mut bus = EventBusImpl::new();
    bus.publish_ready().unwrap();
    let stats = bus.get_stats();
    assert_eq!(stats.total_published, 1);
}

#[test]
fn test_wildcard_channel_matching() {
    let mut bus = EventBusImpl::new();
    let received = Arc::new(Mutex::new(Vec::new()));
    let received_clone = received.clone();

    bus.subscribe("runtime.*".to_string(), move |event: &Event| {
        received_clone.lock().unwrap().push(event.event_type.clone());
    });

    let event = Event::new(Channel::new("runtime.*"), "Test", serde_json::json!({}));
    bus.publish(Channel::new("runtime.*"), event).unwrap();

    assert_eq!(received.lock().unwrap().len(), 1);
}

