// Atlas Workflow Studio — Debug Store Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { useDebugStore } from '../../stores/debug-store';

describe('DebugStore', () => {
  beforeEach(() => {
    useDebugStore.getState().reset();
  });

  it('should create a debug session', () => {
    const id = useDebugStore.getState().createSession('run_1');
    expect(id).toBeTruthy();
    const session = useDebugStore.getState().sessions[id]!;
    expect(session.runId).toBe('run_1');
    expect(session?.paused).toBe(false);
  });

  it('should attach/detach', () => {
    expect(useDebugStore.getState().isAttached).toBe(false);
    useDebugStore.getState().attach();
    expect(useDebugStore.getState().isAttached).toBe(true);
    useDebugStore.getState().detach();
    expect(useDebugStore.getState().isAttached).toBe(false);
  });

  it('should add breakpoints', () => {
    useDebugStore.getState().addBreakpoint({ type: 'node' as const, targetId: 'n1', condition: undefined } as any);
    expect(useDebugStore.getState().breakpoints).toHaveLength(1);
    const bp = useDebugStore.getState().breakpoints[0]!!;
    expect(bp.targetId).toBe('n1');
    expect(bp?.enabled).toBe(true);
    expect(bp?.hitCount).toBe(0);
  });

  it('should toggle breakpoints', () => {
    useDebugStore.getState().addBreakpoint({ type: 'node' as const, targetId: 'n1' } as any);
    const bpList = useDebugStore.getState().breakpoints;
    if (bpList.length > 0) useDebugStore.getState().toggleBreakpoint(bpList[0]!.id);
    const bp = useDebugStore.getState().breakpoints[0]!!;
    expect(bp?.enabled).toBe(false);
  });

  it('should remove breakpoints', () => {
    useDebugStore.getState().addBreakpoint({ type: 'node' as const, targetId: 'n1' } as any);
    const id = useDebugStore.getState().breakpoints[0]!!.id;
    useDebugStore.getState().removeBreakpoint(id);
    expect(useDebugStore.getState().breakpoints).toHaveLength(0);
  });

  it('should clear breakpoints', () => {
    useDebugStore.getState().addBreakpoint({ type: 'node' as const, targetId: 'n1' } as any);
    useDebugStore.getState().addBreakpoint({ type: 'node' as const, targetId: 'n2' } as any);
    useDebugStore.getState().clearBreakpoints();
    expect(useDebugStore.getState().breakpoints).toHaveLength(0);
  });

  it('should track execution path', () => {
    useDebugStore.getState().pushExecutionPath('n1');
    useDebugStore.getState().pushExecutionPath('n2');
    expect(useDebugStore.getState().executionPath).toEqual(['n1', 'n2']);
  });

  it('should track call stack', () => {
    useDebugStore.getState().pushCallStack({ nodeId: 'n1', timestamp: Date.now() });
    expect(useDebugStore.getState().callStack).toHaveLength(1);
    useDebugStore.getState().popCallStack();
    expect(useDebugStore.getState().callStack).toHaveLength(0);
  });

  it('should add debug events', () => {
    useDebugStore.getState().addEvent({
      type: 'node_enter',
      nodeId: 'n1',
      timestamp: Date.now(),
    });
    expect(useDebugStore.getState().events).toHaveLength(1);
  });

  it('should clear events', () => {
    useDebugStore.getState().addEvent({ type: 'node_enter', nodeId: 'n1', timestamp: Date.now() } as any);
    useDebugStore.getState().clearEvents();
    expect(useDebugStore.getState().events).toHaveLength(0);
  });

  it('should inspect a node', () => {
    useDebugStore.getState().inspectNode('n1');
    const events = useDebugStore.getState().events;
    expect(events.length).toBeGreaterThan(0);
    expect(events[events.length - 1]?.type).toBe('node_enter');
  });

  it('should export recording', () => {
    const id = useDebugStore.getState().createSession('run_1');
    const recording = useDebugStore.getState().exportRecording(id);
    expect(recording).toBeTruthy();
  });

  it('should set active session', () => {
    const id = useDebugStore.getState().createSession('run_1');
    useDebugStore.getState().setActiveSession(id);
    expect(useDebugStore.getState().activeSessionId).toBe(id);
  });
});
