//! Plugin lifecycle state machine (RFC-0203).
//!
//! Implements the deterministic finite state machine that governs every
//! plugin. The Platform owns state-machine enforcement (RFC-0203 §5); plugin
//! authors own hook implementations. The lifecycle integrates with the Runtime
//! lifecycle (RFC-0002): plugins may only reach active states while the runtime
//! is in a compatible state.
//!
//! Lifecycle states (per the Plugin Runtime scope):
//! `Created → Loaded → Initialized → Started → Running`, with `Paused`,
//! `Stopped`, `Shutdown`, `Disposed`, `Failed`, and `Recovery` completing the
//! machine.

use crate::error::LifecycleError;
use atlas_contracts::RuntimeState;
use serde::{Deserialize, Serialize};
use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

/// Plugin lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PluginState {
    Created,
    Loaded,
    Initialized,
    Started,
    Running,
    Paused,
    Stopped,
    Shutdown,
    Disposed,
    Failed,
    Recovery,
}

impl PluginState {
    /// `Disposed` is the only terminal state.
    pub fn is_terminal(&self) -> bool {
        matches!(self, Self::Disposed)
    }

    /// Whether the plugin is actively executing logic.
    pub fn is_active(&self) -> bool {
        matches!(self, Self::Running)
    }

    /// Broad lifecycle category.
    pub fn category(&self) -> PluginStateCategory {
        match self {
            Self::Created => PluginStateCategory::PreActivation,
            Self::Loaded | Self::Initialized | Self::Started => PluginStateCategory::PreActivation,
            Self::Running => PluginStateCategory::Active,
            Self::Paused => PluginStateCategory::Suspended,
            Self::Stopped | Self::Shutdown | Self::Disposed => PluginStateCategory::Teardown,
            Self::Failed | Self::Recovery => PluginStateCategory::Error,
        }
    }
}

/// Coarse classification of lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PluginStateCategory {
    PreActivation,
    Active,
    Suspended,
    Teardown,
    Error,
}

impl fmt::Display for PluginState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

/// Legal plugin state transitions.
pub const LEGAL_PLUGIN_TRANSITIONS: &[(PluginState, PluginState)] = &[
    (PluginState::Created, PluginState::Loaded),
    (PluginState::Created, PluginState::Failed),
    (PluginState::Created, PluginState::Disposed),
    (PluginState::Loaded, PluginState::Initialized),
    (PluginState::Loaded, PluginState::Failed),
    (PluginState::Loaded, PluginState::Disposed),
    (PluginState::Initialized, PluginState::Started),
    (PluginState::Initialized, PluginState::Failed),
    (PluginState::Initialized, PluginState::Disposed),
    (PluginState::Started, PluginState::Running),
    (PluginState::Started, PluginState::Paused),
    (PluginState::Started, PluginState::Stopped),
    (PluginState::Started, PluginState::Failed),
    (PluginState::Running, PluginState::Paused),
    (PluginState::Running, PluginState::Stopped),
    (PluginState::Running, PluginState::Failed),
    (PluginState::Running, PluginState::Recovery),
    (PluginState::Paused, PluginState::Running),
    (PluginState::Paused, PluginState::Stopped),
    (PluginState::Paused, PluginState::Failed),
    (PluginState::Stopped, PluginState::Shutdown),
    (PluginState::Stopped, PluginState::Disposed),
    (PluginState::Stopped, PluginState::Failed),
    (PluginState::Stopped, PluginState::Recovery),
    (PluginState::Shutdown, PluginState::Disposed),
    (PluginState::Recovery, PluginState::Running),
    (PluginState::Recovery, PluginState::Stopped),
    (PluginState::Recovery, PluginState::Failed),
    (PluginState::Failed, PluginState::Recovery),
    (PluginState::Failed, PluginState::Disposed),
];

/// Whether a transition from `from` to `to` is legal.
pub fn is_legal_plugin_transition(from: PluginState, to: PluginState) -> bool {
    LEGAL_PLUGIN_TRANSITIONS
        .iter()
        .any(|&(f, t)| f == from && t == to)
}
/// Whether a plugin in `plugin_state` may operate given the runtime is in
/// `runtime_state`.
///
/// Integration rule (RFC-0203 §7): plugins MUST NOT be `Running` unless the
/// runtime itself is `Running`. During runtime shutdown/teardown, plugins must
/// be tearing down too.
pub fn is_runtime_compatible(plugin_state: PluginState, runtime_state: RuntimeState) -> bool {
    match plugin_state {
        // Pre-activation plugin states are allowed while the runtime is booting.
        PluginState::Created
        | PluginState::Loaded
        | PluginState::Initialized
        | PluginState::Started => {
            matches!(
                runtime_state,
                RuntimeState::Created
                    | RuntimeState::Initializing
                    | RuntimeState::Ready
                    | RuntimeState::Running
            )
        }
        // A plugin may only run while the runtime is running.
        PluginState::Running => runtime_state == RuntimeState::Running,
        // Paused plugins are allowed while running or paused.
        PluginState::Paused => {
            matches!(runtime_state, RuntimeState::Running | RuntimeState::Paused)
        }
        // Teardown states are always allowed (even during shutdown/terminated).
        PluginState::Stopped
        | PluginState::Shutdown
        | PluginState::Disposed
        | PluginState::Failed
        | PluginState::Recovery => true,
    }
}

fn monotonic_now() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_micros() as u64
}

/// Lifecycle manager enforcing the plugin state machine.
///
/// Each instance tracks a single plugin's state. Transitions are validated
/// against [`LEGAL_PLUGIN_TRANSITIONS`] and against a monotonic clock (a
/// non-monotonic timestamp is rejected, mirroring RFC-0002 §8).
pub struct PluginLifecycleManager {
    state: PluginState,
    transition_count: u64,
    last_transition_time: u64,
}

