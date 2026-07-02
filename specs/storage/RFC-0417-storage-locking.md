# RFC-0417: Storage Locking

RFC: RFC-0417
Title: Storage Locking
Status: Accepted
Category: Standard
Owner: Storage Team
Authors: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADS Version: 1.0.0
Spec Version: 0.1.0
Normative: YES
Depends On:
  - RFC-0401 Storage Overview
  - RFC-0402 Storage Architecture
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0010 Contract-First Specification
Related JSON Schema:
  - schemas/storage/locking.json
Related Catalog:
  - catalog/storage-locking.md
Layer: Core
Audience: Storage developers, architects, specification reviewers
Target Release: 1.0.0
Review Cycle: Quarterly
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas implementation MUST conform to the locking model, lock acquisition protocols, deadlock prevention strategies, and lock granularity requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---

## Authority
This RFC is the authoritative specification for the Storage Locking domain.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301.

| Term | Definition | Source |
|---|---|---|
| Lock | A concurrency control mechanism that serializes access to shared resources. | RFC-0417 |
| Lock Granularity | The scope of a lock, from individual resources to entire storage domains. | RFC-0417 |
| Deadlock | A situation where two or more operations are each waiting for a lock held by another. | RFC-0417 |
| Optimistic Locking | A locking strategy that assumes conflicts are rare and validates at commit time. | RFC-0417 |
| Pessimistic Locking | A locking strategy that acquires locks before operations to prevent conflicts. | RFC-0417 |
| Lock Timeout | The maximum time to wait for lock acquisition before failing. | RFC-0417 |
| Resource | A unit of data managed by Storage, identified by a unique resource identifier. | RFC-0401 |
| Workflow | A declarative directed graph specification expressing WHAT must happen, not HOW. | RFC-0301 |
| Execution | The process of evaluating a workflow graph and activating nodes to produce results. | RFC-0303 |
 RFC-0301 |
| Task | An atomic unit of work within a workflow, represented as a node. | RFC-0301 |
| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |
| Context | The scoped data environment available to nodes during execution. | RFC-0307 |
| Frame | A discrete unit of visual data processed by vision nodes. | RFC-0301 |
| Tick | A single evaluation cycle of the workflow scheduler. | RFC-0301 |
| Scheduler | The component that determines WHEN and WHERE each node is executed. | RFC-0312 |
| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |

---

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and RFC-0401.

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Lock Types](#4-lock-types)
5. [Lock Protocol](#5-lock-protocol)
6. [Deadlock Prevention](#6-deadlock-prevention)
7. [Lock Escalation](#7-lock-escalation)
8. [Lock Timeout](#8-lock-timeout)
9. [Lock Granularity](#9-lock-granularity)
10. [Acceptance Criteria](#10-acceptance-criteria)
11. [References](#11-references)
12. [Future Evolution](#12-future-evolution)

---


## 2 Goals

1. **Mutual Exclusion**: Write locks prevent concurrent modifications to the same resource.
2. **Deadlock Freedom**: The locking protocol MUST prevent or detect deadlocks.
3. **Minimal Contention**: Locks MUST be held for the shortest duration necessary.
4. **Granularity Control**: Locks MUST support multiple granularity levels.
5. **Timeout Enforcement**: Locks MUST have maximum hold times.

---

- RFC-0324 Workflow Storage


## 4 Lock Types

### 4.1 Lock Categories

| Type | Description | Shared | Compatible With |
|---|---|---|---|
| Read (S) | Shared lock for reading | Yes | Read locks |
| Write (X) | Exclusive lock for writing | No | Nothing |
| Intent Read (IS) | Indicates intention to acquire read lock | Yes | All locks |
| Intent Write (IX) | Indicates intention to acquire write lock | No | Read, IS |
| Update (U) | Reserved lock for update preparation | No | Read, IS, U |

### 4.2 Lock Compatibility Matrix

| | S | IX | U | X |
|---|---|---|---|---|
| S | Compatible | Compatible | Compatible | Incompatible |
| IX | Compatible | Compatible | Compatible | Incompatible |
| U | Compatible | Compatible | Compatible | Incompatible |
| X | Incompatible | Incompatible | Incompatible | Incompatible |

---

- Establishing the relationship between locking and transaction isolation.


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

---

## Security

This specification defines security requirements for locking:

- **Lock Integrity**: Lock state MUST be tamper-evident. Unauthorized lock modifications MUST be detected.
- **Lock Audit Trail**: All lock acquisitions, releases, and timeouts MUST be recorded in the audit log.

---

## Performance

This specification defines performance requirements for locking:

- **Lock Acquisition Latency**: Lock acquisition MUST complete within bounded time under normal contention.
- **Deadlock Detection Time**: Deadlocks MUST be detected within defined time bounds.
- **Lock Contention Overhead**: Locking MUST not degrade throughput beyond acceptable thresholds under normal contention.

---

## Compatibility

This specification defines compatibility requirements:

- **Lock Protocol Stability**: Lock acquisition and release protocols MUST remain stable within a major version.
- **Granularity Compatibility**: Lock granularity semantics MUST remain consistent across minor versions.

---

## Compliance

This specification requires compliance with:

- The Atlas Development System (ADS) Constitution.
- ADR-0010 (Contract-First Specification-Driven Development).
- ADR-0012 (Security Architecture).
- All normative requirements defined in this RFC and its dependent RFCs.

---

## Future Evolution

Future specifications will address:
- **Adaptive Locking**: Dynamic lock granularity selection based on contention patterns.
- **Lock-Free Algorithms**: Support for lock-free data structures for specific high-throughput workloads.
- **Distributed Lock Coordination**: Standardized lock coordination across distributed Storage deployments.

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

### AC-0417-01: Locking Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Lock acquisition MUST enforce mutual exclusion for the locked scope. | Mutual exclusion test. |
| AC-02 | Deadlocks MUST be detected and resolved automatically. | Deadlock detection test. |
| AC-03 | Lock timeouts MUST expire within defined tolerances. | Timeout verification test. |
| AC-04 | Lock state MUST be tamper-evident. | Tamper detection test. |
| AC-05 | Lock operations MUST be recorded in the audit log. | Audit log verification test. |
| AC-06 | Lock contention MUST not degrade throughput beyond acceptable thresholds. | Contention performance test. |

---

## References

| Reference | Description |
|---|---|
| RFC-0401 | Storage Overview |
| RFC-0402 | Storage Architecture |
| RFC-0406 | Storage Transactions |
| RFC-0410 | Storage Cache |
| RFC-0416 | Storage Consistency |
| RFC-0418 | Storage Replication |
| ADR-0010 | Contract-First Specification |
| ADR-0012 | Security Architecture |
| schemas/storage/locking.json | Locking Schema Definition |
| catalog/storage-locking.md | Locking Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |

---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0401, RFC-0402, RFC-0406, RFC-0410, RFC-0416, RFC-0418 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/storage/locking.json |
| Related Catalog | catalog/storage-locking.md |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.0.0 | Accepted | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Security, Performance, Compatibility, Compliance, Runtime Independence, Acceptance Criteria, References, Compliance Matrix, Revision History |




