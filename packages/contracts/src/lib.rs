/// Atlas contracts — trait definitions for all core runtime services.
pub mod service;
pub mod event_bus;
pub mod scheduler;
pub mod lifecycle;
pub mod health;

// Re-export all types from submodules for convenient access
pub use service::{ServiceId, ServiceName, HealthStatus, ServiceError, ServiceContract};
pub use event_bus::{
    Channel, Event, EventPriority, SubscriptionHandle, EventBusStats,
    EventBusError, EventBus,
};
pub use scheduler::{TaskId, TaskDefinition, QueueDepth, WorkerPoolStatus, SchedulerError, SchedulerController};
pub use lifecycle::{RuntimeState, StateTransitionError, LifecycleManager, is_legal_transition, LEGAL_TRANSITIONS};
