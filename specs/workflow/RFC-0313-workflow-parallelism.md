RFC: RFC-0313
Title: Workflow Parallelism
Status: Proposed
Version: 1.0.0
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Fan-Out | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Fan-In | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Pipeline | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Barrier | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Synchronization Point | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Parallelism Degree | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Concurrency Limit | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Task Parallelism | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Data Parallelism | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Pipeline Parallelism | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---

Author: Atlas Specification Committee
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
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
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
Related JSON Schema: schemas/workflow/parallelism.json
Related Catalog: catalog/workflow-capabilities.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Parallelism specification defines the parallel execution model for Atlas workflows. Parallel execution enables independent nodes to execute concurrently, improving throughput and reducing overall execution time.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0313 workflow parallelism.

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
| Parallelism | The execution of multiple nodes concurrently within a single workflow instance. |
| Concurrency | The overlapping execution of nodes, whether truly simultaneous or interleaved. |
| Deterministic | Producing identical results given identical inputs and execution conditions. |
| Idempotent | Producing the same effect regardless of how many times it is executed. |
| Side Effect | Any observable state change beyond the return value of a node execution. |
| Race Condition | A behavior dependent on the relative timing of concurrent events. |
| Barrier | A synchronization point where all parallel branches must arrive before proceeding. |
| Fan-Out | The pattern of dispatching multiple parallel child executions from a single parent. |
| Fan-In | The pattern of collecting results from multiple parallel child executions. |

Additional terms defined in this specification:

| Term | Definition |
|---|---|
| Parallelism Domain | A bounded set of nodes authorized to execute concurrently under shared resource constraints. |
| Parallelism Bound | A configurable limit on concurrent execution (depth, breadth, or resource count). |
| Dependency Frontier | The boundary between ready-to-execute nodes and nodes awaiting upstream completion. |
| Deterministic Variable Resolution | The rule that parallel nodes MUST NOT write to the same variable; reads resolve from the last committed write in topological order. |

---

## 2 Parallelism Overview

Key principles:

- Independent nodes MAY execute in parallel.
- Dependent nodes MUST execute in the specified order.
- Parallel execution is bounded by resource constraints.
- Race conditions are prevented through deterministic variable resolution.
- All parallel execution MUST be deterministic and reproducible.

---

## 3 Parallelism Strategies

| Strategy | Description | Use Case |
|---|---|---|
| Fork-Join | Split work into parallel branches, join results | Batch processing |
| Pipeline | Stages process data concurrently | Streaming processing |
| Map-Reduce | Distribute computation, aggregate results | Large-scale computation |
| Fan-Out/Fan-In | Distribute to many nodes, collect results | Parallel API calls |
| Parallel Loop | Iterate with parallel iterations | Array processing |

### 3.1 Fork-Join

The Fork-Join strategy splits a workflow graph into independent branches that execute concurrently and join at a barrier. The implementation MUST enforce that all branches complete before the join node proceeds.

### 3.2 Pipeline

The Pipeline strategy stages data through sequential processing phases where each stage operates on different data items concurrently. The implementation MUST ensure that data flows through stages in order without reordering.

### 3.3 Map-Reduce

The Map-Reduce strategy distributes independent computations across parallel nodes and aggregates results. The implementation MUST guarantee that aggregation occurs only after all map nodes complete successfully.

### 3.4 Fan-Out/Fan-In

The Fan-Out/Fan-In strategy dispatches N parallel child executions and collects results. The implementation MUST enforce the Max Fan-Out bound (see Section 6).

### 3.5 Parallel Loop

The Parallel Loop strategy iterates over a collection with parallel iterations. The implementation MUST ensure that loop iterations are independent and that collected results maintain deterministic ordering.

---

## 4 Dependency Analysis

### 4.1 Dependency Types

| Dependency | Description | Parallelism Impact |
|---|---|---|
| Data | Output of one node is input of another | Must serialize |
| Control | One node gates another | Must serialize |
| Resource | Both nodes require the same resource | May serialize |
| None | No dependencies | Can parallelize |

### 4.2 Dependency Classification Rules

