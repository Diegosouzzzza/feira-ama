import { create } from "zustand";
import { ApiError, apiPost } from "@/lib/api/client";
import type { ControlGrant } from "@/lib/api/types";

const KEY = "av-control";

interface Saved {
  token: string;
  operator: string;
}

function load(): Saved | null {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Saved) : null;
  } catch {
    return null;
  }
}

function save(value: Saved | null): void {
  try {
    if (value) localStorage.setItem(KEY, JSON.stringify(value));
    else localStorage.removeItem(KEY);
  } catch {
    // Private mode or blocked storage: control still works until the page reloads.
  }
}

interface ControlStore {
  token: string | null;
  operator: string | null;
  /** Last operator name typed here, kept to prefill forms. */
  lastOperator: string | null;
  claim: (operator: string, takeover?: boolean) => Promise<void>;
  release: () => Promise<void>;
  forget: () => void;
}

const saved = load();

export const useControl = create<ControlStore>()((set, get) => ({
  token: saved?.token ?? null,
  operator: saved?.operator ?? null,
  lastOperator: saved?.operator ?? null,
  claim: async (operator, takeover = false) => {
    const grant = await apiPost<ControlGrant>("/control/claim", { operator, takeover }, get().token);
    save({ token: grant.token, operator: grant.operator });
    set({ token: grant.token, operator: grant.operator, lastOperator: grant.operator });
  },
  release: async () => {
    const token = get().token;
    try {
      await apiPost<void>("/control/release", undefined, token);
    } finally {
      get().forget();
    }
  },
  forget: () => {
    save(null);
    set({ token: null, operator: null });
  },
}));

/** POST a control action; a CONTROL_LOCKED answer means this screen lost the control. */
export async function controlPost<T>(path: string, body?: unknown): Promise<T> {
  const { token, forget } = useControl.getState();
  try {
    return await apiPost<T>(path, body, token);
  } catch (error) {
    if (error instanceof ApiError && error.code === "CONTROL_LOCKED") forget();
    throw error;
  }
}
