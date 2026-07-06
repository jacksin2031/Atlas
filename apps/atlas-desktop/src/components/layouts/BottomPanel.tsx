// Atlas Desktop — Tabbed Bottom Panel
// Variables | Console | Problems | Debugger | Output

import React, { useState } from 'react';
import { useThemeStore } from '../../stores';
import { VariableManager } from '../../studio/workflow/components/variables/variable-manager';
import { ConsolePanel } from '../../components/panels';
import { ProblemsPanel } from '../../components/panels';
import { OutputPanel } from '../../components/panels';
import { DebuggerPanel } from '../../studio/workflow/components/toolbar/debugger-panel';

type BottomTab = 'variables' | 'console' | 'problems' | 'debugger' | 'output';

const TABS: { id: BottomTab; label: string }[] = [
  { id: 'variables', label: 'Variables' },
  { id: 'console', label: 'Console' },
  { id: 'problems', label: 'Problems' },
  { id: 'debugger', label: 'Debugger' },
  { id: 'output', label: 'Output' },
];

export const BottomPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const [activeTab, setActiveTab] = useState<BottomTab>('variables');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'variables':
        return <VariableManager />;
      case 'console':
        return <ConsolePanel />;
      case 'problems':
        return <ProblemsPanel />;
      case 'debugger':
        return <DebuggerPanel />;
      case 'output':
        return <OutputPanel />;
      default:
        return null;
    }
  };

  return (
    <div
      style={{
        height: 200,
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: resolvedTheme === 'dark' ? '#252526' : '#fff',
        borderTop: '1px solid ' + (resolvedTheme === 'dark' ? '#333' : '#ddd'),
        overflow: 'hidden',
      }}
    >
      {/* Tab bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          height: 28,
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
              padding: '0 12px',
              fontSize: 11,
              cursor: 'pointer',
              userSelect: 'none',
              height: 28,
              display: 'flex',
              alignItems: 'center',
              color: activeTab === tab.id
                ? (resolvedTheme === 'dark' ? '#fff' : '#000')
                : (resolvedTheme === 'dark' ? '#888' : '#666'),
              borderBottom: activeTab === tab.id
                ? '2px solid #0078d4'
                : '2px solid transparent',
              backgroundColor: activeTab === tab.id
                ? (resolvedTheme === 'dark' ? '#252526' : '#fff')
                : 'transparent',
            }}
          >
            {tab.label}
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
