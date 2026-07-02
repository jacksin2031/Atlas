RFC: RFC-0321
Title: Workflow Observability
Status: Proposed
Version: 1.1.0
Author: Atlas Specification Committee
Created: 2026-07-01
Updated: 2026-07-01
ADR References:
  - ADR-0012 Contract-First Specification-Driven Development`nRelated ADR:`n  - ADR-0012
Related JSON Schema:
  - schemas/workflow/performance-metric.json
  - schemas/workflow/sla-definition.json
Related Catalog:
  - catalog/workflow-metrics.md
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01

---

---

---

## Authority

This RFC is the authoritative specification for the RFC 0321 workflow observability.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.



This RFC is the authoritative specification for the RFC 0321 workflow observability.

Any implementation MUST conform to this document.

If an implementation conflicts with this RFC, this RFC takes precedence.

Conflicts between RFCs SHALL be resolved through the ADR process.


## Normative Status
This specification is normative. Every implementation MUST conform to the requirements defined herein.

---

## 1 Terminology

| Term | Definition | Source |
|---|---|---|
| Tracing | The recording of execution flow through a workflow as a sequence of correlated spans. | RFC-0321 |
| Metric | A quantitative measurement of workflow performance or state. | RFC-0321 |
| Audit Log | An immutable record of security-relevant workflow events. | RFC-0321 |
| Correlation ID | A unique identifier linking related events across workflow execution. | RFC-0321 |
| Telemetry | The automated measurement and reporting of workflow system data. | RFC-0321 |
| Span | A single unit of work within a trace, having a start time and duration. | RFC-0321 |
| Trace | A complete record of a workflow execution's path through the graph. | RFC-0321 |
| Counter | A cumulative metric type (e.g., total nodes executed). | RFC-0321 |
| Gauge | A point-in-time metric type (e.g., current memory usage). | RFC-0321 |
| Histogram | A distribution metric type (e.g., node execution latency distribution). | RFC-0321 |

## 2 Layer Boundaries

## 3 Security
- Audit logs MUST be tamper-evident per RFC-0319.
- Telemetry data MUST NOT contain secrets or sensitive information.
- Correlation IDs MUST NOT leak identifying information.

## 4 Performance
- Trace span recording MUST add less than 100 microseconds per span.
- Metric aggregation MUST complete within 1 second.
- Audit log writes MUST be asynchronous with less than 10ms latency.

## 5 Compatibility
- Telemetry data formats MUST be backward compatible within a major version.
- New metric types MAY be added without breaking existing consumers.

## 6 Compliance
- All observability data MUST be exportable for regulatory compliance per RFC-0330.
- Audit logs MUST meet retention requirements defined by organizational policy.

## 7 Future Evolution
- **Distributed Tracing**: Cross-cluster trace propagation for distributed workflows.
- **AI-Assisted Anomaly Detection**: ML-based detection of unusual workflow execution patterns.
- **Real-Time Alerting**: Automated alerting based on telemetry thresholds.
- **OpenTelemetry Integration**: Native support for OpenTelemetry protocol (OTLP).
- **Trace-Based Testing**: Using production traces for automated testing.

## 8 Runtime Independence
This specification is completely independent of any runtime implementation platform. Specifically, this specification MUST NOT assume:
- Any programming language (a systems programming language, Node.js, a typed programming language, Go, Python, etc.)
- Any runtime environment (a desktop application framework, a desktop application framework, Browser, Desktop, Server)
- Any storage backend (an embedded database engine, a relational database, a document database, an in-memory data store, etc.)
- Any operating system (Windows, Linux, macOS, etc.)
- Any hardware architecture (CPU, GPU, FPGA, etc.)
- Any threading model (single-threaded, multi-threaded, actor-based, etc.)

## 9 References

