# RFC-0226: Plugin Dependency Resolution

RFC: RFC-0226
Title: Plugin Dependency Resolution
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
  - RFC-0211 Plugin Dependency
  - RFC-0212 Plugin Versioning
Related RFC:
  - RFC-0215 Plugin Service Model
  - RFC-0218 Plugin Compatibility
  - RFC-0225 Plugin Hot Reload
Related ADR:
  - ADR-0026 Dependency Resolution Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the dependency solver algorithm, circular dependency detection, optional dependency handling, soft dependency, hard dependency, version conflict resolution, dependency graph construction, topological sort, and resolution error handling requirements defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Dependency Philosophy](#4-dependency-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Dependency Types](#9-dependency-types)
10. [Dependency Graph](#10-dependency-graph)
11. [Dependency Solver](#11-dependency-solver)
12. [Circular Dependency Detection](#12-circular-dependency-detection)
13. [Version Conflict Resolution](#13-version-conflict-resolution)
14. [Topological Sort](#14-topological-sort)
15. [Resolution Errors](#15-resolution-errors)
16. [Performance Budgets](#16-performance-budgets)
17. [Glossary](#17-glossary)
18. [Acceptance Criteria](#18-acceptance-criteria)
19. [Cross References](#19-cross-references)
20. [References](#20-references)
21. [Revision History](#21-revision-history)
22. [Future Evolution](#22-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Solver Algorithm**: Deterministic, efficient dependency resolution.
2. **Circular Dependency Detection**: Detect and report cycles in the dependency graph.
3. **Optional Dependencies**: Plugins load even if optional dependencies are missing.
4. **Soft Dependencies**: Plugins load with degraded functionality if soft dependencies are missing.
5. **Hard Dependencies**: Plugin fails to load if hard dependencies are missing or incompatible.
6. **Version Conflict Resolution**: Resolve version conflicts using a defined precedence algorithm.
7. **Topological Sort**: Determine correct plugin load order.

---

- RFC-0323 Workflow Plugin Integration


## 4 Dependency Philosophy

Dependencies follow these principles:

- All dependencies are declared explicitly in the manifest.
- Hard dependencies are non-negotiable; missing hard dependencies block loading.
- Optional and soft dependencies are transparently handled.
- Circular dependencies are detected and rejected.
- Version conflicts are resolved by the solver using precedence rules.

---


## 6 Boundaries

- Dependency resolution happens BEFORE plugin loading.
- The resolver operates on the dependency graph constructed from all manifests.
- Resolution is deterministic: the same input always produces the same output.
- The resolver does NOT modify any manifests or plugin files.

---

| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
graph TB
    subgraph Manifests
        M1[Plugin A Manifest]
        M2[Plugin B Manifest]
        M3[Plugin C Manifest]
        M4[Plugin D Manifest]
    end
    subgraph Resolver
        DG[Dependency Graph Builder]
        CS[Cycle Detector]
        TS[Topological Sort]
        VCR[Version Conflict Resolver]
    end
    subgraph Output
        LO[Load Order]
        ERR[Errors]
        WARN[Warnings]
    end
    M1 --> DG
    M2 --> DG
    M3 --> DG
    M4 --> DG
    DG --> CS
    CS -->|No cycles| TS
    CS -->|Cycle found| ERR
    TS --> VCR
    VCR --> LO
    VCR -->|Conflicts resolved| WARN
`

---

{
  "dependencies": [
    {
      "name": "optional-ai-engine",
      "version_range": ">=1.0.0",
      "type": "optional"
    }
  ]
}
`

Behavior:
- If the dependency is missing, the plugin loads normally with that feature disabled.
- If available, the plugin uses the dependency.
- No error is generated for missing optional dependencies.

### 9.3 Soft Dependency

The plugin works with degraded functionality if this dependency is missing.

`json
{
  "dependencies": [
    {
      "name": "advanced-vision",
      "version_range": ">=1.0.0",
      "type": "soft"
    }
  ]
}
`

Behavior:
- If the dependency is missing, the plugin loads with degraded functionality.
- A WARNING is logged indicating which features are degraded.
- The plugin MUST gracefully handle the absence of soft dependencies.

### 9.4 Comparison Table

| Type        | Missing = Fail | Degraded Mode | Warning Logged | Load Order Impact |
|-------------|----------------|---------------|----------------|-------------------|
| Hard        | Yes            | No            | Yes            | Required          |
| Optional    | No             | Feature off   | No             | Preferred         |
| Soft        | No             | Yes            | Yes            | Preferred         |

---




## 12 Circular Dependency Detection

Circular dependencies are detected using Tarjan's algorithm for strongly connected components:

`
detect_cycles(graph):
  for each node in graph:
    if not visited[node]:
      scc = tarjan(node)
      if len(scc) > 1:
        return cycle_found(scc)
  return no_cycle
`

Cycle reporting:
- The cycle path is reported: A -> B -> C -> A.
- All plugins in the cycle are marked as DEP_CIRCULAR.
- None of the plugins in the cycle are loaded.
- The operator is notified with the cycle path.

Example:
`
ERROR: Circular dependency detected
  Plugin A (v1.0.0) depends on Plugin B (v2.0.0)
  Plugin B (v2.0.0) depends on Plugin C (v1.5.0)
  Plugin C (v1.5.0) depends on Plugin A (v1.0.0)
  Cycle: A -> B -> C -> A
ACTION: Remove or refactor one of the dependencies
`

---


---

4. Plugin A (depends on B, D)
`

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 16 Performance Budgets

- Graph construction: < 10ms for 1000 plugins.
- Cycle detection: < 50ms for 1000 plugins.
- Version conflict resolution: < 5ms per dependency.
- Topological sort: < 10ms for 1000 plugins.
- Full resolution: < 100ms for 1000 plugins.

---

| RFC-0201 | Consumed | Plugin Overview |


## 18 Acceptance Criteria

1. GIVEN Plugin A has a hard dependency on Plugin B v2.0+, WHEN Plugin B v1.0 is installed, THEN Plugin A fails to load with DEP_VERSION_HARD.
2. GIVEN Plugin A depends on Plugin B, AND Plugin B depends on Plugin A, WHEN resolution runs, THEN a circular dependency error is reported.
3. GIVEN Plugin A has an optional dependency on Plugin B, WHEN Plugin B is not installed, THEN Plugin A loads normally with that feature disabled.
4. GIVEN Plugin A has a soft dependency on Plugin B, WHEN Plugin B is not installed, THEN Plugin A loads with degraded functionality and a warning.
5. GIVEN three plugins require overlapping but compatible versions of Plugin X, WHEN resolution runs, THEN the highest compatible version is selected.
6. GIVEN the dependency graph has 1000 plugins, WHEN resolution completes, THEN it completes within 100ms.

---



## 20 References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [Tarjan's Strongly Connected Components](https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm)
- [Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting)

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 22 Future Evolution

1. Support for transitive dependency resolution across runtime instances.
2. Support for dependency visualization in the operator dashboard.
3. Support for automatic dependency resolution suggestions.

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