---
id: ATLAS-STORAGE-CATALOG-QUOTA
title: Storage Quota Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Quota Types Catalog

## 1. Purpose

This catalog defines the canonical set of quota types and enforcement modes used by the Atlas Storage subsystem for enterprise resource governance.

## 2. Quota Type Prefix

All quota type identifiers use the prefix QT-.

## 3. Complete Quota Type Catalog

| Quota ID | Name | Unit | Description | Enforcement Scope | RFC Reference |
|---|---|---|---|---|---|
| QT-DISK | Disk Storage | bytes | Total persistent storage consumption | Namespace, Tenant | RFC-0424 |
| QT-MEMORY | Cache Memory | bytes | In-memory cache allocation | Provider, Namespace | RFC-0410 |
| QT-BLOB | Binary Large Object | bytes | Blob and binary storage consumption | Namespace | RFC-0423 |
| QT-SNAPSHOT | Snapshot Count | count | Maximum number of snapshots | Resource Type | RFC-0407 |
| QT-SNAPSHOT-SIZE | Snapshot Size | bytes | Total snapshot storage consumption | Namespace | RFC-0407 |
| QT-BACKUP | Backup Storage | bytes | Backup data storage consumption | Domain | RFC-0411 |
| QT-CACHE-ENTRIES | Cache Entry Count | count | Maximum cache entries | Provider | RFC-0410 |
| QT-OPERATIONS | Operations | ops/sec | Maximum operations per second | Namespace, Tenant | RFC-0415 |
| QT-CONNECTIONS | Connections | count | Maximum concurrent connections | Provider | RFC-0403 |
| QT-ENTITIES | Entity Count | count | Total managed entities | Namespace | RFC-0404 |
| QT-BANDWIDTH | Bandwidth | bytes/sec | Data transfer rate limit | Provider | RFC-0418 |

## 4. Quota Enforcement Modes

| Mode | Description | Behavior on Breach | RFC Reference |
|---|---|---|---|
| HARD | Absolute limit | Operation rejected with STOR-CAP-EXCEEDED | RFC-0424 |
| SOFT | Advisory limit | Warning event emitted; operation allowed | RFC-0424 |
| GRACE | Soft with grace period | Allows breach for configured duration | RFC-0424 |
| THROTTLE | Rate limiting | Operations delayed but not rejected | RFC-0424 |

## 5. Quota Hierarchy Levels

| Level | Scope | Inherited From | RFC Reference |
|---|---|---|---|
| SYSTEM | Entire Storage subsystem | N/A | RFC-0424 |
| DOMAIN | Per domain (runtime, plugin, etc.) | SYSTEM | RFC-0421 |
| NAMESPACE | Per namespace path | DOMAIN | RFC-0422 |
| TENANT | Per multi-tenant tenant | NAMESPACE | RFC-0409 |
| RESOURCE | Per resource type | TENANT | RFC-0423 |

## 6. Validation Rules

1. Every quota type identifier MUST match the regex ^QT-[A-Z][A-Z0-9]*$.
2. Quota values MUST be non-negative integers.
3. HARD quotas MUST reject operations with appropriate error codes.
4. SOFT quotas MUST emit warning events per RFC-0413.
5. Quota utilization MUST be reported via metrics per RFC-0414.
