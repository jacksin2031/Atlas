// Atlas Workflow Studio - Node Registry Store
// RFC-0323 compliant — dynamic plugin node discovery

import { create } from 'zustand';
import type { PluginNodeRegistration } from "../types";
import type { NodeCategory } from "../types/node-categories";

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
  { typeName: 'transform', category: 'core', label: 'Transform', description: 'Transforms input data', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
  { typeName: 'constant', category: 'core', label: 'Constant', description: 'Emits a configured value', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
  { typeName: 'set_variable', category: 'core', label: 'Set Variable', description: 'Writes Workflow Runtime variable state', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
  { typeName: 'get_variable', category: 'core', label: 'Get Variable', description: 'Reads Workflow Runtime variable state', inputs: [], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
  { typeName: 'output', category: 'core', label: 'Output', description: 'Publishes a structured workflow output', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
  { typeName: 'delay', category: 'flow', label: 'Delay', description: 'Waits in the backend with cancellation support', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'any' }] },
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
  { typeName: 'condition', category: 'logic', label: 'Condition', description: 'Evaluates conditions without side effects', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'true', type: 'any' }, { id: 'out_1', name: 'false', type: 'any' }] },
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
  { typeName: 'exit', category: 'core', label: 'Exit', description: 'Marks workflow exit point', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [] },
  { typeName: 'math_operation', category: 'math', label: 'Math Operation', description: 'Performs mathematical operations', inputs: [{ id: 'in_0', name: 'a', type: 'float' }, { id: 'in_1', name: 'b', type: 'float' }], outputs: [{ id: 'out_0', name: 'result', type: 'float' }] },
  { typeName: 'string_operation', category: 'string', label: 'String Operation', description: 'Performs string manipulations', inputs: [{ id: 'in_0', name: 'text', type: 'string' }], outputs: [{ id: 'out_0', name: 'result', type: 'string' }] },
  { typeName: 'collection_operation', category: 'collection', label: 'Collection Operation', description: 'Performs collection operations', inputs: [{ id: 'in_0', name: 'items', type: 'array' }], outputs: [{ id: 'out_0', name: 'result', type: 'array' }] },
  { typeName: 'datetime_operation', category: 'datetime', label: 'Date/Time Operation', description: 'Performs date/time operations', inputs: [{ id: 'in_0', name: 'timestamp', type: 'timestamp' }], outputs: [{ id: 'out_0', name: 'result', type: 'string' }] },
  { typeName: 'file_operation', category: 'file', label: 'File Operation', description: 'Performs file operations', inputs: [{ id: 'in_0', name: 'path', type: 'string' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'system_operation', category: 'system', label: 'System Operation', description: 'Performs system operations', inputs: [], outputs: [] },
  { typeName: 'ipc_operation', category: 'ipc', label: 'IPC Operation', description: 'Executes inter-process coordination', inputs: [], outputs: [] },
  { typeName: 'mouse_move', category: 'input', label: 'Mouse Move', description: 'Moves to a typed Vision target reference', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }, { id: 'in_1', name: 'target', type: 'target_reference' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'mouse_click', category: 'input', label: 'Mouse Click', description: 'Clicks the center of a typed Vision target reference', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }, { id: 'in_1', name: 'target', type: 'target_reference' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'mouse_double_click', category: 'input', label: 'Mouse Double Click', description: 'Double-clicks a typed Vision target reference', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }, { id: 'in_1', name: 'target', type: 'target_reference' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'mouse_drag', category: 'input', label: 'Mouse Drag', description: 'Drags between typed target references', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }, { id: 'in_1', name: 'start', type: 'target_reference' }, { id: 'in_2', name: 'end', type: 'target_reference' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'mouse_scroll', category: 'input', label: 'Mouse Scroll', description: 'Scrolls vertically or horizontally', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'keyboard_press', category: 'input', label: 'Keyboard Press', description: 'Presses and releases one key', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'keyboard_hotkey', category: 'input', label: 'Keyboard Hotkey', description: 'Presses a key combination', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'keyboard_type', category: 'input', label: 'Keyboard Type', description: 'Types configured or incoming text', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }, { id: 'in_1', name: 'text', type: 'string' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'key_down', category: 'input', label: 'Key Down', description: 'Holds a key until Key Up or workflow cleanup', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'key_up', category: 'input', label: 'Key Up', description: 'Releases a held key', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'input_wait', category: 'input', label: 'Input Wait', description: 'Waits for a duration or keyboard state', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'input_release_all', category: 'input', label: 'Input Release All', description: 'Safely releases all input held by the provider', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'result', type: 'object' }] },
  { typeName: 'vision_current_frame', category: 'vision', label: 'Vision Current Frame', description: 'Captures a screen-space frame through Tauri', inputs: [{ id: 'in_0', name: 'trigger', type: 'any' }], outputs: [{ id: 'out_0', name: 'frame', type: 'frame_reference' }] },
  { typeName: 'vision_template_match', category: 'vision', label: 'Image Detection', description: 'Finds a selected template image in a captured frame and returns typed target references', inputs: [{ id: 'in_0', name: 'frame', type: 'frame_reference' }], outputs: [{ id: 'out_0', name: 'region', type: 'region_reference' }, { id: 'out_1', name: 'bounds', type: 'bounds_reference' }, { id: 'out_2', name: 'point', type: 'point_reference' }] },
  { typeName: 'vision_detect', category: 'vision', label: 'Detection', description: 'Resolves a detection into typed target references', inputs: [{ id: 'in_0', name: 'frame', type: 'frame_reference' }], outputs: [{ id: 'out_0', name: 'region', type: 'region_reference' }, { id: 'out_1', name: 'bounds', type: 'bounds_reference' }, { id: 'out_2', name: 'point', type: 'point_reference' }] },
  { typeName: 'vision_ocr', category: 'vision', label: 'OCR', description: 'Runs native Windows OCR and emits typed target references', inputs: [{ id: 'in_0', name: 'frame', type: 'frame_reference' }], outputs: [{ id: 'out_0', name: 'region', type: 'region_reference' }, { id: 'out_1', name: 'bounds', type: 'bounds_reference' }, { id: 'out_2', name: 'point', type: 'point_reference' }] },
  { typeName: 'vision_validate', category: 'vision', label: 'Vision Validate', description: 'Validates visual state on a newly captured frame', inputs: [{ id: 'in_0', name: 'frame', type: 'frame_reference' }], outputs: [{ id: 'out_0', name: 'valid', type: 'boolean' }, { id: 'out_1', name: 'result', type: 'object' }] },
  { typeName: 'ai_inference', category: 'ai', label: 'AI Inference', description: 'Executes through the existing AI Runtime host', inputs: [{ id: 'in_0', name: 'prompt', type: 'string' }], outputs: [{ id: 'out_0', name: 'text', type: 'string' }, { id: 'out_1', name: 'response', type: 'ai_response' }] },
  { typeName: 'vision_operation', category: 'vision', label: 'Vision Operation (Legacy)', description: 'Compatibility alias for the Vision Runtime bridge', inputs: [], outputs: [{ id: 'out_0', name: 'frame', type: 'frame_reference' }] },
  { typeName: 'ai_operation', category: 'ai', label: 'AI Operation (Legacy)', description: 'Compatibility alias for AI Runtime inference', inputs: [{ id: 'in_0', name: 'prompt', type: 'string' }], outputs: [{ id: 'out_0', name: 'text', type: 'string' }] },
  { typeName: 'plugin_test', category: 'system', label: 'Plugin Test', description: 'Repository-owned deterministic PluginBridge node', inputs: [{ id: 'in_0', name: 'input', type: 'any' }], outputs: [{ id: 'out_0', name: 'value', type: 'string' }] },
  { typeName: 'knowledge_operation', category: 'knowledge', label: 'Knowledge Operation', description: 'Performs knowledge operations', inputs: [], outputs: [] },
  { typeName: 'project_operation', category: 'project', label: 'Project Operation', description: 'Performs project operations', inputs: [], outputs: [] },
  { typeName: 'storage_operation', category: 'storage', label: 'Storage Operation', description: 'Performs storage operations', inputs: [], outputs: [] },
];

