// Atlas Workflow Studio — Plugin Discovery Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { pluginDiscoveryService } from '../../services/plugin-discovery-service';
import { useNodeRegistryStore } from '../../stores';

describe('PluginDiscoveryService', () => {
  beforeEach(() => {
    useNodeRegistryStore.getState().reset();
  });

  it('should discover builtin nodes', async () => {
    const nodes = await pluginDiscoveryService.discoverFromPluginRuntime();
    expect(nodes.length).toBeGreaterThan(0);
  });

  it('should register discovered nodes', () => {
    const reg = {
      nodeId: 'test_1',
      typeName: 'test_op',
      category: 'custom',
      label: 'Test',
      description: 'A test node',
      inputs: [],
      outputs: [],
      parameters: {},
      version: '1.0.0',
      capabilities: [],
      pluginId: 'test',
    };
    pluginDiscoveryService.registerDiscoveredNodes([reg] as any);
    const found = useNodeRegistryStore.getState().getNodeRegistration('test_1');
    expect(found).toBeDefined();
    expect(found?.label).toBe('Test');
  });

  it('should watch for plugin changes', async () => {
    let called = false;
    const cleanup = pluginDiscoveryService.watchForPluginChanges(() => {
      called = true;
    });
    await pluginDiscoveryService.refresh();
    expect(called).toBe(true);
    cleanup();
  });

  it('should refresh nodes', async () => {
    await pluginDiscoveryService.refresh();
    const nodes = useNodeRegistryStore.getState().discoverNodes();
    expect(nodes.length).toBeGreaterThan(0);
  });
});
