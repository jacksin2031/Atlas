import React from "react";

export const OutputPanel: React.FC = () => {
  return (
    <div style={{ fontSize: 12, height: "100%", overflow: "auto" }}>
      <div style={{ padding: 8, opacity: 0.6 }}>No output channels configured.</div>
    </div>
  );
};

