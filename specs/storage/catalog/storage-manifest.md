---
id: ATLAS-STORAGE-CATALOG-MANIFEST
title: Storage Manifest Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Manifest Catalog

## 1. Purpose

This catalog defines the canonical Storage manifest structure that providers and consumers use to discover, negotiate, and operate with the Storage subsystem.

## 2. Manifest Structure

Every Storage manifest MUST include the following top-level fields:

| Field | Type | Required | Description |
|---|---|---|---|
| storage_id | UUID | YES | Unique Storage subsystem identifier |
| storage_version | String | YES | Semantic version of the Storage implementation |
| provider_type | Enum | YES | Provider type from storage-providers.md |
| provider_id | String | YES | Provider instance identifier |
| capabilities | Array | YES | Declared capability flags from storage-capability-flags.md |
| consistency_model | Enum | YES | Default consistency model |
| quota | Object | NO | Quota configuration from storage-quota.md |
| encryption | Object | YES | Encryption configuration |
| compression | Enum | NO | Compression algorithm |
| extensions | Array | NO | Registered extension point IDs |
| namespace_root | String | YES | Root namespace path |
| domain_scope | Array | YES | Managed domain IDs |
| health_state | Enum | YES | Current health state from storage-health.md |
| initialized_at | Timestamp | YES | Initialization timestamp |
| last_updated | Timestamp | YES | Last update timestamp |

## 3. Encryption Configuration

| Field | Type | Description |
|---|---|---|
| algorithm | Enum | Encryption algorithm identifier |
| key_id | String | Encryption key identifier |
| key_rotation_days | Integer | Key rotation interval |
| in_transit | Boolean | Whether in-transit encryption is enabled |

## 4. Quota Configuration

| Field | Type | Description |
|---|---|---|
| disk_bytes | Integer | Disk quota limit |
| memory_bytes | Integer | Memory quota limit |
| operations_per_sec | Integer | Operation rate limit |
| entity_count | Integer | Entity count limit |

## 5. Validation Rules

1. Every manifest MUST include all REQUIRED fields.
2. Capability arrays MUST reference only flags from storage-capability-flags.md.
3. Domain scopes MUST reference only domains from storage-domains.md.
4. Health state MUST be one of the values from storage-health.md.
5. Manifests MUST be refreshed at least every provider heartbeat interval.
