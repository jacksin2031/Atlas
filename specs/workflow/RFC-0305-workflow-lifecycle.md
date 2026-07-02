RFC: RFC-0305
Title: Workflow Lifecycle
Status: Proposed
Version: 1.1.0
Aut
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Lifecycle State | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| State Transition | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Lifecycle Hook | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Bootstrap Phase | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Shutdown Phase | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Drain Period | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Grace Period | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Recovery Window | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
hor: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0306 Workflow State
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
  - RFC-0306 Workflow State
  - RFC-0307 Workflow Context
  - RFC-0308 Workflow Events
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0317 Workflow Validation
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Related ADR: ADR-0012
Related JSON Schema: contracts/json/workflow.schema.json
Related Catalog: specs/workflow/catalog/workflow-lifecycle.md

---

## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Lifecycle specification defines the state transitions and lifecycle management model for workflow instances and individual nodes within Atlas workflows. The lifecycle model ensures that every workflow instance progresses through well-defined phases from creation to termination.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0305 workflow lifecycle.

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
| **Scheduler** | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | Glossary |
| **Event Bus** | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| **State Store** | The transaction-isolated database containing current configurations and runtime variables. | Glossary |
| **Lifecycle** | The state transitions of a process or service from allocation to disposal. | Glossary |
| **Checkpoint** | A saved snapshot of workflow state at a specific point, enabling recovery and resumption. | RFC-0315 |
| **Compensation** | An action that reverses the effect of a previously completed action, used for rollback semantics. | RFC-0314 |
| **Watchdog** | The monitoring service checking heartbeats of registered services to initiate recovery routines. | Glossary |
| **Runtime** | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | Glossary |

### 1.1 Normative Language

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2 Layer Boundaries

### 2.1 Responsibilities

The Workflow Lifecycle layer is responsible for:

- Defining the canonical state machine for workflow instances and nodes.
- Specifying lifecycle transition rules and invariants.
- Defining creation, initialization, termination, cancellation, pausing, resuming, and restart semantics.
- Providing the contract for checkpoint and compensation actions.

### 2.2 Non-Responsibilities

The Workflow Lifecycle layer MUST NOT:

- Define execution scheduling algorithms (deferred to RFC-0312).
- Define error handling strategies (deferred to RFC-0314).
- Define recovery procedures (deferred to RFC-0315).
- Define debugging instrumentation (deferred to RFC-0316).
- Manage resource allocation (deferred to RFC-0009).
- Specify persistence storage engines.

### 2.3 Dependencies

| Dependency | Direction | Rationale |
|---|---|---|
| RFC-0301 Workflow Overview | Consumes | Provides the overarching graph model and philosophy |
| RFC-0304 Workflow Runtime | Consumes | Runtime provides the execution fabric |
| RFC-0306 Workflow State | Consumes | State model provides the data representation |
| RFC-0307 Workflow Context | Consumes | Context provides variable and parameter management |
| RFC-0308 Workflow Events | Consumes | Events provide lifecycle transition notifications |
| RFC-0312 Workflow Scheduler | Consumes | Scheduler provides dispatch and queuing |
| RFC-0315 Workflow Recovery | Consumes | Recovery provides checkpoint and restart semantics |
| RFC-0314 Workflow Error Handling | Consumes | Error handling provides failure semantics |
| RFC-1002 Common State Model | Consumes | Common state provides base state types |

### 2.4 Consumers

- RFC-0304 Workflow Runtime (execution fabric)
- RFC-0312 Workflow Scheduler (dispatch coordination)
- RFC-0315 Workflow Recovery (checkpoint management)
- RFC-0316 Workflow Debugging (inspection points)
- All subsystem teams implementing workflow-driven operations

### 2.5 Providers

- RFC-0301 Workflow Overview (graph model)
- RFC-0306 Workflow State (state representation)
- RFC-1002 Common State Model (base types)

### 2.6 Forbidden Dependencies

The Workflow Lifecycle layer MUST NOT depend on:

- Any runtime implementation technology (a systems programming language, Node.js, a desktop application framework, a desktop application framework).
- Any specific storage backend (an embedded database engine, a relational database, an in-memory data store).
- Any operating system primitives (threads, processes, signals).
- Any GPU or hardware acceleration model.
- Any browser or presentation-layer technology.

---

## 3 Workflow Instance Lifecycle

### 3.1 Instance States

A workflow instance transitions through the following states:

| State | Description | Transitions From | Transitions To |
|---|---|---|---|
| Created | Instance is created but not yet initialized | Instantiation | Initialized, Failed |
| Initialized | Instance is initialized and ready | Created | Queued, Failed |
| Queued | Instance is in the execution queue | Initialized | Running, Cancelled |
| Running | Instance is actively executing | Queued | Completed, Failed, Paused |
| Paused | Instance execution is suspended | Running | Resumed, Cancelled |
| Resumed | Suspended instance is restarted | Paused | Running |
| Completed | Instance execution completed successfully | Running | Terminated |
| Failed | Instance execution failed | Running, Queued | Terminated, Recovering |
| Recovering | Instance is being recovered from failure | Failed | Running, Terminated |
| Terminated | Instance lifecycle is complete | All terminal states | Final |
| Cancelled | Instance execution was cancelled | Any non-terminal | Terminated |

### 3.2 Lifecycle Transitions

Lifecycle transitions are depicted in the state diagram defined in RFC-0301 Section 11. Every transition MUST emit a corresponding event as defined in RFC-0308. Transitions MUST be atomic with respect to the workflow instance state store.

---

## 4 Node Lifecycle

### 4.1 Node States

Individual nodes within a workflow follow the lifecycle defined in RFC-0301 Section 11. Node states are a subset of the instance state machine, constrained by dependency ordering and execution budget.

### 4.2 Node Lifecycle Rules

1. A node MUST NOT execute before all its dependencies are satisfied.
2. A node MUST be marked as completed, failed, or skipped before dependent nodes can execute.
3. A node that fails MAY be retried according to its retry policy as defined in RFC-0314.
4. A node that requires compensation MUST execute its compensation action before the workflow can terminate.

---

## 5 Workflow Creation

### 5.1 Creation Process

Workflow instance creation involves:

1. Parsing the workflow definition.
2. Validating the workflow graph against the schema defined in contracts/json/workflow.schema.json.
3. Creating the execution context as defined in RFC-0307.
4. Binding parameters to default or provided values.
5. Allocating initial resources.
6. Creating the execution graph from the workflow graph.

### 5.2 Creation Requirements

| Requirement | Description | Enforcement |
|---|---|---|
| Valid Definition | Workflow definition MUST pass validation | Validation phase |
| Bound Parameters | All required parameters MUST be bound | Initialization phase |
| Available Resources | Required resources MUST be available | Initialization phase |
| Permission | Initiator MUST have workflow creation permission | Security check |

---

## 6 Workflow Initialization

### 6.1 Initialization Steps

Workflow initialization prepares the execution environment:

1. Create the execution context with all variables.
2. Bind all parameters to concrete values.
3. Allocate declared resources.
4. Register event handlers.
5. Initialize error handlers.
6. Set up observability hooks.
7. Create the initial execution graph.

### 6.2 Initialization Failure

If initialization fails:

- The workflow instance enters a failed state.
- The failure reason is recorded.
- Allocated resources are released.
- An initialization failure event is emitted.

---

## 7 Workflow Termination

### 7.1 Termination Types

| Type | Description | Condition |
|---|---|---|
| Normal | All exit nodes completed successfully | All paths complete |
| Error | Execution failed unrecoverably | Unrecoverable error |
| Cancelled | Execution was manually cancelled | Cancel request |
| Timeout | Execution exceeded the timeout | Timeout reached |
| Budget | Execution exceeded the budget | Budget violation |
| Compensation | Compensation was required and completed | Compensation required |

### 7.2 Termination Process

Termination involves:

1. Marking all running nodes as terminated.
2. Executing any pending compensations.
3. Releasing all resources.
4. Flushing observability data.
5. Persisting the final state.
6. Emitting a termination event.

