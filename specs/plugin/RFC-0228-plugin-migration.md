# RFC-0228: Plugin Migration

RFC: RFC-0228
Title: Plugin Migration
Status: Proposed
Version: 1.0.0
Category: Plugin Operations
Layer: Runtime
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0202 Plugin Manifest
  - RFC-0212 Plugin Versioning
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0217 Plugin Packaging
  - RFC-0222 Plugin Configuration
  - RFC-0223 Plugin Storage
  - RFC-0225 Plugin Hot Reload
Related ADR:
  - ADR-0028 Migration Architecture
Target Release: 1.0.0
Review Cycle: Core Architecture Board
Compatibility: Compatible with Spec 1.x

---

## Normative Status

## Authority

This RFC is the authoritative specification for the plugin subsystem domain defined herein.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Extension Point | A predefined location in the architecture where external components MAY inject behavior. | Glossary |
| Hook | A callback registered at an extension point. | Glossary |
| Sandbox | An isolated execution process restricting OS access. | Glossary |

---

## Layer Boundaries

### Responsibilities
This specification IS responsible for: defining the architecture and requirements for this plugin subsystem component.

### Non-Responsibilities
This specification IS NOT responsible for: implementation details handled by other subsystems.

### Dependencies
| Dependency | Direction | Description |
|---|---|---|
| RFC-0201 | Consumed | Plugin Overview |

### Consumers
- RFC-0323 Workflow Plugin Integration

### Providers
- RFC-0201 Plugin Overview (provides architecture context)

### Forbidden Dependencies
- This specification MUST NOT depend on any programming language.
- This specification MUST NOT depend on any specific plugin API.

---

This specification is Normative. Every Atlas implementation MUST conform to the migration types (manifest, configuration, storage, permission), migration rules, migration order, migration rollback, migration validation, migration audit, migration dry-run, and migration reporting requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Migration Philosophy](#4-migration-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Migration Types](#9-migration-types)
10. [Migration Rules](#10-migration-rules)
11. [Migration Order](#11-migration-order)
12. [Migration Rollback](#12-migration-rollback)
13. [Migration Validation](#13-migration-validation)
14. [Migration Audit](#14-migration-audit)
15. [Migration Dry-Run](#15-migration-dry-run)
16. [Migration Reporting](#16-migration-reporting)
17. [Performance Budgets](#17-performance-budgets)
18. [Glossary](#18-glossary)
19. [Acceptance Criteria](#19-acceptance-criteria)
20. [Cross References](#20-cross-references)
21. [References](#21-references)
22. [Revision History](#22-revision-history)
23. [Future Evolution](#23-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Manifest Migration**: Migrate between manifest schema versions.
2. **Configuration Migration**: Migrate configuration between schema versions.
3. **Storage Migration**: Migrate storage data between schema versions.
4. **Permission Migration**: Handle permission changes between versions.
5. **Ordered Execution**: Migrations run in a defined, deterministic order.
6. **Rollback**: Failed migrations roll back to the previous state.
7. **Validation**: Migrations are validated before execution.
8. **Audit**: All migrations are logged.
9. **Dry-Run**: Operators can preview migrations without applying.

---

- RFC-0323 Workflow Plugin Integration


## 4 Migration Philosophy

Migration follows these principles:

- Migrations are FORWARD-ONLY: v1 -> v2 -> v3, never backwards.
- Each migration is ATOMIC: it either completes fully or rolls back.
- Migrations are ORDERED: manifest -> config -> storage -> permission.
- Migrations are VALIDATED: invalid migrations are rejected before execution.
- Migrations are AUDITED: every migration is logged with before/after state.

---


## 6 Boundaries

- Migration is scoped to a single plugin instance.
- Cross-plugin migration coordination is NOT supported (migrations are sequential).
- Migration does NOT modify the plugin package itself; it modifies runtime state.
- Migration data is stored in the plugin's storage namespace.

---

| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
graph TB
    subgraph Plugin Update
        OLD[Old Version v1.x]
        NEW[New Version v2.x]
    end
    subgraph Migration Engine
        V[Validation]
        ORDER[Order Resolver]
        EXEC[Executor]
        RB[Rollback]
        AUD[Audit Logger]
    end
    subgraph Migration Stages
        MM[Manifest Migration]
        CM[Config Migration]
        SM[Storage Migration]
        PM[Permission Migration]
    end
    OLD --> V
    V -->|valid| ORDER
    ORDER --> MM
    MM --> CM
    CM --> SM
    SM --> PM
    PM --> NEW
    V -.->|invalid| RB
    EXEC -.->|failure| RB
    RB --> AUD
    AUD --> LOG[Audit Log]
`

---

`json
{
  "config_migrations": [
    {
      "from_version": 1,
      "to_version": 2,
      "script": "function migrate(config) { config.api_endpoint = config.endpoint; delete config.endpoint; return config; }",
      "safe_to_hot_reload": true
    }
  ]
}
`

### 9.3 Storage Migration

Migrates storage data between schema versions:

`json
{
  "storage_migrations": [
    {
      "from_version": 1,
      "to_version": 2,
      "script": "function migrate(db) { db.createTable('users_v2'); db.migrateTable('users', 'users_v2'); }",
      "estimated_duration_ms": 5000
    }
  ]
}
`

### 9.4 Permission Migration

Handles permission changes between versions:

`json
{
  "permission_migrations": [
    {
      "from_version": "1.0.0",
      "to_version": "2.0.0",
      "changes": [
        { "action": "add_permission", "permission": "network:local" },
        { "action": "upgrade_permission", "from": "normal", "to": "elevated", "requires_approval": true },
        { "action": "remove_permission", "permission": "deprecated:feature" }
      ]
    }
  ]
}
`

---

- Migrations MUST be idempotent (can be re-run safely).
- Schema changes are applied within a transaction.
- Failed transactions are rolled back automatically.

### 10.5 Permission Migration Rules

- Added permissions require user/admin approval if they elevate the permission level.
- Upgraded permissions ALWAYS require approval.
- Removed permissions are silently dropped (no data loss).
- Permission migration errors block the plugin activation.

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 12 Migration Rollback

If any migration stage fails:

`
Stage 4 (Permission) fails:
  Rollback Stage 4: Revert permission changes
  Rollback Stage 3: Restore storage to pre-migration state
  Rollback Stage 2: Restore config to pre-migration state
  Rollback Stage 1: Restore manifest to pre-migration state
  Result: Plugin loads with previous version

Stage 2 (Config) fails:
  Rollback Stage 2: Restore config
  Rollback Stage 1: Restore manifest
  Result: Plugin loads with previous version
`

Rollback rules:
- Rollback is ATOMIC and COMPLETE.
- Rollback timeout: 30 seconds.
- Failed rollbacks are logged as CRITICAL errors.
- The operator is notified of the failure.

---

- Workflow execution (covered by RFC-0301).


## 14 Migration Audit

Every migration is logged:

`json
{
  "timestamp": "ISO8601",
  "event": "migration.started | migration.completed | migration.failed | migration.rollback",
  "plugin_id": "string",
  "from_version": "string",
  "to_version": "string",
  "migration_types": ["manifest", "config", "storage", "permission"],
  "duration_ms": number,
  "status": "success | failed | rolled_back",
  "error": "string (if failed)"
}
`

---

- Establishing the boundaries between plugin layers.


## 16 Migration Reporting

After migration completes:

`json
{
  "plugin_id": "my-plugin",
  "from_version": "1.0.0",
  "to_version": "2.0.0",
  "status": "success",
  "duration_ms": 4800,
  "migrations_applied": [
    { "type": "manifest", "rules": 3, "duration_ms": 50 },
    { "type": "config", "rules": 1, "duration_ms": 20 },
    { "type": "storage", "rules": 1, "duration_ms": 4500 },
    { "type": "permission", "rules": 1, "duration_ms": 230 }
  ],
  "warnings": [],
  "errors": []
}
`

---

| RFC-0201 | Consumed | Plugin Overview |


## 18 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Migration         | Transforming plugin state from one version to another.|
| Dry-Run           | Previewing a migration without applying it.          |
| Idempotent        | A migration that can be safely re-run.               |

---

| RFC-0201 | Consumed | Plugin Overview |


## 20 Cross References

- RFC-0201 Plugin Overview
- RFC-0202 Plugin Manifest
- RFC-0212 Plugin Versioning
- RFC-0217 Plugin Packaging
- RFC-0222 Plugin Configuration
- RFC-0223 Plugin Storage
- RFC-0225 Plugin Hot Reload

---



## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---

## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

---

## References

| Reference | Description |
|---|---|
| RFC-0001 | Runtime Overview |
| Glossary | Atlas Master Glossary |

---

## 22 Revision History

| Date       | Version | Author                    | Change                           |
|------------|---------|---------------------------|----------------------------------|
| 2026-07-01 | 1.0.0   | Atlas Specification Committee | Initial proposal               |

---


---

## Runtime Independence

This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:

- Any programming language (Rust, Node.js, TypeScript, Go, Python, etc.)
- Any runtime environment (Electron, Tauri, Browser, Desktop, Server)
- Any storage backend (SQLite, PostgreSQL, MongoDB, Redis, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)
- Any cloud provider (AWS, Azure, GCP, etc.)
- Any container platform (Docker, containerd, etc.)

All contracts in this specification are defined as abstract behavioral interfaces.

---



