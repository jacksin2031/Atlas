# RFC-0202: Plugin Manifest Specification

**RFC:** RFC-0202
**Title:** Plugin Manifest
**Status:** Accepted
**Version:** 1.0.0
**Category:** Plugin
**Layer:** Extension
**Normative:** YES
**Authors:** Atlas Specification Committee
**Created:** 2026-06-30
**Last Updated:** 2026-06-30
**Depends On:**
  - RFC-1005 Common Manifest Model
  - RFC-0010 Runtime Manifest Specification
  - RFC-0201 Plugin Lifecycle Specification
  - RFC-0204 Plugin Registry Specification
  - RFC-0205 Plugin Security Gate Specification
  - RFC-0212 Plugin Dependency Resolution Specification
**Related RFC:** RFC-0201, RFC-0204, RFC-0205, RFC-0212
**Target Release:** 1.0.0

---

## Normative Status
This specification is normative. Every plugin manifest MUST conform to the requirements defined herein. Any deviation MUST be approved through the formal Architecture Decision Record (ADR) process.

This specification is subordinate to the Atlas Development System (ADS) Constitution and all active ADRs.

---

## Authority

This RFC is the authoritative specification for the Plugin Manifest.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.

---

## Terminology

The following terms are defined with exact meanings consistent with the Atlas Master Glossary.

| Term | Definition | Source |
|---|---|---|
| Manifest | The declarative definition of a component, including its metadata, dependencies, capabilities, and configuration. | Glossary |
| Plugin | A package containing extensions, nodes, and custom services loaded into isolated execution sandboxes. | Glossary |
| Capability | A feature declaration verified and exposed by the Runtime Manifest. | Glossary |
| Dependency | A required component or service that must be available for this component to function. | This RFC |
| Permission | A declared authorization scope granting access to system resources. | This RFC |
| Version | The semantic version of a component or specification. | This RFC |
| Signature | A cryptographic proof of package integrity and origin. | This RFC |

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

1. **Binary Distribution**: The manifest describes plugin metadata but does not define the binary packaging format, compression scheme, or transport mechanism for plugin artifacts.

2. **Runtime Execution Model**: The manifest does not specify how plugin code executes, schedules work, or manages threads; those concerns belong to the plugin lifecycle and runtime specifications.

3. **Policy Engine Implementation**: The manifest defines the input to the security gate but does not prescribe the internal algorithm, data structure, or enforcement mechanism of the policy engine.

4. **Marketplace Transaction Logic**: While the manifest carries marketplace metadata for discovery purposes, it does not define pricing, payment processing, or licensing enforcement mechanics.

5. **Plugin Update Protocol**: The manifest declares version information and compatibility constraints but does not define the update transfer protocol, delta computation, or staged rollout mechanics.

6. **End-User Configuration Interface**: The manifest may carry a configuration schema, but the user-facing configuration UI, form generation, and input validation are outside this specification.

---

## 4. Manifest Philosophy

1. **Manifest is Declarative**: The manifest is a statement of what a plugin declares, not how it implements. It describes identity, capabilities, permissions, dependencies, and constraints without embedding executable logic.

2. **Manifest is Immutable at Runtime**: Once a plugin is loaded and active, its manifest fields MUST NOT be modified in memory. Any change requires an unload-reload cycle with full re-validation.

3. **Manifest is Authoritative**: The manifest is the single source of truth for plugin metadata. The runtime MUST NOT infer, fabricate, or override manifest fields except where explicitly permitted by the trust-level progression rules.

4. **Manifest is Verifiable**: Every manifest MUST be structurally valid, semantically consistent, and cryptographically verifiable against the plugin binary before the runtime accepts it.

5. **Manifest is Evolvable**: The manifest schema supports additive evolution through versioned schema releases. Existing plugins MUST remain valid under newer schema versions unless a breaking change is explicitly declared.

6. **Manifest is Scoped**: Each manifest applies to exactly one plugin instance. Multi-plugin bundles MUST be decomposed into individual manifests with cross-referenced dependency declarations.

---

## 5. Ownership

**The Plugin Catalog team owns:**
- The canonical field definitions in the manifest-fields catalog.
- The validation rules applied during manifest parsing.
- The schema version registry and evolution process.

**The Plugin Registry owns:**
- Persistence of manifest data.
- Query and indexing of manifest fields.
- Lifecycle state transitions triggered by manifest changes.

**The Security Gate owns:**
- Trust level assignment and progression.
- Signature verification against the manifest-integrity hash.
- Permission evaluation based on manifest-declared permissions.

**Plugin Publishers own:**
- Correct declaration of manifest fields for their plugin.
- Accuracy of the integrity hash relative to the shipped binary.
- Consistency between declared capabilities and actual functionality.

**The Runtime owns:**
- Manifest loading and parsing.
- Schema validation enforcement.
- Manifest field immutability during active plugin lifecycles.

---

## 6. Boundaries

**The Manifest Specification communicates with:**
- The Plugin Registry (for persistence and query of manifest data).
- The Security Gate (for trust level evaluation and permission enforcement).
- The Dependency Resolver (for dependency type resolution and load-order computation).
- The Plugin Lifecycle Manager (for state transition coordination via manifest-declared hooks).
- The Common Manifest Model (for shared base fields across all Atlas package types).

**The Manifest Specification MUST NOT communicate with:**
- Plugin binary loading or execution mechanisms.
- End-user configuration interfaces.
- Marketplace payment or transaction systems.
- External network protocols or transport layers.

---

## 7. Runtime Invariants

The following invariants MUST hold for every plugin manifest instance at every point during the plugin lifecycle.

**INV-PLG-01**: A plugin manifest MUST be structurally valid against the registered schema version before any runtime subsystem accesses its fields. An invalid manifest MUST cause the plugin to transition to PSTATE-FAILED with error PERR-MANIFEST-INVALID.

**INV-PLG-02**: The plugin_id field MUST be globally unique across all registered plugins. Duplicate plugin_id declarations MUST cause the manifest to be rejected with error PERR-REGISTRY-DUPLICATE.

**INV-PLG-03**: The integrity_hash field MUST be a cryptographic hash of the complete plugin binary, computed using SHA-256 or a stronger algorithm. The hash MUST be recomputed and verified at every load, update, and activation.

**INV-PLG-04**: The 	rust_level field MUST be assigned exclusively by the Security Gate or governance process. A manifest declaring a 	rust_level value set by the publisher MUST be treated as unverified and overridden to TRUST-LEVEL-UNVERIFIED.

**INV-PLG-05**: All permission declarations in the permissions array MUST correspond to entries in the Permissions Catalog. Any undeclared permission identifier MUST cause manifest rejection with error PERR-MANIFEST-INVALID.

**INV-PLG-06**: All capability declarations in the capabilities array MUST correspond to entries in the Capabilities Catalog. Any undeclared capability identifier MUST cause manifest rejection with error PERR-MANIFEST-INVALID.

**INV-PLG-07**: The dependencies object MUST NOT contain a self-referencing key matching the manifest's own plugin_id. Self-dependencies MUST cause manifest rejection with error PERR-MANIFEST-INVALID.

**INV-PLG-08**: If the declared 	rust_level is TRUST-LEVEL-SIG-VALIDATED or above, the signature field MUST be present and verifiable against a trusted certificate authority. Missing or unverifiable signatures MUST cause the trust level to be downgraded to TRUST-LEVEL-UNVERIFIED or the manifest to be rejected depending on the runtime policy.

**INV-PLG-09**: The ersion field MUST follow semantic versioning. Incrementing the major version indicates a breaking manifest schema change. Incrementing the minor version indicates backward-compatible additions. Incrementing the patch version indicates backward-compatible corrections.

**INV-PLG-10**: The esource_limits object, when present, MUST not exceed the runtime-defined maximum quotas for CPU, memory, and I/O. Requests exceeding runtime maximums MUST be clamped to the maximum or cause manifest rejection per runtime policy.

