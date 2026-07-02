---
id: ATLAS-STORAGE-CATALOG-EXTENSION-POINTS
title: Storage Extension Points Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Extension Points Catalog

## 1. Purpose

This catalog defines the canonical extension points and hooks through which the Atlas Storage subsystem MAY be customized without modifying core code.

## 2. Extension Point Catalog

| Extension Point ID | Name | Timing | Description | Invocable By | RFC Reference |
|---|---|---|---|---|---|
| EXT-PROVIDER | Provider | Initialization | Register a custom storage provider implementation. | Third-party | RFC-0419 |
| EXT-HOOK-PRE-READ | Pre-Read | Before read operation | Intercept and modify read requests. | Extension | RFC-0419 |
| EXT-HOOK-POST-READ | Post-Read | After read operation | Observe or transform read results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-WRITE | Pre-Write | Before write operation | Intercept and modify write requests. | Extension | RFC-0419 |
| EXT-HOOK-POST-WRITE | Post-Write | After write operation | Observe or transform write results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-DELETE | Pre-Delete | Before delete operation | Intercept and modify delete requests. | Extension | RFC-0419 |
| EXT-HOOK-POST-DELETE | Post-Delete | After delete operation | Observe or transform delete results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-TRANSACT | Pre-Transaction | Before transaction begins | Intercept and modify transaction parameters. | Extension | RFC-0419 |
| EXT-HOOK-POST-TRANSACT | Post-Transaction | After transaction completes | Observe or transform transaction outcomes. | Extension | RFC-0419 |
| EXT-HOOK-PRE-SCHEMA | Pre-Schema | Before schema validation | Intercept and modify schema definitions. | Extension | RFC-0419 |
| EXT-HOOK-POST-SCHEMA | Post-Schema | After schema validation | Observe validation results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-MIGRATE | Pre-Migrate | Before migration begins | Intercept migration parameters. | Extension | RFC-0419 |
| EXT-HOOK-POST-MIGRATE | Post-Migrate | After migration completes | Observe migration results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-BACKUP | Pre-Backup | Before backup begins | Intercept backup scope and parameters. | Extension | RFC-0419 |
| EXT-HOOK-POST-BACKUP | Post-Backup | After backup completes | Observe backup results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-RECOVER | Pre-Recover | Before recovery begins | Intercept recovery parameters. | Extension | RFC-0419 |
| EXT-HOOK-POST-RECOVER | Post-Recover | After recovery completes | Observe recovery results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-LOCK | Pre-Lock | Before lock acquisition | Intercept lock requests. | Extension | RFC-0419 |
| EXT-HOOK-POST-LOCK | Post-Lock | After lock operation | Observe lock results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-REPLICATE | Pre-Replicate | Before replication sync | Intercept replication parameters. | Extension | RFC-0419 |
| EXT-HOOK-POST-REPLICATE | Post-Replicate | After replication sync | Observe replication results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-CACHE | Pre-Cache | Before cache operation | Intercept cache read/write requests. | Extension | RFC-0419 |
| EXT-HOOK-POST-CACHE | Post-Cache | After cache operation | Observe cache results. | Extension | RFC-0419 |
| EXT-HOOK-PRE-AUDIT | Pre-Audit | Before audit log write | Intercept audit entries. | Extension | RFC-0419 |
| EXT-HOOK-POST-AUDIT | Post-Audit | After audit log write | Observe audit results. | Extension | RFC-0419 |
| EXT-TRANSFORM | Data Transform | During migration | Apply custom data transformation logic. | Extension | RFC-0419 |
| EXT-VALIDATOR | Schema Validator | During validation | Register custom validation rules. | Extension | RFC-0419 |
| EXT-CONFLICT-RESOLVER | Conflict Resolver | During conflict detection | Register custom conflict resolution logic. | Extension | RFC-0419 |

## 3. Hook Timing Categories

| Category | Hooks | Execution Context |
|---|---|---|
| Request Interception | Pre-* hooks | Before the core operation executes. |
| Result Observation | Post-* hooks | After the core operation completes. |
| Lifecycle | Provider, Transform, Validator | During subsystem initialization or migration. |
| Specialized | Conflict Resolver | During conflict detection and resolution. |

## 4. Extension Lifecycle States

| State | Description |
|---|---|
| Registered | Extension point is known but not yet loaded. |
| Loading | Extension code is being initialized. |
| Active | Extension is loaded and participating in operations. |
| Disabled | Extension is loaded but temporarily inactive. |
| Unregistered | Extension has been removed from the system. |
| Failed | Extension initialization or execution failed. |

## 5. Validation Rules

1. Every extension point identifier MUST match the regex ^EXT-[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$.
2. Extensions MUST be validated before activation through the five checks defined in RFC-0419.
3. Hook execution MUST NOT cause side effects outside the hook's designated scope.
4. Extensions MUST declare their required extension points at registration time.
5. Disabled extensions MUST NOT participate in any operations.
6. Extension lifecycle transitions MUST be logged per RFC-0413.
