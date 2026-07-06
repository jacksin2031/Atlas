// Atlas Desktop — App Layout
// New layout: Menu | Toolbar | [Sidebar | Canvas | Inspector] | [Bottom Tabbed Panel] | StatusBar

import React from 'react';
import { MenuBar } from './MenuBar';
import { Toolbar } from './Toolbar';
import { StatusBar } from './StatusBar';
import { SidebarPanel } from './SidebarPanel';
import { InspectorPanel } from './InspectorPanel';
import { WorkflowCanvasView } from './WorkflowCanvasView';
import { BottomPanel } from './BottomPanel';
import { CommandPalette } from "../CommandPalette";

interface AppLayoutProps { }

export const AppLayout: React.FC<AppLayoutProps> = () => {
  const [paletteVisible, setPaletteVisible] = React.useState(false);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <MenuBar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />
      <Toolbar onToggleCommandPalette={() => setPaletteVisible(!paletteVisible)} />

      {/* Main content area */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left sidebar */}
        <SidebarPanel />

        {/* Center: Workflow Canvas */}
        <WorkflowCanvasView />

        {/* Right: Inspector */}
        <InspectorPanel />
      </div>

      {/* Bottom tabbed panel */}
      <BottomPanel />

      {/* Status bar */}
      <StatusBar />

      {/* Command palette */}
      <CommandPalette visible={paletteVisible} onClose={() => setPaletteVisible(false)} />
    </div>
  );
};
