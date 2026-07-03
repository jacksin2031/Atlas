//! In-memory reference transport implementation.
//!
//! Provides a thread-safe, single-process transport suitable for testing
//! and for the reference implementation.  Messages are delivered via
//! interior-mutex channels with no platform-specific IPC primitives.

use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

use super::transport::{
    Transport, TransportError, TransportResult, TransportHealth, ConnectionState,
};
use crate::message::MessageEnvelope;

/// In-memory transport that delivers messages through interior channels.
///
/// Multiple `InMemoryTransport` instances can be connected to each other
/// by sharing the same message store.
#[derive(Clone)]
pub struct InMemoryTransport {
    id: String,
    state: Arc<Mutex<TransportState>>,
    message_store: Arc<MessageStore>,
}

#[derive(Debug, Clone)]
struct TransportState {
    connected: bool,
    health: TransportHealth,
    max_message_size: usize,
}

/// Shared message store for connecting transports.
#[derive(Debug, Default)]
pub struct MessageStore {
    inbound: Arc<Mutex<VecDeque<MessageEnvelope>>>,
}

impl MessageStore {
    fn push(&self, msg: MessageEnvelope) {
        let mut store = self.inbound.lock().unwrap();
        store.push_back(msg);
    }

    fn pop(&self) -> Option<MessageEnvelope> {
        let mut store = self.inbound.lock().unwrap();
        store.pop_front()
    }


}

impl InMemoryTransport {
    /// Create a new in-memory transport with the given ID.
    pub fn new(id: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            state: Arc::new(Mutex::new(TransportState {
                connected: false,
                health: TransportHealth::Disconnected,
                max_message_size: 0,
            })),
            message_store: Arc::new(MessageStore::default()),
        }
    }

    /// Create a transport connected to a shared message store.
    pub fn with_shared_store(id: impl Into<String>, store: Arc<MessageStore>) -> Self {
        Self {
            id: id.into(),
            state: Arc::new(Mutex::new(TransportState {
                connected: false,
                health: TransportHealth::Disconnected,
                max_message_size: 0,
            })),
            message_store: store,
        }
    }

    /// Get the shared message store (for connecting two transports).
    pub fn shared_store(&self) -> Arc<MessageStore> {
        self.message_store.clone()
    }
}

impl Transport for InMemoryTransport {
    fn connect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if state.connected {
            return Err(TransportError::AlreadyConnected);
        }
        state.connected = true;
        state.health = TransportHealth::Healthy;
        tracing::info!(transport = %self.id, "InMemoryTransport connected");
        Ok(())
    }

    fn disconnect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if !state.connected {
            return Err(TransportError::NotConnected);
        }
        state.connected = false;
        state.health = TransportHealth::Disconnected;
        tracing::info!(transport = %self.id, "InMemoryTransport disconnected");
        Ok(())
    }

    fn is_connected(&self) -> bool {
        let state = self.state.lock().unwrap();
        state.connected
    }

    fn send(&mut self, envelope: MessageEnvelope) -> TransportResult<()> {
        let state = self.state.lock().unwrap();
        if !state.connected {
            return Err(TransportError::NotConnected);
        }
        // Check max message size
        if state.max_message_size > 0 {
            let serialized = serde_json::to_vec(&envelope)
                .map_err(|e| TransportError::SendFailed(e.to_string()))?;
            if serialized.len() > state.max_message_size {
                return Err(TransportError::SendFailed(
                    "message exceeds max size".into(),
                ));
            }
        }
        drop(state);
        // Deliver to store
        self.message_store.push(envelope);
        Ok(())
    }

    fn try_receive(&mut self) -> TransportResult<Option<MessageEnvelope>> {
        let state = self.state.lock().unwrap();
        if !state.connected {
            return Err(TransportError::NotConnected);
        }
        drop(state);
        Ok(self.message_store.pop())
    }

    fn health(&self) -> TransportHealth {
        let state = self.state.lock().unwrap();
        state.health
    }

    fn connection_state(&self) -> ConnectionState {
        let state = self.state.lock().unwrap();
        if state.connected {
            ConnectionState::Connected
        } else {
            ConnectionState::Disconnected
        }
    }

    fn transport_id(&self) -> &str {
        &self.id
    }

    fn max_message_size(&self) -> usize {
        let state = self.state.lock().unwrap();
        state.max_message_size
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_msg() -> MessageEnvelope {
        use crate::message::{MessageHeader, MessagePayload, MessageMetadata, MessageType};
        MessageEnvelope {
            header: MessageHeader::new("sender", "receiver", MessageType::Request, 60),
            payload: MessagePayload::new(serde_json::json!({"test": true})).unwrap(),
            metadata: MessageMetadata::default(),
        }
    }

    #[test]
    fn test_connect_disconnect() {
        let mut t = InMemoryTransport::new("test");
        assert!(!t.is_connected());
        assert_eq!(t.connection_state(), ConnectionState::Disconnected);
        t.connect().unwrap();
        assert!(t.is_connected());
        assert_eq!(t.connection_state(), ConnectionState::Connected);
        t.disconnect().unwrap();
        assert!(!t.is_connected());
    }

    #[test]
    fn test_send_receive() {
        let mut t = InMemoryTransport::new("test");
        t.connect().unwrap();
        let msg = sample_msg();
        t.send(msg.clone()).unwrap();
        let received = t.try_receive().unwrap().unwrap();
        assert_eq!(msg, received);
        t.disconnect().unwrap();
    }

    #[test]
    fn test_try_receive_none_when_empty() {
        let mut t = InMemoryTransport::new("test");
        t.connect().unwrap();
        assert!(t.try_receive().unwrap().is_none());
        t.disconnect().unwrap();
    }

    #[test]
    fn test_send_without_connect_fails() {
        let mut t = InMemoryTransport::new("test");
        assert!(t.send(sample_msg()).is_err());
    }

    #[test]
    fn test_double_connect_fails() {
        let mut t = InMemoryTransport::new("test");
        t.connect().unwrap();
        assert!(t.connect().is_err());
        t.disconnect().unwrap();
    }

    #[test]
    fn test_health_states() {
        let mut t = InMemoryTransport::new("test");
        assert_eq!(t.health(), TransportHealth::Disconnected);
        t.connect().unwrap();
        assert_eq!(t.health(), TransportHealth::Healthy);
        t.disconnect().unwrap();
        assert_eq!(t.health(), TransportHealth::Disconnected);
    }

    #[test]
    fn test_shared_store_inter_process() {
        let store = Arc::new(MessageStore::default());
        let mut sender = InMemoryTransport::with_shared_store("A", store.clone());
        let mut receiver = InMemoryTransport::with_shared_store("B", store);

        sender.connect().unwrap();
        receiver.connect().unwrap();

        let msg = sample_msg();
        sender.send(msg.clone()).unwrap();

        let received = receiver.try_receive().unwrap().unwrap();
        assert_eq!(msg, received);
    }
}

