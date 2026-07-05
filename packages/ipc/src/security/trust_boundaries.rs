//! Trust boundary enforcement.

use serde::{Deserialize, Serialize};

/// Trust boundaries between IPC components.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum TrustBoundary {
    /// Trusted: same process, same privilege level.
    Internal,
    /// Semi-trusted: plugin sandbox boundary.
    Plugin,
    /// Untrusted: external process boundary.
    External,
    /// Cross-process boundary with encryption.
    EncryptedCrossProcess,
}

impl TrustBoundary {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Internal => "internal",
            Self::Plugin => "plugin",
            Self::External => "external",
            Self::EncryptedCrossProcess => "encrypted-cross-process",
        }
    }

    /// Returns true if messages crossing this boundary require validation.
    pub fn requires_validation(&self) -> bool {
        matches!(
            self,
            Self::Plugin | Self::External | Self::EncryptedCrossProcess
        )
    }

    /// Returns true if messages require encryption across this boundary.
    pub fn requires_encryption(&self) -> bool {
        matches!(self, Self::External | Self::EncryptedCrossProcess)
    }
}

impl Default for TrustBoundary {
    fn default() -> Self {
        Self::Internal
    }
}

/// Validates that a message crosses the appropriate trust boundary.
pub struct TrustBoundaryValidator;

impl TrustBoundaryValidator {
    /// Check if a message from `sender_boundary` can reach `receiver_boundary`.
    pub fn can_communicate(
        sender_boundary: TrustBoundary,
        receiver_boundary: TrustBoundary,
    ) -> bool {
        // Internal can communicate with anyone
        if sender_boundary == TrustBoundary::Internal
            || receiver_boundary == TrustBoundary::Internal
        {
            return true;
        }
        // Same boundary types can communicate
        sender_boundary == receiver_boundary
    }

    /// Validate a message against the expected trust boundary.
    pub fn validate(
        message_sender_boundary: TrustBoundary,
        expected_boundary: TrustBoundary,
    ) -> Result<(), TrustBoundaryError> {
        if !Self::can_communicate(message_sender_boundary, expected_boundary) {
            return Err(TrustBoundaryError::CrossBoundaryForbidden {
                from: message_sender_boundary,
                to: expected_boundary,
            });
        }
        if expected_boundary.requires_validation() {
            // Validation required — in a real implementation this would check signatures
        }
        Ok(())
    }
}

/// Trust boundary errors.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum TrustBoundaryError {
    #[error("cross-boundary communication forbidden: {from:?} -> {to:?}")]
    CrossBoundaryForbidden {
        from: TrustBoundary,
        to: TrustBoundary,
    },
}