impl PluginLifecycleManager {
    pub fn new() -> Self {
        Self {
            state: PluginState::Created,
            transition_count: 0,
            last_transition_time: monotonic_now(),
        }
    }

    /// Create a manager whose initial state is `state`.
    pub fn with_state(state: PluginState) -> Self {
        Self {
            state,
            transition_count: 0,
            last_transition_time: monotonic_now(),
        }
    }

    /// Transition to `target`, enforcing legality and monotonic time.
    pub fn transition(&mut self, target: PluginState) -> Result<(), LifecycleError> {
        if !is_legal_plugin_transition(self.state, target) {
            return Err(LifecycleError::IllegalTransition {
                from: self.state,
                to: target,
            });
        }
        let now = monotonic_now();
        if now < self.last_transition_time {
            return Err(LifecycleError::IllegalTransition {
                from: self.state,
                to: target,
            });
        }
        self.last_transition_time = now;
        self.state = target;
        self.transition_count += 1;
        Ok(())
    }

    /// Force the state to `target` without checking transitions.
    ///
    /// Used by recovery procedures (RFC-0203 §14) when the platform must move
    /// a plugin into `Failed` or `Recovery` from an otherwise-illegal state.
    pub fn force(&mut self, target: PluginState) {
        self.last_transition_time = monotonic_now();
        self.state = target;
        self.transition_count += 1;
    }

    pub fn current_state(&self) -> PluginState {
        self.state
    }

    pub fn can_transition(&self, target: PluginState) -> bool {
        is_legal_plugin_transition(self.state, target)
    }

    pub fn transition_count(&self) -> u64 {
        self.transition_count
    }
}

impl Default for PluginLifecycleManager {
    fn default() -> Self {
        Self::new()
    }
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state_created() {
        let m = PluginLifecycleManager::new();
        assert_eq!(m.current_state(), PluginState::Created);
        assert_eq!(m.transition_count(), 0);
    }

    #[test]
    fn test_full_activation_sequence() {
        let mut m = PluginLifecycleManager::new();
        m.transition(PluginState::Loaded).unwrap();
        m.transition(PluginState::Initialized).unwrap();
        m.transition(PluginState::Started).unwrap();
        m.transition(PluginState::Running).unwrap();
        assert_eq!(m.current_state(), PluginState::Running);
        assert!(m.current_state().is_active());
        assert_eq!(m.transition_count(), 4);
    }

    #[test]
    fn test_pause_resume() {
        let mut m = PluginLifecycleManager::new();
        for t in [
            PluginState::Loaded,
            PluginState::Initialized,
            PluginState::Started,
            PluginState::Running,
        ] {
            m.transition(t).unwrap();
        }
        m.transition(PluginState::Paused).unwrap();
        assert_eq!(m.current_state(), PluginState::Paused);
        m.transition(PluginState::Running).unwrap();
        assert_eq!(m.current_state(), PluginState::Running);
    }

    #[test]
    fn test_full_teardown() {
        let mut m = PluginLifecycleManager::new();
        for t in [
            PluginState::Loaded,
            PluginState::Initialized,
            PluginState::Started,
            PluginState::Running,
        ] {
            m.transition(t).unwrap();
        }
        m.transition(PluginState::Stopped).unwrap();
        m.transition(PluginState::Shutdown).unwrap();
        m.transition(PluginState::Disposed).unwrap();
        assert!(m.current_state().is_terminal());
    }

    #[test]
    fn test_illegal_transition_rejected() {
        let mut m = PluginLifecycleManager::new();
        let err = m.transition(PluginState::Running).unwrap_err();
        assert!(matches!(err, LifecycleError::IllegalTransition { .. }));
        assert_eq!(m.current_state(), PluginState::Created);
    }

    #[test]
    fn test_failed_to_recovery_to_running() {
        let mut m = PluginLifecycleManager::with_state(PluginState::Running);
        m.transition(PluginState::Failed).unwrap();
        m.transition(PluginState::Recovery).unwrap();
        m.transition(PluginState::Running).unwrap();
        assert_eq!(m.current_state(), PluginState::Running);
    }

    #[test]
    fn test_force_recovery() {
        let mut m = PluginLifecycleManager::with_state(PluginState::Started);
        m.force(PluginState::Failed);
        assert_eq!(m.current_state(), PluginState::Failed);
    }

    #[test]
    fn test_runtime_compatibility() {
        assert!(is_runtime_compatible(
            PluginState::Running,
            RuntimeState::Running
        ));
        assert!(!is_runtime_compatible(
            PluginState::Running,
            RuntimeState::Created
        ));
        assert!(is_runtime_compatible(
            PluginState::Loaded,
            RuntimeState::Initializing
        ));
        assert!(is_runtime_compatible(
            PluginState::Disposed,
            RuntimeState::Terminated
        ));
        assert!(!is_runtime_compatible(
            PluginState::Paused,
            RuntimeState::Created
        ));
    }

    #[test]
    fn test_can_transition() {
        let m = PluginLifecycleManager::new();
        assert!(m.can_transition(PluginState::Loaded));
        assert!(!m.can_transition(PluginState::Running));
    }

    #[test]
    fn test_state_categories() {
        assert_eq!(
            PluginState::Created.category(),
            PluginStateCategory::PreActivation
        );
        assert_eq!(PluginState::Running.category(), PluginStateCategory::Active);
        assert_eq!(
            PluginState::Paused.category(),
            PluginStateCategory::Suspended
        );
        assert_eq!(
            PluginState::Disposed.category(),
            PluginStateCategory::Teardown
        );
        assert_eq!(PluginState::Failed.category(), PluginStateCategory::Error);
    }
}
