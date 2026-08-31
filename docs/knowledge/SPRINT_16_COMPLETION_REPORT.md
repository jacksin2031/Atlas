# Atlas Sprint 16 — Knowledge Studio & Runtime Integration

Date: 2026-08-31

Current verdict: **SPRINT 16: PARTIAL**

The implementation and every automated mandatory scenario pass. Real Tauri
steps 1–10 pass, including create, read, update, search, a process restart, and
Version 2 recovery. The final destructive UI step (delete the disposable entry
and verify deletion after another restart) is awaiting the required action-time
Windows UI confirmation. This report must not be changed to COMPLETE until that
step passes.

## 1. Sprint 16 Initial Audit

The audit was performed against the frozen source before implementation.

| Area | Existing | Complete | Reusable | Missing |
| --- | --- | --- | --- | --- |
| Knowledge Runtime | `packages/knowledge` placeholder | No | Package boundary | Models, CRUD, search, persistence, events, health, host |
| Knowledge RFCs | ADR-0007 Knowledge Pack decision; empty `specs/knowledge/README.md` | Pack architecture only | Immutable/non-executable pack boundary | Mutable project-knowledge decision and contracts |
| Storage RFCs/runtime | Extensive RFCs and Rust Storage crate | General Rust contracts complete; no Python Knowledge adapter | Provider/backup/recovery principles | Runtime-accessible project Knowledge adapter |
| Project Runtime/persistence | Sprint 15.5 project assets/session and recovery | Yes for layouts/assets | Stable project directory, atomic project persistence | Stable project ID across reopen; dedicated Knowledge storage |
| Workflow Knowledge Operation | Registry placeholder | No | Workflow compiler, node registry, persistent host | Real ports, handlers, typed outputs, project scope |
| AI Runtime context | Real AI host/bridge and Context Inspector | Complete for existing context types | Transient request assembly, provider boundary | Knowledge reference resolution and injection |
| Vision/OCR | Capture, native OCR, controlled result path, typed references | Yes | OCR text, frame and reference contracts | Knowledge write/provenance path |
| Knowledge APIs/models | Empty JSON schema; no canonical mutable entry | No | Contract folder | Entry/reference/event/search models and schema |
| Search/index | None for mutable project knowledge | No | None | Deterministic project-scoped retrieval and lifecycle |
| Entity/relationship model | Knowledge Pack prose only | No | None | Not implemented; therefore no production graph UI |
| Import/export | None | No | Browser native file-selection behavior | Safe text formats, validation, provenance and export |
| Runtime events/health | Workflow/AI event patterns | No for Knowledge | Tauri event forwarding and Studio status patterns | Knowledge event taxonomy and real health |
| IPC/Tauri host | Persistent Python Workflow host and AI host | Yes | Long-lived process, request correlation, failure handling | Knowledge commands and event routing |
| Desktop workspace | WorkspaceManager, FlexLayout, panel/command registries | Yes | Entire generalized Studio shell | Knowledge workspace, layout, panels and commands |
| Tests/docs | 1,074 frozen tests; placeholder Knowledge docs | Baseline complete | Regression suites and acceptance style | Focused Runtime/Desktop/IPC/E2E coverage and docs |

The audit found no implemented semantic/vector backend, entity graph,
relationship contract, confidence model, or Knowledge Pack installer. Sprint 16
does not claim or simulate those capabilities.

## 2. Baseline commit and tag

- `HEAD` before Sprint 16 work: `1f2d0480a618e9c3fda314a24a9091c9a431f02d`
- Frozen tag: `v0.15.0-alpha`
- `git merge-base --is-ancestor 1f2d048 HEAD`: PASS
- Frozen tag/history changed: No
- Baseline regression before implementation: 310 root Python, 110 AI
  Python, 185 Vision Python, 135 Desktop, 329 root Rust, 5 Tauri Rust;
  total 1,074

## 3. Architecture

