//! Service Registry — registration, lookup, dependency management.

use atlas_contracts::ServiceError;
use atlas_common::ServiceDeclaration;
use std::collections::HashMap;

#[allow(dead_code)]
pub struct ServiceEntry {
    pub id: String,
    pub name: String,
    pub dependencies: Vec<String>,
    pub priority: u8,
    pub required: bool,
}

/// Service Registry.
pub struct ServiceRegistry {
    services: HashMap<String, ServiceEntry>,
}

impl ServiceRegistry {
    pub fn new() -> Self {
        Self {
            services: HashMap::new(),
        }
    }

    pub fn register_declaration(&mut self, decl: ServiceDeclaration) -> Result<(), ServiceError> {
        if self.services.contains_key(&decl.id) {
            return Err(ServiceError::DuplicateRegistration(decl.id));
        }

        self.services.insert(
            decl.id.clone(),
            ServiceEntry {
                id: decl.id,
                name: decl.name,
                dependencies: decl.dependencies,
                priority: decl.priority,
                required: decl.required,
            },
        );

        Ok(())
    }

    pub fn initialize(&mut self, _service_id: &str) -> Result<(), ServiceError> {
        Ok(())
    }

    pub fn start(&mut self, _service_id: &str) -> Result<(), ServiceError> {
        Ok(())
    }

    pub fn deinitialize_all(&mut self) -> Result<Vec<String>, ServiceError> {
        let mut ids: Vec<String> = self.services.keys().cloned().collect();
        ids.reverse();
        Ok(ids)
    }

    pub fn deinitialize(&mut self, _service_id: &str) -> Result<(), ServiceError> {
        Ok(())
    }

    pub fn get(&self, id: &str) -> Result<&ServiceEntry, ServiceError> {
        self.services.get(id).ok_or_else(|| ServiceError::NotFound(id.to_string()))
    }

    pub fn service_ids(&self) -> Vec<&String> {
        self.services.keys().collect()
    }

    pub fn len(&self) -> usize {
        self.services.len()
    }

    pub fn is_empty(&self) -> bool {
        self.services.is_empty()
    }
}

impl Default for ServiceRegistry {
    fn default() -> Self {
        Self::new()
    }
}
