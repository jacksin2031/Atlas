import React, { useState, useMemo, useRef, useEffect } from "react";
import { useThemeStore } from "../stores";
import { commandPaletteService } from "../services";

interface CommandPaletteProps {
  visible: boolean;
  onClose: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ visible, onClose }) => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const results = useMemo(() => {
    const allCommands = commandPaletteService.getAllCommands();
    if (!query) return allCommands.slice(0, 10);
    return commandPaletteService.search(query);
  }, [query]);

  useEffect(() => {
    if (visible && inputRef.current) {
      inputRef.current.focus();
    }
  }, [visible]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [results]);

  if (!visible) return null;

  const handleKeyDown = (e: React.KeyboardEvent): void => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && results[selectedIndex]) {
      commandPaletteService.execute(results[selectedIndex].id);
      onClose();
      setQuery("");
    } else if (e.key === "Escape") {
      onClose();
      setQuery("");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.4)",
        zIndex: 9999,
        display: "flex",
        justifyContent: "center",
        paddingTop: 80,
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: 560,
          maxHeight: 400,
          backgroundColor: resolvedTheme === "dark" ? "#2d2d2d" : "#fff",
          border: `1px solid ${resolvedTheme === "dark" ? "#555" : "#ccc"}`,
          borderRadius: 8,
          boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <input
          ref={inputRef}
          type="text"
          placeholder="Type a command..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{
            padding: "12px 16px",
            fontSize: 14,
            border: "none",
            borderBottom: `1px solid ${resolvedTheme === "dark" ? "#444" : "#ddd"}`,
            backgroundColor: "transparent",
            color: resolvedTheme === "dark" ? "#eee" : "#333",
            outline: "none",
          }}
        />
        <div style={{ flex: 1, overflow: "auto", padding: 4 }}>
          {results.length === 0 ? (
            <div style={{ padding: 16, textAlign: "center", opacity: 0.5, fontSize: 13 }}>No commands found</div>
          ) : (
            results.map((cmd, i) => (
              <div
                key={cmd.id}
                onMouseEnter={() => setSelectedIndex(i)}
                onClick={() => {
                  commandPaletteService.execute(cmd.id);
                  onClose();
                  setQuery("");
                }}
                style={{
                  padding: "8px 12px",
                  cursor: "pointer",
                  backgroundColor: i === selectedIndex ? (resolvedTheme === "dark" ? "#37373d" : "#e8f0fe") : "transparent",
                  borderRadius: 4,
                  fontSize: 13,
                }}
              >
                <div style={{ fontWeight: 500 }}>{cmd.label}</div>
                <div style={{ fontSize: 11, opacity: 0.5 }}>{cmd.description}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

