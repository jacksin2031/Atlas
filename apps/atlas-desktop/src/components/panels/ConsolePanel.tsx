import React from "react";

export const ConsolePanel: React.FC = () => {
  return (
    <div style={{ fontSize: 12, height: "100%", overflow: "auto" }}>
      <div style={{ padding: 8, opacity: 0.6 }}>Console is disabled. No REPL backend is connected.</div>
    </div>
  );
};
