//! IPC Router — RFC-0104.
//!
//! Provides deterministic message routing with rule-based flexibility,
//! priority scheduling, dead-letter queue, and endpoint discovery.

pub mod dead_letter_queue;
pub mod discovery;
pub mod priority_queue;
#[allow(clippy::module_inception)] // Preserve the published router::router module path.
pub mod router;
pub mod routes;
pub mod rule_engine;

pub use dead_letter_queue::*;
pub use discovery::*;
pub use priority_queue::*;
pub use router::*;
pub use routes::*;
pub use rule_engine::*;
