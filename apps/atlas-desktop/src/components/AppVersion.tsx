import React from "react";
import { getNativeAppVersion } from "../ipc/bridge";

export function AppVersion() {
  const [label, setLabel] = React.useState("Atlas · checking version…");
  React.useEffect(() => {
    let active = true;
    void getNativeAppVersion().then((version) => {
      if (active) setLabel(`Atlas v${version}`);
    }).catch(() => {
      if (active) setLabel("Atlas · version unavailable");
    });
    return () => { active = false; };
  }, []);
  return <span>{label}</span>;
}
