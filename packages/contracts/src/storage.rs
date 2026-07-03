//! Storage provider and registry contracts.
//!
//! Defines the abstract Provider Interface (RFC-0403 §4), the Provider
//! Lifecycle state machine (RFC-0403 §5), the Resource Lifecycle state
//! machine (RFC-0404 §8), and the Provider Registry contract
//! (RFC-0401 / RFC-0403).
//!
//! This module exposes **abstract providers and registries only**. It MUST NOT
//! contain any database-specific logic. Concrete backends implement
//! [`StorageProvider`]; the platform implements [`ProviderRegistry`].

use crate::service::HealthStatus;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use thiserror::Error;

/// Unique identifier for a storage provider.
pub type ProviderId = String;
/// Unique identifier for a stored resource.
pub type ResourceId = String;
/// Unique identifier for an open transaction.
pub type TransactionId = String;

/// Capabilities a storage provider MAY declare (RFC-0403 §6.1).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ProviderCapability {
    /// Read resources by ID. Required for all providers.
    Read,
    /// Write resources by ID. Required for all providers.
    Write,
    /// Delete resources by ID. Required for all providers.
    Delete,
    /// Execute filtered queries.
    Query,
    /// Support transactions.
    Transaction,
    /// Support batch operations.
    Batch,
    /// Support data replication.
    Replicate,
    /// Support backup operations.
    Backup,
    /// Support version history.
    Versioning,
    /// Support encryption at rest.
    Encryption,
    /// Support streaming operations.
    Streaming,
    /// Support row-level locking.
    Locking,
}

impl ProviderCapability {
    /// Return the canonical string name of the capability.
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Read => "read",
            Self::Write => "write",
            Self::Delete => "delete",
            Self::Query => "query",
            Self::Transaction => "transaction",
            Self::Batch => "batch",
            Self::Replicate => "replicate",
            Self::Backup => "backup",
            Self::Versioning => "versioning",
            Self::Encryption => "encryption",
            Self::Streaming => "streaming",
            Self::Locking => "locking",
        }
    }

    /// The capabilities that RFC-0403 §6.1 marks as required for ALL providers.
    pub const REQUIRED_FOR_ALL: &'static [ProviderCapability] =
        &[Self::Read, Self::Write, Self::Delete];
}

/// Provider lifecycle states (RFC-0403 §5.2).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ProviderState {
    /// Detected by the registry but not yet registered.
    Discovered,
    /// Registry is validating the provider implementation.
    Validating,
    /// Passed validation and registered. Not yet serving operations.
    Registered,
    /// Initialising internal state and connections.
    Activating,
    /// Fully initialised and visible to the provider selector.
    Active,
    /// Actively serving operations; health checks passing.
    Running,
    /// Transitioning from Running to Suspended; draining operations.
    Suspending,
    /// Inactive but retains configuration; can be resumed.
    Suspended,
    /// Transitioning from Suspended back to Running.
    Resuming,
    /// Shutting down gracefully; closing connections and flushing buffers.
    Deactivating,
    /// Encountered an unrecoverable error; cannot serve operations.
    Failed,
    /// Fully removed from the registry; all resources released.
    Terminated,
}

impl ProviderState {
    /// Terminal states from which no further transition is allowed.
    pub fn is_terminal(&self) -> bool {
        matches!(self, Self::Terminated)
    }
}

impl std::fmt::Display for ProviderState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}

/// Legal provider state transitions per RFC-0403 §5.3.
pub const LEGAL_PROVIDER_TRANSITIONS: &[(ProviderState, ProviderState)] = &[
    (ProviderState::Discovered, ProviderState::Validating),
    (ProviderState::Validating, ProviderState::Registered),
    (ProviderState::Validating, ProviderState::Failed),
    (ProviderState::Registered, ProviderState::Activating),
    (ProviderState::Activating, ProviderState::Active),
    (ProviderState::Activating, ProviderState::Failed),
    (ProviderState::Active, ProviderState::Running),
    (ProviderState::Running, ProviderState::Suspending),
    (ProviderState::Suspending, ProviderState::Suspended),
    (ProviderState::Suspended, ProviderState::Resuming),
    (ProviderState::Resuming, ProviderState::Running),
    (ProviderState::Running, ProviderState::Deactivating),
    (ProviderState::Deactivating, ProviderState::Registered),
    (ProviderState::Running, ProviderState::Failed),
    (ProviderState::Failed, ProviderState::Terminated),
];

