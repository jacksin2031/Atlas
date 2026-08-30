// Atlas Workflow Studio - Entry Node
import { Handle, Position } from '@xyflow/react';

const stateColor = (state?: string): string => state === 'running' ? '#2196F3' : state === 'failed' ? '#F44336' : state === 'skipped' ? '#666' : '#4CAF50';
export const EntryNode = ({ data, selected }: any) => (
  <div style={{
    backgroundColor: selected ? '#1a4a1a' : '#1a3a1a',
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
      type="source"
      position={Position.Right}
      id={data.outputs?.[0]?.id || 'output'}
      style={{ right: -6, width: 10, height: 10, backgroundColor: '#0078d4', border: '1px solid #fff' }}
    />
    ▶ {data.label || 'Entry'} {data.executionState && <small>· {data.executionState}</small>}
  </div>
);
