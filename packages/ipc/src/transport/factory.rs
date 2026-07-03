//! Transport factory.

use super::transport::{Transport, TransportFactory};
use super::in_memory_transport::InMemoryTransport;

/// Factory for creating transport instances.
#[derive(Debug, Clone, Default)]
pub struct TransportFactoryImpl;

impl TransportFactoryImpl {
    /// Create an in-memory transport.
    pub fn create_in_memory(&self, id: impl Into<String>) -> Box<dyn Transport> {
        Box::new(InMemoryTransport::new(id))
    }
}

impl TransportFactory for TransportFactoryImpl {
    fn create_transport(&self, id: &str) -> Box<dyn Transport> {
        Box::new(InMemoryTransport::new(id))
    }

    fn factory_name(&self) -> &str {
        "in-memory"
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_factory_creates_transport() {
        let factory = TransportFactoryImpl::default();
        let transport = factory.create_transport("test-1");
        assert_eq!(transport.transport_id(), "test-1");
        assert_eq!(factory.factory_name(), "in-memory");
    }
}
