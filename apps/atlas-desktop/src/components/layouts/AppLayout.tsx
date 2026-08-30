// Atlas Desktop — App Layout
// New layout: Menu | Toolbar | [Sidebar | Canvas | Inspector] | [Bottom Tabbed Panel] | StatusBar

import React from 'react';
import { MenuBar } from './MenuBar';
import { Toolbar } from './Toolbar';
import { StatusBar } from './StatusBar';
import { CommandPalette } from "../CommandPalette";
import { WorkspaceManager, useWorkspaceStore } from '../../workspace';
import { VisionToolbar } from '../../studio/vision';
import { installVisionShortcuts, registerVisionCommands } from '../../studio/vision/commands';
import { createVisionDemoData, visionDemoModeEnabled } from '../../studio/vision/services/demo-provider';
import { useVisionResultsStore, useVisionTimelineStore } from '../../studio/vision/stores';
import { AIToolbar, aiDemoModeEnabled, aiStudioService, createAIDemoAdapter, installAIShortcuts, registerAICommands } from '../../studio/ai';
import { executorService, installWorkflowShortcuts, registerWorkflowCommands } from '../../studio/workflow';

export const AppLayout: React.FC = () => {
  const [paletteVisible, setPaletteVisible] = React.useState(false);
  const activeWorkspace = useWorkspaceStore((s) => s.activeWorkspace);
  const aiDiscoveryStarted = React.useRef(false);

  React.useEffect(() => { registerVisionCommands(); registerAICommands(); registerWorkflowCommands(); if(aiDemoModeEnabled)aiStudioService.setAdapter(createAIDemoAdapter()); if (visionDemoModeEnabled) { const demo=createVisionDemoData(); useVisionResultsStore.getState().setOcr(demo.ocr); useVisionResultsStore.getState().setDetections(demo.detections); demo.colors.forEach((color)=>useVisionResultsStore.getState().addColor(color)); useVisionResultsStore.getState().setTemplates(demo.templates); useVisionTimelineStore.getState().setFrames(demo.frames); } }, []);
  React.useEffect(() => { let dispose:(()=>void)|undefined;void aiStudioService.connectRuntimeEvents().then((unlisten)=>{dispose=unlisten;});return()=>dispose?.(); }, []);
  React.useEffect(() => { let dispose:(()=>void)|undefined;void executorService.connectRuntimeEvents().then((unlisten)=>{dispose=unlisten;});return()=>dispose?.(); }, []);
  React.useEffect(() => activeWorkspace === 'vision' ? installVisionShortcuts() : undefined, [activeWorkspace]);
  React.useEffect(() => activeWorkspace === 'ai' ? installAIShortcuts() : undefined, [activeWorkspace]);
  React.useEffect(() => activeWorkspace === 'workflow' ? installWorkflowShortcuts() : undefined, [activeWorkspace]);
  React.useEffect(() => { if(activeWorkspace==='ai'&&!aiDiscoveryStarted.current){aiDiscoveryStarted.current=true;void aiStudioService.refresh();} }, [activeWorkspace]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <MenuBar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />
      <Toolbar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />
      {activeWorkspace === 'vision' && <VisionToolbar onCommandPalette={() => setPaletteVisible(true)} />}
      {activeWorkspace === 'ai' && <AIToolbar />}
      <WorkspaceManager />

      {/* Status bar */}
      <StatusBar />

      {/* Command palette */}
      <CommandPalette visible={paletteVisible} onClose={() => setPaletteVisible(false)} />
    </div>
  );
};
