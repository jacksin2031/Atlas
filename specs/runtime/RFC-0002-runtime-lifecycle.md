# RFC-0002: Runtime Lifecycle

RFC: RFC-0002  
Title: Runtime Lifecycle  
Status: Frozen  
Version: 1.0.0  
Author: Atlas Team  
Reviewers: Atlas Specification Committee  
Created: 2026-06-27  
Last Updated: 2026-06-30  
Depends On:  
  - RFC-0001 Runtime Overview  
Supersedes: None  
Superseded By: None  
Category: Runtime  
Layer: Core Runtime  
Normative: YES
Audience: Systems Engineers  
ADR References:  
  - ADR-0001  
  - ADR-0002  
  - ADR-0010  
  - ADR-0012  
Constitution References:  
  - Section 3.1 (Architecture Freeze)  
  - Section 4.2 (Fault Isolation)  
Related RFCs:  
  - RFC-0001 Runtime Overview  
  - RFC-0003 Runtime Service Model  
  - RFC-0004 Runtime Scheduler  
  - RFC-0005 Runtime Event Bus  
Target Release: 1.0.0  
Review Cycle: Core Architecture Board  
Compatibility: Compatible with Spec 1.x  
Last Updated: 2026-06-30  

---

## Normative Status
This specification is normative.

---

## Authority

This RFC is the authoritative specification for the Runtime Lifecycle.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

This specification is Normative. Every Atlas Runtime implementation MUST conform to the execution lifecycle, state machine, transition rules, APIs, and recovery models defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and all active ADRs.
---

## Terminology
The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Created | Initial state before any boot sequence begins. | Glossary |
| Initializing | Core services are being registered and validated. | This RFC |
| Ready | All core services are registered and the Runtime accepts external commands. | This RFC |
| Running | The Runtime is actively executing workflow tasks. | This RFC |
| Paused | Execution is suspended but state is preserved. | This RFC |
| ShuttingDown | Graceful shutdown sequence is in progress. | This RFC |
| Failed | An unrecoverable error has occurred. | This RFC |
| Terminated | The Runtime has ceased all operations. | This RFC |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | Glossary |
| Watchdog | The monitoring service checking heartbeats of registered services. | Glossary |
| Hook | A callback registered at an extension point, invoked at a defined moment in the lifecycle. | Glossary |

---

## 8 Runtime State Machine

The Runtime Lifecycle is modeled as a deterministic finite-state machine (FSM). The FSM has eight states and a defined set of transitions between them. The state machine is the single source of truth for Runtime lifecycle behavior.

`mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Initializing : boot()
    Initializing --> Ready : services_registered
    Initializing --> Failed : init_failure
    Ready --> Running : activate()
    Ready --> ShuttingDown : shutdown()
    Ready --> Failed : runtime_error
    Running --> Paused : pause()
    Running --> ShuttingDown : shutdown()
    Running --> Failed : unrecoverable_error
    Paused --> Running : resume()
    Paused --> ShuttingDown : shutdown()
    Paused --> Failed : unrecoverable_error
    ShuttingDown --> Terminated : teardown_complete
    Failed --> Terminated : abort()
    Terminated --> [*]
`

The state machine enforces the following rules:
- The Runtime begins in the Created state upon process initialization.
- The Runtime MUST traverse through Initializing and Ready before reaching Running.
- The Failed state is terminal except for the transition to Terminated.
- The Terminated state is the final state; no transitions originate from it.

---

## 9 State Definitions

### 9.1 Created
The Runtime process has been allocated but no initialization has begun. No services are registered, no hooks are invoked, and no resources are acquired. This is the pre-boot state.

**Entry conditions**: Process creation, memory allocation complete.
**Exit conditions**: Invocation of oot().
**Invariants**: No subsystems are active. No event subscriptions exist.

### 9.2 Initializing
The Runtime is loading subsystems in topological order. The Service Registry (refer to RFC-0003) resolves dependencies and instantiates service adapters. The State Manager (refer to RFC-0006) initializes its transaction log. The Event Bus (refer to RFC-0005) opens its routing tables.

**Entry conditions**: oot() called from Created.
**Exit conditions**: All services registered and healthy, transition to Ready. Or initialization failure, transition to Failed.
**Invariants**: Services are loaded sequentially. A service MUST NOT become active until all its declared dependencies are in the Active state.

### 9.3 Ready
All core services are registered, validated, and healthy. The Runtime is prepared to accept workflow submissions but has not yet activated task execution. The Service Dependency Graph (refer to ADR-0010) has been validated.

**Entry conditions**: All services pass health checks during Initializing.
**Exit conditions**: ctivate() transitions to Running. shutdown() transitions to ShuttingDown. An unrecoverable error transitions to Failed.
**Invariants**: No task dispatching occurs. Event subscriptions are open but no events are routed to active handlers.

### 9.4 Running
The Runtime is actively executing workflows, processing events, and managing resources. The Scheduler (refer to RFC-0004) dispatches tasks. The Plugin Host (refer to RFC-0008) manages sandboxed plugin instances.

**Entry conditions**: ctivate() called from Ready.
**Exit conditions**: pause() transitions to Paused. shutdown() transitions to ShuttingDown. An unrecoverable error transitions to Failed.
**Invariants**: All services MUST remain healthy. Watchdog heartbeats MUST not timeout. Resource quotas (refer to RFC-0009) MUST not be exceeded.

