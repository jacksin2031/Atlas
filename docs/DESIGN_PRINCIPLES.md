# Atlas Design Principles

> **Last Updated**: 2026-07-04
> **Owner**: Atlas Architecture Board

---

## Core Philosophy

Atlas is built on six foundational principles that guide every design decision.

---

### 1. Everything is Runtime

Every subsystem is a **Runtime** with its own lifecycle, health monitoring, and service contract.

- Runtimes are independently deployable
- Runtimes share a common lifecycle FSM (CREATED → INITIALIZING → READY → RUNNING → SHUTTING_DOWN → TERMINATED)
- Runtimes expose health and metrics endpoints
- Runtimes can be started/stopped independently

**Example**: The AI Runtime manages model loading/unloading. The Vision Runtime manages camera capture. Both follow the same pattern.

---

### 2. Everything is Plugin

Every capability is exposed through a **Provider Plugin** pattern.

- Providers are discovered at runtime via capability negotiation
- Providers can be swapped without restarting the system
- Plugin interface is versioned and backward-compatible
- Security sandbox isolates untrusted plugins

**Example**: An AI provider (OpenAI, local LLM) is a plugin. A vision provider (OpenCV, PIL) is a plugin. A storage provider (SQLite, PostgreSQL) is a plugin.

---

### 3. Everything is Event

The system communicates through **immutable events** — no direct method calls between subsystems.

- Events are versioned and immutable
- Event bus provides at-least-once delivery
- Subscribers react asynchronously
- Events are persisted for replay and debugging

**Example**: ModelLoaded, InferenceCompleted, FrameCaptured, DocumentIndexed — all are events.

---

### 4. Everything is Deterministic

Every computation produces **deterministic, reproducible results**.

- No hash-dependent ordering
- Topological sort uses sorted insertion
- No global mutable state
- Dependency injection throughout
- Frozen dataclasses with slots=True

**Example**: The Vision Pipeline executes stages in a deterministic order. The Knowledge Index builds in a reproducible sequence.

---

### 5. Contracts First

All interfaces are defined by **Contracts** before implementation.

- Contracts are versioned RFCs
- Contracts define input/output shapes
- Contracts enable cross-language interoperability
- Contracts are tested for compliance

**Example**: RFC-0013 defines Runtime Contracts. RFC-0209 defines Plugin API Contracts. RFC-0107 defines IPC Contracts.

---

### 6. Provider Pattern

All external dependencies are abstracted through **Providers**.

- Provider ABC defines the interface
- Concrete providers implement the interface
- Provider registry discovers and loads providers
- Provider capability negotiation selects the right implementation

**Example**: VisionProvider ABC → OpenCVProvider, PILProvider. StorageProvider ABC → SQLiteProvider, PostgreSQLProvider.

---

## Guiding Questions

When making a design decision, ask:

1. **Is this a Runtime?** — Does it have a lifecycle?
2. **Can this be a Plugin?** — Is it swappable?
3. **Should this be an Event?** — Is it decoupled?
4. **Is this Deterministic?** — Can it be reproduced?
5. **Is this a Contract?** — Is it versioned and tested?
6. **Is this a Provider?** — Is the dependency abstracted?

If the answer is "no" to any of these, reconsider the design.

---

## Governance

Changes to these principles require Architecture Board approval and an RFC update.
