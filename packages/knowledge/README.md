# Atlas Knowledge Runtime

`packages/knowledge` is the authoritative Python runtime for mutable,
project-owned Atlas knowledge. It is intentionally separate from immutable,
installable Knowledge Packs described by ADR-0007.

## Runtime boundary

- Canonical entries: note, document, fact, and observation
- Project-scoped CRUD with incrementing entry versions
- Atomic JSON persistence at `.atlas/knowledge.v1.json`, plus a recovery backup
- Deterministic bounded lexical search with raw ranking scores and trace metadata
- TXT, Markdown, JSON, and CSV import; JSON and Markdown export
- Typed references for Workflow and AI Context integration
- Mutation, import, retrieval, and health telemetry

The desktop never owns canonical knowledge. React/Zustand state is a display and
draft cache; all reads and mutations cross Tauri into the persistent Python host.

## Development

From the repository root:

```powershell
$env:PYTHONPATH='packages/knowledge/src'
python -m pytest -q packages/knowledge/tests
```

## Security and portability

Storage paths are derived from a validated project scope. Imported source paths
are reduced to portable filenames, credential-shaped metadata keys are rejected,
and AI requests resolve only same-project typed references at the Runtime
boundary. Knowledge data is offline and provider-independent.

Semantic/vector search, relations/graph editing, cloud sync, and Knowledge Pack
installation are not implemented in Sprint 16.
