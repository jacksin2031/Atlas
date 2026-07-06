// Atlas Workflow Studio - Execution Store
// RFC-0303, RFC-0304 compliant

import { create } from "zustand";
import type {
  WorkflowRun,
  WorkflowRunStatus,
  ExecutionError,
  ExecutionMetrics,
  NodeExecutionState,
} from "../types";

export interface ExecutionState {
  runs: Record<string, WorkflowRun>;
  activeRunId: string | null;
  status: WorkflowRunStatus;
  isRunning: boolean;
  isPaused: boolean;
  isSimulating: boolean;
  isDryRunning: boolean;
  metrics: ExecutionMetrics;
  createRun: (workflowId: string) => string;
  setActiveRun: (runId: string | null) => void;
  updateRunStatus: (runId: string, status: WorkflowRunStatus) => void;
  updateNodeState: (runId: string, nodeId: string, state: NodeExecutionState) => void;
  addExecutionError: (runId: string, error: ExecutionError) => void;
  updateMetrics: (updates: Partial<ExecutionMetrics>) => void;
  startExecution: () => void;
  pauseExecution: () => void;
  resumeExecution: () => void;
  stopExecution: () => void;
  stepExecution: () => void;
  restartExecution: () => void;
  startSimulation: () => void;
  stopSimulation: () => void;
  startDryRun: () => void;
  stopDryRun: () => void;
  clearRun: (runId: string) => void;
  reset: () => void;
}

function createEmptyMetrics(): ExecutionMetrics {
  return { totalNodes: 0, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 };
}

export const useExecutionStore = create<ExecutionState>((set) => ({
  runs: {},
  activeRunId: null,
  status: "created",
  isRunning: false,
  isPaused: false,
  isSimulating: false,
  isDryRunning: false,
  metrics: createEmptyMetrics(),

  createRun: (workflowId) => {
    const runId = `run_${workflowId}_${Date.now()}`;
    const run: WorkflowRun = {
      id: runId,
      workflowId,
      status: "created",
      nodeStates: {},
      variables: {},
      errors: [],
      metrics: createEmptyMetrics(),
    };
    set((state) => ({
      runs: { ...state.runs, [runId]: run },
      activeRunId: runId,
      status: "initializing",
    }));
    return runId;
  },

  setActiveRun: (runId) => set({ activeRunId: runId }),

  updateRunStatus: (runId, status) =>
    set((state) => {
      const run = state.runs[runId];
      if (!run) return state;
      return {
        runs: { ...state.runs, [runId]: { ...run, status } },
        status,
        isRunning: status === "running",
        isPaused: status === "paused",
      };
    }),

  updateNodeState: (runId, nodeId, nodeState) =>
    set((state) => {
      const run = state.runs[runId];
      if (!run) return state;
      return {
        runs: {
          ...state.runs,
          [runId]: {
            ...run,
            currentNodeId: nodeId,
            nodeStates: { ...run.nodeStates, [nodeId]: nodeState },
          },
        },
      };
    }),

  addExecutionError: (runId, error) =>
    set((state) => {
      const run = state.runs[runId];
      if (!run) return state;
      return {
        runs: {
          ...state.runs,
          [runId]: { ...run, errors: [...run.errors, error] },
        },
      };
    }),

  updateMetrics: (updates) =>
    set((state) => {
      const run = state.runs[state.activeRunId!];
      if (!run) return state;
      return {
        runs: {
          ...state.runs,
          [state.activeRunId!]: {
            ...run,
            metrics: { ...run.metrics, ...updates },
          },
        },
        metrics: { ...state.metrics, ...updates },
      };
    }),

  startExecution: () => set({ status: "running", isRunning: true, isPaused: false }),
  pauseExecution: () => set({ status: "paused", isPaused: true }),
  resumeExecution: () => set({ status: "running", isPaused: false }),
  stopExecution: () => set({ status: "cancelled", isRunning: false, isPaused: false }),
  stepExecution: () =>
    set((state) => ({ status: state.isPaused ? "running" : state.status })),
  restartExecution: () => set({ status: "restarting", isRunning: true, isPaused: false }),
  startSimulation: () => set({ isSimulating: true }),
  stopSimulation: () => set({ isSimulating: false }),
  startDryRun: () => set({ isDryRunning: true }),
  stopDryRun: () => set({ isDryRunning: false }),
  clearRun: (runId) =>
    set((state) => {
      const copy = { ...state.runs };
      delete copy[runId];
      return { runs: copy };
    }),
  reset: () =>
    set({
      runs: {},
      activeRunId: null,
      status: "created",
      isRunning: false,
      isPaused: false,
      isSimulating: false,
      isDryRunning: false,
      metrics: createEmptyMetrics(),
    }),
}));
