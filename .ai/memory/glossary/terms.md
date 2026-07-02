# Atlas Glossary

> **Purpose**: Single source of truth for domain terminology.
> **Audience**: All agents and human contributors.
> **Rule**: When defining a new term in an RFC, add it here first.
> **Do NOT**: Use different meanings for the same term across RFCs.

---

## Terms

| Term | Definition | Source |
|------|-----------|---------|
| Runtime | The core execution engine coordinating process lifecycles, states, resources, and scheduling queues. | RFC-0001 |
| Workspace | The sandboxed directory boundary containing workflow definitions, configuration manifests, local caches, and logs. | RFC-0001 |
| Service | A modular system component registered with the Service Registry, satisfying a specific abstract Service Contract. | RFC-0001 |
| Provider | Infrastructure adapters implementing hardware, operating system, or external API interfaces. | RFC-0001 |
| Scheduler | The execution coordinator that prioritizes tasks and schedules dispatches to worker pools. | RFC-0001 |
| Event Bus | The asynchronous message broker that routes events based on channel names and priority queues. | RFC-0001 |
| State Store | The transaction-isolated database containing current configurations and runtime variables. | RFC-0001 |
| Lifecycle | The state transitions of a process or service from allocation to disposal. | RFC-0001 |
| Watchdog | The monitoring service checking heartbeats of registered services to initiate recovery routines. | RFC-0001 |
| Sandbox | An isolated execution process or virtual machine context restricting OS access. | RFC-0001 |
| Capability | A feature declaration verified and exposed by the Runtime Manifest. | RFC-0001 |
| Manifest | The declarative definition of a component, including its metadata, dependencies, capabilities, and configuration. | RFC-0001 |
| Contract | A formal agreement defining the interface between two components, specifying required behaviors and guarantees. | RFC-0001 |
| Write-Ahead Log (WAL) | A persistent log recording mutations before committing them to the main state database. | RFC-0001 |
| Dead Letter Queue (DLQ) | A dedicated message queue containing events that could not be delivered to their target subscribers. | RFC-0001 |
| Hook | A callback registered at an extension point, invoked at a defined moment in the lifecycle. | RFC-0002 |
| Correlation ID | A globally unique identifier attached to every message for end-to-end tracing. | RFC-1001 |
| Trace ID | An identifier linking related events across subsystem boundaries. | RFC-1001 |

---

## How to Add a Term

1. Add to the table above in alphabetical order.
2. Reference the RFC where the term is first defined.
3. If a term is used across multiple RFCs, reference the first one.
4. Do not redefine terms — use existing definitions.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
