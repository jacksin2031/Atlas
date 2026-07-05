//! Channel management — RFC-0105.
//!
//! Defines channel types, ownership, state machine, and registry.

pub mod channel;
pub mod context;
pub mod registry;
pub mod state_machine;

pub use channel::*;
pub use context::*;
pub use registry::*;
pub use state_machine::*;
