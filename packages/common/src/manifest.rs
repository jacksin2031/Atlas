//! Manifest structures.
//!
//! See RFC-0010 (Runtime Manifest Specification) and RFC-1005 (Common
//! Manifest Model). The runtime manifest conforms to the schema in RFC-0010
//! §9 and is validated independently of any business logic.

use serde::{Deserialize, Serialize};

/// Capability declaration from a manifest (RFC-0010 §10).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Capability {
    pub name: String,
    pub enabled: bool,
    pub required: bool,
}

/// Package type (RFC-1005 §4).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PackageType {
    Runtime,
    Plugin,
    Workflow,
    Vision,
    Ai,
    Marketplace,
}

impl std::fmt::Display for PackageType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Runtime => write!(f, "runtime"),
            Self::Plugin => write!(f, "plugin"),
            Self::Workflow => write!(f, "workflow"),
            Self::Vision => write!(f, "vision"),
            Self::Ai => write!(f, "ai"),
            Self::Marketplace => write!(f, "marketplace"),
        }
    }
}

/// Permission declaration (RFC-1005 §2).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Permission {
    pub name: String,
    pub required: bool,
}

/// Resource limits declared in a manifest (RFC-0010 §9).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Default)]
pub struct ResourceLimits {
    #[serde(default)]
    pub max_memory_mb: Option<u64>,
    #[serde(default)]
    pub max_cpu_cores: Option<u32>,
    #[serde(default)]
    pub max_vram_mb: Option<u64>,
}

/// Backward/forward compatibility matrix (RFC-0010 §9).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Default)]
pub struct Compatibility {
    #[serde(default)]
    pub minimum_runtime_version: Option<String>,
    #[serde(default)]
    pub maximum_runtime_version: Option<String>,
}

/// Runtime manifest (RFC-0010 §9, RFC-1005 §2).
///
/// The manifest is parsed and validated independently of business logic.
/// Once the Runtime reaches the Running state the loaded manifest is
/// immutable (RFC-0010 §4).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Default)]
pub struct Manifest {
    pub schema_version: String,
    pub runtime_version: String,
    #[serde(default)]
    pub name: String,
    #[serde(default)]
    pub version: String,
    #[serde(default)]
    pub author: String,
    #[serde(default)]
    pub description: String,
    #[serde(default)]
    pub capabilities: Vec<Capability>,
    #[serde(default)]
    pub permissions: Vec<Permission>,
    #[serde(default)]
    pub dependencies: Vec<String>,
    #[serde(default)]
    pub services: Vec<ServiceDeclaration>,
    #[serde(default)]
    pub resource_limits: Option<ResourceLimits>,
    #[serde(default)]
    pub compatibility: Option<Compatibility>,
}

/// Service declaration from a manifest (RFC-0010 §9).
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ServiceDeclaration {
    pub id: String,
    pub name: String,
    pub version: String,
    pub dependencies: Vec<String>,
    pub required: bool,
    pub priority: u8,
}
