//! Session manager — creation, authentication, expiration, renewal, termination.

use std::sync::{Arc, Mutex};
use uuid::Uuid;

use super::context::SessionContext;
use super::session::{Session, SessionState};

/// Results of session operations.
pub type SessionResult<T> = Result<T, SessionError>;

/// Session errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum SessionError {
    #[error("session not found: {0}")]
    NotFound(String),
    #[error("session already exists: {0}")]
    AlreadyExists(String),
    #[error("session is terminated: {0}")]
    Terminated(String),
    #[error("session is expired")]
    Expired,
    #[error("authentication failed")]
    AuthenticationFailed,
    #[error("invalid token")]
    InvalidToken,
}

/// Manages session lifecycle.
#[derive(Clone)]
pub struct SessionManager {
    sessions: Arc<Mutex<Vec<Session>>>,
}

impl SessionManager {
    pub fn new() -> Self {
        Self {
            sessions: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// Create a new session.
    pub fn create(
        &self,
        user_id: impl Into<String>,
        context: SessionContext,
    ) -> SessionResult<Session> {
        let mut sessions = self.sessions.lock().unwrap();
        let mut session = Session::new(user_id, context);
        session.activate();
        sessions.push(session.clone());
        Ok(session)
    }

    /// Get a session by ID.
    pub fn get(&self, id: &Uuid) -> SessionResult<Session> {
        let sessions = self.sessions.lock().unwrap();
        sessions
            .iter()
            .find(|s| &s.id == id)
            .cloned()
            .ok_or(SessionError::NotFound(id.to_string()))
    }

    /// Get a session by user ID (returns the most recent active one).
    pub fn get_by_user(&self, user_id: &str) -> Option<Session> {
        let sessions = self.sessions.lock().unwrap();
        sessions
            .iter()
            .filter(|s| s.user_id == user_id && s.state.is_active())
            .last()
            .cloned()
    }

    /// Terminate a session.
    pub fn terminate(&self, id: &Uuid) -> SessionResult<()> {
        let mut sessions = self.sessions.lock().unwrap();
        let session = sessions
            .iter_mut()
            .find(|s| &s.id == id)
            .ok_or(SessionError::NotFound(id.to_string()))?;

        if session.state == SessionState::Terminated {
            return Err(SessionError::Terminated(id.to_string()));
        }

        session.terminate();
        Ok(())
    }

    /// Renew a session.
    pub fn renew(&self, id: &Uuid) -> SessionResult<()> {
        let mut sessions = self.sessions.lock().unwrap();
        let session = sessions
            .iter_mut()
            .find(|s| &s.id == id)
            .ok_or(SessionError::NotFound(id.to_string()))?;

        session.renew();
        Ok(())
    }

    /// Clean up expired sessions.
    pub fn cleanup_expired(&self) -> Vec<Uuid> {
        let mut sessions = self.sessions.lock().unwrap();
        let mut removed = Vec::new();
        sessions.retain(|s| {
            if s.is_expired() || s.state == SessionState::Terminated {
                removed.push(s.id);
                false
            } else {
                true
            }
        });
        removed
    }

    /// Get all active sessions.
    pub fn active_sessions(&self) -> Vec<Session> {
        let sessions = self.sessions.lock().unwrap();
        sessions
            .iter()
            .filter(|s| s.state.is_active() && !s.is_expired())
            .cloned()
            .collect()
    }

    /// Get the count of active sessions.
    pub fn active_count(&self) -> usize {
        let sessions = self.sessions.lock().unwrap();
        sessions
            .iter()
            .filter(|s| s.state.is_active() && !s.is_expired())
            .count()
    }

    /// Get the total session count.
    pub fn total_count(&self) -> usize {
        let sessions = self.sessions.lock().unwrap();
        sessions.len()
    }
}

impl Default for SessionManager {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::session::context::SessionContext;

    #[test]
    fn test_create_and_get() {
        let mgr = SessionManager::new();
        let ctx = SessionContext::new("user-1");
        let session = mgr.create("user-1", ctx).unwrap();
        let retrieved = mgr.get(&session.id).unwrap();
        assert_eq!(retrieved.user_id, "user-1");
    }

    #[test]
    fn test_terminate() {
        let mgr = SessionManager::new();
        let ctx = SessionContext::new("user-1");
        let session = mgr.create("user-1", ctx).unwrap();
        mgr.terminate(&session.id).unwrap();
        assert!(mgr.get(&session.id).unwrap().state == SessionState::Terminated);
    }

    #[test]
    fn test_cleanup_expired() {
        let mgr = SessionManager::new();
        let ctx = SessionContext::new("user-1");
        let session = mgr.create("user-1", ctx).unwrap();
        mgr.terminate(&session.id).unwrap();
        let removed = mgr.cleanup_expired();
        assert_eq!(removed.len(), 1);
    }

    #[test]
    fn test_active_count() {
        let mgr = SessionManager::new();
        let ctx = SessionContext::new("user-1");
        mgr.create("user-1", ctx).unwrap();
        assert_eq!(mgr.active_count(), 1);
    }
}
