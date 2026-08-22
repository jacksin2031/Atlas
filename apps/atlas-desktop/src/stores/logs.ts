import { create } from "zustand";
import type { LogEntry } from "../types";

let logIdCounter = 0;

export interface LogState {
  entries: LogEntry[];
  filter: { level: string; source: string; query: string };
  setFilter: (partial: Partial<{ level: string; source: string; query: string }>) => void;
  addEntry: (entry: Omit<LogEntry, "id">) => void;
  clearEntries: () => void;
  exportLogs: (filter: { level: string; source: string; query: string }) => string;
  searchLogs: (query: string) => LogEntry[];
}

export const useLogStore = create<LogState>((set, get) => ({
  entries: [],
  filter: { level: "all", source: "all", query: "" },

  setFilter: (partial) =>
    set((state) => ({
      filter: { ...state.filter, ...partial },
    })),

  addEntry: (entry) =>
    set((state) => {
      const newEntry: LogEntry = { ...entry, id: "log-" + (++logIdCounter) + "-" + Date.now() };
      return { entries: [...state.entries, newEntry] };
    }),

  clearEntries: () => set({ entries: [] }),

  exportLogs: (filter) => {
    const { entries } = get();
    const filtered = entries.filter((e) => {
      if (filter.level !== "all" && e.level !== filter.level) return false;
      if (filter.source !== "all" && e.source !== filter.source) return false;
      if (filter.query && !e.message.toLowerCase().includes(filter.query.toLowerCase())) return false;
      return true;
    });
    return filtered.map((e) => "[" + new Date(e.timestamp).toISOString() + "] " + e.level.toUpperCase() + " [" + e.source + "] " + e.message).join("\n");
  },

  searchLogs: (query: string) => {
    const { entries } = get();
    return entries.filter((e) => e.message.toLowerCase().includes(query.toLowerCase()));
  },
}));