---

## 8. Architecture

The following diagram illustrates the manifest data flow through the Atlas Plugin subsystem.

`mermaid
graph TD
    Publisher[Plugin Publisher] -->|Creates| Manifest[Plugin Manifest Document]
    Manifest -->|Computes Hash| Integrity[Integrity Hash of Binary]
    Manifest -->|Signs| Signature[Cryptographic Signature]
    Manifest -->|Writes to Disk| ManifestFile[manifest.json]

    Registry[Plugin Registry] -->|Discovers| ManifestFile
    Registry -->|Validates| SchemaValidator[Schema Validator]
    SchemaValidator -->|Checks| FieldRules[Field Validation Rules]
    FieldRules -->|Passes| SecurityGate[Security Gate]

    SecurityGate -->|Assigns| TrustLevel[Trust Level]
    SecurityGate -->|Verifies| SigVerifier[Signature Verifier]
    SigVerifier -->|Compares| Integrity

    SecurityGate -->|Evaluates| PermEvaluator[Permission Evaluator]
    PermEvaluator -->|Against| PermissionsCatalog[Permissions Catalog]

    SecurityGate -->|Passes| DepResolver[Dependency Resolver]
    DepResolver -->|Resolves| Dependencies[Dependency Graph]
    DepResolver -->|Detects| CircularDeps[Circular Dependency Check]

    DepResolver -->|Computes| LoadOrder[Load Order]
    LoadOrder -->|Feeds| LifecycleMgr[Plugin Lifecycle Manager]
    LifecycleMgr -->|Transitions| PluginStates[Plugin State Machine]

    ManifestFile -->|Indexed| Indexer[Registry Indexer]
    Indexer -->|Stored in| RegistryDB[Registry Database]
    RegistryDB -->|Queried by| Discovery[Plugin Discovery]
`

The manifest lifecycle proceeds through these phases:

1. **Declaration Phase**: The plugin publisher creates the manifest document with all required and optional fields.
2. **Integrity Phase**: The publisher computes the integrity hash over the plugin binary and optionally applies a cryptographic signature.
3. **Registration Phase**: The registry discovers the manifest, validates its schema, and indexes its fields for query.
4. **Security Phase**: The security gate evaluates trust level, verifies signatures, checks permissions against the catalog, and enforces sandbox constraints.
5. **Resolution Phase**: The dependency resolver computes the load order, detects circular dependencies, and validates compatibility.
6. **Activation Phase**: The lifecycle manager transitions the plugin through its state machine based on the manifest-declared entry points and hooks.

---

## 9. Manifest Schema Definition

This section defines every field in the plugin manifest schema. Fields are categorized as REQUIRED or OPTIONAL. Each field specifies its data type, constraints, and validation rules.

### 9.1 Core Identity Fields

**manifest_version** (REQUIRED, String)
- The version of the manifest schema this plugin adheres to.
- MUST be a valid semantic version string matching the pattern ^\d+\.\d+\.\d+$.
- MUST match a schema version registered in the runtime's schema registry.
- Changes to this field indicate a schema evolution event.

**plugin_id** (REQUIRED, String)
- The globally unique identifier for this plugin instance.
- MUST conform to the naming convention defined in the Plugin ID Specification.
- MUST be unique across all plugins in the system registry.
- MUST NOT change across plugin version upgrades.

**plugin_name** (REQUIRED, String)
- The human-readable display name of the plugin.
- MUST be non-empty.
- MUST NOT exceed 256 Unicode characters.
- MUST contain only printable Unicode characters.

**ersion** (REQUIRED, String)
- The semantic version of this plugin instance.
- MUST conform to semantic versioning 2.0.0 rules.
- MUST increment on every published update.
- Pre-release and build metadata MAY be included.

**uthor** (REQUIRED, String)
- The name or identity of the plugin publisher.
- MUST be non-empty.
- MUST NOT exceed 256 characters.

**license** (REQUIRED, String)
- The SPDX identifier or full license text governing this plugin.
- MUST be a valid SPDX identifier from the SPDX license list, or a non-empty license text.
- MUST be consistent with any marketplace_info licensing fields.

### 9.2 Descriptive Fields

**description** (OPTIONAL, String)
- A human-readable description of the plugin's purpose and functionality.
- MUST NOT exceed 4096 characters if present.
- SHOULD be sufficient for marketplace discovery and operator decision-making.

### 9.3 Capability and Permission Fields

**capabilities** (OPTIONAL, Array of Strings)
- A list of capability identifiers this plugin provides.
- Each entry MUST reference a registered capability from the Capabilities Catalog.
- MUST be sorted in ascending lexicographic order of stable IDs.
- MUST be non-empty if any capability is claimed by the plugin.
- MUST NOT contain duplicate entries.

**permissions** (OPTIONAL, Array of Strings)
- A list of permission identifiers this plugin requests.
- Each entry MUST correspond to a permission defined in the Permissions Catalog.
- MUST be sorted in ascending lexicographic order of stable IDs.
- MUST NOT request permissions exceeding the plugin's declared trust level.
- MUST NOT contain duplicate entries.

### 9.4 Dependency Fields

**dependencies** (OPTIONAL, Object)
- A map of dependency declarations keyed by target plugin_id.
- Each dependency entry MUST specify a valid DEP-TYPE-* identifier and a version constraint.
- Version constraints MUST use semantic versioning comparison operators.
- MUST NOT declare self-dependencies.
- MUST NOT contain circular dependency chains.

### 9.5 Entry Point and Lifecycle Fields

**entry_points** (OPTIONAL, Array of Objects)
- A list of executable entry point definitions.
- Each entry MUST specify a valid entry point type and a non-empty handler reference.
- Entry point types MUST conform to the Extension Points Catalog.

**lifecycle_hooks** (OPTIONAL, Object)
- Definitions of custom logic executed at lifecycle transition points.
- Each hook MUST reference a valid entry point declared in entry_points.
- MUST NOT define hooks that conflict with runtime-enforced transitions.
- Hooks MUST be idempotent and MUST NOT produce side effects outside the plugin's sandbox.

### 9.6 Security and Trust Fields

**sandbox_config** (OPTIONAL, Object)
- Configuration parameters for the plugin sandbox environment.
- MUST be compatible with the plugin's declared trust level.
- MUST NOT request sandbox exemptions not permitted by the trust level.
- Fields include resource quotas, network restrictions, and filesystem access scopes.

**security_level** (OPTIONAL, String)
- The declared security classification of this plugin.
- MUST be a value from the security level enumeration defined in the security specification.
- SHOULD align with the trust_level for consistency.

**	rust_level** (OPTIONAL, String)
- The trust level assigned to this plugin.
- MUST be a value from the Trust Levels Catalog.
- MUST be set by the runtime or governance process, not by the plugin publisher.
- A publisher-supplied trust_level value MUST be ignored and overridden.

**signature** (OPTIONAL, String)
- The cryptographic signature of the plugin binary and manifest payload.
- MUST be a valid signature verifiable against a trusted certificate authority.
- MUST be present if the plugin claims TRUST-LEVEL-SIG-VALIDATED or above.
- MUST use RSA-2048, ECDSA P-256, or stronger algorithms.

**integrity_hash** (REQUIRED, String)
- A cryptographic hash of the plugin binary for integrity verification.
- MUST be a SHA-256 or stronger hash, expressed as a lowercase hexadecimal string.
- MUST be verifiable against the delivered binary at load time.
- MUST be computed after all other manifest modifications are complete.

### 9.7 Compatibility and Configuration Fields

**compatibility_matrix** (OPTIONAL, Object)
- A declaration of runtime and plugin version compatibility constraints.
- Each entry MUST specify a version range and a compatibility status.
- Version ranges MUST use semantic versioning range notation.

**pi_version** (OPTIONAL, String)
- The version of the plugin API this plugin targets.
- MUST be a valid semantic version.
- MUST be compatible with the runtime API version.

