# Atlas Project Knowledge

Atlas has two deliberately different knowledge concepts:

- Knowledge Packs are immutable, versioned, distributable assets governed by
  ADR-0007.
- Project Knowledge is mutable user/workflow/vision data governed by the Sprint
  16 Knowledge Runtime and ADR-0013.

## Canonical entry

Every Runtime entry has a stable ID and project ID, one of four types (`note`,
`document`, `fact`, `observation`), title, text content, JSON metadata, tags,
source, provenance, timestamps, and an incrementing version. The canonical JSON
contract is `contracts/json/knowledge.schema.json`.

## Ownership and persistence

The persistent Python Knowledge Runtime is the source of truth. It stores each
project independently at `.atlas/knowledge.v1.json` using atomic replacement and
a backup recovery file. Workspace layout and active workspace continue to use
the existing project-assets service, but knowledge entries do not.

Project identity is a stable hash of the normalized project path, so reopening a
project selects the same Runtime namespace. Runtime scope contains both the
stable project ID and the absolute project root; a stored file declaring another
project ID is rejected.

## Retrieval

Sprint 16 implements deterministic lexical retrieval. All normalized query terms
must match title, content, or tags. Ranking favors title and tag matches and adds
a phrase-match bonus. Requests are capped at 100 results; the Studio currently
requests 25. Returned scores are raw ranking values, never percentages.

Each response includes a request/correlation ID, method, candidate and result
counts, filters, matched terms, excerpts, references, and elapsed time. The
Retrieval Inspector exposes this trace. Because the backend is local,
synchronous, and bounded, it does not expose cancellation; the UI still rejects
late responses with a monotonic request sequence.

## Import and export

TXT and Markdown import as one document. JSON accepts an entry array or an
object containing `entries`; CSV maps columns such as title, content/text, type,
and tags. Imports are validated as one batch before the atomic save. Duplicate
content is allowed and receives a new ID; duplicate stable IDs are rejected.
Only the portable filename, format, import time, source hash, and record index
are retained as source/provenance.

JSON and Markdown export are supported through Runtime-owned data. The Studio
downloads the returned content locally.

## Workflow, Vision, and AI

Workflow nodes `knowledge_write`, `knowledge_search`, `knowledge_validate`, and
`knowledge_operation` execute inside the existing persistent Python host. Their
scope comes from the execution session's project context. Vision OCR outputs can
flow directly into `knowledge_write`; the entry records `vision_ocr`, workflow,
node, and frame provenance.

The Studio adds only a typed reference and short preview to AI Context. At
inference time, Tauri/Workflow resolves same-project references through
Knowledge Runtime and passes transient content to the AI Runtime. The AI Runtime
injects that context at the provider-request boundary and returns reference IDs
in response metadata. Canonical content is not copied into frontend state or
persisted in AI Studio assets.

## Deliberately deferred

Semantic/vector search, embeddings, relations, graph views, collections,
entities, cloud sync, collaboration, and Knowledge Pack installation remain
future work. The Studio does not show fake controls for these capabilities.
