//! Transport adapter interface — extensible transport implementations.
//!
//! Defines the TransportAdapter trait that all transport adapters MUST satisfy.
//! The reference implementation ships InMemoryTransport via the main transport module;
//! named-pipe and network adapters plug in here.

use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};

use super::transport::{
    ConnectionState, Transport, TransportError, TransportHealth, TransportResult,
};
use crate::message::MessageEnvelope;

/// Supported transport adapter kinds.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum TransportKind {
    InProcess,
    NamedPipe,
    Tcp,
    Udp,
    WebSocket,
    Grpc,
}

impl TransportKind {
    pub fn label(&self) -> &str {
        match self {
            Self::InProcess => "in-process",
            Self::NamedPipe => "named-pipe",
            Self::Tcp => "tcp",
            Self::Udp => "udp",
            Self::WebSocket => "websocket",
            Self::Grpc => "grpc",
        }
    }
}

/// Adapter metadata describing a transport implementation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransportAdapterInfo {
    pub kind: TransportKind,
    pub name: String,
    pub version: String,
    pub description: String,
}

impl TransportAdapterInfo {
    pub fn new(
        kind: TransportKind,
        name: impl Into<String>,
        version: impl Into<String>,
        description: impl Into<String>,
    ) -> Self {
        Self {
            kind,
            name: name.into(),
            version: version.into(),
            description: description.into(),
        }
    }
}

/// A transport adapter is a Transport with additional factory metadata.
pub trait TransportAdapter: Transport {
    /// Return static info about this adapter.
    fn adapter_info(&self) -> TransportAdapterInfo;

    /// Create a new instance of this adapter type with the given ID.
    fn create(id: impl Into<String>) -> Box<dyn TransportAdapter>
    where
        Self: Sized;
}

/// Named pipe transport adapter — Windows IPC via named pipes.
///
/// Reference implementation provides a skeleton; full implementation
/// requires windows crate for CreateFile/ReadFile/WriteFile.
#[derive(Clone)]
pub struct NamedPipeTransport {
    id: String,
    state: Arc<Mutex<TransportState>>,
    #[allow(dead_code)]
    pipe_name: String,
}

#[derive(Debug, Clone)]
struct TransportState {
    connected: bool,
    health: TransportHealth,
}

impl NamedPipeTransport {
    pub fn new(id: impl Into<String>, pipe_name: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            state: Arc::new(Mutex::new(TransportState {
                connected: false,
                health: TransportHealth::Disconnected,
            })),
            pipe_name: pipe_name.into(),
        }
    }
}

impl TransportAdapter for NamedPipeTransport {
    fn adapter_info(&self) -> TransportAdapterInfo {
        TransportAdapterInfo::new(
            TransportKind::NamedPipe,
            &self.id,
            "0.1.0",
            "Windows named pipe transport adapter",
        )
    }

    fn create(id: impl Into<String>) -> Box<dyn TransportAdapter> {
        let id_str = id.into();
        Box::new(Self::new(
            id_str.clone(),
            format!("\\\\.\\pipe\\atlas-{id_str}"),
        ))
    }
}

impl Transport for NamedPipeTransport {
    fn connect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if state.connected {
            return Err(TransportError::AlreadyConnected);
        }
        state.connected = true;
        state.health = TransportHealth::Healthy;
        Ok(())
    }

    fn disconnect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if !state.connected {
            return Err(TransportError::NotConnected);
        }
        state.connected = false;
        state.health = TransportHealth::Disconnected;
        Ok(())
    }

    fn is_connected(&self) -> bool {
        let state = self.state.lock().unwrap();
        state.connected
    }

    fn send(&mut self, _envelope: MessageEnvelope) -> TransportResult<()> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        // Named pipe write would go here in full implementation
        Ok(())
    }

    fn try_receive(&mut self) -> TransportResult<Option<MessageEnvelope>> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        // Named pipe read would go here in full implementation
        Ok(None)
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
}

/// TCP transport adapter — implements the TransportAdapter trait for TCP/IP.
#[derive(Clone)]
pub struct TcpTransport {
    id: String,
    addr: String,
    state: Arc<Mutex<TransportState>>,
}

impl TcpTransport {
    pub fn new(id: impl Into<String>, addr: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            addr: addr.into(),
            state: Arc::new(Mutex::new(TransportState {
                connected: false,
                health: TransportHealth::Disconnected,
            })),
        }
    }
}

impl TransportAdapter for TcpTransport {
    fn adapter_info(&self) -> TransportAdapterInfo {
        TransportAdapterInfo::new(
            TransportKind::Tcp,
            &self.id,
            "0.1.0",
            format!("TCP transport to {}", self.addr),
        )
    }

    fn create(id: impl Into<String>) -> Box<dyn TransportAdapter>
    where
        Self: Sized,
    {
        Box::new(Self::new(id, "127.0.0.1:0"))
    }
}

