import React, { useState, useMemo } from "react";
import { usePluginStore, useThemeStore } from "../../stores";
import type { PluginEntry, PluginHealth, PluginState as PluginStateType } from "../../types";

const STATE_BADGE: Record<PluginStateType, string> = {
  installed: "#4caf50",
  available: "#2196f3",
  updating: "#ff9800",
  error: "#f44336",
};

const HEALTH_BADGE: Record<PluginHealth, string> = {
  healthy: "\u2714",
  degraded: "\u26a0",
  unhealthy: "\u2717",
  unknown: "?",
};

export const ExtensionsPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const plugins = usePluginStore((s) => s.plugins);
  const togglePlugin = usePluginStore((s) => s.togglePlugin);
  const searchPlugins = usePluginStore((s) => s.searchPlugins);

  const [searchQuery, setSearchQuery] = useState("");

  const displayed = useMemo(() => {
    return searchQuery ? searchPlugins(searchQuery) : plugins;
  }, [plugins, searchQuery, searchPlugins]);

  return (
    <div style={{ padding: 8, fontSize: 12, height: "100%", overflow: "auto" }}>
      <input
        type="text"
        placeholder="Search extensions..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        style={{
          width: "100%",
          fontSize: 11,
          padding: "4px 8px",
          marginBottom: 8,
          backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff",
          color: resolvedTheme === "dark" ? "#ccc" : "#333",
          border: `1px solid ${resolvedTheme === "dark" ? "#555" : "#ccc"}`,
          boxSizing: "border-box",
        }}
      />
      {displayed.map((plugin) => (
        <PluginCard key={plugin.id} plugin={plugin} onToggle={() => togglePlugin(plugin.id)} resolvedTheme={resolvedTheme} />
      ))}
      {displayed.length === 0 && (
        <div style={{ opacity: 0.5, textAlign: "center", padding: 16 }}>No extensions found</div>
      )}
    </div>
  );
};

interface PluginCardProps {
  plugin: PluginEntry;
  onToggle: () => void;
  resolvedTheme: "dark" | "light";
}

const PluginCard: React.FC<PluginCardProps> = ({ plugin, onToggle, resolvedTheme }) => {
  return (
    <div
      style={{
        padding: 8,
        marginBottom: 4,
        backgroundColor: resolvedTheme === "dark" ? "#2d2d2d" : "#f9f9f9",
        border: `1px solid ${resolvedTheme === "dark" ? "#444" : "#ddd"}`,
        borderRadius: 4,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <strong style={{ fontSize: 12 }}>{plugin.name}</strong>{" "}
          <span style={{ opacity: 0.5, fontSize: 11 }}>v{plugin.version}</span>
        </div>
        <label style={{ display: "flex", alignItems: "center", gap: 4, cursor: "pointer" }}>
          <input
            type="checkbox"
            checked={plugin.enabled}
            onChange={onToggle}
          />
          <span style={{ fontSize: 11 }}>On</span>
        </label>
      </div>
      <div style={{ fontSize: 11, opacity: 0.7, marginTop: 4 }}>{plugin.description}</div>
      <div style={{ display: "flex", gap: 8, marginTop: 4, fontSize: 11 }}>
        <span style={{ color: STATE_BADGE[plugin.state] }}>{plugin.state}</span>
        <span>{HEALTH_BADGE[plugin.health]}</span>
        <span style={{ opacity: 0.5 }}>{plugin.author}</span>
      </div>
    </div>
  );
};
