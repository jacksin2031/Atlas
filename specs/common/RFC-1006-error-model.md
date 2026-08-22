# RFC-1006: Common Error Model

RFC: RFC-1006
Title: Common Error Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0011 Runtime Error Taxonomy
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
  - RFC-0011 Runtime Error Taxonomy
Target Release: 1.0.0
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the error model defined in this document.

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
2. [Error Model](#2-error-model)
3. [Error Classification](#3-error-classification)
4. [Error Code Registry](#4-error-code-registry)
5. [Error Payload](#5-error-payload)
6. [Error Escalation](#6-error-escalation)
7. [Performance Budgets](#7-performance-budgets)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [References](#9-references)

---


## 2 Error Model

Every error has:
- errorCode: Standardized error code (e.g., ERR_RUNTIME_TIMEOUT).
- category: Error category (e.g., 	imeout, alidation, esource).
- severity: Error severity (ecoverable, atal, critical).
- source: Subsystem that generated the error.
- context: Additional error context.
- 	raceId: Distributed trace identifier.

---


## 4 Error Code Registry

Error codes follow the pattern: ERR_{CATEGORY}_{SUBSYSTEM}_{DETAIL}

| Code | Category | Subsystem | Detail |
|---|---|---|---|
| ERR_TIMEOUT_RUNTIME_BOOT | timeout | runtime | boot |
| ERR_VALIDATION_MANIFEST_SCHEMA | validation | manifest | schema |
| ERR_RESOURCE_MEMORY_EXHAUSTED | resource | runtime | memory_exhausted |
| ERR_NETWORK_CONNECTION_LOST | network | ipc | connection_lost |
| ERR_AUTH_PERMISSION_DENIED | authentication | plugin | permission_denied |
| ERR_CONFIG_MISSING_CAPABILITY | configuration | capability | missing_capability |
| ERR_STATE_WAL_CORRUPT | state | state | wal_corrupt |
| ERR_PLUGIN_SANDBOX_CRASH | plugin | plugin | sandbox_crash |
| ERR_WORKFLOW_NODE_INVALID | workflow | workflow | node_invalid |
| ERR_VISION_CAPTURE_FAILED | vision | vision | capture_failed |
| ERR_AI_MODEL_LOAD_TIMEOUT | ai | ai | model_load_timeout |

---

- Defining the canonical model for this cross-cutting concern.
- Providing the authoritative definition consumed by all subsystem RFCs.


## 6 Error Escalation

| Severity | Action | Escalation |
|---|---|---|
| Recoverable | Retry with backoff | Subsystem self-heal |
| Fatal | Rollback state, halt subsystem | Runtime supervisor |
| Critical | Full shutdown, crash dump | OS supervisor |

---



## 8 Acceptance Criteria

### AC-1014
- **Requirement**: All errors MUST include errorCode, category, severity, and traceId.
- **Verification**: Audit error payloads.
- **Expected Result**: Zero missing fields.

### AC-1015
- **Requirement**: Error codes MUST follow the naming convention (Section 4).
- **Verification**: Scan all error code declarations.
- **Expected Result**: All match ERR_{CATEGORY}_{SUBSYSTEM}_{DETAIL}.

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







