// Atlas Workflow Studio - Inspector Panel
// Displays node properties in a read-only/editable form

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useWorkflowStore } from '../../stores';
import { useExecutionStore } from '../../stores';
import type { WorkflowGraphNode } from '../../stores/workflow-store';

export const PropertyInspector: React.FC = () => {
  const selectedNodeIds = useWorkflowStore((s) => s.selectedNodeIds);
  const nodes = useWorkflowStore((s: any) => s.nodes);
  const updateNode = useWorkflowStore((s) => s.updateNode);
  const activeRun = useExecutionStore((s) => s.activeRunId ? s.runs[s.activeRunId] : undefined);
  const nodeResults = useExecutionStore((s) => s.nodeResults);

  const selectedNode: WorkflowGraphNode | undefined = useMemo(() => {
    if (selectedNodeIds.length !== 1) return undefined;
    return nodes.find((n: any) => n.id === selectedNodeIds[0]);
  }, [selectedNodeIds, nodes]);
  const runtimeState = selectedNode ? activeRun?.nodeStates[selectedNode.id] : undefined;
  const runtimeResult = selectedNode ? nodeResults[selectedNode.id] : undefined;

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
          <EditablePropertyRow label="Label" value={selectedNode.label} onCommit={(label) => updateNode(selectedNode.id, { label })} />
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
          <PropertyRow label="State" value={runtimeState || selectedNode.executionState || 'pending'} />
          <EditablePropertyRow label="Priority" value={String(selectedNode.priority ?? 0)} type="number" onCommit={(value) => updateNode(selectedNode.id, { priority: Number(value) || 0 })} />
          <EditablePropertyRow label="Timeout" value={selectedNode.timeout ?? ''} placeholder="e.g. 30" onCommit={(timeout) => updateNode(selectedNode.id, { timeout: timeout || undefined })} />
          {selectedNode.statusMessage && <PropertyRow label="Status" value={selectedNode.statusMessage} />}
        </PropertySection>

        {/* Parameters */}
        <PropertySection title="Parameters">
            <button style={{ fontSize: 10, marginBottom: 4 }} onClick={() => {
              const value = prompt('Node parameters (JSON):', JSON.stringify(selectedNode.parameters, null, 2));
              if (value === null) return;
              try { useWorkflowStore.getState().updateNode(selectedNode.id, { parameters: JSON.parse(value) as Record<string, unknown> }); }
              catch { alert('Parameters must be valid JSON.'); }
            }}>Edit JSON</button>
            {selectedNode.type === 'vision_template_match' && (
              <TemplateImageEditor
                value={selectedNode.parameters.templateUrl}
                fileName={selectedNode.parameters.templateName}
                onCommit={(templateUrl, templateName) => updateNode(selectedNode.id, {
                  parameters: { ...selectedNode.parameters, templateUrl, templateName },
                })}
              />
            )}
            {Object.entries(selectedNode.parameters).filter(([key]) => (
              selectedNode.type !== 'vision_template_match' || (key !== 'templateUrl' && key !== 'templateName')
            )).map(([key, value]) => (
              <ParameterEditor key={key} label={key} value={value} onCommit={(next) => updateNode(selectedNode.id, { parameters: { ...selectedNode.parameters, [key]: next } })} />
            ))}
            {Object.keys(selectedNode.parameters).length === 0 && <div style={{ fontSize: 11, color: '#666' }}>No parameters</div>}
          </PropertySection>

        {runtimeResult && <PropertySection title="Runtime Result">
          <PropertyRow label="Duration" value={runtimeResult.duration_ms === undefined ? '—' : `${runtimeResult.duration_ms.toFixed(2)} ms`} />
          <PropertyRow label="Attempt" value={String(runtimeResult.attempt ?? 1)} />
          {runtimeResult.error && <PropertyRow label="Error" value={runtimeResult.error} />}
          <details><summary style={{ color: '#aaa', cursor: 'pointer' }}>Inputs</summary><pre style={{ whiteSpace: 'pre-wrap', fontSize: 10 }}>{JSON.stringify(runtimeResult.inputs ?? {}, null, 2)}</pre></details>
          <details><summary style={{ color: '#aaa', cursor: 'pointer' }}>Outputs</summary><pre style={{ whiteSpace: 'pre-wrap', fontSize: 10 }}>{JSON.stringify(runtimeResult.outputs ?? {}, null, 2)}</pre></details>
        </PropertySection>}

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

interface EditablePropertyRowProps {
  label: string;
  value: string;
  type?: 'text' | 'number';
  placeholder?: string;
  onCommit: (value: string) => void;
}

const fieldStyle: React.CSSProperties = {
  width: 150,
  minWidth: 0,
  height: 24,
  padding: '2px 5px',
  border: '1px solid #444',
  borderRadius: 2,
  background: '#1d1d1d',
  color: '#ddd',
  fontFamily: 'monospace',
  fontSize: 11,
};

export const EditablePropertyRow: React.FC<EditablePropertyRowProps> = ({ label, value, type = 'text', placeholder, onCommit }) => {
  const [draft, setDraft] = useState(value);
  useEffect(() => setDraft(value), [value]);
  const commit = () => { if (draft !== value) onCommit(draft); };
  return <label style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 8, padding: '3px 0', fontSize: 12 }}>
    <span style={{ color: '#999' }}>{label}:</span>
    <input
      aria-label={label}
      type={type}
      value={draft}
      placeholder={placeholder}
      onChange={(event) => setDraft(event.target.value)}
      onBlur={commit}
      onKeyDown={(event) => { if (event.key === 'Enter') event.currentTarget.blur(); }}
      style={fieldStyle}
    />
  </label>;
};

