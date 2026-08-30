# AI Studio

AI Studio is Atlas Desktop's Layer 8 development and debugging UI for the existing Python AI Runtime. It does not implement model inference, retrieval, memory persistence, agent execution, or tool execution in React.

## Architecture

```text
Desktop Shell
  -> WorkspaceManager / FlexLayout / Panel Registry
  -> AI Studio components
  -> AI Studio Zustand store / AIStudioService
  -> typed Desktop IPC bridge
  -> Tauri AIHostManager
  -> long-running Python host
  -> AI Runtime / provider / model
```

The `ai` workspace uses `atlas.layout.ai.v1` through the same persistence and corruption-recovery code as Workflow and Vision. Its default layout contains Providers/Models/Sessions, the multi-mode AI editor, Context/Request/Response inspectors, and Console/Tools/Memory/Retrieval/Metrics/Events/Comparison/Problems.

## Runtime contracts

TypeScript view models mirror the existing runtime vocabulary: the 14 `ModelCapability` values, provider health, normalized inference requests/responses, Session/Workspace/Project/Global memory scopes, tool permissions and invocation states, agent lifecycle states, and explicit AI event types. Components never import `packages/ai`.

`RuntimeAdapter` calls the typed Tauri commands `ai_discover`, `ai_infer`, `ai_cancel`, and `ai_provider_action`. Tauri owns a persistent Python host process and forwards `ai://runtime-event` events to React. Started, chunk, completed, cancelled, and failed events are correlated by request ID; the Playground renders incremental chunks and Runtime metrics. The commands are intentionally not faked when the host or provider is unavailable.

The Python host currently supports OpenAI-compatible chat-completions providers and Ollama. Configure it before starting Tauri:

```powershell
$env:ATLAS_AI_API_KEY='...'
# Optional OpenAI-compatible endpoint override:
$env:ATLAS_AI_BASE_URL='https://api.openai.com/v1'
# Optional Ollama endpoint override:
$env:ATLAS_OLLAMA_URL='http://127.0.0.1:11434'
pnpm tauri dev
```

Desktop provider configuration stores credentials in Windows Credential Manager through Tauri. `OPENAI_API_KEY` is also accepted when `ATLAS_AI_API_KEY` is absent as a developer/CI fallback; environment credentials are read only by the Python host and are never returned through IPC.

For browser development only, `demo-adapter.ts` is enabled when both conditions are true:

```text
import.meta.env.DEV
VITE_ATLAS_AI_DEMO=true
```

It is visibly identified as `Demo Provider` and response metadata includes `production: false`.

## Security

- No credential fields or API keys are stored in Zustand, layout JSON, URLs, or localStorage.
- Request inspection displays the normalized request only.
- Vision attachments are stored as references and metadata; base64 image payloads are not copied into AI UI state.
- Tool controls do not execute tools from React.
- Agent trace shows explicit events and metadata only, never hidden chain-of-thought.

## Current backend limitations

- Native credential configuration is currently implemented for Windows; macOS Keychain and Linux Secret Service adapters remain pending.
- A valid live-provider credential or a running local Ollama instance is required for real-provider inference.
- Prompt/session persistence awaits Project/Storage policy and Runtime IPC.
- Knowledge retrieval, Memory mutation, Agent lifecycle controls, and Tool execution remain Runtime-owned and read-only/unavailable in the UI until bridged.

## Development

```powershell
pnpm run dev
$env:VITE_ATLAS_AI_DEMO='true'; pnpm run dev
pnpm run typecheck
pnpm run lint
pnpm test
pnpm run build
```