### 9.5 Paused
The Runtime has suspended task execution but maintained all service registrations, state stores, and event subscriptions. The Scheduler (refer to RFC-0004) halts dispatch but retains pending tasks in queues.

**Entry conditions**: pause() called from Running.
**Exit conditions**: 
esume() transitions to Running. shutdown() transitions to ShuttingDown.
**Invariants**: No new tasks are dispatched. Existing in-flight tasks complete but do not spawn successors. State transactions remain open.

### 9.6 ShuttingDown
The Runtime is performing ordered teardown of all subsystems. Services are deactivated in reverse topological order. Event subscriptions are closed. Resource allocations are released.

**Entry conditions**: shutdown() called from Running, Paused, or Ready.
**Exit conditions**: All teardown steps complete, transition to Terminated.
**Invariants**: No new events are accepted. Pending events are drained to the Dead Letter Queue (refer to RFC-0005). State snapshots are committed.

### 9.7 Failed
The Runtime encountered an unrecoverable error. The State Manager (refer to RFC-0006) has rolled back to the last consistent checkpoint. The Error Taxonomy (refer to RFC-0011) classifies the error.

**Entry conditions**: Any state receives an error classified as fatal by RFC-0011.
**Exit conditions**: bort() transitions to Terminated.
**Invariants**: No services are active. No tasks are executing. Event publishing is halted.

### 9.8 Terminated
The Runtime process has exited. All resources are released. No state persists beyond this point unless explicitly snapshotted.

**Entry conditions**: 	eardown_complete from ShuttingDown or bort() from Failed.
**Exit conditions**: None. This is the final state.
**Invariants**: Process memory is freed. File handles are closed. Network sockets are released.

---

## 10 Legal State Transitions

The following table enumerates all permitted state transitions. Each transition is identified by a command or event that triggers it.

| From State | To State | Trigger | Condition |
|---|---|---|---|
| Created | Initializing | oot() | Process is healthy |
| Initializing | Ready | services_registered | All services pass health checks |
| Initializing | Failed | init_failure | One or more core services fail to register |
| Ready | Running | ctivate() | No pending rollback state |
| Ready | ShuttingDown | shutdown() | Any |
| Ready | Failed | 
untime_error | Service health check fails after ready |
| Running | Paused | pause() | All in-flight tasks acknowledged |
| Running | ShuttingDown | shutdown() | Any |
| Running | Failed | unrecoverable_error | Error classified as fatal per RFC-0011 |
| Paused | Running | 
esume() | No state corruption detected |
| Paused | ShuttingDown | shutdown() | Any |
| Paused | Failed | unrecoverable_error | Error classified as fatal per RFC-0011 |
| ShuttingDown | Terminated | 	eardown_complete | All services deactivated |
| Failed | Terminated | bort() | Any |

---

## 11 Illegal Transitions

The following transitions are prohibited and MUST result in a StateTransitionError:

| From State | Attempted Transition | Reason |
|---|---|---|
| Created | 
esume() | Cannot resume before initializing |
| Created | pause() | Cannot pause before running |
| Created | shutdown() | Must pass through Initializing first |
| Initializing | ctivate() | Services not yet ready |
| Initializing | pause() | Not yet in running state |
| Ready | oot() | Already initialized |
| Ready | 
esume() | Not in paused state |
| Running | oot() | Already initialized |
| Running | ctivate() | Already active |
| Paused | oot() | Already initialized |
| Paused | ctivate() | Must transition through Running first |
| ShuttingDown | shutdown() | Already shutting down |
| ShuttingDown | 
esume() | Cannot resume during teardown |
| ShuttingDown | pause() | Already ceasing operation |
| Failed | 
esume() | Failed state requires explicit abort |
| Failed | pause() | Cannot pause a failed runtime |
| Failed | ctivate() | Failed state is terminal except abort |
| Terminated | *any* | Terminated is the final state |

---

## 12 Boot Lifecycle

The boot lifecycle encompasses all operations from process creation through the Ready state. It consists of four sequential phases:

1. **Environment Validation**: The Runtime verifies that required system capabilities exist (refer to RFC-0012). Missing mandatory capabilities cause immediate transition to Failed.
2. **Service Discovery**: The Runtime scans registered service adapters and constructs the dependency graph. Circular dependencies cause immediate transition to Failed.
3. **Service Initialization**: Services are instantiated in topological order. Each service's initialize() method is invoked. A single failure halts the remaining initialization and transitions to Failed.
4. **Health Verification**: The Runtime polls all initialized services. Services that fail health checks cause the Runtime to transition to Failed. Services that pass are marked Registered and the Runtime transitions to Ready.

`mermaid
flowchart TD
    A[Process Created] --> B[Environment Validation]
    B --> C{Capabilities OK?}
    C -->|No| D[Transition to Failed]
    C -->|Yes| E[Service Discovery]
    E --> F{Dependency Graph Valid?}
    F -->|No| D
    F -->|Yes| G[Service Initialization]
    G --> H{All Services Healthy?}
    H -->|No| D
    H -->|Yes| I[Health Verification]
    I --> J[Transition to Ready]
`

---

## 13 Startup Sequence

The startup sequence governs the ordered activation of services from the Ready state to the Running state.

