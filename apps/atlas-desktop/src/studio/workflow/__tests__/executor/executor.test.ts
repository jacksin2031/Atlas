import { beforeEach, describe, expect, it } from "vitest";
import { IPCExecutorService } from "../../services/executor-service";
import { serializeWorkflowForRuntime } from "../../services/runtime-serialization";
import { useDebugStore, useExecutionStore, useVariableStore, useWorkflowStore } from "../../stores";
import type { WorkflowDefinition, WorkflowRuntimeState } from "../../types";

const definition: WorkflowDefinition = {
  id: "wf-runtime", name: "Runtime Workflow", version: "1.0.0",
  nodes: [
    { id: "entry", type: "entry", label: "Entry", category: "core", inputs: [], outputs: [{ id: "entry-out", name: "output", type: "any" }], parameters: {} },
    { id: "constant", type: "constant", label: "Constant", category: "core", inputs: [{ id: "constant-in", name: "trigger", type: "any" }], outputs: [{ id: "constant-out", name: "value", type: "string" }], parameters: { value: "Atlas" } },
    { id: "exit", type: "exit", label: "Exit", category: "core", inputs: [{ id: "exit-in", name: "input", type: "string" }], outputs: [], parameters: {} },
  ],
  edges: [
    { id: "edge-1", source: "entry", target: "constant", sourcePort: "entry-out", targetPort: "constant-in", edgeType: "data" },
    { id: "edge-2", source: "constant", target: "exit", sourcePort: "constant-out", targetPort: "exit-in", edgeType: "data" },
  ],
  variables: [{ id: "variable-1", name: "greeting", type: "string", scope: "workflow", defaultValue: "Hello", writable: true }],
  parameters: {}, metadata: { createdAt: 1, updatedAt: 2, tags: ["test"] },
};

const runtimeState = (status: WorkflowRuntimeState["status"] = "scheduled", executionId = "execution-1"): WorkflowRuntimeState => ({
  executionId, workflowId: definition.id, status, currentNodeId: null,
  nodeStates: { entry: "pending", constant: "pending", exit: "pending" }, nodeResults: {},
  variables: { greeting: "Hello" }, startedAt: new Date(0).toISOString(),
  metrics: { totalNodes: 3, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 },
});

describe("Workflow Runtime integration", () => {
  beforeEach(() => {
    useWorkflowStore.getState().resetCanvas();
    useExecutionStore.getState().reset();
    useDebugStore.getState().reset();
    useVariableStore.getState().reset();
  });

  it("serializes graph ports, edges, variables, parameters, and requirements to the canonical manifest", () => {
    const manifest = serializeWorkflowForRuntime({ ...definition, requiredCapabilities: ["core"], requiredPlugins: ["atlas.test"] });
    expect(manifest.entry_nodes).toEqual(["entry"]);
    expect(manifest.exit_nodes).toEqual(["exit"]);
    expect(manifest.nodes[1]).toMatchObject({ id: "constant", type: "constant", config: { value: "Atlas" }, ports_in: ["constant-in"], ports_out: ["constant-out"] });
    expect(manifest.edges[1]).toMatchObject({ source_port: "constant-out", target_port: "exit-in" });
    expect(manifest.variables[0]).toMatchObject({ name: "greeting", scope: "workflow", default: "Hello" });
    expect(manifest.plugins).toEqual(["atlas.test"]);
  });

  it("routes validate/start/control/state/result through the native command contract", async () => {
    const service = new IPCExecutorService();
    const commands: string[] = [];
    service.setIPC({ invoke: async <T>(command: string): Promise<T> => {
      commands.push(command);
      if (command === "workflow_validate") return { valid: true, errors: [], plan: ["entry", "constant", "exit"] } as T;
      if (command === "workflow_get_result") return { result: { executionId: "execution-1", workflowId: definition.id, status: "completed", success: true, output: { value: "Atlas" } }, state: runtimeState("completed"), history: [] } as T;
      return runtimeState(command === "workflow_pause" ? "paused" : command === "workflow_resume" ? "running" : command === "workflow_stop" ? "cancelled" : "scheduled") as T;
    }});
    const executionId = await service.run(definition);
    await service.pause(executionId); await service.resume(executionId); await service.step(executionId); await service.stop(executionId);
    await service.getStatus(executionId); await service.refreshResult(executionId);
    expect(commands).toEqual(["workflow_validate", "workflow_start", "workflow_pause", "workflow_resume", "workflow_step", "workflow_stop", "workflow_get_state", "workflow_get_result"]);
    expect(useExecutionStore.getState().result?.output).toEqual({ value: "Atlas" });
  });

  it("manually restarts an interrupted recovered run as a new execution", async () => {
    const service = new IPCExecutorService();
    const commands: string[] = [];
    useWorkflowStore.getState().loadFromDefinition(definition);
    useExecutionStore.setState({
      runs: { "execution-old": { id: "execution-old", workflowId: definition.id, status: "interrupted", nodeStates: {}, variables: {}, errors: [], metrics: { totalNodes: 3, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 } } },
      activeRunId: "execution-old", status: "interrupted", isRunning: false, isPaused: false,
    });
    service.setIPC({ invoke: async <T>(command: string): Promise<T> => {
      commands.push(command);
      if (command === "workflow_validate") return { valid: true, errors: [], plan: ["entry", "constant", "exit"] } as T;
      return runtimeState("scheduled", "execution-new") as T;
    }});
    expect(await service.restart("execution-old")).toBe("execution-new");
    expect(commands).toEqual(["workflow_validate", "workflow_start"]);
  });

  it("uses correlated runtime events for node state, debugger path, variables, and bounded history", () => {
    const service = new IPCExecutorService();
    useExecutionStore.getState().applyRuntimeState(runtimeState("running"));
    service.handleRuntimeEvent({ eventId: "1", eventType: "NodeStarted", timestamp: new Date().toISOString(), workflowId: definition.id, executionId: "execution-1", nodeId: "constant", correlationId: "execution-1", data: {} });
    service.handleRuntimeEvent({ eventId: "2", eventType: "NodeCompleted", timestamp: new Date().toISOString(), workflowId: definition.id, executionId: "execution-1", nodeId: "constant", correlationId: "execution-1", data: { inputs: { trigger: null }, outputs: { value: "Atlas" }, duration_ms: 2 } });
    service.handleRuntimeEvent({ eventId: "3", eventType: "VariableChanged", timestamp: new Date().toISOString(), workflowId: definition.id, executionId: "execution-1", nodeId: "constant", correlationId: "execution-1", data: { name: "greeting", value: "Atlas" } });
    expect(useExecutionStore.getState().runs["execution-1"]?.nodeStates.constant).toBe("completed");
    expect(useExecutionStore.getState().nodeResults.constant?.outputs).toEqual({ value: "Atlas" });
    expect(useExecutionStore.getState().runs["execution-1"]?.variables.greeting).toBe("Atlas");
    expect(useDebugStore.getState().executionPath).toEqual(["constant"]);
  });

  it("ignores a different execution for active node state", () => {
    const service = new IPCExecutorService();
    useExecutionStore.getState().applyRuntimeState(runtimeState("running"));
    service.handleRuntimeEvent({ eventId: "other", eventType: "NodeFailed", timestamp: new Date().toISOString(), workflowId: definition.id, executionId: "execution-other", nodeId: "constant", correlationId: "execution-other", data: { error: "other" } });
    expect(useExecutionStore.getState().runs["execution-1"]?.nodeStates.constant).toBe("pending");
  });
});
