//! Manifest structures.
//!
//! See RFC-0010 (Runtime Manifest Specification).

use serde::{Deserialize, Serialize};

/// Capability declaration from a manifest.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capability {
    pub name: String,
    pub enabled: bool,
    pub required: bool,
}

/// Runtime manifest.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Manifest {
    pub schema_version: String,
    pub runtime_version: String,
    pub capabilities: Vec<Capability>,
    pub services: Vec<ServiceDeclaration>,
}

/// Service declaration from a manifest.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServiceDeclaration {
    pub id: String,
    pub name: String,
    pub version: String,
    pub dependencies: Vec<String>,
    pub required: bool,
    pub priority: u8,
}
