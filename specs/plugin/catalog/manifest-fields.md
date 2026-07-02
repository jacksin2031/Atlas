# Plugin Manifest Fields Catalog

## 1. Purpose

This catalog defines the canonical set of fields that MUST or MAY appear in a plugin manifest file. Each field specifies its semantic meaning, data type constraints, and validation rules. The manifest is the primary contract between a plugin publisher and the Atlas Plugin runtime.

## 2. Stable ID Prefix

Manifest field identifiers use the field name itself as the stable reference. Field names MUST be lowercase with hyphens separating words, following kebab-case convention.

## 3. Naming Convention

Field names MUST conform to the pattern `<lowercase-kebab-case>` and MUST be globally unique within the manifest schema. Reserved field names beginning with an underscore (`_`) are reserved for future specification use and MUST NOT be used by plugin publishers.

## 4. Canonical Manifest Field Table

| Field Name | Requirement | Type | Description | Validation Rules |
|---|---|---|---|---|
| `manifest_version` | REQUIRED | String | The version of the manifest schema this plugin adheres to. | MUST match a schema version registered in the runtime. MUST be a valid semantic version. |
| `plugin_id` | REQUIRED | String | The unique identifier for this plugin instance. | MUST conform to the stable ID prefix and naming convention defined in the plugin ID catalog. MUST be globally unique across all plugins in the system. |
| `plugin_name` | REQUIRED | String | The human-readable display name of the plugin. | MUST be non-empty. MUST NOT exceed 256 characters. MUST contain only printable Unicode characters. |
| `version` | REQUIRED | String | The semantic version of this plugin. | MUST conform to semantic versioning rules. MUST increment on every published update. |
| `author` | REQUIRED | String | The name or identity of the plugin publisher. | MUST be non-empty. MUST NOT exceed 256 characters. |
| `license` | REQUIRED | String | The SPDX identifier or full text of the license governing this plugin. | MUST be a valid SPDX identifier or a non-empty license text. |
| `description` | OPTIONAL | String | A human-readable description of the plugin purpose and functionality. | MUST NOT exceed 4096 characters if present. |
| `capabilities` | OPTIONAL | Array | A list of capability identifiers this plugin provides. | Each entry MUST reference a registered capability definition. MUST be non-empty if any capability is claimed. |
| `permissions` | OPTIONAL | Array | A list of permission identifiers this plugin requests. | Each entry MUST correspond to a permission defined in the security policy. MUST NOT request permissions exceeding the plugin's declared trust level. |
| `dependencies` | OPTIONAL | Object | A map of dependency declarations keyed by target plugin ID. | Each dependency entry MUST specify a valid `DEP-TYPE-*` identifier and a version constraint. MUST NOT declare self-dependencies. |
| `entry_points` | OPTIONAL | Array | A list of executable entry point definitions. | Each entry MUST specify a valid entry point type and a non-empty handler reference. |
| `sandbox_config` | OPTIONAL | Object | Configuration parameters for the plugin sandbox environment. | MUST be compatible with the plugin's declared trust level. MUST NOT request sandbox exemptions not permitted by the trust level. |
| `security_level` | OPTIONAL | String | The declared security classification of this plugin. | MUST be a value from the security level enumeration defined in the security specification. |
| `trust_level` | OPTIONAL | String | The trust level assigned to this plugin. | MUST be a value from the trust levels catalog. MUST be set by the runtime or governance process, not by the plugin publisher. |
| `signature` | OPTIONAL | String | The cryptographic signature of the plugin binary and manifest. | MUST be a valid signature verifiable against a trusted certificate authority. MUST be present if the plugin claims `TRUST-LEVEL-SIG-VALIDATED` or above. |
| `integrity_hash` | REQUIRED | String | A cryptographic hash of the plugin binary for integrity verification. | MUST be a SHA-256 or stronger hash. MUST be verifiable against the delivered binary. |
| `compatibility_matrix` | OPTIONAL | Object | A declaration of runtime and plugin version compatibility constraints. | Each entry MUST specify a version range and a compatibility status. |
| `extension_points` | OPTIONAL | Array | A list of extension point identifiers this plugin implements. | Each entry MUST be a valid `PEXT-*` identifier from the extension points catalog. |
| `api_version` | OPTIONAL | String | The version of the plugin API this plugin targets. | MUST be a valid semantic version. MUST be compatible with the runtime API version. |
| `config_schema` | OPTIONAL | Object | A JSON Schema definition of the plugin configuration options. | MUST be a valid JSON Schema draft. MUST define all configuration keys referenced in the plugin code. |
| `events_published` | OPTIONAL | Array | A list of event types this plugin emits. | Each entry MUST be a valid event type identifier. MUST NOT publish events not declared here. |
| `events_subscribed` | OPTIONAL | Array | A list of event types this plugin consumes. | Each entry MUST be a valid event type identifier. MUST NOT consume events not declared here. |
| `resource_limits` | OPTIONAL | Object | Declarations of maximum resource consumption (CPU, memory, I/O). | Each limit MUST be a positive integer with an associated unit. MUST NOT exceed the runtime-defined maximums. |
| `lifecycle_hooks` | OPTIONAL | Object | Definitions of custom logic executed at lifecycle transition points. | Each hook MUST reference a valid entry point. MUST NOT define hooks that conflict with runtime-enforced transitions. |
| `registry_metadata` | OPTIONAL | Object | Additional metadata for registry indexing and discovery. | MUST conform to the registry metadata schema. MUST NOT contain sensitive or personally identifiable information. |
| `marketplace_info` | OPTIONAL | Object | Information used by marketplace services for listing and discovery. | MUST conform to the marketplace information schema. Price and licensing fields MUST be consistent with the `license` field. |

