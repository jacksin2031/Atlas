RFC: RFC-0309

Title: Workflow Actions

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

Layer: Standard

Normative: YES

Audience: All Subsystem Teams

ADR References:

  - ADR-0012

Constitution References:

  - Section 1 (Workflow Philosophy)

Related RFCs:

  - RFC-0307 Workflow Context

  - RFC-0308 Workflow Events


  - RFC-0310 Workflow Conditions

  - RFC-0311 Workflow Triggers

  - RFC-0312 Workflow Scheduler

  - RFC-0313 Workflow Parallelism

  - RFC-0314 Workflow Error Handling

  - RFC-0315 Workflow Recovery

  - RFC-0316 Workflow Debugging

  - RFC-0317 Workflow Validation

  - RFC-0318 Workflow Versioning

  - RFC-0319 Workflow Security

  - RFC-0320 Workflow Performance

  - RFC-0321 Workflow Observability

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

  - RFC-0325 Workflow AI

  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC

  - RFC-0328 Workflow Serialization

  - RFC-0329 Workflow Compatibility

  - RFC-0330 Workflow Compliance

Related ADR: ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema: specs/workflow/json-schema/workflow-action-types.md

Related Catalog: specs/workflow/catalog/workflow-actions.md

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x

Last Updated: 2026-07-01

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Actions specification defines the action model for Atlas workflows. Actions are operations performed by nodes during execution. Actions MAY have side effects and MAY produce results.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0309 workflow actions.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 1 Terminology



The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.



| Term | Definition |

|---|---|

| Action | An atomic unit of work declared within a Workflow Node. An action declares its inputs, outputs, side effects, and idempotency properties. Actions are the fundamental executable primitive of the workflow graph. |

| Action Type | A named category of action (e.g., Invoke, Transform, Validate) that determines the action type execution semantics, idempotency guarantee, and available parameters. |

| Action Declaration | The complete set of metadata fields (id, type, inputs, outputs, parameters, timeout, retry_policy, error_handler, idempotent) that describe an action to the Workflow Runtime. |

| Action Chaining | The practice of connecting multiple actions within a single node so that each action receives the outputs of the previous action. Chain execution is atomic. |



| Compensation Action | An action declared to reverse the side effects of a non-idempotent action. Compensation actions MUST be semantically inverse to their paired action. |

| Execution Budget | The maximum computational resources (time, memory, iterations) allocated to a single action or action chain. Defined in RFC-0303. |

| Workflow Runtime | The runtime system responsible for loading, validating, scheduling, executing, and observing workflow instances. Referenced in RFC-0304. |



---



## 2 Layer Boundaries



### 2.1 Responsibilities



The Workflow Actions specification defines:



- The taxonomy of action types and their semantic guarantees.

- The action declaration schema (fields, types, constraints).

- The action execution lifecycle (validate, acquire, execute, emit, release, complete).

- Idempotency and compensation contracts.

- Action chaining rules and atomicity guarantees.

- The mapping between action types and Capability invocations.



### 2.2 Non-Responsibilities



The following are explicitly OUT OF SCOPE for this specification:



- Workflow Runtime scheduling decisions (RFC-0304, RFC-0312).

- Condition evaluation logic (RFC-0310).

- Trigger firing mechanisms (RFC-0311).

- Error handling and retry policies at the workflow level (RFC-0314).

- Recovery and checkpoint semantics (RFC-0315).

- Debugging and inspection interfaces (RFC-0316).

- Capability registration and discovery (RFC-0322).

- Storage backends and persistence mechanisms (RFC-0324).



### 2.3 Dependencies



| Dependency | Direction | Nature |

|---|---|---|

| RFC-0301 Workflow Overview | Consumes | Terminology, philosophy |

| RFC-0303 Workflow Execution | Consumes | Execution phases, budgets |

| RFC-0304 Workflow Runtime | Consumes | Runtime contract, node lifecycle |

| RFC-0307 Workflow Context | Consumes | Variable resolution, context propagation |

| RFC-0308 Workflow Events | Consumes | Event emission model |

| RFC-0310 Workflow Conditions | Consumes | Condition evaluation for gating |

| RFC-0314 Workflow Error Handling | Consumes | Error taxonomy, retry policies |

| RFC-0322 Workflow Extension | Provides | Extension point for custom action types |

| RFC-1003 Common Capability Model | Consumes | Capability invocation contract |



### 2.4 Consumers



- Workflow Runtime (RFC-0304): Loads and executes action declarations.

- Workflow Debugger (RFC-0316): Inspects action inputs, outputs, and side effects.

