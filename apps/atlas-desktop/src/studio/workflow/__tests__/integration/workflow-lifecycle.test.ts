// Atlas Workflow Studio — Canvas Integration Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { useWorkflowStore } from '../../stores/workflow-store';
import { useExecutionStore } from '../../stores/execution-store';
import { useDebugStore } from '../../stores/debug-store';
import { validationService } from '../../services/validation-service';
import { importExportService } from '../../services/import-export-service';
import type { WorkflowDefinition } from '../../types';

describe('Canvas Integration', () => {
  beforeEach(() => {
    useWorkflowStore.getState().resetCanvas();
    useExecutionStore.getState().reset();
    useDebugStore.getState().reset();
  });

  it('should complete a full workflow lifecycle', async () => {
    // 1. Create workflow
    const def: WorkflowDefinition = {
      id: 'wf_full',
      version: '1.0.0',
      name: 'Full Test',
      nodes: [
        { id: 'n1', type: 'entry', label: 'Entry', category: 'core', inputs: [], outputs: [], parameters: {} },
        { id: 'n2', type: 'execute', label: 'Process', category: 'core', inputs: [], outputs: [], parameters: {} },
      ],
      edges: [{ id: 'e1', source: 'n1', target: 'n2', edgeType: 'data' }],
      variables: [],
      parameters: {},
      metadata: { createdAt: Date.now(), updatedAt: Date.now(), tags: [] },
    };

    // 2. Load into store
    useWorkflowStore.getState().loadFromDefinition(def);
    expect(useWorkflowStore.getState().nodes).toHaveLength(2);
    expect(useWorkflowStore.getState().edges).toHaveLength(1);

    // 3. Validate
    const results = await validationService.validate(def);
    const errors = results.filter((r) => r.severity === 'error');
    expect(errors.length).toBe(0);

    // 4. Apply a backend-created execution session
    const runId = 'runtime-full';
    useExecutionStore.getState().applyRuntimeState({ executionId: runId, workflowId: 'wf_full', status: 'running', nodeStates: { n1: 'pending', n2: 'pending' }, nodeResults: {}, variables: {}, startedAt: new Date(0).toISOString(), metrics: { totalNodes: 2, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 } });
    expect(useExecutionStore.getState().isRunning).toBe(true);

    // 6. Update node states
    useExecutionStore.getState().updateNodeState(runId, 'n1', 'completed');
    useExecutionStore.getState().updateNodeState(runId, 'n2', 'running');

    // 7. Export
    const json = await importExportService.exportJSON(def);
    const exported = JSON.parse(json);
    expect(exported.id).toBe('wf_full');

    // 8. Clean up after a backend cancellation event
    useExecutionStore.getState().applyRuntimeEvent({ eventId: 'cancel', eventType: 'WorkflowCancelled', timestamp: new Date().toISOString(), workflowId: 'wf_full', executionId: runId, correlationId: runId, data: {} });
    useWorkflowStore.getState().resetCanvas();
    expect(useWorkflowStore.getState().nodes).toHaveLength(0);
  });

  it('should handle selection and movement', () => {
    useWorkflowStore.getState().addNode({
      id: 'a', type: 'execute', label: 'A', category: 'core',
      inputs: [], outputs: [], parameters: {}, x: 0, y: 0,
      priority: 0, timeout: undefined, retryPolicy: undefined,
      icon: undefined, executionState: 'pending', validationState: 'unchecked',
      statusMessage: '', documentationUrl: undefined, capabilities: [], version: '1.0.0',
    });
    useWorkflowStore.getState().selectNode('a');
    useWorkflowStore.getState().moveSelectedNodes(100, 50);
    const node = useWorkflowStore.getState().nodes[0]!;
    expect(node.x).toBe(100);
    expect(node.y).toBe(50);
  });

  it('should handle undo/redo with edges', () => {
    useWorkflowStore.getState().addNode({
      id: 'n1', type: 'execute', label: 'N1', category: 'core',
      inputs: [], outputs: [], parameters: {}, x: 0, y: 0,
      priority: 0, timeout: undefined, retryPolicy: undefined,
      icon: undefined, executionState: 'pending', validationState: 'unchecked',
      statusMessage: '', documentationUrl: undefined, capabilities: [], version: '1.0.0',
    });
    useWorkflowStore.getState().addEdge({ id: 'e1', source: 'n1', target: 'n1', edgeType: 'data' });
    useWorkflowStore.getState().undo();
    expect(useWorkflowStore.getState().nodes).toHaveLength(1);
    expect(useWorkflowStore.getState().edges).toHaveLength(0);
    useWorkflowStore.getState().undo();
    expect(useWorkflowStore.getState().nodes).toHaveLength(0);
    useWorkflowStore.getState().redo();
    expect(useWorkflowStore.getState().nodes).toHaveLength(1);
    expect(useWorkflowStore.getState().edges).toHaveLength(0);
    useWorkflowStore.getState().redo();
    expect(useWorkflowStore.getState().edges).toHaveLength(1);
  });
});
