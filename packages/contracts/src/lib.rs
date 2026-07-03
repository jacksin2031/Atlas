/// Atlas contracts — trait definitions for all core runtime services.
pub mod service;
pub mod event_bus;
pub mod scheduler;
pub mod lifecycle;
pub mod health;
pub mod metrics;
pub mod storage;

// Re-export all types from submodules for convenient access
pub use service::{ServiceId, ServiceName, HealthStatus, ServiceError, ServiceContract};
pub use event_bus::{
    Channel, Event, EventPriority, SubscriptionHandle, EventBusStats,
    EventBusError, EventBus,
};
pub use scheduler::{TaskId, TaskDefinition, QueueDepth, WorkerPoolStatus, SchedulerError, SchedulerController};
pub use lifecycle::{RuntimeState, StateTransitionError, LifecycleManager, is_legal_transition, LEGAL_TRANSITIONS};
pub use health::HealthChecker;
pub use metrics::{
    MetricKind, MetricDescriptor, MetricValue, HistogramBucket, MetricSnapshot,
    MetricsError, MetricsRecorder,
};
pub use storage::{
    ProviderId, ResourceId, TransactionId, ProviderCapability, ProviderState, ResourceState,
    IsolationLevel, ReadOptions, WriteOptions, DeleteOptions, QueryFilter, Pagination,
    ResultSet, ResourceMetadata, Resource, StorageError, StorageProvider, ProviderRegistry,
    LEGAL_PROVIDER_TRANSITIONS, LEGAL_RESOURCE_TRANSITIONS,
    is_legal_provider_transition, is_legal_resource_transition,
};
