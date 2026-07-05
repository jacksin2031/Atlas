//! Atlas Storage Foundation.
//!
//! Implements the abstract storage provider registry and lifecycle state
//! machines per RFC-0401 (Storage Overview), RFC-0403 (Storage Provider), and
//! RFC-0404 (Storage Lifecycle).
//!
//! This crate exposes **abstract providers and registries only**. It MUST NOT
//! contain any database-specific logic. Concrete backends implement the
//! [`StorageProvider`] trait from `atlas-contracts`; this crate provides the
//! platform-side [`ProviderRegistryImpl`], [`ProviderLifecycleManager`], and
//! [`ResourceManager`].
//!
//! No global mutable state is used; all state is held behind `Mutex`es inside
//! owned registry/manager instances that are shared via dependency injection.

use atlas_common::{
    is_legal_provider_transition, is_legal_resource_transition, HealthStatus, ProviderCapability,
    ProviderId, ProviderState, ResourceId, ResourceState, StorageError, StorageProvider,
};
use atlas_contracts::ProviderRegistry;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

/// Manages the resource lifecycle state machine (RFC-0404 §8).
///
/// Tracks the state of every resource and enforces that only legal
/// transitions (per [`is_legal_resource_transition`]) are applied. Each
/// transition is atomic: either the full transition succeeds or the resource
/// remains in its previous state (RFC-0404 §4).
pub struct ResourceManager {
    states: Mutex<HashMap<ResourceId, ResourceState>>,
}

impl ResourceManager {
    /// Create a new, empty resource manager.
    pub fn new() -> Self {
        Self {
            states: Mutex::new(HashMap::new()),
        }
    }

    /// Register a resource in the [`ResourceState::Created`] state.
    pub fn create(&self, id: &ResourceId) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("resource states mutex poisoned");
        if states.contains_key(id) {
            return Err(StorageError::Conflict(format!(
                "resource already exists: {id}"
            )));
        }
        states.insert(id.clone(), ResourceState::Created);
        Ok(())
    }

    /// Transition a resource to `target`, enforcing legal transitions.
    pub fn transition(&self, id: &ResourceId, target: ResourceState) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("resource states mutex poisoned");
        let current = states
            .get(id)
            .copied()
            .ok_or(StorageError::NotFound(id.clone()))?;
        if !is_legal_resource_transition(current, target) {
            return Err(StorageError::IllegalResourceTransition {
                from: current,
                to: target,
            });
        }
        states.insert(id.clone(), target);
        Ok(())
    }

    /// Return the current state of a resource.
    pub fn state(&self, id: &ResourceId) -> Result<ResourceState, StorageError> {
        self.states
            .lock()
            .expect("resource states mutex poisoned")
            .get(id)
            .copied()
            .ok_or(StorageError::NotFound(id.clone()))
    }

    /// Remove a resource from tracking (after it reaches a terminal state).
    pub fn purge(&self, id: &ResourceId) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("resource states mutex poisoned");
        match states.get(id).copied() {
            Some(ResourceState::Purged) | Some(ResourceState::Failed) => {
                states.remove(id);
                Ok(())
            }
            Some(other) => Err(StorageError::IllegalResourceTransition {
                from: other,
                to: ResourceState::Purged,
            }),
            None => Err(StorageError::NotFound(id.clone())),
        }
    }

    /// Number of tracked resources.
    pub fn len(&self) -> usize {
        self.states
            .lock()
            .expect("resource states mutex poisoned")
            .len()
    }

    /// Whether no resources are tracked.
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

impl Default for ResourceManager {
    fn default() -> Self {
        Self::new()
    }
}

/// Manages the provider lifecycle state machine (RFC-0403 §5).
///
/// Enforces that only legal provider transitions (per
/// [`is_legal_provider_transition`]) are applied. This is the lifecycle
/// enforcement layer used by [`ProviderRegistryImpl`].
pub struct ProviderLifecycleManager {
    states: Mutex<HashMap<ProviderId, ProviderState>>,
}

impl ProviderLifecycleManager {
    /// Create a new, empty provider lifecycle manager.
    pub fn new() -> Self {
        Self {
            states: Mutex::new(HashMap::new()),
        }
    }

