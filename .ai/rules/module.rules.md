# Module Rules

> **Purpose**: Define how modules should be structured within each package.
> **Reference**: engineering.md for code generation best practices.

---

## Module Structure

Every module MUST follow this structure:

`
module_name/
├── mod.rs          # Public API + re-exports + module doc
├── impl.rs         # Implementation details (private)
├── error.rs        # Error types for this module
├── types.rs        # Data structures (if not in common/)
├── event.rs        # Module-specific events (if applicable)
└── test.rs         # Tests (or tests/ submodule)
`

## Module Responsibilities

Each module has exactly ONE responsibility (Single Responsibility Principle):

| Module | Responsibility | Cannot Do |
|--------|---------------|-----------|
| lifecycle | State machine transitions | Schedule tasks |
| registry | Service registration/lookup | Publish events |
| eventbus | Event routing/delivery | Manage services |
| scheduler | Task dispatch/ordering | Handle state transitions |
| health | Service health monitoring | Schedule tasks |
| config | Configuration loading | Manage services |
| manifest | Manifest parsing/validation | Schedule tasks |

## Module Visibility Rules

1. **mod.rs** is the public API surface.
2. Everything else is private by default.
3. Only export what consumers need (Interface Segregation).
4. Error types are always public.
5. Internal helpers are private.

## Module Test Requirements

Every module MUST have:

| Test Type | Coverage |
|-----------|----------|
| Happy path | Every public function |
| Error paths | Every function that returns Result |
| Edge cases | Boundary values, empty inputs |
| Concurrency | Thread safety (if applicable) |
| Lifecycle | State transitions (if stateful) |

## Module Documentation

Every module MUST have:

1. Module-level doc comment in mod.rs
2. Public function doc comments with:
   - Description
   - Arguments
   - Return value
   - Errors
   - Panics (if applicable)

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
