# Atlas Execution Runtime

## Table of Contents
- [Runtime Architecture](#runtime-architecture)
- [Process Lifecycle](#process-lifecycle)
- [Runtime Infrastructure Services](#runtime-infrastructure-services)
- [Storage Foundation](#storage-foundation)
- [Error Handling](#error-handling)

## Runtime Architecture

The Runtime (`packages/runtime`) is the central coordinator for all core
services. It is assembled in dependency order (RFC-0003 §11) and driven by a
deterministic finite state machine (RFC-0002 §8).

```
contracts (traits) → common (shared types) → runtime (services) → storage (abstractions)
```

The Runtime exposes accessors for each subsystem service so consumers obtain
dependencies via dependency injection rather than a service locator
(RFC-0003 §4.2).

## Process Lifecycle

The Runtime state machine (`LifecycleManager`) enforces the legal transitions
defined in RFC-0002 §8: `Created → Initializing → Ready → Running`, with
`Paused`, `ShuttingDown`, `Failed`, and `Terminated` states. Illegal
transitions are rejected with `StateTransitionError`.

- **Bootstrap** loads configuration, parses/validates the manifest, registers
  and initialises services in topological order, then transitions to `Ready`.
- **Activation** transitions to `Running` and **freezes** the configuration
  (RFC-0010 §4 immutability rule).
- **Shutdown** deinitialises services in reverse registration order
  (RFC-0002 §32) and transitions to `Terminated`.

## Runtime Infrastructure Services

All services implement the `ServiceContract` trait (RFC-0003 §9) —
`initialize`, `start`, `pause`, `resume`, `stop`, `deinitialize`, `dispose`,
and `health_check` — and use interior mutability (`&self`) so they are `Send +
Sync` and shareable via dependency injection without global mutable state.

### Configuration Service (`srv-config`)
Loads, parses, and exposes an immutable runtime `Configuration`
(RFC-0010 §9). `freeze()` is called when the Runtime reaches `Running`; any
mutating call afterward returns `ConfigError::Frozen`.

### Manifest Service (`srv-manifest`)
Parses and validates the runtime manifest **independently of business logic**
(RFC-0010 §8–12). Validation checks schema versions, capability declarations,
and service-ID uniqueness. Exposes capability discovery and service
declarations.

### Metrics Service (`srv-metrics`)
Implements the `MetricsRecorder` contract (RFC-0003 §16) with counters,
gauges, and histograms (explicit buckets). Snapshots are point-in-time and
include monotonic timestamps.

### Health Service (`srv-health`)
Implements the `HealthChecker` contract (RFC-0003 §16). Aggregates health with
worst-case semantics (`Unhealthy` > `Disabled` > `Degraded` > `Healthy`).
Enforces degradation escalation: a service that fails its health check
repeatedly is escalated to `Disabled` after a configurable failure threshold
(RFC-0003 §13).

## Storage Foundation

The Storage Foundation (`packages/storage`) provides abstract providers and
registries only — no database-specific logic (RFC-0401 / RFC-0403 / RFC-0404).

- `ProviderRegistryImpl` registers, activates, deactivates, and selects
  providers by capability, enforcing the provider lifecycle state machine.
- `ProviderLifecycleManager` and `ResourceManager` enforce the provider and
  resource state machines with atomic, legal-transition validation.

Concrete backends implement the `StorageProvider` trait; the platform
implements the registry.

## Error Handling

Errors flow through the `AtlasError` hierarchy (`packages/common/src/error.rs`)
covering Service, Event, Scheduler, Lifecycle, Manifest, Config, Health,
Dependency, Metrics, and Storage categories. Each subsystem error type maps
into `AtlasError` via `#[from]` so the Runtime can propagate any failure
uniformly (RFC-0011 / RFC-1006).
