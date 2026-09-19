import React from "react";
import { useThemeStore, useProjectStore } from "../../stores";
import { AppVersion } from "../AppVersion";
import { useWorkspaceStore } from "../../workspace";
import { useAIStudioStore } from "../../studio/ai";
import { useKnowledgeStudioStore } from "../../studio/knowledge";

export const StatusBar: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);
  const currentProject = useProjectStore((s) => s.currentProject);
  const notifications = useProjectStore((s) => s.notifications);
  const unacknowledged = notifications.filter((n) => !n.acknowledged).length;
  const activeWorkspace = useWorkspaceStore((s) => s.activeWorkspace);
  const provider = useAIStudioStore((s) => s.providers.find((item) => item.providerId === s.selectedProviderId)?.name);
  const model = useAIStudioStore((s) => s.models.find((item) => item.modelId === s.selectedModelId)?.name);
  const aiHealth = useAIStudioStore((s) => s.runtimeHealth);
  const aiRunning = useAIStudioStore((s) => s.running);
  const usage = useAIStudioStore((s) => s.lastResponse?.usage?.totalTokens);
  const knowledgeHealth = useKnowledgeStudioStore((s) => s.health);

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        height: 24,
        padding: "0 12px",
        backgroundColor: resolvedTheme === "dark" ? "#007acc" : "#005a9e",
        color: "#fff",
        fontSize: 12,
        gap: 16,
      }}
    >
      <span>{currentProject ? `Project: ${currentProject.name}` : "No project open"}</span>
      {activeWorkspace === "ai" && <><span>Provider: {provider ?? "None"}</span><span>Model: {model ?? "None"}</span><span>AI Runtime: {aiHealth}</span>{usage !== undefined && <span>{usage} tokens</span>}{aiRunning && <span role="status">Generating</span>}</>}
      {activeWorkspace === "knowledge" && <><span>Knowledge Runtime: {knowledgeHealth.status}</span><span>{knowledgeHealth.entryCount} entries</span><span>Index: {knowledgeHealth.index?.state ?? "unavailable"}</span></>}
      <div style={{ flex: 1 }} />
      {unacknowledged > 0 && (
        <span title={`Unacknowledged: ${unacknowledged}`}>&#9888; {unacknowledged}</span>
      )}
      <AppVersion />
    </div>
  );
};
