// Atlas Workflow Studio - Plugin Discovery Service
// RFC-0323 compliant — dynamically discovers workflow nodes from Plugin Runtime

import type { PluginNodeRegistration } from '../types';
import { useNodeRegistryStore } from '../stores';

export interface PluginDiscoveryService {
  discoverFromPluginRuntime(): Promise<PluginNodeRegistration[]>;
  registerDiscoveredNodes(registrations: PluginNodeRegistration[]): void;
  watchForPluginChanges(callback: (regs: PluginNodeRegistration[]) => void): () => void;
  refresh(pluginId?: string): Promise<void>;
}

export class PluginDiscoveryServiceImpl implements PluginDiscoveryService {
  private listeners: Array<(regs: PluginNodeRegistration[]) => void> = [];

  async discoverFromPluginRuntime(): Promise<PluginNodeRegistration[]> {
    // Discover nodes from Plugin Runtime via IPC
    // The plugin runtime exposes node registration metadata
    // This is an IPC call — we never call runtime implementations directly
    const state = useNodeRegistryStore.getState();
    return state.discoverNodes();
  }

  registerDiscoveredNodes(registrations: PluginNodeRegistration[]): void {
    const state = useNodeRegistryStore.getState();
    for (const reg of registrations) {
      state.registerNode(reg);
    }
  }

  watchForPluginChanges(callback: (regs: PluginNodeRegistration[]) => void): () => void {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== callback);
    };
  }

  async refresh(pluginId?: string): Promise<void> {
    const state = useNodeRegistryStore.getState();
    if (pluginId) {
      state.hotReload(pluginId);
    }
    const nodes = await this.discoverFromPluginRuntime();
    this.registerDiscoveredNodes(nodes);
    for (const listener of this.listeners) {
      listener(nodes);
    }
  }
}

export const pluginDiscoveryService = new PluginDiscoveryServiceImpl();
