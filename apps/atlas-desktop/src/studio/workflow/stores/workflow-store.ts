// Atlas Workflow Studio - Workflow Canvas Store
// Central Zustand store for the visual node canvas
// RFC-0302, RFC-0303, RFC-0307 compliant

import { create } from "zustand";
import { subscribeWithSelector } from "zustand/middleware";
import type {
  WorkflowNodeData,
  WorkflowDefinition,
  WorkflowVariable,
  CanvasTransform,
  SelectionState,
  ValidationResult,
  NodeExecutionState,
  ValidationState,
  EdgeType,
} from '../types';
import type { NodeCategory } from '../types/node-categories';
import { NODE_CATEGORIES } from "../types/node-categories";

// ---------------------------------------------------------------------------
// Internal node representation (React Flow compatible)
// ---------------------------------------------------------------------------

export interface WorkflowGraphNode {
  id: string;
  type: string;
  label: string;
  description?: string;
  category: NodeCategory;
  inputs: Array<{ id: string; name: string; type: string; multiple?: boolean; dynamic?: boolean }>;
  outputs: Array<{ id: string; name: string; type: string; multiple?: boolean; dynamic?: boolean }>;
  parameters: Record<string, unknown>;
  priority?: number;
  timeout?: string;
  retryPolicy?: unknown;
  icon?: string;
  executionState?: NodeExecutionState;
  validationState?: ValidationState;
  statusMessage?: string;
  documentationUrl?: string;
  capabilities?: string[];
  version?: string;
  x: number;
  y: number;
}

export interface WorkflowGraphEdge {
  id: string;
  source: string;
  target: string;
  edgeType: EdgeType;
  condition?: string;
  transformation?: string;
  cardinality?: string;
}

// ---------------------------------------------------------------------------
// Undo/Redo stack entry
// ---------------------------------------------------------------------------

interface HistoryEntry {
  nodes: WorkflowGraphNode[];
  edges: WorkflowGraphEdge[];
  variables: WorkflowVariable[];
  timestamp: number;
}

// ---------------------------------------------------------------------------
// Store state
// ---------------------------------------------------------------------------

export interface WorkflowCanvasState {
  nodes: WorkflowGraphNode[];
  edges: WorkflowGraphEdge[];
  variables: WorkflowVariable[];
  transform: CanvasTransform;
  selection: SelectionState;
  validationResults: ValidationResult[];
  history: HistoryEntry[];
  historyIndex: number;
  workflowId: string;
  workflowName: string;
  workflowVersion: string;
  selectedNodeIds: string[];
  selectedEdges: string[];

  setNodes: (nodes: WorkflowGraphNode[]) => void;
  addNode: (node: WorkflowGraphNode) => void;
  updateNode: (id: string, partial: Partial<WorkflowGraphNode>) => void;
  removeNode: (id: string) => void;
  duplicateNode: (id: string) => void;
  setEdges: (edges: WorkflowGraphEdge[]) => void;
  addEdge: (edge: WorkflowGraphEdge) => void;
  removeEdge: (id: string) => void;
  setTransform: (transform: CanvasTransform) => void;
  selectNode: (id: string, multi?: boolean) => void;
  selectEdge: (id: string, multi?: boolean) => void;
  deselectAll: () => void;
  selectAll: () => void;
  setValidationResults: (results: ValidationResult[]) => void;
  setWorkflowInfo: (id: string, name: string, version: string) => void;
  setCanvasPosition: (x: number, y: number, zoom?: number) => void;
  updateNodeExecutionState: (nodeId: string, state: NodeExecutionState) => void;
  updateNodeValidationState: (nodeId: string, state: ValidationState) => void;
  moveSelectedNodes: (dx: number, dy: number) => void;
  panCanvas: (dx: number, dy: number) => void;
  zoomCanvas: (delta: number) => void;
  undo: () => void;
  redo: () => void;
  clearHistory: () => void;
  addVariable: (variable: WorkflowVariable) => void;
  updateVariable: (id: string, updates: Partial<WorkflowVariable>) => void;
  removeVariable: (id: string) => void;
  setVariables: (variables: WorkflowVariable[]) => void;
  loadFromDefinition: (def: WorkflowDefinition) => void;
  exportToDefinition: () => WorkflowDefinition;
  resetCanvas: () => void;
  pushHistory: () => void;
}

const DEFAULT_TRANSFORM: CanvasTransform = { x: 0, y: 0, zoom: 1 };

function createInitialHistory(): HistoryEntry {
  return { nodes: [], edges: [], variables: [], timestamp: Date.now() };
}