/// Whether a provider transition is permitted by RFC-0403 §5.3.
pub fn is_legal_provider_transition(from: ProviderState, to: ProviderState) -> bool {
    LEGAL_PROVIDER_TRANSITIONS
        .iter()
        .any(|&(f, t)| f == from && t == to)
}

/// Resource lifecycle states (RFC-0404 §8).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ResourceState {
    /// Resource is being prepared for validation.
    Created,
    /// Resource is being validated.
    Validating,
    /// Resource is durably stored but not yet active.
    Stored,
    /// Resource is active and available for operations.
    Active,
    /// Resource is being updated.
    Updating,
    /// Resource is archived (soft removal).
    Archived,
    /// Resource is being deleted.
    Deleting,
    /// Resource is permanently removed.
    Purged,
    /// Resource is being restored from archive.
    Restoring,
    /// Resource encountered an unrecoverable error.
    Failed,
}

impl ResourceState {
    /// Terminal resource states.
    pub fn is_terminal(&self) -> bool {
        matches!(self, Self::Purged | Self::Failed)
    }
}

impl std::fmt::Display for ResourceState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}

/// Legal resource state transitions per RFC-0404 §8.
pub const LEGAL_RESOURCE_TRANSITIONS: &[(ResourceState, ResourceState)] = &[
    (ResourceState::Created, ResourceState::Validating),
    (ResourceState::Validating, ResourceState::Stored),
    (ResourceState::Validating, ResourceState::Failed),
    (ResourceState::Stored, ResourceState::Active),
    (ResourceState::Active, ResourceState::Archived),
    (ResourceState::Active, ResourceState::Updating),
    (ResourceState::Updating, ResourceState::Active),
    (ResourceState::Updating, ResourceState::Failed),
    (ResourceState::Active, ResourceState::Deleting),
    (ResourceState::Deleting, ResourceState::Archived),
    (ResourceState::Deleting, ResourceState::Purged),
    (ResourceState::Archived, ResourceState::Restoring),
    (ResourceState::Restoring, ResourceState::Stored),
    (ResourceState::Restoring, ResourceState::Failed),
];

/// Whether a resource transition is permitted by RFC-0404 §8.
pub fn is_legal_resource_transition(from: ResourceState, to: ResourceState) -> bool {
    LEGAL_RESOURCE_TRANSITIONS
        .iter()
        .any(|&(f, t)| f == from && t == to)
}

/// Transaction isolation levels (RFC-0406).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum IsolationLevel {
    /// Read committed isolation.
    ReadCommitted,
    /// Serializable isolation.
    Serializable,
    /// Snapshot isolation.
    Snapshot,
}

/// Options for a read operation (RFC-0403 §4.1).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ReadOptions {
    /// Specific version to read, or latest if `None`.
    pub version: Option<u64>,
    /// Whether to include resource metadata alongside data.
    pub include_metadata: bool,
}

/// Options for a write operation (RFC-0403 §4.1).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct WriteOptions {
    /// Fail if a resource with this ID already exists.
    pub if_not_exists: bool,
    /// Optimistic concurrency: fail unless the current version matches.
    pub expected_version: Option<u64>,
}

/// Options for a delete operation (RFC-0403 §4.1).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct DeleteOptions {
    /// Soft-delete (archive) instead of hard purge.
    pub soft_delete: bool,
}

/// A query filter (RFC-0403 §4.1). The predicate is an opaque JSON expression
/// interpreted by the provider, keeping this contract backend-agnostic.
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct QueryFilter {
    /// Provider-interpreted predicate expression.
    pub predicate: serde_json::Value,
    /// Optional maximum number of results.
    pub limit: Option<usize>,
}

/// Pagination cursor for query results (RFC-0403 §4.1).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct Pagination {
    /// Number of results to skip.
    pub offset: usize,
    /// Maximum number of results to return.
    pub limit: usize,
}

