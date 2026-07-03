//! Endpoint descriptor - declares endpoint properties.

use serde::{Deserialize, Serialize};

/// Descriptor for an IPC endpoint.
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct EndpointDescriptor {
    pub name: String,
    pub capabilities: Vec<String>,
    pub required_permissions: Vec<String>,
    pub supported_message_types: Vec<String>,
    pub requires_authentication: bool,
    pub max_message_size: usize,
}

impl EndpointDescriptor {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            ..Default::default()
        }
    }

    pub fn with_capabilities(mut self, capabilities: Vec<String>) -> Self {
        self.capabilities = capabilities;
        self
    }

    pub fn with_permissions(mut self, permissions: Vec<String>) -> Self {
        self.required_permissions = permissions;
        self
    }

    pub fn with_message_types(mut self, types: Vec<String>) -> Self {
        self.supported_message_types = types;
        self
    }

    pub fn with_auth(mut self, required: bool) -> Self {
        self.requires_authentication = required;
        self
    }

    pub fn with_max_size(mut self, size: usize) -> Self {
        self.max_message_size = size;
        self
    }

    pub fn has_capability(&self, capability: &str) -> bool {
        self.capabilities.iter().any(|c| c == capability)
    }

    pub fn supports_message_type(&self, msg_type: &str) -> bool {
        self.supported_message_types.is_empty() ||
        self.supported_message_types.iter().any(|t| t == msg_type)
    }
}
