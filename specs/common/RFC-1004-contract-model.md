# RFC-1004: Common Contract Model

RFC: RFC-1004
Title: Common Contract Model
Status: Draft
Version: 0.1.0
Author: Atlas Specification Committee
Created: 2026-06-30
Depends On:
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Common
Layer: Cross-Cutting
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Related RFCs:
  - RFC-0013 Runtime Contracts
Target Release: 1.0.0
Last Updated: 2026-06-30

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the contract model defined in this document.

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
3. [Contract Model](#3-contract-model)
4. [Contract Interface](#4-contract-interface)
5. [Contract Versioning](#5-contract-versioning)
6. [Contract Validation](#6-contract-validation)
7. [Performance Budgets](#7-performance-budgets)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [References](#9-references)

---


## 2 Goals

- **Interface Consistency**: All subsystems expose contracts in the same format.
- **Version Compatibility**: Contracts are versioned and backward compatible.
- **Schema Validation**: All contract payloads validate against registered schemas.

---


## 4 Contract Interface

`
interface Contract {
  // Get the contract ID.
  string getContractId();

  // Get the contract version.
  string getVersion();

  // Get all declared methods.
  Method[] getMethods();

  // Get input schema for a method.
  Schema getInputSchema(string methodName);

  // Get output schema for a method.
  Schema getOutputSchema(string methodName);

  // Get declared error types.
  ErrorType[] getErrorTypes();
}
`

---



## 6 Contract Validation

All contract implementations MUST pass:
1. Schema validation against declared schemas.
2. Method signature verification.
3. Error type coverage check.

---



## 8 Acceptance Criteria

### AC-1010
- **Requirement**: All contracts MUST conform to the Contract interface (Section 4).
- **Verification**: Inspect all contract implementations.
- **Expected Result**: Zero non-conforming contracts.

### AC-1011
- **Requirement**: All contract methods MUST have input and output schemas.
- **Verification**: Scan all contract declarations.
- **Expected Result**: Every method has both schemas.

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
| 0.1.0 | Draft | 2026-07-01 | Spec Committee | Initial publication |
| 0.2.0 | Draft | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






