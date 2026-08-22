# ADR-0004: Technology Stack

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

---

# Context

Atlas requires:

- High-performance execution
- Desktop UI
- AI integration
- Cross-platform support
- Plugin ecosystem
- Native APIs
- Low memory usage

---

# Problem Statement

Choosing inappropriate technologies would reduce maintainability and performance.

---

# Decision

Atlas adopts:

Desktop

- Tauri

Frontend

- React
- TypeScript
- Vite

Native Runtime

- Rust

Database

- SQLite

Workflow

- JSON

Configuration

- JSON

Plugin Metadata

- JSON Schema

---

# Design Principles

- Native performance
- Small binary size
- Cross-platform
- Stable ecosystem
- Open standards

---

# Alternatives Considered

Electron

Pros

Large ecosystem

Cons

Large memory usage

Rejected.

Flutter

Pros

Beautiful UI

Cons

Poor desktop plugin ecosystem

Rejected.

C#

Pros

Fast development

Cons

Higher deployment complexity

Rejected.

---

# Consequences

Positive

- Fast startup
- Low memory
- Native integrations
- Strong type safety

Negative

- Two-language codebase
- Rust learning curve

---

# Risks

Communication between Rust and TypeScript.

---

# Mitigations

Strict IPC contracts.

---

# Implementation Notes

Business logic SHALL remain independent of framework APIs.

---

# Related ADRs

ADR-0003

ADR-0010

ADR-0012

---

# Related Specifications

specs/runtime/

specs/ui/

specs/ipc/

---

# References

Tauri

Rust

TypeScript
