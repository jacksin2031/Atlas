# RFC-0221: Plugin Resources

RFC: RFC-0221
Title: Plugin Resources
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
  - RFC-0217 Plugin Packaging
  - RFC-0222 Plugin Configuration
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0223 Plugin Storage
  - RFC-0224 Plugin Testing
Related ADR:
  - ADR-0021 Resource Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the resource types, resource loading, resource namespace, resource fallback, resource caching, resource versioning, resource validation, external resource download, and resource manifest requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Resource Philosophy](#4-resource-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Resource Types](#9-resource-types)
10. [Resource Loading](#10-resource-loading)
11. [Resource Namespace](#11-resource-namespace)
12. [Resource Fallback Chain](#12-resource-fallback-chain)
13. [Resource Caching](#13-resource-caching)
14. [Resource Versioning](#14-resource-versioning)
15. [Resource Validation](#15-resource-validation)
16. [External Resource Download](#16-external-resource-download)
17. [Resource Manifest](#17-resource-manifest)
18. [Performance Budgets](#18-performance-budgets)
19. [Glossary](#19-glossary)
20. [Acceptance Criteria](#20-acceptance-criteria)
21. [Cross References](#21-cross-references)
22. [References](#22-references)
23. [Revision History](#23-revision-history)
24. [Future Evolution](#24-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Resource Types**: Define and categorize all supported resource types.
2. **Resource Loading**: Standardized API for loading resources by type and ID.
3. **Namespace Isolation**: Each plugin has its own resource namespace.
4. **Fallback Chain**: Plugin -> workspace -> runtime default.
5. **Caching**: LRU cache for frequently accessed resources.
6. **Versioning**: Resources versioned alongside the plugin.
7. **Validation**: Schema check for templates, hash check for models.
8. **Lazy Download**: Large assets (models, OCR) downloaded on demand.
9. **Resource Manifest**: List all resources in the plugin manifest with hashes.

---

- RFC-0323 Workflow Plugin Integration


## 4 Resource Philosophy

Resources follow these principles:

- Every resource belongs to a plugin namespace.
- Resources are versioned alongside their plugin.
- Fallback ensures graceful degradation when resources are missing.
- Large resources are downloaded lazily to minimize install footprint.
- All resources are validated before use.

---


## 6 Boundaries

- Resource access is scoped to the plugin namespace.
- Plugins CANNOT access resources from other plugin namespaces.
- Workspace-level resources override plugin defaults.
- Runtime defaults are the final fallback.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Plugin A
        PA_Icons[Icons]
        PA_Trans[Translations]
        PA_Models[Models]
    end
    subgraph Plugin B
        PB_Icons[Icons]
        PB_Fonts[Fonts]
    end
    subgraph Runtime
        RM[Resource Manager]
        RC[LRU Cache]
        DL[Download Manager]
        VAL[Validator]
    end
    subgraph Workspace
        WS_Icons[Workspace Icons]
        WS_Defaults[Runtime Defaults]
    end
    PA_Icons --> RM
    PB_Icons --> RM
    RM --> RC
    RM --> DL
    DL --> VAL
    RM --> WS_Icons
    WS_Icons --> WS_Defaults
`

---



## 10 Resource Loading

`	ypescript
interface ResourceManager {
  get(type: ResourceType, id: string, locale?: string): ResourceHandle;
  list(type: ResourceType, prefix?: string): string[];
  exists(type: ResourceType, id: string): boolean;
  invalidate(id: string): void;
}

type ResourceType = 'icons' | 'translations' | 'fonts' | 'templates' |
                    'themes' | 'models' | 'ocr' | 'prompts' | 'workflow-templates';
`

Loading algorithm:
1. Lookup resource in plugin namespace.
2. If not found, check workspace override.
3. If not found, check runtime default.
4. If not found and lazy-allowed, trigger download.
5. Return ResourceHandle or null.

---


## 12 Resource Fallback Chain

`mermaid
graph LR
    P[Plugin Resource] -->|Found| R[Return]
    P -->|Not Found| W[Workspace Override]
    W -->|Found| R
    W -->|Not Found| D[Runtime Default]
    D -->|Found| R
    D -->|Not Found| L[Lazy Download]
    L -->|Success| R
    L -->|Fail| NULL[Return null]
`

---


## 14 Resource Versioning

Resources are versioned alongside their plugin:

`
<plugin_id>@<version>/icons/logo.png
`

On plugin update:
- Old resource versions are retained for 24 hours (grace period).
- Active references continue to use the old version.
- New references use the new version.

---



## 16 External Resource Download

Large resources (models, OCR) are downloaded on first use:

`	ypescript
interface DownloadManager {
  download(url: string, destination: string, hash: string): Promise<void>;
  cancel(download_id: string): void;
  getStatus(download_id: string): DownloadStatus;
}
`

Rules:
- Downloads require manifest-declared URLs (no arbitrary downloads).
- Downloaded resources are hashed and verified before use.
- Downloads are retried up to 3 times with exponential backoff.
- Download progress is reported via events.

---

- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 18 Performance Budgets

- Resource lookup (cached): < 0.1ms.
- Resource lookup (uncached, filesystem): < 1ms.
- Resource lookup (external download): < 100ms (first), < 1ms (cached).
- Cache eviction: < 10ms.
- Max resource namespace size: 100 MB per plugin.

---

| RFC-0201 | Consumed | Plugin Overview |


## 20 Acceptance Criteria

1. GIVEN a plugin requests an icon by ID, WHEN the icon exists in the namespace, THEN the icon is returned.
2. GIVEN a plugin requests a translation, WHEN the locale file is missing, THEN the fallback locale (en) is returned.
3. GIVEN a plugin requests a model, WHEN the model is not bundled, THEN a lazy download is triggered.
4. GIVEN a downloaded model's hash does not match the manifest, THEN the download is rejected and an error is logged.
5. GIVEN a plugin is updated, WHEN resource cache is checked, THEN the old cache is cleared within 24 hours.
6. GIVEN two plugins request the same icon ID, WHEN resolved, THEN each gets their own namespace's icon.

---



## 22 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [LRU Cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU) — Cache replacement policy.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 24 Future Evolution

1. Support for resource CDNs with geo-aware download routing.
2. Support for resource compression on download.
3. Support for resource analytics (usage frequency, popular resources).

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

All plugin contracts are defined as abstract behavioral interfaces.

---





---

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0012 (and ADR-0010 if security-related) |
| Related JSON Schema | See References section |
| Related Catalog | See References section |

---


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |