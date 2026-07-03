# RFC-0321: Workflow Observability

# RFC-0321: Workflow Observability
'''
## Header
'''
```
RFC: RFC-0321
Title: Workflow Observability
Status: Proposed
Version: 1.0.0
Author: Atlas Specification Committee
Created: 2026-07-01
Depends On:
  - RFC-0001 Runtime Overview
  - RFC-0002 Runtime Lifecycle
  - RFC-0003 Runtime Service Model
  - RFC-0004 Runtime Scheduler
  - RFC-0005 Runtime Event Bus
  - RFC-0006 Runtime State Management
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1004 Common Contract Model
  - RFC-1005 Common Manifest Model
  - RFC-1006 Common Error Model
Supersedes: None
Superseded By: None
Category: Workflow
Layer: Standard
Normative: YES
Audience: All Subsystem Teams
ADR References:
  - ADR-0012
Constitution References:
  - Section 1 (Workflow Philosophy)
Related RFCs:
  - RFC-0301 Workflow Overview
  - RFC-0304 Workflow Runtime
  - RFC-0312 Scheduler
  - RFC-0315 Recovery
  - RFC-0316 Debugging
  - RFC-1001 Common Event Model
  - RFC-1002 Common State Model
  - RFC-1003 Common Capability Model
  - RFC-1006 Common Error Model
Target Release: 1.0.0
Review Cycle: Specification Committee
Compatibility: Compatible with Spec 1.x
Last Updated: 2026-07-01
Related ADR: ADR-0012
Related JSON Schema: workflow-observability.md
Related Catalog: workflow-observability.md
```
'''

## Abstract

This RFC defines the observability framework for Atlas Workflow, establishing standards for distributed tracing, metrics collection, audit logging, correlation identifiers, and telemetry export. The observability layer enables operators to monitor workflow execution health, diagnose failures, track performance, and maintain compliance records. All workflow subsystems MUST emit structured observability data according to this specification.

## Status

This is a Proposed specification. Implementation feedback is encouraged before final adoption.

## Motivation

Atlas Workflow executions span multiple logical and physical boundaries. Without standardized observability, operators cannot:

- Trace a single workflow execution across component boundaries
- Correlate logs, metrics, and traces for a given execution
- Detect performance regressions in scheduler, executor, or connector subsystems
- Maintain audit trails for regulatory compliance
- Debug production failures with sufficient context

Current ad-hoc logging approaches produce fragmented data that requires manual correlation. This RFC mandates a unified observability platform integrated into every workflow subsystem.

## Scope

This RFC covers:

- Distributed tracing with W3C Trace Context propagation
- Prometheus-compatible metrics with standardized naming conventions
- Structured audit logging for compliance and forensics
- Correlation ID propagation across all workflow boundaries
- Telemetry export pipelines with configurable backends
- Health check endpoints for workflow subsystems

This RFC does NOT cover:

- Alerting rule definitions (see RFC-0320 Performance)
- Log aggregation infrastructure (infrastructure concern)
- Dashboard configuration (operational concern)
- Custom metric definition beyond the baseline set

## Terminology

The following terms are defined per RFC-0301 (Workflow Overview) and extended for observability:

| Term | Definition |
| --- | --- |
| Trace | A tree of spans representing the end-to-end execution of a workflow invocation |
| Span | A timed operation within a trace, representing a single workflow step or subsystem interaction |
| Correlation ID | A UUIDv4 identifier that groups all observability data for a single workflow invocation |
| Event ID | A UUIDv4 identifier for a discrete workflow event (trigger, action, condition) |
| Audit Log | An immutable, append-only record of workflow state transitions and user actions |
| Telemetry | Observability data including traces, metrics, and logs emitted by workflow components |
| Instrumentation | Code that emits telemetry data, embedded within workflow subsystems |
| Collector | A process or library that aggregates telemetry from multiple sources |
| Exporter | A component that sends telemetry to a backend system |
| Sampling Rate | The fraction of traces recorded, expressed as a decimal between 0.0 and 1.0 |
| Service Name | The logical name of a workflow component as reported to the tracing system |
| Resource Attributes | Key-value pairs describing the telemetry source (e.g., node ID, version) |
| Span Attributes | Key-value pairs describing a specific operation within a trace |
| Metric Type | The category of metric: counter, gauge, histogram, or summary |
| Observation Window | The time interval over which metrics are aggregated |

## Requirements

### Requirement 1: Distributed Tracing

The implementation MUST implement distributed tracing following the OpenTelemetry specification.

The implementation MUST:

- Assign a unique trace ID (UUIDv6 or equivalent monotonic format) to each workflow invocation
- Create a root span for each workflow execution with the workflow ID as the span name
- Create child spans for each workflow step, including trigger evaluation, condition checks, action execution, and connector interactions
- Propagate trace context using W3C Trace Context headers (traceparent, tracestate) across all inter-component boundaries
- Record span events for significant state transitions (started, completed, failed, retried, skipped)
- Set span status to Ok, Error, or Unset based on execution outcome
- Include workflow ID, step ID, and correlation ID as span attributes on every span
- Support trace sampling with configurable rates per subsystem
- Export traces to at least one backend (OpenTelemetry Protocol, Jaeger, or Zipkin)

The implementation SHOULD:

- Provide automatic instrumentation for common workflow patterns (sequential, parallel, fan-in, fan-out)
- Support manual instrumentation hooks for third-party nodes and actions
- Include exception details (stack trace, error code, error message) as span attributes on error spans

The implementation MAY:

- Support trace tail-sampling for cost-optimized production deployments
- Provide trace visualization within the Atlas Workflow UI
- Allow operators to configure custom span processors

#### Trace Propagation Model

`mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Scheduler
    participant Executor
    participant Connector
    participant Backend

    Client->>Gateway: WorkflowInvocation {trace_id, correlation_id}
    Gateway->>Scheduler: CreateExecution {trace_id, correlation_id}
    Scheduler->>Executor: DispatchStep {trace_id, step_id}
    Executor->>Connector: ExecuteAction {trace_id, step_id}
    Connector-->>Executor: ActionResult {trace_id, status}
    Executor-->>Scheduler: StepComplete {trace_id, step_id, status}
    Scheduler-->>Gateway: ExecutionUpdated {trace_id, status}
    Gateway-->>Backend: ExportTrace {trace_data}
`

### Requirement 2: Metrics Collection

The implementation MUST provide Prometheus-compatible metrics for all workflow subsystems.

The implementation MUST:

- Export metrics in Prometheus exposition format on a dedicated HTTP endpoint (/metrics)
- Use the Atlas Workflow metric naming convention: workflow_<component>_<metric>_<type>
- Include the following baseline counters:
  - workflow_execution_total — total workflow invocations (labels: workflow_id, status)
  - workflow_step_total — total step executions (labels: step_type, status, retry_count)
  - workflow_duration_seconds — histogram of end-to-end execution durations
  - workflow_step_duration_seconds — histogram of individual step durations
  - workflow_error_total — total errors (labels: error_code, component, severity)
  - workflow_queue_depth — current queue depth per workflow type
  - workflow_retry_total — total retry attempts (labels: step_type, reason)
  - workflow_connector_call_total — connector invocations (labels: connector_name, status)
  - workflow_trigger_fired_total — trigger evaluations (labels: trigger_type, result)
- Include the following baseline gauges:
  - workflow_active_executions — currently running executions (labels: workflow_id)
  - workflow_pending_steps — steps awaiting execution (labels: queue_name)
  - workflow_resource_usage — resource utilization (labels: resource_type, node_id)
  - workflow_health_status — component health (labels: component, status)
- Include the following baseline histograms:
  - workflow_latency_seconds — end-to-end execution latency
  - workflow_step_latency_seconds — individual step latency
  - workflow_connector_latency_seconds — connector call latency
- Attach resource attributes to every metric: service_name, service_version, environment, cluster_id, node_id
- Support metric aggregation over configurable observation windows (1m, 5m, 15m, 1h, 24h)
- Implement metric cardinality limits to prevent unbounded label growth (default: 1000 unique series per metric)

The implementation SHOULD:

- Provide recording rules for common aggregations (p50, p95, p99 latencies)
- Support custom metric registration via the extension API
- Export metrics in OpenTelemetry Metrics format alongside Prometheus format

The implementation MAY:

- Provide metric alerting thresholds as configuration
- Support metric deduplication across redundant exporters

#### Metrics Architecture

`mermaid
graph TB
    subgraph Workflow Components
        S[Scheduler]
        E[Executor]
        C[Connectors]
        T[Triggers]
    end

    subgraph Telemetry Pipeline
        I[Instrumentation]
        CP[Collector]
        EP[Exporter]
        PM[Prometheus]
        OTel[OpenTelemetry]
    end

    S --> I
    E --> I
    C --> I
    T --> I
    I --> CP
    CP --> EP
    EP --> PM
    EP --> OTel
`

### Requirement 3: Audit Logging

The implementation MUST provide structured audit logging for compliance and forensic analysis.

The implementation MUST:

- Log all workflow lifecycle events: created, started, paused, resumed, completed, failed, cancelled, expired
- Log all step lifecycle events: enqueued, dispatched, started, completed, failed, retried, skipped, timed_out
- Log all state transitions with before/after values and transition reason
- Log all user-initiated actions: workflow creation, modification, cancellation, manual step intervention
- Log all permission checks: access granted, access denied, role, resource
- Use structured JSON format with the following required fields:
  - timestamp (ISO 8601 with timezone)
  - event_id (UUIDv4)
  - correlation_id (UUIDv4)
  - trace_id (from distributed trace)
  - event_type (one of the enumerated types above)
  - component (source subsystem)
  - severity (INFO, WARN, ERROR, CRITICAL)
  - workflow_id (if applicable)
  - step_id (if applicable)
  - actor (user or system identity)
  - resource (affected resource identifier)
  - metadata (key-value pairs for additional context)
- Write audit logs to an append-only store with tamper-evident sequencing (monotonically increasing sequence number)
- Support audit log export in JSON Lines format for downstream processing
- Retain audit logs for a configurable minimum period (default: 90 days)

The implementation SHOULD:

- Support audit log signing using cryptographic hashes (SHA-256 chain)
- Provide audit log query API with filters by correlation_id, workflow_id, time_range, event_type
- Redact sensitive data (PII, credentials) from audit log output

The implementation MAY:

- Integrate with external SIEM systems via syslog or HTTP push
- Support audit log retention policies based on regulatory requirements

### Requirement 4: Correlation ID Propagation

The implementation MUST propagate correlation identifiers across all workflow boundaries.

The implementation MUST:

- Assign a correlation_id (UUIDv4) at workflow invocation entry point
- Include correlation_id in all internal messages, API calls, and database queries
- Include correlation_id in all telemetry data (traces, metrics labels, log records)
- Support incoming correlation_id from client requests (preserving client-assigned IDs)
- Generate child correlation IDs for sub-workflow invocations while maintaining parent linkage
- Ensure correlation_id is present in all error responses and stack traces

The implementation SHOULD:

- Provide correlation_id context propagation through async boundaries
- Support correlation_id extraction from multiple sources (header, payload, metadata)

The implementation MAY:

- Support hierarchical correlation ID trees for nested workflow invocations

### Requirement 5: Telemetry Export

The implementation MUST provide configurable telemetry export pipelines.

The implementation MUST:

- Support at least one trace exporter: OpenTelemetry Protocol (OTLP), Jaeger, or Zipkin
- Support at least one metrics exporter: Prometheus, OpenTelemetry Protocol (OTLP), or StatsD
- Support at least one log exporter: stdout, file, OpenTelemetry Protocol (OTLP), or syslog
- Configure export endpoints via configuration file or environment variables
- Implement exponential backoff with jitter for failed export connections
- Buffer telemetry data locally (in-memory or disk-backed) during network partitions
- Drop oldest buffered data when buffers reach capacity (configurable, default: 10000 items)
- Report exporter health status as a gauge metric

The implementation SHOULD:

- Support multiple simultaneous exporters per telemetry type
- Allow per-telemetry-type export configuration (different backends for traces vs metrics)
- Provide a dry-run mode that validates exporter configuration without sending data

The implementation MAY:

- Support custom exporter plugins via the extension API
- Implement telemetry data enrichment before export (adding resource attributes, enriching with metadata)

### Requirement 6: Health Checks

The implementation MUST expose health check endpoints for all workflow subsystems.

The implementation MUST:

- Expose readiness probe endpoint (/health/ready) returning HTTP 200 when the component can accept new workflow invocations
- Expose liveness probe endpoint (/health/live) returning HTTP 200 when the component is operational
- Return component version, uptime, and dependency status in health check responses
- Report degraded state when downstream dependencies are unavailable (database, message queue, external services)
- Include dependency health in readiness probe response (labels: database, queue, cache, external_api)

The implementation SHOULD:

- Support startup probe endpoint (/health/startup) for Kubernetes-style startup probes
- Provide detailed health information via /health/detail endpoint

## Layer Boundaries

### Observability Layer Responsibilities

- Emit structured telemetry (traces, metrics, logs) from all workflow components
- Manage telemetry export pipelines and backend connectivity
- Maintain correlation ID context throughout workflow lifecycles
- Enforce audit log immutability and tamper-evidence
- Provide health check endpoints for all subsystems
- Implement metric cardinality limits and sampling controls

### Observability Layer Non-Responsibilities

- Alerting rule definition and notification dispatch (operational concern)
- Log aggregation infrastructure provisioning (infrastructure concern)
- Dashboard configuration and visualization (operational concern)
- Telemetry backend deployment and maintenance (infrastructure concern)
- Custom metric definition beyond the baseline set (extension concern)

### Dependencies

- Depends on: RFC-0304 (Workflow Runtime), RFC-0312 (Scheduler), RFC-0315 (Recovery), RFC-0316 (Debugging)
- Depends on: RFC-1001 (Common Event Model), RFC-1002 (Common State Model)
- Provides to: RFC-0322 (Extension Points), RFC-0323 (Plugin Integration)
- Consumers: Operations team, SRE team, Compliance auditor
- Providers: Observability SDK, OpenTelemetry collector

### Forbidden Dependencies

- The observability layer MUST NOT depend on the UI layer
- The observability layer MUST NOT depend on the storage layer directly (use runtime abstractions)
- The observability layer MUST NOT assume any specific telemetry backend implementation
- The observability layer MUST NOT block workflow execution on telemetry export failures

## Future Evolution

- **v1.1**: Add support for distributed sampling strategies (adaptive, tail-based)
- **v1.2**: Introduce synthetic monitoring endpoints for workflow health validation
- **v1.3**: Add ML-driven anomaly detection on workflow metrics
- **v2.0**: Support for multi-tenant observability with namespace-isolated telemetry
- **v2.0**: Native integration with workflow AI subsystem (RFC-0325) for observability-enhanced debugging

## Runtime Independence

This specification is runtime-independent. The observability framework MUST NOT assume:

- Any specific programming language (Rust, Node.js, Go, Python)
- Any specific runtime environment (Electron, Tauri, browser, server)
- Any specific database backend (SQLite, PostgreSQL, Redis)
- Any specific operating system (Windows, Linux, macOS)
- Any specific GPU or graphics acceleration
- Any specific threading model (goroutines, fibers, async/await, threads)

All observability data MUST be transportable across runtime boundaries via standard protocols (OTLP, Prometheus HTTP, JSON over HTTP).


#### Correlation ID Propagation Model

`mermaid
graph LR
    A[Client Request] -->|correlation_id=C1| B[API Gateway]
    B -->|correlation_id=C1| C[Scheduler]
    C -->|correlation_id=C1, step_id=S1| D[Executor]
    D -->|correlation_id=C1, step_id=S1| E[Connector]
    E -->|correlation_id=C1, step_id=S1| D
    D -->|correlation_id=C1, step_id=S2| F[Action Node]
    F -->|correlation_id=C1, step_id=S2| D
    D -->|correlation_id=C1| C
    C -->|correlation_id=C1| B
    B -->|correlation_id=C1| G[Telemetry Exporter]
    G --> H[Trace Backend]
    G --> I[Metrics Backend]
    G --> J[Audit Log Backend]

`

#### Telemetry Pipeline Architecture

`mermaid
graph TB
    subgraph Sources
        SC[Scheduler]
        EX[Executor]
        CT[Connectors]
        TR[Triggers]
        CN[Conditions]
    end

    subgraph Instrumentation
        TI[Trace Instrumentation]
        MI[Metric Instrumentation]
        LI[Log Instrumentation]
    end

    subgraph Processing
        SP[Span Processor]
        MP[Metric Processor]
        LP[Log Processor]
        SR[Sampling Router]
    end

    subgraph Exporters
        TE[Trace Exporter OTLP]
        ME[Metrics Exporter HTTP]
        LE[Log Exporter Stdout]
    end

    subgraph Backends
        TB[Jaeger/Zipkin]
        PB[Prometheus]
        AB[Audit Store]
    end

    SC --> TI
    EX --> TI
    CT --> TI
    TR --> TI
    CN --> TI
    TI --> SP
    SP --> SR
    SR --> TE
    TE --> TB

    SC --> MI
    EX --> MI
    CT --> MI
    TR --> MI
    CN --> MI
    MI --> MP
    MP --> ME
    ME --> PB

    SC --> LI
    EX --> LI
    CT --> LI
    TR --> LI
    CN --> LI
    LI --> LP
    LP --> LE
    LE --> AB

`
## Acceptance Criteria

1. The implementation MUST emit a complete trace for every workflow execution, from trigger to completion.
2. The implementation MUST export all baseline metrics defined in Requirement 2 in Prometheus exposition format.
3. The implementation MUST write an audit log entry for every workflow lifecycle state transition.
4. The implementation MUST propagate the correlation ID through all subsystem boundaries without loss.
5. The implementation MUST support at least one trace exporter, one metrics exporter, and one log exporter.
6. The implementation MUST expose /health/ready and /health/live endpoints on every workflow component.
7. The implementation MUST NOT block workflow execution on telemetry export failure.
8. The implementation MUST enforce metric cardinality limits to prevent unbounded series growth.
9. The implementation MUST include trace_id, correlation_id, and workflow_id in every audit log entry.
10. The implementation MUST support configurable sampling rates per subsystem.

## References

| Type | Reference | Description |
| --- | --- | --- |
| Related RFC | RFC-0301 | Workflow Overview (Terminology source) |
| Related RFC | RFC-0304 | Workflow Runtime |
| Related RFC | RFC-0312 | Scheduler |
| Related RFC | RFC-0315 | Recovery |
| Related RFC | RFC-0316 | Debugging |
| Related RFC | RFC-0320 | Performance |
| Related RFC | RFC-1001 | Common Event Model |
| Related RFC | RFC-1002 | Common State Model |
| Related ADR | ADR-0012 | Observability Architecture Decision |
| Related JSON Schema | workflow-observability.md | Observability configuration schema |
| Related Catalog | workflow-observability.md | Catalog entry for observability components |
| See Also | OpenTelemetry Spec | https://opentelemetry.io/docs/specs/otel |
| See Also | W3C Trace Context | https://www.w3.org/TR/trace-context/ |
| See Also | Prometheus Exposition | https://prometheus.io/docs/instrumenting/exposition_formats/ |
