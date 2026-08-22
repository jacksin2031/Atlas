# RFC-0006: Runtime State Management

RFC: RFC-0006
Title: Runtime State Management
Status: Frozen
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-27
Last Updated: 2026-06-30
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
Required By:
  - RFC-0008 Runtime Plugin Host
  - RFC-0009 Runtime Resource Management
  - RFC-0010 Runtime Manifest Specification
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.3 (Central State Store)
Related RFCs:
  - RFC-0001 Runtime Overview
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

---

## Normative Status

## Authority

This RFC is the authoritative specification for the domain defined in this document.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Runtime | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | Glossary |
| Service | A modular system component registered with the Service Registry. | Glossary |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | Glossary |

---
This specification is Normative. Every Atlas Runtime implementation MUST conform to the state scopes, transaction boundaries, snapshot formats, and persistence interfaces defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---



## Layer Boundaries

### Responsibilities

This specification IS responsible for:

- Defining the architectural contract for this domain.
- Specifying behavioral requirements that all implementations MUST satisfy.
- Establishing extension points and their contracts.

### Non-Responsibilities

This specification IS NOT responsible for:

- Implementation details (see related RFCs for implementation guidance).
- Runtime platform specifics.
- User-facing UI behavior.

### Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview — foundational runtime architecture |

### Consumers

- See related RFCs for consumer listings.

### Providers

- This specification provides domain-specific contracts and behavioral models.

### Forbidden Dependencies

