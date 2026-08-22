RFC: RFC-0312

Title: Workflow Scheduler

Status: Proposed

Version: 1.0.0

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

  - RFC-0307 Workflow Context

  - RFC-0308 Workflow Events

  - RFC-0309 Workflow Actions

  - RFC-0310 Workflow Conditions

  - RFC-0311 Workflow Triggers


  - RFC-0313 Workflow Parallelism

  - RFC-0314 Workflow Error Handling

  - RFC-0315 Workflow Recovery

  - RFC-0316 Workflow Debugging

  - RFC-0317 Workflow Validation

  - RFC-0318 Workflow Versioning

  - RFC-0319 Workflow Security

  - RFC-0320 Workflow Performance

  - RFC-0321 Workflow Observability

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

  - RFC-0325 Workflow AI

  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC

  - RFC-0328 Workflow Serialization

  - RFC-0329 Workflow Compatibility

  - RFC-0330 Workflow Compliance

Related ADR: ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema: specs/workflow/json-schema/workflow-scheduler-types.md

Related Catalog: specs/workflow/catalog/workflow-schedulers.md

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x

Last Updated: 2026-07-01

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Scheduler specification defines the scheduling model for Atlas workflows. The scheduler determines WHEN and WHERE each node is executed, considering dependencies, resources, priorities, and constraints.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0312 workflow scheduler.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 1 Terminology



The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below.



| Term | Definition |

|---|---|

| Scheduler | The component responsible for determining WHEN and WHERE each workflow node is executed, based on dependencies, resources, priorities, and constraints. |

| Scheduling Policy | A rule set that determines the order and conditions under which nodes are dispatched for execution. |

| Scheduling Queue | A priority-ordered collection of nodes ready for execution, managed by the scheduler. |

| Ready Set | The subset of nodes in the scheduling queue whose dependencies have been fully satisfied. |

| Resource Allocation | The assignment of computational resources (CPU, memory, storage) to scheduled nodes. |

| Resource Contention | The state where multiple ready nodes compete for the same limited resource. |

| Scheduling Mode | The temporal behavior of node dispatch: immediate, delayed, periodic, or deadline-based. |

| Parallelism Discovery | The process of identifying nodes that can execute concurrently without violating dependency constraints. |

| Workflow Runtime | The runtime system responsible for loading, validating, scheduling, executing, and observing workflow instances. Referenced in RFC-0304. |



---



## 2 Layer Boundaries



### 2.1 Responsibilities



The Workflow Scheduler specification defines:



- The taxonomy of scheduling policies and their application contexts.

- The scheduling queue data structure (ready set, priority order, resource requirements, estimated duration).

- Queue operations (enqueue, dequeue, reorder, remove, peek).

- Resource allocation strategies (round-robin, first-fit, reservation-based, namespace-based).

- Resource contention resolution procedures.

- Time-based scheduling modes (immediate, delayed, periodic, deadline).

- Parallelism discovery and dispatch algorithms.



### 2.2 Non-Responsibilities



The following are explicitly OUT OF SCOPE for this specification:



- Condition evaluation logic (RFC-0310).

- Trigger firing mechanisms (RFC-0311).

- Action execution semantics (RFC-0309).

- Error handling and retry policies (RFC-0314).

- Recovery and checkpoint semantics (RFC-0315).

- Debugging and inspection interfaces (RFC-0316).

- Physical resource provisioning (RFC-0009).



### 2.3 Dependencies



| Dependency | Direction | Nature |

|---|---|---|

| RFC-0301 Workflow Overview | Consumes | Terminology, philosophy |

| RFC-0303 Workflow Execution | Consumes | Execution phases, resource budgets |

| RFC-0304 Workflow Runtime | Consumes | Runtime contract, node lifecycle |

| RFC-0307 Workflow Context | Consumes | Variable resolution, context propagation |

| RFC-0308 Workflow Events | Consumes | Event emission model for scheduling events |

| RFC-0309 Workflow Actions | Consumes | Action resource requirements |

| RFC-0310 Workflow Conditions | Consumes | Dependency satisfaction conditions |

| RFC-0313 Workflow Parallelism | Consumes | Parallel execution constraints |

| RFC-0314 Workflow Error Handling | Consumes | Scheduling failure recovery |

| RFC-0320 Workflow Performance | Consumes | Scheduling performance metrics |

| RFC-0322 Workflow Extension | Provides | Extension point for custom scheduling policies |

| RFC-0004 Runtime Scheduler | Consumes | Underlying runtime scheduler contract |



### 2.4 Consumers



- Workflow Runtime (RFC-0304): Dispatches nodes according to scheduling decisions.

- Workflow Debugger (RFC-0316): Inspects scheduling decisions and queue state.

- Workflow Validator (RFC-0317): Validates scheduling constraints against schema.

- Resource Manager (RFC-0009): Provides resource availability information.



### 2.5 Providers



- Workflow Runtime (RFC-0304): Provides execution context, dependency graph, node states.

- Resource Manager (RFC-0009): Provides resource availability and allocation services.

- Event Bus (RFC-1001): Provides scheduling event emission infrastructure.

- Condition Engine (RFC-0310): Provides dependency satisfaction evaluation.



### 2.6 Forbidden Dependencies



Scheduler implementations MUST NOT depend on:



- Any specific programming language runtime (a systems programming language, Node.js, a desktop application framework, a desktop application framework).

- Any specific database engine (an embedded database engine, a relational database, etc.).

- Any browser API or DOM interface.

- Any operating system call or process model.

- Any GPU compute interface.

- Any threading or concurrency model (sequential scheduling is sufficient for correctness).



---



## 3 Scheduler Overview



The workflow scheduler operates on the execution graph and makes scheduling decisions based on:



- Node dependencies (data and control)

- Resource availability

- Priority levels

- Execution budgets

- Time constraints

- Parallelism constraints

- Error handling policies



---



## 4 Scheduling Policies



| Policy | Description | Application |

|---|---|---|

| Topological | Execute nodes in topological order | Default scheduling |

| Priority | Higher-priority nodes execute first | Priority-ordered execution |

| Resource-Aware | Schedule based on resource availability | Resource-constrained environments |

| Time-Bounded | Schedule within time constraints | Deadline-sensitive workflows |

| Cost-Optimized | Minimize resource cost | Cost-sensitive executions |

| Parallel-Optimized | Maximize parallel execution | Throughput-sensitive workflows |



---



## 5 Scheduling Queue



### 5.1 Queue Structure



The scheduling queue is a priority-ordered collection of nodes ready for execution:



| Queue Attribute | Description |

|---|---|

| Ready Set | Nodes whose dependencies are satisfied |

| Priority Order | Nodes ordered by priority |

| Resource Requirements | Resource needs of queued nodes |

| Estimated Duration | Expected execution time of queued nodes |



### 5.2 Queue Operations



| Operation | Description |

|---|---|

| Enqueue | Add node to ready set |

| Dequeue | Remove highest-priority node |

| Reorder | Reorder based on priority change |

| Remove | Remove node from queue |

| Peek | View next node without removing |



---



## 6 Resource Scheduling



### 6.1 Resource Allocation



Resources are allocated by the scheduler:



| Resource | Allocation Strategy |

|---|---|

| CPU | Round-robin among ready nodes |

| Memory | First-fit allocation |

| GPU | Reservation-based allocation |

| Storage | Namespace-based allocation |



### 6.2 Resource Contention



When resources are contended:



1. Higher-priority nodes are scheduled first.

2. Lower-priority nodes are queued.

3. Contention is resolved through preemption (for critical nodes).



---



## 7 Time-Based Scheduling



### 7.1 Scheduling Modes



| Mode | Description |

|---|---|

| Immediate | Execute as soon as dependencies are satisfied |

| Delayed | Execute after a specified delay |

| Periodic | Execute at regular intervals |

| Deadline | Execute before a specified deadline |



---



## 8 Parallel Scheduling



### 8.1 Parallelism Discovery



The scheduler identifies parallel execution opportunities:



1. Build the dependency graph.

2. Find all nodes with satisfied dependencies.

3. Group nodes by resource availability.

4. Dispatch parallel groups concurrently.



---



## 9 Security



### 9.1 Scheduler-Level Security Controls



| Control | Requirement | Enforcement Point |

|---|---|---|

| Scheduling Authorization | Only authorized actors MAY modify scheduling policies. | Declaration |

| Resource Isolation | Scheduled nodes MUST be isolated from other tenants resources. | Runtime |

| Preemption Auditing | All preemptive scheduling decisions MUST be logged. | Post-decision |

| Priority Inversion Prevention | Scheduling MUST prevent priority inversion attacks. | Runtime |

| Queue Integrity | The scheduling queue MUST be tamper-proof. | Runtime |

| Deadline Enforcement | Scheduled deadlines MUST NOT be extendable by unauthorized actors. | Runtime |

| Audit Logging | All scheduling decisions (dispatch, reorder, preempt) MUST emit audit events. | Post-decision |

| Resource Quota Enforcement | Each workflow MUST be bounded by its declared resource quota. | Runtime |



### 9.2 Forbidden Patterns



Schedulers MUST NOT:



- Allow unauthorized actors to modify scheduling policies at runtime.

- Share resources between workflows without explicit isolation guarantees.

- Preempt critical nodes without audit logging.

- Extend deadlines beyond declared limits without authorization.



---



## 10 Performance



### 10.1 Performance Requirements



| Metric | Requirement | Measurement |

|---|---|---|

| Scheduling Decision Latency | Each scheduling decision MUST complete within 1ms. | Per-decision timer |

| Queue Operation | Enqueue/dequeue MUST complete within 100 microseconds. | Benchmark |

| Parallelism Discovery | Finding parallel groups MUST complete within 10ms for 1000 nodes. | Graph traversal test |

| Memory Footprint | Scheduling context MUST not exceed 128 KiB per workflow. | Profiling |

| Contention Resolution | Resource contention MUST be resolved within 5ms. | Concurrency test |

| Compilation Time | Scheduling schema compilation MUST complete within 200ms for 2000 nodes. | Schema benchmark |



### 10.2 Optimization Guidelines



- Topological sort results SHOULD be cached between scheduling rounds.

- Priority queues SHOULD use binary heap or tournament tree implementations.

- Parallelism discovery SHOULD use breadth-first search for deterministic ordering.



---



## 11 Compatibility



### 11.1 Compatibility Levels



| Level | Description | Enforcement |

|---|---|---|

| Full | Fully compatible across all versions | No enforcement needed |

| Backward | Compatible with previous version | Validation warning |

| Forward | Compatible with next version | Validation warning |

| Conditional | Compatible under specific conditions | Runtime check |

| Incompatible | Not compatible | Validation error |



### 11.2 Scheduling Policy Compatibility



- New scheduling policies MAY be added without breaking existing workflows.

- Scheduling queue operations MAY be extended without breaking existing workflows.

- Scheduling policy semantics MUST NOT change between minor versions.

- Removed scheduling policies MUST follow the deprecation cycle defined in RFC-0318.



---



## 12 Compliance



### 12.1 Compliance Categories



| Category | Requirement | Enforcement |

|---|---|---|

| Operational | Schedulers MUST declare resource allocation strategies. | Pre-execution |

| Security | Schedulers MUST enforce resource isolation and priority inversion prevention. | Continuous |

| Audit | All scheduling decisions MUST produce audit trail entries. | Post-decision |

| Data Privacy | Schedulers handling PII data MUST enforce data locality constraints. | Declaration |

| Determinism | Identical scheduling inputs MUST produce identical scheduling decisions. | Runtime |

| Resource Quotas | Each workflow MUST respect its declared resource quota. | Runtime |



---



## 13 Future Evolution



### 13.1 Planned Extensions



| Feature | Status | RFC |

|---|---|---|

| Adaptive scheduling (ML-driven) | Proposed | RFC-0325 |

| Distributed scheduling | Proposed | RFC-0322 |

| Scheduling fairness guarantees | Proposed | RFC-0320 |

| Scheduling composition DSL | Proposed | RFC-0302 |

| Scheduling versioning | Proposed | RFC-0318 |



### 13.2 Deprecation Policy



- Deprecated scheduling policies MUST remain functional for at least two major versions.

- Migration guides MUST be provided for all deprecated scheduling policies.

- New workflows MUST NOT use deprecated scheduling policies.



---



## 14 Runtime Independence



This specification is intentionally runtime-independent. It makes no assumptions about:



- Programming language: Schedulers MAY be implemented in any language.

- Runtime environment: Scheduling MAY occur in-process, out-of-process, or remotely.

- Process model: No assumption of threads, goroutines, or async/await.

- Database: No assumption of an embedded database engine, relational, or document stores.

- Browser: No assumption of DOM, Web APIs, or rendering.

- Operating system: No assumption of POSIX, Windows, or any OS-specific API.

- Hardware: No assumption of GPU, TPU, or specialized accelerators.

- Serialization format: Scheduling contexts MAY use JSON, MessagePack, or any agreed format.



---



## 15 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | The implementation MUST support six (6) distinct scheduling policies as enumerated in Section 4. | Policy enumeration test |

| AC-02 | The implementation MUST support five (5) queue operations as enumerated in Section 5.2. | Queue operation test |

| AC-03 | The implementation MUST define four (4) resource allocation strategies as enumerated in Section 6.1. | Resource allocation test |

| AC-04 | The implementation MUST support four (4) scheduling modes as enumerated in Section 7.1. | Mode enumeration test |

| AC-05 | The implementation MUST enforce acyclicity in scheduling decisions. | Cycle detection test |

| AC-06 | The implementation MUST enforce all eight (8) security controls defined in Section 9.1. | Security audit |

| AC-07 | The implementation MUST measure all six (6) performance metrics defined in Section 10.1. | Performance benchmark |

| AC-08 | The implementation MUST enforce five (5) compatibility levels defined in Section 11.1. | Compatibility test |

| AC-09 | The implementation MUST enforce six (6) compliance categories defined in Section 12.1. | Compliance test |



