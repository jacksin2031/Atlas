//! Channel management — RFC-0105.
//!
//! Defines channel types, ownership, state machine, and registry.

pub mod channel;
pub mod registry;
pub mod context;
pub mod state_machine;

pub use channel::*;
pub use registry::*;
pub use context::*;
pub use state_machine::*;
