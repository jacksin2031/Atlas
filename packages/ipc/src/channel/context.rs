//! Channel context — ownership, permissions, and state tracking.

use serde::{Deserialize, Serialize};
use std::collections::HashSet;

use super::channel::Channel;

/// Permissions for channel access.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ChannelPermission {
    /// Can read/send messages on the channel.
    Read,
    /// Can send messages on the channel.
    Write,
    /// Can manage the channel (create/close).
    Manage,
    /// Full access.
    Admin,
}

/// Context attached to a channel for runtime tracking.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChannelContext {
    /// The channel this context belongs to.
    pub channel: Channel,
    /// Authorized participant IDs.
    pub participants: HashSet<String>,
    /// Permissions for each participant.
    pub permissions: Vec<ChannelPermission>,
    /// Message sequence counter.
    pub message_sequence: u64,
    /// Whether the channel is encrypted.
    pub encrypted: bool,
}

impl ChannelContext {
    /// Create a new channel context.
    pub fn new(channel: Channel) -> Self {
        Self {
            channel,
            participants: HashSet::new(),
            permissions: vec![ChannelPermission::Admin],
            message_sequence: 0,
            encrypted: false,
        }
    }

    /// Add a participant to the channel.
    pub fn add_participant(&mut self, participant_id: impl Into<String>) {
        self.participants.insert(participant_id.into());
    }

    /// Check if a participant is authorized.
    pub fn is_authorized(
        &self,
        participant_id: &str,
        required_permission: &ChannelPermission,
    ) -> bool {
        if !self.participants.contains(participant_id) {
            return false;
        }
        // Admin has all permissions
        if self.permissions.contains(&ChannelPermission::Admin) {
            return true;
        }
        // Check specific permission hierarchy
        match required_permission {
            ChannelPermission::Admin => self.permissions.contains(&ChannelPermission::Admin),
            ChannelPermission::Manage => {
                self.permissions.contains(&ChannelPermission::Manage)
                    || self.permissions.contains(&ChannelPermission::Admin)
            }
            ChannelPermission::Write => {
                self.permissions.contains(&ChannelPermission::Write)
                    || self.permissions.contains(&ChannelPermission::Manage)
                    || self.permissions.contains(&ChannelPermission::Admin)
            }
            ChannelPermission::Read => true, // Everyone in participants can read
        }
    }

    /// Increment the message sequence.
    pub fn next_sequence(&mut self) -> u64 {
        self.message_sequence += 1;
        self.message_sequence
    }

    /// Check if the channel is healthy.
    pub fn is_healthy(&self) -> bool {
        self.channel.is_active() && !self.participants.is_empty()
    }
}
