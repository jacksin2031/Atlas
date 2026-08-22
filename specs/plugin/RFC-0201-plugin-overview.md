# RFC-0201: Plugin Overview

RFC: RFC-0201
Title: Plugin Overview
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-06-30
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0005 Runtime Event Bus
  - RFC-0007 Runtime IPC Architecture
  - RFC-0008 Runtime Plugin Host
  - RFC-0012 Runtime Capability Registry
  - RFC-0101 IPC Overview
  - RFC-0107 IPC Security
  - RFC-0112 IPC Extension
  - RFC-1001 Common Event Model
  - RFC-1003 Common Capability Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Related RFC:
  - RFC-0202 Plugin Manifest
  - RFC-0203 Plugin Lifecycle
  - RFC-0204 Plugin Loader
  - RFC-0214 Plugin Extension Model
Related ADR:
  - ADR-0005 Plugin Architecture
  - ADR-0010 IPC and Runtime Architecture
  - ADR-0012 Contract-First Specification
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
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0002 | Consumed | Runtime Lifecycle |

### Consumers
- RFC-0323 Workflow Plugin Integration
- RFC-0501 Marketplace Protocol (plugin distribution)

### Providers
- RFC-0001 Runtime Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the plugin philosophy, extension architecture, responsibilities, goals, boundaries, lifecycle overview, and interaction models defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, ADR-0010, and ADR-0012.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Plugin Philosophy](#4-plugin-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Plugin Types](#9-plugin-types)
10. [Plugin Lifecycle Overview](#10-plugin-lifecycle-overview)
11. [Interaction with Runtime](#11-interaction-with-runtime)
12. [Interaction with IPC](#12-interaction-with-ipc)
13. [Interaction with Workflow](#13-interaction-with-workflow)
14. [Interaction with Vision](#14-interaction-with-vision)
15. [Interaction with AI](#15-interaction-with-ai)
16. [Extension Principles](#16-extension-principles)
17. [Performance Targets](#17-performance-targets)
18. [Security Principles](#18-security-principles)
19. [Compatibility Model](#19-compatibility-model)
20. [Glossary](#20-glossary)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Cross References](#22-cross-references)
23. [References](#23-references)
24. [Revision History](#24-revision-history)
25. [Future Evolution](#25-future-evolution)

---


## 2 Goals

1. **Extensibility Without Fragmentation**: Provide a uniform extension mechanism that allows diverse plugin types (Workflow, Vision, AI, Storage, UI, IPC, Knowledge, Marketplace, Provider, Adapter, Service, Utility) to integrate through a single architectural pattern.

2. **Isolation by Default**: Every Plugin MUST execute within an enforced isolation boundary. Plugins MUST NOT access host resources without explicit capability negotiation and permission granting.

3. **Deterministic Lifecycle**: Plugin state transitions MUST follow a formally defined state machine (see RFC-0203). Every transition MUST be observable, auditable, and reversible where feasible.

4. **Capability-Driven Integration**: Plugin access to Runtime services, IPC channels, Workflow nodes, Vision processors, and AI adapters MUST be governed by a capability model (see RFC-0206).

5. **Security Through Least Privilege**: Plugins MUST operate with the minimum permissions required for their declared function. The permission system MUST enforce filesystem, network, IPC, and host boundaries.

6. **Observability**: Every Plugin lifecycle event, capability change, security violation, and error MUST produce a standardized event (see RFC-0210) and contribute to platform-level observability.

7. **Versioned Compatibility**: Plugin manifests, APIs, and extension points MUST follow semantic versioning (see RFC-0212). Breaking changes MUST be identifiable and manageable through migration and rollback procedures.

8. **Dependency Resolution**: Plugin dependencies MUST form a directed acyclic graph (see RFC-0211). Circular dependencies MUST be detected before loading. Optional and required dependencies MUST be handled distinctly.

9. **Marketplace Integration**: Plugins MUST be discoverable, verifiable, and installable through marketplace mechanisms (see RFC-0213) while supporting offline and enterprise repositories.

10. **Extension Point Stability**: The extension model (see RFC-0214) MUST provide stable, versioned extension points that enable plugins to register services, workflow nodes, UI components, commands, providers, adapters, processors, and handlers without modifying core platform code.

---



## 4 Plugin Philosophy

1. **Isolation by Default**: Plugins start with zero permissions. Every resource access requires explicit entitlement through the manifest declaration and capability negotiation.

2. **Contract-First Integration**: All Plugin-Platform interactions occur through versioned, schema-validated contracts. No implicit agreements exist between plugins and the Runtime.

3. **Deterministic Lifecycle**: Plugin state transitions follow a finite state machine. Every transition is triggered by an explicit operation and produces a lifecycle event.

4. **Capability Negotiation**: Plugins declare required capabilities in their manifest. The Runtime verifies capability availability before activation. Missing capabilities trigger fallback or rejection.

5. **Observable by Design**: Every Plugin action, state change, error, and security event produces a standardized platform event. No Plugin behavior is invisible to the observability layer.

6. **Versioned Evolution**: All Plugin interfaces, manifests, and extension points follow semantic versioning. Backward compatibility is maintained within major version boundaries.

7. **Dependency Transparency**: Plugin dependencies are fully declared, validated, and visualized. The dependency graph is acyclic and deterministically ordered.

8. **Security Through Defense in Depth**: Multiple independent security controls operate at every Plugin boundary: manifest validation, sandbox isolation, permission enforcement, IPC authentication, and audit logging.

---

This specification IS responsible for:
- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 6 Boundaries

- **Plugin subsystem MAY communicate with**:
  - Runtime Service Registry (RFC-0003)
  - Runtime Event Bus (RFC-0005)
  - Runtime State Manager (RFC-0006)
  - Runtime Capability Registry (RFC-0012)
  - Runtime Resource Manager (RFC-0009)
  - IPC Dispatcher (RFC-0007)
  - IPC Security Layer (RFC-0107)
  - Common Event Model (RFC-1001)
  - Common Capability Model (RFC-1003)
  - Common Manifest Model (RFC-1005)
  - Common Error Model (RFC-1006)

- **Plugin subsystem MUST NOT communicate with**:
  - Direct hardware interfaces
  - User display subsystems without UI framework mediation
  - External networks without IPC channel mediation
  - Other plugin memory spaces directly

---


## 8 Architecture

The Plugin subsystem comprises the following architectural components:

`mermaid
graph TD
    subgraph Platform
        Runtime["Runtime Core"]
        IPC["IPC Dispatcher"]
        EventBus["Event Bus"]
        CapReg["Capability Registry"]
        StateMgr["State Manager"]
        SecurityMgr["Security Manager"]
        Obs["Observability"]
    end
    
    subgraph Plugin Subsystem
        Loader["Plugin Loader"]
        Registry["Plugin Registry"]
        LifecycleMgr["Lifecycle Manager"]
        SandboxMgr["Sandbox Manager"]
        DepResolver["Dependency Resolver"]
        ManifestValidator["Manifest Validator"]
        APIProvider["API Provider"]
    end
    
    subgraph Plugin Packages
        P1["Plugin Package A"]
        P2["Plugin Package B"]
        P3["Plugin Package N"]
    end
    
    Runtime --> Loader
    Runtime --> Registry
    Loader --> ManifestValidator
    Loader --> DepResolver
    Loader --> SandboxMgr
    Loader --> LifecycleMgr
    Registry --> CapReg
    LifecycleMgr --> EventBus
    SandboxMgr --> SecurityMgr
    DepResolver --> Registry
    ManifestValidator --> SecurityMgr
    
    P1 --> Loader
    P2 --> Loader
    P3 --> Loader
    
    LifecycleMgr --> APIProvider
    APIProvider --> IPC
    APIProvider --> Runtime
    SandboxMgr --> P1
    SandboxMgr --> P2
    SandboxMgr --> P3
    
    EventBus --> Obs
    SecurityMgr --> Obs
`

Component responsibilities:

| Component | RFC Reference | Responsibility |
|---|---|---|
| Plugin Loader | RFC-0204 | Discovery, scanning, validation, loading, isolation, registration, activation, failure recovery |
| Plugin Registry | RFC-0205 | Registration, lookup, discovery, filtering, capability query, dependency query, health, metrics |
| Plugin Lifecycle Manager | RFC-0203 | Install, load, initialize, activate, running, suspend, resume, deactivate, unload, update, rollback, removal |
| Plugin Sandbox Manager | RFC-0208 | Execution isolation, resource quotas, filesystem isolation, memory/CPU/GPU limits, IPC restrictions |
| Plugin Capability Manager | RFC-0206 | Capability model, negotiation, discovery, feature flags, runtime compatibility, permission mapping |
| Plugin Security Manager | RFC-0207 | Trust model, authentication, authorization, least privilege, threat model, audit, tamper detection |
| Plugin API Provider | RFC-0209 | API contracts, extension interfaces, service access, event subscriptions, configuration, context |
| Plugin Event Manager | RFC-0210 | Event catalog, lifecycle events, capability events, error events, delivery guarantees |
| Plugin Dependency Resolver | RFC-0211 | Dependency graph, resolution, optional/required handling, circular detection, load order |
| Plugin Version Manager | RFC-0212 | Semantic versioning, compatibility, breaking changes, migration, deprecation, rollback |
| Plugin Marketplace Client | RFC-0213 | Publishing, installation, verification, trust, digital signatures, ratings, updates |
| Plugin Extension Registrar | RFC-0214 | Extension points, custom services, workflow nodes, UI, commands, providers, adapters |

---

- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 10 Plugin Lifecycle Overview

The plugin lifecycle follows a finite state machine. The complete state registry is maintained in catalog/plugin-states.md. Each state has a stable ID prefix PSTATE-.

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

Lifecycle phases:

| Phase | States | RFC Reference |
|---|---|---|
| Installation | DISCOVERED, VALIDATING | RFC-0204 |
| Loading | LOADED, INITIALIZING | RFC-0204 |
| Activation | ACTIVATING, ACTIVE, RUNNING | RFC-0203 |
| Suspension | SUSPENDING, SUSPENDED, RESUMING | RFC-0203 |
| Deactivation | DEACTIVATING, DEACTIVATED, UNLOADING, UNLOADED | RFC-0203 |
| Update | UPDATING, ROLLING-BACK | RFC-0203 |
| Removal | REMOVING, REMOVED | RFC-0203 |
| Error | ERROR, FAILED | RFC-0203 |

---

    Runtime-->>Loader: activation complete
`

---

        end
    else Not Authenticated
        IPC-->>Plugin: ConnectionRefused
    end
`

---

| RFC-0201 | Consumed | Plugin Overview |


## 14 Interaction with Vision

Plugins of type PT-VISION register custom vision processors with the Vision Engine. These processors extend the platform visual perception capabilities.

- **Processor Registration**: Vision plugins declare vision processors in their manifest. The Plugin Extension Registrar registers these processors with the Vision Engine.
- **Frame Processing**: Vision plugins receive frame data through the IPC channel. All frame data transfers conform to the IPC message model (RFC-0102).
- **Result Submission**: Vision plugins submit processing results through the API Provider. Results are validated against the declared output schema.
- **Capability Negotiation**: Vision plugins declare required vision capabilities (screen capture, OCR, gesture recognition). The Capability Registry verifies availability before activation.

---

| RFC-0201 | Consumed | Plugin Overview |


## 16 Extension Principles

1. **Stable Extension Points**: Extension points MUST be versioned and backward-compatible within a major version. New extension points MAY be added in minor versions without breaking existing plugins.

2. **Interface Segregation**: Each extension point MUST define a focused, single-responsibility interface. Plugins MUST NOT be forced to implement unused interface methods.

3. **Declaration Over Convention**: All extension behavior MUST be declared in the plugin manifest. Implicit conventions are prohibited.

4. **Fail-Fast Registration**: Extension registration MUST validate all declarations at registration time. Invalid extensions MUST be rejected before activation.

5. **Runtime Extensibility**: Extensions MUST be activatable and deactivatable at runtime without platform restart. State changes MUST be observable through the event system.

6. **Cross-Plugin Isolation**: Extensions registered by different plugins MUST operate in isolation. One plugin extension MUST NOT interfere with another plugin extension.

---


## 18 Security Principles

1. **Zero-Trust Plugin Execution**: Every plugin is treated as untrusted by default. No plugin receives implicit permissions.

2. **Defense in Depth**: Security controls operate at multiple layers: manifest validation, sandbox isolation, permission enforcement, IPC authentication, and audit logging. Compromise of one layer MUST NOT result in total breach.

3. **Least Privilege**: Plugins operate with the minimum permissions declared in their manifest. Additional permissions MUST be explicitly requested and granted.

4. **Tamper Detection**: Plugin artifacts and manifests MUST be integrity-verified at load time and periodically during execution. Detected tampering MUST trigger immediate suspension.

5. **Audit Trail**: Every security-relevant plugin event (installation, activation, permission request, violation, suspension) MUST produce an immutable audit record.

6. **Trust Hierarchy**: Plugin trust levels form a hierarchy (see catalog/plugin-trust-levels.md). Higher trust levels grant broader permissions. Trust level escalation MUST require organizational approval.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Glossary

| Term | Definition |
|---|---|
| Plugin | A packaged unit of extension logic that integrates with the Atlas Platform through declared contracts. |
| Manifest | A structured metadata document declaring plugin identity, capabilities, permissions, dependencies, and extension points. |
| Sandbox | An isolated execution boundary that restricts plugin access to platform resources. |
| Capability | A declared feature or resource availability that a plugin requires or provides. |
| Extension Point | A versioned interface through which plugins register custom behavior with the platform. |
| Lifecycle State | A discrete phase in the plugin existence timeline, forming a finite state machine. |
| Trust Level | A classification of plugin security posture ranging from unverified to certified. |
| Permission | A granular access right declared in the manifest and enforced by the security subsystem. |
| Dependency | A declared relationship between plugins indicating required or optional capability needs. |
| Registry | The authoritative data store maintaining all registered plugin metadata and state. |


---

- **Expected Result**: Both lists contain at least four entries each with specific subsystem references.

#### AC-0201-006
- **Requirement**: The architecture MUST include a dependency resolver component.
- **Verification**: Inspect the architecture diagram in Section 8 for the dependency resolver box.
- **Expected Result**: The dependency resolver component is present and connected to the loader and registry.

#### AC-0201-007
- **Requirement**: The architecture MUST include a sandbox manager component.
- **Verification**: Inspect the architecture diagram in Section 8 for the sandbox manager box.
- **Expected Result**: The sandbox manager component is present and connected to the loader, security manager, and plugin packages.

#### AC-0201-008
- **Requirement**: The architecture MUST include a manifest validator component.
- **Verification**: Inspect the architecture diagram in Section 8 for the manifest validator box.
- **Expected Result**: The manifest validator component is present and connected to the loader and security manager.

#### AC-0201-009
- **Requirement**: The architecture MUST include an API provider component.
- **Verification**: Inspect the architecture diagram in Section 8 for the API provider box.
- **Expected Result**: The API provider component is present and connected to the lifecycle manager, IPC, and runtime.

#### AC-0201-010
- **Requirement**: The architecture MUST include a capability manager component.
- **Verification**: Inspect the architecture diagram in Section 8 for the capability manager box.
- **Expected Result**: The capability manager component is present and connected to the registry and capability registry.

#### AC-0201-011
- **Requirement**: The architecture MUST show event bus connectivity from the lifecycle manager.
- **Verification**: Inspect the architecture diagram in Section 8 for the lifecycle manager to event bus connection.
- **Expected Result**: A directed arrow connects the lifecycle manager to the event bus.

#### AC-0201-012
- **Requirement**: The architecture MUST show security manager connectivity to observability.
- **Verification**: Inspect the architecture diagram in Section 8 for the security manager to observability connection.
- **Expected Result**: A directed arrow connects the security manager to observability.

#### AC-0201-013
- **Requirement**: The architecture MUST define at least ten distinct plugin subsystem components.
- **Verification**: Count the component entries in the component responsibility table in Section 8.
- **Expected Result**: At least twelve components are listed.

#### AC-0201-014
- **Requirement**: The architecture MUST be consistent with the common manifest model in RFC-1005.
- **Verification**: Compare manifest field definitions between RFC-1005 and RFC-0202.
- **Expected Result**: All common manifest fields are recognized and extended by the plugin manifest.

#### AC-0201-015
- **Requirement**: The architecture MUST be consistent with the common event model in RFC-1001.
- **Verification**: Compare event category definitions between RFC-1001 and RFC-0210.
- **Expected Result**: The plugin event category is defined with all plugin-specific event types.

### Plugin Types

#### AC-0201-016
- **Requirement**: The Plugin subsystem MUST define at least ten distinct plugin types.
- **Verification**: Count the entries in the plugin types table in Section 9.
- **Expected Result**: At least twelve plugin types are defined.

#### AC-0201-017
- **Requirement**: Every plugin type MUST have a stable ID with the PT- prefix.
- **Verification**: Inspect all type IDs in Section 9 for the PT- prefix.
- **Expected Result**: All type IDs conform to the PT-XXXX naming convention.

#### AC-0201-018
- **Requirement**: Every plugin type MUST have a human-readable name.
- **Verification**: Inspect the name column of the plugin types table in Section 9.
- **Expected Result**: All twelve types have non-empty name entries.

#### AC-0201-019
- **Requirement**: Every plugin type MUST have a descriptive definition.
- **Verification**: Inspect the description column of the plugin types table in Section 9.
- **Expected Result**: All descriptions are at least one complete sentence.

#### AC-0201-020
- **Requirement**: Every plugin type MUST reference an associated RFC.
- **Verification**: Inspect the associated RFC column of the plugin types table in Section 9.
- **Expected Result**: All twelve types reference RFC-0209, RFC-0213, or RFC-0214.

#### AC-0201-021
- **Requirement**: A plugin manifest MUST declare exactly one primary plugin type.
- **Verification**: Inspect the manifest schema definition in RFC-0202.
- **Expected Result**: The plugin_type field has a required constraint with exactly one value.

#### AC-0201-022
- **Requirement**: Secondary plugin types MAY be declared in addition to the primary type.
- **Verification**: Inspect the manifest schema definition in RFC-0202.
- **Expected Result**: The secondary_types field exists as an optional array.

#### AC-0201-023
- **Requirement**: Plugin types MUST be consistent with the catalog definition in catalog/plugin-types.md.
- **Verification**: Cross-reference all type IDs between Section 9 and the catalog file.
- **Expected Result**: All twelve type IDs match exactly.

#### AC-0201-024
- **Requirement**: The PT-WORKFLOW type MUST extend workflow execution graph nodes.
- **Verification**: Inspect the PT-WORKFLOW description in Section 9.
- **Expected Result**: The description explicitly references workflow graph node extension.

#### AC-0201-025
- **Requirement**: The PT-VISION type MUST extend visual perception capabilities.
- **Verification**: Inspect the PT-VISION description in Section 9.
- **Expected Result**: The description explicitly references visual perception extension.

### Lifecycle

#### AC-0201-026
- **Requirement**: The plugin lifecycle MUST be represented as a finite state machine.
- **Verification**: Inspect the state diagram in Section 10.
- **Expected Result**: All twenty lifecycle states are represented as state boxes with labeled transitions.

#### AC-0201-027
- **Requirement**: Every lifecycle state MUST have a defined entry and exit transition.
- **Verification**: Trace each state in the state diagram for incoming and outgoing arrows.
- **Expected Result**: All states except DISCOVERED and UNLOADED have both entry and exit transitions.

#### AC-0201-028
- **Requirement**: The lifecycle MUST include an error state that is reachable from any active phase.
- **Verification**: Inspect the state diagram for error-state transitions from INITIALIZING, ACTIVATING, and RUNNING.
- **Expected Result**: At least three error transitions are defined.

#### AC-0201-029
- **Requirement**: The lifecycle MUST include a rollback state for update failures.
- **Verification**: Inspect the state diagram for the ROLLING-BACK state.
- **Expected Result**: The ROLLING-BACK state exists with transitions from UPDATING and to LOADED or FAILED.

#### AC-0201-030
- **Requirement**: The lifecycle MUST define a suspension and resumption path.
- **Verification**: Inspect the state diagram for SUSPENDING, SUSPENDED, and RESUMING states.
- **Expected Result**: All three states exist with correct bidirectional transitions.

#### AC-0201-031
- **Requirement**: The lifecycle MUST define a deactivation and unloading path.
- **Verification**: Inspect the state diagram for DEACTIVATING, DEACTIVATED, UNLOADING, and UNLOADED states.
- **Expected Result**: All four states exist with correct sequential transitions.

#### AC-0201-032
- **Requirement**: The lifecycle MUST define a removal path.
- **Verification**: Inspect the state diagram for REMOVING and REMOVED states.
- **Expected Result**: Both states exist with correct transitions from RUNNING.

#### AC-0201-033
- **Requirement**: The lifecycle MUST define a discovered-to-failed path for validation errors.
- **Verification**: Inspect the state diagram for the VALIDATING to FAILED transition.
- **Expected Result**: The transition exists and is labeled with validation failure.

#### AC-0201-034
- **Requirement**: The lifecycle MUST define at least eight lifecycle phases.
- **Verification**: Count the phase entries in the lifecycle phases table in Section 10.
- **Expected Result**: Eight phases are listed.

#### AC-0201-035
- **Requirement**: The lifecycle state machine MUST be consistent with the common state model in RFC-1002.
- **Verification**: Compare state classification between RFC-1002 and RFC-0203.
- **Expected Result**: Plugin states conform to the common state model categories.

### Runtime Integration

#### AC-0201-036
- **Requirement**: The plugin subsystem MUST register plugins with the Runtime Core.
- **Verification**: Inspect the Runtime interaction sequence diagram in Section 11.
- **Expected Result**: The registerPlugin operation is shown with manifest parameter.

#### AC-0201-037
- **Requirement**: The plugin subsystem MUST check capabilities before registration.
- **Verification**: Inspect the sequence diagram for the capability check step.
- **Expected Result**: The checkCapabilities operation exists between Runtime and Capability Registry.

#### AC-0201-038
- **Requirement**: The plugin subsystem MUST create a state entry upon successful registration.
- **Verification**: Inspect the sequence diagram for the createState operation.
- **Expected Result**: The createState operation exists between Runtime and State Manager.

#### AC-0201-039
- **Requirement**: The plugin subsystem MUST publish activation events to the Event Bus.
- **Verification**: Inspect the sequence diagram for the publish operation.
- **Expected Result**: The publish(PEVT-ACTIVATED) operation exists.

#### AC-0201-040
- **Requirement**: The plugin subsystem MUST handle capability unavailability during registration.
- **Verification**: Inspect the alternative path in the sequence diagram.
- **Expected Result**: A rejection path returns registration rejected with reason.

#### AC-0201-041
- **Requirement**: Plugin registration MUST include the full plugin manifest.
- **Verification**: Inspect the registerPlugin operation signature in Section 11.
- **Expected Result**: The operation accepts pluginId and manifest parameters.

#### AC-0201-042
- **Requirement**: The Runtime MUST acknowledge plugin registration.
- **Verification**: Inspect the sequence diagram for the acknowledgment return.
- **Expected Result**: A return arrow labeled registration acknowledged exists.

#### AC-0201-043
- **Requirement**: Plugin activation MUST be a distinct operation from registration.
- **Verification**: Inspect the sequence diagram for a separate activatePlugin call.
- **Expected Result**: The activatePlugin operation exists as a second call.

#### AC-0201-044
- **Requirement**: The plugin subsystem MUST integrate with the Runtime State Manager.
- **Verification**: Inspect the architecture diagram for the State Manager connection.
- **Expected Result**: The State Manager component is present in the platform boundary.

#### AC-0201-045
- **Requirement**: The plugin subsystem MUST integrate with the Runtime Resource Manager.
- **Verification**: Inspect Section 6 boundaries for Resource Manager reference.
- **Expected Result**: The Runtime Resource Manager is listed as a may-communicate target.

### IPC Integration

#### AC-0201-046
- **Requirement**: Plugin IPC connections MUST require authentication.
- **Verification**: Inspect the IPC sequence diagram in Section 12 for the authenticate step.
- **Expected Result**: The authenticate operation exists between IPC and Security Manager.

#### AC-0201-047
- **Requirement**: Plugin IPC messages MUST require authorization.
- **Verification**: Inspect the IPC sequence diagram for the authorize step.
- **Expected Result**: The authorize operation exists between IPC and Security Manager.

#### AC-0201-048
- **Requirement**: Unauthorized IPC messages MUST be rejected with PermissionDenied.
- **Verification**: Inspect the IPC sequence diagram unauthorized path.
- **Expected Result**: A PermissionDenied return exists with a security violation log.

#### AC-0201-049
- **Requirement**: Unauthenticated IPC connections MUST be refused.
- **Verification**: Inspect the IPC sequence diagram authentication failure path.
- **Expected Result**: A ConnectionRefused return exists.

#### AC-0201-050
- **Requirement**: All IPC interactions MUST conform to RFC-0107 security requirements.
- **Verification**: Inspect Section 12 introduction for RFC-0107 reference.
- **Expected Result**: RFC-0107 is explicitly cited as the governing security specification.

### Extension Principles

#### AC-0201-051
- **Requirement**: Extension points MUST be versioned.
- **Verification**: Inspect Section 16 for versioning statement.
- **Expected Result**: The first extension principle states extension points are versioned and backward-compatible.

#### AC-0201-052
- **Requirement**: Extension points MUST be single-responsibility interfaces.
- **Verification**: Inspect the interface segregation principle in Section 16.
- **Expected Result**: The principle explicitly requires focused, single-responsibility interfaces.

#### AC-0201-053
- **Requirement**: Extension behavior MUST be declared in the manifest.
- **Verification**: Inspect the declaration over convention principle in Section 16.
- **Expected Result**: The principle explicitly prohibits implicit conventions.

#### AC-0201-054
- **Requirement**: Extension registration MUST validate at registration time.
- **Verification**: Inspect the fail-fast registration principle in Section 16.
- **Expected Result**: The principle explicitly requires validation at registration time.

#### AC-0201-055
- **Requirement**: Extensions MUST be activatable and deactivatable at runtime.
- **Verification**: Inspect the runtime extensibility principle in Section 16.
- **Expected Result**: The principle explicitly states runtime activation and deactivation.

### Performance

#### AC-0201-056
- **Requirement**: Plugin discovery MUST complete within 100 ms.
- **Verification**: Inspect the performance targets table in Section 17.
- **Expected Result**: The Plugin Discovery metric shows 100 ms target.

#### AC-0201-057
- **Requirement**: Manifest validation MUST complete within 50 ms.
- **Verification**: Inspect the performance targets table.
- **Expected Result**: The Manifest Validation metric shows 50 ms target.

#### AC-0201-058
- **Requirement**: Dependency resolution MUST complete within 200 ms.
- **Verification**: Inspect the performance targets table.
- **Expected Result**: The Dependency Resolution metric shows 200 ms target.

#### AC-0201-059
- **Requirement**: Hook invocation MUST complete within 500 ms.
- **Verification**: Inspect the performance targets table.
- **Expected Result**: The Hook Invocation metric shows 500 ms target.

#### AC-0201-060
- **Requirement**: Event publication MUST complete within 1 ms.
- **Verification**: Inspect the performance targets table.
- **Expected Result**: The Event Publication metric shows 1 ms target.

### Security

#### AC-0201-061
- **Requirement**: Every plugin MUST start with zero permissions.
- **Verification**: Inspect the zero-trust principle in Section 18.
- **Expected Result**: The principle explicitly states zero default permissions.

#### AC-0201-062
- **Requirement**: Security controls MUST operate at multiple independent layers.
- **Verification**: Inspect the defense in depth principle in Section 18.
- **Expected Result**: Five security layers are enumerated: manifest, sandbox, permission, IPC, audit.

#### AC-0201-063
- **Requirement**: Plugins MUST operate with minimum declared permissions.
- **Verification**: Inspect the least privilege principle in Section 18.
- **Expected Result**: The principle explicitly requires minimum declared permissions.

#### AC-0201-064
- **Requirement**: Plugin integrity MUST be verified at load time.
- **Verification**: Inspect the tamper detection principle in Section 18.
- **Expected Result**: The principle explicitly requires integrity verification at load time.

#### AC-0201-065
- **Requirement**: Security-relevant plugin events MUST produce audit records.
- **Verification**: Inspect the audit trail principle in Section 18.
- **Expected Result**: The principle enumerates installation, activation, permission request, violation, and suspension.

### Compatibility

#### AC-0201-066
- **Requirement**: Major version changes MUST indicate breaking changes.
- **Verification**: Inspect the compatibility model in Section 19.
- **Expected Result**: The major version rule states breaking changes and non-interoperability.

#### AC-0201-067
- **Requirement**: Minor version changes MUST be backward-compatible.
- **Verification**: Inspect the compatibility model in Section 19.
- **Expected Result**: The minor version rule states additive backward-compatible changes.

#### AC-0201-068
- **Requirement**: Patch version changes MUST be freely mixable.
- **Verification**: Inspect the compatibility model in Section 19.
- **Expected Result**: The patch version rule states free mixing is allowed.

#### AC-0201-069
- **Requirement**: Capability negotiation MUST occur during plugin activation.
- **Verification**: Inspect the capability negotiation section in Section 19.
- **Expected Result**: The negotiation process is described with degraded or inactive fallback states.

#### AC-0201-070
- **Requirement**: Extension points MUST be versioned and backward-compatible within a major version.
- **Verification**: Inspect the extension point compatibility section in Section 19.
- **Expected Result**: The section explicitly states backward compatibility within declared version ranges.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 25 Future Evolution

- **Plugin Hot-Swap**: Future versions MAY define hot-swap capabilities allowing plugin binary replacement without state loss.
- **Plugin Composition**: Future versions MAY define plugin composition patterns allowing multiple plugins to be packaged and deployed as a single unit.
- **Plugin Telemetry**: Future versions MAY define standardized telemetry collection within the sandbox boundary for performance analytics.
- **Plugin Testing Framework**: Future versions MAY define a standardized testing framework for plugin validation before marketplace publication.
- **Plugin Federation**: Future versions MAY define cross-instance plugin federation allowing plugins to operate across multiple Atlas platform instances.

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

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

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




