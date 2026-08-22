---
id: ATLAS-STORAGE-CATALOG-RESOURCE-LIFECYCLE
title: Storage Resource Lifecycle by Type Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Resource Lifecycle by Type Catalog

## 1. Purpose

This catalog defines the resource-type-specific lifecycle policies that extend the generic resource lifecycle from storage-lifecycle.md.

## 2. Resource Type Lifecycle Catalog

| Resource Type | Initial State | Active State | Archive Trigger | Purge Trigger | RFC Reference |
|---|---|---|---|---|---|
| Document | Stored | Active | 90 days inactive | Manual or retention policy | RFC-0423 |
| Blob | Stored | Active | N/A (never archived) | Manual or quota pressure | RFC-0423 |
| Binary | Stored | Active | N/A (never archived) | Manual or quota pressure | RFC-0423 |
| Manifest | Stored | Active | On resource deletion | Linked to resource lifecycle | RFC-0423 |
| Metadata | Stored | Active | On resource deletion | Linked to resource lifecycle | RFC-0423 |
| Snapshot | Stored | Active | 365 days old | Retention policy | RFC-0423 |
| Index | Stored | Active | On schema change | Rebuilt automatically | RFC-0423 |
| Cache | Stored | Active | TTL expiry | Eviction policy | RFC-0423 |
| Secret | Stored | Active | On key rotation | Manual rotation | RFC-0423 |
| Certificate | Stored | Active | On expiry | Auto-renewal or manual | RFC-0423 |
| Log | Stored | Active | 365 days old | Retention policy | RFC-0423 |
| Asset | Stored | Active | 180 days inactive | Manual | RFC-0423 |
| Model | Stored | Active | On model update | Manual | RFC-0423 |
| Image | Stored | Active | 180 days inactive | Manual or quota | RFC-0423 |
| Video | Stored | Active | 90 days inactive | Manual or quota | RFC-0423 |
| OCR | Stored | Active | 30 days old | Manual | RFC-0423 |
| Workflow | Stored | Active | On workflow completion | 30 days after completion | RFC-0423 |

## 3. Lifecycle State Mapping

Each resource type maps to the generic states defined in storage-lifecycle.md:

| Generic State | Document | Blob | Secret | Log |
|---|---|---|---|---|
| Created | On write | On write | On write | On append |
| Validating | Schema check | N/A | Key check | N/A |
| Stored | After validation | After write | After encryption | After append |
| Active | Ready for use | Ready for use | Ready for decrypt | Ready for read |
| Updating | On modification | On overwrite | On rotation | N/A |
| Archived | After inactivity | N/A | On rotation | After retention |
| Deleting | On purge request | On purge request | On rotation | On purge |
| Purged | Irrecoverable | Irrecoverable | Irrecoverable | Irrecoverable |

## 4. Validation Rules

1. Every resource type MUST have a defined lifecycle policy.
2. Resource types with permanent retention MUST NOT have purge triggers.
3. Lifecycle transitions MUST produce events per RFC-0413.
4. Archive and purge triggers MUST be configurable per tenant.
