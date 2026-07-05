//! Plugin manager — orchestrates the plugin runtime (RFC-0204/0205/0203/0210).
//!
//! [`PluginManagerImpl`] ties together the registry, loader, capability
//! registry, event bus, and health monitor. It owns the authoritative plugin
//! lifecycle state machines and integrates plugin lifecycle with the Runtime
//! lifecycle via [`is_runtime_compatible`]. It also implements [`PluginHost`],
//! building [`PluginContext`] values for plugins.
//!
//! No global mutable state is used; all state is held behind [`Mutex`]es inside
//! the manager instance shared via [`Arc`].

use crate::capability::{CapabilityRegistry, CapabilityRegistryImpl};
use crate::context::{
    CapabilityServiceDirectory, PluginContext, PluginLogger, PluginServiceDirectory, TracingLogger,
};
use crate::contracts::{
    Plugin, PluginHost, PluginLoader, PluginManager, PluginProvider, PluginRegistry,
};
use crate::error::{LifecycleError, PluginError, RegistryError};
use crate::events::{PluginEvent, PluginEventBusImpl};
use crate::health::{PluginHealthMonitor, PluginHealthServiceImpl, PluginHealthState};
use crate::lifecycle::{is_runtime_compatible, PluginLifecycleManager, PluginState};
use crate::loader::PluginLoaderImpl;
use crate::manifest::PluginManifest;
use crate::registry::PluginRegistryImpl;
use crate::version::SemanticVersion;
use atlas_contracts::RuntimeState;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

/// The plugin manager orchestrating the full plugin runtime.
pub struct PluginManagerImpl {
    registry: Arc<PluginRegistryImpl>,
    capability_registry: Arc<CapabilityRegistryImpl>,
    event_bus: Arc<PluginEventBusImpl>,
    health: Arc<PluginHealthServiceImpl>,
    logger: Arc<dyn PluginLogger>,
    provider: Arc<dyn PluginProvider>,
    runtime_version: SemanticVersion,
    api_version: SemanticVersion,
    loader: Mutex<Option<Arc<PluginLoaderImpl>>>,
    lifecycles: Mutex<HashMap<String, PluginLifecycleManager>>,
    runtime_state: Mutex<RuntimeState>,
}

impl PluginManagerImpl {
    /// Construct a fully-wired plugin manager.
    ///
    /// Returns an [`Arc`] so the manager can serve as its own [`PluginHost`]
    /// for the loader (dependency injection is preserved — the loader receives
    /// the manager as `Arc<dyn PluginHost>`).
    pub fn new(
        provider: Arc<dyn PluginProvider>,
        runtime_version: SemanticVersion,
        api_version: SemanticVersion,
    ) -> Arc<Self> {
        Self::with_logger(
            provider,
            runtime_version,
            api_version,
            Arc::new(TracingLogger),
        )
    }

    /// Construct a manager with a custom logger.
    pub fn with_logger(
        provider: Arc<dyn PluginProvider>,
        runtime_version: SemanticVersion,
        api_version: SemanticVersion,
        logger: Arc<dyn PluginLogger>,
    ) -> Arc<Self> {
        let registry = Arc::new(PluginRegistryImpl::new());
        let capability_registry = Arc::new(CapabilityRegistryImpl::new());
        let event_bus = Arc::new(PluginEventBusImpl::new());
        let health = Arc::new(PluginHealthServiceImpl::new());

        let manager = Arc::new(Self {
            registry: registry.clone(),
            capability_registry: capability_registry.clone(),
            event_bus: event_bus.clone(),
            health: health.clone(),
            logger,
            provider: provider.clone(),
            runtime_version,
            api_version,
            loader: Mutex::new(None),
            lifecycles: Mutex::new(HashMap::new()),
            runtime_state: Mutex::new(RuntimeState::Created),
        });

        let loader = Arc::new(PluginLoaderImpl::new(
            registry.clone() as Arc<dyn PluginRegistry>,
            provider,
            manager.clone() as Arc<dyn PluginHost>,
        ));
        *manager
            .loader
            .lock()
            .expect("manager loader mutex poisoned") = Some(loader);
        manager
    }

    fn loader(&self) -> Arc<PluginLoaderImpl> {
        self.loader
            .lock()
            .expect("manager loader mutex poisoned")
            .clone()
            .expect("plugin loader not initialized")
    }

    /// Update the manager's view of the runtime lifecycle state.
    pub fn set_runtime_state(&self, state: RuntimeState) {
        *self
            .runtime_state
            .lock()
            .expect("manager runtime state mutex poisoned") = state;
    }

