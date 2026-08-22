---
title: Workflow Validation Rules Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Validation Rules Reference

## Overview

This document defines the validation rule reference for the Atlas Development System (ADS) workflow engine. Validation rules ensure that workflow definitions conform to structural, semantic, and policy constraints before execution. The validation phase is mandatory; workflows that fail validation MUST NOT enter execution.

Validation rules are evaluated at planning time. Rule violations produce errors or warnings that prevent or allow execution respectively, based on the rule's severity level.

## Eleven Validation Rules

The workflow engine defines eleven validation rules. Each rule checks a distinct aspect of workflow correctness.

| Rule | Category | Severity | Checked At | Re-checkable |
|------|----------|----------|-----------|-------------|
| Structural | Graph integrity | Critical | Planning | NO |
| Semantic | Logical correctness | Error | Planning | YES |
| Type | Type compatibility | Error | Planning | NO |
| Resource | Resource feasibility | Error | Planning | YES |
| Budget | Cost and limit compliance | Warning | Planning | YES |
| Dependency | Dependency correctness | Critical | Planning | NO |
| Cycle | Acyclicity guarantee | Critical | Planning | NO |
| Reachability | Node connectivity | Error | Planning | YES |
| Completeness | Definition sufficiency | Critical | Planning | NO |
| Policy | Policy compliance | Error | Planning | YES |
| Security | Security constraint adherence | Critical | Planning | YES |

## Detailed Rule Definitions

### Structural Validation

Ensures the workflow graph is structurally well-formed.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Well-formed DAG | The graph must be a valid directed acyclic graph | Critical error; execution blocked |
| Valid node references | All node IDs must be unique and syntactically valid | Critical error |
| Valid edge references | All edge endpoints must reference existing nodes | Critical error |
| Root node existence | At least one node must have no incoming edges | Critical error |
| Leaf node existence | At least one node must have no outgoing edges | Warning |
| Self-loops | No node may have an edge to itself | Critical error |

### Semantic Validation

Ensures the workflow logic is semantically correct.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Condition satisfiability | All conditions must be evaluable with available context | Error; execution blocked |
| Hook validity | All hook references must resolve to valid entities | Warning; invalid hooks are skipped |
| Action compatibility | Action types must be compatible with node types | Error; incompatible nodes are flagged |
| Data flow consistency | Data produced by actions must be consumable by downstream actions | Error; broken data flows block execution |
| Timeout consistency | Timeout values must be positive and within manifest limits | Warning; invalid timeouts are corrected |

### Type Validation

Ensures type compatibility across all entity references.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Variable types | Context variable types must match declared schemas | Error; type mismatches block execution |
| Parameter types | Action parameter types must match expected types | Error; invalid parameters block execution |
| Result types | Action results must conform to the result type taxonomy | Warning; non-conforming results are flagged |
| Capability types | Node capabilities must match required capability types | Error; capability mismatches block execution |
| Operator types | Condition operators must accept the operand types | Error; invalid operator usage blocks execution |

### Resource Validation

Ensures resource requirements are feasible.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Resource availability | Required resources must be available in declared pools | Error; resource shortages block execution |
| Resource capacity | Resource capacity must exceed maximum demand | Warning; capacity warnings allow execution |
| Resource conflicts | No two nodes may exclusively require the same resource simultaneously | Error; conflicts block execution |
| Resource scaling | Dynamic scaling must be possible for elastic resources | Warning; scaling failures are noted |
| Resource timeout | Resource acquisition must complete within declared timeout | Error; acquisition timeouts block execution |

### Budget Validation

Ensures resource and cost budgets are respected.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Execution budget | Estimated execution cost must not exceed declared budget | Warning; budget overruns are flagged |
| Node count limit | Total nodes must not exceed the manifest's maximum | Error; excessive nodes block execution |
| Depth limit | Maximum graph depth must not be exceeded | Warning; deep graphs are flagged |
| Edge count limit | Total edges must not exceed the manifest's maximum | Error; excessive edges block execution |
| Hook count limit | Total hooks must not exceed the manifest's maximum | Warning; hook limits are advisory |

### Dependency Validation

Ensures dependency declarations are correct.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Dependency resolution | All dependency references must resolve | Error; unresolved dependencies block execution |
| Dependency ordering | Dependencies must not create circular ordering | Covered by Cycle rule |
| Dependency completeness | All required dependencies must be declared | Warning; undeclared dependencies are assumed |
| Conditional dependency | Conditional dependencies must have valid guard conditions | Error; invalid guards block execution |
| Optional dependency | Optional dependencies that are missing do not block execution | Informational |

### Cycle Detection

Ensures the workflow graph contains no cycles.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Graph acyclicity | The entire workflow graph must be acyclic | Critical error; cyclic graphs are rejected |
| Sub-graph acyclicity | All sub-graphs must be acyclic | Critical error |
| Trigger cycle | Triggers must not form circular activation chains | Critical error |
| Hook cycle | Hook chains must not form circular references | Critical error |
| Dependency cycle | Dependency edges must not form cycles | Critical error |