/// A query result set (RFC-0403 §4.1).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ResultSet {
    /// Resource IDs matching the query.
    pub ids: Vec<ResourceId>,
    /// Total matching count before pagination.
    pub total_count: usize,
}

/// Metadata describing a stored resource (RFC-0423 resource model).
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ResourceMetadata {
    /// Resource identifier.
    pub id: ResourceId,
    /// Current version number.
    pub version: u64,
    /// Creation timestamp (ms since UNIX epoch).
    pub created_ms: u64,
    /// Last update timestamp (ms since UNIX epoch).
    pub updated_ms: u64,
    /// Size of the resource payload in bytes.
    pub size_bytes: u64,
    /// MIME content type of the payload.
    pub content_type: String,
    /// Arbitrary provider-defined tags.
    pub tags: serde_json::Map<String, serde_json::Value>,
}

/// A stored resource: metadata plus payload bytes (RFC-0423).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Resource {
    /// Resource metadata.
    pub metadata: ResourceMetadata,
    /// Raw resource payload.
    pub data: Vec<u8>,
}

/// Error taxonomy for storage operations (RFC-0403 §4 + RFC-1006).
#[derive(Error, Debug, Clone, PartialEq)]
pub enum StorageError {
    /// Resource not found.
    #[error("resource not found: {0}")]
    NotFound(ResourceId),
    /// Access denied by authorization policy.
    #[error("access denied: {0}")]
    AccessDenied(String),
    /// Resource payload failed validation.
    #[error("validation error: {0}")]
    ValidationError(String),
    /// Write conflict (e.g. version mismatch or duplicate).
    #[error("conflict: {0}")]
    Conflict(String),
    /// Resource is locked by another operation.
    #[error("resource locked: {0}")]
    Locked(ResourceId),
    /// Query expression is invalid.
    #[error("invalid query: {0}")]
    InvalidQuery(String),
    /// Operation timed out.
    #[error("timeout: {0}")]
    Timeout(String),
    /// No provider available to serve the request.
    #[error("provider unavailable: {0}")]
    ProviderUnavailable(String),
    /// Transaction already committed.
    #[error("transaction already committed: {0}")]
    AlreadyCommitted(TransactionId),
    /// Schema migration failed.
    #[error("migration error: {0}")]
    MigrationError(String),
    /// Provider configuration error.
    #[error("config error: {0}")]
    ConfigError(String),
    /// Operation not supported by the provider.
    #[error("not supported: {0}")]
    NotSupported(String),
    /// Provider has failed and cannot serve operations.
    #[error("provider failed: {0}")]
    ProviderFailed(String),
    /// Required capability not declared by any provider.
    #[error("capability not supported: {0}")]
    CapabilityNotSupported(String),
    /// Illegal provider lifecycle transition.
    #[error("illegal provider transition from {from} to {to}")]
    IllegalProviderTransition {
        /// Source state.
        from: ProviderState,
        /// Target state.
        to: ProviderState,
    },
    /// Illegal resource lifecycle transition.
    #[error("illegal resource transition from {from} to {to}")]
    IllegalResourceTransition {
        /// Source state.
        from: ResourceState,
        /// Target state.
        to: ResourceState,
    },
    /// Provider ID already registered.
    #[error("provider already registered: {0}")]
    AlreadyRegistered(ProviderId),
    /// Provider not registered.
    #[error("provider not registered: {0}")]
    ProviderNotFound(ProviderId),
}

/// The Provider Interface (RFC-0403 §4).
///
/// Every storage backend MUST implement this trait. Implementations are
/// expected to use interior mutability (`&self`) for stateful operations so
/// the provider can be shared via [`Arc`] by the registry. The trait is
/// deliberately free of any database-specific types.
pub trait StorageProvider: Send + Sync {
    /// Stable provider identifier.
    fn id(&self) -> &ProviderId;
    /// Capabilities declared by this provider.
    fn capabilities(&self) -> &[ProviderCapability];

