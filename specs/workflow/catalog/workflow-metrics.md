---
title: Workflow Metrics Entity Reference
category: Workflow
layer: Core
normative: YES
version: 1.0.0
lastUpdated: 2026-07-01
---

# Workflow Metrics Entity Reference

## Overview

This document defines the metric entity reference for the Atlas Development System (ADS) workflow engine. Metrics provide quantitative measurements of workflow performance, resource utilization, and operational health. The metric model supports real-time monitoring, historical analysis, and capacity planning.

Metrics MUST be treated as append-only time-series data. Once recorded, metric values MUST NOT be modified. Metric aggregation and derivation MUST be recomputed from the underlying data.

## Six Performance Metrics

The workflow engine defines six core performance metrics. Each metric measures a distinct dimension of workflow execution.

| Metric | Unit | Collection Granularity | Aggregation Method |
|--------|------|----------------------|-------------------|
| Latency | Milliseconds | Per action, per node, per workflow | Mean, p50, p95, p99, max |
| Throughput | Operations per second | Per node, per workflow | Sum, mean, rate |
| Resource Utilization | Percentage | Per resource pool, per node | Mean, max, percentile |
| Memory Footprint | Megabytes | Per action, per node | Peak, mean, current |
| CPU Usage | Percentage | Per node, per resource pool | Mean, max, utilization factor |
| Network Bandwidth | Megabits per second | Per edge, per workflow | Mean, peak, total transferred |

### Latency

Latency measures the elapsed time between the initiation and completion of an operation.

| Dimension | Definition | Calculation |
|-----------|------------|-------------|
| Action Latency | Time from action start to action completion | `completed_at - started_at` |
| Node Latency | Time from node entry to node exit | `node_exit_time - node_entry_time` |
| Workflow Latency | Time from workflow start to workflow completion | `workflow_end - workflow_start` |
| Queue Latency | Time from node readiness to node execution | `execution_start - readiness_time` |
| Wait Latency | Time spent in Waiting state | `waiting_duration` per state entry |

Latency distributions are tracked using histogram buckets. Bucket boundaries are configurable but MUST include the following defaults:

| Bucket | Boundary |
|--------|----------|
| t1 | 1 ms |
| t2 | 10 ms |
| t3 | 100 ms |
| t4 | 1 s |
| t5 | 10 s |
| t6 | 60 s |
| t7 | 300 s |
| t8 | 1800 s |
| t9 | 3600 s |
| t10 | Overflow |

### Throughput

Throughput measures the rate of completed operations within a time window.

| Dimension | Definition | Calculation |
|-----------|------------|-------------|
| Action Throughput | Actions completed per second | `completed_actions / time_window` |
| Node Throughput | Operations processed by a node per second | `node_operations / time_window` |
| Workflow Throughput | Workflows completed per second | `completed_workflows / time_window` |
| Edge Throughput | Traversals per second across an edge | `edge_traversals / time_window` |

Throughput is reported as a rate (operations per second) and as a cumulative count over the measurement window.

### Resource Utilization

Resource utilization measures the fraction of available capacity that is consumed.

| Resource Type | Utilization Formula | Measurement Source |
|--------------|-------------------|-------------------|
| CPU | `used_cycles / total_cycles` | CPU metric |
| Memory | `used_bytes / total_bytes` | Memory metric |
| Disk | `used_blocks / total_blocks` | Disk metric |
| Network | `transferred_bytes / capacity_bytes` | Network metric |
| GPU | `utilized_cores / total_cores` | GPU metric |

Utilization is reported as a percentage (0.0 to 100.0) with configurable precision.

### Memory Footprint

Memory footprint measures the amount of memory consumed by workflow components.

| Component | Measurement | Scope |
|-----------|------------|-------|
| Action | Peak memory during execution | Per action |
| Node | Peak memory during node lifetime | Per node |
| Workflow | Total memory across all active nodes | Per workflow |
| Engine | Total memory including overhead | Global |

Memory footprint includes application heap, stack, buffer pools, and serialized state. Garbage-collected memory that is reclaimed within the measurement window IS excluded from the footprint.

### CPU Usage

CPU usage measures the processor time consumed by workflow components.

| Component | Measurement | Scope |
|-----------|------------|-------|
| Action | CPU cycles consumed during execution | Per action |
| Node | CPU cycles consumed during node lifetime | Per node |
| Workflow | Aggregate CPU across all nodes | Per workflow |
| Scheduling | CPU cycles spent in scheduler logic | Global |

CPU usage is reported as a percentage of available processor time and as absolute cycle counts.

### Network Bandwidth

Network bandwidth measures data transfer rates across workflow edges and external connections.

| Dimension | Measurement | Scope |
|-----------|------------|-------|
| Ingress | Bytes received per second | Per edge |
| Egress | Bytes sent per second | Per edge |
| Total | Combined ingress and egress | Per workflow |
| Overhead | Protocol and metadata bytes | Per connection |