export const useWorkflowStore = create<WorkflowCanvasState>()(
  subscribeWithSelector((set, get) => ({
    nodes: [],
    edges: [],
    variables: [],
    transform: DEFAULT_TRANSFORM,
    selection: {
      selectedNodeIds: new Set<string>(),
      selectedEdgeIds: new Set<string>(),
    },
    validationResults: [],
    history: [createInitialHistory()],
    historyIndex: 0,
    workflowId: "",
    workflowName: "",
    workflowVersion: "1.0.0",

    selectedNodeIds: [],
    selectedEdges: [],

    setNodes: (nodes) => set({ nodes }),
    addNode: (node) => {
      set((state) => ({ nodes: [...state.nodes, node] }));
      get().pushHistory();
    },
    updateNode: (id, partial) => {
      set((state) => ({
        nodes: state.nodes.map((n) => (n.id === id ? { ...n, ...partial } : n)),
      }));
      get().pushHistory();
    },
    removeNode: (id) => {
      set((state) => ({
        nodes: state.nodes.filter((n) => n.id !== id),
        edges: state.edges.filter((e) => e.source !== id && e.target !== id),
      }));
      get().pushHistory();
    },
    duplicateNode: (id) => {
      const source = get().nodes.find((n) => n.id === id);
      if (!source) return;
      const newId = `${source.id}_dup_${Date.now()}`;
      const newNode: WorkflowGraphNode = {
        ...source,
        id: newId,
        label: source.label + " (copy)",
        x: source.x + 20,
        y: source.y + 20,
      };
      set((state) => ({ nodes: [...state.nodes, newNode] }));
      get().pushHistory();
    },
    setEdges: (edges) => set({ edges }),
    addEdge: (edge) => {
      set((state) => ({ edges: [...state.edges, edge] }));
      get().pushHistory();
    },
    removeEdge: (id) => {
      set((state) => ({ edges: state.edges.filter((e) => e.id !== id) }));
      get().pushHistory();
    },
    setTransform: (transform) => set({ transform }),
    selectNode: (id, multi) => set((state) => {
        const selected = multi ? new Set(state.selection.selectedNodeIds) : new Set<string>();
        if (multi && selected.has(id)) { selected.delete(id); } else { selected.add(id); }
        return { selection: { ...state.selection, selectedNodeIds: selected }, selectedNodeIds: Array.from(selected) };
      }),
    selectEdge: (id, multi) => {
      set((state) => {
        const selected = multi
          ? new Set(state.selection.selectedEdgeIds)
          : new Set<string>();
        if (multi && selected.has(id)) {
          selected.delete(id);
        } else {
          selected.add(id);
        }
        return {
          selection: { ...state.selection, selectedEdgeIds: selected },
          selectedEdges: Array.from(selected),
        };
      });
    },
    deselectAll: () =>
      set({
        selection: { selectedNodeIds: new Set<string>(), selectedEdgeIds: new Set<string>() },
        selectedNodeIds: [],
        selectedEdges: [],
      }),
    selectAll: () =>
      set((state) => {
        const allIds = state.nodes.map((n) => n.id);
        return {
          selection: {
            ...state.selection,
            selectedNodeIds: new Set(allIds),
          },
          selectedNodeIds: allIds,
        };
      }),
    setValidationResults: (results) => set({ validationResults: results }),
    setWorkflowInfo: (id, name, version) =>
      set({ workflowId: id, workflowName: name, workflowVersion: version }),
    setCanvasPosition: (x, y, zoom) =>
      set((state) => ({
        transform: { ...state.transform, x, y, zoom: zoom ?? state.transform.zoom },
      })),
    updateNodeExecutionState: (nodeId, state) =>
      get().updateNode(nodeId, { executionState: state }),
    updateNodeValidationState: (nodeId, state) =>
      get().updateNode(nodeId, { validationState: state }),
    moveSelectedNodes: (dx, dy) => {
      const state = get();
      const updated = state.nodes.map((n) => {
        if (state.selection.selectedNodeIds.has(n.id)) {
          return { ...n, x: n.x + dx, y: n.y + dy };
        }
        return n;
      });
      set({ nodes: updated });
      get().pushHistory();
    },
    panCanvas: (dx, dy) =>
      set((state) => ({
        transform: { ...state.transform, x: state.transform.x + dx, y: state.transform.y + dy },
      })),
    zoomCanvas: (delta) =>
      set((state) => ({
        transform: {
          ...state.transform,
          zoom: Math.max(0.1, Math.min(3, state.transform.zoom + delta)),
        },
      })),
    addVariable: (variable) =>
      set((state) => ({ variables: [...state.variables, variable] })),
    updateVariable: (id, updates) =>
      set((state) => ({
        variables: state.variables.map((v) => (v.id === id ? { ...v, ...updates } : v)),
      })),
    removeVariable: (id) =>
      set((state) => ({ variables: state.variables.filter((v) => v.id !== id) })),
    setVariables: (variables) => set({ variables }),

    loadFromDefinition: (def) => {
      const nodes: any[] = def.nodes.map((n, i) => ({
        id: n.id,
        type: n.type,
        label: n.label || n.id,
        description: n.description,
        category: ((n.category || "core") as NodeCategory),
        inputs: n.inputs as any,
        outputs: n.outputs as any,
        parameters: n.parameters || {},
        priority: n.priority,
        timeout: n.timeout,
        retryPolicy: n.retryPolicy as any,
        icon: n.icon,
        executionState: "pending" as NodeExecutionState,
        validationState: "unchecked" as ValidationState,
        statusMessage: "",
        documentationUrl: n.documentationUrl,
        capabilities: n.capabilities,
        version: n.version,
        x: 100 + (i % 5) * 220,
        y: 100 + Math.floor(i / 5) * 160,
      }));
      const edges: any[] = def.edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        edgeType: (e.edgeType as EdgeType) || "data",
        condition: e.condition,
        transformation: e.transformation,
        cardinality: e.cardinality as any,
      }));
      set({
        nodes,
        edges,
        variables: def.variables || [],
        workflowId: def.id,
        workflowName: def.name,
        workflowVersion: def.version,
      });
      get().pushHistory();
    },

    exportToDefinition: (): WorkflowDefinition => {
      const state = get();
      return {
        id: state.workflowId,
        version: state.workflowVersion,
        name: state.workflowName,
        nodes: state.nodes.map((n: any) => ({
          id: n.id,
          type: n.type,
          label: n.label,
          description: n.description,
          category: n.category,
          inputs: n.inputs as any,
          outputs: n.outputs as any,
          parameters: n.parameters,
          priority: n.priority,
          timeout: n.timeout,
          retryPolicy: n.retryPolicy,
          icon: n.icon,
          documentationUrl: n.documentationUrl,
          capabilities: n.capabilities,
          version: n.version,
        })),
        edges: state.edges.map((e: any) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          edgeType: e.edgeType,
          condition: e.condition,
          transformation: e.transformation,
          cardinality: e.cardinality,
        })),
        variables: state.variables,
        parameters: {},
        metadata: {
          createdAt: Date.now(),
          updatedAt: Date.now(),
          tags: [],
        },
      };
    },

    pushHistory: () => {
      const state = get();
      const snapshot: HistoryEntry = {
        nodes: [...state.nodes],
        edges: [...state.edges],
        variables: [...state.variables],
        timestamp: Date.now(),
      };
      const newHistory = state.history.slice(0, state.historyIndex + 1);
      newHistory.push(snapshot);
      if (newHistory.length > 100) {
        newHistory.shift();
      }
      set({ history: newHistory, historyIndex: newHistory.length - 1 });
    },

    undo: () => {
      const state = get();
      if (state.historyIndex <= 0) return;
      const prev = state.history[state.historyIndex - 1]!;
      if (!prev) return;
      set({
        nodes: prev.nodes,
        edges: prev.edges,
        variables: prev.variables,
        historyIndex: state.historyIndex - 1,
        selection: { selectedNodeIds: new Set<string>(), selectedEdgeIds: new Set<string>() },
      });
    },

    redo: () => {
      const state = get();
      if (state.historyIndex >= state.history.length - 1) return;
      const next = state.history[state.historyIndex + 1]!;
      if (!next) return;
      set({
        nodes: next.nodes,
        edges: next.edges,
        variables: next.variables,
        historyIndex: state.historyIndex + 1,
        selection: { selectedNodeIds: new Set<string>(), selectedEdgeIds: new Set<string>() },
      });
    },

    clearHistory: () => {
      set({ history: [createInitialHistory()], historyIndex: 0 });
    },

    resetCanvas: () => {
      set({
        nodes: [],
        edges: [],
        variables: [],
        transform: DEFAULT_TRANSFORM,
        selection: { selectedNodeIds: new Set<string>(), selectedEdgeIds: new Set<string>() },
        validationResults: [],
        history: [createInitialHistory()],
        historyIndex: 0,
        workflowId: "",
        workflowName: "",
        workflowVersion: "1.0.0",
      });
    },
  }))
);