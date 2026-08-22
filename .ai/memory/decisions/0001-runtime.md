# Decision Log — Runtime Foundation

> **Decision**: 0001 — Runtime uses a deterministic finite-state machine for lifecycle management.
> **Date**: 2026-07-02
> **Author**: Architect
> **Status**: Accepted
> **RFC Reference**: RFC-0002 §8

---

## Context

The Runtime lifecycle must be deterministic and auditable.
Non-deterministic state transitions lead to race conditions,
unrecoverable states, and impossible debugging.

## Decision

Adopt a deterministic finite-state machine (FSM) with:
- 8 explicit states (Created → Terminated)
- Whitelist of legal transitions
- Monotonic timestamp on every transition
- Event published on every transition
- No backward transitions except through defined paths

## Consequences

**Positive:**
- Predictable behavior
- Easy to audit (transition log)
- Impossible to reach undefined states
- Clear error messages for illegal transitions

**Negative:**
- Slightly more boilerplate for state management
- New transitions require RFC amendment

## Alternatives Considered

1. **Event-driven state (CQRS)** — More flexible but harder to reason about. Rejected for Sprint 1.
2. **Enum-based with runtime checks** — Less explicit, harder to audit. Rejected.
3. **FSM with explicit transitions** — Chosen approach.

---

# Decision Log — Service Registry

> **Decision**: 0002 — Service Registry uses topological sort for initialization order.
> **Date**: 2026-07-02
> **Author**: Architect
> **Status**: Accepted
> **RFC Reference**: RFC-0003 §11

---

## Context

Services have dependencies. Service A may require Service B to be initialized first.
The initialization order must be deterministic and detect cycles.

## Decision

Use Kahn's algorithm for topological sorting with cycle detection:
- Input: service dependency graph
- Output: initialization order (dependencies first)
- Failure: CircularDependencyError if graph has cycles
- Budget: ≤ 100ms during boot

## Consequences

**Positive:**
- Deterministic initialization order
- Cycles detected before runtime
- O(V+E) complexity
- Simple to test

**Negative:**
- Requires every service to declare its dependencies
- Adding/removing dependencies changes order

## Alternatives Considered

1. **DFS-based topological sort** — Same complexity, but harder to debug cycles.
2. **Manual ordering** — Fragile, untestable, no cycle detection. Rejected.

---

# Decision Log — Event Bus Design

> **Decision**: 0003 — Event Bus uses priority queues with DLQ overflow.
> **Date**: 2026-07-02
> **Author**: Architect
> **Status**: Accepted
> **RFC Reference**: RFC-0005 §10, §15

---

## Context

Events must be delivered in priority order. Critical events (panic, shutdown)
must not be blocked by low-priority events. When the queue is full,
events must not be silently dropped.

## Decision

- 5 priority levels (Critical, High, Normal, Low, Background)
- Priority queue per level
- Backpressure at 80% capacity (publish BackpressureWarning)
- Overflow at 100% → Dead Letter Queue
- Wildcard channel matching for subscriptions

## Consequences

**Positive:**
- Critical events always delivered first
- No silent data loss (DLQ catches overflow)
- Observable backpressure via events
- Flexible subscription patterns

**Negative:**
- More complex queue management
- DLQ needs monitoring

## Alternatives Considered

1. **Single FIFO queue** — Simple but no priority. Rejected.
2. **Separate channels per priority** — Too many channels, hard to manage. Rejected.

---

# Decision Log — Interface-First Implementation

> **Decision**: 0004 — All code follows interface-first ordering.
> **Date**: 2026-07-02
> **Author**: Architect
> **Status**: Accepted
> **RFC Reference**: ADS Constitution §3, RFC-0003 §4

---

## Context

Bottom-up implementation leads to tightly coupled code that is hard to test
and hard to change. Interface-first ensures loose coupling.

## Decision

Implementation order:
1. Contracts (trait/interface definitions)
2. Common types (shared structs, enums)
3. Infrastructure (data access, external dependencies)
4. Services (business logic)
5. Runtime assembly (integration)

No module may import from a module that comes AFTER it in this order.

## Consequences

**Positive:**
- Loose coupling by construction
- Testable interfaces before implementations
- Swappable implementations
- Clear dependency direction

**Negative:**
- Requires planning before coding
- Slightly more upfront design work

## Alternatives Considered

1. **Top-down** — Define Runtime first, then drill down. Leads to coupling.
2. **Bottom-up** — Implement concrete services first. Leads to tight coupling. Rejected.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