interface TemplateImageEditorProps {
  value: unknown;
  fileName: unknown;
  onCommit: (dataUrl: string, fileName: string) => void;
}

export const TemplateImageEditor: React.FC<TemplateImageEditorProps> = ({ value, fileName, onCommit }) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = useState('');
  const dataUrl = typeof value === 'string' ? value : '';
  const name = typeof fileName === 'string' ? fileName : '';

  const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    if (file.type !== 'image/png' && file.type !== 'image/jpeg') {
      setError('Choose a PNG or JPEG image.');
      return;
    }
    const reader = new FileReader();
    reader.onerror = () => setError('Could not read the selected image.');
    reader.onload = () => {
      if (typeof reader.result !== 'string') {
        setError('Could not read the selected image.');
        return;
      }
      setError('');
      onCommit(reader.result, file.name);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div style={{ padding: '4px 0 8px' }}>
      <div style={{ color: '#999', fontSize: 12, marginBottom: 5 }}>Template image:</div>
      {dataUrl ? (
        <div style={{ marginBottom: 6 }}>
          <img
            src={dataUrl}
            alt="Template preview"
            style={{ display: 'block', width: '100%', maxHeight: 120, objectFit: 'contain', background: '#181818', border: '1px solid #444', borderRadius: 3 }}
          />
          <div title={name} style={{ color: '#aaa', fontSize: 10, marginTop: 3, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {name || 'Selected image'}
          </div>
        </div>
      ) : (
        <div style={{ color: '#777', fontSize: 11, marginBottom: 6 }}>No image selected</div>
      )}
      <input ref={inputRef} aria-label="Template image file" type="file" accept="image/png,image/jpeg,.png,.jpg,.jpeg" onChange={selectFile} style={{ display: 'none' }} />
      <button type="button" style={{ fontSize: 10, marginRight: 6 }} onClick={() => inputRef.current?.click()}>
        {dataUrl ? 'Replace image' : 'Choose image'}
      </button>
      {dataUrl && <button type="button" style={{ fontSize: 10 }} onClick={() => { setError(''); onCommit('', ''); }}>Clear</button>}
      {error && <div role="alert" style={{ color: '#F44336', fontSize: 10, marginTop: 4 }}>{error}</div>}
    </div>
  );
};

interface ParameterEditorProps {
  label: string;
  value: unknown;
  onCommit: (value: unknown) => void;
}

const parameterText = (value: unknown): string => typeof value === 'string' ? value : JSON.stringify(value) ?? '';

export const ParameterEditor: React.FC<ParameterEditorProps> = ({ label, value, onCommit }) => {
  const [draft, setDraft] = useState(parameterText(value));
  const [error, setError] = useState(false);
  useEffect(() => { setDraft(parameterText(value)); setError(false); }, [value]);
  if (typeof value === 'boolean') {
    return <label style={{ display: 'flex', justifyContent: 'space-between', padding: '3px 0', fontSize: 12 }}>
      <span style={{ color: '#999' }}>{label}:</span>
      <input aria-label={label} type="checkbox" checked={value} onChange={(event) => onCommit(event.target.checked)} />
    </label>;
  }
  const structured = value !== null && typeof value === 'object';
  const commit = () => {
    try {
      const next = structured ? JSON.parse(draft) : typeof value === 'number' ? Number(draft) : draft;
      if (typeof next === 'number' && !Number.isFinite(next)) throw new Error('invalid number');
      setError(false);
      onCommit(next);
    } catch {
      setError(true);
    }
  };
  const common = {
    'aria-label': label,
    value: draft,
    onChange: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => setDraft(event.target.value),
    onBlur: commit,
    style: { ...fieldStyle, borderColor: error ? '#F44336' : '#444', height: structured ? 48 : 24 },
  };
  return <label style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8, padding: '3px 0', fontSize: 12 }}>
    <span style={{ color: error ? '#F44336' : '#999' }}>{label}:</span>
    {structured ? <textarea {...common} /> : <input {...common} type={typeof value === 'number' ? 'number' : 'text'} />}
  </label>;
};
