# RFC-0216: Plugin Discovery

RFC: RFC-0216
Title: Plugin Discovery
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
  - RFC-0205 Plugin Registry
Related RFC:
  - RFC-0213 Plugin Marketplace
  - RFC-0215 Plugin Service Model
  - RFC-0224 Plugin Testing
Related ADR:
  - ADR-0016 Discovery Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the discovery sources, discovery protocol, manifest scanning, index cache, hot reload discovery, network discovery, priority order, conflict detection, and discovery events requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Discovery Philosophy](#4-discovery-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Discovery Sources](#9-discovery-sources)
10. [Discovery Protocol](#10-discovery-protocol)
11. [Manifest Scanning](#11-manifest-scanning)
12. [Index Cache](#12-index-cache)
13. [Hot Reload Discovery](#13-hot-reload-discovery)
14. [Network Discovery](#14-network-discovery)
15. [Priority Order](#15-priority-order)
16. [Conflict Detection](#16-conflict-detection)
17. [Discovery Events](#17-discovery-events)
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

1. **Multi-Source Discovery**: Support multiple plugin sources simultaneously.
2. **Manifest Scanning**: Recursively scan directories for plugin manifests.
3. **Index Caching**: Maintain a runtime index for fast lookup.
4. **Hot Reload**: Detect workspace plugin changes without restart.
5. **Network Discovery**: Poll marketplace APIs with delta sync.
6. **Priority Ordering**: Resolve conflicts by source priority.
7. **Conflict Detection**: Detect duplicate name/version conflicts.
8. **Discovery Events**: Emit events for observability.

---

- RFC-0323 Workflow Plugin Integration


## 4 Discovery Philosophy

Discovery follows these principles:

- Multiple sources are queried concurrently.
- Priority order determines resolution of duplicates.
- Index caching reduces redundant scanning.
- Hot reload enables rapid plugin development.
- Conflict detection prevents ambiguous plugin states.

---


## 6 Boundaries

- Discovery reads plugin metadata only; it does NOT load or execute plugins.
- The discovery index is separate from the runtime service registry.
- Network discovery is limited to configured sources; arbitrary URLs are NOT scanned.

---



## 8 Architecture

`mermaid
graph TB
    subgraph Sources
        OFF[Official Repo]
        MKT[Marketplace]
        WS[Workspace]
        DEV[Dev Mode]
        PORT[Portable]
        ENT[Enterprise]
    end
    subgraph Discovery Engine
        SCAN[Manifest Scanner]
        CACHE[Index Cache]
        PRIORITY[Priority Resolver]
        CONFLICT[Conflict Detector]
    end
    subgraph Events
        DISC[plugin.discovering]
        FOUND[plugin.discovered]
        IDX[plugin.index-updated]
    end
    OFF --> SCAN
    MKT --> SCAN
    WS --> SCAN
    DEV --> SCAN
    PORT --> SCAN
    ENT --> SCAN
    SCAN --> CACHE
    CACHE --> PRIORITY
    PRIORITY --> CONFLICT
    CONFLICT --> FOUND
    CONFLICT --> IDX
`

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 10 Discovery Protocol

`	ypescript
interface DiscoveryRequest {
  sources: DiscoverySource[];
  filters?: DiscoveryFilters;
  trustLevel?: TrustLevel;
}

interface DiscoveryFilters {
  namePattern?: string;
  capability?: string;
  minVersion?: string;
  maxVersion?: string;
  author?: string;
}

interface DiscoveryResult {
  plugins: DiscoveredPlugin[];
  conflicts: Conflict[];
  scanDurationMs: number;
}

runtime.discovery.scan(request: DiscoveryRequest): DiscoveryResult;
`

Requirements:
- All sources MUST be scanned concurrently.
- Filters MUST be applied per-source where supported.
- Conflicts MUST be reported in the result.
- Scan duration MUST be measured and logged.

---

- Defining the requirements for this plugin subsystem component.
- Establishing the boundaries between plugin layers.


## 12 Index Cache

The index cache stores discovered plugin metadata for fast lookup:

`	ypescript
interface PluginIndexEntry {
  plugin_id: string;
  version: string;
  title: string;
  description: string;
  capabilities: string[];
  source: DiscoverySource;
  last_seen: ISO8601;
  checksum: string;
}

interface IndexCache {
  get(plugin_id: string): PluginIndexEntry | null;
  set(entry: PluginIndexEntry): void;
  remove(plugin_id: string): void;
  list(filter?: IndexFilter): PluginIndexEntry[];
  refresh(sources: DiscoverySource[]): Promise<void>;
}
`

Requirements:
- The cache MUST have a configurable TTL (default: 5 minutes).
- Expired entries MUST be refreshed on next query.
- The cache MUST persist to disk for cross-session lookup.
- Cache refresh MUST detect changes via checksum comparison.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 14 Network Discovery

Network discovery polls marketplace or enterprise APIs:

`	ypescript
interface NetworkDiscovery {
  poll(source: MarketplaceEndpoint, since?: ISO8601): NetworkDiscoveryResult;
}

interface NetworkDiscoveryResult {
  new_plugins: DiscoveredPlugin[];
  updated_plugins: DiscoveredPlugin[];
  removed_plugins: string[];
}
`

Requirements:
- Polling MUST use delta sync (since last successful poll timestamp).
- Network failures MUST NOT block local discovery.
- Poll interval MUST be configurable (default: 1 hour).
- Rate limits MUST be respected with exponential backoff.

---

- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 16 Conflict Detection

Conflicts are detected when:

| Condition                           | Conflict Code     | Resolution                           |
|-------------------------------------|-------------------|--------------------------------------|
| Same name, same source, different versions | DUP_VERSION   | Higher version wins (log warning)    |
| Same name, different sources        | DUP_SOURCE        | Priority order wins (log info)       |
| Same name, incompatible capabilities| CAP_CONFLICT      | Report to operator, block loading    |

Requirements:
- Conflicts MUST be reported in the DiscoveryResult.
- Blocking conflicts MUST prevent plugin loading.
- Warning conflicts MUST allow loading with a log entry.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 18 Performance Budgets

- Full discovery scan: < 2 seconds for up to 100 sources.
- Index cache lookup: < 1ms.
- Hot reload detection: < 100ms from file change to index update.
- Network poll: < 5 seconds per endpoint.
- Memory usage for index: < 50 MB for 10,000 plugins.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Acceptance Criteria

1. GIVEN multiple sources contain a plugin with the same name, WHEN discovery runs, THEN the highest-priority source's plugin is selected.
2. GIVEN a workspace plugin manifest changes, WHEN the file watcher detects the change, THEN the index is updated within 100ms.
3. GIVEN a network marketplace endpoint returns 5 new plugins, WHEN poll completes, THEN 5 new index entries are created.
4. GIVEN two plugins with the same name in the same source with different versions, WHEN discovery runs, THEN the higher version is selected and a warning is logged.
5. GIVEN the network endpoint is unreachable, WHEN discovery runs, THEN local sources are still scanned successfully.
6. GIVEN a plugin directory is deleted from the workspace, WHEN the file watcher detects deletion, THEN the plugin is removed from the index.

---



## 22 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [inotify](https://man7.org/linux/man-pages/man7/inotify.7.html) — Linux file system event notification.
- [Watchdog](https://github.com/gorakhargosh/watchdog) — File system monitoring library.

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 24 Future Evolution

1. Support for plugin source authentication (OAuth tokens for marketplace).
2. Support for plugin source ranking by operator reputation scores.
3. Support for distributed discovery across multiple runtime instances.

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