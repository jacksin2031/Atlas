---
id: ATLAS-STORAGE-CATALOG-PERMISSIONS
title: Storage Permissions Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Permissions Catalog

## 1. Purpose

This catalog defines the canonical set of permission names used by the Atlas Storage subsystem for access control. Permissions govern which operations a principal MAY perform on storage resources.

## 2. Permission ID Prefix

All permission identifiers use the prefix PERM-STOR-.

## 3. Complete Permission Catalog

| Permission ID | Name | Description | Required Role | RFC Reference | Dependencies |
|---|---|---|---|---|---|
| PERM-STOR-READ | Storage Read | Read resource data. | Viewer | RFC-0409 | None |
| PERM-STOR-WRITE | Storage Write | Create or update resources. | Editor | PERM-STOR-READ |
| PERM-STOR-DELETE | Storage Delete | Remove resources. | Editor | PERM-STOR-READ |
| PERM-STOR-LIST | Storage List | Enumerate resources. | Viewer | None |
| PERM-STOR-SCAN | Storage Scan | Sequential iteration over all resources. | Viewer | PERM-STOR-LIST |
| PERM-STOR-QUERY | Storage Query | Execute structured queries. | Analyst | PERM-STOR-LIST |
| PERM-STOR-BACKUP | Storage Backup | Create backups. | Operator | PERM-STOR-READ |
| PERM-STOR-RESTORE | Storage Restore | Restore from backups. | Operator | PERM-STOR-BACKUP |
| PERM-STOR-MIGRATE | Storage Migrate | Run schema or data migrations. | Admin | PERM-STOR-WRITE |
| PERM-STOR-VERSION | Storage Version | Manage resource versions. | Editor | PERM-STOR-WRITE |
| PERM-STOR-LOCK | Storage Lock | Acquire or release locks. | Operator | PERM-STOR-WRITE |
| PERM-STOR-REPLICATE | Storage Replicate | Configure replication topology. | Admin | PERM-STOR-RESTORE |
| PERM-STOR-OBSERVE | Storage Observe | View metrics and traces. | Viewer | None |
| PERM-STOR-EXTEND | Storage Extend | Register custom extensions. | Admin | None |
| PERM-STOR-ENCRYPT | Storage Encrypt | Manage encryption keys. | Security Officer | None |
| PERM-STOR-CLASSIFY | Storage Classify | Assign data classifications. | Security Officer | PERM-STOR-READ |
| PERM-STOR-AUDIT | Storage Audit | View audit logs. | Auditor | None |
| PERM-STOR-PURGE | Storage Purge | Permanently delete data. | Admin | PERM-STOR-DELETE |
| PERM-STOR-SNAPSHOT | Storage Snapshot | Create resource snapshots. | Operator | PERM-STOR-READ |
| PERM-STOR-COMPACT | Storage Compact | Run compaction operations. | Operator | PERM-STOR-WRITE |
| PERM-STOR-REPAIR | Storage Repair | Run repair operations. | Operator | PERM-STOR-WRITE |
| PERM-STOR-ADMIN | Storage Admin | Full administrative access. | Super Admin | All permissions |
| PERM-STOR-CONFIG | Storage Config | Modify storage configuration. | Admin | None |
| PERM-STOR-MONITOR | Storage Monitor | View health and performance. | Operator | PERM-STOR-OBSERVE |

## 4. Role-Permission Mapping

| Role | Permissions |
|---|---|
| Viewer | READ, LIST, SCAN, QUERY, OBSERVE |
| Editor | All Viewer + WRITE, DELETE, VERSION, LOCK, SNAPSHOT |
| Analyst | All Viewer + QUERY, SCAN (full) |
| Operator | All Analyst + BACKUP, RESTORE, COMPACT, REPAIR, MONITOR |
| Admin | All Operator + MIGRATE, REPLICATE, PURGE, CONFIG |
| Security Officer | ENCRYPT, CLASSIFY, AUDIT |
| Auditor | AUDIT, OBSERVE (read-only) |
| Super Admin | ADMIN (all permissions) |

## 5. Permission Evaluation Rules

1. Permissions are evaluated in deny-before-allow order.
2. Explicit DENY overrides all ALLOW rules.
3. Role assignments are additive; the union of all assigned roles determines effective permissions.
4. Permission grants MUST be audited per RFC-0409.
5. Permission revocation MUST take effect within one token refresh cycle.

## 6. Validation Rules

1. Every permission identifier MUST match the regex ^PERM-STOR-[A-Z][A-Z0-9]*$.
2. Permission names MUST be unique.
3. Permission hierarchies MUST be acyclic.
4. Implementations MUST NOT grant permissions outside this catalog.
5. Role definitions MUST include at least one role from the standard set.
