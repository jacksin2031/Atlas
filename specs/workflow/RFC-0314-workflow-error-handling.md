RFC: RFC-0314
Title: Workflow Error Handling
Status: Proposed
Version: 1.0
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Error Category | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Error Code | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Error Context | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Transient Error | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Permanent Error | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Recoverable Error | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Fatal Error | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Error Handler | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Retry Policy | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compensation Action | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
.0
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
  - RFC-0312 Workflow Scheduler
  - RFC-0313 Workflow Parallelism
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0317 Workflow Validation
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0320 Performance
  - RFC-0321 Workflow Observability
  - RFC-0322 Workflow Extension
  - RFC-0323 Plugin Integration
  - RFC-0324 Workflow Storage
  - RFC-0325 Workflow AI
  - RFC-0326 Workflow Vision
  - RFC-0327 Workflow IPC
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Related ADR: ADR-0012
Related JSON Schema: schemas/workflow/error-handling.json
Related Catalog: catalog/workflow-errors.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.

The Workflow Error Handling specification defines how errors are categorized, handled, and recovered from during workflow execution. Every node execution MAY declare error handlers that determine the response to failures.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0314 workflow error handling.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined in RFC-0301 (Workflow Overview) and are used authoritatively throughout this specification:

| Term | Definition |
|---|---|
| Workflow | A declarative directed graph of nodes, edges, conditions, and triggers that defines orchestration intent. |
| Workflow Instance | A single execution of a workflow definition, with its own state, context, and lifecycle. |
| Node | An atomic unit of work within a workflow graph. |
| Condition | A boolean expression evaluated during execution to determine control flow between nodes. | RFC-0310 |
| Variable | A named, typed value held in the workflow context. |
| Context | The immutable snapshot of variables, parameters, and resources at a given execution point. |
| Checkpoint | A deterministic save point capturing full execution state for resumption. |
| Deterministic | Producing identical results given identical inputs and execution conditions. |
| Idempotent | Producing the same effect regardless of how many times it is executed. |
| Side Effect | Any observable state change beyond the return value of a node execution. |

Additional terms defined in this specification:

| Term | Definition |
|---|---|
| Error | An abnormal condition detected during workflow execution that deviates from the expected operational path. |
| Error Code | A machine-readable identifier uniquely classifying an error condition. |
| Error Category | A high-level grouping of related error codes (transient, permanent, resource, security, validation, compliance, version). |
| Error Severity | The urgency level of an error (info, warning, error, fatal). |
| Error Handler | A declarative rule attached to a node that specifies the response to a particular error condition. |
| Retry Policy | A configuration governing the number, timing, and conditions for re-executing a failed node. |
| Compensation Action | A designated operation that reverses or mitigates the side effects of a failed node. |
| Error Event | A standardized event emitted when an error occurs during workflow execution. |
| Dead Letter Queue | A persistent store for errors that exceeded all retry and escalation limits. |
| Error Propagation | The mechanism by which errors flow from a failed node to its parent context and sibling nodes. |

---

## 2 Error Handling Overview

Key principles:

- Every node execution MAY declare error handlers.
- Errors are categorized by type, severity, and recoverability.
- Recovery strategies include retry, compensation, skip, and abort.
- Error events are emitted for all error conditions.
- Error handling MUST be declarative and configurable per node.

---

## 3 Error Categories

| Category | Description | Recoverable |
|---|---|---|
| Transient | Temporary failure (network, timeout) | Yes |
| Permanent | Unrecoverable failure (invalid data, missing resource) | No |
| Resource | Resource exhaustion (memory, CPU, disk) | Conditional |
| Security | Security violation (permission denied, sandbox breach) | No |
| Validation | Data validation failure | Conditional |
| Compliance | Compliance requirement violation | No |
| Version | Version incompatibility | Conditional |

### 3.1 Transient Errors

Transient errors are temporary failures that MAY resolve without intervention. Examples include network timeouts, rate limiting, and temporary resource unavailability. The implementation SHOULD apply retry policies to transient errors (see Section 5).

### 3.2 Permanent Errors

Permanent errors indicate unrecoverable failures. Examples include invalid input data, missing required resources, and semantic violations. The implementation MUST NOT retry permanent errors without explicit handler override.

### 3.3 Resource Errors

Resource errors occur when system resources are exhausted. The implementation MAY retry resource errors subject to the parallelism bounds defined in RFC-0313.

### 3.4 Security Errors

