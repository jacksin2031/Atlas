# Plugin Dependency Types Catalog

## 1. Purpose

This catalog defines the canonical set of dependency relationship types that describe how plugins depend on one another and on the Atlas runtime. Each dependency type carries distinct semantics for resolution, enforcement, and failure handling.

## 2. Stable ID Prefix

All dependency type identifiers use the prefix `DEP-TYPE-`. This prefix is reserved exclusively for plugin dependency relationship definitions within the Atlas ecosystem.

## 3. Naming Convention

Dependency type identifiers MUST conform to the pattern `DEP-TYPE-<CATEGORY>-<CONSTRAINT>` where `<CATEGORY>` denotes the dependency domain and `<CONSTRAINT>` denotes the enforcement strength. Both segments MUST use uppercase ASCII letters and hyphens.

## 4. Canonical Dependency Type Table

| Stable ID | Name | Enforcement | Failure Behavior | Resolution Timing |
|---|---|---|---|---|
| `DEP-TYPE-HARD-REQUIRED` | Hard Required | Mandatory; the dependent plugin MUST NOT load if the dependency is absent or incompatible. | Loading is blocked; the dependent plugin transitions to `PSTATE-FAILED`. | Evaluated at load time before `PSTATE-LOADED`. |
| `DEP-TYPE-SOFT-OPTIONAL` | Soft Optional | Permissive; the dependent plugin MAY function without the dependency, potentially with reduced capability. | The dependency is ignored; the dependent plugin continues loading with capability degradation. | Evaluated at load time; missing dependencies are recorded but do not block loading. |
| `DEP-TYPE-RUNTIME-NEEDED` | Runtime Needed | Conditional; the dependency is not required at load time but MUST be available when the dependent plugin executes specific functionality. | The dependent plugin MUST handle the absence gracefully at runtime and MUST NOT crash or corrupt state. | Evaluated at runtime when the relevant capability is invoked. |
| `DEP-TYPE-LOAD-ORDER` | Load Order | Sequential; the dependency MUST be loaded before the dependent plugin, but both MAY coexist independently. | Violation causes a load order error; the dependent plugin transitions to `PSTATE-ERROR` until the dependency is loaded. | Evaluated during the activation sequence. |
| `DEP-TYPE-CAPABILITY-REQUIRES` | Capability Requires | Functional; the dependency MUST provide a specific capability that the dependent plugin consumes. | The dependent plugin MUST NOT invoke the capability if the provider is unavailable; behavior is equivalent to soft optional for that capability. | Evaluated at capability resolution time. |
| `DEP-TYPE-COMPATIBILITY-CONFLICT` | Compatibility Conflict | Exclusionary; the dependent plugin MUST NOT coexist with the conflicting plugin in the same runtime instance. | Both plugins are blocked from loading; the runtime MUST report the conflict to the operator. | Evaluated at discovery time before loading begins. |
| `DEP-TYPE-FEATURE-FLAG` | Feature Flag | Conditional; the dependency is activated only when a named feature flag is enabled in the runtime configuration. | When the flag is disabled, the dependency is treated as absent; the dependent plugin adapts accordingly. | Evaluated at configuration load time. |

## 5. Dependency Resolution Rules

1. The `PIF-DEPENDENCY-RESOLVER` MUST evaluate all `DEP-TYPE-HARD-REQUIRED` dependencies before allowing any plugin to reach `PSTATE-ACTIVE`.
2. The `PIF-DEPENDENCY-RESOLVER` MUST compute a topological load order based on `DEP-TYPE-LOAD-ORDER` dependencies and MUST reject circular dependency chains.
3. `DEP-TYPE-COMPATIBILITY-CONFLICT` relationships MUST be symmetric; if plugin A declares a conflict with plugin B, then plugin B MUST also declare a conflict with plugin A, or the runtime MUST infer symmetry.
4. `DEP-TYPE-FEATURE-FLAG` dependencies MUST be evaluated after configuration is loaded and MUST NOT affect load order computation.
5. `DEP-TYPE-RUNTIME-NEEDED` dependencies MUST NOT block plugin loading; the runtime MUST track their availability and MUST notify the dependent plugin when they become available or unavailable.
6. `DEP-TYPE-CAPABILITY-REQUIRES` dependencies MUST be resolved through the `PIF-CAPABILITY-MANAGER` and MUST include the specific capability identifier in the dependency declaration.
7. `DEP-TYPE-SOFT-OPTIONAL` dependencies MUST be recorded in the plugin manifest metadata but MUST NOT prevent loading or activation.

## 6. Dependency Declaration Requirements

1. Every dependency declaration MUST specify the target `plugin_id`, the `DEP-TYPE-*` identifier, and any additional constraints (version range, capability name, feature flag name).
2. Version constraints MUST use semantic versioning comparison operators as defined in the Atlas versioning specification.
3. Circular dependency chains MUST NOT contain more than one `DEP-TYPE-HARD-REQUIRED` edge; chains consisting solely of `DEP-TYPE-LOAD-ORDER` edges are permitted if acyclic.
4. Conflicting plugins MUST NOT both reach `PSTATE-ACTIVE` simultaneously; the runtime MUST enforce mutual exclusion.

## 7. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin Dependency Resolution Specification: Defines the algorithm used by `PIF-DEPENDENCY-RESOLVER`.
- Atlas Plugin Versioning Specification: Defines the version comparison rules applied to dependency constraints.

## 8. Usage Guidelines

Plugin authors SHOULD declare the minimum dependency strength necessary; `DEP-TYPE-HARD-REQUIRED` SHOULD be used only when the dependent plugin cannot function at all without the dependency. Authors SHOULD prefer `DEP-TYPE-SOFT-OPTIONAL` when degraded functionality is acceptable. Authors MUST document which capabilities are affected by each `DEP-TYPE-SOFT-OPTIONAL` or `DEP-TYPE-RUNTIME-NEEDED` dependency. Runtime operators MUST review `DEP-TYPE-COMPATIBILITY-CONFLICT` declarations before deploying plugins in production environments.
