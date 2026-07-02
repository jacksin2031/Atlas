RFC: RFC-0001
Title: Runtime Overview
Status: Frozen
Category: Core
Owner: Runtime Architecture Board
Authors: Atlas Specification Committee
Created: 2026-06-27
Updated: 2026-07-01
ADS Version: 1.0.0
Spec Version: 1.0.0
Normative: YES
Depends On: None
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0002 Atlas Development System
Related JSON Schema: None
Related Catalog: None
Audience: All Subsystem Teams
Target Release: 1.0.0
Review Cycle: Annual
Compatibility: Compatible with Spec 1.0

---

## Normative Status

This specification is normative. Every Atlas Runtime implementation MUST conform to the requirements defined herein. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and all active ADRs.

---

## Authority

This RFC is the authoritative specification for the Atlas Runtime architecture.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Runtime | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | Glossary |
| Workspace | The sandboxed directory boundary containing workflow definitions, configuration manifests, local caches, and logs. | Glossary |
| Service | A modular system component registered with the Service Registry, satisfying a specific abstract Service Contract. | Glossary |
| Provider | Infrastructure adapters implementing hardware, operating system, or external API interfaces. | Glossary |
| Scheduler | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | Glossary |
| Event Bus | The asynchronous message broker that routes events based on channel names and priority queues. | Glossary |
| State Store | The transaction-isolated database containing current configurations and runtime variables. | Glossary |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | Glossary |
| Watchdog | The monitoring service checking heartbeats of registered services to initiate recovery routines. | Glossary |
| Sandbox | An isolated execution process or virtual machine context restricting OS access. | Glossary |
| Capability | A feature declaration verified and exposed by the Runtime Manifest. | Glossary |
| Manifest | The declarative definition of a component, including its metadata, dependencies, capabilities, and configuration. | Glossary |
| Contract | A formal agreement defining the interface between two components, specifying required behaviors and guarantees. | Glossary |
| Write-Ahead Log (WAL) | A persistent log recording mutations before committing them to the main state database. | Glossary |
| Dead Letter Queue (DLQ) | A dedicated message queue containing events that could not be delivered to their target subscribers. | Glossary |

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
## 1 Introduction

### 1.1 Purpose

The Atlas Runtime is the foundational execution engine of the Atlas application orchestration platform. It acts as the core supervisor, host environment, and integration broker for all subsystems, including the Workflow Engine, Plugin Host, Vision Capture Engine, and AI Agent Coordinator. It provides a standardized, secure, event-driven, and resource-bounded context within which application workflows execute.

### 1.2 Rationale

Modern application orchestration platforms suffer from fragmented state, non-deterministic side effects, unconstrained resource consumption, and weak security boundaries between plugins, workflows, and host systems. The Atlas Runtime exists to consolidate execution lifecycle management, enforce security sandboxing, guarantee deterministic processing queues, and expose unified communication interfaces.

### 1.3 Goals

- **Deterministic Execution**: Execution queues, event resolution order, and state mutations MUST be deterministic and reproducible. Given the same inputs, states, and event sequences, the Runtime MUST produce identical side effects and state transitions.
- **Strict Modularity**: The Runtime core MUST serve as a thin coordinating container. All domain logic (Workflow execution, Vision processing, AI reasoning) MUST reside in modular, pluggable Services.
- **Scalability and Resource Isolation**: The Runtime MUST scale to coordinate parallel workflow execution threads and handle high-throughput, low-latency operations without compromising state consistency.

### 1.4 Non-Goals

The Runtime explicitly excludes the following:

- **Business Logic**: The Runtime MUST NOT embed application-specific workflows, business logic, or user-defined logic paths.
- **Domain-Specific Automation**: The Runtime MUST NOT know how to interact with specific third-party applications. Automation logic remains the domain of workflows and plugins.

---

## 2 Architecture

The Runtime follows a layered architecture with strict boundaries between components. Each layer exposes a well-defined interface to the layer above and consumes a well-defined interface from the layer below. Cross-layer shortcuts are prohibited.

The Runtime consists of the following core components:

| Component | Responsibility | Related RFC |
|---|---|---|
| Lifecycle Manager | Orchestrates boot, initialization, running, pause, and shutdown sequences | RFC-0002 |
| Service Registry | Registers and locates services using abstract interfaces | RFC-0003 |
| Scheduler | Orchestrates concurrency and thread pool worker allocation | RFC-0004 |
| Event Bus | Routes asynchronous events between services | RFC-0005 |
| State Manager | Manages scopes, snapshots, and transactional WAL flushes | RFC-0006 |
| IPC Bridge | Coordinates inter-process communication | RFC-0007 |
| Plugin Host | Hosts and isolates plugin execution | RFC-0008 |
| Resource Manager | Decides sandboxing thresholds and resource affinity | RFC-0009 |
| Manifest Parser | Loads and validates component manifests | RFC-0010 |
| Error Taxonomy | Defines error codes and failure semantics | RFC-0011 |
| Capability Registry | Coordinates entitlement and permission lookup | RFC-0012 |
| Contracts | Defines service interface signatures | RFC-0013 |

---

## 3 Responsibilities

The Runtime IS responsible for:

- **Lifecycle Management**: Orchestrating the boot, initialization, running, pause, and shutdown sequences of the runtime host and all registered services.
- **Service Discovery**: Managing a Service Registry that registers and locates services using abstract interfaces.
- **Resource Management**: Tracking, limiting, and throttling resource allocations for all running tasks.
- **Scheduling**: Determining execution order and concurrency for tasks.
- **Event Routing**: Validating event structures and scheduling deliveries.
- **Capability Management**: Coordinating entitlement and permission lookup.
- **Configuration Loading**: Reading and locking global immutable constants.
- **State Management**: Managing scopes, snapshots, and transactional persistence.