---



## 16 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (terminology, philosophy) |

| RFC-0303 | Workflow Execution (execution phases, resource budgets) |

| RFC-0304 | Workflow Runtime (runtime contract, node lifecycle) |

| RFC-0307 | Workflow Context (variable resolution, context propagation) |

| RFC-0308 | Workflow Events (event emission for scheduling events) |

| RFC-0309 | Workflow Actions (action resource requirements) |

| RFC-0310 | Workflow Conditions (dependency satisfaction conditions) |

| RFC-0311 | Workflow Triggers (trigger scheduling integration) |

| RFC-0313 | Workflow Parallelism (parallel execution constraints) |

| RFC-0314 | Workflow Error Handling (scheduling failure recovery) |

| RFC-0315 | Workflow Recovery (checkpoint-based scheduling resumption) |

| RFC-0316 | Workflow Debugging (scheduling inspection interfaces) |

| RFC-0317 | Workflow Validation (scheduling schema validation) |

| RFC-0318 | Workflow Versioning (deprecated scheduling policies) |

| RFC-0320 | Workflow Performance (scheduling performance metrics) |

| RFC-0322 | Workflow Extension (custom scheduling policy registration) |

| RFC-0004 | Runtime Scheduler (underlying runtime scheduler contract) |

| ADR-0012 | Contract-First Specification-Driven Development |

| JSON Schema | specs/workflow/json-schema/workflow-scheduler-types.md |

| Catalog | specs/workflow/catalog/workflow-schedulers.md |

| Glossary | Atlas Master Glossary (RFC-0301) |

| Constitution | Atlas AI Constitution, Section 1 (Workflow Philosophy) |

---



## Terminology



| Term | Definition | Source |

|---|---|---|

| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |

| Action | An operation performed by a workflow node. | RFC-0309 |

| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 | RFC-0310 |

| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |

| Scheduler | The component that determines WHEN and WHERE each node is executed. | RFC-0312 |

| Context | The scoped data environment available to nodes during execution. | RFC-0307 |



## Layer Boundaries



### Responsibilities

This specification IS responsible for: defining the scheduling policy model and time semantics.



### Non-Responsibilities

This specification IS NOT responsible for: executing nodes (delegated to RFC-0303), managing the runtime (delegated to RFC-0304), or scheduling decisions (delegated to RFC-0312, except for RFC-0312 itself).



### Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0303 | Consumed | Workflow Execution consumes schedules |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0307 | Consumed | Workflow Context provides context data |

| RFC-0317 | Consumed | Workflow Validation validates scheduler policies |

| RFC-0319 | Consumed | Workflow Security provides scheduling security |

| RFC-0320 | Consumed | Workflow Performance provides scheduling performance |



### Consumers

- Workflow Execution (RFC-0303): Consumes scheduling policies for execution.



### Providers

- 

- 

- 

- Schedulers Catalog (catalog/workflow-schedulers.md)



### Forbidden Dependencies

- This specification MUST NOT depend on any platform-specific implementation.



## Security

- 

- 

- 

- Scheduler policies MUST enforce resource limits per RFC-0319.



## Performance

- 

- 

- 

- Scheduling decisions MUST complete within 1ms per tick.



## Compatibility

- 

- 

- 

- Scheduler policies MUST be backward compatible within a major version.



## Compliance

- All scheduler policies MUST comply with organizational policies per RFC-0330.



## Future Evolution

- 

- 

- 

- Adaptive scheduling based on workload prediction.



## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)

- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)

- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)

- Any operating system (Windows, Linux, macOS, etc.)

- Any hardware architecture (CPU, GPU, FPGA, etc.)

- Any threading model (single-threaded, multi-threaded, actor-based, etc.)




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


## References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (canonical terminology source) |

| RFC-0303 | Workflow Execution (schedule consumption) |

| RFC-0304 | Workflow Runtime (execution context) |

| RFC-0307 | Workflow Context (context data) |

| RFC-0312 | Workflow Scheduler (this document) |

| RFC-0314 | Workflow Error Handling (error propagation) |

| RFC-0315 | Workflow Recovery (recovery) |

| RFC-0317 | Workflow Validation (validation) |

| RFC-0319 | Workflow Security (security) |

| RFC-0320 | Workflow Performance (performance) |

| RFC-0321 | Workflow Observability (telemetry) |

| RFC-0322 | Workflow Extension (extension) |

| RFC-0329 | Workflow Compatibility (compatibility) |

| RFC-0330 | Workflow Compliance (compliance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/scheduler-policy | Scheduler Policy JSON Schema |

| catalog/workflow-schedulers | Scheduler Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0312 (this document), RFC-0301 (Overview), RFC-0313 (Parallelism) |






