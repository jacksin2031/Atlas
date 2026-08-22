# RFC-0203: Plugin Lifecycle

RFC: RFC-0203
Title: Plugin Lifecycle
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0002 Runtime Lifecycle
  - RFC-0008 Runtime Plugin Host
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1006 Common Error Model
Related RFC:
  - RFC-0201 Plugin Overview
  - RFC-0204 Plugin Loader
  - RFC-0205 Plugin Registry
  - RFC-0210 Plugin Events
Related ADR:
  - ADR-0005 Plugin Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the plugin lifecycle state machine, transitions, hooks, events, and recovery procedures defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Lifecycle Philosophy](#4-lifecycle-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [State Machine Architecture](#8-state-machine-architecture)
9. [Lifecycle States](#9-lifecycle-states)
10. [Lifecycle Transitions](#10-lifecycle-transitions)
11. [Lifecycle Hooks](#11-lifecycle-hooks)
12. [Lifecycle Events](#12-lifecycle-events)
13. [Timeout Management](#13-timeout-management)
14. [Recovery Procedures](#14-recovery-procedures)
15. [Performance Budgets](#15-performance-budgets)
16. [Glossary](#16-glossary)
17. [Acceptance Criteria](#17-acceptance-criteria)
18. [Cross References](#18-cross-references)
19. [References](#19-references)
20. [Revision History](#20-revision-history)
21. [Future Evolution](#21-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Deterministic State Transitions**: Every plugin MUST follow the defined finite state machine. Invalid transitions MUST be rejected.
2. **Observable Transitions**: Every state change MUST produce a lifecycle event on the Event Bus.
3. **Timeout Enforcement**: Each lifecycle phase MUST have a maximum duration. Exceeding the timeout MUST trigger failure handling.
4. **Recovery from Failure**: Failed transitions MUST follow defined recovery procedures including rollback, retry, and forced removal.
5. **Hook Extensibility**: Plugins MAY register lifecycle hooks that are invoked at defined transition points.
6. **Ownership Clarity**: The Platform owns the state machine enforcement. Plugin authors own the hook implementations.
7. **Partial Failure Handling**: If a plugin fails during a multi-step transition, partial effects MUST be rolled back.
8. **Consistent Cleanup**: Unloading plugins MUST release all acquired resources regardless of the failure mode.

---


## 4 Lifecycle Philosophy

1. **State Machine Enforcement**: The lifecycle state machine is authoritative. No plugin MAY exist in a state not defined by this specification.
2. **Transition Atomicity**: Each lifecycle transition is atomic. Either the full transition succeeds or the plugin returns to its previous state.
3. **Event-Driven Observation**: Every state transition produces an event. Observers react to events, not state polling.
4. **Graceful Degradation**: Plugins SHOULD enter a SUSPENDED state rather than FAILED when resources are temporarily unavailable.
5. **Defensive Cleanup**: Every exit path from every state MUST release all acquired resources. No resource leak is acceptable.

---



## 6 Boundaries

- **Lifecycle Manager MAY communicate with**:
  - Plugin Loader (RFC-0204) for load/unload operations
  - Plugin Registry (RFC-0205) for state updates
  - Plugin Sandbox Manager (RFC-0208) for sandbox lifecycle
  - Event Bus (RFC-0210) for lifecycle event publication
  - Security Manager (RFC-0207) for security event generation

- **Lifecycle Manager MUST NOT communicate with**:
  - Plugin extension logic directly
  - External update servers
  - User-facing interfaces

---

| RFC-0201 | Consumed | Plugin Overview |


## 8 State Machine Architecture

`mermaid
stateDiagram-v2
    [*] --> DISCOVERED
    DISCOVERED --> VALIDATING: install()
    VALIDATING --> LOADED: validation passes
    VALIDATING --> FAILED: validation fails
    LOADED --> INITIALIZING: initialize()
    INITIALIZING --> ACTIVATING: initialization succeeds
    INITIALIZING --> ERROR: initialization fails
    ACTIVATING --> ACTIVE: activation succeeds
    ACTIVATING --> ERROR: activation fails
    ACTIVE --> RUNNING: start execution
    RUNNING --> SUSPENDING: suspend()
    RUNNING --> DEACTIVATING: deactivate()
    RUNNING --> UPDATING: update()
    RUNNING --> REMOVING: remove()
    SUSPENDING --> SUSPENDED: suspend complete
    SUSPENDED --> RESUMING: resume()
    RESUMING --> RUNNING: resume complete
    DEACTIVATING --> DEACTIVATED: deactivation complete
    DEACTIVATED --> UNLOADING: unload()
    UNLOADING --> UNLOADED: unload complete
    UNLOADED --> [*]
    ERROR --> FAILED: unrecoverable
    FAILED --> [*]
    UPDATING --> LOADED: update succeeds
    UPDATING --> ROLLING-BACK: update fails
    ROLLING-BACK --> LOADED: rollback succeeds
    ROLLING-BACK --> FAILED: rollback fails
    REMOVING --> REMOVED: removal complete
    REMOVED --> [*]
`

State classification:

| Category | States | Description |
|---|---|---|
| Pre-Activation | DISCOVERED, VALIDATING, LOADED, INITIALIZING, ACTIVATING | Plugin preparation phases |
| Active | ACTIVE, RUNNING | Plugin operational phases |
| Suspension | SUSPENDING, SUSPENDED, RESUMING | Plugin pause/resume phases |
| Deactivation | DEACTIVATING, DEACTIVATED, UNLOADING, UNLOADED | Plugin teardown phases |
| Update | UPDATING, ROLLING-BACK | Plugin update phases |
| Removal | REMOVING, REMOVED | Plugin removal phases |
| Error | ERROR, FAILED | Plugin error phases |

---


### 9.9 SUSPENDED (PSTATE-SUSPENDED)
The plugin is paused. No extension logic is executing. Event subscriptions are inactive. Resources are retained but not consumed.

### 9.10 RESUMING (PSTATE-RESUMING)
The plugin is transitioning from SUSPENDED back to RUNNING. Event subscriptions are restored and active operations are restarted.

### 9.11 DEACTIVATING (PSTATE-DEACTIVATING)
The plugin is in the process of being deactivated. Extension points are being unregistered and event subscriptions are being removed.

### 9.12 DEACTIVATED (PSTATE-DEACTIVATED)
The plugin is fully deactivated. Extension points and event subscriptions are removed. Resources are released but the plugin artifact remains loaded.

### 9.13 UNLOADING (PSTATE-UNLOADING)
The plugin is being removed from the Registry. Manifest entries are being purged and registry metadata is being updated.

### 9.14 UNLOADED (PSTATE-UNLOADED)
The plugin has been completely removed from the platform. It no longer exists in the Registry and all traces are cleared.

### 9.15 UPDATING (PSTATE-UPDATING)
The plugin is being replaced with a newer version. The old version continues RUNNING while the new version is validated and initialized.

### 9.16 ROLLING-BACK (PSTATE-ROLLING-BACK)
The update failed and the plugin is reverting to the previous version. The new version is being discarded.

### 9.17 REMOVING (PSTATE-REMOVING)
The plugin is being permanently removed from the platform. All associated data is being cleaned up.

### 9.18 REMOVED (PSTATE-REMOVED)
The plugin has been permanently removed. All traces including registry entries, events, and audit records are archived.

### 9.19 ERROR (PSTATE-ERROR)
A transient error occurred during a lifecycle transition. The plugin may be recoverable through retry.

### 9.20 FAILED (PSTATE-FAILED)
The plugin has entered a terminal failure state. Administrative intervention is required to resolve.

---

| UPDATING -> ROLLING-BACK | update fails | New version partially initialized | Rollback begins | 5,000 ms |
| ROLLING-BACK -> LOADED | rollback succeeds | Previous version restored | New version discarded | Immediate |
| ROLLING-BACK -> FAILED | rollback fails | Previous version corrupted | Terminal failure recorded | Immediate |
| REMOVING -> REMOVED | removal complete | All data cleaned up | Plugin permanently removed | Immediate |

---



## 13 Timeout Management

Each lifecycle transition has a default timeout defined in Section 10. Timeouts are enforced by the Platform. Exceeding a timeout triggers the following sequence:

`mermaid
flowchart TD
    A[Transition Starts] --> B[Timer Started]
    B --> C{Timeout Reached}
    C -->|No| D[Transition Completes]
    C -->|Yes| E[Timeout Event Generated]
    E --> F{Retry Available}
    F -->|Yes| G[Retry with Backoff]
    G --> B
    F -->|No| H[Transition Fails]
    H --> I[Plugin Enters ERROR State]
    I --> J[on_error Hook Invoked]
    J --> K{Recoverable}
    K -->|Yes| L[Attempt Recovery]
    L --> M{Success}
    M -->|Yes| D
    M -->|No| N[Plugin Enters FAILED State]
    K -->|No| N
`

Timeout rules:
- Default timeouts are defined in the transition table (Section 10).
- Plugins MAY declare custom timeouts in their manifest, but custom timeouts MUST NOT exceed platform maximums.
- Platform maximum timeout for any single transition: 30,000 ms.
- Maximum retry attempts: 3.
- Retry backoff: exponential, starting at 100 ms with a multiplier of 2.
- Timeout violations MUST produce a PEVT-FAILED event with PERR-LIFECYCLE-TIMEOUT error code.

---


|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 16 Glossary

| Term | Definition |
|---|---|
| Lifecycle State | A discrete phase in the plugin existence timeline. |
| Transition | A directed edge in the state machine representing a state change. |
| Hook | A plugin-registered callback invoked at a transition point. |
| Timeout | The maximum duration allowed for a transition to complete. |
| Recovery | The procedure for restoring a plugin to a functional state after failure. |
| Rollback | The procedure for reverting to a previous plugin version after update failure. |

---

- **Expected Result**: All transitions have at least one postcondition.

#### AC-0203-006
- **Requirement**: Every transition MUST have a default timeout.
- **Verification**: Inspect the transition table in Section 10 for timeout columns.
- **Expected Result**: All transitions have timeout values defined.

#### AC-0203-007
- **Requirement**: The state machine MUST prevent transitions to undefined states.
- **Verification**: Attempt a transition to a state not in the defined set.
- **Expected Result**: The transition is rejected with an error event.

#### AC-0203-008
- **Requirement**: The state machine MUST prevent invalid transition sequences.
- **Verification**: Attempt a transition from a state that does not define the requested edge.
- **Expected Result**: The transition is rejected and a PEVT-FAILED event is published.

#### AC-0203-009
- **Requirement**: The FAILED state MUST be terminal without administrative intervention.
- **Verification**: Check if any automatic transition exits the FAILED state.
- **Expected Result**: No automatic exit transitions from FAILED exist.

#### AC-0203-010
- **Requirement**: The RUNNING state MUST be reachable from DISCOVERED through a valid path.
- **Verification**: Trace the path: DISCOVERED -> VALIDATING -> LOADED -> INITIALIZING -> ACTIVATING -> ACTIVE -> RUNNING.
- **Expected Result**: All transitions in the path are defined.

### Lifecycle Hooks

#### AC-0203-011
- **Requirement**: The specification MUST define at least eighteen lifecycle hooks.
- **Verification**: Count hook entries in Section 11.
- **Expected Result**: Nineteen hooks are defined.

#### AC-0203-012
- **Requirement**: Every hook MUST have a defined invocation timing (pre-transition or post-transition).
- **Verification**: Inspect the direction column in the hooks table.
- **Expected Result**: All hooks specify pre-transition or post-transition.

#### AC-0203-013
- **Requirement**: Every hook MUST have a defined timeout.
- **Verification**: Inspect the timeout column in the hooks table.
- **Expected Result**: All hooks have timeout values not exceeding 2,000 ms.

#### AC-0203-014
- **Requirement**: Hook failures MUST NOT prevent the lifecycle transition from completing.
- **Verification**: Invoke a hook that fails during a transition.
- **Expected Result**: The transition completes; the hook failure is logged as a warning event.

#### AC-0203-015
- **Requirement**: Hooks MUST be invoked in the order: pre-transition hooks, transition, post-transition hooks.
- **Verification**: Instrument hook invocation order during a transition.
- **Expected Result**: All pre-transition hooks execute before the transition; all post-transition hooks execute after.

### Timeout Management

#### AC-0203-016
- **Requirement**: Every lifecycle transition MUST have an enforceable timeout.
- **Verification**: Inspect the transition table for timeout values.
- **Expected Result**: All twenty-five transitions have timeout values.

#### AC-0203-017
- **Requirement**: No transition timeout MAY exceed 30,000 ms.
- **Verification**: Scan all timeout values in the transition table and manifest declarations.
- **Expected Result**: No timeout exceeds 30,000 ms.

#### AC-0203-018
- **Requirement**: Timeout violations MUST produce a PEVT-FAILED event with PERR-LIFECYCLE-TIMEOUT.
- **Verification**: Simulate a transition that exceeds its timeout.
- **Expected Result**: A PEVT-FAILED event is published with the correct error code.

#### AC-0203-019
- **Requirement**: The system MUST support at least three retry attempts for timeout failures.
- **Verification**: Inspect the timeout management section in Section 13.
- **Expected Result**: Maximum retry attempts is defined as 3.

#### AC-0203-020
- **Requirement**: Retry backoff MUST use exponential growth.
- **Verification**: Inspect the timeout management section for backoff rules.
- **Expected Result**: Exponential backoff with starting value 100 ms and multiplier 2 is defined.

### Event Production

#### AC-0203-021
- **Requirement**: Every state transition MUST produce a lifecycle event.
- **Verification**: Inspect the transition table and event catalog for coverage.
- **Expected Result**: All transitions map to a defined event.

#### AC-0203-022
- **Requirement**: All lifecycle events MUST conform to the common event model (RFC-1001).
- **Verification**: Compare event structures in Section 12 with RFC-1001 schema.
- **Expected Result**: All events include eventId, eventName, category, version, timestamp, source, and payload.

#### AC-0203-023
- **Requirement**: The specification MUST define at least fourteen lifecycle event types.
- **Verification**: Count event entries in Section 12.
- **Expected Result**: Sixteen events are defined.

#### AC-0203-024
- **Requirement**: Each lifecycle event MUST include the plugin_id in its payload.
- **Verification**: Inspect payload fields for all events in Section 12.
- **Expected Result**: plugin_id is present in every event payload.

#### AC-0203-025
- **Requirement**: Lifecycle events MUST be published to the Event Bus before the state is updated.
- **Verification**: Inspect the transition enforcement procedure.
- **Expected Result**: Event publication precedes state update in the transition sequence.

### Recovery

#### AC-0203-026
- **Requirement**: The specification MUST define automatic recovery procedures for at least three failure modes.
- **Verification**: Inspect Section 14.1 for automatic recovery entries.
- **Expected Result**: Capability unavailability, extension registration failure, and resource acquisition timeout are covered.

#### AC-0203-027
- **Requirement**: The specification MUST define manual recovery procedures for at least four failure modes.
- **Verification**: Inspect Section 14.2 for manual recovery entries.
- **Expected Result**: Manifest validation failure, security violation, terminal failure, and data corruption are covered.

#### AC-0203-028
- **Requirement**: The rollback procedure MUST restore the previous plugin version.
- **Verification**: Inspect Section 14.3 for rollback steps.
- **Expected Result**: All five rollback steps are defined including unregistering, restoring, and event publication.

#### AC-0203-029
- **Requirement**: Rollback MUST complete within 5,000 ms.
- **Verification**: Inspect the performance budgets table in Section 15.
- **Expected Result**: Rollback Execution budget is 5,000 ms.

#### AC-0203-030
- **Requirement**: A PEVT_ROLLBACK event MUST be published after rollback completion.
- **Verification**: Inspect Section 14.3 step 5.
- **Expected Result**: The event publication step is defined.

### Resource Cleanup

#### AC-0203-031
- **Requirement**: Every transition exit path MUST release all acquired resources.
- **Verification**: Trace resource acquisition and release for each transition.
- **Expected Result**: No transition path leaves resources unreleased.

#### AC-0203-032
- **Requirement**: The ERROR state MUST trigger the on_error hook.
- **Verification**: Inspect the transition from ERROR to FAILED in Section 10.
- **Expected Result**: The on_error hook is invoked before the FAILED transition.

#### AC-0203-033
- **Requirement**: Resource leaks MUST be detectable through the health event system.
- **Verification**: Inspect the PEVT_HEALTH-DEGRADED event definition.
- **Expected Result**: The event includes degradation_type and affected_capabilities fields.

### Performance

#### AC-0203-034
- **Requirement**: State transitions MUST complete within 100 ms excluding hook execution.
- **Verification**: Benchmark transition enforcement without hooks.
- **Expected Result**: Transition time is within 100 ms budget.

#### AC-0203-035
- **Requirement**: Hook invocations MUST complete within their declared timeouts.
- **Verification**: Measure hook execution times against declared budgets.
- **Expected Result**: All hooks complete within their declared 1,000 ms budget.

### Consistency

#### AC-0203-036
- **Requirement**: The lifecycle state machine MUST be consistent with the common state model (RFC-1002).
- **Verification**: Compare state categories between RFC-1002 and Section 8.
- **Expected Result**: Plugin states conform to the common state model classification.

#### AC-0203-037
- **Requirement**: The lifecycle state machine MUST be consistent with RFC-0201 Section 10.
- **Verification**: Compare the state diagram in Section 8 with RFC-0201.
- **Expected Result**: All states and transitions match between the two documents.

#### AC-0203-038
- **Requirement**: The state classification table MUST include all twenty states.
- **Verification**: Count entries in the state classification table in Section 8.
- **Expected Result**: Seven categories covering all twenty states are listed.

#### AC-0203-039
- **Requirement**: The transition table MUST include all twenty-five valid transitions.
- **Verification**: Count entries in the transition table in Section 10.
- **Expected Result**: Twenty-five transitions are enumerated.

#### AC-0203-040
- **Requirement**: The hooks table MUST include hooks for all major lifecycle phases.
- **Verification**: Cross-reference hooks with state categories.
- **Expected Result**: Pre and post hooks exist for install, initialize, activate, suspend, resume, deactivate, unload, update, remove, and error.

### Security

#### AC-0203-041
- **Requirement**: Lifecycle events MUST be audit-logged.
- **Verification**: Inspect event definitions for audit trail references.
- **Expected Result**: All lifecycle events reference audit logging.

#### AC-0203-042
- **Requirement**: Timeout enforcement MUST be performed by the Platform, not the plugin.
- **Verification**: Inspect Section 4 lifecycle philosophy.
- **Expected Result**: The philosophy states timeouts are Platform-enforced.

#### AC-0203-043
- **Requirement**: A plugin in FAILED state MUST NOT execute any extension logic.
- **Verification**: Check transition rules for FAILED state.
- **Expected Result**: No execution transitions originate from FAILED.

#### AC-0203-044
- **Requirement**: Security violations during lifecycle transitions MUST trigger immediate suspension.
- **Verification**: Inspect the transition from RUNNING to SUSPENDING for security triggers.
- **Expected Result**: Security violations trigger SUSPENDING transition.

#### AC-0203-045
- **Requirement**: The on_error hook MUST complete within 2,000 ms.
- **Verification**: Inspect the hooks table in Section 11 for on_error timeout.
- **Expected Result**: The on_error timeout is 2,000 ms.

### Compatibility

#### AC-0203-046
- **Requirement**: The lifecycle state machine MUST support plugins with different major versions.
- **Verification**: Inspect version handling in the transition table.
- **Expected Result**: Version information is carried in lifecycle events.

#### AC-0203-047
- **Requirement**: State transitions MUST be reversible where defined.
- **Verification**: Check for bidirectional transitions in the state diagram.
- **Expected Result**: At least three pairs of reverse transitions exist (suspend/resume, update/rollback, activating/error).

#### AC-0203-048
- **Requirement**: The SUSPENDED state MUST retain all plugin resources.
- **Verification**: Inspect the SUSPENDED state definition in Section 9.9.
- **Expected Result**: The definition states resources are retained but not consumed.

#### AC-0203-049
- **Requirement**: The DEACTIVATED state MUST release all extension point registrations.
- **Verification**: Inspect the DEACTIVATED state definition in Section 9.12.
- **Expected Result**: The definition states extension points and subscriptions are removed.

#### AC-0203-050
- **Requirement**: The UNLOADED state MUST purge all registry entries.
- **Verification**: Inspect the UNLOADING transition postconditions.
- **Expected Result**: Registry entries are purged during UNLOADING.

### Edge Cases

#### AC-0203-051
- **Requirement**: Double-suspend MUST be a no-op (suspending an already suspended plugin).
- **Verification**: Attempt suspend on a plugin in SUSPENDED state.
- **Expected Result**: The operation is rejected with a benign informational event.

#### AC-0203-052
- **Requirement**: Double-unload MUST be a no-op (unloading an already unloaded plugin).
- **Verification**: Attempt unload on a plugin in UNLOADED state.
- **Expected Result**: The operation is rejected with a benign informational event.

#### AC-0203-053
- **Requirement**: Transition from DISCOVERED to RUNNING without intermediate states MUST be impossible.
- **Verification**: Attempt a direct transition from DISCOVERED to RUNNING.
- **Expected Result**: The transition is rejected; the full path through VALIDATING, LOADED, INITIALIZING, ACTIVATING, and ACTIVE is required.

#### AC-0203-054
- **Requirement**: Concurrent transitions on the same plugin MUST be prevented.
- **Verification**: Attempt two simultaneous transitions on the same plugin.
- **Expected Result**: The second transition is queued or rejected until the first completes.

#### AC-0203-055
- **Requirement**: The UPDATING state MUST allow the old version to continue RUNNING.
- **Verification**: Inspect the UPDATING transition definition.
- **Expected Result**: The old version continues running while the new version is validated.

### Observability

#### AC-0203-056
- **Requirement**: Every lifecycle event MUST include a duration_ms field where applicable.
- **Verification**: Inspect event payload definitions in Section 12.
- **Expected Result**: Events PEVT-LOADED, PEVT-INITIALIZED, PEVT-ACTIVATED, PEVT-UPDATED, PEVT-ROLLBACK include duration_ms.

#### AC-0203-057
- **Requirement**: Lifecycle events MUST include a correlationId for transition tracing.
- **Verification**: Inspect the event payload structure against RFC-1001.
- **Expected Result**: correlationId is present in all event payloads.

#### AC-0203-058
- **Requirement**: The health event system MUST track plugin resource consumption.
- **Verification**: Inspect PEVT_HEALTH-DEGRADED and PEVT_HEALTH-OK payloads.
- **Expected Result**: Both events include metrics-relevant payload fields.

#### AC-0203-059
- **Requirement**: Lifecycle events MUST be publishable to the common Event Bus.
- **Verification**: Inspect Section 12 for Event Bus integration references.
- **Expected Result**: All events reference the Event Bus as the publication target.

#### AC-0203-060
- **Requirement**: The Event Bus MUST deliver lifecycle events in transition order.
- **Verification**: Publish multiple events during rapid state transitions.
- **Expected Result**: Events are delivered in the order of transition completion.

### Diagrams

#### AC-0203-061
- **Requirement**: The state machine diagram MUST be rendered as a Mermaid stateDiagram-v2.
- **Verification**: Inspect Section 8 for the Mermaid diagram.
- **Expected Result**: A valid stateDiagram-v2 is present with all twenty states.

#### AC-0203-062
- **Requirement**: The recovery procedure MUST be illustrated with a Mermaid flowchart.
- **Verification**: Inspect Section 13 for the flowchart.
- **Expected Result**: A flowchart diagram showing timeout, retry, error, and recovery paths exists.

#### AC-0203-063
- **Requirement**: All state definitions MUST include the PSTATE- stable ID.
- **Verification**: Check each state subsection in Section 9 for the stable ID.
- **Expected Result**: All twenty states include their PSTATE- prefixed ID.

#### AC-0203-064
- **Requirement**: The transition table MUST be sortable by trigger operation.
- **Verification**: Inspect the transition table structure in Section 10.
- **Expected Result**: The table includes trigger, precondition, postcondition, and timeout columns.

#### AC-0203-065
- **Requirement**: The hooks table MUST specify the timeout for every hook.
- **Verification**: Inspect the hooks table in Section 11.
- **Expected Result**: All nineteen hooks have timeout values.

---




## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 19 References

1. **RFC-0002**: Runtime Lifecycle
2. **RFC-0008**: Runtime Plugin Host
3. **RFC-0201**: Plugin Overview
4. **RFC-0204**: Plugin Loader
5. **RFC-0210**: Plugin Events
6. **RFC-1001**: Common Event Model
7. **RFC-1002**: Common State Model
8. **RFC-1006**: Common Error Model
9. **ADR-0005**: Plugin Architecture
10. **glossary.md**: Unified Atlas Glossary

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 21 Future Evolution

- **Checkpoint Restore**: Future versions MAY define state checkpointing allowing plugins to save and restore execution state across platform restarts.
- **Predictive Recovery**: Future versions MAY define machine-learning-based failure prediction triggering proactive recovery before timeout.
- **Lifecycle Analytics**: Future versions MAY define standardized analytics collection for lifecycle transition durations and failure rates.
- **Batch Lifecycle**: Future versions MAY define batch operations for applying lifecycle transitions to multiple plugins simultaneously.

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

All plugin contracts are defined as abstract behavioral interfaces.

---




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
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |