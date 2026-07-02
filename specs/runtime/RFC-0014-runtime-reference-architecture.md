# RFC-0014: Runtime Reference Architecture

RFC: RFC-0014
Title: Runtime Reference Architecture
Status: Frozen
Version: 1.0.0
Author: Atlas Team
Created: 2026-06-30
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-0007 Runtime IPC Architecture
  - RFC-0008 Runtime Plugin Host
  - RFC-0009 Runtime Resource Management
  - RFC-0010 Runtime Manifest Specification
  - RFC-0011 Runtime Error Taxonomy
  - RFC-0012 Runtime Capability Registry
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Reference
Normative: YES
Audience: All Developers and Reviewers
ADR References:
  - ADR-0001
  - ADR-0002
  - ADR-0010
  - ADR-0012
Related RFCs:
  - All Runtime RFCs (RFC-0001 through RFC-0013)
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
This specification is Normative. It provides the authoritative visual reference architecture for the Atlas Runtime. All implementations MUST be consistent with the diagrams and models defined herein.

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
2. [Block Architecture Diagram](#2-block-architecture-diagram)
3. [Layer Diagram](#3-layer-diagram)
4. [Dependency Graph](#4-dependency-graph)
5. [Data Flow Diagram](#5-data-flow-diagram)
6. [Thread Model Diagram](#6-thread-model-diagram)
7. [Sequence Diagrams](#7-sequence-diagrams)
8. [Security Model Diagram](#8-security-model-diagram)
9. [Performance Model](#9-performance-model)
10. [References](#10-references)

---


## 2 Block Architecture Diagram

`mermaid
graph TB
    subgraph HostProcess["Host Process: Atlas Runtime"]
        subgraph CoreLayer["Core Layer"]
            SM[State Machine]
            SR[Service Registry]
            EB[Event Bus]
        end

        subgraph ExecutionLayer["Execution Layer"]
            SCH[Scheduler]
            RES[Resource Manager]
            STM[State Manager]
        end

        subgraph CommunicationLayer["Communication Layer"]
            IPC[IPC Dispatcher]
            SEC[Security Manager]
        end

        subgraph ExtensibilityLayer["Extensibility Layer"]
            PLH[Plugin Host]
            MAN[Manifest Parser]
        end

        subgraph MetadataLayer["Metadata Layer"]
            CAP[Capability Registry]
            ERR[Error Registry]
            CON[Contract Registry]
        end
    end

    subgraph ExternalProcesses["External Processes"]
        UI[UI Dashboard]
        WF[Workflow Engine]
        VIS[Vision Engine]
        AI[AI Engine]
        REC[Recorder]
        PLG1[Plugin A]
        PLG2[Plugin B]
    end

    UI <-->|IPC| IPC
    WF <-->|IPC| SCH
    VIS <-->|IPC| SCH
    AI <-->|IPC| SCH
    PLG1 <-->|WASM| PLH
    PLG2 <-->|WASM| PLH

    SM --> SR
    SM --> SCH
    SM --> PLH
    SR --> EB
    SR --> STM
    SCH --> EB
    RES --> SCH
    STM --> EB
    IPC --> EB
    PLH --> EB
    MAN --> CAP
    CAP --> STM
    ERR --> SM
    CON --> SR
`

---


## 4 Dependency Graph

`mermaid
graph LR
    RFC0001["RFC-0001<br/>Overview"] --> RFC0002["RFC-0002<br/>Lifecycle"]
    RFC0001 --> RFC0003["RFC-0003<br/>Service Model"]
    RFC0002 --> RFC0003
    RFC0003 --> RFC0004["RFC-0004<br/>Scheduler"]
    RFC0003 --> RFC0005["RFC-0005<br/>Event Bus"]
    RFC0002 --> RFC0005
    RFC0004 --> RFC0006["RFC-0006<br/>State Mgmt"]
    RFC0005 --> RFC0006
    RFC0005 --> RFC0007["RFC-0007<br/>IPC"]
    RFC0007 --> RFC0008["RFC-0008<br/>Plugin Host"]
    RFC0006 --> RFC0008
    RFC0006 --> RFC0009["RFC-0009<br/>Resources"]
    RFC0008 --> RFC0009
    RFC0005 --> RFC0010["RFC-0010<br/>Manifest"]
    RFC0002 --> RFC0011["RFC-0011<br/>Errors"]
    RFC0010 --> RFC0012["RFC-0012<br/>Capabilities"]
    RFC0003 --> RFC0013["RFC-0013<br/>Contracts"]
    RFC0011 --> RFC0013
    RFC0008 --> RFC0013
    RFC0009 --> RFC0013
`

---

    EVT --> EB
    CMD --> IPC
    REQ --> IPC
    IPC --> SCH
    SCH --> PLH
    PLH --> STM
    EB --> SCH
    STM --> LOG
    SCH --> RESP
    EB --> PUB
`

---

    end

    TC --> HB
    HB --> REC
    REC --> ESC
    EP --> ER
    ER --> EH
    MC --> MP
`

---

    EB-->>Ext: notify(result)
`

### 7.2 Plugin Load Sequence

`mermaid
sequenceDiagram
    autonumber
    participant PM as Plugin Manager
    participant FS as File System
    participant VM as WASM VM
    participant SR as Service Registry
    participant EB as Event Bus

    PM->>FS: scan(plugin_dir)
    FS-->>PM: manifests[]
    PM->>VM: instantiate(binary)
    VM-->>PM: module_handle
    PM->>VM: initialize(handle)
    VM-->>PM: initialized
    PM->>SR: register(handle)
    PM->>EB: subscribe(hooks)
    EB-->>PM: subscription_confirmed
`

---

    WF -->|Token Auth| IPC
    IPC --> SEC
    SEC -->|Validate| SR

    SM -->|Audit Log| AL[Append-Only Log]
    AL --> STM[State Manager]
`

---


| Resource | Limit |
|---|---|
| Max concurrent workers | 64 |
| Max plugins | 100 |
| Max event queues | 1,000 |
| Max IPC connections | 500 |
| Max memory | 8 GB |
| Max disk I/O | 100 MB/s |

---


This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All contracts in this specification are defined as abstract behavioral interfaces.

---
---

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-001 | The implementation MUST accurately reflect the layered architecture defined across RFC-0001 through RFC-0013. | Architecture review against referenced RFCs. |
| AC-002 | The implementation MUST document all layer boundaries and their interfaces. | Cross-reference diagram with text. |

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







