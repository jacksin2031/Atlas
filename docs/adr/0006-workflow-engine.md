# ADR-0006: Workflow Engine

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

Atlas is designed as a universal automation platform capable of automating desktop applications, games, productivity software, and custom user workflows.

Traditional automation solutions are typically script-driven or hardcoded into the application. These approaches make workflows difficult to share, maintain, visualize, validate, and extend.

Atlas requires a workflow engine capable of:

- Executing deterministic automation pipelines
- Supporting AI-generated workflows
- Supporting visual editing
- Supporting plugin-defined nodes
- Remaining provider-independent
- Being serializable and versioned
- Executing locally without Internet connectivity

The workflow engine is considered one of the core platform services and must remain independent from UI, AI providers, and operating system implementations.

---

# Problem Statement

Without a dedicated workflow engine:

- Automation logic becomes tightly coupled with application code.
- AI-generated automation becomes inconsistent.
- Workflows cannot be versioned safely.
- Marketplace distribution becomes difficult.
- Plugins cannot contribute reusable nodes.
- Visual editors cannot represent execution correctly.

Atlas therefore requires a unified execution model that separates workflow definition from workflow execution.

---

# Decision

Atlas SHALL implement a dedicated Workflow Engine.

The Workflow Engine SHALL execute workflow definitions represented as structured JSON documents.

Workflow execution SHALL be interpreted at runtime.

Workflow definitions SHALL remain data only.

Business logic SHALL exist inside executable Nodes.

The engine SHALL NOT contain application-specific automation logic.

---

# Architecture

The Workflow Engine consists of the following components.

## Workflow Definition

Represents the serialized workflow.

Contains:

- Nodes
- Connections
- Variables
- Metadata
- Parameters
- Version

---

## Workflow Graph

Represents the runtime graph.

Responsible for:

- Dependency resolution
- Execution ordering
- Graph validation
- Cycle detection

---

## Node Runtime

Responsible for:

- Node initialization
- Input validation
- Execution
- Output generation
- Error reporting

Every node executes independently.

---

## Scheduler

Responsible for:

- Sequential execution
- Parallel execution
- Queue management
- Retry policies
- Cancellation

The scheduler SHALL remain deterministic.

---

## Event System

Publishes workflow events including:

- Started
- Completed
- Failed
- Cancelled
- Paused
- Resumed
- VariableChanged

The Event Bus SHALL be used for communication.

---

## Context

Runtime execution context contains:

- Variables
- Temporary values
- Runtime state
- User configuration
- AI state
- Execution history

Context SHALL NOT be stored inside workflow definitions.

---

# Workflow Representation

Workflow definitions SHALL use JSON.

Example:

```json
{
  "version": "1.0",
  "nodes": [],
  "connections": [],
  "variables": {},
  "metadata": {}
}
```

The JSON format SHALL be defined by a versioned JSON Schema.

---

# Node Model

Every node SHALL expose:

- Identifier
- Category
- Inputs
- Outputs
- Parameters
- Execution Function
- Validation Rules

Nodes SHALL be stateless whenever practical.

---

# Execution Model

Execution order SHALL be determined by graph dependencies.

Execution SHALL support:

- Sequential execution
- Parallel branches
- Conditional branches
- Loops
- Retry
- Timeout
- Cancellation

Execution SHALL NOT depend on screen refresh rate.

---

# Variable System

Variables SHALL exist independently from nodes.

Supported scopes:

- Workflow
- Local
- Global
- Session

Variables SHALL support serialization.

---

# Error Handling

Workflow execution SHALL continue only when permitted by node policy.

Supported strategies:

- Stop
- Retry
- Ignore
- Fallback
- Compensation

Every execution error SHALL contain:

- Error Code
- Message
- Stack Information
- Node Identifier
- Timestamp

---

# AI Integration

AI SHALL generate workflow definitions.

AI SHALL NOT directly generate executable runtime code.

Generated workflows MUST pass:

- Schema validation
- Graph validation
- Security validation

before execution.

---

# Plugin Integration

Plugins MAY register additional workflow nodes.

Plugins SHALL NOT modify the execution engine.

Plugins SHALL declare:

- Node metadata
- Version
- Permissions
- Compatibility

Node registration SHALL occur during plugin initialization.

---

# Security Considerations

Workflow execution SHALL follow the Principle of Least Privilege.

Dangerous nodes require explicit permission.

Examples include:

- Execute Process
- Write File
- Network Request
- System Command

Workflow imports SHALL be validated before execution.

---

# Performance Considerations

The engine SHALL support:

- Lazy node initialization
- Parallel scheduling
- Incremental graph compilation
- Cached validation
- Memory reuse

Performance regressions SHALL be benchmarked.

---

# Future Extensions

The architecture SHALL support:

- Distributed execution
- Cloud execution
- Remote workers
- AI planning nodes
- Event streaming
- Collaborative workflows
- Marketplace workflow packages

No architectural redesign should be required.

---

# Alternatives Considered

## Hardcoded Automation

Pros

- Easy to implement

Cons

- Impossible to extend
- Difficult to maintain

Rejected.

---

## Script-Based Engine

Examples:

- Lua
- Python

Pros

- Flexible

Cons

- Security risks
- Difficult validation
- Weak visualization

Rejected.

---

## JSON Workflow Graph

Pros

- Deterministic
- Serializable
- Visual
- AI-friendly
- Versionable
- Easy to validate

Accepted.

---

# Consequences

## Positive

- Visual workflow editing
- AI-generated automation
- Marketplace compatibility
- Plugin extensibility
- Deterministic execution
- Easy debugging
- Versioned workflows

## Negative

- More complex runtime
- Graph scheduler required
- Schema evolution required

---

# Risks

Potential graph complexity.

Large workflow execution overhead.

Plugin compatibility issues.

---

# Mitigations

Versioned schemas.

Workflow validation.

Execution profiling.

Plugin compatibility matrix.

Automated testing.

---

# Implementation Notes

Implementation SHALL be separated into:

packages/workflow/
    graph/
    scheduler/
    runtime/
    validator/
    serializer/
    events/
    variables/

Core execution SHALL remain independent from UI and AI providers.

---

# Related ADRs

ADR-0003 Monorepo Strategy

ADR-0005 Plugin Architecture

ADR-0007 Knowledge Pack System

ADR-0010 IPC Architecture

ADR-0012 Contract-First Development

ADR-0013 Specification-Driven Development

---

# Related Specifications

specs/workflow/

specs/runtime/

specs/plugin/

contracts/json/workflow.schema.json

---

# References

Node-RED

n8n

Temporal

Apache Airflow

Unreal Engine Blueprints

Behavior Trees

Microsoft Power Automate