- Workflow Validator (RFC-0317): Validates action declarations against schema.

- Plugin System (RFC-0322): Registers custom action type handlers.



### 2.5 Providers



- Workflow Runtime (RFC-0304): Provides execution context, variable resolution, event bus.

- Capability Registry (RFC-1003): Provides capability lookup and invocation primitives.

- Event Bus (RFC-1001): Provides event emission infrastructure.



### 2.6 Forbidden Dependencies



Action handlers MUST NOT depend on:



- Any specific programming language runtime (a systems programming language, Node.js, a desktop application framework, a desktop application framework).

- Any specific database engine (an embedded database engine, a relational database, etc.).

- Any browser API or DOM interface.

- Any operating system call or process model.

- Any GPU compute interface.

- Any threading or concurrency model (sequential execution is sufficient for correctness).



---



## 3 Action Model Overview



Actions are the fundamental unit of work within a workflow node. Each action declares its inputs, outputs, side effects, and idempotency properties.



---



## 4 Action Types



| Action Type | Description | Idempotent |

|---|---|---|

| Invoke | Invokes a capability or service | No |

| Transform | Transforms data | Yes |

| Validate | Validates data or state | Yes |

| Emit | Emits an event | Yes |

| Wait | Waits for a condition or event | Yes |

| Approve | Requests human approval | No |

| Reject | Requests human rejection | No |

| Compensate | Performs compensation | No |

| Notify | Sends a notification | Yes |

| Store | Stores data | No |

| Retrieve | Retrieves data | Yes |

| Delete | Deletes data | No |

| Query | Queries data | Yes |

| Schedule | Schedules a future action | No |

| Cancel | Cancels a pending action | No |

| Resume | Resumes a paused action | No |

| Pause | Pauses an active action | No |



---



## 5 Action Declaration



### 5.1 Action Fields



| Field | Type | Required | Description |

|---|---|---|---|

| id | String | YES | Unique action identifier |

| type | String | YES | Action type |

| inputs | Variable List | YES | Input variables |

| outputs | Variable List | NO | Output variables |

| parameters | Parameter Map | NO | Action parameters |

| timeout | Duration | NO | Maximum action duration |

| retry_policy | Retry Policy | NO | Retry configuration |

| error_handler | Error Handler | NO | Custom error handler |

| idempotent | Boolean | NO | Whether action is idempotent |



### 5.2 Action Constraints



- Actions MUST declare their inputs and outputs.

- Actions MUST declare their idempotency property.

- Actions MUST declare their timeout.

- Actions MUST declare their retry policy.



---



## 6 Action Execution



### 6.1 Execution Steps



1. Validate action inputs.

2. Acquire required resources.

3. Execute the action.

4. Emit output variables.

5. Release resources.

6. Emit completion event.



### 6.2 Execution Failure



On failure:



1. Emit failure event.

2. Invoke error handler (if any).

3. Apply retry policy (if applicable).

4. Execute compensation (if required).



---



## 7 Action Idempotency



### 7.1 Idempotency Requirements



- Idempotent actions MUST produce the same result when re-executed.

- Non-idempotent actions MUST declare compensation actions.

- Compensation actions MUST reverse the effect of the original action.



---



## 8 Action Chaining



### 8.1 Chaining Rules



Actions MAY be chained within a node:



1. Each action receives the outputs of the previous action.

2. Chain execution is atomic: all actions succeed or all fail.

3. Chain depth is bounded by the execution budget.



---



## 9 Security



### 9.1 Action-Level Security Controls



| Control | Requirement | Enforcement Point |

|---|---|---|

| Input Validation | All action inputs MUST be validated against declared schema before execution. | Pre-execution |

| Capability Permissions | Invoke actions MUST check capability permissions before invocation. | Pre-execution |

| Side Effect Isolation | Actions with side effects MUST declare their side effect scope. | Declaration |

| Compensation Auditing | Compensation actions MUST be logged with before/after state snapshots. | Post-execution |

| Timeout Enforcement | Action timeouts MUST be enforced by the Workflow Runtime. | Runtime |

| Idempotency Key | Non-idempotent actions MUST generate or accept an idempotency key. | Runtime |

| Secret Handling | Action parameters containing secrets MUST be encrypted at rest and in transit. | Runtime |

| Audit Logging | All action executions (success, failure, compensation) MUST emit audit events. | Post-execution |



### 9.2 Forbidden Patterns



Action handlers MUST NOT:



- Read or write arbitrary filesystem paths without explicit declaration.

- Make outbound network calls unless the action type is Notify or Emit.

