//! Plugin bridge — translates plugin events to/from IPC messages.

use super::integration::PluginIntegration;
use crate::message::{
    MessageEnvelope, MessageHeader, MessageMetadata, MessagePayload, MessageType,
};

/// Translates plugin events into IPC messages.
pub struct PluginBridge {
    plugin_integration: PluginIntegration,
}

impl PluginBridge {
    pub fn new(plugin_integration: PluginIntegration) -> Self {
        Self { plugin_integration }
    }

    /// Create an IPC message from a plugin event.
    pub fn event_to_ipc_message(
        &self,
        plugin_id: &str,
        event_data: serde_json::Value,
    ) -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new(
                format!("plugin:{}", plugin_id),
                "runtime",
                MessageType::Event,
                60,
            ),
            payload: MessagePayload::new(event_data).unwrap_or_default(),
            metadata: MessageMetadata::default(),
        }
    }

    /// Validate that a plugin message came through IPC.
    pub fn validate_plugin_message(&self, sender: &str) -> bool {
        self.plugin_integration
            .validate_ipc_communication(sender, "runtime")
    }

    /// Register a plugin for IPC enforcement.
    pub fn register_plugin(&self, plugin_id: impl Into<String>) {
        self.plugin_integration.register_plugin(plugin_id);
    }
}
