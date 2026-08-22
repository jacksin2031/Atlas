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

export const AppLayout: React.FC = () => {
  const [paletteVisible, setPaletteVisible] = React.useState(false);
  const activeWorkspace = useWorkspaceStore((s) => s.activeWorkspace);

  React.useEffect(() => { registerVisionCommands(); if (visionDemoModeEnabled) { const demo=createVisionDemoData(); useVisionResultsStore.getState().setOcr(demo.ocr); useVisionResultsStore.getState().setDetections(demo.detections); demo.colors.forEach((color)=>useVisionResultsStore.getState().addColor(color)); useVisionResultsStore.getState().setTemplates(demo.templates); useVisionTimelineStore.getState().setFrames(demo.frames); } }, []);
  React.useEffect(() => activeWorkspace === 'vision' ? installVisionShortcuts() : undefined, [activeWorkspace]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <MenuBar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />
      <Toolbar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />
      {activeWorkspace === 'vision' && <VisionToolbar onCommandPalette={() => setPaletteVisible(true)} />}
      <WorkspaceManager />

      {/* Status bar */}
      <StatusBar />

      {/* Command palette */}
      <CommandPalette visible={paletteVisible} onClose={() => setPaletteVisible(false)} />
    </div>
  );
};
