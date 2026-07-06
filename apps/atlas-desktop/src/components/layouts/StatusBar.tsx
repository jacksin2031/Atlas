import React from "react";
import { useThemeStore, useProjectStore } from "../../stores";

export const StatusBar: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const currentProject = useProjectStore((s) => s.currentProject);
  const notifications = useProjectStore((s) => s.notifications);
  const unacknowledged = notifications.filter((n) => !n.acknowledged).length;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        height: 24,
        padding: "0 12px",
        backgroundColor: resolvedTheme === "dark" ? "#007acc" : "#005a9e",
        color: "#fff",
        fontSize: 12,
        gap: 16,
      }}
    >
      <span>{currentProject ? `Project: ${currentProject.name}` : "No project open"}</span>
      <div style={{ flex: 1 }} />
      {unacknowledged > 0 && (
        <span title={`Unacknowledged: ${unacknowledged}`}>&#9888; {unacknowledged}</span>
      )}
      <span>Atlas v0.12.0-alpha</span>
    </div>
  );
};

