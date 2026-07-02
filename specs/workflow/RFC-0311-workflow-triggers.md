RFC: RFC-0311

Title: Workflow Triggers

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

  - RFC-0309 Workflow Actions

  - RFC-0310 Workflow Conditions


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

Related JSON Schema: specs/workflow/json-schema/workflow-trigger-types.md

Related Catalog: specs/workflow/catalog/workflow-triggers.md

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x

Last Updated: 2026-07-01

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Triggers specification defines the trigger model for initiating workflow execution. Triggers are external events or conditions that cause a workflow instance to be created and begin execution.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0311 workflow triggers.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 1 Terminology



The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below.



| Term | Definition |

|---|---|

| Trigger | An external event or condition that initiates the creation and execution of a workflow instance. Triggers define WHAT initiates a workflow, WHEN it initiates, and WITH WHAT parameters. |

| Trigger Type | A named category of trigger (e.g., Manual, Scheduled, Event-based) that determines execution initiation. | RFC-0311 |

| Trigger Configuration | The complete set of metadata fields (id, type, workflow_id, parameters, conditions, schedule, event_filter, enabled) that describe a trigger to the Workflow Runtime. |

| Trigger Firing | The process of evaluating a trigger condition, resolving parameters, creating a workflow instance, and beginning execution. |

| Trigger Chaining | The practice of linking multiple triggers across workflows so that the completion of one workflow activates a trigger in another. |

| Trigger Rate Limiting | The restriction on how frequently a trigger may fire, expressed as maximum firings per time window or maximum concurrent instances. |

| Event Filter | A condition expression that selects which events from the event bus activate an event-based trigger. |

| Workflow Runtime | The runtime system responsible for loading, validating, scheduling, executing, and observing workflow instances. Referenced in RFC-0304. |



---



## 2 Layer Boundaries



### 2.1 Responsibilities



The Workflow Triggers specification defines:



- The taxonomy of trigger types and their activation semantics.

- The trigger declaration schema (fields, types, constraints).

- The trigger firing lifecycle (evaluate, resolve, create, begin, emit).

- Trigger chaining rules and acyclicity guarantees.

- Trigger rate limiting policies.

- The mapping between trigger sources and the Workflow Runtime event bus.



### 2.2 Non-Responsibilities



The following are explicitly OUT OF SCOPE for this specification:



- Workflow Runtime scheduling decisions (RFC-0304, RFC-0312).

- Condition evaluation logic (RFC-0310).

- Action execution within triggered workflows (RFC-0309).

- Error handling and retry policies (RFC-0314).

- Recovery and checkpoint semantics (RFC-0315).

- Debugging and inspection interfaces (RFC-0316).

- External system integration protocols (RFC-0322).



### 2.3 Dependencies



| Dependency | Direction | Nature |

|---|---|---|

| RFC-0301 Workflow Overview | Consumes | Terminology, philosophy |

| RFC-0303 Workflow Execution | Consumes | Execution phases, workflow instance lifecycle |

| RFC-0304 Workflow Runtime | Consumes | Runtime contract, instance creation |

| RFC-0307 Workflow Context | Consumes | Variable resolution, context propagation |

| RFC-0308 Workflow Events | Consumes | Event emission model |

| RFC-0310 Workflow Conditions | Consumes | Condition evaluation for trigger gating |

| RFC-0312 Workflow Scheduler | Consumes | Schedule resolution for scheduled triggers |

| RFC-0314 Workflow Error Handling | Consumes | Error taxonomy, trigger failure handling |

| RFC-1001 Common Event Model | Consumes | Event bus integration |

| RFC-1002 Common State Model | Consumes | Workflow instance state management |



### 2.4 Consumers



- Workflow Runtime (RFC-0304): Creates and begins workflow instances on trigger fire.

- Workflow Debugger (RFC-0316): Inspects trigger configurations and firing history.

- Workflow Validator (RFC-0317): Validates trigger declarations against schema.

- Event Bus (RFC-1001): Receives events that activate event-based triggers.



### 2.5 Providers



- Workflow Runtime (RFC-0304): Provides workflow instance creation and execution services.

