---
id: ATLAS-PLUGINSPEC-CATALOG-PT
title: Plugin Types Catalog
version: "1.0.0"
status: active
language: independent
---

# Plugin Types Catalog

## 1. Purpose

This catalog defines the canonical set of plugin types within the Atlas Plugin subsystem. Each type identifies the primary role a plugin fulfills and constrains its permissible capabilities, permissions, and lifecycle behaviors.

## 2. Stable ID Prefix

All plugin type identifiers use the prefix `PT-`.

### 2.1 Naming Convention

Plugin type identifiers SHALL follow the pattern:

```
PT-<CATEGORY>
```

where `<CATEGORY>` is an uppercase alphanumeric word drawn from the approved set in Section 3. No other prefix is permissible for type identifiers.

## 3. Complete Catalog Table

| Stable ID     | Type Name       | Description                                                  |
|---------------|-----------------|--------------------------------------------------------------|
| PT-WORKFLOW   | Workflow        | Orchestrates sequences of operations across plugins.         |
| PT-VISION     | Vision          | Provides visual interpretation, image analysis, or rendering.|
| PT-AI         | AI              | Implements artificial intelligence or machine learning logic.|
| PT-STORAGE    | Storage         | Manages data persistence, retrieval, or caching.             |
| PT-UI         | User Interface  | Supplies graphical or textual interface components.          |
| PT-IPC        | Inter-Process   | Facilitates communication between isolated processes.        |
| PT-KNOWLEDGE  | Knowledge       | Curates, indexes, or serves domain knowledge bases.          |
| PT-MARKETPLACE| Marketplace     | Enables plugin distribution, listing, or transaction logic.  |
| PT-PROVIDER   | Provider        | Supplies external services, APIs, or data sources.           |
| PT-ADAPTER    | Adapter         | Translates between incompatible interfaces or protocols.     |
| PT-SERVICE    | Service         | Exposes reusable functional capabilities to other plugins.   |
| PT-UTILITY    | Utility         | Offers general-purpose helper functions or shared logic.     |

## 4. Validation Rules

1. Every plugin manifest MUST declare exactly one type from this catalog.
2. Type identifiers MUST match the regex `^PT-[A-Z][A-Z0-9]*$`.
3. The type value in a manifest MUST be identical to one of the stable IDs listed in Section 3.
4. No new type identifiers MAY be introduced without updating this catalog.
5. Removing a type identifier from this catalog is prohibited once any registered plugin declares it.
6. Two or more type identifiers MUST NOT share the same description semantics.
7. The catalog table in Section 3 MUST be treated as the authoritative reference for type resolution.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- ATLAS-PLUGINSPEC-CATALOG-CAP — Capabilities Catalog (defines the relationship between types and capabilities).
- ATLAS-PLUGINSPEC-CATALOG-PERM — Permissions Catalog (defines permission constraints per type).

## 6. Usage Guidelines

6.1 Plugin authors SHOULD select the most specific type that describes their plugin's primary responsibility.

6.2 When a plugin serves multiple roles, the author MUST designate the dominant role as the declared type and record secondary roles in the plugin manifest metadata.

6.3 Registry implementations MUST reject manifests that declare a type not present in the catalog table.

6.4 Lifecycle management systems SHOULD enforce type-specific behavior constraints (for example, PT-UI plugins MUST NOT initiate network connections without explicit permission declaration).

6.5 Consumers of the plugin registry SHOULD index plugins by type to enable filtered discovery and dependency resolution.

6.6 Type assignments SHOULD remain stable across plugin version upgrades. Changing a declared type constitutes a breaking change and MUST increment the major version per the versioning specification.