1. **Phase 1 -- Event Bus Activation**: The Event Bus (refer to RFC-0005) opens all channel subscriptions. The Runtime publishes a LifecycleEvent.Starting event.
2. **Phase 2 -- State Manager Warm-Up**: The State Manager (refer to RFC-0006) loads the last committed snapshot and replays the Write-Ahead Log (WAL) to restore consistent state.
3. **Phase 3 -- Scheduler Activation**: The Scheduler (refer to RFC-0004) initializes worker pools and begins accepting task submissions from the queue.
4. **Phase 4 -- Plugin Host Readiness**: The Plugin Host (refer to RFC-0008) loads plugins declared in the Runtime Manifest (refer to RFC-0010).
5. **Phase 5 -- Resource Manager Calibration**: The Resource Manager (refer to RFC-0009) establishes baseline monitoring thresholds and activates the watchdog.
6. **Phase 6 -- Transition to Running**: The Runtime emits LifecycleEvent.Running and begins accepting external workflow submissions.

`mermaid
sequenceDiagram
    autonumber
    participant Cmd as Lifecycle Command
    participant SM as State Machine
    participant EB as Event Bus
    participant Reg as Service Registry

    Cmd->>SM: activate()
    SM->>EB: publish(LifecycleEvent.Starting)
    SM->>Reg: notifyAll(initialize)
    Reg-->>SM: all_services_ready
    SM->>SM: transition(Running)
    SM->>EB: publish(LifecycleEvent.Running)
    SM-->>Cmd: ActivationComplete
`

---

## 14 Shutdown Sequence

The shutdown sequence governs the ordered deactivation of all subsystems from any active state to Terminated.

1. **Phase 1 -- Drain Events**: The Event Bus (refer to RFC-0005) stops accepting new events. Pending events are flushed to the Dead Letter Queue if undeliverable.
2. **Phase 2 -- Suspend Scheduler**: The Scheduler (refer to RFC-0004) stops dispatching new tasks. In-flight tasks are signaled to complete. Tasks exceeding the grace period are forcibly terminated.
3. **Phase 3 -- Deactivate Plugins**: The Plugin Host (refer to RFC-0008) invokes unload() on all plugins in reverse initialization order. Each plugin must release all acquired resources within the timeout budget.
4. **Phase 4 -- Commit State**: The State Manager (refer to RFC-0006) commits a final snapshot and closes the WAL.
5. **Phase 5 -- Release Resources**: The Resource Manager (refer to RFC-0009) releases all memory pools, file handles, and network connections.
6. **Phase 6 -- Transition to Terminated**: The Runtime emits LifecycleEvent.Terminated and the process exits.

`mermaid
flowchart TD
    A[Shutdown Triggered] --> B[Drain Event Bus]
    B --> C[Suspend Scheduler]
    C --> D[Deactivate Plugins]
    D --> E[Commit Final State]
    E --> F[Release Resources]
    F --> G[Transition to Terminated]
`

---

## 15 Pause / Resume

### 15.1 Pause

The pause() command transitions the Runtime from Running to Paused. The following actions occur atomically:

1. The Scheduler (refer to RFC-0004) halts task dispatch.
2. All event subscriptions remain open but no events are routed to handlers.
3. The State Manager (refer to RFC-0006) takes a consistent snapshot.
4. Plugin sandboxes (refer to RFC-0008) receive a PauseNotification and flush their current operations.

A pause operation MUST complete within the timeout budget defined in Section 22. If the pause cannot complete within the budget, the Runtime transitions to Failed.

### 15.2 Resume

The 
esume() command transitions the Runtime from Paused to Running. The following actions occur:

1. The State Manager (refer to RFC-0006) verifies the snapshot integrity.
2. The Scheduler (refer to RFC-0004) re-enables task dispatch and replays pending queue items.
3. The Event Bus (refer to RFC-0005) reopens all channel subscriptions.
4. A LifecycleEvent.Resumed event is published.

If the snapshot is corrupted, the Runtime rejects the resume and transitions to Failed.

---

## 16 Restart

The Runtime supports two restart modes:

### 16.1 Soft Restart
A soft restart transitions through ShuttingDown and then Created, re-executing the boot lifecycle (Section 12) without terminating the host process. Memory pools are reclaimed and re-allocated. State is restored from the last committed snapshot.

Soft restart is used for:
- Configuration updates declared in the Runtime Manifest (refer to RFC-0010).
- Plugin hot-reload following version changes.
- Capability registry updates detected at runtime.

### 16.2 Hard Restart
A hard restart terminates the host process and relies on the operating system or supervisor to recreate it. The restarted process begins in the Created state. State is restored from the last committed snapshot on disk.

Hard restart is used for:
- Kernel-level resource exhaustion.
- Corruption of the in-memory state that cannot be recovered via soft restart.
- Major version upgrades requiring process recreation.

---

## 17 Recovery

The Runtime Recovery Model defines how transient failures are handled without full teardown.

### 17.1 Service-Level Recovery
When a single service fails (detected via heartbeat timeout or explicit error report per RFC-0011), the Runtime attempts service-level recovery:

1. The Service Registry (refer to RFC-0003) marks the service as Degraded.
2. The Runtime attempts to instantiate a replacement service adapter.
3. If the replacement initializes successfully, the service transitions to Active.
4. If the replacement fails, the Runtime escalates to the failure handling path (Section 18).

### 17.2 State-Level Recovery
When the State Manager (refer to RFC-0006) detects WAL corruption:

