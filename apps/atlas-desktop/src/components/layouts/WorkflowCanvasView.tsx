// Atlas Desktop — Workflow Canvas View
// Main React Flow canvas with toolbar

import React from 'react';
import { WorkflowCanvas } from '../../studio/workflow/components/canvas/workflow-canvas';
import { WorkflowToolbar } from '../../studio/workflow/components/toolbar/workflow-toolbar';

export const WorkflowCanvasView: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden', backgroundColor: '#1e1e1e' }}>
      <WorkflowToolbar />
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <WorkflowCanvas />
      </div>
    </div>
  );
};
