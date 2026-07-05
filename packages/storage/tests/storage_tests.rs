//! Integration tests for the Atlas Storage Foundation.
//!
//! Exercises the abstract [`ProviderRegistryImpl`], [`ProviderLifecycleManager`],
//! and [`ResourceManager`] using an in-memory mock provider. No real database
//! backend is used — these tests validate the platform-side registry and
//! lifecycle logic only.

use atlas_common::{
    DeleteOptions, HealthStatus, IsolationLevel, Pagination, ProviderCapability, ProviderId,
    ProviderRegistry, ProviderState, QueryFilter, ReadOptions, Resource, ResourceMetadata,
    ResourceState, ResultSet, StorageError, StorageProvider, WriteOptions,
};
use atlas_storage::{ProviderLifecycleManager, ProviderRegistryImpl, ResourceManager};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};

struct MockProvider {
    id: ProviderId,
    caps: Vec<ProviderCapability>,
    healthy: AtomicBool,
    store: Mutex<std::collections::HashMap<String, Vec<u8>>>,
}

impl MockProvider {
    fn new(id: &str, caps: Vec<ProviderCapability>) -> Self {
        Self {
            id: id.to_string(),
            caps,
            healthy: AtomicBool::new(true),
            store: Mutex::new(std::collections::HashMap::new()),
        }
    }
}

impl StorageProvider for MockProvider {
    fn id(&self) -> &ProviderId {
        &self.id
    }
    fn capabilities(&self) -> &[ProviderCapability] {
        &self.caps
    }
    fn read(&self, id: &String, _o: &ReadOptions) -> Result<Resource, StorageError> {
        self.store
            .lock()
            .unwrap()
            .get(id)
            .map(|data| Resource {
                metadata: ResourceMetadata {
                    id: id.clone(),
                    version: 1,
                    ..Default::default()
                },
                data: data.clone(),
            })
            .ok_or(StorageError::NotFound(id.clone()))
    }
    fn write(&self, id: &String, data: &[u8], _o: &WriteOptions) -> Result<u64, StorageError> {
        self.store.lock().unwrap().insert(id.clone(), data.to_vec());
        Ok(1)
    }
    fn delete(&self, id: &String, _o: &DeleteOptions) -> Result<u64, StorageError> {
        self.store.lock().unwrap().remove(id);
        Ok(1)
    }
    fn query(&self, _f: &QueryFilter, _p: &Pagination) -> Result<ResultSet, StorageError> {
        Ok(ResultSet::default())
    }
    fn exists(&self, id: &String) -> Result<bool, StorageError> {
        Ok(self.store.lock().unwrap().contains_key(id))
    }
    fn begin_transaction(&self, _i: IsolationLevel) -> Result<String, StorageError> {
        Ok("tx1".to_string())
    }
    fn commit_transaction(&self, _tx: &String) -> Result<u64, StorageError> {
        Ok(1)
    }
    fn rollback_transaction(&self, _tx: &String) -> Result<(), StorageError> {
        Ok(())
    }
    fn prepare_transaction(&self, _tx: &String) -> Result<bool, StorageError> {
        Ok(true)
    }
    fn abort_transaction(&self, _tx: &String) -> Result<(), StorageError> {
        Ok(())
    }
    fn health_check(&self) -> HealthStatus {
        if self.healthy.load(Ordering::Acquire) {
            HealthStatus::Healthy
        } else {
            HealthStatus::Unhealthy("mock unhealthy".to_string())
        }
    }
    fn get_metrics(&self) -> serde_json::Value {
        serde_json::json!({})
    }
    fn get_status(&self) -> serde_json::Value {
        serde_json::json!({"id": self.id})
    }
    fn initialize(&self, _c: &serde_json::Value) -> Result<(), StorageError> {
        Ok(())
    }
    fn shutdown(&self) -> Result<(), StorageError> {
        Ok(())
    }
    fn migrate(&self, _from: u32, _to: u32) -> Result<(), StorageError> {
        Ok(())
    }
}

fn base_caps() -> Vec<ProviderCapability> {
    vec![
        ProviderCapability::Read,
        ProviderCapability::Write,
        ProviderCapability::Delete,
    ]
}

#[test]
fn test_register_rejects_missing_required_capability() {
    let registry = ProviderRegistryImpl::new();
    let provider = Arc::new(MockProvider::new(
        "p1",
        vec![ProviderCapability::Read, ProviderCapability::Write],
    ));
    assert!(matches!(
        registry.register(provider).unwrap_err(),
        StorageError::CapabilityNotSupported(_)
    ));
}

