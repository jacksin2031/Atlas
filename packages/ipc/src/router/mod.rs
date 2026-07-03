//! IPC Router — RFC-0104.
//!
//! Provides deterministic message routing with rule-based flexibility,
//! priority scheduling, dead-letter queue, and endpoint discovery.

pub mod router;
pub mod routes;
pub mod rule_engine;
pub mod priority_queue;
pub mod dead_letter_queue;
pub mod discovery;

pub use router::*;
pub use routes::*;
pub use rule_engine::*;
pub use priority_queue::*;
pub use dead_letter_queue::*;
pub use discovery::*;
