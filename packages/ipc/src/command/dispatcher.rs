//! Command dispatcher — routes commands to handlers with timeout, retry, cancellation.

use std::time::Duration;

use super::command::{Command, CommandResult, CommandError};
use super::registry::CommandRegistry;
use crate::reliability::RetryPolicy;

/// Result of dispatching a command.
#[derive(Debug, Clone)]
pub struct DispatchResult {
    pub command_name: String,
    pub result: Result<CommandResult, CommandError>,
    pub attempts: u32,
    pub duration: Duration,
}

/// Dispatches commands to registered handlers.
pub struct CommandDispatcher {
    registry: CommandRegistry,
    default_retry_policy: RetryPolicy,
}

impl CommandDispatcher {
    /// Create a new dispatcher with the given registry.
    pub fn new(registry: CommandRegistry) -> Self {
        Self {
            registry,
            default_retry_policy: RetryPolicy::default(),
        }
    }

    /// Create with a custom default retry policy.
    pub fn with_retry_policy(mut self, policy: RetryPolicy) -> Self {
        self.default_retry_policy = policy;
        self
    }

    /// Dispatch a command with default retry policy.
    pub fn dispatch(&self, command: &dyn Command) -> DispatchResult {
        self.dispatch_with_policy(command, &self.default_retry_policy)
    }

    /// Dispatch a command with a specific retry policy.
    pub fn dispatch_with_policy(
        &self,
        command: &dyn Command,
        policy: &RetryPolicy,
    ) -> DispatchResult {
        let start = std::time::Instant::now();
        let command_name = command.name().to_string();
        let mut attempts = 0u32;

        loop {
            attempts += 1;

            // Check cancellation
            if command.is_cancelled() {
                return DispatchResult {
                    command_name: command_name.clone(),
                    result: Err(CommandError::Cancelled),
                    attempts,
                    duration: start.elapsed(),
                };
            }

            // Check timeout
            if command.timeout() > 0 {
                let elapsed = start.elapsed().as_secs();
                if elapsed >= command.timeout() {
                    return DispatchResult {
                        command_name: command_name.clone(),
                        result: Err(CommandError::Timeout(command.timeout())),
                        attempts,
                        duration: start.elapsed(),
                    };
                }
            }

            // Find handler
            let handler = match self.registry.find_handler(command) {
                Some(h) => h,
                None => {
                    return DispatchResult {
                        command_name: command_name.clone(),
                        result: Err(CommandError::HandlerNotFound(command.name().to_string())),
                        attempts,
                        duration: start.elapsed(),
                    };
                }
            };

            // Execute
            match handler.handle(command) {
                Ok(result) => {
                    return DispatchResult {
                        command_name: command_name.clone(),
                        result: Ok(result),
                        attempts,
                        duration: start.elapsed(),
                    };
                }
                Err(e) => {
                    // Check if we should retry
                    if !policy.should_retry(attempts) {
                        return DispatchResult {
                            command_name: command_name.clone(),
                            result: Err(e),
                            attempts,
                            duration: start.elapsed(),
                        };
                    }
                    if !policy.should_retry_error(&e.to_string()) {
                        return DispatchResult {
                            command_name: command_name.clone(),
                            result: Err(e),
                            attempts,
                            duration: start.elapsed(),
                        };
                    }
                    // Wait before retry
                    let delay = policy.delay_for_attempt(attempts);
                    std::thread::sleep(delay);
                }
            }
        }
    }

    /// Cancel a running command (by finding it in the registry).
    pub fn cancel_command(&self, command: &dyn Command) {
        command.cancel();
    }

    /// Get the handler count.
    pub fn handler_count(&self) -> usize {
        self.registry.count()
    }
}

impl Default for CommandDispatcher {
    fn default() -> Self {
        Self::new(CommandRegistry::default())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Mutex};
    use crate::CommandHandler;

    // A simple test command
    struct TestCommand {
        name: String,
        payload: serde_json::Value,
        cancelled: std::sync::Arc<std::sync::Mutex<bool>>,
    }

    impl TestCommand {
        fn new(name: &str) -> Self {
            Self {
                name: name.to_string(),
                payload: serde_json::Value::Null,
                cancelled: Arc::new(Mutex::new(false)),
            }
        }
    }

    impl Command for TestCommand {
        fn name(&self) -> &str { &self.name }
        fn execute(&self) -> Result<CommandResult, CommandError> {
            Ok(CommandResult::success("done"))
        }
        fn is_cancelled(&self) -> bool { *self.cancelled.lock().unwrap() }
        fn cancel(&self) { *self.cancelled.lock().unwrap() = true; }
        fn timeout(&self) -> u64 { 0 }
        fn payload(&self) -> &serde_json::Value { &self.payload }
    }

    #[test]
    fn test_dispatch_success() {
        let registry = CommandRegistry::default();
        registry.register("test-cmd", Arc::new(TestHandler));
        let dispatcher = CommandDispatcher::new(registry);
        let cmd = TestCommand::new("test-cmd");
        let result = dispatcher.dispatch(&cmd);
        assert!(result.result.is_ok());
        assert_eq!(result.attempts, 1);
    }

    #[test]
    fn test_dispatch_no_handler() {
        let registry = CommandRegistry::default();
        let dispatcher = CommandDispatcher::new(registry);
        let cmd = TestCommand::new("unknown");
        let result = dispatcher.dispatch(&cmd);
        assert!(result.result.is_err());
    }

    struct TestHandler;

    impl CommandHandler for TestHandler {
        fn handles(&self, command: &dyn Command) -> bool {
            command.name() == "test-cmd"
        }
        fn handle(&self, _command: &dyn Command) -> Result<CommandResult, CommandError> {
            Ok(CommandResult::success("handled"))
        }
    }
}


