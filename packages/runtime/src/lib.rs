#[allow(dead_code)]
/// Atlas Runtime — the core execution engine.
pub mod lifecycle;
pub mod registry;
pub mod dependency;
pub mod eventbus;
pub mod scheduler;
pub mod health;
pub mod config;
pub mod manifest;
pub mod error;

use atlas_common::{AtlasError, HealthStatus};
use atlas_contracts::RuntimeState;
use registry::ServiceRegistry;
use lifecycle::LifecycleManager;
use eventbus::EventBusImpl;
use scheduler::SchedulerImpl;
use health::HealthMonitor;
use dependency::DependencyResolver;
use config::ConfigLoader;
use manifest::ManifestLoader;

/// The Atlas Runtime — central coordinator for all core services.
pub struct AtlasRuntime {
    lifecycle: LifecycleManager,
    registry: ServiceRegistry,
    event_bus: EventBusImpl,
    scheduler: SchedulerImpl,
    health_monitor: HealthMonitor,
    config: ConfigLoader,
    manifest_loader: ManifestLoader,
    dependency_resolver: DependencyResolver,
}

impl AtlasRuntime {
    /// Bootstrap the runtime from a configuration file path.
    pub fn bootstrap(config_path: &str) -> Result<Self, AtlasError> {
        let config = ConfigLoader::load(config_path)?;
        let manifest = ManifestLoader::load_from_config(&config)?;

        let mut lifecycle = LifecycleManager::new();
        let mut event_bus = EventBusImpl::new();
        let scheduler = SchedulerImpl::new(&event_bus);
        let health_monitor = HealthMonitor::new(&event_bus);
        let mut registry = ServiceRegistry::new();
        let dependency_resolver = DependencyResolver::new();

        lifecycle.transition(RuntimeState::Initializing)?;

        let services = ManifestLoader::discover_services(&manifest, &registry);
        for decl in &services {
            registry.register_declaration(decl.clone())?;
        }

        let order = dependency_resolver.resolve(&registry)?;
        for service_id in &order {
            registry.initialize(service_id)?;
            registry.start(service_id)?;
        }

        lifecycle.transition(RuntimeState::Ready)?;
        event_bus.publish_ready()?;

        Ok(Self {
            lifecycle,
            registry,
            event_bus,
            scheduler,
            health_monitor,
            config,
            manifest_loader: manifest,
            dependency_resolver,
        })
    }

    /// Activate the runtime — transition to Running state.
    pub fn activate(&mut self) -> Result<(), AtlasError> {
        self.lifecycle.transition(RuntimeState::Running)?;
        self.scheduler.resume()?;
        Ok(())
    }

    /// Pause the runtime.
    pub fn pause(&mut self) -> Result<(), AtlasError> {
        self.lifecycle.transition(RuntimeState::Paused)?;
        self.scheduler.pause()?;
        Ok(())
    }

    /// Resume the runtime from paused state.
    pub fn resume(&mut self) -> Result<(), AtlasError> {
        self.lifecycle.transition(RuntimeState::Running)?;
        self.scheduler.resume()?;
        Ok(())
    }

    /// Perform graceful shutdown.
    pub fn shutdown(&mut self) -> Result<(), AtlasError> {
        self.lifecycle.transition(RuntimeState::ShuttingDown)?;
        self.scheduler.pause()?;

        let services = self.registry.deinitialize_all()?;
        for service_id in &services {
            self.registry.deinitialize(service_id)?;
        }

        self.lifecycle.transition(RuntimeState::Terminated)?;
        Ok(())
    }

    /// Get the current runtime health status.
    pub fn health_status(&self) -> RuntimeHealth {
        RuntimeHealth {
            runtime_state: self.lifecycle.current_state(),
            services: self.health_monitor.aggregate_health(),
        }
    }

    /// Get a reference to the event bus.
    pub fn event_bus(&self) -> &EventBusImpl {
        &self.event_bus
    }

    /// Get a reference to the service registry.
    pub fn registry(&self) -> &ServiceRegistry {
        &self.registry
    }
}

/// Aggregate runtime health.
#[derive(Debug, Clone)]
pub struct RuntimeHealth {
    pub runtime_state: RuntimeState,
    pub services: Vec<(String, HealthStatus)>,
}



