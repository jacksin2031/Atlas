RFC: RFC-0327
Title: Workflow IPC
Status: Proposed
Version: 1.1.0
Author: 
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Message | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Message Queue | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Message Bus | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| RPC Call | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Event Stream | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Channel | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Broker | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Publisher | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Subscriber | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Request-Reply | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Pub-Sub | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Fire-And-Forget | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
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
Layer: Core
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012 Contract-First Specification-Driven Development
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0324 Workflow Storage
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/ipc-channel.json
  - schemas/workflow/ipc-message.json
Related Catalog:
  - catalog/workflow-events.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

---

## Authority

This RFC is the authoritative specification for the RFC 0327 workflow ipc.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

-



## Normative Status



This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

\n

## 1 Introduction



### 1.1 Purpose



The Workflow Inter-Process Communication (IPC) specification defines the messaging model through which workflow components exchange information during definition, execution, monitoring, and lifecycle management. IPC is the communication substrate that enables distributed workflow execution across process boundaries while preserving ordering, reliability, and security guarantees.



This specification MUST NOT be interpreted as defining the Runtime IPC layer described in RFC-0007. Rather, this specification operates at the workflow layer, building upon the Runtime IPC foundation to provide workflow-specific communication semantics, message types, reliability levels, and security policies tailored to workflow orchestration.



### 1.2 Scope



The scope of this specification encompasses:



- Workflow IPC message type taxonomy and structure

- IPC channel model and channel lifecycle

- Reliability and ordering guarantees

- Flow control and backpressure mechanisms

- Timeout and retry semantics

- Security model including authentication, authorization, and encryption

- Monitoring and observability of IPC traffic

- Fault tolerance and failure recovery at the IPC layer

- Performance requirements and benchmarks



### 1.3 Terminology



| Term | Definition |

|---|---|

| IPC Endpoint | A named communication address that participates in workflow IPC |

| IPC Channel | A bidirectional or unidirectional communication pathway between endpoints |

| IPC Message | A discrete unit of information exchanged between workflow endpoints |

| Reliability Level | A guarantee class defining delivery semantics for IPC messages |

| Ordering Class | A guarantee class defining message sequencing semantics |

| Backpressure Signal | An IPC notification indicating receiver capacity constraints |

| Flow Control Window | The maximum number of unacknowledged messages permitted |

| IPC Session | A temporal association between two communicating endpoints |

| Message Correlation ID | A unique identifier linking related IPC messages across a transaction |

| Message Sequence Number | An ordered counter establishing delivery sequence within a channel |

| Heartbeat Interval | The configured period between unsolicited health-check messages |

| Dead Letter Channel | A dedicated channel for messages that failed delivery after retries |



### 1.4 Conventions


## 1.5 Terminology

All terms used in this specification carry the exact definitions from RFC-0301 (Workflow Overview) and the Atlas Master Glossary. Key terms include: IPC Endpoint, IPC Channel, IPC Message, Reliability Level, Ordering Class, Backpressure Signal, Flow Control Window, IPC Session, Message Correlation ID, Message Sequence Number, Heartbeat Interval, and Dead Letter Channel.


All terms carry definitions from RFC-0301 and the Atlas Master Glossary. Key terms include: IPC Endpoint, IPC Channel, IPC Message, Reliability Level, Ordering Class, Backpressure Signal, Flow Control Window, IPC Session, Message Correlation ID, Message Sequence Number, Heartbeat Interval, and Dead Letter Channel.



The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119.


All terms used in this specification carry the exact definitions from RFC-0301 (Workflow Overview) and the Atlas Master Glossary. Key terms include: IPC Endpoint, IPC Channel, IPC Message, Reliability Level, Ordering Class, Backpressure Signal, Flow Control Window, IPC Session, Message Correlation ID, Message Sequence Number, Heartbeat Interval, and Dead Letter Channel.




---

---

---


This RFC is the authoritative specification for the RFC 0327 workflow ipc.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.



This RFC is the authoritative specification for the RFC 0327 workflow ipc.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 2 Layer Boundaries



All terms used in this specification carry the exact definitions from RFC-0301 (Workflow Overview) and the Atlas Master Glossary. Key terms include: IPC Endpoint, IPC Channel, IPC Message, Reliability Level, Ordering Class, Backpressure Signal, Flow Control Window, IPC Session, Message Correlation ID, Message Sequence Number, Heartbeat Interval, and Dead Letter Channel.

