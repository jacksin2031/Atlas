import React from "react";
import { useThemeStore } from "../../stores";
import { Icon } from "../../design-system";

export const ProjectExplorerPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  return (
    <div style={{ fontSize: 12, height: "100%", overflow: "auto" }}>
      <div style={{ padding: "4px 8px", fontWeight: 600, borderBottom: "1px solid " + (resolvedTheme === "dark" ? "#333" : "#ddd") }}>PROJECT EXPLORER</div>
      <div style={{ padding: 4 }}>
        <TreeNode label="Atlas" />
      </div>
    </div>
  );
};

const TreeNode: React.FC<{ label: string; children?: string[] }> = ({ label, children }) => {
  const [expanded, setExpanded] = React.useState(true);
  return (
    <div>
      <div style={{ padding: "2px 8px", cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }} onClick={() => setExpanded(!expanded)}>
        <span style={{ fontSize: 10 }}>{expanded ? "\u25BC" : "\u25B6"}</span>
        <Icon name="folder" size={13} />
        <span>{label}</span>
      </div>
      {expanded && children && (
        <div style={{ paddingLeft: 16 }}>
          {children.map((child) => (
            <div key={child} style={{ padding: "2px 8px", cursor: "pointer" }}>
              <Icon name="folder" size={13} /> {child}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
