import { useLogStore, useRuntimeStore } from "../stores";
import type { LogEntry, RuntimeInfo, RuntimeHealth, AppStatus } from "../types";

export class IPCService {
  private connected = false;

  connect(): void {
    this.connected = true;
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "IPCService",
      message: "IPC connected",
    });
  }

  disconnect(): void {
    this.connected = false;
  }

  isConnected(): boolean {
    return this.connected;
  }

  registerRuntime(runtimeInfo: RuntimeInfo): void {
    useRuntimeStore.getState().initializeRuntimes();
    useRuntimeStore.getState().setStatus(runtimeInfo.name, runtimeInfo.status);
    useRuntimeStore.getState().setHealth(runtimeInfo.name, runtimeInfo.health);
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "IPCService",
      message: `Runtime registered: ${runtimeInfo.name}`,
      runtime: runtimeInfo.name,
    });
  }

  forwardLog(entry: Omit<LogEntry, "id">): void {
    useLogStore.getState().addEntry(entry);
  }

  sendHealthUpdate(runtimeName: string, health: RuntimeHealth): void {
    useRuntimeStore.getState().setHealth(runtimeName, health);
  }

  sendStatusUpdate(runtimeName: string, status: AppStatus): void {
    useRuntimeStore.getState().setStatus(runtimeName, status);
  }

  queryRuntimes(): RuntimeInfo[] {
    return useRuntimeStore.getState().runtimes;
  }
}

export const ipcService = new IPCService();

