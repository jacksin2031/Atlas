import React, { useEffect } from 'react';
import { AppLayout } from './components/layouts';
import { useRuntimeStore } from './stores';
import { ipcService, themeService, pluginManagerService, projectService } from './services';

export const App: React.FC = () => {
  useEffect(() => {
    themeService.initialize();
    pluginManagerService.initialize();
    ipcService.connect();
    useRuntimeStore.getState().initializeRuntimes();
    void projectService.restoreLastProject();
  }, []);

  return <AppLayout />;
};
