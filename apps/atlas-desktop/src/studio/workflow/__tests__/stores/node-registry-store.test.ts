// Atlas Workflow Studio — Node Registry Store Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { useNodeRegistryStore } from '../../stores/node-registry-store';

describe('NodeRegistryStore', () => {
  beforeEach(() => {
    useNodeRegistryStore.getState().reset();
  });

  it('should have builtin nodes', () => {
    const nodes = useNodeRegistryStore.getState().discoverNodes();
    expect(nodes.length).toBeGreaterThan(0);
  });

  it('should register a node', () => {
    useNodeRegistryStore.getState().registerNode({
      nodeId: 'custom_1',
      typeName: 'custom_op',
      category: 'custom',
      label: 'Custom Op',
      description: 'A custom operation',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '1.0.0',
      capabilities: [],
      pluginId: 'custom_plugin',
    });
    const reg = useNodeRegistryStore.getState().getNodeRegistration('custom_1');
    expect(reg).toBeDefined();
    expect(reg?.label).toBe('Custom Op');
  });

  it('should unregister a node', () => {
    useNodeRegistryStore.getState().registerNode({
      nodeId: 'custom_1',
      typeName: 'custom_op',
      category: 'custom',
      label: 'Custom Op',
      description: '',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '1.0.0',
      capabilities: [],
      pluginId: 'custom_plugin',
    });
    useNodeRegistryStore.getState().unregisterNode('custom_1');
    expect(useNodeRegistryStore.getState().getNodeRegistration('custom_1')).toBeUndefined();
  });

  it('should get nodes by category', () => {
    const aiNodes = useNodeRegistryStore.getState().getNodesByCategory('ai');
    expect(aiNodes).toHaveLength(1); // ai_operation builtin
  });

  it('should discover all nodes', () => {
    useNodeRegistryStore.getState().registerNode({
      nodeId: 'custom_1',
      typeName: 'custom_op',
      category: 'custom',
      label: 'Custom Op',
      description: '',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '1.0.0',
      capabilities: [],
      pluginId: 'custom_plugin',
    });
    const nodes = useNodeRegistryStore.getState().discoverNodes();
    const typeNames = nodes.map((n) => n.typeName);
    expect(typeNames).toContain('execute');
    expect(typeNames).toContain('ai_operation');
    expect(typeNames).toContain('custom_op');
  });

  it('should deduplicate by type name on discover', () => {
    useNodeRegistryStore.getState().registerNode({
      nodeId: 'dup_1',
      typeName: 'execute',
      category: 'core',
      label: 'Execute Override',
      description: '',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '2.0.0',
      capabilities: [],
      pluginId: 'override',
    });
    const nodes = useNodeRegistryStore.getState().discoverNodes();
    const executeNodes = nodes.filter((n) => n.typeName === 'execute');
    expect(executeNodes).toHaveLength(1);
  });

  it('should hot reload a plugin', () => {
    useNodeRegistryStore.getState().registerNode({
      nodeId: 'hot_1',
      typeName: 'hot_reload_test',
      category: 'custom',
      label: 'Hot Reload',
      description: '',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '1.0.0',
      capabilities: [],
      pluginId: 'test_plugin',
    });
    useNodeRegistryStore.getState().hotReload('test_plugin');
    expect(useNodeRegistryStore.getState().getNodeRegistration('hot_1')).toBeUndefined();
  });

  it('should check category existence', () => {
    expect(useNodeRegistryStore.getState().hasCategory('ai')).toBe(true);
  });
});