```text
Knowledge Studio (display cache + unsaved drafts only)
        |
        | KnowledgeStudioService
        v
typed Tauri commands <------------------------------+
        |                                            |
        v                                            |
existing persistent Python host                     |
  +-- KnowledgeRuntime -- KnowledgeStorage           |
  |       |                  |                       |
  |       +-- lexical search +-- project/.atlas/knowledge.v1.json
  |       +-- events/health      + .bak recovery     |
  |       +-- typed references                       |
  +-- Workflow Runtime -- Knowledge integration -----+
  +-- Vision/OCR ------ provenance-aware writes -----+
  +-- AI bridge ------- transient reference context --> AI Runtime --> provider
```

React/Zustand holds lists, search results, selection, health, events, and editor
drafts for display. The Python Runtime remains authoritative and reloads storage
for every operation. Workflow, AI, and Vision use Runtime APIs rather than
frontend state or direct storage access.

## 4. Existing functionality reused

- Existing persistent Workflow Python-host lifecycle and Tauri request bridge
- Existing independent AI Python host and provider request boundary
- Sprint 15 Vision/OCR controlled and native paths plus typed frame references
- Sprint 15.5 project asset/layout backup and recovery architecture
- WorkspaceManager, FlexLayout, Panel Registry, Command Registry, menu, toolbar,
  status bar, Atlas Design System and shared panels
- Existing Workflow compiler/executor, plugin bridge, node registry and events
- Existing AI Context Inspector and project asset persistence

## 5. Files created

- `apps/atlas-desktop/src/studio/knowledge/__tests__/knowledge-store.test.ts`
- `apps/atlas-desktop/src/studio/knowledge/commands.ts`
- `apps/atlas-desktop/src/studio/knowledge/components.tsx`
- `apps/atlas-desktop/src/studio/knowledge/index.ts`
- `apps/atlas-desktop/src/studio/knowledge/service.ts`
- `apps/atlas-desktop/src/studio/knowledge/store.ts`
- `apps/atlas-desktop/src/studio/knowledge/types.ts`
- `docs/adr/0013-project-knowledge-runtime.md`
- `docs/knowledge/SPRINT_16_COMPLETION_REPORT.md`
- `packages/knowledge/pyproject.toml`
- `packages/knowledge/src/atlas_knowledge/__init__.py`
- `packages/knowledge/src/atlas_knowledge/errors.py`
- `packages/knowledge/src/atlas_knowledge/models.py`
- `packages/knowledge/src/atlas_knowledge/runtime.py`
- `packages/knowledge/src/atlas_knowledge/storage.py`
- `packages/knowledge/tests/test_runtime.py`
- `tests/integration/test_knowledge_workflow.py`

## 6. Files modified

- `apps/atlas-desktop/src-tauri/src/lib.rs`
- `apps/atlas-desktop/src/components/layouts/AppLayout.tsx`
- `apps/atlas-desktop/src/components/layouts/MenuBar.tsx`
- `apps/atlas-desktop/src/components/layouts/StatusBar.tsx`
- `apps/atlas-desktop/src/components/layouts/Toolbar.tsx`
- `apps/atlas-desktop/src/ipc/bridge.ts`
- `apps/atlas-desktop/src/services/project-assets.ts`
- `apps/atlas-desktop/src/services/project.ts`
- `apps/atlas-desktop/src/studio/ai/commands.ts`
- `apps/atlas-desktop/src/studio/workflow/__tests__/services/project-assets.test.ts`
- `apps/atlas-desktop/src/studio/workflow/stores/node-registry-store.ts`
- `apps/atlas-desktop/src/styles/global.css`
- `apps/atlas-desktop/src/workspace/WorkspaceManager.tsx`
- `apps/atlas-desktop/src/workspace/__tests__/workspace-layout.test.ts`
- `apps/atlas-desktop/src/workspace/layouts.ts`
- `apps/atlas-desktop/src/workspace/panel-registry.tsx`
- `apps/atlas-desktop/src/workspace/types.ts`
- `contracts/json/knowledge.schema.json`
- `docs/knowledge/knowledge.md`
- `packages/ai/src/atlas_ai/host.py`
- `packages/ai/tests/test_host.py`
- `packages/knowledge/README.md`
- `src/atlas_workflow/host.py`

Generated `.tsbuildinfo`, tracked Python cache files, pre-existing temporary JSON,
and unrelated acceptance artifacts are not Sprint 16 source changes and are not
included in these lists.

## 7. Files removed

None.

