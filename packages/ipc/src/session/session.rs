//! Session types and lifecycle.

use super::context::SessionContext;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Session lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SessionState {
    Creating,
    Active,
    Renewing,
    Expiring,
    Terminated,
}

impl SessionState {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Creating => "creating",
            Self::Active => "active",
            Self::Renewing => "renewing",
            Self::Expiring => "expiring",
            Self::Terminated => "terminated",
        }
    }

    pub fn is_active(&self) -> bool {
        matches!(self, Self::Active | Self::Renewing)
    }
}

/// Epoch-based timestamp for serialization.
type EpochTime = u64;

/// A session representing an authenticated IPC communication context.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Session {
    pub id: Uuid,
    pub user_id: String,
    pub state: SessionState,
    pub created_epoch: EpochTime,
    pub expires_after_secs: u64,
    pub context: SessionContext,
}

impl Session {
    pub fn new(user_id: impl Into<String>, context: SessionContext) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            id: Uuid::new_v4(),
            user_id: user_id.into(),
            state: SessionState::Creating,
            created_epoch: now,
            expires_after_secs: 3600,
            context,
        }
    }

    pub fn activate(&mut self) {
        self.state = SessionState::Active;
    }

    pub fn is_expired(&self) -> bool {
        let elapsed = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        elapsed - self.created_epoch >= self.expires_after_secs
    }

    pub fn renew(&mut self) {
        self.state = SessionState::Renewing;
        self.created_epoch = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        self.state = SessionState::Active;
    }

    pub fn terminate(&mut self) {
        self.state = SessionState::Terminated;
    }

    pub fn is_valid(&self) -> bool {
        self.state.is_active() && !self.is_expired()
    }
}
