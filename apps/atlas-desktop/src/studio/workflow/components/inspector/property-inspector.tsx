// Atlas Workflow Studio - Inspector Panel
// Displays node properties in a read-only/editable form

import React, { useMemo } from 'react';
import { useWorkflowStore } from '../../stores';
import type { WorkflowGraphNode } from '../../stores/workflow-store';

export const PropertyInspector: React.FC = () => {
  const selectedNodeIds = useWorkflowStore((s: any) => Array.from(s.selection.selectedNodeIds));
  const nodes = useWorkflowStore((s: any) => s.nodes);

  const selectedNode: WorkflowGraphNode | undefined = useMemo(() => {
    if (selectedNodeIds.length !== 1) return undefined;
    return nodes.find((n: any) => n.id === selectedNodeIds[0]);
  }, [selectedNodeIds, nodes]);

  if (!selectedNode) {
    return (
      <div
        style={{
          width: 280,
          height: '100%',
          backgroundColor: '#252526',
          borderLeft: '1px solid #333',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#666',
          fontSize: 12,
          fontFamily: "'Segoe UI', system-ui, sans-serif",
        }}
      >
        {selectedNodeIds.length === 0
          ? 'Select a node to inspect properties'
          : selectedNodeIds.length > 1
          ? `Selected: ${selectedNodeIds.length} nodes`
          : selectedNodeIds.length === 1 && selectedNode
          ? ''
          : 'Node not found'}
        </div>
    );
  }

  return (
    <div
      style={{
        width: 280,
        height: '100%',
        backgroundColor: '#252526',
        borderLeft: '1px solid #333',
        overflow: 'auto',
        fontFamily: "'Segoe UI', system-ui, sans-serif",
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
          borderBottom: '1px solid #333',
          backgroundColor: '#2d2d2d',
        }}
      >
        Properties
      </div>

      <div style={{ padding: 12 }}>
        {/* Node Info */}
        <PropertySection title="Node">
          <PropertyRow label="ID" value={selectedNode.id} />
          <PropertyRow label="Label" value={selectedNode.label} />
          <PropertyRow label="Type" value={selectedNode.type} />
          <PropertyRow label="Category" value={selectedNode.category} />
        </PropertySection>

        {/* Description */}
        {selectedNode.description && (
          <PropertySection title="Description">
            <div style={{ fontSize: 12, color: '#bbb', lineHeight: 1.5 }}>{selectedNode.description}</div>
          </PropertySection>
        )}

        {/* Inputs */}
        <PropertySection title={`Inputs (${selectedNode.inputs.length})`}>
          {selectedNode.inputs.map((inp: any) => (
            <PropertyRow key={inp.id} label={inp.name} value={inp.type} />
          ))}
        </PropertySection>

        {/* Outputs */}
        <PropertySection title={`Outputs (${selectedNode.outputs.length})`}>
          {selectedNode.outputs.map((out: any) => (
            <PropertyRow key={out.id} label={out.name} value={out.type} />
          ))}
        </PropertySection>

        {/* Execution State */}
        <PropertySection title="Execution">
          <PropertyRow label="State" value={selectedNode.executionState || 'pending'} />
          <PropertyRow label="Priority" value={selectedNode.priority?.toString() || '0'} />
          {selectedNode.timeout && <PropertyRow label="Timeout" value={selectedNode.timeout} />}
          {selectedNode.statusMessage && <PropertyRow label="Status" value={selectedNode.statusMessage} />}
        </PropertySection>

        {/* Parameters */}
        {Object.keys(selectedNode.parameters).length > 0 && (
          <PropertySection title="Parameters">
            {Object.entries(selectedNode.parameters).map(([key, value]) => (
              <PropertyRow key={key} label={key} value={String(value)} />
            ))}
          </PropertySection>
        )}

        {/* Capabilities */}
        {selectedNode.capabilities && selectedNode.capabilities.length > 0 && (
          <PropertySection title="Capabilities">
            {selectedNode.capabilities.map((cap: any) => (
              <div key={cap} style={{ fontSize: 11, color: '#888', padding: '2px 0' }}>• {cap}</div>
            ))}
          </PropertySection>
        )}

        {/* Documentation */}
        {selectedNode.documentationUrl && (
          <PropertySection title="Documentation">
            <a
              href={selectedNode.documentationUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{ fontSize: 11, color: '#4FC3F7', textDecoration: 'underline' }}
            >
              View Documentation
            </a>
          </PropertySection>
        )}
      </div>
    </div>
  );
};

interface PropertySectionProps {
  title: string;
  children: React.ReactNode;
}

const PropertySection: React.FC<PropertySectionProps> = ({ title, children }) => (
  <div style={{ marginBottom: 12 }}>
    <div
      style={{
        fontSize: 11,
        fontWeight: 600,
        color: '#888',
        textTransform: 'uppercase',
        letterSpacing: 0.5,
        marginBottom: 4,
      }}
    >
      {title}
    </div>
    {children}
  </div>
);

interface PropertyRowProps {
  label: string;
  value: string;
}

const PropertyRow: React.FC<PropertyRowProps> = ({ label, value }) => (
  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0', fontSize: 12 }}>
    <span style={{ color: '#999' }}>{label}:</span>
    <span style={{ color: '#ddd', fontFamily: 'monospace', fontSize: 11 }}>{value}</span>
  </div>
);
