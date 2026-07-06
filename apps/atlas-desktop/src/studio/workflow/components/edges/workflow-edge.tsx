// Atlas Workflow Studio - Custom Edge Components
// RFC-0302 §5.3 compliant edge types

import React, { memo } from 'react';
import { type EdgeProps, getSmoothStepPath } from '@xyflow/react';

const EDGE_STYLES: Record<string, { stroke: string; strokeWidth: number; dasharray?: string }> = {
  data: { stroke: '#4FC3F7', strokeWidth: 2 },
  control: { stroke: '#81C784', strokeWidth: 2 },
  condition: { stroke: '#FFB74D', strokeWidth: 2, dasharray: '6 3' },
  event: { stroke: '#BA68C8', strokeWidth: 2, dasharray: '3 3' },
  resource: { stroke: '#F06292', strokeWidth: 2 },
  signal: { stroke: '#A1887F', strokeWidth: 2, dasharray: '8 4' },
};

export const WorkflowEdge = memo(({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
}: EdgeProps & { data?: { edgeType?: string } }) => {
  const edgeType = data?.edgeType || 'data';
  const edgeStyle = EDGE_STYLES[edgeType] ?? EDGE_STYLES.data;
  const [edgePath] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  return (
    <>
      <path
        id={id}
        d={edgePath}
        fill="none"
        stroke={edgeStyle!.stroke}
        strokeWidth={edgeStyle!.strokeWidth}
        strokeDasharray={edgeStyle!.dasharray}
        style={{ transition: 'stroke 0.2s', stroke: edgeStyle!.stroke, strokeWidth: edgeStyle!.strokeWidth, ...(edgeStyle!.dasharray ? { strokeDasharray: edgeStyle!.dasharray } : {}) }}
      />
    </>
  );
});

WorkflowEdge.displayName = 'WorkflowEdge';

export const EDGE_TYPES = {
  data: WorkflowEdge,
  control: WorkflowEdge,
  condition: WorkflowEdge,
  event: WorkflowEdge,
  resource: WorkflowEdge,
  signal: WorkflowEdge,
};