- Data dependencies MUST be resolved before parallel dispatch. The implementation MUST build a directed acyclic graph (DAG) and compute the longest-path schedule.
- Control dependencies MUST be respected. A node gated by a condition branch MUST NOT execute until the condition evaluates.
- Resource dependencies MAY be serialized through a resource scheduler. The implementation SHOULD use the scheduler described in RFC-0312.
- Nodes with no dependencies MAY execute in parallel subject to parallelism bounds.

### 4.3 Parallelism Discovery

1. Build the dependency graph from the workflow definition.
2. Compute the topological order of all nodes.
3. Identify independent node sets at each frontier.
4. Check resource availability and parallelism bounds for each set.
5. Dispatch independent sets concurrently through the scheduler (RFC-0312).

---

## 5 Race Condition Prevention

### 5.1 Prevention Rules

- Variables written by parallel nodes MUST have unique identifiers. No two concurrently executing nodes MAY write to the same variable.
- Variables read by parallel nodes MUST not be written by any parallel node. Reads resolve from the context snapshot at the time of dispatch.
- Resource access by parallel nodes MUST be synchronized through the resource manager.
- The implementation MUST reject workflow definitions that violate these rules at validation time (RFC-0317).

### 5.2 Synchronization Primitives

| Primitive | Description | Use Case |
|---|---|---|
| Barrier | Wait for all parallel nodes to complete | Join point |
| Mutex | Exclusive resource access | Resource protection |
| Semaphore | Bounded concurrent access | Limited resources |

#### 5.2.1 Barrier Semantics

A barrier node MUST block all downstream execution until every incoming parallel branch reaches the barrier. The implementation MUST record which branches have arrived and MUST NOT proceed until all branches are accounted for.

#### 5.2.2 Mutex Semantics

A mutex provides exclusive access to a named resource. The implementation MUST queue requests in FIFO order and MUST release the mutex when the holder completes or aborts.

#### 5.2.3 Semaphore Semantics

A semaphore limits concurrent access to N instances of a resource. The implementation MUST track available permits and MUST block dispatch when no permits are available.

---

## 6 Parallelism Bounds

### 6.1 Bounds

| Bound | Description | Default |
|---|---|---|
| Max Parallelism | Maximum concurrent nodes | Resource-dependent |
| Max Depth | Maximum nesting depth | 10 |
| Max Fan-Out | Maximum parallel children per node | 100 |

### 6.2 Bound Enforcement

- The implementation MUST enforce Max Parallelism globally across the workflow instance.
- The implementation MUST enforce Max Depth to prevent unbounded recursive parallelism.
- The implementation MUST enforce Max Fan-Out per dispatcher node.
- Violations MUST cause the workflow to transition to a failed state with a validation error (RFC-0317).

### 6.3 Bound Configuration

Bounds are configurable at the workflow instance level through the manifest (RFC-0310). The implementation MUST allow overrides per instance while enforcing declared minimums.

---

## 7 Layer Boundaries

### 7.1 Responsibilities

- **This layer (Workflow Parallelism)**: Defines parallelism strategies, dependency analysis algorithms, race condition prevention rules, synchronization primitives, and parallelism bounds.
- **Caller (Workflow Scheduler, RFC-0312)**: Determines WHEN parallel nodes are dispatched based on priority, resource availability, and temporal constraints.
- **Caller (Workflow Execution Engine, RFC-0303)**: Executes nodes and manages the execution context.
- **Dependent (Workflow Recovery, RFC-0315)**: Restores parallel execution state from checkpoints after failure.
- **Dependent (Workflow Debugging, RFC-0316)**: Provides per-node visibility into parallel execution for inspection and stepping.
- **Dependent (Workflow Observability, RFC-0321)**: Emits metrics on parallelism utilization, contention, and throughput.

### 7.2 Non-Responsibilities

- This layer MUST NOT assume a specific thread model, process model, or concurrency primitive from any runtime implementation.
- This layer MUST NOT depend on a systems programming language, Node.js, a desktop application framework, a desktop application framework, an embedded database engine, the browser, or GPU resources.
- This layer MUST NOT define error handling semantics; error handling is defined in RFC-0314.
- This layer MUST NOT define recovery semantics; recovery is defined in RFC-0315.
- This layer MUST NOT define debugging semantics; debugging is defined in RFC-0316.
- This layer MUST NOT define serialization formats; serialization is defined in RFC-0328.

### 7.3 Dependencies

