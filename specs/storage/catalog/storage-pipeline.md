---
id: ATLAS-STORAGE-CATALOG-PIPELINE
title: Storage Pipeline Stages Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Pipeline Stages Catalog

## 1. Purpose

This catalog defines the canonical pipeline stages that every write operation traverses within the Atlas Storage subsystem.

## 2. Pipeline Stage Catalog

| Stage ID | Stage Name | Description | Executed By | RFC Reference |
|---|---|---|---|---|
| PIPE-VALIDATE | Validate | Schema and permission validation | Schema Validator | RFC-0405 |
| PIPE-SERIALIZE | Serialize | Convert resource to wire format | Serialization Engine | RFC-0423 |
| PIPE-ENCRYPT | Encrypt | Apply encryption at rest | Encryption Engine | RFC-0409 |
| PIPE-COMPRESS | Compress | Apply data compression | Compression Engine | RFC-0423 |
| PIPE-PERSIST | Persist | Write to backing store | Provider | RFC-0403 |
| PIPE-VERIFY | Verify | Confirm write integrity | Integrity Checker | RFC-0409 |
| PIPE-COMMIT | Commit | Finalize transaction | Transaction Manager | RFC-0406 |
| PIPE-NOTIFY | Notify | Emit events and update cache | Event Publisher | RFC-0413 |

## 3. Pipeline Execution Model

| Model | Description | Use Case |
|---|---|---|
| Sequential | All stages execute in order | Standard operations |
| Parallel Serialize-Encrypt | Serialization and encryption run in parallel | Large documents |
| Async Notify | Notification fires after commit without blocking | High-throughput scenarios |
| Conditional | Some stages skipped based on resource type | Binary blobs (no schema validation) |

## 4. Stage Skip Rules

| Resource Type | Skipped Stages | Reason |
|---|---|---|
| Binary | PIPE-VALIDATE | No schema to validate |
| Cache Entry | PIPE-ENCRYPT, PIPE-COMPRESS | Ephemeral data |
| Audit Log | PIPE-COMPRESS | Immutable append-only |
| Snapshot | PIPE-VALIDATE, PIPE-COMPRESS | Point-in-time freeze |

## 5. Validation Rules

1. Every pipeline stage identifier MUST match the regex ^PIPE-[A-Z]+$.
2. Sequential pipeline MUST execute all stages in defined order.
3. Stage skips MUST be documented per resource type.
4. PIPE-NOTIFY MUST fire even if PIPE-COMMIT fails (failure event).
5. Pipeline execution time MUST be measurable per RFC-0414.
