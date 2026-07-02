RFC: RFC-0332
Title: Workflow Migration
Status: Proposed
## Terminology

The following terms are defined in the Atlas Master Glossary (RFC-0301) and are used throughout this specification with the exact meanings given below. Where this specification refines a term from RFC-0301, the refinement is noted.

| Term | Definition |
|---|---|
| Migration | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Upgrade | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Rollback | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Forward Compatibility | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Backward Compatibility | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Data Migration | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Schema Migration | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Zero-Downtime Migration | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Canary Deployment | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |
| Blue-Green Deployment | Defined in RFC-0301 and refined in this specification. See the authoritative RFC for the precise definition. |

---

Version: 1.0.0
Author: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADS Version: 1.x.x
Spec Version: 1.x.x
Normative: YES
Depends On:
  - RFC-0301 Workflow Overview
  - RFC-0303 Workflow Execution
  - RFC-0304 Workflow Runtime
  - RFC-0315 Workflow Recovery
  - RFC-0317 Workflow Validation
  - RFC-0318 Workflow Versioning
  - RFC-0319 Workflow Security
  - RFC-0324 Workflow Storage
  - RFC-0328 Workflow Serialization
  - RFC-0329 Workflow Compatibility
  - RFC-0330 Workflow Compliance
Supersedes: None
Superseded By: None
Related ADR:
  - ADR-0012 Contract-First Specification-Driven Development
Related JSON Schema:
  - schemas/workflow/migration-plan.json
  - schemas/workflow/migration-result.json
Related Catalog:
  - catalog/workflow-versioning.md
  - catalog/workflow-status.md
Audience: All Implementation Teams
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

## Normative Status
This specification is Normative. Every Atlas subsystem MUST conform to the migration requirements defined in this document.

---

## Authority
This RFC is the authoritative specification for Workflow Migration.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Migration | The process of transitioning workflow definitions and instances from one version to another. | This RFC |
| Upgrade | Migration from an older version to a newer version. | This RFC |
| Rollback | Migration from a newer version back to an older version. | This RFC |
| Backward Compatibility | Ability of a newer version to process data from an older version. | RFC-0329 |
| Forward Compatibility | Ability of an older version to handle data from a newer version. | RFC-0329 |
| Migration Plan | A structured document describing the steps, validations, and rollback procedures for a migration. | This RFC |
| Migration Dry Run | A non-destructive test of the migration plan against a copy of the data. | This RFC |
| Migration Checkpoint | A saved state during migration enabling pause/resume/rollback. | This RFC |
| Migration Atomicity | The guarantee that migration either completes fully or rolls back completely. | This RFC |
| Schema Drift | Divergence between expected and actual data schema during migration. | This RFC |

## 2 Migration Overview

The Workflow Migration specification defines how workflow definitions and instances are migrated across specification versions. Migration ensures safe, reversible, and verifiable transitions between versions.

Key principles:

- Every migration MUST be atomic: it either completes fully or rolls back completely.
- Every migration MUST be reversible: rollback MUST restore the previous state identically.
- Every migration MUST be dry-run capable: non-destructive testing is supported.
- Every migration MUST preserve data integrity: no data loss or corruption during transition.
- Every migration MUST be auditable: all migration events recorded in the audit trail.
- Every migration MUST maintain compatibility: backward and forward compatibility rules enforced.

## 3 Migration Phases

### 3.1 Phase Definitions

| Phase | Description | Gate |
|---|---|---|
| Planning | Create migration plan with steps, validations, and rollback procedures | Plan approval |
| Dry Run | Execute migration on a copy to verify correctness | Dry run success |
| Backup | Create pre-migration backup of all affected data | Backup verification |
| Execute | Perform migration on production data | Atomicity guarantee |
| Validate | Verify post-migration correctness | Validation success |
| Cleanup | Remove migration artifacts and dry-run copies | Cleanup verification |

### 3.2 Migration Plan Structure

| Field | Type | Required | Description |
|---|---|---|---|
| plan_id | String | YES | Unique migration plan identifier |
| source_version | String | YES | Version being migrated from |
| target_version | String | YES | Version being migrated to |
| steps | Array[Step] | YES | Ordered migration steps |
| validations | Array[Validation] | YES | Post-step validation rules |
| rollback_steps | Array[Step] | YES | Corresponding rollback steps |
| estimated_duration_ms | Integer | YES | Expected migration duration |
| max_rollback_time_ms | Integer | YES | Maximum time to complete rollback |
| affected_workflows | Array[String] | YES | List of workflow IDs affected |
| affected_instances | Array[String] | Conditional | List of running instance IDs |

## 4 Upgrade Procedures

### 4.1 Minor Version Upgrade

Minor version upgrades (X.Y.Z to X.(Y+1).Z) are backward compatible:

1. New features MAY be introduced.
2. Existing features MUST NOT be removed or altered.
3. Running instances continue without interruption.
4. New definitions use the new version.
5. Migration plan MUST be approved but dry run is OPTIONAL.

### 4.2 Major Version Upgrade

Major version upgrades (X.Y.Z to (X+1).0.Z) may introduce breaking changes:

1. Breaking changes MUST be documented in the migration plan.
2. A deprecation period of at least two minor versions MUST elapse before removal.
3. Migration plan MUST include rollback steps for every forward step.
4. Dry run MUST be completed successfully before production execution.
5. Running instances MUST be migrated individually with checkpoint preservation.