const INPUT_DEFAULT_PARAMETERS: Record<string, Record<string, unknown>> = {
  mouse_move: { x: 400, y: 300, duration_ms: 200 },
  mouse_click: { x: 400, y: 300, button: 'left', click_count: 1 },
  mouse_double_click: { x: 400, y: 300, button: 'left' },
  mouse_drag: { start_x: 400, start_y: 300, end_x: 600, end_y: 300, button: 'left', duration_ms: 500 },
  mouse_scroll: { vertical: -3, horizontal: 0 },
  keyboard_press: { key: 'enter' },
  keyboard_hotkey: { keys: ['ctrl', 's'] },
  keyboard_type: { text: 'Atlas', interval_ms: 20 },
  key_down: { key: 'w' },
  key_up: { key: 'w' },
  input_wait: { duration_ms: 500, timeout_ms: 30000 },
  input_release_all: {},
  vision_detect: { targetColor: '#ff00c8', tolerance: 6, minArea: 24, label: 'automation-target' },
  vision_template_match: { templateUrl: '', templateName: '', threshold: 0.95, sampleStep: 2, label: 'template-target' },
  vision_ocr: { contains: 'Atlas', label: 'ocr-target' },
  vision_validate: { operation: 'detection', targetColor: '#a8ff00', tolerance: 6, minArea: 24, expect: 'present' },
};

