# RFC-0225: Plugin Hot Reload

RFC: RFC-0225
Title: Plugin Hot Reload
Status: Proposed
Version: 1.0.0
Category: Plugin Operations
Layer: Runtime
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0203 Plugin Lifecycle
  - RFC-0215 Plugin Service Model
Related RFC:
  - RFC-0216 Plugin Discovery
  - RFC-0217 Plugin Packaging
  - RFC-0224 Plugin Testing
Related ADR:
  - ADR-0025 Hot Reload Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the hot reload lifecycle (load, activate, suspend, unload, reload, recover), reload eligibility, reload budget, resource cleanup, event cleanup, service cleanup, state preservation, and rollback requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Hot Reload Philosophy](#4-hot-reload-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Hot Reload Lifecycle](#9-hot-reload-lifecycle)
10. [Reload Eligibility](#10-reload-eligibility)
11. [Reload Budget](#11-reload-budget)
12. [Resource Cleanup](#12-resource-cleanup)
13. [Event Cleanup](#13-event-cleanup)
14. [Service Cleanup](#14-service-cleanup)
15. [State Preservation](#15-state-preservation)
16. [Rollback](#16-rollback)
17. [Performance Budgets](#17-performance-budgets)
18. [Glossary](#18-glossary)
19. [Acceptance Criteria](#19-acceptance-criteria)
20. [Cross References](#20-cross-references)
21. [References](#21-references)
22. [Revision History](#22-revision-history)
23. [Future Evolution](#23-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Zero-Downtime Reload**: Plugins can be reloaded without restarting the runtime.
2. **Selective Reload**: Not all plugins support hot reload; eligibility is clearly defined.
3. **Budget Management**: Reload operations are bounded to prevent resource exhaustion.
4. **Complete Cleanup**: All resources, events, and services are properly cleaned up.
5. **State Preservation**: Reusable state is preserved across reloads.
6. **Rollback**: Failed reloads roll back to the previous working version.

---

- RFC-0323 Workflow Plugin Integration


## 4 Hot Reload Philosophy

Hot reload follows these principles:

- Not all plugins can be hot-reloaded; only stateless or state-preserving plugins qualify.
- Reload operations are bounded by a budget to prevent resource exhaustion.
- All cleanup (resource, event, service) MUST be deterministic and complete.
- Failed reloads MUST roll back atomically.
- State preservation is opt-in; plugins declare what state survives a reload.

---


## 6 Boundaries

- Hot reload is confined to a single plugin instance within a single runtime.
- Cross-plugin state changes during reload are NOT supported.
- Hot reload does NOT affect plugins that do not declare reload eligibility.
- The reload budget is per-runtime, not per-plugin.

---

| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
graph TB
    subgraph Hot Reload Manager
        HM[Hot Reload Manager]
        RB[Reload Budget]
        CC[Cleanup Coordinator]
        SP[State Preserver]
        RL[Rollback Engine]
    end
    subgraph Plugin States
        LD[Loaded]
        ACT[Activated]
        SUS[Suspended]
        UNLD[Unloaded]
        RLD[Reloaded]
        REC[Recovered]
    end
    HM -->|orchestrate| LD
    LD -->|suspend| SUS
    SUS -->|cleanup| CC
    CC -->|unload| UNLD
    UNLD -->|preserve state| SP
    SP -->|load new| RLD
    RLD -->|activate| ACT
    ACT -->|recover state| REC
    RL -.->|on failure| LD
`

---

- All event subscriptions are removed.
- All resource handles are released.
- The plugin is transitioned to the Unloaded state.

### 9.4 Reload

The new plugin instance is activated.

- The new services are registered.
- The new event subscriptions are established.
- The new resources are loaded into the cache.
- The plugin is transitioned to the Activated state.

### 9.5 Recover

Preserved state is restored to the new plugin instance.

- State that was preserved during Unload is reapplied.
- Services that support state recovery reinitialize from preserved data.
- The plugin is transitioned to the Recovered state.

### 9.6 Resume

The plugin resumes normal operation.

- Paused workflows are resumed.
- Drained requests are processed by the new instance.
- The plugin is fully operational.

`mermaid
stateDiagram-v2
    [*] --> Loaded
    Loaded --> Suspended: reload_requested
    Suspended --> Unloaded: drain_complete
    Unloaded --> Reloaded: new_instance_loaded
    Reloaded --> Recovered: state_restored
    Recovered --> Activated: resume_completed
    Activated --> [*]
    Loaded --> RolledBack: reload_failed
    RolledBack --> Loaded: rollback_complete
`

---

### 10.2 Ineligible Plugins

Plugins that CANNOT be hot-reloaded:

| Plugin Type              | Not Eligible | Reason                                        |
|--------------------------|--------------|-----------------------------------------------|
| Model Runner             | No           | Holds loaded model weights in memory          |
| Database Connector       | No           | Maintains persistent connections              |
| Network Gateway          | No           | Active socket connections                     |
| Kernel Driver            | No           | OS-level state, cannot be unloaded safely     |
| Scheduler                | No           | Active timer jobs and queues                  |
| State Machine            | No           | Complex internal state that cannot be serialized |
| Security Module          | No           | Active security context and session tokens    |

### 10.3 Conditional Eligibility

Plugins that ARE eligible only under certain conditions:

| Plugin Type              | Condition                                  |
|--------------------------|--------------------------------------------|
| Vision Processor         | Eligible only if no active image processing |
| Storage Provider         | Eligible only if no pending write operations |
| IPC Bridge               | Eligible only if all channels are idle     |

Conditional plugins MUST declare their conditions in the manifest.

---




## 13 Event Cleanup

During the Unload phase, all event subscriptions are removed:

`
Event Cleanup Order:
1. Unsubscribe from all event channels
2. Drain all pending event handlers
3. Cancel all in-flight event processing
4. Remove all event listeners from the event bus
`

Rules:
- Event cleanup MUST complete before the plugin is unloaded.
- Pending events are either drained or discarded (configurable).
- Event cleanup timeout: 3 seconds.
- Orphaned event handlers are automatically unregistered by the runtime.

---



## 15 State Preservation

Plugins declare what state survives a reload:

`json
{
  "state_preservation": {
    "enabled": true,
    "preserved_keys": ["user_preferences", "computed_cache", "session_tokens"],
    "max_preserved_size_kb": 512,
    "serialization_format": "json"
  }
}
`

Preservation rules:
- Only keys explicitly declared in preserved_keys are saved.
- State is serialized using the declared format (default: JSON).
- Maximum preserved state size is enforced (default: 512 KB).
- State is stored in memory during the reload window.
- State is applied to the new instance during the Recover phase.
- If state serialization fails, the reload proceeds WITHOUT preserved state (graceful degradation).

---

        RB->>P: Restore previous version
        P-->>HM: Rollback complete
    end

    HM->>P: Phase 4: Reload
    alt Reload fails
        HM->>RB: Trigger rollback
        RB->>P: Restore previous version
        P-->>HM: Rollback complete
    end

    HM->>P: Phase 5: Recover
    alt Recover fails
        HM->>RB: Trigger rollback
        RB->>P: Restore previous version
        P-->>HM: Rollback complete
    end

    HM->>P: Phase 6: Resume
    Note over HM,P: Success - plugin reloaded
`

Rollback rules:
- Rollback is ATOMIC: either the new version is fully operational or the previous version is restored.
- Rollback timeout: 10 seconds.
- Failed rollbacks cause the runtime to enter a degraded state and notify the operator.
- Rollback events are logged to the audit trail.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 18 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Hot Reload        | Reloading a plugin at runtime without restarting.    |
| Reload Budget     | Limits on reload frequency, duration, and resources. |
| State Preservation| Saving plugin state across a reload.                 |
| Rollback          | Restoring the previous version on reload failure.    |
| Drain             | Waiting for in-flight work to complete.              |

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Cross References

- RFC-0201 Plugin Overview
- RFC-0203 Plugin Lifecycle
- RFC-0215 Plugin Service Model
- RFC-0216 Plugin Discovery
- RFC-0217 Plugin Packaging
- RFC-0224 Plugin Testing

---



## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

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

## 22 Revision History

| Date       | Version | Author                    | Change                           |
|------------|---------|---------------------------|----------------------------------|
| 2026-07-01 | 1.0.0   | Atlas Specification Committee | Initial proposal               |

---


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

All contracts in this specification are defined as abstract behavioral interfaces.

---



