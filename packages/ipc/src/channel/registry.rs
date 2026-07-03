//! Channel registry - lifecycle management for channels.

use std::sync::{Arc, Mutex};
use thiserror::Error;

use super::channel::{Channel, ChannelError}; use super::context::ChannelPermission;
use super::context::ChannelContext;

/// Results of channel operations.
pub type ChannelResult<T> = Result<T, ChannelRegistryError>;

/// Errors from channel registry operations.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum ChannelRegistryError {
    #[error("channel already exists: {0}")]
    AlreadyExists(String),
    #[error("channel not found: {0}")]
    NotFound(String),
    #[error("channel is closed: {0}")]
    ChannelClosed(String),
    #[error("owner mismatch for channel {0}")]
    OwnerMismatch(String),
    #[error("unauthorized participant: {0}")]
    Unauthorized(String),
    #[error("fan-out exceeded for channel {0}")]
    FanOutExceeded(String),
    #[error("illegal state transition: {0}")]
    StateTransition(String),
}

impl From<ChannelError> for ChannelRegistryError {
    fn from(e: ChannelError) -> Self {
        match e {
            ChannelError::IllegalStateTransition { from, to } => {
                ChannelRegistryError::StateTransition(format!("{:?} -> {:?}", from, to))
            }
            ChannelError::NotFound(id) => ChannelRegistryError::NotFound(id),
            ChannelError::OwnerMismatch { expected, .. } => ChannelRegistryError::OwnerMismatch(expected),
            ChannelError::ChannelClosed => ChannelRegistryError::ChannelClosed("closed".into()),
            ChannelError::FanOutExceeded(n) => ChannelRegistryError::FanOutExceeded(format!("{}", n)),
            ChannelError::AuthenticationRequired => ChannelRegistryError::Unauthorized("".into()),
        }
    }
}

/// Registry for managing channel lifecycle.
#[derive(Clone)]
pub struct ChannelRegistry {
    channels: Arc<Mutex<std::collections::HashMap<String, Channel>>>,
    contexts: Arc<Mutex<std::collections::HashMap<String, ChannelContext>>>,
}

impl ChannelRegistry {
    pub fn new() -> Self {
        Self {
            channels: Arc::new(Mutex::new(std::collections::HashMap::new())),
            contexts: Arc::new(Mutex::new(std::collections::HashMap::new())),
        }
    }

    pub fn create(&self, mut channel: Channel) -> ChannelResult<()> {
        let mut chans = self.channels.lock().unwrap();
        let mut ctxs = self.contexts.lock().unwrap();

        if chans.contains_key(&channel.id) {
            return Err(ChannelRegistryError::AlreadyExists(channel.id.clone()));
        }

        channel.transition(super::state_machine::ChannelState::Active)?;
        chans.insert(channel.id.clone(), channel.clone());
        ctxs.insert(channel.id.clone(), ChannelContext::new(channel));

        Ok(())
    }

    pub fn get(&self, id: &str) -> ChannelResult<Channel> {
        let chans = self.channels.lock().unwrap();
        chans.get(id).cloned().ok_or(ChannelRegistryError::NotFound(id.to_string()))
    }

    pub fn get_context(&self, id: &str) -> ChannelResult<ChannelContext> {
        let ctxs = self.contexts.lock().unwrap();
        ctxs.get(id).cloned().ok_or(ChannelRegistryError::NotFound(id.to_string()))
    }

    pub fn exists(&self, id: &str) -> bool {
        let chans = self.channels.lock().unwrap();
        chans.contains_key(id)
    }

    pub fn close(&self, id: &str, owner_id: &str) -> ChannelResult<()> {
        let mut chans = self.channels.lock().unwrap();
        let channel = chans.get_mut(id).ok_or(ChannelRegistryError::NotFound(id.to_string()))?;

        if !channel.validate_owner(owner_id) {
            return Err(ChannelRegistryError::OwnerMismatch(id.to_string()));
        }

        if channel.is_closed() {
            return Err(ChannelRegistryError::ChannelClosed(id.to_string()));
        }

        channel.transition(super::state_machine::ChannelState::Closing)?;
        channel.transition(super::state_machine::ChannelState::Closed)?;
        Ok(())
    }

