# RFC-0208: Plugin Sandbox

RFC: Rfc 0208 Plugin Sandbox
Title: Plugin Sandbox
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0008 Runtime Plugin Host
  - RFC-0201 Plugin Overview
  - RFC-0207 Plugin Security
  - RFC-1006 Common Error Model
Related RFC:
  - RFC-0203 Plugin Lifecycle
  - RFC-0204 Plugin Loader
  - RFC-0209 Plugin API
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
This specification is Normative. Every Atlas implementation MUST conform to the sandbox architecture, isolation boundaries, execution constraints, resource quotas, filesystem isolation, memory/CPU/GPU limits, IPC restrictions, runtime interaction controls, recovery procedures, and sandbox lifecycle requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents
1. [Introduction]
2. [Goals]
3. [Non-Goals]
4. [Sandbox Philosophy]
5. [Ownership]
6. [Boundaries]
7. [Runtime Invariants]
8. [Architecture]
9. [Sandbox Architecture]
10. [Execution Isolation]
11. [Resource Quotas]
12. [Filesystem Isolation]
13. [Memory Limits]
14. [CPU Limits]
15. [GPU Limits]
16. [IPC Restrictions]
17. [Runtime Interaction]
18. [Recovery]
19. [Sandbox Lifecycle]
20. [Performance Budgets]
21. [Glossary]
22. [Acceptance Criteria]
23. [Cross References]
24. [References]
25. [Revision History]
26. [Future Evolution]
---

## 2 Goals
1. **Complete Isolation**:  Every plugin executes in an isolated sandbox with no access to host resources outside its declared boundaries.
2. **Defense in Depth**:  Multiple independent security controls operate at every sandbox boundary.
3. **Resource Quotas**:  Plugins are constrained by declared resource limits for memory, CPU, GPU, and disk.
4. **Filesystem Boundaries**:  Plugins have access only to their sandbox namespace.
5. **IPC Restrictions**:  Plugin IPC is restricted to declared channels and targets.
6. **Crash Containment**:  Plugin crashes MUST NOT affect the host platform.
7. **Resource Recovery**:  Sandbox resources MUST be fully recovered on plugin removal.
8. **Monitoring**:  Sandbox health and resource consumption are continuously monitored.

---



## 4 Sandbox Philosophy
1. **Isolate by Default**: Every plugin starts in a sandbox with zero access to host resources.
2. **Declare to Access**: Plugins declare required resources in their manifest. Access is granted only for declared resources.
3. **Contain Failures**: Sandbox failures are contained within the sandbox boundary.
4. **Recover Resources**: All sandbox resources are recovered on sandbox destruction.
5. **Monitor Continuously**: Sandbox health and resource usage are continuously monitored.
6. **Enforce Strictly**: All sandbox boundaries are enforced at the platform level, not by plugin cooperation.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 6 Boundaries
- **Sandbox Manager MAY communicate with**:
  - Plugin Loader (RFC-0204) for sandbox creation requests
  - Plugin Security Manager (RFC-0207) for security policy enforcement
  - Plugin Lifecycle Manager (RFC-0203) for lifecycle events
  - Runtime Resource Manager (RFC-0009) for resource allocation
  - Event Bus (RFC-0210) for sandbox events
- **Sandbox Manager MUST NOT communicate with**:
  - Plugin extension logic directly
  - Host hardware interfaces directly

---



## 8 Architecture
`mermaid
graph TD
    subgraph Sandbox Manager
        ContainerMgr[Container Manager]
        QuotaEnforcer[Quota Enforcer]
        FSIsolator[Filesystem Isolation]
        MemGuard[Memory Guard]
        CPULimiter[CPU Limiter]
        GPUGuard[GPU Guard]
        IPCFilter[IPC Filter]
        HealthMonitor[Health Monitor]
        ResourceReaper[Resource Reaper]
    end
    subgraph Plugin Sandboxes
        SB1[Sandbox 1]
        SB2[Sandbox 2]
        SB3[Sandbox N]
    end
    ContainerMgr --> SB1
    ContainerMgr --> SB2
    ContainerMgr --> SB3
    QuotaEnforcer --> SB1
    FSIsolator --> SB1
    MemGuard --> SB1
    CPULimiter --> SB1
    GPUGuard --> SB1
    IPCFilter --> SB1
    HealthMonitor --> SB1
    HealthMonitor --> SB2
    HealthMonitor --> SB3
    ResourceReaper --> SB1
    ResourceReaper --> SB2
    ResourceReaper --> SB3
`