    /// The current runtime state known to the manager.
    pub fn runtime_state(&self) -> RuntimeState {
        *self
            .runtime_state
            .lock()
            .expect("manager runtime state mutex poisoned")
    }

    /// The event bus used for plugin events.
    pub fn event_bus(&self) -> Arc<PluginEventBusImpl> {
        self.event_bus.clone()
    }

    /// The capability registry.
    pub fn capability_registry(&self) -> Arc<CapabilityRegistryImpl> {
        self.capability_registry.clone()
    }

    /// The health monitor.
    pub fn health_monitor(&self) -> Arc<PluginHealthServiceImpl> {
        self.health.clone()
    }

    fn publish(&self, event: &PluginEvent) {
        let _ = self.event_bus.publish_plugin_event(event);
    }

    fn require_runtime_compatible(&self, plugin_state: PluginState) -> Result<(), PluginError> {
        let rt = self.runtime_state();
        if !is_runtime_compatible(plugin_state, rt) {
            return Err(LifecycleError::OperationFailed(
                "plugin".to_string(),
                format!("runtime state {rt:?} incompatible with plugin state {plugin_state:?}"),
            )
            .into());
        }
        Ok(())
    }
}

impl PluginHost for PluginManagerImpl {
    fn context_for(&self, plugin_id: &str) -> Result<PluginContext, PluginError> {
        let services: Arc<dyn PluginServiceDirectory> = Arc::new(CapabilityServiceDirectory::new(
            self.capability_registry.clone() as Arc<dyn CapabilityRegistry>,
        ));
        PluginContext::builder(plugin_id)
            .logger(self.logger.clone())
            .capabilities(self.capability_registry.clone() as Arc<dyn CapabilityRegistry>)
            .event_bus(self.event_bus.clone())
            .health(self.health.clone() as Arc<dyn PluginHealthMonitor>)
            .services(services)
            .build()
    }

    fn capability_registry(&self) -> Arc<dyn CapabilityRegistry> {
        self.capability_registry.clone() as Arc<dyn CapabilityRegistry>
    }

    fn runtime_state(&self) -> RuntimeState {
        PluginManagerImpl::runtime_state(self)
    }
}

impl PluginManager for PluginManagerImpl {
    fn install(&self, manifest: PluginManifest) -> Result<(), PluginError> {
        manifest.validate()?;
        manifest.check_compatibility(&self.runtime_version, &self.api_version)?;
        let plugin_id = manifest.plugin_id.clone();
        self.registry.register(manifest)?;
        self.publish(&PluginEvent::registered(&plugin_id));
        Ok(())
    }

    fn start_plugin(&self, plugin_id: &str) -> Result<(), PluginError> {
        self.require_runtime_compatible(PluginState::Running)?;
        let manifest = self
            .registry
            .lookup(plugin_id)
            .ok_or_else(|| RegistryError::NotFound(plugin_id.to_string()))?;

        let loader = self.loader();
        let plugin = match loader.get_active(plugin_id) {
            Some(p) => p,
            None => loader.activate(plugin_id)?,
        };

        // Advance the authoritative lifecycle to Initialized (activate did init).
        {
            let mut lcs = self
                .lifecycles
                .lock()
                .expect("manager lifecycles mutex poisoned");
            let lc = lcs.entry(plugin_id.to_string()).or_default();
            if lc.current_state() == PluginState::Created {
                lc.transition(PluginState::Loaded)?;
                lc.transition(PluginState::Initialized)?;
            }
        }

        // Start the plugin; on failure, force Failed and publish.
        if let Err(e) = plugin.start() {
            self.force_failed(plugin_id);
            self.publish(&PluginEvent::failed(plugin_id, &e.to_string()));
            return Err(e);
        }

        // Advance lifecycle to Running.
        {
            let mut lcs = self
                .lifecycles
                .lock()
                .expect("manager lifecycles mutex poisoned");
            let lc = lcs.get_mut(plugin_id).expect("lifecycle must exist");
            lc.transition(PluginState::Started)?;
            lc.transition(PluginState::Running)?;
        }

        // Register provided capabilities.
        let caps = manifest.provided_capabilities();
        if !caps.is_empty() {
            self.capability_registry.register(plugin_id, &caps)?;
        }
        // Record health and publish.
        self.health
            .record(&plugin_id.to_string(), PluginHealthState::Healthy)?;
        self.publish(&PluginEvent::started(plugin_id));
        Ok(())
    }

    fn stop_plugin(&self, plugin_id: &str) -> Result<(), PluginError> {
        let plugin = self.active_plugin(plugin_id)?;
        plugin.stop()?;
        self.transition_lifecycle(plugin_id, PluginState::Stopped)?;
        self.health
            .record(&plugin_id.to_string(), PluginHealthState::Healthy)?;
        self.publish(&PluginEvent::stopped(plugin_id));
        Ok(())
    }