    /// Record a provider in the [`ProviderState::Discovered`] state.
    pub fn discover(&self, id: &ProviderId) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("provider states mutex poisoned");
        if states.contains_key(id) {
            return Err(StorageError::AlreadyRegistered(id.clone()));
        }
        states.insert(id.clone(), ProviderState::Discovered);
        Ok(())
    }

    /// Transition a provider to `target`, enforcing legal transitions.
    pub fn transition(&self, id: &ProviderId, target: ProviderState) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("provider states mutex poisoned");
        let current = states
            .get(id)
            .copied()
            .ok_or(StorageError::ProviderNotFound(id.clone()))?;
        if !is_legal_provider_transition(current, target) {
            return Err(StorageError::IllegalProviderTransition {
                from: current,
                to: target,
            });
        }
        states.insert(id.clone(), target);
        Ok(())
    }

    /// Return the current state of a provider.
    pub fn state(&self, id: &ProviderId) -> Result<ProviderState, StorageError> {
        self.states
            .lock()
            .expect("provider states mutex poisoned")
            .get(id)
            .copied()
            .ok_or(StorageError::ProviderNotFound(id.clone()))
    }

    /// Remove a provider from tracking (after it reaches `Terminated`).
    pub fn terminate(&self, id: &ProviderId) -> Result<(), StorageError> {
        let mut states = self.states.lock().expect("provider states mutex poisoned");
        match states.get(id).copied() {
            Some(ProviderState::Terminated) => {
                states.remove(id);
                Ok(())
            }
            Some(other) => Err(StorageError::IllegalProviderTransition {
                from: other,
                to: ProviderState::Terminated,
            }),
            None => Err(StorageError::ProviderNotFound(id.clone())),
        }
    }
}

impl Default for ProviderLifecycleManager {
    fn default() -> Self {
        Self::new()
    }
}

/// A registered provider entry: the provider instance plus lifecycle state.
struct ProviderEntry {
    provider: Arc<dyn StorageProvider>,
    state: ProviderState,
    capabilities: Vec<ProviderCapability>,
}

/// Concrete [`ProviderRegistry`] implementation.
///
/// Discovers, registers, and manages storage providers; enforces the provider
/// lifecycle state machine (RFC-0403 §5); and performs capability-based
/// provider selection (RFC-0403 §6.2 / §7). Contains no database-specific
/// logic — all backend behaviour is delegated to the registered
/// [`StorageProvider`] implementations.
pub struct ProviderRegistryImpl {
    providers: Mutex<HashMap<ProviderId, ProviderEntry>>,
}

impl ProviderRegistryImpl {
    /// Create a new, empty provider registry.
    pub fn new() -> Self {
        Self {
            providers: Mutex::new(HashMap::new()),
        }
    }

    /// Transition a provider's state, enforcing legal transitions.
    fn transition_state(
        entry: &mut ProviderEntry,
        target: ProviderState,
    ) -> Result<(), StorageError> {
        if !is_legal_provider_transition(entry.state, target) {
            return Err(StorageError::IllegalProviderTransition {
                from: entry.state,
                to: target,
            });
        }
        entry.state = target;
        Ok(())
    }

    /// Whether a provider declares all `required` capabilities.
    fn has_capabilities(entry: &ProviderEntry, required: &[ProviderCapability]) -> bool {
        required.iter().all(|r| entry.capabilities.contains(r))
    }
}

impl Default for ProviderRegistryImpl {
    fn default() -> Self {
        Self::new()
    }
}

impl ProviderRegistry for ProviderRegistryImpl {
    fn register(&self, provider: Arc<dyn StorageProvider>) -> Result<(), StorageError> {
        let id = provider.id().clone();
        let declared = provider.capabilities().to_vec();

        // RFC-0403 §6.1: every provider MUST declare read/write/delete.
        for required in ProviderCapability::REQUIRED_FOR_ALL {
            if !declared.contains(required) {
                return Err(StorageError::CapabilityNotSupported(format!(
                    "provider {id} missing required capability: {}",
                    required.as_str()
                )));
            }
        }

        let mut providers = self.providers.lock().expect("providers mutex poisoned");
        if providers.contains_key(&id) {
            return Err(StorageError::AlreadyRegistered(id));
        }
        providers.insert(
            id,
            ProviderEntry {
                provider,
                // Registered providers have passed validation (RFC-0403 §5.3).
                state: ProviderState::Registered,
                capabilities: declared,
            },
        );
        Ok(())
    }

