import {
  controlWorkflowRuntime,
  getWorkflowRuntimeResult,
  getWorkflowRuntimeState,
  listenWorkflowRuntimeEvents,
  startWorkflowRuntime,
  validateWorkflowRuntime,
  armInputRuntime,
  emergencyStopInputRuntime,
  getInputRuntimeStatus,
} from "../../../ipc/bridge";
import { useProjectStore } from "../../../stores";
import { useDebugStore, useExecutionStore, useVariableStore, useWorkflowStore } from "../stores";
import type {
  ExecutionError, WorkflowDefinition, WorkflowRunStatus, WorkflowRuntimeEvent, WorkflowRuntimeState,
} from "../types";
import { serializeWorkflowForRuntime } from "./runtime-serialization";

type LegacyIPC = { invoke<T>(command: string, args: Record<string, unknown>): Promise<T> };

export interface ExecutorService {
  run(definition?: WorkflowDefinition | string): Promise<string>;
  pause(runId: string): Promise<void>;
  resume(runId: string): Promise<void>;
  stop(runId: string): Promise<void>;
  step(runId: string): Promise<void>;
  restart(runId: string): Promise<string>;
  simulate(runId: string): Promise<void>;
  dryRun(workflowId: string): Promise<ExecutionError[]>;
  getStatus(runId: string): Promise<WorkflowRunStatus>;
  armInput(allowedWindowTitle: string): Promise<void>;
  emergencyStop(): Promise<void>;
  inputStatus(): Promise<import("../../../ipc/bridge").InputSafetyStatus | null>;
}

export class IPCExecutorService implements ExecutorService {
  private ipc: LegacyIPC | null = null;

  setIPC(ipc: LegacyIPC): void { this.ipc = ipc; }

  private async invoke<T>(command: string, args: Record<string, unknown>): Promise<T | null> {
    return this.ipc ? this.ipc.invoke<T>(command, args) : null;
  }

  private definition(value?: WorkflowDefinition | string): WorkflowDefinition {
    const definition = typeof value === "object" ? value : useWorkflowStore.getState().exportToDefinition();
    if (typeof value === "string" && !definition.id) definition.id = value;
    const runtimeVariables = useVariableStore.getState().exportVariables();
    return { ...definition, variables: runtimeVariables.length ? runtimeVariables : definition.variables };
  }

  private projectContext(): Record<string, unknown> {
    const project = useProjectStore.getState().currentProject;
    return project ? { projectId: project.id, name: project.name, path: project.path } : {};
  }

  private breakpoints(): string[] {
    return useDebugStore.getState().breakpoints
      .filter((breakpoint) => breakpoint.enabled && breakpoint.type === "node")
      .map((breakpoint) => breakpoint.targetId);
  }

  private apply(state: WorkflowRuntimeState | null, operation: string): WorkflowRuntimeState {
    if (!state) {
      const message = `Workflow Runtime unavailable during ${operation}. Native execution requires the Tauri application.`;
      useExecutionStore.getState().setRuntimeError(message);
      throw new Error(message);
    }
    useExecutionStore.getState().applyRuntimeState(state);
    return state;
  }

  async validate(definition?: WorkflowDefinition): Promise<string[]> {
    const canonical = serializeWorkflowForRuntime(this.definition(definition));
    const response = this.ipc
      ? await this.invoke<import("../types").WorkflowValidationResponse>("workflow_validate", { definition: canonical })
      : await validateWorkflowRuntime(canonical);
    if (!response) {
      useExecutionStore.getState().setRuntimeError("Workflow Runtime unavailable. Validation requires the Tauri application.");
      return ["Workflow Runtime unavailable"];
    }
    useExecutionStore.getState().setRuntimeError(null);
    return response.errors;
  }

  async run(value?: WorkflowDefinition | string): Promise<string> {
    const definition = this.definition(value);
    const canonical = serializeWorkflowForRuntime(definition);
    const errors = await this.validate(definition);
    if (errors.length) throw new Error(`Workflow validation failed: ${errors.join("; ")}`);
    useExecutionStore.getState().setResult(null);
    const args = { definition: canonical, inputs: {}, projectContext: this.projectContext(), breakpoints: this.breakpoints() };
    const state = this.ipc
      ? await this.invoke<WorkflowRuntimeState>("workflow_start", args)
      : await startWorkflowRuntime(args.definition, args.inputs, args.projectContext, args.breakpoints);
    return this.apply(state, "start").executionId;
  }