- Event Bus (RFC-1001): Provides event delivery infrastructure for event-based triggers.

- Scheduler (RFC-0312): Provides schedule resolution for scheduled triggers.

- Condition Engine (RFC-0310): Provides condition evaluation for trigger gating.



### 2.6 Forbidden Dependencies



Trigger handlers MUST NOT depend on:



- Any specific programming language runtime (a systems programming language, Node.js, a desktop application framework, a desktop application framework).

- Any specific database engine (an embedded database engine, a relational database, etc.).

- Any browser API or DOM interface.

- Any operating system call or process model.

- Any GPU compute interface.

- Any threading or concurrency model (sequential firing is sufficient for correctness).



---



## 3 Trigger Model Overview



Triggers connect external stimuli to workflow execution. A trigger defines WHAT initiates a workflow, WHEN it initiates, and WITH WHAT parameters.



---



## 4 Trigger Types



| Trigger Type | A named category of trigger (e.g., Manual, Scheduled, Event-based) that determines execution initiation. | RFC-0311 | Source |

|---|---|---|

| Manual | Initiated by user action | User interface |

| Scheduled | Initiated at a specific time or interval | Scheduler |

| Event-based | Initiated by an external event | Event bus |

| API | Initiated by an API call | External system |

| Webhook | Initiated by a webhook callback | HTTP endpoint |

| File | Initiated by file system changes | File system watcher |

| Timer | Initiated by a timer expiration | Internal timer |

| Dependency | Initiated by another workflow completion | Parent workflow |

| Resource | Initiated by resource availability | Resource manager |



---



## 5 Trigger Configuration



### 5.1 Trigger Fields



| Field | Type | Required | Description |

|---|---|---|---|

| id | String | YES | Unique trigger identifier |

| type | String | YES | Trigger type |

| workflow_id | String | YES | Target workflow |

| parameters | Parameter Map | NO | Trigger parameters |

| conditions | Condition List | NO | Trigger conditions |

| schedule | Schedule Spec | Conditional | Schedule (for scheduled triggers) |

| event_filter | Event Filter | Conditional | Event filter (for event triggers) |

| enabled | Boolean | NO | Whether trigger is active |



### 5.2 Trigger Constraints



- A trigger MUST reference a valid workflow definition.

- A trigger MUST declare its parameters.

- A trigger MAY declare conditions that must be satisfied before activation.



---



## 6 Trigger Firing



### 6.1 Firing Process



1. Trigger condition is evaluated.

2. Trigger parameters are resolved.

3. Workflow instance is created.

4. Workflow execution begins.

5. Trigger firing event is emitted.



### 6.2 Firing Rate Limiting



Triggers MAY be rate-limited:



| Limit | Description |

|---|---|

| Max per minute | Maximum trigger firings per minute |

| Max per hour | Maximum trigger firings per hour |

| Max concurrent | Maximum concurrent workflow instances |



---



## 7 Trigger Chaining



### 7.1 Chain Rules



Triggers MAY be chained to create dependency-based execution:



1. Trigger A fires workflow X.

2. Workflow X completion triggers Trigger B.

3. Trigger B fires workflow Y.



### 7.2 Chain Constraints



- Trigger chains MUST be acyclic.

- Maximum chain depth is bounded by the execution budget.



---



## 8 Security



### 8.1 Trigger-Level Security Controls



| Control | Requirement | Enforcement Point |

|---|---|---|

| Trigger Authentication | Manual and API triggers MUST authenticate the initiating actor. | Pre-fire |

| Workflow Authorization | Triggers MUST verify the initiating actor has permission to start the target workflow. | Pre-fire |

| Parameter Sanitization | All trigger parameters MUST be sanitized against injection attacks. | Resolution |

| Rate Limit Enforcement | Rate limits MUST be enforced by the Workflow Runtime. | Runtime |

| Chain Cycle Detection | Trigger chains MUST be validated for acyclicity before activation. | Validation |

| Event Filtering | Event-based triggers MUST filter events using declared event filters only. | Runtime |

