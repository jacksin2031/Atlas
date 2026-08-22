import { create } from "zustand";
import type { LayoutConfig, PanelId, DockPosition } from "../types";

const DEFAULT_PANELS: Record<PanelId, import("../types").PanelInstance> = {
  "project-explorer": { id: "project-explorer", title: "Project Explorer", visible: true, position: "left", order: 0, collapsed: false },
  "runtime-monitor": { id: "runtime-monitor", title: "Runtime Monitor", visible: true, position: "center", order: 1, collapsed: false },
  "output": { id: "output", title: "Output", visible: true, position: "bottom", order: 2, collapsed: false },
  "console": { id: "console", title: "Console", visible: false, position: "bottom", order: 3, collapsed: false },
  "logs": { id: "logs", title: "Logs", visible: false, position: "bottom", order: 4, collapsed: false },
  "extensions": { id: "extensions", title: "Extensions", visible: false, position: "right", order: 5, collapsed: false },
  "settings": { id: "settings", title: "Settings", visible: false, position: "right", order: 6, collapsed: false },
  "problems": { id: "problems", title: "Problems", visible: false, position: "bottom", order: 7, collapsed: false },
  "notifications": { id: "notifications", title: "Notifications", visible: false, position: "right", order: 8, collapsed: false },
};

export interface LayoutState {
  config: LayoutConfig;
  setPanelVisible: (id: PanelId, visible: boolean) => void;
  setPanelCollapsed: (id: PanelId, collapsed: boolean) => void;
  setPanelPosition: (id: PanelId, position: DockPosition) => void;
  setActivePanel: (id: PanelId) => void;
  resetLayout: () => void;
  saveLayout: () => void;
  loadLayout: () => void;
}

const STORAGE_KEY = "atlas-layout";

function createDefaultConfig(): LayoutConfig {
  return { panels: DEFAULT_PANELS, splitterPositions: {}, activePanel: "project-explorer" };
}

export const useLayoutStore = create<LayoutState>((set, get) => ({
  config: createDefaultConfig(),

  setPanelVisible: (id, visible) =>
    set((state) => ({
      config: {
        ...state.config,
        panels: { ...state.config.panels, [id]: { ...state.config.panels[id], visible } },
      },
    })),

  setPanelCollapsed: (id, collapsed) =>
    set((state) => ({
      config: {
        ...state.config,
        panels: { ...state.config.panels, [id]: { ...state.config.panels[id], collapsed } },
      },
    })),

  setPanelPosition: (id, position) =>
    set((state) => ({
      config: {
        ...state.config,
        panels: { ...state.config.panels, [id]: { ...state.config.panels[id], position } },
      },
    })),

  setActivePanel: (id) =>
    set((state) => ({
      config: { ...state.config, activePanel: id },
    })),

  resetLayout: () =>
    set({ config: createDefaultConfig() }),

  saveLayout: () => {
    const { config } = get();
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
    } catch {
      // Storage full or unavailable — graceful degradation
    }
  },

  loadLayout: () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as LayoutConfig;
        // Merge with defaults to handle new panels
        const merged: Record<PanelId, typeof DEFAULT_PANELS[PanelId]> = {} as any;
        for (const key of Object.keys(DEFAULT_PANELS) as PanelId[]) {
          merged[key] = parsed.panels[key] ?? DEFAULT_PANELS[key];
        }
        set({ config: { ...parsed, panels: merged } });
      }
    } catch {
      // Corrupt stored layout — fall back to defaults
    }
  },
}));
