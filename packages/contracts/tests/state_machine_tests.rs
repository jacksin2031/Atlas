//! Tests for the runtime state machine.

use atlas_contracts::{is_legal_transition, RuntimeState, LEGAL_TRANSITIONS};

#[test]
fn test_initial_state_is_created() {
    assert!(is_legal_transition(
        RuntimeState::Created,
        RuntimeState::Initializing
    ));
}

#[test]
fn test_legal_transitions() {
    assert!(is_legal_transition(
        RuntimeState::Created,
        RuntimeState::Initializing
    ));
    assert!(is_legal_transition(
        RuntimeState::Initializing,
        RuntimeState::Ready
    ));
    assert!(is_legal_transition(
        RuntimeState::Initializing,
        RuntimeState::Failed
    ));
    assert!(is_legal_transition(
        RuntimeState::Ready,
        RuntimeState::Running
    ));
    assert!(is_legal_transition(
        RuntimeState::Ready,
        RuntimeState::ShuttingDown
    ));
    assert!(is_legal_transition(
        RuntimeState::Running,
        RuntimeState::Paused
    ));
    assert!(is_legal_transition(
        RuntimeState::Running,
        RuntimeState::ShuttingDown
    ));
    assert!(is_legal_transition(
        RuntimeState::Paused,
        RuntimeState::Running
    ));
    assert!(is_legal_transition(
        RuntimeState::Paused,
        RuntimeState::ShuttingDown
    ));
    assert!(is_legal_transition(
        RuntimeState::ShuttingDown,
        RuntimeState::Terminated
    ));
    assert!(is_legal_transition(
        RuntimeState::Failed,
        RuntimeState::Terminated
    ));
}

#[test]
fn test_illegal_transitions() {
    assert!(!is_legal_transition(
        RuntimeState::Created,
        RuntimeState::Running
    ));
    assert!(!is_legal_transition(
        RuntimeState::Created,
        RuntimeState::Ready
    ));
    assert!(!is_legal_transition(
        RuntimeState::Running,
        RuntimeState::Created
    ));
    assert!(!is_legal_transition(
        RuntimeState::Paused,
        RuntimeState::Created
    ));
    assert!(!is_legal_transition(
        RuntimeState::Terminated,
        RuntimeState::Running
    ));
    assert!(!is_legal_transition(
        RuntimeState::Failed,
        RuntimeState::Ready
    ));
    assert!(!is_legal_transition(
        RuntimeState::ShuttingDown,
        RuntimeState::Running
    ));
}

#[test]
fn test_terminal_states() {
    assert!(RuntimeState::Terminated.is_terminal());
    assert!(RuntimeState::Failed.is_terminal());
    assert!(!RuntimeState::Created.is_terminal());
    assert!(!RuntimeState::Ready.is_terminal());
    assert!(!RuntimeState::Running.is_terminal());
}

#[test]
fn test_display() {
    assert_eq!(format!("{}", RuntimeState::Created), "Created");
    assert_eq!(format!("{}", RuntimeState::Running), "Running");
    assert_eq!(format!("{}", RuntimeState::Terminated), "Terminated");
}

#[test]
fn test_transition_count_matches_legal_transitions() {
    assert_eq!(LEGAL_TRANSITIONS.len(), 14);
}
