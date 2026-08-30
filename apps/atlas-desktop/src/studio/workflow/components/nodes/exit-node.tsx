// Atlas Workflow Studio - Exit Node
import { Handle, Position } from '@xyflow/react';

const stateColor = (state?: string): string => state === 'running' ? '#2196F3' : state === 'failed' ? '#F44336' : state === 'skipped' ? '#666' : '#4CAF50';
export const ExitNode = ({ data, selected }: any) => (
  <div style={{
    backgroundColor: selected ? '#4a1a1a' : '#3a1a1a',
    border: `2px solid ${stateColor(data.executionState)}`,
    borderRadius: 20,
    padding: '10px 24px',
    color: '#e0e0e0',
    fontSize: 13,
    fontWeight: 600,
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    textAlign: 'center',
    whiteSpace: 'nowrap',
  }}>
    <Handle
      type="target"
      position={Position.Left}
      id={data.inputs?.[0]?.id || 'input'}
      style={{ left: -6, width: 10, height: 10, backgroundColor: '#0078d4', border: '1px solid #fff' }}
    />
    ■ {data.label || 'Exit'} {data.executionState && <small>· {data.executionState}</small>}
  </div>
);
