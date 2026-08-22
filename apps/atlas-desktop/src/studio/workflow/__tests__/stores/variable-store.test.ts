// Atlas Workflow Studio — Variable Store Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { useVariableStore } from '../../stores/variable-store';

describe('VariableStore', () => {
  beforeEach(() => {
    useVariableStore.getState().reset();
  });

  it('should add a variable', () => {
    const id = useVariableStore.getState().addVariable({
      name: 'count',
      type: 'integer',
      scope: 'workflow',
      writable: true,
      description: 'A counter',
    });
    expect(id).toBeTruthy();
    const vars = useVariableStore.getState().variables;
    expect(vars).toHaveLength(1);
    expect(vars[0]!.name).toBe('count');
  });

  it('should update a variable', () => {
    const id = useVariableStore.getState().addVariable({
      name: 'count',
      type: 'integer',
      scope: 'workflow',
      writable: true,
      description: '',
    });
    useVariableStore.getState().updateVariable(id, { name: 'total' });
    expect(useVariableStore.getState().getVariable(id)?.name).toBe('total');
  });

  it('should remove a variable', () => {
    const id = useVariableStore.getState().addVariable({
      name: 'count',
      type: 'integer',
      scope: 'workflow',
      writable: true,
      description: '',
    });
    useVariableStore.getState().removeVariable(id);
    expect(useVariableStore.getState().variables).toHaveLength(0);
  });

  it('should set variable value', () => {
    const id = useVariableStore.getState().addVariable({
      name: 'count',
      type: 'integer',
      scope: 'workflow',
      writable: true,
      description: '',
    });
    useVariableStore.getState().setVariableValue(id, 42);
    expect(useVariableStore.getState().getVariable(id)?.value).toBe(42);
  });

  it('should get variable by id', () => {
    useVariableStore.getState().addVariable({
      name: 'count',
      type: 'integer',
      scope: 'workflow',
      writable: true,
      description: '',
    });
    const vars = useVariableStore.getState().variables;
    expect(useVariableStore.getState().getVariable(vars[0]!.id)).toBeDefined();
  });

  it('should filter by scope', () => {
    useVariableStore.getState().addVariable({
      name: 'w', type: 'string' as any, scope: 'workflow', writable: true, description: '',
    });
    useVariableStore.getState().addVariable({
      name: 'n', type: 'string' as any, scope: 'node', writable: true, description: '',
    });
    const wfVars = useVariableStore.getState().getVariablesByScope('workflow');
    expect(wfVars).toHaveLength(1);
    expect(wfVars[0]!.name).toBe('w');
  });

  it('should check shadowing', () => {
    useVariableStore.getState().addVariable({
      name: 'x', type: 'integer' as any, scope: 'workflow', writable: true, description: '',
    });
    useVariableStore.getState().addVariable({
      name: 'x', type: 'integer' as any, scope: 'node', writable: true, description: '',
    });
    const shadows = useVariableStore.getState().checkShadowing();
    expect(shadows.length).toBeGreaterThan(0);
  });

  it('should validate variable', () => {
    const errors = useVariableStore.getState().validateVariable({
      id: 'v1', name: '', type: 'string' as any, scope: 'workflow', writable: true,
    });
    expect(errors).toContain('Variable name is required');
  });

  it('should import variables', () => {
    useVariableStore.getState().importVariables([
      { id: 'v1', name: 'a', type: 'string' as any, scope: 'workflow', writable: true },
      { id: 'v2', name: 'b', type: 'integer' as any, scope: 'node', writable: true },
    ]);
    expect(useVariableStore.getState().variables).toHaveLength(2);
  });

  it('should deduplicate on import', () => {
    useVariableStore.getState().importVariables([
      { id: 'v1', name: 'a', type: 'string' as any, scope: 'workflow', writable: true },
    ]);
    useVariableStore.getState().importVariables([
      { id: 'v1', name: 'renamed', type: 'string' as any, scope: 'workflow', writable: true },
    ]);
    expect(useVariableStore.getState().variables).toHaveLength(1);
  });

  it('should export variables', () => {
    useVariableStore.getState().addVariable({
      name: 'a', type: 'string' as any, scope: 'workflow', writable: true, description: '',
    });
    const exported = useVariableStore.getState().exportVariables();
    expect(exported).toHaveLength(1);
  });
});
