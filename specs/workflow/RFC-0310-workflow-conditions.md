RFC: RFC-0310

Title: Workflow Conditions

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

Related JSON Schema: specs/workflow/json-schema/workflow-condition-types.md

Related Catalog: specs/workflow/catalog/workflow-conditions.md

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x

Last Updated: 2026-07-01

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Conditions specification defines the condition model for Atlas workflows. Conditions are boolean expressions that gate the execution of nodes and the traversal of edges.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0310 workflow conditions.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 1 Terminology



The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below.



| Term | Definition |

|---|---|

| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 |

| Condition Type | A named category of condition (e.g., Boolean, Comparison, Temporal) that determines the evaluation semantics and available operators. |

| Condition Operator | A symbolic or functional element (AND, OR, EQUALS, etc.) used within a condition expression to combine or compare operands. |

| Condition Evaluation | The process of resolving a condition expression to a boolean result within a given execution context. |

| Short-Circuit Evaluation | An optimization where condition evaluation stops as soon as the result is determined (e.g., AND with false operand). |

| Composite Condition | A condition composed of multiple simple conditions combined using logical operators. |

| Condition Group | An organizational construct that groups multiple conditions for structured evaluation. |

| Evaluation Context | The runtime state (variables, node states, event queue, resource state, time) available during condition evaluation. |

| Workflow Runtime | The runtime system responsible for loading, validating, scheduling, executing, and observing workflow instances. Referenced in RFC-0304. |



---



## 2 Layer Boundaries



### 2.1 Responsibilities



The Workflow Conditions specification defines:



- The taxonomy of condition types and their evaluation semantics.

- The set of condition operators and their type signatures.

- The condition evaluation algorithm (ordering, short-circuit, caching).

- The evaluation context model (variables, node states, events, resources, time).

- Composite condition composition rules.

- Condition validation rules (syntax, type, reference, completeness, complexity).



### 2.2 Non-Responsibilities



The following are explicitly OUT OF SCOPE for this specification:



- Workflow Runtime scheduling decisions (RFC-0304, RFC-0312).

- Trigger firing mechanisms (RFC-0311).

- Action execution logic (RFC-0309).

- Error handling and retry policies (RFC-0314).

- Recovery and checkpoint semantics (RFC-0315).

- Debugging and inspection interfaces (RFC-0316).

- Expression language syntax beyond condition evaluation (RFC-0302).



### 2.3 Dependencies



| Dependency | Direction | Nature |

|---|---|---|

| RFC-0301 Workflow Overview | Consumes | Terminology, philosophy |

| RFC-0302 Workflow Language | Consumes | Expression language syntax |

| RFC-0303 Workflow Execution | Consumes | Execution phases, context |

| RFC-0304 Workflow Runtime | Consumes | Runtime contract, node lifecycle |

| RFC-0307 Workflow Context | Consumes | Variable resolution, context propagation |

| RFC-0308 Workflow Events | Consumes | Event model for event-based conditions |

| RFC-0309 Workflow Actions | Consumes | Action state for condition evaluation |

| RFC-0317 Workflow Validation | Consumes | Condition schema validation |

| RFC-1002 Common State Model | Consumes | State representation for conditions |



### 2.4 Consumers



- Workflow Runtime (RFC-0304): Evaluates conditions at node gates and edge traversals.

- Workflow Debugger (RFC-0316): Inspects condition evaluation results and contexts.

- Workflow Validator (RFC-0317): Validates condition declarations against schema.

- Trigger System (RFC-0311): Uses conditions for trigger activation gating.



### 2.5 Providers



- Workflow Runtime (RFC-0304): Provides execution context, variable resolution, event bus.

- State Model (RFC-1002): Provides node state representation for state-based conditions.

- Event Bus (RFC-1001): Provides event stream for event-based conditions.



### 2.6 Forbidden Dependencies



Condition evaluators MUST NOT depend on:



- Any specific programming language runtime (a systems programming language, Node.js, a desktop application framework, a desktop application framework).

- Any specific database engine (an embedded database engine, a relational database, etc.).

- Any browser API or DOM interface.

- Any operating system call or process model.

- Any GPU compute interface.

- Any threading or concurrency model (sequential evaluation is sufficient for correctness).



---



## 3 Condition Model Overview



Conditions evaluate to true or false. A condition gate prevents a node from executing or an edge from being traversed until the condition evaluates to true.



---



## 4 Condition Types



| Condition Type | Description | Example |

|---|---|---|

| Boolean | Simple true/false expression | flag == true |

| Comparison | Value comparison | count > 10 |

| Temporal | Time-based condition | now >= scheduled_time |

| State-based | Node state condition | node_a.state == completed |

| Event-based | Event occurrence condition | event_type == approval |

| Resource-based | Resource availability condition | resource.available == true |

| Data-based | Data content condition | data.length > 0 |

| Composite | Combination of conditions | (a AND b) OR c |



---



## 5 Condition Operators



| Operator | Description | Type |

|---|---|---|

| AND | Logical conjunction | Boolean |

| OR | Logical disjunction | Boolean |

| NOT | Logical negation | Boolean |

| EQUALS | Equality | Comparison |

| NOT_EQUALS | Inequality | Comparison |

| LESS_THAN | Less than | Comparison |

| LESS_EQUAL | Less than or equal | Comparison |

| GREATER_THAN | Greater than | Comparison |

| GREATER_EQUAL | Greater than or equal | Comparison |

| IN | Membership | Set |

| NOT_IN | Non-membership | Set |

| EXISTS | Existence check | Data |

| EMPTY | Emptiness check | Data |

| BEFORE | Temporal ordering | Temporal |

| AFTER | Temporal ordering | Temporal |

| BETWEEN | Range check | Temporal |



---



## 6 Condition Evaluation



### 6.1 Evaluation Rules



1. Conditions are evaluated in the order declared.

2. Short-circuit evaluation is applied for AND and OR operators.

3. Condition evaluation results are cached for the duration of the workflow instance.

4. Condition evaluation failures cause the workflow to enter a failed state.



### 6.2 Evaluation Context



Conditions are evaluated in the context of:



- Current variable values

- Current node states

- Current event queue

- Current resource state

- Current time



---



## 7 Condition Composition



### 7.1 Composite Conditions



Composite conditions combine multiple simple conditions using logical operators:



- AND: All sub-conditions must be true.

- OR: At least one sub-condition must be true.

- NOT: The sub-condition must be false.



### 7.2 Condition Groups



Conditions MAY be grouped for organization:



- Groups are evaluated in order.

- A group passes if all conditions in the group pass.

- Groups are combined using logical operators.



---



## 8 Condition Validation



### 8.1 Validation Rules



| Rule | Description | Severity |

|---|---|---|

| Syntax | Condition expression is syntactically valid | Error |

| Type | Condition operands have compatible types | Error |

| Reference | Condition references exist | Error |

| Completeness | All required operands are provided | Error |

| Complexity | Condition complexity is within bounds | Warning |



---



## 9 Security



### 9.1 Condition-Level Security Controls



| Control | Requirement | Enforcement Point |

|---|---|---|

| Expression Sanitization | All condition expressions MUST be sanitized against injection attacks. | Declaration |

| Reference Validation | Condition references MUST resolve to existing variables, nodes, or events. | Pre-evaluation |

| Type Safety | Condition operands MUST be type-checked before evaluation. | Pre-evaluation |

| Complexity Limiting | Condition expression trees MUST not exceed 100 nodes. | Validation |

| Evaluation Timeout | Condition evaluation MUST complete within 50ms. | Runtime |

| Context Isolation | Conditions MUST NOT access variables outside their declared scope. | Runtime |