---



## 10 Execution Isolation
- **Process Separation**: Each plugin runs in its own process or VM.
- **Memory Separation**: Plugin memory is separated from host and other plugins.
- **Thread Isolation**: Plugin threads are isolated from host threads.
- **Signal Handling**: Plugin signals are contained within the sandbox.
- **Exception Containment**: Plugin exceptions do not propagate to the host.

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 12 Filesystem Isolation
- **Sandbox Namespace**: Each plugin has a dedicated file system namespace.
- **Read Access**: Plugins may read from declared resource directories.
- **Write Access**: Plugins may write only to declared output directories.
- **Temp Directory**: Plugins have access to a temporary directory within their namespace.
- **Cross-Plugin Access**: Plugins MUST NOT access other plugin file systems.
- **Host Access**: Plugins MUST NOT access the host file system.
- **Volume Mounts**: Volume mounts are declared in the manifest and mounted read-only unless explicitly allowed.

---



## 14 CPU Limits
- **CPU Percentage**: Plugin CPU usage MUST NOT exceed the declared percentage.
- **CPU Time Slice**: Each CPU time slice is bounded by the declared maximum.
- **CPU Throttling**: Exceeding CPU limits triggers throttling before suspension.
- **CPU Affinity**: Plugins MAY be pinned to specific CPU cores through manifest declaration.
- **CPU Reporting**: CPU usage is reported through PEVT-HEALTH-* events.

---

- RFC-0323 Workflow Plugin Integration


## 16 IPC Restrictions
- **Channel Access**: Plugins may only access IPC channels declared in their manifest.
- **Message Size**: IPC messages are limited to 1 MB per RFC-0007.
- **Rate Limiting**: IPC message rates are limited per plugin.
- **Direction Control**: IPC channels are unidirectional or bidirectional as declared.
- **Security Level**: IPC security levels (RFC-0107) are enforced.
- **Cross-Sandbox IPC**: Plugins MAY communicate with other plugins only through declared IPC channels.

---


## 18 Recovery
- **Auto-Recovery**: Transient failures trigger automatic sandbox restart.
- **Manual Recovery**: Persistent failures require administrative intervention.
- **Resource Cleanup**: Failed sandboxes are cleaned up by the Resource Reaper.
- **State Preservation**: Sandbox state is preserved across restarts where possible.
- **Quarantine**: Suspected malicious sandboxes are quarantined for investigation.

---

| RFC-0201 | Consumed | Plugin Overview |


## 20 Performance Budgets
| Metric | Target Budget | Measurement Context |
|---|---|---|
| Sandbox Creation | 5,000 ms | Creating isolated execution context |
| Resource Allocation | 1 ms | Allocating memory/CPU/GPU quotas |
| Quota Check | 0.01 ms | Checking resource limit |
| Health Poll | 100 ms | Monitoring interval |
| OOM Response | 10 ms | Out-of-memory detection to suspension |
| Sandbox Destruction | 2,000 ms | Full cleanup and resource release |

---



## 22 Acceptance Criteria

### Isolation
#### AC-0208-001
- **Requirement**: Every plugin MUST execute in an isolated sandbox.
- **Verification**: Load a plugin and inspect its execution context.
- **Expected Result**: Plugin runs in isolated sandbox.
#### AC-0208-002
- **Requirement**: Plugin memory MUST NOT be accessible from the host.
- **Verification**: Attempt host access to plugin memory.
- **Expected Result**: Access denied.
#### AC-0208-003
- **Requirement**: Plugin file system access MUST be restricted to sandbox namespace.
- **Verification**: Attempt host file access from plugin.
- **Expected Result**: Access denied.
#### AC-0208-004
- **Requirement**: Plugin crashes MUST NOT affect the host platform.
- **Verification**: Inject a crash into a plugin.
- **Expected Result**: Host remains operational.
#### AC-0208-005
- **Requirement**: Each plugin MUST run in a separate process or VM.
- **Verification**: Inspect processes after loading multiple plugins.
- **Expected Result**: Separate processes/VMs confirmed.
#### AC-0208-006
- **Requirement**: Plugin threads MUST be isolated from host threads.
- **Verification**: Check thread isolation.
- **Expected Result**: Threads are isolated.
#### AC-0208-007
- **Requirement**: Plugin signals MUST be contained within the sandbox.
- **Verification**: Send signal to plugin process.
- **Expected Result**: Signal is contained.
#### AC-0208-008
- **Requirement**: Plugin exceptions MUST NOT propagate to the host.
- **Verification**: Raise exception in plugin.
- **Expected Result**: Exception is contained.

