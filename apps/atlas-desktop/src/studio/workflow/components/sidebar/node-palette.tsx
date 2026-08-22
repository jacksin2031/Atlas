// Atlas Workflow Studio - Node Palette Sidebar
// Draggable node categories for drag-and-drop onto canvas

import React, { useMemo } from 'react';
import { useNodeRegistryStore } from '../../stores';
import { NODE_CATEGORIES, NODE_CATEGORY_LABELS } from '../../types/node-categories';
import { Icon, type IconName } from '../../../../design-system';
import type { PluginNodeRegistration } from '../../types';
import type { NodeCategory } from '../../types/node-categories';

export const NodePalette: React.FC = () => {
  const builtinNodes = useNodeRegistryStore((s) => s.builtinNodes);
  const registrations = useNodeRegistryStore((s) => s.registrations);

  const categorizedNodes = useMemo(() => {
    const seen = new Set<string>();
    const allNodes = [...builtinNodes, ...registrations.values()].filter((node) => !seen.has(node.typeName) && Boolean(seen.add(node.typeName)));
    const groups: Record<string, PluginNodeRegistration[]> = {} as any;
    for (const cat of Object.values(NODE_CATEGORIES) as NodeCategory[]) {
      groups[cat] = [];
    }
    for (const node of allNodes) {
      const cat = node.category as string;
      if (groups[cat]) {
        groups[cat].push(node);
      }
    }
    return groups;
  }, [builtinNodes, registrations]);

  const handleDragStart = (node: PluginNodeRegistration, e: React.DragEvent) => {
    e.dataTransfer.setData(
      'application/x-atlas-node',
      JSON.stringify({
        typeName: node.typeName,
        label: node.label,
        category: node.category,
        inputs: node.inputs.map((i) => ({ name: i.name, type: i.type })),
        outputs: node.outputs.map((o) => ({ name: o.name, type: o.type })),
      })
    );
    e.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div
      style={{
        width: 240,
        height: '100%',
        backgroundColor: '#252526',
        borderRight: '1px solid #333',
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
        }}
      >
        Node Palette
      </div>

      {Object.entries(NODE_CATEGORIES)
        .filter(([, cat]) => (categorizedNodes as any)[cat]?.length > 0)
        .map(([, cat]) => (
          <div key={cat} style={{ borderBottom: '1px solid #333' }}>
            <div
              style={{
                padding: '6px 12px',
                fontSize: 11,
                fontWeight: 600,
                color: '#888',
                textTransform: 'uppercase',
                letterSpacing: 0.5,
                backgroundColor: '#2d2d2d',
              }}
            >
              <span style={{display:'inline-flex',verticalAlign:'middle',marginRight:5}}><Icon name={categoryIcon(cat)} size={12}/></span>{NODE_CATEGORY_LABELS[cat]}
            </div>
            {(categorizedNodes[cat] ?? []).map((node) => (
              <div
                key={node.nodeId}
                draggable
                onDragStart={(e) => handleDragStart(node, e)}
                style={{
                  padding: '4px 12px 4px 24px',
                  fontSize: 12,
                  color: '#ccc',
                  cursor: 'grab',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  userSelect: 'none',
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = '#2a2d2e';
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent';
                }}
                title={node.description || node.label}
              >
                <span style={{ fontSize: 10, color: '#666', display:'inline-flex' }}><Icon name={categoryIcon(node.category)} size={11}/></span>
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {node.label}
                </span>
              </div>
            ))}
          </div>
        ))}
    </div>
  );
};

const categoryIcon = (category: NodeCategory): IconName => category === 'vision' ? 'vision' : category === 'file' || category === 'project' ? 'folder' : category === 'ai' ? 'detect' : 'workflow';
