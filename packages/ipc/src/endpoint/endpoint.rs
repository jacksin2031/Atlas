//! Endpoint definition.

use super::descriptor::EndpointDescriptor;
use serde::{Deserialize, Serialize};

/// Endpoint health status.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EndpointHealth {
    Healthy,
    Busy,
    Disconnected,
    Recovering,
    Failed,
}

impl EndpointHealth {
    pub fn label(&self) -> &'static str {
        match self {
            Self::Healthy => "healthy",
            Self::Busy => "busy",
            Self::Disconnected => "disconnected",
            Self::Recovering => "recovering",
            Self::Failed => "failed",
        }
    }

    pub fn is_healthy(&self) -> bool {
        matches!(self, Self::Healthy)
    }
}

impl Default for EndpointHealth {
    fn default() -> Self {
        Self::Disconnected
    }
}

/// Epoch-based timestamp.
type EpochTime = u64;

/// An endpoint in the IPC runtime.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Endpoint {
    pub id: String,
    pub address: String,
    pub descriptor: EndpointDescriptor,
    pub health_status: EndpointHealth,
    pub version: String,
    pub registered_epoch: EpochTime,
    pub last_health_check_epoch: EpochTime,
}

impl Endpoint {
    pub fn new(
        id: impl Into<String>,
        address: impl Into<String>,
        descriptor: EndpointDescriptor,
    ) -> Self {
        let now = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
        Self {
            id: id.into(),
            address: address.into(),
            descriptor,
            health_status: EndpointHealth::Healthy,
            version: "1.0.0".to_string(),
            registered_epoch: now,
            last_health_check_epoch: now,
        }
    }

    pub fn update_health(&mut self, status: EndpointHealth) {
        self.health_status = status;
        self.last_health_check_epoch = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();
    }

    pub fn is_available(&self) -> bool {
        self.health_status.is_healthy()
    }

    pub fn version_compatible(&self, required_version: &str) -> bool {
        self.version
            .starts_with(required_version.split('.').next().unwrap_or(""))
    }
}
