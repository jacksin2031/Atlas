---
title: Workflow Manifest Entity Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Manifest Entity Reference

## Overview

This document defines the workflow manifest entity reference for the Atlas Development System (ADS) workflow engine. The manifest is the declarative specification that describes a workflow's structure, behavior, and constraints. It serves as the single source of truth for workflow definition and MUST be validated before execution.

The manifest is an abstract entity. Its serialization format is implementation-defined, but the logical structure described herein is normative.

## Manifest Structure

The manifest is organized into a hierarchical structure of sections. Each section declares a distinct aspect of the workflow.

| Section | Description | Nesting |
|---------|-------------|---------|
| `metadata` | Workflow identification and versioning | Top-level |
| `context` | Global context configuration | Top-level |
| `nodes` | Node definitions and configurations | Top-level |
| `edges` | Connectivity and flow relationships | Top-level |
| `conditions` | Predicate definitions for routing | Top-level |
| `hooks` | Hook declarations and activation rules | Top-level |
| `errors` | Error handling policies | Top-level |
| `resources` | Resource pool declarations | Top-level |
| `scheduling` | Scheduler configuration | Top-level |
| `permissions` | Access control rules | Top-level |
| `extensions` | Custom extension registrations | Top-level |

### Metadata Section

The metadata section identifies the workflow and declares its versioning information.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | String | YES | Unique workflow identifier |
| `name` | String | YES | Human-readable workflow name |
| `version` | String | YES | Semantic version per `workflow-versioning.md` |
| `description` | String | NO | Workflow purpose and scope |
| `author` | EntityReference | NO | Creator of the workflow definition |
| `tags` | Array | NO | Classification tags |
| `created_at` | Timestamp | YES | Definition creation time |
| `updated_at` | Timestamp | YES | Last modification time |

### Context Section

The context section declares global and workflow-level context configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `variables` | Object | NO | Global variable declarations |
| `parameters` | Object | NO | Workflow-level parameter defaults |
| `bindings` | Array | NO | Resource binding declarations |
| `inheritance` | Object | NO | Context inheritance rules |

### Nodes Section

The nodes section declares all nodes in the workflow graph.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `definitions` | Array | YES | Node definition objects |
| `default_type` | Enum | NO | Default action type for unspecified nodes |
| `max_nodes` | Integer | NO | Upper bound on node count |

Each node definition object contains:

| Node Field | Type | Required | Description |
|------------|------|----------|-------------|
| `id` | String | YES | Unique node identifier |
| `type` | Enum | YES | Node type per `workflow-node-types.md` |
| `action` | EntityReference | YES | Associated action entity reference |
| `hooks` | Array | NO | Node-level hook declarations |
| `timeout` | Duration | NO | Node execution timeout |
| `retry_policy` | Object | NO | Retry configuration |
| `capabilities_required` | Array | NO | Required capability types |
| `permissions` | Array | NO | Node-specific permission overrides |

### Edges Section

The edges section declares connectivity between nodes.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `connections` | Array | YES | Edge connection objects |
| `default_condition` | EntityReference | NO | Default routing condition |

Each connection object contains:

| Edge Field | Type | Required | Description |
|------------|------|----------|-------------|
| `id` | String | YES | Unique edge identifier |
| `source` | String | YES | Source node ID |
| `target` | String | YES | Target node ID |
| `condition` | EntityReference | NO | Condition governing traversal |
| `data_mapping` | Object | NO | Field-level data mapping |

### Conditions Section

The conditions section declares all condition entities used by the workflow.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entities` | Array | YES | Condition entity definitions |
| `evaluation_order` | Enum | NO | `sequential`, `parallel`, or `lazy` |

### Hooks Section

The hooks section declares workflow-level hook configurations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pre_execution` | Array | NO | Pre-execution hook declarations |
| `post_execution` | Array | NO | Post-execution hook declarations |
| `on_error` | Array | NO | On-error hook declarations |
| `on_complete` | Array | NO | On-complete hook declarations |
| `on_cancel` | Array | NO | On-cancel hook declarations |

### Errors Section

The errors section declares error handling policies.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `default_severity` | Enum | NO | Default error severity |
| `propagation_policy` | Enum | NO | `stop`, `continue`, or `compensate` |
| `categories` | Array | NO | Error category-specific policies |
| `recovery_strategies` | Array | NO | Recovery strategy declarations |

### Resources Section