**config_schema** (OPTIONAL, Object)
- A JSON Schema definition of the plugin configuration options.
- MUST be a valid JSON Schema draft (2020-12 or later).
- MUST define all configuration keys referenced in the plugin code.
- MUST NOT define configuration keys with sensitive data types without explicit encryption annotations.

### 9.8 Event and Observability Fields

**events_published** (OPTIONAL, Array of Strings)
- A list of event types this plugin emits.
- Each entry MUST be a valid event type identifier from the Plugin Events Catalog.
- MUST NOT publish events not declared here.
- MUST NOT contain duplicate entries.

**events_subscribed** (OPTIONAL, Array of Strings)
- A list of event types this plugin consumes.
- Each entry MUST be a valid event type identifier from the Plugin Events Catalog.
- MUST NOT consume events not declared here.
- MUST NOT contain duplicate entries.

### 9.9 Resource and Metadata Fields

**esource_limits** (OPTIONAL, Object)
- Declarations of maximum resource consumption.
- Each limit MUST be a positive integer with an associated unit.
- Supported units: CPU (cores, percentage), memory (bytes with SI prefixes), I/O (operations per second, bytes per second).
- MUST NOT exceed the runtime-defined maximums.

**egistry_metadata** (OPTIONAL, Object)
- Additional metadata for registry indexing and discovery.
- MUST conform to the registry metadata schema.
- MUST NOT contain sensitive or personally identifiable information.

**marketplace_info** (OPTIONAL, Object)
- Information used by marketplace services for listing and discovery.
- MUST conform to the marketplace information schema.
- Price and licensing fields MUST be consistent with the license field.
- MUST NOT contain misleading or deceptive content.

### 9.10 Field Ordering Rules

1. REQUIRED fields MUST appear before OPTIONAL fields in the manifest document.
2. Fields within each group MUST appear in alphabetical order by field name.
3. Array fields MUST preserve element order; order MUST be semantically significant where documented.
4. Object fields MUST be serialized with keys in alphabetical order in canonical form.

---

## 10. Manifest Validation Process

The manifest validation process proceeds through a multi-stage pipeline. Each stage MUST complete successfully before the next stage begins. A failure at any stage causes the manifest to be rejected and the plugin to transition to PSTATE-FAILED.

`mermaid
flowchart TD
    Start([Manifest Received]) --> Stage1[Stage 1: Structural Validation]
    Stage1 --> ValidJSON{Valid JSON?}
    ValidJSON -->|No| Reject1[Reject: PERR-MANIFEST-INVALID]
    ValidJSON -->|Yes| CheckFields{All REQUIRED fields present?}
    CheckFields -->|No| Reject1
    CheckFields -->|Yes| Stage2[Stage 2: Type Validation]

    Stage2 --> TypeOK{All types correct?}
    TypeOK -->|No| Reject1
    TypeOK -->|Yes| Stage3[Stage 3: Enum Validation]

    Stage3 --> EnumOK{All enums valid?}
    EnumOK -->|No| Reject1
    EnumOK -->|Yes| Stage4[Stage 4: Constraint Validation]

    Stage4 --> ConstraintOK{Length, pattern, range OK?}
    ConstraintOK -->|No| Reject1
    ConstraintOK -->|Yes| Stage5[Stage 5: Cross-Field Validation]

    Stage5 --> CrossFieldOK{Consistency checks pass?}
    CrossFieldOK -->|No| Reject1
    CrossFieldOK -->|Yes| Stage6[Stage 6: Catalog Reference Validation]

    Stage6 --> CatalogOK{All refs in catalogs?}
    CatalogOK -->|No| Reject1
    CatalogOK -->|Yes| Stage7[Stage 7: Integrity Hash Verification]

    Stage7 --> HashOK{Hash matches binary?}
    HashOK -->|No| Reject2[Reject: PERR-INTEGRITY-FAIL]
    HashOK -->|Yes| Stage8[Stage 8: Signature Verification]

    Stage8 --> SigPresent{Signature required?}
    SigPresent -->|No| Stage9[Stage 9: Trust Level Assignment]
    SigPresent -->|Yes| SigVerify{Signature valid?}
    SigVerify -->|No| Reject3[Reject: PERR-SIGNATURE-INVALID]
    SigVerify -->|Yes| Stage9

    Stage9 --> Stage10[Stage 10: Dependency Resolution]
    Stage10 --> DepOK{Dependencies resolvable?}
    DepOK -->|No| Reject4[Reject: PERR-DEPENDENCY-UNRESOLVED]
    DepOK -->|Yes| Stage11[Stage 11: Circular Dependency Check]

    Stage11 --> CircularOK{No cycles?}
    CircularOK -->|No| Reject5[Reject: PERR-CIRCULAR-DEPENDENCY]
    CircularOK -->|Yes| Accept([Validation Passed])

    Reject1 -.-> EndFail([Plugin: PSTATE-FAILED])
    Reject2 -.-> EndFail
    Reject3 -.-> EndFail
    Reject4 -.-> EndFail
    Reject5 -.-> EndFail
    Accept -.-> EndOK([Plugin: PSTATE-LOADED])
`

Each validation stage has specific responsibilities:

**Stage 1 - Structural Validation**: Verifies the manifest is well-formed JSON, all REQUIRED fields are present, and basic structural invariants hold.

**Stage 2 - Type Validation**: Verifies each field's value matches its declared data type (string, array, object, etc.).

**Stage 3 - Enum Validation**: Verifies enumerated fields contain values from the approved catalog (plugin_type, trust_level, capability identifiers, permission identifiers).

**Stage 4 - Constraint Validation**: Verifies string lengths, regex patterns, numeric ranges, and format constraints for all fields.

**Stage 5 - Cross-Field Validation**: Verifies consistency between related fields (e.g., trust_level is consistent with signature presence, permissions do not exceed trust level).

**Stage 6 - Catalog Reference Validation**: Verifies all referenced identifiers (capabilities, permissions, events, extension points) exist in their respective catalogs.

**Stage 7 - Integrity Hash Verification**: Recomputes the hash of the plugin binary and compares it against the manifest's integrity_hash field.

**Stage 8 - Signature Verification**: If required by the trust level, verifies the cryptographic signature against a trusted certificate authority.

**Stage 9 - Trust Level Assignment**: The Security Gate assigns or confirms the trust level based on signature verification and policy evaluation.

**Stage 10 - Dependency Resolution**: Resolves all dependency declarations, computes version compatibility, and determines load order.

**Stage 11 - Circular Dependency Check**: Detects and rejects circular dependency chains among plugins.

---

## 11. Manifest Evolution

The manifest schema evolves through a formal versioning process that ensures backward compatibility and predictable migration paths.

`mermaid
stateDiagram-v2
    [*] --> SCHEMA_DRAFT: New schema proposal
    SCHEMA_DRAFT --> SCHEMA_REVIEW: Review committee evaluates
    SCHEMA_REVIEW --> SCHEMA_DRAFT: Requires revision
    SCHEMA_REVIEW --> SCHEMA_PUBLISHED: Approved
    SCHEMA_PUBLISHED --> SCHEMA_DEPRECATED: superseded by newer version
    SCHEMA_DEPRECATED --> [*]: Retired after grace period

    SCHEMA_PUBLISHED --> SCHEMA_ACTIVE: Runtime adopts
    SCHEMA_ACTIVE --> SCHEMA_DEPRECATED: New version published
`

Schema evolution rules:

1. **Additive Changes**: New OPTIONAL fields MAY be added to any schema version without incrementing the major version. Existing plugins MUST remain valid under the new schema.

2. **Removal Changes**: REQUIRED fields MUST NOT be removed. OPTIONAL fields MAY be deprecated but MUST remain accepted by the validator for a minimum grace period of five schema versions after deprecation.

3. **Type Changes**: The data type of any field MUST NOT change between schema versions. Introducing a new field with the same semantic meaning but different type requires a new field name.

