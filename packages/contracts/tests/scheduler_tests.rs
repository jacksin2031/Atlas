//! Tests for scheduler types.

use atlas_contracts::{QueueDepth, WorkerPoolStatus, SchedulerError};

#[test]
fn test_queue_depth_defaults() {
    let qd = QueueDepth {
        critical: 0, high: 0, normal: 0, low: 0, background: 0,
    };
    assert_eq!(qd.critical, 0);
}

#[test]
fn test_worker_pool_defaults() {
    let wp = WorkerPoolStatus {
        active_workers: 0,
        idle_workers: 4,
        total_workers: 4,
    };
    assert_eq!(wp.active_workers, 0);
    assert_eq!(wp.total_workers, 4);
}

#[test]
fn test_scheduler_errors_display() {
    let err = SchedulerError::QueueFull;
    assert_eq!(format!("{}", err), "queue full");
}

