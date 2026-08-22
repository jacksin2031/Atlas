import React, { useState, useMemo } from "react";
import { useLogStore, useThemeStore } from "../../stores";
import { logService } from "../../services";

const LEVEL_COLORS: Record<string, string> = {
  trace: "#888",
  debug: "#4fc3f7",
  info: "#4caf50",
  warn: "#ff9800",
  error: "#f44336",
};

const LEVEL_OPTIONS = [
  { value: "all", label: "All Levels" },
  { value: "trace", label: "Trace" },
  { value: "debug", label: "Debug" },
  { value: "info", label: "Info" },
  { value: "warn", label: "Warn" },
  { value: "error", label: "Error" },
];

export const LogConsolePanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const entries = useLogStore((s) => s.entries);
  const filter = useLogStore((s) => s.filter);
  const setFilter = useLogStore((s) => s.setFilter);
  const clearEntries = useLogStore((s) => s.clearEntries);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredEntries = useMemo(() => {
    return entries.filter((entry) => {
      if (filter.level !== "all" && entry.level !== filter.level) return false;
      if (filter.source !== "all" && entry.source !== filter.source) return false;
      if (searchQuery && !entry.message.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      return true;
    });
  }, [entries, filter, searchQuery]);

  const handleExport = (): void => {
    const logStr = logService.exportLogs(filter);
    const blob = new Blob([logStr], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "atlas-logs-" + new Date().toISOString().slice(0, 10) + ".txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ padding: 4, display: "flex", gap: 4, borderBottom: "1px solid " + (resolvedTheme === "dark" ? "#333" : "#ddd") }}>
        <select value={filter.level} onChange={(e) => setFilter({ level: e.target.value })}
          style={{ fontSize: 11, padding: "2px 4px", backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff", color: resolvedTheme === "dark" ? "#ccc" : "#333", border: "1px solid " + (resolvedTheme === "dark" ? "#555" : "#ccc") }}>
          {LEVEL_OPTIONS.map((opt) => (<option key={opt.value} value={opt.value}>{opt.label}</option>))}
        </select>
        <input type="text" placeholder="Search logs..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
          style={{ flex: 1, fontSize: 11, padding: "2px 4px", backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff", color: resolvedTheme === "dark" ? "#ccc" : "#333", border: "1px solid " + (resolvedTheme === "dark" ? "#555" : "#ccc") }} />
        <button onClick={handleExport} style={{ fontSize: 11, padding: "2px 8px", cursor: "pointer", backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff", color: resolvedTheme === "dark" ? "#ccc" : "#333", border: "1px solid " + (resolvedTheme === "dark" ? "#555" : "#ccc") }}>Export</button>
        <button onClick={clearEntries} style={{ fontSize: 11, padding: "2px 8px", cursor: "pointer", backgroundColor: resolvedTheme === "dark" ? "#333" : "#fff", color: resolvedTheme === "dark" ? "#ccc" : "#333", border: "1px solid " + (resolvedTheme === "dark" ? "#555" : "#ccc") }}>Clear</button>
      </div>
      <div style={{ flex: 1, overflow: "auto", fontFamily: "monospace", fontSize: 11, padding: 4 }}>
        {filteredEntries.length === 0 ? (
          <div style={{ padding: 8, opacity: 0.5 }}>No log entries</div>
        ) : (
          filteredEntries.map((entry) => (
            <div key={entry.id} style={{ padding: "1px 4px", color: LEVEL_COLORS[entry.level] || "#ccc", whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
              {new Date(entry.timestamp).toLocaleTimeString()} [{entry.level.toUpperCase()}] [{entry.source}] {entry.message}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
