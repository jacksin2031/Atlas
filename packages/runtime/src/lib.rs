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
pub mod metrics;
pub mod error;

use atlas_common::{AtlasError, HealthStatus};
use atlas_contracts::{RuntimeState, ServiceContract};
use registry::ServiceRegistry;
use lifecycle::LifecycleManager;
use eventbus::EventBusImpl;
use scheduler::SchedulerImpl;
use health::HealthService;
use config::ConfigService;
use manifest::ManifestService;
use metrics::MetricsService;
use dependency::DependencyResolver;

/// The Atlas Runtime — central coordinator for all core services.
pub struct AtlasRuntime {
    lifecycle: LifecycleManager,
    registry: ServiceRegistry,
    event_bus: EventBusImpl,
    scheduler: SchedulerImpl,
    health: HealthService,
    config: ConfigService,
    manifest: ManifestService,
    metrics: MetricsService,
    dependency_resolver: DependencyResolver,
}

impl AtlasRuntime {
    /// Bootstrap the runtime from a configuration file path.
    pub fn bootstrap(config_path: &str) -> Result<Self, AtlasError> {
        // Configuration Service loads and parses the configuration document.
        let mut config = ConfigService::new();
        config.load(config_path).map_err(AtlasError::from)?;
        config.initialize().map_err(AtlasError::from)?;
        config.start().map_err(AtlasError::from)?;

        // Manifest Service loads and validates the manifest (RFC-0010 §12).
        let mut manifest = ManifestService::new();
        manifest
            .load_from_config(&config)
            .map_err(AtlasError::from)?;
        manifest.initialize().map_err(AtlasError::from)?;
        manifest.start().map_err(AtlasError::from)?;

        let mut lifecycle = LifecycleManager::new();
        let mut event_bus = EventBusImpl::new();
        let scheduler = SchedulerImpl::new(&event_bus);
        let mut health = HealthService::new();
        health.initialize().map_err(AtlasError::from)?;
        health.start().map_err(AtlasError::from)?;
        let mut metrics = MetricsService::new();
        metrics.initialize().map_err(AtlasError::from)?;
        metrics.start().map_err(AtlasError::from)?;
        let mut registry = ServiceRegistry::new();
        let dependency_resolver = DependencyResolver::new();

        lifecycle.transition(RuntimeState::Initializing)?;

        let services = manifest.discover_services().map_err(AtlasError::from)?;
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
            health,
            config,
            manifest,
            metrics,
            dependency_resolver,
        })
    }

    /// Activate the runtime — transition to Running state.
    ///
    /// Configuration is frozen (made immutable) once the Runtime reaches the
    /// Running state, per RFC-0010 §4.
    pub fn activate(&mut self) -> Result<(), AtlasError> {
        self.lifecycle.transition(RuntimeState::Running)?;
        self.config.freeze();
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
            services: self.health.all_health(),
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

    /// Get a reference to the configuration service.
    pub fn config(&self) -> &ConfigService {
        &self.config
    }

    /// Get a reference to the manifest service.
    pub fn manifest(&self) -> &ManifestService {
        &self.manifest
    }

    /// Get a reference to the metrics service.
    pub fn metrics(&self) -> &MetricsService {
        &self.metrics
    }

    /// Get a reference to the health service.
    pub fn health(&self) -> &HealthService {
        &self.health
    }

    /// Get a reference to the dependency resolver.
    pub fn dependency_resolver(&self) -> &DependencyResolver {
        &self.dependency_resolver
    }
}

/// Aggregate runtime health.
#[derive(Debug, Clone)]
pub struct RuntimeHealth {
    pub runtime_state: RuntimeState,
    pub services: Vec<(String, HealthStatus)>,
}



