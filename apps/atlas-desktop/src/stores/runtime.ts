import { create } from "zustand";
import type { RuntimeInfo, RuntimeHealth, AppStatus } from "../types";

const RUNTIME_NAMES = [
  "Workflow Runtime",
  "Vision Runtime",
  "AI Runtime",
  "Knowledge Runtime",
  "Plugin Runtime",
  "IPC Runtime",
  "Project Runtime",
  "Storage Runtime",
];

function createDefaultRuntime(name: string): RuntimeInfo {
  return {
    name,
    status: "created" as AppStatus,
    health: "unknown" as RuntimeHealth,
    cpuUsage: 0,
    memoryUsage: 0,
    uptime: 0,
    metrics: [],
  };
}

export interface RuntimeState {
  runtimes: RuntimeInfo[];
  initializeRuntimes: () => void;
  setStatus: (name: string, status: AppStatus) => void;
  setHealth: (name: string, health: RuntimeHealth) => void;
  setMetrics: (name: string, metrics: RuntimeInfo["metrics"]) => void;
  setResourceUsage: (name: string, cpu: number, memory: number) => void;
  getRuntime: (name: string) => RuntimeInfo | undefined;
}

export const useRuntimeStore = create<RuntimeState>((set, get) => ({
  runtimes: [],

  initializeRuntimes: () => {
    const runtimes = RUNTIME_NAMES.map(createDefaultRuntime);
    set({ runtimes });
  },

  setStatus: (name, status) =>
    set((state) => ({
      runtimes: state.runtimes.map((r) => (r.name === name ? { ...r, status } : r)),
    })),

  setHealth: (name, health) =>
    set((state) => ({
      runtimes: state.runtimes.map((r) => (r.name === name ? { ...r, health } : r)),
    })),

  setMetrics: (name, metrics) =>
    set((state) => ({
      runtimes: state.runtimes.map((r) => (r.name === name ? { ...r, metrics } : r)),
    })),

  setResourceUsage: (name, cpu, memory) =>
    set((state) => ({
      runtimes: state.runtimes.map((r) => (r.name === name ? { ...r, cpuUsage: cpu, memoryUsage: memory } : r)),
    })),

  getRuntime: (name) => get().runtimes.find((r) => r.name === name),
}));

