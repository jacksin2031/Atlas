# RFC-0212: Plugin Versioning

RFC: RFC-0212
Title: Plugin Versioning
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
  - RFC-0211 Plugin Dependency
Related RFC:
  - RFC-0203 Plugin Lifecycle
  - RFC-0213 Plugin Marketplace
Related ADR:
  - ADR-0012 Semantic Versioning Architecture
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

This specification is Normative. Every Atlas implementation MUST conform to the semantic versioning rules, compatibility model, breaking change identification, migration procedures, deprecation policies, upgrade and downgrade mechanisms, rollback procedures, compatibility matrix, manifest evolution, API evolution, and schema evolution defined in this document. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution, ADR-0005, and RFC-0201.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Goals](#2-goals)
3. [Non-Goals](#3-non-goals)
4. [Versioning Philosophy](#4-versioning-philosophy)
5. [Ownership](#5-ownership)
6. [Boundaries](#6-boundaries)
7. [Runtime Invariants](#7-runtime-invariants)
8. [Architecture](#8-architecture)
9. [Semantic Versioning](#9-semantic-versioning)
10. [Compatibility Model](#10-compatibility-model)
11. [Breaking Changes](#11-breaking-changes)
12. [Migration](#12-migration)
13. [Deprecation](#13-deprecation)
14. [Upgrade](#14-upgrade)
15. [Downgrade](#15-downgrade)
16. [Rollback](#16-rollback)
17. [Compatibility Matrix](#17-compatibility-matrix)
18. [Manifest Evolution](#18-manifest-evolution)
19. [API Evolution](#19-api-evolution)
20. [Schema Evolution](#20-schema-evolution)
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

1. **Semantic Versioning**: Adopt semantic versioning (MAJOR.MINOR.PATCH) for all plugin versions.
2. **Compatibility Model**: Define clear compatibility rules between version ranges.
3. **Breaking Change Identification**: Provide criteria for identifying breaking changes.
4. **Migration Procedures**: Define migration paths for version upgrades.
5. **Deprecation Policies**: Establish deprecation timelines and notification mechanisms.
6. **Upgrade Mechanisms**: Support safe version upgrades with rollback capability.
7. **Downgrade Mechanisms**: Support safe version downgrades when required.
8. **Rollback Procedures**: Define automated rollback on upgrade failure.
9. **Compatibility Matrix**: Maintain a registry of compatible version pairs.
10. **Manifest Evolution**: Define rules for manifest schema changes across versions.
11. **API Evolution**: Define rules for API changes across plugin versions.
12. **Schema Evolution**: Define rules for data schema changes across plugin versions.

---



## 4 Versioning Philosophy

Versioning in the Plugin subsystem follows these principles:

- Versions are immutable identifiers of plugin state at a point in time.
- Semantic versioning provides a predictable compatibility contract.
- Breaking changes MUST increment the major version.
- Deprecation provides a migration window before breaking changes.
- Rollback capability ensures upgrade safety.

---


## 6 Boundaries

Versioning is bounded by:

- **Scope Boundary**: Version constraints apply within the plugin subsystem; cross-subsystem versioning is handled through capability interfaces.
- **Temporal Boundary**: Versions are immutable once published; new versions are created through the upgrade process.
- **Compatibility Boundary**: Compatibility is defined within major version ranges; cross-major compatibility requires migration.
- **Security Boundary**: Version changes that affect security posture MUST be flagged as security-relevant.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 8 Architecture

```mermaid
classDiagram
    class Version {
        +string major
        +string minor
        +string patch
        +string preRelease
        +string buildMetadata
        +compare(other) bool
        +isCompatibleWith(other) bool
    }
    class CompatibilityMatrix {
        +Map~string,Set~string~~ supportedVersions
        +checkCompatibility(pluginId, version) bool
        +addCompatibility(pluginId, versionPair) void
    }
    class MigrationPlan {
        +string sourceVersion
        +string targetVersion
        +List~Step~ migrationSteps
        +validate() bool
    }
    class DeprecationPolicy {
        +string pluginId
        +string deprecatedVersion
        +string sunsetDate
        +bool isActive()
    }
    Version --> CompatibilityMatrix : evaluates
    MigrationPlan --> Version : references
    DeprecationPolicy --> Version : tracks

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 10 Compatibility Model

The compatibility model defines which versions are compatible:

1. **Backward compatibility**: A newer version is backward-compatible with an older version if it accepts all inputs accepted by the older version.
2. **Forward compatibility**: An older version is forward-compatible with a newer version if it produces correct outputs for inputs accepted by the newer version.
3. **Same-major compatibility**: All versions with the same major version number are considered same-major compatible.
4. **Cross-major compatibility**: Versions with different major version numbers are NOT compatible without migration.
5. **Dependency compatibility**: A plugin is compatible with its dependencies if all dependency version constraints are satisfied.

---



## 12 Migration

Migration procedures enable safe version upgrades:

1. Every major version upgrade MUST include a migration plan.
2. Migration plans MUST describe all data transformations required.
3. Migration plans MUST be reversible to support rollback.
4. Migration plans MUST be validated before execution.
5. Migration failures MUST trigger automatic rollback.
6. Migration progress MUST be reported through lifecycle events.
7. Migration plans MUST be stored in the plugin registry.
8. Operators MUST be able to preview migration impacts before execution.

---


## 14 Upgrade

Upgrade procedures manage version increases:

1. Upgrades MUST follow the migration plan defined for the target version.
2. Upgrades MUST be atomic: either the full upgrade completes or the system rolls back.
3. Upgrades MUST preserve plugin state across the version boundary.
4. Upgrades MUST validate the target version against the compatibility matrix.
5. Upgrades MUST emit `PEVT-UPDATED` events upon completion.
6. Upgrades MUST be reversible through the rollback mechanism.
7. Concurrent upgrades of interdependent plugins MUST be coordinated through the dependency resolver.
8. Upgrade failures MUST trigger automatic rollback to the previous version.

---


## 16 Rollback

Rollback procedures revert failed upgrades:

1. Rollback MUST restore the previous version's binary, manifest, and configuration.
2. Rollback MUST restore the previous version's persisted state.
3. Rollback MUST be automatic when an upgrade fails during migration.
4. Rollback MUST be manual when explicitly requested by an operator.
5. Rollback operations MUST emit `PEVT-ROLLBACK` events.
6. Rollback MUST verify the integrity of the restored version.
7. Rollback MUST re-register the restored version with the registry.
8. Rollback failures MUST escalate to operator intervention.

---


## 18 Manifest Evolution

Manifest schema evolution rules:

1. New REQUIRED fields MUST NOT be added to the manifest schema without a major version increment.
2. New OPTIONAL fields MAY be added to the manifest schema without version increment.
3. REQUIRED fields MUST NOT be removed without a major version increment.
4. REQUIRED fields MAY be renamed with a major version increment and a migration path.
5. Field type changes MUST be accompanied by a major version increment.
6. Enumeration value additions MUST be backward-compatible.
7. Enumeration value removals MUST be accompanied by a major version increment.
8. Manifest schema versions MUST be declared in the `manifest_version` field.

---


## 20 Schema Evolution

Data schema evolution rules:

1. New data fields MAY be added without version increment.
2. Existing data fields MUST NOT be removed without a major version increment.
3. Data field type changes MUST be accompanied by a major version increment and a migration plan.
4. Data format changes MUST include a migration path.
5. Data validation rules MAY be relaxed without version increment.
6. Data validation rules MUST NOT be tightened without a major version increment.
7. Index changes MUST NOT affect data integrity.
8. Schema migrations MUST be idempotent.

---

|---|---|---|
| RFC-0001 | Consumed | Runtime Overview |
| RFC-0201 | Consumed | Plugin Overview |


## 22 Glossary

| Term | Definition |
|---|---|
| Semantic Versioning | A versioning scheme using MAJOR.MINOR.PATCH format. |
| Breaking Change | A change that violates backward compatibility. |
| Compatibility Matrix | A registry of compatible version pairs. |
| Migration Plan | A set of steps for upgrading between major versions. |
| Deprecation | The process of marking a version for eventual removal. |
| Rollback | The process of reverting to a previous version. |
| Sunset Date | The date after which a deprecated version is no longer supported. |
| Pre-release Version | A version identifier indicating the release is not final. |

---

- **Expected Result**: Normal version has higher precedence.

#### AC-0212-006
- **Requirement**: Build metadata MUST NOT affect version precedence.
- **Verification**: Compare two versions with identical MAJOR.MINOR.PATCH but different build metadata.
- **Expected Result**: Versions are considered equal in precedence.

#### AC-0212-007
- **Requirement**: Versions MUST be compared numerically, not lexicographically.
- **Verification**: Compare version 1.9.0 with version 1.10.0.
- **Expected Result**: 1.10.0 is correctly identified as greater than 1.9.0.

#### AC-0212-008
- **Requirement**: Version strings MUST be globally unique within a plugin's history.
- **Verification**: Attempt to register a duplicate version.
- **Expected Result**: Duplicate registration is rejected.

#### AC-0212-009
- **Requirement**: Version increments MUST be monotonic.
- **Verification**: Attempt to register a version lower than the current version.
- **Expected Result**: Registration is rejected.

#### AC-0212-010
- **Requirement**: The manifest version field MUST match a registered schema version.
- **Verification**: Submit a manifest with an unregistered schema version.
- **Expected Result**: Manifest is rejected.

### Compatibility (AC-0212-011 to AC-0212-018)

#### AC-0212-011
- **Requirement**: Same-major versions MUST be considered backward-compatible.
- **Verification**: Check compatibility between two versions with the same major number.
- **Expected Result**: Versions are marked as compatible.

#### AC-0212-012
- **Requirement**: Cross-major versions MUST NOT be considered compatible without migration.
- **Verification**: Check compatibility between versions with different major numbers.
- **Expected Result**: Versions are marked as incompatible.

#### AC-0212-013
- **Requirement**: Dependency compatibility MUST be evaluated against the compatibility matrix.
- **Verification**: Resolve dependencies with version constraints spanning multiple major versions.
- **Expected Result**: Resolution fails for incompatible version pairs.

#### AC-0212-014
- **Requirement**: The compatibility matrix MUST support transitive compatibility inference.
- **Verification**: Check compatibility through a chain of three versions.
- **Expected Result**: Transitive compatibility is correctly inferred.

#### AC-0212-015
- **Requirement**: The compatibility matrix MUST be queryable by plugin ID and version pair.
- **Verification**: Query the matrix for a specific version pair.
- **Expected Result**: Correct compatibility status is returned.

#### AC-0212-016
- **Requirement**: The compatibility matrix MUST be persisted in the registry.
- **Verification**: Query the registry for the compatibility matrix.
- **Expected Result**: Matrix data is present and complete.

#### AC-0212-017
- **Requirement**: The compatibility matrix MUST be updated automatically when new versions are published.
- **Verification**: Publish a new version and check the matrix.
- **Expected Result**: Matrix is updated without manual intervention.

#### AC-0212-018
- **Requirement**: The compatibility matrix MUST distinguish between backward-compatible, forward-compatible, and incompatible versions.
- **Verification**: Query the matrix for each compatibility type.
- **Expected Result**: Each type is correctly categorized.

### Breaking Changes (AC-0212-019 to AC-0212-024)

#### AC-0212-019
- **Requirement**: Removing a declared capability MUST increment the major version.
- **Verification**: Remove a capability and check the version.
- **Expected Result**: Major version is incremented.

#### AC-0212-020
- **Requirement**: Changing a public interface signature MUST increment the major version.
- **Verification**: Modify an interface signature and check the version.
- **Expected Result**: Major version is incremented.

#### AC-0212-021
- **Requirement**: Modifying the manifest schema incompatibly MUST increment the major version.
- **Verification**: Modify the manifest schema incompatibly and check the version.
- **Expected Result**: Major version is incremented.

#### AC-0212-022
- **Requirement**: Breaking changes MUST be documented in release notes.
- **Verification**: Check release notes for a major version update.
- **Expected Result**: Breaking changes are documented.

#### AC-0212-023
- **Requirement**: All seven categories of breaking changes defined in Section 11 MUST be detected.
- **Verification**: Trigger each category of breaking change.
- **Expected Result**: Each is detected and flagged.

#### AC-0212-024
- **Requirement**: Breaking change detection MUST occur before version increment.
- **Verification**: Attempt to increment the version without documenting breaking changes.
- **Expected Result**: Increment is rejected.

### Migration (AC-0212-025 to AC-0212-030)

#### AC-0212-025
- **Requirement**: Every major version upgrade MUST include a migration plan.
- **Verification**: Attempt a major version upgrade without a migration plan.
- **Expected Result**: Upgrade is blocked.

#### AC-0212-026
- **Requirement**: Migration plans MUST describe all required data transformations.
- **Verification**: Inspect a migration plan for completeness.
- **Expected Result**: All transformations are described.

#### AC-0212-027
- **Requirement**: Migration plans MUST be reversible.
- **Verification**: Execute a migration and then its reverse.
- **Expected Result**: Original state is restored.

#### AC-0212-028
- **Requirement**: Migration plans MUST be validated before execution.
- **Verification**: Submit an invalid migration plan and attempt execution.
- **Expected Result**: Execution is blocked.

#### AC-0212-029
- **Requirement**: Migration failures MUST trigger automatic rollback.
- **Verification**: Simulate a migration failure.
- **Expected Result**: Rollback is initiated automatically.

#### AC-0212-030
- **Requirement**: Migration progress MUST be reported through lifecycle events.
- **Verification**: Monitor events during a migration.
- **Expected Result**: Progress events are emitted.

### Deprecation (AC-0212-031 to AC-0212-036)

#### AC-0212-031
- **Requirement**: Deprecated versions MUST continue to function until the sunset date.
- **Verification**: Attempt to use a deprecated version before the sunset date.
- **Expected Result**: Version functions normally.

#### AC-0212-032
- **Requirement**: Sunset dates MUST be at least 12 months from the deprecation announcement.
- **Verification**: Check sunset dates for all deprecated versions.
- **Expected Result**: All sunset dates are at or after the 12-month minimum.

#### AC-0212-033
- **Requirement**: Deprecation notices MUST be emitted as events through the event bus.
- **Verification**: Deprecate a version and check emitted events.
- **Expected Result**: Deprecation event is emitted.

#### AC-0212-034
- **Requirement**: Deprecated versions MUST NOT receive security patches except for critical vulnerabilities.
- **Verification**: Attempt to patch a non-critical vulnerability in a deprecated version.
- **Expected Result**: Patch is rejected.

#### AC-0212-035
- **Requirement**: New installations MUST NOT be permitted for deprecated versions after the sunset date.
- **Verification**: Attempt to install a deprecated version after sunset.
- **Expected Result**: Installation is blocked.

#### AC-0212-036
- **Requirement**: Deprecation status MUST be queryable through the registry.
- **Verification**: Query the registry for a deprecated version's status.
- **Expected Result**: Deprecation status is returned.

### Upgrade/Downgrade/Rollback (AC-0212-037 to AC-0212-048)

#### AC-0212-037
- **Requirement**: Upgrades MUST follow the migration plan defined for the target version.
- **Verification**: Attempt an upgrade that bypasses the migration plan.
- **Expected Result**: Upgrade is blocked.

#### AC-0212-038
- **Requirement**: Upgrades MUST be atomic: either full completion or full rollback.
- **Verification**: Interrupt an upgrade midway and check the result.
- **Expected Result**: System is rolled back to the pre-upgrade state.

#### AC-0212-039
- **Requirement**: Upgrades MUST preserve plugin state across the version boundary.
- **Verification**: Check plugin state after an upgrade.
- **Expected Result**: State is preserved.

#### AC-0212-040
- **Requirement**: Upgrades MUST validate the target version against the compatibility matrix.
- **Verification**: Attempt an upgrade to an incompatible version.
- **Expected Result**: Upgrade is blocked.

#### AC-0212-041
- **Requirement**: Upgrades MUST emit `PEVT-UPDATED` events upon completion.
- **Verification**: Complete an upgrade and check emitted events.
- **Expected Result**: Update event is emitted.

#### AC-0212-042
- **Requirement**: Downgrades MUST be permitted only when explicitly requested by an operator.
- **Verification**: Attempt an automatic downgrade.
- **Expected Result**: Downgrade is blocked.

#### AC-0212-043
- **Requirement**: Downgrades MUST follow a reverse migration plan.
- **Verification**: Attempt a downgrade without a reverse migration plan.
- **Expected Result**: Downgrade is blocked.

#### AC-0212-044
- **Requirement**: Downgrades of plugins with hard dependencies on newer versions MUST be blocked.
- **Verification**: Attempt a downgrade that violates a hard dependency.
- **Expected Result**: Downgrade is blocked.

#### AC-0212-045
- **Requirement**: Rollback MUST restore the previous version's binary, manifest, and configuration.
- **Verification**: Roll back and check restored components.
- **Expected Result**: All components are restored.

#### AC-0212-046
- **Requirement**: Rollback MUST restore the previous version's persisted state.
- **Verification**: Roll back and check persisted state.
- **Expected Result**: State is restored.

#### AC-0212-047
- **Requirement**: Rollback MUST be automatic when an upgrade fails during migration.
- **Verification**: Simulate an upgrade failure during migration.
- **Expected Result**: Rollback is initiated automatically.

#### AC-0212-048
- **Requirement**: Rollback MUST verify the integrity of the restored version.
- **Verification**: Check integrity verification during rollback.
- **Expected Result**: Integrity is verified before restoration.

### Manifest/API/Schema Evolution (AC-0212-049 to AC-0212-056)

#### AC-0212-049
- **Requirement**: New REQUIRED fields MUST NOT be added without a major version increment.
- **Verification**: Add a required field without incrementing the major version.
- **Expected Result**: Addition is rejected.

#### AC-0212-050
- **Requirement**: New OPTIONAL fields MAY be added without version increment.
- **Verification**: Add an optional field and check version stability.
- **Expected Result**: Version is unchanged.

#### AC-0212-051
- **Requirement**: New API endpoints MAY be added without version increment.
- **Verification**: Add an API endpoint and check version stability.
- **Expected Result**: Version is unchanged.

#### AC-0212-052
- **Requirement**: Existing API endpoints MUST NOT be removed without a major version increment.
- **Verification**: Remove an API endpoint without incrementing the major version.
- **Expected Result**: Removal is rejected.

#### AC-0212-053
- **Requirement**: New data fields MAY be added without version increment.
- **Verification**: Add a data field and check version stability.
- **Expected Result**: Version is unchanged.

#### AC-0212-054
- **Requirement**: Data field type changes MUST be accompanied by a major version increment and migration plan.
- **Verification**: Change a data field type without the required increment and plan.
- **Expected Result**: Change is rejected.

#### AC-0212-055
- **Requirement**: Schema migrations MUST be idempotent.
- **Verification**: Run the same migration twice.
- **Expected Result**: Second run has no additional effect.

#### AC-0212-056
- **Requirement**: Deprecated API endpoints MUST continue functioning until sunset.
- **Verification**: Call a deprecated API endpoint before sunset.
- **Expected Result**: Endpoint functions normally.

### Performance (AC-0212-057 to AC-0212-060)

#### AC-0212-057
- **Requirement**: Version comparison MUST complete within 1 microsecond.
- **Verification**: Compare 1,000,000 version pairs.
- **Expected Result**: Average comparison time is at or below 1 microsecond.

#### AC-0212-058
- **Requirement**: Compatibility matrix lookup MUST complete within 1 millisecond.
- **Verification**: Perform 10,000 compatibility lookups.
- **Expected Result**: Average lookup time is at or below 1 millisecond.

#### AC-0212-059
- **Requirement**: Migration plan validation MUST complete within 1 second.
- **Verification**: Validate 100 migration plans.
- **Expected Result**: Average validation time is at or below 1 second.

#### AC-0212-060
- **Requirement**: Rollback operations MUST complete within 30 seconds for typical plugins.
- **Verification**: Measure rollback time for typical plugins.
- **Expected Result**: Rollback completes within 30 seconds.

### Security (AC-0212-061 to AC-0212-063)

#### AC-0212-061
- **Requirement**: Version changes that affect security posture MUST be flagged as security-relevant.
- **Verification**: Make a security-relevant version change.
- **Expected Result**: Change is flagged as security-relevant.

#### AC-0212-062
- **Requirement**: Version history MUST be tamper-evident.
- **Verification**: Modify a version history entry and check integrity.
- **Expected Result**: Tampering is detected.

#### AC-0212-063
- **Requirement**: Rollback operations MUST be logged for audit purposes.
- **Verification**: Perform a rollback and check audit logs.
- **Expected Result**: Rollback is logged.

### Consistency (AC-0212-064 to AC-0212-068)

#### AC-0212-064
- **Requirement**: Every plugin MUST have exactly one version at any point in time.
- **Verification**: Query the registry for a plugin's current version.
- **Expected Result**: Exactly one version is returned.

#### AC-0212-065
- **Requirement**: Version history MUST be complete and unbroken.
- **Verification**: Query the version history for a plugin.
- **Expected Result**: All versions from initial to current are present.

#### AC-0212-066
- **Requirement**: Compatibility matrix MUST be consistent with plugin manifests.
- **Verification**: Compare the matrix with manifest version declarations.
- **Expected Result**: Matrix and manifests are consistent.

#### AC-0212-067
- **Requirement**: Migration plans MUST be stored in the plugin registry.
- **Verification**: Query the registry for a migration plan.
- **Expected Result**: Plan is present.

#### AC-0212-068
- **Requirement**: Deprecation status MUST be consistent across all subsystem components.
- **Verification**: Query deprecation status from multiple components.
- **Expected Result**: All components report the same status.

### Edge Cases (AC-0212-069 to AC-0212-073)

#### AC-0212-069
- **Requirement**: The system MUST handle version strings with pre-release and build metadata.
- **Verification**: Parse versions with both pre-release and build metadata.
- **Expected Result**: Versions are parsed correctly.

#### AC-0212-070
- **Requirement**: The system MUST handle a plugin with 100 version history entries.
- **Verification**: Create 100 versions for a single plugin.
- **Expected Result**: All versions are managed correctly.

#### AC-0212-071
- **Requirement**: The system MUST handle simultaneous upgrades of interdependent plugins.
- **Verification**: Upgrade two interdependent plugins simultaneously.
- **Expected Result**: Upgrades are coordinated and consistent.

#### AC-0212-072
- **Requirement**: The system MUST handle a rollback triggered during an ongoing migration.
- **Verification**: Trigger a rollback during migration.
- **Expected Result**: Migration is aborted and rollback completes.

#### AC-0212-073
- **Requirement**: The system MUST handle a deprecated version reaching its sunset date.
- **Verification**: Advance time past the sunset date and check behavior.
- **Expected Result**: New installations are blocked; existing installations continue.

### Documentation (AC-0212-074 to AC-0212-075)

#### AC-0212-074
- **Requirement**: The version catalog MUST be published as a machine-readable reference.
- **Verification**: Locate the machine-readable version catalog.
- **Expected Result**: Catalog is available and matches the specification.

#### AC-0212-075
- **Requirement**: Migration plan documentation MUST include examples for each upgrade path.
- **Verification**: Check migration plan documentation for examples.
- **Expected Result**: Examples are present for each upgrade path.

---




## Acceptance Criteria

### Architecture

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | The implementation MUST satisfy all normative requirements in this specification. | Specification conformance review |
| AC-02 | The implementation MUST NOT assume any specific runtime platform. | Platform independence audit |
| AC-03 | All cross-references to related RFCs MUST resolve to valid specifications. | Cross-reference validation |

## 25 References

1. RFC 2119: Key Words for Use in RFCs to Indicate Requirement Levels
2. Semantic Versioning 2.0.0: https://semver.org
3. CalVer Alternative: Calendar-based versioning considerations

---

This specification IS NOT responsible for:
- Runtime core lifecycle (covered by RFC-0002).
- Workflow execution (covered by RFC-0301).


## 27 Future Evolution

1. Support for calendar-based versioning as an alternative to semantic versioning.
2. Automated compatibility prediction for planned changes.
3. Version-based feature flag integration.
4. Multi-version plugin coexistence for gradual migration.
5. Machine-readable changelog generation from version metadata.

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