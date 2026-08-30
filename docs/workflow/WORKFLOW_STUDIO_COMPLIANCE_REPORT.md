# Workflow Studio Compliance Report

> Component: Atlas Workflow Studio and Desktop execution integration
> Updated: 2026-08-24
> Status: Alpha; deterministic Runtime integration verified, live-provider acceptance pending

## Executive status

The Sprint 13 visual editor is no longer described as fully compliant merely because UI types and placeholders exist. Sprint 15.2 connects the editor to the real Python Workflow Runtime through Tauri. The deterministic core execution path and the AI, Vision, and Plugin integration boundaries are implemented and tested. Claims below distinguish implemented behavior from partial or pending behavior.

| Boundary | Status | Evidence |
|---|---|---|
| Editable graph remains data | Pass | Workflow Zustand store and canonical serializer |
| React performs no native node execution | Pass | `executor-service.ts` calls typed IPC only |
| Persistent Python Runtime host | Pass | `src/atlas_workflow/host.py`, Tauri `WorkflowHostManager` |
| Nine lifecycle commands | Pass | Tauri command registration and Desktop IPC bridge |
| Canonical manifest mapping | Pass | `runtime-serialization.ts`; nodes, ports, edges, variables, metadata, capabilities, plugins |
| Deterministic DAG order | Pass | immutable graph topological order in `ExecutionEngine` |
| Real edge values | Pass | source-port to target-port propagation and integration tests |
| Typed-port validation | Pass for current canonical types | Workflow validator compatibility rules |
| Condition branch skipping | Pass | inactive branch nodes emit `NodeSkipped` |
| Runtime variables | Pass for current host scopes | Runtime-authoritative state and `VariableChanged` events |
| Pause/resume/step/stop/restart | Pass | shared `ExecutionControl`, host commands, lifecycle tests |
| Node breakpoint | Pass | breakpoint set included in start request and enforced by Runtime control |
| Runtime event bridge | Pass | `workflow://runtime-event`, execution/workflow/node correlation |
| Output and node inspection | Pass | structured result panel and Properties runtime result section |
| AI integration boundary | Pass; live provider pending | Workflow host bridge request → existing Tauri AI host |
| Vision integration boundary | Pass; multimodal provider pending | Workflow host bridge request → existing native capture command |
| Plugin node integration | Pass for repository test provider | Node Registry + Plugin Bridge deterministic node |
| Durable execution-history persistence | Pending | in-memory bounded history only |
| Checkpoint/resume UI | Pending | not required for basic execution acceptance |
| Secure provider credential vault | Pending | inherited Sprint 15.1 limitation |

## Active architecture

```text
Workflow Studio
  -> WorkflowExecutionService
  -> Tauri workflow_* command
  -> WorkflowHostManager
  -> persistent atlas_workflow.host
  -> WorkflowRuntime / ExecutionEngine
  -> NodeRegistry / PluginBridge
  -> Core or AI/Vision/Plugin bridge
  -> workflow://runtime-event and result
  -> execution/debug/variable stores and inspectors
```

The editable graph is not mutated by Runtime events. Execution state is normalized separately and merged only for rendering. Browser development mode reports the native Runtime as unavailable; simulation is explicitly labeled and never returned as a Runtime result.

## Command coverage

| Command | Implemented behavior |
|---|---|
| `workflow_validate` | Parse, validate, compile, and return deterministic plan/errors |
| `workflow_start` | Create a unique execution and start it asynchronously |
| `workflow_pause` | Pause the backend execution control |
| `workflow_resume` | Continue the same execution |
| `workflow_stop` | Cancel the backend control and active cancel-aware node |
| `workflow_step` | Release one Runtime scheduling step |
| `workflow_restart` | Create a new execution ID from the stored manifest |
| `workflow_get_state` | Return authoritative lifecycle, nodes, results, variables, metrics |
| `workflow_get_result` | Return result, state, and bounded event history |

## Initial executable node scope

- Core: Entry, Exit, Constant, Transform/Map, Condition, Delay, Output, Set Variable, Get Variable, No-op.
- AI: AI Inference and the legacy alias, normalized through the existing AI Runtime host.
- Vision: Current Frame and the legacy alias, routed through existing Tauri capture.
- Plugin: deterministic repository-owned test node through the Runtime Plugin Bridge.

Palette node types outside this initial scope remain design-time catalog entries and are not claimed as executable. Unsupported nodes fail explicitly during validation or execution rather than succeeding as placeholders.

## Security and reliability

- Result/event payload keys that look like API keys, authorization, credentials, secrets, or tokens are masked in the Python host.
- Provider credentials are not stored in Zustand or workflow definitions.
- Each request and execution has a correlation identifier.
- Runtime history is capped at 500 events per execution.
- Malformed and unknown host requests return structured errors without killing the persistent process.
- One failed execution does not prevent a later valid execution.

## Verification snapshot

| Suite/check | Result |
|---|---:|
| Root Workflow/Conformance Python | 294 passed |
| Focused Desktop Workflow host integration | 5 passed (included above) |
| AI Runtime/host Python | 109 passed |
| Vision Runtime Python | 185 passed |
| Desktop Vitest | 125 passed |
| Desktop TypeScript | Pass |
| Desktop ESLint | Pass |
| Desktop production build | Pass |
| Tauri Rust fmt/check/test | Pass |

The backend acceptance proves `Constant("Atlas")` is propagated through an edge and returned from the output. Additional integration coverage proves true/false branch skipping, cancellation, pause/step/resume, restart with a new ID, malformed-request recovery, typed mismatch rejection, AI request normalization, and Plugin Bridge execution.

The running Tauri desktop acceptance imported `sample-workflow-execution.json`, executed it through F5, rendered all five nodes as completed from Runtime events, and displayed the backend execution ID, success status, and `HELLO FROM ATLAS WORKFLOW RUNTIME` value in the React Output panel.

## External acceptance

Live-provider AI and Vision→multimodal AI workflow acceptance is pending. The integration boundary exists, but no usable provider credential/model was available: the previously configured OpenAI credential returned HTTP 401 and Ollama was not running. No Demo Provider or fabricated response is counted as live acceptance.

## Conclusion

Sprint 15.2 infrastructure and deterministic backend acceptance are implemented. The overall Workflow Studio remains alpha, not “all RFCs complete”: durable execution persistence, advanced checkpoint UX, broader node executors, Project Runtime resolution, plugin permission/health expansion, secure credentials, and live-provider E2E remain follow-up work.
