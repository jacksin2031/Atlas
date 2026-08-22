# Common Patterns

> **Purpose**: Documented patterns that agents should recognize and apply.
> **Audience**: All agents.
> **Rule**: When a situation matches a documented pattern, use it.

---

## Pattern 0001: Topological Sort for Dependency Resolution

**When**: Services declare dependencies and must be initialized in order.
**Where**: Service Registry, Scheduler task ordering.
**How**: Kahn's algorithm with cycle detection.
**RFC Reference**: RFC-0003 §11
**Complexity**: O(V + E)

`
Input: [ServiceA(deps: [B, C]), ServiceB(deps: [C]), ServiceC(deps: [])]
Output: [C, B, A]
`

---

## Pattern 0002: Priority Queue with Backpressure

**When**: Event Bus or Scheduler needs ordered delivery with capacity limits.
**Where**: EventBus, Scheduler.
**How**: 
- 5 priority levels
- 80% capacity → BackpressureWarning event
- 100% capacity → Dead Letter Queue
**RFC Reference**: RFC-0005 §10, RFC-0004 §10

---

## Pattern 0003: FSM with Whitelisted Transitions

**When**: Any component has a defined lifecycle with strict state transitions.
**Where**: Runtime Lifecycle, Service Lifecycle.
**How**:
- Enum for all states
- Whitelist of legal transitions
- Reject illegal transitions with typed error
- Publish event on every transition
**RFC Reference**: RFC-0002 §8

---

## Pattern 0004: Interface Segregation

**When**: A service needs only a subset of another service's capabilities.
**Where**: All cross-service communication.
**How**:
- Define narrow interfaces (one method per concern)
- Implement all interfaces in the providing service
- Depend on interfaces, not implementations
**RFC Reference**: RFC-0003 §4, architecture-rules.md

---

## Pattern 0005: Exponential Backoff Retry

**When**: A task may fail transiently and should be retried.
**Where**: Scheduler task retries, IPC reconnection.
**How**:
- InitialDelay × BackoffMultiplier^n, capped at MaxDelay
- Default: 100ms × 2^n, max 30000ms
- Only retry on retryable error types
**RFC Reference**: RFC-0004 §14

---

## Pattern 0006: Contract-First Development

**When**: Starting a new module or service.
**Where**: Every new subsystem.
**How**:
1. Define the trait/interface first
2. Define the error types
3. Define the data structures
4. Implement the interface
5. Write tests against the interface
**RFC Reference**: RFC-0003 §4, ADR-0012

---

## Pattern 0007: Event-Driven Decoupling

**When**: Components need to communicate without direct dependencies.
**Where**: Cross-subsystem communication.
**How**:
1. Define the event schema (RFC-1001)
2. Publisher publishes to a channel
3. Subscriber listens via pattern matching
4. No direct import between publisher and subscriber
**RFC Reference**: RFC-0005, RFC-1001

---

## How to Add a Pattern

1. Find the next available number.
2. Fill in: When, Where, How, RFC Reference.
3. Keep it to one page.
4. Link to the implementation that uses it.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
