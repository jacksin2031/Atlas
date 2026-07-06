// Atlas Workflow Studio - Node Components Index
import { WorkflowNode } from './workflow-node';
import { EntryNode } from './entry-node';
import { ExitNode } from './exit-node';
import { CompositeNode } from './composite-node';

// Node type registry for React Flow
import type { Node } from '@xyflow/react';
import type { WorkflowGraphNode } from '../../stores/workflow-store';

export { WorkflowNode, EntryNode, ExitNode, CompositeNode };

export const NODE_TYPES = {
  workflow: WorkflowNode,
  entry: EntryNode,
  exit: ExitNode,
  composite: CompositeNode,
};

export type NodeTypeName = keyof typeof NODE_TYPES;

// Default node type mapping
export function getNodeTypeName(data: any): NodeTypeName {
  if (!data || typeof data !== 'object') return 'workflow';
  if (data.type === 'entry') return 'entry';
  if (data.type === 'exit') return 'exit';
  if (data.type === 'composite') return 'composite';
  return 'workflow';
}
