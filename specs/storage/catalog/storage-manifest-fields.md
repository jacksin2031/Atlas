---
id: ATLAS-STORAGE-CATALOG-MANIFEST-FIELDS
title: Storage Manifest Fields Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Manifest Fields Catalog

## 1. Purpose

This catalog defines the canonical set of fields that MAY appear in storage resource manifests. Manifests are structured metadata documents that accompany every resource through its lifecycle.

## 2. Field Catalog

| Field Name | Type | Required | Description | RFC Reference |
|---|---|---|---|---|
| resource_id | UUID | YES | Unique identifier for the resource. | RFC-0402 |
| resource_type | Enum | YES | Category of the resource (document, config, state, etc.). | RFC-0404 |
| schema_version | String | YES | Semantic version of the schema this resource conforms to. | RFC-0405 |
| document_version | Integer | YES | Monotonically increasing version number for this document. | RFC-0407 |
| state | Enum | YES | Current lifecycle state of the resource. | RFC-0404 |
| created_at | Timestamp | YES | ISO 8601 timestamp of resource creation. | RFC-0404 |
| updated_at | Timestamp | YES | ISO 8601 timestamp of last modification. | RFC-0404 |
| deleted_at | Timestamp | NO | ISO 8601 timestamp of deletion (null if not deleted). | RFC-0404 |
| owner | String | YES | Identifier of the entity that owns this resource. | RFC-0409 |
| tenant | String | NO | Multi-tenant namespace identifier. | RFC-0409 |
| classification | Enum | YES | Data classification level (public, internal, confidential, restricted). | RFC-0409 |
| encryption_key_id | String | YES | Identifier of the key used to encrypt this resource. | RFC-0409 |
| backup_policy | Enum | NO | Backup retention policy applied to this resource. | RFC-0411 |
| retention_days | Integer | NO | Number of days to retain this resource after deletion. | RFC-0411 |
| lifecycle_policy | Enum | NO | Lifecycle transition policy (auto-archive, manual, permanent). | RFC-0404 |
| versioning_strategy | Enum | NO | Versioning strategy applied (sequential, branch-prefixed, etc.). | RFC-0407 |
| lock_mode | Enum | NO | Current lock mode (none, read, write, schema). | RFC-0417 |
| replication_factor | Integer | NO | Number of replica copies maintained. | RFC-0418 |
| cache_policy | Enum | NO | Caching behavior (hot, warm, cold, bypass). | RFC-0410 |
| observability_tags | Array | NO | Key-value pairs for trace and metric correlation. | RFC-0414 |

## 3. Field Value Constraints

### 3.1 resource_type Values

| Value | Description |
|---|---|
| document | User-generated content or data payload. |
| configuration | System or user configuration data. |
| state | Runtime or workflow execution state. |
| snapshot | Point-in-time data copy. |
| backup | Backup archive metadata. |
| migration | Migration operation metadata. |
| schema | Schema definition document. |
| version | Version control metadata. |
| lock | Lock state descriptor. |
| event | Event log entry. |
| metric | Collected metric data. |
| audit_log | Security audit trail entry. |
| cache_entry | Cache metadata. |
| index | Search index entry. |
| manifest | Resource manifest document. |
| credential | Encrypted credential data. |
| preference | User preference data. |
| session | Session state data. |
| queue_item | Queue entry for deferred processing. |
| knowledge_pack | Knowledge pack metadata. |
| plugin_state | Plugin runtime state. |
| ai_context | AI conversation or context data. |
| workflow_state | Workflow execution state. |
| project_config | Project-level configuration. |

### 3.2 classification Values

| Value | Description | Encryption Required |
|---|---|---|
| public | No sensitivity restrictions. | No |
| internal | Internal use only; no external exposure. | Recommended |
| confidential | Requires access control enforcement. | Yes |
| restricted | Highest sensitivity; audit trail required. | Yes |

### 3.3 state Values

| Value | Description |
|---|---|
| created | Resource instantiated, not yet persisted. |
| validating | Schema validation in progress. |
| stored | Persisted, awaiting activation. |
| active | Fully operational. |
| updating | Being modified. |
| archived | Retained but inactive. |
| deleting | Scheduled for removal. |
| restoring | Being recovered. |
| purged | Permanently removed. |
| failed | Unrecoverable error state. |

## 4. Validation Rules

1. Every manifest MUST include all REQUIRED fields.
2. Field types MUST be strictly enforced; type coercion is prohibited.
3. Timestamp fields MUST use ISO 8601 format with timezone information.
4. The resource_id MUST be globally unique within the Storage namespace.
5. Manifests MUST NOT contain fields outside this catalog without Extension registration.
6. Encryption_key_id MUST reference a key in the active key management system.
7. retention_days MUST be a positive integer when specified.
