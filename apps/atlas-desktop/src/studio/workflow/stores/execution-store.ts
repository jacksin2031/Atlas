// Atlas Workflow Studio - Execution Store
// RFC-0303, RFC-0304 compliant

import { create } from "zustand";
import type {
  WorkflowRun,
  WorkflowRunStatus,
  ExecutionError,
  ExecutionMetrics,
  NodeExecutionState,
  WorkflowNodeRuntimeResult,
  WorkflowRuntimeEvent,
  WorkflowRuntimeResult,
  WorkflowRuntimeState,
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
  runtimeAvailable: boolean | null;
  runtimeError: string | null;
  result: WorkflowRuntimeResult | null;
  nodeResults: Record<string, WorkflowNodeRuntimeResult>;
  events: WorkflowRuntimeEvent[];
  createRun: (workflowId: string) => string;
  setActiveRun: (runId: string | null) => void;
  updateRunStatus: (runId: string, status: WorkflowRunStatus) => void;
  updateNodeState: (runId: string, nodeId: string, state: NodeExecutionState) => void;
  addExecutionError: (runId: string, error: ExecutionError) => void;
  updateMetrics: (updates: Partial<ExecutionMetrics>) => void;
  startSimulation: () => void;
  stopSimulation: () => void;
  startDryRun: () => void;
  stopDryRun: () => void;
  clearRun: (runId: string) => void;
  reset: () => void;
  applyRuntimeState: (state: WorkflowRuntimeState) => void;
  applyRuntimeEvent: (event: WorkflowRuntimeEvent) => void;
  setRuntimeError: (error: string | null) => void;
  setResult: (result: WorkflowRuntimeResult | null) => void;
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
  runtimeAvailable: null,
  runtimeError: null,
  result: null,
  nodeResults: {},
  events: [],

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
      runtimeAvailable: null,
      runtimeError: null,
      result: null,
      nodeResults: {},
      events: [],
    }),
  applyRuntimeState: (runtimeState) => set((state) => {
    const metrics = { ...createEmptyMetrics(), ...runtimeState.metrics };
    const existing = state.runs[runtimeState.executionId];
    const run: WorkflowRun = {
      id: runtimeState.executionId,
      workflowId: runtimeState.workflowId,
      status: runtimeState.status,
      currentNodeId: runtimeState.currentNodeId ?? undefined,
      startedAt: Date.parse(runtimeState.startedAt),
      completedAt: runtimeState.completedAt ? Date.parse(runtimeState.completedAt) : undefined,
      nodeStates: runtimeState.nodeStates,
      variables: runtimeState.variables,
      errors: existing?.errors ?? [],
      metrics,
    };
    return {
      runs: { ...state.runs, [runtimeState.executionId]: run },
      activeRunId: runtimeState.executionId,
      status: runtimeState.status,
      isRunning: runtimeState.status === "running" || runtimeState.status === "scheduled",
      isPaused: runtimeState.status === "paused",
      runtimeAvailable: true,
      runtimeError: null,
      metrics,
      nodeResults: runtimeState.nodeResults,
    };
  }),
  applyRuntimeEvent: (event) => set((state) => {
    if (!event.executionId || (state.activeRunId && event.executionId !== state.activeRunId)) {
      return { events: [...state.events, event].slice(-500) };
    }
    const run = state.runs[event.executionId];
    if (!run) return { events: [...state.events, event].slice(-500) };
    const statusMap: Record<string, WorkflowRunStatus> = {
      WorkflowStarted: "running", WorkflowPaused: "paused", WorkflowResumed: "running",
      WorkflowCompleted: "completed", WorkflowFailed: "failed", WorkflowCancelled: "cancelled",
    };
    const nodeMap: Record<string, NodeExecutionState> = {
      NodeStarted: "running", NodeCompleted: "completed", NodeFailed: "failed", NodeSkipped: "skipped",
    };
    const nextStatus = statusMap[event.eventType] ?? run.status;
    const runtimeNodeState = nodeMap[event.eventType];
    const nextNodeStates = event.nodeId && runtimeNodeState
      ? { ...run.nodeStates, [event.nodeId]: runtimeNodeState }
      : run.nodeStates;
    const nextResults = event.nodeId && (event.eventType === "NodeCompleted" || event.eventType === "NodeFailed")
      ? { ...state.nodeResults, [event.nodeId]: event.data as WorkflowNodeRuntimeResult }
      : state.nodeResults;
    const variables = event.eventType === "VariableChanged" && typeof event.data.name === "string"
      ? { ...run.variables, [event.data.name]: event.data.value }
      : run.variables;
    const nextRun = { ...run, status: nextStatus, currentNodeId: event.nodeId ?? run.currentNodeId, nodeStates: nextNodeStates, variables };
    return {
      runs: { ...state.runs, [event.executionId]: nextRun }, status: nextStatus,
      isRunning: nextStatus === "running" || nextStatus === "scheduled", isPaused: nextStatus === "paused",
      nodeResults: nextResults, events: [...state.events, event].slice(-500), runtimeAvailable: true,
      runtimeError: event.eventType === "WorkflowFailed" ? String(event.data.error ?? "Workflow execution failed") : state.runtimeError,
    };
  }),
  setRuntimeError: (runtimeError) => set({ runtimeError, runtimeAvailable: runtimeError ? false : true }),
  setResult: (result) => set({ result }),
}));
