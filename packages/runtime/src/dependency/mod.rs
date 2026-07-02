//! Dependency resolver — topological sort with cycle detection.

use atlas_common::DependencyError;
use std::collections::{HashMap, VecDeque};

pub struct DependencyResolver;

impl DependencyResolver {
    pub fn new() -> Self {
        Self
    }

    pub fn resolve(
        &self,
        registry: &crate::registry::ServiceRegistry,
    ) -> Result<Vec<String>, DependencyError> {
        let all_ids: Vec<String> = registry.service_ids().into_iter().cloned().collect();
        let mut adj: HashMap<String, Vec<String>> = HashMap::new();
        let mut in_degree: HashMap<String, usize> = HashMap::new();

        for id in &all_ids {
            adj.entry(id.clone()).or_default();
            in_degree.entry(id.clone()).or_insert(0);
        }

        for id in &all_ids {
            if let Ok(entry) = registry.get(id) {
                for dep in &entry.dependencies {
                    if let Some(deps) = adj.get_mut(dep) {
                        deps.push(id.clone());
                    }
                    if let Some(deg) = in_degree.get_mut(id) {
                        *deg += 1;
                    }
                }
            }
        }

        let mut queue: VecDeque<String> = VecDeque::new();
        for id in &all_ids {
            if in_degree.get(id).copied().unwrap_or(0) == 0 {
                queue.push_back(id.clone());
            }
        }

        let mut result = Vec::with_capacity(all_ids.len());
        while let Some(node) = queue.pop_front() {
            result.push(node.clone());
            if let Some(dependents) = adj.get(&node) {
                for dependent in dependents {
                    if let Some(deg) = in_degree.get_mut(dependent) {
                        *deg -= 1;
                        if *deg == 0 {
                            queue.push_back(dependent.clone());
                        }
                    }
                }
            }
        }

        if result.len() != all_ids.len() {
            return Err(DependencyError::CircularDependency(
                "cycle detected during dependency resolution".to_string(),
            ));
        }

        Ok(result)
    }
}

impl Default for DependencyResolver {
    fn default() -> Self {
        Self::new()
    }
}
