import { describe, expect, it } from "vitest";
import { assertCredentialFree, interruptRecoverableRuns } from "../../../../services/project-assets";
import { stableProjectId } from "../../../../services/project";
import { sanitizeRestoredAIContexts } from "../../../ai/store";
import type { WorkflowRun } from "../../types";

const run = (status: WorkflowRun["status"]): WorkflowRun => ({
  id: `run-${status}`, workflowId: "workflow", status, nodeStates: {}, variables: {}, errors: [],
  metrics: { totalNodes: 1, completedNodes: 0, failedNodes: 0, duration: 0, throughput: 0 },
});

describe("project asset hardening", () => {
  it("rejects credential-shaped fields but permits token usage metrics", () => {
    expect(() => assertCredentialFree({ provider: { apiKey: "must-not-persist" } })).toThrow(/apiKey/);
    expect(() => assertCredentialFree({ metrics: { inputTokens: 12, totalTokens: 20 } })).not.toThrow();
  });

  it("restores non-terminal workflow runs as explicitly interrupted", () => {
    const restored = interruptRecoverableRuns({ active: run("running"), done: run("completed") });
    expect(restored.active?.status).toBe("interrupted");
    expect(restored.active?.errors.at(-1)?.errorCode).toBe("INTERRUPTED");
    expect(restored.done?.status).toBe("completed");
  });

  it("derives stable project ownership across restart and path spelling", () => {
    expect(stableProjectId("C:\\Atlas\\Project\\")).toBe(stableProjectId("c:/atlas/project"));
    expect(stableProjectId("C:\\Atlas\\Project-B")).not.toBe(stableProjectId("C:\\Atlas\\Project-A"));
  });

  it("restores Knowledge references as unresolved without stale content", () => {
    const contexts = sanitizeRestoredAIContexts([{ id:"knowledge:project-a:deleted", kind:"knowledge", label:"Deleted", preview:"stale content", includedInRequest:true }]);
    expect(contexts[0]).toMatchObject({ availability:"resolving", includedInRequest:false });
    expect(contexts[0]?.preview).toBeUndefined();
  });
});
