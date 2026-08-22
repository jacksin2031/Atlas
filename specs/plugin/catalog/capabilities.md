---
id: ATLAS-PLUGINSPEC-CATALOG-CAP
title: Capabilities Catalog
version: "1.0.0"
status: active
language: independent
---

# Capabilities Catalog

## 1. Purpose

This catalog defines the canonical set of capabilities that plugins MAY implement within the Atlas Plugin subsystem. Capabilities describe discrete functional competencies that the plugin registry, loader, and security subsystem recognize and enforce.

## 2. Stable ID Prefix

All capability identifiers use the prefix `CAP-PLUGIN-`.

### 2.1 Naming Convention

Capability identifiers SHALL follow the pattern:

```
CAP-PLUGIN-<FUNCTION>
```

where `<FUNCTION>` is an uppercase alphanumeric word drawn from the approved set in Section 3. No other prefix is permissible for capability identifiers.

## 3. Complete Catalog Table

| Stable ID                      | Capability Name              | Description                                                      |
|--------------------------------|------------------------------|------------------------------------------------------------------|
| CAP-PLUGIN-DISCOVERY           | Plugin Discovery             | Locates and enumerates available plugins.                        |
| CAP-PLUGIN-LOAD                | Plugin Load                  | Loads plugin binaries or modules into memory.                    |
| CAP-PLUGIN-SANDBOX             | Plugin Sandbox               | Enforces isolation boundaries for plugin execution.              |
| CAP-PLUGIN-EVENT               | Plugin Event                 | Publishes and subscribes to inter-plugin events.                 |
| CAP-PLUGIN-CONFIG              | Plugin Configuration         | Reads, validates, and persists plugin configuration data.        |
| CAP-PLUGIN-MANIFEST            | Plugin Manifest              | Parses and validates plugin manifest documents.                  |
| CAP-PLUGIN-REGISTRY            | Plugin Registry              | Registers, queries, and manages plugin metadata.                 |
| CAP-PLUGIN-DEPENDENCY          | Plugin Dependency            | Resolves and enforces inter-plugin dependency relationships.     |
| CAP-PLUGIN-SECURITY            | Plugin Security              | Applies security policies, access controls, and integrity checks.|
| CAP-PLUGIN-LIFECYCLE           | Plugin Lifecycle             | Manages plugin state transitions from install to removal.        |
| CAP-PLUGIN-MARKETPLACE         | Plugin Marketplace           | Interfaces with plugin distribution and transaction systems.     |
| CAP-PLUGIN-EXTENSION           | Plugin Extension             | Allows other plugins to extend core functionality.               |
| CAP-PLUGIN-API                 | Plugin API                   | Exposes programmatic interfaces for plugin interaction.          |
| CAP-PLUGIN-OBSERVABILITY       | Plugin Observability         | Collects metrics, traces, and diagnostic information.            |
| CAP-PLUGIN-VERSIONING          | Plugin Versioning            | Manages version declarations, compatibility, and upgrades.       |

## 4. Validation Rules

1. Every capability identifier MUST match the regex `^CAP-PLUGIN-[A-Z][A-Z0-9]*$`.
2. A plugin manifest MAY declare one or more capabilities from this catalog.
3. The plugin loader MUST reject any capability declared in a manifest that does not appear in the catalog table.
4. Two or more capability identifiers MUST NOT share identical functional descriptions.
5. Implementations MUST NOT introduce capability identifiers outside this catalog.
6. The capability list in a manifest MUST be sorted in ascending lexicographic order of stable IDs for deterministic comparison.
7. Removing a capability from this catalog is prohibited once any registered plugin declares it.
8. Adding a new capability to this catalog MUST NOT invalidate any existing plugin manifest.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- ATLAS-PLUGINSPEC-CATALOG-PT — Plugin Types Catalog (defines type-to-capability mappings).
- ATLAS-PLUGINSPEC-CATALOG-PERM — Permissions Catalog (capabilities REQUIRE corresponding permissions).
- ATLAS-PLUGINSPEC-CATALOG-PEVT — Plugin Events Catalog (capabilities MUST emit defined events on state transitions).
- ATLAS-PLUGINSPEC-CATALOG-PERR — Plugin Errors Catalog (capabilities MUST report errors using defined codes).

## 6. Usage Guidelines

6.1 Plugin authors SHOULD declare only the capabilities their plugin actually implements.

6.2 The plugin registry SHOULD verify that a plugin's declared capabilities are satisfied by its loaded modules before activating the plugin.

6.3 Capability enforcement MUST occur at load time; a plugin MUST NOT become active if any declared capability cannot be fulfilled.

6.4 Plugins that depend on a specific capability SHOULD declare that capability in their manifest dependencies.

6.5 Implementations of CAP-PLUGIN-SECURITY MUST align with the permissions defined in the Permissions Catalog.

6.6 Capability advertisements SHOULD include a version identifier to enable consumers to verify compatibility.

6.7 Observability capabilities (CAP-PLUGIN-OBSERVABILITY) SHOULD emit events defined in the Plugin Events Catalog for every significant state transition.
