# RFC-IPC-CAT-IF: IPC Interface Catalog

RFC: IPC-CAT-IF
Title: IPC Interface Catalog
Status: Accepted
Version: 1.0.0
Category: IPC
Layer: Communication
Normative: YES
Authors: Atlas Team
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0007 Runtime IPC Architecture
  - RFC-0101 Runtime Core
  - RFC-0102 Plugin System
  - RFC-0103 Vision Engine
  - RFC-0105 AI Host
  - RFC-0107 Workflow Engine
Required By:
  - All RFCs defining IPC communication between Atlas processes
Supersedes: None
Superseded By: None
Audience: Systems Engineers, IPC Implementers
Constitution References:
  - Section 3.5 (IPC Isolation)
  - Section 4.2 (Process Boundaries)
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status
This specification is Normative. Every Atlas process implementation MUST reference the Interface IDs defined herein for all IPC communication boundaries. Free-text descriptions of IPC endpoints are prohibited in favor of these fixed Interface IDs. Any deviation from this catalog MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and RFC-0007 (Runtime IPC Architecture).

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Interface Registry](#2-interface-registry)
3. [Interface Lifecycle](#3-interface-lifecycle)
4. [Interface Versioning](#4-interface-versioning)
5. [Interface Discovery](#5-interface-discovery)
6. [Interface Security Requirements](#6-interface-security-requirements)
7. [Interface Catalog Usage](#7-interface-catalog-usage)
8. [Cross-References](#8-cross-references)
9. [Glossary](#9-glossary)
10. [Revision History](#10-revision-history)

---

## 1 Introduction

The Atlas platform comprises independent processes operating within separate memory contexts. Each process communicates exclusively through the Inter-Process Communication (IPC) infrastructure defined in RFC-0007. This Interface Catalog establishes a fixed, versioned registry of all IPC communication boundaries within the Atlas ecosystem.

Every process, service, and subsystem within Atlas MUST use the Interface IDs defined in this catalog when declaring, documenting, or implementing IPC communication. Free-text descriptions of IPC endpoints are prohibited in normative contexts.

### 1.1 Purpose

This catalog serves three primary purposes:

1. **Unambiguous Identification**: Every IPC boundary has a unique, stable Interface ID that eliminates naming collisions and semantic drift across specification documents.
2. **Contract Enforcement**: Each interface definition specifies the communication paradigm, protocol family, and security classification, enabling automated verification of IPC conformance.
3. **Lifecycle Management**: Interfaces progress through a defined lifecycle from registration through deprecation, ensuring backward compatibility and controlled evolution of the IPC fabric.

### 1.2 Scope

This catalog covers all IPC boundaries between Atlas processes, including but not limited to:

- Runtime-to-Plugin communication channels
- Vision-to-AI data pipelines
- AI-to-Runtime reasoning results
- Workflow orchestration control paths
- Storage and logging subsystem interfaces
- Inter-plugin communication pathways
- Marketplace and scheduler coordination channels

### 1.3 Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2 Interface Registry

The following table defines all IPC interfaces within the Atlas platform. Each interface is assigned a unique Interface ID and specifies its source process, destination process, communication direction, functional description, and supported protocol families.

| Interface ID | Source | Destination | Direction | Description | Protocol |
|---|---|---|---|---|---|
| IPC-IF-001 | Runtime | Plugin | Bidirectional | Runtime-to-Plugin command and control | Request-Response, Event |
| IPC-IF-002 | Plugin | Runtime | Bidirectional | Plugin-to-Runtime status and telemetry | Request-Response, Event |
| IPC-IF-003 | Runtime | Vision | Bidirectional | Runtime-to-Vision frame capture control | Request-Response, Stream |
| IPC-IF-004 | Vision | AI | Bidirectional | Vision-to-AI frame and recognition results | Request-Response, Stream |
| IPC-IF-005 | AI | Runtime | Bidirectional | AI-to-Runtime reasoning and action results | Request-Response, Event |
| IPC-IF-006 | Runtime | Workflow | Bidirectional | Runtime-to-Workflow execution control | Request-Response, Event |
| IPC-IF-007 | Workflow | Runtime | Bidirectional | Workflow-to-Runtime step completion and state | Request-Response, Event |
| IPC-IF-008 | Runtime | Storage | Bidirectional | Runtime-to-Storage data persistence operations | Request-Response |
| IPC-IF-009 | Plugin | Plugin | Bidirectional | Plugin-to-Plugin inter-plugin communication | Request-Response, Event |
| IPC-IF-010 | Runtime | Logger | Unidirectional | Runtime-to-Logger audit and diagnostic events | Event (Fire-and-Forget) |
| IPC-IF-011 | Plugin | Logger | Unidirectional | Plugin-to-Logger diagnostic events | Event (Fire-and-Forget) |
| IPC-IF-012 | Vision | Storage | Unidirectional | Vision-to-Storage frame archival | Request-Response |
| IPC-IF-013 | AI | Knowledge | Bidirectional | AI-to-Knowledge pack retrieval and update | Request-Response |
| IPC-IF-014 | Runtime | Marketplace | Bidirectional | Runtime-to-Marketplace plugin catalog operations | Request-Response |
| IPC-IF-015 | Runtime | Scheduler | Bidirectional | Runtime-to-Scheduler task dispatch and priority | Request-Response, Event |

### 2.1 Interface ID Assignment Rules

Interface IDs are assigned sequentially within the `IPC-IF-NNN` namespace. The assignment rules are:

1. New interfaces MUST receive the next available sequential number in the registry.
2. Removed interface IDs MUST NOT be reassigned to new interfaces.
3. Interfaces that transition to Deprecated status retain their ID for the duration of the deprecation period.
4. Each interface definition MUST specify at least one source process, one destination process, and a communication direction.

### 2.2 Protocol Family Definitions

Each interface references one or more protocol families. The protocol families are defined as follows:

| Protocol Family | Semantics | Concurrency Model | Ordering Guarantee |
|---|---|---|---|
| Request-Response | A sender transmits a request and awaits a correlated response within a bounded timeout | Synchronous or asynchronous | Per-request FIFO |
| Event | A sender publishes an event without awaiting acknowledgment | Asynchronous, fire-and-forget | Best-effort delivery |
| Stream | A sender transmits a continuous sequence of data units to one or more receivers | Asynchronous, push-based | In-order delivery per stream |
| Event (Fire-and-Forget) | A sender publishes an event with no delivery guarantee and no backpressure | Asynchronous, unconstrained | No ordering guarantee |

### 2.3 Direction Semantics

The Direction column indicates the logical communication pattern between source and destination:

- **Bidirectional**: Both processes MAY initiate communication independently. Separate request-response pairs or event subscriptions exist in each direction.
- **Unidirectional**: Only the Source process initiates communication. The Destination process responds only within the protocol-defined constraints (e.g., acknowledgment events).

---

## 3 Interface Lifecycle

Every interface progresses through four defined lifecycle states. Transitions between states are governed by formal procedures to maintain system stability and backward compatibility.

### 3.1 Lifecycle States

| State | Description | Transition Trigger |
|---|---|---|
| Registered | The interface is formally defined in this catalog and announced to all affected processes. No implementation is required. | New interface addition or catalog revision |
| Active | The interface is implemented and operational. Processes communicate over this interface in production. | Implementation verification passes |
| Deprecated | The interface is scheduled for removal. New implementations MUST NOT depend on it. Existing implementations MAY continue operation during the transition period. | Architectural decision to replace or consolidate |
| Removed | The interface is deleted from this catalog. No process MAY reference the removed Interface ID. | Transition period expires and all dependent implementations are migrated |

### 3.2 State Transition Rules

1. An interface MUST be in the Registered state for a minimum of one full release cycle before transitioning to Active.
2. An interface MAY transition directly from Registered to Active if all dependent processes implement it simultaneously within the same release.
3. An interface in Active state MUST NOT transition to Deprecated without a minimum ninety-day transition period.
4. During the Deprecated state, all processes communicating over the interface MUST provide a migration path to the replacement interface.
5. An interface in Deprecated state MUST continue to function without degradation for all existing consumers.
6. An interface MAY transition from Deprecated to Removed only after all known dependent processes have confirmed migration.
7. Once Removed, the Interface ID is permanently reserved and MUST NOT appear in any future catalog revision.

### 3.3 Deprecation Notice Requirements

A deprecation notice MUST include the following information:

- The Interface ID being deprecated
- The effective deprecation date
- The scheduled removal date
- The replacement Interface ID(s), if applicable
- A migration guide describing the required changes
- A list of known dependent interfaces and processes

---

## 4 Interface Versioning

Each interface has an independent version lifecycle. Version negotiation occurs at connection establishment and MUST comply with the compatibility rules defined in this section.

### 4.1 Version Scheme

Interface versions follow the Semantic Versioning scheme (MAJOR.MINOR.PATCH):

- **MAJOR**: Incremented for incompatible API changes. A MAJOR version bump indicates that consumers of the older version MUST NOT communicate with producers of the newer version without explicit version negotiation.
- **MINOR**: Incremented for backwards-compatible functionality additions. MINOR version increments MUST NOT break existing consumers.
- **PATCH**: Incremented for backwards-compatible bug fixes. PATCH version increments carry no behavioral changes observable to consumers.

### 4.2 Version Negotiation

When a process initiates communication over an interface, the following version negotiation procedure applies:

1. The initiating process MUST include its supported version range in the connection handshake.
2. The receiving process MUST select the highest mutually supported version within the offered range.
3. If no common version exists, the receiving process MUST reject the connection with a `VersionMismatchError`.
4. If the receiving process supports only a lower version than offered, it MUST negotiate down to its highest supported version.
5. Version negotiation MUST complete before any application-layer messages are exchanged.

### 4.3 Backward Compatibility Requirements

1. A process implementing version N of an interface MUST accept and correctly process all messages conforming to version N-1 of that interface.
2. A process implementing version N of an interface MAY reject messages from version N-2 or earlier.
3. New fields added to request or response schemas in a MINOR version increment MUST be OPTIONAL for consumers on version N-1.
4. Removed fields in a MAJOR version increment MUST be documented in the deprecation notice.
5. Changes to the protocol family of an interface (e.g., adding Stream to an existing Request-Response interface) constitute a MINOR version increment only if all existing consumers remain unaffected.

### 4.4 Default Versions

Unless otherwise specified by the interface definition, the default version for each interface is 1.0.0. The default version represents the initial stable release of the interface contract.

---

## 5 Interface Discovery

Processes MUST be able to discover available interfaces at runtime without hardcoding interface metadata. Interface discovery enables dynamic service registration, graceful degradation, and cross-version interoperability.

### 5.1 Discovery Mechanism

The Atlas Runtime provides a service registry that exposes interface metadata to all connected processes. The discovery mechanism operates as follows:

1. Upon initialization, each process MUST register its available interfaces with the Runtime service registry.
2. The service registry maintains a live inventory of all registered interfaces, including their current lifecycle state, supported versions, and security classification.
3. Any process MAY query the service registry for the interface inventory at any time.
4. The service registry MUST respond to discovery queries within 500 milliseconds under normal operating conditions.

### 5.2 Discovery Query Format

Discovery queries MUST include the following parameters:

| Parameter | Required | Description |
|---|---|---|
| `source_filter` | No | Restrict results to interfaces originating from the specified process |
| `destination_filter` | No | Restrict results to interfaces targeting the specified process |
| `lifecycle_state` | No | Restrict results to interfaces in the specified lifecycle state |
| `version_range` | No | Restrict results to interfaces supporting the specified version range |
| `security_level` | No | Restrict results to interfaces meeting or exceeding the specified security level |

### 5.3 Discovery Response

The service registry response MUST include, for each matching interface:

- The Interface ID
- The source and destination process identifiers
- The communication direction
- The current lifecycle state
- The supported version range
- The protocol families
- The security classification

### 5.4 Discovery Refresh

1. The service registry MUST publish an event to all subscribed processes when any interface transitions between lifecycle states.
2. Processes MUST refresh their cached interface inventory within 10 seconds of receiving a lifecycle transition event.
3. Processes MAY cache the interface inventory for up to 60 seconds without re-querying the service registry.

---

## 6 Interface Security Requirements

Each interface has a minimum security classification that ALL implementations MUST enforce. Security classifications are defined in terms of authentication, authorization, encryption, and audit requirements.

### 6.1 Security Classification Levels

| Level | Name | Authentication | Authorization | Encryption | Audit Logging |
|---|---|---|---|---|---|
| S1 | Public | NONE | NONE | NONE | OPTIONAL |
| S2 | Internal | Process Token | Role-Based | Transport-Level | RECOMMENDED |
| S3 | Restricted | Process Token + Scope | Attribute-Based | End-to-End | REQUIRED |
| S4 | Confidential | Mutual TLS + Token | Policy-Based | End-to-End + At-Rest | REQUIRED + Integrity |

### 6.2 Interface Security Assignments

| Interface ID | Security Level | Rationale |
|---|---|---|
| IPC-IF-001 | S3 | Command and control of plugins requires strict authentication and scope enforcement |
| IPC-IF-002 | S3 | Telemetry from plugins to runtime must be authenticated to prevent spoofing |
| IPC-IF-003 | S3 | Frame capture control affects vision system behavior and resource allocation |
| IPC-IF-004 | S2 | Vision-to-AI frame data requires transport encryption but is within trusted boundary |
| IPC-IF-005 | S3 | AI reasoning results influence runtime decisions and require integrity guarantees |
| IPC-IF-006 | S3 | Workflow execution control must prevent unauthorized state transitions |
| IPC-IF-007 | S3 | Step completion reporting affects workflow integrity and requires authentication |
| IPC-IF-008 | S3 | Data persistence operations must prevent unauthorized read/write access |
| IPC-IF-009 | S2 | Inter-plugin communication is within the sandboxed plugin boundary |
| IPC-IF-010 | S2 | Audit events are fire-and-forget and do not require request authentication |
| IPC-IF-011 | S2 | Diagnostic events are fire-and-forget and do not require request authentication |
| IPC-IF-012 | S2 | Frame archival is a data pipeline operation within trusted subsystems |
| IPC-IF-013 | S3 | Knowledge pack operations affect AI reasoning capability and require strict access control |
| IPC-IF-014 | S3 | Marketplace operations affect plugin installation and require admin-level authorization |
| IPC-IF-015 | S3 | Task dispatch affects system scheduling and resource allocation |

### 6.3 Security Enforcement Rules

1. An interface implementation MUST enforce the minimum security level specified for that interface.
2. An implementation MAY apply a higher security level than the minimum, but MUST NOT apply a lower one.
3. Processes communicating over an interface MUST negotiate the highest common security level during connection establishment.
4. If security level negotiation fails, the connection MUST be rejected with a `SecurityNegotiationFailedError`.
5. All S3 and S4 interfaces MUST implement per-message integrity verification using cryptographic signatures.
6. All S4 interfaces MUST implement message encryption using TLS 1.3 or an equivalent forward-secret cipher suite.
7. Audit logging for S3 and S4 interfaces MUST capture the correlation ID, source process identity, timestamp, and interface ID for every message.

---

## 7 Interface Catalog Usage

This section describes how to reference interfaces in sequence diagrams, architectural documents, and implementation specifications.

### 7.1 Sequence Diagram References

When documenting communication flows in sequence diagrams, ALL references to IPC boundaries MUST use the Interface ID as the channel identifier. Free-text descriptions of IPC channels are prohibited in normative sequence diagrams.

**Correct Usage:**

```
Runtime --> Plugin: IPC-IF-001
  LoadModule(plugin_id="vision-enhancer-v2")
Plugin --> Runtime: IPC-IF-002
  StatusUpdate(state="loaded", version="2.1.0")
```

**Incorrect Usage (Prohibited):**

```
Runtime --> Plugin: "Load plugin module"
Plugin --> Runtime: "Send status back"
```

### 7.2 Document Cross-Referencing

When an RFC or architectural document references an IPC interface, it MUST use the canonical form `IPC-IF-NNN`. Additional context MAY be provided in parentheses.

**Examples:**

- Module initialization over `IPC-IF-001`
- Telemetry reporting over `IPC-IF-002`
- Frame streaming over `IPC-IF-004`

### 7.3 Error Reporting

When an implementation reports an error related to a specific interface, the error context MUST include the Interface ID. Error messages MUST follow the format:

```
[IPC-IF-NNN] ErrorType: Description
```

### 7.4 Trace and Correlation

All trace and correlation identifiers in IPC messages MUST include the Interface ID to enable end-to-end tracing across the communication chain. The correlation ID format is:

```
<correlation-uuid>:<interface-id>:<hop-count>
```

---

## 8 Cross-References

This catalog is referenced by and complements the following Atlas specifications:

| Reference | Title | Relationship |
|---|---|---|
| RFC-0101 | Runtime Core Specification | Defines the Runtime process and its role as the central IPC coordinator. References IPC-IF-001, IPC-IF-005, IPC-IF-006, IPC-IF-008, IPC-IF-010, IPC-IF-014, IPC-IF-015 |
| RFC-0102 | Plugin System Specification | Defines the Plugin lifecycle and its communication channels with the Runtime. References IPC-IF-001, IPC-IF-002, IPC-IF-009 |
| RFC-0103 | Vision Engine Specification | Defines the Vision process, frame capture workflows, and archival pipelines. References IPC-IF-003, IPC-IF-004, IPC-IF-012 |
| RFC-0105 | AI Host Specification | Defines the AI process, reasoning pipelines, and knowledge integration. References IPC-IF-004, IPC-IF-005, IPC-IF-013 |
| RFC-0107 | Workflow Engine Specification | Defines the Workflow process, step execution, and state management. References IPC-IF-006, IPC-IF-007 |

### 8.1 Dependency Mapping

Each cross-referenced specification maps its operational communication patterns to the Interface IDs defined in this catalog. When a specification defines a new communication pattern, it MUST either:

1. Reference an existing Interface ID from this catalog if the pattern matches an established interface.
2. Propose a new Interface ID through the Interface ID assignment process defined in Section 2.1.

---

## 9 Glossary

| Term | Definition |
|---|---|
| **Interface ID** | A unique, stable identifier (format: `IPC-IF-NNN`) assigned to each IPC communication boundary in the Atlas platform. |
| **Source Process** | The process that initiates communication over an interface. |
| **Destination Process** | The process that receives communication initiated by the source process. |
| **Bidirectional** | A communication pattern where both processes MAY independently initiate messages over the interface. |
| **Unidirectional** | A communication pattern where only the source process initiates messages; the destination responds only within protocol constraints. |
| **Request-Response** | A protocol family where a sender transmits a request and awaits a correlated response within a bounded timeout. |
| **Event** | A protocol family where a sender publishes a message without awaiting acknowledgment. |
| **Stream** | A protocol family where a sender transmits a continuous sequence of data units to one or more receivers. |
| **Fire-and-Forget** | An event delivery model with no delivery guarantee and no backpressure mechanism. |
| **Lifecycle State** | The current stage of an interface in its lifecycle: Registered, Active, Deprecated, or Removed. |
| **Service Registry** | The Runtime-provided metadata store that maintains the live inventory of all registered interfaces. |
| **Security Level** | A classification (S1-S4) defining the minimum authentication, authorization, encryption, and audit requirements for an interface. |
| **Version Negotiation** | The handshake procedure by which two processes agree on a mutually supported interface version. |
| **Correlation ID** | A unique identifier propagated across IPC messages to enable end-to-end tracing of a communication session. |
| **Backpressure** | A flow-control mechanism that prevents a sender from overwhelming a receiver's processing capacity. |
| **Forward Secret** | A cryptographic property where compromise of long-term keys does not allow decryption of past session messages. |

---

## 10 Revision History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 1.0.0 | 2026-06-30 | Atlas Team | Initial release. Defined 15 IPC interfaces covering Runtime, Plugin, Vision, AI, Workflow, Storage, Logger, Knowledge, Marketplace, and Scheduler communication boundaries. Established interface lifecycle, versioning, discovery, and security frameworks. |

---

## 11 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| IPC-CAT-01 | All IPC boundaries reference a defined Interface ID | Static analysis of specification documents |
| IPC-CAT-02 | No free-text IPC channel descriptions in normative sequence diagrams | Document review |
| IPC-CAT-03 | Interface IDs are sequential and never reassigned | Catalog audit |
| IPC-CAT-04 | Version negotiation completes before application-layer exchange | Integration test |
| IPC-CAT-05 | Security level enforcement matches the assigned classification | Penetration test |
| IPC-CAT-06 | Service registry responds within 500 ms under normal conditions | Load test |
| IPC-CAT-07 | Deprecated interfaces remain fully functional during transition period | Migration test |
| IPC-CAT-08 | Removed Interface IDs do not appear in new implementations | Code review |
| IPC-CAT-09 | Correlation IDs include the Interface ID | Trace analysis |
| IPC-CAT-10 | Backward compatibility with N-1 version is maintained | Cross-version communication test |

---

## 12 Acceptance Criteria

### AC-IPC-001
- **Requirement**: Every IPC communication boundary in the Atlas platform MUST reference an Interface ID from this catalog.
- **Verification**: Review all RFC documents and implementation specifications.
- **Expected Result**: No undocumented or free-text IPC boundaries exist.

### AC-IPC-002
- **Requirement**: Interface version negotiation MUST prevent communication between incompatible major versions.
- **Verification**: Connect a v1 consumer to a v2 producer with no overlap.
- **Expected Result**: Connection is rejected with `VersionMismatchError`.

### AC-IPC-003
- **Requirement**: All S3-classified interfaces MUST enforce mutual authentication.
- **Verification**: Attempt communication over an S3 interface without valid credentials.
- **Expected Result**: Connection is refused with `AuthenticationFailed`.

### AC-IPC-004
- **Requirement**: The service registry MUST reflect the current lifecycle state of all registered interfaces.
- **Verification**: Transition an interface to Deprecated and query the registry.
- **Expected Result**: The registry reports the interface as Deprecated within 10 seconds.

### AC-IPC-005
- **Requirement**: Removed Interface IDs MUST NOT be assignable to new interfaces.
- **Verification**: Attempt to assign a previously removed Interface ID.
- **Expected Result**: Assignment is rejected with `InterfaceIDReserved`.

---

## 13 References
1. **RFC-0007**: Runtime IPC Architecture
2. **RFC-0101**: Runtime Core Specification
3. **RFC-0102**: Plugin System Specification
4. **RFC-0103**: Vision Engine Specification
5. **RFC-0105**: AI Host Specification
6. **RFC-0107**: Workflow Engine Specification
7. **RFC 2119**: Key words for use in RFCs to Indicate Requirement Levels (IETF)
8. **Semantic Versioning 2.0.0**: http://semver.org/

---

## 14 Compatibility
- Compatible with Spec Version 1.x.
- Compatible with RFC-0007 Runtime IPC Architecture.