1. The Runtime reverts to the last known-good snapshot.
2. The WAL is truncated at the snapshot boundary.
3. A RecoveryEvent.StateRestored event is published.
4. If no valid snapshot exists, the Runtime transitions to Failed.

### 17.3 Plugin-Level Recovery
When a plugin sandbox crashes (per RFC-0008):

1. The Plugin Host terminates the crashed sandbox.
2. The Runtime clears the plugin's state from the State Manager.
3. The plugin is unloaded and reloaded from its manifest declaration.
4. If reload fails three times within a rolling window, the plugin is marked PermanentlyDisabled.

---

## 18 Failure Handling

Failure handling is governed by the Runtime Error Taxonomy (refer to RFC-0011). Errors are classified as either recoverable or fatal.

### 18.1 Recoverable Errors
Recoverable errors trigger localized recovery without affecting the overall Runtime state:

- **Timeout errors**: The Scheduler (refer to RFC-0004) retries the task with exponential backoff.
- **Transient IPC failures**: The IPC Dispatcher (refer to RFC-0007) re-establishes the connection.
- **Plugin sandbox crashes**: The Plugin Host (refer to RFC-0008) performs service-level recovery (Section 17.1).

### 18.2 Fatal Errors
Fatal errors trigger immediate transition to the Failed state:

- **Configuration errors**: Invalid manifest schemas (refer to RFC-0010) prevent service initialization.
- **Dependency failures**: Missing core services at boot halt the startup sequence.
- **Storage write lockouts**: The State Manager (refer to RFC-0006) cannot commit transactions.
- **Memory exhaustion**: The Resource Manager (refer to RFC-0009) cannot allocate required pages.

### 18.3 Post-Failure Actions
Upon transition to Failed:

1. A LifecycleEvent.Failed event is published with the error classification.
2. The State Manager commits a rollback checkpoint.
3. Diagnostic data is collected for the crash report.
4. The Runtime awaits an bort() command to reach Terminated.

---

## 19 Lifecycle Events

All lifecycle transitions are communicated through the Event Bus (refer to RFC-0005) using the following event schema. Events are immutable once published.

### 19.1 Event Catalog

| Event Name | Source State | Destination State | Priority | Payload Fields |
|---|---|---|---|---|
| LifecycleEvent.BootStarted | Created | Initializing | 1 (Critical) | phase, 	imestamp |
| LifecycleEvent.ServiceRegistered | Initializing | Initializing | 2 (Normal) | service_id, ersion |
| LifecycleEvent.HealthCheckPassed | Initializing | Initializing | 2 (Normal) | service_id, latency_ms |
| LifecycleEvent.Ready | Initializing | Ready | 1 (Critical) | uptime_ms, service_count |
| LifecycleEvent.Starting | Ready | Ready | 1 (Critical) | _none_ |
| LifecycleEvent.Running | Ready | Running | 1 (Critical) | ctive_plugins, queued_tasks |
| LifecycleEvent.PauseRequested | Running | Paused | 1 (Critical) | 
eason |
| LifecycleEvent.Paused | Running | Paused | 2 (Normal) | snapshot_version |
| LifecycleEvent.ResumeRequested | Paused | Paused | 1 (Critical) | _none_ |
| LifecycleEvent.Resumed | Paused | Running | 1 (Critical) | 
ecovered_from_snapshot |
| LifecycleEvent.ShutdownRequested | Any Active | ShuttingDown | 1 (Critical) | 
eason, grace_period_ms |
| LifecycleEvent.Draining | ShuttingDown | ShuttingDown | 2 (Normal) | pending_events |
| LifecycleEvent.Terminating | ShuttingDown | ShuttingDown | 2 (Normal) | phase |
| LifecycleEvent.Terminated | ShuttingDown | Terminated | 1 (Critical) | 	otal_uptime_ms |
| LifecycleEvent.Failed | Any | Failed | 1 (Critical) | error_code, error_class, 	race_id |
| LifecycleEvent.RestartRequested | Running | ShuttingDown | 1 (Critical) | 
estart_type |

### 19.2 Event Ordering
Lifecycle events MUST be published in strict chronological order. No two lifecycle events with different timestamps MAY be reordered by the Event Bus. Events sharing the same timestamp are ordered by priority (lower number equals higher priority).

---

## 20 Hooks

Hooks are user-defined or system-defined callbacks invoked at specific lifecycle junctures. The Runtime supports three hook categories:

### 20.1 Pre-Boot Hooks
Invoked before the boot sequence begins (entering Initializing). These hooks MAY modify runtime configuration but MUST NOT block for more than the timeout budget (Section 22).

**Use cases**: Environment variable injection, capability probe registration, configuration migration.

### 20.2 Post-Ready Hooks
Invoked immediately upon transition to Ready (after all services are registered but before ctivate()). These hooks MAY perform one-time setup but MUST NOT block indefinitely.

**Use cases**: Plugin manifest pre-validation, capability readiness verification, telemetry initialization.

### 20.3 Pre-Termination Hooks
Invoked before the shutdown sequence begins. These hooks MUST complete within the timeout budget. Hooks that exceed the budget are forcibly aborted.

**Use cases**: Final state snapshot, telemetry flush, graceful client notification.

### 20.4 Hook Registration

Hooks are registered with the Service Registry (refer to RFC-0003) during the Initializing phase. Each hook declaration includes:

- hook_point: The lifecycle phase at which the hook is invoked.
- execution_order: Integer determining invocation order among hooks at the same point.
- 	imeout_ms: Maximum allowed execution time.
- ailure_policy: Whether hook failure aborts the lifecycle transition (Fatal) or logs and continues (Warning).

`mermaid
graph TD
    HB[Hook Registry] --> PH1[Pre-Boot Hooks]
    HB --> PH2[Post-Ready Hooks]
    HB --> PH3[Pre-Termination Hooks]
    PH1 --> HO[Hook Orchestrator]
    PH2 --> HO
    PH3 --> HO
    HO --> HC[Hook Caller]
    HC --> HV[Validation Gate]
    HV --> HE[Execution]
    HE --> HF{Success?}
    HF -->|Yes| HR[Continue Lifecycle]
    HF -->|No| HP[Failure Policy]
    HP -->|Fatal| HFA[Abort Transition]
    HP -->|Warning| HWC[Log and Continue]
`

---

## 21 Health Monitoring

The Runtime employs a multi-layered health monitoring system to detect degradation before it causes failures.

### 21.1 Heartbeat Mechanism
Every registered service (refer to RFC-0003) MUST emit a heartbeat at intervals not exceeding the configured heartbeat_interval_ms. The Runtime monitors these heartbeats and flags services as Unhealthy when heartbeats are missed.

### 21.2 Watchdog Timer
A watchdog timer runs on a dedicated thread independent of the Runtime state machine. The watchdog:

1. Polls all service heartbeats at twice the heartbeat frequency.
2. Detects missed heartbeats and initiates recovery (Section 17).
3. Escalates to Failed state if recovery fails after the maximum retry count.

### 21.3 Liveness Probes
Services MAY expose liveness probe endpoints. The Runtime calls these probes during the Initializing phase to verify that services are not only responding to heartbeats but are functionally operational.

### 21.4 Readiness Probes
After transition to Ready, the Runtime executes readiness probes to verify that services can accept external traffic. Services that fail readiness probes prevent the Running transition.

---

## 22 Timeout Rules

All lifecycle operations are subject to strict timeout budgets to prevent indefinite hangs.

| Operation | Timeout Budget | Escalation |
|---|---|---|
| Pre-Boot Hook Execution | 5,000 ms per hook | Abort hook, log warning |
| Service Initialization | 30,000 ms per service | Fail boot, transition to Failed |
| Health Check (all services) | 10,000 ms total | Fail boot, transition to Failed |
| Pause Transition | 15,000 ms | Fail transition, transition to Failed |
| Resume Transition | 10,000 ms | Fail transition, transition to Failed |
| Plugin Unload | 5,000 ms per plugin | Force terminate, log error |
| State Snapshot Commit | 30,000 ms | Retry once, then fail |
| Full Shutdown Sequence | 60,000 ms total | Force abort process |
| Watchdog Heartbeat Miss | 2x heartbeat interval | Initiate recovery |
| Service Recovery Retry | 3 attempts per 60s window | Mark permanently disabled |

Timeouts are measured from the moment the operation is initiated. If the operation does not complete within the budget, the Runtime escalates according to the escalation column.

---

## 23 Concurrency Rules

### 23.1 Sequential Transitions
State transitions are inherently sequential. Only one transition command MAY be processed at any given time. Concurrent transition commands are queued and processed in order of arrival.

### 23.2 Hook Concurrency
Hooks at the same lifecycle point execute sequentially in registration order. Hooks at different lifecycle points MAY execute concurrently with state transitions they do not interfere with.

### 23.3 Watchdog Independence
The watchdog thread operates independently of the state machine. Watchdog actions (recovery, escalation) do not constitute lifecycle transitions and do not compete with transition commands.

### 23.4 Event Publishing During Transitions
Events MAY be published during any state transition. The Event Bus (refer to RFC-0005) buffers events if the bus is temporarily unavailable during the transition window.

---

## 24 Constraints

### 24.1 Single Supervisor Constraint
Only one Runtime supervisor process MAY exist per workspace. Attempts to start a second supervisor in the same workspace MUST be rejected with a WorkspaceLockedError.

### 24.2 Topological Ordering Constraint
Services MUST be initialized and shut down in strict topological order of the dependency graph. Violations of this order are prohibited and cause immediate Failed state transition.

### 24.3 Atomicity Constraint
All operations within a single lifecycle transition are atomic. Either all operations complete successfully, or the Runtime rolls back to the previous state. Partial transitions are not permitted.

### 24.4 Idempotency Constraint
Repeated invocation of the same lifecycle command (e.g., shutdown() called twice) MUST be idempotent. The second invocation MUST return success without side effects if the target state is already reached.

### 24.5 No Backward Transition Constraint
The Runtime MUST NOT transition backward in the lifecycle order. Once a state is left, it cannot be re-entered except through the full boot sequence.

---

## 25 Metrics

The Runtime exposes the following lifecycle metrics for observability:

| Metric Name | Type | Description | Labels |
|---|---|---|---|
| lifecycle_state_current | Gauge | Current state of the Runtime (encoded as integer) | state |
| lifecycle_transitions_total | Counter | Total number of state transitions since process start | rom_state, 	o_state |
| lifecycle_transition_duration_ms | Histogram | Duration of each state transition | rom_state, 	o_state |
| lifecycle_heartbeats_missed_total | Counter | Total missed heartbeats per service | service_id |
| lifecycle_recovery_attempts_total | Counter | Total recovery attempts per service | service_id, 
esult |
| lifecycle_uptime_seconds | Gauge | Seconds since last transition to Running | _none_ |
| lifecycle_shutdown_grace_remaining_ms | Gauge | Milliseconds remaining in shutdown grace period | _none_ |

