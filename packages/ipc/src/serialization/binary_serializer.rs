//! Binary serializer - hex-encoded JSON representation.

use super::serializer::{Serializer, SerializeResult, SerializationError};
use crate::message::{MessageEnvelope, MessageValidator};

/// Binary serializer that encodes messages as hex-encoded JSON.
#[derive(Debug, Clone, Default)]
pub struct BinarySerializer;

impl BinarySerializer {
    pub fn new() -> Self {
        Self
    }
}

impl Serializer for BinarySerializer {
    fn serialize(&self, envelope: &MessageEnvelope) -> SerializeResult<Vec<u8>> {
        MessageValidator::validate(envelope).map_err(|e| {
            SerializationError::ValidationFailed(e.to_string())
        })?;

        let json = serde_json::to_vec(envelope).map_err(|e| SerializationError::Serialize(e.to_string()))?;
        let hex_str: String = json.iter().map(|b| format!("{:02x}", b)).collect();
        Ok(hex_str.into_bytes())
    }

    fn deserialize(&self, bytes: &[u8]) -> SerializeResult<MessageEnvelope> {
        let hex_str = String::from_utf8(bytes.to_vec())
            .map_err(|e| SerializationError::Deserialize(e.to_string()))?;
        let json_bytes = hex_decode(&hex_str)
            .map_err(|e| SerializationError::Deserialize(e.to_string()))?;
        serde_json::from_slice(&json_bytes)
            .map_err(|e| SerializationError::Deserialize(e.to_string()))
    }

    fn format_name(&self) -> &str {
        "binary"
    }
}

fn hex_decode(hex: &str) -> Result<Vec<u8>, String> {
    let mut bytes = Vec::with_capacity(hex.len() / 2);
    let mut chars = hex.chars();
    while let Some(hi) = chars.next() {
        let lo = chars.next().ok_or("odd number of hex chars")?;
        let hi_val = hex_char_to_nibble(hi)?;
        let lo_val = hex_char_to_nibble(lo)?;
        bytes.push((hi_val << 4) | lo_val);
    }
    Ok(bytes)
}

fn hex_char_to_nibble(c: char) -> Result<u8, String> {
    match c {
        '0'..='9' => Ok(c as u8 - b'0'),
        'a'..='f' => Ok(c as u8 - b'a' + 10),
        'A'..='F' => Ok(c as u8 - b'A' + 10),
        _ => Err(format!("invalid hex character: {}", c)),
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
    fn test_binary_roundtrip() {
        let original = sample_envelope();
        let ser = BinarySerializer::new();
        let bytes = ser.serialize(&original).expect("serialize");
        let restored = ser.deserialize(&bytes).expect("deserialize");
        assert_eq!(original, restored);
    }

    #[test]
    fn test_binary_format_name() {
        assert_eq!(BinarySerializer::new().format_name(), "binary");
    }
}
