/// Atlas shared types for the Runtime Foundation.
pub mod event;
pub mod manifest;
pub mod error;
pub mod lifecycle;
pub mod service;
pub mod scheduler_types;
pub mod health;

// Re-export everything from submodules
pub use event::{Event, Channel, EventPriority, SubscriptionHandle, EventBusStats};
pub use manifest::{Manifest, ServiceDeclaration, Capability};
pub use error::{
    AtlasError, ServiceError, EventBusError, SchedulerError,
    ManifestError, ConfigError, HealthError, DependencyError,
};
pub use lifecycle::{RuntimeState, is_legal_transition, LEGAL_TRANSITIONS};
pub use atlas_contracts::StateTransitionError;
pub use service::{ServiceId, ServiceName, HealthStatus};
pub use scheduler_types::{TaskId, TaskDefinition, QueueDepth, WorkerPoolStatus};