Security errors indicate violations of sandbox boundaries, access control, or policy constraints. The implementation MUST NOT retry security errors and MUST escalate immediately.

### 3.5 Validation Errors

Validation errors indicate data or configuration that fails validation checks. The implementation MAY retry validation errors if the error is conditionally recoverable.

### 3.6 Compliance Errors

Compliance errors indicate violations of organizational or regulatory rules. The implementation MUST log compliance errors and MUST escalate according to the compliance model (RFC-0330).

### 3.7 Version Errors

Version errors indicate incompatibility between workflow definitions and runtime capabilities. The implementation MAY retry version errors during version migration periods.

---

## 4 Error Handling Strategies

| Strategy | Description | When Used |
|---|---|---|
| Retry | Re-execute the failed node | Transient errors |
| Compensation | Execute compensating action | Permanent errors with side effects |
| Skip | Skip the failed node and continue | Non-critical nodes |
| Abort | Terminate the workflow | Unrecoverable errors |
| Escalate | Notify an operator | Critical errors requiring human intervention |
| Fallback | Execute a fallback action | Errors with predefined alternatives |

### 4.1 Retry

The Retry strategy re-executes the failed node according to the configured retry policy. The implementation MUST apply exponential backoff between retries (see Section 5).

### 4.2 Compensation

The Compensation strategy executes a designated compensating action to reverse or mitigate side effects of the failed node. The implementation MUST ensure idempotency of compensation actions.

### 4.3 Skip

The Skip strategy bypasses the failed node and continues execution of unaffected downstream nodes. The implementation MUST verify that no critical dependencies are violated.

### 4.4 Abort

The Abort strategy terminates the entire workflow instance. The implementation MUST execute all pending compensations before termination and MUST emit a terminal error event.

### 4.5 Escalate

The Escalate strategy notifies an operator or external system when automatic recovery is insufficient. The implementation MUST record the escalation event and MUST pause the workflow instance.

### 4.6 Fallback

The Fallback strategy executes a predefined alternative action when the primary action fails. The implementation MUST ensure the fallback action satisfies the same interface contracts as the primary action.

---

## 5 Retry Policy

### 5.1 Retry Parameters

| Parameter | Description | Default |
|---|---|---|
| Max Retries | Maximum retry attempts | 3 |
| Backoff | Delay between retries | Exponential |
| Backoff Base | Base delay for exponential backoff | 1 second |
| Backoff Max | Maximum delay between retries | 60 seconds |
| Retry On | Error types that trigger retry | Transient |

### 5.2 Retry Exponential Backoff

Delay = min(backoff_base * 2^(attempt-1), backoff_max)

### 5.3 Retry Conditions

- The implementation MUST NOT retry permanent or security errors by default.
- The implementation MUST honor the Retry On configuration to limit which error categories trigger retries.
- The implementation MUST record the retry count in the error event (see Section 6).
- The implementation MUST enforce the Max Retries bound; exceeding this limit MUST trigger the configured escalation handler.

### 5.4 Dead Letter Queue

Errors that exceed all retry limits MUST be persisted in a dead letter queue. The implementation MUST record the error code, category, retry count, and timestamp for each dead letter entry.

---

## 6 Error Events

### 6.1 Error Event Fields

| Field | Description |
|---|---|
| error_code | Unique error identifier |
| error_category | Error category (transient, permanent, etc.) |
| error_message | Human-readable error description |
| node_id | Node that failed |
| workflow_id | Associated workflow instance |
| recovery_action | Action taken to recover |
| retry_count | Number of retries attempted |

### 6.2 Error Event Emission

- The implementation MUST emit an error event immediately upon detecting any error condition.
- Error events MUST conform to the event model defined in RFC-1001.
- Error events MUST include the full error context including node state, variable values, and resource allocations at the time of failure.
- Error events MUST be observable through the observability interface (RFC-0321).

### 6.3 Error Propagation

- Errors MUST propagate from the failed node to its parent context according to the error handling strategy.
- Concurrent sibling nodes MUST receive error notifications to enable coordinated recovery.
- The implementation MUST NOT suppress error events; all errors MUST be emitted regardless of whether they are recoverable.

---

## 7 Layer Boundaries

### 7.1 Responsibilities

