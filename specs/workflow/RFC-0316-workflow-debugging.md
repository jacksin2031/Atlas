RFC: RFC-0316
Title: Workflow Debugging
Status: Proposed
Version: 1.0.0
A
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Debug Operation | An action performed through the debugging interface for inspection or intervention. | RFC-0316 |
| Breakpoint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Watchpoint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Step Over | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Step Into | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Step Out | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Inspect | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Trace Point | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Diagnostic Context | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Debug Session | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
uthor: Atlas Specification Committee
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
  - RFC-0312 Workflow Scheduler
  - RFC-0313 Workflow Parallelism
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0317 Workflow Validation
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0320 Performance
  - RFC-0321 Workflow Observability
  - RFC-0322 Workflow Extension
  - RFC-0323 Plugin Integration
  - RFC-0324 Workflow Storage
  - RFC-0325 Workflow AI
  - RFC-0326 Workflow Vision
  - RFC-0327 Workflow IPC
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Related ADR: ADR-0012
Related JSON Schema: schemas/workflow/debugging.json
Related Catalog: catalog/workflow-debug-events.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Debugging specification defines the debugging model for Atlas workflows. Debugging enables operators to inspect, step through, and diagnose workflow execution at any point.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0316 workflow debugging.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined in RFC-0301 (Workflow Overview) and are used authoritatively throughout this specification:

| Term | Definition |
|---|---|
| Workflow | A declarative directed graph of nodes, edges, conditions, and triggers that defines orchestration intent. |
| Workflow Instance | A single execution of a workflow definition, with its own state, context, and lifecycle. |
| Node | An atomic unit of work within a workflow graph. |
| Edge | A directed connection between nodes representing data flow, control flow, or dependency. |
| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 |
| Variable | A named, typed value held in the workflow context. |
| Context | The immutable snapshot of variables, parameters, and resources at a given execution point. |
| Checkpoint | A deterministic save point capturing full execution state for resumption. |
| Deterministic | Producing identical results given identical inputs and execution conditions. |
| Idempotent | Producing the same effect regardless of how many times it is executed. |

Additional terms defined in this specification:

| Term | Definition |
|---|---|
| Debugger | An external tool or interface that attaches to a running workflow instance for inspection and control. |
| Debug Session | A continuous period of debugger attachment to a workflow instance, including all inspection and modification operations. |
| Breakpoint | A debugging marker that pauses workflow execution at a specified point (node, edge, condition, event, or variable). |
| Watchpoint | A breakpoint triggered by read or write access to a specific variable. |
| Stepping | The operation of advancing execution one logical unit at a time (node, edge, or statement). |
| Stack Frame | The execution context snapshot of a node invocation, including local variables and call chain. |
| Debug Event | A standardized event emitted by the debugging system for state changes, breakpoint hits, or inspection operations. |
| Replay | The deterministic re-execution of a recorded debug session for diagnostic analysis. |
| Inspection | The read-only observation of workflow state at a specific execution point. |
| Modification | The write operation that changes workflow state at a specific execution point during debugging. |

---

## 2 Debugging Overview

Key principles:

- Debuggers can attach to running workflow instances.
- Breakpoints can be set on nodes, edges, conditions, and events.
- Variable values can be inspected at any execution point.
- Execution can be stepped through node by node.
- Debug sessions are recorded for replay.
- Debugging operations MUST NOT alter the deterministic execution semantics of the workflow.

---

## 3 Debug Operations

| Operation | Description |
|---|---|
| Attach | Connect debugger to workflow instance |
| Detach | Disconnect debugger |
| Breakpoint | Set breakpoint on node, edge, condition, or event |
| Step Over | Execute current node, stop at next |
| Step Into | Enter sub-graph or called node |
| Step Out | Complete current node, stop at caller |
| Continue | Resume execution until next breakpoint |
| Inspect | View variable values at current execution point |
| Modify | Change variable values at current execution point |
| Replay | Re-execute from a checkpoint with debugger attached |

### 3.1 Attach

The Attach operation connects a debugger session to a running workflow instance. The implementation MUST verify that the debugger has appropriate authorization before granting access. The implementation MUST emit a debug event upon successful attachment.

### 3.2 Detach

The Detach operation disconnects the debugger session. The implementation MUST ensure that detachment does not affect the workflow execution state. The implementation MUST flush all pending debug session recordings before disconnection.

