// Atlas Workflow Studio — Execution Store Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { useExecutionStore } from '../../stores/execution-store';

describe('ExecutionStore', () => {
  beforeEach(() => {
    useExecutionStore.getState().reset();
  });

  it('should create a run', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    expect(runId).toBeTruthy();
    const run = useExecutionStore.getState().runs[runId]!;
    expect(run).toBeDefined();
    expect(run.workflowId).toBe('wf_1');
    expect(run?.status).toBe('created');
  });

  it('should set active run', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().setActiveRun(runId);
    expect(useExecutionStore.getState().activeRunId).toBe(runId);
  });

  it('should update run status', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().updateRunStatus(runId, 'running');
    expect(useExecutionStore.getState().runs[runId]!.status).toBe('running');
    expect(useExecutionStore.getState().isRunning).toBe(true);
  });

  it('should update node state', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().updateNodeState(runId, 'node_1', 'running');
    expect(useExecutionStore.getState().runs[runId]!.nodeStates['node_1']).toBe('running');
  });

  it('should add execution error', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().addExecutionError(runId, {
      nodeId: 'node_1',
      errorCode: 'E_TIMEOUT',
      message: 'Timed out',
      timestamp: Date.now(),
    });
    expect(useExecutionStore.getState().runs[runId]!.errors).toHaveLength(1);
  });

  it('should start execution', () => {
    useExecutionStore.getState().startExecution();
    expect(useExecutionStore.getState().status).toBe('running');
    expect(useExecutionStore.getState().isRunning).toBe(true);
  });

  it('should pause execution', () => {
    useExecutionStore.getState().startExecution();
    useExecutionStore.getState().pauseExecution();
    expect(useExecutionStore.getState().isPaused).toBe(true);
  });

  it('should resume execution', () => {
    useExecutionStore.getState().startExecution();
    useExecutionStore.getState().pauseExecution();
    useExecutionStore.getState().resumeExecution();
    expect(useExecutionStore.getState().isPaused).toBe(false);
  });

  it('should stop execution', () => {
    useExecutionStore.getState().startExecution();
    useExecutionStore.getState().stopExecution();
    expect(useExecutionStore.getState().isRunning).toBe(false);
  });

  it('should start simulation', () => {
    useExecutionStore.getState().startSimulation();
    expect(useExecutionStore.getState().isSimulating).toBe(true);
  });

  it('should start dry run', () => {
    useExecutionStore.getState().startDryRun();
    expect(useExecutionStore.getState().isDryRunning).toBe(true);
  });

  it('should clear run', () => {
    const runId = useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().clearRun(runId);
    expect(useExecutionStore.getState().runs[runId]!).toBeUndefined();
  });

  it('should reset', () => {
    useExecutionStore.getState().createRun('wf_1');
    useExecutionStore.getState().reset();
    expect(useExecutionStore.getState().runs).toEqual({});
    expect(useExecutionStore.getState().activeRunId).toBeNull();
    expect(useExecutionStore.getState().isRunning).toBe(false);
  });
});
