//! The `Transport` trait — platform-independent transport abstraction.

use thiserror::Error;

use crate::message::MessageEnvelope;

/// Result type for transport operations.
pub type TransportResult<T> = Result<T, TransportError>;

/// Transport-level errors.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum TransportError {
    #[error("not connected")]
    NotConnected,
    #[error("connection failed: {0}")]
    ConnectionFailed(String),
    #[error("disconnection failed: {0}")]
    DisconnectionFailed(String),
    #[error("send failed: {0}")]
    SendFailed(String),
    #[error("receive timed out")]
    ReceiveTimeout,
    #[error("already connected")]
    AlreadyConnected,
    #[error("address not found: {0}")]
    AddressNotFound(String),
    #[error("protocol version mismatch: expected {expected}, got {got}")]
    ProtocolVersionMismatch { expected: String, got: String },
    #[error("transport is shutting down")]
    ShuttingDown,
}

/// Transport health states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum TransportHealth {
    Healthy,
    Busy,
    #[default]
    Disconnected,
    Recovering,
    Failed,
}

impl TransportHealth {
    pub fn is_healthy(&self) -> bool {
        matches!(self, Self::Healthy)
    }

    pub fn label(&self) -> &'static str {
        match self {
            Self::Healthy => "healthy",
            Self::Busy => "busy",
            Self::Disconnected => "disconnected",
            Self::Recovering => "recovering",
            Self::Failed => "failed",
        }
    }
}

/// Connection states for the transport lifecycle.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionState {
    Disconnected,
    Connecting,
    Connected,
    Disconnecting,
}

/// The transport trait that all transport implementations MUST satisfy.
///
/// This trait is deliberately platform-independent — it describes the
/// behavioral contract without prescribing any specific mechanism.
pub trait Transport: Send + Sync {
    /// Connect to the transport endpoint.
    fn connect(&mut self) -> TransportResult<()>;

    /// Disconnect from the transport endpoint.
    fn disconnect(&mut self) -> TransportResult<()>;

    /// Check whether the transport is connected.
    fn is_connected(&self) -> bool;

    /// Send a message envelope through the transport.
    fn send(&mut self, envelope: MessageEnvelope) -> TransportResult<()>;

    /// Attempt to receive a message (non-blocking).
    /// Returns `Ok(None)` if no message is available.
    fn try_receive(&mut self) -> TransportResult<Option<MessageEnvelope>>;

    /// Get the current health status.
    fn health(&self) -> TransportHealth;

    /// Get the current connection state.
    fn connection_state(&self) -> ConnectionState;

    /// Get a human-readable identifier for this transport.
    fn transport_id(&self) -> &str;

    /// Get the maximum message size supported by this transport (0 = unlimited).
    fn max_message_size(&self) -> usize {
        0
    }
}

/// Factory trait for creating transports.
pub trait TransportFactory: Send + Sync {
    /// Create a new transport instance.
    fn create_transport(&self, id: &str) -> Box<dyn Transport>;

    /// Get the factory name.
    fn factory_name(&self) -> &str;
}