    pub fn pause(&self, id: &str, owner_id: &str) -> ChannelResult<()> {
        let mut chans = self.channels.lock().unwrap();
        let channel = chans.get_mut(id).ok_or(ChannelRegistryError::NotFound(id.to_string()))?;

        if !channel.validate_owner(owner_id) {
            return Err(ChannelRegistryError::OwnerMismatch(id.to_string()));
        }

        channel.transition(super::state_machine::ChannelState::Paused)?;
        Ok(())
    }

    pub fn resume(&self, id: &str, owner_id: &str) -> ChannelResult<()> {
        let mut chans = self.channels.lock().unwrap();
        let channel = chans.get_mut(id).ok_or(ChannelRegistryError::NotFound(id.to_string()))?;

        if !channel.validate_owner(owner_id) {
            return Err(ChannelRegistryError::OwnerMismatch(id.to_string()));
        }

        channel.transition(super::state_machine::ChannelState::Active)?;
        Ok(())
    }

    pub fn add_participant(&self, channel_id: &str, participant_id: &str) -> ChannelResult<()> {
        let mut ctxs = self.contexts.lock().unwrap();
        let ctx = ctxs.get_mut(channel_id)
            .ok_or(ChannelRegistryError::NotFound(channel_id.to_string()))?;

        ctx.add_participant(participant_id);
        Ok(())
    }

    pub fn is_authorized(&self, channel_id: &str, participant_id: &str, permission: &ChannelPermission) -> bool {
        let ctxs = self.contexts.lock().unwrap();
        ctxs.get(channel_id)
            .map(|ctx| ctx.is_authorized(participant_id, permission))
            .unwrap_or(false)
    }

    pub fn channel_ids(&self) -> Vec<String> {
        let chans = self.channels.lock().unwrap();
        chans.keys().cloned().collect()
    }

    pub fn active_count(&self) -> usize {
        let chans = self.channels.lock().unwrap();
        chans.values().filter(|c| c.is_active()).count()
    }

    pub fn cleanup_closed(&self) -> Vec<String> {
        let mut chans = self.channels.lock().unwrap();
        let mut ctxs = self.contexts.lock().unwrap();
        let closed_ids: Vec<String> = chans.iter()
            .filter(|(_, c)| c.is_closed())
            .map(|(k, _)| k.clone())
            .collect();

        for id in &closed_ids {
            chans.remove(id);
            ctxs.remove(id);
        }
        closed_ids
    }
}

impl Default for ChannelRegistry {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_and_get() {
        let reg = ChannelRegistry::new();
        let ch = Channel::unicast("ch-1", "owner-1");
        reg.create(ch).unwrap();
        let retrieved = reg.get("ch-1").unwrap();
        assert_eq!(retrieved.id, "ch-1");
    }

    #[test]
    fn test_duplicate_create_fails() {
        let reg = ChannelRegistry::new();
        let ch = Channel::unicast("ch-1", "owner-1");
        reg.create(ch.clone()).unwrap();
        assert!(reg.create(ch).is_err());
    }

    #[test]
    fn test_close_requires_owner() {
        let reg = ChannelRegistry::new();
        reg.create(Channel::unicast("ch-1", "owner-1")).unwrap();
        assert!(reg.close("ch-1", "wrong-owner").is_err());
        assert!(reg.close("ch-1", "owner-1").is_ok());
    }

    #[test]
    fn test_pause_and_resume() {
        let reg = ChannelRegistry::new();
        reg.create(Channel::unicast("ch-1", "owner-1")).unwrap();
        assert!(reg.pause("ch-1", "owner-1").is_ok());
        assert!(reg.resume("ch-1", "owner-1").is_ok());
    }

    #[test]
    fn test_participant_management() {
        let reg = ChannelRegistry::new();
        reg.create(Channel::unicast("ch-1", "owner-1")).unwrap();
        reg.add_participant("ch-1", "participant-1").unwrap();
        assert!(reg.is_authorized("ch-1", "participant-1", &ChannelPermission::Read));
    }

    #[test]
    fn test_cleanup_closed() {
        let reg = ChannelRegistry::new();
        reg.create(Channel::unicast("ch-1", "owner-1")).unwrap();
        reg.close("ch-1", "owner-1").unwrap();
        let removed = reg.cleanup_closed();
        assert_eq!(removed.len(), 1);
        assert!(!reg.exists("ch-1"));
    }
}


