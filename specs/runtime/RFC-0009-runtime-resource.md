# RFC-0009: Runtime Resource Management

RFC: RFC-0009
Title: Runtime Resource Management
Status: Frozen
Version: 1.0.0
Author: Atlas Team
Reviewers: Atlas Specification Committee
Created: 2026-06-27
Last Updated: 2026-06-30
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
Required By:
  - RFC-0008 Runtime Plugin Host
  - RFC-0010 Runtime Manifest Specification
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 4.1 (Resource Throttling)
Related RFCs:
  - RFC-0001 Runtime Overview
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-06-30

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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the resource monitoring thresholds, allocation quotas, VRAM limits, and throttling policies defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

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
4. [Resource Management Philosophy](#4-resource-management-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Resource Monitor Architecture](#8-resource-monitor-architecture)
9. [CPU Thread Allocation and Affinity](#9-cpu-thread-allocation-and-affinity)
10. [RAM Heap Limits and Isolation](#10-ram-heap-limits-and-isolation)
11. [GPU Context Lock and VRAM Quotas](#11-gpu-context-lock-and-vram-quotas)
12. [Disk I/O Bandwidth Sandboxing](#12-disk-io-bandwidth-sandboxing)
13. [Screen Capture Frame Buffers](#13-screen-capture-frame-buffers)
14. [AI and Vision Model Caching](#14-ai-and-vision-model-caching)
15. [Plugin Sandbox Resource Caps](#15-plugin-sandbox-resource-caps)
16. [Resource Allocation Flowchart](#16-resource-allocation-flowchart)
17. [Eviction and Cleanup Policies](#17-eviction-and-cleanup-policies)
18. [Security and Privilege Separation](#18-security-and-privilege-separation)
19. [Performance Budgets](#19-performance-budgets)
20. [Exposed Resource Manager APIs](#20-exposed-resource-manager-apis)
21. [Standard Resource Event Schema](#21-standard-resource-event-schema)
22. [Normative Contracts](#22-normative-contracts)
23. [Compliance Checklist](#23-compliance-checklist)
24. [Acceptance Criteria](#24-acceptance-criteria)
25. [References](#25-references)
26. [Changelog](#26-changelog)
27. [Compatibility](#27-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Starvation Prevention**: The Resource Manager MUST prioritize real-time vision capture and event loop threads over background tasks.
- **VRAM Allocation Quotas**: GPU memory allocations MUST be validated and locked before loading local AI or Vision models.
- **Sandbox Isolation**: Memory pools allocated to plugins and workflows MUST be isolated to prevent memory leaks or exhaustion.
- **Throttling Policies**: The system MUST throttle task dispatching when CPU or RAM utilization crosses critical thresholds.
- **Cache Eviction**: Non-active models and frame caches MUST be evicted from RAM/VRAM using Least-Recently-Used (LRU) rules.

---



## 4 Resource Management Philosophy

1. **Safety Budgets Override Execution**: If RAM utilization crosses critical limits, workflows are paused to prevent host crashes.
2. **Deterministic Allocations**: Buffers (such as vision frame buffers) reuse pre-allocated memory slices.
3. **Defense-in-Depth Control**: Subsystems cannot access hardware contexts directly.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Resource Manager may communicate with**:
  - Scheduler (refer to RFC-0004)
  - Event Bus (refer to RFC-0005)
  - Service Registry (refer to RFC-0003)
- **Resource Manager MUST NOT communicate with**:
  - Outside model marketplaces
  - UI presentation controls directly

---



## 8 Resource Monitor Architecture

The Resource Monitor consists of four subsystems: the CPU Monitor, the Memory Monitor, the GPU Monitor, and the Disk I/O Monitor.

`mermaid
graph TD
    RM[Resource Manager] --> CM[CPU Monitor]
    RM --> MM[Memory Monitor]
    RM --> GM[GPU Monitor]
    RM --> DIM[Disk I/O Monitor]
    CM --> TH[Thread Heaper]
    MM --> HEAP[Heap Allocator]
    GM --> VRAM[VRAM Allocator]
    DIM --> DISK[Disk I/O Scheduler]
    RM --> SB[Throttle Broker]
    SB --> SCH[Scheduler]
    SB --> PLG[Plugin Host]
`

---


## 10 RAM Heap Limits and Isolation

### 10.1 Heap Allocation

The Runtime maintains a dedicated heap for each subsystem:

| Subsystem | Default Heap | Maximum Heap |
|---|---|---|
| Core Runtime | 256 MB | 1 GB |
| Workflow Engine | 512 MB | 2 GB |
| Vision Engine | 1 GB | 4 GB |
| AI Engine | 2 GB | 8 GB |
| Plugin Sandboxes | 64 MB each | 512 MB each |

### 10.2 Heap Isolation

Heaps are isolated between subsystems. A memory leak in one subsystem does not affect others.

---

- Defining the architecture and requirements for this subsystem.


## 12 Disk I/O Bandwidth Sandboxing

### 12.1 I/O Priorities

Disk I/O is prioritized as follows:

| Priority | I/O Type | Bandwidth Share |
|---|---|---|
| Critical | State snapshot commit | Unlimited |
| High | WAL writes | 30% |
| Normal | Plugin file access | 20% |
| Background | Cache eviction, cleanup | 10% |
| Low | Log rotation | 5% |

### 12.2 I/O Throttling

When disk I/O latency exceeds 100 ms, the Resource Manager reduces background I/O bandwidth by 50%.

---

- Cross-cutting concerns handled by other subsystems.


## 14 AI and Vision Model Caching

### 14.1 Model Cache

Models are cached in RAM and VRAM for fast loading:

| Cache Tier | Location | Eviction Policy |
|---|---|---|
| Hot | VRAM | Never (until model swap) |
| Warm | RAM | LRU after 5 minutes idle |
| Cold | Disk | LRU after 1 hour idle |

### 14.2 Cache Size Limits

| Tier | Default Limit | Maximum |
|---|---|---|
| Hot (VRAM) | 50% of available VRAM | 80% of available VRAM |
| Warm (RAM) | 2 GB | 8 GB |
| Cold (Disk) | 10 GB | 50 GB |

---


## 16 Resource Allocation Flowchart

`mermaid
flowchart TD
    Request[Resource Request] --> Check{Available?}
    Check -->|Yes| Allocate[Allocate Resource]
    Check -->|No| Queue[Queue Request]
    Queue --> Wait{Timeout?}
    Wait -->|No| Check
    Wait -->|Yes| Reject[Reject Request]
    Allocate --> Use[Use Resource]
    Use --> Release[Release Resource]
    Release --> Check
`

---

- Defining the architecture and requirements for this subsystem.


## 18 Security and Privilege Separation

### 18.1 Privilege Levels

Resource access is divided into privilege levels:

| Level | Access | Examples |
|---|---|---|
| Admin | All resources | Runtime supervisor |
| Service | Allocated resources | Workflow engine, Vision engine |
| Plugin | Sandboxed resources | Third-party plugins |
| Guest | Read-only resources | Telemetry collectors |

### 18.2 Resource Auditing

All resource allocations and releases are logged with:
- Timestamp
- Allocating service
- Resource type and size
- Allocation ID

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 20 Exposed Resource Manager APIs

`
interface ResourceManager {
  // Allocate a resource with the given constraints.
  ResourceHandle allocate(ResourceRequest request);

  // Release an allocated resource.
  void release(ResourceHandle handle);

  // Check current resource utilization.
  ResourceUtilization getUtilization();

  // Set resource limits for a subsystem.
  void setLimits(string subsystem, ResourceLimits limits);

  // Get resource events.
  Subscription subscribeToEvents(EventHandler handler);
}
`

---

- Defining the architecture and requirements for this subsystem.


## 22 Normative Contracts

- Every resource allocation MUST be logged.
- Every resource release MUST be matched to a prior allocation.
- Resource quotas MUST NOT be exceeded under normal operation.
- Emergency cleanup MUST preserve at least 5% of host memory free.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 24 Acceptance Criteria

### AC-091
- **Requirement**: Host memory exceeding 95% MUST trigger emergency task suspensions.
- **Verification**: Fill host memory to 95% and observe behavior.
- **Expected Result**: Non-critical workflows are paused; critical services continue.

### AC-092
- **Requirement**: Real-time frame capture threads MUST run on dedicated CPU cores.
- **Verification**: Inspect thread affinity masks for capture threads.
- **Expected Result**: Capture threads are pinned to Core 1.

### AC-093
- **Requirement**: VRAM allocation MUST be locked before model loading.
- **Verification**: Attempt to load a model without a VRAM lock.
- **Expected Result**: Load is rejected with VRAMLockedError.

### AC-094
- **Requirement**: Plugin sandbox memory MUST NOT exceed configured heap caps.
- **Verification**: Allocate memory beyond the heap cap inside a plugin.
- **Expected Result**: Allocation fails with MemoryLimitExceeded.

### AC-095
- **Requirement**: Cache eviction MUST follow LRU order.
- **Verification**: Access a set of cached models in a specific pattern, then trigger eviction.
- **Expected Result**: Least-recently-used models are evicted first.

---


## 26 Changelog
- 1.0.0: Initial release. Defined memory caps and VRAM context locks.
- 1.1.0: Expanded all placeholder sections with full resource architecture, quotas, and compliance checklist.

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






