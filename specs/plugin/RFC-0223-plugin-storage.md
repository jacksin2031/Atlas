# RFC-0223: Plugin Storage

RFC: RFC-0223
Title: Plugin Storage
Status: Proposed
Version: 1.0.0
Category: Plugin Architecture
Layer: Runtime
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-07-01
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0208 Plugin Sandbox
  - RFC-0221 Plugin Resources
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0222 Plugin Configuration
  - RFC-0224 Plugin Testing
Related ADR:
  - ADR-0023 Storage Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the storage types (cache, persistent, secret, session, database, blob, binary), storage isolation, storage path convention, storage quota, storage encryption, storage migration, storage backup, storage cleanup, storage API, and cross-plugin sharing requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Storage Philosophy](#4-storage-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Storage Types](#9-storage-types)
10. [Storage Isolation](#10-storage-isolation)
11. [Storage Path Convention](#11-storage-path-convention)
12. [Storage Quota](#12-storage-quota)
13. [Storage Encryption](#13-storage-encryption)
14. [Storage Migration](#14-storage-migration)
15. [Storage Backup](#15-storage-backup)
16. [Storage Cleanup](#16-storage-cleanup)
17. [Storage API](#17-storage-api)
18. [Cross-Plugin Sharing](#18-cross-plugin-sharing)
19. [Performance Budgets](#19-performance-budgets)
20. [Glossary](#20-glossary)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Cross References](#22-cross-references)
23. [References](#23-references)
24. [Revision History](#24-revision-history)
25. [Future Evolution](#25-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Storage Types**: Seven distinct storage types with different characteristics.
2. **Isolation**: Each plugin gets an isolated storage namespace.
3. **Quotas**: Configurable per-plugin storage limits.
4. **Encryption**: Secret storage encrypted at rest.
5. **Migration**: Schema versioning for persistent storage.
6. **Backup**: Runtime-managed backup for persistent storage.
7. **Cleanup**: Garbage collection for orphaned data.
8. **Unified API**: Consistent interface across all storage types.

---

- RFC-0323 Workflow Plugin Integration


## 4 Storage Philosophy

Storage follows these principles:

- Every plugin has an isolated storage namespace.
- Storage types have distinct lifecycle and persistence guarantees.
- Quotas prevent disk abuse.
- Secrets are encrypted; other storage types are not by default.
- Cleanup is automatic for volatile storage types.

---


## 6 Boundaries

- Storage access is scoped to the plugin namespace.
- Plugins CANNOT access other plugins' storage.
- Cross-plugin sharing requires explicit opt-in.
- Storage paths are managed by the runtime, not plugins.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin A
        PA_Store[Storage API]
    end
    subgraph Plugin B
        PB_Store[Storage API]
    end
    subgraph Runtime Storage
        SM[Storage Manager]
        SQ[Quota Enforcer]
        SE[Secret Encryptor]
        GC[Garbage Collector]
        BK[Backup Manager]
    end
    subgraph Backends
        CA[Cache (RAM)]
        PS[Persistent (Disk)]
        SC[Secret (Encrypted Disk)]
        SS[Session (RAM)]
        DB[Database]
        BL[Blob (Disk)]
        BI[Binary (Disk)]
    end
    PA_Store --> SM
    PB_Store --> SM
    SM --> SQ
    SM --> SE
    SM --> GC
    SM --> BK
    SM --> CA
    SM --> PS
    SM --> SC
    SM --> SS
    SM --> DB
    SM --> BL
    SM --> BI
`

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Storage Isolation

Each plugin gets:

`
~/.atlas/data/<plugin_id>/<type>/
`

- Plugin A CANNOT access Plugin B's storage path.
- The runtime enforces filesystem permissions at the OS level.
- Violations are logged and may trigger security events.

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 12 Storage Quota

| Type        | Default  | Max      | Eviction Policy     |
|-------------|----------|----------|---------------------|
| Cache       | 100 MB   | 1 GB     | LRU + TTL           |
| Persistent  | 500 MB   | 5 GB     | Manual delete       |
| Secret      | 10 KB    | 50 KB    | Manual revoke       |
| Session     | 50 MB    | 200 MB   | Auto-clear on exit  |
| Database    | 500 MB   | 5 GB     | Manual delete       |
| Blob        | 1 GB     | 10 GB    | Manual delete       |
| Binary      | 500 MB   | 5 GB     | Manual delete       |

Quota enforcement:
- Exceeding the quota returns STORAGE_001 (QuotaExceeded).
- The operator can increase quotas per-plugin via workspace settings.

---


## 14 Storage Migration

Storage migration handles schema version changes:

`json
{
  "storage_migrations": [
    {
      "from_version": 1,
      "to_version": 2,
      "script": "function migrate(db) { db.addTable('new_table'); }"
    }
  ]
}
`

Rules:
- Migrations run on plugin load, before the plugin is activated.
- Failed migrations abort the plugin load.
- Migrations are idempotent (can be re-run safely).

---



## 16 Storage Cleanup

Garbage collection runs periodically:

| Type        | Cleanup Trigger              | Action                          |
|-------------|------------------------------|---------------------------------|
| Cache       | TTL expired / LRU eviction   | Remove expired or least-used    |
| Session     | Session end                  | Delete all session data         |
| Persistent  | Plugin uninstall             | Offer user confirmation         |
| Secret      | Plugin uninstall             | Secure wipe (no prompt)         |
| Database    | Plugin uninstall             | Offer user confirmation         |
| Blob        | Plugin uninstall             | Offer user confirmation         |
| Binary      | Plugin uninstall             | Offer user confirmation         |

---

- Establishing the boundaries between plugin layers.


## 18 Cross-Plugin Sharing

Cross-plugin storage sharing requires explicit opt-in:

`json
{
  "storage_sharing": {
    "enabled": true,
    "allowed_plugins": ["plugin-a", "plugin-b"],
    "type": "persistent"
  }
}
`

Rules:
- Sharing is READ-ONLY by default.
- WRITE sharing requires both plugins to declare it.
- Shared storage is audited.

---



## 20 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Storage Type      | Distinct storage backend with defined characteristics.|
| Quota             | Maximum storage allowed per plugin per type.         |
| Garbage Collection| Automatic cleanup of stale/orphaned data.            |

---

| RFC-0201 | Consumed | Plugin Overview |


## 22 Cross References

- RFC-0201 Plugin Overview
- RFC-0208 Plugin Sandbox
- RFC-0221 Plugin Resources
- RFC-0222 Plugin Configuration
- RFC-0224 Plugin Testing

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

## 24 Revision History

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



