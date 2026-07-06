// Atlas Workflow Studio — Validation Service Tests

import { describe, it, expect } from 'vitest';
import { validationService } from '../../services/validation-service';
import type { WorkflowDefinition } from '../../types';

function createTestWorkflow(overrides: Partial<WorkflowDefinition> = {}): WorkflowDefinition {
  return {
    id: 'wf_test',
    version: '1.0.0',
    name: 'Test Workflow',
    nodes: [
      { id: 'n1', type: 'entry', label: 'Entry', category: 'core', inputs: [], outputs: [{ id: 'out_0', name: 'out', type: 'object' }], parameters: {} },
      { id: 'n2', type: 'execute', label: 'Execute', category: 'core', inputs: [{ id: 'in_0', name: 'in', type: 'object' }], outputs: [{ id: 'out_0', name: 'out', type: 'object' }], parameters: {} },
      { id: 'n3', type: 'exit', label: 'Exit', category: 'core', inputs: [{ id: 'in_0', name: 'in', type: 'object' }], outputs: [], parameters: {} },
    ],
    edges: [
      { id: 'e1', source: 'n1', target: 'n2', edgeType: 'data' },
      { id: 'e2', source: 'n2', target: 'n3', edgeType: 'data' },
    ],
    variables: [],
    parameters: {},
    metadata: { createdAt: Date.now(), updatedAt: Date.now(), tags: [] },
    ...overrides,
  };
}

describe('ValidationService', () => {
  it('should validate a correct workflow', async () => {
    const results = await validationService.validate(createTestWorkflow());
    const errors = results.filter((r) => r.severity === 'error');
    expect(errors).toHaveLength(0);
  });

  it('should detect cycles', async () => {
    const def = createTestWorkflow({
      edges: [
        { id: 'e1', source: 'n1', target: 'n2', edgeType: 'data' },
        { id: 'e2', source: 'n2', target: 'n3', edgeType: 'data' },
        { id: 'e3', source: 'n3', target: 'n1', edgeType: 'data' },
      ],
    });
    const results = await validationService.validate(def);
    const cycleErrors = results.filter((r) => r.rule === 'no_cycles' && r.severity === 'error');
    expect(cycleErrors.length).toBeGreaterThan(0);
  });

  it('should detect disconnected nodes', async () => {
    const def = createTestWorkflow({
      nodes: [
        ...createTestWorkflow().nodes,
        { id: 'isolated', type: 'execute', label: 'Isolated', category: 'core', inputs: [], outputs: [], parameters: {} },
      ],
    });
    const results = await validationService.validate(def);
    const disconnectWarnings = results.filter((r) => r.rule === 'disconnected_nodes');
    expect(disconnectWarnings.length).toBeGreaterThan(0);
  });

  it('should detect duplicate IDs', async () => {
    const def = createTestWorkflow({
      nodes: [
        ...createTestWorkflow().nodes,
        { id: 'n1', type: 'execute', label: 'Dup', category: 'core', inputs: [], outputs: [], parameters: {} },
      ],
    });
    const results = await validationService.validate(def);
    const dupErrors = results.filter((r) => r.rule === 'duplicate_ids' && r.severity === 'error');
    expect(dupErrors.length).toBeGreaterThan(0);
  });

  it('should detect invalid edge targets', async () => {
    const def = createTestWorkflow({
      edges: [{ id: 'bad', source: 'nonexistent', target: 'n1', edgeType: 'data' }],
    });
    const results = await validationService.validate(def);
    const edgeErrors = results.filter((r) => r.rule === 'invalid_edge_targets' && r.severity === 'error');
    expect(edgeErrors.length).toBeGreaterThan(0);
  });

  it('should get all rules', () => {
    const rules = validationService.getAllRules();
    expect(rules.length).toBeGreaterThan(0);
  });

  it('should get rule by id', () => {
    const rule = validationService.getRuleById('no_cycles');
    expect(rule).toBeDefined();
    expect(rule?.name).toBe('No Cycles');
  });

  it('should return undefined for unknown rule', () => {
    expect(validationService.getRuleById('nonexistent')).toBeUndefined();
  });
});
