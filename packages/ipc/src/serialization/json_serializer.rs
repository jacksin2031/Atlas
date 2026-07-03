//! JSON serializer — the default reference implementation.

use super::serializer::{Serializer, SerializeResult, SerializationError};
use crate::message::{MessageEnvelope, MessageValidator};

/// JSON-based message serializer.
///
/// Serializes the entire `MessageEnvelope` to a JSON object using serde.
#[derive(Debug, Clone, Default)]
pub struct JsonSerializer;

impl JsonSerializer {
    pub fn new() -> Self {
        Self
    }
}

impl Serializer for JsonSerializer {
    fn serialize(&self, envelope: &MessageEnvelope) -> SerializeResult<Vec<u8>> {
        // Validate before serializing.
        MessageValidator::validate(envelope).map_err(|e| {
            SerializationError::ValidationFailed(e.to_string())
        })?;

        serde_json::to_vec(envelope).map_err(|e| SerializationError::Serialize(e.to_string()))
    }

    fn deserialize(&self, bytes: &[u8]) -> SerializeResult<MessageEnvelope> {
        serde_json::from_slice(bytes).map_err(|e| SerializationError::Deserialize(e.to_string()))
    }

    fn format_name(&self) -> &str {
        "json"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessagePayload, MessageMetadata, MessageType};

    fn sample_envelope() -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender-1", "receiver-1", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"key": "value"})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_json_serialize_deserialize_roundtrip() {
        let original = sample_envelope();
        let ser = JsonSerializer::new();
        let bytes = ser.serialize(&original).expect("serialize");
        let restored = ser.deserialize(&bytes).expect("deserialize");
        assert_eq!(original, restored);
    }

    #[test]
    fn test_json_format_name() {
        assert_eq!(JsonSerializer::new().format_name(), "json");
    }

    #[test]
    fn test_json_validates_before_serialize() {
        let bad = MessageEnvelope {
            header: MessageHeader::new("", "receiver-1", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"key": "value"})).unwrap(),
            metadata: MessageMetadata::default(),
        };
        let ser = JsonSerializer::new();
        assert!(ser.serialize(&bad).is_err());
    }
}
