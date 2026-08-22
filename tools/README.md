@'@ | Set-Content "$base\plugins\community\README.md" -Encoding UTF8

# === tools/ README ===
@'
# tools/

## Purpose

Development and maintenance tools that do not ship with Atlas. Build helpers,
code generators, migration scripts, and internal utilities.

## Ownership

Platform team

## Dependency Rules

- Tools depend on `packages/*` only for shared utilities.
- Tools MUST NOT be imported by production code.

## Related RFCs

- N/A (internal tooling)

## Future Scope

Additional tooling for CI, linting, and code generation.
