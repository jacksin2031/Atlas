# plugins/

## Purpose

Plugin repository layout for Atlas. Plugins are distributed in three categories:
official, community, and experimental.

## Ownership

- **plugins/official** — Plugin team
- **plugins/community** — Community contributors (vetted by Plugin team)
- **plugins/experimental** — Plugin team (unvetted, preview)

## Dependency Rules

- Plugins depend on `packages/plugin-api` and `packages/common`.
- Plugins MUST NOT depend on `apps/*` directly.
- Official plugins are vetted and signed by the Plugin team.

## Related RFCs

- RFC-0201 (Plugin API)
- RFC-0202 (Plugin Repository)

## Future Scope

Plugin marketplace integration, versioning, and sandbox policies.
