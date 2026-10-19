// Starts the API for end-to-end tests: simulated bench, fixed seed, throwaway data folder.
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const candidates = [join(process.env.APPDATA ?? "", "Python", "Python312", "Scripts", "uv.exe"), "uv"];
const uv = candidates.find((c) => c === "uv" || existsSync(c));
const dataDir = mkdtempSync(join(tmpdir(), "amazonvision-e2e-"));

const child = spawn(uv, ["run", "--directory", "../api", "amazonvision"], {
  stdio: "inherit",
  env: {
    ...process.env,
    AV_PORT: "8010",
    AV_MODE: "simulado",
    AV_DATA_DIR: dataDir,
    AV_SIM_SPEED: "15",
    AV_SIM_SEED: "9",
    AV_LOG_TO_FILE: "false",
  },
});

for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => child.kill());
child.on("exit", (code) => process.exit(code ?? 0));
