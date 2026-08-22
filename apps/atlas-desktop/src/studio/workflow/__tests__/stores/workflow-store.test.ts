// Atlas Workflow Studio — Workflow Store Tests
// Tests: node CRUD, selection, undo/redo, transform, variables

import { describe, it, expect, beforeEach } from 'vitest';
import { useWorkflowStore, type WorkflowGraphNode, type WorkflowGraphEdge } from '../../stores/workflow-store';

function createTestNode(id: string, x = 0, y = 0): WorkflowGraphNode {
  return {
    id,
    type: 'execute',
    label: 'Test Node', 
    category: 'core',
    inputs: [{ id: 'in_0', name: 'input', type: 'object', multiple: false, dynamic: false }],
    outputs: [{ id: 'out_0', name: 'output', type: 'object', multiple: false, dynamic: false }],
    parameters: {},
    x,
    y,
    priority: 0,
    timeout: undefined,
    retryPolicy: undefined,
    icon: undefined,
    executionState: 'pending',
    validationState: 'unchecked',
    statusMessage: '',
    documentationUrl: undefined,
    capabilities: [],
    version: '1.0.0',
  };
}

function createTestEdge(source: string, target: string): WorkflowGraphEdge {
  return {
    id: `edge_${source}_${target}`,
    source,
    target,
    edgeType: 'data',
  };
}

