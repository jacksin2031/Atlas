//! Workflow bridge — translates workflow events to/from IPC messages.

use super::integration::WorkflowIntegration;
use crate::message::{
    MessageEnvelope, MessageHeader, MessageMetadata, MessagePayload, MessageType,
};

/// Translates workflow events into IPC messages.
pub struct WorkflowBridge {
    workflow_integration: WorkflowIntegration,
}

impl WorkflowBridge {
    pub fn new(workflow_integration: WorkflowIntegration) -> Self {
        Self {
            workflow_integration,
        }
    }

    /// Create an IPC message from a workflow event.
    pub fn event_to_ipc_message(
        &self,
        workflow_id: &str,
        event_data: serde_json::Value,
    ) -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new(
                format!("workflow:{}", workflow_id),
                "runtime",
                MessageType::Event,
                60,
            ),
            payload: MessagePayload::new(event_data).unwrap_or_default(),
            metadata: MessageMetadata::default(),
        }
    }

    /// Validate that a workflow uses IPC for external communication.
    pub fn validate_workflow_communication(&self, workflow_id: &str, target: &str) -> bool {
        self.workflow_integration
            .validate_external_communication(workflow_id, target)
    }
}
