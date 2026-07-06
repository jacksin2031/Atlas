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
| UI | Fluent UI (base styles) |

## Structure

```
apps/atlas-desktop/
├── src/
│   ├── components/
│   │   ├── layouts/        # AppLayout, MenuBar, Toolbar, DockPanels, StatusBar
│   │   ├── panels/         # All dockable panel implementations
│   │   └── CommandPalette.tsx
│   ├── services/           # IPC, plugin, project, theme, layout, log, command-palette
│   ├── stores/             # Zustand stores (theme, layout, logs, runtime, plugins, project)
│   ├── ipc/                # Tauri IPC bridge layer
│   ├── plugins/            # Plugin registration hooks
│   ├── types/              # Shared TypeScript types
│   ├── styles/             # Global CSS
│   ├── App.tsx             # Root React component
│   └── main.tsx            # Entry point
├── public/                 # Static assets (favicon)
├── tauri.conf.json         # Tauri 2 configuration
├── vite.config.ts          # Vite bundler config
├── tsconfig.json           # TypeScript config
└── package.json
```

## Panels

| Panel | Position | Default Visible |
|-------|----------|-----------------|
| Project Explorer | Left | Yes |
| Runtime Monitor | Center | Yes |
| Output | Bottom | Yes |
| Console | Bottom | No |
| Logs | Bottom | No |
| Extensions | Right | No |
| Settings | Right | No |
| Problems | Bottom | No |
| Notifications | Right | No |

## Commands

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+P | Toggle Command Palette |

## Running

```bash
npm install
npm run dev        # Vite dev server at localhost:1420
npm run tauri dev  # Full Tauri desktop app
```

## Architecture Compliance

- Conforms to MODULE_DEPENDENCIES.md (Layer 8 — Desktop UI)
- Depends on: Core Foundation, Plugin, IPC, Workflow, Vision, AI, Knowledge, Project
- No forbidden dependencies
- IPC compliant with RFC-0101 through RFC-0112
- Plugin compliant with RFC-0201 through RFC-0230
- Runtime lifecycle FSM aligned with RFC-0002
