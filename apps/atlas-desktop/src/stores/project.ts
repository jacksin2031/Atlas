import { create } from "zustand";
import type { ProjectDescriptor, Notification, CommandPaletteItem } from "../types";

export interface ProjectState {
  currentProject: ProjectDescriptor | null;
  recentProjects: ProjectDescriptor[];
  notifications: Notification[];
  commands: CommandPaletteItem[];
  commandHistory: string[];
  openProject: (project: ProjectDescriptor) => void;
  closeProject: () => void;
  addRecentProject: (project: ProjectDescriptor) => void;
  addNotification: (notification: Omit<Notification, "id" | "timestamp">) => void;
  acknowledgeNotification: (id: string) => void;
  clearNotifications: () => void;
  registerCommand: (command: CommandPaletteItem) => void;
  searchCommands: (query: string) => CommandPaletteItem[];
  recordCommandUsed: (label: string) => void;
  getRecentCommands: () => string[];
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  currentProject: null,
  recentProjects: [],
  notifications: [],
  commands: [],
  commandHistory: [],

  openProject: (project) => set({ currentProject: project }),

  closeProject: () => set({ currentProject: null }),

  addRecentProject: (project) =>
    set((state) => {
      const existing = state.recentProjects.filter((p) => p.id !== project.id);
      return { recentProjects: [project, ...existing].slice(0, 10) };
    }),

  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: `notif-${Date.now()}`, timestamp: Date.now(), acknowledged: false },
      ].slice(-100),
    })),

  acknowledgeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.map((n) =>
        n.id === id ? { ...n, acknowledged: true } : n
      ),
    })),

  clearNotifications: () => set({ notifications: [] }),

  registerCommand: (command) =>
    set((state) => ({ commands: [...state.commands, command] })), 

  searchCommands: (query) => {
    const lower = query.toLowerCase();
    return get().commands.filter(
      (c) => c.label.toLowerCase().includes(lower) || c.description.toLowerCase().includes(lower) || c.category.toLowerCase().includes(lower)
    );
  },

  recordCommandUsed: (label) =>
    set((state) => {
      const history = [label, ...state.commandHistory.filter((h) => h !== label)].slice(0, 50);
      return { commandHistory: history };
    }),

  getRecentCommands: () => get().commandHistory,
}));