| Audit Logging | All condition evaluations (result, context, timing) MUST be logged. | Post-evaluation |

| Recursive Prevention | Composite conditions MUST not contain circular references. | Validation |



### 9.2 Forbidden Patterns



Condition evaluators MUST NOT:



- Execute arbitrary code or scripts within condition expressions.

- Access variables not declared in the condition context.

- Modify workflow state during condition evaluation.

- Make network calls or I/O operations during evaluation.



---



## 10 Performance



### 10.1 Performance Requirements



| Metric | Requirement | Measurement |

|---|---|---|

| Evaluation Latency | Simple condition evaluation MUST complete within 1ms. | Per-evaluation timer |

| Composite Evaluation | Composite condition evaluation MUST complete within 10ms. | Tree evaluation benchmark |

| Cache Hit Rate | Cached condition results MUST be served within 100 microseconds. | Cache lookup test |

| Memory Footprint | Condition evaluation context MUST not exceed 32 KiB per condition. | Profiling |

| Short-Circuit Efficiency | Short-circuit evaluation MUST reduce average evaluation time by at least 30 percent. | Benchmark |

| Compilation Time | Condition schema compilation MUST complete within 50ms for 500 conditions. | Schema benchmark |



### 10.2 Optimization Guidelines



- Simple conditions SHOULD be evaluated before composite conditions.

- Frequently evaluated conditions SHOULD be cached by the runtime.

- Condition complexity SHOULD be monitored and flagged when exceeding thresholds.



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



### 11.2 Condition Type Compatibility



- New condition types MAY be added without breaking existing workflows.

- Condition operators MAY be added without breaking existing workflows.

- Condition operator semantics MUST NOT change between minor versions.

- Removed condition types MUST follow the deprecation cycle defined in RFC-0318.



---



## 12 Compliance



### 12.1 Compliance Categories



| Category | Requirement | Enforcement |

|---|---|---|

| Operational | Conditions MUST declare their evaluation context. | Pre-execution |

| Security | Conditions MUST enforce expression sanitization and type safety. | Continuous |

| Audit | All condition evaluations MUST produce audit trail entries. | Post-evaluation |

| Data Privacy | Conditions accessing PII variables MUST declare data classification. | Declaration |

| Determinism | Identical condition inputs MUST produce identical evaluation results. | Runtime |

| Complexity | Condition expression trees MUST not exceed 100 nodes. | Validation |



---



## 13 Future Evolution



### 13.1 Planned Extensions



| Feature | Status | RFC |

|---|---|---|

| Fuzzy conditions (approximate matching) | Proposed | RFC-0325 |

| Probabilistic conditions | Proposed | RFC-0325 |

| Condition composition DSL | Proposed | RFC-0302 |

| Condition performance profiling | Proposed | RFC-0320 |

| Condition versioning | Proposed | RFC-0318 |



### 13.2 Deprecation Policy



- Deprecated condition types MUST remain functional for at least two major versions.

- Migration guides MUST be provided for all deprecated condition operators.

- New workflows MUST NOT use deprecated condition types.



---



## 14 Runtime Independence



This specification is intentionally runtime-independent. It makes no assumptions about:



- Programming language: Condition evaluators MAY be implemented in any language.

- Runtime environment: Conditions MAY be evaluated in-process or remotely.

- Process model: No assumption of threads, goroutines, or async/await.

- Database: No assumption of an embedded database engine, relational, or document stores.

- Browser: No assumption of DOM, Web APIs, or rendering.

- Operating system: No assumption of POSIX, Windows, or any OS-specific API.

- Hardware: No assumption of GPU, TPU, or specialized accelerators.

- Serialization format: Condition contexts MAY use JSON, MessagePack, or any agreed format.



---



## 15 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | The implementation MUST support eight (8) distinct condition types as enumerated in Section 4. | Type enumeration test |

| AC-02 | The implementation MUST support sixteen (16) distinct condition operators as enumerated in Section 5. | Operator enumeration test |

