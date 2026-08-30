# Sprint 15.2 Workflow Execution Integration Report

> Date: 2026-08-24
> Release line: 0.15.0-alpha
> Verdict: Deterministic execution integration complete; live-provider acceptance pending externally

## Delivered

Sprint 15.2 replaces the Workflow Studio's visual-only execution boundary with a persistent native Runtime chain:

```text
React graph -> TypeScript service -> Tauri IPC -> persistent Python host
-> Workflow Runtime -> Execution Engine -> Node Registry / Plugin Bridge
-> result and Runtime events -> Tauri -> React
```

All required native commands are present: validate, start, pause, resume, stop, step, restart, get state, and get result. The Desktop serializer maps the existing Studio definition to the existing canonical Workflow manifest rather than creating a Desktop-only schema.

## Runtime semantics verified

- Immutable graph compilation and deterministic topological execution.
- Source-port to target-port value propagation with default and missing-input handling.
- Type validation for primitives, numeric compatibility, generic values, frame/image references, Knowledge references, and AI response values.
- True/false condition selection and explicit `NodeSkipped` state for inactive paths.
- Runtime-authoritative variables and variable-change events.
- Unique execution IDs, correlated commands/events/results, bounded history, metrics, and structured errors.
- Backend cancellation, pause/resume, node breakpoint, one-step scheduling, and restart with a new execution.
- Core node executors plus AI, Vision, and Plugin integration boundaries.

## Desktop behavior

- Toolbar, Run menu, shortcuts, and command palette route through the central command registry.
- Node and edge visuals are driven by Runtime state.
- Debugger, variable inspector, Output panel, and selected-node Properties use backend events/results.
- Browser development fails safely with Runtime unavailable; simulation stays separate.
- Output can be copied or exported and secret-like metadata is masked before IPC.

## Acceptance evidence

The repository sample `sample-workflow-execution.json` represents:

```text
Entry -> Constant("Hello from Atlas Workflow Runtime")
      -> Uppercase Transform -> Output -> Exit
```

The focused Python host test executes the same canonical path without mocks and verifies edge-propagated output. A second acceptance uses `Constant("Atlas")` and asserts the final Runtime output is `Atlas`. Branch, lifecycle, AI bridge, plugin, error, and recovery behavior are also automated.

The full native desktop acceptance also passed in the running Tauri application. The sample was imported in Workflow Studio, F5 routed through the command registry, Tauri started the persistent Python host, all five nodes changed to `completed` from Runtime events, and the React Output panel displayed execution `execution-02b2ae83-db63-4a96-922f-77cc1515f865` with `success: true` and `{"value":"HELLO FROM ATLAS WORKFLOW RUNTIME"}`. This proves the required React → Tauri → Python → Runtime → events/result → React loop rather than only a direct host test.

## Quality gates

- Root Python: 294 passed.
- AI Python: 109 passed.
- Vision Python: 185 passed.
- Desktop: 125 passed; TypeScript, ESLint, and production build pass.
- Rust/Tauri: fmt, check, and test pass with the MSVC toolchain.

## Pending external/follow-up work

- Live AI node acceptance (`ATLAS_OK`) and Vision→multimodal AI require a usable real provider credential/model.
- Secure credential storage remains pending from Sprint 15.1.
- Durable execution-history policy and advanced checkpoint/resume UX are not part of the initial integration.
- Broader palette node execution, full Project Runtime resolution, and expanded plugin permission/version/health adapters are future increments.

The sprint is therefore complete for the deterministic Runtime integration boundary, but not declared complete for live-provider AI/multimodal acceptance.