### 2.1 Responsibilities

This specification IS responsible for:
- Defining the workflow-layer IPC message taxonomy and structure.
- Specifying the IPC channel model and channel lifecycle.
- Establishing reliability and ordering guarantees at the workflow layer.
- Defining flow control and backpressure mechanisms.
- Specifying timeout and retry semantics for workflow IPC.
- Defining the workflow IPC security model (authentication, authorization, encryption).

### 2.2 Non-Responsibilities

This specification IS NOT responsible for:
- Defining the Runtime IPC layer (covered by RFC-0007).
- Implementing transport protocols (delegated to the Runtime IPC layer).
- Managing user identities (delegated to identity providers).
- Persisting IPC messages (handled by Workflow Storage, RFC-0324).

### 2.3 Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0007 | Consumed | Runtime IPC Architecture provides the transport foundation |
| RFC-0301 | Consumed | Workflow Overview provides foundational workflow concepts |
| RFC-0304 | Consumed | Workflow Runtime provides execution context |
| RFC-0319 | Consumed | Workflow Security provides security model |
| RFC-0320 | Consumed | Workflow Performance provides performance requirements |
| RFC-0321 | Consumed | Workflow Observability provides IPC monitoring |
| RFC-0324 | Consumed | Workflow Storage provides message persistence |
| RFC-0328 | Consumed | Workflow Serialization provides IPC message serialization |

### 2.4 Consumers
- Workflow Runtime (RFC-0304): Uses IPC for component communication.
- Workflow Plugin Integration (RFC-0323): Uses IPC for plugin-host communication.
- Workflow Observability (RFC-0321): Monitors IPC traffic for telemetry.

### 2.5 Providers
- IPC Channel Schema (schemas/workflow/ipc-channel.json): Provides channel format contract.
- IPC Message Schema (schemas/workflow/ipc-message.json): Provides message format contract.

### 2.6 Forbidden Dependencies
- This specification MUST NOT depend on any specific transport protocol (gRPC, REST, WebSocket, etc.).
- This specification MUST NOT assume a particular serialization format (JSON, Protocol Buffers, MessagePack).
- This specification MUST NOT depend on any platform-specific networking stack.

## 3 Security

Workflow IPC MUST enforce the security model defined in RFC-0319:
- All IPC endpoints MUST authenticate before establishing channels.
- All IPC messages MUST be encrypted in transit (TLS 1.3 or equivalent).
- IPC channels MUST enforce permission boundaries per the permission model (RFC-0319 Section 4).
- Dead letter channels MUST be isolated from production channels.
- IPC messages carrying secrets MUST use envelope encryption.

## 4 Performance

- IPC message serialization MUST complete within 1ms for messages up to 1MB.
- IPC channel establishment MUST complete within 10ms.
- IPC backpressure signals MUST propagate within 1ms of receiver capacity change.
- Heartbeat interval MUST be configurable with a default of 5 seconds.
- Flow control window MUST be configurable with a default of 100 unacknowledged messages.

## 5 Compatibility

- IPC message formats MUST be backward compatible within a major version.
- New message types MAY be added without breaking existing consumers.
- Reliability levels MUST be negotiable between endpoints.
- Channel lifecycle states MUST be compatible across implementations.

## 6 Compliance

- All IPC events MUST be recorded in the audit trail per RFC-0321.
- IPC security violations MUST be reported to the compliance system per RFC-0330.
- IPC message retention MUST comply with organizational data retention policies.

## 7 Future Evolution

- **Stream-based IPC**: Support for streaming channels for continuous data flow between nodes.
- **Cross-cluster IPC**: Protocol for IPC across distributed Atlas deployments.
- **Adaptive Reliability**: Dynamic reliability level negotiation based on workload characteristics.
- **GraphQL-style Query Channels**: Bidirectional query-response channels for interactive workflows.
- **Multi-tenant IPC**: Isolation guarantees for shared infrastructure deployments.

## 8 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any specific network protocol (TCP, UDP, HTTP/2, QUIC, etc.)

## 9 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST support twelve IPC terms defined in Section 1.3. | Terminology test |
| AC-02 | The implementation MUST enforce authentication for all IPC endpoints. | Security test |
| AC-03 | The implementation MUST encrypt all IPC messages in transit. | Encryption test |
| AC-04 | IPC message serialization MUST complete within 1ms for messages up to 1MB. | Performance test |
| AC-05 | IPC channel establishment MUST complete within 10ms. | Latency test |
| AC-06 | Backpressure signals MUST propagate within 1ms. | Backpressure test |