    /// Read a resource by ID. Returns `NotFound` if absent, `AccessDenied` on
    /// authorization failure (RFC-0403 §4.1).
    fn read(&self, id: &ResourceId, options: &ReadOptions) -> Result<Resource, StorageError>;
    /// Store or update a resource. Returns the new version number, or
    /// `ValidationError` / `Conflict` on failure (RFC-0403 §4.1).
    fn write(
        &self,
        id: &ResourceId,
        data: &[u8],
        options: &WriteOptions,
    ) -> Result<u64, StorageError>;
    /// Remove a resource. Returns the deleted version, or `NotFound` / `Locked`
    /// on failure (RFC-0403 §4.1).
    fn delete(&self, id: &ResourceId, options: &DeleteOptions) -> Result<u64, StorageError>;
    /// Execute a filtered query (RFC-0403 §4.1).
    fn query(
        &self,
        filter: &QueryFilter,
        pagination: &Pagination,
    ) -> Result<ResultSet, StorageError>;
    /// Check whether a resource exists (RFC-0403 §4.1).
    fn exists(&self, id: &ResourceId) -> Result<bool, StorageError>;

    /// Begin a new transaction at the given isolation level (RFC-0403 §4.2).
    fn begin_transaction(
        &self,
        isolation: IsolationLevel,
    ) -> Result<TransactionId, StorageError>;
    /// Commit an open transaction (RFC-0403 §4.2).
    fn commit_transaction(&self, tx: &TransactionId) -> Result<u64, StorageError>;
    /// Roll back an open transaction (RFC-0403 §4.2).
    fn rollback_transaction(&self, tx: &TransactionId) -> Result<(), StorageError>;
    /// Prepare a transaction for two-phase commit (RFC-0403 §4.2).
    fn prepare_transaction(&self, tx: &TransactionId) -> Result<bool, StorageError>;
    /// Abort a transaction without rollback (RFC-0403 §4.2).
    fn abort_transaction(&self, tx: &TransactionId) -> Result<(), StorageError>;

    /// Check provider health (RFC-0403 §4.3).
    fn health_check(&self) -> HealthStatus;
    /// Return provider metrics as an opaque JSON map (RFC-0403 §4.3).
    fn get_metrics(&self) -> serde_json::Value;
    /// Return detailed provider status as an opaque JSON object (RFC-0403 §4.3).
    fn get_status(&self) -> serde_json::Value;

    /// Initialise the provider with backend configuration (RFC-0403 §4.4).
    fn initialize(&self, config: &serde_json::Value) -> Result<(), StorageError>;
    /// Gracefully shut down the provider (RFC-0403 §4.4).
    fn shutdown(&self) -> Result<(), StorageError>;
    /// Migrate provider data between schema versions (RFC-0403 §4.4).
    fn migrate(&self, version_from: u32, version_to: u32) -> Result<(), StorageError>;
}

/// The Provider Registry contract (RFC-0401 / RFC-0403).
///
/// The registry discovers, registers, and manages storage providers, enforces
/// the provider lifecycle state machine, and performs capability-based
/// provider selection (RFC-0403 §6.2 / §7).
pub trait ProviderRegistry: Send + Sync {
    /// Register a discovered provider. Validates that the provider declares
    /// all capabilities required for every provider (RFC-0403 §6.1) and
    /// transitions it through `Validating` → `Registered`.
    fn register(&self, provider: Arc<dyn StorageProvider>) -> Result<(), StorageError>;
    /// Activate a registered provider (`Registered` → `Active` → `Running`).
    fn activate(&self, provider_id: &ProviderId) -> Result<(), StorageError>;
    /// Deactivate a running provider (`Running` → `Deactivating` → `Registered`).
    fn deactivate(&self, provider_id: &ProviderId) -> Result<(), StorageError>;
    /// Look up a registered provider by ID.
    fn get(&self, provider_id: &ProviderId) -> Result<Arc<dyn StorageProvider>, StorageError>;
    /// Select the best provider that declares all `required` capabilities
    /// (RFC-0403 §6.2 / §7).
    fn select(
        &self,
        required: &[ProviderCapability],
    ) -> Result<Arc<dyn StorageProvider>, StorageError>;
    /// List the IDs of all registered providers.
    fn list(&self) -> Vec<ProviderId>;
    /// Return the lifecycle state of a provider.
    fn state(&self, provider_id: &ProviderId) -> Result<ProviderState, StorageError>;
    /// Aggregate health across all running providers.
    fn health_check(&self) -> HealthStatus;
}



