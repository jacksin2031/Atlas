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

  it('derives execution lifecycle only from Runtime state and events', () => {
    useExecutionStore.getState().applyRuntimeState({ executionId: 'runtime-1', workflowId: 'wf_1', status: 'running', nodeStates: {}, nodeResults: {}, variables: {}, startedAt: new Date(0).toISOString(), metrics: { totalNodes: 0, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 } });
    expect(useExecutionStore.getState().isRunning).toBe(true);
    useExecutionStore.getState().applyRuntimeEvent({ eventId: 'pause', eventType: 'WorkflowPaused', timestamp: new Date().toISOString(), workflowId: 'wf_1', executionId: 'runtime-1', correlationId: 'runtime-1', data: {} });
    expect(useExecutionStore.getState().isPaused).toBe(true);
    useExecutionStore.getState().applyRuntimeEvent({ eventId: 'resume', eventType: 'WorkflowResumed', timestamp: new Date().toISOString(), workflowId: 'wf_1', executionId: 'runtime-1', correlationId: 'runtime-1', data: {} });
    expect(useExecutionStore.getState().isPaused).toBe(false);
    useExecutionStore.getState().applyRuntimeEvent({ eventId: 'stop', eventType: 'WorkflowCancelled', timestamp: new Date().toISOString(), workflowId: 'wf_1', executionId: 'runtime-1', correlationId: 'runtime-1', data: {} });
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
