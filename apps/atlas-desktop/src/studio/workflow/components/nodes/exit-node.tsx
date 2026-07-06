// Atlas Workflow Studio - Exit Node
export const ExitNode = ({ data, selected }: any) => (
  <div style={{
    backgroundColor: selected ? '#4a1a1a' : '#3a1a1a',
    border: '2px solid #4CAF50',
    borderRadius: 20,
    padding: '10px 24px',
    color: '#e0e0e0',
    fontSize: 13,
    fontWeight: 600,
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    textAlign: 'center',
    whiteSpace: 'nowrap',
  }}>
    ■ {data.label || 'Exit'}
  </div>
);
