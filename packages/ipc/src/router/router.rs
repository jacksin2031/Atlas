//! The IPC Router - deterministic message routing engine.

use crate::message::{MessageEnvelope, MessageValidator};
use crate::router::dead_letter_queue::DeadLetterQueue;
use crate::router::discovery::{DiscoveredEndpoint, EndpointDiscovery};
use crate::router::priority_queue::PriorityMessageQueue;
use crate::router::routes::{Route, RouteAction};
use crate::router::rule_engine::{RuleEngine, RuleEvaluation};
use crate::tracing::SpanContext;
use std::sync::{Arc, Mutex};
/// Routing result describing what happened to a message.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RoutingResult {
    Forwarded { destination: String },
    Broadcast { count: usize },
    DeadLetterQueued { reason: String },
    Dropped,
    NoRoute,
    Expired,
}

/// Configuration for the router.
#[derive(Debug, Clone)]
pub struct RouterConfig {
    pub max_queue_size: usize,
    pub dlq_capacity: usize,
    pub max_broadcast_fanout: usize,
    pub enforce_ttl: bool,
    pub max_hop_count: u32,
}

impl Default for RouterConfig {
    fn default() -> Self {
        Self {
            max_queue_size: 10000,
            dlq_capacity: 10000,
            max_broadcast_fanout: 1000,
            enforce_ttl: true,
            max_hop_count: 255,
        }
    }
}

/// Router metrics.
#[derive(Debug, Clone, Default)]
pub struct RouterMetrics {
    pub messages_routed: u64,
    pub messages_dropped: u64,
    pub messages_dead_lettered: u64,
    pub broadcasts_sent: u64,
}

/// The main IPC Router.
pub struct Router {
    config: RouterConfig,
    rule_engine: RuleEngine,
    priority_queue: Mutex<PriorityMessageQueue>,
    dlq: Mutex<DeadLetterQueue>,
    discovery: EndpointDiscovery,
    routing_table_version: Arc<Mutex<u64>>,
    metrics: Arc<Mutex<RouterMetrics>>,
}

impl Router {
    pub fn new() -> Self {
        Self::with_config(RouterConfig::default())
    }

    pub fn with_config(config: RouterConfig) -> Self {
        Self {
            config: config.clone(),
            rule_engine: RuleEngine::new(),
            priority_queue: Mutex::new(PriorityMessageQueue::new(config.max_queue_size)),
            dlq: Mutex::new(DeadLetterQueue::new(config.dlq_capacity)),
            discovery: EndpointDiscovery::new(),
            routing_table_version: Arc::new(Mutex::new(0)),
            metrics: Arc::new(Mutex::new(RouterMetrics::default())),
        }
    }

    pub fn add_route(&mut self, route: Route) {
        self.rule_engine.add_rule(route);
        self.increment_version();
    }

    pub fn add_route_group(&mut self, routes: Vec<Route>) {
        self.rule_engine.add_rules(routes);
        self.increment_version();
    }

    pub fn replace_routes(&mut self, routes: Vec<Route>) {
        self.rule_engine.replace_all(routes);
        self.increment_version();
    }

    pub fn remove_route(&mut self, route_id: &str) -> bool {
        let result = self.rule_engine.remove_rule(route_id);
        if result {
            self.increment_version();
        }
        result
    }

    pub fn routing_table_version(&self) -> u64 {
        *self.routing_table_version.lock().unwrap()
    }

    pub fn discover_endpoint(&self, endpoint: DiscoveredEndpoint) {
        self.discovery.register(endpoint);
    }

    pub fn unregister_endpoint(&self, id: &str) -> bool {
        self.discovery.unregister(id)
    }

    pub fn find_by_capability(&self, capability: &str) -> Vec<DiscoveredEndpoint> {
        self.discovery.find_by_capability(capability)
    }

    pub fn route(&self, mut message: MessageEnvelope) -> RoutingResult {
        if let Err(e) = MessageValidator::validate(&message) {
            tracing::warn!(error = %e, "routing failed: validation error");
            return RoutingResult::DeadLetterQueued {
                reason: e.to_string(),
            };
        }

        if self.config.enforce_ttl && message.is_expired() {
            return RoutingResult::Expired;
        }

        if message.metadata.hop_count >= self.config.max_hop_count {
            return RoutingResult::DeadLetterQueued {
                reason: "max hop count exceeded".into(),
            };
        }

        let eval = self.rule_engine.evaluate(&message);

        match eval {
            RuleEvaluation {
                matched: true,
                route: Some(route),
                ..
            } => {
                match &route.action {
                    RouteAction::Forward { destination } => {
                        message.metadata.increment_hop();
                        // Propagate trace context on each hop
                        if message.metadata.trace_id.is_none() {
                            let ctx = SpanContext::new_root();
                            message.metadata = message
                                .metadata
                                .with_trace(ctx.trace_id.to_string())
                                .with_span(ctx.span_id.to_string());
                        } else {
                            let ctx = SpanContext::new_root();
                            message.metadata = message.metadata.with_span(ctx.span_id.to_string());
                        }
                        {
                            let mut m = self.metrics.lock().unwrap();
                            m.messages_routed += 1;
                        }
                        RoutingResult::Forwarded {
                            destination: destination.clone(),
                        }
                    }
                    RouteAction::Broadcast => {
                        let endpoints = self.discovery.all_endpoints();
                        let fanout =
                            std::cmp::min(endpoints.len(), self.config.max_broadcast_fanout);
                        {
                            let mut m = self.metrics.lock().unwrap();
                            m.broadcasts_sent += 1;
                        }
                        RoutingResult::Broadcast { count: fanout }
                    }
                    RouteAction::DeadLetterQueue => {
                        self.dead_letter(message, "explicit DLQ route".into());
                        RoutingResult::DeadLetterQueued {
                            reason: "explicit DLQ route".into(),
                        }
                    }
                    RouteAction::Drop => {
                        {
                            let mut m = self.metrics.lock().unwrap();
                            m.messages_dropped += 1;
                        }
                        RoutingResult::Dropped
                    }
                    RouteAction::Custom { action_name, .. } => {
                        message.metadata.increment_hop();
                        {
                            let mut m = self.metrics.lock().unwrap();
                            m.messages_routed += 1;
                        }
                        RoutingResult::Forwarded {
                            destination: action_name.clone(),
                        }
                    }
                }
            }
            _ => {
                {
                    let mut m = self.metrics.lock().unwrap();
                    m.messages_dropped += 1;
                }
                RoutingResult::NoRoute
            }
        }
    }