## 5 Rollback Procedures

### 5.1 Rollback Triggers

Rollback MUST be triggered when:

- Validation fails after any migration step.
- Data integrity check reveals corruption.
- Performance degrades beyond acceptable threshold (>50% increase in latency).
- Security validation reveals a vulnerability.
- Manual abort is requested by an authorized operator.

### 5.2 Rollback Guarantees

- Rollback MUST restore the system to the exact pre-migration state.
- Rollback MUST complete within the declared max_rollback_time_ms.
- Rollback MUST NOT require human intervention unless the migration plan specifies it.
- Rollback events MUST be recorded in the audit trail.

## 6 Layer Boundaries

### 6.1 Responsibilities
This specification IS responsible for: defining the migration process model, specifying migration plan structure, establishing upgrade and rollback procedures, and defining migration verification requirements.

### 6.2 Non-Responsibilities
This specification IS NOT responsible for: implementing specific migration tools (infrastructure concern), executing migrations (delegated to RFC-0304), or persisting migration state (delegated to RFC-0324).

### 6.3 Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0301 | Consumed | Workflow Overview provides foundational concepts |
| RFC-0303 | Consumed | Workflow Execution provides execution context |
| RFC-0304 | Consumed | Workflow Runtime executes migration |
| RFC-0315 | Consumed | Workflow Recovery provides checkpoint model |
| RFC-0317 | Consumed | Workflow Validation provides validation rules |
| RFC-0318 | Consumed | Workflow Versioning provides version model |
| RFC-0319 | Consumed | Workflow Security provides security constraints |
| RFC-0324 | Consumed | Workflow Storage provides state persistence |
| RFC-0328 | Consumed | Workflow Serialization provides data encoding |
| RFC-0329 | Consumed | Workflow Compatibility provides compatibility model |
| RFC-0330 | Consumed | Workflow Compliance provides compliance verification |

### 6.4 Consumers
- Workflow Runtime (RFC-0304): Executes migration steps.
- Workflow Versioning (RFC-0318): Manages version transitions.
- Workflow Compatibility (RFC-0329): Verifies compatibility during migration.

### 6.5 Providers
- Migration Plan Schema (schemas/workflow/migration-plan.json): Provides plan format contract.
- Migration Result Schema (schemas/workflow/migration-result.json): Provides result format contract.

### 6.6 Forbidden Dependencies
- This specification MUST NOT depend on any specific CI/CD toolchain.
- This specification MUST NOT assume a particular deployment strategy (blue-green, canary, rolling).

## 7 Security
- Migration plans MUST be authorized per the permission model (RFC-0319).
- Migration data MUST be encrypted in transit and at rest.
- Rollback operations MUST be logged as security events.

## 8 Performance
- Migration dry run MUST complete within 10x the estimated production migration time.
- Rollback MUST complete within the declared max_rollback_time_ms.
- Migration validation MUST complete within 1 minute per 1,000 affected workflows.

## 9 Compatibility
- Backward compatibility MUST be maintained within a major version.
- Forward compatibility MUST be supported for one minor version ahead.
- Breaking changes require a major version bump and migration plan.

## 10 Compliance
- All migration events MUST be recorded in the audit trail per RFC-0321.
- Migration compliance MUST be verified per RFC-0330.
- Migration reports MUST be exportable for regulatory audits.

## 11 Future Evolution
- **Automated Migration Planning**: ML-assisted migration plan generation.
- **Zero-Downtime Migration**: Live migration without service interruption.
- **Cross-Platform Migration**: Migration between different Atlas deployment platforms.
- **Incremental Migration**: Migrate workflows one at a time without full-system downtime.
- **Migration Simulation**: Full simulation of migration impact before execution.

## 12 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any deployment strategy (blue-green, canary, rolling, etc.)

## 13 Acceptance Criteria

### 13.1 Migration Process

| # | Criterion | Verification Method |
|---|---|---|

### 13.2 Rollback

| # | Criterion | Verification Method |
|---|---|---|

### 13.3 Upgrade

| # | Criterion | Verification Method |
|---|---|---|

## 14 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (migration execution context) |
| RFC-0304 | Workflow Runtime (migration execution) |
| RFC-0315 | Workflow Recovery (checkpoint model) |
| RFC-0317 | Workflow Validation (validation rules) |
| RFC-0318 | Workflow Versioning (version model) |
| RFC-0319 | Workflow Security (authorization) |
| RFC-0324 | Workflow Storage (state persistence) |
| RFC-0328 | Workflow Serialization (data encoding) |
| RFC-0329 | Workflow Compatibility (compatibility model) |
| RFC-0330 | Workflow Compliance (compliance verification) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/migration-plan.json | Migration Plan JSON Schema |
| schemas/workflow/migration-result.json | Migration Result JSON Schema |
| catalog/workflow-versioning.md | Versioning Catalog |
| catalog/workflow-status.md | Status Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0332 (this document), RFC-0331 (Testing), RFC-0333 (SDK) |

## 15 Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0301, RFC-0303, RFC-0304, RFC-0315, RFC-0317, RFC-0318, RFC-0319, RFC-0324, RFC-0328, RFC-0329, RFC-0330 |
| Related ADR | ADR-0012 |
| Related JSON Schema | schemas/workflow/migration-plan.json, schemas/workflow/migration-result.json |
| Related Catalog | catalog/workflow-versioning.md, catalog/workflow-status.md |

## 16 Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |





