import React from "react";
import { Button, EmptyState } from "../../design-system";
import { openMarketplace } from "../../studio/marketplace/service";
export const ExtensionsPanel: React.FC = () => <EmptyState icon="folder" title="Installed plugins" description="Manage package permissions, runtime status, and updates in Marketplace." actions={<Button onClick={() => openMarketplace("Installed")}>Open installed plugins</Button>}/>;