---

## 8 Workflow Pausing and Resuming

### 8.1 Pausing

A workflow instance MAY be paused at any time:

- Pausing suspends all node execution.
- Pausing preserves the full execution context.
- Pausing is recorded in the audit trail.

### 8.2 Resuming

A paused workflow instance MAY be resumed:

- Resuming restores the execution context from the pause point.
- Resumed execution continues from where it was paused.
- Resumption does not affect node state (nodes are not re-executed).

---

## 9 Workflow Cancellation

### 9.1 Cancellation Process

Cancellation terminates a workflow instance immediately:

1. All running nodes are marked as cancelled.
2. All pending nodes are removed from the queue.
3. Compensation actions are executed for completed nodes.
4. Resources are released.
5. A cancellation event is emitted.

### 9.2 Cancellation Constraints

- Cancellation of a running workflow MUST be atomic.
- Cancellation cannot be undone once completed.
- Compensating actions MUST complete before the workflow enters the terminated state.

---

## 10 Workflow Restart

### 10.1 Restart Types

| Type | Description | Starting Point |
|---|---|---|
| Full Restart | Restart from the beginning | Entry node |
| Checkpoint Restart | Restart from the last checkpoint | Last checkpoint |
| Node Restart | Restart from a specific node | Specified node |

### 10.2 Restart Constraints

- Restarts are subject to the same validation as initial creation.
- Parameter values from the original execution are preserved unless overridden.
- Restart history is recorded in the audit trail.

---

## 11 Security

### 11.1 Lifecycle Security Controls

- Workflow creation MUST require authorization from the initiator identity.
- Lifecycle state transitions MUST be auditable.
- Cancellation of a running workflow MUST require the same permission level as creation.
- Checkpoint data MUST be encrypted at rest using the platform encryption policy.
- Restart operations MUST validate that the original parameter bindings are still compatible with the current system state.

### 11.2 Access Control

| Operation | Required Permission | Enforced At |
|---|---|---|
| Create | workflow.create | Creation phase |
| Pause | workflow.pause | Running phase |
| Resume | workflow.resume | Paused phase |
| Cancel | workflow.cancel | Any non-terminal phase |
| Restart | workflow.restart | Terminal phase |
| Inspect | workflow.inspect | Any phase |

### 11.3 Audit Trail

All lifecycle transitions MUST be recorded in an immutable audit log. Each entry MUST contain: timestamp, initiating entity, transition type, source state, target state, and correlation ID.

---

## 12 Performance

### 12.1 Lifecycle Performance Requirements

- State transition operations MUST complete within 10ms for in-memory state stores.
- Checkpoint creation MUST complete within 100ms for workflows with fewer than 100 nodes.
- Workflow initialization MUST complete within 1s for standard-definition workflows.
- Cancellation propagation MUST reach all nodes within 500ms.

### 12.2 Resource Constraints

- The lifecycle engine MUST NOT hold more than 10MB of state data per workflow instance in memory.
- Checkpoint frequency MUST be configurable and MUST NOT exceed one checkpoint per 100 nodes processed.
- The state store MUST support concurrent reads without blocking writes.

---

## 13 Compatibility

### 13.1 Version Compatibility

- Lifecycle state machines MUST remain backward-compatible within a major version.
- New states MAY be added in minor versions but MUST NOT alter existing transition rules.
- Deprecated states MUST remain recognized but MUST NOT be entered by default.
- State transition tables MUST be versioned alongside the workflow definition.

### 13.2 Interoperability

- Lifecycle events emitted by one implementation MUST be consumable by any conformant implementation.
- Checkpoint formats MUST include a version field to enable cross-version compatibility.
- Workflow definitions targeting older lifecycle versions MUST be validated for compatibility before execution.

---

## 14 Compliance

### 14.1 Regulatory Compliance

- Lifecycle audit trails MUST satisfy SOX Section 404 requirements for operational process logging.
- Workflow termination records MUST be retained for a minimum of 7 years.
- Cancellation events MUST include a justification field for compliance reporting.

