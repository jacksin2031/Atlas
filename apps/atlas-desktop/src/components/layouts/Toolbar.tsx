import React from "react";
import { useThemeStore } from "../../stores";

interface ToolbarProps {
  onToggleCommandPalette: () => void;
}

export const Toolbar: React.FC<ToolbarProps> = ({ onToggleCommandPalette }) => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const iconColor = resolvedTheme === "dark" ? "#aaa" : "#555";
  const hoverBg = resolvedTheme === "dark" ? "#3a3a3a" : "#e8e8e8";

  const btnStyle = (active = false): React.CSSProperties => ({
    background: active ? hoverBg : "none",
    border: "none",
    padding: "4px 8px",
    cursor: "pointer",
    color: iconColor,
    fontSize: 14,
    borderRadius: 4,
  });

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        height: 36,
        padding: "0 8px",
        gap: 2,
        backgroundColor: resolvedTheme === "dark" ? "#252526" : "#f0f0f0",
        borderBottom: `1px solid ${resolvedTheme === "dark" ? "#333" : "#ddd"}`,
      }}
    >
      <button style={btnStyle()} title="Back" onClick={() => console.info("[Toolbar] Back")}>&#8592;</button>
      <button style={btnStyle()} title="Forward" onClick={() => console.info("[Toolbar] Forward")}>&#8594;</button>
      <div style={{ width: 1, height: 20, backgroundColor: resolvedTheme === "dark" ? "#444" : "#ccc", margin: "0 4px" }} />
      <button style={btnStyle()} title="Refresh" onClick={() => console.info("[Toolbar] Refresh")}>&#8635;</button>
      <div style={{ flex: 1 }} />
      <button style={btnStyle()} title="Command Palette (Ctrl+Shift+P)" onClick={onToggleCommandPalette}>&#8984;</button>
    </div>
  );
};