| Direction | Dependency | Nature |
|---|---|---|
| Depends On | RFC-0303 Workflow Execution | Execution model contract |
| Depends On | RFC-0312 Workflow Scheduler | Dispatch ordering |
| Depends On | RFC-0315 Workflow Recovery | Checkpoint semantics |
| Depends On | RFC-1001 Common Event Model | Event emission |
| Depends On | RFC-1002 Common State Model | State representation |
| Depends On | RFC-1006 Common Error Model | Error classification |
| Provided To | RFC-0314 Workflow Error Handling | Error classification for parallel faults |
| Provided To | RFC-0316 Workflow Debugging | Execution visibility |
| Provided To | RFC-0321 Workflow Observability | Metrics data |

### 7.4 Forbidden Dependencies

- This layer MUST NOT depend on any subsystem-specific implementation (Plugin, Storage, Vision, AI, Marketplace, Knowledge).
- This layer MUST NOT depend on any runtime-specific library or framework.
- This layer MUST NOT assume network topology or distributed deployment.

---

## 8 Security

### 8.1 Security Requirements

- Parallel execution MUST NOT bypass sandbox boundaries defined for individual nodes. Each parallel node MUST execute within its declared sandbox.
- Shared resources accessed by parallel nodes MUST enforce access control per the capability model (RFC-1003).
- The implementation MUST prevent side-channel timing attacks through deterministic scheduling. Parallel execution order MUST NOT leak information about internal state.
- Parallelism bounds MUST be enforced as a denial-of-service protection. Malicious workflow definitions MUST NOT be able to exhaust system resources through unbounded parallelism.

### 8.2 Security Controls

| Control | Requirement | Enforcement Point |
|---|---|---|
| Sandbox Isolation | Each parallel node runs in its declared sandbox | Execution engine |
| Resource Limits | Parallelism bounds enforced as DoS protection | Scheduler |
| Access Control | Shared resources use capability-based permissions | Resource manager |
| Timing Determinism | No timing-based information leakage | Dispatcher |
| Validation | Invalid parallelism definitions rejected at load time | Validator (RFC-0317) |

---

## 9 Performance

### 9.1 Performance Requirements

- The implementation MUST measure and expose parallelism utilization as a metric (RFC-0321).
- The implementation MUST support configurable parallelism bounds to tune throughput versus resource consumption.
- The dependency analysis algorithm MUST complete within O(V + E) time where V is the number of nodes and E is the number of edges.
- Synchronization primitives MUST NOT introduce unbounded waiting. All barriers, mutexes, and semaphores MUST have configurable timeouts.

### 9.2 Performance Characteristics

| Metric | Requirement | Measurement |
|---|---|---|
| Dependency Analysis | O(V + E) | Algorithm benchmark |
| Barrier Wait Timeout | Configurable, default 300s | Timeout enforcement test |
| Mutex Acquisition | FIFO ordering, bounded wait | Contention test |
| Throughput | Scales with available resources | Load test |
| Overhead | Per-node dispatch overhead < 1ms | Microbenchmark |

### 9.3 Scalability

- The implementation MUST support horizontal scaling of parallel dispatch through the scheduler (RFC-0312).
- The implementation MUST NOT assume a single-threaded execution model. Parallelism bounds apply regardless of the underlying threading strategy.

---

## 10 Compatibility

### 10.1 Compatibility Levels

| Level | Description | Requirement |
|---|---|---|
| Full | Identical parallelism behavior | Same version |
| Forward | Older definitions run on newer runtime | Backward compatible |
| Backward | Newer definitions run on older runtime | Best-effort |
| Partial | Some parallelism features unavailable | Feature flag |
| Incompatible | Behavior differs significantly | Version migration required |

### 10.2 Version Compatibility

- Workflow definitions created under one version of this specification MUST execute identically under the same version of the implementation.
- Implementations MUST support at least one prior minor version of parallelism semantics for backward compatibility.
- Breaking changes to parallelism semantics MUST be communicated through the versioning process (RFC-0318).

---

## 11 Compliance

### 11.1 Compliance Requirements

- The implementation MUST enforce deterministic variable resolution for all parallel executions.
- The implementation MUST reject workflow definitions that declare conflicting variable writes in parallel branches.
- The implementation MUST log all parallelism bound violations for audit purposes.
- The implementation MUST support parallelism policy enforcement through organizational compliance rules (RFC-0330).