## 5. Field Validation Rules

1. REQUIRED fields MUST be present and MUST pass all validation rules defined in the catalog table.
2. OPTIONAL fields, when present, MUST pass all validation rules defined in the catalog table.
3. When a field value is an array, it MUST NOT contain duplicate entries unless explicitly permitted by the field specification.
4. When a field value is an object, all keys MUST be strings and all values MUST be of a type permitted by the field specification.
5. String fields with character limits MUST enforce the limit strictly; values exceeding the limit MUST cause manifest rejection.
6. Cryptographic fields (`signature`, `integrity_hash`) MUST use industry-standard algorithms; weak or deprecated algorithms MUST NOT be accepted.
7. Version fields MUST use semantic versioning with pre-release and build metadata as permitted by the specification.
8. Enumerated fields MUST accept only values from the defined enumeration; unrecognized values MUST cause manifest rejection.
9. Cross-field consistency checks MUST be performed; for example, `trust_level` MUST be consistent with the presence or absence of `signature`.
10. The manifest MUST be serializable and deserializable without loss of information using the canonical encoding defined by the manifest specification.

## 6. Manifest Ordering Rules

1. REQUIRED fields MUST appear before OPTIONAL fields in the manifest document, where ordering is significant.
2. Fields within each group (REQUIRED and OPTIONAL) MUST appear in alphabetical order by field name.
3. Array fields MUST preserve the order of their elements; order MUST be semantically significant where documented.
4. Object fields MUST be serialized with keys in alphabetical order in the canonical form.

## 7. Cross-References

- RFC 2119: Key words for use in RFCs to Indicate Requirement Levels.
- Atlas Plugin ID Specification: Defines the stable ID prefix and naming convention for plugin identifiers.
- Atlas Plugin Extension Points Catalog: Defines valid `PEXT-*` identifiers for the `extension_points` field.
- Atlas Plugin Dependency Types Catalog: Defines valid `DEP-TYPE-*` identifiers for the `dependencies` field.
- Atlas Plugin Trust Levels Catalog: Defines valid trust level values for the `trust_level` field.
- IETF RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format.
- IETF RFC 8792: OAuth 2.0 Pushed Authorization Requests (for marketplace authentication flows).

## 8. Usage Guidelines

Plugin authors SHOULD include all OPTIONAL fields that provide useful information for discovery, configuration, and operations. Authors MUST ensure that the `integrity_hash` is computed after all other manifest modifications are complete to guarantee hash consistency. Authors SHOULD use `config_schema` to provide a discoverable configuration interface for end users. Runtime operators MUST NOT modify manifest fields directly; all modifications MUST go through the plugin update mechanism. Publishers MUST keep `marketplace_info` consistent with actual pricing and licensing terms. The `trust_level` field MUST be managed exclusively by the runtime or governance process; plugin publishers MUST NOT set this field.
