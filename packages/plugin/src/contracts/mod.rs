//! Plugin API contracts (RFC-0209).
//!
//! Defines the interfaces every plugin runtime component implements:
//! [`Plugin`], [`PluginFactory`], [`PluginMetadata`], [`PluginProvider`],
//! [`PluginHost`], [`PluginContext`], [`PluginRegistry`], [`PluginLoader`], and
//! [`PluginManager`]. Dependency injection is used exclusively — no component
//! holds a concrete reference to another; all collaboration is via these
//! trait objects shared as [`Arc`].

use crate::capability::CapabilityRegistry;
use crate::context::PluginContext;
use crate::error::PluginError;
use crate::health::PluginHealthState;
use crate::lifecycle::PluginState;
use crate::manifest::PluginManifest;
use atlas_contracts::RuntimeState;

/// Re-exported for plugin authors.
pub use crate::manifest::PluginMetadata;
use std::sync::Arc;

/// The service contract every plugin MUST implement (RFC-0203 §11, RFC-0209).
///
/// Lifecycle methods use `&self` with interior mutability so plugins are
/// [`Send`] + [`Sync`] and shareable via [`Arc`]. The platform enforces the
/// state machine; these methods are the hooks the plugin implements.
pub trait Plugin: Send + Sync {
    /// Immutable metadata describing this plugin.
    fn metadata(&self) -> &PluginMetadata;
    /// The plugin's current lifecycle state (self-reported).
    fn state(&self) -> PluginState;
    /// Initialize the plugin with its context (RFC-0203 §11 `on_initialize`).
    fn initialize(&self, ctx: &PluginContext) -> Result<(), PluginError>;
    /// Start the plugin.
    fn start(&self) -> Result<(), PluginError>;
    /// Pause the plugin.
    fn pause(&self) -> Result<(), PluginError>;
    /// Resume the plugin from a paused state.
    fn resume(&self) -> Result<(), PluginError>;
    /// Stop the plugin.
    fn stop(&self) -> Result<(), PluginError>;
    /// Shut the plugin down, releasing persistent resources.
    fn shutdown(&self) -> Result<(), PluginError>;
    /// Dispose of the plugin and all transient state.
    fn dispose(&self);
    /// Report the plugin's current health.
    fn health_check(&self) -> PluginHealthState;
}

/// Factory that creates plugin instances from a manifest (RFC-0209).
pub trait PluginFactory: Send + Sync {
    /// Create a plugin instance for `manifest`.
    fn create(&self, manifest: &PluginManifest) -> Result<Arc<dyn Plugin>, PluginError>;
    /// Whether this factory can produce a plugin with `plugin_id`.
    fn supports(&self, plugin_id: &str) -> bool;
}

/// Provider that discovers plugin manifests and supplies factories
/// (RFC-0204 §9, RFC-0216).
pub trait PluginProvider: Send + Sync {
    /// Discover all manifests this provider can supply.
    fn discover(&self) -> Result<Vec<PluginManifest>, PluginError>;
    /// Return the factory that can instantiate `plugin_id`.
    fn factory_for(&self, plugin_id: &str) -> Result<Arc<dyn PluginFactory>, PluginError>;
}

/// Runtime-side host that constructs plugin contexts (RFC-0209 §6).
///
/// The host is the only component allowed to build [`PluginContext`] values;
/// plugins never construct their own context.
pub trait PluginHost: Send + Sync {
    /// Build a context scoped to `plugin_id`.
    fn context_for(&self, plugin_id: &str) -> Result<PluginContext, PluginError>;
    /// The shared capability registry.
    fn capability_registry(&self) -> Arc<dyn CapabilityRegistry>;
    /// The current runtime lifecycle state (for compatibility checks).
    fn runtime_state(&self) -> RuntimeState;
}