## 10 References

| Reference | Description |
|---|---|
| RFC-0007 | Runtime IPC Architecture (transport foundation) |
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0304 | Workflow Runtime (execution context) |
| RFC-0312 | Workflow Scheduler (scheduling constraints) |
| RFC-0314 | Workflow Error Handling (error propagation) |
| RFC-0315 | Workflow Recovery (failure recovery) |
| RFC-0316 | Workflow Debugging (debug IPC) |
| RFC-0319 | Workflow Security (security model) |
| RFC-0320 | Workflow Performance (performance requirements) |
| RFC-0321 | Workflow Observability (IPC monitoring) |
| RFC-0324 | Workflow Storage (message persistence) |
| RFC-0328 | Workflow Serialization (message serialization) |
| RFC-0329 | Workflow Compatibility (format compatibility) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/ipc-channel.json | IPC Channel JSON Schema |
| schemas/workflow/ipc-message.json | IPC Message JSON Schema |
| catalog/workflow-events.md | Event Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0327 (this document), RFC-0007 (Runtime IPC), RFC-0328 (Serialization) |

This specification IS responsible for: defining the workflow-layer IPC message taxonomy, specifying the IPC channel model, establishing reliability and ordering guarantees, and defining flow control and backpressure mechanisms.

This specification IS NOT responsible for: defining the Runtime IPC layer (RFC-0007), implementing transport protocols, or managing user identities.

| Dependency | Direction | Description |
|---|---|---|
| RFC-0007 | Consumed | Runtime IPC Architecture provides transport foundation |
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0304 | Consumed | Workflow Runtime provides execution context |
| RFC-0319 | Consumed | Workflow Security provides security model |
| RFC-0320 | Consumed | Workflow Performance provides performance requirements |
| RFC-0321 | Consumed | Workflow Observability provides IPC monitoring |
| RFC-0324 | Consumed | Workflow Storage provides message persistence |
| RFC-0328 | Consumed | Workflow Serialization provides message serialization |

- Workflow Runtime (RFC-0304): Uses IPC for component communication.
- Workflow Plugin Integration (RFC-0323): Uses IPC for plugin-host communication.

- IPC Channel Schema (schemas/workflow/ipc-channel.json): Provides channel format contract.
- IPC Message Schema (schemas/workflow/ipc-message.json): Provides message format contract.

- This specification MUST NOT depend on any specific transport protocol (gRPC, REST, WebSocket, etc.).
- This specification MUST NOT depend on any specific serialization format.

Workflow IPC MUST enforce the security model defined in RFC-0319: all endpoints authenticate, all messages encrypted, channels enforce permission boundaries.

- IPC message serialization MUST complete within 1ms for messages up to 1MB.
- IPC channel establishment MUST complete within 10ms.

- IPC message formats MUST be backward compatible within a major version.

- All IPC events MUST be recorded in the audit trail per RFC-0321.

- **Stream-based IPC**: Streaming channels for continuous data flow.
- **Cross-cluster IPC**: Protocol for IPC across distributed Atlas deployments.
- **Adaptive Reliability**: Dynamic reliability level negotiation.

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any specific network protocol (TCP, UDP, HTTP/2, QUIC, etc.)

## 9 References

| Reference | Description |
|---|---|
| RFC-0007 | Runtime IPC Architecture (transport foundation) |
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0304 | Workflow Runtime (execution context) |
| RFC-0312 | Workflow Scheduler (scheduling constraints) |
| RFC-0314 | Workflow Error Handling (error propagation) |
| RFC-0315 | Workflow Recovery (failure recovery) |
| RFC-0316 | Workflow Debugging (debug IPC) |
| RFC-0319 | Workflow Security (security model) |
| RFC-0320 | Workflow Performance (performance requirements) |
| RFC-0321 | Workflow Observability (IPC monitoring) |
| RFC-0324 | Workflow Storage (message persistence) |
| RFC-0328 | Workflow Serialization (message serialization) |
| RFC-0329 | Workflow Compatibility (format compatibility) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/ipc-channel.json | IPC Channel JSON Schema |
| schemas/workflow/ipc-message.json | IPC Message JSON Schema |
| catalog/workflow-events.md | Event Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0327 (this document), RFC-0007 (Runtime IPC), RFC-0328 (Serialization) |
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
