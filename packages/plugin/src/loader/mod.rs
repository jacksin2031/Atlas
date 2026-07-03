//! Plugin loader implementation (RFC-0204).
//!
//! Responsible for manifest discovery (via the registry), dependency
//! verification and load ordering (via the registry's resolver), and runtime
//! activation/deactivation of plugins. Activation instantiates a plugin
//! through its [`PluginProvider`]/[`PluginFactory`] and initializes it with a
//! [`PluginContext`] built by the [`PluginHost`]. Deactivation shuts the plugin
//! down and disposes of it.
//!
//! Loading is deterministic: the load order is the registry's topological
//! dependency order. The loader does NOT own lifecycle state — that is the
//! manager's responsibility.

use crate::contracts::{Plugin, PluginHost, PluginLoader, PluginProvider, PluginRegistry};
use crate::error::{LoaderError, PluginError, RegistryError};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

/// In-memory implementation of [`PluginLoader`].
pub struct PluginLoaderImpl {
    registry: Arc<dyn PluginRegistry>,
    provider: Arc<dyn PluginProvider>,
    host: Arc<dyn PluginHost>,
    active: Mutex<HashMap<String, Arc<dyn Plugin>>>,
}

impl PluginLoaderImpl {
    /// Create a new loader wired to its dependencies via dependency injection.
    pub fn new(
        registry: Arc<dyn PluginRegistry>,
        provider: Arc<dyn PluginProvider>,
        host: Arc<dyn PluginHost>,
    ) -> Self {
        Self {
            registry,
            provider,
            host,
            active: Mutex::new(HashMap::new()),
        }
    }

    /// Return the currently active plugin instance, if any.
    pub fn get_active(&self, plugin_id: &str) -> Option<Arc<dyn Plugin>> {
        self.active.lock().expect("loader active mutex poisoned").get(plugin_id).cloned()
    }
}

impl PluginLoader for PluginLoaderImpl {
    fn load_order(&self) -> Result<Vec<String>, PluginError> {
        self.registry.dependency_order()
    }

    fn activate(&self, plugin_id: &str) -> Result<Arc<dyn Plugin>, PluginError> {
        if self.get_active(plugin_id).is_some() {
            return Err(LoaderError::ActivationFailed(
                plugin_id.to_string(),
                "already active".to_string(),
            )
            .into());
        }
        let manifest = self
            .registry
            .lookup(plugin_id)
            .ok_or_else(|| RegistryError::NotFound(plugin_id.to_string()))?;
        if !self.registry.is_enabled(plugin_id) {
            return Err(RegistryError::Disabled(plugin_id.to_string()).into());
        }
        let factory = self.provider.factory_for(plugin_id)?;
        let plugin = factory.create(&manifest)?;
        let ctx = self.host.context_for(plugin_id)?;
        plugin
            .initialize(&ctx)
            .map_err(|e| LoaderError::ActivationFailed(plugin_id.to_string(), e.to_string()))?;
        self.active
            .lock()
            .expect("loader active mutex poisoned")
            .insert(plugin_id.to_string(), plugin.clone());
        Ok(plugin)
    }

    fn deactivate(&self, plugin_id: &str) -> Result<(), PluginError> {
        let plugin = self
            .active
            .lock()
            .expect("loader active mutex poisoned")
            .remove(plugin_id)
            .ok_or_else(|| RegistryError::NotFound(plugin_id.to_string()))?;
        plugin
            .shutdown()
            .map_err(|e| LoaderError::DeactivationFailed(plugin_id.to_string(), e.to_string()))?;
        plugin.dispose();
        Ok(())
    }

    fn active_plugins(&self) -> Vec<String> {
        let mut ids: Vec<String> = self
            .active
            .lock()
            .expect("loader active mutex poisoned")
            .keys()
            .cloned()
            .collect();
        ids.sort();
        ids
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::context::PluginContext;
    use crate::health::PluginHealthState;
    use crate::lifecycle::PluginState;
    use crate::manifest::{
        DependencyType, PluginCompatibility, PluginDependency, PluginManifest, PluginMetadata,
        PluginResourceLimits, PluginType,
    };
    use crate::registry::PluginRegistryImpl;
    use atlas_contracts::RuntimeState;
    use std::sync::atomic::{AtomicBool, Ordering};

    fn manifest(id: &str, deps: Vec<PluginDependency>) -> PluginManifest {
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
            dependencies: deps,
            permissions: Vec::new(),
            compatibility: PluginCompatibility::default(),
            resource_limits: PluginResourceLimits::default(),
        }
    }

    struct MockPlugin {
        metadata: PluginMetadata,
        initialized: AtomicBool,
        started: AtomicBool,
    }

