//! Endpoint registry — registration, lookup, discovery, health, permissions.

pub mod endpoint;
pub mod registry;
pub mod descriptor;

pub use endpoint::*;
pub use registry::*;
pub use descriptor::*;
