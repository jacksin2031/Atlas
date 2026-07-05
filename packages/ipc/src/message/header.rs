//! Message header containing routing, identification, and lifecycle metadata.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::types::MessageType;

/// Canonical message version enforced by the runtime.
pub const MESSAGE_VERSION: &str = "1.0.0";

/// Immutable header attached to every message envelope.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct MessageHeader {
    /// Unique message identifier (UUID v4).
    pub message_id: Uuid,
    /// Correlation identifier linking request/response pairs.
    pub correlation_id: Uuid,
    /// UTC timestamp when the header was created.
    pub timestamp: DateTime<Utc>,
    /// Protocol version string (currently "1.0.0").
    pub version: String,
    /// Sender endpoint identifier.
    pub sender: String,
    /// Receiver endpoint identifier.
    pub receiver: String,
    /// Semantic type of the message.
    pub message_type: MessageType,
    /// Time-to-live in seconds.
    pub ttl: u64,
    /// Bit-flag field for auxiliary properties.
    pub flags: u32,
}

/// Header flag bits.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct MessageFlags {
    bits: u32,
}

impl MessageFlags {
    /// Flag: message is idempotent.
    pub const IDEMPOTENT: u32 = 1 << 0;
    /// Flag: message must be acknowledged by the receiver.
    pub const REQUIRES_ACK: u32 = 1 << 1;
    /// Flag: message is compressed.
    pub const COMPRESSED: u32 = 1 << 2;
    /// Flag: message carries a trace context.
    pub const TRACEABLE: u32 = 1 << 3;

    pub fn new() -> Self {
        Self { bits: 0 }
    }

    pub fn contains(&self, flag: u32) -> bool {
        (self.bits & flag) != 0
    }

    pub fn set(&mut self, flag: u32) {
        self.bits |= flag;
    }

    pub fn clear(&mut self, flag: u32) {
        self.bits &= !flag;
    }

    pub fn bits(&self) -> u32 {
        self.bits
    }
}

impl Default for MessageFlags {
    fn default() -> Self {
        Self::new()
    }
}

impl MessageHeader {
    /// Create a new header with random IDs.
    pub fn new(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        message_type: MessageType,
        ttl: u64,
    ) -> Self {
        Self {
            message_id: Uuid::new_v4(),
            correlation_id: Uuid::new_v4(),
            timestamp: Utc::now(),
            version: MESSAGE_VERSION.to_string(),
            sender: sender.into(),
            receiver: receiver.into(),
            message_type,
            ttl,
            flags: 0,
        }
    }

    /// Create a header tied to an existing correlation.
    pub fn with_correlation(
        sender: impl Into<String>,
        receiver: impl Into<String>,
        message_type: MessageType,
        correlation_id: Uuid,
        ttl: u64,
    ) -> Self {
        Self {
            correlation_id,
            ..Self::new(sender, receiver, message_type, ttl)
        }
    }

    /// Check whether this message has expired relative to the given time.
    pub fn is_expired(&self, now: DateTime<Utc>) -> bool {
        let expiry = self
            .timestamp
            .checked_add_signed(chrono::Duration::seconds(self.ttl as i64))
            .unwrap_or(Utc::now());
        now >= expiry
    }

    /// Check whether this message has expired relative to the current time.
    pub fn is_expired_now(&self) -> bool {
        self.is_expired(Utc::now())
    }

    pub fn correlation_id(&self) -> &Uuid {
        &self.correlation_id
    }

    pub fn message_id(&self) -> &Uuid {
        &self.message_id
    }
}

impl Default for MessageHeader {
    fn default() -> Self {
        Self::new("unknown", "unknown", MessageType::Heartbeat, 30)
    }
}

impl core::fmt::Display for MessageHeader {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(
            f,
            "MessageHeader(id={}, corr={}, type={}, sender={}, receiver={})",
            self.message_id, self.correlation_id, self.message_type, self.sender, self.receiver
        )
    }
}
