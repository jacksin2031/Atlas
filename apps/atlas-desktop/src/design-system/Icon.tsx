import React from "react";

export type IconName =
  | "pointer" | "hand" | "zoom" | "rectangle" | "ellipse" | "polygon" | "lasso"
  | "line" | "arrow" | "text" | "ocr" | "detect" | "template" | "eyedropper"
  | "probe" | "measure" | "capture" | "freeze" | "record" | "stop" | "play"
  | "pause" | "previous" | "next" | "open" | "save" | "export" | "undo"
  | "redo" | "zoom-in" | "zoom-out" | "fit" | "actual" | "grid" | "rulers"
  | "command" | "workflow" | "vision" | "folder" | "search" | "copy" | "lock"
  | "eye" | "trash" | "duplicate" | "marker" | "ai" | "retry" | "settings"
  | "image" | "memory" | "tools" | "metrics" | "inspect" | "clear" | "add";

const paths: Record<IconName, React.ReactNode> = {
  pointer: <path d="M5 3l11 9-6 .7-2.7 5.1z" />,
  hand: <path d="M7 11V6a1 1 0 012 0v4-6a1 1 0 012 0v6-5a1 1 0 012 0v6-4a1 1 0 012 0v7c0 4-3 6-6 6H8c-2 0-4-2-5-4l-1-3a1.5 1.5 0 013-.8z" />,
  zoom: <><circle cx="9" cy="9" r="5"/><path d="M13 13l5 5M9 6v6M6 9h6"/></>,
  rectangle: <rect x="3" y="4" width="14" height="12" rx="1" />,
  ellipse: <ellipse cx="10" cy="10" rx="7" ry="5" />,
  polygon: <path d="M10 2l8 6-3 9H5L2 8z" />,
  lasso: <path d="M16 13c2-2 2-7-2-9S4 3 3 8s5 7 9 6c3-1 5 1 3 3-1 2-5 2-5 0 0-1 2-2 3-1" />,
  line: <path d="M3 17L17 3" />,
  arrow: <path d="M3 17L17 3M10 3h7v7" />,
  text: <path d="M4 4h12M10 4v13M7 17h6" />,
  ocr: <><path d="M3 7V3h4M13 3h4v4M17 13v4h-4M7 17H3v-4"/><path d="M6 8h8M6 11h8M6 14h5"/></>,
  detect: <><path d="M3 7V3h4M13 3h4v4M17 13v4h-4M7 17H3v-4"/><circle cx="10" cy="10" r="3"/></>,
  template: <><rect x="3" y="3" width="14" height="14"/><path d="M7 3v14M13 3v14M3 8h14M3 13h14"/></>,
  eyedropper: <path d="M12 3l5 5-8 8-4 1 1-4zM10 5l5 5" />,
  probe: <><path d="M10 2v16M2 10h16"/><circle cx="10" cy="10" r="3"/></>,
  measure: <><path d="M3 15L15 3l3 3L6 18z"/><path d="M9 9l2 2M12 6l2 2"/></>,
  capture: <><rect x="3" y="5" width="14" height="11" rx="2"/><circle cx="10" cy="10.5" r="3"/><path d="M7 5l1-2h4l1 2"/></>,
  freeze: <path d="M10 2v16M3 6l14 8M17 6L3 14M6 3l8 14M14 3L6 17" />,
  record: <circle cx="10" cy="10" r="6" fill="currentColor" stroke="none" />,
  stop: <rect x="5" y="5" width="10" height="10" fill="currentColor" stroke="none" />,
  play: <path d="M6 3l11 7-11 7z" />,
  pause: <><path d="M6 4v12M14 4v12"/></>,
  previous: <><path d="M5 4v12M16 4L7 10l9 6z"/></>,
  next: <><path d="M15 4v12M4 4l9 6-9 6z"/></>,
  open: <path d="M2 7h6l2-3h8v13H2zM2 9h16" />,
  save: <><path d="M3 3h12l2 2v12H3z"/><path d="M6 3v5h8V3M6 17v-6h8v6"/></>,
  export: <><path d="M4 9v8h12V9"/><path d="M10 13V2M6 6l4-4 4 4"/></>,
  undo: <path d="M7 6L3 10l4 4M4 10h8a5 5 0 015 5" />,
  redo: <path d="M13 6l4 4-4 4M16 10H8a5 5 0 00-5 5" />,
  "zoom-in": <><circle cx="9" cy="9" r="5"/><path d="M13 13l5 5M9 6v6M6 9h6"/></>,
  "zoom-out": <><circle cx="9" cy="9" r="5"/><path d="M13 13l5 5M6 9h6"/></>,
  fit: <path d="M7 3H3v4M13 3h4v4M17 13v4h-4M7 17H3v-4" />,
  actual: <><path d="M5 3h10v14H5z"/><path d="M8 7h4M8 10h4M8 13h4"/></>,
  grid: <><path d="M3 3h14v14H3zM8 3v14M13 3v14M3 8h14M3 13h14"/></>,
  rulers: <><path d="M3 3h14v4H3zM3 7h4v10H3z"/><path d="M6 3v2M10 3v2M14 3v2M3 10h2M3 14h2"/></>,
  command: <path d="M7 7H5a3 3 0 100 6h2V7zm6 0h2a3 3 0 110 6h-2V7zM7 7v6h6V7H7z" />,
  workflow: <><circle cx="4" cy="5" r="2"/><circle cx="16" cy="10" r="2"/><circle cx="4" cy="15" r="2"/><path d="M6 5h4a4 4 0 014 4M6 15h4a4 4 0 004-4"/></>,
  vision: <><path d="M2 10s3-5 8-5 8 5 8 5-3 5-8 5-8-5-8-5z"/><circle cx="10" cy="10" r="2.5"/></>,
  folder: <path d="M2 5h6l2 2h8v10H2z" />,
  search: <><circle cx="8" cy="8" r="5"/><path d="M12 12l6 6"/></>,
  copy: <><rect x="7" y="7" width="10" height="10"/><path d="M13 7V3H3v10h4"/></>,
  lock: <><rect x="4" y="9" width="12" height="9" rx="1"/><path d="M7 9V6a3 3 0 016 0v3"/></>,
  eye: <><path d="M2 10s3-5 8-5 8 5 8 5-3 5-8 5-8-5-8-5z"/><circle cx="10" cy="10" r="2"/></>,
  trash: <><path d="M4 6h12M8 3h4l1 3M6 6l1 11h6l1-11"/></>,
  duplicate: <><rect x="6" y="6" width="11" height="11"/><path d="M13 6V3H3v10h3"/></>,
  marker: <path d="M5 3h10v14l-5-3-5 3z" />,
  ai: <><path d="M5 7a5 5 0 0110 0v6a5 5 0 01-10 0z"/><path d="M8 10h.01M12 10h.01M8 14h4M10 2V0M2 10H0M20 10h-2"/></>,
  retry: <><path d="M16 6V2l-3 3a7 7 0 10.5 10.5"/><path d="M16 2v4h-4"/></>,
  settings: <><circle cx="10" cy="10" r="3"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.3 4.3l1.4 1.4M14.3 14.3l1.4 1.4M15.7 4.3l-1.4 1.4M5.7 14.3l-1.4 1.4"/></>,
  image: <><rect x="2" y="3" width="16" height="14" rx="1"/><circle cx="7" cy="8" r="2"/><path d="M3 16l5-5 3 3 2-2 4 4"/></>,
  memory: <><rect x="4" y="4" width="12" height="12" rx="2"/><path d="M7 1v3M10 1v3M13 1v3M7 16v3M10 16v3M13 16v3M1 7h3M1 10h3M1 13h3M16 7h3M16 10h3M16 13h3"/></>,
  tools: <path d="M12 3a4 4 0 01-5 5L3 12l5 5 4-4a4 4 0 005-5l-3 3-3-3z"/>,
  metrics: <><path d="M3 17V9M8 17V4M13 17v-6M18 17V2"/><path d="M1 17h18"/></>,
  inspect: <><circle cx="8" cy="8" r="5"/><path d="M12 12l6 6M8 5v6M5 8h6"/></>,
  clear: <><path d="M4 4l12 12M16 4L4 16"/></>,
  add: <path d="M10 3v14M3 10h14"/>,
};

export const Icon: React.FC<{ name: IconName; size?: number; className?: string }> = ({ name, size = 16, className }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {paths[name]}
  </svg>
);
