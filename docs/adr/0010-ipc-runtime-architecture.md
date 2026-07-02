# ADR-0010: IPC & Runtime Architecture

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

Supersedes:
None

Superseded By:
None

---

# Context

Atlas is a modular desktop automation platform composed of multiple independent subsystems.

Major runtime components include:

- Desktop UI
- Runtime Engine
- Workflow Engine
- Vision Engine
- Recorder
- AI Operating System (AIOS)
- Plugin Host
- Marketplace
- Local Services
- Native Rust Modules

These components execute with different performance, security, and lifecycle requirements.

Direct dependencies between modules would introduce tight coupling and significantly reduce maintainability.

Atlas therefore requires a unified Inter-Process Communication (IPC) architecture.

---

# Problem Statement

Without a standardized IPC layer:

- Modules directly import each other.
- Plugin isolation becomes impossible.
- Runtime crashes propagate across components.
- Native code becomes tightly coupled with UI.
- AI providers become difficult to replace.
- Security boundaries disappear.
- Testing becomes increasingly difficult.

Atlas requires explicit communication boundaries.

---

# Decision

Atlas SHALL adopt an event-driven, contract-first IPC architecture.

All cross-module communication SHALL occur through defined IPC interfaces.

No module SHALL directly invoke another module across architectural boundaries.

Every IPC interface SHALL be versioned.

Every IPC payload SHALL be validated.

---

# Design Principles

The IPC architecture SHALL be:

- Contract-first
- Strongly typed
- Versioned
- Observable
- Secure
- Asynchronous by default
- Transport-independent

Modules SHALL communicate through messages instead of direct dependencies.

---

# Runtime Architecture

Atlas SHALL consist of independent runtimes.

Examples:

- UI Runtime
- Core Runtime
- Workflow Runtime
- Vision Runtime
- AI Runtime
- Plugin Runtime
- Recorder Runtime

Each runtime SHALL own its internal state.

---

# IPC Layers

The communication stack SHALL contain:

Layer 1

UI API

↓

Layer 2

Application Services

↓

Layer 3

IPC Dispatcher

↓

Layer 4

Runtime Services

↓

Layer 5

Native Rust Components

Every request SHALL pass through the dispatcher.

---

# IPC Dispatcher

The dispatcher SHALL be responsible for:

- Message routing
- Validation
- Authentication
- Authorization
- Logging
- Metrics
- Version negotiation

Business logic SHALL NOT exist inside the dispatcher.

---

# Message Format

Every IPC message SHALL contain:

Request ID

Timestamp

Protocol Version

Source

Destination

Command

Payload

Metadata

Example

{
    "id": "request-001",
    "version": "1.0",
    "source": "workflow",
    "destination": "vision",
    "command": "capture_screen",
    "payload": {}
}

---

# Contract Validation

Every IPC endpoint SHALL have a contract.

Contracts SHALL define:

Input Schema

Output Schema

Error Codes

Permissions

Version

Invalid messages SHALL be rejected.

---

# Communication Modes

Supported modes:

- Request / Response
- Publish / Subscribe
- Event Stream
- Fire-and-forget

Each communication pattern SHALL define timeout behavior.

---

# Event Bus

All system-wide events SHALL pass through the Event Bus.

Examples:

WorkflowStarted

WorkflowFinished

PluginLoaded

PluginUnloaded

OCRCompleted

AICompleted

CaptureFinished

UserInteractionDetected

Events SHALL remain immutable.

---

# Runtime Isolation

Every runtime SHALL remain isolated.

Failures SHALL NOT propagate between runtimes.

Each runtime SHALL support graceful restart.

---

# Plugin Communication

Plugins SHALL communicate only through IPC.

Plugins SHALL NOT directly import internal modules.

All plugin permissions SHALL be validated.

---

# Native Communication

Rust components SHALL expose typed IPC APIs.

Unsafe FFI SHALL remain internal.

UI SHALL never call Rust functions directly.

---

# AI Communication

AI Runtime SHALL communicate through IPC.

Workflow Engine SHALL never access providers directly.

All AI execution SHALL pass through AIOS.

---

# Vision Communication

Vision Runtime SHALL expose services such as:

Capture

OCR

Object Detection

Template Matching

Image Comparison

These services SHALL remain independent.

---

# Recorder Communication

Recorder SHALL publish events instead of executing workflows.

Workflow execution SHALL subscribe to recorder events.

---

# Marketplace Communication

Marketplace SHALL never install plugins directly.

Installation SHALL be delegated to the Plugin Manager.

---

# Security

IPC SHALL validate:

Origin

Permissions

Schema

Protocol Version

Payload Size

Unauthorized requests SHALL be rejected.

---

# Performance

IPC SHALL support:

Message batching

Compression

Binary payloads

Streaming

Shared memory (future)

Backpressure

Large payloads SHOULD avoid unnecessary copying.

---

# Logging

Every IPC request SHALL generate:

Request ID

Execution Time

Source

Destination

Result

Error Code

Logs SHALL support distributed tracing.

---

# Monitoring

Metrics SHALL include:

Request Count

Latency

Error Rate

Queue Length

Runtime Health

These metrics SHALL be accessible to developers.

---

# Versioning

IPC SHALL use semantic versioning.

Breaking changes SHALL require:

New protocol version

Compatibility validation

Migration strategy

---

# Future Extensions

The architecture SHALL support:

Remote runtimes

Distributed execution

Cloud workers

Remote plugins

Network IPC

WASM runtimes

No redesign shall be required.

---

# Alternatives Considered

## Direct Module Imports

Pros

Simple.

Cons

Tight coupling.

Rejected.

---

## Shared Global State

Pros

Easy.

Cons

Unsafe.

Rejected.

---

## Event-driven IPC

Pros

Decoupled.

Scalable.

Observable.

Secure.

Accepted.

---

# Consequences

## Positive

Loose coupling.

Plugin isolation.

Runtime stability.

Independent testing.

Future distributed execution.

Enterprise readiness.

## Negative

Higher architectural complexity.

Additional serialization.

Debugging IPC requires tooling.

---

# Risks

Message storms.

Protocol fragmentation.

Serialization overhead.

---

# Mitigations

Rate limiting.

Version negotiation.

Schema validation.

Monitoring.

Automated compatibility testing.

---

# Implementation Notes

Implementation SHALL reside under:

packages/core/ipc/

Suggested modules:

dispatcher/

contracts/

events/

transport/

validator/

registry/

metrics/

logger/

bridge/

Runtime services SHALL communicate only through the dispatcher.

---

# Related ADRs

ADR-0003 Monorepo Strategy

ADR-0005 Plugin Architecture

ADR-0006 Workflow Engine

ADR-0008 AI Provider Independence

ADR-0009 AI Routing & Model Orchestration

ADR-0011 Vision Engine

ADR-0012 Contract-First Development

ADR-0013 Specification-Driven Development

---

# Related Specifications

specs/ipc/

specs/runtime/

specs/plugin/

contracts/ipc/

---

# References

Tauri IPC

Electron IPC

VS Code Extension Host

Chrome DevTools Protocol

JSON-RPC 2.0

gRPC

Apache Kafka Event Architecture

Model Context Protocol (MCP)
