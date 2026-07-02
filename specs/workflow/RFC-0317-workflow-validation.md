RFC: RFC-0317
Title: Workflow Validation
Status: Proposed
Version: 1.1.0
Author:
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Validation Rule | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Validation Phase | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Validation Error | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Schema Validation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Semantic Validation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Policy Validation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Lint Rule | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Constraint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Invariant | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Precondition | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
 Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
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
Supersedes: RFC-0101
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
  - RFC-0301 Workflow Overview
  - RFC-0302 Workflow Language
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0305 Workflow Lifecycle
  - RFC-0306 Workflow State
  - RFC-0312 Workflow Scheduler
  - RFC-0314 Workflow Error Handling
  - RFC-0315 Workflow Recovery
  - RFC-0316 Workflow Debugging
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0320 Workflow Performance
  - RFC-0321 Workflow Observability
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/validation-rule.json
  - schemas/workflow/validation-result.json
Related Catalog:
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development

  - catalog/workflow-validation-rules.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the validation requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0010, and ADR-0012.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0317 workflow validation.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary and RFC-0301 (Workflow Overview). Every occurrence of these terms in this specification carries the same definition.

| Term | Definition | Source |
|---|---|---|
| Validation | The process of verifying that a workflow definition satisfies all structural, semantic, and policy constraints before and during execution. | RFC-0301 |
| Validation Rule | A declarative constraint that a workflow definition MUST satisfy. Rules are classified by severity: Error, Warning, or Info. | RFC-0301 |
| Validation Phase | A discrete stage in the validation lifecycle where specific rules are applied. | This RFC |
| Validation Result | The outcome of applying validation rules to a workflow definition, categorized as Error, Warning, or Info. | This RFC |
| Design-time Validation | Pre-deployment validation of workflow definition structure and completeness. | This RFC |
| Deployment Validation | Environment-specific validation of workflow against target runtime capabilities. | This RFC |
| Pre-execution Validation | Input and parameter validation immediately before workflow instance creation. | This RFC |
| Runtime Validation | Continuous state validation during workflow execution. | This RFC |
| Syntax Validation | Structural correctness check of the workflow definition against the language grammar. | RFC-0302 |
| Semantic Validation | Meaning and intent correctness check beyond structural validity. | RFC-0302 |
| Constraint Validation | Verification that declared constraints (budget, resource, priority) are satisfiable. | RFC-0320 |
| Policy Validation | Verification that the workflow definition complies with organizational security and compliance policies. | RFC-0319, RFC-0330 |

---

## 2 Validation Overview

The Workflow Validation specification defines the validation model for Atlas workflows. Validation ensures that workflow definitions are syntactically correct, semantically valid, and compliant with organizational policies before and during execution.

Validation operates at four distinct phases, each with specific responsibilities and rule sets. The validation system MUST enforce that Error-severity violations prevent execution, while Warning-severity violations MAY allow execution with appropriate logging.

Key principles:

- Workflow definitions MUST pass all validation phases before execution begins.
- Validation covers syntax, semantics, constraints, and policies.
- Validation errors MUST prevent execution.
- Validation warnings MUST be logged and MAY allow execution with operator acknowledgment.
- Validation is idempotent: re-validating an unchanged definition MUST produce identical results.
- Validation results MUST be deterministic and reproducible across implementations.

---

## 3 Validation Rules

### 3.1 Rule Taxonomy

Validation rules are classified by category and severity. Every rule MUST have a unique identifier, a category, a severity level, and a deterministic evaluation procedure.

