//! Request and response types.

use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Request lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum RequestState {
    Pending,
    Sent,
    Responded,
    TimedOut,
    Cancelled,
}

/// A request message sent through the IPC runtime.
#[derive(Debug, Clone, Serialize)]
pub struct Request {
    pub id: Uuid,
    pub correlation_id: Uuid,
    pub sender: String,
    pub receiver: String,
    pub payload: serde_json::Value,
    pub timeout_secs: u64,
    pub state: RequestState,
    cancelled: bool,
}

impl Request {
    pub fn new(sender: impl Into<String>, receiver: impl Into<String>, payload: serde_json::Value) -> Self {
        Self {
            id: Uuid::new_v4(),
            correlation_id: Uuid::new_v4(),
            sender: sender.into(),
            receiver: receiver.into(),
            payload,
            timeout_secs: 30,
            state: RequestState::Pending,
            cancelled: false,
        }
    }

    pub fn with_timeout(mut self, timeout_secs: u64) -> Self {
        self.timeout_secs = timeout_secs;
        self
    }

    pub fn mark_sent(&mut self) {
        self.state = RequestState::Sent;
    }

    pub fn mark_responded(&mut self) {
        self.state = RequestState::Responded;
    }

    pub fn mark_timed_out(&mut self) {
        self.state = RequestState::TimedOut;
    }

    pub fn mark_cancelled(&mut self) {
        self.state = RequestState::Cancelled;
        self.cancelled = true;
    }

    pub fn is_cancelled(&self) -> bool {
        self.cancelled
    }

    pub fn correlation_id(&self) -> &Uuid {
        &self.correlation_id
    }
}

/// A response message correlating to a request.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Response {
    pub correlation_id: Uuid,
    pub result: Option<serde_json::Value>,
    pub error: Option<String>,
}

impl Response {
    pub fn success(correlation_id: Uuid, result: impl Into<serde_json::Value>) -> Self {
        Self {
            correlation_id,
            result: Some(result.into()),
            error: None,
        }
    }

    pub fn error(correlation_id: Uuid, error: impl Into<String>) -> Self {
        Self {
            correlation_id,
            result: None,
            error: Some(error.into()),
        }
    }

    pub fn is_success(&self) -> bool {
        self.error.is_none()
    }

    pub fn is_error(&self) -> bool {
        self.error.is_some()
    }
}
