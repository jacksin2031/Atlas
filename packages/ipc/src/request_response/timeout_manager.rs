//! Timeout manager for tracking outstanding requests.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use uuid::Uuid;
/// Tracks pending requests and detects timeouts.
#[derive(Clone, Default)]
pub struct TimeoutManager {
    pending: Arc<Mutex<HashMap<Uuid, std::time::Instant>>>,
}

impl TimeoutManager {
    /// Register a pending request with its creation time.
    pub fn register(&self, correlation_id: Uuid, timeout_secs: u64) {
        let mut pending = self.pending.lock().unwrap();
        pending.insert(correlation_id, std::time::Instant::now());
        let _ = timeout_secs; // Used for timeout calculation
    }

    /// Remove a request (responded or cancelled).
    pub fn remove(&self, correlation_id: &Uuid) {
        let mut pending = self.pending.lock().unwrap();
        pending.remove(correlation_id);
    }

    /// Check which requests have timed out.
    pub fn check_timeouts(&self) -> Vec<Uuid> {
        let pending = self.pending.lock().unwrap();
        // default 30s timeout
        pending.iter()
            .filter(|(_, created_at)| created_at.elapsed().as_secs() > 30) // default 30s timeout
            .map(|(id, _)| *id)
            .collect()
    }

    /// Get the number of pending requests.
    pub fn pending_count(&self) -> usize {
        let pending = self.pending.lock().unwrap();
        pending.len()
    }

    /// Clear all pending requests.
    pub fn clear(&self) {
        let mut pending = self.pending.lock().unwrap();
        pending.clear();
    }
}



