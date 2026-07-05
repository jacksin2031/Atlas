//! Message envelope — the complete, immutable container for every IPC message.
//!
//! Combines a [MessageHeader](crate::message::header::MessageHeader),
//! [MessagePayload](crate::message::payload::MessagePayload), and
//! [MessageMetadata](crate::message::metadata::MessageMetadata) into a single
//! envelope that flows through the entire IPC runtime.

use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::header::MessageHeader;
use super::metadata::MessageMetadata;
use super::payload::MessagePayload;
use super::priority::MessagePriority;
use super::types::MessageType;

/// The complete, immutable message envelope used throughout the Atlas IPC runtime.
///
/// Every field is `pub` and `Clone` so the envelope can be inspected at every
/// stage of the routing pipeline without mutation.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MessageEnvelope {
    /// Fixed header with routing and identification fields.
    pub header: MessageHeader,
    /// Arbitrary application payload.
    pub payload: MessagePayload,
    /// Routing, tracing, and extension metadata.
    pub metadata: MessageMetadata,
}

// --- Constructors -----------------------------------------------------------

impl MessageEnvelope {
    /// Create a new envelope from constituent parts.
    pub fn new(header: MessageHeader, payload: MessagePayload, metadata: MessageMetadata) -> Self {
        Self {
            header,
            payload,
            metadata,
        }
    }

    /// Convenience constructor with a typed payload.
    pub fn with_payload<T: serde::Serialize>(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        message_type: MessageType,
        correlation_id: Uuid,
        ttl: u64,
        payload_value: T,
    ) -> Result<Self, super::payload::PayloadError> {
        Ok(Self {
            header: MessageHeader::with_correlation(
                sender,
                receiver,
                message_type,
                correlation_id,
                ttl,
            ),
            payload: MessagePayload::new(payload_value)?,
            metadata: MessageMetadata::default(),
        })
    }

    /// Convenience constructor for fire-and-forget messages.
    pub fn fire_and_forget(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        message_type: MessageType,
        payload_value: impl serde::Serialize,
    ) -> Result<Self, super::payload::PayloadError> {
        Self::with_payload(
            sender,
            receiver,
            message_type,
            Uuid::new_v4(),
            60,
            payload_value,
        )
    }

    /// Convenience constructor for a heartbeat.
    pub fn heartbeat(sender: impl Into<String>) -> Self {
        Self {
            header: MessageHeader::new(sender, "*", MessageType::Heartbeat, 30),
            payload: MessagePayload::empty(),
            metadata: MessageMetadata::default(),
        }
    }

    /// Convenience constructor for a request.
    pub fn request(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        payload_value: impl serde::Serialize,
    ) -> Result<Self, super::payload::PayloadError> {
        let corr = Uuid::new_v4();
        Ok(Self {
            header: MessageHeader::with_correlation(
                sender,
                receiver,
                MessageType::Request,
                corr,
                30,
            ),
            payload: MessagePayload::new(payload_value)?,
            metadata: MessageMetadata::default(),
        })
    }

    /// Convenience constructor for a response correlating to a request.
    pub fn response(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        correlation_id: Uuid,
        payload_value: impl serde::Serialize,
    ) -> Result<Self, super::payload::PayloadError> {
        Ok(Self {
            header: MessageHeader::with_correlation(
                sender,
                receiver,
                MessageType::Response,
                correlation_id,
                60,
            ),
            payload: MessagePayload::new(payload_value)?,
            metadata: MessageMetadata::default(),
        })
    }

    /// Convenience constructor for an error message.
    pub fn error(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        correlation_id: Uuid,
        error_code: impl Into<String>,
        error_message: impl Into<String>,
    ) -> Self {
        let payload = serde_json::json!({
            "error_code": error_code.into(),
            "error_message": error_message.into(),
        });
        Self {
            header: MessageHeader::with_correlation(
                sender,
                receiver,
                MessageType::Error,
                correlation_id,
                60,
            ),
            payload: MessagePayload::from_value(payload),
            metadata: MessageMetadata::default(),
        }
    }

    // --- Accessors ------------------------------------------------------------

    /// Returns the message type.
    pub fn message_type(&self) -> MessageType {
        self.header.message_type
    }

    /// Returns the message priority (derived from metadata).
    pub fn priority(&self) -> MessagePriority {
        self.metadata.priority
    }

    /// Returns the sender identifier.
    pub fn sender(&self) -> &str {
        &self.header.sender
    }

    /// Returns the receiver identifier.
    pub fn receiver(&self) -> &str {
        &self.header.receiver
    }

    /// Returns the correlation ID.
    pub fn correlation_id(&self) -> &Uuid {
        self.header.correlation_id()
    }

    /// Returns the message ID.
    pub fn message_id(&self) -> &Uuid {
        self.header.message_id()
    }

    /// Check whether this message has expired.
    pub fn is_expired(&self) -> bool {
        self.header.is_expired_now()
    }

    /// Returns a human-readable summary for logging.
    pub fn summary(&self) -> String {
        format!(
            "[{}] {} from={} to={} corr={}",
            self.header.message_type,
            self.header.message_id,
            self.header.sender,
            self.header.receiver,
            self.header.correlation_id,
        )
    }
}

// --- Display ----------------------------------------------------------------

impl core::fmt::Display for MessageEnvelope {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.summary())
    }
}
