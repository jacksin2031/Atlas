/// Atlas shared types for the Runtime Foundation.
pub mod event;
pub mod manifest;
pub mod error;
pub mod lifecycle;
pub mod service;
pub mod scheduler_types;
pub mod health;
pub mod config;

// Re-export everything from submodules
pub use event::{Event, Channel, EventPriority, SubscriptionHandle, EventBusStats};
pub use manifest::{
    Manifest, ServiceDeclaration, Capability, PackageType, Permission, ResourceLimits,
    Compatibility,
};
pub use config::{
    Configuration, RuntimeConfig, HealthConfig, SchedulerConfig, MetricsConfig, StorageConfig,
    ProviderConfig,
};
pub use error::{
    AtlasError, ServiceError, EventBusError, SchedulerError,
    ManifestError, ConfigError, HealthError, DependencyError,
};
pub use lifecycle::{RuntimeState, is_legal_transition, LEGAL_TRANSITIONS};
pub use atlas_contracts::StateTransitionError;
pub use service::{ServiceId, ServiceName, HealthStatus};
pub use scheduler_types::{TaskId, TaskDefinition, QueueDepth, WorkerPoolStatus};
// Re-export metrics & storage contracts for downstream crates.
pub use atlas_contracts::{
    MetricKind, MetricDescriptor, MetricValue, HistogramBucket, MetricSnapshot,
    MetricsError, MetricsRecorder,
    ProviderId, ResourceId, TransactionId, ProviderCapability, ProviderState, ResourceState,
    IsolationLevel, ReadOptions, WriteOptions, DeleteOptions, QueryFilter, Pagination,
    ResultSet, ResourceMetadata, Resource, StorageError, StorageProvider, ProviderRegistry,
    LEGAL_PROVIDER_TRANSITIONS, LEGAL_RESOURCE_TRANSITIONS,
    is_legal_provider_transition, is_legal_resource_transition,
};
