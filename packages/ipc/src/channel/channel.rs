//! Channel types and core channel definition.

use serde::{Deserialize, Serialize};
use super::state_machine::ChannelState;

/// Channel types supported by the IPC runtime.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ChannelType {
    Unicast,
    Multicast,
    Broadcast,
    Private,
    System,
}

impl ChannelType {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Unicast => "unicast",
            Self::Multicast => "multicast",
            Self::Broadcast => "broadcast",
            Self::Private => "private",
            Self::System => "system",
        }
    }
}

pub const DEFAULT_MAX_BROADCAST_FANOUT: usize = 1000;

/// Epoch-based timestamp.
type EpochTime = u64;

/// A channel is a communication pathway between endpoints.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Channel {
    pub id: String,
    pub channel_type: ChannelType,
    pub owner_id: String,
    pub state: ChannelState,
    pub max_fanout: usize,
    pub requires_auth: bool,
    pub created_epoch: EpochTime,
}

impl Channel {
    pub fn unicast(id: impl Into<String>, owner: impl Into<String>) -> Self {
        Self::new(id, owner, ChannelType::Unicast, 1, false)
    }

    pub fn broadcast(id: impl Into<String>, owner: impl Into<String>) -> Self {
        Self::new(id, owner, ChannelType::Broadcast, DEFAULT_MAX_BROADCAST_FANOUT, false)
    }

    pub fn private(id: impl Into<String>, owner: impl Into<String>) -> Self {
        Self::new(id, owner, ChannelType::Private, 100, true)
    }

    pub fn system(id: impl Into<String>) -> Self {
        Self::new(id, "system", ChannelType::System, 0, false)
    }

    fn new(id: impl Into<String>, owner: impl Into<String>, channel_type: ChannelType, max_fanout: usize, requires_auth: bool) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            id: id.into(),
            channel_type,
            owner_id: owner.into(),
            state: ChannelState::Creating,
            max_fanout,
            requires_auth,
            created_epoch: now,
        }
    }

    pub fn transition(&mut self, new_state: ChannelState) -> Result<(), ChannelError> {
        use ChannelState::*;
        let current = self.state;
        match (current, new_state) {
            (Creating, Active) => {}
            (Active, Paused) => {}
            (Paused, Active) => {}
            (Active, Closing) => {}
            (Paused, Closing) => {}
            (Closing, Closed) => {}
            (Active, Closed) => {}
            _ => return Err(ChannelError::IllegalStateTransition { from: current, to: new_state }),
        }
        self.state = new_state;
        Ok(())
    }

    pub fn is_active(&self) -> bool {
        matches!(self.state, ChannelState::Active)
    }

    pub fn is_closed(&self) -> bool {
        matches!(self.state, ChannelState::Closed)
    }

    pub fn validate_owner(&self, caller_id: &str) -> bool {
        caller_id == self.owner_id || caller_id == "system"
    }
}

/// Channel errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ChannelError {
    #[error("illegal state transition: {from:?} -> {to:?}")]
    IllegalStateTransition { from: ChannelState, to: ChannelState },
    #[error("channel not found: {0}")]
    NotFound(String),
    #[error("owner mismatch: expected {expected}, got {got}")]
    OwnerMismatch { expected: String, got: String },
    #[error("channel is closed")]
    ChannelClosed,
    #[error("fan-out exceeded: {0}")]
    FanOutExceeded(usize),
    #[error("authentication required")]
    AuthenticationRequired,
}