| AC-03 | The implementation MUST define five (5) evaluation context elements as enumerated in Section 6.2. | Context test |

| AC-04 | The implementation MUST enforce five (5) condition validation rules as enumerated in Section 8.1. | Validation test |

| AC-05 | The implementation MUST enforce short-circuit evaluation for AND and OR operators. | Short-circuit test |

| AC-06 | The implementation MUST cache condition evaluation results for the duration of the workflow instance. | Cache test |

| AC-07 | The implementation MUST enforce all eight (8) security controls defined in Section 9.1. | Security audit |

| AC-08 | The implementation MUST measure all six (6) performance metrics defined in Section 10.1. | Performance benchmark |

| AC-09 | The implementation MUST enforce five (5) compatibility levels defined in Section 11.1. | Compatibility test |

| AC-10 | The implementation MUST enforce six (6) compliance categories defined in Section 12.1. | Compliance test |



---



## 16 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (terminology, philosophy) |

| RFC-0302 | Workflow Language (expression language syntax) |

| RFC-0303 | Workflow Execution (execution phases, context) |

| RFC-0304 | Workflow Runtime (runtime contract, node lifecycle) |

| RFC-0307 | Workflow Context (variable resolution, context propagation) |

| RFC-0308 | Workflow Events (event model for event-based conditions) |

| RFC-0309 | Workflow Actions (action state for condition evaluation) |

| RFC-0311 | Workflow Triggers (trigger activation gating) |

| RFC-0315 | Workflow Recovery (state-based condition semantics) |

| RFC-0316 | Workflow Debugging (condition inspection interfaces) |

| RFC-0317 | Workflow Validation (condition schema validation) |

| RFC-0318 | Workflow Versioning (deprecated condition types) |

| RFC-1001 | Common Event Model (event stream for event-based conditions) |

| RFC-1002 | Common State Model (state representation for conditions) |

| ADR-0012 | Contract-First Specification-Driven Development |

| JSON Schema | specs/workflow/json-schema/workflow-condition-types.md |

| Catalog | specs/workflow/catalog/workflow-conditions.md |

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

This specification IS responsible for: defining the condition expression model and evaluation semantics.



### Non-Responsibilities

This specification IS NOT responsible for: executing nodes (delegated to RFC-0303), managing the runtime (delegated to RFC-0304), or scheduling decisions (delegated to RFC-0312, except for RFC-0312 itself).



### Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0303 | Consumed | Workflow Execution consumes conditions |

| RFC-0304 | Consumed | Workflow Runtime provides execution context |

| RFC-0307 | Consumed | Workflow Context provides context data |

| RFC-0317 | Consumed | Workflow Validation validates condition expressions |

| RFC-0319 | Consumed | Workflow Security provides condition evaluation security |

| RFC-0320 | Consumed | Workflow Performance provides condition evaluation performance |



### Consumers

- Workflow Execution (RFC-0303): Consumes condition definitions for execution.



### Providers

- 

- Conditions Catalog (catalog/workflow-conditions.md)

- 

- 



### Forbidden Dependencies

- This specification MUST NOT depend on any platform-specific implementation.



## Security

- 

- Condition expressions MUST be validated for injection attacks per RFC-0317.

- 

- 



## Performance

- 

- Condition evaluation MUST complete within 1ms.

- 

- 



## Compatibility

- 

- Condition expression syntax MUST be backward compatible within a major version.

- 

- 



## Compliance

- All conditions MUST comply with organizational policies per RFC-0330.



## Future Evolution

- 

- Machine learning-assisted condition optimization.

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

| RFC-0303 | Workflow Execution (condition consumption) |

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

| schemas/workflow/condition-expression | Condition Expression JSON Schema |

| catalog/workflow-conditions | Condition Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0310 (this document), RFC-0301 (Overview), RFC-0309 (Actions) |






