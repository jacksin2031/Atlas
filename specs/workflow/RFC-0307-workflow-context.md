RFC: RFC-0307
Title: Workflow Context
Status: Proposed
Version: 1.1.0
Author:
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Context | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Scope | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Variable | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Mutation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Inheritance | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Propagation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Isolation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Snapshot | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Context Merge | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
 Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0308 Workflow Events
  - RFC-0312 Workflow Scheduler
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1004 Common Contract Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012 (Contract-First Specification-Driven Development)
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0308 Workflow Events
  - RFC-0309 Workflow Actions
  - RFC-0312 Workflow Scheduler
  - RFC-0313 Workflow Parallelism
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0317 Workflow Validation
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Related ADR: ADR-0012
Related JSON Schema: contracts/json/workflow.schema.json
Related Catalog: specs/workflow/catalog/workflow-context.md

---

## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Context specification defines the execution context model for Atlas workflows. The context is the state container that holds all data relevant to a single workflow execution instance, including variables, parameters, resources, and metadata.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0307 workflow context.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined authoritatively in the [Atlas Master Glossary](../glossary.md) and MUST be interpreted consistently across all implementations:

| Term | Definition | Source |
|---|---|---|
| **Workflow** | A directed acyclic graph (DAG) defining a series of automation steps, inputs, outputs, and dependencies. | Glossary |
| **Workflow Instance** | A single execution of a workflow definition with concrete parameter bindings and runtime state. | RFC-0301 |
| **Context** | A transaction state container holding variables and metrics passed between executing tasks. | Glossary |
| **Variable** | A named data holder within the execution context, with a type and optional default value. | RFC-0301 |
| **Parameter** | A named input to a workflow or node, bound at creation or initialization time. | RFC-0301 |
| **Node** | An atomic unit of work within a workflow DAG, representing a single action or group of actions. | RFC-0301 |
| **Edge** | A directed connection between nodes carrying data flow, control flow, or dependency relationships. | RFC-0301 |
| **State Store** | The transaction-isolated database containing current configurations and runtime variables. | Glossary |
| **Scheduler** | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | Glossary |
| **Runtime** | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | Glossary |

### 1.1 Normative Language

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2 Layer Boundaries

### 2.1 Responsibilities

The Workflow Context layer is responsible for:

- Defining the hierarchical context model for workflow execution.
- Specifying variable and parameter lifecycle management.
- Defining context inheritance rules between parent and child scopes.
- Managing resource tracking within the context.
- Providing the security context and observability context.

### 2.2 Non-Responsibilities

The Workflow Context layer MUST NOT:

- Define variable type systems (deferred to RFC-0302).
- Define parameter binding mechanisms (deferred to RFC-0317).
- Manage context persistence (deferred to RFC-0306).
- Define context serialization formats (deferred to RFC-0328).
- Implement context garbage collection.

### 2.3 Dependencies

| Dependency | Direction | Rationale |
|---|---|---|
| RFC-0301 Workflow Overview | Consumes | Provides the overarching graph model |
| RFC-0304 Workflow Runtime | Consumes | Runtime provides the execution fabric |
| RFC-0305 Workflow Lifecycle | Consumes | Lifecycle defines context creation triggers |
| RFC-0306 Workflow State | Consumes | State model provides persistence |
| RFC-0308 Workflow Events | Consumes | Events provide context change notifications |
| RFC-0312 Workflow Scheduler | Consumes | Scheduler provides resource allocation |
| RFC-0309 Workflow Actions | Consumes | Actions consume context variables |
| RFC-0317 Workflow Validation | Consumes | Validation requires context inspection |

### 2.4 Consumers

- RFC-0304 Workflow Runtime (context access during execution)
- RFC-0309 Workflow Actions (variable consumption)
- RFC-0310 Workflow Conditions (condition evaluation)
- RFC-0313 Workflow Parallelism (concurrent context access)
- RFC-0316 Workflow Debugging (context inspection)
- RFC-0321 Workflow Observability (context metrics)

### 2.5 Providers

- RFC-0301 Workflow Overview (graph model)
- RFC-0306 Workflow State (state persistence)
- RFC-1002 Common State Model (base types)

### 2.6 Forbidden Dependencies

The Workflow Context layer MUST NOT depend on:

- Any runtime implementation technology (a systems programming language, Node.js, a desktop application framework, a desktop application framework).
- Any specific storage engine (an embedded database engine, a relational database, an in-memory data store, filesystem).
- Any operating system primitives (threads, processes, signals).
- Any GPU or hardware acceleration model.
- Any browser or presentation-layer technology.

---

## 3 Context Model Overview

The execution context is a hierarchical state container that encompasses:

- Variables and their current values
- Parameters bound to nodes
- Resource allocations
- Event subscriptions
- Error handlers
- Timing information
- Security context
- Observability hooks

### 3.1 Context Properties

Every context object MUST have:

- A unique identifier scoped to its workflow instance.
- A creation timestamp.
- A scope level (workflow, node, sub-graph, edge).
- A parent context reference (nullable for root context).
- A status indicator reflecting the current execution phase.

---

## 4 Context Structure

### 4.1 Context Hierarchy

Context is organized hierarchically:

| Level | Scope | Contents |
|---|---|---|
| Workflow | Entire execution | Variables, parameters, resources |
| Node | Single node execution | Node-specific variables |
| Sub-Graph | Sub-workflow execution | Sub-graph variables |
| Edge | Data transfer | Edge transformation state |

### 4.2 Context Inheritance

Child contexts inherit from parent contexts:

- Child contexts CAN read parent variables.
- Child contexts CAN write to parent variables (with permission).
- Child contexts CAN declare new variables scoped to the child.
- Variable shadowing is allowed: child declarations with the same name as parent variables MUST NOT affect parent values.

---

## 5 Variable Management

### 5.1 Variable Lifecycle

Variables follow this lifecycle:

1. **Declaration**: Variable is declared with a type and optional default.
2. **Binding**: Variable is bound to a concrete value.
3. **Resolution**: Variable value is resolved during execution.
4. **Update**: Variable value is updated during execution.
5. **Propagation**: Variable value is propagated along edges.
6. **Destruction**: Variable is destroyed when context is destroyed.

### 5.2 Variable Types

Supported variable types are defined in RFC-0302 Section 6.3. Every variable MUST declare its type explicitly.

---

## 6 Parameter Management

### 6.1 Parameter Lifecycle

Parameters follow this lifecycle:

1. **Declaration**: Parameter is declared with a type and optional default.
2. **Binding**: Parameter is bound at workflow or node initialization.
3. **Override**: Parameter value MAY be overridden at execution time.
4. **Resolution**: Parameter value is resolved for each node execution.

### 6.2 Parameter Constraints

- Required parameters MUST be bound before workflow initialization completes.
- Default values MUST be compatible with the declared parameter type.
- Parameter overrides MUST be validated against the parameter schema.

---

## 7 Resource Management in Context

### 7.1 Resource Tracking

Resources are tracked within the context:

| Resource | Tracking Method | Release Trigger |
|---|---|---|
| Memory | Allocation counter | Node completion |
| CPU | Scheduler allocation | Node completion |
| Storage | Namespace binding | Workflow termination |

### 7.2 Resource Lifecycle

- Resources are acquired during initialization and released during termination.
- Resource leaks MUST be detected by the watchdog as defined in RFC-0320.
- Resource allocation MUST be logged for audit purposes.

---

## 8 Security Context

### 8.1 Security Attributes

The security context includes:

- Initiator identity
- Permission grants
- Sandbox boundaries
- Data classification

### 8.2 Security Enforcement

Security is enforced at every context access:

- Read access requires READ permission.
- Write access requires WRITE permission.
- Resource access requires RESOURCE permission.

### 8.3 Isolation

- Context data MUST be isolated between workflow instances.
- Cross-instance context access MUST require explicit authorization.
- Sensitive context data MUST be encrypted at rest.

---

## 9 Observability Context

### 9.1 Observability Data

The context collects:

- Execution timing data
- Resource utilization data
- Event emission data
- Error occurrence data

### 9.2 Observability Hooks

- Observability hooks MUST be registered during initialization.
- Hook invocations MUST NOT block workflow execution.
- Hook failures MUST be logged but MUST NOT cause workflow failure.

---

## 10 Security

### 10.1 Context Security Controls

- Context data at rest MUST be encrypted using the platform encryption policy.
- Context access MUST follow the principle of least privilege.
- Security context attributes MUST be immutable once set.
- Sandbox boundaries MUST be enforced at every context access.

