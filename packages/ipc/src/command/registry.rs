//! Command registry — stores command-handler mappings.

use std::sync::{Arc, Mutex};

use super::command::Command;
use super::handler::CommandHandler;

/// Registry for command handlers.
#[derive(Clone, Default)]
pub struct CommandRegistry {
    handlers: Arc<Mutex<Vec<(String, Arc<dyn CommandHandler>)>>>,
}

impl CommandRegistry {
    /// Register a command handler with a name.
    pub fn register(&self, name: impl Into<String>, handler: Arc<dyn CommandHandler>) {
        let mut handlers = self.handlers.lock().unwrap();
        // Remove existing handler with same name if any
        let name_str = name.into(); handlers.retain(|(n, _)| n != &name_str);
        handlers.push((name_str.clone(), handler));
    }

    /// Unregister a handler by name.
    pub fn unregister(&self, name: &str) -> bool {
        let mut handlers = self.handlers.lock().unwrap();
        let before = handlers.len();
        handlers.retain(|(n, _)| n != name);
        handlers.len() < before
    }

    /// Find a handler that can handle the given command.
    pub fn find_handler(&self, command: &dyn Command) -> Option<Arc<dyn CommandHandler>> {
        let handlers = self.handlers.lock().unwrap();
        for (_, handler) in handlers.iter() {
            if handler.handles(command) {
                return Some(handler.clone());
            }
        }
        None
    }

    /// Get all registered handler names.
    pub fn handler_names(&self) -> Vec<String> {
        let handlers = self.handlers.lock().unwrap();
        handlers.iter().map(|(n, _)| n.clone()).collect()
    }

    /// Get the number of registered handlers.
    pub fn count(&self) -> usize {
        let handlers = self.handlers.lock().unwrap();
        handlers.len()
    }
}


