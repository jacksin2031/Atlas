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
} from "../../stores";
import { NODE_TYPES, getNodeTypeName } from "../nodes/index";
import type { WorkflowGraphEdge } from "../../stores/workflow-store";
import type { DraggableNodeTemplate } from "../../hooks/use-canvas-drag-drop";
import { createNodeFromTemplate as _createNodeFromTemplate } from "../../hooks/use-canvas-drag-drop";

const NODE_WIDTH = 220;

export const WorkflowCanvas: React.FC = () => {
  const nodes = useWorkflowStore((s) => s.nodes);
  const edges = useWorkflowStore((s) => s.edges);
  const setNodes = useWorkflowStore((s) => s.setNodes);
  const setEdges = useWorkflowStore((s) => s.setEdges);
  const selectNode = useWorkflowStore((s) => s.selectNode);
  const selectEdge = useWorkflowStore((s) => s.selectEdge);
  const deselectAll = useWorkflowStore((s) => s.deselectAll);
  const setTransform = useWorkflowStore((s) => s.setTransform);
  // transform removed useWorkflowStore((s) => s.transform);

  const rfRef = useRef<any>(null);

  // Sync store -> React Flow
  const [rfNodes, setRfNodes, onNodesChange]: any = useNodesState(
    (nodes.map((n) => ({
      ...n,
      width: NODE_WIDTH,
      type: getNodeTypeName(n as any),
      data: n,
    })) as any)
  );

  const [rfEdges, setRfEdges, onEdgesChange]: any = useEdgesState(edges);

  // Push RF changes back to store
  const handleNodesChange: OnNodesChange = useCallback(
    (changes: NodeChange[]) => {
      setRfNodes((nds: any[]) => applyNodeChanges(changes, nds));
      // Sync position changes back to store
      for (const change of changes) {
        if (change.type === 'position' && change.position) {
          useWorkflowStore.getState().updateNode(change.id, {
            x: change.position.x,
            y: change.position.y,
          });
        }
      }
    },
    [setRfNodes]
  );

  const handleEdgesChange: OnEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      setRfEdges((eds: any[]) => applyEdgeChanges(changes, eds));
    },
    [setRfEdges]
  );

  const handleConnect: OnConnect = useCallback(
    (connection: Connection) => {
      const edge: WorkflowGraphEdge = {
        id: `edge_${connection.source}_${connection.target}_${Date.now()}`, 
        source: connection.source,
        target: connection.target,
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
      // Sync selection from RF to store
      if (params.nodes) {
        for (const n of params.nodes) {
          selectNode(n.id, true);
        }
      }
      if (params.edges) {
        for (const e of params.edges) {
          selectEdge(e.id, true);
        }
      }
    },
    [selectNode, selectEdge]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const data = e.dataTransfer.getData('application/x-atlas-node');
      if (!data) return;
      try {
        const template: DraggableNodeTemplate = JSON.parse(data);
        const reactFlowBounds = (e.currentTarget as HTMLElement).getBoundingClientRect();
        const x = e.clientX - reactFlowBounds.left;
        const y = e.clientY - reactFlowBounds.top;
        const node = _createNodeFromTemplate(template, x, y);
        setNodes([...nodes, node]);
      } catch {
        // Invalid drag data
      }
    },
    [nodes, setNodes]
  );

  const nodeTypes = useMemo(() => NODE_TYPES, []);
  const edgeTypes = useMemo(() => ({}), []);

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
    onSelection: handleSelection,
    onDragOver: handleDragOver,
    onDrop: handleDrop,
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
        onSelection={handleSelection}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
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