- **This layer (Workflow Error Handling)**: Defines error categories, handling strategies, retry policies, error event structure, and error propagation semantics.
- **Caller (Workflow Execution Engine, RFC-0303)**: Invokes error handlers and manages error state transitions.
- **Caller (Workflow Scheduler, RFC-0312)**: Respects error-driven scheduling adjustments (retry delays, backoff).
- **Dependent (Workflow Recovery, RFC-0315)**: Uses error information to determine recovery strategy and checkpoint selection.
- **Dependent (Workflow Debugging, RFC-0316)**: Provides error context for diagnostic inspection.
- **Dependent (Workflow Observability, RFC-0321)**: Emits error metrics and dashboards.

### 7.2 Non-Responsibilities

- This layer MUST NOT assume a specific thread model, process model, or concurrency primitive from any runtime implementation.
- This layer MUST NOT depend on a systems programming language, Node.js, a desktop application framework, a desktop application framework, an embedded database engine, the browser, or GPU resources.
- This layer MUST NOT define parallelism semantics; parallelism is defined in RFC-0313.
- This layer MUST NOT define recovery mechanics; recovery is defined in RFC-0315.
- This layer MUST NOT define debugging interfaces; debugging is defined in RFC-0316.
- This layer MUST NOT define serialization formats; serialization is defined in RFC-0328.

### 7.3 Dependencies

| Direction | Dependency | Nature |
|---|---|---|
| Depends On | RFC-0303 Workflow Execution | Execution model contract |
| Depends On | RFC-0312 Workflow Scheduler | Scheduling adjustments on error |
| Depends On | RFC-0313 Workflow Parallelism | Error classification for parallel faults |
| Depends On | RFC-0315 Workflow Recovery | Recovery strategy selection |
| Depends On | RFC-1001 Common Event Model | Error event emission |
| Depends On | RFC-1006 Common Error Model | Error taxonomy |
| Provided To | RFC-0315 Workflow Recovery | Error context for recovery decisions |
| Provided To | RFC-0316 Workflow Debugging | Error diagnostics |
| Provided To | RFC-0321 Workflow Observability | Error metrics |

### 7.4 Forbidden Dependencies

- This layer MUST NOT depend on any subsystem-specific implementation (Plugin, Storage, Vision, AI, Marketplace, Knowledge).
- This layer MUST NOT depend on any runtime-specific library or framework.
- This layer MUST NOT assume network topology or distributed deployment.

---

## 8 Security

### 8.1 Security Requirements

- Error messages MUST NOT expose sensitive data such as credentials, tokens, or internal system addresses.
- Security errors MUST trigger immediate escalation without retry or suppression.
- The implementation MUST prevent error-based side-channel attacks through controlled error message granularity.
- Error event data MUST respect the same access control policies as the underlying workflow data.

### 8.2 Security Controls

| Control | Requirement | Enforcement Point |
|---|---|---|
| Message Sanitization | No sensitive data in error messages | Error formatter |
| Security Escalation | Immediate escalation, no retry | Error handler |
| Side-Channel Protection | Controlled error granularity | Dispatcher |
| Access Control | Error events respect data policies | Event bus |
| Audit Logging | All security errors logged | Audit trail |

---

## 9 Performance

### 9.1 Performance Requirements

- The implementation MUST measure and expose error rate as a metric (RFC-0321).
- Error event emission MUST complete within 10ms of error detection.
- Retry backoff MUST be accurately enforced with less than 1% timing variance.
- The dead letter queue MUST persist errors asynchronously without blocking workflow execution.

### 9.2 Performance Characteristics

| Metric | Requirement | Measurement |
|---|---|---|
| Error Event Emission | < 10ms | Latency test |
| Retry Backoff Accuracy | < 1% variance | Timing test |
| Dead Letter Persistence | Asynchronous | Throughput test |
| Error Handler Lookup | O(1) hash lookup | Benchmark |
| Error Propagation | < 5ms | Latency test |

---

## 10 Compatibility

### 10.1 Compatibility Levels

| Level | Description | Requirement |
|---|---|---|
| Full | Identical error handling behavior | Same version |
| Forward | Older error definitions run on newer runtime | Backward compatible |
| Backward | Newer error definitions run on older runtime | Best-effort |
| Partial | Some error categories unavailable | Feature flag |
| Incompatible | Error semantics differ significantly | Version migration required |

### 10.2 Version Compatibility

- Error codes defined in one version of this specification MUST be recognized by implementations of the same version.
- Implementations MUST support at least one prior minor version of error codes for backward compatibility.
- New error categories MUST be additive and MUST NOT break existing error handling behavior.
- Breaking changes to error semantics MUST be communicated through the versioning process (RFC-0318).

---

