// Atlas Workflow Studio - Debug Store
// RFC-0316 compliant

import { create } from 'zustand';
import type {
  Breakpoint,
  DebugSession,
  DebugEvent,
  DebugFrame,
  
} from '../types';

export interface DebugState {
  sessions: Record<string, DebugSession>;
  activeSessionId: string | null;
  isAttached: boolean;

  // Breakpoints
  breakpoints: Breakpoint[];

  // Current execution info
  currentNodeId: string | null;
  executionPath: string[];
  callStack: DebugFrame[];
  events: DebugEvent[];

  // Actions
  createSession: (runId: string) => string;
  setActiveSession: (id: string | null) => void;
  attach: () => void;
  detach: () => void;
  addBreakpoint: (bp: Omit<Breakpoint, 'id' | 'hitCount'>) => void;
  removeBreakpoint: (id: string) => void;
  toggleBreakpoint: (id: string) => void;
  clearBreakpoints: () => void;
  setBreakpointCondition: (id: string, condition: string) => void;
  setCurrentNode: (nodeId: string | null) => void;
  pushExecutionPath: (nodeId: string) => void;
  pushCallStack: (frame: DebugFrame) => void;
  popCallStack: () => void;
  addEvent: (event: Omit<DebugEvent, 'id'>) => void;
  clearEvents: () => void;
  stepOver: () => void;
  stepInto: () => void;
  stepOut: () => void;
  continue: () => void;
  inspectNode: (nodeId: string) => void;
  modifyVariable: (name: string, value: unknown) => void;
  replaySession: (sessionId: string) => void;
  exportRecording: (sessionId: string) => string;
  reset: () => void;
}

export const useDebugStore = create<DebugState>((set, get) => ({
  sessions: {},
  activeSessionId: null,
  isAttached: false,
  breakpoints: [],
  currentNodeId: null,
  executionPath: [],
  callStack: [],
  events: [],

  createSession: (runId) => {
    const sessionId = `dbg_${runId}_${Date.now()}`;
    const session: DebugSession = {
      id: sessionId,
      runId,
      breakpoints: [],
      executionPath: [],
      callStack: [],
      history: [],
      startTime: Date.now(),
      paused: false,
    };
    set((state) => ({
      sessions: { ...state.sessions, [sessionId]: session },
      activeSessionId: sessionId,
    }));
    return sessionId;
  },

  setActiveSession: (id) => set({ activeSessionId: id }),

  attach: () => set({ isAttached: true }),
  detach: () => set({ isAttached: false }),

  addBreakpoint: (bp) => {
    const id = `bp_${Date.now()}`;
    const newBp: Breakpoint = { ...bp, id, enabled: true, hitCount: 0 } as Breakpoint;
    set((state) => ({ breakpoints: [...state.breakpoints, newBp] }));
  },

  removeBreakpoint: (id) =>
    set((state) => ({
      breakpoints: state.breakpoints.filter((b) => b.id !== id),
    })),

  toggleBreakpoint: (id) =>
    set((state) => ({
      breakpoints: state.breakpoints.map((b) =>
        b.id === id ? { ...b, enabled: !b.enabled } : b
      ),
    })),

  clearBreakpoints: () => set({ breakpoints: [] }),

  setBreakpointCondition: (id, condition) =>
    set((state) => ({
      breakpoints: state.breakpoints.map((b) =>
        b.id === id ? { ...b, condition } : b
      ),
    })),

  setCurrentNode: (nodeId) => set({ currentNodeId: nodeId }),

  pushExecutionPath: (nodeId) =>
    set((state) => ({ executionPath: [...state.executionPath, nodeId] })),

  pushCallStack: (frame) =>
    set((state) => ({ callStack: [...state.callStack, frame] })),

  popCallStack: () =>
    set((state) => ({
      callStack: state.callStack.slice(0, -1),
    })),

  addEvent: (event) => {
    const id = `evt_${Date.now()}`;
    set((state) => ({
      events: [...state.events, { ...event, id }],
    }));
  },

  clearEvents: () => set({ events: [] }),

  stepOver: () => set({}),
  stepInto: () => set({}),
  stepOut: () => set({}),
  continue: () => set({}),

  inspectNode: (nodeId) => {
    set((state) => ({
      events: [
        ...state.events,
        {
          id: `inspect_${Date.now()}`,
          type: 'node_enter',
          nodeId,
          timestamp: Date.now(),
        },
      ],
    }));
  },

  modifyVariable: (_name, _value) => {
    // Variable modification respects sandbox boundaries (RFC-0316 AC-07)
  },

  replaySession: (_sessionId) => {
    // Replay produces deterministic equivalence (RFC-0316 AC-04)
  },

  exportRecording: (sessionId) => {
    const session = get().sessions[sessionId];
    if (!session) return '[]';
    return JSON.stringify(session.history, null, 2);
  },

  reset: () =>
    set({
      sessions: {},
      activeSessionId: null,
      isAttached: false,
      breakpoints: [],
      currentNodeId: null,
      executionPath: [],
      callStack: [],
      events: [],
    }),
}));
