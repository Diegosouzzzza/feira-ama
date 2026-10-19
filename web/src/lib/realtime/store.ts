import { create } from "zustand";
import { apiGet } from "@/lib/api/client";
import type { InspectionPage, WsEvent } from "@/lib/api/types";
import { applyEvent, initialLive, type LiveState, mergeRecent, RECENT_LIMIT } from "./reducer";

export type Connection = "connecting" | "open" | "closed";

interface LiveStore extends LiveState {
  connection: Connection;
  /** When the last message from the service arrived (ISO). */
  receivedAt: string | null;
  dismissIncident: () => void;
}

export const useLive = create<LiveStore>()((set) => ({
  ...initialLive,
  connection: "connecting",
  receivedAt: null,
  dismissIncident: () => set({ incident: null }),
}));

let socket: WebSocket | null = null;
let retryMs = 500;
let retryTimer: ReturnType<typeof setTimeout> | undefined;
let started = false;

async function loadRecent(lotId: number): Promise<void> {
  try {
    const page = await apiGet<InspectionPage>(`/inspections?lot_id=${lotId}&limit=${RECENT_LIMIT}`);
    if (useLive.getState().status?.active_lot?.id !== lotId) return;
    useLive.setState((s) => ({ recent: mergeRecent(s.recent, page.items) }));
  } catch {
    // The live stream still fills the list; a failed fetch only means fewer old items shown.
  }
}

let freshConnection = false;

function handle(event: WsEvent): void {
  const before = useLive.getState();
  const { state, resync } = applyEvent(before, event);
  if (resync) {
    socket?.close(4000, "resync");
    return;
  }
  useLive.setState({ ...state, receivedAt: new Date().toISOString() });
  const lotId = state.status?.active_lot?.id;
  const lotChanged = lotId !== before.status?.active_lot?.id;
  // After (re)connecting, events missed while offline are only recoverable from the API.
  if (lotId !== undefined && (lotChanged || freshConnection)) void loadRecent(lotId);
  freshConnection = false;
}

function connect(): void {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${scheme}://${window.location.host}/api/events`);
  socket = ws;
  useLive.setState({ connection: "connecting" });

  ws.onopen = () => {
    retryMs = 500;
    freshConnection = true;
    useLive.setState({ connection: "open" });
  };
  ws.onmessage = (message) => {
    try {
      handle(JSON.parse(String(message.data)) as WsEvent);
    } catch {
      ws.close(4000, "resync");
    }
  };
  ws.onclose = () => {
    if (socket !== ws) return;
    useLive.setState({ connection: "closed", seq: 0 });
    retryTimer = setTimeout(connect, retryMs);
    retryMs = Math.min(retryMs * 2, 5000);
  };
}

/** Open the event stream once for the whole app; reconnects forever with backoff. */
export function startRealtime(): () => void {
  if (!started) {
    started = true;
    connect();
  }
  return () => undefined;
}

/** Test helper. */
export function stopRealtime(): void {
  started = false;
  clearTimeout(retryTimer);
  const ws = socket;
  socket = null;
  ws?.close();
}
