---
id: ATLAS-STORAGE-CATALOG-RESOURCE-TYPES
title: Storage Resource Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Resource Types Catalog

## 1. Purpose

This catalog defines the canonical set of resource types that MAY be managed by the Atlas Storage subsystem. Each resource type carries default lifecycle policies, versioning strategies, and classification levels.

## 2. Resource Type ID Prefix

All resource type identifiers use the prefix RT-.

## 3. Complete Resource Type Catalog

| Resource Type ID | Name | Schema Versioning | Lifecycle Policy | RFC Reference | Default Classification |
|---|---|---|---|---|---|
| RT-DOCUMENT | Document | Enabled | Manual archive | RFC-0404 | Confidential |
| RT-CONFIGURATION | Configuration | Enabled | Auto-archive after update | RFC-0404 | Restricted |
| RT-STATE | State | Disabled | Immediate purge on delete | RFC-0404 | Internal |
| RT-SNAPSHOT | Snapshot | Immutable | Retention policy driven | RFC-0407 | Internal |
| RT-BACKUP | Backup | Immutable | Full retention | RFC-0411 | Restricted |
| RT-MIGRATION | Migration | Disabled | Purge after completion | RFC-0408 | Internal |
| RT-SCHEMA | Schema | Versioned | Permanent retention | RFC-0405 | Confidential |
| RT-VERSION | Version | N/A | Linked to parent resource | RFC-0407 | Internal |
| RT-LOCK | Lock | N/A | Auto-purge on release | RFC-0417 | Internal |
| RT-EVENT | Event | Append-only | Retention policy driven | RFC-0413 | Internal |
| RT-METRIC | Metric | Append-only | Aggregated and purged | RFC-0414 | Public |
| RT-AUDIT_LOG | Audit Log | Append-only | Permanent retention | RFC-0409 | Restricted |
| RT-CACHE_ENTRY | Cache Entry | N/A | TTL-driven purge | RFC-0410 | Internal |
| RT-INDEX | Index | Enabled | Rebuilt on schema change | RFC-0405 | Internal |
| RT-MANIFEST | Manifest | Enabled | Linked to parent resource | RFC-0404 | Confidential |
| RT-CREDENTIAL | Credential | Disabled | Immediate purge | RFC-0409 | Restricted |
| RT-PREFERENCE | Preference | Disabled | Manual archive | RFC-0404 | Internal |
| RT-SESSION | Session | Disabled | TTL-driven purge | RFC-0404 | Internal |
| RT-QUEUE_ITEM | Queue Item | Disabled | Purge after processing | RFC-0413 | Internal |
| RT-KNOWLEDGE_PACK | Knowledge Pack | Enabled | Permanent retention | RFC-0601 | Confidential |
| RT-PLUGIN_STATE | Plugin State | Disabled | Purge on plugin removal | RFC-0201 | Internal |
| RT-AI_CONTEXT | AI Context | Enabled | TTL-driven purge | RFC-0301 | Confidential |
| RT-WORKFLOW_STATE | Workflow State | Enabled | Archive after completion | RFC-0101 | Internal |
| RT-PROJECT_CONFIG | Project Config | Enabled | Permanent retention | RFC-0701 | Restricted |

## 4. Lifecycle Policy Definitions

| Policy | Description | Purge Behavior |
|---|---|---|
| Manual Archive | Human operator decides when to archive. | Never auto-purged. |
| Auto-Archive After Update | Archived upon next version update. | Purged after retention period. |
| Immediate Purge | Removed immediately when no longer needed. | No retention period. |
| Retention Policy Driven | Governed by backup/retention configuration. | Purged per policy schedule. |
| Permanent Retention | Never purged; compliance requirement. | Never purged. |
| TTL-Driven Purge | Removed after time-to-live expires. | Auto-purged on TTL expiry. |
| Purge After Processing | Removed after workflow consumption. | Auto-purged post-processing. |
| Rebuild on Schema Change | Dropped and rebuilt when schema evolves. | No persistence across schema changes. |
| Archive After Completion | Archived upon workflow completion. | Purged after retention period. |
| Purge on Plugin Removal | Removed when hosting plugin is uninstalled. | Auto-purged on plugin removal. |
| Linked to Parent | Inherits lifecycle from parent resource. | Follows parent lifecycle. |
| Append-Only | Never modified; only new entries appended. | Purged per retention policy. |

## 5. Validation Rules

1. Every resource type identifier MUST match the regex ^RT-[A-Z][A-Z0-9]*$.
2. Resource type names MUST be unique.
3. Default classification MUST be assignable per tenant.
4. Lifecycle policies MUST be enforceable by the Storage subsystem.
5. New resource types MUST be registered through the extension mechanism in RFC-0419.