| Audit Logging | All trigger firings (success, blocked, rate-limited) MUST emit audit events. | Post-fire |

| Secret Handling | Trigger parameters containing secrets MUST be encrypted at rest and in transit. | Runtime |



### 8.2 Forbidden Patterns



Trigger handlers MUST NOT:



- Fire workflows without authentication for Manual or API triggers.

- Bypass rate limits under any condition.

- Create cyclic trigger chains.

- Access secrets or credentials not declared in the trigger parameters.



---



## 9 Performance



### 9.1 Performance Requirements



| Metric | Requirement | Measurement |

|---|---|---|

| Trigger Latency | Time from trigger activation to workflow instance creation MUST be under 100ms. | Per-trigger timer |

| Rate Limit Check | Rate limit evaluation MUST complete within 1ms. | Benchmark |

| Chain Detection | Acyclicity check for trigger chains MUST complete within 10ms. | Graph traversal test |

| Memory Footprint | Trigger execution context MUST not exceed 32 KiB per trigger. | Profiling |

| Concurrent Firing | The runtime MUST handle at least 100 concurrent trigger firings. | Concurrency test |

| Compilation Time | Trigger schema compilation MUST complete within 50ms for 500 triggers. | Schema benchmark |



### 9.2 Optimization Guidelines



- Frequently triggered workflows SHOULD be pre-warmed by the runtime.

- Rate limit counters SHOULD use sliding window algorithms for accuracy.

- Trigger chains SHOULD be validated at declaration time, not at runtime.



---



## 10 Compatibility



### 10.1 Compatibility Levels



| Level | Description | Enforcement |

|---|---|---|

| Full | Fully compatible across all versions | No enforcement needed |

| Backward | Compatible with previous version | Validation warning |

| Forward | Compatible with next version | Validation warning |

| Conditional | Compatible under specific conditions | Runtime check |

| Incompatible | Not compatible | Validation error |



### 10.2 Trigger Type Compatibility



- New trigger types MAY be added without breaking existing workflows.

- Trigger fields MAY be added as optional without breaking existing workflows.

- Trigger fields MUST NOT be removed or made required without a deprecation cycle.

- Trigger type semantics MUST NOT change between minor versions.



---



## 11 Compliance



### 11.1 Compliance Categories



| Category | Requirement | Enforcement |

|---|---|---|

| Operational | Triggers MUST declare target workflow and parameters. | Pre-execution |

| Security | Triggers MUST enforce authentication, authorization, and rate limiting. | Continuous |

| Audit | All trigger firings MUST produce audit trail entries. | Post-execution |

| Data Privacy | Triggers handling PII parameters MUST declare data classification. | Declaration |

| Chain Integrity | Trigger chains MUST be acyclic and validated at declaration. | Validation |

| Determinism | Identical trigger inputs MUST produce identical workflow instances. | Runtime |



---



## 12 Future Evolution



### 12.1 Planned Extensions



| Feature | Status | RFC |

|---|---|---|

| Cross-system trigger federation | Proposed | RFC-0322 |

| Trigger priority queuing | Proposed | RFC-0312 |

| Trigger composition DSL | Proposed | RFC-0302 |

| Trigger performance profiling | Proposed | RFC-0320 |

| Trigger versioning | Proposed | RFC-0318 |



### 12.2 Deprecation Policy



- Deprecated trigger types MUST remain functional for at least two major versions.

- Migration guides MUST be provided for all deprecated trigger types.

- New workflows MUST NOT use deprecated trigger types.



---



## 13 Runtime Independence



This specification is intentionally runtime-independent. It makes no assumptions about:



- Programming language: Trigger handlers MAY be implemented in any language.

- Runtime environment: Triggers MAY fire in-process, out-of-process, or remotely.

- Process model: No assumption of threads, goroutines, or async/await.

- Database: No assumption of an embedded database engine, relational, or document stores.

- Browser: No assumption of DOM, Web APIs, or rendering.

- Operating system: No assumption of POSIX, Windows, or any OS-specific API.

- Hardware: No assumption of GPU, TPU, or specialized accelerators.

