---
title: Workflow Node Types Taxonomy
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Node Types Taxonomy

## Overview

This document defines the taxonomy of all node types supported by the Atlas Development System (ADS) workflow engine. Nodes are the vertices of the workflow execution graph. Each node type declares its attributes, advertised capabilities, and operational constraints.

Node types are abstract entities. Concrete node instances are created from these types during workflow execution. The engine enforces type constraints at planning time and validates instance properties at execution time.

## Node Type Categories

Node types are organized into four categories based on their primary execution role:

| Category | Node Types | Purpose |
|----------|-----------|---------|
| Core | Execute, Transform, Route, Branch, Loop, Wait, Signal, Notify | Fundamental workflow operations |
| Control | Compensate, Manual | Error handling and human interaction |
| Intelligence | AI, Vision | Cognitive and perception capabilities |
| Infrastructure | Plugin, Storage, IPC, SubGraph | System integration and composition |

## Detailed Node Type Definitions

### Execute

Performs a unit of work as defined by its associated action entity reference.

| Attribute | Type | Description |
|-----------|------|-------------|
| `action_ref` | EntityReference | The action to execute |
| `input_schema` | Object | Expected input data schema |
| `output_schema` | Object | Produced output data schema |
| `parallelism` | Integer | Maximum concurrent executions |
| `isolation` | Enum | `none`, `process`, or `container` |

| Capability | Description |
|------------|-------------|
| Compute | Processing capacity for the action workload |
| Security | Credential access for authenticated operations |

| Constraint | Description |
|------------|-------------|
| DAG | MUST NOT introduce cycles in the execution graph |
| Timeout | Execution bounded by declared timeout |
| Resource | Resource demands declared in action parameters |

### Transform

Transforms input data into output data according to a declared mapping.

| Attribute | Type | Description |
|-----------|------|-------------|
| `mapping_rules` | Array | Field-level transformation rules |
| `input_schema` | Object | Source data schema |
| `output_schema` | Object | Destination data schema |
| `validators` | Array | Post-transformation validation rules |
| `idempotent` | Boolean | Whether repeated transformation is safe |

| Capability | Description |
|------------|-------------|
| Compute | Processing capacity for transformation logic |
| Storage | Temporary storage for intermediate data |

| Constraint | Description |
|------------|-------------|
| Schema | Input and output schemas MUST be compatible |
| Purity | MUST NOT modify input data in place |
| Size | Output size bounded by manifest limit |

### Route

Directs flow along edges based on condition evaluation.

| Attribute | Type | Description |
|-----------|------|-------------|
| `conditions` | Array | Condition entity references |
| `default_edge` | String | Fallback edge ID |
| `evaluation_mode` | Enum | `first_match`, `all_match`, or `weighted` |
| `outgoing_edges` | Integer | Number of possible output edges |

| Capability | Description |
|------------|-------------|
| Logic | Condition evaluation capacity |

| Constraint | Description |
|------------|-------------|
| Coverage | All possible outcomes MUST have an edge |
| Mutually Exclusive | Conditional branches MUST be disjoint |
| Deterministic | Same conditions produce same routing |

### Branch

Splits flow into multiple parallel or conditional sub-flows.

| Attribute | Type | Description |
|-----------|------|-------------|
| `strategy` | Enum | `parallel`, `conditional`, or `fan_out` |
| `max_branches` | Integer | Maximum number of concurrent branches |
| `merge_policy` | Object | Rules for combining branch outputs |
| `timeout_per_branch` | Duration | Per-branch timeout |

| Capability | Description |
|------------|-------------|
| Compute | Capacity for concurrent branch execution |
| Synchronization | Merge and coordination capacity |

| Constraint | Description |
|------------|-------------|
| Concurrency | Branch count bounded by max_branches |
| Merge | All branches MUST converge or terminate |
| Isolation | Branches MUST NOT share mutable state |

### Loop

Repeats execution of a contained sub-graph.

| Attribute | Type | Description |
|-----------|------|-------------|
| `iterator_ref` | EntityReference | Data source for iteration |
| `exit_condition` | ConditionEntity | Loop termination predicate |
| `max_iterations` | Integer | Hard iteration limit |
| `batch_mode` | Boolean | Whether iterations are batched |
| `batch_size` | Integer | Items per batch |

