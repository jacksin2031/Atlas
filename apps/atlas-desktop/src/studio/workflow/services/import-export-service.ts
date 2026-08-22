// Atlas Workflow Studio - Import/Export Service
// RFC-0328 compliant serialization

import { parse as parseYAML, stringify as stringifyYAML } from 'yaml';
import type {
  WorkflowDefinition,
  SerializationFormat,
  ImportExportResult,
  ValidationResult,
} from '../types';

export interface ImportExportService {
  serialize(def: WorkflowDefinition, format: SerializationFormat): Promise<string>;
  deserialize(data: string, format: SerializationFormat): Promise<ImportExportResult>;
  exportJSON(def: WorkflowDefinition): Promise<string>;
  exportYAML(def: WorkflowDefinition): Promise<string>;
  importJSON(data: string): Promise<ImportExportResult>;
  importYAML(data: string): Promise<ImportExportResult>;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function validateWorkflow(value: unknown): {
  workflow?: WorkflowDefinition;
  errors: ValidationResult[];
  version: string;
} {
  if (!isRecord(value)) {
    return {
      errors: [{
        rule: 'invalid_workflow',
        severity: 'error',
        message: 'Workflow must be an object',
        location: 'workflow',
      }],
      version: '0.0.0',
    };
  }

  const errors: ValidationResult[] = [];
  const requireString = (key: 'id' | 'name' | 'version') => {
    if (typeof value[key] !== 'string' || value[key].trim() === '') {
      errors.push({
        rule: 'required_field',
        severity: 'error',
        message: `Workflow field "${key}" must be a non-empty string`,
        location: 'workflow',
      });
    }
  };

  requireString('id');
  requireString('name');
  requireString('version');

  for (const key of ['nodes', 'edges', 'variables'] as const) {
    if (!Array.isArray(value[key])) {
      errors.push({
        rule: 'required_field',
        severity: 'error',
        message: `Workflow field "${key}" must be an array`,
        location: 'workflow',
      });
    }
  }

  if (!isRecord(value.parameters)) {
    errors.push({
      rule: 'required_field',
      severity: 'error',
      message: 'Workflow field "parameters" must be an object',
      location: 'workflow',
    });
  }

  if (
    !isRecord(value.metadata)
    || typeof value.metadata.createdAt !== 'number'
    || typeof value.metadata.updatedAt !== 'number'
  ) {
    errors.push({
      rule: 'invalid_metadata',
      severity: 'error',
      message: 'Workflow metadata must contain numeric createdAt and updatedAt values',
      location: 'workflow',
    });
  }

  if (Array.isArray(value.nodes)) {
    value.nodes.forEach((node, index) => {
      if (
        !isRecord(node)
        || typeof node.id !== 'string'
        || typeof node.type !== 'string'
        || !Array.isArray(node.inputs)
        || !Array.isArray(node.outputs)
        || !isRecord(node.parameters)
      ) {
        errors.push({
          rule: 'invalid_node',
          severity: 'error',
          message: `Workflow node at index ${index} is invalid`,
          location: 'node',
          nodeId: isRecord(node) && typeof node.id === 'string' ? node.id : undefined,
        });
      }
    });
  }

  if (Array.isArray(value.edges)) {
    value.edges.forEach((edge, index) => {
      if (
        !isRecord(edge)
        || typeof edge.id !== 'string'
        || typeof edge.source !== 'string'
        || typeof edge.target !== 'string'
      ) {
        errors.push({
          rule: 'invalid_edge',
          severity: 'error',
          message: `Workflow edge at index ${index} is invalid`,
          location: 'edge',
        });
      }
    });
  }

  if (errors.length > 0) {
    return {
      errors,
      version: typeof value.version === 'string' ? value.version : '0.0.0',
    };
  }

  return {
    workflow: value as unknown as WorkflowDefinition,
    errors: [],
    version: value.version as string,
  };
}

export class ImportExportServiceImpl implements ImportExportService {
  async serialize(def: WorkflowDefinition, format: SerializationFormat): Promise<string> {
    if (format === 'json') {
      return this.exportJSON(def);
    }
    if (format === 'yaml') {
      return this.exportYAML(def);
    }
    throw new Error(`Unsupported format: ${format}`);
  }

  async deserialize(data: string, format: SerializationFormat): Promise<ImportExportResult> {
    if (format !== 'json' && format !== 'yaml') {
      return {
        success: false,
        errors: [{
          rule: 'unsupported_format',
          severity: 'error',
          message: `Unsupported format: ${format}`,
          location: 'workflow',
        }],
        format,
        version: '0.0.0',
      };
    }

    try {
      const parsed: unknown = format === 'json' ? JSON.parse(data) : parseYAML(data);
      const result = validateWorkflow(parsed);
      return {
        success: result.errors.length === 0,
        workflow: result.workflow,
        errors: result.errors,
        format,
        version: result.version,
      };
    } catch (error: unknown) {
      return {
        success: false,
        errors: [{
          rule: 'parse_error',
          severity: 'error',
          message: `Failed to parse: ${String(error)}`,
          location: 'workflow',
        }],
        format,
        version: '0.0.0',
      };
    }
  }

  async exportJSON(def: WorkflowDefinition): Promise<string> {
    return JSON.stringify(def, null, 2);
  }

  async exportYAML(def: WorkflowDefinition): Promise<string> {
    return stringifyYAML(def);
  }

  async importJSON(data: string): Promise<ImportExportResult> {
    return this.deserialize(data, 'json');
  }

  async importYAML(data: string): Promise<ImportExportResult> {
    return this.deserialize(data, 'yaml');
  }
}

export const importExportService = new ImportExportServiceImpl();

