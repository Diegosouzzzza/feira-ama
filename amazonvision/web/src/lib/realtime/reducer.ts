import type { FaultData, InspectionOut, SystemStatus, WsEvent } from "@/lib/api/types";

export const RECENT_LIMIT = 12;

export interface Incident {
  component: "device" | "camera" | "model" | "storage";
  message: string;
  at: string;
}

export interface LiveState {
  status: SystemStatus | null;
  seq: number;
  recent: InspectionOut[];
  lastFault: FaultData | null;
  /** Last equipment problem reported by the service (cleared when restored or dismissed). */
  incident: Incident | null;
}

export const initialLive: LiveState = {
  status: null,
  seq: 0,
  recent: [],
  lastFault: null,
  incident: null,
};

export interface Outcome {
  state: LiveState;
  /** The event stream has a gap: reconnect to receive a fresh snapshot. */
  resync: boolean;
}

export function mergeRecent(current: InspectionOut[], incoming: InspectionOut[]): InspectionOut[] {
  const byId = new Map<number, InspectionOut>();
  for (const item of [...incoming, ...current]) {
    if (!byId.has(item.id)) byId.set(item.id, item);
  }
  return [...byId.values()].sort((a, b) => b.id - a.id).slice(0, RECENT_LIMIT);
}

function patchRecent(
  recent: InspectionOut[],
  match: (item: InspectionOut) => boolean,
  patch: Partial<InspectionOut>,
): InspectionOut[] {
  return recent.map((item) => (match(item) ? { ...item, ...patch } : item));
}

function withStatus(state: LiveState, patch: (status: SystemStatus) => SystemStatus): LiveState {
  return state.status ? { ...state, status: patch(state.status) } : state;
}

export function applyEvent(state: LiveState, event: WsEvent): Outcome {
  if (event.type === "SNAPSHOT") {
    const lotChanged = state.status?.active_lot?.id !== event.data.active_lot?.id;
    return {
      state: {
        ...state,
        status: event.data,
        // A broadcast snapshot carries the seq captured before the server read its state, so it
        // can arrive after newer events. Never move the cursor back, or the next event looks
        // like a gap and the client reconnects in a loop.
        seq: Math.max(state.seq, event.seq),
        recent: lotChanged ? [] : state.recent,
        lastFault: event.data.machine.fault ? state.lastFault : null,
      },
      resync: false,
    };
  }
  if (event.seq <= state.seq) return { state, resync: false };
  if (state.status === null || event.seq !== state.seq + 1) return { state, resync: true };

  const next: LiveState = { ...state, seq: event.seq };
  switch (event.type) {
    case "STATE_CHANGED": {
      const { from_state, to_state, fault } = event.data;
      return {
        state: withStatus(next, (s) => ({
          ...s,
          machine: {
            ...s.machine,
            state: to_state,
            fault: to_state === "FAULT" ? (fault ?? s.machine.fault) : from_state === "FAULT" ? null : s.machine.fault,
          },
        })),
        resync: false,
      };
    }
    case "SENSOR_CHANGED": {
      const key = event.data.sensor.toLowerCase() as "s1" | "s2" | "estop";
      return {
        state: withStatus(next, (s) => ({
          ...s,
          machine: {
            ...s.machine,
            sensors: { ...(s.machine.sensors ?? { s1: false, s2: false, estop: false }), [key]: event.data.active },
          },
        })),
        resync: false,
      };
    }
    case "INSPECTION_READY":
      return { state: { ...next, recent: mergeRecent(next.recent, [event.data]) }, resync: false };
    case "DECISION_ACCEPTED": {
      const { inspection_id, destination, decided_by } = event.data;
      const updated = {
        ...next,
        recent: patchRecent(next.recent, (i) => i.id === inspection_id, {
          final_decision: destination,
          decided_by,
        }),
      };
      return {
        state: withStatus(updated, (s) => ({
          ...s,
          machine: {
            ...s.machine,
            pending_review_inspection_id:
              s.machine.pending_review_inspection_id === inspection_id ? null : s.machine.pending_review_inspection_id,
          },
        })),
        resync: false,
      };
    }
    case "CYCLE_COMPLETED":
    case "CYCLE_ABORTED": {
      const cycleStatus = event.type === "CYCLE_COMPLETED" ? "completed" : "aborted";
      const updated = {
        ...next,
        recent: patchRecent(next.recent, (i) => i.cycle_id === event.cycle_id, { cycle_status: cycleStatus }),
      };
      return {
        state: withStatus(updated, (s) =>
          s.active_lot?.id === event.lot_id ? { ...s, active_lot_summary: event.data.summary } : s,
        ),
        resync: false,
      };
    }
    case "LOT_UPDATED": {
      const { lot, summary } = event.data;
      return {
        state: withStatus(next, (s) => {
          if (lot.status === "open") return { ...s, active_lot: lot, active_lot_summary: summary };
          if (s.active_lot?.id === lot.id) return { ...s, active_lot: null, active_lot_summary: null };
          return s;
        }),
        resync: false,
      };
    }
    case "CONNECTION_LOST":
    case "CONNECTION_RESTORED": {
      const up = event.type === "CONNECTION_RESTORED";
      const { component, message } = event.data;
      const incident = up
        ? next.incident?.component === component
          ? null
          : next.incident
        : { component, message, at: event.at };
      return {
        state: withStatus({ ...next, incident }, (s) => {
          if (event.data.component === "device") {
            return { ...s, machine: { ...s.machine, link: { ...s.machine.link, connected: up } } };
          }
          if (event.data.component === "camera") {
            return { ...s, camera: { ...s.camera, status: up ? "ok" : "unavailable" } };
          }
          return s;
        }),
        resync: false,
      };
    }
    case "FAULT":
      return { state: { ...next, lastFault: event.data }, resync: false };
  }
}
