pub mod config;
pub mod error;
/// Atlas shared types for the Runtime Foundation.
pub mod event;
pub mod health;
pub mod lifecycle;
pub mod manifest;
pub mod scheduler_types;
pub mod service;

// Re-export everything from submodules
pub use atlas_contracts::StateTransitionError;
pub use config::{
    Configuration, HealthConfig, MetricsConfig, ProviderConfig, RuntimeConfig, SchedulerConfig,
    StorageConfig,
};
pub use error::{
    AtlasError, ConfigError, DependencyError, EventBusError, HealthError, ManifestError,
    SchedulerError, ServiceError,
};
pub use event::{Channel, Event, EventBusStats, EventPriority, SubscriptionHandle};
pub use lifecycle::{is_legal_transition, RuntimeState, LEGAL_TRANSITIONS};
pub use manifest::{
    Capability, Compatibility, Manifest, PackageType, Permission, ResourceLimits,
    ServiceDeclaration,
};
pub use scheduler_types::{QueueDepth, TaskDefinition, TaskId, WorkerPoolStatus};
pub use service::{HealthStatus, ServiceId, ServiceName};
// Re-export metrics & storage contracts for downstream crates.
pub use atlas_contracts::{
    is_legal_provider_transition, is_legal_resource_transition, DeleteOptions, HistogramBucket,
    IsolationLevel, MetricDescriptor, MetricKind, MetricSnapshot, MetricValue, MetricsError,
    MetricsRecorder, Pagination, ProviderCapability, ProviderId, ProviderRegistry, ProviderState,
    QueryFilter, ReadOptions, Resource, ResourceId, ResourceMetadata, ResourceState, ResultSet,
    StorageError, StorageProvider, TransactionId, WriteOptions, LEGAL_PROVIDER_TRANSITIONS,
    LEGAL_RESOURCE_TRANSITIONS,
};