Metrics are published to the Event Bus (refer to RFC-0005) on every lifecycle event and at configurable intervals for gauge metrics.

---

## 26 Security

### 26.1 Lifecycle Command Authentication
All lifecycle commands (boot, shutdown, pause, resume, restart) MUST be authenticated. The Runtime verifies the caller's security token against the registered service identities before executing any transition.

### 26.2 Transition Audit Logging
Every lifecycle transition is logged with:
- Timestamp (monotonic clock)
- Source state
- Destination state
- Triggering command
- Authenticating caller identity
- Trace ID (per RFC-0005)

Audit logs are immutable and persisted to the State Manager (refer to RFC-0006) transaction log.

### 26.3 Restricted Commands
The following commands are restricted to privileged callers:
- bort(): Requires dmin role.
- shutdown(): Requires dmin or operator role.
- 
estart(): Requires dmin role.

---

## 27 Execution Context

The Runtime Lifecycle operates within a well-defined execution context that governs resource allocation and isolation.

### 27.1 Process Boundary
The Runtime supervisor runs as a single process. All core services (Logger, Storage, Event Bus, Scheduler, State Manager) run within this process boundary. Plugins run in separate sandboxed processes or WASM VMs (refer to RFC-0008).

### 27.2 Thread Model
The Runtime uses the following thread model:
- **Main thread**: Executes the state machine and processes lifecycle commands.
- **Watchdog thread**: Monitors service health and initiates recovery.
- **Event dispatch thread**: Routes events from the Event Bus to subscribers.
- **Metrics thread**: Collects and publishes lifecycle metrics.

The watchdog, event dispatch, and metrics threads operate independently of the main thread's state machine but MUST respect the concurrency rules in Section 23.

### 27.3 Memory Context
The Runtime maintains a dedicated memory region for lifecycle state. This region is isolated from plugin memory pools (refer to RFC-0009). Memory corruption in a plugin sandbox does not affect lifecycle state.

---

## 28 Service Dependency Graph

The Runtime Lifecycle depends on the Service Dependency Graph defined by the Service Registry (refer to RFC-0003). The dependency graph determines the topological order of service initialization and shutdown.

### 28.1 Dependency Resolution
During the Initializing phase, the Runtime resolves the dependency graph:

1. The Service Registry collects all service declarations.
2. The Runtime constructs a directed acyclic graph (DAG) from service dependency declarations.
3. A topological sort produces the initialization order.
4. If a cycle is detected, the Runtime transitions to Failed.

### 28.2 Dependency Graph Structure

`mermaid
graph LR
    Core[Core Runtime] --> SRV[Service Registry]
    SRV --> EB[Event Bus]
    SRV --> SM[State Manager]
    SRV --> SCH[Scheduler]
    SRV --> IPC[IPC Dispatcher]
    SRV --> RES[Resource Manager]
    SRV --> PLG[Plugin Host]
    EB --> SM
    EB --> SCH
    SCH --> PLG
    PLG --> RES
    PLG --> SM
`

### 28.3 Dependency Categories
- **Mandatory dependencies**: Services that MUST be available for the Runtime to function. Missing a mandatory dependency causes boot failure.
- **Optional dependencies**: Services that enhance Runtime capability but are not required for basic operation. Missing an optional dependency is logged as a warning.

---

## 29 Runtime Recovery Model

The Runtime Recovery Model defines the strategies and limits for recovering from transient failures during any lifecycle phase.

### 29.1 Recovery Strategies

| Failure Type | Strategy | Max Retries | Backoff |
|---|---|---|---|
| Service initialization failure | Restart service | 3 | Exponential (1s, 2s, 4s) |
| Heartbeat miss | Probe service | 2 | Immediate |
| State snapshot corruption | Revert to previous snapshot | 1 | N/A |
| Plugin sandbox crash | Terminate and reload | 3 per 60s window | Linear (2s intervals) |
| IPC connection loss | Re-establish connection | 5 | Exponential (500ms, 1s, 2s, 4s, 8s) |
| Resource quota exhaustion | Throttle and retry | 10 | Exponential (100ms base) |

### 29.2 Recovery Limits
When recovery attempts exceed the maximum retry count, the Runtime transitions to the Failed state. The error classification follows RFC-0011.

### 29.3 Post-Recovery Verification
After a successful recovery, the Runtime performs a verification pass:

1. All affected services emit a fresh heartbeat.
2. The State Manager (refer to RFC-0006) verifies data consistency.
3. A RecoveryEvent.Verified event is published.
4. The Runtime returns to the state it was in before the failure.

---

## 30 Runtime Time Model

The Runtime Lifecycle operates under a unified time model that ensures deterministic behavior across all subsystems.

### 30.1 Time Sources
The Runtime uses two time sources:
- **Wall-clock time**: For human-readable timestamps and external communication.
- **Monotonic time**: For measuring durations, timeouts, and heartbeat intervals. Monotonic time is guaranteed to never decrease and is immune to system clock adjustments.

