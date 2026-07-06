// Atlas Workflow Studio - Node Registry Store
// RFC-0323 compliant — dynamic plugin node discovery

import { create } from 'zustand';
import type { PluginNodeRegistration } from "../types";
import type { NodeCategory } from "../types/node-categories";
import { NODE_CATEGORIES, NODE_CATEGORY_LABELS } from '../types/node-categories';

export interface NodeRegistryState {
  registrations: Map<string, PluginNodeRegistration>;
  builtinNodes: PluginNodeRegistration[];
  categories: Set<NodeCategory>;

  // Builtin node definitions (discovered, not hardcoded)
  builtinDefinitions: Array<{
    typeName: string;
    category: NodeCategory;
    label: string;
    description: string;
    inputs: Array<{ id: string; name: string; type: string }>;
    outputs: Array<{ id: string; name: string; type: string }>;
  }>;

  // Actions
  registerNode: (reg: PluginNodeRegistration) => void;
  unregisterNode: (nodeId: string) => void;
  getNodeRegistration: (nodeId: string) => PluginNodeRegistration | undefined;
  getAllRegistrations: () => PluginNodeRegistration[];
  getNodesByCategory: (category: NodeCategory) => PluginNodeRegistration[];
  getAllCategories: () => NodeCategory[];
  hasCategory: (category: NodeCategory) => boolean;
  discoverNodes: () => PluginNodeRegistration[];
  hotReload: (pluginId: string) => void;
  reset: () => void;
}

// Built-in node type definitions (RFC-0301 §10.1 catalog)
const BUILTIN_DEFINITIONS: NodeRegistryState['builtinDefinitions'] = [
  { typeName: 'execute', category: 'core', label: 'Execute', description: 'Executes a unit of work', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'transform', category: 'core', label: 'Transform', description: 'Transforms input data', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'route', category: 'flow', label: 'Route', description: 'Directs flow based on conditions', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'true', type: 'object' }, { id: 'out_1', name: 'false', type: 'object' }] },
  { typeName: 'branch', category: 'flow', label: 'Branch', description: 'Splits flow into parallel or conditional paths', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'loop', category: 'flow', label: 'Loop', description: 'Repeats execution of a sub-graph', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'wait', category: 'flow', label: 'Wait', description: 'Suspends until signal or timeout', inputs: [], outputs: [{ id: 'out_0', name: 'signal', type: 'object' }] },
  { typeName: 'signal', category: 'flow', label: 'Signal', description: 'Sends notification to downstream', inputs: [{ id: 'in_0', name: 'payload', type: 'object' }], outputs: [] },
  { typeName: 'notify', category: 'flow', label: 'Notify', description: 'Notifies downstream nodes', inputs: [{ id: 'in_0', name: 'message', type: 'string' }], outputs: [] },
  { typeName: 'compensate', category: 'flow', label: 'Compensate', description: 'Reverses prior work', inputs: [], outputs: [] },
  { typeName: 'manual', category: 'flow', label: 'Manual', description: 'Requires human intervention', inputs: [], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'human_approval', category: 'flow', label: 'Human Approval', description: 'Waits for explicit human approval', inputs: [], outputs: [{ id: 'out_0', name: 'approved', type: 'boolean' }] },
  { typeName: 'resource', category: 'core', label: 'Resource', description: 'Manages resource allocation', inputs: [], outputs: [] },
  { typeName: 'condition', category: 'logic', label: 'Condition', description: 'Evaluates conditions without side effects', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'true', type: 'object' }, { id: 'out_1', name: 'false', type: 'object' }] },
  { typeName: 'action', category: 'logic', label: 'Action', description: 'Performs an action with side effects', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'trigger', category: 'logic', label: 'Trigger', description: 'Monitors for trigger events', inputs: [], outputs: [{ id: 'out_0', name: 'event', type: 'object' }] },
  { typeName: 'scheduler', category: 'logic', label: 'Scheduler', description: 'Manages scheduled execution', inputs: [], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'error_handler', category: 'logic', label: 'Error Handler', description: 'Handles error conditions', inputs: [{ id: 'in_0', name: 'error', type: 'object' }], outputs: [{ id: 'out_0', name: 'recovered', type: 'object' }] },
  { typeName: 'recovery', category: 'logic', label: 'Recovery', description: 'Manages recovery operations', inputs: [], outputs: [] },
  { typeName: 'debug', category: 'logic', label: 'Debug', description: 'Provides debugging instrumentation', inputs: [], outputs: [] },
  { typeName: 'observation', category: 'logic', label: 'Observation', description: 'Emits observability data', inputs: [], outputs: [] },
  { typeName: 'validation', category: 'logic', label: 'Validation', description: 'Validates data or state', inputs: [{ id: 'in_0', name: 'data', type: 'object' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'serialization', category: 'core', label: 'Serialization', description: 'Serializes/deserializes data', inputs: [{ id: 'in_0', name: 'data', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'string' }] },
  { typeName: 'version', category: 'core', label: 'Version', description: 'Manages version compatibility', inputs: [], outputs: [] },
  { typeName: 'compliance', category: 'core', label: 'Compliance', description: 'Enforces compliance requirements', inputs: [], outputs: [] },
  { typeName: 'extension', category: 'core', label: 'Extension', description: 'Provides extension point functionality', inputs: [], outputs: [] },
  { typeName: 'composite', category: 'core', label: 'Composite', description: 'Contains a sub-graph', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'entry', category: 'core', label: 'Entry', description: 'Marks workflow entry point', inputs: [], outputs: [{ id: 'out_0', name: 'output', type: 'object' }] },
  { typeName: 'exit', category: 'core', label: 'Exit', description: 'Marks workflow exit point', inputs: [{ id: 'in_0', name: 'input', type: 'object' }], outputs: [] },
  { typeName: 'math_operation', category: 'math', label: 'Math Operation', description: 'Performs mathematical operations', inputs: [{ id: 'in_0', name: 'a', type: 'float' }, { id: 'in_1', name: 'b', type: 'float' }], outputs: [{ id: 'out_0', name: 'result', type: 'float' }] },
  { typeName: 'string_operation', category: 'string', label: 'String Operation', description: 'Performs string manipulations', inputs: [{ id: 'in_0', name: 'text', type: 'string' }], outputs: [{ id: 'out_0', name: 'result', type: 'string' }] },
  { typeName: 'collection_operation', category: 'collection', label: 'Collection Operation', description: 'Performs collection operations', inputs: [{ id: 'in_0', name: 'items', type: 'array' }], outputs: [{ id: 'out_0', name: 'result', type: 'array' }] },
  { typeName: 'datetime_operation', category: 'datetime', label: 'Date/Time Operation', description: 'Performs date/time operations', inputs: [{ id: 'in_0', name: 'timestamp', type: 'timestamp' }], outputs: [{ id: 'out_0', name: 'result', type: 'string' }] },
  { typeName: 'file_operation', category: 'file', label: 'File Operation', description: 'Performs file operations', inputs: [{ id: 'in_0', name: 'path', type: 'string' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'system_operation', category: 'system', label: 'System Operation', description: 'Performs system operations', inputs: [], outputs: [] },
  { typeName: 'ipc_operation', category: 'ipc', label: 'IPC Operation', description: 'Executes inter-process coordination', inputs: [], outputs: [] },
  { typeName: 'vision_operation', category: 'vision', label: 'Vision Operation', description: 'Executes vision operations', inputs: [], outputs: [] },
  { typeName: 'ai_operation', category: 'ai', label: 'AI Operation', description: 'Executes AI model inference', inputs: [], outputs: [] },
  { typeName: 'knowledge_operation', category: 'knowledge', label: 'Knowledge Operation', description: 'Performs knowledge operations', inputs: [], outputs: [] },
  { typeName: 'project_operation', category: 'project', label: 'Project Operation', description: 'Performs project operations', inputs: [], outputs: [] },
  { typeName: 'storage_operation', category: 'storage', label: 'Storage Operation', description: 'Performs storage operations', inputs: [], outputs: [] },
];

function createBuiltinRegistrations(): PluginNodeRegistration[] {
  return BUILTIN_DEFINITIONS.map((def, idx) => ({
      nodeId: `builtin_${def.typeName}_${idx}`,
    typeName: def.typeName,
    category: def.category,
    label: def.label,
    description: def.description,
    inputs: def.inputs.map((i) => ({ id: i.id, name: i.name, type: i.type as any, multiple: false })) as any,
    outputs: def.outputs.map((o) => ({ id: o.id, name: o.name, type: o.type as any, multiple: false })) as any,
    parameters: {},
    version: '1.0.0',
    capabilities: [],
    pluginId: 'builtin',
  }));
}

export const useNodeRegistryStore = create<NodeRegistryState>((set, get) => ({
  builtinDefinitions: [],
  registrations: new Map(),
  builtinNodes: createBuiltinRegistrations(),
  categories: new Set(['core', 'logic', 'flow']),

  registerNode: (reg) => {
    set((state) => {
      const map = new Map(state.registrations);
      map.set(reg.nodeId, reg);
      return { registrations: map };
    });
  },

  unregisterNode: (nodeId) => {
    set((state) => {
      const map = new Map(state.registrations);
      map.delete(nodeId);
      return { registrations: map };
    });
  },

  getNodeRegistration: (nodeId) => get().registrations.get(nodeId),

  getAllRegistrations: () => Array.from(get().registrations.values()),

  getNodesByCategory: (category) => {
    const all = get().getAllRegistrations();
    return all.filter((r) => r.category === category);
  },

  getAllCategories: () => {
    const regs = get().getAllRegistrations();
    const cats = new Set<NodeCategory>();
    for (const r of regs) cats.add(r.category);
    return Array.from(cats);
  },

  hasCategory: (category) => get().categories.has(category),

  discoverNodes: () => {
    const state = get();
    const all = [...state.builtinNodes, ...state.getAllRegistrations()];
    // Deduplicate by typeName
    const seen = new Set<string>();
    const unique: PluginNodeRegistration[] = [];
    for (const node of all) {
      if (!seen.has(node.typeName)) {
        seen.add(node.typeName);
        unique.push(node);
      }
    }
    return unique;
  },

  hotReload: (pluginId) => {
    // Hot reload: remove and re-register nodes from the plugin
    set((state) => {
      const map = new Map(state.registrations);
      for (const [key, val] of map) {
        if (val.pluginId === pluginId) {
          map.delete(key);
        }
      }
      return { registrations: map };
    });
  },

  reset: () =>
    set({
      builtinDefinitions: [],
  registrations: new Map(),
      categories: new Set(['core', 'logic', 'flow']),
    }),
}));
