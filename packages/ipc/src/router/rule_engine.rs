//! Rule engine for evaluating routing rules against messages.

use crate::message::MessageEnvelope;
use super::routes::{Route, RouteAction};

/// Result of a rule evaluation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RuleEvaluation {
    pub matched: bool,
    pub route: Option<Route>,
    pub failure_reason: Option<String>,
}

impl RuleEvaluation {
    pub fn matched(route: Route) -> Self {
        Self {
            matched: true,
            route: Some(route),
            failure_reason: None,
        }
    }

    pub fn no_match() -> Self {
        Self {
            matched: false,
            route: None,
            failure_reason: None,
        }
    }

    pub fn failed(reason: impl Into<String>) -> Self {
        Self {
            matched: false,
            route: None,
            failure_reason: Some(reason.into()),
        }
    }
}

/// Evaluates routing rules against messages.
#[derive(Debug, Clone, Default)]
pub struct RuleEngine {
    rules: Vec<Route>,
}

impl RuleEngine {
    /// Create a new rule engine.
    pub fn new() -> Self {
        Self {
            rules: Vec::new(),
        }
    }

    /// Add a rule to the engine.
    pub fn add_rule(&mut self, route: Route) {
        self.rules.push(route);
        self.rules.sort_by_key(|r| r.priority);
    }

    /// Add a batch of rules from a group.
    pub fn add_rules(&mut self, routes: Vec<Route>) {
        for route in routes {
            self.add_rule(route);
        }
    }

    /// Remove a rule by ID.
    pub fn remove_rule(&mut self, route_id: &str) -> bool {
        let before = self.rules.len();
        self.rules.retain(|r| r.id != route_id);
        self.rules.len() < before
    }

    /// Atomically replace all rules (for rule group operations).
    pub fn replace_all(&mut self, routes: Vec<Route>) {
        self.rules = routes;
        self.rules.sort_by_key(|r| r.priority);
    }

    /// Evaluate a message against all rules, returning the first match.
    pub fn evaluate(&self, message: &MessageEnvelope) -> RuleEvaluation {
        for route in &self.rules {
            if !route.enabled {
                continue;
            }
            if self.matches_pattern(route, message) {
                return RuleEvaluation::matched(route.clone());
            }
        }
        RuleEvaluation::no_match()
    }

    /// Check whether a route pattern matches a message.
    fn matches_pattern(&self, route: &Route, message: &MessageEnvelope) -> bool {
        // Pattern matching: exact match, wildcard "*", or prefix match with "*" suffix
        let pattern = &route.pattern;
        if pattern == "*" {
            return true;
        }
        if pattern.ends_with("*") {
            let prefix = &pattern[..pattern.len() - 1];
            return message.header.receiver.starts_with(prefix)
                || message.header.message_type.label().starts_with(prefix);
        }
        // Exact match on receiver or message type
        *pattern == message.header.receiver
            || pattern == message.header.message_type.label()
    }

    /// Get the resolved action for a matched route.
    pub fn resolve_action(&self, route: &Route, message: &MessageEnvelope) -> Option<RouteAction> {
        if !route.enabled {
            return None;
        }
        if !self.matches_pattern(route, message) {
            return None;
        }
        Some(route.action.clone())
    }

    /// Get all active rules sorted by priority.
    pub fn active_rules(&self) -> Vec<&Route> {
        self.rules.iter().filter(|r| r.enabled).collect()
    }

    /// Get the number of rules.
    pub fn rule_count(&self) -> usize {
        self.rules.len()
    }

    /// Log evaluation failure (tracing).
    pub fn log_evaluation_failure(&self, message: &MessageEnvelope, reason: &str) {
        tracing::warn!(
            message_id = ?message.header.message_id,
            correlation_id = ?message.header.correlation_id,
            reason = reason,
            "rule evaluation failed"
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessagePayload, MessageMetadata, MessageType};

    fn sample_msg(receiver: &str, msg_type: MessageType) -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender", receiver, msg_type, 60),
            payload: MessagePayload::new(serde_json::json!({"test": true})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_exact_pattern_match() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "endpoint-A", "dest-A"));
        let msg = sample_msg("endpoint-A", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(eval.matched);
        assert_eq!(eval.route.as_ref().unwrap().destination, Some("dest-A".into()));
    }

    #[test]
    fn test_wildcard_match() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "*", "default-dest"));
        let msg = sample_msg("any-endpoint", MessageType::Event);
        let eval = engine.evaluate(&msg);
        assert!(eval.matched);
    }

    #[test]
    fn test_prefix_match() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "svc-*", "service-dest"));
        let msg = sample_msg("svc-alpha", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(eval.matched);
    }

    #[test]
    fn test_no_match() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "endpoint-A", "dest-A"));
        let msg = sample_msg("endpoint-B", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(!eval.matched);
    }

    #[test]
    fn test_disabled_rule_not_matched() {
        let mut engine = RuleEngine::new();
        let mut route = Route::forward("r1", "endpoint-A", "dest-A");
        route.enabled = false;
        engine.add_rule(route);
        let msg = sample_msg("endpoint-A", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(!eval.matched);
    }

    #[test]
    fn test_rule_priority_ordering() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("low", "endpoint-A", "low-dest"));
        engine.rules.last_mut().unwrap().priority = 200;
        engine.add_rule(Route::forward("high", "endpoint-A", "high-dest"));
        engine.rules.first_mut().unwrap().priority = 10;
        let msg = sample_msg("endpoint-A", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(eval.matched);
        assert_eq!(eval.route.as_ref().unwrap().destination, Some("high-dest".into()));
    }

    #[test]
    fn test_remove_rule() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "endpoint-A", "dest-A"));
        assert_eq!(engine.rule_count(), 1);
        engine.remove_rule("r1");
        assert_eq!(engine.rule_count(), 0);
    }

    #[test]
    fn test_replace_all_atomic() {
        let mut engine = RuleEngine::new();
        engine.add_rule(Route::forward("r1", "A", "dest-A"));
        engine.add_rule(Route::forward("r2", "B", "dest-B"));
        engine.replace_all(vec![Route::forward("r3", "C", "dest-C")]);
        assert_eq!(engine.rule_count(), 1);
        let msg = sample_msg("C", MessageType::Request);
        let eval = engine.evaluate(&msg);
        assert!(eval.matched);
    }
}

