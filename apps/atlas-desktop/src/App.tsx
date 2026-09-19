import React, { useEffect } from 'react';
import { AppLayout } from './components/layouts';
import { useRuntimeStore, useProjectStore } from './stores';
import { ipcService, themeService, pluginManagerService, projectService } from './services';

export const App: React.FC = () => {
  useEffect(() => {
    themeService.initialize();
    pluginManagerService.initialize();
    ipcService.connect();
    useRuntimeStore.getState().initializeRuntimes();
    void projectService.restoreLastProject().catch(() => useProjectStore.getState().addNotification({ title: "Project restore unavailable", message: "Open your project manually. Check folder access and compatibility if it cannot be reopened.", severity: "error", acknowledged: false }));
  }, []);

  return <AppLayout />;
};
