//! Endpoint registry — registration, lookup, discovery, health, permissions.

pub mod descriptor;
#[allow(clippy::module_inception)] // Preserve the published endpoint::endpoint module path.
pub mod endpoint;
pub mod registry;

pub use descriptor::*;
pub use endpoint::*;
pub use registry::*;
