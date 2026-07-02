# RFC-0211: Plugin Dependency

RFC: RFC-0211
Title: Plugin Dependency
Status: Accepted
Version: 1.0.0
Category: Plugin
Layer: Extension
Normative: YES
Authors: Atlas Specification Committee
Created: 2026-06-30
Last Updated: 2026-07-01
Depends On:
  - RFC-0201 Plugin Overview
  - RFC-0202 Plugin Manifest
  - RFC-0204 Plugin Loader
  - RFC-0205 Plugin Registry
  - RFC-0206 Plugin Capability
Related RFC:
  - RFC-0212 Plugin Versioning
  - RFC-0203 Plugin Lifecycle
Related ADR:
  - ADR-0011 Dependency Management Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the dependency graph, dependency resolution, optional and required dependency handling, version constraints, circular dependency detection, dependency validation, dependency recovery, load order computation, and dependency visualization defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

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
9. [Dependency Graph](#9-dependency-graph)
10. [Dependency Resolution](#10-dependency-resolution)
11. [Optional Dependency](#11-optional-dependency)
12. [Required Dependency](#12-required-dependency)
13. [Version Constraints](#13-version-constraints)
14. [Circular Dependency Detection](#14-circular-dependency-detection)
15. [Dependency Validation](#15-dependency-validation)
16. [Dependency Recovery](#16-dependency-recovery)
17. [Load Order](#17-load-order)
18. [Dependency Visualization](#18-dependency-visualization)
19. [Dependency Types](#19-dependency-types)
20. [Dependency Metadata](#20-dependency-metadata)
21. [Performance Budgets](#21-performance-budgets)
22. [Glossary](#22-glossary)
23. [Acceptance Criteria](#23-acceptance-criteria)
24. [Cross References](#24-cross-references)
25. [References](#25-references)
26. [Revision History](#26-revision-history)
27. [Future Evolution](#27-future-evolution)

---

- RFC-0323 Workflow Plugin Integration

## 2 Goals

1. **Dependency Graph**: Maintain a directed graph representing all plugin dependencies.
2. **Dependency Resolution**: Compute satisfiable dependency configurations deterministically.
3. **Optional Dependencies**: Support graceful degradation when optional dependencies are absent.
4. **Required Dependencies**: Block activation when required dependencies are unsatisfied.
5. **Version Constraints**: Enforce version compatibility through semantic versioning.
6. **Circular Dependency Detection**: Identify and report dependency cycles at load time.
7. **Dependency Validation**: Verify dependency declarations against catalog constraints.
8. **Dependency Recovery**: Provide recovery strategies for failed dependency resolution.
9. **Load Order**: Compute deterministic topological load ordering.
10. **Dependency Visualization**: Enable operators to inspect dependency relationships.

---



## 4 Dependency Philosophy

Dependencies in the Plugin subsystem follow these principles:

- Dependencies express capability requirements, not implementation details.
- Dependencies are declarative; resolution is computed at load time.
- Circular dependencies are prohibited except through explicitly declared exceptions.
- Optional dependencies MUST NOT block loading; required dependencies MUST.
- Dependency resolution MUST be deterministic and reproducible.
---


## 6 Boundaries

Dependencies are bounded by:

- **Scope Boundary**: Dependencies are scoped to plugin identifiers; cross-subsystem dependencies are handled through capability interfaces.
- **Temporal Boundary**: Dependencies are resolved at load time; runtime availability is checked through capability queries.
- **Version Boundary**: Dependencies respect version constraints; incompatible versions are rejected.
- **Security Boundary**: Dependencies between plugins at different trust levels are subject to security policy evaluation.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

`mermaid
graph TD
    M[Plugin Manifest] -->|extracts deps| DR[Dependency Resolver]
    DR -->|builds graph| DG[Dependency Graph]
    DG -->|detects cycles| CD[Cycle Detector]
    CD -->|acyclic| TO[Topological Sort]
    TO -->|load order| LO[Load Order List]
    DR -->|version check| VC[Version Constraint Evaluator]
    VC -->|satisfied| ACT[Activate Plugin]
    VC -->|unsatisfied| FAIL[Reject Plugin]
    CD -->|cycle found| CIRC[Report Circular Dependency]
`

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 10 Dependency Resolution

Dependency resolution computes a valid configuration from the dependency graph:

1. **Collection**: Gather all plugin dependency declarations from manifests.
2. **Construction**: Build the directed dependency graph.
3. **Validation**: Check version constraints and dependency types.
4. **Cycle Detection**: Identify and report any circular dependencies.
5. **Topological Sort**: Compute a deterministic load order.
6. **Conflict Resolution**: Resolve version conflicts when multiple versions are required.
7. **Result**: Produce a resolved dependency configuration.

Resolution rules:

1. Resolution MUST be deterministic for identical inputs.
2. Resolution MUST fail if any required dependency is unsatisfied.
3. Resolution MUST succeed even if optional dependencies are unsatisfied.
4. Resolution MUST report all conflicts, not just the first one found.
5. Resolution MUST cache results to avoid recomputation.

---


## 12 Required Dependency

Required dependencies are blocking relationships:

1. A DEP-TYPE-HARD-REQUIRED dependency MUST be satisfied for the plugin to reach PSTATE-ACTIVE.
2. Unsatisfied required dependencies MUST prevent plugin activation.
3. Required dependency failures MUST emit PEVT-DEPENDENCY-FAILED events with the appropriate error code.
4. Required dependencies MUST be resolved before any plugin reaches PSTATE-ACTIVE.
5. Required dependencies MUST be included in load order computation.
6. The dependency resolver MUST report all unsatisfied required dependencies.
7. Required dependencies MAY be satisfied by transitive dependencies.
8. Required dependency resolution MUST be deterministic.

---


## 14 Circular Dependency Detection

Circular dependencies are detected and handled as follows:

1. The cycle detector MUST identify all cycles in the dependency graph.
2. Cycles MUST be reported with the full chain of plugins involved.
3. Plugins involved in a required dependency cycle MUST NOT be activated.
4. Optional dependency cycles are permitted but MUST be logged.
5. Cycle detection MUST complete within the configured timeout.
6. The cycle detector MUST distinguish between hard cycles and soft cycles.
7. Circular dependency errors MUST report PERR-CIRCULAR-DEPENDENCY.
8. Exception declarations for intentional circular dependencies MUST be recorded in the registry.

---


## 16 Dependency Recovery

Dependency recovery strategies for failed resolution:

1. If a required dependency fails resolution, the dependent plugin MUST transition to PSTATE-ERROR.
2. The recovery system MUST attempt to satisfy the dependency by loading missing plugins.
3. If recovery fails, the system MUST fall back to the previous known-good dependency configuration.
4. Recovery attempts MUST be logged with the failure reason and recovery action taken.
5. Recovery MUST NOT alter the dependency graph structure; it MAY only change plugin states.
6. Dependency recovery MUST respect the trust level constraints of the plugins involved.
7. Automatic recovery MUST be limited to a configurable number of attempts.
8. Persistent dependency failures MUST escalate to operator notification.
---


## 18 Dependency Visualization

Dependency visualization enables operators to inspect relationships:

1. The dependency graph MUST be serializable in a standard graph format.
2. Graph visualization MUST support filtering by dependency type, plugin ID, and capability.
3. Circular dependencies MUST be highlighted in visualizations.
4. Optional dependencies MUST be visually distinguished from required dependencies.
5. Dependency depth MUST be computable for any plugin in the graph.
6. Transitive dependencies MUST be visible in the visualization.
7. The visualization MUST support zoom and navigation for large graphs.
8. Dependency statistics (total plugins, total edges, average depth) MUST be available.

---

| Dependency | Direction | Description |
|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 20 Dependency Metadata

Every dependency declaration MUST include:

1. The target plugin_id.
2. The DEP-TYPE-* identifier.
3. The version constraint (if applicable).
4. The capability identifier (for DEP-TYPE-CAPABILITY-REQUIRES).
5. The feature flag name (for DEP-TYPE-FEATURE-FLAG).
6. A human-readable description of the dependency purpose.
7. The declaring plugin trust level for security evaluation.
8. Whether the dependency is required or optional.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 22 Glossary

| Term | Definition |
|---|---|
| Dependency Graph | A directed graph representing plugin dependency relationships. |
| Topological Sort | A linear ordering of graph nodes consistent with edge directions. |
| Cycle Detection | The process of identifying circular dependency chains. |
| Version Constraint | A rule defining acceptable version ranges for a dependency. |
| Required Dependency | A dependency that blocks loading if unsatisfied. |
| Optional Dependency | A dependency that does not block loading if unsatisfied. |
| Transitive Dependency | A dependency inferred through a chain of direct dependencies. |
| Load Order | The computed sequence in which plugins must be loaded. |
---

- **Expected Result**: Evaluation results are consistent with the compatibility interface.

#### AC-0211-006
- **Requirement**: The dependency cache MUST store resolution results keyed by the set of plugin IDs and their dependency declarations.
- **Verification**: Clear the cache and verify that subsequent resolutions miss the cache.
- **Expected Result**: Cache miss results in recomputation; cache hit returns stored result.

#### AC-0211-007
- **Requirement**: Dependency resolution MUST be idempotent: resolving the same graph twice MUST produce identical results.
- **Verification**: Resolve the same graph twice and compare results.
- **Expected Result**: Results are identical.

#### AC-0211-008
- **Requirement**: The dependency architecture MUST support graphs with at least 10,000 plugins.
- **Verification**: Construct and resolve a graph with 10,000 plugins.
- **Expected Result**: Resolution completes without errors within the performance budget.

#### AC-0211-009
- **Requirement**: Dependency metadata MUST be persisted in the registry.
- **Verification**: Resolve dependencies and query the registry for the metadata.
- **Expected Result**: Metadata is present and matches the resolution results.

#### AC-0211-010
- **Requirement**: The dependency resolver MUST log all resolution attempts and outcomes.
- **Verification**: Trigger a resolution and inspect the logs.
- **Expected Result**: Resolution attempt and outcome are logged.

### Dependency Graph (AC-0211-011 to AC-0211-018)

#### AC-0211-011
- **Requirement**: Each node in the dependency graph MUST represent a unique plugin identified by its plugin_id.
- **Verification**: Add two nodes with the same plugin ID and verify deduplication.
- **Expected Result**: Only one node exists for the duplicated plugin ID.

#### AC-0211-012
- **Requirement**: Each edge in the dependency graph MUST be labeled with a DEP-TYPE-* identifier.
- **Verification**: Inspect edges in the graph and verify labels.
- **Expected Result**: All edges have valid DEP-TYPE-* labels.

#### AC-0211-013
- **Requirement**: The graph MUST be queryable by plugin ID.
- **Verification**: Query the graph for a specific plugin ID and retrieve its dependencies.
- **Expected Result**: Correct dependencies are returned.

#### AC-0211-014
- **Requirement**: The graph MUST be queryable by dependency type.
- **Verification**: Query the graph for all DEP-TYPE-HARD-REQUIRED edges.
- **Expected Result**: Only required dependency edges are returned.

#### AC-0211-015
- **Requirement**: The graph MUST support transitive dependency resolution.
- **Verification**: Resolve transitive dependencies for a plugin three levels deep.
- **Expected Result**: All transitive dependencies are returned.

#### AC-0211-016
- **Requirement**: The graph MUST distinguish between required and optional edges.
- **Verification**: Inspect edge types in the graph.
- **Expected Result**: Required and optional edges are correctly classified.

#### AC-0211-017
- **Requirement**: The graph MUST be rebuildable from plugin manifests at any time.
- **Verification**: Destroy the graph and rebuild it from manifests.
- **Expected Result**: Rebuilt graph is identical to the original.

#### AC-0211-018
- **Requirement**: The graph MUST include both direct and transitive dependencies.
- **Verification**: Query for both direct and transitive dependencies of a plugin.
- **Expected Result**: Both sets are present and correctly distinguished.

### Dependency Resolution (AC-0211-019 to AC-0211-025)

#### AC-0211-019
- **Requirement**: Dependency resolution MUST be deterministic for identical inputs.
- **Verification**: Run resolution three times on the same graph and compare results.
- **Expected Result**: All three results are identical.

#### AC-0211-020
- **Requirement**: Resolution MUST fail if any required dependency is unsatisfied.
- **Verification**: Declare a required dependency on a non-existent plugin.
- **Expected Result**: Resolution fails and reports the unsatisfied dependency.

#### AC-0211-021
- **Requirement**: Resolution MUST succeed even if optional dependencies are unsatisfied.
- **Verification**: Declare an optional dependency on a non-existent plugin.
- **Expected Result**: Resolution succeeds with the optional dependency noted as unsatisfied.

#### AC-0211-022
- **Requirement**: Resolution MUST report all conflicts, not just the first one found.
- **Verification**: Introduce multiple version conflicts and run resolution.
- **Expected Result**: All conflicts are reported in the resolution result.

#### AC-0211-023
- **Requirement**: Resolution MUST cache results to avoid recomputation.
- **Verification**: Resolve a graph, clear the graph, and resolve again with the same inputs.
- **Expected Result**: Second resolution uses cached result.

#### AC-0211-024
- **Requirement**: Resolution MUST complete within 100 milliseconds for up to 1,000 plugins.
- **Verification**: Measure resolution time for 1,000 plugins.
- **Expected Result**: Resolution completes within 100 milliseconds.

#### AC-0211-025
- **Requirement**: Resolution results MUST include the computed load order.
- **Verification**: Check resolution result for load order.
- **Expected Result**: Load order is present and valid.

### Optional/Required (AC-0211-026 to AC-0211-032)

#### AC-0211-026
- **Requirement**: A DEP-TYPE-SOFT-OPTIONAL dependency MUST NOT block plugin loading.
- **Verification**: Declare a soft optional dependency on a non-existent plugin and load the dependent plugin.
- **Expected Result**: Plugin loads successfully.

#### AC-0211-027
- **Requirement**: A DEP-TYPE-HARD-REQUIRED dependency MUST block loading if unsatisfied.
- **Verification**: Declare a hard required dependency on a non-existent plugin and attempt to load.
- **Expected Result**: Loading is blocked.

#### AC-0211-028
- **Requirement**: The plugin MUST document which capabilities are affected by each optional dependency.
- **Verification**: Inspect the plugin manifest for optional dependency documentation.
- **Expected Result**: Affected capabilities are documented.

#### AC-0211-029
- **Requirement**: Optional dependency failures MUST emit PEVT-DEPENDENCY-FAILED events.
- **Verification**: Trigger an optional dependency failure and check emitted events.
- **Expected Result**: Event is emitted with the correct identifier.

#### AC-0211-030
- **Requirement**: Optional dependencies MUST NOT affect load order computation.
- **Verification**: Compute load order with and without optional dependencies present.
- **Expected Result**: Load order is identical in both cases.

#### AC-0211-031
- **Requirement**: Required dependencies MUST be included in load order computation.
- **Verification**: Compute load order with required dependencies and verify ordering.
- **Expected Result**: Dependencies are loaded before dependents.

#### AC-0211-032
- **Requirement**: Required dependency failures MUST emit PEVT-DEPENDENCY-FAILED events.
- **Verification**: Trigger a required dependency failure and check emitted events.
- **Expected Result**: Event is emitted with the correct identifier and error code.

### Version Constraints (AC-0211-033 to AC-0211-038)

#### AC-0211-033
- **Requirement**: Version constraints MUST follow semantic versioning rules.
- **Verification**: Declare a version constraint using semver operators.
- **Expected Result**: Constraint is accepted and evaluated correctly.

#### AC-0211-034
- **Requirement**: Constraints MUST support range operators: equal, not-equal, greater-than, less-than, and range.
- **Verification**: Declare constraints using each operator type.
- **Expected Result**: Each constraint is evaluated correctly.

#### AC-0211-035
- **Requirement**: Version constraints MUST be declared in the plugin manifest under the dependencies field.
- **Verification**: Inspect a manifest with version constraints.
- **Expected Result**: Constraints are present under the dependencies field.

#### AC-0211-036
- **Requirement**: Incompatible versions MUST cause dependency resolution to fail.
- **Verification**: Declare a dependency with an incompatible version constraint.
- **Expected Result**: Resolution fails with a version incompatibility error.

#### AC-0211-037
- **Requirement**: Pre-release versions MUST be excluded from constraint matching unless explicitly included.
- **Verification**: Match a constraint against a pre-release version.
- **Expected Result**: Pre-release version is excluded.

#### AC-0211-038
- **Requirement**: Version constraint syntax MUST be consistent across all dependency declarations.
- **Verification**: Declare version constraints in multiple manifests and compare parsing results.
- **Expected Result**: All constraints are parsed consistently.

### Circular Detection (AC-0211-039 to AC-0211-044)

#### AC-0211-039
- **Requirement**: The cycle detector MUST identify all cycles in the dependency graph.
- **Verification**: Construct a graph with multiple cycles and run the detector.
- **Expected Result**: All cycles are identified.

#### AC-0211-040
- **Requirement**: Cycles MUST be reported with the full chain of plugins involved.
- **Verification**: Inspect cycle detection output for a known cycle.
- **Expected Result**: Output includes the complete chain.

#### AC-0211-041
- **Requirement**: Plugins involved in a required dependency cycle MUST NOT be activated.
- **Verification**: Create a required dependency cycle and attempt activation.
- **Expected Result**: Activation is blocked.

#### AC-0211-042
- **Requirement**: Optional dependency cycles are permitted but MUST be logged.
- **Verification**: Create an optional dependency cycle and check logs.
- **Expected Result**: Cycle is logged.

#### AC-0211-043
- **Requirement**: Cycle detection MUST complete within 100 milliseconds for up to 1,000 plugins.
- **Verification**: Measure cycle detection time for 1,000 plugins.
- **Expected Result**: Detection completes within 100 milliseconds.

#### AC-0211-044
- **Requirement**: Circular dependency errors MUST report PERR-CIRCULAR-DEPENDENCY.
- **Verification**: Trigger a circular dependency and check the error code.
- **Expected Result**: Error code is PERR-CIRCULAR-DEPENDENCY.

### Validation (AC-0211-045 to AC-0211-050)

#### AC-0211-045
- **Requirement**: Every dependency declaration MUST reference a valid plugin ID from the registry.
- **Verification**: Declare a dependency on a non-existent plugin ID.
- **Expected Result**: Declaration is rejected.

#### AC-0211-046
- **Requirement**: Every dependency type MUST be a valid DEP-TYPE-* identifier from the catalog.
- **Verification**: Declare a dependency with an invalid type.
- **Expected Result**: Declaration is rejected.

#### AC-0211-047
- **Requirement**: Self-dependencies MUST be rejected.
- **Verification**: Declare a dependency on the declaring plugin itself.
- **Expected Result**: Declaration is rejected.

#### AC-0211-048
- **Requirement**: Version constraints MUST be syntactically valid.
- **Verification**: Declare a dependency with an invalid version constraint syntax.
- **Expected Result**: Declaration is rejected.

#### AC-0211-049
- **Requirement**: Dependency validation MUST occur before dependency resolution.
- **Verification**: Attempt resolution with invalid dependencies.
- **Expected Result**: Validation fails before resolution begins.

#### AC-0211-050
- **Requirement**: Validation failures MUST emit PEVT-MANIFEST-INVALID events.
- **Verification**: Trigger a validation failure and check emitted events.
- **Expected Result**: Event is emitted with the correct identifier.

### Recovery (AC-0211-051 to AC-0211-056)

#### AC-0211-051
- **Requirement**: If a required dependency fails resolution, the dependent plugin MUST transition to PSTATE-ERROR.
- **Verification**: Trigger a required dependency failure and check plugin state.
- **Expected Result**: Plugin transitions to PSTATE-ERROR.

#### AC-0211-052
- **Requirement**: The recovery system MUST attempt to satisfy the dependency by loading missing plugins.
- **Verification**: Trigger a dependency failure and verify recovery attempt.
- **Expected Result**: Missing plugin is loaded.

#### AC-0211-053
- **Requirement**: If recovery fails, the system MUST fall back to the previous known-good dependency configuration.
- **Verification**: Simulate recovery failure and check fallback.
- **Expected Result**: Previous configuration is restored.

#### AC-0211-054
- **Requirement**: Recovery attempts MUST be logged with the failure reason and recovery action taken.
- **Verification**: Check recovery logs.
- **Expected Result**: Logs contain failure reason and recovery action.

#### AC-0211-055
- **Requirement**: Recovery MUST NOT alter the dependency graph structure.
- **Verification**: Compare the graph before and after recovery.
- **Expected Result**: Graph structure is unchanged.

#### AC-0211-056
- **Requirement**: Automatic recovery MUST be limited to a configurable number of attempts.
- **Verification**: Set a maximum of 3 recovery attempts and trigger repeated failures.
- **Expected Result**: After 3 attempts, recovery stops and escalation occurs.

### Load Order (AC-0211-057 to AC-0211-062)

#### AC-0211-057
- **Requirement**: Load order MUST be a topological sort of the dependency graph.
- **Verification**: Compare load order to a manual topological sort.
- **Expected Result**: Orders are consistent.

#### AC-0211-058
- **Requirement**: Plugins with no dependencies MUST be loaded first.
- **Verification**: Check load order for leaf plugins.
- **Expected Result**: Leaf plugins appear first.

#### AC-0211-059
- **Requirement**: A plugin MUST NOT be loaded before any of its required dependencies.
- **Verification**: Check load order for a plugin and its dependencies.
- **Expected Result**: Dependencies appear before the plugin.

#### AC-0211-060
- **Requirement**: Load order MUST be deterministic: the same graph MUST always produce the same order.
- **Verification**: Compute load order three times on the same graph.
- **Expected Result**: All three orders are identical.

#### AC-0211-061
- **Requirement**: Plugins with equivalent load positions MUST be loaded in alphabetical order by plugin ID.
- **Verification**: Create two plugins with no dependencies and check load order.
- **Expected Result**: Plugins are loaded alphabetically.

#### AC-0211-062
- **Requirement**: Load order changes MUST emit PEVT-DEPENDENCY-RESOLVED events.
- **Verification**: Change the dependency graph and check emitted events.
- **Expected Result**: Event is emitted with the correct identifier.

### Performance (AC-0211-063 to AC-0211-065)

#### AC-0211-063
- **Requirement**: Topological sort MUST complete within 50 milliseconds for up to 1,000 plugins.
- **Verification**: Measure topological sort time for 1,000 plugins.
- **Expected Result**: Sort completes within 50 milliseconds.

#### AC-0211-064
- **Requirement**: Version constraint evaluation MUST complete within 1 millisecond per constraint.
- **Verification**: Evaluate 10,000 constraints and measure time per constraint.
- **Expected Result**: Average time is at or below 1 millisecond.

#### AC-0211-065
- **Requirement**: Dependency resolution caching MUST achieve at least 90% hit rate for repeated resolutions.
- **Verification**: Resolve the same graph 100 times and count cache hits.
- **Expected Result**: Hit rate is at or above 90%.

### Security (AC-0211-066 to AC-0211-068)

#### AC-0211-066
- **Requirement**: Dependencies between plugins at different trust levels MUST be subject to security policy evaluation.
- **Verification**: Declare a dependency between plugins at different trust levels.
- **Expected Result**: Security policy is evaluated and decision is recorded.

#### AC-0211-067
- **Requirement**: Dependency declarations MUST be tamper-evident.
- **Verification**: Modify a dependency declaration after signing and check integrity.
- **Expected Result**: Tampering is detected.

#### AC-0211-068
- **Requirement**: Cross-dependency consistency checks MUST verify symmetric conflict declarations.
- **Verification**: Declare a conflict asymmetrically and check resolution.
- **Expected Result**: Symmetry is inferred and enforced.

### Consistency (AC-0211-069 to AC-0211-072)

#### AC-0211-069
- **Requirement**: The dependency graph MUST be consistent with plugin manifests at all times.
- **Verification**: Modify a manifest and verify graph consistency.
- **Expected Result**: Graph is updated to reflect the manifest change.

#### AC-0211-070
- **Requirement**: Dependency metadata in the registry MUST match the computed dependency graph.
- **Verification**: Compare registry metadata to the computed graph.
- **Expected Result**: Metadata and graph are consistent.

#### AC-0211-071
- **Requirement**: Load order MUST be consistent with the dependency graph.
- **Verification**: Verify that no plugin appears before its dependencies in the load order.
- **Expected Result**: Load order respects all dependency edges.

#### AC-0211-072
- **Requirement**: Dependency resolution results MUST be reproducible after system restart.
- **Verification**: Resolve dependencies, restart the system, and resolve again.
- **Expected Result**: Results are identical.

### Edge Cases (AC-0211-073 to AC-0211-075)

#### AC-0211-073
- **Requirement**: The system MUST handle a plugin with 100 direct dependencies.
- **Verification**: Declare 100 dependencies for a single plugin and resolve.
- **Expected Result**: Resolution completes successfully.

#### AC-0211-074
- **Requirement**: The system MUST handle a dependency chain of 500 plugins deep.
- **Verification**: Create a chain of 500 plugins each depending on the previous.
- **Expected Result**: Resolution and load order are computed correctly.

#### AC-0211-075
- **Requirement**: The system MUST handle simultaneous dependency resolution for 100 plugins.
- **Verification**: Trigger resolution for 100 plugins concurrently.
- **Expected Result**: All resolutions complete without data corruption.

### Documentation (AC-0211-076 to AC-0211-077)

#### AC-0211-076
- **Requirement**: The dependency catalog MUST be published as a machine-readable reference alongside this specification.
- **Verification**: Locate the machine-readable dependency catalog document.
- **Expected Result**: Catalog is available and matches the identifiers in Section 19.

#### AC-0211-077
- **Requirement**: Dependency visualization documentation MUST include examples for each dependency type.
- **Verification**: Check that each dependency type has a visualization example.
- **Expected Result**: All dependency types have examples.

---

| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |



## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 25 References

1. RFC 2119: Key Words for Use in RFCs to Indicate Requirement Levels
2. Cormen, T. et al.: Introduction to Algorithms, Topological Sorting Chapter
3. Semantic Versioning 2.0.0: https://semver.org

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 27 Future Evolution

1. Support for dynamic dependency resolution at runtime.
2. Dependency health monitoring and predictive failure detection.
3. Automated dependency conflict resolution suggestions.
4. Dependency impact analysis for planned plugin removals.
5. Support for multi-tenant dependency isolation.

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