| Rule ID | Category | Description | Severity | Enforced At |
|---|---|---|---|---|
| VR-001 | Syntax | Workflow definition is syntactically valid per RFC-0302 grammar | Error | All phases |
| VR-002 | Type | Variable and parameter types are correct and consistent | Error | Design-time, Pre-execution |
| VR-003 | Reference | All node and edge references point to existing entities | Error | Design-time |
| VR-004 | Cycle | Execution graph is acyclic | Error | Design-time |
| VR-005 | Connectivity | All nodes are reachable from at least one entry point | Error | Design-time |
| VR-006 | Completeness | All required attributes are present per node type catalog | Error | Design-time |
| VR-007 | Uniqueness | Node and edge IDs are globally unique within the workflow | Error | Design-time |
| VR-008 | Budget | Execution budget is sufficient for declared resource requirements | Warning | Deployment, Pre-execution |
| VR-009 | Security | Security constraints are satisfied per RFC-0319 | Error | Deployment, Pre-execution |
| VR-010 | Version | Version compatibility is maintained per RFC-0329 | Warning | Deployment, Pre-execution |
| VR-011 | Compliance | Compliance requirements are met per RFC-0330 | Error | Deployment, Pre-execution |
| VR-012 | Scheduler | Scheduling constraints are satisfiable per RFC-0312 | Warning | Deployment |
| VR-013 | Recovery | Recovery point objectives are achievable per RFC-0315 | Warning | Deployment |
| VR-014 | Performance | Performance SLAs are achievable per RFC-0320 | Warning | Deployment |
| VR-015 | Extension | Extension point registrations are valid per RFC-0322 | Error | Design-time |

### 3.2 Rule Evaluation

Rule evaluation follows a deterministic order:

1. Syntax and structural rules (VR-001 through VR-007) MUST be evaluated first.
2. Semantic and reference rules (VR-002, VR-003) are evaluated second.
3. Policy and constraint rules (VR-008 through VR-015) are evaluated last.

If any Error-severity rule fails, subsequent rule evaluation MAY be skipped for efficiency, but all Error rules that have already been evaluated MUST be reported.

---

## 4 Validation Phases

### 4.1 Phase Definitions

| Phase | Description | When Invoked | Rules Applied |
|---|---|---|---|
| Design-time | Validate workflow definition structure and grammar compliance | Before deployment | VR-001 through VR-007, VR-015 |
| Deployment | Validate workflow against target environment capabilities | At deployment | VR-008 through VR-014 |
| Pre-execution | Validate workflow inputs, parameters, and runtime readiness | Before execution | VR-002, VR-008, VR-009, VR-010, VR-011 |
| Runtime | Validate execution state integrity during execution | During execution | VR-009, VR-011, VR-014 |

### 4.2 Phase Transitions

- A workflow definition MUST pass Design-time validation before entering Deployment validation.
- A workflow definition MUST pass Deployment validation before entering Pre-execution validation.
- Runtime validation runs concurrently with execution and MAY trigger corrective actions (per RFC-0314).

---

## 5 Validation Results

### 5.1 Result Types

| Type | Description | Action Required |
|---|---|---|
| Error | Validation failed; constraint is violated | MUST prevent execution |
| Warning | Validation passed with caution; constraint is marginal | MAY allow execution with logging |
| Info | Informational message; no constraint violation | Log only; no action required |

### 5.2 Result Format

Every validation result MUST include:

- Rule ID that was evaluated
- Result type (Error, Warning, Info)
- Description of the violation or confirmation
- Location in the workflow definition (node ID, edge ID, or global)
- Remediation guidance (for Errors and Warnings)

### 5.3 Result Aggregation

Validation results MUST be aggregated per phase. A workflow definition passes a phase only if:

- No Error-severity results exist for that phase.
- All Warning-severity results have been acknowledged by the operator (or the operator MAY choose to proceed at their discretion).

---

## 6 Layer Boundaries

### 6.1 Responsibilities

This specification IS responsible for:

- Defining the validation rule taxonomy and severity model.
- Specifying the four validation phases and their ordering.
- Defining the validation result format and aggregation rules.
- Establishing the relationship between validation results and execution gating.

### 6.2 Non-Responsibilities

This specification IS NOT responsible for:

- Defining individual validation rule implementations (delegated to specific RFCs).
- Executing validation (handled by the Workflow Runtime, RFC-0304).
- Persisting validation results (handled by Workflow Storage, RFC-0324).
- Observing validation events (handled by Workflow Observability, RFC-0321).