4. **Enum Expansion**: New values MAY be added to enumerated fields. Existing values MUST NOT be removed or reordered.

5. **Constraint Relaxation**: Validation constraints (length limits, pattern rules) MAY be relaxed in newer schema versions. Constraints MUST NOT be tightened without a major version bump.

6. **Constraint Tightening**: Tightening any validation constraint requires a major schema version increment and MUST be accompanied by a migration guide.

7. **Schema Version Registry**: The runtime maintains a registry of all active schema versions. Multiple schema versions MUST be supported simultaneously during transition periods.

8. **Migration Policy**: When a schema version reaches end-of-life, the runtime MUST provide a minimum twelve-month migration window. Plugins on deprecated schema versions MUST be flagged with warnings but MUST NOT be automatically rejected.

---

## 12. Manifest Versioning

This section distinguishes between the manifest schema version and the plugin version, as they serve different purposes.

**Manifest Schema Version** (manifest_version):
- Indicates which version of the manifest schema the document conforms to.
- Incremented when the schema structure changes in a way that affects parsing or validation.
- The runtime MUST support at least the two most recent schema versions simultaneously.
- Format: Semantic versioning (MAJOR.MINOR.PATCH).

**Plugin Version** (ersion):
- Indicates the version of the plugin binary and its associated manifest.
- Incremented by the plugin publisher on every release.
- Major version increments indicate breaking changes in plugin behavior or manifest schema incompatibility.
- Minor version increments indicate backward-compatible feature additions.
- Patch version increments indicate backward-compatible bug fixes.

**Version Compatibility Rules**:
1. A plugin with schema version 2.0.0 MUST NOT be loaded by a runtime that only supports schema version 1.x.
2. A plugin with version 2.0.0 MAY be loaded by a runtime targeting API version 1.x if the compatibility_matrix declares forward compatibility.
3. The runtime MUST reject a plugin whose manifest_schema_version exceeds the maximum supported schema version.
4. The runtime MUST warn (but not reject) a plugin whose manifest_schema_version is older than the minimum supported schema version, subject to a deprecation grace period.

---

## 13. Signature and Integrity

The manifest incorporates two complementary mechanisms for ensuring plugin authenticity and integrity: the integrity hash and the cryptographic signature.

### 13.1 Integrity Hash

The integrity hash provides binary-level integrity verification:

1. The publisher computes a SHA-256 hash over the complete plugin binary artifact.
2. The resulting 64-character lowercase hexadecimal string is placed in the integrity_hash field.
3. The runtime recomputes the hash at every load, update, and activation event.
4. A hash mismatch causes the manifest to be rejected with error PERR-INTEGRITY-FAIL.
5. The hash MUST be computed after all manifest modifications are finalized to ensure consistency.

### 13.2 Cryptographic Signature

The signature provides publisher authenticity and non-repudiation:

1. The publisher signs a canonical form of the manifest (alphabetically ordered fields, canonical JSON encoding) using a private key.
2. The signature algorithm MUST be RSA-2048 or higher, ECDSA P-256 or higher, or an equivalent-strength algorithm.
3. The signature value is placed in the signature field as a base64-encoded string.
4. The runtime verifies the signature against the certificate chain rooted in a trusted certificate authority.
5. Certificate revocation status MUST be checked using CRL or OCSP.
6. Signature verification is REQUIRED for trust levels at or above TRUST-LEVEL-SIG-VALIDATED.
7. A failed signature check causes the manifest to be rejected with error PERR-SIGNATURE-INVALID.

### 13.3 Signature Payload

The signature covers the following payload:
- All REQUIRED fields in the manifest.
- All OPTIONAL fields that are present and non-null.
- The canonical form is defined as: alphabetically sorted field names, canonical JSON encoding with no whitespace, UTF-8 byte order mark excluded.

### 13.4 Key Rotation

1. Publishers MUST support key rotation with a minimum ninety-day overlap period between old and new keys.
2. The runtime MUST accept signatures from any key within the active rotation window.
3. Expired keys MUST NOT be accepted for new installations but MAY be accepted for existing plugin updates during the grace period.

---

## 14. Manifest Registry

The manifest registry is the centralized store for all plugin manifest data. It provides persistence, indexing, querying, and lifecycle management capabilities.

`mermaid
graph TD
    RegistryDB[(Registry Database)]

    RegistryDB -->|Stores| RawManifest[Raw Manifest Document]
    RegistryDB -->|Indexes| Fields[Indexed Manifest Fields]
    RegistryDB -->|Tracks| Lifecycle[Plugin Lifecycle State]
    RegistryDB -->|Maintains| Audit[Audit Trail]

    Fields -->|By plugin_id| Q1[Unique Lookup]
    Fields -->|By plugin_type| Q2[Type Filter]
    Fields -->|By trust_level| Q3[Trust Filter]
    Fields -->|By capability| Q4[Capability Search]
    Fields -->|By version| Q5[Version Query]
    Fields -->|By author| Q6[Author Search]

    Q1 --> Response1[Query Response]
    Q2 --> Response1
    Q3 --> Response1
    Q4 --> Response1
    Q5 --> Response1
    Q6 --> Response1

    Audit -->|Records| Events[All manifest mutations]
    Events -->|Include| Timestamps[Timestamp, actor, operation]
`

**Registry Responsibilities**:
1. **Persistence**: Store the raw manifest document and all indexed fields durably.
2. **Indexing**: Maintain indexes on commonly queried fields: plugin_id, plugin_type, trust_level, capabilities, permissions, version, and author.
3. **Query API**: Support filtered, sorted, and paginated queries over the manifest dataset.
4. **Version History**: Retain historical manifest versions for every plugin_id, enabling rollback and audit.
5. **Conflict Resolution**: Detect and resolve concurrent manifest update conflicts using optimistic locking based on version numbers.
6. **Audit Logging**: Record every manifest mutation (create, update, delete, trust level change) with timestamp, actor, and operation type.

**Query Capabilities**:
- Retrieve a manifest by plugin_id (primary lookup).
- List all manifests matching a plugin_type filter.
- List all manifests at or above a trust_level threshold.
- List all manifests declaring a specific capability.
- List all manifests within a version range.
- List all manifests by author.
- Full-text search across plugin_name and description fields.

**Data Retention**:
- Active manifests MUST be retained indefinitely.
- Removed manifests MUST be retained in an archived state for a minimum of thirty-six months.
- Historical manifest versions MUST be retained for a minimum of twenty-four months.

---

## 15. Compatibility Declaration

Plugins declare their compatibility with the runtime and other plugins through the compatibility_matrix field and the pi_version field.

### 15.1 Runtime Compatibility

The compatibility_matrix MUST declare the runtime version ranges with which the plugin is compatible:

1. **Minimum Runtime Version**: The oldest runtime version the plugin supports.
2. **Maximum Runtime Version**: The newest runtime version the plugin supports.
3. **Compatibility Status**: One of FULL, PARTIAL, or NONE for each declared range.

### 15.2 Plugin Dependency Compatibility

For each dependency in the dependencies object, the version constraint defines the acceptable version range:

1. **Exact Match**: The dependency MUST be at exactly the specified version.
2. **Range Constraint**: The dependency version MUST fall within the specified semantic version range.
3. **Minimum Version**: The dependency version MUST be at or above the specified version.
4. **Maximum Version**: The dependency version MUST be at or below the specified version.

### 15.3 Compatibility Verification

1. The dependency resolver MUST verify that all declared compatibility constraints are satisfiable by the currently installed plugin set.
2. Unsatisfiable constraints MUST cause the manifest to be rejected with error PERR-VERSION-INCOMPATIBLE.
3. The runtime MUST support forward compatibility for at least one minor version beyond the plugin's declared maximum.
4. The runtime MUST support backward compatibility for at least two minor versions below the plugin's declared minimum.

---

## 16. Security Considerations

### 16.1 Manifest Tampering Prevention

