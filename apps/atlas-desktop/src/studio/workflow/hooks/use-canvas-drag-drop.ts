// Atlas Workflow Studio - Canvas Drag Hook
// Handles drag-and-drop of nodes from palette to canvas

import { useRef, useCallback } from 'react';
import { useWorkflowStore } from '../stores';
import type { NodeCategory } from '../types/node-categories';

export interface DraggableNodeTemplate {
  typeName: string;
  label: string;
  category: NodeCategory;
  inputs: Array<{ name: string; type: string }>;
  outputs: Array<{ name: string; type: string }>;
}

export function useCanvasDragDrop(onNodeDrop: (template: DraggableNodeTemplate, x: number, y: number) => void) {
  const dragCounterRef = useRef(0);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current++;
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current--;
    if (dragCounterRef.current === 0) {
      // Last leave event — reset
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      dragCounterRef.current = 0;

      const data = e.dataTransfer.getData('application/x-atlas-node');
      if (!data) return;

      try {
        const template: DraggableNodeTemplate = JSON.parse(data);
        const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
        const x = (e.clientX - rect.left) / 1 - 50;
        const y = (e.clientY - rect.top) / 1 - 30;
        onNodeDrop(template, x, y);
      } catch {
        // Invalid drag data — ignore
      }
    },
    [onNodeDrop]
  );

  return { handleDragOver, handleDragLeave, handleDrop };
}

// Helper to create a node from a template
export function createNodeFromTemplate(
  template: DraggableNodeTemplate,
  x: number,
  y: number
): ReturnType<typeof useWorkflowStore.getState>['nodes'][0] {
  return {
    id: `template_${Date.now()}`, 

    type: template.typeName,
    label: template.label,
    category: template.category,
    inputs: template.inputs.map((inp) => ({
      id: `in_${Date.now()}`, 
      name: inp.name,
      type: inp.type,
      multiple: false,
      dynamic: false,
    })),
    outputs: template.outputs.map((out) => ({
      id: `out_${Date.now()}`, 
      name: out.name,
      type: out.type,
      multiple: false,
      dynamic: false,
    })),
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