    fn activate(&self, provider_id: &ProviderId) -> Result<(), StorageError> {
        let mut providers = self.providers.lock().expect("providers mutex poisoned");
        let entry = providers
            .get_mut(provider_id)
            .ok_or(StorageError::ProviderNotFound(provider_id.clone()))?;

        // Registered → Activating → Active → Running (RFC-0403 §5.3).
        Self::transition_state(entry, ProviderState::Activating)?;
        let init_result = entry.provider.initialize(&serde_json::Value::Null);
        if init_result.is_err() {
            Self::transition_state(entry, ProviderState::Failed)?;
            return Err(init_result.unwrap_err());
        }
        Self::transition_state(entry, ProviderState::Active)?;
        Self::transition_state(entry, ProviderState::Running)?;
        Ok(())
    }

    fn deactivate(&self, provider_id: &ProviderId) -> Result<(), StorageError> {
        let mut providers = self.providers.lock().expect("providers mutex poisoned");
        let entry = providers
            .get_mut(provider_id)
            .ok_or(StorageError::ProviderNotFound(provider_id.clone()))?;
        // Running → Deactivating → Registered (RFC-0403 §5.3).
        Self::transition_state(entry, ProviderState::Deactivating)?;
        let shutdown_result = entry.provider.shutdown();
        if shutdown_result.is_err() {
            Self::transition_state(entry, ProviderState::Failed)?;
            return Err(shutdown_result.unwrap_err());
        }
        Self::transition_state(entry, ProviderState::Registered)?;
        Ok(())
    }

    fn get(&self, provider_id: &ProviderId) -> Result<Arc<dyn StorageProvider>, StorageError> {
        let providers = self.providers.lock().expect("providers mutex poisoned");
        providers
            .get(provider_id)
            .map(|e| Arc::clone(&e.provider))
            .ok_or(StorageError::ProviderNotFound(provider_id.clone()))
    }

    fn select(
        &self,
        required: &[ProviderCapability],
    ) -> Result<Arc<dyn StorageProvider>, StorageError> {
        let providers = self.providers.lock().expect("providers mutex poisoned");
        for entry in providers.values() {
            if entry.state != ProviderState::Running {
                continue;
            }
            if !Self::has_capabilities(entry, required) {
                continue;
            }
            if !entry.provider.health_check().is_healthy() {
                continue;
            }
            return Ok(Arc::clone(&entry.provider));
        }
        Err(StorageError::ProviderUnavailable(format!(
            "no running provider with capabilities: {:?}",
            required.iter().map(|c| c.as_str()).collect::<Vec<_>>()
        )))
    }

    fn list(&self) -> Vec<ProviderId> {
        self.providers
            .lock()
            .expect("providers mutex poisoned")
            .keys()
            .cloned()
            .collect()
    }

    fn state(&self, provider_id: &ProviderId) -> Result<ProviderState, StorageError> {
        let providers = self.providers.lock().expect("providers mutex poisoned");
        providers
            .get(provider_id)
            .map(|e| e.state)
            .ok_or(StorageError::ProviderNotFound(provider_id.clone()))
    }

    fn health_check(&self) -> HealthStatus {
        let providers = self.providers.lock().expect("providers mutex poisoned");
        let mut has_degraded = false;
        for entry in providers.values() {
            if entry.state != ProviderState::Running {
                continue;
            }
            match entry.provider.health_check() {
                HealthStatus::Unhealthy(_) => {
                    return HealthStatus::Unhealthy("a provider is unhealthy".to_string());
                }
                HealthStatus::Disabled => {
                    return HealthStatus::Unhealthy("a provider is disabled".to_string());
                }
                HealthStatus::Degraded(_) => has_degraded = true,
                HealthStatus::Healthy => {}
            }
        }
        if has_degraded {
            HealthStatus::Degraded("a provider is degraded".to_string())
        } else {
            HealthStatus::Healthy
        }
    }
}
