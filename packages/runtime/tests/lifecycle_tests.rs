//! Lifecycle manager tests.

use atlas_runtime::lifecycle::LifecycleManager;
use atlas_common::{RuntimeState, StateTransitionError};

#[test]
fn test_initial_state_is_created() {
    let lm = LifecycleManager::new();
    assert_eq!(lm.current_state(), RuntimeState::Created);
    assert_eq!(lm.transition_count(), 0);
}

#[test]
fn test_successful_boot_sequence() {
    let mut lm = LifecycleManager::new();

    lm.transition(RuntimeState::Initializing).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Initializing);

    lm.transition(RuntimeState::Ready).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Ready);

    lm.transition(RuntimeState::Running).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Running);

    assert_eq!(lm.transition_count(), 3);
}

#[test]
fn test_pause_resume_cycle() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::Running).unwrap();
    lm.transition(RuntimeState::Paused).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Paused);

    lm.transition(RuntimeState::Running).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Running);
}

#[test]
fn test_graceful_shutdown() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::Running).unwrap();
    lm.transition(RuntimeState::ShuttingDown).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Terminated);
}

#[test]
fn test_illegal_transition_from_created() {
    let mut lm = LifecycleManager::new();
    let result = lm.transition(RuntimeState::Running);
    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err(),
        StateTransitionError::IllegalTransition {
            from: RuntimeState::Created,
            to: RuntimeState::Running,
        }
    );
}

#[test]
fn test_can_transition_checks() {
    let lm = LifecycleManager::new();
    assert!(lm.can_transition(RuntimeState::Initializing));
    assert!(!lm.can_transition(RuntimeState::Running));
    assert!(!lm.can_transition(RuntimeState::Ready));
}

#[test]
fn test_failed_to_terminated() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Failed).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Terminated);
}

#[test]
fn test_no_transition_from_terminated() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::ShuttingDown).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert!(lm.current_state().is_terminal());

    assert!(!lm.can_transition(RuntimeState::Running));
}
