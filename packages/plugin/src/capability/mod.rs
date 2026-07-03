//! Plugin capability model and registry (RFC-0206).
//!
//! Defines the set of capabilities a plugin MAY declare, the
//! [`CapabilityDeclaration`] used in manifests, and the central
//! [`CapabilityRegistry`] that tracks which plugin provides which capability.
//!
//! The registry is queryable by both the Runtime and the Workflow Engine
//! (RFC-0206 §12) so that consumers can locate capability providers without
//! holding direct references to individual plugins. All state is held behind a
//! [`Mutex`] inside the registry instance shared via dependency injection — no
//! global mutable state is used.

use crate::error::CapabilityError;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::fmt;
use std::sync::Mutex;

/// Unique plugin identifier.
pub type PluginId = String;

/// A functional capability a plugin MAY provide (RFC-0206 §10).
///
/// The nine canonical capabilities listed in the Plugin Runtime scope are
/// enumerated explicitly. The [`PluginCapability::Custom`] variant allows
/// future capabilities to be declared without changing the enum, preserving
/// forward compatibility (RFC-0206 §13).
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PluginCapability {
    Vision,
    OCR,
    AI,
    Workflow,
    Storage,
    IPC,
    Metrics,
    Logging,
    Scheduling,
    /// An extension capability identified by a canonical name.
    Custom(String),
}

impl PluginCapability {
    /// Return the canonical lowercase name of the capability.
    pub fn as_str(&self) -> &str {
        match self {
            Self::Vision => "vision",
            Self::OCR => "ocr",
            Self::AI => "ai",
            Self::Workflow => "workflow",
            Self::Storage => "storage",
            Self::IPC => "ipc",
            Self::Metrics => "metrics",
            Self::Logging => "logging",
            Self::Scheduling => "scheduling",
            Self::Custom(name) => name.as_str(),
        }
    }

    /// Parse a capability from its canonical name (case-insensitive).
    pub fn from_str(name: &str) -> Option<Self> {
        match name.trim().to_ascii_lowercase().as_str() {
            "vision" => Some(Self::Vision),
            "ocr" => Some(Self::OCR),
            "ai" => Some(Self::AI),
            "workflow" => Some(Self::Workflow),
            "storage" => Some(Self::Storage),
            "ipc" => Some(Self::IPC),
            "metrics" => Some(Self::Metrics),
            "logging" => Some(Self::Logging),
            "scheduling" => Some(Self::Scheduling),
            other if !other.is_empty() => Some(Self::Custom(other.to_string())),
            _ => None,
        }
    }
}

impl fmt::Display for PluginCapability {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// A capability declaration inside a plugin manifest (RFC-0206 §9).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CapabilityDeclaration {
    pub capability: PluginCapability,
    /// Whether the plugin requires this capability to function.
    #[serde(default)]
    pub required: bool,
    /// Whether the capability is currently enabled for the plugin.
    #[serde(default = "default_enabled")]
    pub enabled: bool,
}

fn default_enabled() -> bool {
    true
}

impl CapabilityDeclaration {
    pub fn new(capability: PluginCapability) -> Self {
        Self { capability, required: false, enabled: true }
    }

    pub fn required(mut self) -> Self {
        self.required = true;
        self
    }

    pub fn disabled(mut self) -> Self {
        self.enabled = false;
        self
    }
}
/// The central capability registry contract (RFC-0206 §12).
///
/// Tracks the set of capabilities each registered plugin provides and supports
/// querying by capability (to find providers) and by plugin (to list a
/// plugin's capabilities). Implementations MUST be [`Send`] + [`Sync`].
pub trait CapabilityRegistry: Send + Sync {
    /// Register the capabilities a plugin provides.
    fn register(&self, plugin_id: &str, capabilities: &[PluginCapability]) -> Result<(), CapabilityError>;
    /// Remove all capability registrations for a plugin.
    fn deregister(&self, plugin_id: &str);
    /// Return the IDs of every plugin that provides `capability`.
    fn providers(&self, capability: &PluginCapability) -> Vec<PluginId>;
    /// Return the capabilities a plugin provides.
    fn capabilities(&self, plugin_id: &str) -> Vec<PluginCapability>;
    /// Whether any plugin currently provides `capability`.
    fn has(&self, capability: &PluginCapability) -> bool;
    /// Return every distinct capability currently registered.
    fn list_all(&self) -> Vec<PluginCapability>;
    /// The number of plugins currently registered.
    fn plugin_count(&self) -> usize;
}

/// In-memory implementation of [`CapabilityRegistry`].
pub struct CapabilityRegistryImpl {
    /// plugin_id -> set of capabilities.
    by_plugin: Mutex<HashMap<PluginId, HashSet<PluginCapability>>>,
}

impl CapabilityRegistryImpl {
    pub fn new() -> Self {
        Self { by_plugin: Mutex::new(HashMap::new()) }
    }
}

