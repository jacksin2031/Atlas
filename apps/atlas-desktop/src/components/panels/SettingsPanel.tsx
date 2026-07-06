import React from "react";
import { useThemeStore, useLayoutStore, useLogStore } from "../../stores";
import { themeService } from "../../services";
import type { ThemeMode } from "../../types";

export const SettingsPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const themeMode = useThemeStore((s) => s.mode);

  const handleThemeChange = (mode: ThemeMode): void => {
    themeService.setTheme(mode);
  };

  const handleResetLayout = (): void => {
    useLayoutStore.getState().resetLayout();
    useLogStore.getState().addEntry({
      timestamp: Date.now(),
      level: "info",
      source: "SettingsPanel",
      message: "Layout reset triggered from Settings",
    });
  };

  return (
    <div style={{ padding: 16, fontSize: 12, height: "100%", overflow: "auto" }}>
      <h3 style={{ margin: "0 0 12px", fontSize: 14 }}>Settings</h3>
      <section style={{ marginBottom: 20 }}>
        <h4 style={{ margin: "0 0 8px", fontSize: 13 }}>Appearance</h4>
        <label style={{ display: "block", marginBottom: 4 }}>
          <input type="radio" name="theme" checked={themeMode === "dark"} onChange={() => handleThemeChange("dark")} /> Dark
        </label>
        <label style={{ display: "block", marginBottom: 4 }}>
          <input type="radio" name="theme" checked={themeMode === "light"} onChange={() => handleThemeChange("light")} /> Light
        </label>
        <label style={{ display: "block", marginBottom: 4 }}>
          <input type="radio" name="theme" checked={themeMode === "system"} onChange={() => handleThemeChange("system")} /> System
        </label>
      </section>
      <section style={{ marginBottom: 20 }}>
        <h4 style={{ margin: "0 0 8px", fontSize: 13 }}>Layout</h4>
        <button onClick={handleResetLayout} style={{ padding: "6px 16px", fontSize: 12, cursor: "pointer", backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff", color: resolvedTheme === "dark" ? "#ccc" : "#333", border: `1px solid ${resolvedTheme === "dark" ? "#555" : "#ccc"}`, borderRadius: 4 }}>Reset Layout</button>
      </section>
      <section style={{ marginBottom: 20 }}>
        <h4 style={{ margin: "0 0 8px", fontSize: 13 }}>About</h4>
        <div style={{ opacity: 0.7 }}>
          <div>Atlas Desktop Shell v0.12.0-alpha</div>
          <div>Atlas Platform - Record Once. Understand Forever.</div>
        </div>
      </section>
    </div>
  );
};

