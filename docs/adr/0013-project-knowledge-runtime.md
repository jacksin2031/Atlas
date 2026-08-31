# ADR-0013: Project Knowledge Runtime

Status: Accepted

Date: 2026-08-31

## Context

ADR-0007 defines immutable, distributable Knowledge Packs. Atlas also needs
mutable knowledge created by users, imports, Workflow executions, and Vision/OCR.
Before Sprint 16 the repository had only placeholder package/schema/UI surfaces,
so no component could authoritatively persist or retrieve that data.

## Decision

Atlas SHALL use a project-scoped Python Knowledge Runtime as the sole authority
for mutable project knowledge.

- The Runtime SHALL run in the existing persistent Python host reused by Tauri.
- Canonical data SHALL be accessed through Runtime APIs, never frontend stores.
- The initial storage adapter SHALL use atomic project-local JSON at
  `.atlas/knowledge.v1.json` with backup recovery.
- Project scope SHALL combine a stable path-derived project ID with the absolute
  project root and SHALL be validated at every boundary.
- Sprint 16 retrieval SHALL be deterministic, offline lexical search. Scores
  SHALL be labeled as raw ranking values.
- Workflow and AI integrations SHALL exchange typed references. Full knowledge
  content SHALL be resolved transiently at the Runtime boundary.
- Vision/OCR writes SHALL preserve source and frame/workflow provenance.
- Import SHALL validate a full batch before a single atomic persistence step and
  SHALL retain portable source metadata only.

## Architecture

```text
Knowledge Studio (display cache + drafts)
          |
          | typed IPC commands/events
          v
Tauri project scope and command boundary
          |
          v
Persistent Python host
  +-- Knowledge Runtime -- storage adapter -- project/.atlas/knowledge.v1.json
  +-- Workflow Runtime -- typed Knowledge/Vision nodes
  +-- AI bridge -------- transient resolved context --------> AI Runtime
```

## Consequences

Project isolation and restart persistence are explicit and testable. Search and
CRUD share one source of truth, so updates/deletes cannot leave a frontend-owned
index stale. The JSON adapter is simple and auditable but is not intended for
large-scale semantic retrieval; future backends can implement the storage
abstraction without changing Studio/Workflow contracts.

Knowledge Packs remain separate and immutable. Semantic search, vectors,
relations, cloud sync, and collaboration require future decisions and are not
represented as implemented UI.

## Related decisions

- ADR-0007 Knowledge Pack System
- ADR-0008 AI Provider Independence
- ADR-0010 IPC Runtime Architecture
- ADR-0011 Vision Engine Architecture
- ADR-0012 Contract-First Specification-Driven Development
