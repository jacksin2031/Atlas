// Atlas Desktop — Node Palette Sidebar
// Tabbed sidebar: Explorer | Workflow Nodes | AI Nodes | Vision Nodes | Plugins

import React, { useState } from 'react';
import { useThemeStore } from '../../stores';
import { ProjectExplorerPanel } from '../panels/ProjectExplorerPanel';
import { NodePalette } from '../../studio/workflow/components/sidebar/node-palette';
import { useNodeRegistryStore } from '../../studio/workflow/stores';

type SidebarTab = 'explorer' | 'workflow' | 'ai' | 'vision' | 'plugins';

const TABS: { id: SidebarTab; label: string; icon: string }[] = [
  { id: 'explorer', label: 'Explorer', icon: '\\uD83D\\uDCC1' },
  { id: 'workflow', label: 'Workflow Nodes', icon: '\\u2699' },
  { id: 'ai', label: 'AI Nodes', icon: '\\u2726' },
  { id: 'vision', label: 'Vision Nodes', icon: '\\u25CE' },
  { id: 'plugins', label: 'Plugins', icon: '\\u229E' },
];

export const SidebarPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const [activeTab, setActiveTab] = useState<SidebarTab>('explorer');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'explorer':
        return <ProjectExplorerPanel />;
      case 'workflow':
        return <NodePalette />;
      case 'ai': {
        const aiNodes = useNodeRegistryStore.getState().getNodesByCategory('ai');
        return (
          <div style={{ fontSize: 12, padding: 8 }}>
            <div style={{ fontWeight: 600, marginBottom: 8, color: '#aaa' }}>AI NODES</div>
            {aiNodes.length === 0 && <div style={{ color: '#666', fontSize: 11 }}>No AI nodes registered.</div>}
            {aiNodes.map((node) => (
              <div key={node.nodeId} style={{ padding: '4px 8px', fontSize: 11, color: '#ccc', borderBottom: '1px solid #2a2a2a' }}>
                {node.label}
              </div>
            ))}
          </div>
        );
      }
      case 'vision': {
        const visionNodes = useNodeRegistryStore.getState().getNodesByCategory('vision');
        return (
          <div style={{ fontSize: 12, padding: 8 }}>
            <div style={{ fontWeight: 600, marginBottom: 8, color: '#aaa' }}>VISION NODES</div>
            {visionNodes.length === 0 && <div style={{ color: '#666', fontSize: 11 }}>No vision nodes registered.</div>}
            {visionNodes.map((node) => (
              <div key={node.nodeId} style={{ padding: '4px 8px', fontSize: 11, color: '#ccc', borderBottom: '1px solid #2a2a2a' }}>
                {node.label}
              </div>
            ))}
          </div>
        );
      }
      case 'plugins': {
        const allNodes = useNodeRegistryStore.getState().discoverNodes();
        const pluginNodes = allNodes.filter((n) => n.pluginId !== 'builtin');
        return (
          <div style={{ fontSize: 12, padding: 8 }}>
            <div style={{ fontWeight: 600, marginBottom: 8, color: '#aaa' }}>PLUGINS</div>
            {pluginNodes.length === 0 && <div style={{ color: '#666', fontSize: 11 }}>No plugin nodes registered.</div>}
            {pluginNodes.map((node) => (
              <div key={node.nodeId} style={{ padding: '4px 8px', fontSize: 11, color: '#ccc', borderBottom: '1px solid #2a2a2a' }}>
                {node.label} ({node.pluginId})
              </div>
            ))}
          </div>
        );
      }
      default:
        return null;
    }
  };

  return (
    <div
      style={{
        width: 240,
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: resolvedTheme === 'dark' ? '#252526' : '#fff',
        borderRight: '1px solid ' + (resolvedTheme === 'dark' ? '#333' : '#ddd'),
        overflow: 'hidden',
      }}
    >
      {/* Tab bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          borderBottom: '1px solid ' + (resolvedTheme === 'dark' ? '#333' : '#ddd'),
          backgroundColor: resolvedTheme === 'dark' ? '#2d2d2d' : '#f5f5f5',
          overflow: 'hidden',
        }}
      >
        {TABS.map((tab) => (
          <div
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '0 6px',
              fontSize: 10,
              cursor: 'pointer',
              userSelect: 'none',
              height: 28,
              display: 'flex',
              alignItems: 'center',
              gap: 3,
              color: activeTab === tab.id
                ? (resolvedTheme === 'dark' ? '#fff' : '#000')
                : (resolvedTheme === 'dark' ? '#888' : '#666'),
              borderBottom: activeTab === tab.id
                ? '2px solid #0078d4'
                : '2px solid transparent',
              backgroundColor: activeTab === tab.id
                ? (resolvedTheme === 'dark' ? '#252526' : '#fff')
                : 'transparent',
              whiteSpace: 'nowrap',
              flex: 1,
              justifyContent: 'center',
            }}
          >
            <span style={{ fontSize: 11 }}>{tab.icon}</span>
            <span>{tab.label.split(' ')[0]}</span>
          </div>
        ))}
      </div>

      {/* Tab content */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        {renderTabContent()}
      </div>
    </div>
  );
};
