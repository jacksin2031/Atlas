RFC: RFC-0330

Title: Workflow Compliance

Status: Proposed

Version: 1.0.0

Author: Atlas Specification Committee

C
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Compliance Category | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compliance Rule | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compliance Check | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compliance Report | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Audit Trail | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Regulatory Requirement | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Policy Rule | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Control Objective | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Evidence | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Remediation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Certification | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
reated: 2026-07-01

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

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

  - RFC-0325 Workflow AI

  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC

  - RFC-0328 Workflow Serialization

  - RFC-0329 Workflow Compatibility


Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x



Related ADR:

  - ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema:

  - schemas/workflow/compliance-report.json

Related Catalog:

  - catalog/workflow-status.md

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Compliance specification defines the compliance model for Atlas workflows. Compliance ensures that workflow execution adheres to organizational, regulatory, and operational requirements.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0330 workflow compliance.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 2 Compliance Overview



Key principles:



- Workflow execution enforces organizational and regulatory compliance requirements.

- Compliance rules are declarative and extensible.

- Compliance violations are reported and logged.

- Compliance audit trails are maintained.



---



## 3 Compliance Categories



| Category | Description | Enforcement |

|---|---|---|

| Operational | Operational procedure compliance | Pre-execution check |

| Regulatory | Regulatory requirement compliance | Pre-execution check |

| Security | Security policy compliance | Continuous monitoring |

| Data Privacy | Data privacy requirement compliance | Continuous monitoring |

| Audit | Audit trail requirement compliance | Post-execution verification |

| Quality | Quality assurance requirement compliance | Post-execution verification |



---



## 4 Compliance Rules



### 4.1 Rule Structure



| Field | Description |

|---|---|

| rule_id | Unique rule identifier |

| category | Compliance category |

| description | Human-readable rule description |

| condition | Condition that must be satisfied |

| violation_action | Action on violation (warn, block, log) |

| severity | Violation severity (info, warning, error) |



### 4.2 Enforcement Points



| Point | Description |

|---|---|

| Pre-execution | Rules checked before workflow starts |

| During execution | Rules checked at each node |

| Post-execution | Rules checked after workflow completes |



---



## 5 Compliance Reporting



### 5.1 Report Types



| Type | Description | Frequency |

|---|---|---|

| Real-time | Immediate violation notification | On violation |

| Periodic | Summary of compliance status | Daily/Weekly |

| On-demand | Ad-hoc compliance report | Requested |



---



## 6 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | Six compliance categories MUST be supported. | Category enumeration test |

| AC-02 | Six compliance rule fields MUST be defined. | Rule field test |

| AC-03 | Three enforcement points MUST be supported. | Enforcement test |

| AC-04 | Three compliance report types MUST be supported. | Report type test |



---



## 7 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview |

| RFC-0319 | Workflow Security |

| RFC-0321 | Workflow Observability |



---



## 5 Terminology



| Term | Definition | Source |

|---|---|---|

| Compliance | The degree to which workflow definitions and executions adhere to organizational policies, regulatory requirements, and specification standards. | RFC-0301 |

| Compliance Rule | A declarative constraint that defines a required condition for workflow execution. | This RFC |

| Compliance Category | A classification of compliance rules by domain (Operational, Regulatory, Security, Data Privacy, Audit, Quality). | This RFC |

| Enforcement Point | A lifecycle stage at which compliance rules are evaluated (Pre-execution, During execution, Post-execution). | This RFC |

| Compliance Report | A structured output summarizing compliance status, violations, and remediation actions. | This RFC |



## 6 Layer Boundaries



### 6.1 Responsibilities

This specification IS responsible for: defining the compliance model, specifying compliance categories and rules, establishing enforcement points, and defining compliance reporting.



### 6.2 Non-Responsibilities

This specification IS NOT responsible for: implementing compliance checks (delegated to Workflow Validation, RFC-0317), storing compliance data (delegated to Workflow Storage, RFC-0324), or observing compliance events (delegated to Workflow Observability, RFC-0321).



### 6.3 Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0304 | Consumed | Workflow Runtime enforces compliance during execution |

| RFC-0317 | Consumed | Workflow Validation applies compliance rules |

| RFC-0319 | Consumed | Workflow Security provides security compliance rules |

| RFC-0320 | Consumed | Workflow Performance provides performance compliance |

| RFC-0321 | Consumed | Workflow Observability provides compliance event reporting |

| RFC-0324 | Consumed | Workflow Storage provides compliance data persistence |

| RFC-0329 | Consumed | Workflow Compatibility provides compliance version compatibility |



### 6.4 Consumers

- Workflow Validation (RFC-0317): Uses compliance rules as validation constraints.

- Workflow Security (RFC-0319): Provides security compliance requirements.

- Workflow Observability (RFC-0321): Reports compliance events.



### 6.5 Providers

- Compliance Report Schema (schemas/workflow/compliance-report.json): Provides the report format contract.



### 6.6 Forbidden Dependencies

- This specification MUST NOT depend on any specific regulatory framework (SOX, GDPR, HIPAA) as a hard requirement; frameworks are policy decisions.

- This specification MUST NOT assume a particular compliance tooling ecosystem.



## 7 Security

- Compliance violations MUST be treated as security events per RFC-0319.

- Compliance audit trails MUST be tamper-evident.

- Compliance reports MUST NOT expose secrets or sensitive data.



## 8 Performance

- Compliance rule evaluation MUST complete within 5ms per rule.

- Compliance report generation MUST complete within 100ms.

- Real-time compliance notifications MUST be delivered within 1 second of violation detection.



## 9 Compatibility

- Compliance rules MUST be versioned and backward compatible within a major version.

- New compliance categories MAY be added without breaking existing compliance reports.



## 10 Future Evolution

- **Automated Compliance Certification**: Machine-readable compliance certificates for regulatory audits.

- **Cross-Platform Compliance**: Unified compliance model across different Atlas deployment platforms.

- **Real-Time Compliance Dashboards**: Live compliance status visualization for operations teams.

- **Compliance-as-Code**: Declarative compliance policies with version-controlled rule definitions.

- **AI-Assisted Compliance**: Machine learning models that predict compliance risks before execution.



## 11 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)

- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)

- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)

- Any operating system (Windows, Linux, macOS, etc.)

- Any hardware architecture (CPU, GPU, FPGA, etc.)

- Any threading model (single-threaded, multi-threaded, actor-based, etc.)



## 12 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview (canonical terminology source) |

| RFC-0304 | Workflow Runtime (execution compliance) |

| RFC-0312 | Workflow Scheduler (scheduling compliance) |

| RFC-0314 | Workflow Error Handling (compliance error reporting) |

| RFC-0315 | Workflow Recovery (recovery compliance) |

| RFC-0316 | Workflow Debugging (debug compliance) |

| RFC-0317 | Workflow Validation (compliance rule application) |

| RFC-0318 | Workflow Versioning (version compliance) |

| RFC-0319 | Workflow Security (security compliance) |

| RFC-0320 | Workflow Performance (performance compliance) |

| RFC-0321 | Workflow Observability (compliance event reporting) |

| RFC-0322 | Workflow Extension (extension compliance) |

| RFC-0324 | Workflow Storage (compliance data persistence) |

| RFC-0327 | Workflow IPC (IPC compliance) |

| RFC-0328 | Workflow Serialization (serialization compliance) |

| RFC-0329 | Workflow Compatibility (compatibility compliance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/compliance-report.json | Compliance Report JSON Schema |

| catalog/workflow-status.md | Status Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0330 (this document), RFC-0319 (Security), RFC-0321 (Observability) |
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
