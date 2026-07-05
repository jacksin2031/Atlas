//! Lifecycle transition trait definitions.
//!
//! See RFC-0002 §8 (Runtime State Machine).

use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Runtime lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum RuntimeState {
    Created,
    Initializing,
    Ready,
    Running,
    Paused,
    ShuttingDown,
    Failed,
    Terminated,
}

impl RuntimeState {
    pub fn is_terminal(&self) -> bool {
        matches!(self, RuntimeState::Terminated | RuntimeState::Failed)
    }
}

impl std::fmt::Display for RuntimeState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RuntimeState::Created => write!(f, "Created"),
            RuntimeState::Initializing => write!(f, "Initializing"),
            RuntimeState::Ready => write!(f, "Ready"),
            RuntimeState::Running => write!(f, "Running"),
            RuntimeState::Paused => write!(f, "Paused"),
            RuntimeState::ShuttingDown => write!(f, "ShuttingDown"),
            RuntimeState::Failed => write!(f, "Failed"),
            RuntimeState::Terminated => write!(f, "Terminated"),
        }
    }
}

/// Legal transitions from each state.
pub const LEGAL_TRANSITIONS: &[(RuntimeState, RuntimeState)] = &[
    (RuntimeState::Created, RuntimeState::Initializing),
    (RuntimeState::Initializing, RuntimeState::Ready),
    (RuntimeState::Initializing, RuntimeState::Failed),
    (RuntimeState::Ready, RuntimeState::Running),
    (RuntimeState::Ready, RuntimeState::ShuttingDown),
    (RuntimeState::Ready, RuntimeState::Failed),
    (RuntimeState::Running, RuntimeState::Paused),
    (RuntimeState::Running, RuntimeState::ShuttingDown),
    (RuntimeState::Running, RuntimeState::Failed),
    (RuntimeState::Paused, RuntimeState::Running),
    (RuntimeState::Paused, RuntimeState::ShuttingDown),
    (RuntimeState::Paused, RuntimeState::Failed),
    (RuntimeState::ShuttingDown, RuntimeState::Terminated),
    (RuntimeState::Failed, RuntimeState::Terminated),
];

pub fn is_legal_transition(from: RuntimeState, to: RuntimeState) -> bool {
    LEGAL_TRANSITIONS.iter().any(|&(f, t)| f == from && t == to)
}

/// Error from illegal state transitions.
#[derive(Error, Debug, PartialEq, Clone)]
pub enum StateTransitionError {
    #[error("cannot transition from {from:?} to {to:?}")]
    IllegalTransition {
        from: RuntimeState,
        to: RuntimeState,
    },
}

/// Lifecycle manager trait.
pub trait LifecycleManager: Send + Sync {
    fn transition(&mut self, target: RuntimeState) -> Result<(), StateTransitionError>;
    fn current_state(&self) -> RuntimeState;
    fn can_transition(&self, target: RuntimeState) -> bool;
}
