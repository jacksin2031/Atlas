# Atlas Workflow Runtime — Implementation Strategy

## Overview

This document clarifies the relationship between the Atlas specification, this reference implementation, and the production implementation. Every contributor should read this before starting work.

## Architecture Layers

```
Atlas Architecture
       ↓
    RFCs (specification)
       ↓
Reference Implementation (Python) ← you are here
       ↓
Production Implementation (Rust)
       ↓
Integration Tests
       ↓
Conformance Tests
```

### 1. Atlas Architecture

The top-level architectural decisions that define what the system must do. This is the source of truth.

### 2. RFCs (Specification)

Formal requirements derived from the architecture. RFCs define interfaces, behaviors, and constraints. They are language-agnostic.

### 3. Reference Implementation (Python)

This codebase. Its purposes:

- **Validate the specification**: Prove that RFCs are fully implementable as written
- **Provide a testable reference**: Give the Rust production team a concrete baseline to compare against
- **Enable rapid iteration**: Python allows faster design exploration than Rust compilation cycles
- **Serve as conformance test oracle**: Integration and conformance tests use this implementation to verify correctness

**This is NOT production code.** It is not optimized, does not target performance constraints, and may use Python idioms that would not translate to Rust.

### 4. Production Implementation (Rust)

The real system. It must:

- Satisfy all RFC requirements
- Meet performance, memory, and safety constraints defined by the architecture
- Pass all integration and conformance tests (against the reference implementation)

The Rust implementation is the **authoritative** implementation for deployment. The Python reference is the **authoritative** implementation for specification validation.

### 5. Integration Tests

End-to-end tests that exercise the full workflow pipeline (manifest → parser → validator → graph → runtime → execution). These run against both implementations to ensure behavioral equivalence.

### 6. Conformance Tests

Tests that verify a specific implementation conforms to the RFC specification. The reference implementation is the "gold standard" — if the Rust implementation passes the same conformance tests, it is considered conformant.

## Contributing

### If you are working on the Reference Implementation (Python):

- Focus on correctness and specification coverage
- Do NOT optimize for performance
- Do NOT add production-only features (e.g., distributed execution, cloud deployment)
- Ensure every RFC requirement is tested
- Keep the code readable and spec-aligned, not idiomatic-Python-at-all-costs

### If you are working on the Production Implementation (Rust):

- Focus on correctness, performance, and safety
- Use the reference implementation as a behavioral oracle
- Pass all integration and conformance tests
- Respect the platform-independent architecture — do not tie to Rust-specific patterns unless necessary

### If you are reviewing an RFC:

- Ask: "Can this be implemented by the reference?"
- Ask: "Does the reference implementation have a test for this?"
- Ask: "Would this constraint survive translation to Rust?"

## File Locations

| Artifact | Location |
|----------|----------|
| RFCs | `specs/workflow/RFC-*.md` |
| Reference Implementation | `src/atlas_workflow/` |
| Reference Tests | `tests/` |
| Production Implementation | *(future: `src/atlas_runtime/`)* |
| Architecture Decisions | *(future: `docs/ADRs/`)* |

## Key Principle

> **The reference implementation proves the spec is sound. The production implementation proves the spec is buildable. Both must agree on behavior.**
