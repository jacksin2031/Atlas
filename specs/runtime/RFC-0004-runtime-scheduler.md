# RFC-0004: Runtime Scheduler

RFC: RFC-0004
Title: Runtime Scheduler
Status: Frozen
Authors: Atlas Team
Created: 2026-06-27
Last Updated: 2026-06-30
Requires:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0005 Runtime Event Bus
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Target Release: 1.0.0

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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the task queue management structures, execution scheduling models, priority rules, and worker allocations defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

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
4. [Scheduler Philosophy](#4-scheduler-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Scheduler Architecture](#8-scheduler-architecture)
9. [Task Models and Triggers](#9-task-models-and-triggers)
10. [Queue Management and Concurrency](#10-queue-management-and-concurrency)
11. [Worker Pool Allocation](#11-worker-pool-allocation)
12. [Task Execution Sequence](#12-task-execution-sequence)
13. [Frame-Level Execution Flow](#13-frame-level-execution-flow)
14. [Task Retries and Cancellation](#14-task-retries-and-cancellation)
15. [Timeout and Backpressure Constraints](#15-timeout-and-backpressure-constraints)
16. [Security and Thread Isolation](#16-security-and-thread-isolation)
17. [Performance Budgets](#17-performance-budgets)
18. [Exposed Scheduler APIs](#18-exposed-scheduler-apis)
19. [Normative Contracts](#19-normative-contracts)
20. [Compliance Checklist](#20-compliance-checklist)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [References](#22-references)
23. [Changelog](#23-changelog)
24. [Compatibility](#24-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Execution Determinism**: Tasks with identical priorities, triggers, and resources MUST resolve in a reproducible sequence.
- **Topological Order Safeguards**: Tasks with dependencies MUST execute only when all upstream conditions are satisfied.
- **Priority Fairness**: Higher-priority tasks MUST NOT starve lower-priority tasks indefinitely.
- **Resource Awareness**: The Scheduler MUST respect resource quotas defined by the Resource Manager (refer to RFC-0009).

---



## 4 Scheduler Philosophy

1. **Topological Execution Rules**: Workflows compile to directed acyclic graphs (DAGs). The Scheduler executes nodes topological-first.
2. **Prioritization Laws**: System checks and security filters override workflow executions.
3. **Dispatch-Only Execution**: The Scheduler dispatches tasks to worker pools but does NOT execute task logic itself.
4. **Backpressure-Resilient**: When downstream consumers are slow, the Scheduler applies backpressure to upstream producers.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Scheduler may communicate with**:
  - Runtime Lifecycle (refer to RFC-0002)
  - Event Bus (refer to RFC-0005)
  - Metrics Service
- **Scheduler MUST NOT communicate with**:
  - Plugins directly (refer to RFC-0008)
  - UI controllers

---



## 8 Scheduler Architecture

The Scheduler consists of three core components: the Task Queue Manager, the Worker Pool Allocator, and the Execution Dispatcher.

### 8.1 Task Queue Manager

The Task Queue Manager maintains priority-based queues for different task categories. Tasks are enqueued with a priority level (1=Critical, 2=High, 3=Normal, 4=Background) and a dependency set.

`mermaid
graph TD
    EQ[Enqueue Point] --> PQ1[Priority 1: Critical Queue]
    EQ --> PQ2[Priority 2: High Queue]
    EQ --> PQ3[Priority 3: Normal Queue]
    EQ --> PQ4[Priority 4: Background Queue]
    PQ1 --> DQ[Dispatch Queue]
    PQ2 --> DQ
    PQ3 --> DQ
    PQ4 --> DQ
    DQ --> WP[Worker Pool]
`

### 8.2 Worker Pool Allocator

The Worker Pool Allocator manages a pool of worker threads. Workers are drawn from a pre-allocated pool sized according to the system resource profile (refer to RFC-0009). The pool supports dynamic scaling within configured bounds.

### 8.3 Execution Dispatcher

The Execution Dispatcher selects the highest-priority ready task from the queues and assigns it to an available worker. A task is ready when all its dependency tasks have completed successfully.

---

This specification IS responsible for:
- Defining the architecture and requirements for this subsystem.


## 10 Queue Management and Concurrency

### 10.1 Priority Queue Structure

The Scheduler maintains separate queues per priority level. Within each priority level, tasks are ordered by submission time (FIFO).

### 10.2 Concurrency Limits

The maximum number of concurrently executing tasks is bounded by the Worker Pool size. The Scheduler enforces the following concurrency rules:

- **Critical tasks**: Up to N critical tasks may execute concurrently (N = number of cores / 2).
- **High tasks**: Up to N high-priority tasks may execute concurrently.
- **Normal tasks**: Up to 2*N normal tasks may execute concurrently.
- **Background tasks**: Executed only when no higher-priority tasks are queued.

### 10.3 Queue Drain Order

During shutdown, the Scheduler drains queues in priority order: Critical first, then High, then Normal, then Background. Tasks in-progress are allowed to complete; newly enqueued tasks are rejected.

---

`

---

- Implementation details (see related RFCs).
- Cross-cutting concerns handled by other subsystems.


## 14 Task Retries and Cancellation

### 14.1 Retry Policy

Tasks MAY be retried on failure according to the following policy:

| Parameter | Default | Description |
|---|---|---|
| MaxRetries | 3 | Maximum retry attempts |
| InitialDelay | 100 ms | Delay before first retry |
| MaxDelay | 30,000 ms | Maximum delay between retries |
| BackoffMultiplier | 2.0 | Exponential backoff factor |
| RetryableErrors | Timeout, Network | Error types that trigger retry |

### 14.2 Cancellation

Tasks MAY be cancelled by the caller. Cancellation is propagated to the executing worker, which MUST attempt to stop execution gracefully. If the worker does not respond within the cancellation timeout (5,000 ms default), the worker is forcibly terminated.

---


## 16 Security and Thread Isolation

### 16.1 Thread Isolation

Workers MUST NOT share mutable state between tasks. Each task execution context is isolated to prevent cross-task data leakage.

### 16.2 Resource Quotas

Each worker is subject to resource quotas defined by the Resource Manager (refer to RFC-0009). Workers that exceed their quotas are throttled or terminated.

### 16.3 Task Authentication

Tasks submitted to the Scheduler MUST include a valid security token. Unauthorized tasks are rejected with a PermissionDenied error.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 18 Exposed Scheduler APIs

`
interface SchedulerController {
  // Submit a task for execution. Returns TaskId.
  TaskId submitTask(TaskDefinition task);

  // Cancel a pending or in-flight task.
  void cancelTask(TaskId taskId);

  // Get the current queue depth for each priority level.
  QueueDepth getQueueDepth();

  // Get the current worker pool status.
  WorkerPoolStatus getWorkerPoolStatus();

  // Pause task dispatch.
  void pause();

  // Resume task dispatch.
  void resume();
}

interface TaskDefinition {
  string taskId;
  int priority;
  string[] dependencies;
  string taskType;
  int timeoutMs;
  int maxRetries;
  object payload;
}
`

---

- Downstream subsystem RFCs reference this specification.


## 20 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| SCH-01 | Tasks execute in priority order | Priority ordering test |
| SCH-02 | Dependencies are respected | DAG execution test |
| SCH-03 | Timeouts are enforced | Timeout stress test |
| SCH-04 | Workers are isolated | Cross-task data leak test |
| SCH-05 | Backpressure is applied at watermark | Queue depth test |
| SCH-06 | Retries follow exponential backoff | Retry timing verification |

---

- **Expected Result**: New enqueues are rejected with QueueFull error.

---


## 23 Changelog
- 1.0.0: Initial release. Defined Scheduler queues.
- 1.1.0: Expanded all placeholder sections with full architecture, task models, worker pools, and compliance checklist.

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






