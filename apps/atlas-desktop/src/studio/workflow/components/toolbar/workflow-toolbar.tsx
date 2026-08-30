// Atlas Workflow Studio - Toolbar with Execution Controls
// RFC-0303 execution controls

import React from 'react';
import { useExecutionStore } from '../../stores';
import { useWorkflowStore } from '../../stores';
import { importExportService } from '../../services/import-export-service';
import { pluginDiscoveryService } from '../../services/plugin-discovery-service';
import { executorService } from '../../services/executor-service';
import type { SerializationFormat } from '../../types';
import { Button, IconButton } from '../../../../design-system';
import visualClosedLoop from '../../../../../../../sample-workflow-vision-closed-loop.json';
import templateClosedLoop from '../../../../../../../sample-workflow-template-closed-loop.json';
import ocrWorkflow from '../../../../../../../sample-workflow-ocr.json';
import recoveryWorkflow from '../../../../../../../sample-workflow-recovery.json';
import dynamicPluginWorkflow from '../../../../../../../sample-workflow-dynamic-plugin.json';
import type { WorkflowDefinition } from '../../types';

export const WorkflowToolbar: React.FC = () => {
  const [visualTargetActivated, setVisualTargetActivated] = React.useState(false);
  const [visualTargetLocation, setVisualTargetLocation] = React.useState<"left" | "right">("right");
  const [visualTargetVisible, setVisualTargetVisible] = React.useState(true);
  const [inputArmed, setInputArmed] = React.useState(false);
  const status = useExecutionStore((s: any) => s.status);
  const isRunning = useExecutionStore((s: any) => s.isRunning);
  const isPaused = useExecutionStore((s: any) => s.isPaused);
  const isSimulating = useExecutionStore((s: any) => s.isSimulating);
  const isDryRunning = useExecutionStore((s: any) => s.isDryRunning);
  const activeRunId = useExecutionStore((s: any) => s.activeRunId);
  const runtimeError = useExecutionStore((s: any) => s.runtimeError);
  const workflowId = useWorkflowStore((s: any) => s.workflowId);
  const workflowName = useWorkflowStore((s: any) => s.workflowName);

  const startSimulation = useExecutionStore((s: any) => s.startSimulation);
  const stopSimulation = useExecutionStore((s: any) => s.stopSimulation);
  const startDryRun = useExecutionStore((s: any) => s.startDryRun);
  const stopDryRun = useExecutionStore((s: any) => s.stopDryRun);

  const undo = useWorkflowStore((s: any) => s.undo);
  const redo = useWorkflowStore((s: any) => s.redo);

  const report = (error: unknown) => useExecutionStore.getState().setRuntimeError(error instanceof Error ? error.message : String(error));
  const handleRun = async () => {
    try {
      if (isPaused && activeRunId) await executorService.resume(activeRunId);
      else if (isRunning && activeRunId) await executorService.pause(activeRunId);
      else await executorService.run();
    } catch (error) { report(error); }
  };
  const handleStop = async () => { if (activeRunId) try { await executorService.stop(activeRunId); } catch (error) { report(error); } };
  const handleStep = async () => { if (activeRunId) try { await executorService.step(activeRunId); } catch (error) { report(error); } };
  const handleRestart = async () => { if (activeRunId) try { await executorService.restart(activeRunId); } catch (error) { report(error); } };
  const handleArmInput = async () => {
    if (!window.confirm('Arm Atlas to control the real mouse and keyboard? Dangerous shortcuts remain blocked.')) return;
    const target = window.prompt('Allowed foreground window title (required):', 'Atlas');
    if (!target?.trim()) { report('Input Runtime was not armed: an allowed foreground window title is required.'); return; }
    try { await executorService.armInput(target.trim()); setInputArmed(true); useExecutionStore.getState().setRuntimeError(null); }
    catch (error) { setInputArmed(false); report(error); }
  };
  const handleEmergencyStop = async () => {
    try { await executorService.emergencyStop(); setInputArmed(false); }
    catch (error) { report(error); }
  };
  const handleDryRun = async () => {
    if (isDryRunning) { stopDryRun(); return; }
    startDryRun();
    try {
      const errors = await executorService.dryRun(workflowId);
      useExecutionStore.getState().setRuntimeError(errors.length ? errors.map((error) => error.message).join('; ') : null);
    } catch (error) { report(error); }
    finally { stopDryRun(); }
  };

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
  const handleLoadVisualLoop = () => {
    setVisualTargetActivated(false);
    setVisualTargetVisible(true);
    useWorkflowStore.getState().loadFromDefinition(visualClosedLoop as unknown as WorkflowDefinition);
  };
  const loadAcceptanceWorkflow = (workflow: WorkflowDefinition): void => {
    setVisualTargetActivated(false);
    setVisualTargetVisible(true);
    useWorkflowStore.getState().loadFromDefinition(workflow);
  };
  const handleLoadDynamicPlugin = async (): Promise<void> => {
    try {
      await pluginDiscoveryService.registerManifest({
        id: 'atlas.acceptance.dynamic',
        version: '1.0.0',
        nodes: [{
          typeName: 'acceptance_dynamic_prefix',
          label: 'Dynamic Acceptance Prefix',
          description: 'Safe data-driven node registered through the Desktop Plugin bridge',
          operation: 'prefix',
          prefix: 'dynamic:',
        }],
      });
      loadAcceptanceWorkflow(dynamicPluginWorkflow as unknown as WorkflowDefinition);
      useExecutionStore.getState().setRuntimeError(null);
    } catch (error) { report(error); }
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
      <Button icon="vision" onClick={handleLoadVisualLoop} title="Load the Sprint 15.4 closed-loop sample">Load Visual Loop</Button>
      <Button icon="vision" onClick={() => loadAcceptanceWorkflow(templateClosedLoop as unknown as WorkflowDefinition)} title="Load the native Template Matching closed-loop sample">Load Template</Button>
      <Button icon="vision" onClick={() => loadAcceptanceWorkflow(ocrWorkflow as unknown as WorkflowDefinition)} title="Load the native Windows OCR sample">Load OCR</Button>
      <Button icon="retry" onClick={() => loadAcceptanceWorkflow(recoveryWorkflow as unknown as WorkflowDefinition)} title="Load the restart/interrupted recovery sample">Load Recovery</Button>
      <Button icon="tools" onClick={() => void handleLoadDynamicPlugin()} title="Register and load a runtime plugin node">Load Plugin</Button>
      <Button icon="save" onClick={() => handleExport('json')} title="Export as JSON">JSON</Button>
      <Button icon="export" onClick={() => handleExport('yaml')} title="Export as YAML">YAML</Button>

      <div style={{ width: 1, height: 20, backgroundColor: '#444', margin: '0 4px' }} />

      {/* Execution controls */}
      <button
        style={activeBtnStyle(isRunning && !isPaused)}
        onClick={() => void handleRun()}
        title={isPaused ? 'Resume (F8)' : isRunning ? 'Pause (F8)' : 'Run (F5)'}
        disabled={!workflowId}
      >
        {isPaused ? 'Resume' : isRunning ? 'Pause' : 'Run'}
      </button>
      <Button icon="next" onClick={() => void handleStep()} title="Step (F7)" disabled={!isPaused}>Step</Button>
      <button
        style={activeBtnStyle(isSimulating)}
        onClick={isSimulating ? stopSimulation : startSimulation}
      >
        Simulate
      </button>
      <button
        style={activeBtnStyle(isDryRunning)}
        onClick={() => void handleDryRun()}
      >
        Dry Run
      </button>
      <Button icon="stop" onClick={() => void handleStop()} title="Stop" disabled={!activeRunId || (!isRunning && !isPaused)}>Stop</Button>
      <Button icon="retry" onClick={() => void handleRestart()} title="Restart" disabled={!activeRunId}>Restart</Button>
      <Button onClick={() => void handleArmInput()} title="Grant bounded permission to the Input Runtime">{inputArmed ? 'Input Armed' : 'Arm Input'}</Button>
      <button style={{ ...btnStyle, backgroundColor: '#8b1e1e', borderColor: '#d34b4b', color: '#fff', fontWeight: 700 }} onClick={() => void handleEmergencyStop()} title="Immediately cancel workflows and release held input (global Pause/Break or in-app Escape)">EMERGENCY STOP</button>

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
      {runtimeError && <span title={runtimeError} style={{ maxWidth: 280, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', color: '#F44336', fontSize: 10 }}>{runtimeError}</span>}
      {visualTargetVisible && <button
        data-testid="visual-automation-target"
        aria-label="Visual automation target"
        onClick={() => { setVisualTargetActivated(true); setVisualTargetLocation((location) => location === "right" ? "left" : "right"); }}
        onContextMenu={(event) => { event.preventDefault(); setVisualTargetVisible(false); }}
        title="Left click activates and relocates; right click removes the acceptance target"
        style={{
          position: 'fixed',
          right: visualTargetLocation === "right" ? 18 : undefined,
          left: visualTargetLocation === "left" ? 280 : undefined,
          bottom: 34,
          zIndex: 10000,
          width: 120,
          height: 24,
          border: '1px solid #111',
          borderRadius: 3,
          background: visualTargetActivated ? '#a8ff00' : '#ff00c8',
          color: '#111',
          fontSize: 10,
          fontWeight: 700,
          cursor: 'pointer',
        }}
      >
        {visualTargetActivated ? 'TARGET CLICKED' : 'VISUAL TARGET'}
      </button>}
    </div>
  );
};
