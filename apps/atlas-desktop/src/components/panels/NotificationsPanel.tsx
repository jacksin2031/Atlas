import React from "react";
import { useThemeStore, useProjectStore } from "../../stores";

export const NotificationsPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const notifications = useProjectStore((s) => s.notifications);
  const acknowledge = useProjectStore((s) => s.acknowledgeNotification);

  return (
    <div style={{ fontSize: 12, height: "100%", overflow: "auto" }}>
      {notifications.length === 0 ? (
        <div style={{ padding: 8, opacity: 0.5 }}>No notifications</div>
      ) : (
        notifications.map((n) => (
          <div key={n.id} style={{ padding: 8, marginBottom: 4, backgroundColor: resolvedTheme === "dark" ? "#2d2d2d" : "#f5f5f5", borderLeft: `3px solid ${n.severity === "error" ? "#f44336" : n.severity === "warning" ? "#ff9800" : n.severity === "success" ? "#4caf50" : "#2196f3"}`, borderRadius: 2 }}>
            <div style={{ fontWeight: 600 }}>{n.title}</div>
            <div style={{ opacity: 0.7, marginTop: 2 }}>{n.message}</div>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
              <span style={{ opacity: 0.4, fontSize: 10 }}>{new Date(n.timestamp).toLocaleString()}</span>
              {!n.acknowledged && (
                <button onClick={() => acknowledge(n.id)} style={{ background: "none", border: "none", color: "#2196f3", cursor: "pointer", fontSize: 11, padding: 0 }}>Acknowledge</button>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