- This specification MUST NOT depend on any specific programming language.
- This specification MUST NOT depend on any specific storage backend.
- This specification MUST NOT depend on any specific operating system.
## Table of Contents
1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [State Philosophy](#4-state-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [State Isolation and Segregation](#8-state-isolation-and-segregation)
9. [Transaction Boundaries](#9-transaction-boundaries)
10. [Write-Ahead Logging and Rollbacks](#10-write-ahead-logging-and-rollbacks)
11. [Snapshotting and Restoration](#11-snapshotting-and-restoration)
12. [Transactional Mutation Sequence](#12-transactional-mutation-sequence)
13. [State Replication and Synchronization](#13-state-replication-and-synchronization)
14. [Conflict Resolution and State Versioning](#14-conflict-resolution-and-state-versioning)
15. [Persistence Contracts](#15-persistence-contracts)
16. [Security and Memory Isolation](#16-security-and-memory-isolation)
17. [Performance Budgets](#17-performance-budgets)
18. [Exposed State Manager APIs](#18-exposed-state-manager-apis)
19. [Normative Contracts](#19-normative-contracts)
20. [Compliance Checklist](#20-compliance-checklist)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [References](#22-references)
23. [Changelog](#23-changelog)
24. [Compatibility](#24-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Transaction Isolation**: State mutations MUST be isolated and atomic. If a step fails, the State Manager MUST execute a clean rollback.
- **Strict Scope Boundaries**: State spaces (Global, Workspace, Project, Workflow, Plugin, Node) MUST be segregated in memory to prevent access boundary bleed.
- **Non-blocking Snapshots**: Periodic state snapshots MUST compile and commit to disk without blocking the main event loop.
- **Traceable History**: Every state mutation MUST be recorded in a transaction log with matching Correlation IDs and Trace IDs.
- **Conflict Resolution**: The system MUST deploy deterministic policies (such as Last-Write-Wins or Vector Clocks) to resolve concurrent state updates.

---



## 4 State Philosophy

1. **Transactions are Immutable**: Commits write new states rather than mutating historical references.
2. **Single Writer, Multi Reader**: Only authorized engines may write to specific scopes; readers consume snapshot logs.
3. **No Private State**: Services MUST NOT maintain hidden states that affect workflow routing.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **State Management may communicate with**:
  - Event Bus (refer to RFC-0005)
  - Storage Manager
  - Service Registry (refer to RFC-0003)
- **State Management MUST NOT communicate with**:
  - Plugins directly (refer to RFC-0008)
  - UI templates directly

---



## 8 State Isolation and Segregation

### 8.1 State Scopes

The State Manager enforces the following scope hierarchy:

| Scope | Level | Description | Access |
|---|---|---|---|
| Global | 0 | Runtime-wide configuration | All services |
| Workspace | 1 | Workspace-level state | Workspace owner |
| Project | 2 | Project-level state | Project members |
| Workflow | 3 | Workflow execution state | Workflow engine |
| Plugin | 4 | Plugin-specific state | Plugin sandbox |
| Node | 5 | Individual node state | Node executor |

### 8.2 Scope Enforcement

Cross-scope access is prohibited. A service operating in the Plugin scope MUST NOT read or write to the Global scope. Scope violations result in a ScopeAccessError.

---

- Defining the architecture and requirements for this subsystem.


## 10 Write-Ahead Logging and Rollbacks

### 10.1 WAL Structure

Every state mutation is recorded in the Write-Ahead Log before being applied to the state store:

`
WAL Entry:
  - sequence_number: Monotonically increasing integer
  - timestamp: Monotonic clock timestamp
  - scope: State scope being modified
  - operation: INSERT, UPDATE, DELETE
  - key: State key being modified
  - value: New state value (serialized)
  - correlation_id: Event correlation identifier
  - trace_id: Distributed trace identifier
  - checksum: CRC32 of the entry
`

### 10.2 Rollback Procedure

When a transaction fails:

1. The State Manager identifies the last committed sequence number.
2. All WAL entries after the committed sequence number are discarded.
3. The state store is reverted to the last consistent snapshot.
4. A StateRollbackEvent is published to the Event Bus.

---

    "project": { "key": "value" }
  },
  "checksum": "sha256:abc123..."
}
`

### 11.3 Restoration

Restoration from a snapshot:

1. Load the snapshot file and verify its checksum.
2. Replay WAL entries from the snapshot sequence number.
3. Validate the resulting state for consistency.
4. Commit the restored state.

---

        TM->>Caller: throw TransactionException
    end
    TM->>TM: releaseLock(scope)
`

---


## 14 Conflict Resolution and State Versioning

### 14.1 Conflict Detection

Conflicts are detected using optimistic concurrency control:

1. Each state key has a version counter.
2. Transactions read the version at the start.
3. On commit, the current version is compared to the read version.
4. If versions differ, a ConflictDetected error is raised.

### 14.2 Conflict Resolution Policies

| Policy | Description | Use Case |
|---|---|---|
| Last-Write-Wins | The most recent write wins | Configuration updates |
| Vector Clocks | Merge based on causal ordering | Collaborative state |
| Manual | Operator resolves conflict | Critical state data |
| Abort | Transaction is aborted | Simple workflows |

---


---



## 17 Performance Budgets

| Metric | Target Budget Limit | Measurement Context |
|---|---|---|
| Read Operation | 0.5 ms | Single key read within scope |
| Write Operation | 1.0 ms | Single key write within transaction |
| Snapshot Commit | 500 ms | Full snapshot to disk |
| WAL Append | 0.1 ms | Single WAL entry append |
| Conflict Detection | 0.05 ms | Version comparison on commit |

---

`

---


## 20 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| ST-01 | Transactions are atomic | Transaction rollback test |
| ST-02 | WAL is written before state commit | WAL ordering test |
| ST-03 | Snapshots include valid checksums | Checksum verification test |
| ST-04 | Scope boundaries are enforced | Cross-scope access test |
| ST-05 | Conflict detection works correctly | Concurrent write test |
| ST-06 | State restoration from snapshot succeeds | Snapshot restore test |

---

- **Expected Result**: One transaction succeeds, the other receives ConflictDetected.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 23 Changelog
- 1.0.0: Initial release. Defined transaction scopes and snapshotting.
- 1.1.0: Expanded all placeholder sections with full architecture, WAL, snapshots, and compliance checklist.

---


| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

---

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

---

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Frozen | 2026-06-30 | Runtime Architecture Board | Initial publication |
| 1.1.0 | Frozen | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






