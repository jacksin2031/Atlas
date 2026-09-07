import React, { useEffect, useRef, useState } from "react";
import { Button, EmptyState, Field } from "../../design-system";
import { marketplaceService, useMarketplaceStore, type Manifest, type View } from "./service";
import "./styles.css";

export function MarketplaceBrowser(): React.JSX.Element {
  const { snapshot, view, query, busy, error, selected } = useMarketplaceStore();
  const rows = snapshot ? (view === "Discover" ? snapshot.available.filter((p) => p.manifest).map((p) => p.manifest!) : snapshot.installed.filter((i) => view !== "Updates" || i.update).map((i) => view === "Updates" ? i.update!.manifest! : i.installation.manifest)) : [];
  const select = (manifest: Manifest) => useMarketplaceStore.setState({ selected: manifest, review: null });
  return <section className="marketplace-panel" aria-label="Marketplace browser">
    <header><h2>Marketplace</h2><p>{snapshot?.source ?? "Plugin distribution"}</p></header>
    <nav aria-label="Marketplace views">{(["Discover", "Installed", "Updates"] as View[]).map((name) => <Button key={name} aria-pressed={view === name} onClick={() => useMarketplaceStore.setState({ view: name })}>{name}</Button>)}</nav>
    <form onSubmit={(event) => { event.preventDefault(); void marketplaceService.refresh(); }}><Field label="Search registry"><input value={query} onChange={(event) => useMarketplaceStore.setState({ query: event.target.value })}/></Field><Button type="submit" disabled={busy}>Search</Button></form>
    <div className="marketplace-actions"><Button disabled={busy} onClick={() => void marketplaceService.refresh()}>Refresh</Button><Button disabled={busy} onClick={() => void marketplaceService.inspect()}>Install from local package</Button></div>
    {error && <p role="alert">{error.code}: {error.message}</p>}
    {snapshot?.providerError && <p role="status">{snapshot.providerError.message}. Installed plugins remain manageable.</p>}
    {busy && <p role="status">Processing package operation…</p>}
    {!rows.length && <EmptyState icon="folder" title={snapshot ? `No ${view.toLowerCase()} packages` : "Marketplace backend unavailable"} description={snapshot ? "Refresh or change the search to discover packages." : "Run Atlas Desktop to discover and manage installed plugins."}/>}
    <ul className="marketplace-list">{rows.map((manifest) => <li key={`${manifest.plugin_id}@${manifest.version}`}><button type="button" aria-pressed={selected?.plugin_id === manifest.plugin_id && selected.version === manifest.version} onClick={() => select(manifest)}><strong>{manifest.plugin_name}</strong><span>{manifest.version} · {manifest.author}</span><small>{manifest.description}</small></button></li>)}</ul>
    {view === "Discover" && snapshot?.available.filter((p) => !p.compatible).map((p) => <p key={`${p.pluginId}@${p.version}`} role="status">{p.pluginId} {p.version}: {p.error?.code} — {p.error?.message}</p>)}
  </section>;
}

