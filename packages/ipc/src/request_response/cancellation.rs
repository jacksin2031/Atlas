//! Cancellation token for request cancellation.

use std::sync::{Arc, Mutex};

type CancelCallback = Box<dyn FnOnce() + Send + Sync>;
type CancelCallbacks = Arc<Mutex<Vec<CancelCallback>>>;

/// Token for cancelling a pending request.
#[derive(Clone, Default)]
pub struct CancellationToken {
    cancelled: Arc<Mutex<bool>>,
    callbacks: CancelCallbacks,
}

impl CancellationToken {
    /// Create a new cancellation token.
    pub fn new() -> Self {
        Self::default()
    }

    /// Cancel the request.
    pub fn cancel(&self) {
        let mut cancelled = self.cancelled.lock().unwrap();
        if *cancelled {
            return;
        }
        *cancelled = true;
        drop(cancelled);

        // Fire callbacks
        let mut callbacks = self.callbacks.lock().unwrap();
        for cb in callbacks.drain(..) {
            cb();
        }
    }

    /// Check if the request has been cancelled.
    pub fn is_cancelled(&self) -> bool {
        *self.cancelled.lock().unwrap()
    }

    /// Register a callback to fire on cancellation.
    pub fn on_cancel<F>(&self, callback: F)
    where
        F: FnOnce() + Send + Sync + 'static,
    {
        let mut callbacks = self.callbacks.lock().unwrap();
        callbacks.push(Box::new(callback));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cancel() {
        let token = CancellationToken::new();
        assert!(!token.is_cancelled());
        token.cancel();
        assert!(token.is_cancelled());
    }

    #[test]
    fn test_cancel_callback() {
        let token = CancellationToken::new();
        let fired = Arc::new(Mutex::new(false));
        let fired_clone = fired.clone();
        token.on_cancel(move || {
            *fired_clone.lock().unwrap() = true;
        });
        token.cancel();
        assert!(*fired.lock().unwrap());
    }
}