### 6.3 Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides the foundational graph model |
| RFC-0302 | Consumed | Workflow Language provides the grammar and AST model |
| RFC-0304 | Consumed | Workflow Runtime provides the execution gating mechanism |
| RFC-0312 | Consumed | Workflow Scheduler provides scheduling constraint definitions |
| RFC-0314 | Consumed | Workflow Error Handling provides error propagation semantics |
| RFC-0315 | Consumed | Workflow Recovery provides recovery constraint definitions |
| RFC-0319 | Consumed | Workflow Security provides security policy definitions |
| RFC-0320 | Consumed | Workflow Performance provides performance SLA definitions |
| RFC-0322 | Consumed | Workflow Extension provides extension point definitions |
| RFC-0324 | Consumed | Workflow Storage provides result persistence |
| RFC-0329 | Consumed | Workflow Compatibility provides version compatibility model |
| RFC-0330 | Consumed | Workflow Compliance provides compliance rule definitions |

### 6.4 Consumers

- Workflow Runtime (RFC-0304): Uses validation results for execution gating.
- Workflow Language (RFC-0302): Provides grammar rules for syntax validation.
- Workflow Security (RFC-0319): Provides security constraints for policy validation.
- Workflow Compliance (RFC-0330): Provides compliance rules for policy validation.

### 6.5 Providers

- Validation Rule Catalog (catalog/workflow-validation-rules.md): Provides the definitive list of validation rules.
- Validation Result Schema (schemas/workflow/validation-result.json): Provides the result format contract.

### 6.6 Forbidden Dependencies

- This specification MUST NOT depend on any platform-specific validation library.
- This specification MUST NOT prescribe a particular validation engine implementation.
- Runtime validation MUST NOT block execution for Warning-severity results unless explicitly configured.

---

## 7 Security

### 7.1 Security Controls

| Control | Requirement | Enforcement |
|---|---|---|
| Rule Integrity | Validation rules MUST be tamper-evident | Cryptographic hash per rule |
| Access Control | Only authorized actors MAY modify validation rules | RBAC per RFC-0319 |
| Audit Trail | All validation events MUST be logged | Immutable log per RFC-0321 |
| Sandboxing | Validation of untrusted workflows MUST occur in sandbox | Isolated evaluation per RFC-0319 |
| Rate Limiting | Validation requests MAY be rate-limited to prevent DoS | Configurable per RFC-0320 |

### 7.2 Security Validation Rules

The following security-specific validation rules MUST be enforced:

- VR-S01: Workflow MUST NOT declare capabilities it does not possess.
- VR-S02: Workflow MUST NOT reference nodes outside its permission boundary.
- VR-S03: Workflow MUST NOT bypass security constraints through graph manipulation.
- VR-S04: All extension points used by the workflow MUST be registered and authorized.

---

## 8 Performance

### 8.1 Performance Requirements

| Metric | Requirement | Measurement |
|---|---|---|
| Design-time validation latency | MUST complete within 100ms for workflows up to 100 nodes | Wall-clock time |
| Pre-execution validation latency | MUST complete within 50ms | Wall-clock time |
| Rule evaluation throughput | MUST evaluate at least 1,000 rules per second | Rules/second |
| Memory usage | Validation state MUST NOT exceed 10MB for typical workflows | RSS |
| Idempotency | Re-validating unchanged definition MUST produce identical results within 10% time variance | Statistical test |

### 8.2 Performance Constraints

- Validation MUST NOT introduce unbounded blocking during execution.
- Runtime validation checks MUST complete within 1ms per check to avoid affecting execution latency.
- Large workflow definitions (10,000+ nodes) MUST support incremental validation.

---

## 9 Compatibility

### 9.1 Version Compatibility

Validation rules themselves are versioned. A validation rule defined in version N of this specification MUST be recognized by all implementations conforming to version N or later.

### 9.2 Cross-Version Validation

- A workflow definition created under an older version of this specification MUST be revalidated under the current version before execution.
- Rules that are new in a later version MUST be treated as Warnings during transitional validation; they MUST become Errors in the version following the next minor release.

### 9.3 Format Compatibility

Validation result formats MUST be backward compatible within a major version. Breaking changes to the validation result schema MUST be accompanied by a version bump.

---

## 10 Compliance

### 10.1 Regulatory Compliance

Validation results MUST support export in formats required by regulatory auditors (SOX, GDPR, HIPAA as applicable).

### 10.2 Internal Policy Compliance

