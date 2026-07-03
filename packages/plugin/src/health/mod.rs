//! Plugin health monitoring (RFC-0210 §14, RFC-0205 §14).
//!
//! Defines the plugin health state model, the [`PluginHealthMonitor`] contract,
//! and an in-memory implementation. Plugin health is integrated with the
//! Runtime Health Service (RFC-0003 §16) via the [`to_runtime_status`]
//! conversion so the runtime can aggregate plugin health alongside service
//! health.
//!
//! All state is held behind a [`Mutex`] inside the monitor instance shared via
//! dependency injection — no global mutable state is used.

use crate::capability::PluginId;
use crate::error::HealthError;
use atlas_contracts::HealthStatus;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fmt;
use std::sync::Mutex;

/// Plugin health states (RFC-0210 §14).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PluginHealthState {
    Healthy,
    Degraded(String),
    Recovering(String),
    Disabled,
    Failed(String),
}

impl PluginHealthState {
    /// Severity rank used for worst-case aggregation (higher is worse).
    ///
    /// `Disabled` plugins are intentionally excluded from worst-case
    /// aggregation (a disabled plugin is not an active health problem), so its
    /// rank is lower than `Failed`/`Degraded`.
    pub fn severity(&self) -> u8 {
        match self {
            Self::Healthy => 0,
            Self::Disabled => 1,
            Self::Recovering(_) => 2,
            Self::Degraded(_) => 3,
            Self::Failed(_) => 4,
        }
    }

    pub fn is_healthy(&self) -> bool {
        matches!(self, Self::Healthy)
    }
}

impl fmt::Display for PluginHealthState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Healthy => write!(f, "Healthy"),
            Self::Degraded(msg) => write!(f, "Degraded({msg})"),
            Self::Recovering(msg) => write!(f, "Recovering({msg})"),
            Self::Disabled => write!(f, "Disabled"),
            Self::Failed(msg) => write!(f, "Failed({msg})"),
        }
    }
}

/// Convert a plugin health state into a runtime [`HealthStatus`] so the
/// Runtime Health Service can aggregate it (RFC-0003 §16).
pub fn to_runtime_status(state: &PluginHealthState) -> HealthStatus {
    match state {
        PluginHealthState::Healthy => HealthStatus::Healthy,
        PluginHealthState::Degraded(msg) => HealthStatus::Degraded(msg.clone()),
        PluginHealthState::Recovering(msg) => HealthStatus::Degraded(format!("recovering: {msg}")),
        PluginHealthState::Failed(msg) => HealthStatus::Unhealthy(msg.clone()),
        PluginHealthState::Disabled => HealthStatus::Disabled,
    }
}

/// The plugin health monitor contract.
pub trait PluginHealthMonitor: Send + Sync {
    /// Record the health state for a plugin.
    fn record(&self, plugin_id: &PluginId, state: PluginHealthState) -> Result<(), HealthError>;
    /// Query the health state of a plugin.
    fn health_of(&self, plugin_id: &PluginId) -> Option<PluginHealthState>;
    /// Aggregate the health of all monitored plugins (worst-case semantics).
    fn aggregate(&self) -> PluginHealthState;
    /// Return all recorded `(plugin_id, state)` pairs.
    fn all(&self) -> Vec<(PluginId, PluginHealthState)>;
    /// Remove a plugin from monitoring.
    fn remove(&self, plugin_id: &PluginId);
}
/// In-memory implementation of [`PluginHealthMonitor`].
pub struct PluginHealthServiceImpl {
    states: Mutex<HashMap<PluginId, PluginHealthState>>,
}

impl PluginHealthServiceImpl {
    pub fn new() -> Self {
        Self { states: Mutex::new(HashMap::new()) }
    }
}

impl Default for PluginHealthServiceImpl {
    fn default() -> Self {
        Self::new()
    }
}

impl PluginHealthMonitor for PluginHealthServiceImpl {
    fn record(&self, plugin_id: &PluginId, state: PluginHealthState) -> Result<(), HealthError> {
        let mut states = self.states.lock().expect("plugin health mutex poisoned");
        states.insert(plugin_id.clone(), state);
        Ok(())
    }

