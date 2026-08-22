//! Origin validation for incoming messages.

use std::collections::HashSet;

/// Validates that messages originate from trusted sources.
#[derive(Clone)]
pub struct OriginValidator {
    trusted_origins: HashSet<String>,
    default_policy: DefaultPolicy,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DefaultPolicy {
    /// Reject messages from untrusted origins.
    DenyUnknown,
    /// Allow messages from untrusted origins but log a warning.
    WarnUnknown,
}

impl OriginValidator {
    /// Create a new origin validator with trusted origins.
    pub fn new(trusted_origins: Vec<String>) -> Self {
        Self {
            trusted_origins: trusted_origins.into_iter().collect(),
            default_policy: DefaultPolicy::DenyUnknown,
        }
    }

    /// Set the default policy for unknown origins.
    pub fn with_default_policy(mut self, policy: DefaultPolicy) -> Self {
        self.default_policy = policy;
        self
    }

    /// Validate that an origin is trusted.
    pub fn validate_origin(&self, origin: &str) -> Result<(), OriginValidationError> {
        if self.trusted_origins.contains(origin) {
            return Ok(());
        }
        match self.default_policy {
            DefaultPolicy::DenyUnknown => {
                Err(OriginValidationError::UntrustedOrigin(origin.to_string()))
            }
            DefaultPolicy::WarnUnknown => {
                tracing::warn!(origin, "message from untrusted origin");
                Ok(())
            }
        }
    }

    /// Check if an origin is trusted without raising an error.
    pub fn is_trusted(&self, origin: &str) -> bool {
        self.trusted_origins.contains(origin)
    }

    /// Add a trusted origin.
    pub fn add_trusted_origin(&mut self, origin: impl Into<String>) {
        self.trusted_origins.insert(origin.into());
    }

    /// Remove a trusted origin.
    pub fn remove_trusted_origin(&mut self, origin: &str) -> bool {
        self.trusted_origins.remove(origin)
    }

    /// Get the count of trusted origins.
    pub fn trusted_origin_count(&self) -> usize {
        self.trusted_origins.len()
    }
}

/// Origin validation errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum OriginValidationError {
    #[error("untrusted origin: {0}")]
    UntrustedOrigin(String),
}