### 3.3 Breakpoint

The Breakpoint operation sets a marker that pauses workflow execution when reached. The implementation MUST support breakpoints on nodes, edges, conditions, events, and variables (see Section 4).

### 3.4 Step Over

The Step Over operation executes the current node to completion and pauses at the next execution point. The implementation MUST NOT interrupt nodes that are already executing; stepping applies only at node boundaries.

### 3.5 Step Into

The Step Into operation enters a sub-graph or called node for granular inspection. The implementation MUST preserve the call stack context and MUST provide stack frame navigation.

### 3.6 Step Out

The Step Out operation completes the current node and pauses at the caller. The implementation MUST restore the caller context and MUST record the node return value for inspection.

### 3.7 Continue

The Continue operation resumes workflow execution until the next breakpoint or instance completion. The implementation MUST honor all active breakpoints and MUST suspend execution immediately upon breakpoint hit.

### 3.8 Inspect

The Inspect operation provides read-only access to variable values, node states, and execution context at the current execution point. The implementation MUST present data consistent with the context snapshot at that point.

### 3.9 Modify

The Modify operation changes variable values at the current execution point. The implementation MUST validate modifications against the variable type system and MUST record all modifications in the debug session audit trail.

### 3.10 Replay

The Replay operation re-executes a recorded debug session deterministically. The implementation MUST produce identical state transitions as the original execution. Modifications made during the original session MAY be varied during replay for hypothesis testing.

---

## 4 Breakpoint Types

| Type | Description | Scope |
|---|---|---|
| Node | Triggered when a node starts or completes | Single node |
| Edge | Triggered when data flows along an edge | Single edge |
| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 | Single condition |
| Event | Triggered when a specific event is emitted | Single event type |
| Variable | Triggered when a variable is read or written | Single variable |

### 4.1 Node Breakpoints

Node breakpoints trigger on node start and node completion events. The implementation MUST distinguish between start and completion triggers and MUST allow separate configuration for each.

### 4.2 Edge Breakpoints

Edge breakpoints trigger when data flows along a specific edge. The implementation MUST capture the data payload at the time of the breakpoint for inspection.

### 4.3 Condition Breakpoints

Condition breakpoints trigger when a specific condition predicate is evaluated. The implementation MUST record the condition inputs and evaluation result at the time of the breakpoint.

### 4.4 Event Breakpoints

Event breakpoints trigger when a specific event type is emitted. The implementation MUST capture the full event payload for inspection.

### 4.5 Variable Breakpoints (Watchpoints)

Variable breakpoints trigger on read or write access to a specific variable. The implementation MUST record the variable value, access type (read/write), and the executing node at the time of the breakpoint.

---

## 5 Debug Session Recording

### 5.1 Recorded Data

Debug sessions record:

- All variable values at each step
- All state transitions
- All event emissions
- All resource allocations
- All timing information

### 5.2 Recording Format

- Each debug session MUST be recorded as a sequence of timestamped events.
- Events MUST conform to the debug event model defined in RFC-1001 and extended by the catalog entry workflow-debug-events.md.
- The recording MUST include the debugger attachment timestamp, all breakpoint hits, and the detachment timestamp.

### 5.3 Replay

Recorded sessions can be replayed:

1. Load the recorded session.
2. Replay state transitions in order.
3. Replay variable updates.
4. Replay event emissions.
5. Validate deterministic equivalence with the original execution.

### 5.4 Session Storage

- Debug session recordings MUST be stored with configurable retention policies.
- The implementation MUST support exporting debug sessions in a portable format for offline analysis.
- Debug session data MUST respect the same access control policies as the underlying workflow data.

---

## 6 Layer Boundaries

### 6.1 Responsibilities

- **This layer (Workflow Debugging)**: Defines debug operations, breakpoint types, session recording, and replay semantics.
- **Caller (Workflow Execution Engine, RFC-0303)**: Provides execution state for inspection and accepts stepping commands.
- **Caller (Workflow Scheduler, RFC-0312)**: Pauses and resumes scheduling based on debugger state.
- **Dependent (Workflow Recovery, RFC-0315)**: Uses debug session recordings to identify recovery-relevant state.
- **Dependent (Workflow Observability, RFC-0321)**: Emits debug metrics and session statistics.
- **Dependent (Workflow Error Handling, RFC-0314)**: Correlates debug sessions with error events for root cause analysis.

### 6.2 Non-Responsibilities

