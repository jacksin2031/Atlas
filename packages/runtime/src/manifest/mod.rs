//! Manifest loader.

use atlas_common::{AtlasError, manifest::ServiceDeclaration};
use crate::config::ConfigLoader;
use crate::registry::ServiceRegistry;

#[allow(dead_code)]
/// Manifest loader.
pub struct ManifestLoader {
    schema_version: String,
    runtime_version: String,
    capabilities: Vec<atlas_common::manifest::Capability>,
    services: Vec<ServiceDeclaration>,
}

impl ManifestLoader {
    pub fn load_from_config(_config: &ConfigLoader) -> Result<Self, AtlasError> {
        Ok(Self {
            schema_version: "1.0.0".to_string(),
            runtime_version: "1.0.0".to_string(),
            capabilities: Vec::new(),
            services: Vec::new(),
        })
    }

    pub fn discover_services(
        &self,
        _registry: &ServiceRegistry,
    ) -> Vec<ServiceDeclaration> {
        Vec::new()
    }
}