1. The integrity_hash field MUST be computed over the plugin binary, not the manifest itself, to prevent manifest-only tampering attacks.
2. The signature field covers the canonical manifest form, preventing field substitution attacks.
3. The runtime MUST verify both integrity_hash and signature before accepting a manifest.
4. Manifest fields MUST NOT be modifiable by any runtime component after initial validation.

### 16.2 Privilege Escalation Prevention

1. A plugin MUST NOT be able to increase its trust_level through manifest manipulation.
2. Permission requests in the manifest MUST NOT exceed the permissions granted by the assigned trust_level.
3. Sandbox configuration MUST be validated against the trust_level constraints before acceptance.
4. The runtime MUST enforce the principle of least privilege: a plugin receives only the minimum permissions necessary for its declared capabilities.

### 16.3 Information Disclosure Prevention

1. The registry_metadata field MUST NOT contain sensitive or personally identifiable information.
2. Marketplace_info fields MUST be sanitized before exposure to unprivileged consumers.
3. Error messages originating from manifest validation MUST NOT leak internal system paths, certificate details, or implementation specifics.
4. The audit trail MUST be accessible only to operators with appropriate authorization levels.

### 16.4 Denial of Service Prevention

1. Manifest parsing MUST enforce size limits: the manifest document MUST NOT exceed 64 kilobytes in canonical form.
2. Schema validation MUST complete within the performance budget defined in Section 17.
3. Dependency resolution MUST detect and reject excessively deep or wide dependency graphs.
4. The registry MUST rate-limit manifest query operations to prevent resource exhaustion.

### 16.5 Supply Chain Security

1. Plugin publishers MUST maintain a secure key management process for signing keys.
2. The runtime MUST verify the certificate chain for every signed manifest.
3. Compromised signing keys MUST be reported and revoked through the certificate revocation process.
4. The registry MUST track the signing key fingerprint for each plugin publisher.

---

## 17. Performance Budgets

The following performance budgets define the maximum allowable time for manifest-related operations. These budgets ensure that manifest processing does not become a bottleneck in the plugin lifecycle.

| Metric | Target Budget | Measurement Context |
|---|---|---|
| Manifest Structural Parse | 20 ms | Full manifest document parse from canonical JSON |
| Type Validation | 30 ms | Validation of all field types against schema |
| Enum Validation | 10 ms | Verification of all enumerated field values |
| Constraint Validation | 20 ms | Length, pattern, and range checks on all fields |
| Cross-Field Validation | 15 ms | Consistency checks between related fields |
| Catalog Reference Validation | 25 ms | Verification that all references exist in catalogs |
| Integrity Hash Recomputation | 50 ms | SHA-256 hash of plugin binary |
| Signature Verification | 100 ms | Cryptographic signature verification against CA |
| Trust Level Assignment | 10 ms | Security gate trust level evaluation |
| Dependency Resolution | 50 ms | Full dependency graph resolution and load-order computation |
| Circular Dependency Detection | 20 ms | Cycle detection in dependency graph |
| Total Validation Pipeline | 300 ms | End-to-end manifest validation from receipt to acceptance |
| Registry Index Update | 10 ms | Updating registry indexes after manifest acceptance |
| Registry Query (indexed) | 5 ms | Single-index lookup by plugin_id |
| Registry Query (filtered) | 50 ms | Multi-field filtered query with pagination |
| Manifest Serialization | 10 ms | Canonical form serialization for signature or storage |

---

## 18. Glossary

| Term | Definition |
|---|---|
| **Manifest** | The declarative metadata document that binds a plugin to the Atlas runtime through declared identity, capabilities, permissions, dependencies, and integrity guarantees. |
| **Plugin** | A modular software component that extends the Atlas runtime with additional capabilities, following the plugin lifecycle and manifest contract. |
| **Plugin ID** | A globally unique, stable identifier for a plugin instance that persists across version upgrades. |
| **Capability** | A discrete functional competency that a plugin declares and the runtime recognizes and enforces. |
| **Permission** | A granular access right that a plugin requests, which the security gate evaluates and grants or denies based on trust level and policy. |
| **Trust Level** | A classification assigned by the runtime or governance process that determines the sandbox scope, permission grants, and verification depth for a plugin. |
| **Integrity Hash** | A cryptographic hash of the plugin binary stored in the manifest, used to detect tampering and verify binary consistency. |
| **Signature** | A cryptographic signature of the canonical manifest form, used to verify publisher authenticity and non-repudiation. |
| **Dependency Type** | A classification of the relationship between plugins, defining enforcement strength, failure behavior, and resolution timing. |
| **Schema Version** | The version of the manifest schema definition that a particular manifest document conforms to. |
| **Security Gate** | The runtime subsystem responsible for trust level assignment, signature verification, permission evaluation, and sandbox enforcement. |
| **Dependency Resolver** | The runtime subsystem responsible for resolving inter-plugin dependencies, computing load order, and detecting circular dependencies. |
| **Plugin Registry** | The centralized store for all plugin manifest data, providing persistence, indexing, querying, and lifecycle management. |
| **Canonical Form** | The deterministic serialization of a manifest document with alphabetically sorted fields, canonical JSON encoding, and no extraneous whitespace. |
| **PSTATE** | A plugin lifecycle state identifier prefixed with PSTATE-, representing a discrete phase in the plugin state machine. |
| **PERR** | A plugin subsystem error code identifier prefixed with PERR-, representing a specific failure condition. |
| **CAP-PLUGIN** | A capability identifier prefixed with CAP-PLUGIN-, representing a discrete functional competency in the plugin subsystem. |
| **PERM-** | A permission identifier prefixed with PERM-, representing a granular access right in the plugin subsystem. |
| **DEP-TYPE-** | A dependency type identifier prefixed with DEP-TYPE-, representing a relationship classification between plugins. |
| **TRUST-LEVEL-** | A trust level identifier prefixed with TRUST-LEVEL-, representing a security classification for a plugin. |
| **PT-** | A plugin type identifier prefixed with PT-, representing the primary role a plugin fulfills. |

---

## 19. Acceptance Criteria

### 19.1 Schema Definition (AC-0202-001 through AC-0202-015)

**AC-0202-001**
- **Requirement**: The manifest MUST contain a manifest_version field that is a REQUIRED string field.
- **Verification**: Parse a manifest document and check for the presence and type of manifest_version.
- **Expected Result**: The field is present, is a string, and matches the pattern ^\d+\.\d+\.\d+$.

**AC-0202-002**
- **Requirement**: The manifest MUST contain a plugin_id field that is a REQUIRED string field with global uniqueness.
- **Verification**: Register two plugins with identical plugin_id values.
- **Expected Result**: The second registration is rejected with error PERR-REGISTRY-DUPLICATE.

**AC-0202-003**
- **Requirement**: The plugin_name field MUST NOT exceed 256 characters.
- **Verification**: Submit a manifest with a plugin_name of 257 characters.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID.

**AC-0202-004**
- **Requirement**: The ersion field MUST conform to semantic versioning 2.0.0.
- **Verification**: Submit manifests with versions "1.0", "1.0.0-beta", "1.0.0+build.123", and "1.0.0".
- **Expected Result**: "1.0" is rejected. "1.0.0-beta", "1.0.0+build.123", and "1.0.0" are accepted.

**AC-0202-005**
- **Requirement**: The license field MUST be a valid SPDX identifier or non-empty license text.
- **Verification**: Submit manifests with license values "MIT", "Apache-2.0", "", and "Custom License v1".
- **Expected Result**: "MIT" and "Apache-2.0" are accepted. "" is rejected. "Custom License v1" is accepted.

**AC-0202-006**
- **Requirement**: The capabilities array, when present, MUST contain only identifiers from the Capabilities Catalog.
- **Verification**: Submit a manifest declaring capabilities "CAP-PLUGIN-LOAD" and "CAP-PLUGIN-NONEXISTENT".
- **Expected Result**: The manifest is rejected because "CAP-PLUGIN-NONEXISTENT" is not in the catalog.

