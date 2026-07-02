# apps/

## Purpose

Application entry points for Atlas. Each subdirectory represents a distinct
distribution target — a desktop application, a CLI tool, or a launcher process.

## Ownership

- **apps/desktop** — Desktop UI team
- **apps/cli** — CLI / tooling team
- **apps/launcher** — Platform team

## Dependency Rules

- Apps depend on `packages/*` for shared logic.
- Apps MUST NOT contain business logic; delegate to packages.
- Apps MAY depend on `crates/*` for native interop.

## Related RFCs

- RFC-0001 (Runtime Architecture)
- RFC-0007 (Desktop Application)

## Future Scope

Additional distribution targets (mobile, web, service daemon) may be added as
subdirectories under `apps/`.
