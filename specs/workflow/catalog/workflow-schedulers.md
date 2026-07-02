---
title: Workflow Schedulers Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Schedulers Reference

## Overview

This document defines the scheduler reference for the Atlas Development System (ADS) workflow engine. Schedulers determine the order and manner in which workflow nodes are dispatched to execution resources. The scheduling model balances competing objectives: throughput, latency, fairness, and resource utilization.

Schedulers are abstract entities. Concrete scheduling algorithms are bound to scheduler instances at runtime, but the scheduling strategies and attributes described herein are normative.

## Scheduling Strategies

The workflow engine defines six scheduling strategies. Each strategy optimizes for a distinct objective.

| Strategy | Primary Objective | Secondary Objective | Complexity |
|----------|------------------|--------------------|------------|
| FIFO | Fairness through order preservation | Simplicity | O(n) |
| Priority | Minimize latency for high-priority work | Throughput | O(n log n) |
| Deadline | Meet time-critical commitments | Fairness | O(n log n) |
| Resource-aware | Optimize resource utilization | Throughput | O(n * m) |
| Fair-share | Equitable distribution across workflows | Isolation | O(n) |
| Weighted | Proportional allocation by declared weight | Flexibility | O(n log n) |

### FIFO (First-In, First-Out)

Nodes are dispatched in the order they become ready, respecting dependency ordering.

| Attribute | Type | Description |
|-----------|------|-------------|
| `queue_depth` | Integer | Maximum pending nodes in the queue |
| `preemption` | Boolean | Whether higher-priority nodes may preempt FIFO order |
| `starvation_prevention` | Boolean | Whether aging is applied to long-waiting nodes |

**Selection Rules:**
1. Ready nodes are sorted by their readiness timestamp.
2. Ties are broken by node ID (alphabetical).
3. If preemption is enabled and a higher-priority node becomes ready, the FIFO order is disrupted.
4. If starvation prevention is enabled, nodes waiting beyond a threshold receive boosted priority.

**Use Cases:**
- Batch processing workflows where order preservation is critical.
- Audited workflows where execution traceability is required.
- Low-contention environments where simplicity is preferred.

### Priority

Nodes are dispatched based on their declared priority values.

| Attribute | Type | Description |
|-----------|------|-------------|
| `priority_range` | Object | Minimum and maximum priority values |
| `priority_boost` | Float | Factor by which priority is multiplied |
| `priority_decay` | Float | Rate at which priority decreases over wait time |
| `preemption_threshold` | Integer | Priority difference required for preemption |

**Selection Rules:**
1. Ready nodes are sorted by priority (descending), then by readiness timestamp.
2. Nodes with priority above the preemption threshold MAY preempt lower-priority running nodes.
3. Priority decay reduces the effective priority of waiting nodes over time.
4. Priority boost amplifies the declared priority for scheduling calculations.

**Use Cases:**
- Multi-tenant environments with SLA-tiered workloads.
- Interrupt-driven workflows where urgent tasks must proceed.
- Resource-constrained environments requiring prioritized allocation.

### Deadline

Nodes are dispatched to meet declared deadline commitments.

| Attribute | Type | Description |
|-----------|------|-------------|
| `deadline_granularity` | Enum | `per_node`, `per_workflow`, or `per_batch` |
| `slack_ratio` | Float | Ratio of slack time used for scheduling decisions |
| `miss_penalty` | Float | Penalty score for missed deadlines |
| `earliest_deadline_first` | Boolean | Whether EDF ordering is used |

**Selection Rules:**
1. Ready nodes are sorted by deadline (ascending) when EDF is enabled.
2. When EDF is disabled, nodes are sorted by slack time (earliest deadline minus estimated execution time).
3. Nodes with zero or negative slack time are dispatched immediately.
4. Deadline misses incur the declared penalty and trigger alerting.

**Use Cases:**
- Time-sensitive workflows with contractual deadlines.
- Real-time processing pipelines.
- Service-level agreement (SLA) compliant execution.

### Resource-Aware

Nodes are dispatched considering the resource availability and utilization state.

| Attribute | Type | Description |
|-----------|------|-------------|
| `resource_prediction` | Boolean | Whether future resource availability is predicted |
| `locality_preference` | Enum | `prefer_local`, `prefer_spread`, or `agnostic` |
| `bin_packing` | Boolean | Whether nodes are packed onto fewer resources |
| `spread_policy` | Enum | `round-robin`, `least-loaded`, or `random` |

**Selection Rules:**
1. Ready nodes are matched to resource pools that satisfy their capability requirements.
2. Within matching pools, the node is assigned to the resource with the best fit.
3. Locality preference influences whether nodes are co-located or spread across resources.
4. Bin packing concentrates workloads; spread policy distributes them.

