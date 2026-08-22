# RFC-0222: Plugin Configuration

RFC: RFC-0222
Title: Plugin Configuration
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
  - RFC-0202 Plugin Manifest
  - RFC-0217 Plugin Packaging
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0221 Plugin Resources
  - RFC-0223 Plugin Storage
Related ADR:
  - ADR-0022 Configuration Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the configuration hierarchy (session, temporary, user, project, workspace, global, default), configuration resolution, configuration schema, configuration validation, configuration hot reload, configuration migration, configuration secret handling, configuration export/import, configuration audit, and default isolation requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Configuration Philosophy](#4-configuration-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Configuration Hierarchy](#9-configuration-hierarchy)
10. [Configuration Resolution](#10-configuration-resolution)
11. [Configuration Schema](#11-configuration-schema)
12. [Configuration Validation](#12-configuration-validation)
13. [Configuration Hot Reload](#13-configuration-hot-reload)
14. [Configuration Migration](#14-configuration-migration)
15. [Configuration Secret Handling](#15-configuration-secret-handling)
16. [Configuration Export/Import](#16-configuration-exportimport)
17. [Configuration Audit](#17-configuration-audit)
18. [Default Isolation](#18-default-isolation)
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

1. **Hierarchy**: Seven-level configuration priority system.
2. **Resolution**: Deterministic top-to-bottom resolution algorithm.
3. **Schema**: JSON Schema validation for all configurations.
4. **Hot Reload**: Apply changes without restart where safe.
5. **Migration**: Schema versioning with migration scripts.
6. **Secrets**: Encrypted storage for sensitive values.
7. **Export/Import**: Serialize/deserialize for team sharing.
8. **Audit**: Track who changed what and when.
9. **Isolation**: Plugin defaults NEVER leak into global config.

---

- RFC-0323 Workflow Plugin Integration


## 4 Configuration Philosophy

Configuration follows these principles:

- Higher priority levels ALWAYS override lower levels.
- Plugin defaults are isolated and never leak upward.
- Secrets are encrypted at rest and never logged.
- Hot reload is the default; restart is the exception.
- Migrations preserve existing configurations.

---


## 6 Boundaries

- Configuration is scoped to the plugin and the level.
- Cross-level configuration merges are handled by the runtime.
- Secrets are encrypted by the runtime; plugins never see raw encryption keys.
- Configuration files are owned by the runtime, not by plugins.

---



## 8 Architecture

`mermaid
graph BT
    subgraph Hierarchy
        S[Session]
        T[Temporary]
        U[User]
        P[Project]
        W[Workspace]
        G[Global]
        D[Plugin Default]
    end
    subgraph Resolution
        MERGE[Deep Merge Engine]
        VAL[Schema Validator]
    end
    S --> MERGE
    T --> MERGE
    U --> MERGE
    P --> MERGE
    W --> MERGE
    G --> MERGE
    D --> MERGE
    MERGE --> VAL
    VAL --> CFG[Resolved Config]
`

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Configuration Resolution

`	ypescript
resolve(key: string, plugin_id: string): ConfigValue {
  // Walk hierarchy from highest to lowest priority
  for (const level of ['session', 'temporary', 'user', 'project', 'workspace', 'global', 'default']) {
    const value = getConfig(plugin_id, level, key);
    if (value !== undefined) return value;
  }
  return undefined;
}
`

Merge rules:
- Scalars (string, number, boolean): later levels override earlier.
- Arrays: REPLACED entirely (not merged).
- Objects: DEEP-MERGED recursively.
- Missing keys: fall through to next lower priority level.

---


## 12 Configuration Validation

1. Configuration MUST conform to the declared schema on load.
2. Invalid configuration causes plugin load failure with CONFIG_001.
3. Runtime rejects configuration updates that violate the schema.
4. Default values from the schema are applied when keys are missing.

---


## 14 Configuration Migration

`json
{
  "config_migrations": [
    {
      "from_version": 1,
      "to_version": 2,
      "script": "function migrate(config) { config.cache_ttl = 3600; return config; }",
      "safe_to_hot_reload": true
    }
  ]
}
`

Rules:
- Migrations are applied in order (1->2, 2->3, etc.).
- Failed migrations abort the plugin load.
- Migration scripts run in a sandboxed environment.

---


## 16 Configuration Export/Import

- Export serializes the configuration (excluding secrets) for team sharing.
- Import validates against the schema and merges at the appropriate level.
- Exported configurations include a metadata section with export timestamp and source.

---

- Establishing the boundaries between plugin layers.


## 18 Default Isolation

Plugin defaults (hardcoded in code) are:
- Applied as the lowest priority level.
- NEVER written to disk.
- NEVER included in configuration exports.
- NEVER visible to other plugins.

---


## 20 Glossary

| Term              | Definition                                           |
|-------------------|------------------------------------------------------|
| Configuration     | Plugin-adjustable settings at various priority levels.|
| Hot Reload        | Applying config changes without restart.             |
| Secret            | Encrypted configuration value (API keys, tokens).    |

---

| RFC-0201 | Consumed | Plugin Overview |


## 22 Cross References

- RFC-0201 Plugin Overview
- RFC-0202 Plugin Manifest
- RFC-0217 Plugin Packaging
- RFC-0223 Plugin Storage
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



