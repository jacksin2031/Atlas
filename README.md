# Atlas Workflow Runtime

**Reference Implementation** — Python 3.10+

The Atlas Workflow Runtime transforms declarative workflow definitions into executable runtime graphs. This is the **Python reference implementation**; the production implementation targets Rust.

## Architecture

`
Atlas Architecture
       ↓
    RFCs (specification)
       ↓
Reference Implementation (Python) ← you are here
       ↓
Production Implementation (Rust)
       ↓
Integration Tests
       ↓
Conformance Tests
`

## Structure

`
src/atlas_workflow/     Reference implementation
tests/                   Unit + integration tests (237 passing)
docs/                    Architecture, compliance, strategy
specs/workflow/          RFC specifications
`

## Quick Start

`python
from atlas_workflow.runtime import WorkflowRuntime

runtime = WorkflowRuntime()
manifest = runtime.create_manifest({
    "metadata": {"name": "my-workflow"},
    "nodes": [{"id": "start", "type": "noop", "ports_out": [], "ports_in": []}],
    "edges": [],
    "entry_nodes": ["start"],
    "exit_nodes": ["start"],
})
graph = runtime.compile(manifest)
instance = runtime.create_instance(graph, inputs={})
result = runtime.execute(instance)
`

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — Module structure and design principles
- [Compliance Report](docs/COMPLIANCE_REPORT.md) — RFC-by-RFC requirement traceability
- [Implementation Strategy](docs/IMPLEMENTATION_STRATEGY.md) — Reference vs. Production distinction

## Tests

`ash
python -m pytest tests/ -v
`

237 tests, 0 failures.

## License

MIT
