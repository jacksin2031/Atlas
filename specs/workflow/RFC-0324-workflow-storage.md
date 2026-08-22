RFC: RFC-0324
Title: Workflow Storage
Status: Proposed
Version: 1.1.0
Author: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADR References:
  - ADR-0012 Contract-First Specification-Driven Development`nRelated ADR: ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/performance-metric.json
  - schemas/workflow/sla-definition.json
Related Catalog:
  - catalog/workflow-metrics.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

---

---

## Authority

This RFC is the authoritative specification for the RFC 0324 workflow storage.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.



This RFC is the authoritative specification for the RFC 0324 workflow storage.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## Normative Status
This specification is normative. Every implementation MUST conform to the requirements defined herein.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Storage Backend | A pluggable data persistence mechanism for workflow state and results. | RFC-0324 |
| Storage Route | A mapping that directs workflow data to the appropriate storage backend. | RFC-0324 |
| State Persistence | The durable storage of workflow execution state for recovery. | RFC-0324 |
| Resource Lifecycle | The managed progression of stored workflow resources from creation to deletion. | RFC-0324 |

## 2 Layer Boundaries

## 3 Security
- Stored workflow data MUST be encrypted at rest per RFC-0319.
- Storage access MUST be authorized per the permission model.
- Sensitive data in storage MUST be classified and handled per RFC-0319 data classification.

## 4 Performance
- State persistence MUST complete within 10ms for typical workflow state.
- Checkpoint reads for recovery MUST complete within 50ms.
- Storage operations MUST NOT block workflow execution (async writes).

## 5 Compatibility
- Storage formats MUST be backward compatible within a major version.
- New storage backends MAY be added without breaking existing workflows.

## 6 Compliance
- All stored workflow data MUST include version metadata for compliance tracking per RFC-0330.
- Storage retention policies MUST comply with organizational data retention requirements.

## 7 Future Evolution
- **Multi-Region Storage**: Geographically distributed storage with automatic replication.
- **Tiered Storage**: Automatic migration of data between hot, warm, and cold storage tiers.
- **Immutable Storage**: Append-only storage for regulatory compliance.
- **Serverless Storage**: Pay-per-use storage for ephemeral workflow data.

## 8 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

## 9 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (state persistence) |
| RFC-0304 | Workflow Runtime (storage context) |
| RFC-0315 | Workflow Recovery (checkpoint restoration) |
| RFC-0317 | Workflow Validation (validation result storage) |
| RFC-0319 | Workflow Security (storage encryption) |
| RFC-0320 | Workflow Performance (storage performance) |
| RFC-0321 | Workflow Observability (audit log storage) |
| RFC-0328 | Workflow Serialization (data serialization) |`n| RFC-0312 | Workflow Scheduler (scheduling state storage)
| RFC-0330 | Workflow Compliance (storage compliance) |`n| RFC-0316 | Workflow Debugging (debug storage hooks)
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/storage-route.json | Storage Route JSON Schema |
| catalog/workflow-resource-types.md | Resource Types Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0324 (this document), RFC-0315 (Recovery), RFC-0319 (Security) |
---


## 10 Storage Architecture

This section defines the storage abstraction architecture for workflow data.

### 10.1 Storage Abstraction Layer

The storage layer provides a uniform interface over heterogeneous storage backends. The abstraction consists of:

| Component | Responsibility | Interface |
|---|---|---|
| Storage Router | Routes data to appropriate backend based on type and policy | oute(data_type, policy) → backend_id |
| Storage Backend | Pluggable persistence mechanism for a data category | CRUD interface per RFC-0324 |
| Storage Cache | In-memory cache for hot data with configurable eviction | LRU/LFU with TTL |
| Storage Serializer | Serializes workflow data for persistence | RFC-0328 contract |
| Storage Encryptor | Encrypts sensitive data at rest | Per RFC-0319 classification |
| Storage Compactor | Reclaims space from deleted/overwritten data | Periodic compaction |

### 10.2 Storage Routes

Storage routes define how data types map to storage backends:

| Route Type | Data Category | Backend Example | Retention |
|---|---|---|---|
| State | Workflow execution state | Any durable store | Per checkpoint policy |
| Result | Node/action output results | Any durable store | Per workflow policy |
| Checkpoint | Recovery checkpoints | Any durable store | Per recovery policy |
| Audit | Audit log entries | Append-only store | Per compliance policy |
| Telemetry | Metrics and traces | Time-series store | Per retention policy |
| Metadata | Workflow definitions, schemas | Any durable store | Permanent |
| Temporary | Session data, caches | In-memory store | Ephemeral |

Each route declares: oute_id, data_types[], ackend_id, policy, etention, encryption_required.

### 10.3 Storage Backend Interface

Every storage backend MUST implement the following interface:

| Method | Input | Output | Description |
|---|---|---|---|
| Put | key, value, options | result | Store a value |
| Get | key, options | value \| null | Retrieve a value |
| Delete | key, options | result | Remove a value |
| List | prefix, options | key[] | List keys with prefix |
| Exists | key | bool | Check key existence |
| Transaction | operations[] | result | Atomic multi-operation |
| Migrate | source_backend, keys[] | result | Move data between backends |
| Compact | - | result | Reclaim storage space |

All methods MUST support the standard options: 	tl, encrypt, priority, callback.

### 10.4 State Persistence Model

Workflow state persistence follows a write-ahead log (WAL) pattern:

1. **Write**: State mutation is appended to the WAL first.
2. **Flush**: WAL is flushed to durable storage.
3. **Checkpoint**: Periodic snapshot of state is taken.
4. **Compact**: Old WAL segments are compacted after checkpoint confirmation.

The WAL MUST support replay from any committed entry for recovery.

### 10.5 Checkpoint Model

Checkpoints are full or incremental snapshots of workflow state:

| Checkpoint Type | Content | Frequency | Size |
|---|---|---|---|
| Full | Complete workflow state | Manual or scheduled | Large |
| Incremental | State deltas since last checkpoint | Automatic | Small |
| Transactional | Committed transaction state | Per transaction | Variable |

Checkpoints MUST include: checkpoint_id, workflow_id, execution_id, 	imestamp_ns, state_hash, size_bytes, 	ype.

### 10.6 Storage Encryption Model

Data at rest MUST be encrypted per RFC-0319 data classification:

| Classification | Encryption | Key Management |
|---|---|---|
| Public | None | None |
| Internal | AES-256-GCM | Symmetric key |
| Confidential | AES-256-GCM | Per-record key |
| Restricted | AES-256-GCM + HSM | Hardware-backed key |

Encryption keys MUST never be stored alongside the data they protect.

### 10.7 Storage Tiering

Implementations SHOULD support automatic data tiering:

| Tier | Characteristics | Use Case | Migration Trigger |
|---|---|---|---|
| Hot | In-memory or NVMe | Active workflow state | N/A |
| Warm | SSD storage | Recent checkpoints | 24 hours idle |
| Cold | Object storage | Archived workflows | 30 days idle |
| Archive | Tape/durable | Compliance retention | 1 year idle |

### 10.8 Storage Consistency Model

Different data categories have different consistency requirements:

| Data Category | Consistency Level | Isolation Level | Durability |
|---|---|---|---|
| Execution State | Strong | Serializable | Immediately durable |
| Results | Eventual | Read Committed | Durable on write |
| Checkpoints | Strong | Serializable | Durable on flush |
| Audit Logs | Strong | Serializable | Append-only durable |
| Telemetry | Eventual | Read Your Writes | Buffered durable |
| Metadata | Strong | Serializable | Immediately durable |

## 11 Acceptance Criteria

### 11.1 Storage Interface Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Every storage backend MUST implement all eight (8) interface methods: Put, Get, Delete, List, Exists, Transaction, Migrate, Compact. | Interface test: Instantiate any backend → Verify all eight methods callable with correct signatures |
| AC-02 | The Transaction method MUST provide atomic semantics: either all operations succeed or none do. | Atomicity test: Execute 5-operation transaction with simulated failure on operation 3 → Verify all 5 operations rolled back, no partial state |
| AC-03 | Storage routes MUST support at least seven (7) route types: State, Result, Checkpoint, Audit, Telemetry, Metadata, Temporary. | Route enumeration test: Configure all seven route types → Verify data routed correctly to designated backends |

### 11.2 Persistence Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-04 | State mutations MUST be written to WAL before being applied to state. | WAL order test: Trigger state mutation → Inspect WAL → Verify WAL entry precedes state change |
| AC-05 | Checkpoints MUST include all six (6) required fields: checkpoint_id, workflow_id, execution_id, timestamp_ns, state_hash, size_bytes. | Checkpoint schema test: Create checkpoint → Verify all six fields present with valid types |
| AC-06 | The WAL MUST support replay from any committed entry. | WAL replay test: Record 100 mutations → Remove last 50 → Replay from entry 50 → Verify state matches post-entry-50 state |

### 11.3 Security Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-07 | Confidential-class data MUST be encrypted with per-record keys. | Encryption test: Store confidential data → Inspect storage → Verify ciphertext (not plaintext) with per-record key metadata |
| AC-08 | Encryption keys MUST never be stored alongside protected data. | Key separation test: Locate key storage path and data storage path → Verify paths are disjoint |
| AC-09 | All four classification levels (Public, Internal, Confidential, Restricted) MUST be supported with correct encryption. | Classification test: Store data at each level → Verify encryption matches classification requirements |

### 11.4 Performance Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-10 | State persistence MUST complete within 10ms for typical workflow state (≤ 1MB). | Timing test: Persist 1MB state → Measure wall-clock time → Verify ≤ 10ms |
| AC-11 | Checkpoint reads for recovery MUST complete within 50ms. | Recovery timing test: Load checkpoint → Measure read time → Verify ≤ 50ms |
| AC-12 | Storage operations MUST NOT block workflow execution (async writes enforced). | Blocking test: Trigger storage write during workflow execution → Verify workflow continues without waiting for storage completion |## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |