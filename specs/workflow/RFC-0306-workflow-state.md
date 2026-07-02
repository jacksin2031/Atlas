RFC: RFC-0306
Title: Workflow State
Status: Proposed
Version: 1.1.0
Auth
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Workflow State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Execution State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Node State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Edge State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| State Machine | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| State Transition | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Checkpoint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Snapshot | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Delta State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
or: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0006 Runtime State Management
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0307 Workflow Context
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
  - ADR-0012 (Contract-First Specification-Driven Development)
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0307 Workflow Context
  - RFC-0308 Workflow Events
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0324 Workflow Storage
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Related ADR: ADR-0012
Related JSON Schema: contracts/json/workflow.schema.json
Related Catalog: specs/workflow/catalog/workflow-state-types.md

---

## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow State specification defines the state model for workflow instances and nodes. State is the fundamental abstraction through which workflow execution is tracked, persisted, and recovered. The state model ensures that workflow execution is deterministic, resumable, and observable.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0306 workflow state.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined authoritatively in the [Atlas Master Glossary](../glossary.md) and MUST be interpreted consistently across all implementations:

| Term | Definition | Source |
|---|---|---|
| **Workflow** | A directed acyclic graph (DAG) defining a series of automation steps, inputs, outputs, and dependencies. | Glossary |
| **Workflow Instance** | A single execution of a workflow definition with concrete parameter bindings and runtime state. | RFC-0301 |
| **Node** | An atomic unit of work within a workflow DAG, representing a single action or group of actions. | RFC-0301 |
| **Context** | A transaction state container holding variables and metrics passed between executing tasks. | Glossary |
| **State Store** | The transaction-isolated database containing current configurations and runtime variables. | Glossary |
| **Checkpoint** | A saved snapshot of workflow state at a specific point, enabling recovery and resumption. | RFC-0315 |
| **Event Bus** | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| **Lifecycle** | The state transitions of a process or service from allocation to disposal. | Glossary |
| **Consistency** | The property that all state reads reflect the most recent committed write. | RFC-0301 |
| **Deterministic** | Producing the same output given the same input and state, without dependence on timing or external factors. | RFC-0301 |

### 1.1 Normative Language

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2 Layer Boundaries

### 2.1 Responsibilities

The Workflow State layer is responsible for:

- Defining the canonical state types for workflow instances, nodes, edges, variables, resources, and events.
- Specifying state persistence requirements and guarantees.
- Defining state transition rules and consistency models.
- Establishing checkpoint semantics and conflict resolution strategies.

### 2.2 Non-Responsibilities

The Workflow State layer MUST NOT:

- Define persistence storage engine implementations.
- Define state migration tools or scripts.
- Define serialization formats (deferred to RFC-0328).
- Manage state concurrency control beyond the consistency model.
- Specify garbage collection of historical state.

### 2.3 Dependencies

| Dependency | Direction | Rationale |
|---|---|---|
| RFC-0301 Workflow Overview | Consumes | Provides the overarching graph model |
| RFC-0304 Workflow Runtime | Consumes | Runtime provides the execution fabric |
| RFC-0305 Workflow Lifecycle | Consumes | Lifecycle defines state transition triggers |
| RFC-0307 Workflow Context | Consumes | Context provides variable management |
| RFC-0308 Workflow Events | Consumes | Events provide state change notifications |
| RFC-0315 Workflow Recovery | Consumes | Recovery provides checkpoint semantics |
| RFC-0324 Workflow Storage | Consumes | Storage provides persistence infrastructure |
| RFC-1002 Common State Model | Consumes | Common state provides base types |

### 2.4 Consumers

- RFC-0304 Workflow Runtime (state queries)
- RFC-0305 Workflow Lifecycle (state transitions)
- RFC-0315 Workflow Recovery (checkpoint management)
- RFC-0316 Workflow Debugging (state inspection)
- RFC-0321 Workflow Observability (state metrics)

### 2.5 Providers

- RFC-0301 Workflow Overview (graph model)
- RFC-1002 Common State Model (base types)
- RFC-0324 Workflow Storage (persistence infrastructure)

### 2.6 Forbidden Dependencies

The Workflow State layer MUST NOT depend on:

- Any runtime implementation technology (a systems programming language, Node.js, a desktop application framework, a desktop application framework).
- Any specific storage engine (an embedded database engine, a relational database, an in-memory data store, filesystem).
- Any operating system primitives (threads, processes, signals).
- Any GPU or hardware acceleration model.
- Any browser or presentation-layer technology.

---

## 3 State Model Overview

Workflow state encompasses:

- **Workflow instance state**: creation, execution, completion, termination.
- **Node state**: draft, validated, queued, pending, running, completed, failed, skipped, cancelled, terminated.
- **Edge state**: evaluated, traversed, broken.
- **Variable state**: declared, bound, resolved, updated.
- **Resource state**: available, allocated, released.
- **Event state**: emitted, consumed, acknowledged.

### 3.1 State Properties

Every state object MUST have:

- A unique identifier scoped to its state type.
- A version number for optimistic concurrency control.
- A timestamp of the last modification.
- A correlation ID linking to the originating workflow instance.
- A status indicator reflecting the current phase.

---

## 4 State Persistence

### 4.1 Persistence Requirements

All workflow state MUST be persistable:

| State Type | Persistence Location | Persistence Trigger |
|---|---|---|
| Workflow Instance | State store | Phase transition |
| Node State | State store | Node state change |
| Variable State | Execution context | Variable update |
| Resource State | Resource manager | Resource change |
| Event State | Event log | Event emission |

### 4.2 Persistence Guarantees

- State persistence MUST be atomic with state changes.
- State persistence MUST survive system failures as defined in RFC-0324.
- State persistence MUST be consistent with the execution graph.
- The state store MUST provide write-ahead logging (WAL) for crash recovery.

---

## 5 State Transitions

### 5.1 Transition Rules

State transitions follow these rules:

1. Transitions MUST be deterministic.
2. Transitions MUST be reversible within defined constraints.
3. Transitions MUST emit corresponding events as defined in RFC-0308.
4. Transitions MUST update the execution graph.
5. Transitions MUST be idempotent: reapplying the same transition MUST produce the same result.

### 5.2 Transition Matrix

State transitions are defined in RFC-0301 Section 11.2. Each transition MUST specify: preconditions, postconditions, side effects, and emitted events.

---

## 6 State Checkpointing

### 6.1 Checkpoint Types

| Type | Frequency | Content |
|---|---|---|
| Full | At workflow start | Complete state |
| Incremental | After each node | Node output state |
| Conditional | On significant change | Changed state only |

### 6.2 Checkpoint Requirements

- Checkpoints MUST capture all state needed for resumption as defined in RFC-0315.
- Checkpoints MUST be minimally sized for efficient storage.
- Checkpoints MUST be version-aware for compatibility as defined in RFC-0318.
- Checkpoint data MUST be tamper-evident using cryptographic hashing.

---

## 7 State Consistency

### 7.1 Consistency Model

Workflow state follows a strong consistency model:

- All state changes are serialized.
- State reads see the most recent write.
- State is consistent across all subsystems.
- The state store MUST provide serializable isolation as defined in RFC-0324.

### 7.2 Conflict Resolution

State conflicts are resolved through:

1. Last-write-wins for independent variables.
2. Merge functions for dependent variables.
3. Abort and retry for irreconcilable conflicts.

---

## 8 Security

### 8.1 State Security Controls

- State data at rest MUST be encrypted using the platform encryption policy.
- State read operations MUST require workflow.inspect permission.
- State write operations MUST require workflow.modify permission.
- Checkpoint data MUST be accessible only to the owning workflow instance and authorized administrators.
- State history MUST be immutable once committed.

### 8.2 Audit Trail

All state modifications MUST be recorded in an immutable audit log with: timestamp, actor, state type, operation, and correlation ID.

---

## 9 Performance

### 9.1 State Performance Requirements

