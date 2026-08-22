---
id: ATLAS-STORAGE-CATALOG-CAPABILITIES
title: Storage Capabilities Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Capabilities Catalog

## 1. Purpose

This catalog defines the canonical set of capabilities that the Atlas Storage subsystem MAY expose to consumers. Capabilities represent discrete, independently addressable functions that a Storage Provider implementation MUST support to be considered compliant. Each capability maps to a specific RFC section and carries a maturity level.

## 2. Stable ID Prefix

All capability identifiers use the prefix CAP-.

### 2.1 Naming Convention

Capability identifiers SHALL follow the pattern:

`
CAP-<DOMAIN>-<NAME>
`

where <DOMAIN> identifies the functional area and <NAME> describes the specific capability.

## 3. Complete Capability Catalog

| Stable ID | Capability Name | Domain | Description | RFC Reference | Maturity |
|---|---|---|---|---|---|
| CAP-STORAGE-READ | Storage Read | CORE | Retrieve a resource by identifier from persistent storage. | RFC-0403 | STABLE |
| CAP-STORAGE-WRITE | Storage Write | CORE | Store or update a resource in persistent storage. | RFC-0403 | STABLE |
| CAP-STORAGE-DELETE | Storage Delete | CORE | Remove a resource from persistent storage. | RFC-0403 | STABLE |
| CAP-STORAGE-LIST | Storage List | CORE | Enumerate resources matching a filter criteria. | RFC-0403 | STABLE |
| CAP-STORAGE-SCAN | Storage Scan | CORE | Sequentially iterate over all resources without filter. | RFC-0403 | STABLE |
| CAP-STORAGE-QUERY | Storage Query | CORE | Execute structured queries with join, sort, and aggregation. | RFC-0405 | STABLE |
| CAP-STORAGE-BACKUP | Storage Backup | RELIABILITY | Create a consistent snapshot of stored data for preservation. | RFC-0411 | STABLE |
| CAP-STORAGE-RESTORE | Storage Restore | RELIABILITY | Reconstruct data from a backup source. | RFC-0412 | STABLE |
| CAP-STORAGE-MIGRATE | Storage Migrate | EVOLUTION | Transform data or schema between versions without loss. | RFC-0408 | STABLE |
| CAP-STORAGE-VERSION | Storage Version | INTEGRITY | Maintain and resolve resource version identifiers. | RFC-0407 | STABLE |
| CAP-STORAGE-LOCK | Storage Lock | CONCURRENCY | Acquire exclusive or shared access locks on resources. | RFC-0417 | STABLE |
| CAP-STORAGE-REPLICATE | Storage Replicate | AVAILABILITY | Synchronize data copies across storage nodes or regions. | RFC-0418 | STABLE |
| CAP-STORAGE-OBSERVE | Storage Observe | OBSERVABILITY | Emit metrics, traces, and structured logs for operations. | RFC-0414 | STABLE |
| CAP-STORAGE-EXTEND | Storage Extend | EXTENSIBILITY | Register custom hooks, providers, or transformation logic. | RFC-0419 | GA |
| CAP-STORAGE-ENCRYPT | Storage Encrypt | SECURITY | Apply cryptographic transformation to stored data. | RFC-0409 | STABLE |
| CAP-STORAGE-CLASSIFY | Storage Classify | SECURITY | Assign data classification labels based on policy. | RFC-0409 | GA |
| CAP-STORAGE-AUDIT | Storage Audit | COMPLIANCE | Record immutable logs of all storage operations. | RFC-0409 | STABLE |
| CAP-STORAGE-PURGE | Storage Purge | LIFECYCLE | Permanently remove data beyond recovery. | RFC-0404 | STABLE |
| CAP-STORAGE-SNAPSHOT | Storage Snapshot | VERSIONING | Create a point-in-time immutable copy of a resource set. | RFC-0407 | STABLE |
| CAP-STORAGE-COMPACT | Storage Compact | PERFORMANCE | Defragment and optimize stored data layout. | RFC-0415 | GA |
| CAP-STORAGE-REPAIR | Storage Repair | RELIABILITY | Detect and fix corrupted data without external backup. | RFC-0412 | GA |

## 4. Capability Composition Rules

1. A Storage Provider MUST implement all STABLE capabilities to achieve baseline compliance.
2. GA capabilities MAY be implemented optionally; when implemented, they MUST conform to their RFC definitions.
3. Capabilities marked STABLE MUST NOT be removed or have their signatures altered in a breaking manner.
4. Capabilities MAY be composed into groups for simplified compliance declaration.

## 5. Capability Maturity Levels

| Level | Meaning | Transition Requirement |
|---|---|---|
| EXPERIMENTAL | Under active development; subject to change without notice. | Architecture Board approval. |
| GA | General Availability; stable interface. | Successful integration testing. |
| STABLE | Production-ready; backward compatible. | Formal specification review. |
| DEPRECATED | Marked for removal; replacement available. | Deprecation period of at least 2 major versions. |

## 6. Validation Rules

1. Every capability identifier MUST match the regex ^CAP-STORAGE-[A-Z][A-Z0-9]*$.
2. Capability names MUST be unique within their domain.
3. Capability descriptions MUST be self-contained and reference exactly one RFC section.
4. Implementations MUST NOT expose capabilities outside this catalog without Architecture Board approval.
5. Capability maturity levels MUST be updated through the formal versioning process defined in RFC-0407.
