//! Integration tests for the full runtime lifecycle.

use atlas_common::RuntimeState;
use atlas_runtime::lifecycle::LifecycleManager;

#[test]
fn test_lifecycle_manager_full_boot() {
    let mut lm = LifecycleManager::new();
    assert_eq!(lm.current_state(), RuntimeState::Created);

    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::Running).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Running);
}

#[test]
fn test_lifecycle_full_shutdown() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::Running).unwrap();
    lm.transition(RuntimeState::ShuttingDown).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert!(lm.current_state().is_terminal());
}

#[test]
fn test_shutdown_from_ready() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Ready).unwrap();
    lm.transition(RuntimeState::ShuttingDown).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Terminated);
}

#[test]
fn test_fatal_recovery() {
    let mut lm = LifecycleManager::new();
    lm.transition(RuntimeState::Initializing).unwrap();
    lm.transition(RuntimeState::Failed).unwrap();
    lm.transition(RuntimeState::Terminated).unwrap();
    assert_eq!(lm.current_state(), RuntimeState::Terminated);
}

#[test]
fn test_config_service_missing_file() {
    let result = atlas_runtime::config::ConfigService::new().load("/nonexistent/path.toml");
    assert!(result.is_err());
    assert!(matches!(
        result.unwrap_err(),
        atlas_common::ConfigError::FileNotFound(_)
    ));
}
