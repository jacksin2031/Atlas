# scripts/

## Purpose

Automation scripts for build, deploy, test, and release workflows. Shell and
PowerShell scripts that support the Atlas development lifecycle.

## Ownership

Release team / Platform team

## Dependency Rules

- Scripts are standalone; they MAY invoke binaries from `apps/` or `crates/`.
- Scripts MUST NOT contain business logic.

## Related RFCs

- N/A (operational tooling)

## Future Scope

Release automation, CI pipeline scripts, and environment provisioning.
