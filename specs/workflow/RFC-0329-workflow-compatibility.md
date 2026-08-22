RFC: RFC-0329

Title: Workflow Compatibility

Status: Proposed

Version: 1.0.0

Author: Atlas Specification Committee

## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Compatibility Level | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Migration Strategy | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Feature Flag | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Deprecation Notice | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Sunset Date | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Override Flag | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Fallback Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Compatibility Test | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Breaking Change | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Non-Breaking Change | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---

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

  - RFC-0322 Workflow Extension

  - RFC-0323 Workflow Plugin Integration

  - RFC-0324 Workflow Storage

  - RFC-0325 Workflow AI

  - RFC-0326 Workflow Vision

  - RFC-0327 Workflow IPC

  - RFC-0328 Workflow Serialization


  - RFC-0330 Workflow Compliance

Target Release: 1.0.0

Review Cycle: Specification Committee

Compatibility: Compatible with Spec 1.x



Related ADR:

  - ADR-0012 Contract-First Specification-Driven Development

Related JSON Schema:

  - schemas/workflow/compatibility-matrix.json

Related Catalog:

  - catalog/workflow-versioning.md

---



## Normative Status

This specification is Normative. Every Atlas subsystem MUST conform to the requirements defined in this document.



The Workflow Compatibility specification defines the compatibility model for Atlas workflows. Compatibility ensures that workflow definitions work correctly across specification versions and implementations.



---
---

## Authority

This RFC is the authoritative specification for the RFC 0329 workflow compatibility.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.




## 2 Compatibility Overview



Key principles:



- Workflow definitions are compatible across specification versions according to the compatibility matrix.

- Incompatible changes require migration.

- Compatibility is verified at validation time.

- Compatibility violations are reported as errors or warnings.



---



## 3 Compatibility Levels



| Level | Description | Enforcement |

|---|---|---|

| Full | Fully compatible across all versions | No enforcement needed |

| Backward | Compatible with previous version | Validation warning |

| Forward | Compatible with next version | Validation warning |

| Conditional | Compatible under specific conditions | Runtime check |

| Incompatible | Not compatible | Validation error |



---



## 4 Compatibility Verification



### 4.1 Verification Steps



1. Compare workflow definition version with runtime version.

2. Check compatibility matrix for known changes.

3. Validate deprecated features are not used.

4. Report compatibility results.



---



## 5 Acceptance Criteria



| # | Criterion | Verification Method |

|---|---|---|

| AC-01 | Five compatibility levels MUST be defined. | Level enumeration test |

| AC-02 | Four compatibility verification steps MUST be enforced. | Verification test |



---



## 6 References



| Reference | Description |

|---|---|

| RFC-0301 | Workflow Overview |

| RFC-0318 | Workflow Versioning |



---



## 5 Terminology



| Term | Definition | Source |

|---|---|---|

| Compatibility | The ability of workflow definitions, instances, and implementations to work correctly across specification versions. | RFC-0301 |

| Backward Compatibility | The ability of a newer version to process data or definitions created by an older version. | This RFC |

| Forward Compatibility | The ability of an older version to gracefully handle data or definitions from a newer version. | This RFC |

| Migration | The process of transitioning a workflow definition or instance from one version to another. | RFC-0318 |

| Deprecation | The formal announcement that a workflow version or feature will no longer be supported. | RFC-0318 |

| Feature Flag | A runtime configuration switch that enables or disables specific workflow features independently of version. | This RFC |



## 6 Layer Boundaries



### 6.1 Responsibilities

This specification IS responsible for: defining the compatibility model, specifying compatibility levels and enforcement, defining the migration process, and establishing the deprecation policy.



### 6.2 Non-Responsibilities

This specification IS NOT responsible for: implementing migration tools (delegated to Workflow Runtime, RFC-0304), performing version validation (delegated to Workflow Validation, RFC-0317), or enforcing compliance (delegated to RFC-0330).



### 6.3 Dependencies

| Dependency | Direction | Description |

|---|---|---|

| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |

| RFC-0304 | Consumed | Workflow Runtime performs version-gated execution |

| RFC-0317 | Consumed | Workflow Validation enforces compatibility rules |

| RFC-0318 | Consumed | Workflow Versioning provides version lifecycle |

| RFC-0328 | Consumed | Workflow Serialization provides version-aware serialization |

| RFC-0330 | Consumed | Workflow Compliance verifies compatibility |



### 6.4 Consumers

- Workflow Runtime (RFC-0304): Uses compatibility matrix for execution decisions.

- Workflow Validation (RFC-0317): Applies compatibility rules during validation.

- Workflow Versioning (RFC-0318): Uses compatibility levels for version transitions.



### 6.5 Providers

- Compatibility Matrix Schema (schemas/workflow/compatibility-matrix.json): Provides the matrix format contract.



### 6.6 Forbidden Dependencies

- This specification MUST NOT depend on any external versioning system (npm, PyPI, Maven).

- This specification MUST NOT assume a particular CI/CD pipeline for compatibility verification.



## 7 Security

- Compatibility checks MUST NOT bypass security validations (RFC-0319).

- Deprecated security features MUST NOT be re-enabled in newer versions.

- Migration processes MUST preserve all security constraints.



## 8 Performance

- Compatibility matrix lookups MUST complete within 1ms.

- Version compatibility checks MUST complete within 10ms per workflow definition.

- Migration validation MUST complete within 100ms for typical workflows.



## 9 Compliance

- All compatibility violations MUST be reported to the compliance system (RFC-0330).

- Deprecated features MUST be tracked in compliance reports.

- Feature flags MUST be auditable for compliance verification.



## 10 Future Evolution

- **Automated Compatibility Testing**: Continuous integration pipelines that automatically test cross-version compatibility.

- **Machine Learning Compatibility Prediction**: Predictive models that forecast compatibility issues before they occur.

- **Multi-Engine Compatibility**: Compatibility guarantees across different workflow engine implementations.

- **Cross-Namespace Compatibility**: Compatibility for workflows spanning multiple Atlas namespaces or tenants.



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

| RFC-0304 | Workflow Runtime (version-gated execution) |

| RFC-0312 | Workflow Scheduler (scheduler compatibility) |

| RFC-0315 | Workflow Recovery (recovery compatibility) |

| RFC-0317 | Workflow Validation (compatibility validation) |

| RFC-0318 | Workflow Versioning (version lifecycle) |

| RFC-0319 | Workflow Security (security compatibility) |

| RFC-0320 | Workflow Performance (performance compatibility) |

| RFC-0328 | Workflow Serialization (format compatibility) |

| RFC-0330 | Workflow Compliance (compatibility compliance) |

| ADR-0012 | Contract-First Specification-Driven Development |

| schemas/workflow/compatibility-matrix.json | Compatibility Matrix JSON Schema |

| catalog/workflow-versioning.md | Versioning Catalog |

| Glossary | Atlas Master Glossary |

| Constitution | Atlas AI Constitution |

| See Also | RFC-0329 (this document), RFC-0318 (Versioning), RFC-0330 (Compliance) |
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
