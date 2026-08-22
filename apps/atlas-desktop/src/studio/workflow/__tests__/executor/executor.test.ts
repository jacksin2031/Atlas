// Atlas Workflow Studio — Executor Tests

import { describe, it, expect, beforeEach } from 'vitest';
import { IPCExecutorService } from '../../services/executor-service';

describe('IPCExecutorService', () => {
  let service: IPCExecutorService;

  beforeEach(() => {
    service = new IPCExecutorService();
  });

  it('should throw when IPC not connected', async () => {
    await expect(service.run('wf_1')).rejects.toThrow('IPC not connected');
  });

  it('should set IPC and call RPC', async () => {
    const mockIPC = {
      invoke: async <T>(_command: string, args: Record<string, unknown>): Promise<T> => {
        expect(args).toHaveProperty('command');
        expect(args).toHaveProperty('args');
        return 'run_123' as T;
      },
    };
    service.setIPC(mockIPC);
    const result = await service.run('wf_1');
    expect(result).toBe('run_123');
  });

  it('should support all execution operations', async () => {
    const mockIPC = {
      invoke: async <T>(_command: string, _args: Record<string, unknown>): Promise<T> => {
        return undefined as T;
      },
    };
    service.setIPC(mockIPC);
    await service.pause('run_1');
    await service.resume('run_1');
    await service.stop('run_1');
    await service.step('run_1');
    await service.restart('run_1');
    await service.simulate('run_1');
    await service.getStatus('run_1');
  });
});
