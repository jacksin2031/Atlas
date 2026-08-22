# RFC-IPC-CAT-MSG: IPC Message Catalog

RFC: RFC-IPC-CAT-MSG
Title: IPC Message Catalog
Status: Accepted
Version: 1.0.0
Category: IPC
Layer: Communication
Normative: YES
Authors: Atlas Team
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0101 IPC Overview
  - RFC-0102 IPC Message Model
  - RFC-0104 IPC Routing
Required By:
  - RFC-0101 IPC Overview
  - RFC-0102 IPC Message Model
  - RFC-0104 IPC Routing
  - RFC-0105 IPC Channel
  - RFC-0106 IPC Serialization
  - RFC-0107 IPC Security
  - RFC-0108 IPC Reliability
  - RFC-0109 IPC Lifecycle
  - RFC-0110 IPC Observability
  - RFC-0111 IPC Error Model
  - RFC-0112 IPC Extension
Supersedes: None
Superseded By: None
Category: IPC
Layer: Communication
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 3.5 (IPC Isolation)
Related RFCs:
  - RFC-0101 IPC Overview
  - RFC-0102 IPC Message Model
  - RFC-0104 IPC Routing
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

This specification is Normative. Every Atlas IPC subsystem implementation MUST reference the Message IDs defined in this catalog for all standard inter-process communications. No implementation MAY define a Message ID that collides with an entry in this registry. Extensions that require new message IDs MUST follow the procedure defined in RFC-0112.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Message Registry](#2-message-registry)
3. [Message Schema Reference](#3-message-schema-reference)
4. [Message Lifecycle](#4-message-lifecycle)
5. [Message Priority Definitions](#5-message-priority-definitions)
6. [Message Versioning](#6-message-versioning)
7. [Cross-References](#7-cross-references)
8. [Glossary](#8-glossary)
9. [Revision History](#9-revision-history)

---

## 1 Introduction

### 1.1 Purpose

The IPC Message Catalog is the authoritative registry of all standard Message IDs used within the Atlas platform. It provides a single source of truth for message identification, ensuring that every component, plugin, and subsystem communicates using consistent, unambiguous identifiers.

Every RFC within the Atlas IPC subsystem MUST reference Message IDs from this catalog rather than free-text descriptions. This eliminates ambiguity in routing rules, schema definitions, security policies, and observability configurations.

### 1.2 Scope

This catalog defines Message IDs for the following Atlas service domains:

- **Runtime** — Core orchestration, lifecycle management, and system coordination.
- **Plugin** — Plugin host interaction, capability negotiation, and status reporting.
- **Workflow** — Execution scheduling, step tracking, and cancellation.
- **Vision** — Frame capture, streaming, and recognition pipelines.
- **AI** — Request-response cycles, tool calls, and streaming responses.
- **Storage** — CRUD operations and synchronization events.
- **Logger** — Audit logging and structured event emission.
- **Scheduler** — Dispatch, completion, and priority management.
- **Marketplace** — Query and update notifications.

### 1.3 Usage

Implementations MUST:

1. Use the `Message ID` column as the sole identifier for any IPC message.
2. Reference the `Protocol` column to determine the communication paradigm.
3. Consult the `Priority` column for queue ordering and backpressure decisions.
4. Map each Message ID to its corresponding schema definition in RFC-0102.

Consumers MUST NOT invent new Message IDs outside of the extension mechanism defined in RFC-0112.

---

## 2 Message Registry

The following table enumerates all standard IPC Message IDs. Each entry is immutable once published; new entries are added via the extension process in RFC-0112.

| # | Message ID | Source | Destination | Type | Priority | Protocol |
|---|---|---|---|---|---|---|
| 1 | MSG-0001 | Runtime | All | Command | Critical | Request-Response |
| 2 | MSG-0002 | Runtime | All | Command | High | Request-Response |
| 3 | MSG-0003 | Runtime | All | Command | Critical | Request-Response |
| 4 | MSG-0004 | Runtime | All | Command | Low | Request-Response |
| 5 | MSG-0005 | Runtime | Runtime | Event | Medium | Event |
| 6 | MSG-0006 | Runtime | Plugin | Command | High | Request-Response |
| 7 | MSG-0007 | Runtime | Plugin | Command | High | Request-Response |
| 8 | MSG-0008 | Plugin | Runtime | Event | Medium | Event |
| 9 | MSG-0009 | Plugin | Runtime | Event | Critical | Event |
| 10 | MSG-0010 | Plugin | Runtime | Event | Medium | Request-Response |
| 11 | MSG-0011 | Runtime | Workflow | Command | High | Request-Response |
| 12 | MSG-0012 | Workflow | Runtime | Event | Medium | Event |
| 13 | MSG-0013 | Workflow | Runtime | Event | Critical | Event |
| 14 | MSG-0014 | Runtime | Workflow | Command | High | Request-Response |
| 15 | MSG-0015 | Runtime | Workflow | Command | Medium | Request-Response |
| 16 | MSG-0016 | Runtime | Workflow | Command | Medium | Request-Response |
| 17 | MSG-0017 | Runtime | Vision | Command | High | Request-Response |
| 18 | MSG-0018 | Vision | Runtime | Event | High | Event |
| 19 | MSG-0019 | Runtime | Vision | Command | High | Stream |
| 20 | MSG-0020 | Runtime | Vision | Command | High | Request-Response |
| 21 | MSG-0021 | Vision | AI | Event | High | Stream |
| 22 | MSG-0022 | Vision | AI | Event | High | Event |
| 23 | MSG-0023 | Runtime | AI | Command | High | Request-Response |
| 24 | MSG-0024 | AI | Runtime | Event | High | Request-Response |
| 25 | MSG-0025 | AI | Runtime | Event | Medium | Stream |
| 26 | MSG-0026 | Runtime | AI | Command | High | Request-Response |
| 27 | MSG-0027 | AI | Runtime | Event | High | Request-Response |
| 28 | MSG-0028 | Runtime | AI | Event | High | Event |
| 29 | MSG-0029 | Runtime | Storage | Command | Medium | Request-Response |
| 30 | MSG-0030 | Runtime | Storage | Command | Medium | Request-Response |
| 31 | MSG-0031 | Runtime | Storage | Command | Medium | Request-Response |
| 32 | MSG-0032 | Runtime | Storage | Command | Medium | Request-Response |
| 33 | MSG-0033 | Storage | Runtime | Event | Medium | Event |
| 34 | MSG-0034 | Any | Logger | Event | Medium | Fire-and-Forget |
| 35 | MSG-0035 | Any | Logger | Event | Critical | Fire-and-Forget |
| 36 | MSG-0036 | Runtime | Scheduler | Command | High | Request-Response |
| 37 | MSG-0037 | Scheduler | Runtime | Event | Medium | Event |
| 38 | MSG-0038 | Runtime | Scheduler | Event | Medium | Event |
| 39 | MSG-0039 | Runtime | Marketplace | Command | Medium | Request-Response |
| 40 | MSG-0040 | Marketplace | Runtime | Event | Medium | Event |

### 2.1 Message ID Format

All Message IDs MUST conform to the pattern `MSG-NNNN`, where `NNNN` is a zero-padded four-digit decimal integer starting from `0001`. The leading zeros are significant and MUST be preserved in all serializations and routing tables.

### 2.2 Reserved Ranges

| Range | Allocation | Notes |
|---|---|---|
| MSG-0001 – MSG-0099 | Standard Messages | Defined in this catalog |
| MSG-0100 – MSG-0999 | Extension Messages | Assigned per RFC-0112 |
| MSG-1000 – MSG-9999 | Reserved | Future Atlas expansion |
| MSG-0000 | Null ID | MUST NOT be used |

### 2.3 Semantics of Source and Destination Columns

- **Source**: The process or service domain that originates the message. The value `Any` indicates that any registered Atlas process MAY emit the message.
- **Destination**: The target process or service domain. The value `All` indicates a broadcast scope, meaning every registered process MUST receive and acknowledge the message.

### 2.4 Semantics of Message Type Column

- **Command**: A directive from a sender to a receiver. Commands typically carry intent and require an acknowledgment or response.
- **Event**: An asynchronous notification emitted by a sender. Events are fire-and-forget unless the protocol explicitly pairs them with a request-response exchange.

---

## 3 Message Schema Reference

### 3.1 Schema Binding

Every Message ID in this catalog maps to a schema definition in RFC-0102 (IPC Message Model). Implementations MUST:

1. Look up the schema for a given Message ID in the registry defined by RFC-0102.
2. Validate incoming messages against the corresponding schema before routing.
3. Serialize outgoing messages according to the schema definition.

### 3.2 Schema Versioning

Each Message ID carries a schema version as defined in Section 6 of this catalog. The initial version for all Message IDs is `v1.0.0`. Schema evolution MUST follow the rules in RFC-0102 and RFC-0106.

### 3.3 Payload Structure

All Message IDs follow the envelope structure defined in RFC-0102, Section 4. The payload field within that envelope is populated according to the per-message schema registered in RFC-0102, Section 5.

---

## 4 Message Lifecycle

Every Message ID progresses through the following five stages. Implementations MUST enforce stage transitions as described.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Created   │────▶│ Validated   │────▶│   Routed    │────▶│  Delivered  │────▶│Acknowledged│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼                   ▼
  Message constructed   Schema validated   Dispatcher selects   Receiver receives   Confirmation sent
  with Message ID       against RFC-0102    target channel      and processes       or timed out
                        schema              per RFC-0104
```

### 4.1 Stage Definitions

| Stage | Description | Enforced By |
|---|---|---|
| Created | The originating process constructs the message with a valid Message ID from this catalog. | Sender process |
| Validated | The IPC Dispatcher validates the message against the schema registered in RFC-0102. | RFC-0102 validator |
| Routed | The Dispatcher determines the target channel and applies routing rules from RFC-0104. | RFC-0104 router |
| Delivered | The message is placed on the destination channel and received by the target process. | RFC-0105 channel |
| Acknowledged | The receiver sends a confirmation (for Request-Response protocols) or the message is logged as delivered (for Event protocols). | Protocol handler |

### 4.2 Lifecycle States Per Protocol

| Protocol | Expected Lifecycle Path |
|---|---|
| Request-Response | Created → Validated → Routed → Delivered → Acknowledged (response) |
| Event | Created → Validated → Routed → Delivered → (logged) |
| Stream | Created → Validated → Routed → Delivered (continuously) |
| Fire-and-Forget | Created → Validated → Routed → Delivered (no acknowledgment) |

---

## 5 Message Priority Definitions

Message priorities determine queue ordering, backpressure thresholds, and scheduling behavior. Every Message ID in this catalog is assigned one of four priority levels.

### 5.1 Priority Levels

| Priority | Queue Depth | Max Latency | Drop Policy | Description |
|---|---|---|---|---|
| Critical | Unlimited | 10 ms | NEVER dropped | System-critical lifecycle messages. MUST be processed before any lower-priority message. |
| High | 10,000 | 100 ms | Dropped only under extreme backpressure | Operational messages that drive core functionality. |
| Medium | 50,000 | 500 ms | Dropped under sustained backpressure | Routine coordination and status messages. |
| Low | 100,000 | 2,000 ms | Dropped first under backpressure | Diagnostic and housekeeping messages. |

### 5.2 Priority Assignment Rules

- **Critical** messages MUST be limited to system lifecycle operations: initialization, shutdown, and error conditions that threaten stability.
- **High** messages MUST be used for operational commands that affect active workflows or real-time data pipelines.
- **Medium** messages MUST be used for routine coordination, status reporting, and non-blocking events.
- **Low** messages MUST be reserved for health checks, diagnostics, and non-urgent telemetry.

### 5.3 Priority Enforcement

The IPC Dispatcher MUST enforce priority ordering as follows:

1. Messages of a higher priority MUST be dequeued before messages of lower priority.
2. When a Critical message arrives, the Dispatcher MUST interrupt processing of any Medium or Low message currently in the pipeline.
3. Under backpressure (queue depth exceeding threshold), the Dispatcher MUST drop messages starting from the lowest priority tier.

---

## 6 Message Versioning

### 6.1 Schema Version Model

Each Message ID carries a schema version in the format `vM.m.p` (major.minor.patch), following Semantic Versioning principles as adapted for IPC schemas:

- **Major version increment** (`vM.0.0`): Breaking change to the message schema. Existing consumers MUST NOT accept messages with a different major version.
- **Minor version increment** (`vM.m.0`): Backward-compatible addition of fields. Older consumers MUST ignore unknown fields.
- **Patch version increment** (`vM.m.p`): Backward-compatible corrections or clarifications. No schema change.

### 6.2 Version Negotiation

When two processes communicate, the following rules apply:

1. Both processes MUST advertise their supported schema versions during connection establishment.
2. If the major versions differ, the connection MUST be rejected with a `VersionMismatch` error as defined in RFC-0111.
3. If the major versions match but minor versions differ, the sender MUST use the lower minor version of the two.
4. Patch version differences MUST be ignored for compatibility purposes.

### 6.3 Deprecation

Messages MAY be deprecated but MUST NOT be removed from this catalog. Deprecated messages:

- MUST remain routable for a minimum of two major Atlas releases.
- MUST carry a deprecation notice in the catalog metadata.
- MUST continue to be accepted by all processes during the grace period.

### 6.4 Current Versions

All Message IDs in this catalog are initially assigned schema version `v1.0.0`.

---

## 7 Cross-References

This catalog serves as the authoritative identifier registry for the following IPC specifications:

| Referenced RFC | Title | Relationship |
|---|---|---|
| RFC-0101 | IPC Overview | Defines the overall architecture; references this catalog for message identification. |
| RFC-0102 | IPC Message Model | Defines the envelope structure and schema validation; maps each Message ID to its payload schema. |
| RFC-0103 | IPC Transport | Defines physical transport layers; uses Message IDs for transport-agnostic framing. |
| RFC-0104 | IPC Routing | Defines routing rules; uses Message ID source/destination pairs to determine channel topology. |
| RFC-0105 | IPC Channel | Defines channel semantics; routes messages by priority and protocol type from this catalog. |
| RFC-0106 | IPC Serialization | Defines encoding formats; uses Message IDs to select the correct schema for serialization. |
| RFC-0107 | IPC Security | Defines access control; uses Message IDs to enforce channel permission policies. |
| RFC-0108 | IPC Reliability | Defines delivery guarantees; uses Message IDs to apply retry and acknowledgment policies. |
| RFC-0109 | IPC Lifecycle | Defines process lifecycle hooks; uses Message IDs for startup, shutdown, and health sequences. |
| RFC-0110 | IPC Observability | Defines tracing and metrics; uses Message IDs as correlation keys for end-to-end tracing. |
| RFC-0111 | IPC Error Model | Defines error types; uses Message IDs in error context for diagnostic precision. |
| RFC-0112 | IPC Extension | Defines the extension mechanism; uses reserved Message ID ranges from this catalog. |

---

## 8 Glossary

| Term | Definition |
|---|---|
| **IPC** | Inter-Process Communication. The mechanism by which independent Atlas processes exchange structured data. |
| **Message ID** | A unique, catalog-assigned identifier in the format `MSG-NNNN` that designates a specific IPC message. |
| **Source** | The originating process or service domain of a message. |
| **Destination** | The target process or service domain of a message. |
| **Command** | A message type that conveys an intent requiring processing and typically a response. |
| **Event** | A message type that conveys a notification, optionally paired with a request-response protocol. |
| **Protocol** | The communication paradigm governing message exchange: Request-Response, Event, Stream, or Fire-and-Forget. |
| **Priority** | A classification determining queue ordering and backpressure behavior: Critical, High, Medium, or Low. |
| **Schema Version** | The version of the message payload structure, expressed as `vM.m.p`. |
| **Envelope** | The outer wrapper structure defined in RFC-0102 that contains the Message ID, metadata, and payload. |
| **Channel** | A communication pathway defined in RFC-0105 through which messages flow between source and destination. |
| **Dispatcher** | The IPC component responsible for validating, routing, and delivering messages as defined in RFC-0104. |
| **Correlation ID** | A unique identifier propagated across message hops to enable end-to-end tracing as defined in RFC-0110. |
| **Backpressure** | A flow-control mechanism that regulates message throughput when the destination cannot keep pace. |
| **Fire-and-Forget** | A delivery model where the sender does not expect an acknowledgment from the receiver. |
| **Stream** | A continuous, bidirectional message flow where data is sent incrementally over an established channel. |

---

## 9 Revision History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-06-30 | Atlas Team | Initial release. Defined 40 standard Message IDs (MSG-0001 through MSG-0040) across nine service domains. Established message lifecycle, priority definitions, versioning model, and cross-references to the full IPC subsystem. |

---

## 10 Normative Contracts

The following contracts are binding on all Atlas IPC implementations:

1. Every IPC message MUST carry a Message ID from this catalog.
2. The Message ID MUST be encoded in the envelope header as defined in RFC-0102.
3. The Dispatcher MUST reject any message with a Message ID not present in this catalog and not within the extension range defined in Section 2.2.
4. Schema validation MUST occur at the Validated stage of the message lifecycle (Section 4).
5. Priority ordering MUST be enforced as defined in Section 5.
6. Version negotiation MUST follow the rules in Section 6.2.
7. All Message IDs are immutable; no Message ID MAY be reassigned or repurposed.
8. New Message IDs beyond MSG-0040 MUST be assigned sequentially within the extension range per RFC-0112.

---

## 11 Acceptance Criteria

### AC-MSG-001
- **Requirement**: Every IPC message MUST carry a valid Message ID from this catalog.
- **Verification**: Intercept a message at the Dispatcher entry point and inspect the envelope header.
- **Expected Result**: The Message ID matches the `MSG-NNNN` pattern and exists in the Message Registry.

### AC-MSG-002
- **Requirement**: The Dispatcher MUST reject messages with unregistered Message IDs.
- **Verification**: Send a message with a fabricated Message ID (e.g., `MSG-9999`).
- **Expected Result**: The Dispatcher rejects the message with an `InvalidMessageID` error per RFC-0111.

### AC-MSG-003
- **Requirement**: Priority ordering MUST be enforced at the Dispatcher queue.
- **Verification**: Enqueue a Low-priority message, then enqueue a Critical-priority message.
- **Expected Result**: The Critical message is dequeued and delivered before the Low message.

### AC-MSG-004
- **Requirement**: Schema version negotiation MUST prevent cross-major-version communication.
- **Verification**: Connect two processes with differing major schema versions.
- **Expected Result**: Connection is rejected with a `VersionMismatch` error per RFC-0111.

### AC-MSG-005
- **Requirement**: All 40 Message IDs in this catalog MUST be routable.
- **Verification**: Run the routing table generator against each Message ID.
- **Expected Result**: Every Message ID resolves to a valid source-destination pair and channel per RFC-0104.

---

## 12 References

1. **RFC-0101**: IPC Overview
2. **RFC-0102**: IPC Message Model
3. **RFC-0103**: IPC Transport
4. **RFC-0104**: IPC Routing
5. **RFC-0105**: IPC Channel
6. **RFC-0106**: IPC Serialization
7. **RFC-0107**: IPC Security
8. **RFC-0108**: IPC Reliability
9. **RFC-0109**: IPC Lifecycle
10. **RFC-0110**: IPC Observability
11. **RFC-0111**: IPC Error Model
12. **RFC-0112**: IPC Extension
13. **glossary.md**: Unified Atlas Glossary

---

*End of RFC-IPC-CAT-MSG: IPC Message Catalog*
