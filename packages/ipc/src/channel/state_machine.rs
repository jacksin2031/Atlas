//! Channel state machine — RFC-0105 §20.

use serde::{Deserialize, Serialize};

/// Channel lifecycle states.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ChannelState {
    /// Channel is being created.
    Creating,
    /// Channel is active and accepting messages.
    Active,
    /// Channel is temporarily paused.
    Paused,
    /// Channel is closing (draining messages).
    Closing,
    /// Channel is fully closed.
    Closed,
}

impl ChannelState {
    /// Returns true if the channel can accept messages.
    pub fn accepts_messages(&self) -> bool {
        matches!(self, Self::Active)
    }

    /// Returns a human-readable label.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Creating => "creating",
            Self::Active => "active",
            Self::Paused => "paused",
            Self::Closing => "closing",
            Self::Closed => "closed",
        }
    }
}

impl Default for ChannelState {
    fn default() -> Self {
        Self::Creating
    }
}

impl core::fmt::Display for ChannelState {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.label())
    }
}
