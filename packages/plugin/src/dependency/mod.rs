//! Plugin dependency resolution (RFC-0226).
//!
//! Builds a dependency graph from a set of plugin manifests, validates required
//! / optional / soft dependencies, enforces version constraints and capability
//! dependencies, detects circular dependencies, and produces a deterministic
//! topological load order.
//!
//! The resolver operates purely on manifest data — it does NOT instantiate
//! plugins (RFC-0226 §6). Resolution is deterministic: identical inputs always
//! yield identical outputs.

use crate::error::DependencyError;
use crate::manifest::{DependencyType, PluginDependency, PluginManifest};
use crate::version::VersionConstraint;
use std::collections::{HashMap, HashSet};

/// Plugin identifier alias shared across the plugin subsystem.
pub type PluginId = String;

/// The result of dependency resolution.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ResolutionResult {
    /// Plugins in dependency-first (topological) load order.
    pub load_order: Vec<PluginId>,
    /// Non-fatal warnings (e.g. missing optional/soft dependencies).
    pub warnings: Vec<String>,
}

/// Dependency resolver implementing the RFC-0226 solver algorithm.
pub struct DependencyResolver;

impl DependencyResolver {
    pub fn new() -> Self {
        Self
    }

    /// Resolve dependencies for a set of manifests.
    ///
    /// Manifests MUST have unique `plugin_id`s. Required dependencies that are
    /// missing or version-incompatible cause a hard error. Optional and soft
    /// dependencies that are missing produce warnings and are skipped.
    /// Capability dependencies require the dependency to declare the capability.
    /// Circular dependencies are detected and rejected.
    pub fn resolve(&self, manifests: &[PluginManifest]) -> Result<ResolutionResult, DependencyError> {
        if manifests.is_empty() {
            return Ok(ResolutionResult { load_order: Vec::new(), warnings: Vec::new() });
        }

        let mut seen = HashSet::new();
        for m in manifests {
            if !seen.insert(m.plugin_id.as_str()) {
                return Err(DependencyError::CircularDependency(format!(
                    "duplicate plugin id '{}' in resolver input",
                    m.plugin_id
                )));
            }
        }

        let by_id: HashMap<&str, &PluginManifest> =
            manifests.iter().map(|m| (m.plugin_id.as_str(), m)).collect();

        let mut warnings = Vec::new();
        let mut adj: HashMap<String, Vec<String>> = HashMap::new();
        let mut in_degree: HashMap<String, usize> = HashMap::new();
        for m in manifests {
            adj.entry(m.plugin_id.clone()).or_default();
            in_degree.entry(m.plugin_id.clone()).or_insert(0);
        }

        for m in manifests {
            for dep in &m.dependencies {
                self.process_dependency(m, dep, &by_id, &mut adj, &mut in_degree, &mut warnings)?;
            }
        }

        let order = self.topological_sort(&adj, &mut in_degree)?;
        if order.len() != manifests.len() {
            let remaining: Vec<String> = in_degree
                .iter()
                .filter(|(_, d)| **d > 0)
                .map(|(k, _)| k.clone())
                .collect();
            return Err(DependencyError::CircularDependency(format!(
                "cycle detected among: {}",
                remaining.join(" -> ")
            )));
        }

        Ok(ResolutionResult { load_order: order, warnings })
    }
}

impl DependencyResolver {
    fn process_dependency(
        &self,
        owner: &PluginManifest,
        dep: &PluginDependency,
        by_id: &HashMap<&str, &PluginManifest>,
        adj: &mut HashMap<String, Vec<String>>,
        in_degree: &mut HashMap<String, usize>,
        warnings: &mut Vec<String>,
    ) -> Result<(), DependencyError> {
        let Some(dep_manifest) = by_id.get(dep.plugin_id.as_str()) else {
            match dep.dependency_type {
                DependencyType::Required => {
                    return Err(DependencyError::MissingDependency(format!(
                        "{} requires {}",
                        owner.plugin_id, dep.plugin_id
                    )))
                }
                DependencyType::Optional | DependencyType::Soft => {
                    warnings.push(format!(
                        "{} {} dependency {} is not present",
                        owner.plugin_id,
                        dependency_type_name(dep.dependency_type),
                        dep.plugin_id
                    ));
                    return Ok(());
                }
            }
        };

        let constraint = VersionConstraint::parse(&dep.version)?;
        let dep_version = dep_manifest.semantic_version();
        if !constraint.satisfies(&dep_version) {
            match dep.dependency_type {
                DependencyType::Required => {
                    return Err(DependencyError::VersionConflict {
                        plugin: dep.plugin_id.clone(),
                        constraint: dep.version.clone(),
                        version: dep_version.to_string(),
                    })
                }
                DependencyType::Optional | DependencyType::Soft => {
                    warnings.push(format!(
                        "{} {} dependency {} version {} does not satisfy {}",
                        owner.plugin_id,
                        dependency_type_name(dep.dependency_type),
                        dep.plugin_id,
                        dep_version,
                        dep.version
                    ));
                    return Ok(());
                }
            }
        }

        if let Some(cap) = &dep.capability {
            if !dep_manifest.provided_capabilities().contains(cap) {
                match dep.dependency_type {
                    DependencyType::Required => {
                        return Err(DependencyError::CapabilityNotSatisfied(
                            owner.plugin_id.clone(),
                            cap.to_string(),
                        ))
                    }
                    DependencyType::Optional | DependencyType::Soft => {
                        warnings.push(format!(
                            "{} {} dependency {} does not provide capability {}",
                            owner.plugin_id,
                            dependency_type_name(dep.dependency_type),
                            dep.plugin_id,
                            cap
                        ));
                        return Ok(());
                    }
                }
            }
        }

        adj.entry(dep.plugin_id.clone()).or_default().push(owner.plugin_id.clone());
        *in_degree.entry(owner.plugin_id.clone()).or_insert(0) += 1;
        Ok(())
    }

    /// Kahn's algorithm with lexicographic selection for determinism.
    fn topological_sort(
        &self,
        adj: &HashMap<String, Vec<String>>,
        in_degree: &mut HashMap<String, usize>,
    ) -> Result<Vec<String>, DependencyError> {
        let mut queue: Vec<String> = in_degree
            .iter()
            .filter(|(_, d)| **d == 0)
            .map(|(k, _)| k.clone())
            .collect();
        queue.sort();

        let mut order = Vec::new();
        while let Some(node) = queue.first().cloned() {
            queue.remove(0);
            order.push(node.clone());
            if let Some(dependents) = adj.get(&node) {
                for dependent in dependents {
                    if let Some(deg) = in_degree.get_mut(dependent) {
                        *deg -= 1;
                        if *deg == 0 {
                            insert_sorted(&mut queue, dependent.clone());
                        }
                    }
                }
            }
        }
        Ok(order)
    }
}

fn dependency_type_name(t: DependencyType) -> &'static str {
    match t {
        DependencyType::Required => "required",
        DependencyType::Optional => "optional",
        DependencyType::Soft => "soft",
    }
}

fn insert_sorted(vec: &mut Vec<String>, value: String) {
    let pos = vec.binary_search(&value).unwrap_or_else(|p| p);
    vec.insert(pos, value);
}

