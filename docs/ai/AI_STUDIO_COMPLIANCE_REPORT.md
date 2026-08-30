# AI Studio Compliance Report

- **Sprint**: 15 — AI Studio
- **Date**: 2026-08-30
**Status**: **Sprint 15 Final Acceptance PASS**

## 1. Initial repository audit

- Desktop Shell: Tauri 2, React 19, Vite 7, Zustand 5.
- Workspaces: one `WorkspaceManager` owns independent Workflow and Vision FlexLayout models; Sprint 15 extends its `WorkspaceId`, default-layout record, registry, and versioned persistence with `ai`.
- Panels: one data-driven registry maps stable component IDs to shared or Studio-specific React components.
- Commands: `commandPaletteService` is the command registry/executor used by menus, toolbars, shortcuts, and the palette UI.
- IPC: typed functions in `src/ipc/bridge.ts` call Tauri commands. Before Sprint 15, native screen capture was the only Vision-specific Tauri command; no AI Tauri commands existed.
- Vision integration: `useVisionDocumentStore` owns the current source; native capture remains in Vision. AI consumes frame/image references and metadata, not duplicated capture code.
- AI Runtime: `packages/ai/src/atlas_ai` already defines provider/model discovery, 14 capabilities, normalized inference, prompts, conversations, four memory scopes, tools/permissions, agents, events, metrics, health, and IPC/Workflow/Vision bridge abstractions.
- Knowledge/Workflow integration: runtime interfaces exist, but there is no Desktop Knowledge bridge or safe project reference command yet.
- Reused UI: Atlas SVG icons, compact buttons/toolbars/empty states, shared Console/Problems panels, global focus styling, and existing dark workspace theme.

## 2. Existing architecture reused

No Runtime logic, layout engine, Workspace Manager, design system, native capture path, Knowledge search, tool executor, or credential store was recreated. The active path is:

```text
AI toolbar/menu/shortcut/palette
  -> Command Registry
  -> AIStudioService / Zustand UI state
  -> typed IPC bridge
  -> persistent Tauri AIHostManager
  -> JSON-lines Python host
  -> existing Python AI Runtime
  -> OpenAI-compatible or Ollama provider
```

## 3. Implementation inventory

Created under `apps/atlas-desktop/src/studio/ai/`:

- `types.ts`, `store.ts`, `service.ts`, `commands.ts`
- `components.tsx`, `AIToolbar.tsx`, `demo-adapter.ts`, `index.ts`
- `__tests__/ai-store.test.ts`, `__tests__/ai-service.test.ts`
- `README.md`

Modified:

- Workspace types/layout/registry/manager/service/store/persistence tests
- Desktop AppLayout, MenuBar, Toolbar, StatusBar, icons, CSS, IPC bridge
- Store barrel export (restored the existing `useLayoutStore` export needed by repository typecheck)
- Root and Desktop documentation/status files

Removed: none.

## 4. AI Workspace and FlexLayout

- Independent `ai` model and `atlas.layout.ai.v1` key.
- Default left, center, right, and bottom dock regions.
- Resize, dock, tab, close, maximize, persistence, corruption recovery, reset, stable component uniqueness, and Workflow/Vision/AI switching use the existing generalized workspace code.
- Command-driven panel requests are applied by the current `WorkspaceManager` model rather than a Studio-specific manager.

## 5. Provider, model, playground, prompt, and conversation

- Runtime-discovered provider/model descriptors; production lists are not hardcoded.
- Provider health, connection state, capabilities, latency, type/version, and actions.
- Capability badges and provider-filtered model selection.
- Vision input is rejected when the selected model lacks `vision`.
- Normalized request construction includes supported parameters only.
- Playground provides system prompt, context, editable multi-turn messages, input, response, Run/Stop/Retry, inspectors, copy, clear, elapsed/streaming state boundary, and accessible status/error UX.
- Prompt editor provides metadata, variable extraction, defaults, validation, compiled preview, Playground handoff, duplicate/save boundaries, and two-request comparison with output/latency/tokens/tool calls/errors and no synthetic score.
- Conversation mode supports add/edit/delete/duplicate/rerun/branch state operations.

## 6. Context, memory, tools, agents, events, and metrics

