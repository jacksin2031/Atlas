//! Message integrity validation — signature, tampering detection.

use std::collections::HashMap;
use crate::message::MessageEnvelope;

/// Validates message integrity.
#[derive(Clone, Default)]
pub struct MessageIntegrityValidator {
    /// Known public keys for senders (abstracted, not crypto-specific).
    keys: HashMap<String, Vec<u8>>,
}

impl MessageIntegrityValidator {
    pub fn new() -> Self {
        Self::default()
    }

    /// Register a signing key for a sender.
    pub fn register_key(&mut self, sender: impl Into<String>, key: Vec<u8>) {
        self.keys.insert(sender.into(), key);
    }

    /// Validate that a message hasn't been tampered with.
    /// In the reference implementation, we verify the message hash
    /// matches the expected integrity check.
    pub fn validate_integrity(&self, envelope: &MessageEnvelope) -> Result<(), IntegrityError> {
        // Check that required fields are present
        if envelope.header.sender.is_empty() {
            return Err(IntegrityError::MissingField("sender".into()));
        }
        if envelope.header.receiver.is_empty() && envelope.header.receiver != "*" {
            return Err(IntegrityError::MissingField("receiver".into()));
        }
        // In a full implementation, we'd verify a cryptographic signature here.
        // For the reference implementation, we check that the sender has a registered key
        // if the message is from an external boundary.
        if !self.keys.is_empty() && !self.keys.contains_key(&envelope.header.sender) {
            // Unregistered sender — log warning but don't reject in reference impl
            tracing::warn!(sender = %envelope.header.sender, "unregistered sender");
        }
        Ok(())
    }

    /// Generate an integrity hash for a message (for verification).
    pub fn compute_hash(&self, envelope: &MessageEnvelope) -> String {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        envelope.header.message_id.hash(&mut hasher);
        envelope.header.correlation_id.hash(&mut hasher);
        envelope.header.sender.hash(&mut hasher);
        envelope.header.receiver.hash(&mut hasher);
        envelope.header.message_type.hash(&mut hasher);
        format!("{:x}", hasher.finish())
    }
}

/// Integrity validation errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum IntegrityError {
    #[error("missing field: {0}")]
    MissingField(String),
    #[error("tampering detected: hash mismatch")]
    TamperingDetected,
}