- This layer MUST NOT assume a specific thread model, process model, or concurrency primitive from any runtime implementation.
- This layer MUST NOT depend on a systems programming language, Node.js, a desktop application framework, a desktop application framework, an embedded database engine, the browser, or GPU resources.
- This layer MUST NOT define error categorization; error handling is defined in RFC-0314.
- This layer MUST NOT define recovery mechanics; recovery is defined in RFC-0315.
- This layer MUST NOT define parallelism semantics; parallelism is defined in RFC-0313.
- This layer MUST NOT define serialization formats; serialization is defined in RFC-0328.

### 6.3 Dependencies

| Direction | Dependency | Nature |
|---|---|---|
| Depends On | RFC-0303 Workflow Execution | Execution state access |
| Depends On | RFC-0312 Workflow Scheduler | Debugger-controlled scheduling |
| Depends On | RFC-0315 Workflow Recovery | Debug-relevant state identification |
| Depends On | RFC-1001 Common Event Model | Debug event emission |
| Depends On | RFC-1002 Common State Model | State inspection |
| Provided To | RFC-0314 Workflow Error Handling | Error correlation |
| Provided To | RFC-0315 Workflow Recovery | Recovery-relevant state |
| Provided To | RFC-0321 Workflow Observability | Debug metrics |

### 6.4 Forbidden Dependencies

- This layer MUST NOT depend on any subsystem-specific implementation (Plugin, Storage, Vision, AI, Marketplace, Knowledge).
- This layer MUST NOT depend on any runtime-specific library or framework.
- This layer MUST NOT assume network topology or distributed deployment.

---

## 7 Security

### 7.1 Security Requirements

- Debugger access MUST be authenticated and authorized. The implementation MUST enforce role-based access control for debugging operations.
- Variable modifications during debugging MUST NOT bypass sandbox boundaries. Modified values MUST still satisfy all declared type and constraint checks.
- Debug session recordings containing sensitive data MUST be encrypted at rest and MUST respect data classification policies.
- The implementation MUST prevent debugging operations from being used as a side-channel attack vector.

### 7.2 Security Controls

| Control | Requirement | Enforcement Point |
|---|---|---|
| Authentication | Debugger sessions require valid credentials | Attachment handler |
| Authorization | Role-based access to debugging operations | Debug manager |
| Sandbox Integrity | Modifications respect declared constraints | Variable validator |
| Data Encryption | Sensitive debug recordings encrypted at rest | Storage layer |
| Side-Channel Protection | Debug operations bounded in timing | Dispatcher |
| Audit Logging | All debug operations logged | Audit trail |

---

## 8 Performance

### 8.1 Performance Requirements

- The implementation MUST measure and expose debug session overhead as a metric (RFC-0321).
- Breakpoint evaluation MUST complete within 1ms without affecting workflow execution throughput.
- Debug session recording MUST be asynchronous and MUST NOT block workflow execution.
- The implementation MUST support concurrent debug sessions for the same workflow instance with bounded resource usage.

### 8.2 Performance Characteristics

| Metric | Requirement | Measurement |
|---|---|---|
| Breakpoint Evaluation | < 1ms | Latency test |
| Recording Overhead | Asynchronous, < 5% CPU | CPU usage test |
| Variable Inspection | < 10ms | Latency test |
| Session Attachment | < 100ms | Attachment test |
| Replay Speed | Real-time or faster | Playback test |

---

## 9 Compatibility

### 9.1 Compatibility Levels

| Level | Description | Requirement |
|---|---|---|
| Full | Identical debugging behavior | Same version |
| Forward | Older debug sessions readable by newer runtime | Backward compatible |
| Backward | Newer debug sessions readable by older runtime | Best-effort |
| Partial | Some debug operations unavailable | Feature flag |
| Incompatible | Debug session format differs | Version migration required |

### 9.2 Version Compatibility

- Debug session recordings created under one version of this specification MUST be readable by implementations of the same version.
- Implementations MUST support at least one prior minor version of debug session format for backward compatibility.
- Breaking changes to debug session formats MUST include a migration path.
- Breaking changes to debugging semantics MUST be communicated through the versioning process (RFC-0318).

---

## 10 Compliance

### 10.1 Compliance Requirements

