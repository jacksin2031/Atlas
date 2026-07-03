//! Negotiation result — outcome of capability negotiation.

use serde::{Deserialize, Serialize};


/// Result of a capability negotiation handshake.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NegotiationResult {
    /// Whether negotiation succeeded.
    pub success: bool,
    /// Matched capabilities.
    pub matched_capabilities: Vec<(String, String)>,
    /// Missing required capabilities.
    pub missing_required: Vec<String>,
    /// Available optional capabilities.
    pub available_optional: Vec<String>,
    /// Fallback capabilities for missing optional ones.
    pub fallbacks: Vec<String>,
    /// Feature flags agreed upon.
    pub feature_flags: Vec<String>,
}

impl NegotiationResult {
    pub fn success(matched: Vec<(String, String)>, optional: Vec<String>) -> Self {
        Self {
            success: true,
            matched_capabilities: matched,
            missing_required: Vec::new(),
            available_optional: optional,
            fallbacks: Vec::new(),
            feature_flags: Vec::new(),
        }
    }

    pub fn failure(missing: Vec<String>) -> Self {
        Self {
            success: false,
            matched_capabilities: Vec::new(),
            missing_required: missing,
            available_optional: Vec::new(),
            fallbacks: Vec::new(),
            feature_flags: Vec::new(),
        }
    }

    pub fn is_success(&self) -> bool {
        self.success
    }
}


