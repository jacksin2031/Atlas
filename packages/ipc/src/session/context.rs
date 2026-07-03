//! Session context attached to IPC messages.

use serde::{Deserialize, Serialize};

/// Context attached to every IPC message for session tracking.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionContext {
    pub session_id: Option<uuid::Uuid>,
    pub user_id: String,
    pub authentication_token: Option<String>,
    pub bound_channels: Vec<String>,
    pub bound_endpoints: Vec<String>,
}

impl SessionContext {
    pub fn new(user_id: impl Into<String>) -> Self {
        Self {
            session_id: None,
            user_id: user_id.into(),
            authentication_token: None,
            bound_channels: Vec::new(),
            bound_endpoints: Vec::new(),
        }
    }

    pub fn with_session(mut self, session_id: uuid::Uuid) -> Self {
        self.session_id = Some(session_id);
        self
    }

    pub fn with_token(mut self, token: impl Into<String>) -> Self {
        self.authentication_token = Some(token.into());
        self
    }

    pub fn bind_channel(&mut self, channel_id: impl Into<String>) {
        self.bound_channels.push(channel_id.into());
    }

    pub fn bind_endpoint(&mut self, endpoint_id: impl Into<String>) {
        self.bound_endpoints.push(endpoint_id.into());
    }

    pub fn unbind_channel(&mut self, channel_id: &str) {
        self.bound_channels.retain(|c| c != channel_id);
    }

    pub fn unbind_endpoint(&mut self, endpoint_id: &str) {
        self.bound_endpoints.retain(|e| e != endpoint_id);
    }
}
