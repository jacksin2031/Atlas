import React from "react";
import { Button, EmptyState } from "../design-system";

export class PanelErrorBoundary extends React.Component<{ title: string; children: React.ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    return this.state.failed ? <div role="alert"><EmptyState title={`${this.props.title} could not be displayed`} description="Other panels remain available. Retry this panel; if it fails again, export diagnostics and restart Atlas." actions={<Button onClick={() => this.setState({ failed: false })}>Retry panel</Button>}/></div> : this.props.children;
  }
}
