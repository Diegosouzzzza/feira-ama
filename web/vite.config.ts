import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { configDefaults, defineConfig } from "vitest/config";

const API_TARGET = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { "@": path.resolve(import.meta.dirname, "src") },
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: {
      "/api": { target: API_TARGET, ws: true },
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    // Served from the same machine, offline: ~175 kB gzip is fine; no need to split routes.
    chunkSizeWarningLimit: 800,
  },
  test: {
    // Browser flows live in e2e/ and run with Playwright, not Vitest.
    exclude: [...configDefaults.exclude, "e2e/**"],
  },
});