## 8. Knowledge Runtime changes

The new canonical immutable entry model supports `note`, `document`, `fact`, and
`observation`, with stable/project IDs, title, content, JSON metadata, tags,
source, provenance, timestamps and incrementing version. The Runtime provides
CRUD, bounded list, deterministic lexical search, import, export, events, health,
and AI context assembly. Errors carry stable `KNOWLEDGE_VALIDATION`,
`KNOWLEDGE_NOT_FOUND`, or `KNOWLEDGE_STORAGE` codes through the host error
boundary. A malformed request does not terminate the host.

## 9. Knowledge Studio

Knowledge is a fourth first-class workspace alongside Workflow, Vision, and AI.
It uses the existing shell and has real loading, empty, unavailable, error, dirty
and saved states. Browser/Vite mode never substitutes localStorage; native calls
fail visibly when the Tauri backend is absent.

## 10. Workspace and layout

The `knowledge` WorkspaceId has its own versioned FlexLayout model with Explorer,
Editor, Search, Retrieval, Activity, Health, Metadata/Provenance and Import.
Project assets save and recover this layout independently from Workflow, Vision
and AI. Existing backup/recovery behavior is reused. Active workspace restoration
includes Knowledge.

## 11. Explorer

The Explorer lists only real project Runtime entries, bounded to 100 per refresh.
It supports filtering, selection, refresh, create, editor open, context menu,
typed AI reference addition, deletion with confirmation, and empty-state Create/
Import actions. It exposes only entry/type/tag/source concepts supported by the
Runtime.

## 12. Search and retrieval inspector

Search accepts query, project, types, tags, limit, and request ID at the Runtime
contract. All query terms must match title/content/tags. Results contain title,
excerpt, type, source, tags, reference, matched terms and a raw deterministic
ranking score. The UI labels scores as raw values, never percentages.

The Retrieval Inspector shows query, lexical method, candidates, selected count,
filters, timing, IDs, scores and references. A monotonic frontend sequence plus
echoed request ID prevents late result overwrite. Runtime results are capped at
100 and Studio searches at 25. The synchronous local backend does not expose
search cancellation because it is bounded and not long-running.

## 13. Editor

Create/update calls go through Runtime IPC. The Runtime response replaces the
display cache. Title, type, content, tags and structured metadata are editable.
Dirty/saved state is explicit, switching selection prompts before discarding,
metadata must be a JSON object, and deletion is confirmed.

## 14. Metadata and provenance

The inspector shows stable and project IDs, type, version, timestamps, source,
provenance and metadata. Content SHA-256 is stored as provenance. Workflow writes
record workflow and node IDs. Vision OCR writes additionally record the frame
reference. Imports record portable filename, format, import timestamp, source
hash and record index.

## 15. Relationships and graph

**NOT APPLICABLE in Sprint 16.** No canonical mutable relationship/entity
contract or graph storage was present in the audited Runtime. No fake relationship
controls or second graph database were added. ADR-0007 Knowledge Pack prose is
not treated as an implemented project-knowledge graph contract.

## 16. Import and export

The Import panel uses the WebView file input, which invokes the native system
picker in Tauri, previews text, accepts TXT/Markdown/JSON/CSV only, and sends file
content plus a portable filename—not an unrestricted path—to Runtime. JSON/CSV
records are batch-validated before one atomic save. Duplicate content is allowed
with new IDs; duplicate IDs are rejected; nothing is silently overwritten.

Runtime export supports JSON and Markdown. Exported data contains only Knowledge
entries and supported metadata/provenance; credential-shaped metadata is rejected
at model validation.

## 17. Index lifecycle

Sprint 16's index is deterministic lexical retrieval over authoritative storage,
not a separately persisted stale cache. Create/import become visible after the
atomic save; update replaces current content/version; delete removes the entry;
reload/restart reads the same project file. Tests prove no old Version 1 marker
or deleted marker remains searchable and repeated searches preserve identity.

## 18. Project ownership and persistence

Project IDs are stable FNV-1a hashes of normalized, case-insensitive project
paths rather than random per-open IDs. Every entry and reference carries the
project ID; every operation also carries the absolute project root. Storage
rejects a file whose declared project ID differs. AI reference assembly rejects
cross-project references. Project A/B isolation is a mandatory passing test.

Knowledge data lives in dedicated Runtime storage, not
`.atlas/project-assets.v1.json`. Project assets retain only appropriate layout,
active workspace, and AI reference/display state.

## 19. Storage integration and recovery

`KnowledgeStorage` is the Runtime storage abstraction; the initial
`JsonProjectKnowledgeStorage` adapter writes `.atlas/knowledge.v1.json`. Writes
use a same-directory temporary file, flush, `fsync`, backup, then atomic replace.
Reads recover the primary from a valid backup. Both-corrupt files return a
structured storage error. Paths are resolved beneath the validated project root.

The existing Rust Storage Runtime is not directly callable from the persistent
Python host; replacing the JSON adapter with a cross-runtime Storage provider is
a future adapter change, not a Studio/API redesign.

## 20. IPC commands and events

Implemented Tauri commands:

- `knowledge_activate`
- `knowledge_status`
- `knowledge_list`
- `knowledge_get`
- `knowledge_create`
- `knowledge_update`
- `knowledge_delete`
- `knowledge_search`
- `knowledge_import`
- `knowledge_export`
- `knowledge_events`

An internal `knowledge_context` host command resolves AI references. Runtime
events flow as `knowledge://runtime-event` through host, Tauri listener, service,
and Studio. Events include entry create/update/delete, search completion and
import start/completion/failure. Events are bounded to 500 per project and carry
correlation IDs without content or credentials.

## 21. Persistent Runtime host and reliability

KnowledgeRuntime is instantiated once inside the existing persistent Python
Workflow host; no Python process is spawned per operation. Host stdin parsing,
pending request correlation, stderr isolation, and unexpected-exit handling are
reused. Focused tests cover invalid query/failure followed by a successful
command, missing/corrupt storage, invalid project/model data and request IDs.

## 22. Workflow integration

Real Workflow nodes now include `knowledge_search`, `knowledge_write`,
`knowledge_validate`, and multi-operation `knowledge_operation` (get/search/
query/create/write/update/delete). Ports use typed Knowledge entry/reference/
result types. The handler obtains scope from the Workflow execution session's
`projectContext`; it never queries Studio/Zustand.

The deterministic real Runtime workflow is:

```text
Entry -> Knowledge Write -> Knowledge Search -> Knowledge Validate -> Exit
```

It writes KRT-1600, searches it, validates content/project ownership and returns
`success: true`.

## 23. Vision/OCR integration

The OCR Workflow handler now exposes recognized text, provider result and frame
alongside typed region/bounds/point references. `knowledge_write` detects OCR
provider output and persists an observation with `source.type = vision_ocr`,
workflow/node IDs and only `frame_reference`, never raw screenshot/base64.

The controlled real Workflow Runtime test runs:

```text
Entry -> controlled Vision OCR -> Knowledge Write -> Search -> Validate -> Exit
```

`ATLAS KNOWLEDGE VISION TEST` is stored, retrieved, validated and returns
`success: true` without external AI.

## 24. AI context integration

Studio stores a typed `knowledgeReference`, label/source and at most a 220-character
display preview in AI Context. It does not copy canonical content into AI project
assets. The project activates the Knowledge scope independently of which Studio
is open.

At inference, Tauri selects only context items explicitly typed as Knowledge,
resolves them through KnowledgeRuntime with same-project validation, and attaches
transient context. The AI Runtime converts this to a system context message at
the provider request boundary and returns reference IDs/count in response
metadata. Tests prove `ORANGE CAPYBARA` reaches the provider request body and the
typed reference reaches both direct and Workflow AI boundaries.

## 25. Security

- Credential-shaped keys (`api_key`, authorization, bearer, credential,
  password, secret, token after normalization) are rejected recursively.
- No credential vault, environment, provider secret, or hidden reasoning is
  persisted or emitted.
- Frontend import sends selected content and portable filename only.
- Project paths are absolute, existing project directories and storage is fixed
  below `.atlas`; storage-file project IDs must match scope.
- AI and Workflow reference resolution enforces same-project ownership.
- Content is capped at 2 MB; list/search/event limits are bounded.
- AI output is never auto-persisted. Persistence requires an explicit Studio or
  Workflow mutation.