function createBuiltinRegistrations(): PluginNodeRegistration[] {
  return BUILTIN_DEFINITIONS.map((def, idx) => ({
      nodeId: `builtin_${def.typeName}_${idx}`,
    typeName: def.typeName,
    category: def.category,
    label: def.label,
    description: def.description,
    inputs: def.inputs.map((i) => ({ id: i.id, name: i.name, type: i.type as any, multiple: false })) as any,
    outputs: def.outputs.map((o) => ({ id: o.id, name: o.name, type: o.type as any, multiple: false })) as any,
    parameters: INPUT_DEFAULT_PARAMETERS[def.typeName] ?? (def.typeName === 'constant' ? { value: 'Hello' } : def.typeName === 'delay' ? { seconds: 1 } : def.typeName === 'set_variable' || def.typeName === 'get_variable' ? { name: 'value' } : def.typeName === 'ai_inference' ? { providerId: '', modelId: '', prompt: 'Reply exactly with ATLAS_OK' } : {}),
    version: '1.0.0',
    capabilities: def.category === 'input' ? ['input.control'] : def.category === 'vision' ? ['vision'] : [],
    pluginId: 'builtin',
  }));
}

function collectCategories(nodes: PluginNodeRegistration[]): Set<NodeCategory> {
  return new Set(nodes.map((node) => node.category));
}

const BUILTIN_NODES = createBuiltinRegistrations();
const BUILTIN_CATEGORIES = collectCategories(BUILTIN_NODES);

export const useNodeRegistryStore = create<NodeRegistryState>((set, get) => ({
  builtinDefinitions: BUILTIN_DEFINITIONS,
  registrations: new Map(),
  builtinNodes: BUILTIN_NODES,
  categories: new Set(BUILTIN_CATEGORIES),

  registerNode: (reg) => {
    set((state) => {
      const map = new Map(state.registrations);
      map.set(reg.nodeId, reg);
      return {
        registrations: map,
        categories: collectCategories([...state.builtinNodes, ...map.values()]),
      };
    });
  },

  unregisterNode: (nodeId) => {
    set((state) => {
      const map = new Map(state.registrations);
      map.delete(nodeId);
      return {
        registrations: map,
        categories: collectCategories([...state.builtinNodes, ...map.values()]),
      };
    });
  },

  getNodeRegistration: (nodeId) =>
    get().registrations.get(nodeId) ?? get().builtinNodes.find((node) => node.nodeId === nodeId),

  getAllRegistrations: () => Array.from(get().registrations.values()),

  getNodesByCategory: (category) => {
    const all = get().discoverNodes();
    return all.filter((r) => r.category === category);
  },

  getAllCategories: () => Array.from(collectCategories(get().discoverNodes())),

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
      return {
        registrations: map,
        categories: collectCategories([...state.builtinNodes, ...map.values()]),
      };
    });
  },

  reset: () =>
    set({
      builtinDefinitions: BUILTIN_DEFINITIONS,
      builtinNodes: BUILTIN_NODES,
      registrations: new Map(),
      categories: new Set(BUILTIN_CATEGORIES),
    }),
}));
