# Atlas Master Glossary

> **Authoritative Terminology Registry** — All RFCs MUST reference this document. No RFC may define a term that already appears here.
> **Created**: 2026-07-02
> **Owner**: Atlas Specification Committee
> **Related**: [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md), [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md), [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md)

This glossary defines the authoritative terminology for all components, specifications, and systems within Project Atlas. All RFCs MUST reference this master document. Every term defined here has a single authoritative definition that MUST be used consistently across all RFCs.

| Term | Definition | Source RFC |


| Runtime | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | RFC-0001 |
| Workspace | The sandboxed directory boundary containing workflow definitions, configuration manifests, local caches, and logs. | RFC-0301 |
| Project | A logical collection of workflows, local plugins, and schemas defining a complete execution project context. | RFC-0301 |
| Workflow | A declarative directed graph specification expressing WHAT must happen, not HOW. | RFC-0301 |
| Service | A modular system component registered with the Service Registry, satisfying a specific abstract Service Contract. | RFC-0003 |
| Provider | Infrastructure adapters implementing hardware, operating system, or external API interfaces (e.g., storage drivers). | RFC-0003 |
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | RFC-0201 |
| Capability | A feature declaration (e.g., Vision, OCR, GPU) verified and exposed by the Runtime Manifest. | RFC-0012 |
| Context | A transaction state container holding variables and metrics passed between executing tasks. | RFC-0307 |
| Knowledge Pack | Database collections containing prompt templates, reference documents, search indices, and context configurations. | RFC-0601 |
| Scheduler | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | RFC-0312 |
| Event Bus | The asynchronous message broker that routes events based on channel names and priority queues. | RFC-0005 |
| State Store | The transaction-isolated database containing current configurations and runtime variables. | RFC-0006 |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | RFC-0002 |
| Watchdog | The monitoring service checking heartbeats of registered services to initiate recovery routines. | RFC-0002 |
| Dead Letter Queue (DLQ) | A dedicated message queue containing events that could not be delivered to their target subscribers. | RFC-1001 |
| Write-Ahead Log (WAL) | A persistent log recording mutations before committing them to the main state database. | RFC-0006 |
| Sandbox | An isolated execution process or virtual machine context restricting OS access. | RFC-0208 |
| Execution | The process of evaluating a workflow graph and activating nodes to produce results. | RFC-0303 |
| Run | A single invocation of a workflow definition producing a workflow instance. | RFC-0301 |
| Task | An atomic unit of work within a workflow, represented as a node. | RFC-0301 |
| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |
| Frame | A discrete unit of visual data processed by vision nodes. | RFC-0301 |
| Tick | A single evaluation cycle of the workflow scheduler. | RFC-0301 |
| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |
| Condition | A boolean expression evaluated to determine execution flow between nodes. | RFC-0310 |
| Manifest | The declarative definition of a component, including its metadata, dependencies, capabilities, and configuration. | RFC-0202 |
| Contract | A formal agreement defining the interface between two components, specifying required behaviors and guarantees. | RFC-0013 |
| Event | A discrete occurrence within the system that may trigger state changes or notifications. | RFC-1001 |
| State | The persistent snapshot of a system component at a point in time, including all configurable and runtime variables. | RFC-1002 |
| Error | A condition indicating that an operation could not be completed as specified. | RFC-1006 |
| Channel | A bidirectional or unidirectional communication pathway between two endpoints. | RFC-0105 |
| Transport | The underlying mechanism by which messages are serialized and delivered between processes. | RFC-0103 |
| Registry | A centralized directory of available services, capabilities, and their current status. | RFC-0205 |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | RFC-0214 |
| Checkpoint | A durable snapshot of state used for recovery, containing all data necessary to resume execution. | RFC-0315 |
| Recovery | The process of restoring a system or workflow from a checkpoint after a failure. | RFC-0315 |
| Orchestration | The coordination of multiple workflow executions to achieve a higher-level goal. | RFC-0301 |
| Sub-Graph | A contained workflow graph nested within a parent workflow for modularity. | RFC-0301 |
| Parallelism Strategy | The approach to concurrent node execution (fan-out, fan-in, pipeline). | RFC-0313 |
| Error Category | A classification of execution errors (Transient, Permanent, Recoverable, Fatal). | RFC-0314 |
| Recovery Strategy | The approach to handling failures (Restart, Resume, Rollback, Compensate, Skip, Abort). | RFC-0315 |
| Validation Rule | A constraint checked during manifest validation. | RFC-0317 |
| Compliance Category | A classification of regulatory or policy requirements applied to system operation. | RFC-0330 |
| IPC | Inter-Process Communication; the unified messaging fabric enabling cross-process data exchange. | RFC-0101 |
| Serialization | The process of converting structured data into a transmittable byte stream and vice versa. | RFC-0106 |
| Routing | The process of determining the destination of a message based on its address and the current channel configuration. | RFC-0104 |
| Backpressure | A mechanism by which a receiver signals to a sender that transmission rate must be reduced. | RFC-0108 |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | RFC-0102 |
| Capability Discovery | The process by which components announce and enumerate their available capabilities at runtime. | RFC-0425 |
| Storage Domain | A logical partition of storage resources with independent lifecycle and policy. | RFC-0421 |
| Storage Namespace | A hierarchical addressing scheme for storage entities within a domain. | RFC-0422 |
| Knowledge Base | A collection of indexed documents, embeddings, and metadata supporting semantic search. | RFC-0601 |
| Vector Index | An optimized data structure for similarity search over embedding vectors. | RFC-0602 |
| Marketplace | A registry and distribution system for plugins, knowledge packs, and other distributable assets. | RFC-0501 |
| Package | A versioned, signed, distributable bundle of assets (plugins, knowledge packs, schemas). | RFC-0502 |
| Hook | A callback registered at an extension point, invoked at a defined moment in the lifecycle. | RFC-0214 |
| Telemetry | Observability data including metrics, traces, and logs emitted by system components. | RFC-0229 |
| Diagnostic | Runtime inspection data used to troubleshoot failures and performance issues. | RFC-0230 |
| Hot Reload | The ability to update a plugin or configuration without restarting the hosting process. | RFC-0225 |
| 
---

*This document is part of the Atlas Specification hierarchy. For governance, see [RFC_GOVERNANCE.md](RFC_GOVERNANCE.md). For principles, see [SPECIFICATION_PRINCIPLES.md](SPECIFICATION_PRINCIPLES.md). For domain ownership, see [DOMAIN_OWNERS.md](DOMAIN_OWNERS.md). For change processes, see [SPECIFICATION_CHANGE_PROCESS.md](SPECIFICATION_CHANGE_PROCESS.md).

| Migration | The process of transforming state or configuration from one schema version to another. | RFC-0408 |




