// Atlas Workflow Studio - Variable Store
// RFC-0302 §6, RFC-0307 compliant

import { create } from 'zustand';
import type { WorkflowVariable, VariableScope, DataType } from '../types';

export type VariableState = {
  variables: WorkflowVariable[];
  scopeOrder: VariableScope[];

  // Actions
  addVariable: (variable: Omit<WorkflowVariable, 'id'>) => string;
  updateVariable: (id: string, updates: Partial<WorkflowVariable>) => void;
  removeVariable: (id: string) => void;
  setVariableValue: (id: string, value: unknown) => void;
  getVariable: (id: string) => WorkflowVariable | undefined;
  getVariablesByScope: (scope: VariableScope) => WorkflowVariable[];
  getVisibleVariables: (scope: VariableScope) => WorkflowVariable[];
  checkShadowing: () => string[];
  validateVariable: (variable: WorkflowVariable) => string[];
  importVariables: (vars: WorkflowVariable[]) => void;
  exportVariables: () => WorkflowVariable[];
  reset: () => void;
}

const SCOPE_HIERARCHY: VariableScope[] = [
  'global',
  'project',
  'environment',
  'workflow',
  'session',
  'subgraph',
  'node',
  'edge',
];

export const useVariableStore = create<VariableState>((set, get) => ({
  variables: [],
  scopeOrder: SCOPE_HIERARCHY,

  addVariable: (variable) => {
    const id = `var_${variable.name}_${Date.now()}`;
    const fullVar: WorkflowVariable = {
      id,
      name: variable.name,
      type: variable.type,
      scope: variable.scope,
      value: variable.defaultValue,
      description: variable.description,
      writable: variable.writable ?? true,
      defaultValue: variable.defaultValue,
    };
    set((state) => ({ variables: [...state.variables, fullVar] }));
    return id;
  },

  updateVariable: (id, updates) =>
    set((state) => ({
      variables: state.variables.map((v) =>
        v.id === id ? { ...v, ...updates } : v
      ),
    })),

  removeVariable: (id) =>
    set((state) => ({
      variables: state.variables.filter((v) => v.id !== id),
    })),

  setVariableValue: (id, value) =>
    set((state) => ({
      variables: state.variables.map((v) =>
        v.id === id ? { ...v, value } : v
      ),
    })),

  getVariable: (id) => get().variables.find((v) => v.id === id),

  getVariablesByScope: (scope) =>
    get().variables.filter((v) => v.scope === scope),

  getVisibleVariables: (scope) => {
    const currentIdx = SCOPE_HIERARCHY.indexOf(scope as VariableScope);
    if (currentIdx === -1) return [];
    // Variables at this scope and all higher (more global) scopes are visible
    const visibleScopes = SCOPE_HIERARCHY.slice(0, currentIdx + 1);
    return get().variables.filter((v) => visibleScopes.includes(v.scope));
  },

  checkShadowing: () => {
    const nameMap = new Map<string, WorkflowVariable[]>();
    for (const v of get().variables) {
      if (!nameMap.has(v.name)) nameMap.set(v.name, []);
      nameMap.get(v.name)!.push(v);
    }
    const shadows: string[] = [];
    for (const [name, vars] of nameMap) {
      if (vars.length > 1) {
        // Check if any share a parent-child scope relationship
        for (let i = 0; i < vars.length; i++) {
          for (let j = i + 1; j < vars.length; j++) {
            const vi = vars[i]!;
            const vj = vars[j]!;
            const si = SCOPE_HIERARCHY.indexOf(vi.scope as VariableScope);
            const sj = SCOPE_HIERARCHY.indexOf(vj.scope as VariableScope);
            if (si !== sj) {
              shadows.push(
                `Variable "${name}" shadowed: "${name}" (${vi.scope}) vs "${name}" (${vj.scope})`,
              );
            }
          }
        }
      }
    }
    return shadows;
  },

  validateVariable: (variable) => {
    const errors: string[] = [];
    if (!variable.name || variable.name.trim() === '') {
      errors.push('Variable name is required');
    }
    if (!variable.id) {
      errors.push('Variable id is required');
    }
    const validTypes: DataType[] = [
      'string', 'integer', 'float', 'boolean',
      'array', 'object', 'null', 'duration', 'timestamp',
    ];
    if (!(validTypes as string[]).includes(variable.type as string)) {
      errors.push(`Invalid variable type: ${variable.type}`);
    }
    return errors;
  },

  importVariables: (vars) => {
    set((state) => {
      const existingIds = new Set(state.variables.map((v) => v.id));
      const newVars = vars.filter((v) => !existingIds.has(v.id));
      return { variables: [...state.variables, ...newVars] };
    });
  },

  exportVariables: () => [...get().variables],

  reset: () => set({ variables: [] }),
}));
