import React, { useMemo } from "react";
import { useRuntimeStore, useThemeStore } from "../../stores";
import type { RuntimeInfo, RuntimeHealth, AppStatus } from "../../types";

const STATUS_COLORS: Record<AppStatus, string> = {
  created: "#888",
  initializing: "#e6a817",
  ready: "#4caf50",
  running: "#2196f3",
  shutting_down: "#e6a817",
  terminated: "#f44336",
};

const HEALTH_ICONS: Record<RuntimeHealth, string> = {
  healthy: "\\u2714",
  degraded: "\\u26a0",
  unhealthy: "\\u2717",
  unknown: "?",
  starting: "\\u21bb",
  stopping: "\\u21ba",
};

export const RuntimeMonitorPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const runtimes = useRuntimeStore((s) => s.runtimes);

  const isInitialized = useRuntimeStore.getState().runtimes.length > 0;
  if (!isInitialized) {
    useRuntimeStore.getState().initializeRuntimes();
  }

  const stats = useMemo(() => {
    let healthy = 0;
    let running = 0;
    const total = runtimes.length;
    for (const r of runtimes) {
      if (r.health === "healthy") healthy++;
      if (r.status === "running" || r.status === "ready") running++;
    }
    return { healthy, running, total };
  }, [runtimes]);

  return (
    <div style={{ padding: 8, fontSize: 12, height: "100%", overflow: "auto" }}>
      <div style={{ marginBottom: 8, display: "flex", gap: 12 }}>
        <span>Total: {stats.total}</span>
        <span style={{ color: "#4caf50" }}>Healthy: {stats.healthy}</span>
        <span style={{ color: "#2196f3" }}>Running: {stats.running}</span>
      </div>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: `1px solid ${resolvedTheme === "dark" ? "#444" : "#ccc"}` }}>
            <th style={{ textAlign: "left", padding: "4px 8px" }}>Runtime</th>
            <th style={{ textAlign: "left", padding: "4px 8px" }}>Status</th>
            <th style={{ textAlign: "left", padding: "4px 8px" }}>Health</th>
            <th style={{ textAlign: "right", padding: "4px 8px" }}>CPU %</th>
            <th style={{ textAlign: "right", padding: "4px 8px" }}>Mem MB</th>
          </tr>
        </thead>
        <tbody>
          {runtimes.map((r) => (
            <RuntimeRow key={r.name} runtime={r} resolvedTheme={resolvedTheme} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

interface RuntimeRowProps {
  runtime: RuntimeInfo;
  resolvedTheme: "dark" | "light";
}

const RuntimeRow: React.FC<RuntimeRowProps> = ({ runtime, resolvedTheme }) => {
  const statusColor = STATUS_COLORS[runtime.status] || "#888";
  const healthIcon = HEALTH_ICONS[runtime.health] || "?";
  return (
    <tr style={{ borderBottom: `1px solid ${resolvedTheme === "dark" ? "#333" : "#eee"}` }}>
      <td style={{ padding: "4px 8px" }}>{runtime.name}</td>
      <td style={{ padding: "4px 8px", color: statusColor, fontWeight: 600 }}>{runtime.status.replace("_", " ")}</td>
      <td style={{ padding: "4px 8px" }}>{healthIcon}</td>
      <td style={{ padding: "4px 8px", textAlign: "right" }}>{runtime.cpuUsage.toFixed(1)}</td>
      <td style={{ padding: "4px 8px", textAlign: "right" }}>{runtime.memoryUsage.toFixed(0)}</td>
    </tr>
  );
};