## 11 Compliance

### 11.1 Compliance Requirements

- The implementation MUST log all error events for audit purposes.
- The implementation MUST enforce organizational error handling policies through compliance rules (RFC-0330).
- Security and compliance errors MUST be reported to organizational monitoring systems.
- The implementation MUST maintain an immutable error audit trail conforming to RFC-1001.

### 11.2 Audit Trail

- Every error event MUST be recorded with error code, category, severity, node ID, workflow ID, and timestamp.
- Every retry attempt MUST be recorded with the attempt number and backoff duration.
- Every escalation MUST be recorded with the escalation target and response time.
- Audit records MUST be immutable and MUST survive workflow instance termination.

---

## 12 Future Evolution

### 12.1 Planned Extensions

- Machine learning-assisted error prediction: Proactive error prevention based on historical error patterns.
- Adaptive retry policies: Dynamic adjustment of retry parameters based on error frequency and type.
- Cross-workflow error correlation: Detection of systemic errors affecting multiple workflow instances.
- Error budget management: Integration with SLO/SLI frameworks for error budget tracking.

### 12.2 Extension Points

- Custom error categories MAY be registered through the extension model (RFC-0322).
- Custom error handlers MAY be plugged in through the validation interface (RFC-0317).
- Custom retry policies MAY be defined through the manifest extension (RFC-0310).

---

## 13 Runtime Independence

This specification is intentionally runtime-independent. The following assumptions are explicitly forbidden:

- This specification MUST NOT assume a specific programming language (a systems programming language, Node.js, Python, etc.).
- This specification MUST NOT assume a specific runtime environment (a desktop application framework, a desktop application framework, browser, native).
- This specification MUST NOT assume a specific database or persistence layer (an embedded database engine, a relational database, etc.).
- This specification MUST NOT assume a specific threading or process model (threads, async/await, actors, coroutines).
- This specification MUST NOT assume GPU acceleration or hardware-specific error recovery primitives.
- This specification MUST NOT assume a particular operating system or kernel scheduling strategy.

Implementations MAY use any error handling model provided by their runtime, as long as the external behavior conforms to the declarative, deterministic error handling model defined herein.

---

## 14 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Seven error categories MUST be defined and classified. | Category enumeration test |
| AC-02 | Six error handling strategies (Retry, Compensation, Skip, Abort, Escalate, Fallback) MUST be supported. | Strategy enumeration test |
| AC-03 | Five retry policy parameters MUST be configurable. | Retry policy test |
| AC-04 | Seven error event fields MUST be defined and emitted. | Field enumeration test |
| AC-05 | The implementation MUST enforce exponential backoff with configurable base and maximum. | Backoff enforcement test |
| AC-06 | The implementation MUST persist unrecoverable errors to a dead letter queue. | Dead letter test |
| AC-07 | Error event emission MUST complete within 10ms of error detection. | Latency test |
| AC-08 | Security errors MUST trigger immediate escalation without retry. | Security escalation test |
| AC-09 | The implementation MUST reject error handler configurations that violate declared constraints. | Validation rejection test |
| AC-10 | All error events MUST conform to the common event model (RFC-1001). | Event conformance test |

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (Terminology authority) |
| RFC-0303 | Workflow Execution (Execution engine contract) |
| RFC-0304 | Workflow Runtime (Runtime model) |
| RFC-0310 | Workflow Manifest (Configuration) |
| RFC-0312 | Workflow Scheduler (Scheduling adjustments) |
| RFC-0313 | Workflow Parallelism (Error classification for parallel faults) |
| RFC-0315 | Workflow Recovery (Recovery strategy selection) |
| RFC-0316 | Workflow Debugging (Error diagnostics) |
| RFC-0317 | Workflow Validation (Validation interface) |
| RFC-0318 | Workflow Versioning (Version management) |
| RFC-0320 | Performance (Performance requirements) |
| RFC-0321 | Workflow Observability (Error metrics) |
| RFC-0322 | Workflow Extension (Extension model) |
| RFC-0328 | Workflow Serialization (Serialization) |
| RFC-0330 | Workflow Compliance (Compliance rules) |
| ADR-0012 | Contract-First Specification-Driven Development |
| RFC-1001 | Common Event Model |
| RFC-1006 | Common Error Model |
| Catalog: workflow-errors.md | Error category catalog |
| Catalog: workflow-error-codes.md | Error code registry |
| Schema: error-handling.json | JSON Schema for error handling configuration |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |


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
