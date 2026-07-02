RFC: RFC-0315
Title: Workflow Recovery
Status: Proposed
Version: 1.0.0
Auth
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Recovery Strategy | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Checkpoint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Restore Point | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Recovery Window | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| State Reconstruction | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compensating Transaction | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Rollback | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Forward Recovery | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Backward Recovery | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Partial Recovery | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
or: Atlas Specification Committee
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
  - RFC-0316 Workflow Debugging
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
Related JSON Schema: schemas/workflow/recovery.json
Related Catalog: catalog/workflow-recovery-types.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Recovery specification defines how workflow instances are recovered from failures. Recovery ensures that workflow execution can continue after transient failures, catastrophic crashes, or partial failures.

This specification IS the authoritative source for workflow recovery semantics. All other specifications that reference "Recovery" MUST defer to RFC-0315 for recovery strategy selection, checkpoint semantics, and resumption guarantees.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0315 workflow recovery.

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
| Side Effect | Any observable state change beyond the return value of a node execution. |
| Consistent State | A state in which all workflow invariants hold and no partial or corrupted data exists. |

Additional terms defined in this specification:

| Term | Definition |
|---|---|
| Recovery Strategy | A defined approach for restoring workflow execution after a failure (restart, resume, rollback, compensate, skip, abort). |
| Recovery Point Objective (RPO) | The maximum acceptable data loss measured in time or checkpoint distance. |
| Recovery Time Objective (RTO) | The maximum acceptable time between failure detection and resumption of execution. |
| Compensation Action | A designated operation that reverses or mitigates the side effects of a failed node execution. |
| Recovery Chain | The ordered sequence of recovery actions applied from failure detection through full resumption. |
| Checkpoint Consistency | The guarantee that a checkpoint represents a logically consistent state from which execution can safely resume. |
| Recovery Scope | The boundary of workflow state affected by a recovery operation (single node, branch, or entire instance). |

---

## 2 Recovery Overview

Key principles:

- Workflow instances are checkpointed at deterministic points.
- Checkpoints contain full execution state for resumption.
- Recovery strategies include restart, resume, rollback, compensate, skip, and abort.
- Recovery is transparent to the workflow definition.
- Recovery MUST restore a consistent state before resuming execution.

---

## 3 Recovery Strategies

| Strategy | Description | When Used |
|---|---|---|
| Restart | Restart from the beginning | Catastrophic failure |
| Resume | Resume from last checkpoint | Normal recovery |
| Rollback | Rollback to a previous state | Data corruption detected |
| Compensate | Execute compensating actions | Partial failure |
| Skip | Skip failed node and continue | Non-critical node failure |
| Abort | Terminate workflow | Unrecoverable failure |

### 3.1 Restart

The Restart strategy re-executes the entire workflow from the initial checkpoint. The implementation MUST clear all execution state and re-initialize from the workflow definition. Restart is used when the failure affects the global execution context.

### 3.2 Resume

The Resume strategy restores execution from the most recent consistent checkpoint. The implementation MUST verify checkpoint consistency before resuming and MUST NOT re-execute any nodes that completed successfully.

### 3.3 Rollback

The Rollback strategy reverts the workflow state to a specified prior checkpoint. The implementation MUST execute compensations for all side effects produced between the target checkpoint and the failure point.

### 3.4 Compensate

The Compensate strategy executes designated compensating actions for failed nodes with side effects. The implementation MUST execute compensations in reverse order of the original node execution.

### 3.5 Skip

The Skip strategy bypasses the failed node and continues execution of unaffected downstream nodes. The implementation MUST verify that skipping the node does not violate any critical data or control dependencies.

### 3.6 Abort

The Abort strategy terminates the workflow instance and executes all pending compensations. The implementation MUST ensure that all side effects are either compensated or committed before termination.

---

## 4 Checkpoint Model

### 4.1 Checkpoint Contents

Checkpoints contain:

- Execution context (variables, parameters, resources)
- Node states (all node current states)
- Edge evaluations (all edge evaluation results)
- Pending actions (actions not yet completed)
- Event queue (unsent events)

### 4.2 Checkpoint Consistency Guarantees

