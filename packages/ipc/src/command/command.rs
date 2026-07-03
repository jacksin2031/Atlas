//! Command trait — the basis of the command bus.

use std::sync::{Arc, Mutex};
use serde::{Deserialize, Serialize};

/// Trait that all commands MUST implement.
pub trait Command: Send + Sync {
    /// Unique command name for routing.
    fn name(&self) -> &str;

    /// Execute the command and return a result.
    fn execute(&self) -> Result<CommandResult, CommandError>;

    /// Check if the command has been cancelled.
    fn is_cancelled(&self) -> bool;

    /// Request cancellation of this command.
    fn cancel(&self);

    /// Get the command timeout in seconds (0 = no timeout).
    fn timeout(&self) -> u64;

    /// Get the command payload as a JSON value.
    fn payload(&self) -> &serde_json::Value;
}

/// Result of a command execution.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CommandResult {
    pub success: bool,
    pub data: serde_json::Value,
    pub error: Option<String>,
}

impl CommandResult {
    pub fn success(data: impl serde::Serialize) -> Self {
        Self {
            success: true,
            data: serde_json::to_value(data).unwrap_or_else(|_| serde_json::Value::Null),
            error: None,
        }
    }

    pub fn failure(error: impl Into<String>) -> Self {
        Self {
            success: false,
            data: serde_json::Value::Null,
            error: Some(error.into()),
        }
    }
}

/// Errors from command execution.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CommandError {
    #[error("command cancelled")]
    Cancelled,
    #[error("command timed out after {0}s")]
    Timeout(u64),
    #[error("execution failed: {0}")]
    ExecutionFailed(String),
    #[error("handler not found for command: {0}")]
    HandlerNotFound(String),
    #[error("retry limit exceeded")]
    RetryLimitExceeded,
}

/// Internal command state shared between the command and its handler.
#[derive(Debug, Clone, Default)]
pub struct CommandState {
    cancelled: Arc<Mutex<bool>>,
}

impl CommandState {
    pub fn new() -> Self {
        Self {
            cancelled: Arc::new(Mutex::new(false)),
        }
    }

    pub fn is_cancelled(&self) -> bool {
        *self.cancelled.lock().unwrap()
    }

    pub fn cancel(&self) {
        *self.cancelled.lock().unwrap() = true;
    }
}



