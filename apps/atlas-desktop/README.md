# apps/atlas-desktop

> Sprint 18 candidate: **0.18.0-alpha**. Beta readiness is **NOT YET**; see [current evidence and acceptance gaps](../../docs/beta/SPRINT_18_BETA_READINESS_REPORT.md). Earlier sprint results below remain historical evidence.

## Purpose

Atlas Desktop Shell — the graphical user interface that hosts every Atlas runtime.

This is the application shell that hosts the independent Workflow, Vision, AI, Knowledge, and Marketplace workspaces.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Shell | Tauri 2 (Rust) |
| Frontend | React 19 + TypeScript |
| Bundler | Vite 7 |
| State | Zustand |
| Docking | FlexLayout 0.10 |
| UI | Atlas SVG icons and shared compact primitives |

## Structure

```
apps/atlas-desktop/
├── src/
│   ├── components/
│   │   ├── layouts/        # AppLayout, MenuBar, Toolbar, StatusBar
│   │   ├── panels/         # All dockable panel implementations
│   │   └── CommandPalette.tsx
│   ├── design-system/      # Atlas SVG icons and compact shared primitives
│   ├── workspace/          # FlexLayout manager, models, registry, persistence
│   ├── studio/             # Workflow, Vision, AI, Knowledge, and Marketplace workspaces
│   ├── services/           # IPC, plugin, project, theme, log, command registry/palette
│   ├── stores/             # Shell Zustand stores
│   ├── ipc/                # Tauri IPC bridge layer
│   ├── plugins/            # Plugin registration hooks
│   ├── types/              # Shared TypeScript types
│   ├── styles/             # Global CSS
│   ├── App.tsx             # Root React component
│   └── main.tsx            # Entry point
├── public/                 # Static assets (favicon)
├── src-tauri/              # Rust desktop backend
│   ├── capabilities/       # Explicit Tauri permissions
│   ├── src/                # Rust entry points
│   ├── Cargo.toml
│   └── tauri.conf.json     # Tauri 2 configuration
├── vite.config.ts          # Vite bundler config
├── tsconfig.json           # TypeScript config
└── package.json
```

## Workspaces

Workflow, Vision, AI, Knowledge, and Marketplace each own an independent versioned FlexLayout model. Panel tabs can be moved, docked, split, reordered, resized, closed, reopened, and maximized. Layouts persist independently and recover to defaults when invalid.

- Workflow: Project Explorer / Node Palette, Workflow Canvas, Properties, Variables / Console / Problems / Debugger / Output.
- Vision: Vision Toolbox / Project Explorer, Vision Canvas, Vision Properties, OCR / Detection / Color / Template / Timeline / Console / Output / Problems.
- AI: Providers / Models / Sessions, multi-mode AI editor, Context / Request / Response, Console / Tools / Memory / Retrieval / Metrics / Events / Comparison / Problems.
- Knowledge: project-scoped browser/editor/search with provenance, events, persistence and import/export surfaces.
- Marketplace: local-development package discovery/details/activity, permission review and installed/update state.

AI Studio uses the existing AI Runtime contracts through a typed IPC boundary, a persistent Tauri process manager, and a long-running Python host. The host implements discovery, inference, cancellation, provider actions, and request-correlated streaming for OpenAI-compatible and Ollama providers. Production mode shows explicit Runtime/provider-unavailable states; browser development can opt into the visibly isolated adapter with `VITE_ATLAS_AI_DEMO=true`.

Workflow Studio uses a separate typed IPC boundary and persistent Python Workflow host. The graph is mapped to the canonical Workflow manifest; the host executes it through the existing Runtime, immutable DAG, Node Registry, and Plugin Bridge. Runtime events, not React timers, drive node/edge state, debugger state, variables, metrics, and result inspection. Browser development reports Runtime unavailable and keeps simulation explicitly separate from native execution.

## Commands

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+P | Toggle Command Palette |
| F5 | Run workflow |
| F8 | Pause or resume workflow |
| Shift+F5 | Stop workflow |
| F7 | Step workflow |
| Ctrl+Shift+F5 | Restart workflow |

## Running

```bash
pnpm install
pnpm run dev       # Vite dev server at localhost:1420
pnpm tauri dev     # Full Tauri desktop app
pnpm run lint
pnpm run typecheck
pnpm test
```

On Windows, Tauri requires the MSVC Rust toolchain. If another toolchain is the
system default, run a command with `$env:RUSTUP_TOOLCHAIN='stable-x86_64-pc-windows-msvc'`.

## Architecture Compliance

- Conforms to MODULE_DEPENDENCIES.md (Layer 8 — Desktop UI)
- Depends on: Core Foundation, Plugin, IPC, Workflow, Vision, AI, Knowledge, Project
- No forbidden dependencies
- Tauri API imports are constrained to `src/ipc/bridge.ts`; React/workspace/Studio code consumes typed bridge/service boundaries
- IPC compliant with RFC-0101 through RFC-0112
- Plugin compliant with RFC-0201 through RFC-0230
- Runtime lifecycle FSM aligned with RFC-0002