- State read operations MUST complete within 5ms for in-memory state stores.
- State write operations MUST complete within 10ms for in-memory state stores.
- Checkpoint serialization MUST complete within 50ms per 100 nodes.
- State reconciliation after recovery MUST complete within 5s for standard-definition workflows.

### 9.2 Resource Constraints

- The state store MUST support at least 10,000 concurrent workflow instances.
- State data MUST NOT exceed 100MB per workflow instance including history.
- Checkpoint frequency MUST be configurable and MUST NOT degrade throughput by more than 5%.

---

## 10 Compatibility

### 10.1 State Format Compatibility

- State serialization formats MUST be versioned and MUST include a compatibility header.
- Older state formats MUST be readable by newer implementations (backward compatibility).
- New state fields MUST be optional and MUST have default values.
- Removed state fields MUST be migrated before the removal version is deployed.

### 10.2 Cross-Version Operations

- State transitions defined in older versions MUST remain valid in newer versions.
- State migration tools MUST be provided when breaking changes are introduced.

---

## 11 Compliance

### 11.1 Regulatory Compliance

- State audit trails MUST satisfy SOX Section 404 requirements for operational process logging.
- State data retention MUST comply with the platform data retention policy.
- Encrypted state at rest MUST use algorithms approved by the platform security policy.

### 11.2 Internal Policy Compliance

- All state modifications MUST be consistent with the Atlas Constitution Section 1 (Workflow Philosophy).
- State data classification MUST follow the platform data classification policy.
- State access MUST follow the principle of least privilege.

---

## 12 Future Evolution

### 12.1 Planned Extensions

- Event-sourced state models (append-only state logs) are planned for future versions.
- Distributed state replication (multi-datacenter consistency) is under consideration.
- Differential state compression (delta checkpoints) is exploratory.

### 12.2 Stability Guarantee

The state types and transition rules defined in this RFC are stable and MUST NOT change without a formal RFC revision cycle.

---

## 13 Runtime Independence

This specification makes NO assumptions about:

- **Implementation language**: No a systems programming language, Node.js, Python, Go, or any other language is required.
- **Runtime environment**: No a desktop application framework, a desktop application framework, browser, or desktop framework dependency.
- **Storage technology**: No an embedded database engine, a relational database, an in-memory data store, or any specific database is mandated.
- **Operating system**: No thread model, process model, signal handling, or OS-specific primitive is assumed.
- **Hardware**: No GPU, VRAM, CPU affinity, or hardware acceleration is required.
- **Network topology**: No specific network protocol or topology is assumed.

The state model is purely logical and data-structure based. Any implementation MAY use any technology stack to realize this specification.

---

## 14 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (graph model, philosophy) |
| RFC-0304 | Workflow Runtime (execution fabric) |
| RFC-0305 | Workflow Lifecycle (state transition triggers) |
| RFC-0307 | Workflow Context (variable management) |
| RFC-0308 | Workflow Events (state change notifications) |
| RFC-0312 | Workflow Scheduler (dispatch coordination) |
| RFC-0314 | Workflow Error Handling (failure state transitions) |
| RFC-0315 | Workflow Recovery (checkpoint and restart) |
| RFC-0316 | Workflow Debugging (state inspection) |
| RFC-0318 | Workflow Versioning (state version management) |
| RFC-0319 | Workflow Security (security controls) |
| RFC-0320 | Workflow Performance (performance metrics) |
| RFC-0321 | Workflow Observability (state metrics) |
| RFC-0324 | Workflow Storage (persistence infrastructure) |
| RFC-0328 | Workflow Serialization (data formats) |
| RFC-0329 | Workflow Compatibility (version compatibility) |
| RFC-0330 | Workflow Compliance (regulatory compliance) |
| RFC-1002 | Common State Model (base state types) |
| ADR-0012 | Contract-First Specification-Driven Development |
| JSON Schema | contracts/json/workflow.schema.json |
| Catalog | specs/workflow/catalog/workflow-state-types.md |
| Glossary | specs/glossary.md (Atlas Master Glossary) |


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
