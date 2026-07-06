import { useLogStore } from "../stores";
import type { PluginEntry, PluginState as PluginStateType, PluginHealth as PluginHealthType } from "../types";

export class PluginManagerService {
  private initialized = false;

  initialize(): void {
    this.initialized = true;
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "PluginManagerService",
      message: "Plugin manager initialized",
    });
  }

  togglePlugin(id: string): void {
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "PluginManagerService",
      message: "Plugin toggled: " + id,
    });
  }

  setPluginHealth(_id: string, _health: PluginHealthType): void {
    // Handled by usePluginStore
  }

  setPluginState(_id: string, _state: PluginStateType): void {
    // Handled by usePluginStore
  }

  getPlugin(_id: string): PluginEntry | undefined {
    return undefined;
  }

  getAllPlugins(): PluginEntry[] {
    return [];
  }

  searchPlugins(_query: string): PluginEntry[] {
    return [];
  }

  isInitialized(): boolean {
    return this.initialized;
  }
}

export const pluginManagerService = new PluginManagerService();
