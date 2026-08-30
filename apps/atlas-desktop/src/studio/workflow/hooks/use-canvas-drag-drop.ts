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
  parameters?: Record<string, unknown>;
  capabilities?: string[];
  pluginId?: string;
}

// Tauri's embedded WebView does not consistently deliver HTML5 drag events
// from the palette to React Flow. Keep a small pointer-drag channel shared by
// the palette and canvas so dropping still works in that host.
let activePalettePointerDrag: {
  template: DraggableNodeTemplate;
  startX: number;
  startY: number;
  moved: boolean;
} | null = null;
let suppressNextPaletteClick = false;

export function beginPalettePointerDrag(template: DraggableNodeTemplate, x: number, y: number): void {
  activePalettePointerDrag = { template, startX: x, startY: y, moved: false };
}

export function updatePalettePointerDrag(x: number, y: number): void {
  if (!activePalettePointerDrag) return;
  const dx = x - activePalettePointerDrag.startX;
  const dy = y - activePalettePointerDrag.startY;
  if (dx * dx + dy * dy >= 36) activePalettePointerDrag.moved = true;
}

export function takePalettePointerDrop(): DraggableNodeTemplate | null {
  const drag = activePalettePointerDrag;
  activePalettePointerDrag = null;
  if (!drag?.moved) return null;
  suppressNextPaletteClick = true;
  return drag.template;
}

export function cancelPalettePointerDrag(): void {
  activePalettePointerDrag = null;
}

export function consumeSuppressedPaletteClick(): boolean {
  const suppressed = suppressNextPaletteClick;
  suppressNextPaletteClick = false;
  return suppressed;
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
    inputs: template.inputs.map((inp, index) => ({
      id: `in_${Date.now()}_${index}`,
      name: inp.name,
      type: inp.type,
      multiple: false,
      dynamic: false,
    })),
    outputs: template.outputs.map((out, index) => ({
      id: `out_${Date.now()}_${index}`,
      name: out.name,
      type: out.type,
      multiple: false,
      dynamic: false,
    })),
    parameters: { ...(template.parameters ?? {}) },
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
    capabilities: [...(template.capabilities ?? [])],
    pluginId: template.pluginId,
    requiredPlugins: template.pluginId && template.pluginId !== 'builtin' ? [template.pluginId] : [],
    version: '1.0.0',
  };
}