- Access secrets or credentials not declared in the action parameters.

- Modify global state outside the action-scoped variable namespace.



---



## 10 Performance



### 10.1 Performance Requirements



| Metric | Requirement | Measurement |

|---|---|---|

| Action Latency | Individual action execution MUST complete within declared timeout. | Per-action timer |

| Chain Overhead | Action chaining adds at most 1ms of overhead per hop. | Benchmark |

| Idempotency Lookup | Idempotency key lookup MUST complete within 10ms. | Cache lookup test |

| Memory Footprint | Action execution context MUST not exceed 64 KiB per action. | Profiling |

| Parallel Dispatch | The runtime MUST dispatch independent actions in parallel without serialization. | Concurrency test |

| Compilation Time | Action schema compilation MUST complete within 100ms for 1000 actions. | Schema benchmark |



### 10.2 Optimization Guidelines



- Idempotent actions SHOULD be cached by the runtime to avoid redundant computation.

- Actions with no side effects SHOULD be eligible for speculative execution.

- Action chains SHOULD be minimized; flat action declarations are preferred when possible.



---



## 11 Compatibility



### 11.1 Compatibility Levels



| Level | Description | Enforcement |

|---|---|---|

| Full | Fully compatible across all versions | No enforcement needed |

| Backward | Compatible with previous version | Validation warning |

| Forward | Compatible with next version | Validation warning |

| Conditional | Compatible under specific conditions | Runtime check |

| Incompatible | Not compatible | Validation error |



### 11.2 Action Type Compatibility



- New action types MAY be added without breaking existing workflows.

- Action fields MAY be added as optional without breaking existing workflows.

- Action fields MUST NOT be removed or made required without a deprecation cycle.

- Action type semantics MUST NOT change between minor versions.



---



## 12 Compliance



### 12.1 Compliance Categories



| Category | Requirement | Enforcement |

|---|---|---|

| Operational | Actions MUST declare timeout and retry policy. | Pre-execution |

| Security | Actions MUST enforce input validation and permission checks. | Continuous |

| Audit | All action executions MUST produce audit trail entries. | Post-execution |

| Data Privacy | Actions handling PII MUST declare data classification. | Declaration |

| Idempotency | Non-idempotent actions MUST declare compensation. | Validation |

| Determinism | Identical action inputs MUST produce identical outputs for idempotent actions. | Runtime |



---



## 13 Future Evolution



### 13.1 Planned Extensions



| Feature | Status | RFC |

|---|---|---|

| Streaming actions (progressive output) | Proposed | RFC-0325 |

| Async action callbacks | Proposed | RFC-0322 |

| Action-level ML inference | Proposed | RFC-0325 |

| Action composition DSL | Proposed | RFC-0302 |

| Action cost estimation | Proposed | RFC-0320 |



### 13.2 Deprecation Policy



- Deprecated action types MUST remain functional for at least two major versions.

- Migration guides MUST be provided for all deprecated action types.

- New workflows MUST NOT use deprecated action types.



---



## 14 Runtime Independence



This specification is intentionally runtime-independent. It makes no assumptions about:



- Programming language: Action handlers MAY be implemented in any language.

- Runtime environment: Actions MAY execute in-process, out-of-process, or remotely.

- Process model: No assumption of threads, goroutines, or async/await.

- Database: No assumption of an embedded database engine, relational, or document stores.

- Browser: No assumption of DOM, Web APIs, or rendering.

- Operating system: No assumption of POSIX, Windows, or any OS-specific API.

- Hardware: No assumption of GPU, TPU, or specialized accelerators.

- Serialization format: Actions MAY use JSON, MessagePack, or any agreed format.



---



## 15 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | The implementation MUST support seventeen (17) distinct action types as enumerated in Section 4. | Type enumeration test |

| AC-02 | The implementation MUST define eight (8) action declaration fields as enumerated in Section 5.1. | Field enumeration test |

| AC-03 | The implementation MUST enforce six (6) action execution steps as enumerated in Section 6.1. | Execution test |

| AC-04 | The implementation MUST enforce three (3) action chaining rules as enumerated in Section 8.1. | Chaining test |

| AC-05 | The implementation MUST enforce idempotency guarantees: idempotent actions MUST produce identical results on re-execution. | Idempotency test |

| AC-06 | The implementation MUST require compensation action declarations for all non-idempotent actions. | Validation test |

| AC-07 | The implementation MUST enforce all eight (8) security controls defined in Section 9.1. | Security audit |

| AC-08 | The implementation MUST measure all six (6) performance metrics defined in Section 10.1. | Performance benchmark |

