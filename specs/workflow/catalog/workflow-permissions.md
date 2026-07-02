---
title: Workflow Permissions Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Permissions Reference

## Overview

This document defines the permission reference for the Atlas Development System (ADS) workflow engine. Permissions control access to workflow entities, resources, data, and operations. The permission model ensures that only authorized actors can perform actions within the workflow execution environment.

Permissions MUST be enforced at every layer of the workflow engine. No execution path MAY bypass permission checks. The permission model is abstract; concrete identity and authorization systems are bound at implementation time.

## Permission Types

The workflow engine defines three fundamental permission types that govern access to workflow entities.

| Permission Type | Scope | Description |
|----------------|-------|-------------|
| Role-based | Actor-centric | Access granted based on the actor's assigned roles |
| Attribute-based | Entity-centric | Access granted based on entity and contextual attributes |
| Capability-based | Node-centric | Access granted based on the node's advertised capabilities |

### Role-Based Permissions

Role-based permissions grant access based on the actor's role assignment. Roles are hierarchical and accumulate permissions from parent roles.

| Role Level | Permissions Granted | Examples |
|-----------|--------------------|----------|
| Viewer | Read-only access to workflow definitions and results | `readonly`, `observer` |
| Operator | Execute, monitor, and manage workflow instances | `operator`, `runner` |
| Administrator | Full access including definition, execution, and configuration | `admin`, `manager` |
| Developer | Create and modify workflow definitions | `developer`, `author` |
| Auditor | Read access to all workflow data including audit logs | `auditor`, `compliance` |

#### Role Assignment

Roles are assigned to actors through the following mechanisms:

| Mechanism | Description | Persistence |
|-----------|-------------|-------------|
| Direct Assignment | Explicit role-to-actor mapping | Persistent |
| Implicit Inheritance | Roles inherited from organizational hierarchy | Persistent |
| Dynamic Assignment | Roles assigned based on runtime context | Ephemeral |
| Temporary Delegation | Roles delegated for a limited duration | Time-bound |

#### Role Hierarchy

Roles form a Directed Acyclic Graph (DAG) of inheritance. A child role inherits all permissions from its parent roles.

| Parent Role | Child Role | Additional Permissions |
|------------|-----------|----------------------|
| Viewer | Operator | Execute, modify state |
| Viewer | Auditor | Read audit logs |
| Operator | Administrator | Modify definitions, manage roles |
| Developer | Operator | Execute own definitions |
| Auditor | Administrator | Full access (special privilege) |

### Attribute-Based Permissions

Attribute-based permissions grant access based on the attributes of the requesting entity, the target entity, and the surrounding context.

| Attribute Category | Examples | Use Case |
|-------------------|----------|----------|
| Actor Attributes | Organization, department, clearance level | Data segregation |
| Entity Attributes | Workflow type, sensitivity label, owner | Content-based access |
| Context Attributes | Time of day, geographic location, network zone | Situational access |
| Resource Attributes | Resource type, ownership, encryption status | Resource protection |

#### Policy Rules

Attribute-based policies are expressed as rules that evaluate attribute predicates.

| Rule Component | Type | Description |
|---------------|------|-------------|
| Effect | Enum | `allow` or `deny` |
| Principal | EntityReference | The actor requesting access |
| Action | Enum | The operation being requested |
| Resource | EntityReference | The target of the operation |
| Condition | ConditionEntity | Attribute predicate that must evaluate to true |
| Environment | Object | Additional context attributes |

#### Policy Evaluation Order

1. Explicit deny rules are evaluated first. If any deny rule matches, access is denied.
2. Explicit allow rules are evaluated next. If any allow rule matches, access is granted.
3. If no rule matches, the default policy applies.

### Capability-Based Permissions

Capability-based permissions grant access based on the node's advertised capabilities as defined in `workflow-capabilities.md`.

| Capability | Permission Granted | Required Attribute |
|-----------|-------------------|-------------------|
| Security | Access to credential-sensitive actions | Security capability with encryption attribute |
| Storage | Access to storage operations | Storage capability with write attribute |
| Network | Access to IPC and Signal operations | Network capability with protocol attribute |
| AI | Access to AI and Vision operations | AI capability with model attribute |
| Compute | Access to Execute and Transform operations | Compute capability with throughput attribute |

