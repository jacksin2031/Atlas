// Atlas Workflow Studio - Keyboard Shortcuts Hook
// Supports: undo, redo, copy, paste, delete, duplicate, select-all, run, step

import { useEffect, useCallback } from 'react';
import { useWorkflowStore } from '../stores';
import { useExecutionStore } from '../stores';

const SHORTCUTS: Record<string, () => void> = {
  'Control+z': () => useWorkflowStore.getState().undo(),
  'Control+y': () => useWorkflowStore.getState().redo(),
  'Control+d': () => {
    const selected = useWorkflowStore.getState().selectedNodeIds;
    if (selected.length > 0 && selected[0]) {
      useWorkflowStore.getState().duplicateNode(selected[0]);
    }
  },
  'Delete': () => {
    const { selectedNodeIds, selectedEdges } = useWorkflowStore.getState();
    for (const id of selectedNodeIds) useWorkflowStore.getState().removeNode(id);
    for (const id of selectedEdges) useWorkflowStore.getState().removeEdge(id);
  },
  'Escape': () => useWorkflowStore.getState().deselectAll(),
  'Control+a': () => useWorkflowStore.getState().selectAll(),
};

export function useKeyboardShortcuts() {
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      const key = (event.ctrlKey || event.metaKey ? "Control+" : "") + event.key;
      const handler = key ? SHORTCUTS[key as keyof typeof SHORTCUTS] : undefined;
      if (handler) {
        event.preventDefault();
        handler();
      }
    },
    []
  );

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
}

// Run/Debug shortcuts
export function useExecutionShortcuts() {
  const start = useCallback(() => useExecutionStore.getState().startExecution(), []);
  const pause = useCallback(() => useExecutionStore.getState().pauseExecution(), []);
  const stop = useCallback(() => useExecutionStore.getState().stopExecution(), []);
  const step = useCallback(() => useExecutionStore.getState().stepExecution(), []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'F5' && !event.ctrlKey) {
        event.preventDefault();
        start();
      } else if (event.key === 'F7') {
        event.preventDefault();
        step();
      } else if (event.key === 'F8') {
        event.preventDefault();
        pause();
      } else if (event.shiftKey && event.key === 'F5') {
        event.preventDefault();
        stop();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [start, pause, stop, step]);
}
