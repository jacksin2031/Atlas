// Atlas Workflow Studio - Node Canvas
// Main React Flow canvas with zoom, minimap, pan, selection

import React, { useCallback, useMemo, useRef, useEffect } from 'react';
import {
  ReactFlow,
  Controls,
  MiniMap,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  type Connection,
  type NodeChange,
  type EdgeChange,
  type OnSelectionChangeParams,
  type OnNodesChange,
  type OnEdgesChange,
  type OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import {
  useWorkflowStore,
  useExecutionStore,
} from "../../stores";
import { NODE_TYPES, getNodeTypeName } from "../nodes/index";
import { EDGE_TYPES } from "../edges";
import type { WorkflowGraphEdge } from "../../stores/workflow-store";
import type { DraggableNodeTemplate } from "../../hooks/use-canvas-drag-drop";
import {
  cancelPalettePointerDrag,
  createNodeFromTemplate as _createNodeFromTemplate,
  takePalettePointerDrop,
  updatePalettePointerDrag,
} from "../../hooks/use-canvas-drag-drop";

const NODE_WIDTH = 220;

export const WorkflowCanvas: React.FC = () => {
  const nodes = useWorkflowStore((s) => s.nodes);
  const edges = useWorkflowStore((s) => s.edges);
  const setNodes = useWorkflowStore((s) => s.setNodes);
  const setNodePosition = useWorkflowStore((s) => s.setNodePosition);
  const pushHistory = useWorkflowStore((s) => s.pushHistory);
  const removeNode = useWorkflowStore((s) => s.removeNode);
  const setEdges = useWorkflowStore((s) => s.setEdges);
  const removeEdge = useWorkflowStore((s) => s.removeEdge);
  const selectNode = useWorkflowStore((s) => s.selectNode);
  const selectEdge = useWorkflowStore((s) => s.selectEdge);
  const setSelection = useWorkflowStore((s) => s.setSelection);
  const deselectAll = useWorkflowStore((s) => s.deselectAll);
  const setTransform = useWorkflowStore((s) => s.setTransform);
  const activeRun = useExecutionStore((s) => s.activeRunId ? s.runs[s.activeRunId] : undefined);
  // transform removed useWorkflowStore((s) => s.transform);

  const rfRef = useRef<any>(null);
  const draggingNodeIdsRef = useRef(new Set<string>());

  // Sync store -> React Flow
  const [rfNodes, setRfNodes]: any = useNodesState(
    (nodes.map((n) => ({
      ...n,
      width: NODE_WIDTH,
      type: getNodeTypeName(n as any),
      data: { ...n, executionState: activeRun?.nodeStates[n.id] ?? n.executionState },
      position: { x: n.x, y: n.y },
    })) as any)
  );

  const [rfEdges, setRfEdges]: any = useEdgesState([]);

  // Keep the rendered React Flow graph in sync when nodes/edges are added from
  // the palette, imported, or changed by another workflow panel.
  useEffect(() => {
    if (draggingNodeIdsRef.current.size > 0) return;
    setRfNodes(nodes.map((n) => ({
      ...n,
      width: NODE_WIDTH,
      type: getNodeTypeName(n as any),
      data: { ...n, executionState: activeRun?.nodeStates[n.id] ?? n.executionState },
      position: { x: n.x, y: n.y },
    })) as any);
  }, [nodes, activeRun?.nodeStates, setRfNodes]);

  useEffect(() => {
    setRfEdges(edges.map((edge) => {
      const source = activeRun?.nodeStates[edge.source];
      const target = activeRun?.nodeStates[edge.target];
      const runtimeState = target === 'skipped' ? 'skipped' : source === 'failed' || target === 'failed' ? 'failed' : target === 'running' ? 'active' : source === 'completed' && target === 'completed' ? 'completed' : 'idle';
      return { ...edge, sourceHandle: edge.sourcePort, targetHandle: edge.targetPort, type: 'data', data: { edgeType: edge.edgeType, runtimeState } };
    }) as any);
  }, [edges, activeRun?.nodeStates, setRfEdges]);

  // Push RF changes back to store
  const handleNodesChange: OnNodesChange = useCallback(
    (changes: NodeChange[]) => {
      setRfNodes((nds: any[]) => applyNodeChanges(changes, nds));
      // Sync position changes back to store
      for (const change of changes) {
        if (change.type === 'position' && change.position) {
          setNodePosition(change.id, change.position.x, change.position.y);
          if (change.dragging) {
            draggingNodeIdsRef.current.add(change.id);
          } else {
            draggingNodeIdsRef.current.delete(change.id);
            pushHistory();
          }
        } else if (change.type === 'remove') {
          removeNode(change.id);
        }
      }
    },
    [setRfNodes, removeNode, setNodePosition, pushHistory]
  );

  const handleEdgesChange: OnEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      setRfEdges((eds: any[]) => applyEdgeChanges(changes, eds));
      for (const change of changes) {
        if (change.type === 'remove') removeEdge(change.id);
      }
    },
    [setRfEdges, removeEdge]
  );

  const handleConnect: OnConnect = useCallback(
    (connection: Connection) => {
      const edge: WorkflowGraphEdge = {
        id: `edge_${connection.source}_${connection.target}_${Date.now()}`, 
        source: connection.source,
        target: connection.target,
        sourcePort: connection.sourceHandle ?? undefined,
        targetPort: connection.targetHandle ?? undefined,
        edgeType: 'data',
      };
      setEdges([...edges, edge]);
      const rfEdge = {
        ...connection,
        id: edge.id,
        type: 'workflow',
        style: { stroke: '#4FC3F7' },
        data: { edgeType: 'data' },
      };
      setRfEdges((eds: any[]) => addEdge(rfEdge, eds));
    },
    [edges, setEdges, setRfEdges]
  );

  const handleNodeClick = useCallback(
    (_e: React.MouseEvent, node: any) => {
      selectNode(node.id);
    },
    [selectNode]
  );

  const handleEdgeClick = useCallback(
    (_e: React.MouseEvent, edge: any) => {
      selectEdge(edge.id);
    },
    [selectEdge]
  );

  const handlePaneClick = useCallback(() => {
    deselectAll();
  }, [deselectAll]);

  const handleSelection = useCallback(
    (params: OnSelectionChangeParams) => {
      setSelection(
        (params.nodes ?? []).map((node) => node.id),
        (params.edges ?? []).map((edge) => edge.id),
      );
    },
    [setSelection]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  const screenToFlowPosition = useCallback((clientX: number, clientY: number) => {
    if (rfRef.current?.screenToFlowPosition) {
      return rfRef.current.screenToFlowPosition({ x: clientX, y: clientY });
    }
    const bounds = document.querySelector('.react-flow')?.getBoundingClientRect();
    return {
      x: clientX - (bounds?.left ?? 0),
      y: clientY - (bounds?.top ?? 0),
    };
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const data = e.dataTransfer.getData('application/x-atlas-node');
      if (!data) return;
      try {
        const template: DraggableNodeTemplate = JSON.parse(data);
        const position = screenToFlowPosition(e.clientX, e.clientY);
        const node = _createNodeFromTemplate(template, position.x, position.y);
        setNodes([...nodes, node]);
      } catch {
        // Invalid drag data
      }
    },
    [nodes, screenToFlowPosition, setNodes]
  );

  const handlePointerMove = useCallback((e: React.PointerEvent) => {
    updatePalettePointerDrag(e.clientX, e.clientY);
  }, []);

  const handlePointerUp = useCallback((e: React.PointerEvent) => {
    const template = takePalettePointerDrop();
    if (!template) return;
    const position = screenToFlowPosition(e.clientX, e.clientY);
    const node = _createNodeFromTemplate(template, position.x, position.y);
    setNodes([...useWorkflowStore.getState().nodes, node]);
  }, [screenToFlowPosition, setNodes]);

  const handlePointerCancel = useCallback(() => {
    cancelPalettePointerDrag();
  }, []);

  const nodeTypes = useMemo(() => NODE_TYPES, []);
  const edgeTypes = useMemo(() => EDGE_TYPES, []);

  // Handle keyboard pan/zoom
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const rfInstance = rfRef.current;
      if (!rfInstance) return;
      if (e.key === '=' || e.key === '+') {
        rfInstance.zoomIn(0.1);
      } else if (e.key === '-') {
        rfInstance.zoomOut(0.1);
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const reactFlowProps: any = {
    ref: rfRef,
    nodes: rfNodes,
    edges: rfEdges,
    onNodesChange: handleNodesChange,
    onEdgesChange: handleEdgesChange,
    onConnect: handleConnect,
    onNodeClick: handleNodeClick,
    onEdgeClick: handleEdgeClick,
    onPaneClick: handlePaneClick,
    onSelectionChange: handleSelection,
    onDragOver: handleDragOver,
    onDrop: handleDrop,
    onPointerMove: handlePointerMove,
    onPointerUp: handlePointerUp,
    onPointerCancel: handlePointerCancel,
    onMove: (_e: any, viewPort: any) => {
      setTransform({ x: viewPort.x, y: viewPort.y, zoom: viewPort.zoom });
    },
    nodeTypes: nodeTypes,
    edgeTypes: edgeTypes,
    fitView: true,
    minZoom: 0.1,
    maxZoom: 5,
    defaultViewport: { x: 0, y: 0, zoom: 1 },
    connectionRadius: 20,
    snapToGrid: true,
    snapGrid: [16, 16],
    deleteKeyCode: ['Delete', 'Backspace'],
    multiSelectionKeyCode: ['Control', 'Meta'],
    panOnDrag: true,
    zoomOnScroll: true,
    zoomOnPinch: true,
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <ReactFlow {...reactFlowProps}
        ref={rfRef}
        nodes={rfNodes}
        edges={rfEdges}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={handleConnect}
        onNodeClick={handleNodeClick}
        onEdgeClick={handleEdgeClick}
        onPaneClick={handlePaneClick}
        onSelectionChange={handleSelection}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerCancel={handlePointerCancel}
        onMove={( _e, viewPort) => {
          setTransform({ x: viewPort.x, y: viewPort.y, zoom: viewPort.zoom });
        }}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        minZoom={0.1}
        maxZoom={5}
        defaultViewport={{ x: 0, y: 0, zoom: 1 }}
        connectionRadius={20}
        snapToGrid
        snapGrid={[16, 16]}
        deleteKeyCode={['Delete', 'Backspace']}
        multiSelectionKeyCode={['Control', 'Meta']}
        panOnDrag
        zoomOnScroll
        zoomOnPinch
        
      >
        <Controls
          showInteractive={false}
          style={{
            backgroundColor: '#2d2d2d',
            border: '1px solid #444',
            borderRadius: 4,
          }}
        />
        <MiniMap
          nodeStrokeColor={(n: any) => {
            if (n.style?.hidden) return '#004199';
            return '#0078d4';
          }}
          nodeColor={() => '#252526'}
          maskColor="rgba(0, 0, 0, 0.5)"
          pannable
          zoomable
          style={{
            backgroundColor: '#1e1e1e',
            border: '1px solid #444',
            borderRadius: 4,
          }}
        />
        <Background color="#333" gap={16} />
      </ReactFlow>
    </div>
  );
};