| Capability | Description |
|------------|-------------|
| Compute | Capacity per iteration |
| State | Persistence for loop state across iterations |

| Constraint | Description |
|------------|-------------|
| Termination | Exit condition MUST be eventually satisfiable |
| State | Loop variables scoped to the node |
| Depth | Nested loops bounded by manifest limit |

### Wait

Pauses execution until a condition or time elapses.

| Attribute | Type | Description |
|-----------|------|-------------|
| `trigger_ref` | EntityReference | Event or signal to wait for |
| `duration` | Duration | Fixed wait period |
| `timeout_action` | Enum | `fail`, `skip`, or `continue` |
| `polling_interval` | Duration | Check frequency for trigger |

| Capability | Description |
|------------|-------------|
| Temporal | Time-tracking capacity |
| Event | Event-listening capacity |

| Constraint | Description |
|------------|-------------|
| No Cycle | Wait trigger MUST NOT be downstream of the wait node |
| Timeout | Duration bounded by manifest limit |
| Resource | Minimal resource consumption while waiting |

### Signal

Emits an event to notify observers.

| Attribute | Type | Description |
|-----------|------|-------------|
| `event_type` | String | Category of the emitted event |
| `payload_schema` | Object | Expected payload structure |
| `target_subscribers` | Array | Subscriber entity references |
| `delivery_mode` | Enum | `fire-and-forget` or `acknowledged` |

| Capability | Description |
|------------|-------------|
| Network | Event delivery capacity |
| Observability | Event publishing capacity |

| Constraint | Description |
|------------|-------------|
| Payload Size | Bounded by manifest limit |
| Event Type | Must be declared in event schema |
| Idempotency | Duplicate signals may be deduplicated |

### Notify

Delivers a notification to registered subscribers.

| Attribute | Type | Description |
|-----------|------|-------------|
| `channel_ref` | EntityReference | Notification channel |
| `template_ref` | EntityReference | Message template |
| `recipients` | Array | Subscriber entity references |
| `delivery_policy` | Enum | `at_least_once`, `at_most_once`, or `exactly_once` |

| Capability | Description |
|------------|-------------|
| Network | Message delivery capacity |
| Security | Encrypted channel support |

| Constraint | Description |
|------------|-------------|
| Template | Must resolve before dispatch |
| Recipients | Must be validated against subscriptions |
| Channel | Must be active and available |

### Compensate

Reverses the effects of a previously executed action.

| Attribute | Type | Description |
|-----------|------|-------------|
| `target_action_id` | String | ID of the action to compensate |
| `compensation_data_ref` | EntityReference | Stored compensation data |
| `order` | Enum | `reverse_topological` or `explicit` |
| `max_retries` | Integer | Retry attempts for compensation |

| Capability | Description |
|------------|-------------|
| State | Rollback capacity |
| Audit | Compensation recording capacity |

| Constraint | Description |
|------------|-------------|
| Precedence | Target action MUST have completed successfully |
| Idempotency | Double compensation is harmless |
| Scope | Compensation limited to declared actions |

### Manual

Requires human operator interaction to proceed.

| Attribute | Type | Description |
|-----------|------|-------------|
| `operator_ref` | EntityReference | Authorized operator |
| `timeout` | Duration | Approval deadline |
| `fallback_state` | Enum | State on timeout: `approve`, `reject`, or `hold` |
| `display_data` | Object | Data presented to the operator |

| Capability | Description |
|------------|-------------|
| UI | Display capacity for operator interface |
| Security | Authorization verification capacity |

| Constraint | Description |
|------------|-------------|
| Authorization | Operator must have declared permissions |
| Timeout | Expired actions transition to fallback state |
| Audit | Decisions are recorded permanently |

### AI

Invokes an artificial intelligence entity reference for computation.

| Attribute | Type | Description |
|-----------|------|-------------|
| `model_ref` | EntityReference | AI model to invoke |
| `input_schema` | Object | Expected input structure |
| `output_schema` | Object | Expected output structure |
| `confidence_threshold` | Float | Minimum confidence for acceptance |
| `cost_budget` | Float | Maximum cost per invocation |

