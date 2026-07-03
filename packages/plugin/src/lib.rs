#![allow(dead_code)]
//! Atlas Plugin Runtime — the extensible platform layer (Sprint 3).
//!
//! Implements the complete Plugin Runtime per the Atlas ADS, ADRs, and Plugin
//! RFCs (RFC-0201 through RFC-0229). Provides plugin manifest parsing and
//! validation, a central registry, a deterministic loader, the plugin lifecycle
//! state machine, dependency resolution with cycle detection, a capability
//! registry, the plugin context, plugin health integration, a sandbox
//! abstraction, and event-bus integration.
//!
//! The crate follows the Runtime architecture established in Sprint 1/2:
//! contracts-first, dependency injection, interior mutability, [`Send`] +
//! [`Sync`] services, and no global mutable state.

pub mod capability;
pub mod config;
pub mod contracts;
pub mod context;
pub mod dependency;
pub mod error;
pub mod events;
pub mod health;
pub mod lifecycle;
pub mod loader;
pub mod manager;
pub mod manifest;
pub mod registry;
pub mod sandbox;
pub mod version;

// Re-export the primary public API.
pub use capability::{CapabilityDeclaration, CapabilityRegistry, CapabilityRegistryImpl, PluginCapability, PluginId};
pub use config::{PluginConfig, PluginConfigSnapshot};
pub use contracts::{
    Plugin, PluginFactory, PluginHost, PluginLoader, PluginManager, PluginMetadata, PluginProvider,
    PluginRegistry,
};
pub use context::{CapturingLogger, CapabilityServiceDirectory, PluginContext, PluginContextBuilder, PluginLogger, PluginServiceDirectory, TracingLogger};
pub use dependency::{DependencyResolver, ResolutionResult};
pub use error::PluginError;
pub use events::{PluginEvent, PluginEventBusImpl, PluginEventType, PLUGIN_CHANNEL};
pub use health::{PluginHealthMonitor, PluginHealthServiceImpl, PluginHealthState};
pub use lifecycle::{
    is_legal_plugin_transition, is_runtime_compatible, PluginLifecycleManager, PluginState,
    PluginStateCategory, LEGAL_PLUGIN_TRANSITIONS,
};
pub use loader::PluginLoaderImpl;
pub use manager::PluginManagerImpl;
pub use manifest::{
    DependencyType, PermissionLevel, PluginCompatibility, PluginDependency, PluginManifest,
    PluginPermission, PluginResourceLimits, PluginType,
};
pub use registry::PluginRegistryImpl;
pub use sandbox::{NoopSandboxExecutor, ResourceUsage, SandboxBoundary, SandboxExecutor, SandboxPolicy};
pub use version::{ConstraintOperator, SemanticVersion, VersionConstraint};
