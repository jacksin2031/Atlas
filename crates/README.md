# crates/

## Purpose

Rust-native modules for Atlas. These crates provide performance-critical or
OS-level functionality that is bound to TypeScript/JavaScript via packages.

## Ownership

Platform team / Rust team

## Dependency Rules

- Crates depend on `crates/*` only.
- Crates MUST NOT depend on `packages/*` or `apps/*`.
- Public interfaces are exposed through `packages/*` bindings.

## Related RFCs

- RFC-0001 (Runtime Architecture)

## Future Scope

Additional native modules (vision, capture, plugin runtime) may be added.