#### Capability Verification

1. The requesting node MUST advertise the required capability at the time of access.
2. The capability version MUST be compatible with the permission requirement.
3. Capability attributes MUST meet or exceed the minimum thresholds declared in the permission.
4. Expired or revoked capabilities result in immediate permission denial.

## Permission Model Integration

The three permission types are evaluated in combination. The overall access decision follows these rules:

1. Role-based permissions provide the baseline access model.
2. Attribute-based permissions refine access based on context.
3. Capability-based permissions provide node-level access for distributed execution.
4. All three types MUST agree for access to be granted. If any type denies, access is denied.

### Permission Evaluation Rules

| Rule | Description |
|------|-------------|
| Deny Overrides | Any explicit deny from any permission type results in denial |
| Require All | All applicable permission types MUST allow for access to be granted |
| Least Privilege | When multiple roles apply, the union of permissions is NOT granted; only the minimum required set is applied |
| Context Awareness | Attribute-based permissions evaluate against the current context snapshot |
| Capability Freshness | Capability-based permissions require current capability advertisements |

## Permission Inheritance

Permissions propagate through the workflow hierarchy following defined rules.

### Hierarchy Levels

| Level | Inherited From | Inherited By |
|-------|---------------|-------------|
| Global | N/A | Workflow |
| Workflow | Global | Nodes, Edges |
| Node | Workflow | Node's actions, hooks |
| Edge | Node | Edge's data flow |

### Inheritance Rules

1. Permissions flow downward from parent to child scopes.
2. Child scopes MAY restrict inherited permissions but MUST NOT expand them.
3. Explicit permissions at any level override inherited permissions.
4. Role assignments at the global level apply to all descendant scopes.
5. Capability requirements at the node level do NOT propagate to edges.

### Permission Escalation Prevention

1. A child scope CANNOT grant permissions that exceed the parent scope's permissions.
2. Role assignments at child scopes MUST be a subset of parent scope roles.
3. Attribute-based policies at child scopes MUST be stricter or equal to parent policies.
4. Capability-based permissions at child scopes MUST not relax parent requirements.

## Permission Revocation

Permissions MAY be revoked at any time through the following mechanisms:

### Revocation Methods

| Method | Scope | Trigger | Reversibility |
|--------|-------|---------|--------------|
| Immediate Revocation | Single entity | Administrative action | Reversible |
| Expiration | Time-bound | Timeout reached | Automatic |
| Cascade Revocation | Sub-tree | Parent revocation | Automatic |
| Conditional Revocation | Context-dependent | Condition evaluation | Context-dependent |

### Revocation Process

1. The revocation request is validated against the revoker's permissions.
2. The target permission entity is identified.
3. All dependent permissions are evaluated for cascade revocation.
4. The revocation is applied atomically.
5. Active workflows using revoked permissions enter a degraded state.
6. Events are emitted per `workflow-events.md` documenting the revocation.

### Revocation Impact

| Impact | Description |
|--------|-------------|
| Active Workflows | Workflows in progress may lose access to required resources |
| Scheduled Workflows | Workflows queued for execution are blocked |
| Cached Permissions | Permission caches are invalidated |
| Audit Trail | All revocations are recorded in the audit log |

## Permission Auditing

All permission decisions are logged for audit purposes.

| Log Entry | Field | Description |
|-----------|-------|-------------|
| Decision | Enum | `allow` or `deny` |
| Actor | EntityReference | The requesting actor |
| Resource | EntityReference | The target resource |
| Action | Enum | The requested operation |
| PermissionType | Enum | `role-based`, `attribute-based`, or `capability-based` |
| PolicyID | String | Identifier of the matching policy |
| Timestamp | Timestamp | Time of the decision |
| Context | Object | Relevant context attributes at decision time |

Audit logs are subject to the retention policies defined in `workflow-metrics.md` and MUST NOT be modified after creation.