| Reference | Description |
|---|---|
| RFC-0301 | Workflow Overview (canonical terminology source) |
| RFC-0303 | Workflow Execution (execution telemetry) |
| RFC-0304 | Workflow Runtime (runtime observability) |
| RFC-0314 | Workflow Error Handling (error telemetry) |
| RFC-0315 | Workflow Recovery (recovery telemetry) |`n| RFC-0312 | Workflow Scheduler (scheduler telemetry)
| RFC-0316 | Workflow Debugging (debug telemetry) |
| RFC-0319 | Workflow Security (security telemetry) |
| RFC-0320 | Workflow Performance (performance telemetry) |
| RFC-0324 | Workflow Storage (audit log persistence) |
| RFC-0330 | Workflow Compliance (compliance reporting) |
| ADR-0012 | Contract-First Specification-Driven Development |
| schemas/workflow/trace.json | Trace JSON Schema |
| schemas/workflow/metric.json | Metric JSON Schema |
| schemas/workflow/audit-log.json | Audit Log JSON Schema |
| catalog/workflow-metrics.md | Metrics Catalog |
| catalog/workflow-observability.md | Observability Catalog |
| Glossary | Atlas Master Glossary |
| Constitution | Atlas AI Constitution |
| See Also | RFC-0321 (this document), RFC-0319 (Security), RFC-0330 (Compliance) |
---


## 10 Architecture

This section defines the architectural model for workflow observability.

### 10.1 Observability Pipeline

The observability pipeline consists of four stages:

1. **Instrumentation**: Every workflow component emits telemetry data at defined boundaries. Instrumentation points are specified in Section 10.2.
2. **Collection**: Telemetry data is collected through the telemetry pipeline. Collection occurs asynchronously to minimize execution impact.
3. **Aggregation**: Raw telemetry is aggregated into metrics, traces, and audit logs. Aggregation rules are defined per data type.
4. **Export**: Aggregated data is exported through standardized interfaces for consumption by monitoring systems.

### 10.2 Instrumentation Points

Every workflow component MUST instrument at the following boundaries:

| Component | Instrumentation Point | Data Type | Severity |
|---|---|---|---|
| Workflow Engine | Execution start/end | Trace | Info |
| Scheduler | Task scheduling decision | Metric | Info |
| Node Executor | Node enter/exit | Trace | Info |
| Condition Evaluator | Condition evaluation result | Metric | Debug |
| Action Executor | Action invoke/result/error | Trace | Warning/Error |
| Trigger Handler | Trigger fired/consumed | Event | Info |
| Error Handler | Error caught/recovered | Event | Error |
| Recovery Manager | Recovery initiated/completed | Event | Warning |
| Context Manager | Context mutation | Event | Debug |
| Runtime | Health check result | Metric | Info |

### 10.3 Trace Model

Every workflow execution MUST produce a trace composed of spans. Each span has:

- 	race_id: Unique identifier for the entire execution trace (UUID v7).
- span_id: Unique identifier for this span (64-bit random).
- parent_span_id: Identifier of the parent span, null for root span.
- operation_name: Semantic name of the operation (e.g., workflow.start, 
ode.execute, ction.invoke).
- 	imestamp_ns: Nanosecond-precision start timestamp.
- duration_ns: Nanosecond-precision duration, zero for event-only spans.
- status: Span status from {Ok, Error, Cancelled, Unknown}.
- ttributes: Key-value pairs describing the span context.
- events: Named events within the span with timestamps.
- links: References to related spans from other traces.

The trace model MUST support hierarchical nesting, distributed propagation, and sampling.

### 10.4 Metrics Taxonomy

All workflow observability metrics MUST conform to one of four metric types:

| Type | Semantics | Example | Cardinality |
|---|---|---|---|
| Counter | Monotonically increasing cumulative value | workflow_nodes_executed_total | Low |
| Gauge | Point-in-time value that may increase or decrease | workflow_active_count | Medium |
| Histogram | Distribution of observed values with configurable buckets | workflow_node_duration_seconds | Medium |
| Summary | Pre-calculated quantiles over a sliding window | workflow_execution_latency_p99 | High |

Every metric MUST include the following standard labels: workflow_id, execution_id, ersion, environment.

### 10.5 Audit Log Model

The audit log MUST record every security-relevant event in an append-only, tamper-evident fashion.

| Field | Type | Required | Description |
|---|---|---|---|
| event_id | UUID v7 | Yes | Unique event identifier |
| timestamp_ns | uint64 | Yes | Event occurrence time |
| actor_id | string | Yes | Identity of the actor |
| action | enum | Yes | Operation performed |
| resource_type | string | Yes | Type of resource affected |
| resource_id | string | Yes | Identifier of resource |
| outcome | enum | Yes | Success or failure |
| correlation_id | string | Yes | Workflow execution correlation |
| metadata | object | No | Event-specific context |

Valid action values: {workflow_created, workflow_started, workflow_completed, workflow_failed, workflow_cancelled, node_executed, node_skipped, node_retried, checkpoint_created, checkpoint_restored, secret_accessed, permission_changed, plugin_loaded, plugin_unloaded}.

Valid outcome values: {success, failure, denied}.

### 10.6 Correlation ID Propagation

Correlation IDs MUST propagate through every layer of the workflow execution stack.

- The root correlation ID is assigned at workflow creation and is immutable.
- Child correlation IDs MAY be generated for sub-workflow executions.
- Every span, metric, audit log entry, and debug event MUST include the full correlation chain.
- Correlation ID chains MUST be bounded to a maximum depth of 128 to prevent unbounded growth.

### 10.7 Sampling Strategy

To control telemetry volume, implementations MUST support the following sampling modes:

| Mode | Behavior | Use Case |
|---|---|---|
| Always sample | Every event is recorded | Development, debugging |
| Rate limited | Fixed percentage of events sampled | Production default |
| Adaptive | Sample rate adjusts based on system load | High-throughput production |
| Tail-based | Full traces collected for error cases | Post-mortem analysis |

Sampling decisions MUST be made at the trace root and propagated to all child spans.

### 10.8 Telemetry Data Retention

| Data Type | Minimum Retention | Archival |
|---|---|---|
| Traces (full) | 7 days | Export to cold storage |
| Traces (sampled) | 30 days | Export to cold storage |
| Metrics | 90 days | Aggregated rollups retained indefinitely |
| Audit logs | 1 year (minimum) | Immutable, tamper-evident storage |
| Debug events | 24 hours | Volatile, not persisted by default |

Retention periods are organizational policy defaults; implementations MUST support configurable retention per data type.

## 11 Acceptance Criteria

### 11.1 Trace Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-01 | Every workflow execution MUST produce a trace with a root span containing trace_id, span_id, and operation_name. | Execution trace test: Start workflow → Capture trace output → Verify root span contains all required fields with valid UUID format |
| AC-02 | Running the same workflow twice with identical inputs MUST produce traces with identical span structure (same operations, same hierarchy). | Determinism test: Execute workflow twice with same inputs → Compare span operation names and parent-child relationships → Verify structural identity |
| AC-03 | Every span MUST have a status field with a value from {Ok, Error, Cancelled, Unknown}. | Status enumeration test: Trigger all span outcomes → Verify each span status maps to one of four enumerated values |
| AC-04 | Correlation ID chains MUST NOT exceed 128 levels. | Depth test: Create nested workflow chain of 129 levels → Verify deepest correlation ID is rejected or truncated at 128 |

### 11.2 Metrics Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-05 | All four metric types (Counter, Gauge, Histogram, Summary) MUST be supported. | Type enumeration test: Register one metric of each type → Verify each type produces correctly formatted telemetry output |
| AC-06 | Every metric MUST include standard labels: workflow_id, execution_id, version, environment. | Label presence test: Emit any metric → Verify all four standard labels present in every data point |
| AC-07 | Histogram bucket boundaries MUST be configurable and default to {0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0}. | Bucket verification test: Emit histogram without custom buckets → Verify default bucket boundaries present in output |

### 11.3 Audit Log Compliance

| # | Criterion | Verification Method |
|---|---|---|
| AC-08 | Every security-relevant event MUST produce an audit log entry with all nine required fields. | Audit completeness test: Perform all ten valid actions → Verify each produces audit entry with event_id, timestamp_ns, actor_id, action, resource_type, resource_id, outcome, correlation_id, metadata |
| AC-09 | Audit log entries MUST be append-only; no entry MAY be modified or deleted after creation. | Immutability test: Attempt to modify audit entry → Verify modification rejected; attempt to delete → Verify deletion rejected |
| AC-10 | Audit log entries MUST include a tamper-evident checksum or hash chain. | Tamper test: Alter any byte in audit log → Verify tamper detection triggers |

### 11.4 Sampling and Retention

| # | Criterion | Verification Method |
|---|---|---|
| AC-11 | All four sampling modes (Always, Rate Limited, Adaptive, Tail-based) MUST be selectable. | Mode enumeration test: Configure each mode → Verify telemetry volume matches expected behavior for that mode |
| AC-12 | Tail-based sampling MUST capture full traces for all error-status spans. | Error trace test: Inject error into workflow → Verify full trace (not sampled) captured despite rate-limiting mode |
| AC-13 | Data retention MUST be configurable per data type with minimum values enforced. | Retention test: Set retention below minimum for each type → Verify system enforces minimum; set above → Verify custom retention honored |## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |
| 1.1.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Enterprise specification upgrade: added Authority, Terminology, Layer Boundaries, Runtime Independence, Future Evolution, Compliance Matrix, and verifiable Acceptance Criteria |


## Compliance Matrix

| Category | Value |
|---|---|
| Related RFC | See References section |
| Related ADR | ADR-0010, ADR-0012 |
| Related JSON Schema | N/A |
| Related Catalog | N/A |


## Revision History

| Version | Status | Date | Author | Notes |
|---|---|---|---|---|
| 1.0.0 | Proposed | 2026-07-01 | Atlas Specification Committee | Initial publication |