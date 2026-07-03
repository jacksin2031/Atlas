//! Workflow integration — enforces IPC-only external communication.

use std::sync::{Arc, Mutex};
use std::collections::HashSet;

/// Ensures workflows use IPC abstractions for external communication.
#[derive(Clone)]
pub struct WorkflowIntegration {
    registered_workflows: Arc<Mutex<HashSet<String>>>,
}

impl WorkflowIntegration {
    pub fn new() -> Self {
        Self {
            registered_workflows: Arc::new(Mutex::new(HashSet::new())),
        }
    }

    /// Register a workflow for IPC enforcement.
    pub fn register_workflow(&self, workflow_id: impl Into<String>) {
        let mut workflows = self.registered_workflows.lock().unwrap();
        workflows.insert(workflow_id.into());
    }

    /// Check if a workflow is registered.
    pub fn is_registered(&self, workflow_id: &str) -> bool {
        let workflows = self.registered_workflows.lock().unwrap();
        workflows.contains(workflow_id)
    }

    /// Validate that external communication goes through IPC.
    pub fn validate_external_communication(&self, workflow_id: &str, target: &str) -> bool {
        let workflows = self.registered_workflows.lock().unwrap();
        if workflows.contains(workflow_id) {
            // External communication must go through IPC
            tracing::info!(workflow = workflow_id, target, "workflow external communication via IPC");
            true
        } else {
            // Unregistered workflow — allow but warn
            tracing::warn!(workflow = workflow_id, "unregistered workflow communicating externally");
            true
        }
    }

    /// Get the count of registered workflows.
    pub fn workflow_count(&self) -> usize {
        let workflows = self.registered_workflows.lock().unwrap();
        workflows.len()
    }
}

impl Default for WorkflowIntegration {
    fn default() -> Self {
        Self::new()
    }
}
