RFC: RFC-0304

Title: Workflow Runtime

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

Layer: Core

Normative: YES

Audience: All Subsystem Teams

ADR References:

  - ADR-0012

Constitution References:

  - Section 1 (Workflow Philosophy)

Related RFCs:

  - RFC-0301 Workflow Overview

  - RFC-0302 Workflow Language

  - RFC-0303 Workflow Execution

  - RFC-0305 Workflow Lifecycle

  - RFC-0306 Workflow State

  - RFC-0307 Workflow Context

  - RFC-0308 Workflow Events

  - RFC-0309 Workflow Actions

  - RFC-0310 Workflow Conditions

  - RFC-0311 Workflow Triggers

  - RFC-0312 Workflow Scheduler

  - RFC-0313 Workflow Parallelism

  - RFC-0314 Workflow Error Handling

  - RFC-0315 Workflow Recovery

  - RFC-0317 Workflow Validation

  - RFC-0319 Workflow Security

  - RFC-0320 Workflow Performance

  - RFC-0321 Workflow Observability

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x

Last Updated: 2026-07-01

Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/runtime-contract.json
  - schemas/workflow/service-registration.json
Related Catalog:
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/runtime-contract.json
  -   - schemas/workflow/service-registration.json
Related Catalog:
  - catalog/workflow-capabilities.md
  -   - catalog/workflow-resource-types.md

  - catalog/workflow-capabilities.md
  - catalog/workflow-resource-types.md

---



## Normative Status

## Authority

This RFC is the authoritative specification for the workflow subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Workflow | A declarative directed graph specification expressing WHAT must happen. | Glossary |
| Execution | The process of evaluating a workflow graph and activating nodes. | Glossary |
| Run | A single invocation of a workflow definition. | Glossary |
| Node | A graph element representing an atomic unit of work. | Glossary |
| Context | A transaction state container holding variables and metrics. | Glossary |
| Scheduler | The execution coordinator that prioritizes tasks. | Glossary |

---

This specification is Normative. Every Atlas subsystem MUST conform to the runtime contract defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.



This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.



---
---


This RFC is the authoritative specification for the RFC 0304 workflow runtime.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## Table of Contents