### 14.2 Internal Policy Compliance

- All lifecycle transitions MUST be consistent with the Atlas Constitution Section 1 (Workflow Philosophy).
- Checkpoint encryption MUST comply with the platform data protection policy.
- Resource release on termination MUST be verified before the termination event is emitted.

---

## 15 Future Evolution

### 15.1 Planned Extensions

- Hierarchical workflow instances (nested lifecycles) are planned for a future version.
- Distributed lifecycle coordination (multi-runtime instances) is under consideration.
- Machine learning-based lifecycle optimization (predictive checkpointing) is exploratory.

### 15.2 Stability Guarantee

The lifecycle state machine defined in this RFC is stable and MUST NOT change without a formal RFC revision cycle. Any extension to the state machine MUST be additive only and MUST NOT invalidate existing workflow definitions.

---

## 16 Runtime Independence

This specification makes NO assumptions about:

- **Implementation language**: No a systems programming language, Node.js, Python, Go, or any other language is required.
- **Runtime environment**: No a desktop application framework, a desktop application framework, browser, or desktop framework dependency.
- **Storage technology**: No an embedded database engine, a relational database, an in-memory data store, or any specific database is mandated.
- **Operating system**: No thread model, process model, signal handling, or OS-specific primitive is assumed.
- **Hardware**: No GPU, VRAM, CPU affinity, or hardware acceleration is required.
- **Network topology**: No specific network protocol or topology is assumed.

The lifecycle model is purely logical and state-machine based. Any implementation MAY use any technology stack to realize this specification.

---

## 17 Acceptance Criteria

### 17.1 Lifecycle

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST support eleven workflow instance states as defined in Section 3.1. | State enumeration test |
| AC-02 | The implementation MUST define and validate all state transitions. | Transition table verification |
| AC-03 | The implementation MUST validate definition, parameters, resources, and permissions during creation. | Creation test |
| AC-04 | The implementation MUST perform all seven initialization steps in Section 6.1. | Initialization test |
| AC-05 | The implementation MUST support six termination types as defined in Section 7.1. | Termination test |
| AC-06 | The implementation MUST preserve full execution context during pausing and resuming. | Pause-resume test |
| AC-07 | The implementation MUST enforce atomic cancellation as defined in Section 9.2. | Cancellation test |
| AC-08 | The implementation MUST support three restart types as defined in Section 10.1. | Restart test |

### 17.2 State

| # | Criterion | Verification Method |
|---|---|---|
| AC-09 | The implementation MUST enforce the node lifecycle state machine defined in RFC-0301. | Node lifecycle test |
| AC-10 | The implementation MUST enforce four node lifecycle rules as defined in Section 4.2. | Rule enforcement test |

---

## 18 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (graph model, philosophy) |
| RFC-0304 | Workflow Runtime (execution fabric) |
| RFC-0306 | Workflow State (state representation) |
| RFC-0307 | Workflow Context (variable management) |
| RFC-0308 | Workflow Events (transition notifications) |
| RFC-0312 | Workflow Scheduler (dispatch and queuing) |
| RFC-0314 | Workflow Error Handling (failure semantics) |
| RFC-0315 | Workflow Recovery (checkpoint and restart) |
| RFC-0316 | Workflow Debugging (inspection points) |
| RFC-0317 | Workflow Validation (definition validation) |
| RFC-0318 | Workflow Versioning (version management) |
| RFC-0319 | Workflow Security (security controls) |
| RFC-0320 | Workflow Performance (performance metrics) |
| RFC-0321 | Workflow Observability (monitoring) |
| RFC-0329 | Workflow Compatibility (version compatibility) |
| RFC-0330 | Workflow Compliance (regulatory compliance) |
| RFC-1002 | Common State Model (base state types) |
| ADR-0012 | Contract-First Specification-Driven Development |
| JSON Schema | contracts/json/workflow.schema.json |
| Catalog | specs/workflow/catalog/workflow-lifecycle.md |
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
