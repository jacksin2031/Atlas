// Atlas Workflow Studio - Import/Export Service
// RFC-0328 compliant serialization

import type {
  WorkflowDefinition,
  SerializationFormat,
  ImportExportResult,
} from '../types';

export interface ImportExportService {
  serialize(def: WorkflowDefinition, format: SerializationFormat): Promise<string>;
  deserialize(data: string, format: SerializationFormat): Promise<ImportExportResult>;
  exportJSON(def: WorkflowDefinition): Promise<string>;
  exportYAML(def: WorkflowDefinition): Promise<string>;
  importJSON(data: string): Promise<ImportExportResult>;
  importYAML(data: string): Promise<ImportExportResult>;
}

export class ImportExportServiceImpl implements ImportExportService {
  private formatValue(obj: unknown, indent: number = 0): string {
    const prefix = '  '.repeat(indent);
    if (obj === null || obj === undefined) return 'null';
    if (typeof obj === 'string') return `"${obj}"`;
    if (typeof obj === 'number' || typeof obj === 'boolean') return String(obj);
    if (Array.isArray(obj)) {
      if (obj.length === 0) return '[]';
      return obj.map((item) => `  - ${this.formatValue(item, indent + 1)}`).join('\n');
    }
    if (typeof obj === 'object') {
      const entries = Object.entries(obj as Record<string, unknown>);
      if (entries.length === 0) return '{}';
      return entries
        .map(([key, value]) => `${key}: ${this.formatValue(value, indent + 1)}`)
        .join('\n');
    }
    return String(obj);
  }

  async serialize(def: WorkflowDefinition, format: SerializationFormat): Promise<string> {
    if (format === 'json') {
      return this.exportJSON(def);
    } else if (format === 'yaml') {
      return this.exportYAML(def);
    }
    throw new Error(`Unsupported format: ${format}`);
  }

  async deserialize(data: string, format: SerializationFormat): Promise<ImportExportResult> {
    try {
      if (format === 'json') {
        const def = JSON.parse(data);
        return {
          success: true,
          workflow: def as WorkflowDefinition,
          errors: [],
          format,
          version: def.version || '0.0.0',
        };
      } else if (format === 'yaml') {
        // YAML parsing would require a library like js-yaml
        // For now, return a placeholder
        return {
          success: false,
          errors: [{ rule: 'yaml_not_implemented', severity: 'error', message: `YAML parsing not yet implemented`, location: 'workflow' }],
          format,
          version: '0.0.0',
        };
      }
    } catch (_err: unknown) {
      return {
        success: false,
        errors: [{ rule: 'parse_error', severity: 'error', message: `Failed to parse: ${String(_err)}`, location: 'workflow' }],
        format,
        version: '0.0.0',
      };
    }
    return {
      success: false,
      errors: [{ rule: 'unsupported_format', severity: 'error', message: `Unsupported format: ${format}`, location: 'workflow' }],
      format,
      version: '0.0.0',
    };
  }

  async exportJSON(def: WorkflowDefinition): Promise<string> {
    return JSON.stringify(def, null, 2);
  }

  async exportYAML(def: WorkflowDefinition): Promise<string> {
    // Simple YAML serializer for demonstration
    // In production, use a proper YAML library
    return `# YAML export not fully implemented
# Workflow: ${def.name}
# Version: ${def.version}`;
  }

  async importJSON(data: string): Promise<ImportExportResult> {
    return this.deserialize(data, 'json');
  }

  async importYAML(data: string): Promise<ImportExportResult> {
    return this.deserialize(data, 'yaml');
  }
}

export const importExportService = new ImportExportServiceImpl();
