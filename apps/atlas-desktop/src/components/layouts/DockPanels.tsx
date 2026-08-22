import React, { useMemo } from "react";
import { useLayoutStore, useThemeStore } from "../../stores";
import type { PanelId } from "../../types";

interface DockPanelsProps {
  children: React.ReactNode;
}

/**
 * DockPanels renders visible panels in a grid layout based on their dock position.
 * Supports resizable splitters between panels.
 */
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
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: resolvedTheme === "dark" ? "#666" : "#999",
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
        display: "grid",
        gridTemplateColumns: visiblePanels.some((p) => p.position === "left" || p.position === "right")
          ? "auto 1fr auto"
          : "1fr",
        gridTemplateRows: visiblePanels.some((p) => p.position === "bottom")
          ? "1fr auto"
          : "1fr",
        gap: 0,
        overflow: "hidden",
      }}
    >
      {children}
    </div>
  );
};

interface PanelContainerProps {
  panelId: PanelId;
  title: string;
  children: React.ReactNode;
  position?: "left" | "right" | "bottom";
}

export const PanelContainer: React.FC<PanelContainerProps> = ({
  panelId,
  title,
  children,
  position = "left",
}) => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const panel = useLayoutStore((s) => s.config.panels[panelId]);
  const isActive = useLayoutStore((s) => s.config.activePanel === panelId);

  if (!panel || !panel.visible) return null;

  const isCollapsed = panel.collapsed;
  const isBottom = position === "bottom";
  const isRight = position === "right";

  const baseStyle: React.CSSProperties = {
    backgroundColor: resolvedTheme === "dark" ? "#252526" : "#fff",
    border: `1px solid ${resolvedTheme === "dark" ? "#333" : "#ddd"}`,
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  };

  const widthStyle = isBottom ? {} : { width: isRight ? 300 : 260 };
  const heightStyle = isBottom ? { height: 200 } : {};
  const gridArea = isBottom
    ? "2 / 1 / 3 / -1"
    : position === "left"
      ? "1 / 1 / -1 / 2"
      : position === "right"
        ? "1 / 3 / -1 / -1"
        : "1 / 1 / -1 / -1";

  return (
    <div
      style={{
        ...baseStyle,
        ...widthStyle,
        ...heightStyle,
        gridArea,
        borderRight: isRight ? "none" : undefined,
        borderBottom: isBottom ? "none" : undefined,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          height: 28,
          padding: "0 8px",
          backgroundColor: isActive
            ? resolvedTheme === "dark" ? "#37373d" : "#e8e8e8"
            : resolvedTheme === "dark" ? "#2d2d2d" : "#f5f5f5",
          borderBottom: `1px solid ${resolvedTheme === "dark" ? "#333" : "#ddd"}`,
          cursor: "pointer",
          userSelect: "none",
        }}
        onClick={() => useLayoutStore.getState().setPanelCollapsed(panelId, !isCollapsed)}
      >
        <span style={{ fontSize: 12, color: resolvedTheme === "dark" ? "#ccc" : "#444", flex: 1 }}>
          {title}
        </span>
        <button
          style={{
            background: "none",
            border: "none",
            color: resolvedTheme === "dark" ? "#888" : "#666",
            cursor: "pointer",
            fontSize: 14,
            padding: "0 4px",
          }}
          onClick={(e) => {
            e.stopPropagation();
            useLayoutStore.getState().setPanelVisible(panelId, false);
          }}
          title="Close panel"
        >
          &#10005;
        </button>
      </div>
      {!isCollapsed && <div style={{ flex: 1, overflow: "auto" }}>{children}</div>}
    </div>
  );
};
