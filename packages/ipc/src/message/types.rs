//! Message type enumeration.
//!
//! Defines the eight canonical message types used throughout the Atlas IPC runtime.

use serde::{Deserialize, Serialize};

/// The eight canonical message types in the Atlas IPC runtime.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[non_exhaustive]
pub enum MessageType {
    /// A request message expecting a response.
    Request,
    /// A response message correlating to a Request.
    Response,
    /// A command message instructing a service to perform an action.
    Command,
    /// An event message broadcast to interested subscribers.
    Event,
    /// A notification — fire-and-forget informational message.
    Notification,
    /// A broadcast message delivered to all endpoints on a channel.
    Broadcast,
    /// A heartbeat probe for liveness detection.
    Heartbeat,
    /// An error message carrying diagnostic information.
    Error,
}

impl MessageType {
    /// Returns true if this message type expects a response.
    pub fn expects_response(self) -> bool {
        matches!(self, Self::Request)
    }

    /// Returns true if this message type is fire-and-forget.
    pub fn is_fire_and_forget(self) -> bool {
        matches!(self, Self::Notification | Self::Broadcast | Self::Heartbeat)
    }

    /// Returns a human-readable label for telemetry and logging.
    pub fn label(self) -> &'static str {
        match self {
            Self::Request => "request",
            Self::Response => "response",
            Self::Command => "command",
            Self::Event => "event",
            Self::Notification => "notification",
            Self::Broadcast => "broadcast",
            Self::Heartbeat => "heartbeat",
            Self::Error => "error",
        }
    }
}

impl core::fmt::Display for MessageType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.label())
    }
}

impl Default for MessageType {
    fn default() -> Self {
        Self::Request
    }
}