**AC-0202-007**
- **Requirement**: The permissions array, when present, MUST contain only identifiers from the Permissions Catalog.
- **Verification**: Submit a manifest declaring permissions "PERM-FILESYSTEM-READ" and "PERM-FAKE-OPERATION".
- **Expected Result**: The manifest is rejected because "PERM-FAKE-OPERATION" is not in the catalog.

**AC-0202-008**
- **Requirement**: The dependencies object MUST NOT contain a self-referencing key.
- **Verification**: Submit a manifest where a dependency key equals the manifest's own plugin_id.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID.

**AC-0202-009**
- **Requirement**: The integrity_hash field MUST be a SHA-256 or stronger hash in lowercase hexadecimal format.
- **Verification**: Submit manifests with valid SHA-256 hashes, SHA-1 hashes, and non-hexadecimal strings.
- **Expected Result**: SHA-256 is accepted. SHA-1 and non-hexadecimal strings are rejected.

**AC-0202-010**
- **Requirement**: The 	rust_level field MUST be a value from the Trust Levels Catalog.
- **Verification**: Submit manifests with trust_level values "TRUST-LEVEL-SIG-VALIDATED", "CUSTOM-TRUST", and "TRUST-LEVEL-CERTIFIED".
- **Expected Result**: "TRUST-LEVEL-SIG-VALIDATED" and "TRUST-LEVEL-CERTIFIED" are accepted. "CUSTOM-TRUST" is rejected.

**AC-0202-011**
- **Requirement**: The description field, when present, MUST NOT exceed 4096 characters.
- **Verification**: Submit a manifest with a description of 4097 characters.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID.

**AC-0202-012**
- **Requirement**: The entry_points array, when present, MUST specify valid entry point types from the Extension Points Catalog.
- **Verification**: Submit a manifest with an entry point type not in the catalog.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID.

**AC-0202-013**
- **Requirement**: All array fields in the manifest MUST NOT contain duplicate entries unless explicitly permitted.
- **Verification**: Submit a manifest with duplicate entries in capabilities, permissions, events_published, and events_subscribed.
- **Expected Result**: All duplicates are detected and cause manifest rejection.

**AC-0202-014**
- **Requirement**: The config_schema field, when present, MUST be a valid JSON Schema draft 2020-12 or later.
- **Verification**: Submit manifests with valid and invalid JSON Schema documents.
- **Expected Result**: Valid schemas are accepted. Invalid schemas are rejected with error PERR-MANIFEST-INVALID.

**AC-0202-015**
- **Requirement**: Field ordering in the manifest MUST follow the alphabetical ordering rule within REQUIRED and OPTIONAL groups.
- **Verification**: Parse a manifest with fields in non-alphabetical order and verify canonical serialization produces alphabetical order.
- **Expected Result**: Non-alphabetical order is accepted for submission but canonical serialization produces alphabetical order.

### 19.2 Manifest Validation (AC-0202-016 through AC-0202-025)

**AC-0202-016**
- **Requirement**: The manifest validation pipeline MUST consist of eleven sequential stages as defined in Section 10.
- **Verification**: Instrument the validation pipeline and verify stage execution order.
- **Expected Result**: All eleven stages execute in the defined sequence without bypass.

**AC-0202-017**
- **Requirement**: A manifest with invalid JSON syntax MUST be rejected at Stage 1.
- **Verification**: Submit a manifest document with malformed JSON.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID at Stage 1.

**AC-0202-018**
- **Requirement**: A manifest missing any REQUIRED field MUST be rejected at Stage 1.
- **Verification**: Submit a manifest omitting manifest_version, plugin_id, plugin_name, ersion, uthor, license, and integrity_hash individually.
- **Expected Result**: Each omission causes rejection at Stage 1 with error PERR-MANIFEST-INVALID.

**AC-0202-019**
- **Requirement**: A manifest with incorrect field types MUST be rejected at Stage 2.
- **Verification**: Submit a manifest where ersion is an integer instead of a string.
- **Expected Result**: The manifest is rejected at Stage 2 with error PERR-MANIFEST-INVALID.

**AC-0202-020**
- **Requirement**: A manifest with invalid enum values MUST be rejected at Stage 3.
- **Verification**: Submit a manifest with plugin_type set to an unrecognized value.
- **Expected Result**: The manifest is rejected at Stage 3 with error PERR-MANIFEST-INVALID.

**AC-0202-021**
- **Requirement**: Cross-field consistency checks MUST verify that 	rust_level is consistent with signature presence.
- **Verification**: Submit a manifest declaring TRUST-LEVEL-SIG-VALIDATED without a signature field.
- **Expected Result**: The manifest is rejected at Stage 5 with error PERR-MANIFEST-INVALID.

**AC-0202-022**
- **Requirement**: Catalog reference validation MUST verify all capability, permission, event, and extension point references.
- **Verification**: Submit a manifest with one valid and one invalid reference in each array field.
- **Expected Result**: All invalid references are detected and cause rejection at Stage 6.

**AC-0202-023**
- **Requirement**: Integrity hash verification MUST recompute the hash and compare against the manifest field.
- **Verification**: Submit a manifest with an integrity_hash that does not match the plugin binary.
- **Expected Result**: The manifest is rejected at Stage 7 with error PERR-INTEGRITY-FAIL.

**AC-0202-024**
- **Requirement**: Signature verification MUST validate against a trusted certificate authority.
- **Verification**: Submit a manifest with a valid signature from an untrusted CA.
- **Expected Result**: The manifest is rejected at Stage 8 with error PERR-SIGNATURE-INVALID.

**AC-0202-025**
- **Requirement**: The total validation pipeline MUST complete within 300 ms for a manifest with 20 capabilities, 15 permissions, and 10 dependencies.
- **Verification**: Measure wall-clock time for validation of the described manifest.
- **Expected Result**: Total validation time is less than or equal to 300 ms.

### 19.3 Manifest Evolution (AC-0202-026 through AC-0202-033)

**AC-0202-026**
- **Requirement**: Adding a new OPTIONAL field to the schema MUST NOT require a major schema version increment.
- **Verification**: Propose a schema change that adds one OPTIONAL field and increment the minor version.
- **Expected Result**: Existing plugin manifests remain valid under the new schema.

**AC-0202-027**
- **Requirement**: Removing a REQUIRED field from the schema MUST require a major schema version increment.
- **Verification**: Propose removing a REQUIRED field and observe the version increment requirement.
- **Expected Result**: The schema version major component is incremented.

**AC-0202-028**
- **Requirement**: Changing the data type of any field MUST require a major schema version increment.
- **Verification**: Propose changing a string field to an integer field.
- **Expected Result**: The schema version major component is incremented and existing manifests are rejected.

**AC-0202-029**
- **Requirement**: Adding new values to enumerated fields MUST NOT require a major schema version increment.
- **Verification**: Add a new trust level to the Trust Levels Catalog.
- **Expected Result**: Existing plugin manifests remain valid. The new value is available for use.

**AC-0202-030**
- **Requirement**: The runtime MUST support at least the two most recent schema versions simultaneously.
- **Verification**: Deploy a runtime supporting schema versions 1.0.0, 2.0.0, and 3.0.0. Attempt to load plugins on all three versions.
- **Expected Result**: All three plugin versions load successfully.

**AC-0202-031**
- **Requirement**: Deprecated schema versions MUST provide a minimum twelve-month migration window before rejection.
- **Verification**: Deprecate schema version 1.0.0 and measure the time until manifests on that version are rejected.
- **Expected Result**: The rejection occurs no sooner than twelve months after deprecation.

**AC-0202-032**
- **Requirement**: Tightening a validation constraint MUST require a major schema version increment.
- **Verification**: Reduce the maximum character length of plugin_name from 256 to 128.
- **Expected Result**: The schema version major component is incremented.

