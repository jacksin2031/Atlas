---
id: ATLAS-STORAGE-CATALOG-LIFECYCLE
title: Storage Lifecycle States Catalog
version: "1.0.0"
status: active
language: independent
---

# Storage Lifecycle States Catalog

## 1. Purpose

This catalog defines the canonical set of resource lifecycle states and transitions within the Atlas Storage subsystem. Every resource managed by Storage MUST enter one of these states and follow the transition rules defined herein.

## 2. State ID Prefix

All state identifiers use the prefix LC-.

## 3. Complete State Catalog

| State ID | Name | Description | Entry Conditions | Exit Transitions | RFC Reference |
|---|---|---|---|---|---|
| LC-CREATED | Created | Resource object instantiated but not yet persisted. | Write operation initiated. | Validating, Failed | RFC-0404 |
| LC-VALIDATING | Validating | Resource data is being checked against schema. | Entry from Created. | Stored, Failed | RFC-0404 |
| LC-STORED | Stored | Resource has been persisted but is not yet active. | Validation passed. | Active, Failed | RFC-0404 |
| LC-ACTIVE | Active | Resource is fully operational and accessible. | Storage confirmed. | Updating, Archived, Deleting, Restoring | RFC-0404 |
| LC-UPDATING | Updating | Resource data is being modified. | Entry from Active. | Active, Archived, Failed | RFC-0404 |
| LC-ARCHIVED | Archived | Resource is retained but no longer actively served. | Entry from Active or Updating. | Restoring, Purged | RFC-0404 |
| LC-DELETING | Deleting | Resource is scheduled for removal. | Entry from Active. | Purged, Failed | RFC-0404 |
| LC-RESTORING | Restoring | Resource is being recovered from archive or backup. | Entry from Archived or Purged (if recoverable). | Active, Failed | RFC-0404 |
| LC-PURGED | Purged | Resource has been permanently removed. | Entry from Deleting or Archived. | None (terminal) | RFC-0404 |
| LC-FAILED | Failed | Resource entered an unrecoverable error state. | Any state with unrecoverable error. | Restoring (manual) | RFC-0404 |

## 4. Legal Transition Matrix

| From \\ To | Created | Validating | Stored | Active | Updating | Archived | Deleting | Restoring | Purged | Failed |
|---|---|---|---|---|---|---|---|---|---|---|
| Created | X | OK | | | | | | | | |
| Validating | | X | OK | | | | | | | Failed |
| Stored | | | X | OK | | | | | | Failed |
| Active | | | | X | OK | OK | OK | | | |
| Updating | | | | | X | OK | OK | | | Failed |
| Archived | | | | | | X | | OK | | |
| Deleting | | | | | | | X | | Purged | Failed |
| Restoring | | | | | | | | X | | Failed |
| Purged | | | | | | | | | X | |
| Failed | | | | | | | | | | X | Restoring |

Legend: OK = legal transition, | = illegal transition, X = self-loop permitted.

## 5. Illegal Transitions

The following transitions are explicitly prohibited:

| From | To | Reason |
|---|---|---|
| Created | Active | Must pass through Validating and Stored. |
| Validating | Archived | Cannot archive before storage confirmation. |
| Stored | Deleting | Resource must be Active before deletion. |
| Purged | Any | Purged state is terminal; data is irrecoverable. |
| Archived | Updating | Archived resources must be restored first. |
| Failed | Active | Failed resources require manual intervention. |

## 6. Lifecycle Hooks

Each state transition MAY trigger pre- and post-hooks:

| Hook Phase | Description | RFC Reference |
|---|---|---|
| Pre-Transition | Executed before state change; MAY abort transition. | RFC-0419 |
| Post-Transition | Executed after state change; MUST NOT alter state. | RFC-0419 |
| Pre-Validation | Executed before schema validation. | RFC-0405 |
| Post-Storage | Executed after data is persisted. | RFC-0403 |
| Pre-Deletion | Executed before resource removal. | RFC-0404 |
| Post-Archive | Executed after archival is confirmed. | RFC-0411 |

## 7. Validation Rules

1. Every resource MUST begin in the Created state.
2. Every resource MUST reach the Active state before serving read operations.
3. The Purged state is terminal; no transitions FROM Purged are permitted.
4. Failed resources MAY be manually restored only from Failed to Restoring.
5. Lifecycle hooks MUST NOT cause cascading state changes.
6. State transitions MUST be atomic and durable.
