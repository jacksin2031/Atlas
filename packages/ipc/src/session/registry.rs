//! Session registry — stores and queries active sessions.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use uuid::Uuid;

use super::session::Session;

/// Registry for session storage and lookup.
#[derive(Clone)]
pub struct SessionRegistry {
    sessions: Arc<Mutex<HashMap<Uuid, Session>>>,
}

impl SessionRegistry {
    pub fn new() -> Self {
        Self {
            sessions: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    /// Store a session.
    pub fn store(&self, session: Session) {
        let mut sessions = self.sessions.lock().unwrap();
        sessions.insert(session.id, session);
    }

    /// Retrieve a session by ID.
    pub fn retrieve(&self, id: &Uuid) -> Option<Session> {
        let sessions = self.sessions.lock().unwrap();
        sessions.get(id).cloned()
    }

    /// Remove a session.
    pub fn remove(&self, id: &Uuid) -> bool {
        let mut sessions = self.sessions.lock().unwrap();
        sessions.remove(id).is_some()
    }

    /// Get all sessions.
    pub fn all_sessions(&self) -> Vec<Session> {
        let sessions = self.sessions.lock().unwrap();
        sessions.values().cloned().collect()
    }

    /// Get the count of stored sessions.
    pub fn count(&self) -> usize {
        let sessions = self.sessions.lock().unwrap();
        sessions.len()
    }
}

impl Default for SessionRegistry {
    fn default() -> Self {
        Self::new()
    }
}