- The implementation MUST log all debug operations for audit purposes.
- The implementation MUST enforce organizational debugging policies through compliance rules (RFC-0330).
- Debug session recordings containing regulated data MUST comply with data retention and privacy requirements.
- The implementation MUST support read-only debug modes that prevent variable modification for compliance-sensitive environments.

### 10.2 Audit Trail

- Every debug session MUST be recorded with start time, end time, attaching user, and operations performed.
- Every breakpoint hit MUST be recorded with type, location, and resulting state.
- Every variable modification MUST be recorded with the previous value, new value, and modifying operation.
- Audit records MUST conform to the event model defined in RFC-1001 and MUST be immutable.

---

## 11 Future Evolution

### 11.1 Planned Extensions

- Remote debugging: Support for debugger attachment over network connections.
- Collaborative debugging: Multiple debuggers attached to the same workflow instance with conflict resolution.
- AI-assisted debugging: Machine learning-based root cause analysis from debug session recordings.
- Visual debugging: Graphical representation of workflow state and execution flow for IDE integration.

### 11.2 Extension Points

- Custom breakpoint types MAY be registered through the extension model (RFC-0322).
- Custom debug event schemas MAY be defined through the serialization interface (RFC-0328).
- Custom debugging policies MAY be defined through the manifest extension (RFC-0310).

---

## 12 Runtime Independence

This specification is intentionally runtime-independent. The following assumptions are explicitly forbidden:

- This specification MUST NOT assume a specific programming language (a systems programming language, Node.js, Python, etc.).
- This specification MUST NOT assume a specific runtime environment (a desktop application framework, a desktop application framework, browser, native).
- This specification MUST NOT assume a specific database or persistence layer (an embedded database engine, a relational database, etc.).
- This specification MUST NOT assume a specific threading or process model (threads, async/await, actors, coroutines).
- This specification MUST NOT assume GPU acceleration or hardware-specific debugging primitives.
- This specification MUST NOT assume a particular operating system or kernel scheduling strategy.

Implementations MAY use any debugging model provided by their runtime, as long as the external behavior conforms to the deterministic, reproducible debugging model defined herein.

---

## 13 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Ten debug operations (Attach, Detach, Breakpoint, Step Over, Step Into, Step Out, Continue, Inspect, Modify, Replay) MUST be supported. | Operation enumeration test |
| AC-02 | Five breakpoint types (Node, Edge, Condition, Event, Variable) MUST be supported. | Breakpoint enumeration test |
| AC-03 | Five debug session recording fields (variable values, state transitions, event emissions, resource allocations, timing) MUST be defined. | Recording test |
| AC-04 | Debug session replay MUST produce deterministic equivalence with the original execution. | Determinism test |
| AC-05 | Breakpoint evaluation MUST complete within 1ms. | Latency test |
| AC-06 | Debugger access MUST be authenticated and authorized. | Authorization test |
| AC-07 | Variable modifications MUST respect sandbox boundaries and type constraints. | Constraint enforcement test |
| AC-08 | All debug operations MUST be logged in the audit trail. | Audit trail test |
| AC-09 | Debug session recordings MUST be exportable in a portable format. | Export test |
| AC-10 | Concurrent debug sessions MUST be supported with bounded resource usage. | Concurrency test |

---

## 14 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (Terminology authority) |
| RFC-0303 | Workflow Execution (Execution state access) |
| RFC-0304 | Workflow Runtime (Runtime model) |
| RFC-0310 | Workflow Manifest (Configuration) |
| RFC-0312 | Workflow Scheduler (Debugger-controlled scheduling) |
| RFC-0313 | Workflow Parallelism (Parallel execution visibility) |
| RFC-0314 | Workflow Error Handling (Error correlation) |
| RFC-0315 | Workflow Recovery (Recovery-relevant state) |
| RFC-0317 | Workflow Validation (Validation interface) |
| RFC-0318 | Workflow Versioning (Version management) |
| RFC-0320 | Performance (Performance requirements) |
| RFC-0321 | Workflow Observability (Debug metrics) |
| RFC-0322 | Workflow Extension (Extension model) |
| RFC-0328 | Workflow Serialization (Serialization) |
| RFC-0330 | Workflow Compliance (Compliance rules) |
| ADR-0012 | Contract-First Specification-Driven Development |
| RFC-1001 | Common Event Model |
| RFC-1002 | Common State Model |
| Catalog: workflow-debug-events.md | Debug event catalog |
| Schema: debugging.json | JSON Schema for debugging configuration |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |


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