    fn pause_plugin(&self, plugin_id: &str) -> Result<(), PluginError> {
        self.require_runtime_compatible(PluginState::Paused)?;
        let plugin = self.active_plugin(plugin_id)?;
        plugin.pause()?;
        self.transition_lifecycle(plugin_id, PluginState::Paused)?;
        self.publish(&PluginEvent::paused(plugin_id));
        Ok(())
    }

    fn resume_plugin(&self, plugin_id: &str) -> Result<(), PluginError> {
        self.require_runtime_compatible(PluginState::Running)?;
        let plugin = self.active_plugin(plugin_id)?;
        plugin.resume()?;
        self.transition_lifecycle(plugin_id, PluginState::Running)?;
        self.publish(&PluginEvent::resumed(plugin_id));
        Ok(())
    }

    fn unload_plugin(&self, plugin_id: &str) -> Result<(), PluginError> {
        // Stop if running, then deactivate and remove from the registry.
        if self.loader().get_active(plugin_id).is_some() {
            let plugin = self.active_plugin(plugin_id)?;
            let _ = plugin.stop();
            self.loader().deactivate(plugin_id)?;
        }
        self.capability_registry.deregister(plugin_id);
        self.health.remove(&plugin_id.to_string());
        self.lifecycles
            .lock()
            .expect("manager lifecycles mutex poisoned")
            .remove(plugin_id);
        self.registry.unload(plugin_id)?;
        self.publish(&PluginEvent::removed(plugin_id));
        Ok(())
    }

    fn shutdown_all(&self) -> Result<(), PluginError> {
        let order = self.registry.dependency_order()?;
        // Stop in reverse load order (dependents before dependencies).
        for plugin_id in order.iter().rev() {
            if self.loader().get_active(plugin_id).is_some() {
                self.stop_plugin(plugin_id)?;
                self.loader().deactivate(plugin_id)?;
                self.lifecycles
                    .lock()
                    .expect("manager lifecycles mutex poisoned")
                    .remove(plugin_id);
            }
        }
        Ok(())
    }

    fn aggregate_health(&self) -> PluginHealthState {
        self.health.aggregate()
    }

    fn registry(&self) -> Arc<dyn PluginRegistry> {
        self.registry.clone() as Arc<dyn PluginRegistry>
    }
}

impl PluginManagerImpl {
    /// Force a plugin into the `Failed` state and record failed health.
    fn force_failed(&self, plugin_id: &str) {
        let mut lcs = self
            .lifecycles
            .lock()
            .expect("manager lifecycles mutex poisoned");
        if let Some(lc) = lcs.get_mut(plugin_id) {
            lc.force(PluginState::Failed);
        }
        let _ = self.health.record(
            &plugin_id.to_string(),
            PluginHealthState::Failed("start failed".to_string()),
        );
    }

    /// Return the active plugin instance for `plugin_id`, if any.
    fn active_plugin(&self, plugin_id: &str) -> Result<Arc<dyn Plugin>, PluginError> {
        self.loader()
            .get_active(plugin_id)
            .ok_or_else(|| RegistryError::NotFound(plugin_id.to_string()).into())
    }

