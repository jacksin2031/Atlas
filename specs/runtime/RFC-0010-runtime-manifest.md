# RFC-0010: Runtime Manifest Specification

RFC: RFC-0010
Title: Runtime Manifest Specification
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
  - RFC-0005 Runtime Event Bus
Required By:
  - RFC-0012 Runtime Capability Registry
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0012
  - ADR-0014
Constitution References:
  - Section 1.2 (Bootstrap Manifest)
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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the manifest schemas, capability registration blocks, loading protocols, and version negotiation rules defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0012, and ADR-0014.

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
4. [Manifest Philosophy](#4-manifest-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Manifest System Architecture](#8-manifest-system-architecture)
9. [Standard Manifest Schema](#9-standard-manifest-schema)
10. [Capabilities Discovery Registration](#10-capabilities-discovery-registration)
11. [Version Negotiation Protocols](#11-version-negotiation-protocols)
12. [Manifest Loading Sequence](#12-manifest-loading-sequence)
13. [Capability Discovery Diagram](#13-capability-discovery-diagram)
14. [Version Negotiation Flowchart](#14-version-negotiation-flowchart)
15. [API Fallback Policies](#15-api-fallback-policies)
16. [Security and Verification Gates](#16-security-and-verification-gates)
17. [Performance Budgets](#17-performance-budgets)
18. [Exposed Manifest APIs](#18-exposed-manifest-apis)
19. [Normative Contracts](#19-normative-contracts)
20. [Compliance Checklist](#20-compliance-checklist)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [References](#22-references)
23. [Changelog](#23-changelog)
24. [Compatibility](#24-compatibility)

---

- Downstream subsystem RFCs.


## 2 Goals

- **Configuration Validation**: The manifest file MUST validate against JSON Schema specs before initialization.
- **Dynamic Capability Discovery**: The Runtime MUST expose active capabilities (e.g., Vision, OCR, GPU acceleration) in a queryable state block.
- **Strict Version Negotiation**: Third-party plugins and workflows MUST perform version negotiation gates before loading.
- **Fail-Safe Fallbacks**: If required capabilities are unsupported, the loading process MUST halt safely, returning a CapabilityUnsupported warning.
- **Backward Compatibility Mapping**: Manifests MUST define a compatibility matrix showing supported legacy versions.

---



## 4 Manifest Philosophy

1. **Manifest is Immutable**: The manifest configuration is locked at boot.
2. **Contract-First Validation**: Changes to manifest formats require schema updates.
3. **Universally Queryable**: The Capability map is queryable via standard service registry interfaces.

---

| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Manifest Specification may communicate with**:
  - State Manager (refer to RFC-0006)
  - Config Manager
  - Service Registry (refer to RFC-0003)
- **Manifest Specification MUST NOT communicate with**:
  - External package repositories
  - Remote client interfaces

---



## 8 Manifest System Architecture

The Manifest System consists of three components: the Manifest Parser, the Schema Validator, and the Capability Registry.

`mermaid
graph TD
    MF[Manifest File] --> MP[Manifest Parser]
    MP --> SV[Schema Validator]
    SV --> CR[Capability Registry]
    CR --> SM[State Manager]
    CR --> SR[Service Registry]
    SV --> ER[Error Reporter]
`

### 8.1 Manifest Parser

The Manifest Parser reads the manifest file and converts it into an internal representation. It supports:
- **JSON**: Primary manifest format.
- **YAML**: Alternative manifest format (parsed to JSON internally).

### 8.2 Schema Validator

The Schema Validator checks the parsed manifest against the registered JSON Schema. Invalid manifests cause boot failure.

### 8.3 Capability Registry

The Capability Registry populates the system capability map from the manifest declarations. This map is queried by the Capability Registry (refer to RFC-0012).

---

    },
    "plugins": {
      "type": "array",
      "items": { "type": "string" }
    },
    "resource_limits": {
      "type": "object",
      "properties": {
        "max_memory_mb": { "type": "integer" },
        "max_cpu_cores": { "type": "integer" },
        "max_vram_mb": { "type": "integer" }
      }
    },
    "compatibility": {
      "type": "object",
      "properties": {
        "minimum_runtime_version": { "type": "string" },
        "maximum_runtime_version": { "type": "string" }
      }
    }
  }
}
`

---


## 12 Manifest Loading Sequence

The following sequence details how a manifest is loaded and validated:

`mermaid
sequenceDiagram
    autonumber
    participant LM as Load Manager
    participant FS as File System
    participant MP as Manifest Parser
    participant SV as Schema Validator
    participant CR as Capability Registry
    participant EB as Event Bus

    LM->>FS: read(manifest_file)
    FS-->>LM: manifest_bytes
    LM->>MP: parse(manifest_bytes)
    MP-->>LM: manifest_object
    LM->>SV: validate(manifest_object, schema)
    alt Validation Success
        SV-->>LM: valid
        LM->>CR: registerCapabilities(capabilities)
        LM->>EB: publish(ManifestLoaded)
    else Validation Failure
        SV-->>LM: ValidationError
        LM->>EB: publish(ManifestLoadFailed)
        LM->>LM: abort_boot()
    end
`

---

    AReg --> Done
    ASkip --> Done
    GReg --> Done
    GSkip --> Done
`

---



## 15 API Fallback Policies

When a capability is unavailable, the Runtime applies the following fallback policies:

| Capability | Fallback Behavior |
|---|---|
| Vision | Skip vision-dependent workflow nodes |
| OCR | Use alternative text extraction method |
| AI Inference | Queue requests for cloud provider |
| GPU Acceleration | Fall back to CPU computation |
| Screen Capture | Display error to user |

---

This specification IS NOT responsible for:
- Implementation details.


## 17 Performance Budgets

| Metric | Target Budget Limit | Measurement Context |
|---|---|---|
| Manifest Parsing | 50 ms | Full manifest file parse |
| Schema Validation | 100 ms | Full manifest validation |
| Capability Probe | 200 ms | Probe all declared capabilities |
| Version Negotiation | 10 ms | Compute common version range |
| Signature Verification | 50 ms | Cryptographic signature check |

---



## 19 Normative Contracts

- Every manifest MUST conform to the standard manifest schema (Section 9).
- Every capability declaration MUST include an enabled flag and a required flag.
- Version negotiation MUST follow the protocol defined in Section 11.
- Manifest signatures MUST use RSA-2048 or stronger algorithms.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 21 Acceptance Criteria

### AC-101
- **Requirement**: Manifest MUST validate against JSON Schema before boot.
- **Verification**: Load a manifest with an invalid capability declaration.
- **Expected Result**: Boot is aborted with a ValidationError.

### AC-102
- **Requirement**: Missing required capabilities MUST prevent boot.
- **Verification**: Declare a required capability that is unavailable.
- **Expected Result**: Boot fails with CapabilityUnsupported error.

### AC-103
- **Requirement**: Version negotiation MUST reject major version mismatches.
- **Verification**: Connect a v2 client to a v1 server.
- **Expected Result**: Connection is rejected with VersionMismatchError.

### AC-104
- **Requirement**: Capability fallback MUST be applied for optional capabilities.
- **Verification**: Declare an optional GPU capability that is unavailable.
- **Expected Result**: Runtime falls back to CPU computation without error.

### AC-105
- **Requirement**: Manifest loading MUST complete within the performance budget.
- **Verification**: Load a manifest with 50 capabilities and 10 plugins.
- **Expected Result**: Total load time is less than 500 ms.

---



## 23 Changelog
- 1.0.0: Initial release. Defined Manifest validation schemas and loading.
- 1.1.0: Expanded all placeholder sections with full architecture, schema, and compliance checklist.

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
| 1.0.0 | Frozen | 2026-06-30 | Runtime Architecture Board | Initial publication |
| 1.1.0 | Frozen | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence per RFC_TEMPLATE.md |






