//! Lifecycle manager — deterministic FSM per RFC-0002 §8.

use atlas_contracts::{RuntimeState, StateTransitionError, is_legal_transition};
use std::time::{SystemTime, UNIX_EPOCH};

fn monotonic_now() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_micros() as u64
}

/// Lifecycle manager implementing the Runtime state machine.
pub struct LifecycleManager {
    state: RuntimeState,
    transition_count: u64,
    last_transition_time: u64,
}

impl LifecycleManager {
    pub fn new() -> Self {
        Self {
            state: RuntimeState::Created,
            transition_count: 0,
            last_transition_time: monotonic_now(),
        }
    }

    pub fn transition(&mut self, target: RuntimeState) -> Result<(), StateTransitionError> {
        if !is_legal_transition(self.state, target) {
            return Err(StateTransitionError::IllegalTransition {
                from: self.state,
                to: target,
            });
        }

        let now = monotonic_now();
        if now < self.last_transition_time {
            return Err(StateTransitionError::IllegalTransition {
                from: self.state,
                to: target,
            });
        }

        self.last_transition_time = now;
        self.state = target;
        self.transition_count += 1;
        Ok(())
    }

    pub fn current_state(&self) -> RuntimeState {
        self.state
    }

    pub fn can_transition(&self, target: RuntimeState) -> bool {
        is_legal_transition(self.state, target)
    }

    pub fn transition_count(&self) -> u64 {
        self.transition_count
    }
}

impl Default for LifecycleManager {
    fn default() -> Self {
        Self::new()
    }
}