impl Transport for TcpTransport {
    fn connect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if state.connected {
            return Err(TransportError::AlreadyConnected);
        }
        state.connected = true;
        state.health = TransportHealth::Healthy;
        Ok(())
    }
    fn disconnect(&mut self) -> TransportResult<()> {
        let mut state = self.state.lock().unwrap();
        if !state.connected {
            return Err(TransportError::NotConnected);
        }
        state.connected = false;
        state.health = TransportHealth::Disconnected;
        Ok(())
    }
    fn is_connected(&self) -> bool {
        let s = self.state.lock().unwrap();
        s.connected
    }
    fn send(&mut self, _envelope: MessageEnvelope) -> TransportResult<()> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        Ok(())
    }
    fn try_receive(&mut self) -> TransportResult<Option<MessageEnvelope>> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        Ok(None)
    }
    fn health(&self) -> TransportHealth {
        let s = self.state.lock().unwrap();
        s.health
    }
    fn connection_state(&self) -> ConnectionState {
        let s = self.state.lock().unwrap();
        if s.connected {
            ConnectionState::Connected
        } else {
            ConnectionState::Disconnected
        }
    }
    fn transport_id(&self) -> &str {
        &self.id
    }
}

/// WebSocket transport adapter — implements the TransportAdapter trait for WebSocket.
#[derive(Clone)]
pub struct WebSocketTransport {
    id: String,
    url: String,
    state: Arc<Mutex<TransportState>>,
}

impl WebSocketTransport {
    pub fn new(id: impl Into<String>, url: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            url: url.into(),
            state: Arc::new(Mutex::new(TransportState {
                connected: false,
                health: TransportHealth::Disconnected,
            })),
        }
    }
}

impl TransportAdapter for WebSocketTransport {
    fn adapter_info(&self) -> TransportAdapterInfo {
        TransportAdapterInfo::new(
            TransportKind::WebSocket,
            &self.id,
            "0.1.0",
            format!("WS to {}", self.url),
        )
    }
    fn create(id: impl Into<String>) -> Box<dyn TransportAdapter>
    where
        Self: Sized,
    {
        Box::new(Self::new(id, "ws://127.0.0.1:0"))
    }
}

impl Transport for WebSocketTransport {
    fn connect(&mut self) -> TransportResult<()> {
        let mut s = self.state.lock().unwrap();
        if s.connected {
            return Err(TransportError::AlreadyConnected);
        }
        s.connected = true;
        s.health = TransportHealth::Healthy;
        Ok(())
    }
    fn disconnect(&mut self) -> TransportResult<()> {
        let mut s = self.state.lock().unwrap();
        if !s.connected {
            return Err(TransportError::NotConnected);
        }
        s.connected = false;
        s.health = TransportHealth::Disconnected;
        Ok(())
    }
    fn is_connected(&self) -> bool {
        let s = self.state.lock().unwrap();
        s.connected
    }
    fn send(&mut self, _envelope: MessageEnvelope) -> TransportResult<()> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        Ok(())
    }
    fn try_receive(&mut self) -> TransportResult<Option<MessageEnvelope>> {
        if !self.is_connected() {
            return Err(TransportError::NotConnected);
        }
        Ok(None)
    }
    fn health(&self) -> TransportHealth {
        let s = self.state.lock().unwrap();
        s.health
    }
    fn connection_state(&self) -> ConnectionState {
        let s = self.state.lock().unwrap();
        if s.connected {
            ConnectionState::Connected
        } else {
            ConnectionState::Disconnected
        }
    }
    fn transport_id(&self) -> &str {
        &self.id
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_named_pipe_adapter_info() {
        let tp = NamedPipeTransport::new("np-1", "test-pipe");
        let info = tp.adapter_info();
        assert_eq!(info.kind, TransportKind::NamedPipe);
        assert_eq!(info.name, "np-1");
    }

    #[test]
    fn test_tcp_adapter_info() {
        let tp = TcpTransport::new("tcp-1", "127.0.0.1:8080");
        let info = tp.adapter_info();
        assert_eq!(info.kind, TransportKind::Tcp);
        assert!(info.description.contains("8080"));
    }

    #[test]
    fn test_websocket_adapter_info() {
        let tp = WebSocketTransport::new("ws-1", "ws://localhost:3000");
        let info = tp.adapter_info();
        assert_eq!(info.kind, TransportKind::WebSocket);
    }

    #[test]
    fn test_transport_kind_labels() {
        assert_eq!(TransportKind::InProcess.label(), "in-process");
        assert_eq!(TransportKind::NamedPipe.label(), "named-pipe");
        assert_eq!(TransportKind::Tcp.label(), "tcp");
        assert_eq!(TransportKind::Udp.label(), "udp");
        assert_eq!(TransportKind::WebSocket.label(), "websocket");
        assert_eq!(TransportKind::Grpc.label(), "grpc");
    }

    #[test]
    fn test_named_pipe_lifecycle() {
        let mut tp = NamedPipeTransport::new("np-1", "test");
        assert_eq!(tp.health(), TransportHealth::Disconnected);
        tp.connect().unwrap();
        assert!(tp.is_connected());
        assert_eq!(tp.health(), TransportHealth::Healthy);
        tp.disconnect().unwrap();
        assert!(!tp.is_connected());
    }

    #[test]
    fn test_tcp_lifecycle() {
        let mut tp = TcpTransport::new("tcp-1", "127.0.0.1:9090");
        tp.connect().unwrap();
        assert!(tp.is_connected());
        tp.disconnect().unwrap();
    }

    #[test]
    fn test_websocket_lifecycle() {
        let mut tp = WebSocketTransport::new("ws-1", "ws://localhost");
        tp.connect().unwrap();
        assert!(tp.is_connected());
        tp.disconnect().unwrap();
    }

    #[test]
    fn test_double_connect_fails() {
        let mut tp = NamedPipeTransport::new("np-1", "test");
        tp.connect().unwrap();
        assert!(tp.connect().is_err());
    }
}
