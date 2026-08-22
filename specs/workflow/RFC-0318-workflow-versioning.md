RFC: RFC-0318
Title: Workflow Versioning
Status: Proposed
Vers
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Semantic Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Major Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Minor Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Patch Version | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Version Constraint | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Version Range | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Deprecation | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Sunset | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Backward Compatibility | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Forward Compatibility | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---
ion: 1.1.0
Author: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-1005 Common Manifest Model
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
  - RFC-0301 Workflow Overview
  - RFC-0302 Workflow Language
  - RFC-0304 Workflow Runtime
  - RFC-0315 Workflow Recovery
  - RFC-0317 Workflow Validation
  - RFC-0319 Workflow Security
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/version-metadata.json
Related Catalog:
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development

  - catalog/workflow-versioning.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the versioning requirements defined in this document.

---
---

## Authority

This RFC is the authoritative specification for the RFC 0318 workflow versioning.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Version | A semantic identifier for a specific snapshot of a workflow definition, comprising major, minor, and patch components. | RFC-0301 |
| Major Version | The leftmost component of a semantic version, incremented when incompatible changes are introduced. | RFC-0329 |
| Minor Version | The middle component, incremented when backward-compatible functionality is added. | RFC-0329 |
| Patch Version | The rightmost component, incremented when backward-compatible bug fixes are made. | RFC-0329 |
| Version Metadata | Structured data attached to a workflow version describing the changes, authors, and compliance status. | This RFC |
| Deprecation | The formal process of marking a workflow version or feature as obsolete while maintaining backward compatibility during a transition period. | RFC-0329 |
| Migration | The process of transitioning a workflow instance or definition from one version to another. | RFC-0329 |
| Version Anchor | A stable identifier that references a specific workflow version across all Atlas subsystems. | This RFC |

---

## 2 Versioning Overview

The Workflow Versioning specification defines how workflow definitions and instances are versioned throughout their lifecycle. Versioning ensures traceability, enables safe evolution, and supports backward-compatible upgrades.

Key principles:

- Every workflow definition version MUST be immutable once published.
- Versions follow Semantic Versioning 2.0.0 (SEMVER) conventions adapted for workflow specifications.
- Version changes MUST be documented in version metadata.
- Running workflow instances MUST NOT be affected by workflow definition version changes unless explicitly migrated.
- Version compatibility MUST be verified at validation time per RFC-0317.

---

## 3 Version Model

### 3.1 Semantic Versioning

Workflow versions follow the MAJOR.MINOR.PATCH format:

| Component | Increment When | Backward Compatible |
|---|---|---|
| MAJOR | Incompatible API or graph model changes | NO |
| MINOR | Backward-compatible feature additions | YES (to previous MINOR) |
| PATCH | Backward-compatible bug fixes | YES (to all previous versions) |

### 3.2 Pre-Release and Build Metadata

Pre-release versions MAY include a hyphen-separated pre-release identifier (e.g., 1.0.0-alpha.1). Build metadata MAY be appended with a plus sign (e.g., 1.0.0+build.123) and MUST NOT affect version precedence.

### 3.3 Version Lifecycle States

| State | Description | Transitions |
|---|---|---|
| Draft | Version is being developed and is not published | Any -> Draft |
| Published | Version is released and available for use | Draft -> Published |
| Deprecated | Version is superseded but still supported | Published -> Deprecated |
| Retired | Version is no longer supported | Deprecated -> Retired |
| Archived | Version is preserved for historical reference | Retired -> Archived |

---

## 4 Version Metadata

Every workflow version MUST include the following metadata:

| Field | Type | Required | Description |
|---|---|---|---|
| version | String | YES | Semantic version string |
| published_at | Timestamp | YES | ISO 8601 publication timestamp |
| author | String | YES | Author or team identifier |
| changelog | String | YES | Human-readable change description |
| breaking_changes | Array[String] | Conditional | List of breaking change identifiers (required if MAJOR incremented) |
| migration_guide | String | Conditional | Path to migration guide (required if MAJOR incremented) |
| compliance_status | Object | YES | Compliance validation results per RFC-0330 |
| deprecated_at | Timestamp | Conditional | Deprecation timestamp (required if Deprecated) |
| superseded_by | String | Conditional | Version that supersedes this one |

---

## 5 Version Resolution

### 5.1 Resolution Order

When a workflow references a version range, the resolver MUST select the highest matching version according to this order:

1. Exact version match (e.g., 1.2.3)
2. Caret range (e.g., ^1.2.0 resolves to highest 1.x.x)
3. Tilde range (e.g., ~1.2.0 resolves to highest 1.2.x)
4. Latest stable version (if no range specified)

### 5.2 Resolution Constraints

- Resolved versions MUST be Published or later in the version lifecycle state.
- Resolved versions MUST pass all validation rules per RFC-0317.
- Resolved versions MUST be compatible with the target runtime per RFC-0329.

---

## 6 Deprecation and Migration

### 6.1 Deprecation Process

When a workflow version is deprecated:

1. The deprecation MUST be announced with at least one minor version advance.
2. A migration guide MUST be provided.
3. The deprecated version MUST continue to function without modification for a minimum of two minor releases.
4. All deprecated features MUST be logged in the observability system per RFC-0321.

### 6.2 Migration Process

Migration from version N to version M MUST:

1. Validate that the target version is compatible with the current runtime.
2. Preserve all running workflow instances until explicit migration is confirmed.
3. Update version references atomically per RFC-0328 serialization.
4. Record the migration event in the audit trail per RFC-0321.

---

## 7 Layer Boundaries

### 7.1 Responsibilities

This specification IS responsible for:
- Defining the semantic versioning model for workflow definitions.
- Specifying the version lifecycle states and transitions.
- Defining version metadata requirements.
- Establishing version resolution and deprecation processes.

### 7.2 Non-Responsibilities

This specification IS NOT responsible for:
- Executing migrations (handled by Workflow Runtime, RFC-0304).
- Persisting version metadata (handled by Workflow Storage, RFC-0324).
- Observing version events (handled by Workflow Observability, RFC-0321).
- Validating version compatibility (handled by Workflow Compatibility, RFC-0329).

### 7.3 Dependencies

| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides the version concept |
| RFC-0304 | Consumed | Workflow Runtime provides execution gating |`n| RFC-0312 | Consumed | Workflow Scheduler provides scheduling version constraints
| RFC-0317 | Consumed | Workflow Validation provides version validation rules |
| RFC-0324 | Consumed | Workflow Storage provides version persistence |
| RFC-0328 | Consumed | Workflow Serialization provides version encoding |
| RFC-0329 | Consumed | Workflow Compatibility provides compatibility model |
| RFC-0330 | Consumed | Workflow Compliance provides compliance status |`n| RFC-0316 | Consumed | Workflow Debugging provides debug version tracking

### 7.4 Consumers
- Workflow Runtime (RFC-0304): Uses version metadata for execution decisions.
- Workflow Serialization (RFC-0328): Encodes version information.
- Workflow Compatibility (RFC-0329): Checks version compatibility.

### 7.5 Providers
- Version Metadata Schema (schemas/workflow/version-metadata.json): Provides the metadata format contract.
- Versioning Catalog (catalog/workflow-versioning.md): Provides the version lifecycle catalog.

### 7.6 Forbidden Dependencies
- This specification MUST NOT depend on any external versioning system (npm, PyPI, etc.).
- This specification MUST NOT assume a particular version control system (Git, SVN, etc.).

---

## 8 Security

- Version metadata MUST be signed to prevent tampering.
- Only authorized actors MAY publish or deprecate versions.
- Archived versions MUST be immutable and read-only.

---

## 9 Performance

- Version resolution MUST complete within 10ms.
- Version metadata lookup MUST complete within 1ms.
- Version comparison (precedence) MUST complete within 100ns.

---

## 10 Compatibility

- Minor and patch versions MUST be backward compatible with all previous versions in the same major version.
- Major version changes MUST include a migration guide and maintain the old version for at least two minor releases.
- Pre-release versions MUST NOT be used in production deployments.

---

## 11 Compliance

- All version transitions MUST be recorded in the audit trail.
- Deprecated versions MUST be reported in compliance reports per RFC-0330.
- Version metadata MUST include compliance validation results.

---

## 12 Future Evolution

- **Semantic Versioning for Workflow Instances**: Version tracking for individual workflow instances alongside definition versions.
- **Distributed Version Resolution**: Consensus-based version resolution for multi-region deployments.
- **Automated Migration**: AI-assisted migration planning and execution.
- **Version Pinning**: Support for immutable version pinning in production environments.

---

## 13 Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

---

## 14 Acceptance Criteria

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST support semantic versioning with MAJOR.MINOR.PATCH format. | Version parsing test |
| AC-02 | The implementation MUST enforce five version lifecycle states. | State machine test |
| AC-03 | The implementation MUST include all required version metadata fields. | Metadata validation test |
| AC-04 | The implementation MUST resolve version ranges according to the specified priority order. | Resolution test |
| AC-05 | The implementation MUST enforce a minimum two-minor-release deprecation period. | Deprecation test |
| AC-06 | The implementation MUST record all version transitions in the audit trail. | Audit trail test |

---

## 15 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0302 | Workflow Language (version in graph definitions) |
| RFC-0304 | Workflow Runtime (version-based execution gating) |`n| RFC-0312 | Workflow Scheduler (scheduling version constraints)
| RFC-0317 | Workflow Validation (version validation rules) |
| RFC-0324 | Workflow Storage (version persistence) |
| RFC-0328 | Workflow Serialization (version encoding) |
| RFC-0329 | Workflow Compatibility (compatibility model) |
| RFC-0330 | Workflow Compliance (compliance status) |`n| RFC-0316 | Workflow Debugging (debug version tracking)
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/version-metadata.json | Version Metadata JSON Schema |
| catalog/workflow-versioning.md | Versioning Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0318 (this document), RFC-0329 (Compatibility), RFC-0328 (Serialization) |
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
