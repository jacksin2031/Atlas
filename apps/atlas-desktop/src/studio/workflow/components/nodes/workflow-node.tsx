// Atlas Workflow Studio - Custom Node Component
// Renders workflow nodes with inputs, outputs, status indicators

import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { NODE_CATEGORY_ICONS } from '../../types/node-categories';

const STATUS_COLORS = {
  pending: '#888888',
  ready: '#4CAF50',
  running: '#2196F3',
  waiting: '#FF9800',
  completed: '#4CAF50',
  failed: '#F44336',
  cancelled: '#9E9E9E',
  skipped: '#666666',
  paused: '#FF9800',
  compensated: '#9C27B0',
} as const;

const VALIDATION_COLORS = {
  valid: '#4CAF50',
  invalid: '#F44336',
  unchecked: '#888888',
} as const;

const CATEGORY_STYLES: Record<string, { accent: string; surface: string; header: string }> = {
  core: { accent: '#4CAF50', surface: '#202d22', header: '#2c4430' },
  logic: { accent: '#FF9800', surface: '#30271b', header: '#49351f' },
  flow: { accent: '#FFC107', surface: '#302c18', header: '#4b431d' },
  math: { accent: '#AB47BC', surface: '#2c2030', header: '#452d4b' },
  string: { accent: '#EC407A', surface: '#321e29', header: '#512c3c' },
  collection: { accent: '#26A69A', surface: '#1c2d2c', header: '#2a4845' },
  datetime: { accent: '#42A5F5', surface: '#1d2935', header: '#2b4259' },
  file: { accent: '#8D6E63', surface: '#2c2521', header: '#463831' },
  system: { accent: '#78909C', surface: '#222b2f', header: '#34434a' },
  ipc: { accent: '#90A4AE', surface: '#222a2d', header: '#3a484e' },
  input: { accent: '#26C6DA', surface: '#182c30', header: '#20505a' },
  vision: { accent: '#00BCD4', surface: '#182d31', header: '#20515a' },
  ai: { accent: '#7C4DFF', surface: '#241d38', header: '#3b2d62' },
  knowledge: { accent: '#5C6BC0', surface: '#20243a', header: '#303a66' },
  project: { accent: '#29B6F6', surface: '#1b2935', header: '#27506a' },
  storage: { accent: '#66BB6A', surface: '#202d22', header: '#315636' },
};

export const WorkflowNode = memo(({ data, selected }: any) => {
  const {
    label,
    description,
    category,
    inputs = [],
    outputs = [],
    executionState,
    validationState,
    icon,
  } = data;

  const statusColor = executionState && STATUS_COLORS[executionState as keyof typeof STATUS_COLORS] ? STATUS_COLORS[executionState as keyof typeof STATUS_COLORS] : STATUS_COLORS.pending;
  const validationColor = validationState && VALIDATION_COLORS[validationState as keyof typeof VALIDATION_COLORS] ? VALIDATION_COLORS[validationState as keyof typeof VALIDATION_COLORS] : VALIDATION_COLORS.unchecked;
  const catIcon = (NODE_CATEGORY_ICONS as unknown as Record<string, string>)[category] || '\u2699';
  const categoryStyle = CATEGORY_STYLES[category] ?? CATEGORY_STYLES.core!;

  return (
    <div
      style={{
        backgroundColor: selected ? '#37373d' : categoryStyle.surface,
        border: `2px solid ${categoryStyle.accent}`,
        borderRadius: 6,
        minWidth: 180,
        maxWidth: 260,
        padding: 0,
        boxShadow: selected ? '0 0 0 2px rgba(0,120,212,0.4)' : '0 2px 4px rgba(0,0,0,0.3)',
        color: '#e0e0e0',
        fontFamily: "'Segoe UI', system-ui, sans-serif",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '8px 10px',
          borderBottom: '1px solid #444',
          backgroundColor: categoryStyle.header,
          borderRadius: '6px 6px 0 0',
        }}
      >
        {/* Status dot */}
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            backgroundColor: statusColor,
            flexShrink: 0,
          }}
          title={executionState || 'pending'}
        />
        {/* Validation dot */}
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            backgroundColor: validationColor,
            flexShrink: 0,
          }}
          title={validationState || 'unchecked'}
        />
        {/* Icon + Label */}
        <span style={{ fontSize: 14, fontWeight: 600, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {icon ? <>{icon} </> : null}{catIcon} {label}
        </span>
      </div>

      {/* Description */}
      {description && (
        <div style={{ padding: '4px 10px', fontSize: 11, color: '#999', borderBottom: '1px solid #3a3a3a' }}>
          {description}
        </div>
      )}

      {/* Category badge */}
      <div style={{ padding: '2px 10px', fontSize: 10, color: categoryStyle.accent, textTransform: 'uppercase', letterSpacing: 0.5 }}>
        {category}
      </div>

      {/* Input handles */}
      <div style={{ padding: '4px 0' }}>
        {inputs.map((input: any) => (
          <div key={input.id} style={{ display: 'flex', alignItems: 'center', padding: '2px 10px', fontSize: 11 }}>
            <Handle
              type="target"
              position={Position.Left}
              id={input.id}
              style={{ left: 0, width: 10, height: 10, backgroundColor: categoryStyle.accent, border: '1px solid #fff' }}
            />
            <span style={{ marginLeft: 14, color: '#bbb' }}>{input.name}</span>
            <span style={{ marginLeft: 'auto', fontSize: 9, color: '#666' }}>{input.type}</span>
          </div>
        ))}
      </div>

      {/* Output handles */}
      <div style={{ padding: '4px 0' }}>
        {outputs.map((output: any) => (
          <div key={output.id} style={{ display: 'flex', alignItems: 'center', padding: '2px 10px', fontSize: 11 }}>
            <span style={{ marginRight: 'auto', color: '#bbb' }}>{output.name}</span>
            <span style={{ marginRight: 8, fontSize: 9, color: '#666' }}>{output.type}</span>
            <Handle
              type="source"
              position={Position.Right}
              id={output.id}
              style={{ right: 0, width: 10, height: 10, backgroundColor: categoryStyle.accent, border: '1px solid #fff' }}
            />
          </div>
        ))}
      </div>
    </div>
  );
});

WorkflowNode.displayName = 'WorkflowNode';