Organizations MAY define additional validation rules beyond the normative set in this specification. Additional rules MUST:

- Conform to the validation rule taxonomy defined in Section 3.
- Be registered in the validation rule catalog.
- NOT conflict with existing normative rules.

### 10.3 Audit Trail

All validation events (rule evaluation, results, phase transitions) MUST be recorded in an immutable audit trail per RFC-0321.

---

## 11 Future Evolution

### 11.1 Planned Extensions

- **Machine Learning-Assisted Validation**: Predictive validation rules that learn from historical execution data.
- **Distributed Validation**: Parallel validation across multiple nodes for very large workflow definitions.
- **Real-Time Policy Engine**: Dynamic policy evaluation during execution without full re-validation.
- **Cross-Workflow Validation**: Validation of interdependent workflow collections.

### 11.2 Stability Guarantee

The validation rule taxonomy (Section 3) and phase model (Section 4) are stable and will not change within a major version. New rules MAY be added; existing rules MUST NOT be removed or have their severity increased without a deprecation period of at least one minor version.

---

## 12 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

All validation contracts are defined in terms of abstract data structures and behavioral requirements.

---

## 13 Acceptance Criteria

### 13.1 Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST support at least fifteen validation rules as defined in Section 3.1. | Rule enumeration test |
| AC-02 | The implementation MUST enforce four distinct validation phases as defined in Section 4.1. | Phase enumeration test |
| AC-03 | The implementation MUST classify all validation results into Error, Warning, or Info categories. | Result classification test |

### 13.2 Rule Evaluation

| # | Criterion | Verification Method |
|---|---|---|
| AC-04 | The implementation MUST evaluate rules in the deterministic order specified in Section 3.2. | Order enforcement test |
| AC-05 | The implementation MUST skip subsequent rule evaluation when Error-severity rules fail (optimization). | Optimization test |

### 13.3 Security

| # | Criterion | Verification Method |
|---|---|---|
| AC-06 | The implementation MUST enforce all four security validation rules (VR-S01 through VR-S04). | Security rule test |
| AC-07 | The implementation MUST log all validation events to the audit trail. | Audit trail test |

### 13.4 Performance

| # | Criterion | Verification Method |
|---|---|---|
| AC-08 | The implementation MUST complete design-time validation within 100ms for workflows up to 100 nodes. | Latency test |
| AC-09 | The implementation MUST evaluate at least 1,000 rules per second. | Throughput test |

### 13.5 Compatibility

| # | Criterion | Verification Method |
|---|---|---|
| AC-10 | The implementation MUST revalidate older workflow definitions under the current version before execution. | Cross-version test |
| AC-11 | The implementation MUST treat new rules as Warnings during transitional validation. | Deprecation test |

---

## 14 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0302 | Workflow Language (grammar and AST model) |
| RFC-0303 | Workflow Execution (execution semantics) |
| RFC-0304 | Workflow Runtime (execution gating) |
| RFC-0305 | Workflow Lifecycle (phase integration) |
| RFC-0306 | Workflow State (state validation) |
| RFC-0312 | Workflow Scheduler (scheduling constraints) |
| RFC-0314 | Workflow Error Handling (error propagation) |
| RFC-0315 | Workflow Recovery (recovery constraints) |
| RFC-0316 | Workflow Debugging (debug validation) |
| RFC-0318 | Workflow Versioning (version compatibility) |
| RFC-0319 | Workflow Security (security policies) |
| RFC-0320 | Workflow Performance (performance SLAs) |
| RFC-0321 | Workflow Observability (audit trail) |
| RFC-0322 | Workflow Extension (extension point validation) |
| RFC-0324 | Workflow Storage (result persistence) |
| RFC-0328 | Workflow Serialization (validation result serialization) |
| RFC-0329 | Workflow Compatibility (version compatibility model) |
| RFC-0330 | Workflow Compliance (compliance rules) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/validation-rule.json | Validation Rule JSON Schema |
| schemas/workflow/validation-result.json | Validation Result JSON Schema |
| catalog/workflow-validation-rules.md | Validation Rule Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0317 (this document), RFC-0330 (Compliance), RFC-0329 (Compatibility) |
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
