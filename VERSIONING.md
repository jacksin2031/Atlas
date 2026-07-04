# Atlas Versioning Policy

> **Effective**: 2026-07-04
> **Owner**: Atlas Architecture Board

---

## Version Number Format

```
MAJOR.MINOR.PATCH-PREIDENTIFIER
```

Example: `0.5.0-alpha`

---

## Pre-Identifiers

| Pre-ID | Meaning |
|---|---|
| `alpha` | Active development. APIs may change. Use during Runtime construction. |
| `beta` | Feature-complete. APIs frozen. Used after all Runtime modules are implemented. |
| `rc` | Release candidate. Conformance tests must pass. |
| *(none)* | Stable release. All acceptance criteria pass. |

---

## Version Semantics

### Alpha (`0.x.x-alpha`)
- Created at the end of each Sprint.
- Each Sprint adds one Runtime module.
- MAJOR stays `0` until all Runtimes are complete.
- MINOR increments each Sprint.
- PATCH is used for hotfixes between Sprints.

### Beta (`0.x.x-beta`)
- All Runtime modules implemented.
- Focus shifts to stability, performance, and conformance.
- MINOR increments for significant improvements.

### Release Candidate (`0.x.x-rc.N`)
- Conformance tests pass.
- No blocking bugs.
- `N` increments for each RC iteration.

### Stable (`x.y.z`)
- All acceptance criteria met.
- Production-ready.
- MAJOR increments for breaking changes.

---

## Sprint-to-Version Mapping

| Sprint | Version | Module |
|---|---|---|
| Sprint 0 | 0.0.1-alpha | Bootstrap |
| Sprint 1 | 0.1.0-alpha | Runtime Foundation |
| Sprint 2 | 0.2.0-alpha | Runtime Infrastructure |
| Sprint 3 | 0.3.0-alpha | Plugin Runtime |
| Sprint 4 | 0.4.0-alpha | Workflow Runtime |
| Sprint 5 | 0.5.0-alpha | IPC Runtime |
| Sprint 6 | 0.6.0-alpha | Vision Runtime |
| Sprint 7 | 0.7.0-alpha | AI Runtime |
| Sprint 8 | 0.8.0-alpha | Knowledge Runtime |
| Sprint 9 | 0.9.0-alpha | Project Runtime |
| Sprint 10 | 0.10.0-alpha | Conformance Tests |

---

## Tag Naming Rules

- Git tags use the exact version string: `v0.5.0-alpha`
- Tags are lightweight or annotated (`-a`): `git tag -a v0.5.0-alpha -m "Atlas v0.5.0-alpha"`
- Tags are pushed after all documentation updates are committed.
- Historical tags are never deleted or rewritten.

---

## Branch Naming Rules

- `main` — stable development branch
- `sprint/N` — Sprint feature branches
- `release/vX.Y.Z` — release preparation branches
- `hotfix/description` — emergency fixes

---

## Changelog Rules

- Follow [Keep a Changelog](https://keepachangelog.com/) format.
- Sections: Added, Changed, Deprecated, Removed, Fixed, Security.
- One version section per release.
- Never remove or modify previous release entries.
- Dates in ISO-8601 format (`YYYY-MM-DD`).

---

## Governance

Changes to this policy require Architecture Board approval and an RFC update.
