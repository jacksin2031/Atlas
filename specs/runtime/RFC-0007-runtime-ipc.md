# RFC-0007: Runtime IPC Architecture

RFC: RFC-0007
Title: Runtime IPC Architecture
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
  - RFC-0008 Runtime Plugin Host
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
  - Section 3.5 (IPC Isolation)
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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the IPC transport protocols, message schemas, dispatching structures, contract verifications, and security check gates defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

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
4. [IPC Philosophy](#4-ipc-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [IPC Dispatcher Architecture](#8-ipc-dispatcher-architecture)
9. [Standard Message Schema](#9-standard-message-schema)
10. [Contract Verification Engine](#10-contract-verification-engine)
11. [Communication Paradigms](#11-communication-paradigms)
12. [IPC Dispatch Sequence](#12-ipc-dispatch-sequence)
13. [Packet Validation Flow](#13-packet-validation-flow)
14. [Performance and Throttling](#14-performance-and-throttling)
15. [Security and Access Control](#15-security-and-access-control)
16. [Performance Budgets](#16-performance-budgets)
17. [Exposed IPC APIs](#17-exposed-ipc-apis)
18. [Normative Contracts](#18-normative-contracts)
19. [Compliance Checklist](#19-compliance-checklist)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [References](#21-references)
22. [Changelog](#22-changelog)
23. [Compatibility](#23-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Decoupled Messaging**: Components MUST communicate strictly through serialized IPC channels. Direct DLL binding or shared memory context bypasses are prohibited.
- **Contract Verification**: Every IPC request MUST undergo input and output schema validations.
- **Origin Authentication**: The IPC Dispatcher MUST verify the cryptographic signature and token identity of any calling process.
- **Transport Independence**: The logical packet formats and dispatching mechanics MUST remain independent of the physical transport (e.g., named pipes, TCP sockets, Unix sockets).
- **Graceful Performance Throttling**: The dispatcher MUST support packet compression, message batching, and backpressure controls to prevent connection queues from blocking.

---



## 4 IPC Philosophy

1. **Zero-Trust Message Traversal**: Every message crossing process boundaries is treated as an untrusted input.
2. **Contract First**: IPC schemas are immutable versioned contracts. Invalid payloads trigger immediate drops.
3. **Universally Auditable**: Every message is traced via correlation identifiers.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **IPC Architecture may communicate with**:
  - Event Bus (refer to RFC-0005)
  - Security Manager
  - Service Registry (refer to RFC-0003)
- **IPC Architecture MUST NOT communicate with**:
  - Direct workflow files
  - Direct hardware display interfaces

---



## 8 IPC Dispatcher Architecture

The IPC Dispatcher consists of three layers: the Transport Layer, the Protocol Layer, and the Application Layer.

`mermaid
graph TD
    App1[Application 1] --> TL1[Transport Layer]
    App2[Application 2] --> TL2[Transport Layer]
    TL1 --> PL[Protocol Layer]
    TL2 --> PL
    PL --> CV[Contract Verifier]
    CV --> Auth[Authentication Gate]
    Auth --> Route[Message Router]
    Route --> App1
    Route --> App2
`

### 8.1 Transport Layer

The Transport Layer handles physical message delivery. It supports:
- **Named Pipes**: For local process communication on Windows.
- **Unix Domain Sockets**: For local process communication on Unix-like systems.
- **TCP Sockets**: For remote process communication.

The Transport Layer is transparent to the Protocol Layer and Application Layer.

### 8.2 Protocol Layer

The Protocol Layer handles message framing, serialization, and version negotiation. It wraps application messages in a protocol envelope that includes:
- Message length prefix (for framing).
- Protocol version (for negotiation).
- Message type indicator (request, response, event, stream).

### 8.3 Application Layer

The Application Layer handles business logic routing. It maps commands to target services using the Service Registry (refer to RFC-0003).

---

    }
  }
}
`

---

- Defining the architecture and requirements for this subsystem.


## 11 Communication Paradigms

The IPC Architecture supports four communication paradigms:

| Paradigm | Description | Use Case |
|---|---|---|
| Request-Response | Synchronous call with response | Service method invocation |
| Publish-Subscribe | Asynchronous event distribution | System notifications |
| Streaming | Continuous data flow | Video frame delivery |
| Fire-and-Forget | One-way message, no response | Telemetry logging |

---


---


## 14 Performance and Throttling

### 14.1 Message Batching

The IPC Dispatcher supports message batching for high-throughput scenarios. Batching combines multiple small messages into a single transport frame, reducing per-message overhead.

### 14.2 Compression

Messages exceeding 1 KB MAY be compressed using LZ4 or Zstandard compression before transmission. Decompression is performed on the receiving side.

### 14.3 Throttling

The Dispatcher applies the following throttling rules:

| Rule | Threshold | Action |
|---|---|---|
| Max message size | 1 MB | Drop message |
| Max connections per client | 10 | Reject new connections |
| Max messages per second | 10,000 | Queue excess messages |
| Max queue depth | 100,000 | Apply backpressure |

---

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 17 Exposed IPC APIs

`
interface IPCDispatcher {
  // Send a message to a target service. Returns response or timeout.
  IPCResponse send(IPCRequest request);

  // Publish an event to a channel.
  void publish(IPCEvent event);

  // Subscribe to a channel. Returns SubscriptionHandle.
  SubscriptionHandle subscribe(string channel, IPCEventHandler handler);

  // Close an IPC connection.
  void close(SubscriptionHandle handle);

  // Get connection statistics.
  IPCStats getStats();
}

interface IPCRequest {
  string id;
  string version;
  string source;
  string destination;
  string command;
  object payload;
  IPCMetadata metadata;
}
`

---


## 19 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| IPC-01 | Messages conform to standard schema | Schema validation test |
| IPC-02 | Authentication is enforced | Unauthenticated request test |
| IPC-03 | Oversized messages are dropped | Large message stress test |
| IPC-04 | Version negotiation works correctly | Cross-version communication test |
| IPC-05 | Correlation IDs are preserved | End-to-end trace test |
| IPC-06 | Encryption is applied to confidential channels | Packet inspection test |

---

- **Expected Result**: Connection is rejected with VersionMismatchError.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 22 Changelog
- 1.0.0: Initial release. Defined structures, parameters, and validations.
- 1.1.0: Expanded all placeholder sections with full architecture, validation flow, and compliance checklist.

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






