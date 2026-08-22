//! Replay protection with sequence numbers and sliding windows.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

/// Replay protection service.
#[derive(Clone)]
pub struct ReplayProtection {
    sent_sequences: Arc<Mutex<SequenceTracker>>,
    window_size: usize,
}

impl ReplayProtection {
    pub fn new(window_size: usize) -> Self {
        Self {
            sent_sequences: Arc::new(Mutex::new(SequenceTracker::new(window_size))),
            window_size,
        }
    }

    pub fn check_replay(&self, sender: &str, sequence: u64) -> Result<(), ReplayError> {
        let mut tracker = self.sent_sequences.lock().unwrap();
        if tracker.is_replay(sender, sequence) {
            return Err(ReplayError::ReplayDetected {
                sender: sender.to_string(),
                sequence,
            });
        }
        tracker.record(sender, sequence);
        Ok(())
    }

    pub fn last_sequence(&self, sender: &str) -> Option<u64> {
        let tracker = self.sent_sequences.lock().unwrap();
        tracker.last_sequence(sender)
    }

    pub fn reset_sender(&self, sender: &str) {
        let mut tracker = self.sent_sequences.lock().unwrap();
        tracker.reset(sender);
    }

    pub fn window_size(&self) -> usize {
        self.window_size
    }
}

/// Tracks sequence numbers per sender.
struct SequenceTracker {
    last_accepted: HashMap<String, u64>,
    seen: HashMap<String, std::collections::HashSet<u64>>,
    window_size: usize,
}

impl SequenceTracker {
    fn new(window_size: usize) -> Self {
        Self {
            last_accepted: HashMap::new(),
            seen: HashMap::new(),
            window_size,
        }
    }

    fn is_replay(&mut self, sender: &str, sequence: u64) -> bool {
        let last = self.last_accepted.get(sender).copied().unwrap_or(0);
        if sequence <= last {
            return true;
        }
        let seen = self.seen.entry(sender.to_string()).or_default();
        if seen.contains(&sequence) {
            return true;
        }
        false
    }

    fn record(&mut self, sender: &str, sequence: u64) {
        let last = self.last_accepted.entry(sender.to_string()).or_insert(0);
        if sequence > *last {
            *last = sequence;
        }
        let seen = self.seen.entry(sender.to_string()).or_default();
        seen.insert(sequence);
        if seen.len() > self.window_size {
            let min_seq = *last - self.window_size as u64;
            seen.retain(|&seq| seq >= min_seq);
        }
    }

    fn last_sequence(&self, sender: &str) -> Option<u64> {
        self.last_accepted.get(sender).copied()
    }

    fn reset(&mut self, sender: &str) {
        self.last_accepted.remove(sender);
        self.seen.remove(sender);
    }
}

/// Replay protection errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ReplayError {
    #[error("replay detected: sender={sender}, sequence={sequence}")]
    ReplayDetected { sender: String, sequence: u64 },
}
