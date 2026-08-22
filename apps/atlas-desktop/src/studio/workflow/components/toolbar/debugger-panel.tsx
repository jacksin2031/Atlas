// Atlas Workflow Studio - Debugger Panel
// RFC-0316 compliant debug visualization

import React from 'react';
import { useDebugStore, useExecutionStore } from '../../stores';

export const DebuggerPanel: React.FC = () => {
  const breakpoints = useDebugStore((s: any) => s.breakpoints);
  const events = useDebugStore((s: any) => s.events);
  const currentNodeId = useDebugStore((s: any) => s.currentNodeId);
  const executionPath = useDebugStore((s: any) => s.executionPath);
  const callStack = useDebugStore((s: any) => s.callStack);
  const isAttached = useDebugStore((s: any) => s.isAttached);
  const activeRunId = useExecutionStore((s: any) => s.activeRunId);

  const addBreakpoint = useDebugStore((s: any) => s.addBreakpoint);
  const removeBreakpoint = useDebugStore((s: any) => s.removeBreakpoint);
  const toggleBreakpoint = useDebugStore((s: any) => s.toggleBreakpoint);
  const attach = useDebugStore((s: any) => s.attach);
  const detach = useDebugStore((s: any) => s.detach);
  const clearBreakpoints = useDebugStore((s: any) => s.clearBreakpoints);
  const clearEvents = useDebugStore((s: any) => s.clearEvents);

  const handleAddBreakpoint = () => {
    const nodeId = prompt('Node ID to breakpoint on:');
    if (!nodeId) return;
    addBreakpoint({ type: 'node', targetId: nodeId, condition: undefined } as any);
  };

  return (
    <div
      style={{
        width: 300,
        height: '100%',
        backgroundColor: '#1e1e1e',
        borderLeft: '1px solid #333',
        overflow: 'auto',
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        fontSize: 12,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '8px 12px',
          fontSize: 12,
          fontWeight: 600,
          color: '#aaa',
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          borderBottom: '1px solid #333',
          backgroundColor: '#2d2d2d',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>Debugger</span>
        <button
          onClick={isAttached ? detach : attach}
          style={{
            fontSize: 10,
            padding: '2px 8px',
            border: '1px solid #444',
            borderRadius: 3,
            backgroundColor: isAttached ? '#2E7D32' : '#2d2d2d',
            color: isAttached ? '#fff' : '#ccc',
            cursor: 'pointer',
          }}
        >
          {isAttached ? 'Detached' : 'Attach'}
        </button>
      </div>

      {/* Active run */}
      {activeRunId && (
        <div style={{ padding: '4px 12px', fontSize: 10, color: '#888', backgroundColor: '#252526' }}>
          Run: {activeRunId.slice(0, 16)}
        </div>
      )}

      {/* Current node */}
      <div style={{ padding: '6px 12px', borderBottom: '1px solid #2a2a2a' }}>
        <div style={{ fontSize: 10, color: '#666', marginBottom: 2 }}>Current Node</div>
        <div style={{ fontSize: 12, color: currentNodeId ? '#4FC3F7' : '#666', fontFamily: 'monospace' }}>
          {currentNodeId || '\u2014'}
        </div>
      </div>

      {/* Breakpoints */}
      <div style={{ padding: '6px 12px', borderBottom: '1px solid #2a2a2a' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
          <span style={{ fontSize: 10, color: '#666', textTransform: 'uppercase' }}>
            Breakpoints ({breakpoints.length})
          </span>
          <div style={{ display: 'flex', gap: 4 }}>
            <button onClick={handleAddBreakpoint} style={{ fontSize: 10, padding: '1px 4px', cursor: 'pointer', backgroundColor: '#0078d4', color: '#fff', border: 'none', borderRadius: 2 }}>+</button>
            <button onClick={clearBreakpoints} style={{ fontSize: 10, padding: '1px 4px', cursor: 'pointer', backgroundColor: '#444', color: '#ccc', border: 'none', borderRadius: 2 }}>Clear</button>
          </div>
        </div>
        {breakpoints.length === 0 ? (
          <div style={{ fontSize: 11, color: '#555' }}>No breakpoints</div>
        ) : (
          breakpoints.map((bp: any) => (
            <div
              key={bp.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 4,
                padding: '2px 0',
                fontSize: 11,
              }}
            >
              <button
                onClick={() => toggleBreakpoint(bp.id)}
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  backgroundColor: bp.enabled ? '#F44336' : '#444',
                  border: 'none',
                  cursor: 'pointer',
                  padding: 0,
                }}
              />
              <span style={{ flex: 1, color: '#ccc', fontFamily: 'monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {bp.targetId}
              </span>
              <span style={{ fontSize: 9, color: '#666' }}>H:{bp.hitCount}</span>
              <button
                onClick={() => removeBreakpoint(bp.id)}
                style={{ fontSize: 10, color: '#888', cursor: 'pointer', border: 'none', background: 'none', padding: 0 }}
              >
                \u00D7
              </button>
            </div>
          ))
        )}
      </div>

      {/* Execution path */}
      <div style={{ padding: '6px 12px', borderBottom: '1px solid #2a2a2a' }}>
        <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>
          Execution Path ({executionPath.length})
        </div>
        <div style={{ maxHeight: 100, overflow: 'auto', fontSize: 11, fontFamily: 'monospace', color: '#888' }}>
          {executionPath.map((id: any, i: number) => (
            <div key={i} style={{ padding: '1px 0' }}>
              {i + 1}. {id}
            </div>
          ))}
          {executionPath.length === 0 && <div style={{ color: '#444' }}>\u2014</div>}
        </div>
      </div>

      {/* Call stack */}
      <div style={{ padding: '6px 12px', borderBottom: '1px solid #2a2a2a' }}>
        <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>
          Call Stack ({callStack.length})
        </div>
        <div style={{ maxHeight: 80, overflow: 'auto', fontSize: 11, fontFamily: 'monospace', color: '#888' }}>
          {callStack.map((frame: any, i: number) => (
            <div key={i} style={{ padding: '1px 0' }}>
              #{i + 1} {frame.nodeId}{frame.functionName ? ` (${frame.functionName})` : ""}
            </div>
          ))}
          {callStack.length === 0 && <div style={{ color: '#444' }}>\u2014</div>}
        </div>
      </div>

      {/* Events */}
      <div style={{ padding: '6px 12px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
          <span style={{ fontSize: 10, color: '#666', textTransform: 'uppercase' }}>
            Events ({events.length})
          </span>
          <button onClick={clearEvents} style={{ fontSize: 10, padding: '1px 4px', cursor: 'pointer', backgroundColor: '#444', color: '#ccc', border: 'none', borderRadius: 2 }}>Clear</button>
        </div>
        <div style={{ maxHeight: 150, overflow: 'auto', fontSize: 11 }}>
          {events.slice(-30).reverse().map((evt: any) => (
            <div
              key={evt.id}
              style={{
                padding: '2px 0',
                borderBottom: '1px solid #1a1a1a',
                color: evt.type === 'error' ? '#F44336' : evt.type === 'breakpoint_hit' ? '#FFB74D' : '#888',
                fontFamily: 'monospace',
                fontSize: 10,
              }}
            >
              {evt.type}
              {evt.nodeId ? ` @ ${evt.nodeId}` : ""}
              {evt.variableName ? ` [${evt.variableName}]` : ""}
            </div>
          ))}
          {events.length === 0 && <div style={{ color: '#444' }}>No events</div>}
        </div>
      </div>
    </div>
  );
};