    /// Transition a plugin's lifecycle.
    fn transition_lifecycle(
        &self,
        plugin_id: &str,
        target: PluginState,
    ) -> Result<(), PluginError> {
        let mut lcs = self
            .lifecycles
            .lock()
            .expect("manager lifecycles mutex poisoned");
        let lc = lcs
            .get_mut(plugin_id)
            .ok_or_else(|| RegistryError::NotFound(plugin_id.to_string()))?;
        lc.transition(target).map_err(PluginError::from)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::contracts::{Plugin, PluginFactory, PluginProvider};
    use crate::health::PluginHealthState;
    use crate::lifecycle::PluginState;
    use crate::manifest::{
        PluginCompatibility, PluginDependency, PluginManifest, PluginMetadata,
        PluginResourceLimits, PluginType,
    };
    use std::sync::atomic::{AtomicBool, Ordering};

    fn make_manifest(id: &str, deps: Vec<PluginDependency>) -> PluginManifest {
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

    struct TestPlugin {
        metadata: PluginMetadata,
        initialized: AtomicBool,
        started: AtomicBool,
    }

    impl Plugin for TestPlugin {
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
        fn initialize(&self, _ctx: &crate::context::PluginContext) -> Result<(), PluginError> {
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

    struct TestFactory;
    impl PluginFactory for TestFactory {
        fn create(&self, manifest: &PluginManifest) -> Result<Arc<dyn Plugin>, PluginError> {
            Ok(Arc::new(TestPlugin {
                metadata: manifest.metadata(),
                initialized: AtomicBool::new(false),
                started: AtomicBool::new(false),
            }))
        }
        fn supports(&self, _plugin_id: &str) -> bool {
            true
        }
    }

    struct TestProvider {
        manifests: Vec<PluginManifest>,
    }
    impl PluginProvider for TestProvider {
        fn discover(&self) -> Result<Vec<PluginManifest>, PluginError> {
            Ok(self.manifests.clone())
        }
        fn factory_for(&self, _plugin_id: &str) -> Result<Arc<dyn PluginFactory>, PluginError> {
            Ok(Arc::new(TestFactory))
        }
    }

    fn make_manager(manifests: Vec<PluginManifest>) -> Arc<PluginManagerImpl> {
        let provider = Arc::new(TestProvider {
            manifests: manifests.clone(),
        });
        PluginManagerImpl::new(
            provider,
            SemanticVersion::parse("1.5.0").unwrap(),
            SemanticVersion::parse("1.0.0").unwrap(),
        )
    }

    #[test]
    fn test_manager_creation() {
        let mgr = make_manager(vec![]);
        assert_eq!(mgr.registry().list().len(), 0);
        assert_eq!(mgr.runtime_state(), RuntimeState::Created);
    }

    #[test]
    fn test_install_plugin() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        assert_eq!(mgr.registry().list(), vec!["p1".to_string()]);
    }

    #[test]
    fn test_install_duplicate_rejected() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        assert!(mgr.install(make_manifest("p1", vec![])).is_err());
    }

    #[test]
    fn test_start_and_stop_plugin() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        mgr.set_runtime_state(atlas_contracts::RuntimeState::Running);

        mgr.start_plugin("p1").unwrap();
        assert_eq!(mgr.runtime_state(), RuntimeState::Running);
        mgr.stop_plugin("p1").unwrap();
    }

    #[test]
    fn test_start_unknown_plugin_rejected() {
        let mgr = make_manager(vec![]);
        assert!(mgr.start_plugin("nonexistent").is_err());
    }

    #[test]
    fn test_pause_and_resume_plugin() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        mgr.set_runtime_state(atlas_contracts::RuntimeState::Running);

        mgr.start_plugin("p1").unwrap();
        mgr.pause_plugin("p1").unwrap();
        mgr.resume_plugin("p1").unwrap();
    }

    #[test]
    fn test_unload_plugin() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        mgr.set_runtime_state(atlas_contracts::RuntimeState::Running);

        mgr.start_plugin("p1").unwrap();
        mgr.unload_plugin("p1").unwrap();
        assert!(mgr.registry().lookup("p1").is_none());
    }

    #[test]
    fn test_shutdown_all() {
        let mgr = make_manager(vec![make_manifest("a", vec![]), make_manifest("b", vec![])]);
        mgr.install(make_manifest("a", vec![])).unwrap();
        mgr.install(make_manifest("b", vec![])).unwrap();
        mgr.set_runtime_state(atlas_contracts::RuntimeState::Running);

        mgr.start_plugin("a").unwrap();
        mgr.start_plugin("b").unwrap();
        mgr.shutdown_all().unwrap();
    }

    #[test]
    fn test_aggregate_health_healthy() {
        let mgr = make_manager(vec![make_manifest("p1", vec![])]);
        mgr.install(make_manifest("p1", vec![])).unwrap();
        let health = mgr.aggregate_health();
        assert!(matches!(health, PluginHealthState::Healthy));
    }

    #[test]
    fn test_runtime_state_update() {
        let mgr = make_manager(vec![]);
        assert_eq!(mgr.runtime_state(), RuntimeState::Created);
        mgr.set_runtime_state(RuntimeState::Running);
        assert_eq!(mgr.runtime_state(), RuntimeState::Running);
    }

    #[test]
    fn test_event_bus_available() {
        let mgr = make_manager(vec![]);
        let _bus = mgr.event_bus();
    }

    #[test]
    fn test_capability_registry_available() {
        let mgr = make_manager(vec![]);
        let cr = mgr.capability_registry();
        assert_eq!(cr.plugin_count(), 0);
    }

    #[test]
    fn test_health_monitor_available() {
        let mgr = make_manager(vec![]);
        let hm = mgr.health_monitor();
        assert_eq!(hm.aggregate(), PluginHealthState::Healthy);
    }

    #[test]
    fn test_registry_accessor() {
        let mgr = make_manager(vec![]);
        let reg = mgr.registry();
        assert_eq!(reg.list().len(), 0);
    }
}
