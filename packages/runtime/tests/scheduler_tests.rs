//! Scheduler tests.

use atlas_contracts::{SchedulerError, TaskDefinition};
use atlas_runtime::eventbus::EventBusImpl;
use atlas_runtime::scheduler::SchedulerImpl;

fn make_scheduler() -> (SchedulerImpl, EventBusImpl) {
    let event_bus = EventBusImpl::new();
    let scheduler = SchedulerImpl::new(&event_bus);
    (scheduler, event_bus)
}

#[test]
fn test_submit_task() {
    let (mut scheduler, _eb) = make_scheduler();
    let task = TaskDefinition {
        task_id: "t1".to_string(),
        priority: 2,
        task_type: "compute".to_string(),
        timeout_ms: 5000,
        max_retries: 3,
        payload: serde_json::json!({}),
    };
    let id = scheduler.submit_task(task).unwrap();
    assert_eq!(id, "t1");
}

#[test]
fn test_queue_depth_on_submit() {
    let (mut scheduler, _eb) = make_scheduler();
    let task = TaskDefinition {
        task_id: "t1".to_string(),
        priority: 0,
        task_type: "critical".to_string(),
        timeout_ms: 1000,
        max_retries: 0,
        payload: serde_json::json!({}),
    };
    scheduler.submit_task(task).unwrap();
    let depth = scheduler.get_queue_depth();
    assert_eq!(depth.critical, 1);
}

#[test]
fn test_cancel_task() {
    let (mut scheduler, _eb) = make_scheduler();
    let result = scheduler.cancel_task(&"t1".to_string());
    assert!(result.is_ok());
}

#[test]
fn test_pause_and_resume() {
    let (mut scheduler, _eb) = make_scheduler();
    assert!(!scheduler.is_paused());

    scheduler.pause().unwrap();
    assert!(scheduler.is_paused());

    // Submitting while paused returns backpressure error
    let task = TaskDefinition {
        task_id: "t2".to_string(),
        priority: 2,
        task_type: "test".to_string(),
        timeout_ms: 1000,
        max_retries: 0,
        payload: serde_json::json!({}),
    };
    assert_eq!(
        scheduler.submit_task(task).unwrap_err(),
        SchedulerError::Backpressure
    );

    scheduler.resume().unwrap();
    assert!(!scheduler.is_paused());
}

#[test]
fn test_worker_pool_defaults() {
    let (scheduler, _eb) = make_scheduler();
    let status = scheduler.get_worker_pool_status();
    assert_eq!(status.total_workers, 4);
    assert_eq!(status.idle_workers, 4);
    assert_eq!(status.active_workers, 0);
}
