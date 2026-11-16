import { defineConfig } from "@playwright/test";

// Uses the Microsoft Edge already installed on Windows: no browser download needed.
export default defineConfig({
  testDir: "e2e",
  timeout: 60_000,
  workers: 1,
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:8010",
    channel: "msedge",
    locale: "pt-BR",
    timezoneId: "America/Manaus",
    viewport: { width: 1366, height: 768 },
  },
  webServer: {
    command: "node e2e/start-api.mjs",
    url: "http://127.0.0.1:8010/api/health",
    reuseExistingServer: false,
    timeout: 60_000,
  },
});
