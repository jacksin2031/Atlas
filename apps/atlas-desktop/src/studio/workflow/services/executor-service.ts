// Atlas Workflow Studio - Executor Service
// Bridges to Workflow Runtime via IPC (RFC-0303, RFC-0304)
// Never calls runtime implementations directly

import type { WorkflowRunStatus, ExecutionError } from '../types';

export interface ExecutorService {
  run(workflowId: string): Promise<string>;
  pause(runId: string): Promise<void>;
  resume(runId: string): Promise<void>;
  stop(runId: string): Promise<void>;
  step(runId: string): Promise<void>;
  restart(runId: string): Promise<void>;
  simulate(runId: string): Promise<void>;
  dryRun(workflowId: string): Promise<ExecutionError[]>;
  getStatus(runId: string): Promise<WorkflowRunStatus>;
}

// IPC bridge wrapper — all calls go through the Desktop Shell IPC layer
export class IPCExecutorService implements ExecutorService {
  private ipc: any = null;

  setIPC(ipc: any): void {
    this.ipc = ipc;
  }

  private async rpc<T>(command: string, args: Record<string, unknown>): Promise<T> {
    if (!this.ipc) {
      throw new Error('IPC not connected');
    }
    // Forward to Tauri command via IPC bridge
    // In production this uses @tauri-apps/api invoke
    return ((this.ipc as any).invoke.bind(this.ipc))('workflow_executor', { command, args }) as Promise<T>;
  }

  async run(workflowId: string): Promise<string> {
    return this.rpc<string>('run_workflow', { workflowId });
  }

  async pause(runId: string): Promise<void> {
    return this.rpc<void>('pause_execution', { runId });
  }

  async resume(runId: string): Promise<void> {
    return this.rpc<void>('resume_execution', { runId });
  }

  async stop(runId: string): Promise<void> {
    return this.rpc<void>('stop_execution', { runId });
  }

  async step(runId: string): Promise<void> {
    return this.rpc<void>('step_execution', { runId });
  }

  async restart(runId: string): Promise<void> {
    return this.rpc<void>('restart_execution', { runId });
  }

  async simulate(runId: string): Promise<void> {
    return this.rpc<void>('simulate_execution', { runId });
  }

  async dryRun(workflowId: string): Promise<ExecutionError[]> {
    return this.rpc<ExecutionError[]>('dry_run', { workflowId });
  }

  async getStatus(runId: string): Promise<WorkflowRunStatus> {
    return this.rpc<WorkflowRunStatus>('get_execution_status', { runId });
  }
}

export const executorService = new IPCExecutorService();
