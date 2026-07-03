//! Plugin registry implementation (RFC-0205).
//!
//! Central store for all plugin manifest data. Provides registration, lookup,
//! discovery, enable/disable, unloading, and dependency resolution. The
//! registry stores manifests and metadata ONLY — it MUST NOT instantiate
//! plugins (RFC-0205 §5). Instantiation is the loader's responsibility.
//!
//! All state is held behind [`Mutex`]es inside the registry instance shared
//! via dependency injection — no global mutable state is used.

use crate::capability::PluginId;
use crate::contracts::PluginRegistry;
use crate::dependency::DependencyResolver;
use crate::error::{PluginError, RegistryError};
use crate::manifest::PluginManifest;
use std::collections::{HashMap, HashSet};
use std::sync::Mutex;

/// In-memory implementation of [`PluginRegistry`].
pub struct PluginRegistryImpl {
    manifests: Mutex<HashMap<PluginId, PluginManifest>>,
    enabled: Mutex<HashSet<PluginId>>,
    order: Mutex<Vec<PluginId>>,
    resolver: DependencyResolver,
}

impl PluginRegistryImpl {
    pub fn new() -> Self {
        Self {
            manifests: Mutex::new(HashMap::new()),
            enabled: Mutex::new(HashSet::new()),
            order: Mutex::new(Vec::new()),
            resolver: DependencyResolver::new(),
        }
    }

    /// The number of registered plugins.
    pub fn len(&self) -> usize {
        self.manifests.lock().expect("registry manifests mutex poisoned").len()
    }

    /// Whether the registry is empty.
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

impl Default for PluginRegistryImpl {
    fn default() -> Self {
        Self::new()
    }
}

impl PluginRegistry for PluginRegistryImpl {
    fn register(&self, manifest: PluginManifest) -> Result<(), PluginError> {
        manifest.validate().map_err(PluginError::from)?;
        let mut manifests = self.manifests.lock().expect("registry manifests mutex poisoned");
        if manifests.contains_key(&manifest.plugin_id) {
            return Err(RegistryError::AlreadyRegistered(manifest.plugin_id.clone()).into());
        }
        let id = manifest.plugin_id.clone();
        manifests.insert(id.clone(), manifest);
        self.order.lock().expect("registry order mutex poisoned").push(id.clone());
        self.enabled.lock().expect("registry enabled mutex poisoned").insert(id);
        Ok(())
    }

    fn lookup(&self, plugin_id: &str) -> Option<PluginManifest> {
        self.manifests
            .lock()
            .expect("registry manifests mutex poisoned")
            .get(plugin_id)
            .cloned()
    }

    fn discovery(&self) -> Vec<PluginManifest> {
        let order = self.order.lock().expect("registry order mutex poisoned").clone();
        let manifests = self.manifests.lock().expect("registry manifests mutex poisoned");
        order.iter().filter_map(|id| manifests.get(id).cloned()).collect()
    }

    fn list(&self) -> Vec<String> {
        self.order.lock().expect("registry order mutex poisoned").clone()
    }

    fn enable(&self, plugin_id: &str) -> Result<(), PluginError> {
        let manifests = self.manifests.lock().expect("registry manifests mutex poisoned");
        if !manifests.contains_key(plugin_id) {
            return Err(RegistryError::NotFound(plugin_id.to_string()).into());
        }
        self.enabled.lock().expect("registry enabled mutex poisoned").insert(plugin_id.to_string());
        Ok(())
    }

    fn disable(&self, plugin_id: &str) -> Result<(), PluginError> {
        let manifests = self.manifests.lock().expect("registry manifests mutex poisoned");
        if !manifests.contains_key(plugin_id) {
            return Err(RegistryError::NotFound(plugin_id.to_string()).into());
        }
        self.enabled.lock().expect("registry enabled mutex poisoned").remove(plugin_id);
        Ok(())
    }