export function MarketplaceDetails(): React.JSX.Element {
  const { snapshot, selected, review, busy } = useMarketplaceStore();
  const [confirm, setConfirm] = useState<"install" | "uninstall" | null>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const manifest = review?.manifest ?? selected;
  const installed = snapshot?.installed.find((i) => i.installation.manifest.plugin_id === manifest?.plugin_id);
  const available = snapshot?.available.find((p) => p.manifest?.plugin_id === manifest?.plugin_id && p.manifest?.version === manifest?.version);
  const digest = review?.digest ?? available?.digest ?? (installed?.installation.manifest.version === manifest?.version ? installed?.installation.digest : undefined);
  useEffect(() => { if (confirm) dialog.current?.showModal(); else dialog.current?.close(); }, [confirm]);
  useEffect(() => { setConfirm(null); }, [selected?.plugin_id, selected?.version, review?.reviewId]);
  if (!manifest) return <EmptyState icon="folder" title="Inspect a plugin" description="Select a package to review its identity, permissions, compatibility, and runtime status."/>;
  return <section className="marketplace-panel" aria-label="Plugin details">
    <h2>{manifest.plugin_name}</h2><code>{manifest.plugin_id}</code><p>{manifest.description}</p>
    <div className="marketplace-actions">
      <Button disabled={busy} onClick={() => void marketplaceService.inspect(manifest)}>Validate & review package</Button>
      {review && <Button disabled={busy} onClick={() => setConfirm("install")}>{installed ? "Review update" : "Review installation"}</Button>}
      {installed && <><Button disabled={busy} onClick={() => void marketplaceService.mutate(installed.installation.enabled ? "disable" : "enable", manifest.plugin_id)}>{installed.installation.enabled ? "Disable" : "Enable"}</Button><Button disabled={busy} onClick={() => setConfirm("uninstall")}>Uninstall</Button></>}
    </div>
    <dl><dt>Version</dt><dd>{manifest.version}</dd><dt>Author / license</dt><dd>{manifest.author} / {manifest.license}</dd><dt>Source</dt><dd>{review?.source ?? installed?.installation.source ?? snapshot?.source}</dd><dt>Trust</dt><dd>{review?.trust ?? snapshot?.trust}</dd><dt>Scope</dt><dd>{snapshot?.scope}</dd><dt>Runtime</dt><dd>{installed ? `${installed.installation.enabled ? "Enabled" : "Disabled"} · ${installed.health}` : "Not installed"}</dd><dt>Installed version</dt><dd>{installed?.installation.manifest.version ?? "None"}</dd><dt>Compatible update</dt><dd>{installed?.update?.manifest?.version ?? "None"}</dd></dl>
    {installed?.error && <p role="alert">{installed.error.code}: {installed.error.message}</p>}
    <h3>Compatibility</h3><pre>{JSON.stringify(manifest.compatibility, null, 2)}</pre>
    <h3>Capabilities</h3><p>{manifest.capabilities.filter((c) => c.enabled).map((c) => c.capability).join(", ") || "None"}</p>
    <h3>Requested permissions</h3><PermissionList manifest={manifest}/>
    <p>Plugin permission approval does not arm Input automation. Privileged host services are unavailable in this constrained package provider.</p>
    {digest && <><h3>SHA-256</h3><code className="marketplace-digest">{digest}</code></>}
    <dialog ref={dialog} aria-labelledby="marketplace-confirm-title" onCancel={() => setConfirm(null)}>
      <h2 id="marketplace-confirm-title">{confirm === "install" ? `Approve ${manifest.plugin_name} ${manifest.version}` : `Uninstall ${manifest.plugin_name}?`}</h2>
      {confirm === "install" ? <><p>Approve these exact permissions for the inspected package.</p><PermissionList manifest={manifest}/><p>{review?.trust}</p><code className="marketplace-digest">{review?.digest}</code><p>New installations remain disabled until you enable them.</p></> : <p>Contributed nodes will be unavailable. Saved workflow definitions will remain intact.</p>}
      <div className="marketplace-actions"><Button autoFocus onClick={() => setConfirm(null)}>Cancel</Button><Button disabled={busy} onClick={() => { const action = confirm; setConfirm(null); if (action) void marketplaceService.mutate(action, manifest.plugin_id); }}>{confirm === "install" ? "Approve & install" : "Confirm uninstall"}</Button></div>
    </dialog>
  </section>;
}
function PermissionList({ manifest }: { manifest: Manifest }): React.JSX.Element { return manifest.permissions.length ? <ul>{manifest.permissions.map((p) => <li key={p.name}><strong>{p.name}</strong> · {p.level} · {p.required ? "Required" : "Optional"}</li>)}</ul> : <p>No privileged permissions requested.</p>; }
export function MarketplaceActivity(): React.JSX.Element {
  const audit = useMarketplaceStore((s) => s.snapshot?.audit);
  return <section className="marketplace-panel" aria-label="Plugin activity"><h2>Package activity</h2><ul>{audit?.map((event) => <li key={event.revision}>{event.action} · {event.pluginId}<br/><small>{event.timestamp} · {event.requestId}</small></li>)}</ul></section>;
}