impl Default for CapabilityRegistryImpl {
    fn default() -> Self {
        Self::new()
    }
}

impl CapabilityRegistry for CapabilityRegistryImpl {
    fn register(&self, plugin_id: &str, capabilities: &[PluginCapability]) -> Result<(), CapabilityError> {
        let mut map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        let entry = map.entry(plugin_id.to_string()).or_default();
        for cap in capabilities {
            entry.insert(cap.clone());
        }
        Ok(())
    }

    fn deregister(&self, plugin_id: &str) {
        let mut map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        map.remove(plugin_id);
    }

    fn providers(&self, capability: &PluginCapability) -> Vec<PluginId> {
        let map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        let mut result: Vec<PluginId> = map
            .iter()
            .filter(|(_, caps)| caps.contains(capability))
            .map(|(id, _)| id.clone())
            .collect();
        result.sort();
        result
    }

    fn capabilities(&self, plugin_id: &str) -> Vec<PluginCapability> {
        let map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        map.get(plugin_id)
            .map(|caps| {
                let mut v: Vec<PluginCapability> = caps.iter().cloned().collect();
                v.sort_by(|a, b| a.as_str().cmp(b.as_str()));
                v
            })
            .unwrap_or_default()
    }

    fn has(&self, capability: &PluginCapability) -> bool {
        let map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        map.values().any(|caps| caps.contains(capability))
    }

    fn list_all(&self) -> Vec<PluginCapability> {
        let map = self.by_plugin.lock().expect("capability registry mutex poisoned");
        let mut all: HashSet<PluginCapability> = HashSet::new();
        for caps in map.values() {
            all.extend(caps.iter().cloned());
        }
        let mut v: Vec<PluginCapability> = all.into_iter().collect();
        v.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        v
    }

    fn plugin_count(&self) -> usize {
        self.by_plugin.lock().expect("capability registry mutex poisoned").len()
    }
}
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_capability_roundtrip() {
        for cap in [
            PluginCapability::Vision,
            PluginCapability::OCR,
            PluginCapability::AI,
            PluginCapability::Workflow,
            PluginCapability::Storage,
            PluginCapability::IPC,
            PluginCapability::Metrics,
            PluginCapability::Logging,
            PluginCapability::Scheduling,
        ] {
            let parsed = PluginCapability::from_str(cap.as_str()).unwrap();
            assert_eq!(parsed, cap);
        }
    }

    #[test]
    fn test_capability_custom() {
        let cap = PluginCapability::from_str("telemetry").unwrap();
        assert_eq!(cap, PluginCapability::Custom("telemetry".to_string()));
        assert_eq!(cap.as_str(), "telemetry");
    }

    #[test]
    fn test_capability_case_insensitive() {
        assert_eq!(PluginCapability::from_str("VISION").unwrap(), PluginCapability::Vision);
    }

    #[test]
    fn test_registry_register_and_query() {
        let reg = CapabilityRegistryImpl::new();
        reg.register(
            &"p1".to_string(),
            &[PluginCapability::Vision, PluginCapability::OCR],
        )
        .unwrap();
        reg.register(&"p2".to_string(), &[PluginCapability::Vision]).unwrap();

        let mut providers = reg.providers(&PluginCapability::Vision);
        providers.sort();
        assert_eq!(providers, vec!["p1".to_string(), "p2".to_string()]);

        let caps = reg.capabilities(&"p1".to_string());
        assert!(caps.contains(&PluginCapability::Vision));
        assert!(caps.contains(&PluginCapability::OCR));
        assert!(reg.has(&PluginCapability::OCR));
        assert!(!reg.has(&PluginCapability::AI));
        assert_eq!(reg.plugin_count(), 2);
    }

    #[test]
    fn test_registry_deregister() {
        let reg = CapabilityRegistryImpl::new();
        reg.register(&"p1".to_string(), &[PluginCapability::AI]).unwrap();
        assert!(reg.has(&PluginCapability::AI));
        reg.deregister(&"p1".to_string());
        assert!(!reg.has(&PluginCapability::AI));
        assert!(reg.capabilities(&"p1".to_string()).is_empty());
    }

    #[test]
    fn test_registry_list_all() {
        let reg = CapabilityRegistryImpl::new();
        reg.register(&"p1".to_string(), &[PluginCapability::Vision]).unwrap();
        reg.register(&"p2".to_string(), &[PluginCapability::Storage, PluginCapability::IPC]).unwrap();
        let all = reg.list_all();
        assert_eq!(all.len(), 3);
    }

    #[test]
    fn test_capability_declaration_builder() {
        let d = CapabilityDeclaration::new(PluginCapability::Vision).required().disabled();
        assert!(d.required);
        assert!(!d.enabled);
        assert_eq!(d.capability, PluginCapability::Vision);
    }
}
