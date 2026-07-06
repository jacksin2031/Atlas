import React, { useEffect } from 'react';
import { AppLayout } from './components/layouts';
import { useRuntimeStore } from './stores';
import { ipcService, themeService, layoutService, pluginManagerService } from './services';

export const App: React.FC = () => {
  useEffect(() => {
    themeService.initialize();
    layoutService.initialize();
    pluginManagerService.initialize();
    ipcService.connect();
    useRuntimeStore.getState().initializeRuntimes();
  }, []);

  return <AppLayout />;
};
