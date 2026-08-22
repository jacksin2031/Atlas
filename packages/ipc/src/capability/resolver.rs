//! Capability resolver — resolves required and optional capabilities.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Capability declaration.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capability {
    pub name: String,
    pub required: bool,
    pub version: String,
    pub description: String,
}

impl Capability {
    pub fn required(name: impl Into<String>, version: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            required: true,
            version: version.into(),
            description: String::new(),
        }
    }

    pub fn optional(name: impl Into<String>, version: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            required: false,
            version: version.into(),
            description: String::new(),
        }
    }

    pub fn with_description(mut self, desc: impl Into<String>) -> Self {
        self.description = desc.into();
        self
    }
}

/// Resolver for capabilities between endpoints.
#[derive(Clone, Default)]
pub struct CapabilityResolver {
    /// Declared capabilities.
    capabilities: HashMap<String, Capability>,
    /// Available capabilities from remote endpoints.
    available: HashMap<String, Capability>,
}

impl CapabilityResolver {
    /// Register a declared capability.
    pub fn register_capability(&mut self, capability: Capability) {
        self.capabilities
            .insert(capability.name.clone(), capability);
    }

    /// Register an available (remote) capability.
    pub fn register_available(&mut self, capability: Capability) {
        self.available.insert(capability.name.clone(), capability);
    }

    /// Resolve all required capabilities.
    pub fn resolve_required(&self) -> Vec<&Capability> {
        self.capabilities.values().filter(|c| c.required).collect()
    }

    /// Resolve all optional capabilities that are available.
    pub fn resolve_optional_available(&self) -> Vec<&Capability> {
        self.capabilities
            .values()
            .filter(|c| !c.required && self.available.contains_key(&c.name))
            .collect()
    }

    /// Check if all required capabilities are satisfied.
    pub fn all_required_satisfied(&self) -> bool {
        for cap in self.resolve_required() {
            if !self.available.contains_key(&cap.name) {
                return false;
            }
        }
        true
    }

    /// Get the list of missing required capabilities.
    pub fn missing_required(&self) -> Vec<String> {
        self.resolve_required()
            .iter()
            .filter(|c| !self.available.contains_key(&c.name))
            .map(|c| c.name.clone())
            .collect()
    }

    /// Get fallback capabilities for missing optional ones.
    pub fn get_fallbacks(&self) -> Vec<String> {
        self.capabilities
            .values()
            .filter(|c| !c.required && !self.available.contains_key(&c.name))
            .map(|c| c.name.clone())
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_resolve_required() {
        let mut resolver = CapabilityResolver::default();
        resolver.register_capability(Capability::required("auth", "1.0"));
        resolver.register_capability(Capability::optional("logging", "1.0"));
        resolver.register_available(Capability::required("auth", "1.0"));
        assert!(resolver.all_required_satisfied());
        assert_eq!(resolver.resolve_required().len(), 1);
        assert_eq!(resolver.resolve_optional_available().len(), 0);
    }

    #[test]
    fn test_missing_required() {
        let mut resolver = CapabilityResolver::default();
        resolver.register_capability(Capability::required("auth", "1.0"));
        assert!(!resolver.all_required_satisfied());
        assert_eq!(resolver.missing_required(), vec!["auth"]);
    }
}