**AC-0202-033**
- **Requirement**: The schema version registry MUST track all active, deprecated, and retired schema versions.
- **Verification**: Query the schema version registry and verify the state of each registered version.
- **Expected Result**: The registry accurately reflects the state of every registered schema version.

### 19.4 Signature and Integrity (AC-0202-034 through AC-0202-042)

**AC-0202-034**
- **Requirement**: The integrity hash MUST use SHA-256 or a stronger algorithm.
- **Verification**: Submit manifests with SHA-256, SHA-384, and MD5 hashes.
- **Expected Result**: SHA-256 and SHA-384 are accepted. MD5 is rejected.

**AC-0202-035**
- **Requirement**: The integrity hash MUST be expressed as a lowercase hexadecimal string of exactly 64 characters for SHA-256.
- **Verification**: Submit hashes in uppercase, mixed case, and incorrect length.
- **Expected Result**: Only lowercase 64-character hex strings are accepted.

**AC-0202-036**
- **Requirement**: The signature algorithm MUST be RSA-2048 or higher, ECDSA P-256 or higher, or equivalent.
- **Verification**: Submit signatures using RSA-1024, RSA-2048, ECDSA P-256, and Ed25519.
- **Expected Result**: RSA-1024 is rejected. RSA-2048, ECDSA P-256, and Ed25519 are accepted.

**AC-0202-037**
- **Requirement**: Signature verification MUST check certificate revocation status.
- **Verification**: Submit a manifest signed with a certificate that has been revoked.
- **Expected Result**: The manifest is rejected with error PERR-SIGNATURE-INVALID.

**AC-0202-038**
- **Requirement**: The signature MUST cover the canonical form of the manifest.
- **Verification**: Modify a non-significant field (e.g., add whitespace) and verify the signature.
- **Expected Result**: The signature remains valid because the canonical form is unchanged.

**AC-0202-039**
- **Requirement**: A manifest declaring TRUST-LEVEL-SIG-VALIDATED or above MUST include a valid signature.
- **Verification**: Submit a manifest with TRUST-LEVEL-SIG-VALIDATED but no signature field.
- **Expected Result**: The trust level is downgraded to TRUST-LEVEL-UNVERIFIED or the manifest is rejected per runtime policy.

**AC-0202-040**
- **Requirement**: Key rotation MUST support a minimum ninety-day overlap period.
- **Verification**: Rotate a signing key and submit manifests signed with both old and new keys during the overlap window.
- **Expected Result**: Both signatures are accepted during the overlap period.

**AC-0202-041**
- **Requirement**: Expired signing keys MUST NOT be accepted for new installations.
- **Verification**: Submit a manifest signed with a key whose validity period has expired.
- **Expected Result**: The signature is rejected with error PERR-SIGNATURE-INVALID.

**AC-0202-042**
- **Requirement**: The runtime MUST verify the integrity hash at every load, update, and activation event.
- **Verification**: Tamper with the plugin binary after initial validation and attempt to activate the plugin.
- **Expected Result**: Activation is prevented with error PERR-INTEGRITY-FAIL.

### 19.5 Manifest Registry (AC-0202-043 through AC-0202-050)

**AC-0202-043**
- **Requirement**: The registry MUST store the raw manifest document durably.
- **Verification**: Submit a manifest, restart the registry, and retrieve the stored document.
- **Expected Result**: The retrieved document matches the submitted document exactly.

**AC-0202-044**
- **Requirement**: The registry MUST maintain indexes on plugin_id, plugin_type, trust_level, capabilities, permissions, version, and author.
- **Verification**: Query each index individually and verify result accuracy.
- **Expected Result**: Each query returns the correct set of manifests.

**AC-0202-045**
- **Requirement**: Registry queries MUST support filtering, sorting, and pagination.
- **Verification**: Execute a query with all three modifiers and verify the result set.
- **Expected Result**: Results are correctly filtered, sorted, and limited to the page size.

**AC-0202-046**
- **Requirement**: The registry MUST retain historical manifest versions for a minimum of twenty-four months.
- **Verification**: Submit a manifest, update it, and query historical versions after twenty-five months.
- **Expected Result**: Historical versions are still retrievable.

**AC-0202-047**
- **Requirement**: Removed manifests MUST be retained in archived state for a minimum of thirty-six months.
- **Verification**: Remove a plugin and query the archive after thirty-seven months.
- **Expected Result**: The removed manifest is still retrievable from the archive.

**AC-0202-048**
- **Requirement**: Concurrent manifest updates MUST be resolved using optimistic locking based on version numbers.
- **Verification**: Submit two concurrent updates to the same plugin with different version numbers.
- **Expected Result**: One update succeeds and the other is rejected with a conflict error.

**AC-0202-049**
- **Requirement**: The audit trail MUST record every manifest mutation with timestamp, actor, and operation type.
- **Verification**: Perform create, update, and delete operations on a manifest and query the audit trail.
- **Expected Result**: All three operations are recorded with correct metadata.

**AC-0202-050**
- **Requirement**: Indexed registry queries by plugin_id MUST complete within 5 ms.
- **Verification**: Measure the response time for a plugin_id lookup in a registry with 10,000 manifests.
- **Expected Result**: Query response time is less than or equal to 5 ms.

### 19.6 Security (AC-0202-051 through AC-0202-056)

**AC-0202-051**
- **Requirement**: A plugin MUST NOT be able to increase its trust_level through manifest manipulation.
- **Verification**: Submit a manifest with a trust_level higher than what the security gate would assign.
- **Expected Result**: The trust_level is overridden to the gate-assigned value.

**AC-0202-052**
- **Requirement**: Permission requests MUST NOT exceed the permissions granted by the assigned trust_level.
- **Verification**: Submit a manifest requesting PERM-HOST-INTEGRATION at TRUST-LEVEL-UNVERIFIED.
- **Expected Result**: The permission is denied or the manifest is rejected.

**AC-0202-053**
- **Requirement**: The registry_metadata field MUST NOT contain sensitive or personally identifiable information.
- **Verification**: Submit a manifest with email addresses and phone numbers in registry_metadata.
- **Expected Result**: The manifest is rejected or the fields are sanitized before storage.

**AC-0202-054**
- **Requirement**: Error messages from manifest validation MUST NOT leak internal system paths or certificate details.
- **Verification**: Trigger validation errors and examine the error messages returned to the caller.
- **Expected Result**: Error messages contain only generic descriptions without sensitive internals.

**AC-0202-055**
- **Requirement**: The manifest document MUST NOT exceed 64 kilobytes in canonical form.
- **Verification**: Submit a manifest with a canonical form of 65 kilobytes.
- **Expected Result**: The manifest is rejected with error PERR-MANIFEST-INVALID.

**AC-0202-056**
- **Requirement**: The security gate MUST enforce the principle of least privilege.
- **Verification**: Submit a manifest requesting more permissions than necessary for its declared capabilities.
- **Expected Result**: The security gate either rejects excess permissions or grants only the minimum required set.

### 19.7 Performance (AC-0202-057 through AC-0202-062)

**AC-0202-057**
- **Requirement**: Manifest structural parse MUST complete within 20 ms.
- **Verification**: Parse a manifest with 30 fields and measure parse time.
- **Expected Result**: Parse time is less than or equal to 20 ms.

**AC-0202-058**
- **Requirement**: Schema validation MUST complete within 100 ms for a manifest with 20 capabilities and 15 permissions.
- **Verification**: Validate the described manifest and measure total validation time.
- **Expected Result**: Validation time is less than or equal to 100 ms.

**AC-0202-059**
- **Requirement**: Signature verification MUST complete within 100 ms.
- **Verification**: Verify an RSA-2048 signature and measure verification time.
- **Expected Result**: Verification time is less than or equal to 100 ms.

**AC-0202-060**
- **Requirement**: Dependency resolution MUST complete within 50 ms for a graph with 50 plugins and 100 edges.
- **Verification**: Resolve dependencies for the described graph and measure resolution time.
- **Expected Result**: Resolution time is less than or equal to 50 ms.

