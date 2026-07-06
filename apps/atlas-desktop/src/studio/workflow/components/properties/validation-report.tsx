// Atlas Workflow Studio - Validation Report Panel
// RFC-0317 compliant validation visualization

import React from 'react';
import { useWorkflowStore } from '../../stores';
import { validationService } from '../../services/validation-service';
import type { ValidationResult } from '../../types';

export const ValidationReportPanel: React.FC = () => {
  const nodes = useWorkflowStore((s: any) => s.nodes);
  const edges = useWorkflowStore((s) => s.edges);
  const setValidationResults = useWorkflowStore((s) => s.setValidationResults);
  const [results, setResults] = React.useState<ValidationResult[]>([]);
  const [isValid, setIsValid] = React.useState<boolean | null>(null);

  const handleValidate = async () => {
    // Build a minimal workflow definition from current state
    const def = useWorkflowStore.getState().exportToDefinition();
    const validationResults = await validationService.validate(def);
    setResults(validationResults);
    setValidationResults(validationResults);
    const hasErrors = validationResults.some((r) => r.severity === 'error');
    setIsValid(!hasErrors);
  };

  const errorCount = results.filter((r) => r.severity === 'error').length;
  const warningCount = results.filter((r) => r.severity === 'warning').length;
  const infoCount = results.filter((r) => r.severity === 'info').length;

  const severityColor = (severity: string) => {
    switch (severity) {
      case 'error': return '#F44336';
      case 'warning': return '#FFB74D';
      case 'info': return '#4FC3F7';
      default: return '#888';
    }
  };

  return (
    <div
      style={{
        width: 300,
        height: '100%',
        backgroundColor: '#1e1e1e',
        borderLeft: '1px solid #333',
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
          backgroundColor: '#2d2d2d',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>Validation</span>
        <button
          onClick={handleValidate}
          style={{
            fontSize: 10,
            padding: '2px 8px',
            border: '1px solid #0078d4',
            borderRadius: 3,
            backgroundColor: '#0078d4',
            color: '#fff',
            cursor: 'pointer',
          }}
        >
          Validate
        </button>
      </div>

      {/* Summary */}
      <div style={{ padding: 8, display: 'flex', gap: 8 }}>
        {isValid === true && (
          <div style={{ flex: 1, padding: 6, backgroundColor: '#1a3a1a', borderRadius: 4, textAlign: 'center', fontSize: 11, color: '#4CAF50' }}>
            ✓ Valid
          </div>
        )}
        {isValid === false && (
          <div style={{ flex: 1, padding: 6, backgroundColor: '#3a1a1a', borderRadius: 4, textAlign: 'center', fontSize: 11, color: '#F44336' }}>
            ✗ Invalid
          </div>
        )}
        {isValid === null && (
          <div style={{ flex: 1, padding: 6, backgroundColor: '#2a2a2a', borderRadius: 4, textAlign: 'center', fontSize: 11, color: '#666' }}>
            Not validated
          </div>
        )}
      </div>

      {/* Counts */}
      {(errorCount > 0 || warningCount > 0 || infoCount > 0) && (
        <div style={{ padding: '4px 12px', display: 'flex', gap: 8, fontSize: 11 }}>
          <span style={{ color: '#F44336' }}>● {errorCount} errors</span>
          <span style={{ color: '#FFB74D' }}>● {warningCount} warnings</span>
          <span style={{ color: '#4FC3F7' }}>● {infoCount} info</span>
        </div>
      )}

      {/* Results */}
      {results.map((r, i) => (
        <div
          key={i}
          style={{
            padding: '4px 12px',
            borderBottom: '1px solid #2a2a2a',
            borderLeft: '3px solid #F44336', 
            backgroundColor: r.severity === 'error' ? '#2a1a1a' : r.severity === 'warning' ? '#2a2a1a' : 'transparent',
          }}
        >
          <div style={{ fontSize: 10, color: severityColor(r.severity), textTransform: 'uppercase' }}>
            {r.rule}
          </div>
          <div style={{ fontSize: 11, color: '#ccc', marginTop: 2 }}>{r.message}</div>
          {r.nodeId && (
            <div style={{ fontSize: 9, color: '#666', fontFamily: 'monospace', marginTop: 2 }}>
              Node: {r.nodeId}
            </div>
          )}
        </div>
      ))}

      {results.length === 0 && isValid !== false && (
        <div style={{ padding: 16, fontSize: 12, color: '#555', textAlign: 'center' }}>
          Click Validate to check the workflow
        </div>
      )}
    </div>
  );
};