### Resource Quotas
#### AC-0208-009
- **Requirement**: Plugin heap usage MUST NOT exceed declared limit.
- **Verification**: Allocate beyond heap limit.
- **Expected Result**: Allocation fails.
#### AC-0208-010
- **Requirement**: Plugin stack usage MUST NOT exceed declared limit.
- **Verification**: Cause stack overflow in plugin.
- **Expected Result**: Overflow is contained.
#### AC-0208-011
- **Requirement**: Total plugin memory MUST NOT exceed declared limit.
- **Verification**: Allocate beyond total limit.
- **Expected Result**: Allocation fails.
#### AC-0208-012
- **Requirement**: CPU usage MUST NOT exceed declared percentage.
- **Verification**: Run CPU-intensive plugin.
- **Expected Result**: Usage is throttled.
#### AC-0208-013
- **Requirement**: GPU memory usage MUST NOT exceed declared limit.
- **Verification**: Allocate beyond GPU memory limit.
- **Expected Result**: Allocation fails.
#### AC-0208-014
- **Requirement**: Disk write usage MUST NOT exceed declared limit.
- **Verification**: Write beyond disk limit.
- **Expected Result**: Write is rejected.
#### AC-0208-015
- **Requirement**: Network connections MUST be limited per plugin.
- **Verification**: Open more connections than allowed.
- **Expected Result**: Connections are blocked.
#### AC-0208-016
- **Requirement**: Syscall rate MUST be limited per plugin.
- **Verification**: Generate excessive syscalls.
- **Expected Result**: Rate is throttled.

### Filesystem
#### AC-0208-017
- **Requirement**: Plugins MUST have access only to sandbox namespace.
- **Verification**: Check file system access from plugin.
- **Expected Result**: Only sandbox files are accessible.
#### AC-0208-018
- **Requirement**: Plugins MUST NOT access host file system directly.
- **Verification**: Attempt host file read.
- **Expected Result**: Access denied.
#### AC-0208-019
- **Requirement**: Plugins MUST NOT access other plugin file systems.
- **Verification**: Attempt cross-plugin file read.
- **Expected Result**: Access denied.
#### AC-0208-020
- **Requirement**: Volume mounts MUST be declared in manifest.
- **Verification**: Mount volume without declaration.
- **Expected Result**: Mount is rejected.
#### AC-0208-021
- **Requirement**: Volume mounts MUST be read-only by default.
- **Verification**: Mount volume and check permissions.
- **Expected Result**: Volume is read-only.

### IPC
#### AC-0208-022
- **Requirement**: Plugins may only access declared IPC channels.
- **Verification**: Access undeclared IPC channel.
- **Expected Result**: Access denied.
#### AC-0208-023
- **Requirement**: IPC messages MUST be validated against schemas.
- **Verification**: Send malformed IPC message.
- **Expected Result**: Message is rejected.
#### AC-0208-024
- **Requirement**: IPC message rate MUST be limited per plugin.
- **Verification**: Send excessive IPC messages.
- **Expected Result**: Rate is throttled.
#### AC-0208-025
- **Requirement**: IPC security levels (RFC-0107) MUST be enforced.
- **Verification**: Attempt cross-level IPC.
- **Expected Result**: Connection rejected.
#### AC-0208-026
- **Requirement**: Cross-sandbox IPC MUST use declared channels only.
- **Verification**: Attempt undeclared cross-sandbox IPC.
- **Expected Result**: Access denied.

### Memory
#### AC-0208-027
- **Requirement**: OOM events MUST trigger sandbox suspension.
- **Verification**: Exceed memory limit.
- **Expected Result**: Sandbox is suspended.
#### AC-0208-028
- **Requirement**: Memory leak detection MUST be performed by Health Monitor.
- **Verification**: Run plugin with memory leak.
- **Expected Result**: Leak is detected.
#### AC-0208-029
- **Requirement**: Memory usage MUST be reported through PEVT-HEALTH-* events.
- **Verification**: Check event log for memory events.
- **Expected Result**: Events are produced.

### Recovery
#### AC-0208-030
- **Requirement**: Transient failures MUST trigger automatic sandbox restart.
- **Verification**: Simulate transient failure.
- **Expected Result**: Sandbox restarts automatically.
#### AC-0208-031
- **Requirement**: Persistent failures MUST require administrative intervention.
- **Verification**: Simulate persistent failure.
- **Expected Result**: Administrative intervention required.
#### AC-0208-032
- **Requirement**: Failed sandbox resources MUST be cleaned up by Resource Reaper.
- **Verification**: Destroy sandbox and check resources.
- **Expected Result**: Resources are recovered.
#### AC-0208-033
- **Requirement**: Sandbox state MUST be preserved across restarts where possible.
- **Verification**: Restart sandbox and check state.
- **Expected Result**: State is preserved.
#### AC-0208-034
- **Requirement**: Suspected malicious sandboxes MUST be quarantined.
- **Verification**: Flag sandbox as suspicious.
- **Expected Result**: Sandbox is quarantined.

### Architecture
#### AC-0208-035
- **Requirement**: The architecture MUST be illustrated with a Mermaid graph TD diagram.
- **Verification**: Inspect Section 8.
- **Expected Result**: Graph TD diagram is present.
#### AC-0208-036
- **Requirement**: The sandbox manager MUST define at least six runtime invariants.
- **Verification**: Count invariants in Section 7.
- **Expected Result**: Six invariants are defined.
#### AC-0208-037
- **Requirement**: The specification MUST define at least eight goals.
- **Verification**: Count goals in Section 2.
- **Expected Result**: Eight goals are defined.
#### AC-0208-038
- **Requirement**: The specification MUST define at least three non-goals.
- **Verification**: Count non-goals in Section 3.
- **Expected Result**: Three non-goals are defined.
#### AC-0208-039
- **Requirement**: The specification MUST define at least six sandbox philosophy principles.
- **Verification**: Count principles in Section 4.
- **Expected Result**: Six principles are defined.

### Performance
#### AC-0208-040
- **Requirement**: Sandbox creation MUST complete within 5,000 ms.
- **Verification**: Benchmark sandbox creation.
- **Expected Result**: Creation completes within 5,000 ms.
#### AC-0208-041
- **Requirement**: Resource allocation MUST complete within 1 ms.
- **Verification**: Benchmark resource allocation.
- **Expected Result**: Allocation completes within 1 ms.
#### AC-0208-042
- **Requirement**: Quota check MUST complete within 0.01 ms.
- **Verification**: Benchmark quota check.
- **Expected Result**: Check completes within 0.01 ms.
#### AC-0208-043
- **Requirement**: OOM response MUST complete within 10 ms.
- **Verification**: Measure OOM response time.
- **Expected Result**: Response completes within 10 ms.
#### AC-0208-044
- **Requirement**: Sandbox destruction MUST complete within 2,000 ms.
- **Verification**: Benchmark sandbox destruction.
- **Expected Result**: Destruction completes within 2,000 ms.

### Consistency
#### AC-0208-045
- **Requirement**: The sandbox model MUST be consistent with RFC-0201.
- **Verification**: Compare sandbox definitions between RFC-0201 and RFC-0208.
- **Expected Result**: Definitions are consistent.
#### AC-0208-046
- **Requirement**: The sandbox model MUST be consistent with RFC-0008.
- **Verification**: Compare sandbox definitions between RFC-0008 and RFC-0208.
- **Expected Result**: Definitions are consistent.
#### AC-0208-047
- **Requirement**: The sandbox model MUST be consistent with RFC-0207 security boundaries.
- **Verification**: Compare security boundaries between RFC-0207 and RFC-0208.
- **Expected Result**: Boundaries are consistent.
#### AC-0208-048
- **Requirement**: The sandbox lifecycle MUST be consistent with RFC-0203.
- **Verification**: Compare lifecycle states between RFC-0203 and RFC-0208.
- **Expected Result**: States are consistent.
#### AC-0208-049
- **Requirement**: The resource quotas MUST be consistent with RFC-0204 performance budgets.
- **Verification**: Compare budgets between RFC-0204 and RFC-0208.
- **Expected Result**: Budgets are consistent.