- Opening Knowledge Studio does not touch Input arming, focus policy, emergency
  stop, or permissions.

## 26. Automated tests and exact counts

All executed suites pass with zero failures:

| Suite | Sprint 15 | Sprint 16 | Result |
| --- | ---: | ---: | --- |
| Root Python (Workflow/Input/integration) | 310 | 314 | PASS |
| AI Python | 110 | 111 | PASS |
| Vision Python | 185 | 185 | PASS |
| Knowledge Python | — | 19 | PASS |
| Desktop Vitest | 135 | 141 | PASS |
| Root Rust workspace | 329 | 329 | PASS |
| Tauri Rust | 5 | 7 | PASS |
| **Total** | **1,074** | **1,106** | **PASS (+32)** |

Knowledge tests cover CRUD, versioning, deterministic search, stale-update/delete
visibility, restart, project isolation, primary/backup corruption, provenance,
credential rejection, malformed records, TXT/Markdown/JSON/CSV import, JSON/
Markdown export, bounded listing, events, AI context and health. Desktop tests
cover store/dirty/search behavior, request race protection, command registration,
workspace/panels/layout and stable project identity. Rust tests cover scoped
correlated payloads and AI Knowledge reference selection.

## 27. TypeScript, ESLint, Python and Rust quality gates

- `pnpm typecheck`: PASS, 0 TypeScript errors
- `pnpm lint`: PASS, 0 ESLint errors/warnings
- All four Python invocations above: PASS
- Root `cargo fmt --all -- --check`: PASS
- Tauri `cargo fmt --all -- --check`: PASS
- Tauri `cargo check` using installed `stable-x86_64-pc-windows-msvc`: PASS
- Root `cargo test --workspace`: PASS, 329
- Tauri `cargo test`: PASS, 7

The machine's default GNU Rust toolchain lacks `dlltool`; the correct installed
MSVC toolchain was used for Windows Tauri check/test. This is an environment
toolchain condition, not a source warning or skipped gate.

## 28. Production build

`pnpm build`: PASS. Vite transformed 385 modules. Output was:

- `index.html`: 0.62 kB (0.34 kB gzip)
- CSS: 117.45 kB (14.18 kB gzip)
- flow-engine: 178.18 kB (58.36 kB gzip)
- main: 336.73 kB (93.94 kB gzip)
- layout-engine: 366.11 kB (105.79 kB gzip)

No graph/search dependency was added and no chunk advisory was emitted.

## 29. Real Tauri acceptance

Executed against the real MSVC Tauri application and a disposable project at
`.acceptance/sprint16-real-tauri`, using the Windows app UI rather than browser
mode.

| Step | Evidence | Result |
| --- | --- | --- |
| Open Knowledge Studio | Dedicated FlexLayout workspace rendered | PASS |
| Runtime health | `available`, lexical index `ready`, 0 initial entries | PASS |
| Create/save | “Real Tauri Acceptance” persisted as Runtime entry v1 | PASS |
| Search | `REAL_TAURI_KNOWLEDGE_1600` returned 1/1, score 6 | PASS |
| Open/edit/save | Content gained `EDITED_1600`; entry became v2 | PASS |
| Restart process/project | App reopened same project and listed v2 | PASS |
| Read after restart | Editor showed Version 2 edited content and metadata | PASS |
| AI Context Inspector | Knowledge category showed 1 typed reference/title | PASS |
| Delete disposable entry | Requires action-time Windows UI confirmation | NOT EXECUTED — ENVIRONMENT LIMITATION |
| Restart/search deletion | Blocked on preceding confirmation | NOT EXECUTED — ENVIRONMENT LIMITATION |

Automated Runtime acceptance independently proves delete persistence after a new
Runtime instance, but it does not replace the two mandatory real-UI steps.

## 30. Mandatory scenario results

- K-A CRUD: automated PASS; real Tauri create/read/update PASS, delete pending
  confirmation.
- K-B Search: PASS automated and real Tauri.
- K-C Persistence: PASS automated and real Tauri (Version 2 after restart).
- K-D Project Isolation: PASS automated; Project B returns zero Project A secret
  results.
