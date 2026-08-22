---
id: ATLAS-PLUGINSPEC-CATALOG-PERM
title: Permissions Catalog
version: "1.0.0"
status: active
language: independent
---

# Permissions Catalog

## 1. Purpose

This catalog defines the canonical set of permissions that govern what resources and operations a plugin MAY access during its lifetime. Permissions form the basis of the sandbox enforcement and security policy evaluation within the Atlas Plugin subsystem.

## 2. Stable ID Prefix

All permission identifiers use the prefix `PERM-`.

### 2.1 Naming Convention

Permission identifiers SHALL follow the pattern:

```
PERM-<DOMAIN>-<OPERATION>
```

where `<DOMAIN>` is an uppercase alphanumeric word identifying the resource category and `<OPERATION>` is an uppercase alphanumeric word identifying the access mode. The approved combinations are listed in Section 3.

## 3. Complete Catalog Table

| Stable ID                  | Permission Name            | Domain        | Operation  | Description                                              |
|----------------------------|----------------------------|---------------|------------|----------------------------------------------------------|
| PERM-FILESYSTEM-READ       | Filesystem Read            | FILESYSTEM    | READ       | Accesses files and directories on the host storage.      |
| PERM-FILESYSTEM-WRITE      | Filesystem Write           | FILESYSTEM    | WRITE      | Creates, modifies, or deletes files and directories.     |
| PERM-NETWORK-OUTBOUND      | Network Outbound           | NETWORK       | OUTBOUND   | Initiates connections to external hosts.                 |
| PERM-NETWORK-INBOUND       | Network Inbound            | NETWORK       | INBOUND    | Accepts incoming connections from external hosts.        |
| PERM-IPC-SEND              | IPC Send                   | IPC           | SEND       | Transmits messages to other processes or plugins.        |
| PERM-IPC-RECEIVE           | IPC Receive                | IPC           | RECEIVE    | Accepts messages from other processes or plugins.        |
| PERM-EVENT-PUBLISH         | Event Publish              | EVENT         | PUBLISH    | Emits events to the inter-plugin event bus.              |
| PERM-EVENT-SUBSCRIBE       | Event Subscribe            | EVENT         | SUBSCRIBE  | Registers listeners for events on the inter-plugin bus.  |
| PERM-CONFIG-READ           | Config Read                | CONFIG        | READ       | Accesses configuration data from the registry.           |
| PERM-CONFIG-WRITE          | Config Write               | CONFIG        | WRITE      | Modifies configuration data in the registry.             |
| PERM-MARKETPLACE-ACCESS    | Marketplace Access         | MARKETPLACE   | ACCESS     | Queries or interacts with plugin marketplaces.           |
| PERM-RESOURCE-LIMIT        | Resource Limit             | RESOURCE      | LIMIT      | Operates within defined CPU, memory, and I/O quotas.     |
| PERM-AUDIT-LOG             | Audit Log                  | AUDIT         | LOG        | Writes entries to the system audit log.                  |
| PERM-HOST-INTEGRATION      | Host Integration           | HOST          | INTEGRATE  | Interfaces with host operating system services.          |

## 4. Validation Rules

1. Every permission identifier MUST match the regex `^PERM-[A-Z]+-[A-Z]+$`.
2. A plugin manifest MUST declare each permission it requires from this catalog.
3. The sandbox enforcement layer MUST deny any operation for which the plugin holds no corresponding permission.
4. Declaring a permission in a manifest does NOT grant it; the runtime policy engine MUST explicitly authorize it.
5. Two or more permission identifiers MUST NOT share identical operational scope.
6. Implementations MUST NOT introduce permission identifiers outside this catalog.
7. Removing a permission from this catalog is prohibited once any registered plugin declares it.
8. Permission declarations in a manifest MUST be sorted in ascending lexicographic order of stable IDs.
9. The domain and operation components of a permission MUST correspond exactly to the values in the catalog table.

## 5. Cross-References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs to Indicate Requirement Levels.
- ATLAS-PLUGINSPEC-CATALOG-CAP — Capabilities Catalog (capabilities REQUIRE permissions to operate).
- ATLAS-PLUGINSPEC-CATALOG-PT — Plugin Types Catalog (types inform default permission grants).
- ATLAS-PLUGINSPEC-CATALOG-PEVT — Plugin Events Catalog (event permissions govern publish/subscribe).
- ATLAS-PLUGINSPEC-CATALOG-PERR — Plugin Errors Catalog (security violations MUST report PERR-SECURITY-VIOLATION).

## 6. Usage Guidelines

6.1 Plugin authors SHOULD request the minimum set of permissions necessary for their plugin to function.

6.2 Permission grants SHOULD be evaluated at plugin activation time; a plugin MUST NOT operate without the required permissions.

6.3 Implementations SHOULD support permission scoping by domain, allowing partial authorization (for example, granting PERM-FILESYSTEM-READ without PERM-FILESYSTEM-WRITE).

6.4 Plugins that declare PERM-NETWORK-OUTBOUND SHOULD also declare their intended destination scopes to enable policy filtering.

6.5 The audit log permission (PERM-AUDIT-LOG) SHOULD be granted only to plugins that participate in compliance or diagnostic workflows.

6.6 Host integration permissions (PERM-HOST-INTEGRATION) SHOULD be subject to elevated review and explicit administrator authorization.

6.7 Resource limit permissions (PERM-RESOURCE-LIMIT) MUST be enforced by the sandbox layer regardless of manifest declaration.

6.8 Marketplace access permissions (PERM-MARKETPLACE-ACCESS) SHOULD be scoped to specific marketplace endpoints.
