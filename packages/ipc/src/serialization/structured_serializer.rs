//! Structured serializer - separates header, payload, and metadata into distinct sections.

use super::serializer::{SerializationError, SerializeResult, Serializer};
use crate::message::{MessageEnvelope, MessageValidator};

/// Structured serializer that produces a delimited format.
#[derive(Debug, Clone, Default)]
pub struct StructuredSerializer;

const HEADER_PREFIX: &[u8] = b"HDR:";
const PAYLOAD_PREFIX: &[u8] = b"PLD:";
const META_PREFIX: &[u8] = b"META:";

impl StructuredSerializer {
    pub fn new() -> Self {
        Self
    }
}

impl Serializer for StructuredSerializer {
    fn serialize(&self, envelope: &MessageEnvelope) -> SerializeResult<Vec<u8>> {
        MessageValidator::validate(envelope)
            .map_err(|e| SerializationError::ValidationFailed(e.to_string()))?;

        let mut buf = Vec::new();

        let header_json = serde_json::to_vec(&envelope.header)
            .map_err(|e| SerializationError::Serialize(e.to_string()))?;
        buf.extend_from_slice(HEADER_PREFIX);
        buf.extend_from_slice(&(header_json.len() as u32).to_le_bytes());
        buf.extend_from_slice(&header_json);

        let payload_json = serde_json::to_vec(&envelope.payload)
            .map_err(|e| SerializationError::Serialize(e.to_string()))?;
        buf.extend_from_slice(PAYLOAD_PREFIX);
        buf.extend_from_slice(&(payload_json.len() as u32).to_le_bytes());
        buf.extend_from_slice(&payload_json);

        let meta_json = serde_json::to_vec(&envelope.metadata)
            .map_err(|e| SerializationError::Serialize(e.to_string()))?;
        buf.extend_from_slice(META_PREFIX);
        buf.extend_from_slice(&(meta_json.len() as u32).to_le_bytes());
        buf.extend_from_slice(&meta_json);

        Ok(buf)
    }

    fn deserialize(&self, bytes: &[u8]) -> SerializeResult<MessageEnvelope> {
        serde_json::from_slice(bytes).map_err(|e| SerializationError::Deserialize(e.to_string()))
    }

    fn format_name(&self) -> &str {
        "structured"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::message::{MessageHeader, MessageMetadata, MessagePayload, MessageType};

    fn sample_envelope() -> MessageEnvelope {
        MessageEnvelope {
            header: MessageHeader::new("sender-1", "receiver-1", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"key": "value"})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_structured_format_name() {
        assert_eq!(StructuredSerializer::new().format_name(), "structured");
    }

    #[test]
    fn test_structured_serialize_structure() {
        let envelope = sample_envelope();
        let ser = StructuredSerializer::new();
        let bytes = ser.serialize(&envelope).expect("serialize");
        let s = String::from_utf8_lossy(&bytes);
        assert!(s.contains("HDR:"));
        assert!(s.contains("PLD:"));
        assert!(s.contains("META:"));
    }
}
