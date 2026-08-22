// Atlas Workflow Studio — Import/Export Service Tests

import { describe, it, expect } from 'vitest';
import { importExportService } from '../../services/import-export-service';
import type { WorkflowDefinition } from '../../types';

function createTestDef(): WorkflowDefinition {
  return {
    id: 'wf_test',
    version: '1.0.0',
    name: 'Test',
    nodes: [],
    edges: [],
    variables: [],
    parameters: {},
    metadata: { createdAt: Date.now(), updatedAt: Date.now(), tags: [] },
  };
}

describe('ImportExportService', () => {
  it('should serialize to JSON', async () => {
    const def = createTestDef();
    const json = await importExportService.exportJSON(def);
    const parsed = JSON.parse(json);
    expect(parsed.id).toBe('wf_test');
  });

  it('should serialize to YAML', async () => {
    const def = createTestDef();
    const yaml = await importExportService.exportYAML(def);
    expect(yaml).toContain('wf_test');
    const result = await importExportService.importYAML(yaml);
    expect(result.success).toBe(true);
    expect(result.workflow?.id).toBe('wf_test');
  });

  it('should deserialize JSON', async () => {
    const def = createTestDef();
    const json = await importExportService.exportJSON(def);
    const result = await importExportService.importJSON(json);
    expect(result.success).toBe(true);
    expect(result.workflow?.id).toBe('wf_test');
  });

  it('should reject invalid JSON', async () => {
    const result = await importExportService.importJSON('{invalid}');
    expect(result.success).toBe(false);
    expect(result.errors).toBeDefined();
  });

  it('should reject JSON with an invalid workflow structure', async () => {
    const result = await importExportService.importJSON('{}');
    expect(result.success).toBe(false);
    expect(result.errors?.some((error) => error.rule === 'required_field')).toBe(true);
  });

  it('should reject malformed nodes', async () => {
    const def = createTestDef() as any;
    def.nodes = [{ id: 'broken' }];
    const result = await importExportService.importJSON(JSON.stringify(def));
    expect(result.success).toBe(false);
    expect(result.errors?.some((error) => error.rule === 'invalid_node')).toBe(true);
  });
});