describe('WorkflowStore', () => {
  beforeEach(() => {
    useWorkflowStore.getState().resetCanvas();
  });

  describe('Node operations', () => {
    it('should add a node', () => {
      const node = createTestNode('node_1');
      useWorkflowStore.getState().addNode(node);
      expect(useWorkflowStore.getState().nodes).toHaveLength(1);
      expect(useWorkflowStore.getState().nodes[0]!.id).toBe('node_1');
    });

    it('should update a node', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().updateNode('node_1', { label: 'Updated' });
      expect(useWorkflowStore.getState().nodes[0]!.label).toBe('Updated');
    });

    it('should remove a node and its edges', () => {
      const n1 = createTestNode('node_1');
      const n2 = createTestNode('node_2');
      useWorkflowStore.getState().addNode(n1);
      useWorkflowStore.getState().addNode(n2);
      useWorkflowStore.getState().addEdge(createTestEdge('node_1', 'node_2'));
      useWorkflowStore.getState().removeNode('node_1');
      expect(useWorkflowStore.getState().nodes).toHaveLength(1);
      expect(useWorkflowStore.getState().edges).toHaveLength(0);
    });

    it('should duplicate a node', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1', 100, 100));
      useWorkflowStore.getState().duplicateNode('node_1');
      const nodes = useWorkflowStore.getState().nodes;
      expect(nodes).toHaveLength(2);
      expect(nodes[1]!.id).not.toBe('node_1');
      expect(nodes[1]!.label).toContain('(copy)');
    });

    it('should set nodes', () => {
      const nodes = [createTestNode('a'), createTestNode('b')];
      useWorkflowStore.getState().setNodes(nodes);
      expect(useWorkflowStore.getState().nodes).toHaveLength(2);
    });
  });

  describe('Edge operations', () => {
    it('should add an edge', () => {
      useWorkflowStore.getState().addEdge(createTestEdge('a', 'b'));
      expect(useWorkflowStore.getState().edges).toHaveLength(1);
    });

    it('should remove an edge', () => {
      useWorkflowStore.getState().addEdge(createTestEdge('a', 'b'));
      useWorkflowStore.getState().removeEdge('edge_a_b');
      expect(useWorkflowStore.getState().edges).toHaveLength(0);
    });
  });

  describe('Selection', () => {
    it('should select a node', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().selectNode('node_1');
      expect(useWorkflowStore.getState().selectedNodeIds).toEqual(['node_1']);
    });

    it('should deselect all', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().selectNode('node_1');
      useWorkflowStore.getState().deselectAll();
      expect(useWorkflowStore.getState().selectedNodeIds).toHaveLength(0);
    });

    it('should multi-select nodes', () => {
      useWorkflowStore.getState().addNode(createTestNode('a'));
      useWorkflowStore.getState().addNode(createTestNode('b'));
      useWorkflowStore.getState().selectNode('a', true);
      useWorkflowStore.getState().selectNode('b', true);
      expect(useWorkflowStore.getState().selectedNodeIds).toHaveLength(2);
    });

    it('should toggle selection on multi-select', () => {
      useWorkflowStore.getState().addNode(createTestNode('a'));
      useWorkflowStore.getState().selectNode('a', true);
      useWorkflowStore.getState().selectNode('a', true);
      expect(useWorkflowStore.getState().selectedNodeIds).toHaveLength(0);
    });
  });

  describe('Undo/Redo', () => {
    it('should push history on add', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      expect(useWorkflowStore.getState().historyIndex).toBeGreaterThan(0);
    });

    it('should undo', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().undo();
      expect(useWorkflowStore.getState().nodes).toHaveLength(0);
    });

    it('should redo', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().undo();
      useWorkflowStore.getState().redo();
      expect(useWorkflowStore.getState().nodes).toHaveLength(1);
    });

    it('should not undo past beginning', () => {
      useWorkflowStore.getState().undo();
      expect(useWorkflowStore.getState().nodes).toHaveLength(0);
    });

    it('should not redo past end', () => {
      useWorkflowStore.getState().redo();
      expect(useWorkflowStore.getState().nodes).toHaveLength(0);
    });
  });

  describe('Canvas transform', () => {
    it('should pan canvas', () => {
      useWorkflowStore.getState().panCanvas(10, 20);
      const t = useWorkflowStore.getState().transform;
      expect(t.x).toBe(10);
      expect(t.y).toBe(20);
    });

    it('should zoom canvas', () => {
      useWorkflowStore.getState().zoomCanvas(0.5);
      expect(useWorkflowStore.getState().transform.zoom).toBe(1.5);
    });

    it('should clamp zoom', () => {
      useWorkflowStore.getState().zoomCanvas(-2);
      expect(useWorkflowStore.getState().transform.zoom).toBeGreaterThanOrEqual(0.1);
    });
  });

  describe('Move selected nodes', () => {
    it('should move selected nodes', () => {
      useWorkflowStore.getState().addNode(createTestNode('a', 0, 0));
      useWorkflowStore.getState().selectNode('a');
      useWorkflowStore.getState().moveSelectedNodes(50, 30);
      const node = useWorkflowStore.getState().nodes[0]!;
      expect(node.x).toBe(50);
      expect(node.y).toBe(30);
    });

    it('should not move unselected nodes', () => {
      useWorkflowStore.getState().addNode(createTestNode('a', 0, 0));
      useWorkflowStore.getState().addNode(createTestNode('b', 100, 100));
      useWorkflowStore.getState().selectNode('a');
      useWorkflowStore.getState().moveSelectedNodes(50, 0);
      expect(useWorkflowStore.getState().nodes[0]!.x).toBe(50);
      expect(useWorkflowStore.getState().nodes[1]!.x).toBe(100);
    });
  });

  describe('Execution state', () => {
    it('should update node execution state', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().updateNodeExecutionState('node_1', 'running');
      const node = useWorkflowStore.getState().nodes[0]!;
      expect(node.executionState).toBe('running');
    });

    it('should update node validation state', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().updateNodeValidationState('node_1', 'valid');
      const node = useWorkflowStore.getState().nodes[0]!;
      expect(node.validationState).toBe('valid');
    });
  });

  describe('Import/Export', () => {
    it('should export to definition', () => {
      useWorkflowStore.getState().setWorkflowInfo('wf_1', 'Test', '1.0.0');
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      const def = useWorkflowStore.getState().exportToDefinition();
      expect(def.id).toBe('wf_1');
      expect(def.name).toBe('Test');
      expect(def.nodes).toHaveLength(1);
    });
  });

  describe('Variables', () => {
    it('should add a variable', () => {
      useWorkflowStore.getState().addVariable({
        id: 'v1', name: 'count', type: 'integer', scope: 'workflow', writable: true,
      });
      expect(useWorkflowStore.getState().variables).toHaveLength(1);
    });

    it('should update a variable', () => {
      useWorkflowStore.getState().addVariable({
        id: 'v1', name: 'count', type: 'integer', scope: 'workflow', writable: true,
      });
      useWorkflowStore.getState().updateVariable('v1', { name: 'total' });
      expect(useWorkflowStore.getState().variables[0]!.name).toBe('total');
    });

    it('should remove a variable', () => {
      useWorkflowStore.getState().addVariable({
        id: 'v1', name: 'count', type: 'integer', scope: 'workflow', writable: true,
      });
      useWorkflowStore.getState().removeVariable('v1');
      expect(useWorkflowStore.getState().variables).toHaveLength(0);
    });
  });

  describe('Reset', () => {
    it('should reset canvas to empty state', () => {
      useWorkflowStore.getState().addNode(createTestNode('node_1'));
      useWorkflowStore.getState().addEdge(createTestEdge('a', 'b'));
      useWorkflowStore.getState().resetCanvas();
      expect(useWorkflowStore.getState().nodes).toHaveLength(0);
      expect(useWorkflowStore.getState().edges).toHaveLength(0);
      expect(useWorkflowStore.getState().variables).toHaveLength(0);
    });
  });
});
