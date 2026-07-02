---
id: ATLAS-STORAGE-CATALOG-VERSIONING
title: Storage Versioning Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Versioning Catalog

## 1. Purpose

This catalog defines the canonical versioning strategies and snapshot strategies used by the Atlas Storage subsystem for document and schema version management.

## 2. Version Strategy Catalog

| Strategy ID | Name | Description | Collision Resistance | Branch Support | RFC Reference | Example Format |
|---|---|---|---|---|---|---|
| VER-SEQ | Sequential | Monotonically increasing integer counter. | Low | No | RFC-0407 | v1, v2, v3 |
| VER-BRANCH | Branch-Prefixed | Counter prefixed with branch identifier. | Medium | Yes | RFC-0407 | main-1, dev-3 |
| VER-TS | Timestamp-Based | Epoch timestamp with nanosecond precision. | High | No | RFC-0407 | 1719820800000000000 |
| VER-SEMANTIC | Semantic | SemVer-compliant version string. | High | Yes | RFC-0407 | 1.2.3, 2.0.0-beta |
| VER-HASH | Hash-Derived | Content-addressable hash identifier. | Maximum | No | RFC-0407 | sha256:a1b2c3d4 |
| VER-MONO | Monotonically Increasing | Globally unique incrementing counter. | High | Yes | RFC-0407 | 0000000001, 0000000002 |

## 3. Resolution Strategy Catalog

| Resolution ID | Name | Description | RFC Reference |
|---|---|---|---|
| RES-LATEST | Latest | Returns the most recent version. | RFC-0407 |
| RES-SPECIFIC | Specific | Returns the version identified by exact ID. | RFC-0407 |
| RES-TIMESTAMP | Timestamp | Returns the version closest to the given time. | RFC-0407 |
| RES-BRANCH | Branch | Returns the latest version on a named branch. | RFC-0407 |
| RES-PARENT | Parent | Returns the parent version in the version chain. | RFC-0407 |

## 4. Storage Strategy Catalog

| Storage ID | Name | Description | Overhead | RFC Reference |
|---|---|---|---|---|
| STR-FULL | Full | Stores complete copy of each version. | High | RFC-0407 |
| STR-DELTA | Delta | Stores only the difference from previous version. | Low | RFC-0407 |
| STR-HYBRID | Hybrid | Full snapshots at intervals with deltas between. | Medium | RFC-0407 |
| STR-INCREMENTAL | Incremental | Stores only changes since last backup. | Low | RFC-0407 |
| STR-CUMULATIVE | Cumulative | Full snapshot since last full backup. | Medium | RFC-0407 |

## 5. Pruning Policy Catalog

| Policy ID | Name | Description | RFC Reference |
|---|---|---|---|
| PRUNE-AGE | Age-Based | Prunes versions older than N days. | RFC-0407 |
| PRUNE-COUNT | Count-Based | Retains only the N most recent versions. | RFC-0407 |
| PRUNE-HYBRID | Hybrid | Combination of age and count limits. | RFC-0407 |
| PRUNE-MANUAL | Manual | Versions pruned only by operator action. | RFC-0407 |

## 6. Validation Rules

1. Every version strategy identifier MUST match the regex ^VER-[A-Z]+$.
2. Every resolution strategy identifier MUST match the regex ^RES-[A-Z]+$.
3. Every storage strategy identifier MUST match the regex ^STR-[A-Z]+$.
4. Version identifiers MUST be globally unique within a resource namespace.
5. Pruning policies MUST NOT remove versions that are referenced by active transactions.
6. Branch-prefixed versions MUST include the branch name as a manifest field.