    fn health_of(&self, plugin_id: &PluginId) -> Option<PluginHealthState> {
        self.states
            .lock()
            .expect("plugin health mutex poisoned")
            .get(plugin_id)
            .cloned()
    }

    fn aggregate(&self) -> PluginHealthState {
        let states = self.states.lock().expect("plugin health mutex poisoned");
        // Worst-case over non-Disabled plugins. A disabled plugin is not an
        // active health problem and is excluded from the worst-case rollup;
        // if every monitored plugin is disabled, the aggregate is Healthy.
        let mut worst: Option<PluginHealthState> = None;
        for state in states.values() {
            if matches!(state, PluginHealthState::Disabled) {
                continue;
            }
            match &worst {
                None => worst = Some(state.clone()),
                Some(current) if state.severity() > current.severity() => worst = Some(state.clone()),
                _ => {}
            }
        }
        worst.unwrap_or(PluginHealthState::Healthy)
    }

    fn all(&self) -> Vec<(PluginId, PluginHealthState)> {
        self.states
            .lock()
            .expect("plugin health mutex poisoned")
            .iter()
            .map(|(id, s)| (id.clone(), s.clone()))
            .collect()
    }

    fn remove(&self, plugin_id: &PluginId) {
        self.states
            .lock()
            .expect("plugin health mutex poisoned")
            .remove(plugin_id);
    }
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_record_and_query() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"p1".to_string(), PluginHealthState::Healthy).unwrap();
        assert_eq!(mon.health_of(&"p1".to_string()), Some(PluginHealthState::Healthy));
        assert!(mon.health_of(&"p2".to_string()).is_none());
    }

    #[test]
    fn test_aggregate_healthy_when_empty() {
        let mon = PluginHealthServiceImpl::new();
        assert_eq!(mon.aggregate(), PluginHealthState::Healthy);
    }

    #[test]
    fn test_aggregate_worst_case() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"a".to_string(), PluginHealthState::Healthy).unwrap();
        mon.record(&"b".to_string(), PluginHealthState::Degraded("slow".to_string())).unwrap();
        assert!(matches!(mon.aggregate(), PluginHealthState::Degraded(_)));
        mon.record(&"c".to_string(), PluginHealthState::Failed("down".to_string())).unwrap();
        assert!(matches!(mon.aggregate(), PluginHealthState::Failed(_)));
    }

    #[test]
    fn test_aggregate_skips_disabled() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"a".to_string(), PluginHealthState::Disabled).unwrap();
        mon.record(&"b".to_string(), PluginHealthState::Disabled).unwrap();
        assert_eq!(mon.aggregate(), PluginHealthState::Healthy);
    }

    #[test]
    fn test_aggregate_recovering_beats_degraded() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"a".to_string(), PluginHealthState::Recovering("retry".to_string())).unwrap();
        mon.record(&"b".to_string(), PluginHealthState::Degraded("slow".to_string())).unwrap();
        assert!(matches!(mon.aggregate(), PluginHealthState::Degraded(_)));
    }

    #[test]
    fn test_to_runtime_status() {
        assert!(to_runtime_status(&PluginHealthState::Healthy).is_healthy());
        assert!(matches!(
            to_runtime_status(&PluginHealthState::Failed("x".to_string())),
            HealthStatus::Unhealthy(_)
        ));
        assert_eq!(to_runtime_status(&PluginHealthState::Disabled), HealthStatus::Disabled);
    }

    #[test]
    fn test_remove() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"p1".to_string(), PluginHealthState::Healthy).unwrap();
        mon.remove(&"p1".to_string());
        assert!(mon.health_of(&"p1".to_string()).is_none());
    }

    #[test]
    fn test_all_returns_pairs() {
        let mon = PluginHealthServiceImpl::new();
        mon.record(&"a".to_string(), PluginHealthState::Healthy).unwrap();
        mon.record(&"b".to_string(), PluginHealthState::Failed("e".to_string())).unwrap();
        assert_eq!(mon.all().len(), 2);
    }

    #[test]
    fn test_severity_ordering() {
        assert!(PluginHealthState::Failed("x".to_string()).severity() > PluginHealthState::Degraded("y".to_string()).severity());
        assert!(PluginHealthState::Healthy.severity() < PluginHealthState::Recovering("z".to_string()).severity());
    }
}