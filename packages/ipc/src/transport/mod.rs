//! Transport abstraction — RFC-0103.
//!
//! Defines the `Transport` trait and a reference in-memory implementation.
//! All transports MUST be platform-independent.

pub mod transport;
pub mod in_memory_transport;
pub mod factory;

pub use transport::*;
pub use in_memory_transport::*;
pub use factory::*;
