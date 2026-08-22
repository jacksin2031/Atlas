# packages/

## Purpose

Shared TypeScript/JavaScript packages consumed by apps and crates. These are
pure-library packages with no application-level concerns.

## Ownership

Platform team owns the package boundary; individual package teams own content.

## Dependency Rules

- Packages depend only on other packages in this directory.
- Packages MUST NOT depend on `apps/*` or `crates/*`.
- Internal packages use workspace protocol for linking.

## Related RFCs

- RFC-1001 (Package Boundary Protocol)

## Future Scope

Additional shared packages (e.g., telemetry, logging, i18n) may be added.
