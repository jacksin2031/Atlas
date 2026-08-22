# RFC-1002: Common State Model

RFC: RFC-1002
Title: Common State Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0006 Runtime State Management
Supersedes: None
Superseded By: None
Category: Common
Layer: Cross-Cutting
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0010
  - ADR-0012
Related RFCs:
  - RFC-0006 Runtime State Management
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the state model defined in this document. This is the single source of truth for state structure across ALL subsystems.

---

## Authority

This RFC is the authoritative specification for the common event model. All subsystems MUST reference this document when defining domain-specific events.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Event | A discrete occurrence within the system that may trigger state changes or notifications. | Glossary |
| Event Bus | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| Dead Letter Queue (DLQ) | A dedicated message queue containing events that could not be delivered to their target subscribers. | Glossary |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | Glossary |

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
4. [State Model](#4-state-model)
5. [State Scopes](#5-state-scopes)
6. [State Keys](#6-state-keys)
7. [State Transactions](#7-state-transactions)
8. [State Versioning](#8-state-versioning)
9. [State Persistence](#9-state-persistence)
10. [Cross-Subsystem State Mapping](#10-cross-subsystem-state-mapping)
11. [Performance Budgets](#11-performance-budgets)
12. [Acceptance Criteria](#12-acceptance-criteria)
13. [References](#13-references)

---


## 2 Goals

- **Universal Consistency**: All subsystems use the same state structure.
- **Scope Isolation**: State is strictly partitioned by scope.
- **Transaction Safety**: All state mutations are atomic.
- **Cross-Subsystem Visibility**: State can be queried across subsystem boundaries.

---



## 4 State Model

Every state in Atlas follows this model:

1. **Scoped**: State lives in a named scope (e.g., untime, workflow, ision).
2. **Keyed**: State is accessed by a hierarchical key (e.g., workflow/task_001/status).
3. **Typed**: State values have a type (string, integer, boolean, object, array).
4. **Versioned**: Each state entry has a version number.
5. **Tracked**: Every mutation is logged with a sequence number.

---

- Implementation details.


## 6 State Keys

Keys follow the pattern: {scope}/{entity}/{id}/{attribute}

| Example | Scope | Entity | ID | Attribute |
|---|---|---|---|---|
| untime/state/version | runtime | state | version | — |
| workflow/task_001/status | workflow | task | task_001 | status |
| ision/capture/frame_count | vision | capture | frame_count | — |
| plugin/my_plugin/config | plugin | my_plugin | config | — |

---


## 8 State Versioning

Each state entry has a monotonically increasing version:

| Field | Type | Description |
|---|---|---|
| ersion | integer | Monotonically increasing version number |
| modified_at | timestamp | Last modification timestamp |
| modified_by | string | Source subsystem that modified |
| checksum | string | SHA-256 of the value |

---

| RFC-0001 | Consumed | Runtime Overview |


## 10 Cross-Subsystem State Mapping

States flow between subsystems via the State Manager:

| Source | Target | State |
|---|---|---|
| Runtime → Workflow | untime/state/version → Workflow reads |
| Workflow → State | workflow/task_001/status → State Manager writes |
| Vision → Workflow | ision/capture/frame_count → Workflow reads |

---

| RFC-0001 | Consumed | Runtime Overview |


## 12 Acceptance Criteria

### AC-1005
- **Requirement**: All state keys MUST follow the naming convention (Section 6).
- **Verification**: Scan all state keys across subsystems.
- **Expected Result**: Zero violations.

### AC-1006
- **Requirement**: All state mutations MUST occur within transactions.
- **Verification**: Audit state write paths.
- **Expected Result**: All writes wrapped in begin/commit or begin/rollback.

### AC-1007
- **Requirement**: State versions MUST be monotonically increasing.
- **Verification**: Check version ordering on every mutation.
- **Expected Result**: No version decreases observed.

---

## Compliance Matrix

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

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 0.1.0 | Draft | 2026-07-01 | Spec Committee | Initial publication |
| 0.2.0 | Draft | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