| AC-09 | The implementation MUST enforce five (5) compatibility levels defined in Section 11.1. | Compatibility test |

| AC-10 | The implementation MUST enforce six (6) compliance categories defined in Section 12.1. | Compliance test |



---



## 16 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (terminology, philosophy) |

| RFC-0303 | Workflow Execution (execution phases, budgets) |

| RFC-0304 | Workflow Runtime (runtime contract, node lifecycle) |

| RFC-0307 | Workflow Context (variable resolution, context propagation) |

| RFC-0308 | Workflow Events (event emission model) |

| RFC-0310 | Workflow Conditions (condition evaluation for gating) |

| RFC-0314 | Workflow Error Handling (error taxonomy, retry policies) |

| RFC-0315 | Workflow Recovery (compensation semantics) |

| RFC-0316 | Workflow Debugging (action inspection interfaces) |

| RFC-0317 | Workflow Validation (action schema validation) |

| RFC-0322 | Workflow Extension (custom action type registration) |

| RFC-0324 | Workflow Storage (persistence mechanisms) |

| RFC-1003 | Common Capability Model (capability invocation contract) |

| ADR-0012 | Contract-First Specification-Driven Development |

| JSON Schema | specs/workflow/json-schema/workflow-action-types.md |

| Catalog | specs/workflow/catalog/workflow-actions.md |

| Glossary | Atlas Master Glossary (RFC-0301) |

| Constitution | Atlas AI Constitution, Section 1 (Workflow Philosophy) |

---



## Terminology



| Term | Definition | Source |

|---|---|---|

| Node | A graph element representing an atomic unit of work with defined inputs and outputs. | RFC-0301 |

| Action | An operation performed by a workflow node. | RFC-0309 |

| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 | RFC-0310 |

| Trigger | An event or condition that initiates workflow execution. | RFC-0311 |

| Scheduler | The component that determines WHEN and WHERE each node is executed. | RFC-0312 |

| Context | The scoped data environment available to nodes during execution. | RFC-0307 |



## Layer Boundaries



### Responsibilities

This specification IS responsible for: defining the action type model and node execution semantics.



### Non-Responsibilities

This specification IS NOT responsible for: executing nodes (delegated to RFC-0303), managing the runtime (delegated to RFC-0304), or scheduling decisions (delegated to RFC-0312, except for RFC-0312 itself).



### Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0303 | Consumed | Workflow Execution consumes actions |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0307 | Consumed | Workflow Context provides context data |

| RFC-0317 | Consumed | Workflow Validation validates action declarations |

| RFC-0319 | Consumed | Workflow Security provides action sandboxing |

| RFC-0320 | Consumed | Workflow Performance provides action performance |



### Consumers

- Workflow Execution (RFC-0303): Consumes action definitions for execution.



### Providers

- Actions Catalog (catalog/workflow-actions.md)

- 

- 

- 



### Forbidden Dependencies

- This specification MUST NOT depend on any platform-specific implementation.



## Security

- Actions MUST operate within sandbox boundaries per RFC-0319.

- 

- 

- 



## Performance

- Action execution MUST complete within the node's performance budget.

- 

- 

- 



## Compatibility

- Action type definitions MUST be backward compatible within a major version.

- 

- 

- 



## Compliance

- All actions MUST comply with organizational policies per RFC-0330.



## Future Evolution

- AI-driven action selection based on historical performance data.

- 

- 

- 



## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)

- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)

- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)

- Any operating system (Windows, Linux, macOS, etc.)

- Any hardware architecture (CPU, GPU, FPGA, etc.)

- Any threading model (single-threaded, multi-threaded, actor-based, etc.)




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


## References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (canonical terminology source) |

| RFC-0303 | Workflow Execution (action consumption) |

| RFC-0304 | Workflow Runtime (execution context) |

| RFC-0307 | Workflow Context (context data) |

| RFC-0312 | Workflow Scheduler (scheduling) |

| RFC-0314 | Workflow Error Handling (error propagation) |

| RFC-0315 | Workflow Recovery (recovery) |

| RFC-0317 | Workflow Validation (validation) |

| RFC-0319 | Workflow Security (security) |

| RFC-0320 | Workflow Performance (performance) |

| RFC-0321 | Workflow Observability (telemetry) |

| RFC-0322 | Workflow Extension (extension) |

| RFC-0329 | Workflow Compatibility (compatibility) |

| RFC-0330 | Workflow Compliance (compliance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/actions | Action JSON Schema |

| catalog/workflow-actions | Action Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0309 (this document), RFC-0301 (Overview), RFC-0303 (Execution) |