### 10.2 Audit Trail

All context modifications MUST be recorded in an immutable audit log with: timestamp, actor, context level, operation, and correlation ID.

---

## 11 Performance

### 11.1 Context Performance Requirements

- Context variable lookups MUST complete within 1ms.
- Context creation MUST complete within 10ms for standard workflows.
- Context inheritance resolution MUST complete within 5ms.
- Context serialization for checkpointing MUST complete within 20ms per 100 variables.

### 11.2 Resource Constraints

- Context memory usage MUST NOT exceed 5MB per workflow instance.
- The context tree depth MUST be bounded to prevent stack overflow.
- Concurrent context access MUST NOT cause contention beyond 5% throughput degradation.

---

## 12 Compatibility

### 12.1 Context Format Compatibility

- Context serialization formats MUST be versioned and MUST include a compatibility header.
- Older context formats MUST be readable by newer implementations.
- New context fields MUST be optional and MUST have default values.

### 12.2 Cross-Version Operations

- Context variable types defined in older versions MUST remain valid in newer versions.
- Context migration tools MUST be provided when breaking changes are introduced.

---

## 13 Compliance

### 13.1 Regulatory Compliance

- Context audit trails MUST satisfy SOX Section 404 requirements for operational process logging.
- Context data retention MUST comply with the platform data retention policy.
- Sensitive context data classification MUST follow the platform data classification policy.

### 13.2 Internal Policy Compliance

- All context modifications MUST be consistent with the Atlas Constitution Section 1 (Workflow Philosophy).
- Context access MUST follow the principle of least privilege.

---

## 14 Future Evolution

### 14.1 Planned Extensions

- Dynamic context scaling (auto-expanding context trees) is planned for future versions.
- Context sharing across workflow instances (cross-instance collaboration) is under consideration.
- Machine learning-based context optimization (predictive variable caching) is exploratory.

### 14.2 Stability Guarantee

The context model defined in this RFC is stable and MUST NOT change without a formal RFC revision cycle.

---

## 15 Runtime Independence

This specification makes NO assumptions about:

- **Implementation language**: No a systems programming language, Node.js, Python, Go, or any other language is required.
- **Runtime environment**: No a desktop application framework, a desktop application framework, browser, or desktop framework dependency.
- **Storage technology**: No an embedded database engine, a relational database, an in-memory data store, or any specific database is mandated.
- **Operating system**: No thread model, process model, signal handling, or OS-specific primitive is assumed.
- **Hardware**: No GPU, VRAM, CPU affinity, or hardware acceleration is required.
- **Network topology**: No specific network protocol or topology is assumed.

The context model is purely logical and data-structure based. Any implementation MAY use any technology stack to realize this specification.

---

## 16 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|

---

## 17 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (graph model, philosophy) |
| RFC-0302 | Workflow Language (variable types) |
| RFC-0304 | Workflow Runtime (execution fabric) |
| RFC-0305 | Workflow Lifecycle (context creation triggers) |
| RFC-0306 | Workflow State (state persistence) |
| RFC-0308 | Workflow Events (context change notifications) |
| RFC-0309 | Workflow Actions (variable consumption) |
| RFC-0310 | Workflow Conditions (condition evaluation) |
| RFC-0312 | Workflow Scheduler (resource allocation) |
| RFC-0313 | Workflow Parallelism (concurrent access) |
| RFC-0314 | Workflow Error Handling (error context) |
| RFC-0315 | Workflow Recovery (checkpoint context) |
| RFC-0316 | Workflow Debugging (context inspection) |
| RFC-0317 | Workflow Validation (parameter binding) |
| RFC-0319 | Workflow Security (security controls) |
| RFC-0320 | Workflow Performance (performance metrics) |
| RFC-0321 | Workflow Observability (context metrics) |
| RFC-0328 | Workflow Serialization (context formats) |
| RFC-0329 | Workflow Compatibility (version compatibility) |
| RFC-0330 | Workflow Compliance (regulatory compliance) |
| RFC-1002 | Common State Model (base types) |
| ADR-0012 | Contract-First Specification-Driven Development |
| JSON Schema | contracts/json/workflow.schema.json |
| Catalog | specs/workflow/catalog/workflow-context.md |
| Glossary | specs/glossary.md (Atlas Master Glossary) |


---

## Revision History

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