- Every checkpoint MUST represent a consistent state. No checkpoint MAY contain partial node execution results.
- Checkpoints MUST be written atomically. A checkpoint is either fully committed or fully absent; partial checkpoints MUST NOT exist.
- The implementation MUST verify checkpoint integrity before using it for recovery.

### 4.3 Checkpoint Frequency

| Type | Frequency | Overhead |
|---|---|---|
| Full | At workflow start | High |
| Incremental | After each node | Low |
| Conditional | On state change | Medium |

### 4.4 Checkpoint Selection

- The implementation MUST select the most recent consistent checkpoint for resume operations.
- For rollback operations, the implementation MUST locate the nearest checkpoint preceding the corruption point.
- The implementation MUST support checkpoint pruning to manage storage, retaining only checkpoints within the configured RPO window.

---

## 5 Recovery Process

### 5.1 Recovery Steps

1. Detect failure through error event or health check.
2. Load the most recent consistent checkpoint.
3. Verify checkpoint integrity and consistency.
4. Restore the execution context from the checkpoint.
5. Re-evaluate all pending conditions against restored state.
6. Re-dispatch pending nodes respecting dependency order.
7. Resume execution from the restored state.

### 5.2 Recovery Constraints

- Recovery MUST restore a consistent state.
- Recovery MUST not re-execute completed nodes.
- Recovery MUST execute compensations for failed nodes with side effects.
- The implementation MUST ensure that all compensations complete before resuming forward execution.
- The implementation MUST emit a recovery event upon successful state restoration.

### 5.3 Failure Detection

- The implementation MUST detect failures through error events emitted by the error handling system (RFC-0314).
- The implementation MUST detect failures through health check timeouts on long-running nodes.
- The implementation MUST detect failures through checkpoint corruption or integrity verification failures.

---

## 6 Recovery Types

### 6.1 Recovery Type Classification

| Type | Description | Scope |
|---|---|---|
| Node-Level | Recovery of a single failed node | Single node |
| Branch-Level | Recovery of an entire parallel branch | Branch |
| Instance-Level | Recovery of the entire workflow instance | Whole instance |
| Cross-Instance | Recovery using state from another instance | Cross-instance |

### 6.2 Node-Level Recovery

Node-level recovery attempts to recover a single failed node using retry or skip strategies. The implementation MUST preserve the state of all unaffected nodes.

### 6.3 Branch-Level Recovery

Branch-level recovery recovers an entire parallel branch from the last branch-level checkpoint. The implementation MUST re-execute all nodes in the branch that have not completed successfully.

### 6.4 Instance-Level Recovery

Instance-level recovery restores the entire workflow instance from a global checkpoint. The implementation MUST clear all execution state and re-initialize from the selected checkpoint.

### 6.5 Cross-Instance Recovery

Cross-instance recovery uses state from a related workflow instance as a recovery source. The implementation MUST verify that the source instance state is consistent and compatible.

---

## 7 Layer Boundaries

### 7.1 Responsibilities

- **This layer (Workflow Recovery)**: Defines recovery strategies, checkpoint model, recovery process, failure detection, and recovery type classification.
- **Caller (Workflow Execution Engine, RFC-0303)**: Initiates recovery upon failure notification.
- **Caller (Workflow Error Handling, RFC-0314)**: Provides error context for recovery strategy selection.
- **Dependent (Workflow Scheduler, RFC-0312)**: Re-schedules recovered nodes according to dependency order.
- **Dependent (Workflow Debugging, RFC-0316)**: Records recovery events for diagnostic replay.
- **Dependent (Workflow Observability, RFC-0321)**: Emits recovery metrics and RPO/RTO measurements.

### 7.2 Non-Responsibilities

- This layer MUST NOT assume a specific thread model, process model, or concurrency primitive from any runtime implementation.
- This layer MUST NOT depend on a systems programming language, Node.js, a desktop application framework, a desktop application framework, an embedded database engine, the browser, or GPU resources.
- This layer MUST NOT define error categorization; error handling is defined in RFC-0314.
- This layer MUST NOT define parallelism semantics; parallelism is defined in RFC-0313.
- This layer MUST NOT define debugging interfaces; debugging is defined in RFC-0316.
- This layer MUST NOT define serialization formats; serialization is defined in RFC-0328.

### 7.3 Dependencies

| Direction | Dependency | Nature |
|---|---|---|
| Depends On | RFC-0303 Workflow Execution | Execution model contract |
| Depends On | RFC-0312 Workflow Scheduler | Re-scheduling after recovery |
| Depends On | RFC-0313 Workflow Parallelism | Branch-level recovery |
| Depends On | RFC-0314 Workflow Error Handling | Error context for recovery |
| Depends On | RFC-1001 Common Event Model | Recovery event emission |
| Depends On | RFC-1002 Common State Model | State restoration |
| Provided To | RFC-0312 Workflow Scheduler | Recovery-triggered rescheduling |
| Provided To | RFC-0316 Workflow Debugging | Recovery event recording |
| Provided To | RFC-0321 Workflow Observability | Recovery metrics |

### 7.4 Forbidden Dependencies

- This layer MUST NOT depend on any subsystem-specific implementation (Plugin, Storage, Vision, AI, Marketplace, Knowledge).
- This layer MUST NOT depend on any runtime-specific library or framework.
- This layer MUST NOT assume network topology or distributed deployment.

---

## 8 Security

### 8.1 Security Requirements

- Checkpoint data MUST be encrypted at rest to protect sensitive workflow state.
- Recovery operations MUST verify the integrity of checkpoint data using cryptographic hashes.
- Unauthorized recovery attempts MUST be rejected and logged.
- Compensating actions MUST respect the same sandbox and access control boundaries as the original node execution.

### 8.2 Security Controls

| Control | Requirement | Enforcement Point |
|---|---|---|
| Checkpoint Encryption | Checkpoints encrypted at rest | Checkpoint writer |
| Integrity Verification | Cryptographic hash verification | Checkpoint reader |
| Access Control | Only authorized entities trigger recovery | Recovery manager |
| Compensation Sandboxing | Compensations enforce sandbox policies | Execution engine |
| Audit Logging | All recovery events logged | Audit trail |

---

## 9 Performance

### 9.1 Performance Requirements

- The implementation MUST measure and expose recovery time as a metric (RFC-0321).
- Checkpoint write operations MUST complete within 100ms for incremental checkpoints.
- Checkpoint restore operations MUST complete within 500ms for typical workflow states.
- The implementation MUST support configurable RPO and RTO targets per workflow instance.

### 9.2 Performance Characteristics

| Metric | Requirement | Measurement |
|---|---|---|
| Incremental Checkpoint Write | < 100ms | Write latency test |
| Checkpoint Restore | < 500ms | Restore latency test |
| Recovery Decision | < 50ms | Decision latency test |
| Compensation Execution | Per-node SLA | Compensation test |
| Checkpoint Pruning | Background, < 1s | Pruning test |

---

## 10 Compatibility

### 10.1 Compatibility Levels

| Level | Description | Requirement |
|---|---|---|
| Full | Identical recovery behavior | Same version |
| Forward | Older checkpoints usable by newer runtime | Backward compatible |
| Backward | Newer checkpoints usable by older runtime | Best-effort |
| Partial | Some recovery strategies unavailable | Feature flag |
| Incompatible | Checkpoint format differs | Version migration required |

### 10.2 Version Compatibility

- Checkpoints created under one version of this specification MUST be restorable by implementations of the same version.
- Implementations MUST support at least one prior minor version of checkpoint format for backward compatibility.
- Checkpoint format changes MUST include a migration path and MUST NOT invalidate existing checkpoints.
- Breaking changes to recovery semantics MUST be communicated through the versioning process (RFC-0318).

---

## 11 Compliance

### 11.1 Compliance Requirements

- The implementation MUST enforce RPO and RTO compliance for all workflow instances.
- The implementation MUST log all recovery operations for audit purposes.
- The implementation MUST support organizational recovery policies through compliance rules (RFC-0330).
- Recovery operations affecting regulated data MUST comply with data retention and privacy requirements.

### 11.2 Audit Trail

- Every recovery event MUST be recorded with strategy used, checkpoint selected, nodes recovered, and duration.
- Every checkpoint operation MUST be recorded with timestamp, size, and integrity hash.
- Every compensation action MUST be recorded with the original node ID and compensation result.
- Audit records MUST conform to the event model defined in RFC-1001 and MUST be immutable.

---

## 12 Future Evolution

### 12.1 Planned Extensions

- Predictive recovery: Proactive checkpointing triggered by anomaly detection in execution patterns.
- Multi-region recovery: Cross-datacenter checkpoint replication for geographic disaster recovery.
- Automated recovery policy optimization: Machine learning-assisted tuning of RPO/RTO parameters.
- Incremental checkpoint deltas: Storage-efficient checkpoint representation using differential encoding.

### 12.2 Extension Points

- Custom recovery strategies MAY be registered through the extension model (RFC-0322).
- Custom checkpoint formats MAY be supported through the serialization interface (RFC-0328).
- Custom recovery policies MAY be defined through the manifest extension (RFC-0310).

---

## 13 Runtime Independence

This specification is intentionally runtime-independent. The following assumptions are explicitly forbidden:

- This specification MUST NOT assume a specific programming language (a systems programming language, Node.js, Python, etc.).
- This specification MUST NOT assume a specific runtime environment (a desktop application framework, a desktop application framework, browser, native).
- This specification MUST NOT assume a specific database or persistence layer (an embedded database engine, a relational database, etc.).
- This specification MUST NOT assume a specific threading or process model (threads, async/await, actors, coroutines).
- This specification MUST NOT assume GPU acceleration or hardware-specific checkpoint primitives.
- This specification MUST NOT assume a particular operating system or kernel scheduling strategy.

Implementations MAY use any persistence model provided by their runtime, as long as the external behavior conforms to the deterministic, consistent recovery model defined herein.

---

## 14 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Six recovery strategies (Restart, Resume, Rollback, Compensate, Skip, Abort) MUST be supported. | Strategy enumeration test |
| AC-02 | Five checkpoint contents (context, node states, edge evaluations, pending actions, event queue) MUST be defined. | Checkpoint content test |
| AC-03 | Three checkpoint frequencies (Full, Incremental, Conditional) MUST be supported. | Frequency test |
| AC-04 | Seven recovery steps MUST be enforced in order. | Recovery process test |
| AC-05 | Checkpoint writes MUST complete within 100ms for incremental checkpoints. | Write latency test |
| AC-06 | Checkpoint restores MUST complete within 500ms for typical workflow states. | Restore latency test |
| AC-07 | The implementation MUST enforce checkpoint consistency: no partial checkpoints MAY exist. | Consistency test |
| AC-08 | The implementation MUST verify checkpoint integrity using cryptographic hashes. | Integrity test |
| AC-09 | All recovery operations MUST be recorded in the audit trail. | Audit trail test |
| AC-10 | Four recovery types (Node-Level, Branch-Level, Instance-Level, Cross-Instance) MUST be supported. | Recovery type test |

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (Terminology authority) |
| RFC-0303 | Workflow Execution (Execution model contract) |
| RFC-0304 | Workflow Runtime (Runtime model) |
| RFC-0310 | Workflow Manifest (Configuration) |
| RFC-0312 | Workflow Scheduler (Re-scheduling after recovery) |
| RFC-0313 | Workflow Parallelism (Branch-level recovery) |
| RFC-0314 | Workflow Error Handling (Error context for recovery) |
| RFC-0316 | Workflow Debugging (Recovery event recording) |
| RFC-0317 | Workflow Validation (Validation interface) |
| RFC-0318 | Workflow Versioning (Version management) |
| RFC-0320 | Performance (Performance requirements) |
| RFC-0321 | Workflow Observability (Recovery metrics) |
| RFC-0322 | Workflow Extension (Extension model) |
| RFC-0328 | Workflow Serialization (Checkpoint serialization) |
| RFC-0330 | Workflow Compliance (Compliance rules) |
| ADR-0012 | Contract-First Specification-Driven Development |
| RFC-1001 | Common Event Model |
| RFC-1002 | Common State Model |
| RFC-1006 | Common Error Model |
| Catalog: workflow-recovery-types.md | Recovery type catalog |
| Schema: recovery.json | JSON Schema for recovery configuration |
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
