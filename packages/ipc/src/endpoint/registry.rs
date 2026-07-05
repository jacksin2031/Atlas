//! Endpoint registry — registration, lookup, discovery, health checks.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use super::endpoint::{Endpoint, EndpointHealth};

/// Registry for IPC endpoints.
#[derive(Clone)]
pub struct EndpointRegistry {
    endpoints: Arc<Mutex<HashMap<String, Endpoint>>>,
}

impl EndpointRegistry {
    pub fn new() -> Self {
        Self {
            endpoints: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    /// Register an endpoint.
    pub fn register(&self, endpoint: Endpoint) {
        let mut endpoints = self.endpoints.lock().unwrap();
        endpoints.insert(endpoint.id.clone(), endpoint);
    }

    /// Lookup an endpoint by ID.
    pub fn lookup(&self, id: &str) -> Option<Endpoint> {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints.get(id).cloned()
    }

    /// Discover endpoints by capability.
    pub fn discover_by_capability(&self, capability: &str) -> Vec<Endpoint> {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints
            .values()
            .filter(|e| e.descriptor.has_capability(capability))
            .cloned()
            .collect()
    }

    /// Discover endpoints by health status.
    pub fn discover_by_health(&self, health: EndpointHealth) -> Vec<Endpoint> {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints
            .values()
            .filter(|e| e.health_status == health)
            .cloned()
            .collect()
    }

    /// Discover all available endpoints.
    pub fn discover_all(&self) -> Vec<Endpoint> {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints
            .values()
            .filter(|e| e.is_available())
            .cloned()
            .collect()
    }

    /// Update health status for an endpoint.
    pub fn update_health(&self, id: &str, health: EndpointHealth) -> bool {
        let mut endpoints = self.endpoints.lock().unwrap();
        if let Some(endpoint) = endpoints.get_mut(id) {
            endpoint.update_health(health);
            true
        } else {
            false
        }
    }

    /// Deregister an endpoint.
    pub fn deregister(&self, id: &str) -> bool {
        let mut endpoints = self.endpoints.lock().unwrap();
        endpoints.remove(id).is_some()
    }

    /// Deregister endpoints that have failed health checks.
    pub fn deregister_failed(&self) -> Vec<String> {
        let mut endpoints = self.endpoints.lock().unwrap();
        let mut removed = Vec::new();
        endpoints.retain(|id, endpoint| {
            if !endpoint.is_available() {
                removed.push(id.clone());
                false
            } else {
                true
            }
        });
        removed
    }

    /// Get all endpoint IDs.
    pub fn all_ids(&self) -> Vec<String> {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints.keys().cloned().collect()
    }

    /// Get the count of registered endpoints.
    pub fn count(&self) -> usize {
        let endpoints = self.endpoints.lock().unwrap();
        endpoints.len()
    }
}

impl Default for EndpointRegistry {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::EndpointDescriptor;

    #[test]
    fn test_register_and_lookup() {
        let reg = EndpointRegistry::new();
        let desc = EndpointDescriptor::new("test-endpoint");
        let ep = Endpoint::new("ep-1", "addr-1", desc);
        reg.register(ep.clone());
        assert_eq!(reg.lookup("ep-1"), Some(ep));
        assert_eq!(reg.count(), 1);
    }

    #[test]
    fn test_discover_by_capability() {
        let reg = EndpointRegistry::new();
        let desc = EndpointDescriptor::new("ep1").with_capabilities(vec!["compute".into()]);
        reg.register(Endpoint::new("ep-1", "addr-1", desc));
        let results = reg.discover_by_capability("compute");
        assert_eq!(results.len(), 1);
    }

    #[test]
    fn test_deregister() {
        let reg = EndpointRegistry::new();
        reg.register(Endpoint::new(
            "ep-1",
            "addr-1",
            EndpointDescriptor::new("ep1"),
        ));
        assert!(reg.deregister("ep-1"));
        assert!(!reg.deregister("ep-1")); // Already removed
    }
}