  private async control(command: "workflow_pause" | "workflow_resume" | "workflow_stop" | "workflow_step", runId: string): Promise<void> {
    const state = this.ipc
      ? await this.invoke<WorkflowRuntimeState>(command, { executionId: runId })
      : await controlWorkflowRuntime(command, runId);
    this.apply(state, command);
  }

  pause(runId: string): Promise<void> { return this.control("workflow_pause", runId); }
  resume(runId: string): Promise<void> { return this.control("workflow_resume", runId); }
  stop(runId: string): Promise<void> { return this.control("workflow_stop", runId); }
  step(runId: string): Promise<void> { return this.control("workflow_step", runId); }

  async restart(runId: string): Promise<string> {
    if (useExecutionStore.getState().runs[runId]?.status === "interrupted") {
      return this.run();
    }
    const state = this.ipc
      ? await this.invoke<WorkflowRuntimeState>("workflow_restart", { executionId: runId })
      : await controlWorkflowRuntime("workflow_restart", runId);
    return this.apply(state, "restart").executionId;
  }

  async simulate(_runId: string): Promise<void> {
    throw new Error("Simulation is separate from Runtime Execution and no simulation adapter is configured.");
  }

  async dryRun(_workflowId: string): Promise<ExecutionError[]> {
    return (await this.validate()).map((message) => ({ nodeId: "", errorCode: "VALIDATION", message, timestamp: Date.now() }));
  }

  async getStatus(runId: string): Promise<WorkflowRunStatus> {
    const state = this.ipc
      ? await this.invoke<WorkflowRuntimeState>("workflow_get_state", { executionId: runId })
      : await getWorkflowRuntimeState(runId);
    return this.apply(state, "state query").status;
  }

  async refreshResult(runId: string): Promise<void> {
    const envelope = this.ipc
      ? await this.invoke<import("../types").WorkflowResultEnvelope>("workflow_get_result", { executionId: runId })
      : await getWorkflowRuntimeResult(runId);
    if (!envelope) return;
    useExecutionStore.getState().applyRuntimeState(envelope.state);
    useExecutionStore.getState().setResult(envelope.result);
  }

  handleRuntimeEvent(event: WorkflowRuntimeEvent): void {
    useExecutionStore.getState().applyRuntimeEvent(event);
    const debug = useDebugStore.getState();
    const timestamp = Date.parse(event.timestamp);
    if (event.eventType === "NodeStarted" && event.nodeId) {
      debug.setCurrentNode(event.nodeId);
      debug.pushExecutionPath(event.nodeId);
      debug.pushCallStack({ nodeId: event.nodeId, timestamp });
      debug.addEvent({ type: "node_enter", nodeId: event.nodeId, timestamp, data: event.data });
    } else if ((event.eventType === "NodeCompleted" || event.eventType === "NodeFailed") && event.nodeId) {
      debug.popCallStack();
      debug.addEvent({ type: event.eventType === "NodeFailed" ? "error" : "node_exit", nodeId: event.nodeId, timestamp, data: event.data });
    } else if (event.eventType === "WorkflowPaused") {
      debug.addEvent({ type: event.data.reason === "breakpoint" ? "breakpoint_hit" : "node_enter", nodeId: event.nodeId ?? undefined, timestamp, data: event.data });
    } else if (event.eventType === "VariableChanged" && typeof event.data.name === "string") {
      const variable = useVariableStore.getState().variables.find((item) => item.name === event.data.name);
      if (variable) useVariableStore.getState().setVariableValue(variable.id, event.data.value);
      debug.addEvent({ type: "variable_change", variableName: event.data.name, timestamp, data: event.data });
    }
    if (["WorkflowCompleted", "WorkflowFailed", "WorkflowCancelled"].includes(event.eventType)) {
      debug.setCurrentNode(null);
      void this.refreshResult(event.executionId);
    }
  }

  async connectRuntimeEvents(): Promise<() => void> {
    return listenWorkflowRuntimeEvents((event) => this.handleRuntimeEvent(event));
  }

  async armInput(allowedWindowTitle: string): Promise<void> {
    const status = await armInputRuntime({
      permissionGranted: true,
      allowedWindowTitle,
      maxActionsPerSecond: 15,
      maxTextLength: 1000,
      allowDangerousActions: false,
    });
    if (!status?.armed) throw new Error("Input Runtime could not be armed in the Tauri application.");
  }

  async emergencyStop(): Promise<void> {
    const status = await emergencyStopInputRuntime();
    if (!status?.emergencyStopped) throw new Error("Emergency stop did not reach the Input Runtime.");
  }

  inputStatus(): Promise<import("../../../ipc/bridge").InputSafetyStatus | null> {
    return getInputRuntimeStatus();
  }
}

export const executorService = new IPCExecutorService();
