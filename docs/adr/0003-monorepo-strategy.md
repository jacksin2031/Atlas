# ADR-0003: Monorepo Strategy

Status: Accepted

Date: 2026-06-28

Authors:
Atlas Core Team

---

# Context

Atlas is designed as an extensible automation platform rather than a single application. The project includes multiple deliverables:

- Desktop Application
- CLI
- Runtime Engine
- Vision Engine
- Recorder
- SDK
- Plugin SDK
- Marketplace
- Knowledge Packs
- Documentation
- AI Development System (ADS)

These components evolve together and share contracts, interfaces, and release cycles.

---

# Problem Statement

Maintaining these components in independent repositories would introduce:

- Version drift
- Duplicate infrastructure
- Cross-repository dependency management
- Difficult refactoring
- Fragmented documentation
- Inconsistent AI context

---

# Decision

Atlas SHALL use a single Monorepo.

All first-party projects are developed inside one repository.

Shared contracts, schemas, packages and documentation SHALL exist only once.

---

# Design Principles

- Single source of truth
- Atomic commits across modules
- Shared tooling
- Shared CI/CD
- Unified version management
- Consistent developer experience

---

# Alternatives Considered

## Multiple repositories

Pros

- Smaller repositories
- Independent permissions

Cons

- Cross-version incompatibilities
- Difficult large-scale refactoring
- Duplicate CI pipelines

Rejected.

---

## Git Submodules

Pros

- Reusable modules

Cons

- Complex workflow
- Poor developer experience
- Difficult onboarding

Rejected.

---

# Consequences

## Positive

- Easier refactoring
- Unified architecture
- Better AI understanding
- Easier dependency management

## Negative

- Larger repository size
- Longer CI pipelines

---

# Risks

Repository growth over time.

---

# Mitigations

- Workspace isolation
- Incremental builds
- Build caching
- Modular package boundaries

---

# Implementation Notes

Repository layout SHALL follow the ADS structure.

No module may exist outside the monorepo without architectural approval.

---

# Related ADRs

ADR-0001

ADR-0002

ADR-0004

---

# Related Specifications

specs/project/

specs/runtime/

specs/plugin/

---

# References

Google Monorepo

Nx

Turborepo

Rush
