# apps/atlas-desktop

## Purpose

Atlas Desktop Shell — the graphical user interface that hosts every Atlas runtime.

This is NOT the Workflow Editor.
This is NOT the Vision Editor.
This is NOT the AI Studio.

This is the application shell.

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
│   ├── studio/             # Workflow Studio and Vision Studio
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

Workflow and Vision each own a FlexLayout model. Panel tabs can be moved, docked, split, reordered, resized, closed, reopened, and maximized. Layouts persist independently and recover to defaults when invalid.

- Workflow: Project Explorer / Node Palette, Workflow Canvas, Properties, Variables / Console / Problems / Debugger / Output.
- Vision: Vision Toolbox / Project Explorer, Vision Canvas, Vision Properties, OCR / Detection / Color / Template / Timeline / Console / Output / Problems.

## Commands

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+P | Toggle Command Palette |

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
- IPC compliant with RFC-0101 through RFC-0112
- Plugin compliant with RFC-0201 through RFC-0230
- Runtime lifecycle FSM aligned with RFC-0002
