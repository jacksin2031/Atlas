# Atlas Vision Runtime

## Purpose

Platform-independent Vision Runtime reference implementation providing frame acquisition,
computer vision pipelines, provider abstraction, and deterministic execution.

## Ownership

Vision team

## Dependencies

- packages/common (shared types)

## Related RFCs

- RFC-0001 Runtime Overview
- RFC-0003 Runtime Service Model
- RFC-0004 Runtime Scheduler
- RFC-0005 Runtime Event Bus
- RFC-0007 Runtime IPC Architecture
- RFC-0008 Runtime Plugin Host
- RFC-0009 Runtime Resource Management
- RFC-0326 Workflow Vision
- RFC-1001 Common Event Model
- RFC-1003 Common Capability Model
- RFC-1006 Common Error Model

## Modules

- models.frame — Immutable frame models
- capture — Capture abstraction (sources, sessions, providers)
- services — VisionRuntime, VisionManager, VisionContext, VisionSession, VisionService
- scheduler — VisionScheduler with trigger support
- pipeline — Deterministic composable vision pipelines
- provider — Provider abstraction (OCR, Detection, Classification, etc.)
- egistry — VisionRegistry, ProviderRegistry, PipelineRegistry, etc.
- graph — Pipeline graph (nodes, edges, execution plan, validator)
- capabilities — Capability negotiation
- esources — VisionResourceManager
- metrics — Metrics collection
- health — Health status reporting
- events — Vision event types
- security — Permission validation, capture authorization
- storage — Abstract storage integration
- integration — IPC, workflow, plugin integration