The resources section declares resource pools and constraints.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pools` | Array | NO | Resource pool definitions |
| `limits` | Object | NO | Overall resource limits |
| `allocation_policy` | Enum | NO | `greedy`, `fair-share`, or `priority` |

### Scheduling Section

The scheduling section declares scheduler configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `strategy` | Enum | YES | Scheduling strategy per `workflow-schedulers.md` |
| `priority_config` | Object | NO | Priority weight configuration |
| `deadline_config` | Object | NO | Deadline enforcement configuration |

### Permissions Section

The permissions section declares access control rules.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `roles` | Array | NO | Role definitions |
| `rules` | Array | YES | Permission rule objects |
| `default_policy` | Enum | NO | `deny-all` or `allow-all` |

### Extensions Section

The extensions section declares custom extension registrations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `node_types` | Array | NO | Custom node type registrations |
| `condition_types` | Array | NO | Custom condition type registrations |
| `hook_types` | Array | NO | Custom hook type registrations |
| `serializers` | Array | NO | Custom serializer registrations |

## Required Fields

The following fields are required in every manifest:

| Field | Section | Constraint |
|-------|---------|------------|
| `metadata.id` | metadata | MUST be globally unique |
| `metadata.name` | metadata | MUST be non-empty |
| `metadata.version` | metadata | MUST conform to semantic versioning |
| `metadata.created_at` | metadata | MUST be a valid timestamp |
| `metadata.updated_at` | metadata | MUST be a valid timestamp |
| `nodes.definitions` | nodes | MUST contain at least one node |
| `edges.connections` | edges | MAY be empty for single-node workflows |
| `scheduling.strategy` | scheduling | MUST be a valid strategy enum |
| `permissions.rules` | permissions | MUST declare at least one rule |

## Optional Fields

All fields not listed in the required fields table are optional. Optional fields have well-defined defaults when omitted:

| Optional Field | Default Value |
|---------------|---------------|
| `metadata.description` | Empty string |
| `metadata.author` | Engine system identity |
| `metadata.tags` | Empty array |
| `context.variables` | Empty object |
| `context.bindings` | Empty array |
| `nodes.default_type` | `Execute` |
| `nodes.max_nodes` | No limit |
| `edges.default_condition` | Unconditional traversal |
| `conditions.evaluation_order` | `sequential` |
| `hooks.*` | Empty arrays |
| `errors.default_severity` | `Error` |
| `errors.propagation_policy` | `stop` |
| `resources.pools` | Engine default pools |
| `resources.limits` | No limits |
| `resources.allocation_policy` | `priority` |
| `scheduling.priority_config` | Equal weights |
| `scheduling.deadline_config` | No deadlines |
| `permissions.default_policy` | `deny-all` |
| `extensions.*` | Empty arrays |

## Manifest Validation Rules

Manifest validation follows the rules defined in `workflow-validation-rules.md`. The manifest-specific validation rules are:

| Rule | Description | Severity |
|------|-------------|----------|
| `StructuralValidity` | Manifest JSON/XML structure is well-formed | Critical |
| `RequiredFieldsPresent` | All required fields are present and non-null | Critical |
| `VersionFormat` | Version string conforms to semantic versioning | Critical |
| `NodeConnectivity` | All nodes are reachable from a root node | Error |
| `CycleDetection` | No circular dependencies exist in the graph | Critical |
| `TypeCompatibility` | Edge data mappings are type-compatible | Error |
| `PermissionConsistency` | Permission rules are non-contradictory | Warning |
| `ResourceFeasibility` | Resource demands are satisfiable by available pools | Error |
| `HookValidity` | All hook references resolve to valid entities | Warning |
| `ExtensionCompatibility` | Extension registrations conform to declared schemas | Error |

## Manifest Versioning

Manifests are versioned using the scheme defined in `workflow-versioning.md`.

### Version Compatibility

| Version Change | Compatibility | Migration Required |
|---------------|--------------|-------------------|
| Patch increment | Fully compatible | NO |
| Minor increment | Backward compatible | Recommended |
| Major increment | Breaking change | Mandatory |

### Migration Strategies

When a manifest version is deprecated, the following migration strategies are available:

1. **Automatic Migration**: The engine applies transformation rules to upgrade the manifest.
2. **Manual Migration**: The operator reviews and applies changes using migration guides.
3. **Parallel Execution**: Both old and new manifest versions run concurrently during transition.
4. **Rollback**: The manifest is reverted to the previous version if migration fails.

### Deprecation Policy

Deprecated manifest versions are supported for a minimum of two major releases after deprecation. The deprecation notice includes:

1. The deprecated version range.
2. The replacement version.
3. A changelog of breaking differences.
4. A migration guide reference.
