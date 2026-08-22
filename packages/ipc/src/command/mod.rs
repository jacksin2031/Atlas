//! Command bus — RFC-0104 integration.
//!
//! CommandBus, CommandHandler, CommandRegistry, CommandDispatcher.

#[allow(clippy::module_inception)] // Preserve the published command::command module path.
pub mod command;
pub mod dispatcher;
pub mod handler;
pub mod registry;

pub use command::*;
pub use dispatcher::*;
pub use handler::*;
pub use registry::*;
