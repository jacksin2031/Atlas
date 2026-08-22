pub mod event_bus;
pub mod health;
pub mod lifecycle;
pub mod metrics;
pub mod scheduler;
/// Atlas contracts — trait definitions for all core runtime services.
pub mod service;
pub mod storage;

// Re-export all types from submodules for convenient access
pub use event_bus::{
    Channel, Event, EventBus, EventBusError, EventBusStats, EventPriority, SubscriptionHandle,
};
pub use health::HealthChecker;
pub use lifecycle::{
    is_legal_transition, LifecycleManager, RuntimeState, StateTransitionError, LEGAL_TRANSITIONS,
};
pub use metrics::{
    HistogramBucket, MetricDescriptor, MetricKind, MetricSnapshot, MetricValue, MetricsError,
    MetricsRecorder,
};
pub use scheduler::{
    QueueDepth, SchedulerController, SchedulerError, TaskDefinition, TaskId, WorkerPoolStatus,
};
pub use service::{HealthStatus, ServiceContract, ServiceError, ServiceId, ServiceName};
pub use storage::{
    is_legal_provider_transition, is_legal_resource_transition, DeleteOptions, IsolationLevel,
    Pagination, ProviderCapability, ProviderId, ProviderRegistry, ProviderState, QueryFilter,
    ReadOptions, Resource, ResourceId, ResourceMetadata, ResourceState, ResultSet, StorageError,
    StorageProvider, TransactionId, WriteOptions, LEGAL_PROVIDER_TRANSITIONS,
    LEGAL_RESOURCE_TRANSITIONS,
};
