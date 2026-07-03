# Atlas Workflow Runtime Architecture

## Overview

The Atlas Workflow Runtime transforms declarative workflow definitions into executable runtime graphs.
The architecture is platform-independent. The current reference implementation is written in Python 3.10+.

## Module Structure

```
src/atlas_workflow/
├── common/           # Shared models (events, state, errors, capabilities)
│   ├── errors.py     # All exception types
│   ├── events.py     # WorkflowEvent, EventType
│   ├── state.py      # Lifecycle states, execution states, health states
│   ├── capabilities.py # Capability model
│   ├── contracts.py  # Input/output contracts, variables, ports
│   ├── manifest_model.py # Manifest metadata model
│   └── error_model.py  # Structured error details
├── manifest/         # Workflow manifest parsing
│   ├── models.py     # WorkflowManifest
│   └── parser.py     # WorkflowManifestParser
├── parser/           # Workflow definition parser
│   ├── models.py     # ParsedNode, ParsedEdge, ParsedWorkflow
│   └── workflow_parser.py # WorkflowParser
├── validator/        # Workflow validation
│   └── workflow_validator.py # WorkflowValidator
├── graph/            # Immutable workflow graphs
│   └── models.py     # WorkflowGraph, GraphNode, GraphEdge
├── node_registry/    # Plugin-discovered node definitions
│   ├── models.py     # NodeDefinition
│   └── node_registry.py # NodeRegistry
├── runtime/          # Workflow runtime orchestration
│   └── runtime.py    # WorkflowRuntime, WorkflowInstance, WorkflowContext
├── execution/        # Deterministic execution engine
│   ├── models.py     # ExecutionResult, ExecutionToken, ExecutionHistory
│   └── execution_engine.py # ExecutionEngine
├── scheduler/        # Scheduler integration
│   └── integration.py # TriggerType, ScheduleConfig, InMemoryScheduler
├── events/           # Event bus integration
│   └── event_bus.py  # EventBus
├── storage/          # Storage abstraction
│   └── abstraction.py # StorageBackend, StorageAbstraction
├── metrics/          # Metrics collection
│   └── collector.py  # MetricsCollector
├── health/           # Health service
│   └── service.py    # HealthService
└── plugin_integration/ # Plugin Runtime bridge
    └── bridge.py     # PluginBridge
```

## Design Principles

1. **Immutability**: Workflow definitions and graphs are immutable once created
2. **Determinism**: No hash-dependent ordering; topological sort uses sorted insertion
3. **Platform Independence**: No OS-specific, language-specific, or runtime-specific dependencies
4. **Dependency Injection**: All subsystems injected via constructor
5. **Zero Global Mutable State**: No module-level mutable state
6. **Separation of Concerns**: Each module has a single responsibility

## RFC Compliance

| RFC | Title | Compliance |
|-----|-------|------------|
| RFC-0301 | Workflow Overview | Full compliance |
| RFC-0304 | Workflow Runtime | Full compliance |
| RFC-0305 | Lifecycle | Full compliance |
| RFC-0309 | Actions | Full compliance |
| RFC-0312 | Scheduler | Full compliance |
| RFC-0313 | Parallelism | Full compliance |
| RFC-0315 | Recovery | Full compliance |
| RFC-0316 | Debugging | Full compliance |
| RFC-0317 | Validation | Full compliance |
| RFC-0319 | Security | Full compliance |
| RFC-0320 | Performance | Full compliance |
| RFC-0321 | Observability | Full compliance |
| RFC-0322 | Extension Points | Full compliance |
| RFC-0323 | Plugin Integration | Full compliance |
| RFC-0324 | Storage | Full compliance |
| RFC-1001 | Common Event Model | Full compliance |
| RFC-1002 | Common State Model | Full compliance |
| RFC-1003 | Common Capability Model | Full compliance |
| RFC-1004 | Common Contract Model | Full compliance |
| RFC-1005 | Common Manifest Model | Full compliance |
| RFC-1006 | Common Error Model | Full compliance |

## Related Documents

- [IMPLEMENTATION_STRATEGY.md](IMPLEMENTATION_STRATEGY.md) — Reference vs. Production distinction
- [COMPLIANCE_REPORT.md](COMPLIANCE_REPORT.md) — RFC traceability matrix
