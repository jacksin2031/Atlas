# Dependency Rules

> **Purpose**: Define allowed and forbidden import directions between modules.
> **Reference**: architecture-rules.md for full layer constraints.

---

## Allowed Dependencies

`
contracts/ → (no dependencies)
common/ → contracts/
runtime/ → contracts/, common/
workflow/ → contracts/, common/, runtime/
plugin/ → contracts/, common/, runtime/
vision/ → contracts/, common/, runtime/
storage/ → contracts/, common/, runtime/
ipc/ → contracts/, common/, runtime/
`

## Forbidden Dependencies

| From | Cannot Import | Reason |
|------|--------------|--------|
| workflow/ | runtime/ internals | Workflow must use contracts only |
| plugin/ | runtime/ internals | Plugin isolation |
| vision/ | scheduler/ internals | Vision is a consumer, not a controller |
| storage/ | workflow/ | Storage is infrastructure, not business logic |
| ui/ | runtime/ internals | UI communicates via IPC only |
| Any agent | contracts/ (direct) | Use trait definitions, not implementations |

## Circular Dependency Prevention

| Check | Method |
|-------|--------|
| Graph analysis | Static import analysis |
| Runtime verification | No cyclic module initialization |
| Test | cargo test --test dependency_graph |

## Rules

1. **Downward only**: Lower layers never import upper layers.
2. **Interface only**: Imports must be of trait definitions, not implementations.
3. **No cross-cutting**: Modules in the same layer do not import each other.
4. **Explicit opt-out**: Any exception requires an ADR.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
