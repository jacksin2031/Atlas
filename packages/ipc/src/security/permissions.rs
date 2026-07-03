//! Permission system for IPC access control.

use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// Permission levels for IPC operations.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Hash, PartialOrd, Ord)]
pub enum Permission {
    Send,
    Receive,
    CreateChannel,
    ManageChannel,
    RegisterEndpoint,
    Admin,
}

impl core::fmt::Display for Permission {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            Self::Send => write!(f, "send"),
            Self::Receive => write!(f, "receive"),
            Self::CreateChannel => write!(f, "create_channel"),
            Self::ManageChannel => write!(f, "manage_channel"),
            Self::RegisterEndpoint => write!(f, "register_endpoint"),
            Self::Admin => write!(f, "admin"),
        }
    }
}

/// A set of permissions for a principal.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct PermissionSet {
    permissions: HashSet<Permission>,
}

impl PermissionSet {
    pub fn new() -> Self {
        Self { permissions: HashSet::new() }
    }

    pub fn with_permissions(perms: Vec<Permission>) -> Self {
        Self { permissions: perms.into_iter().collect() }
    }

    pub fn add(&mut self, perm: Permission) {
        self.permissions.insert(perm);
    }

    pub fn has(&self, perm: &Permission) -> bool {
        if self.permissions.contains(&Permission::Admin) {
            return true;
        }
        self.permissions.contains(perm)
    }

    pub fn len(&self) -> usize {
        self.permissions.len()
    }

    pub fn is_empty(&self) -> bool {
        self.permissions.is_empty()
    }
}

/// Validator for permission sets.
#[derive(Debug, Clone, Default)]
pub struct PermissionValidator;

impl PermissionValidator {
    pub fn check(perm_set: &PermissionSet, required: &Permission) -> bool {
        perm_set.has(required)
    }

    pub fn validate_non_empty(perm_set: &PermissionSet, principal: &str) -> Result<(), PermissionError> {
        if perm_set.is_empty() {
            return Err(PermissionError::NoPermissions(principal.to_string()));
        }
        Ok(())
    }

    pub fn validate_no_admin_for_untrusted(perm_set: &PermissionSet, trusted: bool) -> Result<(), PermissionError> {
        if !trusted && perm_set.has(&Permission::Admin) {
            return Err(PermissionError::AdminNotAllowedForUntrusted);
        }
        Ok(())
    }
}

/// Permission errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum PermissionError {
    #[error("principal {0} has no permissions")]
    NoPermissions(String),
    #[error("admin permission not allowed for untrusted principal")]
    AdminNotAllowedForUntrusted,
    #[error("permission denied: required {required}, has {has}")]
    Denied { required: Permission, has: String },
}