impl Default for DependencyResolver {
    fn default() -> Self {
        Self::new()
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::capability::{CapabilityDeclaration, PluginCapability};
    use crate::manifest::{
        DependencyType, PluginCompatibility, PluginDependency, PluginManifest, PluginResourceLimits,
        PluginType,
    };

    fn manifest(id: &str, version: &str, deps: Vec<PluginDependency>, caps: Vec<CapabilityDeclaration>) -> PluginManifest {
        PluginManifest {
            manifest_version: "1.0.0".to_string(),
            plugin_id: id.to_string(),
            plugin_name: id.to_string(),
            version: version.to_string(),
            description: String::new(),
            author: String::new(),
            license: "MIT".to_string(),
            plugin_type: PluginType::Extension,
            entry_point: "main".to_string(),
            capabilities: caps,
            dependencies: deps,
            permissions: Vec::new(),
            compatibility: PluginCompatibility::default(),
            resource_limits: PluginResourceLimits::default(),
        }
    }

    fn dep(id: &str, version: &str, t: DependencyType) -> PluginDependency {
        PluginDependency { plugin_id: id.to_string(), version: version.to_string(), dependency_type: t, capability: None }
    }

    #[test]
    fn test_linear_order() {
        let a = manifest("a", "1.0.0", vec![], vec![]);
        let b = manifest("b", "1.0.0", vec![dep("a", "*", DependencyType::Required)], vec![]);
        let r = DependencyResolver::new().resolve(&[a, b]).unwrap();
        assert_eq!(r.load_order, vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn test_deterministic_order() {
        let a = manifest("a", "1.0.0", vec![], vec![]);
        let b = manifest("b", "1.0.0", vec![], vec![]);
        let c = manifest("c", "1.0.0", vec![dep("a", "*", DependencyType::Required), dep("b", "*", DependencyType::Required)], vec![]);
        let r = DependencyResolver::new().resolve(&[c.clone(), b.clone(), a.clone()]).unwrap();
        assert_eq!(r.load_order, vec!["a".to_string(), "b".to_string(), "c".to_string()]);
    }

    #[test]
    fn test_cycle_detected() {
        let a = manifest("a", "1.0.0", vec![dep("b", "*", DependencyType::Required)], vec![]);
        let b = manifest("b", "1.0.0", vec![dep("a", "*", DependencyType::Required)], vec![]);
        let err = DependencyResolver::new().resolve(&[a, b]).unwrap_err();
        assert!(matches!(err, DependencyError::CircularDependency(_)));
    }

    #[test]
    fn test_missing_required() {
        let a = manifest("a", "1.0.0", vec![dep("missing", "*", DependencyType::Required)], vec![]);
        let err = DependencyResolver::new().resolve(&[a]).unwrap_err();
        assert!(matches!(err, DependencyError::MissingDependency(_)));
    }

    #[test]
    fn test_optional_missing_produces_warning() {
        let a = manifest("a", "1.0.0", vec![dep("missing", "*", DependencyType::Optional)], vec![]);
        let r = DependencyResolver::new().resolve(&[a]).unwrap();
        assert_eq!(r.load_order, vec!["a".to_string()]);
        assert!(!r.warnings.is_empty());
    }

    #[test]
    fn test_version_conflict_required() {
        let a = manifest("a", "1.0.0", vec![], vec![]);
        let b = manifest("b", "1.0.0", vec![dep("a", ">=2.0.0", DependencyType::Required)], vec![]);
        let err = DependencyResolver::new().resolve(&[a, b]).unwrap_err();
        assert!(matches!(err, DependencyError::VersionConflict { .. }));
    }

    #[test]
    fn test_version_satisfied() {
        let a = manifest("a", "1.5.0", vec![], vec![]);
        let b = manifest("b", "1.0.0", vec![dep("a", "^1.2.0", DependencyType::Required)], vec![]);
        let r = DependencyResolver::new().resolve(&[a, b]).unwrap();
        assert_eq!(r.load_order, vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn test_capability_dependency_satisfied() {
        let a = manifest("a", "1.0.0", vec![], vec![CapabilityDeclaration::new(PluginCapability::OCR)]);
        let mut d = dep("a", "*", DependencyType::Required);
        d.capability = Some(PluginCapability::OCR);
        let b = manifest("b", "1.0.0", vec![d], vec![]);
        let r = DependencyResolver::new().resolve(&[a, b]).unwrap();
        assert_eq!(r.load_order, vec!["a".to_string(), "b".to_string()]);
    }

    #[test]
    fn test_capability_dependency_unsatisfied() {
        let a = manifest("a", "1.0.0", vec![], vec![CapabilityDeclaration::new(PluginCapability::Vision)]);
        let mut d = dep("a", "*", DependencyType::Required);
        d.capability = Some(PluginCapability::OCR);
        let b = manifest("b", "1.0.0", vec![d], vec![]);
        let err = DependencyResolver::new().resolve(&[a, b]).unwrap_err();
        assert!(matches!(err, DependencyError::CapabilityNotSatisfied(_, _)));
    }

    #[test]
    fn test_empty_manifests() {
        let r = DependencyResolver::new().resolve(&[]).unwrap();
        assert!(r.load_order.is_empty());
    }

    #[test]
    fn test_duplicate_ids_rejected() {
        let a = manifest("a", "1.0.0", vec![], vec![]);
        let a2 = manifest("a", "2.0.0", vec![], vec![]);
        let err = DependencyResolver::new().resolve(&[a, a2]).unwrap_err();
        assert!(matches!(err, DependencyError::CircularDependency(_)));
    }
}


