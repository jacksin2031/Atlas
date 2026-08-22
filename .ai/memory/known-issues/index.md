# Known Issues

> **Purpose**: Track known problems that are acknowledged but not yet fixed.
> **Audience**: All agents and human contributors.
> **Rule**: Every known issue has a status, impact, and workaround.
> **Do NOT**: Implement fixes for Known Issues without updating this file first.

---

## KNI-0001: Empty .ai/ Standard Files

**Status**: Open
**Impact**: Medium — Agents may not understand engineering standards without content.
**Workaround**: Read RFCs directly; standards files are referenced but not yet populated.
**Reported**: 2026-07-02
**Assigned**: Documentation agent
**Description**: Most .ai/*.md files are skeleton templates with headings but no content.
  - architecture-rules.md: empty
  - coding-standard.md: empty
  - constitution.md: empty
  - testing-standard.md: empty
  - security-standard.md: empty
  - performance-standard.md: empty
  - definition-of-done.md: empty
  - engineering.md: empty

## KNI-0002: Empty Root Markdown Files

**Status**: Open
**Impact**: Low — README, CONTRIBUTING, CHANGELOG, ROADMAP, SECURITY are all empty.
**Workaround**: Read specs/ and docs/adr/ directly for project context.
**Reported**: 2026-07-02
**Assigned**: Documentation agent

## KNI-0003: Empty packages/ Directories

**Status**: Open
**Impact**: High — All package directories contain only .gitkeep.
**Workaround**: Implementation creates the actual files.
**Reported**: 2026-07-02
**Assigned**: Sprint 1 implementation team

## KNI-0004: No Build System Configured

**Status**: Open
**Impact**: Medium — No Cargo.toml, package.json, or build scripts exist.
**Workaround**: Create build configuration as part of Sprint 1 implementation.
**Reported**: 2026-07-02
**Assigned**: Sprint 1 implementation team

---

## How to Add a Known Issue

1. Find the next available KNI number.
2. Fill in: Status, Impact, Workaround, Reported, Assigned, Description.
3. Update Status when fixed: Open → Fixed → Verified → Closed.

---

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-07-02 | Atlas Specification Committee | Initial publication |
