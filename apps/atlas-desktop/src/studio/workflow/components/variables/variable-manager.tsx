// Atlas Workflow Studio - Variable Manager Panel
// RFC-0302 §6, RFC-0307 compliant

import React, { useMemo } from 'react';
import { useVariableStore, useWorkflowStore } from '../../stores';
import type { VariableScope, DataType } from '../../types';

const SCOPE_LABELS: Record<VariableScope, string> = {
  workflow: 'Workflow',
  node: 'Node',
  subgraph: 'Sub-Graph',
  edge: 'Edge',
  environment: 'Environment',
  project: 'Project',
  global: 'Global',
  session: 'Session',
};

const TYPE_COLORS: Record<DataType, string> = {
  string: '#4FC3F7',
  integer: '#81C784',
  float: '#FFB74D',
  boolean: '#BA68C8',
  array: '#F06292',
  object: '#A1887F',
  null: '#666',
  duration: '#4DD0E1',
  timestamp: '#CE93D8',
};

export const VariableManager: React.FC = () => {
  const variables = useVariableStore((s: any) => s.variables);
  const addVariable = useVariableStore((s) => s.addVariable);
  const removeVariable = useVariableStore((s) => s.removeVariable);
  const setVariableValue = useVariableStore((s) => s.setVariableValue);
  const checkShadowing = useVariableStore((s) => s.checkShadowing);

  const shadows = useMemo(() => checkShadowing(), [checkShadowing]);
  const [filterScope, setFilterScope] = React.useState<VariableScope | 'all'>('all');

  const filtered = useMemo(
    () => (filterScope === 'all' ? variables : variables.filter((v: any) => v.scope === filterScope)),
    [variables, filterScope]
  );

  const handleAddVariable = () => {
    const name = prompt('Variable name:');
    if (!name) return;
    addVariable({
      name,
      type: 'string' as DataType,
      scope: 'workflow' as VariableScope,
      writable: true,
      description: '',
    });
  };

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
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>Variables</span>
        <button
          onClick={handleAddVariable}
          style={{
            background: '#0078d4',
            color: '#fff',
            border: 'none',
            borderRadius: 3,
            padding: '2px 8px',
            fontSize: 11,
            cursor: 'pointer',
          }}
          title="Add variable"
        >
          +
        </button>
      </div>

      {/* Shadow warnings */}
      {shadows.length > 0 && (
        <div style={{ padding: '4px 12px', backgroundColor: '#3a2a2a', fontSize: 10, color: '#F44336' }}>
          {shadows.map((s: any, i: number) => (
            <div key={i}>{s}</div>
          ))}
        </div>
      )}

      {/* Scope filter */}
      <div style={{ padding: '4px 8px', display: 'flex', flexWrap: 'wrap', gap: 2 }}>
        <button
          onClick={() => setFilterScope('all')}
          style={{
            fontSize: 10,
            padding: '1px 6px',
            border: '1px solid #444',
            borderRadius: 3,
            backgroundColor: filterScope === 'all' ? '#0078d4' : '#2d2d2d',
            color: '#ccc',
            cursor: 'pointer',
          }}
        >
          All
        </button>
        {Object.entries(SCOPE_LABELS).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setFilterScope(key as VariableScope)}
            style={{
              fontSize: 10,
              padding: '1px 6px',
              border: '1px solid #444',
              borderRadius: 3,
              backgroundColor: filterScope === key ? '#0078d4' : '#2d2d2d',
              color: '#ccc',
              cursor: 'pointer',
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Variable list */}
      {filtered.length === 0 ? (
        <div style={{ padding: 16, fontSize: 12, color: '#666', textAlign: 'center' }}>
          No variables declared
        </div>
      ) : (
        filtered.map((v: any) => (
          <div
            key={v.id}
            style={{
              padding: '4px 12px',
              fontSize: 11,
              color: '#ccc',
              borderBottom: '1px solid #2a2a2a',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                backgroundColor: (TYPE_COLORS as any)[v.type] || '#888',
                flexShrink: 0,
              }}
              title={v.type}
            />
            <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {v.name}
            </span>
            <span style={{ fontSize: 9, color: '#666' }}>{(SCOPE_LABELS as any)[v.scope] || v.scope}</span>
            {!v.writable && <span style={{ fontSize: 9, color: '#F44336' }}>RO</span>}
          </div>
        ))
      )}
    </div>
  );
};
