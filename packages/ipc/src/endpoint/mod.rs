//! Endpoint registry — registration, lookup, discovery, health, permissions.

pub mod descriptor;
pub mod endpoint;
pub mod registry;

pub use descriptor::*;
pub use endpoint::*;
pub use registry::*;