#[test]
fn test_register_activate_deactivate() {
    let registry = ProviderRegistryImpl::new();
    registry
        .register(Arc::new(MockProvider::new("p1", base_caps())))
        .unwrap();
    assert_eq!(
        registry.state(&"p1".to_string()).unwrap(),
        ProviderState::Registered
    );
    registry.activate(&"p1".to_string()).unwrap();
    assert_eq!(
        registry.state(&"p1".to_string()).unwrap(),
        ProviderState::Running
    );
    registry.deactivate(&"p1".to_string()).unwrap();
    assert_eq!(
        registry.state(&"p1".to_string()).unwrap(),
        ProviderState::Registered
    );
}

#[test]
fn test_duplicate_register_rejected() {
    let registry = ProviderRegistryImpl::new();
    registry
        .register(Arc::new(MockProvider::new("p1", base_caps())))
        .unwrap();
    assert!(matches!(
        registry
            .register(Arc::new(MockProvider::new("p1", base_caps())))
            .unwrap_err(),
        StorageError::AlreadyRegistered(_)
    ));
}

#[test]
fn test_select_by_capability() {
    let registry = ProviderRegistryImpl::new();
    registry
        .register(Arc::new(MockProvider::new("p1", base_caps())))
        .unwrap();
    let p2: Arc<dyn StorageProvider> = Arc::new(MockProvider::new(
        "p2",
        vec![
            ProviderCapability::Read,
            ProviderCapability::Write,
            ProviderCapability::Delete,
            ProviderCapability::Query,
        ],
    ));
    registry.register(Arc::clone(&p2)).unwrap();
    registry.activate(&"p1".to_string()).unwrap();
    registry.activate(&"p2".to_string()).unwrap();
    let selected = registry.select(&[ProviderCapability::Query]).unwrap();
    assert_eq!(selected.id(), "p2");
}

#[test]
fn test_select_none_running_returns_unavailable() {
    let registry = ProviderRegistryImpl::new();
    registry
        .register(Arc::new(MockProvider::new("p1", base_caps())))
        .unwrap();
    let res = registry.select(&[ProviderCapability::Read]);
    assert!(res.is_err());
    assert!(matches!(res, Err(StorageError::ProviderUnavailable(_))));
}

#[test]
fn test_health_check_aggregate() {
    let registry = ProviderRegistryImpl::new();
    let p1 = Arc::new(MockProvider::new("p1", base_caps()));
    let p1_dyn: Arc<dyn StorageProvider> = p1.clone();
    registry.register(p1_dyn).unwrap();
    registry.activate(&"p1".to_string()).unwrap();
    assert_eq!(registry.health_check(), HealthStatus::Healthy);
    p1.healthy.store(false, Ordering::Release);
    assert!(matches!(registry.health_check(), HealthStatus::Unhealthy(_)));
}

#[test]
fn test_get_and_list() {
    let registry = ProviderRegistryImpl::new();
    registry
        .register(Arc::new(MockProvider::new("p1", base_caps())))
        .unwrap();
    registry
        .register(Arc::new(MockProvider::new("p2", base_caps())))
        .unwrap();
    assert_eq!(registry.list().len(), 2);
    assert!(registry.get(&"p1".to_string()).is_ok());
    let res = registry.get(&"nope".to_string());
    assert!(res.is_err());
    assert!(matches!(res, Err(StorageError::ProviderNotFound(_))));
}

#[test]
fn test_resource_lifecycle_legal_path() {
    let rm = ResourceManager::new();
    let id = "res-1".to_string();
    rm.create(&id).unwrap();
    rm.transition(&id, ResourceState::Validating).unwrap();
    rm.transition(&id, ResourceState::Stored).unwrap();
    rm.transition(&id, ResourceState::Active).unwrap();
    rm.transition(&id, ResourceState::Deleting).unwrap();
    rm.transition(&id, ResourceState::Purged).unwrap();
    rm.purge(&id).unwrap();
    assert!(rm.is_empty());
}

#[test]
fn test_resource_illegal_transition_rejected() {
    let rm = ResourceManager::new();
    let id = "res-1".to_string();
    rm.create(&id).unwrap();
    assert!(matches!(
        rm.transition(&id, ResourceState::Active).unwrap_err(),
        StorageError::IllegalResourceTransition { .. }
    ));
}

#[test]
fn test_provider_lifecycle_illegal_transition_rejected() {
    let lm = ProviderLifecycleManager::new();
    let id = "p1".to_string();
    lm.discover(&id).unwrap();
    assert!(matches!(
        lm.transition(&id, ProviderState::Running).unwrap_err(),
        StorageError::IllegalProviderTransition { .. }
    ));
}