    impl Plugin for MockPlugin {
        fn metadata(&self) -> &PluginMetadata {
            &self.metadata
        }
        fn state(&self) -> PluginState {
            if self.started.load(Ordering::Acquire) {
                PluginState::Running
            } else if self.initialized.load(Ordering::Acquire) {
                PluginState::Initialized
            } else {
                PluginState::Created
            }
        }
        fn initialize(&self, _ctx: &PluginContext) -> Result<(), PluginError> {
            self.initialized.store(true, Ordering::Release);
            Ok(())
        }
        fn start(&self) -> Result<(), PluginError> {
            self.started.store(true, Ordering::Release);
            Ok(())
        }
        fn pause(&self) -> Result<(), PluginError> {
            Ok(())
        }
        fn resume(&self) -> Result<(), PluginError> {
            Ok(())
        }
        fn stop(&self) -> Result<(), PluginError> {
            self.started.store(false, Ordering::Release);
            Ok(())
        }
        fn shutdown(&self) -> Result<(), PluginError> {
            Ok(())
        }
        fn dispose(&self) {}
        fn health_check(&self) -> PluginHealthState {
            PluginHealthState::Healthy
        }
    }

    struct MockFactory;
    impl crate::contracts::PluginFactory for MockFactory {
        fn create(&self, manifest: &PluginManifest) -> Result<Arc<dyn Plugin>, PluginError> {
            Ok(Arc::new(MockPlugin {
                metadata: manifest.metadata(),
                initialized: AtomicBool::new(false),
                started: AtomicBool::new(false),
            }))
        }
        fn supports(&self, _plugin_id: &str) -> bool {
            true
        }
    }

    struct MockProvider {
        manifests: Vec<PluginManifest>,
    }
    impl crate::contracts::PluginProvider for MockProvider {
        fn discover(&self) -> Result<Vec<PluginManifest>, PluginError> {
            Ok(self.manifests.clone())
        }
        fn factory_for(&self, _plugin_id: &str) -> Result<Arc<dyn crate::contracts::PluginFactory>, PluginError> {
            Ok(Arc::new(MockFactory))
        }
    }

    struct MockHost {
        caps: Arc<crate::capability::CapabilityRegistryImpl>,
    }
    impl crate::contracts::PluginHost for MockHost {
        fn context_for(&self, plugin_id: &str) -> Result<PluginContext, PluginError> {
            PluginContext::builder(plugin_id)
                .capabilities(self.caps.clone())
                .health(Arc::new(crate::health::PluginHealthServiceImpl::new()))
                .build()
        }
        fn capability_registry(&self) -> Arc<dyn crate::capability::CapabilityRegistry> {
            self.caps.clone()
        }
        fn runtime_state(&self) -> RuntimeState {
            RuntimeState::Running
        }
    }

    fn setup(manifests: Vec<PluginManifest>) -> (Arc<PluginRegistryImpl>, Arc<PluginLoaderImpl>) {
        let registry = Arc::new(PluginRegistryImpl::new());
        for m in manifests {
            registry.register(m).unwrap();
        }
        let provider = Arc::new(MockProvider { manifests: registry.discovery() });
        let host = Arc::new(MockHost { caps: Arc::new(crate::capability::CapabilityRegistryImpl::new()) });
        let loader = Arc::new(PluginLoaderImpl::new(registry.clone(), provider, host));
        (registry, loader)
    }

    #[test]
    fn test_load_order() {
        let (reg, loader) = setup(vec![
            manifest("a", vec![PluginDependency {
                plugin_id: "b".to_string(),
                version: "*".to_string(),
                dependency_type: DependencyType::Required,
                capability: None,
            }]),
            manifest("b", vec![]),
        ]);
        let order = loader.load_order().unwrap();
        assert_eq!(order, vec!["b".to_string(), "a".to_string()]);
        let _ = reg;
    }

    #[test]
    fn test_activate_and_deactivate() {
        let (_reg, loader) = setup(vec![manifest("a", vec![])]);
        let plugin = loader.activate("a").unwrap();
        assert_eq!(plugin.state(), PluginState::Initialized);
        assert_eq!(loader.active_plugins(), vec!["a".to_string()]);
        loader.deactivate("a").unwrap();
        assert!(loader.active_plugins().is_empty());
    }

    #[test]
    fn test_activate_unknown_rejected() {
        let (_reg, loader) = setup(vec![]);
        assert!(loader.activate("nope").is_err());
    }

    #[test]
    fn test_activate_disabled_rejected() {
        let (reg, loader) = setup(vec![manifest("a", vec![])]);
        reg.disable("a").unwrap();
        assert!(loader.activate("a").is_err());
    }

    #[test]
    fn test_double_activate_rejected() {
        let (_reg, loader) = setup(vec![manifest("a", vec![])]);
        loader.activate("a").unwrap();
        assert!(loader.activate("a").is_err());
    }

    #[test]
    fn test_deactivate_unknown_rejected() {
        let (_reg, loader) = setup(vec![]);
        assert!(loader.deactivate("nope").is_err());
    }
}

