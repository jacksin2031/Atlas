# RFC-0008: Runtime Plugin Host

RFC: RFC-0008
Title: Runtime Plugin Host
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
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-0007 Runtime IPC Architecture
  - RFC-0009 Runtime Resource Management
Required By:
  - RFC-0010 Runtime Manifest Specification
  - RFC-0013 Runtime Contracts
Supersedes: None
Superseded By: None
Category: Runtime
Layer: Core Runtime
Normative: YES
Audience: Systems Engineers
ADR References:
  - ADR-0005
  - ADR-0010
  - ADR-0012
Constitution References:
  - Section 5.1 (Sandboxing)
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
This specification is Normative. Every Atlas Runtime implementation MUST conform to the plugin loading lifecycles, sandbox memory allocations, WebAssembly VM execution parameters, and dynamic hook bindings defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and ADR-0012.

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
4. [Plugin Philosophy](#4-plugin-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Plugin Sandbox Architecture](#8-plugin-sandbox-architecture)
9. [WASM Virtual System Specification](#9-wasm-virtual-system-specification)
10. [Plugin Lifecycle Coordination](#10-plugin-lifecycle-coordination)
11. [Hook Registration and Bindings](#11-hook-registration-and-bindings)
12. [Plugin Loading Sequence](#12-plugin-loading-sequence)
13. [Dynamic Hook Invocation Flow](#13-dynamic-hook-invocation-flow)
14. [Security and Syscall Throttling](#14-security-and-syscall-throttling)
15. [Memory Page Caps and Isolation](#15-memory-page-caps-and-isolation)
16. [Performance Budgets](#16-performance-budgets)
17. [Exposed Plugin Manager APIs](#17-exposed-plugin-manager-apis)
18. [Normative Contracts](#18-normative-contracts)
19. [Compliance Checklist](#19-compliance-checklist)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [References](#21-references)
22. [Changelog](#22-changelog)
23. [Compatibility](#23-compatibility)

---

- Downstream subsystem RFCs reference this specification.


## 2 Goals

- **Secure Isolation**: Plugins MUST run inside sandboxed processes. They MUST NOT access host memory or file systems directly.
- **WASM execution**: The host MUST support executing compiled WASM binaries inside memory-isolated sandboxes.
- **Topological Lifecycle Gates**: Plugins MUST transition through a standard lifecycle (Discover, Load, Validate, Initialize, Activate, Suspend, Unload).
- **Dynamic Event Hooks**: Plugins MUST register event handlers with the Event Bus (refer to RFC-0005) without modifying the coordinator codebase.
- **Resource Constraints**: The Plugin Manager MUST limit CPU slices, memory size, and execution duration per plugin context.

---



## 4 Plugin Philosophy

1. **Isolation by Default**: Plugins start with zero permissions. Host resource accesses require explicit entitlement declarations.
2. **Deterministic Interfaces**: Communication across boundaries occurs via serialized message schemas (refer to RFC-0007).
3. **Graceful Release**: Unloaded plugins release all allocated file handles and memory.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |


## 6 Boundaries

- **Plugin Host may communicate with**:
  - Service Registry (refer to RFC-0003)
  - Event Bus (refer to RFC-0005)
  - Security Manager
- **Plugin Host MUST NOT communicate with**:
  - OS Kernels directly (all calls are sandboxed)
  - Presentation UI components directly

---



## 8 Plugin Sandbox Architecture

The Plugin Sandbox isolates each plugin execution context from the host process. The sandbox architecture has two layers: the Process Boundary and the VM Boundary.

`mermaid
graph TD
    subgraph HostProcess ["Host Process (Core Runtime)"]
        PM[Plugin Manager]
        SRV[Service Registry]
        EB[Event Bus]
    end

    subgraph Sandbox1 ["Plugin A Sandbox"]
        WASM1[WASM Runtime]
        MEM1[Memory Pool: 64MB]
        SYS1[System Call Filter]
    end

    subgraph Sandbox2 ["Plugin B Sandbox"]
        WASM2[WASM Runtime]
        MEM2[Memory Pool: 64MB]
        SYS2[System Call Filter]
    end

    PM -->|Load Plugin A| WASM1
    PM -->|Load Plugin B| WASM2
    WASM1 --> SYS1
    WASM2 --> SYS2
    SYS1 -->|Allowed calls only| HOST_API[Host API Gateway]
    SYS2 -->|Allowed calls only| HOST_API
    HOST_API --> PM
`

### 8.1 Process Boundary

Each plugin runs in a separate process. The process boundary prevents memory corruption in one plugin from affecting another. Process creation and termination are managed by the Plugin Manager.

### 8.2 VM Boundary

Within each process, the WASM runtime provides a second isolation layer. The WASM module has no direct access to host memory, file system, or network. All access is mediated through the Host API Gateway.

---

---

|---|---|---|
| Discover | Scan plugin directory, parse manifest | 5,000 ms |
| Load | Read plugin binary into sandbox | 10,000 ms |
| Validate | Verify signature, check permissions | 2,000 ms |
| Initialize | Call plugin initialize() | 15,000 ms |
| Activate | Register hooks, open event subscriptions | 5,000 ms |
| Suspend | Pause plugin execution, save state | 10,000 ms |
| Resume | Restore state, re-open subscriptions | 10,000 ms |
| Unload | Call plugin deinitialize(), release resources | 15,000 ms |

---


## 12 Plugin Loading Sequence

The following sequence details how a plugin is loaded and activated:

`mermaid
sequenceDiagram
    autonumber
    participant PM as Plugin Manager
    participant FS as File System
    participant VM as WASM VM
    participant EB as Event Bus
    participant Reg as Service Registry

    PM->>FS: scan(plugin_dir)
    FS-->>PM: plugin_manifests[]
    loop For each manifest
        PM->>PM: validate(manifest)
        PM->>VM: instantiate(wasm_binary)
        VM-->>PM: module_handle
        PM->>VM: initialize(module_handle)
        VM-->>PM: initialized
        PM->>Reg: registerPlugin(module_handle)
        PM->>EB: subscribe(hooks)
    end
    PM->>PM: all_plugins_active
`

---

This specification IS responsible for:
- Defining the architecture and requirements for this subsystem.


## 14 Security and Syscall Throttling

### 14.1 Permission Model

Plugins declare required permissions in their manifest. The Plugin Manager grants permissions at load time:

| Permission | Description | Default |
|---|---|---|
| filesystem.read | Read from workspace files | Denied |
| filesystem.write | Write to workspace files | Denied |
| network.outbound | Make outbound network calls | Denied |
| network.inbound | Accept inbound connections | Denied |
| process.spawn | Spawn child processes | Denied |
| environment.read | Read environment variables | Allowed |
| event.publish | Publish to Event Bus | Allowed |
| event.subscribe | Subscribe to Event Bus | Allowed |

### 14.2 Syscall Throttling

Each plugin sandbox is throttled at the syscall level:

- **Max syscalls per second**: 10,000 per plugin.
- **Max file descriptors**: 64 per plugin.
- **Max network connections**: 8 per plugin.

Exceeding these limits results in a SyscallLimitExceeded error and temporary sandbox suspension.

---

This specification IS NOT responsible for:
- Implementation details (see related RFCs).
- Cross-cutting concerns handled by other subsystems.


## 16 Performance Budgets

| Metric | Target Budget Limit | Measurement Context |
|---|---|---|
| Plugin Load | 10,000 ms | Full load from disk to Active |
| Hook Invocation | 500 ms | Single hook handler execution |
| Sandbox Creation | 5,000 ms | WASM VM instantiation |
| Plugin Unload | 15,000 ms | Full cleanup and process termination |
| Memory Allocation | 1 ms | Memory pool reservation |

---

  // Get the status of all loaded plugins.
  PluginStatus[] getPluginStatus();
}
`

---


## 19 Compliance Checklist

| # | Requirement | Verification Method |
|---|---|---|
| PLG-01 | Plugins run in isolated sandboxes | Process isolation test |
| PLG-02 | Memory limits are enforced | Memory overflow test |
| PLG-03 | Syscall filtering works correctly | Syscall interception test |
| PLG-04 | Plugin lifecycle transitions are correct | Lifecycle state machine test |
| PLG-05 | Hook timeouts are enforced | Hook timeout stress test |
| PLG-06 | Plugin crashes do not affect host | Crash containment test |

---

- **Expected Result**: Allocation fails with MemoryLimitExceeded error.

---



## 22 Changelog
- 1.0.0: Initial release. Defined sandboxing, loading, and hooks.
- 1.1.0: Expanded all placeholder sections with full sandbox architecture, WASM spec, and compliance checklist.

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