Bandwidth includes both application data and protocol overhead. Compression ratios are tracked separately.

## Metric Collection Rules

Metrics are collected according to the following rules:

### Collection Triggers

| Trigger | Metric Affected | Collection Method |
|---------|----------------|------------------|
| Action start | Latency (counter), CPU (counter) | Instrumentation at entry |
| Action end | Latency (histogram), Throughput (counter) | Instrumentation at exit |
| Periodic tick | Resource Utilization, Memory, CPU | Polling at configured interval |
| State transition | Latency (wait time), Throughput | Event-driven |
| Resource allocation | Resource Utilization, Memory | Allocation callback |

### Collection Intervals

| Metric | Default Interval | Configurable |
|--------|-----------------|--------------|
| Latency | Per operation | NO (event-driven) |
| Throughput | Per operation | NO (event-driven) |
| Resource Utilization | 1 second | YES |
| Memory Footprint | 5 seconds | YES |
| CPU Usage | 1 second | YES |
| Network Bandwidth | 1 second | YES |

### Collection Points

Metrics are collected at four points in the workflow graph:

1. **Action level**: Fine-grained metrics for individual actions.
2. **Node level**: Aggregated metrics for all actions within a node.
3. **Workflow level**: Aggregate metrics for the entire workflow execution.
4. **Engine level**: Global metrics across all workflows.

## Metric Aggregation Methods

Metrics are aggregated using the following mathematical methods:

| Method | Description | Use Case |
|--------|-------------|----------|
| Mean | Arithmetic average | Overall performance trends |
| Median (p50) | 50th percentile | Typical experience |
| p95 | 95th percentile | Tail latency analysis |
| p99 | 99th percentile | Extreme tail analysis |
| Max | Maximum observed value | Peak load assessment |
| Min | Minimum observed value | Best-case analysis |
| Sum | Total accumulated value | Capacity planning |
| Count | Number of observations | Volume measurement |
| Rate | Change per time unit | Trend detection |
| Histogram | Distribution bucket counts | Latency profiling |

### Aggregation Windows

| Window | Duration | Purpose |
|--------|----------|---------|
| Real-time | Current interval | Live monitoring |
| Short-term | 5 minutes | Recent trend analysis |
| Medium-term | 1 hour | Shift-level analysis |
| Long-term | 24 hours | Daily pattern analysis |
| Extended | 30 days | Monthly trend analysis |

## Metric Retention Policies

Metric data is retained according to configurable policies that balance storage cost against analytical needs.

| Retention Tier | Duration | Granularity | Storage Location |
|---------------|----------|------------|-----------------|
| Hot | 24 hours | Per-operation | In-memory cache |
| Warm | 7 days | Per-second | Fast disk storage |
| Cold | 90 days | Per-minute | Compressed disk storage |
| Archive | 1 year | Per-hour | Object storage |
| Deep Archive | 7 years | Per-day | Tape or cold storage |

### Retention Rules

1. Metrics transition between tiers automatically based on age.
2. Aggregated metrics at coarser granularity replace raw metrics upon tier transition.
3. Deep archive metrics are immutable and require explicit restoration for access.
4. Retention policies are configured per metric dimension and MAY vary by workflow type.

### Data Downsampling

When transitioning from hot to warm tier, metrics are downsampled:

| Source Metric | Downsampled Metric | Method |
|--------------|-------------------|--------|
| Per-operation latency | Per-second mean, max, min | Statistical aggregation |
| Per-operation throughput | Per-minute sum | Cumulative aggregation |
| Per-second utilization | Per-minute mean, max | Statistical aggregation |
| Per-second memory | Per-minute mean, peak | Statistical aggregation |
| Per-second CPU | Per-minute mean, max | Statistical aggregation |
| Per-second bandwidth | Per-minute mean, peak | Statistical aggregation |

## Metric Alerts

Metrics support threshold-based alerting integrated with the observability pillars defined in `workflow-observability.md`.

| Alert Dimension | Configuration | Description |
|----------------|--------------|-------------|
| Threshold | Numeric value | Alert when metric crosses this value |
| Duration | Time window | Alert only if threshold is breached for this duration |
| Severity | Enum | Alert severity level |
| Notification | EntityReference | Target for alert delivery |
| Cooldown | Duration | Minimum time between repeated alerts |

## Metric API Contracts

Metrics are accessible through standardized interfaces:

| Interface | Method | Description |
|-----------|--------|-------------|
| Query | GET /metrics | Retrieve metric values with filters |
| Subscribe | WS /metrics/stream | Real-time metric stream |
| Aggregate | POST /metrics/aggregate | Compute aggregated metrics |
| Export | GET /metrics/export | Export metrics in canonical format |
| Configure | PUT /metrics/config | Update retention and collection policies |

Query parameters support filtering by workflow ID, node ID, metric name, time range, and aggregation method.
