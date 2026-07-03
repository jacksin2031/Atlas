//! Command bus — RFC-0104 integration.
//!
//! CommandBus, CommandHandler, CommandRegistry, CommandDispatcher.

pub mod command;
pub mod handler;
pub mod registry;
pub mod dispatcher;

pub use command::*;
pub use handler::*;
pub use registry::*;
pub use dispatcher::*;
