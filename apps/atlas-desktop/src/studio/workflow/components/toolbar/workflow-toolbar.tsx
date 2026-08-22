// Atlas Workflow Studio - Toolbar with Execution Controls
// RFC-0303 execution controls

import React from 'react';
import { useExecutionStore } from '../../stores';
import { useWorkflowStore } from '../../stores';
import { importExportService } from '../../services/import-export-service';
import type { SerializationFormat } from '../../types';
import { Button, IconButton } from '../../../../design-system';

export const WorkflowToolbar: React.FC = () => {
  const status = useExecutionStore((s: any) => s.status);
  const isRunning = useExecutionStore((s: any) => s.isRunning);
  const isPaused = useExecutionStore((s: any) => s.isPaused);
  const isSimulating = useExecutionStore((s: any) => s.isSimulating);
  const isDryRunning = useExecutionStore((s: any) => s.isDryRunning);
  const activeRunId = useExecutionStore((s: any) => s.activeRunId);
  const workflowId = useWorkflowStore((s: any) => s.workflowId);
  const workflowName = useWorkflowStore((s: any) => s.workflowName);

  const startExecution = useExecutionStore((s: any) => s.startExecution);
  const pauseExecution = useExecutionStore((s: any) => s.pauseExecution);
  const resumeExecution = useExecutionStore((s: any) => s.resumeExecution);
  const stopExecution = useExecutionStore((s: any) => s.stopExecution);
  const stepExecution = useExecutionStore((s: any) => s.stepExecution);
  const startSimulation = useExecutionStore((s: any) => s.startSimulation);
  const stopSimulation = useExecutionStore((s: any) => s.stopSimulation);
  const startDryRun = useExecutionStore((s: any) => s.startDryRun);
  const stopDryRun = useExecutionStore((s: any) => s.stopDryRun);

  const undo = useWorkflowStore((s: any) => s.undo);
  const redo = useWorkflowStore((s: any) => s.redo);

  const handleExport = async (format: SerializationFormat) => {
    const def = useWorkflowStore.getState().exportToDefinition();
    const data = await importExportService.serialize(def, format);
    const blob = new Blob([data], { type: format === 'json' ? 'application/json' : 'text/yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
      a.download = `workflow_${(workflowName || "untitled")}_${Date.now()}.${format === "json" ? "json" : "yaml"}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = async () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json,.yaml,.yml';
    input.onchange = async () => {
      const file = input.files?.[0];
      if (!file) return;
      const text = await file.text();
      const ext = file.name.split('.').pop()?.toLowerCase();
      const format = ext === 'yaml' || ext === 'yml' ? 'yaml' : 'json';
      const result = await importExportService.deserialize(text, format as SerializationFormat);
      if (result.success && result.workflow) {
        useWorkflowStore.getState().loadFromDefinition(result.workflow);
      }
    };
    input.click();
  };

  const btnStyle: React.CSSProperties = {
    padding: '4px 10px',
    fontSize: 12,
    border: '1px solid #444',
    borderRadius: 3,
    backgroundColor: '#2d2d2d',
    color: '#ccc',
    cursor: 'pointer',
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    display: 'flex',
    alignItems: 'center',
    gap: 4,
  };

  const activeBtnStyle = (active: boolean): React.CSSProperties => ({
    ...btnStyle,
    backgroundColor: active ? '#0078d4' : '#2d2d2d',
    borderColor: active ? '#0078d4' : '#444',
  });

  return (
    <div
      style={{
        height: 36,
        backgroundColor: '#2d2d2d',
        borderBottom: '1px solid #333',
        display: 'flex',
        alignItems: 'center',
        padding: '0 8px',
        gap: 4,
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        overflow: 'auto',
      }}
    >
      {/* Workflow name */}
      <span style={{ fontSize: 12, color: '#aaa', fontWeight: 600, marginRight: 8, whiteSpace: 'nowrap' }}>
        {workflowName || 'Untitled Workflow'}
      </span>

      <div style={{ width: 1, height: 20, backgroundColor: '#444', margin: '0 4px' }} />

      {/* Undo/Redo */}
      <IconButton icon="undo" onClick={undo} label="Undo (Ctrl+Z)" />
      <IconButton icon="redo" onClick={redo} label="Redo (Ctrl+Y)" />

      <div style={{ width: 1, height: 20, backgroundColor: '#444', margin: '0 4px' }} />

      {/* Import/Export */}
      <Button icon="open" onClick={handleImport} title="Import workflow">Import</Button>
      <Button icon="save" onClick={() => handleExport('json')} title="Export as JSON">JSON</Button>
      <Button icon="export" onClick={() => handleExport('yaml')} title="Export as YAML">YAML</Button>

      <div style={{ width: 1, height: 20, backgroundColor: '#444', margin: '0 4px' }} />

      {/* Execution controls */}
      <button
        style={activeBtnStyle(isRunning && !isPaused)}
        onClick={isPaused ? resumeExecution : isRunning ? pauseExecution : startExecution}
        title={isPaused ? 'Resume (F8)' : isRunning ? 'Pause (F8)' : 'Run (F5)'}
        disabled={!workflowId}
      >
        {isPaused ? 'Resume' : isRunning ? 'Pause' : 'Run'}
      </button>
      <Button icon="next" onClick={stepExecution} title="Step (F7)">Step</Button>
      <button
        style={activeBtnStyle(isSimulating)}
        onClick={isSimulating ? stopSimulation : startSimulation}
      >
        Simulate
      </button>
      <button
        style={activeBtnStyle(isDryRunning)}
        onClick={isDryRunning ? stopDryRun : startDryRun}
      >
        Dry Run
      </button>
      <Button icon="stop" onClick={stopExecution} title="Stop">Stop</Button>

      <div style={{ flex: 1 }} />

      {/* Status indicator */}
      <span
        style={{
          fontSize: 11,
          color: isRunning ? '#4CAF50' : isPaused ? '#FF9800' : '#888',
          whiteSpace: 'nowrap',
        }}
      >
        {status === 'running' ? 'Running' : status === 'paused' ? 'Paused' : status === 'completed' ? 'Done' : status === 'failed' ? 'Failed' : status === 'cancelled' ? 'Stopped' : status}
      </span>
      {activeRunId && (
        <span style={{ fontSize: 10, color: '#666', fontFamily: 'monospace' }}>
          {activeRunId.slice(0, 12)}
        </span>
      )}
    </div>
  );
};