    fn unload(&self, plugin_id: &str) -> Result<(), PluginError> {
        let mut manifests = self.manifests.lock().expect("registry manifests mutex poisoned");
        if manifests.remove(plugin_id).is_none() {
            return Err(RegistryError::NotFound(plugin_id.to_string()).into());
        }
        self.enabled.lock().expect("registry enabled mutex poisoned").remove(plugin_id);
        self.order.lock().expect("registry order mutex poisoned").retain(|id| id != plugin_id);
        Ok(())
    }

    fn is_enabled(&self, plugin_id: &str) -> bool {
        self.enabled.lock().expect("registry enabled mutex poisoned").contains(plugin_id)
    }

    fn dependency_order(&self) -> Result<Vec<String>, PluginError> {
        let manifests = self.discovery();
        let result = self.resolver.resolve(&manifests)?;
        Ok(result.load_order)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::manifest::{PluginCompatibility, PluginResourceLimits, PluginType};

    fn manifest(id: &str) -> PluginManifest {
        PluginManifest {
            manifest_version: "1.0.0".to_string(),
            plugin_id: id.to_string(),
            plugin_name: id.to_string(),
            version: "1.0.0".to_string(),
            description: String::new(),
            author: String::new(),
            license: "MIT".to_string(),
            plugin_type: PluginType::Extension,
            entry_point: "main".to_string(),
            capabilities: Vec::new(),
            dependencies: Vec::new(),
            permissions: Vec::new(),
            compatibility: PluginCompatibility::default(),
            resource_limits: PluginResourceLimits::default(),
        }
    }

    #[test]
    fn test_register_and_lookup() {
        let reg = PluginRegistryImpl::new();
        reg.register(manifest("a")).unwrap();
        assert!(reg.lookup("a").is_some());
        assert!(reg.lookup("missing").is_none());
        assert_eq!(reg.len(), 1);
    }

    #[test]
    fn test_duplicate_registration_rejected() {
        let reg = PluginRegistryImpl::new();
        reg.register(manifest("a")).unwrap();
        assert!(reg.register(manifest("a")).is_err());
    }

    #[test]
    fn test_invalid_manifest_rejected() {
        let reg = PluginRegistryImpl::new();
        let mut m = manifest("a");
        m.license = "".to_string();
        assert!(reg.register(m).is_err());
    }

    #[test]
    fn test_enable_disable() {
        let reg = PluginRegistryImpl::new();
        reg.register(manifest("a")).unwrap();
        assert!(reg.is_enabled("a"));
        reg.disable("a").unwrap();
        assert!(!reg.is_enabled("a"));
        reg.enable("a").unwrap();
        assert!(reg.is_enabled("a"));
    }

    #[test]
    fn test_enable_unknown_rejected() {
        let reg = PluginRegistryImpl::new();
        assert!(reg.enable("nope").is_err());
    }

    #[test]
    fn test_unload() {
        let reg = PluginRegistryImpl::new();
        reg.register(manifest("a")).unwrap();
        reg.unload("a").unwrap();
        assert!(reg.lookup("a").is_none());
        assert!(!reg.is_enabled("a"));
        assert!(reg.is_empty());
    }

    #[test]
    fn test_unload_unknown_rejected() {
        let reg = PluginRegistryImpl::new();
        assert!(reg.unload("nope").is_err());
    }

    #[test]
    fn test_discovery_preserves_order() {
        let reg = PluginRegistryImpl::new();
        reg.register(manifest("a")).unwrap();
        reg.register(manifest("b")).unwrap();
        let ids: Vec<String> = reg.discovery().iter().map(|m| m.plugin_id.clone()).collect();
        assert_eq!(ids, vec!["a".to_string(), "b".to_string()]);
        assert_eq!(reg.list(), vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn test_dependency_order() {
        let reg = PluginRegistryImpl::new();
        let mut b = manifest("b");
        b.dependencies = vec![crate::manifest::PluginDependency {
            plugin_id: "a".to_string(),
            version: "*".to_string(),
            dependency_type: crate::manifest::DependencyType::Required,
            capability: None,
        }];
        reg.register(manifest("a")).unwrap();
        reg.register(b).unwrap();
        let order = reg.dependency_order().unwrap();
        assert_eq!(order, vec!["a".to_string(), "b".to_string()]);
    }
}

