//! Scheduler implementation.

use crate::eventbus::EventBusImpl;
use atlas_contracts::{QueueDepth, SchedulerError, TaskDefinition, TaskId, WorkerPoolStatus};

#[allow(dead_code)]
/// Task scheduler.
pub struct SchedulerImpl {
    event_bus: &'static EventBusImpl,
    paused: bool,
    queue_depth: QueueDepth,
    worker_pool: WorkerPoolStatus,
}

impl SchedulerImpl {
    pub fn new(event_bus: &EventBusImpl) -> Self {
        unsafe {
            Self {
                event_bus: std::mem::transmute(event_bus),
                paused: false,
                queue_depth: QueueDepth {
                    critical: 0,
                    high: 0,
                    normal: 0,
                    low: 0,
                    background: 0,
                },
                worker_pool: WorkerPoolStatus {
                    active_workers: 0,
                    idle_workers: 4,
                    total_workers: 4,
                },
            }
        }
    }

    pub fn submit_task(&mut self, task: TaskDefinition) -> Result<TaskId, SchedulerError> {
        if self.paused {
            return Err(SchedulerError::Backpressure);
        }
        match task.priority {
            0 => self.queue_depth.critical += 1,
            1 => self.queue_depth.high += 1,
            2 => self.queue_depth.normal += 1,
            3 => self.queue_depth.low += 1,
            _ => self.queue_depth.background += 1,
        }
        Ok(task.task_id)
    }

    pub fn cancel_task(&mut self, _task_id: &TaskId) -> Result<(), SchedulerError> {
        Ok(())
    }

    pub fn get_queue_depth(&self) -> QueueDepth {
        self.queue_depth.clone()
    }

    pub fn get_worker_pool_status(&self) -> WorkerPoolStatus {
        self.worker_pool.clone()
    }

    pub fn pause(&mut self) -> Result<(), SchedulerError> {
        self.paused = true;
        Ok(())
    }

    pub fn resume(&mut self) -> Result<(), SchedulerError> {
        self.paused = false;
        Ok(())
    }

    pub fn is_paused(&self) -> bool {
        self.paused
    }
}
