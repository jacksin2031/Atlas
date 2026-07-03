//! Reliability layer — RFC-0108.
//!
//! Delivery guarantees, ordering guarantees, retry policies, and DLQ management.

pub mod delivery_guarantees;
pub mod ordering;
pub mod retry;
pub mod dlq_manager;

pub use delivery_guarantees::*;
pub use ordering::*;
pub use retry::*;
pub use dlq_manager::*;