- Context Inspector counts and lists System, Conversation, Vision, Knowledge, Memory, and Tools.
- Local images and current Vision sources become reference/metadata cards; AI Studio does not call native capture.
- Knowledge items, memories, tools, invocations, agents, events, and metrics render only Runtime-supplied fields with explicit empty states.
- Tool permissions and schemas are visible. Opening the panel never invokes a tool.
- Agent trace explicitly excludes hidden reasoning.
- Missing metrics render as an em dash; cost is omitted.

## 7. IPC and security

- Added typed `ai_discover`, `ai_infer`, `ai_cancel`, and `ai_provider_action` bridge calls.
- Implemented all four Rust/Tauri commands through a persistent, request-correlated Python host process.
- Runtime `started`, `chunk`, `completed`, `cancelled`, and `failed` events are forwarded through `ai://runtime-event` and consumed incrementally by React.
- OpenAI-compatible and Ollama discovery/inference transports are implemented in the Python host, including streamed chat and Vision image payload conversion.
- Production-unavailable and provider-unhealthy states remain explicit.
- Optional development data is isolated behind `DEV && VITE_ATLAS_AI_DEMO=true` and visibly named `Demo Provider`.
- Provider credentials are resolved through the native credential boundary and are never accepted by React contracts, returned through IPC, logged, inspected, or persisted in project assets.

## 8. Tests added

- AI layout defaults, uniqueness, persistence, corruption recovery, routing, and three-Studio switching.
- Prompt extraction/compilation/validation.
- Provider filtering and Vision capability validation.
- Conversation CRUD/branching and context deduplication.
- Discovery/unavailable behavior, normalized safe request creation, inference, stop, comparison, and adapter injection.
- Runtime-event request correlation, streaming content/metrics, and Vision payload submission without retaining base64 in Zustand or the Request Inspector.
- Python host discovery, streamed inference, provider actions, usage metrics, and active cancellation against a local OpenAI-compatible protocol server.
- Existing Workflow, Vision, and Desktop Vitest coverage remains in the same suite.

## 9. Exact verification results

Commands executed from the repository snapshot:

```text
cd apps/atlas-desktop && pnpm run typecheck
cd apps/atlas-desktop && pnpm run lint
cd apps/atlas-desktop && pnpm test
cd apps/atlas-desktop && pnpm run build
cd apps/atlas-desktop/src-tauri && cargo fmt --check --manifest-path Cargo.toml
cd apps/atlas-desktop/src-tauri && cargo check --manifest-path Cargo.toml
python -m pytest packages/ai/tests -q
```

Sprint 15 final verification results:

- TypeScript: pass, 0 errors.
- ESLint: pass, 0 warnings.
- Vitest: 17 files passed, 135 tests passed.
- Production Vite build: pass; 379 modules; existing `layout-engine` and `flow-engine` chunks preserved.
- Rust fmt: pass.
- Tauri cargo check and test: pass with `stable-x86_64-pc-windows-msvc` (the default GNU toolchain lacks `dlltool.exe` on this machine).
- AI Runtime and host: 110 passed, including provider action and host transport coverage.
- Workflow/Vision/Desktop UI regressions: included in the full Vitest run and passed.
- Real Tauri window: AI Studio connected through Tauri to the Python host, discovered OpenAI, routed Connect without `unavailable`, and reported the external endpoint as unhealthy. No fake response was substituted.
- Browser fallback: AI workspace rendered with the explicit Runtime-unavailable state and without a render/subscription loop.
- Vision boundary: automated tests confirm the current frame data is attached to the IPC request while raw base64 is excluded from persisted AI UI state and request inspection.

## 10. External conditions and post-freeze work

1. Supply a healthy OpenAI-compatible endpoint or running Ollama service to execute live stream/cancel/retry and the final multimodal provider response.
2. Runtime-owned Memory mutations, Tool/Agent lifecycle operations, and Knowledge retrieval remain future feature work outside the Sprint 15 freeze.

The first item is `PENDING EXTERNAL CONDITION`; it does not block the verified Atlas integration boundary. The correct result is:

**Sprint 15 Final Acceptance PASS**

Recommended next step: preserve tag `v0.15.0-alpha` and begin Sprint 16 work from the frozen baseline.
