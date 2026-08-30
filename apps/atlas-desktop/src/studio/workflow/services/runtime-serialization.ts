import type { WorkflowDefinition } from "../types";

export interface CanonicalWorkflowManifest {
  name: string;
  version: string;
  metadata: Record<string, unknown>;
  nodes: Array<Record<string, unknown>>;
  edges: Array<Record<string, unknown>>;
  variables: Array<Record<string, unknown>>;
  entry_nodes: string[];
  exit_nodes: string[];
  capabilities: Array<{ name: string; minimum_version: string }>;
  plugins: string[];
}

const unique = (values: Array<string | undefined>): string[] =>
  [...new Set(values.filter((value): value is string => Boolean(value)))].sort();

/** Maps the editable Studio model onto the existing WorkflowManifest schema. */
export function serializeWorkflowForRuntime(definition: WorkflowDefinition): CanonicalWorkflowManifest {
  const capabilities = unique([
    ...(definition.requiredCapabilities ?? []),
    ...definition.nodes.flatMap((node) => node.capabilities ?? []),
  ]);
  const plugins = unique([
    ...(definition.requiredPlugins ?? []),
    ...definition.nodes.flatMap((node) => node.requiredPlugins ?? []),
    ...definition.nodes.map((node) => node.pluginId === "builtin" ? undefined : node.pluginId),
  ]);
  return {
    name: definition.id || definition.name,
    version: definition.version,
    metadata: {
      name: definition.id || definition.name,
      version: definition.version,
      description: definition.description ?? "",
      tags: definition.metadata.tags ?? [],
      display_name: definition.name,
      project_id: definition.projectId,
    },
    nodes: definition.nodes.map((node) => ({
      id: node.id,
      type: node.type,
      label: node.label,
      config: node.parameters,
      inputs: node.inputs.map((port) => port.name),
      outputs: node.outputs.map((port) => port.name),
      ports_in: node.inputs.map((port) => port.id),
      ports_out: node.outputs.map((port) => port.id),
      timeout_seconds: node.timeout ? Number.parseFloat(node.timeout) : undefined,
      retry_policy: node.retryPolicy ? {
        max_retries: node.retryPolicy.maxRetries,
        backoff_strategy: node.retryPolicy.backoffStrategy,
      } : undefined,
      metadata: {
        category: node.category,
        capabilities: node.capabilities ?? [],
        plugin_id: node.pluginId,
        input_ports: Object.fromEntries(node.inputs.map((port) => [port.id, port.name])),
        output_ports: Object.fromEntries(node.outputs.map((port) => [port.id, port.name])),
        input_port_types: Object.fromEntries(node.inputs.map((port) => [port.id, port.type])),
        output_port_types: Object.fromEntries(node.outputs.map((port) => [port.id, port.type])),
        input_defaults: Object.fromEntries(node.inputs.filter((port) => port.defaultValue !== undefined).map((port) => [port.name, port.defaultValue])),
      },
    })),
    edges: definition.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      source_port: edge.sourcePort ?? "",
      target_port: edge.targetPort ?? "",
      condition: edge.condition ?? "",
      metadata: { edge_type: edge.edgeType, cardinality: edge.cardinality },
    })),
    variables: definition.variables.map((variable) => ({
      name: variable.name,
      type: variable.type,
      scope: variable.scope,
      default: variable.value ?? variable.defaultValue,
      description: variable.description ?? "",
    })),
    entry_nodes: definition.nodes.filter((node) => node.type === "entry").map((node) => node.id),
    exit_nodes: definition.nodes.filter((node) => node.type === "exit").map((node) => node.id),
    capabilities: capabilities.map((name) => ({ name, minimum_version: "1.0.0" })),
    plugins,
  };
}
