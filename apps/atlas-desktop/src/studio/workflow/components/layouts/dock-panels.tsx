// Atlas Workflow Studio — Dock Panels Integration
import React, { useMemo } from 'react';
import { useLayoutStore, useThemeStore } from '../../../../stores';

interface DockPanelsProps {
  children: React.ReactNode;
}

export const DockPanels: React.FC<DockPanelsProps> = ({ children }) => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const config = useLayoutStore((s) => s.config);

  const visiblePanels = useMemo(() => {
    return Object.values(config.panels).filter((p) => p.visible);
  }, [config.panels]);

  if (visiblePanels.length === 0) {
    return (
      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: resolvedTheme === 'dark' ? '#666' : '#999',
          fontSize: 14,
        }}
      >
        No panels are visible. Enable panels via View menu.
      </div>
    );
  }

  return (
    <div
      style={{
        flex: 1,
        display: 'grid',
        gridTemplateColumns: visiblePanels.some((p) => p.position === 'left' || p.position === 'right')
          ? 'auto 1fr auto'
          : '1fr',
        gridTemplateRows: visiblePanels.some((p) => p.position === 'bottom')
          ? '1fr auto'
          : '1fr',
        gap: 0,
        overflow: 'hidden',
      }}
    >
      {children}
    </div>
  );
};
