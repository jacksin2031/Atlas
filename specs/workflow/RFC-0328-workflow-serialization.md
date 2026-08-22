RFC: RFC-0328

Title: Workflow Serialization

Status: Proposed

Version: 1.0.0

Author: Atlas Specification Committee

## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Serializer | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Deserializer | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Serialization Format | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Schema | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Encoding | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Decoding | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Payload | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Message Pack | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Binary Format | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Text Format | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Streaming Serialization | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Batch Serialization | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---

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

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

  - RFC-0325 Workflow AI

  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC


  - RFC-0329 Workflow Compatibility

  - RFC-0330 Workflow Compliance

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x



Related ADR:

  - ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema:

  - schemas/workflow/serialization-format.json

Related Catalog:

  - catalog/workflow-state-types.md

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Serialization specification defines the serialization model for Atlas workflows. Serialization enables workflow definitions and execution state to be persisted, transferred, and restored.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0328 workflow serialization.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 2 Serialization Overview



Key principles:



- Workflow definitions are serializable to a canonical form.

- Execution state is serializable for checkpointing.

- Serialization is version-aware and compatible.

- Serialized workflows are portable across implementations.



---



## 3 Serialization Formats



| Format | Description | Use Case |

|---|---|---|

| Canonical | Canonical representation for comparison | Validation, versioning |

| Exchange | Exchange format for portability | Cross-platform transfer |

| Checkpoint | Checkpoint format for recovery | State persistence |

| Archive | Archive format for distribution | Distribution, storage |



---



## 4 Serialization Constraints



| Constraint | Description |

|---|---|

| Version Awareness | Serialized data includes version information |

| Integrity | Serialized data includes checksums |

| Compression | Serialized data MAY be compressed |

| Encryption | Serialized sensitive data MAY be encrypted |



---



## 5 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | Four serialization formats MUST be supported. | Format enumeration test |

| AC-02 | Four serialization constraints MUST be enforced. | Constraint test |



---



## 6 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview |

| RFC-0315 | Workflow Recovery |



---



## 5 Terminology



| Term | Definition | Source |

|---|---|---|

| Serialization | The process of converting a workflow definition or execution state into a storable/transmittable format. | RFC-0301 |

| Deserialization | The reverse process of reconstructing a workflow definition or state from serialized form. | RFC-0301 |

| Canonical Form | A normalized representation of a workflow definition that is identical for semantically equivalent definitions. | This RFC |

| Checkpoint | A serialized snapshot of workflow execution state used for recovery. | RFC-0315 |

| Integrity Checksum | A cryptographic hash used to detect unauthorized modification of serialized data. | This RFC |



## 6 Layer Boundaries



### 6.1 Responsibilities

This specification IS responsible for: defining serialization formats, version-aware serialization, integrity verification, and cross-implementation portability guarantees.



### 6.2 Non-Responsibilities

This specification IS NOT responsible for: implementing specific serialization libraries, managing storage backends (RFC-0324), or defining wire protocols (RFC-0327).



### 6.3 Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0304 | Consumed | Workflow Runtime consumes serialized definitions |

| RFC-0315 | Consumed | Workflow Recovery uses checkpoint serialization |

| RFC-0317 | Consumed | Workflow Validation uses canonical forms |

| RFC-0324 | Consumed | Workflow Storage persists serialized data |



### 6.4 Consumers

- Workflow Runtime (RFC-0304): Deserializes workflow definitions for execution.

- Workflow Recovery (RFC-0315): Deserializes checkpoints for state restoration.

- Workflow Validation (RFC-0317): Compares canonical forms for equality.



### 6.5 Providers

- Serialization Format Schema (schemas/workflow/serialization-format.json): Provides the format contract.



### 6.6 Forbidden Dependencies

- This specification MUST NOT depend on any language-specific serialization library (pickle, json.Marshal, serde).

- This specification MUST NOT assume a particular encoding (UTF-8, ASCII, binary).



## 7 Security

- Serialized workflow definitions MUST include integrity checksums.

- Serialized data containing secrets MUST be encrypted.

- Deserialization of untrusted workflow definitions MUST occur in a sandbox (RFC-0319).



## 8 Performance

- Serialization of a typical workflow definition (up to 100 nodes) MUST complete within 50ms.

- Deserialization MUST complete within 50ms for the same definition size.

- Canonical form computation MUST be deterministic and idempotent.



## 9 Compatibility

- Serialization formats MUST be versioned and backward compatible within a major version.

- New serialization formats MAY be introduced alongside existing ones during a transition period.



## 10 Compliance

- All serialized workflow definitions MUST include version metadata for compliance tracking (RFC-0330).



## 11 Future Evolution

- **Schema Registry**: Centralized schema version registry for cross-implementation compatibility.

- **Incremental Serialization**: Support for serializing only changed portions of workflow state.

- **Streaming Serialization**: Support for streaming serialization of very large workflow definitions.

- **Compression Profiles**: Standardized compression profiles for bandwidth-constrained environments.



## 12 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)

- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)

- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)

- Any operating system (Windows, Linux, macOS, etc.)

- Any hardware architecture (CPU, GPU, FPGA, etc.)

- Any threading model (single-threaded, multi-threaded, actor-based, etc.)



## 13 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (canonical terminology source) |

| RFC-0304 | Workflow Runtime (definition deserialization) |

| RFC-0315 | Workflow Recovery (checkpoint serialization) |

| RFC-0317 | Workflow Validation (canonical form comparison) |

| RFC-0319 | Workflow Security (serialization security) |

| RFC-0320 | Workflow Performance (serialization performance) |

| RFC-0324 | Workflow Storage (serialized data persistence) |

| RFC-0327 | Workflow IPC (serialized message transmission) |

| RFC-0329 | Workflow Compatibility (format compatibility) |

| RFC-0330 | Workflow Compliance (version metadata) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/serialization-format.json | Serialization Format JSON Schema |

| catalog/workflow-state-types.md | State Type Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0328 (this document), RFC-0324 (Storage), RFC-0315 (Recovery) |
---

## Revision History

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