**AC-0202-061**
- **Requirement**: Circular dependency detection MUST complete within 20 ms for a graph with 100 plugins.
- **Verification**: Detect cycles in a dependency graph with 100 plugins and 200 edges.
- **Expected Result**: Detection time is less than or equal to 20 ms.

**AC-0202-062**
- **Requirement**: Registry query for filtered results with pagination MUST complete within 50 ms for 10,000 manifests.
- **Verification**: Query manifests filtered by plugin_type with a page size of 50.
- **Expected Result**: Query time is less than or equal to 50 ms.

### 19.8 Compatibility (AC-0202-063 through AC-0202-068)

**AC-0202-063**
- **Requirement**: The compatibility_matrix MUST declare minimum and maximum runtime version ranges.
- **Verification**: Submit a manifest without version range declarations in the compatibility_matrix.
- **Expected Result**: The manifest is accepted if the field is OPTIONAL, but the runtime applies default compatibility rules.

**AC-0202-064**
- **Requirement**: Unsatisfiable version constraints MUST cause manifest rejection.
- **Verification**: Submit a manifest declaring a dependency version range that no installed plugin satisfies.
- **Expected Result**: The manifest is rejected with error PERR-VERSION-INCOMPATIBLE.

**AC-0202-065**
- **Requirement**: The runtime MUST support forward compatibility for at least one minor version beyond the declared maximum.
- **Verification**: Deploy a runtime two minor versions ahead of a plugin's declared maximum and attempt loading.
- **Expected Result**: The plugin loads successfully within the forward compatibility window.

**AC-0202-066**
- **Requirement**: The runtime MUST support backward compatibility for at least two minor versions below the declared minimum.
- **Verification**: Deploy a runtime two minor versions behind a plugin's declared minimum and attempt loading.
- **Expected Result**: The plugin loads successfully within the backward compatibility window.

**AC-0202-067**
- **Requirement**: Version constraints MUST use semantic versioning comparison operators.
- **Verification**: Submit dependency version constraints using caret, tilde, greater-than-or-equal, less-than-or-equal, equality, and greater-than operators.
- **Expected Result**: All standard semantic versioning operators are accepted and correctly evaluated.

**AC-0202-068**
- **Requirement**: The pi_version field MUST be compatible with the runtime API version.
- **Verification**: Submit a manifest with an api_version that has a different major version from the runtime.
- **Expected Result**: The manifest is rejected with error PERR-VERSION-INCOMPATIBLE.

---

## 20. Cross References

| This RFC Section | Referenced RFC | Referenced Section |
|---|---|---|
| 9.3 Dependency Fields | RFC-0212 | Plugin Dependency Resolution |
| 9.6 Security and Trust Fields | RFC-0205 | Security Gate Specification |
| 9.10 Field Ordering Rules | RFC-1005 | Common Manifest Model |
| 10. Manifest Validation Process | RFC-0201 | Plugin Lifecycle Specification |
| 11. Manifest Evolution | RFC-1005 | Common Manifest Model |
| 13. Signature and Integrity | RFC-0205 | Security Gate Specification |
| 14. Manifest Registry | RFC-0204 | Plugin Registry Specification |
| 15. Compatibility Declaration | RFC-0212 | Plugin Dependency Resolution |
| 16. Security Considerations | RFC-0205 | Security Gate Specification |
| Section 7 (Invariants) | RFC-0201 | Plugin Lifecycle Specification |
| Section 7 (Invariants) | RFC-0205 | Security Gate Specification |

---

## 21. References

1. **RFC 2119** — Key words for use in RFCs to Indicate Requirement Levels, IETF.
2. **RFC 1005** — Common Manifest Model, Atlas Specification Committee.
3. **RFC 0010** — Runtime Manifest Specification, Atlas Specification Committee.
4. **RFC 0201** — Plugin Lifecycle Specification, Atlas Specification Committee.
5. **RFC 0204** — Plugin Registry Specification, Atlas Specification Committee.
6. **RFC 0205** — Plugin Security Gate Specification, Atlas Specification Committee.
7. **RFC 0212** — Plugin Dependency Resolution Specification, Atlas Specification Committee.
8. **Plugin Manifest Fields Catalog** — Canonical field definitions, Atlas Plugin Catalog.
9. **Plugin Types Catalog** — Plugin type taxonomy, Atlas Plugin Catalog.
10. **Capabilities Catalog** — Capability identifier taxonomy, Atlas Plugin Catalog.
11. **Permissions Catalog** — Permission identifier taxonomy, Atlas Plugin Catalog.
12. **Plugin Errors Catalog** — Error code taxonomy, Atlas Plugin Catalog.
13. **Plugin Dependency Types Catalog** — Dependency relationship taxonomy, Atlas Plugin Catalog.
14. **Plugin Trust Levels Catalog** — Trust classification taxonomy, Atlas Plugin Catalog.
15. **Plugin States Catalog** — Lifecycle state taxonomy, Atlas Plugin Catalog.
16. **IETF RFC 8259** — The JavaScript Object Notation (JSON) Data Interchange Format.
17. **IETF RFC 8252** — OAuth 2.0 for Native Apps.
18. **Semantic Versioning 2.0.0** — Versioning specification for software manifests.
19. **NIST SP 800-57** — Recommendation for Key Management.
20. **SPDX License List** — Standardized license identifiers.

---

## 22. Revision History

| Version | Date | Author | Change Description |
|---|---|---|---|
| 0.1.0 | 2026-06-30 | Atlas Specification Committee | Initial draft. Defined manifest schema, validation pipeline, evolution process, signature and integrity mechanisms, registry integration, and performance budgets. |
| 1.0.0 | 2026-06-30 | Atlas Specification Committee | Accepted. Added 68 acceptance criteria across 8 categories. Finalized all sections with normative language per RFC 2119. Integrated cross-references to all plugin catalog specifications. |

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

## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | RFC-0201, RFC-0202, RFC-0214 |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | schemas/plugin/manifest.json |
| Related Catalog | catalog/plugin-manifest-examples.md |

## 23. Future Evolution

### 23.1 Planned Enhancements

1. **Plugin Bundle Manifests**: Support for multi-plugin bundles with a single manifest declaring inter-plugin relationships and shared resources.

2. **Dynamic Manifest Updates**: Mechanism for runtime-initiated manifest field updates (e.g., trust level changes, permission revocations) without full unload-reload cycles.

3. **Manifest Compression**: Optional compression of manifest documents for large plugins with extensive configuration schemas, with decompression transparent to the validation pipeline.

4. **Multi-tenancy Support**: Manifest fields for tenant isolation, enabling multi-tenant deployments where plugins are scoped to specific tenants.

5. **Machine-Readable License Verification**: Integration with license compliance engines that automatically verify that plugin licenses are compatible with the deployment's licensing policy.

6. **Manifest Diff and Patch**: Mechanism for expressing incremental manifest changes (patches) rather than full-document replacement, reducing bandwidth for registry synchronization.

### 23.2 Exploration Topics

1. **Zero-Knowledge Manifest Proofs**: Investigating zero-knowledge proof systems that allow a plugin to prove compliance with manifest constraints without revealing the full manifest content.

2. **Decentralized Plugin Identity**: Exploring decentralized identifier (DID) systems for plugin identity management, enabling publisher-independent identity verification.

3. **Automated Schema Migration**: Tooling for automated migration of plugin manifests across schema versions, reducing operator burden during schema evolution.

4. **Manifest-Based Policy-as-Code**: Extending the manifest to support declarative policy expressions that complement the security gate's rule-based evaluation.

5. **Cross-Subsystem Manifest Federation**: Mechanisms for sharing manifest data between the Plugin subsystem and other Atlas subsystems (Runtime, Workflow, Vision) to enable cross-domain dependency resolution.

---
