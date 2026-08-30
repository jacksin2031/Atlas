import React from "react";
import { useExecutionStore } from "../../studio/workflow/stores";
import { useWorkspaceStore } from "../../workspace";

export const OutputPanel: React.FC = () => {
  const workspace = useWorkspaceStore((state) => state.activeWorkspace);
  const result = useExecutionStore((state) => state.result);
  const activeRunId = useExecutionStore((state) => state.activeRunId);
  const activeRun = useExecutionStore((state) => state.activeRunId ? state.runs[state.activeRunId] : undefined);
  const runtimeError = useExecutionStore((state) => state.runtimeError);
  if (workspace !== "workflow") return <div style={{ padding: 8, opacity: 0.6, fontSize: 12 }}>No output channels configured for this workspace.</div>;
  const value = result ? JSON.stringify(result, null, 2) : "";
  const exportResult = (): void => {
    if (!value) return;
    const url = URL.createObjectURL(new Blob([value], { type: "application/json" }));
    const link = document.createElement("a"); link.href = url; link.download = `workflow-result-${activeRunId ?? "unknown"}.json`; link.click(); URL.revokeObjectURL(url);
  };
  return <div style={{ fontSize: 12, height: "100%", overflow: "auto", padding: 8 }}>
    <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 8 }}>
      <strong>Runtime Execution</strong>
      <span style={{ color: activeRun?.status === "completed" ? "#4CAF50" : activeRun?.status === "failed" ? "#F44336" : "#aaa" }}>{activeRun?.status ?? "idle"}</span>
      <span style={{ fontFamily: "monospace", color: "#777" }}>{activeRunId ?? "No execution"}</span>
      <span style={{ flex: 1 }}/>
      <button disabled={!value} onClick={() => value && void navigator.clipboard.writeText(value)}>Copy</button>
      <button disabled={!value} onClick={exportResult}>Export</button>
    </div>
    {runtimeError && <div style={{ color: "#F44336", marginBottom: 8 }}>{runtimeError}</div>}
    {result ? <>
      <dl style={{ display: "grid", gridTemplateColumns: "100px 1fr", margin: 0 }}>
        <dt>Workflow</dt><dd>{result.workflowId}</dd>
        <dt>Execution</dt><dd>{result.executionId}</dd>
        <dt>Status</dt><dd>{result.status}</dd>
        <dt>Success</dt><dd>{String(result.success)}</dd>
        <dt>Started</dt><dd>{activeRun?.startedAt ? new Date(activeRun.startedAt).toISOString() : "—"}</dd>
        <dt>Completed</dt><dd>{activeRun?.completedAt ? new Date(activeRun.completedAt).toISOString() : "—"}</dd>
        <dt>Duration</dt><dd>{result.durationMs ?? activeRun?.metrics.duration ?? 0} ms</dd>
        <dt>Nodes</dt><dd>{activeRun ? `${activeRun.metrics.completedNodes}/${activeRun.metrics.totalNodes} completed, ${activeRun.metrics.failedNodes} failed` : "—"}</dd>
      </dl>
      <h4>Workflow Output</h4><pre style={{ whiteSpace: "pre-wrap", userSelect: "text" }}>{JSON.stringify(result.output, null, 2)}</pre>
      {result.error && <><h4>Error</h4><pre style={{ color: "#F44336" }}>{result.error}</pre></>}
      <details><summary>Structured Result</summary><pre style={{ whiteSpace: "pre-wrap" }}>{value}</pre></details>
    </> : <div style={{ opacity: 0.6 }}>Run a workflow in the Tauri application. Backend results appear here; browser mode does not simulate execution.</div>}
  </div>;
};
