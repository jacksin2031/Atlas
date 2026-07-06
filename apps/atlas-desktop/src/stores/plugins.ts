import { create } from "zustand";
import type { PluginEntry, PluginState as PluginStateType, PluginHealth as PluginHealthType } from "../types";

const INITIAL_PLUGINS: PluginEntry[] = [
  { id: "atlas-core", name: "Atlas Core", description: "Core platform integration", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-ipc-bridge", name: "IPC Bridge", description: "Inter-process communication bridge", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-runtime-watcher", name: "Runtime Watcher", description: "Monitors all Atlas runtimes", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-theme-engine", name: "Theme Engine", description: "Manages application themes", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-log-collector", name: "Log Collector", description: "Collects and aggregates runtime logs", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-project-manager", name: "Project Manager", description: "Manages project lifecycle", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-notification-handler", name: "Notification Handler", description: "System and runtime notifications", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-command-palette", name: "Command Palette", description: "Quick command execution", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-layout-manager", name: "Layout Manager", description: "Persists and restores panel layouts", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
  { id: "atlas-health-checker", name: "Health Checker", description: "Periodic runtime health verification", version: "0.12.0", state: "installed", health: "healthy", enabled: true, author: "Atlas Team" },
];

export interface PluginManagerState {
  plugins: PluginEntry[];
  togglePlugin: (id: string) => void;
  setPluginHealth: (id: string, health: PluginHealthType) => void;
  setPluginState: (id: string, state: PluginStateType) => void;
  getPlugin: (id: string) => PluginEntry | undefined;
  searchPlugins: (query: string) => PluginEntry[];
}

export const usePluginStore = create<PluginManagerState>((set, get) => ({
  plugins: INITIAL_PLUGINS,

  togglePlugin: (id) =>
    set((state) => ({
      plugins: state.plugins.map((p) =>
        p.id === id ? { ...p, enabled: !p.enabled } : p
      ),
    })),

  setPluginHealth: (id, health) =>
    set((state) => ({
      plugins: state.plugins.map((p) =>
        p.id === id ? { ...p, health } : p
      ),
    })),

  setPluginState: (id, newState) =>
    set((state) => ({
      plugins: state.plugins.map((p) =>
        p.id === id ? { ...p, state: newState } : p
      ),
    })),

  getPlugin: (id) => get().plugins.find((p) => p.id === id),

  searchPlugins: (query) => {
    const lower = query.toLowerCase();
    return get().plugins.filter(
      (p) => p.name.toLowerCase().includes(lower) || p.description.toLowerCase().includes(lower)
    );
  },
}));

