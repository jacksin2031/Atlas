// Atlas Desktop — Property Inspector Sidebar

import React from 'react';
import { useWorkflowStore } from '../../studio/workflow/stores';
import { useThemeStore } from '../../stores';

export const InspectorPanel: React.FC = () => {
  const resolvedTheme = useThemeStore((s) => s.resolvedTheme);

  // Access selection directly from store state
  const selection = useWorkflowStore((s) => s.selection);
  const nodes = useWorkflowStore((s) => s.nodes);

  const selectedNodeIds = Array.from(selection.selectedNodeIds);
  const selectedNode = selectedNodeIds.length === 1 ? nodes.find((n) => n.id === selectedNodeIds[0]) : null;

  return (
    <div
      style={{
        width: 280,
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: resolvedTheme === 'dark' ? '#252526' : '#fff',
        borderLeft: '1px solid ' + (resolvedTheme === 'dark' ? '#333' : '#ddd'),
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          padding: '8px 12px',
          fontSize: 12,
          fontWeight: 600,
          color: '#aaa',
          textTransform: 'uppercase',
          letterSpacing: 0.5,
          borderBottom: '1px solid ' + (resolvedTheme === 'dark' ? '#333' : '#ddd'),
          backgroundColor: resolvedTheme === 'dark' ? '#2d2d2d' : '#f5f5f5',
        }}
      >
        PROPERTIES
      </div>

      <div style={{ flex: 1, overflow: 'auto', padding: 12 }}>
        {selectedNode ? (
          <div style={{ fontSize: 12 }}>
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Name</div>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#e0e0e0' }}>{selectedNode.label}</div>
            </div>

            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Type</div>
              <div style={{ fontSize: 12, color: '#ccc', fontFamily: 'monospace' }}>{selectedNode.type}</div>
            </div>

            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Category</div>
              <div style={{ fontSize: 12, color: '#ccc' }}>{selectedNode.category}</div>
            </div>

            {selectedNode.description && (
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Description</div>
                <div style={{ fontSize: 12, color: '#bbb', lineHeight: 1.5 }}>{selectedNode.description}</div>
              </div>
            )}

            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>
                Inputs ({selectedNode.inputs.length})
              </div>
              {selectedNode.inputs.map((inp) => (
                <div key={inp.id} style={{ padding: '2px 0', fontSize: 11, color: '#ccc' }}>
                  {inp.name} <span style={{ color: '#666', fontSize: 10 }}>({inp.type})</span>
                </div>
              ))}
            </div>

            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>
                Outputs ({selectedNode.outputs.length})
              </div>
              {selectedNode.outputs.map((out) => (
                <div key={out.id} style={{ padding: '2px 0', fontSize: 11, color: '#ccc' }}>
                  {out.name} <span style={{ color: '#666', fontSize: 10 }}>({out.type})</span>
                </div>
              ))}
            </div>

            {Object.keys(selectedNode.parameters).length > 0 && (
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Parameters</div>
                {Object.entries(selectedNode.parameters).map(([key, value]) => (
                  <div key={key} style={{ padding: '2px 0', fontSize: 11, color: '#ccc' }}>
                    {key}: <span style={{ fontFamily: 'monospace', color: '#888' }}>{String(value)}</span>
                  </div>
                ))}
              </div>
            )}

            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Execution</div>
              <div style={{ padding: '2px 0', fontSize: 11, color: '#ccc' }}>
                State: <span style={{ color: selectedNode.executionState === 'running' ? '#4CAF50' : '#888' }}>{selectedNode.executionState || 'pending'}</span>
              </div>
              {selectedNode.priority !== undefined && selectedNode.priority !== 0 && (
                <div style={{ padding: '2px 0', fontSize: 11, color: '#ccc' }}>
                  Priority: {selectedNode.priority}
                </div>
              )}
            </div>

            {selectedNode.capabilities && selectedNode.capabilities.length > 0 && (
              <div>
                <div style={{ fontSize: 10, color: '#666', textTransform: 'uppercase', marginBottom: 4 }}>Capabilities</div>
                {selectedNode.capabilities.map((cap) => (
                  <div key={cap} style={{ padding: '1px 0', fontSize: 10, color: '#888' }}>• {cap}</div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div style={{ fontSize: 12, color: '#666', textAlign: 'center', paddingTop: 40 }}>
            {selectedNodeIds.length === 0
              ? 'Select a node to view properties'
              : selectedNodeIds.length > 1
                ? 'Select a single node'
                : 'Node not found'}
          </div>
        )}
      </div>
    </div>
  );
};
