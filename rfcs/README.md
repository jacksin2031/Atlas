# rfcs/

## Purpose

This directory is preserved for historical RFC references.

**The single source of truth for specifications is `specs/`.**

All RFCs should be placed under `specs/{subsystem}/` with the naming convention:
`RFC-NNNN-title.md`

## Directory Structure

```
specs/
  runtime/     ← RFC-0001 through RFC-0014
  plugin/      ← RFC-0201 through RFC-0229
  workflow/    ← RFC-0301 through RFC-0333
  storage/     ← RFC-0401 through RFC-0425
  ipc/         ← RFC-0101 through RFC-0112
  common/      ← Cross-cutting RFCs
```

## Convention

| Path | Role |
|------|------|
| `specs/` | Formal RFCs (authoritative) |
| `docs/` | Design notes, walkthroughs, examples |
| `rfcs/` | Legacy/historical references only |

## Revision History

| Date | Change |
|------|--------|
| 2026-07-02 | Root-level RFCs migrated to specs/ subdirectories |