1. [Introduction](#1-introduction)

2. [Runtime Philosophy](#2-runtime-philosophy)

3. [Goals](#3-goals)

4. [Non-Goals](#4-non-goals)

5. [Runtime Responsibilities](#5-runtime-responsibilities)

6. [Runtime-Workflow Interaction Model](#6-runtime-workflow-interaction-model)

7. [Runtime Lifecycle Integration](#7-runtime-lifecycle-integration)

8. [Runtime Resource Management for Workflows](#8-runtime-resource-management-for-workflows)

9. [Runtime Service Model for Workflow Execution](#9-runtime-service-model-for-workflow-execution)

10. [Runtime Event Bus Integration](#10-runtime-event-bus-integration)

11. [Runtime Capability Discovery for Workflow Nodes](#11-runtime-capability-discovery-for-workflow-nodes)

12. [Runtime Manifest Loading for Workflows](#12-runtime-manifest-loading-for-workflows)

13. [Runtime-Workflow Contract Boundary](#13-runtime-workflow-contract-boundary)

14. [Runtime Isolation Model](#14-runtime-isolation-model)

15. [Runtime Scaling for Workflows](#15-runtime-scaling-for-workflows)

16. [Runtime Health Monitoring](#16-runtime-health-monitoring)

17. [Acceptance Criteria](#17-acceptance-criteria)

18. [References](#18-references)

19. [Changelog](#19-changelog)

20. [Compatibility](#20-compatibility)



---



## 1 Introduction



The Workflow Runtime specification defines the contract between the Atlas runtime and the workflow execution engine. The runtime is the platform layer that hosts, manages, and orchestrates workflow execution. The workflow engine is the component that evaluates, traverses, and completes workflow graphs. This specification defines the boundaries, interactions, and integration points between these two layers.



The runtime is NOT the workflow engine. The runtime provides the platform services; the workflow engine provides the execution logic. The runtime hosts workflows; the workflow engine executes them. The runtime manages resources; the workflow engine consumes them. The runtime observes execution; the workflow engine produces observability data.



The runtime contract encompasses:

- **Responsibilities**: What the runtime MUST provide to the workflow engine.

- **Interaction Model**: How the runtime and workflow engine communicate.

- **Lifecycle Integration**: How workflow lifecycles integrate with runtime lifecycles.

- **Resource Management**: How the runtime allocates and manages resources for workflows.

- **Service Model**: How the runtime exposes services to the workflow engine.

- **Event Integration**: How the runtime event bus carries workflow events.

- **Capability Discovery**: How the workflow engine discovers available capabilities.

- **Manifest Loading**: How the runtime loads and validates workflow manifests.





---



## 2 Runtime Philosophy



The runtime philosophy rests upon four foundational principles:



### Principle 1: Separation of Platform and Execution



The runtime MUST separate platform concerns (resource management, lifecycle, observability) from execution concerns (graph evaluation, node activation, result propagation). This separation ensures that changes to the execution model do not require changes to the runtime, and vice versa.



### Principle 2: Hosting Over Controlling



The runtime HOSTS workflows; it does NOT control their execution. The workflow engine retains full authority over execution decisions. The runtime provides services and resources but does not dictate how the workflow engine uses them.



### Principle 3: Lifecycle Alignment



The runtime lifecycle MUST align with the workflow lifecycle. Workflow creation, execution, and termination MUST map to runtime resource allocation, utilization, and release. The runtime MUST support the full workflow lifecycle without premature resource release or delayed resource acquisition.



### Principle 4: Observability by Default



Every runtime interaction with workflows MUST be observable. The runtime MUST emit events, metrics, and traces that provide complete visibility into workflow hosting, resource allocation, and lifecycle transitions.



---



## 3 Goals



| Goal | Description | Verification Method |

|---|---|---|

| Clear Responsibilities | Runtime responsibilities MUST be well-defined and non-overlapping with workflow engine duties. | Responsibility matrix test |

| Clean Interaction Model | The runtime-workflow interaction MUST follow a defined contract. | Contract verification test |

| Lifecycle Integration | Workflow lifecycle MUST integrate seamlessly with runtime lifecycle. | Integration test |

| Resource Management | The runtime MUST manage resources for workflows effectively. | Resource management test |

| Service Model | The runtime MUST expose services for workflow execution. | Service interface test |

| Event Integration | Workflow events MUST flow through the runtime event bus. | Event flow test |

| Capability Discovery | The workflow engine MUST discover capabilities through the runtime. | Discovery test |

| Manifest Loading | The runtime MUST load and validate workflow manifests. | Loading test |



---



## 4 Non-Goals



The following are explicitly OUT of scope for this specification:



- **Execution Logic**: The runtime does not define how workflows are executed; that is covered by RFC-0303.

- **Workflow Language**: The syntax and semantics of workflow definitions are covered by RFC-0302.

- **Node Implementation**: How individual nodes perform their work is outside the runtime scope.

- **Condition Evaluation**: Condition evaluation logic is handled by the workflow engine per RFC-0310.

- **Action Execution**: Action execution semantics are defined by RFC-0309.

- **Storage Backend**: The runtime delegates storage to the storage subsystem per RFC-0324.





---



## 5 Runtime Responsibilities



### 5.1 Responsibility Matrix



The runtime is responsible for the following categories of duties:



| Responsibility Category | Duties | Boundary |

|---|---|---|

| Hosting | Provide execution environment for workflows. | Runtime owns, workflow consumes. |

| Resource Management | Allocate, track, and release resources for workflows. | Runtime owns, workflow declares. |

| Lifecycle Management | Manage runtime-level lifecycle events affecting workflows. | Runtime initiates, workflow responds. |

| Event Routing | Route workflow events through the event bus. | Runtime routes, workflow emits. |

| Service Provision | Provide services (scheduler, state, IPC) to workflows. | Runtime provides, workflow uses. |

| Observability | Emit runtime-level metrics and traces for workflows. | Runtime emits, workflow observed. |

| Security | Enforce security policies on workflow execution. | Runtime enforces, workflow complies. |

| Scaling | Scale runtime resources to accommodate workflow demand. | Runtime scales, workflow triggers. |

| Health Monitoring | Monitor runtime health and workflow hosting health. | Runtime monitors, workflow affected. |

| Cleanup | Clean up resources and state after workflow termination. | Runtime cleans, workflow signals. |



### 5.2 Responsibility Boundaries



| Boundary | Runtime Responsibility | Workflow Engine Responsibility |

|---|---|---|

| Environment | Provides the execution environment. | Defines what the environment needs. |

| Resources | Allocates and tracks resources. | Declares resource requirements. |

| Scheduling | Provides scheduling primitives. | Computes execution ordering. |

| Events | Routes and delivers events. | Emits workflow events. |

| State | Persists runtime state. | Manages workflow state transitions. |

| Security | Enforces access control. | Declares security requirements. |

| Metrics | Collects runtime metrics. | Produces execution metrics. |

| Recovery | Restores runtime from failure. | Restores workflow from checkpoint. |



### 5.3 Runtime Duty Execution Order



The runtime executes its duties in the following order:



1. **Load**: Load the workflow manifest and validate its structure.

2. **Allocate**: Allocate resources based on workflow requirements.

3. **Initialize**: Initialize the execution environment for the workflow.

4. **Host**: Host the workflow during its execution lifecycle.

5. **Observe**: Observe and record workflow execution events.

6. **Manage**: Manage resource allocation and lifecycle during execution.

7. **Terminate**: Terminate the workflow hosting when execution completes.

8. **Clean Up**: Release all resources and clean up artifacts.





---



## 6 Runtime-Workflow Interaction Model



### 6.1 Interaction Layers



The runtime and workflow engine interact through three distinct layers:



| Layer | Purpose | Interface Type |

|---|---|---|

| Hosting Layer | Provides execution environment and lifecycle management. | Lifecycle API |

| Service Layer | Provides runtime services (scheduler, state, event bus). | Service API |

| Observability Layer | Exposes runtime metrics and traces for workflow observation. | Observability API |



### 6.2 Interaction Flow



mermaid

sequenceDiagram

    participant RM as Runtime Manager

    participant WL as Workflow Loader

    participant HE as Hosting Engine

    participant WE as Workflow Engine

    participant EB as Event Bus

    participant SM as State Manager

    

    RM->>WL: Load workflow manifest

    WL->>WE: Create workflow instance

    WE->>HE: Request hosting

    HE->>RM: Allocate resources

    RM->>HE: Confirm allocation

    HE->>WE: Hosting confirmed

    WE->>EB: Emit WorkflowStarted

    WE->>WE: Execute workflow graph

    WE->>EB: Emit NodeStarted/NodeCompleted

    WE->>SM: Persist state checkpoints

    WE->>EB: Emit WorkflowCompleted

    WE->>HE: Request termination

    HE->>RM: Release resources

    RM->>HE: Confirm release

    HE->>WE: Termination confirmed





### 6.3 Interaction Contracts



| Contract | Direction | Description |

|---|---|---|

| Manifest Contract | Runtime to Workflow Engine | Runtime provides manifest to workflow engine. |

| Resource Contract | Workflow Engine to Runtime | Workflow engine declares resource needs to runtime. |

| Lifecycle Contract | Bidirectional | Both parties agree on lifecycle state transitions. |

| Event Contract | Workflow Engine to Runtime | Workflow engine emits events through runtime bus. |

| State Contract | Workflow Engine to Runtime | Workflow engine persists state through runtime store. |

| Observability Contract | Runtime to External | Runtime exposes workflow observability data. |



### 6.4 Interaction Error Handling



When an interaction fails:



| Failure | Runtime Action | Workflow Engine Action |

|---|---|---|

| Manifest load failure | Report error, abort hosting. | Reject workflow instance. |

| Resource allocation failure | Report shortage, retry or fail. | Queue or cancel workflow. |

| Event bus failure | Buffer events, retry delivery. | Retry emission or fail. |

| State persistence failure | Report error, retry write. | Retry persist or halt. |

| Lifecycle transition failure | Rollback to previous state. | Wait for recovery or fail. |





---



## 7 Runtime Lifecycle Integration



### 7.1 Lifecycle Mapping



The workflow lifecycle maps to the runtime lifecycle as follows:



| Workflow Phase | Runtime Phase | Runtime Action |

|---|---|---|

| Creation | Provisioning | Allocate hosting infrastructure. |

| Parsing | Initialization | Load manifest, resolve references. |

| Validation | Configuration | Validate resource requirements. |

| Planning | Scheduling | Compute resource allocation plan. |

| Execution | Hosting | Maintain execution environment. |

| Completion | Teardown | Collect results, release resources. |

| Termination | Cleanup | Remove artifacts, close connections. |



### 7.2 Lifecycle State Synchronization



The runtime MUST synchronize its state with the workflow lifecycle state:



| Workflow State | Runtime State | Synchronization Rule |

|---|---|---|

| Created | Provisioning | Runtime begins provisioning on workflow creation. |

| Initialized | Initialized | Runtime confirms resource availability. |

| Queued | Queued | Runtime places workflow in execution queue. |

| Running | Hosting | Runtime maintains active hosting environment. |

| Paused | Suspended | Runtime freezes resource allocation. |

| Resumed | Resumed | Runtime restores resource allocation. |

| Completed | Teardown | Runtime begins resource release process. |

| Failed | Error | Runtime records error state and initiates recovery. |

| Terminated | Terminated | Runtime completes all cleanup operations. |



### 7.3 Lifecycle Integration Sequence



mermaid

sequenceDiagram

    participant WF as Workflow Engine

    participant RT as Runtime

    participant RS as Resource Manager

    participant SC as Scheduler

    

    WF->>RT: Create workflow instance

    RT->>RS: Request resources

    RS->>RT: Confirm allocation

    RT->>WF: Instance ready

    WF->>SC: Submit execution plan

    SC->>WF: Confirm scheduling

    WF->>RT: Begin execution

    RT->>RT: Maintain hosting

    loop Execution

        WF->>RT: Emit events

        RT->>RT: Route events

        WF->>RT: Persist checkpoints

        RT->>RT: Store checkpoints

    end

    WF->>RT: Complete execution

    RT->>RS: Release resources

    RS->>RT: Confirm release

    RT->>WF: Termination confirmed







---



## 8 Runtime Resource Management for Workflows



### 8.1 Resource Categories



The runtime manages the following resource categories for workflow execution:



| Resource Category | Type | Allocation Unit | Scope |

|---|---|---|---|

| Compute | Processing capacity | Processing units | Per workflow |

| Memory | Heap and stack space | Bytes | Per workflow |

| Storage | Persistent and ephemeral | Bytes | Per workflow |

| Network | Bandwidth and connections | Megabits per second | Per workflow |

| External Services | API connections and queues | Connections | Per workflow |

| Custom | Vendor-defined resources | Vendor units | Per workflow |



### 8.2 Resource Allocation Model



The runtime uses a hierarchical resource allocation model:



| Level | Description | Allocation Method |

|---|---|---|

| Cluster | Physical or virtual cluster resources. | Cluster manager. |

| Node Pool | Collection of compute nodes. | Pool allocator. |

| Workflow Instance | Individual workflow resource allocation. | Instance allocator. |

| Node Execution | Per-node execution resource reservation. | Node allocator. |

| Execution Window | Time-bounded resource usage window. | Time allocator. |



### 8.3 Resource Quotas



The runtime enforces resource quotas at multiple levels:



| Quota Level | Constraint | Enforcement |

|---|---|---|

| Per Workflow | Maximum resources per workflow instance. | Instance allocator. |

| Per Workflow Type | Maximum resources per workflow type definition. | Type validator. |

| Per Runtime Partition | Maximum resources per runtime partition. | Partition manager. |

| Global | Maximum total runtime resources. | Global allocator. |



### 8.4 Resource Lifecycle



Resources follow a defined lifecycle within the runtime:



| Stage | Description | Transition |

|---|---|---|

| Requested | Resource requirement declared by workflow. | Manifest parsing. |

| Reserved | Resource tentatively held for workflow. | Planning phase. |

| Allocated | Resource committed to workflow. | Execution phase. |

| In Use | Resource actively consumed by workflow. | During execution. |

| Released | Resource returned to the pool. | Workflow termination. |

| Freed | Resource available for new allocations. | After cleanup. |



### 8.5 Resource Monitoring



The runtime monitors resource utilization continuously:



| Monitor | Metric | Threshold | Action |

|---|---|---|---|

| CPU Utilization | Percentage of processing units used. | 90% | Throttle or scale. |

| Memory Utilization | Percentage of allocated memory used. | 85% | Alert or reclaim. |

| Storage Utilization | Percentage of allocated storage used. | 95% | Expand or reject. |

| Network Utilization | Bandwidth consumption rate. | 90% | Rate limit. |

| Connection Count | Number of active external connections. | Max limit | Reject new connections. |





---



## 9 Runtime Service Model for Workflow Execution



### 9.1 Service Catalog



The runtime provides the following services to the workflow engine:



| Service | Description | Provider | Consumer |

|---|---|---|---|

| Scheduler | Provides task scheduling primitives. | Runtime Scheduler | Workflow Engine |

| EventBus | Routes workflow events to subscribers. | Runtime Event Bus | Workflow Engine |

| StateManager | Persists and retrieves workflow state. | Runtime State Manager | Workflow Engine |

| ResourceManager | Allocates and tracks workflow resources. | Runtime Resource Manager | Workflow Engine |

| CapabilityRegistry | Provides capability discovery and registration. | Runtime Capability Registry | Workflow Engine |

| ManifestLoader | Loads and validates workflow manifests. | Runtime Manifest Loader | Workflow Engine |

| SecurityManager | Enforces security policies on workflows. | Runtime Security Manager | Workflow Engine |

| ObservabilityCollector | Collects and exposes workflow metrics. | Runtime Observability | Workflow Engine |

| StorageManager | Provides persistent storage for workflows. | Runtime Storage Manager | Workflow Engine |

| IPCBroker | Provides inter-process communication. | Runtime IPC Broker | Workflow Engine |



### 9.2 Service Interface Contract



Each runtime service exposes a defined interface contract:



| Contract Element | Requirement |

|---|---|

| Service Name | Each service MUST have a unique, registered name. |

| Service Version | Each service MUST declare its version. |

| Service Endpoint | Each service MUST expose a discoverable endpoint. |

| Service Capabilities | Each service MUST declare its supported operations. |

| Service SLA | Each service MUST declare its availability and latency guarantees. |

| Service Error Codes | Each service MUST define its error code taxonomy. |



### 9.3 Service Discovery



The workflow engine discovers available runtime services through:



1. **Registration**: Services register themselves with the runtime service registry.

2. **Discovery**: The workflow engine queries the registry for available services.

3. **Selection**: The workflow engine selects services based on capability requirements.

4. **Binding**: The workflow engine binds to the selected services.

5. **Health Check**: The workflow engine verifies service health before use.



### 9.4 Service Availability



The runtime guarantees the following service availability levels:



| Service | Availability | Downtime Tolerance | Recovery Time |

|---|---|---|---|

| Scheduler | 99.99% | Zero | Sub-second |

| EventBus | 99.99% | Zero | Sub-second |

| StateManager | 99.99% | Minimal | Second-level |

| ResourceManager | 99.99% | Minimal | Second-level |

| CapabilityRegistry | 99.95% | Low | Minute-level |

| ManifestLoader | 99.9% | Low | Second-level |

| SecurityManager | 99.99% | Zero | Sub-second |

| ObservabilityCollector | 99.9% | Medium | Minute-level |

| StorageManager | 99.99% | Minimal | Second-level |

| IPCBroker | 99.99% | Zero | Sub-second |





---



## 10 Runtime Event Bus Integration



### 10.1 Event Routing



The runtime event bus serves as the central communication channel for workflow events. All workflow events MUST flow through the runtime event bus.



**Event Flow Architecture:**



mermaid

flowchart LR

    WE[Workflow Engine] -->|Emits| EB[Runtime Event Bus]

    EB -->|Routes| OS[Observability System]

    EB -->|Routes| SM[State Manager]

    EB -->|Routes| RM[Resource Manager]

    EB -->|Routes| SC[Scheduler]

    EB -->|Routes| ES[External Subscribers]





### 10.2 Event Categories Through Bus



The runtime event bus carries the following workflow event categories:



| Event Category | Source | Destination | Priority |

|---|---|---|---|

| Lifecycle Events | Workflow Engine | Runtime Manager | High |

| Execution Events | Workflow Engine | Observability | Normal |

| State Events | State Manager | All subscribers | Normal |

| Error Events | Any component | Error handler | Critical |

| Metric Events | Any component | Metrics collector | Low |

| Security Events | Security Manager | Audit log | Critical |



### 10.3 Event Delivery Guarantees



The runtime event bus provides the following delivery guarantees:



| Guarantee | Description | Implementation |

|---|---|---|

| Ordering | Events for the same workflow are delivered in order. | Per-workflow queue. |

| Persistence | Events are persisted before delivery acknowledgment. | Write-ahead log. |

| At-Least-Once | Every event is delivered at least once. | Retry on failure. |

| Deduplication | Duplicate events are identified and removed. | Event ID tracking. |

| Filtering | Subscribers receive only relevant events. | Topic-based routing. |

| Rate Limiting | Event emission rates are bounded. | Token bucket algorithm. |



### 10.4 Event Schema



Workflow events carried by the runtime bus conform to the common event model (RFC-1001):



| Field | Required | Description |

|---|---|---|

| event_id | YES | Unique event identifier. |

| event_type | YES | Category of the event. |

| timestamp | YES | Event creation time. |

| workflow_id | YES | Associated workflow instance ID. |

| node_id | NO | Associated node ID, if applicable. |

| payload | YES | Event-specific data. |

| metadata | YES | Additional event metadata. |

| correlation_id | NO | Correlation with related events. |

| causation_id | NO | ID of the event that caused this event. |





---



## 11 Runtime Capability Discovery for Workflow Nodes



### 11.1 Capability Registry



The runtime maintains a capability registry that maps node type declarations to available capability implementations. The workflow engine queries this registry during the Parse and Plan phases.



**Capability Registry Structure:**



mermaid

classDiagram

    class CapabilityRegistry {

        +register(capability)

        +lookup(type_id)

        +list_all()

        +validate(type_id)

    }

    class Capability {

        +capability_id

        +capability_type

        +version

        +parameters

        +results

        +constraints

    }

    class NodeDefinition {

        +node_id

        +node_type

        +required_capabilities

    }

    CapabilityRegistry --> Capability : contains

    NodeDefinition ..> Capability : requires





### 11.2 Discovery Process



The capability discovery process follows these steps:



1. **Registration**: Capability implementations register with the runtime registry.

2. **Declaration**: Workflow node types declare their required capabilities.

3. **Query**: The workflow engine queries the registry for matching capabilities.

4. **Validation**: The runtime validates that all required capabilities are available.

5. **Binding**: The workflow engine binds node types to capability implementations.

6. **Verification**: The runtime verifies binding integrity before execution.



### 11.3 Capability Matching Rules



| Rule | Description |

|---|---|

| Exact Match | Capability type MUST match the node type declaration exactly. |

| Version Compatibility | Capability version MUST be compatible with the declared version range. |

| Parameter Compatibility | Capability parameters MUST satisfy the node parameter requirements. |

| Result Compatibility | Capability results MUST satisfy the node result expectations. |

| Constraint Satisfaction | Capability constraints MUST be satisfiable by the runtime environment. |

| Availability | Capability MUST be available at discovery time. |



### 11.4 Capability Fallback



When a required capability is not available:



| Scenario | Action |

|---|---|

| Exact match unavailable | Search for compatible version. |

| Compatible version unavailable | Search for substitute capability. |

| Substitute available | Use substitute with warning. |

| No substitute available | Fail workflow validation. |

| Partial match available | Require manual override. |





---



## 12 Runtime Manifest Loading for Workflows



### 12.1 Manifest Loading Process



The runtime manifest loader is responsible for loading, validating, and resolving workflow manifests before they are passed to the workflow engine.



**Manifest Loading Sequence:**



mermaid

sequenceDiagram

    participant ML as Manifest Loader

    participant VM as Version Manager

    participant RV as Reference Resolver

    participant SV as Schema Validator

    participant WE as Workflow Engine

    

    ML->>ML: Read manifest file

    ML->>VM: Resolve manifest version

    VM-->>ML: Return version info

    ML->>RV: Resolve all references

    RV-->>ML: Return resolved manifest

    ML->>SV: Validate against schema

    SV-->>ML: Return validation result

    alt Validation passed

        ML->>WE: Pass validated manifest

    else Validation failed

        ML-->>WE: Return validation errors

    end





### 12.2 Manifest Validation Rules



The runtime validates manifests against the following rules:



| Rule | Description | Severity |

|---|---|---|

| Schema Compliance | Manifest MUST conform to the workflow manifest schema. | Error |

| Version Compatibility | Manifest version MUST be compatible with runtime version. | Error |

| Reference Integrity | All referenced nodes, edges, and capabilities MUST exist. | Error |

| Type Consistency | All type references MUST resolve to valid types. | Error |

| Parameter Completeness | All required parameters MUST be present. | Error |

| Resource Sufficiency | Declared resources MUST be available. | Warning |

| Security Compliance | Manifest MUST comply with security policies. | Error |

| Size Limits | Manifest size MUST not exceed maximum limits. | Error |



### 12.3 Manifest Caching



The runtime caches validated manifests to avoid repeated loading:



| Cache Level | Scope | Lifetime | Eviction |

|---|---|---|---|

| Instance | Single workflow instance. | Instance lifetime. | Instance termination. |

| Definition | Workflow definition. | Definition validity. | Definition update. |

| Type | Node type definitions. | Runtime lifetime. | Type update. |

| Capability | Capability registrations. | Runtime lifetime. | Capability deregistration. |



### 12.4 Manifest Versioning



The runtime supports manifest versioning for backward compatibility:



| Version Policy | Description |

|---|---|

| Forward Compatible | Newer runtimes MUST support older manifest versions. |

| Backward Compatible | Older runtimes MAY reject newer manifest versions. |

| Version Negotiation | Runtime and manifest negotiate compatible version. |

| Deprecation Warning | Deprecated manifest versions trigger warnings. |

| Mandatory Upgrade | Some manifest versions require runtime upgrade. |





---



## 13 Runtime-Workflow Contract Boundary



### 13.1 Contract Definition



The runtime-workflow contract defines the explicit boundary between runtime responsibilities and workflow engine responsibilities. Both parties MUST adhere to this contract.



**Contract Boundary Diagram:**



mermaid

flowchart TB

    subgraph Runtime

        RM[Runtime Manager]

        RS[Resource Manager]

        EB[Event Bus]

        SM[State Manager]

        CM[Capability Manager]

        ML[Manifest Loader]

        SC[Scheduler]

        SEC[Security Manager]

        OBS[Observability]

    end

    

    subgraph WorkflowEngine

        WE[Workflow Engine]

        GE[Graph Executor]

        NE[Node Executor]

        PE[Phase Manager]

        CE[Context Manager]

        RE[Result Engine]

        FT[Fault Tolerance]

        OB[Observability Producer]

    end

    

    RM -->|Lifecycle| WE

    RS -->|Resources| GE

    EB <-->|Events| OB

    SM <-->|State| GE

    CM -->|Capabilities| NE

    ML -->|Manifest| WE

    SC -->|Schedule| GE

    SEC -->|Policy| WE

    OBS <--|Metrics| OB





### 13.2 Contract Obligations



| Party | Obligation | Enforcement |

|---|---|---|

| Runtime | Provide declared services. | Service contract. |

| Runtime | Enforce resource quotas. | Resource manager. |

| Runtime | Route events correctly. | Event bus. |

| Runtime | Persist state reliably. | State manager. |

| Runtime | Discover capabilities accurately. | Capability registry. |

| Runtime | Load manifests correctly. | Manifest loader. |

| Workflow Engine | Declare resource requirements. | Manifest schema. |

| Workflow Engine | Emit events per protocol. | Event contract. |

| Workflow Engine | Persist state per protocol. | State contract. |

| Workflow Engine | Respect runtime policies. | Security manager. |

| Workflow Engine | Comply with resource limits. | Resource manager. |

| Workflow Engine | Produce observability data. | Observability producer. |



### 13.3 Contract Violation Handling



When a contract violation occurs:



| Violation Type | Detection | Response |

|---|---|---|

| Runtime service unavailable | Health check failure | Retry, escalate, or fail workflow. |

| Resource quota exceeded | Quota monitor | Throttle or terminate workflow. |

| Event protocol violation | Event validator | Drop event, log violation. |

| State persistence failure | State manager | Retry, alert, halt workflow. |

| Manifest loading failure | Manifest loader | Reject workflow, report error. |

| Capability mismatch | Capability registry | Fail validation, report error. |





---



## 14 Runtime Isolation Model



### 14.1 Isolation Levels



The runtime provides isolation between workflow instances at multiple levels:



| Isolation Level | Scope | Description |

|---|---|---|

| Process | Process boundary | Separate processes for separate workflows. |

| Memory | Memory space | Isolated memory spaces prevent data leakage. |

| Resource | Resource pool | Dedicated resource pools per workflow. |

| Network | Network namespace | Isolated network paths per workflow. |

| State | State store | Separate state partitions per workflow. |

| Event | Event topic | Separate event topics per workflow. |



### 14.2 Isolation Guarantees



| Guarantee | Description | Enforcement |

|---|---|---|

| Data Isolation | Workflow data MUST NOT leak between instances. | Memory isolation. |

| Resource Isolation | Resource usage MUST NOT interfere between instances. | Resource quotas. |

| State Isolation | Workflow state MUST be separate per instance. | State partitioning. |

| Event Isolation | Events from one workflow MUST NOT affect another. | Event topic separation. |

| Timing Isolation | Timing attacks MUST be prevented. | Timing randomization. |

| Security Isolation | Privilege escalation MUST be prevented. | Security manager. |



### 14.3 Isolation Violation Response



When isolation is violated:



1. The runtime detects the violation through monitoring.

2. The runtime isolates the affected workflow instance.

3. The runtime logs the violation for investigation.

4. The runtime determines the scope of the breach.

5. The runtime initiates remediation procedures.

6. The runtime notifies relevant stakeholders.





---



## 15 Runtime Scaling for Workflows



### 15.1 Scaling Dimensions



The runtime scales workflows along multiple dimensions:



| Dimension | Description | Scaling Method |

|---|---|---|

| Horizontal | Add more runtime instances. | Instance replication. |

| Vertical | Increase resources per instance. | Resource augmentation. |

| Parallel | Execute more workflows concurrently. | Concurrency scaling. |

| Geographic | Deploy to multiple regions. | Regional distribution. |



### 15.2 Scaling Triggers



The runtime scales based on the following triggers:



| Trigger | Condition | Scaling Action |

|---|---|---|

| Queue Depth | Pending workflows exceed threshold. | Add runtime instances. |

| Resource Utilization | Average utilization exceeds 80%. | Scale vertically. |

| Latency | Execution latency exceeds SLA. | Add capacity. |

| Error Rate | Error rate exceeds threshold. | Scale out and investigate. |

| Throughput | Requests per second exceeds capacity. | Horizontal scaling. |

| Availability | Instance health degrades. | Replace unhealthy instance. |



### 15.3 Scaling Policies



| Policy | Description | Use Case |

|---|---|---|

| Reactive | Scale based on current metrics. | Variable workloads. |

| Predictive | Scale based on historical patterns. | Scheduled workloads. |

| Scheduled | Scale at predefined times. | Known peak periods. |

| Manual | Scale based on operator decision. | Critical workloads. |

| Auto | Combination of reactive and predictive. | General purpose. |





---



## 16 Runtime Health Monitoring



### 16.1 Health Check Categories



The runtime monitors health across the following categories:



| Category | Check | Frequency | Alert Threshold |

|---|---|---|---|

| Process Health | Runtime process is alive. | Every 5 seconds | 3 consecutive failures. |

| Service Health | All services are responding. | Every 10 seconds | 2 consecutive failures. |

| Resource Health | Resource availability is sufficient. | Every 30 seconds | Below minimum threshold. |

| Queue Health | Execution queue depth is manageable. | Every 15 seconds | Exceeds maximum depth. |

| Event Health | Event bus throughput is normal. | Every 10 seconds | Lag exceeds threshold. |

| State Health | State manager is accessible. | Every 15 seconds | Unavailable for 30 seconds. |

| Workflow Health | Active workflows are progressing. | Every 60 seconds | Stalled for timeout. |

| Security Health | Security policies are enforced. | Every 5 minutes | Policy violation detected. |
---

## 18 Terminology

| Term | Definition | Source |
|---|---|---|
| Runtime | The platform layer that hosts, manages, and orchestrates workflow execution. | RFC-0301 |
| Runtime Contract | The defined interface between the runtime platform and the workflow execution engine. | This RFC |
| Service Registration | The process of registering workflow services with the runtime. | This RFC |
| Resource Allocation | The runtime's assignment of computational resources to workflow instances. | This RFC |
| Health Monitoring | The continuous assessment of runtime and workflow component status. | This RFC |

## 19 Layer Boundaries

### 19.1 Responsibilities
This specification IS responsible for: defining the runtime-workflow contract, specifying the hosting model, establishing resource management for workflows, and defining the service model for workflow execution.

### 19.2 Non-Responsibilities
This specification IS NOT responsible for: executing workflow graphs (delegated to RFC-0303), defining the workflow language (delegated to RFC-0302), or managing plugin lifecycles (delegated to RFC-0323).

### 19.3 Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0302 | Consumed | Workflow Language provides definition model |
| RFC-0303 | Consumed | Workflow Execution provides the execution engine contract |
| RFC-0305 | Consumed | Workflow Lifecycle provides lifecycle integration |
| RFC-0312 | Consumed | Workflow Scheduler provides scheduling integration |
| RFC-0319 | Consumed | Workflow Security provides runtime security |
| RFC-0320 | Consumed | Workflow Performance provides runtime performance |
| RFC-0321 | Consumed | Workflow Observability provides runtime telemetry |
| RFC-0323 | Consumed | Workflow Plugin Integration provides plugin hosting |
| RFC-0324 | Consumed | Workflow Storage provides runtime persistence |

### 19.4 Consumers
- Workflow Execution (RFC-0303): Hosted by the runtime.
- Workflow Scheduler (RFC-0312): Integrated with runtime resource management.
- Workflow Plugin Integration (RFC-0323): Plugins hosted by the runtime.
- Workflow Observability (RFC-0321): Runtime emits observability data.

### 19.5 Providers
- Runtime Contract Schema (schemas/workflow/runtime-contract.json): Provides the runtime contract format.
- Service Registration Schema (schemas/workflow/service-registration.json): Provides the service registration format.
- Capabilities Catalog (catalog/workflow-capabilities.md): Provides the capability taxonomy.
- Resource Types Catalog (catalog/workflow-resource-types.md): Provides the resource type taxonomy.

### 19.6 Forbidden Dependencies
- This specification MUST NOT depend on any specific runtime implementation (Node.js, .NET, Java, etc.).
- This specification MUST NOT assume a particular process model (single-process, multi-process, microservices).

## 20 Future Evolution
- **Distributed Runtime**: Runtime spanning multiple physical or virtual machines.
- **Serverless Runtime**: Ephemeral runtime instances triggered by workflow events.
- **Multi-Tenant Runtime**: Runtime with isolation guarantees between tenant workloads.
- **Edge Runtime**: Lightweight runtime for edge computing environments.
- **Hybrid Runtime**: Seamless orchestration across cloud, on-premises, and edge runtimes.

## 21 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

The runtime contract is defined as abstract behavioral interfaces, not implementation-specific APIs.

## 22 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0302 | Workflow Language (definition model) |
| RFC-0303 | Workflow Execution (execution engine contract) |
| RFC-0305 | Workflow Lifecycle (lifecycle integration) |
| RFC-0312 | Workflow Scheduler (scheduling integration) |
| RFC-0319 | Workflow Security (runtime security) |
| RFC-0320 | Workflow Performance (runtime performance) |
| RFC-0321 | Workflow Observability (runtime telemetry) |
| RFC-0323 | Workflow Plugin Integration (plugin hosting) |
| RFC-0324 | Workflow Storage (runtime persistence) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/runtime-contract.json | Runtime Contract JSON Schema |
| schemas/workflow/service-registration.json | Service Registration JSON Schema |
| catalog/workflow-capabilities.md | Capabilities Catalog |
| catalog/workflow-resource-types.md | Resource Types Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0304 (this document), RFC-0301 (Overview), RFC-0303 (Execution) |
---


## 17 Acceptance Criteria

### 17.1 Runtime Contract Conformance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The runtime MUST expose a service discovery interface that returns all registered services on request. | Service discovery query test: Query service catalog → Verify all services listed in Section 9.1 appear in response |
| AC-02 | The runtime MUST initialize all declared services before the first workflow execution begins. | Startup sequence test: Start runtime → Wait for Ready state → Verify service registry is non-empty and all services report Healthy |
| AC-03 | The runtime MUST enforce isolation boundaries between concurrently executing workflows. | Concurrent execution test: Launch N workflows with overlapping resource requirements → Verify no cross-workflow state leakage detected via correlation ID tracing |
| AC-04 | The runtime MUST support at least three (3) distinct hosting models: embedded, sidecar, and standalone. | Hosting model test: Deploy runtime in each model → Verify workflow manifest loading, service registration, and execution succeed identically across all three |
| AC-05 | The runtime MUST provide health check endpoints for all services with status values from {Healthy, Degraded, Unhealthy, Unknown}. | Health check test: Query health endpoint → Verify response contains status field with one of four enumerated values for each service |
| AC-06 | The runtime MUST load workflow manifests from a pluggable source without hard-coded path assumptions. | Manifest loading test: Configure three different manifest sources (filesystem, HTTP, embedded) → Verify identical workflow execution from all three |
| AC-07 | The runtime MUST reject malformed workflow manifests with a validation error matching the schema defined in RFC-0317. | Schema validation test: Submit workflow manifest with invalid field types → Verify rejection with error code from workflow-error-codes.md catalog |
| AC-08 | The runtime MUST propagate capability advertisements from plugins to the workflow execution engine within 100ms of plugin registration. | Capability propagation test: Register plugin with capabilities → Measure time until workflow engine can discover and use those capabilities → Verify ≤ 100ms |

### 17.2 Lifecycle Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-09 | The runtime MUST follow the lifecycle sequence: Initializing → Ready → Running → Stopping → Stopped. | Lifecycle order test: Transition runtime through all states → Verify state transitions occur in prescribed order, no backwards transitions allowed |
| AC-10 | The runtime MUST persist workflow state at every checkpoint boundary defined in RFC-0315. | Checkpoint persistence test: Execute workflow with checkpoints → Inspect storage backend → Verify checkpoint files exist with valid serialized state at each boundary |
| AC-11 | The runtime MUST resume a workflow from the last checkpoint within 5 seconds of restart. | Resume timing test: Stop runtime mid-execution → Restart → Measure time from Ready state to resumption of execution → Verify ≤ 5 seconds |

### 17.3 Resource Management

| # | Criterion | Verification Method |
|---|---|---|
| AC-12 | The runtime MUST enforce resource quotas per workflow as declared in the manifest. | Quota enforcement test: Declare CPU/memory quotas → Execute workflow exceeding quotas → Verify runtime throttles or terminates the workflow |
| AC-13 | The runtime MUST report resource utilization metrics at intervals not exceeding 1 second. | Metrics interval test: Enable resource monitoring → Capture metrics over 10-second window → Verify at least 10 data points collected |

### 17.4 Error Handling

| # | Criterion | Verification Method |
|---|---|---|
| AC-14 | The runtime MUST convert all internal errors to the standardized error format defined in RFC-0314. | Error format test: Trigger five different internal failure modes → Verify each error response conforms to the error schema with category, code, and context fields |
| AC-15 | The runtime MUST log all fatal errors with sufficient context for post-mortem analysis per RFC-0321. | Error logging test: Induce fatal error → Inspect log output → Verify presence of workflow ID, execution ID, node ID, error code, and stack trace |## Revision History

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


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |