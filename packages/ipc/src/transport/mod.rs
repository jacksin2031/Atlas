//! Transport abstraction — RFC-0103.
//!
//! Defines the `Transport` trait and a reference in-memory implementation.
//! All transports MUST be platform-independent.

pub mod factory;
pub mod in_memory_transport;
#[allow(clippy::module_inception)] // Preserve the published transport::transport module path.
pub mod transport;

pub use factory::*;
pub use in_memory_transport::*;
pub use transport::*;

pub mod adapters;

pub use adapters::*;