    pub fn queue_message(&self, message: MessageEnvelope) -> bool {
        let mut queue = self.priority_queue.lock().unwrap();
        queue.enqueue(message)
    }

    pub fn dequeue_message(&self) -> Option<MessageEnvelope> {
        let mut queue = self.priority_queue.lock().unwrap();
        queue.dequeue()
    }

    pub fn queue_size(&self) -> usize {
        let queue = self.priority_queue.lock().unwrap();
        queue.len()
    }

    pub fn preempt_if_needed(&self, threshold: usize) {
        let mut queue = self.priority_queue.lock().unwrap();
        queue.preempt_if_needed(threshold);
    }

    pub fn dead_letter(&self, message: MessageEnvelope, reason: String) {
        let mut dlq = self.dlq.lock().unwrap();
        dlq.add(message, reason, 0, 3);
        {
            let mut m = self.metrics.lock().unwrap();
            m.messages_dead_lettered += 1;
        }
    }

    pub fn dlq_stats(&self) -> crate::router::dead_letter_queue::DlqStats {
        let dlq = self.dlq.lock().unwrap();
        dlq.stats()
    }

    pub fn metrics(&self) -> RouterMetrics {
        let m = self.metrics.lock().unwrap();
        m.clone()
    }

    pub fn is_corrupted(&self) -> bool {
        self.rule_engine.rule_count() == 0
    }

    pub fn is_degraded(&self) -> bool {
        self.is_corrupted()
    }

    fn increment_version(&self) {
        let mut version = self.routing_table_version.lock().unwrap();
        *version += 1;
    }
}

impl Default for Router {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessageMetadata, MessagePayload, MessageType};

    fn sample_msg(receiver: &str, msg_type: MessageType) -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender", receiver, msg_type, 60),
            payload: MessagePayload::new(serde_json::json!({"test": true})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_route_forward() {
        let mut router = Router::new();
        router.add_route(Route::forward("r1", "endpoint-A", "dest-A"));
        let msg = sample_msg("endpoint-A", MessageType::Request);
        let result = router.route(msg);
        assert!(matches!(result, RoutingResult::Forwarded { .. }));
    }

    #[test]
    fn test_route_no_match() {
        let mut router = Router::new();
        router.add_route(Route::forward("r1", "endpoint-A", "dest-A"));
        let msg = sample_msg("endpoint-B", MessageType::Request);
        let result = router.route(msg);
        assert!(matches!(result, RoutingResult::NoRoute));
    }

    #[test]
    fn test_routing_table_version_increments() {
        let mut router = Router::new();
        assert_eq!(router.routing_table_version(), 0);
        router.add_route(Route::forward("r1", "A", "dest-A"));
        assert_eq!(router.routing_table_version(), 1);
        router.remove_route("r1");
        assert_eq!(router.routing_table_version(), 2);
    }

    #[test]
    fn test_deterministic_routing() {
        let mut router = Router::new();
        router.add_route(Route::forward("r1", "endpoint-A", "dest-A"));
        let msg = sample_msg("endpoint-A", MessageType::Request);
        let r1 = router.route(msg.clone());
        let r2 = router.route(msg);
        assert_eq!(r1, r2);
    }

    #[test]
    fn test_priority_queue() {
        let router = Router::new();
        let critical = sample_msg("dest", MessageType::Command);
        let critical = MessageEnvelope {
            metadata: critical
                .metadata
                .with_priority(crate::message::MessagePriority::Critical),
            ..critical
        };
        let low = sample_msg("dest", MessageType::Notification);
        let low = MessageEnvelope {
            metadata: low
                .metadata
                .with_priority(crate::message::MessagePriority::Low),
            ..low
        };
        router.queue_message(low);
        router.queue_message(critical);
        let next = router.dequeue_message().unwrap();
        assert_eq!(
            next.metadata.priority,
            crate::message::MessagePriority::Critical
        );
    }
}
