import React from "react";
import { Icon, type IconName } from "./Icon";
export { Icon, type IconName } from "./Icon";

export const IconButton: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement> & { icon: IconName; active?: boolean; label: string }> = ({ icon, active, label, className = "", ...props }) => (
  <button type="button" className={`atlas-icon-button${active ? " is-active" : ""} ${className}`} title={label} aria-label={label} aria-pressed={active} {...props}><Icon name={icon} /></button>
);

export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement> & { icon?: IconName }> = ({ icon, children, className = "", ...props }) => (
  <button type="button" className={`atlas-button ${className}`} {...props}>{icon && <Icon name={icon} size={14} />}{children}</button>
);

export const EmptyState: React.FC<{ title: string; description?: string; actions?: React.ReactNode; icon?: IconName }> = ({ title, description, actions, icon = "vision" }) => (
  <div className="atlas-empty-state"><Icon name={icon} size={34}/><strong>{title}</strong>{description && <span>{description}</span>}{actions && <div className="atlas-empty-actions">{actions}</div>}</div>
);

export const Field: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => <label className="atlas-field"><span>{label}</span>{children}</label>;

export const ToolbarGroup: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => <div className="atlas-toolbar-group" role="group" aria-label={label}>{children}</div>;
