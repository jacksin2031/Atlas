# configs/

## Purpose

Default configuration files for Atlas. These include base configs, environment
profiles, and schema definitions.

## Ownership

Platform team

## Dependency Rules

- Configs are consumed by `apps/*` and `packages/runtime`.
- Config files follow the schema defined in RFC-0010.

## Related RFCs

- RFC-0010 (Configuration)

## Future Scope

Environment-specific configs (dev, staging, prod) and config validation tooling.
