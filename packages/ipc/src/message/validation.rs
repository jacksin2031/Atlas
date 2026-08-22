//! Message validation - contract enforcement for every IPC message.

use std::collections::HashSet;
use thiserror::Error;

use super::envelope::MessageEnvelope;
use super::header::MessageHeader;
use super::types::MessageType;

/// Result of a validation pass.
pub type ValidationResult = Result<(), ValidationError>;

/// Validation errors.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ValidationError {
    #[error("missing required field: {0}")]
    MissingField(String),
    #[error("invalid message type: {0}")]
    InvalidMessageType(String),
    #[error("sender is empty")]
    EmptySender,
    #[error("receiver is empty")]
    EmptyReceiver,
    #[error("message has expired")]
    Expired,
    #[error("TTL is zero or negative")]
    InvalidTtl,
    #[error("payload is empty for message type {0}")]
    EmptyPayload(MessageType),
    #[error("message ID is empty/nil")]
    EmptyMessageId,
    #[error("correlation ID is empty/nil")]
    EmptyCorrelationId,
    #[error("version mismatch: expected {expected}, got {actual}")]
    VersionMismatch { expected: String, actual: String },
    #[error("hop count exceeds maximum: {0}")]
    HopCountExceeded(u32),
    #[error("validation failed: {0}")]
    General(String),
}

/// Validates a message envelope against the Atlas IPC contract.
pub struct MessageValidator;

impl MessageValidator {
    pub const MAX_HOP_COUNT: u32 = 255;
    pub const MIN_TTL: u64 = 1;

    pub fn validate(envelope: &MessageEnvelope) -> ValidationResult {
        Self::validate_header(&envelope.header)?;
        Self::validate_type_constraints(&envelope.header, &envelope.payload)?;
        Ok(())
    }

    pub fn validate_header(header: &MessageHeader) -> ValidationResult {
        if header.sender.is_empty() {
            return Err(ValidationError::EmptySender);
        }
        if header.receiver.is_empty() && header.receiver != "*" {
            return Err(ValidationError::EmptyReceiver);
        }
        if header.ttl == 0 {
            return Err(ValidationError::InvalidTtl);
        }
        if header.message_id.is_nil() {
            return Err(ValidationError::EmptyMessageId);
        }
        if header.correlation_id.is_nil() {
            return Err(ValidationError::EmptyCorrelationId);
        }
        Ok(())
    }

    pub fn validate_type_constraints(
        header: &MessageHeader,
        payload: &super::payload::MessagePayload,
    ) -> ValidationResult {
        match header.message_type {
            MessageType::Request | MessageType::Response | MessageType::Command => {
                if payload.is_empty() {
                    return Err(ValidationError::EmptyPayload(header.message_type));
                }
            }
            MessageType::Error => {
                if let Some(obj) = payload.as_object() {
                    if !obj.contains_key("error_code") || !obj.contains_key("error_message") {
                        return Err(ValidationError::General(
                            "Error message must contain error_code and error_message".into(),
                        ));
                    }
                }
            }
            MessageType::Notification
            | MessageType::Broadcast
            | MessageType::Heartbeat
            | MessageType::Event => {}
        }
        Ok(())
    }

    pub fn validate_full(envelope: &MessageEnvelope) -> ValidationResult {
        Self::validate(envelope)?;
        if envelope.metadata.hop_count > Self::MAX_HOP_COUNT {
            return Err(ValidationError::HopCountExceeded(
                envelope.metadata.hop_count,
            ));
        }
        Ok(())
    }

    pub fn validate_message_type(mt: &str) -> ValidationResult {
        match mt {
            "Request" | "Response" | "Command" | "Event" | "Notification" | "Broadcast"
            | "Heartbeat" | "Error" => Ok(()),
            _ => Err(ValidationError::InvalidMessageType(mt.to_string())),
        }
    }

    pub fn validate_extensions(
        extensions: &HashSet<String>,
        required: &HashSet<String>,
    ) -> ValidationResult {
        for field in required {
            if !extensions.contains(field) {
                return Err(ValidationError::MissingField(field.clone()));
            }
        }
        Ok(())
    }
}
