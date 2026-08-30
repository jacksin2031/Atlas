import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
    plugins: [react()],
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    "layout-engine": ["flexlayout-react"],
                    "flow-engine": ["@xyflow/react"],
                },
            },
        },
    },
    server: {
        port: 1420,
        watch: {
            ignored: ["**/src-tauri/target/**"],
        },
    },
});
