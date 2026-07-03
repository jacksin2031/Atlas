//! Authorization service — channel-permission class enforcement.

use std::collections::HashMap;
use crate::message::MessageEnvelope;
use super::permissions::{Permission, PermissionSet};

/// Permission classes for channels.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PermissionClass {
    /// Can only receive.
    ReceiveOnly,
    /// Can send and receive.
    SendReceive,
    /// Can manage the channel.
    Manage,
    /// Full admin access.
    Admin,
}

impl PermissionClass {
    pub fn to_permissions(&self) -> PermissionSet {
        match self {
            Self::ReceiveOnly => PermissionSet::with_permissions(vec![Permission::Receive]),
            Self::SendReceive => PermissionSet::with_permissions(vec![
                Permission::Send,
                Permission::Receive,
            ]),
            Self::Manage => PermissionSet::with_permissions(vec![
                Permission::Send,
                Permission::Receive,
                Permission::ManageChannel,
            ]),
            Self::Admin => PermissionSet::with_permissions(vec![Permission::Admin]),
        }
    }
}

/// Authorization service that enforces channel permissions.
#[derive(Clone, Default)]
pub struct AuthorizationService {
    /// Principal -> permission set mapping.
    principal_permissions: HashMap<String, PermissionSet>,
    /// Channel -> permission class mapping.
    channel_classes: HashMap<String, PermissionClass>,
}

impl AuthorizationService {
    /// Register a principal with a permission set.
    pub fn register_principal(&mut self, principal: impl Into<String>, perms: PermissionSet) {
        self.principal_permissions.insert(principal.into(), perms);
    }

    /// Set the permission class for a channel.
    pub fn set_channel_class(&mut self, channel_id: impl Into<String>, class: PermissionClass) {
        self.channel_classes.insert(channel_id.into(), class);
    }

    /// Check if a principal can send a message.
    pub fn can_send(&self, principal: &str, _message: &MessageEnvelope) -> bool {
        let perms = self.principal_permissions.get(principal);
        match perms {
            Some(p) => p.has(&Permission::Send),
            None => false,
        }
    }

    /// Check if a principal can receive a message.
    pub fn can_receive(&self, principal: &str) -> bool {
        let perms = self.principal_permissions.get(principal);
        match perms {
            Some(p) => p.has(&Permission::Receive),
            None => false,
        }
    }

    /// Check if a principal can manage a channel.
    pub fn can_manage_channel(&self, principal: &str, _channel_id: &str) -> bool {
        let perms = self.principal_permissions.get(principal);
        match perms {
            Some(p) => p.has(&Permission::ManageChannel),
            None => false,
        }
    }

    /// Check if a principal is admin.
    pub fn is_admin(&self, principal: &str) -> bool {
        self.principal_permissions.get(principal)
            .map(|p| p.has(&Permission::Admin))
            .unwrap_or(false)
    }

    /// Check if authorization is granted (any permission).
    pub fn authorize(&self, principal: &str, required: &Permission) -> bool {
        self.principal_permissions.get(principal)
            .map(|p| p.has(required))
            .unwrap_or(false)
    }
}


