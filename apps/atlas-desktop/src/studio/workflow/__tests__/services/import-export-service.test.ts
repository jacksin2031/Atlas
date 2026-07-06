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

  it('should export validation report', async () => {
    const def = createTestDef();
    const report = await importExportService.exportJSON(def);
    const parsed = JSON.parse(report);
    expect(parsed.format).toBe('validation-report');
  });

  it('should export execution report', async () => {
    const report = await importExportService.exportJSON({ id: 'test', version: '1.0.0', name: 'Test', nodes: [], edges: [], variables: [], parameters: {}, metadata: { createdAt: 0, updatedAt: 0 } } as any);
    const parsed = JSON.parse(report);
    expect(parsed.runId).toBe('run_1');
  });
});
