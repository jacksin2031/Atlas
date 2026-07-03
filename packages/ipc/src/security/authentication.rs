//! Authentication abstraction - no hardcoded auth mechanisms.

use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Authentication result.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AuthResult {
    Success { user_id: String, token: String },
    Failed { reason: String },
}

/// Authentication credential types.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CredentialType {
    ApiKey,
    Token,
    Certificate,
    Custom { name: String },
}

/// Epoch-based timestamp.
type EpochTime = u64;

/// Authentication context attached to a session or message.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuthContext {
    pub user_id: String,
    pub credential_type: CredentialType,
    pub authenticated_at_epoch: EpochTime,
    pub metadata: HashMap<String, String>,
}

impl AuthContext {
    pub fn new(user_id: impl Into<String>, credential_type: CredentialType) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            user_id: user_id.into(),
            credential_type,
            authenticated_at_epoch: now,
            metadata: HashMap::new(),
        }
    }

    pub fn with_metadata(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.metadata.insert(key.into(), value.into());
        self
    }
}

/// Trait for authentication providers - implementations are pluggable.
pub trait AuthenticationProvider: Send + Sync {
    fn authenticate(&self, credential: &[u8]) -> AuthResult;
    fn validate_token(&self, token: &str) -> AuthResult;
    fn provider_name(&self) -> &str;
    fn rotate_credentials(&self) -> Result<(), AuthError>;
}

/// Authentication errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum AuthError {
    #[error("authentication failed: {0}")]
    AuthenticationFailed(String),
    #[error("invalid token")]
    InvalidToken,
    #[error("credential rotation failed: {0}")]
    RotationFailed(String),
    #[error("provider not found: {0}")]
    ProviderNotFound(String),
}