### 30.2 Temporal Ordering
All lifecycle events are ordered by monotonic time. When two events share the same monotonic timestamp, they are ordered by:
1. Priority (lower number equals earlier).
2. Source service ID (lexicographic).
3. Event sequence number (monotonically increasing counter per source).

### 30.3 Timeout Measurement
All timeout budgets (Section 22) are measured using monotonic time. Timeouts are not affected by system clock changes.

---

## 31 Exposed Runtime APIs

The Runtime exposes the following abstract lifecycle APIs. Implementations MUST provide these interfaces; the concrete transport (IPC, local call, or shared memory) is implementation-dependent.

### 31.1 Lifecycle Commands

`
interface LifecycleController {
  BootResult boot(Configuration config);
  void activate();
  void pause(PauseOptions options);
  void resume();
  void shutdown(ShutdownOptions options);
  void abort();
  LifecycleState getState();
  void registerHook(HookDefinition hook);
  void unregisterHook(string hookId);
}
`

### 31.2 Lifecycle Queries

`
interface LifecycleQuery {
  StateTransitionLog getTransitionHistory();
  ServiceHealthReport getServiceHealthReport();
  DependencyGraph getDependencyGraph();
  HookList getPendingHooks(LifecyclePhase phase);
}
`

### 31.3 Lifecycle Events (Subscriptions)

`
interface LifecycleEventBus {
  Subscription subscribe(EventFilter filter, EventHandler handler);
  void unsubscribe(SubscriptionHandle handle);
}
`

---

## 32 Standard Event Contract

All lifecycle events conform to the standard event schema defined in RFC-0005 (Event Bus). The lifecycle-specific envelope adds the following fields:

`json
{
  "type": "lifecycle.event",
  "phase": "<lifecycle_phase>",
  "from_state": "<source_state>",
  "to_state": "<destination_state>",
  "trigger": "<command_or_event>",
  "timestamp_monotonic": "<int>",
  "timestamp_wall": "<int>",
  "trace_id": "<uuid>",
  "correlation_id": "<uuid>",
  "caller_id": "<service_id_or_null>",
  "metadata": {
    "retry_count": "<int_or_null>",
    "recovery_attempt": "<bool>",
    "snapshot_version": "<string_or_null>"
  }
}
`

---

## 33 Timeout Budget

The total timeout budget for the complete lifecycle from Created to Terminated is bounded as follows:

| Phase | Budget | Notes |
|---|---|---|
| Boot (Created to Ready) | 60,000 ms | Includes all service initialization |
| Activate (Ready to Running) | 5,000 ms | Event bus and scheduler activation |
| Pause (Running to Paused) | 15,000 ms | Drain in-flight operations |
| Resume (Paused to Running) | 10,000 ms | Verify snapshot, re-enable dispatch |
| Shutdown (Any to Terminated) | 60,000 ms | Full teardown including plugin unload |
| Recovery (per attempt) | 30,000 ms | Per-service recovery window |

Exceeding any individual phase budget triggers the escalation path defined in Section 18.

---

## 34 Recovery Budget

The Recovery Budget defines the aggregate resources allocated for recovery operations:

- **Maximum concurrent recoveries**: 1 (only one service may be recovered at a time to prevent cascading failures).
- **Maximum total recovery time**: 120,000 ms per recovery window (rolling 60-second window).
- **Maximum rollback depth**: 10 snapshots (the Runtime retains at most 10 prior snapshots for rollback).
- **Recovery event rate limit**: 100 lifecycle events per second during recovery mode (to prevent event storms).

---

## 35 State Invariants

The following invariants MUST hold at all times during the Runtime lifecycle:

- **INV-LC-03**: The Runtime state MUST always be consistent with the last published lifecycle event.
- **INV-LC-04**: The Service Dependency Graph MUST be acyclic at all times.
- **INV-LC-05**: All hooks registered for a lifecycle phase MUST complete before the transition to the next phase begins.
- **INV-LC-06**: The monotonic time counter MUST never decrease across the Runtime lifetime.
- **INV-LC-07**: The State Manager snapshot version MUST monotonically increase with each committed snapshot.
- **INV-LC-08**: The number of active services MUST equal the number of registered services minus the number of permanently disabled services.

---

## 36 Normative Contracts

The Runtime Lifecycle adheres to the following normative contracts:

### 36.1 Service Contract
Every service registered with the Runtime MUST implement the ServiceContract interface defined in RFC-0003, which includes initialize(), healthCheck(), and deinitialize() methods.

### 36.2 Event Contract
Every lifecycle event MUST conform to the standard event schema defined in RFC-0005 and MUST include the lifecycle-specific envelope fields defined in Section 32.

### 36.3 Error Contract
Every error generated during lifecycle operations MUST conform to the error taxonomy defined in RFC-0011 and MUST include trace and correlation identifiers.

### 36.4 Hook Contract
Every registered hook MUST conform to the hook definition schema in Section 20.4 and MUST complete within its declared timeout budget.

---

## 37 Compliance Checklist

Implementations MUST verify the following compliance points:

| # | Requirement | Verification Method |
|---|---|---|
| LC-01 | State machine has exactly 8 defined states | Static analysis of state enum |
| LC-02 | All legal transitions are enumerated and enforced | Unit test of transition matrix |
| LC-03 | All illegal transitions produce StateTransitionError | Negative test suite |
| LC-04 | Boot sequence respects topological order | Dependency graph validation test |
| LC-05 | Shutdown sequence reverses topological order | Teardown audit log review |
| LC-06 | All lifecycle transitions publish events | Event bus subscription test |
| LC-07 | Hooks execute in registration order | Hook execution trace test |
| LC-08 | Timeouts are enforced per Section 22 | Stress test with delayed services |
| LC-09 | Recovery respects max retry limits | Recovery exhaustion test |
| LC-10 | Audit logs are immutable | Append-only storage verification |
| LC-11 | Watchdog operates on independent thread | Concurrency isolation test |
| LC-12 | Idempotency of repeated commands | Duplicate command stress test |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for:
- Defining the Runtime state machine and all legal state transitions.
- Specifying boot, shutdown, pause, resume, restart, and recovery sequences.
- Defining hook registration and execution semantics.
- Defining health monitoring (heartbeat, watchdog, liveness probes).
- Defining timeout and concurrency rules for lifecycle transitions.

### Non-Responsibilities
This specification IS NOT responsible for:
- Service-level error handling (covered by RFC-0011).
- Plugin lifecycle (covered by RFC-0203).
- Workflow lifecycle (covered by RFC-0305).
- Storage lifecycle (covered by RFC-0404).

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0003 | Consumed | Service Model (service registration order) |
| RFC-0005 | Consumed | Event Bus (lifecycle events) |
| RFC-0009 | Consumed | Resource Management (resource cleanup on shutdown) |

### Consumers
- RFC-0003 Runtime Service Model (services register during Initializing→Ready transition)
- RFC-0008 Runtime Plugin Host (plugins load during Ready state)
- RFC-0203 Plugin Lifecycle (plugin lifecycle maps to Runtime lifecycle)
- RFC-0305 Workflow Lifecycle (workflow lifecycle maps to Runtime lifecycle)

### Providers
- RFC-0001 Runtime Overview (provides architecture context)
- RFC-0005 Runtime Event Bus (provides lifecycle event definitions)

### Forbidden Dependencies
- This specification MUST NOT define service-level error handling.
- This specification MUST NOT depend on any specific threading model.

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

All lifecycle contracts are defined as abstract state transitions.

---

## 38 Acceptance Criteria

### AC-011
- **Requirement**: The Runtime MUST transition to the Running state upon successful boot sequences.
- **Verification**: Launch boot coordinator sequence.
- **Expected Result**: Lifecycle log registers transition to Running state.

### AC-012
- **Requirement**: The lifecycle machine MUST reject illegal transitions and return a StateTransitionError.
- **Verification**: Request pause() command while in the Created state.
- **Expected Result**: Command is blocked and throws StateTransitionError.

### AC-013
- **Requirement**: Graceful shutdowns MUST complete within the timeout budget.
- **Verification**: Trigger a SIGTERM signal to active host process.
- **Expected Result**: Teardown completes within 60,000 ms.

### AC-014
- **Requirement**: The Runtime MUST enforce sequential state transitions.
- **Verification**: Send two concurrent shutdown() commands.
- **Expected Result**: Second command is idempotent; no double-teardown occurs.

### AC-015
- **Requirement**: Service initialization MUST follow topological order.
- **Verification**: Register services with known dependency chain A-B-C.
- **Expected Result**: Services initialize in order C, B, A (dependencies first).

### AC-016
- **Requirement**: Recovery attempts MUST not exceed configured retry limits.
- **Verification**: Inject a service that consistently fails health checks.
- **Expected Result**: After 3 retries, the service is marked PermanentlyDisabled and the Runtime transitions to Failed.

### AC-017
- **Requirement**: The Runtime MUST publish a lifecycle event for every state transition.
- **Verification**: Monitor the Event Bus during a full boot-to-run-to-shutdown cycle.
- **Expected Result**: Exactly 5 lifecycle events are observed: BootStarted, Ready, Running, ShutdownRequested, Terminated.

### AC-018
- **Requirement**: Monotonic time MUST never decrease during the Runtime lifetime.
- **Verification**: Record monotonic timestamps at each state transition.
- **Expected Result**: Each subsequent timestamp is greater than or equal to the previous.

---

## 39 References
1. **RFC-0001**: Runtime Overview
2. **RFC-0003**: Runtime Service Model
3. **RFC-0004**: Runtime Scheduler
4. **RFC-0005**: Runtime Event Bus
5. **RFC-0006**: Runtime State Management
6. **RFC-0007**: Runtime IPC Architecture
7. **RFC-0008**: Runtime Plugin Host
8. **RFC-0009**: Runtime Resource Management
9. **RFC-0010**: Runtime Manifest Specification
10. **RFC-0011**: Runtime Error Taxonomy
11. **ADR-0010**: IPC and Runtime Architecture
12. **ADR-0012**: Contract-First Specification
13. **glossary.md**: Unified glossary

---

## 40 Changelog
- 1.0.0: Initial release. Defined state machine, transitions, and lifecycle phases.
- 1.1.0: Expanded all placeholder sections. Added recovery model, time model, compliance checklist, and acceptance criteria.

---

## 41 Compatibility
- Compatible with Spec Version 1.x.




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
| 1.1.0 | Frozen | 2026-07-01 | Atlas Specification Committee | Added Authority, Terminology, Layer Boundaries, Runtime Independence sections per RFC_TEMPLATE.md |



