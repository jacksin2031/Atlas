# packages/runtime

## Purpose

The Atlas Runtime — the core execution engine that coordinates process
lifecycles, services, scheduling, events, configuration, manifests, metrics,
health, and storage abstractions.

This crate implements the in-scope **Runtime Infrastructure** services per the
ADS, ADRs, and RFCs:

- **Configuration Service** (`src/config`) — loads, parses, and exposes an
  immutable runtime `Configuration`. Configuration is frozen once the Runtime
  reaches the `Running` state (RFC-0010 §4).
- **Manifest Service** (`src/manifest`) — parses and validates the runtime
  manifest independently of business logic, and exposes capability/service
  declarations (RFC-0010 §8–12).
- **Metrics Service** (`src/metrics`) — system diagnostic time-series
  collector (SRV-METRICS) implementing the `MetricsRecorder` contract with
  counters, gauges, and histograms (RFC-0003 §16).
- **Health Service** (`src/health`) — health monitor (SRV-HEALTH) implementing
  the `HealthChecker` contract with worst-case aggregation and degradation
  escalation to `Disabled` after a configurable failure threshold
  (RFC-0003 §13, §16).

Every service above implements the `ServiceContract` trait
(`initialize` / `start` / `pause` / `resume` / `stop` / `deinitialize` /
`dispose` / `health_check`) and uses interior mutability so it is `Send +
Sync` and shareable via dependency injection **without global mutable state**.

Sprint 1 modules retained: `lifecycle` (FSM per RFC-0002 §8), `registry`
(service registration + dependency-ordered shutdown), `dependency`
(topological sort with cycle detection), `eventbus`, `scheduler`, `error`.

## Ownership

Platform team

## Dependencies

- `packages/contracts` (trait definitions)
- `packages/common` (shared types)

## Related RFCs

- RFC-0001 (Runtime Overview)
- RFC-0002 (Runtime Lifecycle)
- RFC-0003 (Runtime Service Model)
- RFC-0010 (Runtime Manifest Specification)
- RFC-0011 (Runtime Error Taxonomy)
- RFC-1005 (Common Manifest Model)
- RFC-1006 (Common Error Model)

## Testing

Unit tests are co-located in each module (`#[cfg(test)] mod tests`).
Integration tests live in `tests/`. Run with `cargo test -p atlas-runtime`.

