//! Command handler trait.

use super::command::{Command, CommandResult, CommandError};

/// Trait that command handlers MUST implement.
pub trait CommandHandler: Send + Sync {
    /// Check if this handler can handle the given command.
    fn handles(&self, command: &dyn Command) -> bool;

    /// Handle the command and return a result.
    fn handle(&self, command: &dyn Command) -> Result<CommandResult, CommandError>;
}

/// A simple handler adapter for functions.
pub struct FunctionHandler<F>
where
    F: Fn(&dyn Command) -> Result<CommandResult, CommandError> + Send + Sync,
{
    func: F,
    command_name: String,
}

impl<F> FunctionHandler<F>
where
    F: Fn(&dyn Command) -> Result<CommandResult, CommandError> + Send + Sync,
{
    pub fn new(command_name: impl Into<String>, func: F) -> Self {
        Self {
            command_name: command_name.into(),
            func,
        }
    }
}

impl<F> CommandHandler for FunctionHandler<F>
where
    F: Fn(&dyn Command) -> Result<CommandResult, CommandError> + Send + Sync,
{
    fn handles(&self, command: &dyn Command) -> bool {
        command.name() == self.command_name
    }

    fn handle(&self, command: &dyn Command) -> Result<CommandResult, CommandError> {
        (self.func)(command)
    }
}
