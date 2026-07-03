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
///
/// Tracks services in registration order so that shutdown can proceed in
/// reverse registration order (RFC-0003 §10.1 / RFC-0002 §32: services are
/// deinitialised in the reverse of their initialization order).
pub struct ServiceRegistry {
    services: HashMap<String, ServiceEntry>,
    /// Insertion order of service IDs (registration order).
    order: Vec<String>,
}

impl ServiceRegistry {
    pub fn new() -> Self {
        Self {
            services: HashMap::new(),
            order: Vec::new(),
        }
    }

    pub fn register_declaration(&mut self, decl: ServiceDeclaration) -> Result<(), ServiceError> {
        if self.services.contains_key(&decl.id) {
            return Err(ServiceError::DuplicateRegistration(decl.id));
        }

        self.order.push(decl.id.clone());
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

    /// Return service IDs in reverse registration order for shutdown.
    pub fn deinitialize_all(&mut self) -> Result<Vec<String>, ServiceError> {
        let mut ids = self.order.clone();
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
