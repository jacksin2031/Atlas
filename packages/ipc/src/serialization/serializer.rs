//! The `Serializer` trait — platform-independent serialization abstraction.

use thiserror::Error;

use crate::message::MessageEnvelope;

/// Result type for serialization operations.
pub type SerializeResult<T> = Result<T, SerializationError>;

/// Errors that can occur during serialization or deserialization.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum SerializationError {
    #[error("message validation failed before serialization: {0}")]
    ValidationFailed(String),
    #[error("serialization failed: {0}")]
    Serialize(String),
    #[error("deserialization failed: {0}")]
    Deserialize(String),
    #[error("unsupported message type: {0}")]
    UnsupportedMessageType(String),
    #[error("buffer too small: required {required}, available {available}")]
    BufferTooSmall { required: usize, available: usize },
    #[error("schema not registered: {0}")]
    SchemaNotRegistered(String),
    #[error("compression not supported for this serializer")]
    CompressionNotSupported,
}

/// Trait that all serializers MUST implement.
///
/// The trait is deliberately minimal and platform-independent.
pub trait Serializer: Send + Sync {
    /// Serialize a message envelope to bytes.
    fn serialize(&self, envelope: &MessageEnvelope) -> SerializeResult<Vec<u8>>;

    /// Deserialize bytes back into a message envelope.
    fn deserialize(&self, bytes: &[u8]) -> SerializeResult<MessageEnvelope>;

    /// Return the format name (e.g. "json", "binary", "structured").
    fn format_name(&self) -> &str;

    /// Validate the envelope against a registered schema before serialization.
    fn validate_schema(
        &self,
        _envelope: &MessageEnvelope,
        schema_name: &str,
    ) -> SerializeResult<()> {
        // Default: no schema enforcement. Subtypes may override.
        let _ = schema_name;
        Ok(())
    }

    /// Register a schema for validation.
    fn register_schema(&mut self, _name: &str, _schema: Vec<u8>) {
        // Default: no-op. Subtypes may override.
    }
}
