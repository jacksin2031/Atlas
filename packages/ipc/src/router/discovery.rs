//! Endpoint discovery for automatic registration and lookup.

use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Epoch-based timestamp.
type EpochTime = u64;

/// Discovered endpoint information.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscoveredEndpoint {
    pub id: String,
    pub address: String,
    pub capabilities: Vec<String>,
    pub version: String,
    pub registered_epoch: EpochTime,
    pub last_heartbeat_epoch: EpochTime,
}

impl DiscoveredEndpoint {
    pub fn new(id: impl Into<String>, address: impl Into<String>) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            id: id.into(),
            address: address.into(),
            capabilities: Vec::new(),
            version: "1.0.0".to_string(),
            registered_epoch: now,
            last_heartbeat_epoch: now,
        }
    }

    pub fn with_capabilities(mut self, capabilities: Vec<String>) -> Self {
        self.capabilities = capabilities;
        self
    }

    pub fn with_version(mut self, version: impl Into<String>) -> Self {
        self.version = version.into();
        self
    }

    pub fn update_heartbeat(&mut self) {
        self.last_heartbeat_epoch = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
    }

    pub fn is_timed_out(&self, timeout_secs: u64) -> bool {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        now - self.last_heartbeat_epoch > timeout_secs
    }
}

/// Automatic endpoint discovery service.
#[derive(Clone)]
pub struct EndpointDiscovery {
    endpoints: std::sync::Arc<std::sync::Mutex<HashMap<String, DiscoveredEndpoint>>>,
}

impl EndpointDiscovery {
    pub fn new() -> Self {
        Self {
            endpoints: std::sync::Arc::new(std::sync::Mutex::new(HashMap::new())),
        }
    }

    pub fn register(&self, endpoint: DiscoveredEndpoint) {
        let mut map = self.endpoints.lock().unwrap();
        map.insert(endpoint.id.clone(), endpoint);
    }

    pub fn unregister(&self, id: &str) -> bool {
        let mut map = self.endpoints.lock().unwrap();
        map.remove(id).is_some()
    }

    pub fn lookup(&self, id: &str) -> Option<DiscoveredEndpoint> {
        let map = self.endpoints.lock().unwrap();
        map.get(id).cloned()
    }

    pub fn find_by_capability(&self, capability: &str) -> Vec<DiscoveredEndpoint> {
        let map = self.endpoints.lock().unwrap();
        map.values()
            .filter(|ep| ep.capabilities.iter().any(|c| c == capability))
            .cloned()
            .collect()
    }

    pub fn all_endpoints(&self) -> Vec<DiscoveredEndpoint> {
        let map = self.endpoints.lock().unwrap();
        map.values().cloned().collect()
    }

    pub fn update_heartbeat(&self, id: &str) -> bool {
        let mut map = self.endpoints.lock().unwrap();
        if let Some(ep) = map.get_mut(id) {
            ep.update_heartbeat();
            true
        } else {
            false
        }
    }

    pub fn cleanup(&self, timeout_secs: u64) -> Vec<String> {
        let mut map = self.endpoints.lock().unwrap();
        let mut removed = Vec::new();
        map.retain(|id, ep| {
            if ep.is_timed_out(timeout_secs) {
                removed.push(id.clone());
                false
            } else {
                true
            }
        });
        removed
    }

    pub fn count(&self) -> usize {
        let map = self.endpoints.lock().unwrap();
        map.len()
    }
}

impl Default for EndpointDiscovery {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_register_and_lookup() {
        let discovery = EndpointDiscovery::new();
        let ep = DiscoveredEndpoint::new("ep-1", "addr-1");
        discovery.register(ep.clone());
        assert_eq!(discovery.lookup("ep-1"), Some(ep));
        assert_eq!(discovery.lookup("ep-2"), None);
    }

    #[test]
    fn test_unregister() {
        let discovery = EndpointDiscovery::new();
        discovery.register(DiscoveredEndpoint::new("ep-1", "addr-1"));
        assert_eq!(discovery.count(), 1);
        discovery.unregister("ep-1");
        assert_eq!(discovery.count(), 0);
    }

    #[test]
    fn test_find_by_capability() {
        let discovery = EndpointDiscovery::new();
        discovery.register(
            DiscoveredEndpoint::new("ep-1", "addr-1")
                .with_capabilities(vec!["compute".into(), "storage".into()]),
        );
        discovery.register(
            DiscoveredEndpoint::new("ep-2", "addr-2")
                .with_capabilities(vec!["compute".into()]),
        );
        let results = discovery.find_by_capability("compute");
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_heartbeat_update() {
        let discovery = EndpointDiscovery::new();
        discovery.register(DiscoveredEndpoint::new("ep-1", "addr-1"));
        assert!(discovery.update_heartbeat("ep-1"));
        assert!(!discovery.update_heartbeat("ep-999"));
    }

    #[test]
    fn test_all_endpoints() {
        let discovery = EndpointDiscovery::new();
        discovery.register(DiscoveredEndpoint::new("ep-1", "addr-1"));
        discovery.register(DiscoveredEndpoint::new("ep-2", "addr-2"));
        let all = discovery.all_endpoints();
        assert_eq!(all.len(), 2);
    }
}