The Runtime IS NOT responsible for:

- **Workflow Logic**: Script variables and user-defined steps.
- **Plugin Logic**: Third-party operations inside sandboxed environments.
- **Vision Algorithms**: OCR engines and template matching calculations.
- **AI Reasoning**: Model prompts and token routing.
- **User Interface**: Views, windows, widget configurations, and client layout structures.

---

## 4 Principles

1. **Single Runtime Instance**: There MUST be exactly one active Runtime supervisor process per workspace.
2. **Immutable Configuration**: Once loaded during the bootstrap sequence, core configuration parameters MUST be read-only.
3. **Circular Dependency Prohibition**: Circular dependencies are prohibited. If a dependency loop is detected during initialization, the Runtime MUST halt.

---

## 5 Invariants

The Runtime enforces the following invariants on all operations:

- **INV-RT-01**: There MUST be exactly one active Runtime supervisor process executing per workspace.
- **INV-RT-02**: Circular dependency maps among services are prohibited.

Violation of any invariant constitutes a specification breach.

---

## 6 Security

The Runtime enforces the following security requirements:

- **Sandboxing**: All plugin execution MUST occur within an isolated sandbox. The Runtime MUST enforce memory, CPU, and network boundaries.
- **Access Control**: The Runtime MUST implement capability-based access control. Services MUST declare required capabilities in their manifest.
- **Integrity**: The Runtime MUST validate the integrity of all loaded components before initialization.

See [RFC-0008](specs/runtime/RFC-0008-runtime-plugin.md) for plugin host security details. See [RFC-0207](specs/plugin/RFC-0207-plugin-security.md) for plugin security model details.

---

## 7 Performance

The Runtime MUST:

- Initialize all core services within the configured timeout.
- Maintain deterministic scheduling order under concurrent load.
- Support graceful degradation when resource limits are reached.

See [RFC-0004](specs/runtime/RFC-0004-runtime-scheduler.md) for scheduler performance requirements.

---

## 8 Compatibility

This specification is compatible with Spec 1.0. The Runtime maintains backward compatibility within a major version. Breaking changes require a MAJOR version increment per RFC_VERSIONING_POLICY.md.

---

## 9 Compliance

Every Runtime implementation MUST comply with:

- The ADS Constitution
- ADR-0002 (Atlas Development System)
- All Frozen RFCs in the Runtime series (RFC-0001 through RFC-0014)

---

## 10 Future Evolution

Assuming Atlas will exist for at least 10 years, the Runtime MUST support the following future capabilities WITHOUT requiring changes to existing RFCs:

- **Distributed Runtime**: Runtime spanning multiple physical or virtual machines with transparent coordination.
- **Cloud-Native Runtime**: Exposing execution queues and state engines as cloud-native services.
- **Multi-Tenant Runtime**: Isolated execution contexts for multiple organizations on shared infrastructure.
- **Headless Runtime**: Runtime execution without any user interface or interactive component.

Stability Guarantee: The core concepts defined in this specification (Runtime, Service, Scheduler, Event Bus, State Store, Lifecycle, Capability, Manifest) are stable and will NOT change within any major version of the Atlas specification.

---

## 11 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All Runtime contracts are defined as abstract behavioral interfaces.

---

## 12 Acceptance Criteria

### 12.1 Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST register all core services before transitioning to Ready state. | Query Service Registry state after initialization. Expected: Core services report active state. |
| AC-02 | The implementation MUST enforce exactly one Runtime supervisor per workspace. | Attempt to launch a second Runtime instance in the same workspace. Expected: Second instance is rejected. |
| AC-03 | The implementation MUST detect circular dependencies during initialization. | Construct a service dependency graph with a cycle. Expected: Initialization halts with a dependency cycle error. |
| AC-04 | The implementation MUST support rollback of state changes to prevent corruption. | Force task termination mid-operation and inspect state logs. Expected: WAL commits are rolled back successfully. |

### 12.2 Security

| # | Criterion | Verification Method |
|---|---|---|
| AC-05 | The implementation MUST isolate plugin execution from the host process. | Load a plugin that attempts cross-boundary access. Expected: Access is denied. |
| AC-06 | The implementation MUST validate component integrity before loading. | Attempt to load a tampered manifest. Expected: Loading is rejected. |

---

## 13 References

| Reference | Description |
|---|---|
| RFC-0002 | Runtime Lifecycle |
| RFC-0003 | Runtime Service Model |
| RFC-0004 | Runtime Scheduler |
| RFC-0005 | Runtime Event Bus |
| RFC-0006 | Runtime State Management |
| RFC-0007 | Runtime IPC Architecture |
| RFC-0008 | Runtime Plugin Host |
| RFC-0009 | Runtime Resource Management |
| RFC-0010 | Runtime Manifest Specification |
| RFC-0011 | Runtime Error Taxonomy |
| RFC-0012 | Runtime Capability Registry |
| RFC-0013 | Runtime Contracts |
| RFC-0014 | Runtime Reference Architecture |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| ADR-0002 | Atlas Development System |

---

## 14 Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0002 through RFC-0014 |
| Related ADR | ADR-0002 |
| Related JSON Schema | None |
| Related Catalog | None |

---

## 15 Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Frozen | 2026-06-27 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Frozen | 2026-07-01 | Atlas Specification Committee | Restructured to follow RFC_TEMPLATE.md: added Authority, Terminology table, Layer Boundaries, Runtime Independence, improved Acceptance Criteria, consolidated 37 sections into coherent structure |