- Serialization format: Trigger contexts MAY use JSON, MessagePack, or any agreed format.



---



## 14 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | The implementation MUST support nine (9) distinct trigger types as enumerated in Section 4. | Type enumeration test |

| AC-02 | The implementation MUST define eight (8) trigger configuration fields as enumerated in Section 5.1. | Field enumeration test |

| AC-03 | The implementation MUST enforce five (5) trigger firing steps as enumerated in Section 6.1. | Firing test |

| AC-04 | The implementation MUST support four (4) rate limiting constraints as enumerated in Section 6.2. | Rate limit test |

| AC-05 | The implementation MUST enforce acyclicity for all trigger chains. | Chain validation test |

| AC-06 | The implementation MUST enforce all eight (8) security controls defined in Section 8.1. | Security audit |

| AC-07 | The implementation MUST measure all six (6) performance metrics defined in Section 9.1. | Performance benchmark |

| AC-08 | The implementation MUST enforce five (5) compatibility levels defined in Section 10.1. | Compatibility test |

| AC-09 | The implementation MUST enforce six (6) compliance categories defined in Section 11.1. | Compliance test |



---



## 15 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (terminology, philosophy) |

| RFC-0303 | Workflow Execution (execution phases, instance lifecycle) |

| RFC-0304 | Workflow Runtime (runtime contract, instance creation) |

| RFC-0307 | Workflow Context (variable resolution, context propagation) |

| RFC-0308 | Workflow Events (event emission model) |

| RFC-0310 | Workflow Conditions (condition evaluation for trigger gating) |

| RFC-0312 | Workflow Scheduler (schedule resolution for scheduled triggers) |

| RFC-0314 | Workflow Error Handling (error taxonomy, trigger failure handling) |

| RFC-0315 | Workflow Recovery (workflow instance state management) |

| RFC-0316 | Workflow Debugging (trigger inspection interfaces) |

| RFC-0317 | Workflow Validation (trigger schema validation) |

| RFC-0318 | Workflow Versioning (deprecated trigger types) |

| RFC-0322 | Workflow Extension (cross-system trigger federation) |

| RFC-1001 | Common Event Model (event bus integration) |

| RFC-1002 | Common State Model (workflow instance state management) |

| ADR-0012 | Contract-First Specification-Driven Development |

| JSON Schema | specs/workflow/json-schema/workflow-trigger-types.md |

| Catalog | specs/workflow/catalog/workflow-triggers.md |

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

This specification IS responsible for: defining the trigger definition model and event semantics.



### Non-Responsibilities

This specification IS NOT responsible for: executing nodes (delegated to RFC-0303), managing the runtime (delegated to RFC-0304), or scheduling decisions (delegated to RFC-0312, except for RFC-0312 itself).



### Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0303 | Consumed | Workflow Execution consumes triggers |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0307 | Consumed | Workflow Context provides context data |

| RFC-0317 | Consumed | Workflow Validation validates trigger definitions |

| RFC-0319 | Consumed | Workflow Security provides trigger authentication |

| RFC-0320 | Consumed | Workflow Performance provides trigger response time |



### Consumers

- Workflow Execution (RFC-0303): Consumes trigger definitions for execution.



### Providers

- 

- 

- Triggers Catalog (catalog/workflow-triggers.md)

- 



### Forbidden Dependencies

- This specification MUST NOT depend on any platform-specific implementation.



## Security

- 

- 

- Triggers MUST be authenticated per RFC-0319.

- 



## Performance

- 

- 

- Trigger response MUST complete within 10ms of event arrival.

- 



## Compatibility

- 

- 

- Trigger definitions MUST be backward compatible within a major version.

- 



## Compliance

- All triggers MUST comply with organizational policies per RFC-0330.



## Future Evolution

- 

- 

- Cross-system trigger federation for distributed workflows.

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

| RFC-0303 | Workflow Execution (trigger consumption) |

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

| schemas/workflow/trigger-definition | Trigger Definition JSON Schema |

| catalog/workflow-triggers | Trigger Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0311 (this document), RFC-0301 (Overview), RFC-0312 (Scheduler) |