- K-E Workflow Integration: PASS through real Workflow Runtime.
- K-F Vision/OCR Integration: PASS through controlled OCR and real Workflow
  Runtime.
- K-G AI Context Boundary: PASS through Tauri/Workflow/AI Runtime request
  construction. Live provider response not claimed.
- K-H Regression: PASS; 1,106 tests, zero failures, production build and quality
  gates pass.

## 31. Live RAG and external pending conditions

The real desktop showed no healthy configured provider/model. Therefore:

```text
Knowledge Retrieval Integration: PASS
Live RAG Acceptance: PENDING EXTERNAL CONDITION
Knowledge + multimodal AI response: PENDING EXTERNAL CONDITION
```

No provider, model or request ID exists to record, and no live response success
is claimed.

## 32. Sprint 15 regression

All frozen deterministic suites remain at or above their prior counts. Root Rust
remains 329, Vision remains 185, Input/Workflow/root Python increased to 314, AI
increased to 111, Desktop increased to 141, and Tauri increased to 7. Dynamic
plugin registration tests, Input safety/emergency behavior, Vision capture/
detection/template/OCR tests, Workflow real execution and AI host boundary all
pass. The frozen tag remains unchanged.

## 33. Known limitations

- Mutable relationships/entities/collections/graph are not implemented because
  the audited Runtime had no canonical contract.
- Retrieval is lexical only; semantic/vector retrieval and embeddings are not
  claimed.
- The JSON adapter is appropriate for bounded project-local knowledge, not a
  large collaborative corpus.
- Activity events are process-memory telemetry (bounded to 500); canonical entry
  data persists, but the event feed itself is not a durable audit ledger.
- Import supports text-based TXT/Markdown/JSON/CSV only. PDF/binary OCR import is
  intentionally rejected.
- Duplicate content is allowed; there is no content-hash deduplication UI.
- Search is bounded/synchronous, so no backend cancellation endpoint exists.
- Live RAG and multimodal provider acceptance require a healthy external model.
- Real Tauri destructive deletion is awaiting explicit action-time confirmation.

## 34. Final acceptance matrix

| Capability | Automated | Real Tauri | Persistence | Integration | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Knowledge CRUD | PASS | delete pending | PASS | PASS | NOT EXECUTED — ENVIRONMENT LIMITATION |
| Search | PASS | PASS | PASS | PASS | PASS |
| Indexing | PASS | PASS | PASS | PASS | PASS |
| Project Isolation | PASS | NOT APPLICABLE | PASS | PASS | PASS |
| Knowledge Studio | PASS | PASS | PASS | PASS | PASS |
| Workflow -> Knowledge | PASS | NOT APPLICABLE | PASS | PASS | PASS |
| Vision/OCR -> Knowledge | PASS | NOT APPLICABLE | PASS | PASS | PASS |
| Knowledge -> AI Context | PASS | PASS | reference-only | PASS | PASS |
| Import/Export | PASS | NOT EXECUTED — ENVIRONMENT LIMITATION | PASS | PASS | PASS |
| Provenance | PASS | PASS | PASS | PASS | PASS |
| Relations | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE | NOT APPLICABLE |
| Sprint 15 Regression | PASS | PASS where exercised | PASS | PASS | PASS |
| Live RAG | PASS to request boundary | PENDING EXTERNAL CONDITION | NOT APPLICABLE | PASS to provider boundary | PENDING EXTERNAL CONDITION |

## 35. Final verdict and recommended next step

```text
SPRINT 16: PARTIAL
```

Reason: the implementation, automated acceptance, restart persistence and all
non-destructive real Tauri steps pass, but Definition of Done requires real Tauri
delete and post-delete confirmation. The Windows automation confirmation policy
does not permit that destructive action without an action-time user confirmation.

Recommended immediate next step: authorize deletion of the disposable “Real
Tauri Acceptance” entry, then rerun the app, search for
`REAL_TAURI_KNOWLEDGE_1600`, record zero results, update this report/matrix to
PASS, and change the verdict to `SPRINT 16: COMPLETE`.

After Sprint 16 acceptance, the recommended product step is a contract-first
decision for durable events and relationship/entity semantics before adding a
graph UI or semantic/vector backend.