Cycle detection uses topological sort with O(V + E) complexity, where V is the number of vertices and E is the number of edges.

### Reachability Validation

Ensures all nodes are reachable from the root.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Root reachability | All nodes must be reachable from at least one root node | Error; unreachable nodes block execution |
| Edge reachability | All edges must connect reachable nodes | Warning; unreachable edges are removed |
| Condition reachability | All conditions must be reachable from an activating trigger | Error; unreachable conditions block execution |
| Hook reachability | All hooks must be attached to reachable nodes | Warning; unreachable hooks are ignored |
| Output reachability | All outputs must be consumed by at least one downstream node | Informational |

### Completeness Validation

Ensures the workflow definition is complete.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Manifest completeness | All required manifest fields must be present | Critical error; incomplete manifests are rejected |
| Node completeness | All nodes must have required attributes declared | Critical error; incomplete nodes block execution |
| Edge completeness | All edges must declare source and target | Critical error; incomplete edges block execution |
| Condition completeness | All conditions must declare type and operands | Critical error; incomplete conditions block execution |
| Hook completeness | All hooks must declare type and target | Warning; incomplete hooks are skipped |
| Permission completeness | All permission rules must declare principal and resource | Critical error; incomplete rules block execution |

### Policy Validation

Ensures compliance with declared policies.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Execution policy | Workflow must comply with declared execution policies | Error; policy violations block execution |
| Data policy | Data flows must comply with declared data policies | Error; data policy violations block execution |
| Retention policy | State retention must comply with declared retention policies | Warning; non-compliant retention is flagged |
| Audit policy | Required audit points must be declared | Warning; missing audit points are noted |
| Compliance policy | Workflow must comply with regulatory policies | Critical error; compliance failures block execution |

### Security Validation

Ensures security constraints are satisfied.

| Check | Description | Failure Behavior |
|-------|-------------|-----------------|
| Permission compliance | All node accesses must be permitted by the permission model | Critical error; unauthorized access blocks execution |
| Secret handling | Secret variables must be encrypted at rest and in transit | Critical error; unencrypted secrets block execution |
| Sandbox compliance | Sandboxed plugins must not access restricted resources | Error; sandbox violations block execution |
| Network isolation | Sensitive nodes must not communicate on untrusted networks | Warning; network violations are flagged |
| Injection prevention | Input data must be sanitized against injection attacks | Critical error; injection risks block execution |

## Rule Severity Levels

Each validation rule has an associated severity level that determines the impact of a violation.

| Severity | Symbol | Impact | Action |
|----------|--------|--------|--------|
| Critical | C | Execution is blocked | The workflow MUST NOT execute |
| Error | E | Execution is blocked | The workflow MUST NOT execute |
| Warning | W | Execution proceeds with caution | The workflow MAY execute; operator is notified |
| Informational | I | No operational impact | The workflow executes; information is logged |

## Rule Composition

Validation rules MAY be composed into rule sets for batch evaluation.

### Composition Operators

| Operator | Semantics | Use Case |
|----------|-----------|----------|
| ALL | All rules must pass | Strict validation |
| ANY | At least one rule must pass | Alternative validation paths |
| EXCEPT | All rules except specified | Selective validation |
| GROUP | Rules evaluated as a unit | Themed validation sets |

### Rule Set Definition

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | String | Rule set identifier |
| `rules` | Array | Member rule identifiers |
| `composition` | Enum | Composition operator |
| `severity_threshold` | Enum | Minimum severity for blocking |

## Rule Evaluation Order

Validation rules are evaluated in a specific order to maximize early failure detection and minimize redundant computation.

### Evaluation Sequence

1. **Structural** - Graph integrity is verified first to enable subsequent checks.
2. **Cycle** - Cycles are detected early to prevent infinite loops in later checks.
3. **Reachability** - Unreachable elements are identified before semantic checks.
4. **Completeness** - Missing declarations are identified before type checks.
5. **Type** - Type compatibility is verified before resource checks.
6. **Semantic** - Logical correctness is verified before policy checks.
7. **Resource** - Feasibility is verified before budget checks.
8. **Budget** - Cost compliance is verified before security checks.
9. **Dependency** - Dependency correctness is verified before policy checks.
10. **Policy** - Policy compliance is verified before security checks.
11. **Security** - Security constraints are verified last as they depend on all prior validations.

### Early Termination

Rule evaluation MAY terminate early under the following conditions:

1. If any Critical rule fails, evaluation terminates immediately; no further rules are evaluated.
2. If any Error rule fails, evaluation continues to collect all errors before blocking.
3. Warning and Informational rules are always evaluated regardless of prior failures.

## Rule Re-validation

Rules marked as re-checkable are re-evaluated when the workflow definition changes at runtime.

| Rule | Re-validation Trigger |
|------|---------------------|
| Semantic | Node or condition modification |
| Resource | Resource pool change |
| Budget | Budget limit adjustment |
| Dependency | Edge modification |
| Reachability | Node addition or removal |
| Policy | Policy update |
| Security | Permission change |

Re-validation is incremental; only affected rules are re-evaluated.
