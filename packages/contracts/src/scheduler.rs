//! Scheduler trait definitions.
//!
//! See RFC-0004 §18 (Exposed Scheduler APIs).

use serde::{Deserialize, Serialize};

/// Unique task identifier.
pub type TaskId = String;

/// Task definition.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskDefinition {
    pub task_id: TaskId,
    pub priority: u8,
    pub task_type: String,
    pub timeout_ms: u64,
    pub max_retries: u8,
    pub payload: serde_json::Value,
}

/// Queue depth per priority level.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueueDepth {
    pub critical: usize,
    pub high: usize,
    pub normal: usize,
    pub low: usize,
    pub background: usize,
}

/// Worker pool status.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkerPoolStatus {
    pub active_workers: usize,
    pub idle_workers: usize,
    pub total_workers: usize,
}

/// Error from scheduler operations.
#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum SchedulerError {
    #[error("task not found: {0}")]
    TaskNotFound(String),
    #[error("queue full")]
    QueueFull,
    #[error("task timeout exceeded")]
    Timeout,
    #[error("backpressure active")]
    Backpressure,
}

/// Controller interface for the task scheduler.
pub trait SchedulerController: Send + Sync {
    fn submit_task(&self, task: TaskDefinition) -> Result<TaskId, SchedulerError>;
    fn cancel_task(&self, task_id: &TaskId) -> Result<(), SchedulerError>;
    fn get_queue_depth(&self) -> QueueDepth;
    fn get_worker_pool_status(&self) -> WorkerPoolStatus;
    fn pause(&self) -> Result<(), SchedulerError>;
    fn resume(&self) -> Result<(), SchedulerError>;
}