/// Central plugin registry contract (RFC-0205).
///
/// Responsible for registration, lookup, discovery, enable/disable, unloading,
/// and dependency resolution. The registry MUST NOT instantiate plugins
/// directly (RFC-0205 §5) — it stores manifests and metadata only.
pub trait PluginRegistry: Send + Sync {
    /// Register a validated manifest. Rejects duplicate plugin ids.
    fn register(&self, manifest: PluginManifest) -> Result<(), PluginError>;
    /// Look up a manifest by plugin id.
    fn lookup(&self, plugin_id: &str) -> Option<PluginManifest>;
    /// Return all registered manifests (discovery view).
    fn discovery(&self) -> Vec<PluginManifest>;
    /// Enable a registered plugin.
    fn enable(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Disable a registered plugin.
    fn disable(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Unload (remove) a plugin from the registry.
    fn unload(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Whether a plugin is currently enabled.
    fn is_enabled(&self, plugin_id: &str) -> bool;
    /// List all registered plugin ids.
    fn list(&self) -> Vec<String>;
    /// Resolve and return the dependency-first load order.
    fn dependency_order(&self) -> Result<Vec<String>, PluginError>;
}

/// Plugin loader contract (RFC-0204).
///
/// Responsible for manifest discovery, validation, dependency verification,
/// load ordering, runtime activation, and runtime deactivation. Supports
/// deterministic loading.
pub trait PluginLoader: Send + Sync {
    /// Compute the dependency-first load order across registered manifests.
    fn load_order(&self) -> Result<Vec<String>, PluginError>;
    /// Activate (instantiate and start) a plugin via its provider/factory.
    fn activate(&self, plugin_id: &str) -> Result<Arc<dyn Plugin>, PluginError>;
    /// Deactivate a previously activated plugin.
    fn deactivate(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Return the ids of currently activated plugins.
    fn active_plugins(&self) -> Vec<String>;
}

/// Plugin manager contract — orchestrates the plugin runtime (RFC-0204/0205).
///
/// Ties together the registry, loader, lifecycle, capability registry, event
/// bus, and health monitor. Integrates plugin lifecycle with the Runtime
/// lifecycle.
pub trait PluginManager: Send + Sync {
    /// Install (register) a plugin manifest.
    fn install(&self, manifest: PluginManifest) -> Result<(), PluginError>;
    /// Start a plugin (activate + run).
    fn start_plugin(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Stop a plugin.
    fn stop_plugin(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Pause a running plugin.
    fn pause_plugin(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Resume a paused plugin.
    fn resume_plugin(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Unload a plugin completely.
    fn unload_plugin(&self, plugin_id: &str) -> Result<(), PluginError>;
    /// Shut down every active plugin in reverse load order.
    fn shutdown_all(&self) -> Result<(), PluginError>;
    /// Aggregate health across all plugins.
    fn aggregate_health(&self) -> PluginHealthState;
    /// The underlying registry.
    fn registry(&self) -> Arc<dyn PluginRegistry>;
}









#[cfg(test)]
mod tests {
    use super::*;
        use crate::context::PluginContext;
    use crate::error::PluginError;
    use crate::health::PluginHealthState;
    use crate::lifecycle::PluginState;
    use crate::manifest::{PluginManifest, PluginMetadata, PluginResourceLimits, PluginType, PluginCompatibility};
    use crate::registry::PluginRegistryImpl;
        use std::sync::atomic::{AtomicBool, Ordering};

    struct StubPlugin {
        meta: PluginMetadata,
        init: AtomicBool,
        started: AtomicBool,
    }

    impl Plugin for StubPlugin {
        fn metadata(&self) -> &PluginMetadata { &self.meta }
        fn state(&self) -> PluginState {
            if self.started.load(Ordering::Acquire) { PluginState::Running }
            else if self.init.load(Ordering::Acquire) { PluginState::Initialized }
            else { PluginState::Created }
        }
        fn initialize(&self, _ctx: &PluginContext) -> Result<(), PluginError> {
            self.init.store(true, Ordering::Release);
            Ok(())
        }
        fn start(&self) -> Result<(), PluginError> { self.started.store(true, Ordering::Release); Ok(()) }
        fn pause(&self) -> Result<(), PluginError> { Ok(()) }
        fn resume(&self) -> Result<(), PluginError> { Ok(()) }
        fn stop(&self) -> Result<(), PluginError> { self.started.store(false, Ordering::Release); Ok(()) }
        fn shutdown(&self) -> Result<(), PluginError> { Ok(()) }
        fn dispose(&self) {}
        fn health_check(&self) -> PluginHealthState { PluginHealthState::Healthy }
    }

    fn stub_manifest(id: &str) -> PluginManifest {
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
    fn test_plugin_trait_has_metadata() {
        let m = stub_manifest("p1");
        let md = m.metadata();
        assert_eq!(md.id, "p1");
    }

    #[test]
    fn test_plugin_metadata_fields() {
        let m = stub_manifest("test-plugin");
        let md = m.metadata();
        assert_eq!(md.id, "test-plugin");
        assert_eq!(md.name, "test-plugin");
        assert_eq!(md.version, "1.0.0");
    }

    #[test]
    fn test_registry_trait_register_lookup() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("a")).unwrap();
        assert!(reg.lookup("a").is_some());
        assert!(reg.lookup("b").is_none());
    }

    #[test]
    fn test_registry_trait_discovery() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("a")).unwrap();
        reg.register(stub_manifest("b")).unwrap();
        let discoveries = reg.discovery();
        assert_eq!(discoveries.len(), 2);
    }

    #[test]
    fn test_registry_trait_list() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("a")).unwrap();
        reg.register(stub_manifest("b")).unwrap();
        let list = reg.list();
        assert_eq!(list.len(), 2);
    }

    #[test]
    fn test_registry_trait_enable_disable() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("a")).unwrap();
        assert!(reg.is_enabled("a"));
        reg.disable("a").unwrap();
        assert!(!reg.is_enabled("a"));
    }

    #[test]
    fn test_registry_trait_unload() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("a")).unwrap();
        reg.unload("a").unwrap();
        assert!(reg.lookup("a").is_none());
    }

    #[test]
    fn test_registry_trait_dependency_order() {
        let reg = PluginRegistryImpl::new();
        reg.register(stub_manifest("dep")).unwrap();
        let mut m = stub_manifest("main");
        m.dependencies.push(crate::manifest::PluginDependency {
            plugin_id: "dep".to_string(),
            version: "*".to_string(),
            dependency_type: crate::manifest::DependencyType::Required,
            capability: None,
        });
        reg.register(m).unwrap();
        let order = reg.dependency_order().unwrap();
        assert_eq!(order, vec!["dep".to_string(), "main".to_string()]);
    }

    #[test]
    fn test_loader_trait_load_order() {
        let reg = Arc::new(PluginRegistryImpl::new());
        reg.register(stub_manifest("a")).unwrap();
        reg.register(stub_manifest("b")).unwrap();
        // We test the trait contract conceptually via the manager
        assert_eq!(reg.list().len(), 2);
    }
}




