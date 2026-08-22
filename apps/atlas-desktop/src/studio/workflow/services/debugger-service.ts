// Atlas Workflow Studio - Debugger Service
// RFC-0316 compliant debug interface via IPC

import type { Breakpoint, DebugEvent } from '../types';

export interface DebuggerService {
  attach(runId: string): Promise<void>;
  detach(): Promise<void>;
  setBreakpoint(bp: Omit<Breakpoint, 'id' | 'hitCount'>): Promise<string>;
  removeBreakpoint(id: string): Promise<void>;
  stepOver(runId: string): Promise<void>;
  stepInto(runId: string): Promise<void>;
  stepOut(runId: string): Promise<void>;
  continue(runId: string): Promise<void>;
  inspect(runId: string, nodeId: string): Promise<Record<string, unknown>>;
  modifyVariable(runId: string, name: string, value: unknown): Promise<void>;
  replay(runId: string): Promise<DebugEvent[]>;
  exportRecording(runId: string): Promise<string>;
}

export class IPCDebuggerService implements DebuggerService {
  private ipc: any;

  setIPC(ipc: any): void {
    this.ipc = ipc;
  }

  private async rpc<T>(command: string, args: Record<string, unknown>): Promise<T> {
    if (!this.ipc) throw new Error('IPC not connected');
    return ((this.ipc as any).invoke.bind(this.ipc))('workflow_debugger', { command, args }) as Promise<T>;
  }

  async attach(runId: string): Promise<void> {
    return this.rpc<void>('attach_debugger', { runId });
  }

  async detach(): Promise<void> {
    return this.rpc<void>('detach_debugger', {});
  }

  async setBreakpoint(bp: { type: string; targetId: string; condition?: string }): Promise<string> {
    return this.rpc<string>('set_breakpoint', { breakpoint: bp });
  }

  async removeBreakpoint(id: string): Promise<void> {
    return this.rpc<void>('remove_breakpoint', { id });
  }

  async stepOver(runId: string): Promise<void> {
    return this.rpc<void>('step_over', { runId });
  }

  async stepInto(runId: string): Promise<void> {
    return this.rpc<void>('step_into', { runId });
  }

  async stepOut(runId: string): Promise<void> {
    return this.rpc<void>('step_out', { runId });
  }

  async continue(runId: string): Promise<void> {
    return this.rpc<void>('continue_execution', { runId });
  }

  async inspect(runId: string, nodeId: string): Promise<Record<string, unknown>> {
    return this.rpc<Record<string, unknown>>('inspect_node', { runId, nodeId });
  }

  async modifyVariable(runId: string, name: string, value: unknown): Promise<void> {
    return this.rpc<void>('modify_variable', { runId, name, value });
  }

  async replay(runId: string): Promise<DebugEvent[]> {
    return this.rpc<DebugEvent[]>('replay_session', { runId });
  }

  async exportRecording(runId: string): Promise<string> {
    return this.rpc<string>('export_recording', { runId });
  }
}

export const debuggerService = new IPCDebuggerService();