| Capability | Description |
|------------|-------------|
| AI | Inference capacity |
| Compute | Model execution capacity |

| Constraint | Description |
|------------|-------------|
| Schema | Input must match model's expected schema |
| Budget | Cost bounded by declared limit |
| Privacy | Data handling per privacy policy |

### Vision

Processes visual data through a vision-capable entity reference.

| Attribute | Type | Description |
|-----------|------|-------------|
| `processor_ref` | EntityReference | Vision processing entity |
| `input_format` | Enum | `image`, `video_frame`, or `stream` |
| `interpretation_schema` | Object | Expected structured output |
| `confidence_threshold` | Float | Minimum confidence for acceptance |

| Capability | Description |
|------------|-------------|
| Vision | Image processing capacity |
| Storage | Temporary visual data storage |

| Constraint | Description |
|------------|-------------|
| Format | Input restricted to declared visual types |
| Output | Interpretations include confidence scores |
| Privacy | Visual data handling per policy |

### Plugin

Invokes a registered plugin entity reference.

| Attribute | Type | Description |
|-----------|------|-------------|
| `plugin_ref` | EntityReference | Plugin to invoke |
| `plugin_version` | String | Required plugin version |
| `interface_schema` | Object | Plugin interface contract |
| `sandbox` | Boolean | Whether plugin runs in sandbox |

| Capability | Description |
|------------|-------------|
| Extensibility | Plugin invocation capacity |
| Security | Sandboxing capacity |

| Constraint | Description |
|------------|-------------|
| Registration | Plugin must be registered via extension points |
| Version | Must be compatible with declared version |
| Sandbox | Sandboxed plugins have restricted access |

### Storage

Performs data storage or retrieval operations.

| Attribute | Type | Description |
|-----------|------|-------------|
| `storage_ref` | EntityReference | Storage entity to use |
| `access_pattern` | Enum | `read`, `write`, `append`, or `delete` |
| `encryption` | Boolean | Whether data is encrypted at rest |
| `durability` | Enum | `eventual`, `strong`, or `sequential` |

| Capability | Description |
|------------|-------------|
| Storage | Data persistence capacity |
| Security | Encryption capacity |

| Constraint | Description |
|------------|-------------|
| Size | Data size bounded by manifest limit |
| Access | Credentials must be valid |
| Pattern | Access pattern must match storage capabilities |

### IPC

Facilitates inter-process or inter-service communication.

| Attribute | Type | Description |
|-----------|------|-------------|
| `peer_ref` | EntityReference | Communication peer |
| `protocol` | String | Communication protocol |
| `message_limit` | Integer | Maximum message size |
| `ordering` | Enum | `ordered`, `unordered`, or `partial` |

| Capability | Description |
|------------|-------------|
| Network | Communication capacity |
| Protocol | Protocol-specific handling capacity |

| Constraint | Description |
|------------|-------------|
| Reachability | Peer must be reachable |
| Timeout | Dead-peer detection per timeout config |
| Protocol | Protocol must be supported by both peers |

### SubGraph

Represents a nested workflow graph as a single node.

| Attribute | Type | Description |
|-----------|------|-------------|
| `sub_graph_ref` | EntityReference | Nested workflow definition |
| `input_contract` | Object | Parent-to-sub-graph data contract |
| `output_contract` | Object | Sub-graph-to-parent data contract |
| `isolation_level` | Enum | `none`, `partial`, or `full` |

| Capability | Description |
|------------|-------------|
| Composition | Nested workflow execution capacity |
| Context | Context propagation capacity |

| Constraint | Description |
|------------|-------------|
| Acyclic | Sub-graph must be a DAG; no recursion |
| Contract | Input/output contracts must be explicit |
| Visibility | Sub-graph scope is isolated by default |

## Node Type Selection

When the engine assigns a node type to a node instance, it follows these rules:

1. The node's declared type in the manifest takes precedence.
2. If no type is declared, the default type from the nodes section is used.
3. Capability requirements from the associated action constrain the set of permissible types.
4. Resource availability influences the final selection among compatible types.