### Edge Cases
#### AC-0208-050
- **Requirement**: The sandbox MUST handle plugins with zero resource declarations.
- **Verification**: Load plugin with no resource declarations.
- **Expected Result**: Plugin loads with defaults.
#### AC-0208-051
- **Requirement**: The sandbox MUST handle concurrent plugin loads.
- **Verification**: Load 100 plugins simultaneously.
- **Expected Result**: All load successfully.
#### AC-0208-052
- **Requirement**: The sandbox MUST handle plugin resource limit changes at runtime.
- **Verification**: Change resource limits of running plugin.
- **Expected Result**: Limits are updated.
#### AC-0208-053
- **Requirement**: The sandbox MUST handle plugin removal during active execution.
- **Verification**: Remove plugin during execution.
- **Expected Result**: Resources are recovered.
#### AC-0208-054
- **Requirement**: The sandbox MUST handle network disconnection during plugin operation.
- **Verification**: Disconnect network during plugin operation.
- **Expected Result**: Plugin handles gracefully.

### Security
#### AC-0208-055
- **Requirement**: Sandbox boundaries MUST be enforced by the Platform, not by plugin cooperation.
- **Verification**: Inspect enforcement mechanism.
- **Expected Result**: Platform enforces boundaries.
#### AC-0208-056
- **Requirement**: Resource quota violations MUST be logged as security events.
- **Verification**: Exceed resource quota and check logs.
- **Expected Result**: Violation is logged.
#### AC-0208-057
- **Requirement**: The sandbox MUST prevent privilege escalation beyond declared limits.
- **Verification**: Attempt privilege escalation.
- **Expected Result**: Escalation is blocked.
#### AC-0208-058
- **Requirement**: Sandbox isolation MUST survive host OS crashes.
- **Verification**: Simulate host crash.
- **Expected Result**: Isolation is maintained.
#### AC-0208-059
- **Requirement**: The sandbox MUST prevent information leakage between plugins.
- **Verification**: Attempt cross-plugin information theft.
- **Expected Result**: Information is isolated.

### Documentation
#### AC-0208-060
- **Requirement**: The resource quota table MUST include all twelve resource types.
- **Verification**: Count entries in Section 11.
- **Expected Result**: All twelve resources are listed.
#### AC-0208-061
- **Requirement**: The glossary MUST define at least five sandbox terms.
- **Verification**: Count glossary entries in Section 21.
- **Expected Result**: At least five terms are defined.
#### AC-0208-062
- **Requirement**: The specification MUST include a Mermaid state diagram for sandbox lifecycle.
- **Verification**: Inspect Section 19.
- **Expected Result**: State diagram is present.
---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 24 References
1. **RFC-0008**: Runtime Plugin Host
2. **RFC-0201**: Plugin Overview
3. **RFC-0203**: Plugin Lifecycle
4. **RFC-0204**: Plugin Loader
5. **RFC-0207**: Plugin Security
6. **RFC-0209**: Plugin API
7. **RFC-1006**: Common Error Model
8. **ADR-0005**: Plugin Architecture
9. **glossary.md**: Unified Atlas Glossary

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 26 Future Evolution
- **Dynamic Resource Scaling**: Future versions MAY define dynamic resource scaling allowing plugins to request additional resources at runtime.
- **Sandbox Snapshot**: Future versions MAY define sandbox snapshotting allowing plugins to save and restore execution state.
- **Hardware-Accelerated Isolation**: Future versions MAY define hardware-assisted isolation for improved performance.
- **Multi-Tenant Sandboxing**: Future versions MAY define multi-tenant sandboxing for shared infrastructure deployments.
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