# RFC-0324: Workflow Storage

# RFC-0324: Workflow Storage
'''
## Header
'''
```
RFC: RFC-0324
Title: Workflow Storage
Status: Proposed
Version: 1.0.0
Author: Atlas Specification Committee
Created: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1004 Common Contract Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0312 Scheduler
  - RFC-0315 Recovery
  - RFC-0316 Debugging
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1006 Common Error Model
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01
Related ADR: ADR-0012
Related JSON Schema: workflow-result-types.md
Related Catalog: workflow-result-types.md
```
'''

## Abstract

This RFC defines the storage abstraction layer for Atlas Workflow, providing a uniform interface for persisting workflow state, execution data, plugin configurations, and audit records. The storage layer supports multiple backend implementations while maintaining a consistent API contract, enabling deployment flexibility and operational resilience.

## Status

This is a Proposed specification. Implementation feedback is encouraged before final adoption.

## Motivation

Atlas Workflow must persist diverse data types with varying consistency, durability, and performance requirements:

- Workflow execution state (running, completed, failed)
- Step execution results and intermediate data
- Plugin configuration and version metadata
- Audit logs and observability data references
- Scheduling queues and pending execution state

Without a unified storage abstraction, the workflow engine couples directly to specific database technologies, creating deployment rigidity, upgrade friction, and vendor lock-in. A storage abstraction layer enables:

- Backend-agnostic workflow engine (any SQL, NoSQL, or key-value store)
- Seamless migration between storage backends
- Multi-backend strategies (e.g., SQL for state, blob store for artifacts)
- Consistent data lifecycle management across backends

## Scope

This RFC covers:

- Storage abstraction interface definitions
- Workflow state persistence model
- Execution data storage and retrieval
- Plugin configuration storage
- Audit log storage
- Storage backend selection and routing
- Data lifecycle management (retention, archival, purge)
- Storage consistency and durability guarantees

This RFC does NOT cover:

- Specific storage backend implementations (configuration concern)
- Storage infrastructure provisioning (infrastructure concern)
- Database schema design for specific backends (implementation detail)
- Storage encryption at rest (security concern, covered by RFC-0319)
- Storage network security (security concern)

## Terminology

The following terms are defined per RFC-0301 (Workflow Overview) and extended for storage:

| Term | Definition |
| --- | --- |
| Storage Backend | A specific database or storage system implementation behind the abstraction |
| Storage Abstraction | The interface layer between workflow components and storage backends |
| Storage Router | Component that directs data access requests to appropriate backends |
| Data Partition | A logical subdivision of storage for a specific data type or tenant |
| Storage Consistency | The guarantee level for data visibility after write (strong, eventual, causal) |
| Storage Durability | The guarantee that persisted data survives system failures |
| Storage TTL | Time-To-Live for stored data entries, after which they are automatically purged |
| Storage Index | A secondary data structure optimizing query performance for specific access patterns |
| Storage Migration | The process of transforming data between storage schema versions |
| Storage Snapshot | A point-in-time backup of storage data |
| Storage WAL | Write-Ahead Log for transactional durability |
| Storage Sharding | Distribution of data across multiple storage instances |
| Storage Replication | Copying data across multiple storage instances for availability |
| Storage Tier | A storage backend with specific performance and cost characteristics |

## Requirements

### Requirement 1: Storage Abstraction Interface

The implementation MUST provide a unified storage interface abstracting backend details.

The implementation MUST define the following core storage operations:

**Entity CRUD Operations:**
- create(entity_type, entity_id, data, options) -> StorageResult
- 
ead(entity_type, entity_id, options) -> StorageResult
- update(entity_type, entity_id, data, options) -> StorageResult
- delete(entity_type, entity_id, options) -> StorageResult
- exists(entity_type, entity_id) -> bool

**Query Operations:**
- query(entity_type, filter, options) -> StorageResult[]
- count(entity_type, filter) -> int
- scan(entity_type, cursor, limit) -> StorageResult[]

**Transaction Operations:**
- egin_transaction() -> TransactionHandle
- 	ransaction.commit(handle) -> bool
- 	ransaction.rollback(handle) -> bool
- 	ransaction.isolation_level() -> IsolationLevel

**Lifecycle Operations:**
- migrate(schema_version) -> MigrationResult
- ackup(target) -> BackupResult
- 
estore(source) -> RestoreResult

The implementation MUST:

- Support at least one SQL backend (PostgreSQL, MySQL, or compatible)
- Support at least one NoSQL backend (MongoDB, DynamoDB, or compatible)
- Support at least one key-value backend (Redis, etcd, or compatible)
- Route data access to the appropriate backend based on entity type
- Maintain a storage backend registry mapping entity types to backends

The implementation SHOULD:

- Support connection pooling for all backends
- Provide automatic retry with exponential backoff for transient failures
- Support configurable consistency levels per operation

### Requirement 2: Workflow State Persistence

The implementation MUST persist workflow execution state with appropriate durability guarantees.

The implementation MUST:

- Store workflow execution state in a durable, transactional backend (SQL)
- Persist the following workflow state entities:
  - Workflow definition (id, name, version, schema, status)
  - Workflow execution (id, workflow_id, status, inputs, outputs, created_at, updated_at)
  - Workflow step state (execution_id, step_id, status, inputs, outputs, retries, error)
  - Workflow trigger state (execution_id, trigger_id, fired_at, result)
  - Workflow condition state (step_id, condition_id, evaluated_at, result)
- Use optimistic concurrency control for workflow state updates
- Implement workflow state snapshots for long-running executions (interval: configurable, default: every 100 steps)
- Support workflow state restore from snapshot

The implementation SHOULD:

- Compress workflow execution payload data exceeding 1MB
- Support workflow state export/import for migration

The implementation MAY:

- Support workflow state replication across geographic regions

#### Workflow State Storage Model

`mermaid
entityRelation
    WorkflowDef ||--o{ WorkflowExec : defines
    WorkflowExec ||--o{ StepState : contains
    WorkflowExec ||--o{ TriggerState : contains
    WorkflowExec ||--o{ ConditionState : contains
    StepState ||--o{ StepOutput : produces
    WorkflowExec }|--|| WorkflowSnapshot : snapshotted_by
`

### Requirement 3: Execution Data Storage

The implementation MUST store execution data with appropriate performance characteristics.

The implementation MUST:

- Store step execution results in a write-optimized backend (NoSQL or key-value)
- Store workflow input/output data with configurable retention (default: 30 days)
- Support bulk read of execution data for observability queries (RFC-0321)
- Implement data partitioning by workflow_id and time_range for query performance
- Enforce maximum payload size per execution record (default: 10MB)

The implementation SHOULD:

- Support streaming export of execution data for analytics
- Provide execution data deduplication for idempotent operations

### Requirement 4: Plugin Configuration Storage

The implementation MUST store plugin configurations and metadata.

The implementation MUST:

- Store plugin manifests in a versioned configuration store
- Store plugin dependency graphs for conflict detection
- Store plugin permission grants and access policies
- Support plugin configuration hot-reload without engine restart
- Implement plugin configuration change auditing

The implementation SHOULD:

- Cache plugin configurations in memory for performance
- Support plugin configuration rollback to previous versions

### Requirement 5: Audit Log Storage

The implementation MUST provide durable storage for audit logs.

The implementation MUST:

- Store audit logs in an append-only, immutable store
- Enforce write-once, read-many semantics for audit log entries
- Implement audit log integrity verification (hash chain or equivalent)
- Support audit log query by correlation_id, workflow_id, time_range, event_type
- Store audit logs with configurable retention period (default: 90 days, minimum: 30 days)

The implementation SHOULD:

- Support audit log export to external storage (S3, blob store) for long-term retention
- Implement audit log compression for archived entries

The implementation MAY:

- Support audit log signing for legal compliance

### Requirement 6: Storage Consistency and Durability

The implementation MUST define and enforce storage consistency guarantees.

The implementation MUST:

- Provide strong consistency for workflow state reads and writes
- Provide eventual consistency for execution data reads (with configurable staleness tolerance)
- Provide strong durability for audit logs (write-ahead logging)
- Implement storage transaction isolation at the Serializable level for workflow state
- Support storage failover with automatic reconnection and state reconciliation

The implementation SHOULD:

- Provide storage health monitoring and alerting
- Implement storage capacity planning metrics

## Layer Boundaries

### Storage Layer Responsibilities
- Provide unified storage abstraction interface
- Route data access requests to appropriate backends
- Manage storage backend connections and pooling
- Enforce data consistency and durability guarantees
- Handle storage migrations and schema evolution
- Manage data lifecycle (retention, archival, purge)

### Storage Layer Non-Responsibilities
- Business logic for workflow state transitions (workflow engine)
- Query optimization beyond standard indexing (backend responsibility)
- Storage infrastructure provisioning and scaling (infrastructure)
- Data encryption at rest (security layer)
- Network security for storage connections (infrastructure)

### Dependencies
- Depends on: RFC-0304 (Workflow Runtime), RFC-0321 (Observability)
- Depends on: RFC-0322 (Extension Points), RFC-0323 (Plugin Integration)
- Provides to: Workflow Executor, Scheduler, Plugin Manager, Audit Logger
- Consumers: All workflow subsystems requiring data persistence
- Providers: SQL backends, NoSQL backends, key-value backends

### Forbidden Dependencies
- The storage layer MUST NOT depend on any specific backend implementation details
- The storage layer MUST NOT expose backend-specific APIs to workflow components
- Workflow components MUST NOT access storage backends directly (must route through abstraction)
- The storage layer MUST NOT assume any specific operating system or hardware

## Future Evolution

- **v1.1**: Add support for distributed storage transactions across backends
- **v1.2**: Introduce storage tiering (hot/warm/cold) for cost optimization
- **v1.3**: Add storage compression algorithms for large execution payloads
- **v2.0**: Support for multi-region storage replication with conflict resolution
- **v2.0**: Add storage-aware query optimization based on access pattern analysis

## Runtime Independence

This specification is runtime-independent. The storage layer MUST NOT assume:

- Any specific programming language for implementation
- Any specific runtime environment (Electron, Tauri, browser, server)
- Any specific operating system
- Any specific GPU or graphics acceleration
- Any specific threading model

Storage backends MUST be accessible via standard network protocols (TCP/IP, HTTP, gRPC) or standard library interfaces.


#### Storage Backend Routing

`mermaid
graph TB
    subgraph Workflow Components
        WE[Workflow Executor]
        WS[Workflow Scheduler]
        WP[Plugin Manager]
        WA[Audit Logger]
    end

    subgraph Storage Abstraction
        SAR[Storage Router]
        SP[Connection Pool]
        ST[Transaction Manager]
    end

    subgraph SQL Backend
        PG[(PostgreSQL)]
        PGWF[Workflow State]
        PGPC[Plugin Config]
    end

    subgraph NoSQL Backend
        MO[(MongoDB)]
        MOED[Execution Data]
        MOAT[Audit Logs]
    end

    subgraph KV Backend
        RD[(Redis)]
        RDCQ[Scheduling Queue]
        RDCache[Config Cache]
    end

    WE --> SAR
    WS --> SAR
    WP --> SAR
    WA --> SAR
    SAR --> SP
    SP --> ST
    ST --> PG
    ST --> MO
    ST --> RD
    PG --> PGWF
    PG --> PGPC
    MO --> MOED
    MO --> MOAT
    RD --> RDCQ
    RD --> RDCache

`

#### Data Lifecycle Management

`mermaid
graph LR
    subgraph Active Tier
        AT1[Workflow State<br/>SQL Backend]
        AT2[Execution Data<br/>NoSQL Backend]
        AT3[Plugin Config<br/>SQL Backend]
    end

    subgraph Archive Tier
        AR1[Completed Workflows<br/>Blob Store]
        AR2[Audit Logs<br/>Append-Only Store]
        AR3[Old Executions<br/>Cold Storage]
    end

    subgraph Purge Tier
        PU1[Expired Sessions]
        PU2[Orphaned Data]
        PU3[Temp Files]
    end

    AT1 -->|TTL exceeded| AR1
    AT2 -->|Retention policy| AR2
    AT3 -->|Version obsolete| AR3
    AR1 -->|Legal hold| PU1
    AR2 -->|Compliance period| PU2
    AR3 -->|Cleanup job| PU3

`
## Acceptance Criteria

1. The implementation MUST provide a unified storage abstraction interface as defined in Requirement 1.
2. The implementation MUST persist workflow execution state with strong consistency and durability.
3. The implementation MUST store step execution results with write-optimized performance.
4. The implementation MUST enforce append-only, immutable semantics for audit log storage.
5. The implementation MUST support at least one SQL, one NoSQL, and one key-value storage backend.
6. The implementation MUST route data access to appropriate backends based on entity type.
7. The implementation MUST provide transaction support for workflow state operations.
8. The implementation MUST enforce data retention policies for execution data and audit logs.
9. The implementation MUST support storage migration between schema versions.
10. The implementation MUST NOT expose backend-specific APIs to workflow components.

## References

| Type | Reference | Description |
| --- | --- | --- |
| Related RFC | RFC-0301 | Workflow Overview (Terminology source) |
| Related RFC | RFC-0304 | Workflow Runtime |
| Related RFC | RFC-0312 | Scheduler |
| Related RFC | RFC-0315 | Recovery |
| Related RFC | RFC-0316 | Debugging |
| Related RFC | RFC-0321 | Observability |
| Related RFC | RFC-0322 | Extension Points |
| Related RFC | RFC-0323 | Plugin Integration |
| Related RFC | RFC-1002 | Common State Model |
| Related ADR | ADR-0012 | Storage Architecture Decision |
| Related JSON Schema | workflow-result-types.md | Storage result type schema |
| Related Catalog | workflow-result-types.md | Catalog entry for storage types |
| See Also | ACID Properties | Database transaction guarantees reference |
| See Also | CAP Theorem | Distributed storage tradeoffs reference |
