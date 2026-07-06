import React from "react";
import { useLayoutStore, useThemeStore } from "../../stores";
import type { PanelId } from "../../types";

interface MenuBarProps {
  onToggleCommandPalette: () => void;
}

type MenuItem = { label: string; action?: () => void; shortcut?: string } | { separator: true };

export const MenuBar: React.FC<MenuBarProps> = ({ onToggleCommandPalette }) => {
  const resolvedTheme = useThemeStore((s: { resolvedTheme: string }) => s.resolvedTheme);

  const handleResetLayout = (): void => {
    useLayoutStore.getState().resetLayout();
  };

  return (
    <nav style={{
      display: "flex", alignItems: "center", height: 32, padding: "0 8px",
      backgroundColor: resolvedTheme === "dark" ? "#1e1e1e" : "#f3f3f3",
      borderBottom: "1px solid " + (resolvedTheme === "dark" ? "#333" : "#ddd"),
      userSelect: "none",
    }}>
      <span style={{ fontWeight: 600, fontSize: 13, marginRight: 16, color: resolvedTheme === "dark" ? "#fff" : "#333" }}>Atlas</span>
      <MenuDropdown label="File" items={[
        { label: "Open Project" }, { label: "Close Project" }, { separator: true } as const, { label: "Exit" }
      ]} resolvedTheme={resolvedTheme} />
      <MenuDropdown label="Edit" items={[
        { label: "Undo" }, { label: "Redo" }, { separator: true } as const, { label: "Find and Replace" }
      ]} resolvedTheme={resolvedTheme} />
      <MenuDropdown label="View" items={[
        { label: "Command Palette", shortcut: "Ctrl+Shift+P", action: onToggleCommandPalette },
        { separator: true } as const,
        { label: "Project Explorer", action: () => togglePanel("project-explorer") },
        { label: "Runtime Monitor", action: () => togglePanel("runtime-monitor") },
        { label: "Output", action: () => togglePanel("output") },
        { label: "Console", action: () => togglePanel("console") },
        { label: "Logs", action: () => togglePanel("logs") },
        { label: "Extensions", action: () => togglePanel("extensions") },
        { label: "Settings", action: () => togglePanel("settings") },
        { label: "Problems", action: () => togglePanel("problems") },
        { label: "Notifications", action: () => togglePanel("notifications") },
        { separator: true } as const,
        { label: "Reset Layout", action: handleResetLayout },
      ]} resolvedTheme={resolvedTheme} />
      <MenuDropdown label="Run" items={[
        { label: "Start All Runtimes" }, { label: "Stop All Runtimes" }, { separator: true } as const, { label: "Restart Selected" }
      ]} resolvedTheme={resolvedTheme} />
      <MenuDropdown label="Tools" items={[
        { label: "Export Logs" }, { label: "Clear Logs" }
      ]} resolvedTheme={resolvedTheme} />
      <MenuDropdown label="Help" items={[
        { label: "About Atlas" }
      ]} resolvedTheme={resolvedTheme} />
    </nav>
  );

  function togglePanel(id: PanelId): void {
    const current = useLayoutStore.getState().config.panels[id];
    useLayoutStore.getState().setPanelVisible(id, !(current?.visible ?? false));
  }
};

interface MenuDropdownProps {
  label: string;
  items: readonly MenuItem[];
  resolvedTheme: string;
}

const MenuDropdown: React.FC<MenuDropdownProps> = ({ label, items, resolvedTheme }) => {
  const [open, setOpen] = React.useState(false);
  // hovered state reserved for future use
// const [hovered, setHovered] = React.useState(false);
  const timerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  const openMenu = () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    setOpen(true);
  };

  const closeMenu = () => {
    timerRef.current = setTimeout(() => setOpen(false), 200);
  };

  const handleMouseEnter = () => {
    openMenu();
  };

  const handleMouseLeave = () => {
    closeMenu();
  };

  return (
    <div
      style={{ position: "relative", display: "inline-block" }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <button
        style={{
          background: "none",
          border: "none",
          padding: "4px 10px",
          fontSize: 12,
          color: resolvedTheme === "dark" ? "#ccc" : "#444",
          cursor: "pointer",
        }}
        onClick={() => setOpen(!open)}
      >
        {label}
      </button>
      {open && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            minWidth: 200,
            backgroundColor: resolvedTheme === "dark" ? "#2d2d2d" : "#fff",
            border: "1px solid " + (resolvedTheme === "dark" ? "#444" : "#ccc"),
            boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
            zIndex: 1000,
          }}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          {items.map((item, i) =>
            "separator" in item ? (
              <hr
                key={i}
                style={{
                  margin: 0,
                  border: "none",
                  borderTop: "1px solid " + (resolvedTheme === "dark" ? "#444" : "#ddd"),
                }}
              />
            ) : (
              <div
                key={i}
                style={{
                  padding: "6px 16px",
                  fontSize: 12,
                  color: resolvedTheme === "dark" ? "#ddd" : "#333",
                  cursor: "pointer",
                  display: "flex",
                  justifyContent: "space-between",
                }}
                onClick={() => {
                  item.action?.();
                  setOpen(false);
                }}
              >
                <span>{item.label}</span>
                {item.shortcut && <span style={{ opacity: 0.5 }}>{item.shortcut}</span>}
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
};