**Use Cases:**
- Distributed execution environments with heterogeneous resources.
- Cost-optimized execution where resource efficiency matters.
- Geographic-aware execution where data locality is important.

### Fair-Share

Workflows receive equitable shares of available resources regardless of priority.

| Attribute | Type | Description |
|-----------|------|-------------|
| `share_algorithm` | Enum | `proportional`, `egalitarian`, or `dominant` |
| `weight_per_workflow` | Float | Default weight for unweighted workflows |
| `starvation_threshold` | Duration | Maximum time a workflow may wait before dispatch |
| `preemption` | Boolean | Whether fair-share violations trigger preemption |

**Selection Rules:**
1. Each workflow is assigned a weight (default: equal weights).
2. Resource shares are proportional to declared weights.
3. Workflows below their fair share receive boosted dispatch priority.
4. Starvation threshold triggers emergency dispatch for long-waiting workflows.

**Use Cases:**
- Multi-tenant shared execution environments.
- Collaborative platforms where equity is required.
- Cost-sharing arrangements between organizations.

### Weighted

Nodes are dispatched proportionally to declared weights, allowing fine-grained control.

| Attribute | Type | Description |
|-----------|------|-------------|
| `weight_normalization` | Boolean | Whether weights are normalized to sum to one |
| `weight_update_frequency` | Duration | How often weights are re-evaluated |
| `minimum_weight` | Float | Floor weight below which a node is deprioritized |
| `maximum_weight` | Float | Ceiling weight above which a node is capped |

**Selection Rules:**
1. Each node is assigned a weight reflecting its importance.
2. Dispatch probability is proportional to the node's weight divided by the sum of all weights.
3. Weights outside the [minimum, maximum] range are clamped.
4. Weight updates are applied at the declared frequency.

**Use Cases:**
- Custom prioritization schemes beyond simple priority levels.
- Dynamic workload rebalancing.
- Experimentation where relative importance varies over time.

## Scheduler Attributes

Every scheduler instance possesses the following attributes:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | String | YES | Unique scheduler identifier |
| `strategy` | Enum | YES | One of the six scheduling strategies |
| `priority` | Integer | NO | Scheduler priority when multiple schedulers compete |
| `configuration` | Object | NO | Strategy-specific configuration parameters |
| `scope` | Enum | NO | `global`, `workflow`, or `node` |
| `tags` | Array | NO | Metadata tags for classification |

## Scheduler Configuration

Scheduler configuration is declared in the workflow manifest's scheduling section.

| Configuration Parameter | Type | Description |
|------------------------|------|-------------|
| `strategy` | Enum | Selected scheduling strategy |
| `parameters` | Object | Strategy-specific parameters |
| `constraints` | Object | Scheduling constraints (time, resource, priority) |
| `overrides` | Object | Node-specific scheduling overrides |

### Constraint Types

| Constraint | Type | Description |
|-----------|------|-------------|
| `max_queue_depth` | Integer | Maximum pending nodes |
| `max_parallelism` | Integer | Maximum concurrent node executions |
| `min_resource_utilization` | Float | Minimum resource utilization target |
| `max_wait_time` | Duration | Maximum node wait time before dispatch |
| `affinity_rules` | Array | Node-to-resource affinity declarations |

## Scheduler Selection Rules

When multiple schedulers are available, the following rules determine which scheduler handles a workflow:

1. **Scope Matching**: The scheduler whose scope matches the workflow scope is selected first.
2. **Strategy Preference**: Among matching schedulers, the one with the highest declared priority is selected.
3. **Load Balancing**: If multiple schedulers have equal priority, the least-loaded scheduler is selected.
4. **Fallback**: If no scheduler matches, the default FIFO scheduler is used.

### Scheduler Fallback

If the selected scheduler becomes unavailable:

1. The workflow is reassigned to the next-highest-priority available scheduler.
2. If no scheduler is available, the workflow enters a queued state.
3. Queue duration is bounded by the manifest's maximum queue timeout.
4. Queue overflow triggers a Resource error per `workflow-errors.md`.

## Scheduler Metrics

Schedulers are monitored for the following metrics:

| Metric | Description | Collection Point |
|--------|-------------|-----------------|
| Dispatch Latency | Time from node readiness to dispatch | Node boundary |
| Queue Depth | Number of pending nodes | Per scheduler |
| Utilization Efficiency | Ratio of productive to total time | Per resource pool |
| Fairness Index | Jain's fairness index across workflows | Per scheduler |
| Deadline Miss Rate | Fraction of missed deadlines | Per workflow |
| Preemption Rate | Fraction of preempted executions | Per scheduler |

Scheduler metrics are collected per `workflow-metrics.md` and exposed through the observability pillars defined in `workflow-observability.md`.