### 11.2 Audit Trail

- Every parallel dispatch event MUST be recorded with node IDs, timestamps, and resource allocations.
- Every synchronization event (barrier arrival, mutex acquire/release) MUST be recorded.
- Audit records MUST conform to the event model defined in RFC-1001.

---

## 12 Future Evolution

### 12.1 Planned Extensions

- Adaptive parallelism: Dynamic adjustment of parallelism bounds based on runtime resource telemetry.
- Priority-aware scheduling: Integration with the scheduler (RFC-0312) to prioritize high-priority parallel branches.
- Distributed parallelism: Support for cross-process and cross-machine parallel execution while maintaining determinism.
- Predictive dependency analysis: Machine learning-assisted estimation of execution times for optimized dispatch ordering.

### 12.2 Extension Points

- Custom synchronization primitives MAY be registered through the extension model (RFC-0322).
- Custom dependency analysis strategies MAY be plugged in through the validation interface (RFC-0317).
- Custom parallelism bounds policies MAY be defined through the manifest extension (RFC-0310).

---

## 13 Runtime Independence

This specification is intentionally runtime-independent. The following assumptions are explicitly forbidden:

- This specification MUST NOT assume a specific programming language (a systems programming language, Node.js, Python, etc.).
- This specification MUST NOT assume a specific runtime environment (a desktop application framework, a desktop application framework, browser, native).
- This specification MUST NOT assume a specific database or persistence layer (an embedded database engine, a relational database, etc.).
- This specification MUST NOT assume a specific threading or process model (threads, async/await, actors, coroutines).
- This specification MUST NOT assume GPU acceleration or hardware-specific parallelism primitives.
- This specification MUST NOT assume a particular operating system or kernel scheduling strategy.

Implementations MAY use any concurrency model provided by their runtime, as long as the external behavior conforms to the deterministic, reproducible execution model defined herein.

---

## 14 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Five parallelism strategies MUST be supported. | Strategy enumeration test |
| AC-02 | Four dependency types MUST be defined and classified. | Dependency classification test |
| AC-03 | Three race condition prevention rules MUST be enforced. | Race condition test |
| AC-04 | Three synchronization primitives (Barrier, Mutex, Semaphore) MUST be supported. | Synchronization test |
| AC-05 | Three parallelism bounds (Max Parallelism, Max Depth, Max Fan-Out) MUST be configurable. | Bound test |
| AC-06 | The implementation MUST enforce deterministic variable resolution for all parallel executions. | Determinism test |
| AC-07 | The implementation MUST reject workflow definitions with conflicting parallel variable writes. | Validation rejection test |
| AC-08 | The dependency analysis algorithm MUST complete within O(V + E) time complexity. | Complexity benchmark |
| AC-09 | All synchronization primitives MUST support configurable timeouts. | Timeout enforcement test |
| AC-10 | Parallelism bounds MUST be enforceable as denial-of-service protection. | DoS protection test |

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (Terminology authority) |
| RFC-0303 | Workflow Execution (Execution engine contract) |
| RFC-0304 | Workflow Runtime (Runtime model) |
| RFC-0310 | Workflow Manifest (Configuration) |
| RFC-0312 | Workflow Scheduler (Dispatch ordering) |
| RFC-0314 | Workflow Error Handling (Error classification) |
| RFC-0315 | Workflow Recovery (Checkpoint semantics) |
| RFC-0316 | Workflow Debugging (Execution visibility) |
| RFC-0317 | Workflow Validation (Validation interface) |
| RFC-0318 | Workflow Versioning (Version management) |
| RFC-0320 | Performance (Performance requirements) |
| RFC-0321 | Workflow Observability (Metrics) |
| RFC-0322 | Workflow Extension (Extension model) |
| RFC-0328 | Workflow Serialization (Serialization) |
| RFC-0330 | Workflow Compliance (Compliance) |
| ADR-0012 | Contract-First Specification-Driven Development |
| RFC-1001 | Common Event Model |
| RFC-1002 | Common State Model |
| RFC-1003 | Common Capability Model |
| RFC-1006 | Common Error Model |
| Catalog: workflow-capabilities.md | Capability catalog |
| Schema: parallelism.json | JSON Schema for parallelism configuration |
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
