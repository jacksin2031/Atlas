//! Route definition and action types.

use serde::{Deserialize, Serialize};

/// Actions the router can take when a rule matches.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RouteAction {
    /// Forward to a specific destination endpoint.
    Forward { destination: String },
    /// Broadcast to all endpoints on the channel.
    Broadcast,
    /// Send to the dead-letter queue.
    DeadLetterQueue,
    /// Drop the message silently.
    Drop,
    /// Apply a custom action identified by name.
    Custom {
        action_name: String,
        params: serde_json::Value,
    },
}

/// A single routing rule.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Route {
    pub id: String,
    pub pattern: String,
    pub destination: Option<String>,
    pub action: RouteAction,
    pub priority: u32,
    pub enabled: bool,
    pub ttl: u64,
}

impl Route {
    pub fn forward(
        id: impl Into<String>,
        pattern: impl Into<String>,
        destination: impl Into<String>,
    ) -> Self {
        let dest = destination.into();
        Self {
            id: id.into(),
            pattern: pattern.into(),
            destination: Some(dest.clone()),
            action: RouteAction::Forward { destination: dest },
            priority: 100,
            enabled: true,
            ttl: 0,
        }
    }

    pub fn broadcast(id: impl Into<String>, pattern: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            pattern: pattern.into(),
            destination: None,
            action: RouteAction::Broadcast,
            priority: 100,
            enabled: true,
            ttl: 0,
        }
    }

    pub fn dead_letter(id: impl Into<String>, pattern: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            pattern: pattern.into(),
            destination: None,
            action: RouteAction::DeadLetterQueue,
            priority: 200,
            enabled: true,
            ttl: 0,
        }
    }

    pub fn is_expired(&self, created_at: std::time::Instant) -> bool {
        if self.ttl == 0 {
            return false;
        }
        created_at.elapsed().as_secs() >= self.ttl
    }
}

/// A group of routes that can be added/removed atomically.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct RuleGroup {
    pub name: String,
    pub routes: Vec<Route>,
}

impl RuleGroup {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            routes: Vec::new(),
        }
    }

    pub fn add_route(&mut self, route: Route) {
        self.routes.push(route);
        self.routes.sort_by_key(|r| r.priority);
    }

    pub fn remove_route(&mut self, route_id: &str) -> bool {
        let before = self.routes.len();
        self.routes.retain(|r| r.id != route_id);
        self.routes.len() < before
    }

    pub fn clear(&mut self) {
        self.routes.clear();
    }

    pub fn len(&self) -> usize {
        self.routes.len()
    }

    pub fn is_empty(&self) -> bool {
        self.routes.is_empty()
    }
}
