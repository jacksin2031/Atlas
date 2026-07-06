// Atlas Workflow Studio - Main Panel
// Integrated workflow editor with canvas, palette, inspector, and debugger

import React, { useCallback } from 'react';
import { useLayoutStore } from '../../stores';
import { useWorkflowStore } from './stores';
import { WorkflowCanvas } from './components/canvas';
import { NodePalette } from './components/sidebar/node-palette';
import { PropertyInspector } from './components/inspector/property-inspector';
import { VariableManager } from './components/variables/variable-manager';
import { WorkflowToolbar } from './components/toolbar/workflow-toolbar';
import { DebuggerPanel } from './components/toolbar/debugger-panel';
import { ValidationReportPanel } from './components/properties/validation-report';
import { useKeyboardShortcuts } from './hooks/use-keyboard-shortcuts';

export const WorkflowStudioPanel: React.FC = () => {
  const [showInspector, setShowInspector] = React.useState(true);
  const [showVariables, setShowVariables] = React.useState(false);
  const [showDebugger, setShowDebugger] = React.useState(false);
  const [showValidation, setShowValidation] = React.useState(false);
  const [showPalette, setShowPalette] = React.useState(true);

  // Register keyboard shortcuts
  useKeyboardShortcuts();



  const handleNewWorkflow = useCallback(() => {
    const name = prompt('Workflow name:');
    if (!name) return;
    useWorkflowStore.getState().resetCanvas();
    useWorkflowStore.getState().setWorkflowInfo(
      `wf_${Date.now()}`,
      name,
      '1.0.0'
    );
  }, []);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        width: '100%',
        backgroundColor: '#1e1e1e',
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        overflow: 'hidden',
      }}
    >
      {/* Toolbar */}
      <WorkflowToolbar />

      {/* Secondary toolbar — panel toggles */}
      <div
        style={{
          height: 28,
          backgroundColor: '#252526',
          borderBottom: '1px solid #333',
          display: 'flex',
          alignItems: 'center',
          padding: '0 8px',
          gap: 2,
        }}
      >
        <button
          onClick={() => setShowPalette(!showPalette)}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: showPalette ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          Palette
        </button>
        <button
          onClick={() => setShowInspector(!showInspector)}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: showInspector ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          Inspector
        </button>
        <button
          onClick={() => setShowVariables(!showVariables)}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: showVariables ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          Variables
        </button>
        <button
          onClick={() => setShowDebugger(!showDebugger)}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: showDebugger ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          Debugger
        </button>
        <button
          onClick={() => setShowValidation(!showValidation)}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: showValidation ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          Validation
        </button>
        <div style={{ flex: 1 }} />
        <button
          onClick={handleNewWorkflow}
          style={{
            fontSize: 10,
            padding: '1px 8px',
            border: '1px solid #444',
            borderRadius: 2,
            backgroundColor: '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          New Workflow
        </button>
      </div>

      {/* Main content area */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Node Palette */}
        {showPalette && <NodePalette />}

        {/* Canvas */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
            <WorkflowCanvas />
          </div>
        </div>

        {/* Right side panels */}
        <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          {showInspector && <PropertyInspector />}
          {showDebugger && <DebuggerPanel />}
          {showValidation && <ValidationReportPanel />}
          {showVariables && <VariableManager />}
        </div>
      </div>
    </div>
  );
};
