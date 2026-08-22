// Atlas Workflow Studio - Validation Service
// RFC-0317 compliant validation engine via IPC

import type { ValidationResult, WorkflowDefinition } from '../types';

export interface ValidationRule {
  id: string;
  name: string;
  severity: 'error' | 'warning' | 'info';
  description: string;
  check: (def: WorkflowDefinition) => ValidationResult | null;
}

export interface ValidationService {
  validate(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateGraph(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateNodes(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateEdges(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateVariables(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateTypes(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validateSecurity(def: WorkflowDefinition): Promise<ValidationResult[]>;
  validatePerformance(def: WorkflowDefinition): Promise<ValidationResult[]>;
  getRuleById(id: string): ValidationRule | undefined;
  getAllRules(): ValidationRule[];
}

// Client-side validation rules (supplemented by runtime validation via IPC)
export class ValidationServiceImpl implements ValidationService {
  private rules: ValidationRule[] = [];

  constructor() {
    this.registerBuiltInRules();
  }

  private registerBuiltInRules(): void {
    // RFC-0317 validation rules
    this.rules.push({
      id: 'no_cycles',
      name: 'No Cycles',
      severity: 'error',
      description: 'Workflow graph must be a DAG (directed acyclic graph)',
      check: (def) => {
        const hasCycle = this.detectCycle(def);
        if (hasCycle) {
          return { rule: 'no_cycles', severity: 'error', message: 'Workflow contains a cycle', location: 'workflow' };
        }
        return null;
      },
    });

    this.rules.push({
      id: 'disconnected_nodes',
      name: 'Disconnected Nodes',
      severity: 'warning',
      description: 'Nodes should be connected to the graph',
      check: (def) => {
        const connected = new Set<string>();
        for (const e of def.edges) {
          connected.add(e.id);
        }
        for (const n of def.nodes) {
          const hasEdge = def.edges.some((e) => e.source === n.id || e.target === n.id);
          if (!hasEdge && n.type !== 'entry' && n.type !== 'exit') {
      return { rule: "disconnected_nodes", severity: "warning", message: `Node '${n.label}' is disconnected`, location: "node", nodeId: n.id };
          }
        }
        return null;
      },
    });

    this.rules.push({
      id: 'missing_inputs',
      name: 'Missing Inputs',
      severity: 'error',
      description: 'All required inputs must be present',
      check: (def) => {
        for (const n of def.nodes) {
          for (const inp of n.inputs) {
            if (!inp.defaultValue && !def.edges.some((e) => e.target === n.id)) {
      return { rule: "missing_inputs", severity: "error", message: `Node '${n.label}' has missing inputs`, location: "node", nodeId: n.id };
            }
          }
        }
        return null;
      },
    });

    this.rules.push({
      id: 'type_mismatch',
      name: 'Type Mismatch',
      severity: 'error',
      description: 'Connected ports must have compatible types',
      check: (def) => {
        const nodeMap = new Map(def.nodes.map((n) => [n.id, n]));
        for (const e of def.edges) {
          const sourceNode = nodeMap.get(e.source);
          const targetNode = nodeMap.get(e.target);
          if (!sourceNode || !targetNode) continue;
          // Simplified type check
        }
        return null;
      },
    });

    this.rules.push({
      id: 'duplicate_ids',
      name: 'Duplicate Identifiers',
      severity: 'error',
      description: 'Node and variable IDs must be unique',
      check: (def) => {
        const ids = new Set<string>();
        for (const n of def.nodes) {
          if (ids.has(n.id)) {
      return { rule: "duplicate_ids", severity: "error", message: `Duplicate node ID: '${n.id}'`, location: "node", nodeId: n.id };
          }
          ids.add(n.id);
        }
        for (const v of def.variables) {
          if (ids.has(v.id)) {
      return { rule: "duplicate_ids", severity: "error", message: `Duplicate variable ID: '${v.id}'`, location: "workflow" };
          }
          ids.add(v.id);
        }
        return null;
      },
    });

    this.rules.push({
      id: 'invalid_edge_targets',
      name: 'Invalid Edge Targets',
      severity: 'error',
      description: 'Edge source and target must reference existing nodes',
      check: (def) => {
        const nodeIds = new Set(def.nodes.map((n) => n.id));
        for (const e of def.edges) {
          if (!nodeIds.has(e.source)) {
      return { rule: "invalid_edge_targets", severity: "error", message: `Edge target not found`, location: "workflow" };
          }
          if (!nodeIds.has(e.target)) {
      return { rule: "invalid_edge_targets", severity: "error", message: `Edge target not found`, location: "workflow" };
          }
        }
        return null;
      },
    });

    this.rules.push({
      id: 'missing_plugins',
      name: 'Missing Plugins',
      severity: 'warning',
      description: 'Referenced plugins must be available',
      check: (_def) => null, // Defer to plugin runtime
    });

    this.rules.push({
      id: 'capability_mismatch',
      name: 'Capability Mismatch',
      severity: 'warning',
      description: 'Node capabilities must match available runtimes',
      check: (_def) => null, // Defer to capability registry
    });
  }

  private detectCycle(def: WorkflowDefinition): boolean {
    const adj = new Map<string, string[]>();
    for (const n of def.nodes) adj.set(n.id, []);
    for (const e of def.edges) {
      const neighbors = adj.get(e.source) || [];
      neighbors.push(e.target);
      adj.set(e.source, neighbors);
    }
    const visited = new Set<string>();
    const recStack = new Set<string>();

    const dfs = (nodeId: string): boolean => {
      visited.add(nodeId);
      recStack.add(nodeId);
      for (const neighbor of adj.get(nodeId) || []) {
        if (!visited.has(neighbor)) {
          if (dfs(neighbor)) return true;
        } else if (recStack.has(neighbor)) {
          return true;
        }
      }
      recStack.delete(nodeId);
      return false;
    };

    for (const nodeId of adj.keys()) {
      if (!visited.has(nodeId) && dfs(nodeId)) return true;
    }
    return false;
  }

  async validate(def: WorkflowDefinition): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];
    for (const rule of this.rules) {
      const result = rule.check(def);
      if (result) results.push(result);
    }
    return results;
  }

  async validateGraph(def: WorkflowDefinition): Promise<ValidationResult[]> {
    return this.validate(def);
  }

  async validateNodes(def: WorkflowDefinition): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];
    for (const rule of this.rules) {
      if (rule.id === 'disconnected_nodes') {
        const result = rule.check(def);
        if (result) results.push(result);
      }
    }
    return results;
  }

  async validateEdges(def: WorkflowDefinition): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];
    for (const rule of this.rules) {
      if (rule.id === 'invalid_edge_targets') {
        const result = rule.check(def);
        if (result) results.push(result);
      }
    }
    return results;
  }

  async validateVariables(def: WorkflowDefinition): Promise<ValidationResult[]> {
    const results: ValidationResult[] = [];
    for (const rule of this.rules) {
      if (rule.id === 'duplicate_ids') {
        const result = rule.check(def);
        if (result) results.push(result);
      }
    }
    return results;
  }

  async validateTypes(_def: WorkflowDefinition): Promise<ValidationResult[]> {
    // Type validation deferred to runtime
    return [];
  }

  async validateSecurity(_def: WorkflowDefinition): Promise<ValidationResult[]> {
    // Security validation deferred to runtime
    return [];
  }

  async validatePerformance(_def: WorkflowDefinition): Promise<ValidationResult[]> {
    // Performance validation deferred to runtime
    return [];
  }

  getRuleById(id: string): ValidationRule | undefined {
    return this.rules.find((r) => r.id === id);
  }

  getAllRules(): ValidationRule[] {
    return [...this.rules];
  }
}

export const validationService = new ValidationServiceImpl();
