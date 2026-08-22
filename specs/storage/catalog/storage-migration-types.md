---
id: ATLAS-STORAGE-CATALOG-MIGRATION-TYPES
title: Storage Migration Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Migration Types Catalog

## 1. Purpose

This catalog defines the canonical migration types used by the Atlas Storage subsystem for schema evolution, data transformation, provider replacement, and system upgrades.

## 2. Migration Type Catalog

| Migration ID | Name | Description | Reversible | Atomic | RFC Reference | Staging Required | Validation Steps |
|---|---|---|---|---|---|---|---|
| MIG-SCHEMA-FWD | Schema Forward | Evolve schema to a newer version. | No | Yes | RFC-0408 | Pre, Post |
| MIG-SCHEMA-BWD | Schema Backward | Revert schema to an older version. | Yes | Yes | RFC-0408 | Pre, Post |
| MIG-SCHEMA-BIDI | Schema Bi-Directional | Support both old and new schema simultaneously. | Yes | Partial | RFC-0408 | Pre, Mid, Post |
| MIG-DATA-TRANSFORM | Data Transform | Transform data values without schema change. | Yes | Yes | RFC-0408 | Pre, Post |
| MIG-DATA-MIGRATE | Data Migrate | Move data between storage locations. | Yes | Yes | RFC-0408 | Pre, Post |
| MIG-PROVIDER-SWAP | Provider Swap | Replace the backing storage provider. | Yes | Yes | RFC-0408 | Pre, Mid, Post |
| MIG-HYBRID | Hybrid | Combined schema and data migration. | Partial | Partial | RFC-0408 | Pre, Mid, Post |
| MIG-CANARY | Canary | Gradual rollout to a subset of data. | Yes | Yes | RFC-0408 | Pre, Mid, Post |
| MIG-BLUE-GREEN | Blue-Green | Dual-environment zero-downtime migration. | Yes | Yes | RFC-0408 | Pre, Switch, Post |
| MIG-ZERO-DOWN | Zero Downtime | Migration with no service interruption. | Yes | Yes | RFC-0408 | Pre, Post |
| MIG-REVERSE | Reverse | Rollback a completed migration. | Yes | Yes | RFC-0408 | Pre, Post |
| MIG-ROLLBACK | Rollback | Emergency revert due to migration failure. | Yes | Yes | RFC-0408 | Post |
| MIG-DRY-RUN | Dry Run | Simulate migration without applying changes. | N/A | N/A | RFC-0408 | None |
| MIG-VALIDATE-ONLY | Validate Only | Check migration compatibility without executing. | N/A | N/A | RFC-0408 | None |

## 3. Migration Staging Model

| Stage | Description | Enter Condition | Exit Condition |
|---|---|---|---|
| STAGE-PLANNED | Migration is defined but not yet initiated. | Migration request submitted. | STAGE-STAGING |
| STAGE-STAGING | Data is copied to a staging area. | Pre-validation passes. | STAGE-VALIDATING |
| STAGE-VALIDATING | Staged data is validated against target schema. | Staging complete. | STAGE-APPLYING or STAGE-ABORTING |
| STAGE-APPLYING | Changes are atomically applied to production. | Validation passes. | STAGE-COMPLETED or STAGE-ROLLBACK |
| STAGE-COMPLETED | Migration finished successfully. | Apply phase complete. | STAGE-CLEANUP |
| STAGE-ROLLBACK | Migration failed; reverting to original state. | Apply phase fails. | STAGE-COMPLETED or STAGE-FAILED |
| STAGE-FAILED | Migration terminated with unrecoverable error. | Rollback fails or is skipped. | None (terminal) |
| STAGE-CLEANUP | Staging area is removed. | Apply or Rollback complete. | STAGE-PLANNED |

## 4. Validation Rules

1. Every migration type identifier MUST match the regex ^MIG-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$.
2. Migration types MUST be selected exclusively from this catalog.
3. Reversible migrations MUST include a documented rollback procedure.
4. Atomic migrations MUST guarantee all-or-nothing semantics.
5. Staging stages MUST follow the ordered progression in Section 3.
6. Dry-run migrations MUST produce a migration plan without side effects.
