---
id: ATLAS-STORAGE-CATALOG-CAPABILITY-FLAGS
title: Storage Capability Flags Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Capability Flags Catalog

## 1. Purpose

This catalog defines the canonical set of capability flags that Storage Providers declare to enable capability-based discovery and negotiation.

## 2. Flag Prefix

All capability flag identifiers use the prefix CF-.

## 3. Complete Capability Flags Catalog

| Flag ID | Flag Name | Description | Required for Baseline | RFC Reference |
|---|---|---|---|---|
| CF-TX | supports_transactions | Provider supports atomic transactions | Yes | RFC-0425 |
| CF-SNAPSHOT | supports_snapshot | Provider supports point-in-time snapshots | No | RFC-0425 |
| CF-COMPRESSION | supports_compression | Provider supports data compression | No | RFC-0425 |
| CF-ENCRYPTION | supports_encryption | Provider supports encryption at rest | Yes | RFC-0425 |
| CF-REPLICATION | supports_replication | Provider supports data replication | No | RFC-0425 |
| CF-CACHE | supports_cache | Provider supports cache integration | Yes | RFC-0425 |
| CF-STREAMING | supports_streaming | Provider supports streaming read/write | No | RFC-0425 |
| CF-INDEX | supports_index | Provider supports indexed queries | No | RFC-0425 |
| CF-VERSIONING | supports_versioning | Provider supports document versioning | Yes | RFC-0425 |
| CF-LOCKING | supports_locking | Provider supports concurrency locking | No | RFC-0425 |
| CF-BACKUP | supports_backup | Provider supports backup operations | Yes | RFC-0425 |
| CF-RECOVERY | supports_recovery | Provider supports recovery procedures | Yes | RFC-0425 |
| CF-SCHEMA-EVOLUTION | supports_schema_evolution | Provider supports schema changes | Yes | RFC-0425 |
| CF-MULTI-TENANCY | supports_multi_tenancy | Provider supports tenant isolation | No | RFC-0425 |
| CF-AUDIT | supports_audit | Provider supports audit logging | Yes | RFC-0425 |
| CF-QUERY | supports_query | Provider supports structured queries | No | RFC-0425 |
| CF-SCAN | supports_scan | Provider supports sequential scan | Yes | RFC-0425 |
| CF-BATCH | supports_batch | Provider supports batch operations | No | RFC-0425 |
| CF-NESTED-TX | supports_nested_transactions | Provider supports nested transaction scopes | No | RFC-0425 |
| CF-DIST-COMMIT | supports_distributed_commit | Provider supports two-phase commit | No | RFC-0425 |

## 4. Capability Declaration Format

Providers MUST declare capabilities at initialization time using the following structure:

| Field | Type | Description |
|---|---|---|
| provider_id | String | Unique provider identifier |
| provider_type | Enum | One of the provider types from storage-providers.md |
| capabilities | Array | List of declared capability flags |
| capability_versions | Map | Version per capability flag |
| declared_at | Timestamp | ISO 8601 declaration timestamp |

## 5. Validation Rules

1. Every capability flag identifier MUST match the regex ^CF-[A-Z][A-Z0-9]*$.
2. Providers MUST declare all baseline-required capabilities.
3. Capability flags MUST be immutable once declared for a provider instance.
4. Capability version strings MUST follow semantic versioning.
5. Capability queries MUST return results within 100ms per RFC-0415.
