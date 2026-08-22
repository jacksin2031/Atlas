// Atlas Workflow Studio - Composite Node (sub-graph)
export const CompositeNode = ({ data, selected }: any) => (
  <div style={{
    backgroundColor: selected ? '#3a3a5a' : '#2a2a4a',
    border: '2px dashed #9C27B0',
    borderRadius: 8,
    padding: 12,
    color: '#e0e0e0',
    fontFamily: "'Segoe UI', system-ui, sans-serif",
    minWidth: 160,
  }}>
    <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 4 }}>
      ⊞ {data.label || 'Sub-Graph'}
    </div>
    <div style={{ fontSize: 10, color: '#888' }}>{data.description || 'Nested workflow'}</div>
  </div>
);
