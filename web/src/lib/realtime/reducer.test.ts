import { describe, expect, it } from "vitest";
import type { InspectionOut, LotSummary, SystemStatus, WsEvent } from "@/lib/api/types";
import { applyEvent, initialLive, type LiveState, mergeRecent, RECENT_LIMIT } from "./reducer";

const AT = "2026-10-19T12:00:00Z";

const summary = (inspected: number): LotSummary => ({
  lot_id: 1,
  inspected,
  approved: inspected,
  rejected: 0,
  review_pending: 0,
  reviewed: 0,
  by_grade: { A: inspected, B: 0, C: 0 },
  cycles_completed: inspected,
  cycles_aborted: 0,
  approval_rate: inspected ? 1 : null,
  approval_rate_denominator: inspected,
});

const status = (overrides: Partial<SystemStatus> = {}): SystemStatus => ({
  mode: "simulado",
  generated_at: AT,
  state_version: 1,
  machine: {
    state: "READY",
    fault: null,
    fault_message: null,
    fault_recovery: null,
    sensors: { s1: false, s2: false, estop: false },
    link: { connected: true, port: "simulador", boot_id: "b0071d2e", firmware_version: "sim", last_seen_at: AT },
    running: true,
    pending_review_inspection_id: null,
  },
  camera: { status: "ok", source: "simulada", last_frame_at: null },
  model: { status: "ready", model_id: null, product_id: "tucuma" },
  storage: { status: "ok", free_bytes: 1 },
  control_locked: false,
  control_holder: null,
  active_lot: {
    id: 1,
    product_id: "tucuma",
    model_id: null,
    operator: "Ana",
    status: "open",
    is_simulated: true,
    started_at: AT,
    ended_at: null,
    notes: null,
  },
  active_lot_summary: summary(0),
  current_cycle: null,
  ...overrides,
});

const inspection = (id: number, cycle_id = id): InspectionOut => ({
  id,
  cycle_id,
  lot_id: 1,
  product_id: "tucuma",
  captured_at: AT,
  image_url: `/api/inspections/${id}/image`,
  model_id: null,
  predicted_grade: "A",
  scores: { A: 0.9, B: 0.05, C: 0.05 },
  confidence: 0.9,
  latency_ms: 1,
  auto_decision: "APPROVED",
  review_reason: null,
  final_decision: "APPROVED",
  decided_by: "auto",
  cycle_status: "running",
});

const base = { at: AT, state_version: 2, lot_id: 1, cycle_id: null };

function snapshot(seq: number, data = status()): WsEvent {
  return { ...base, type: "SNAPSHOT", seq, data };
}

function run(state: LiveState, ...events: WsEvent[]): { state: LiveState; resyncs: number } {
  let resyncs = 0;
  for (const event of events) {
    const out = applyEvent(state, event);
    state = out.state;
    if (out.resync) resyncs += 1;
  }
  return { state, resyncs };
}

describe("applyEvent", () => {
  it("starts from a snapshot and applies consecutive events", () => {
    const { state, resyncs } = run(
      initialLive,
      snapshot(4),
      { ...base, type: "STATE_CHANGED", seq: 5, data: { from_state: "READY", to_state: "TO_S1", trigger: "START_CYCLE", fault: null } },
      { ...base, type: "INSPECTION_READY", seq: 6, data: inspection(10) },
    );
    expect(resyncs).toBe(0);
    expect(state.seq).toBe(6);
    expect(state.status?.machine.state).toBe("TO_S1");
    expect(state.recent.map((i) => i.id)).toEqual([10]);
  });

  it("asks for a resync when a seq is skipped", () => {
    const { resyncs, state } = run(
      initialLive,
      snapshot(4),
      { ...base, type: "INSPECTION_READY", seq: 6, data: inspection(10) },
    );
    expect(resyncs).toBe(1);
    expect(state.recent).toEqual([]);
  });

  it("ignores duplicates", () => {
    const event: WsEvent = { ...base, type: "INSPECTION_READY", seq: 5, data: inspection(10) };
    const { state, resyncs } = run(initialLive, snapshot(4), event, event);
    expect(resyncs).toBe(0);
    expect(state.recent).toHaveLength(1);
  });

  it("does not move back on a late broadcast snapshot (no reconnect loop)", () => {
    const { state, resyncs } = run(
      initialLive,
      snapshot(4),
      { ...base, type: "INSPECTION_READY", seq: 5, data: inspection(10) },
      snapshot(4),
      { ...base, type: "INSPECTION_READY", seq: 6, data: inspection(11) },
    );
    expect(resyncs).toBe(0);
    expect(state.seq).toBe(6);
    expect(state.recent.map((i) => i.id)).toEqual([11, 10]);
  });

  it("keeps recent items across snapshots of the same lot and clears them on lot change", () => {
    const withItem = run(initialLive, snapshot(1), { ...base, type: "INSPECTION_READY", seq: 2, data: inspection(3) }).state;
    expect(run(withItem, snapshot(2)).state.recent).toHaveLength(1);
    const otherLot = status({ active_lot: { ...status().active_lot!, id: 2 } });
    expect(run(withItem, snapshot(2, otherLot)).state.recent).toEqual([]);
  });

  it("updates decision, cycle outcome and summary", () => {
    const { state } = run(
      initialLive,
      snapshot(1, status({ machine: { ...status().machine, pending_review_inspection_id: 10 } })),
      { ...base, type: "INSPECTION_READY", seq: 2, data: { ...inspection(10, 7), final_decision: null, decided_by: null, auto_decision: "REVIEW" } },
      { ...base, type: "DECISION_ACCEPTED", seq: 3, data: { inspection_id: 10, destination: "REJECTED", decided_by: "operator" } },
      { ...base, type: "CYCLE_COMPLETED", seq: 4, cycle_id: 7, data: { destination: "REJECTED", summary: summary(1) } },
    );
    expect(state.recent[0]).toMatchObject({ final_decision: "REJECTED", decided_by: "operator", cycle_status: "completed" });
    expect(state.status?.machine.pending_review_inspection_id).toBeNull();
    expect(state.status?.active_lot_summary?.inspected).toBe(1);
  });

  it("tracks connection incidents and their recovery", () => {
    const lost = run(initialLive, snapshot(1), {
      ...base,
      type: "CONNECTION_LOST",
      seq: 2,
      data: { component: "camera", message: "Câmera desconectada" },
    }).state;
    expect(lost.incident?.component).toBe("camera");
    expect(lost.status?.camera.status).toBe("unavailable");
    const back = run(lost, {
      ...base,
      type: "CONNECTION_RESTORED",
      seq: 3,
      data: { component: "camera", message: "ok" },
    }).state;
    expect(back.incident).toBeNull();
    expect(back.status?.camera.status).toBe("ok");
  });

  it("closing the active lot clears it", () => {
    const closed = { ...status().active_lot!, status: "closed" as const, ended_at: AT };
    const { state } = run(initialLive, snapshot(1), {
      ...base,
      type: "LOT_UPDATED",
      seq: 2,
      data: { lot: closed, summary: summary(0) },
    });
    expect(state.status?.active_lot).toBeNull();
  });
});

describe("mergeRecent", () => {
  it("dedupes by id, sorts newest first and caps the list", () => {
    const many = Array.from({ length: 20 }, (_, i) => inspection(i + 1));
    const merged = mergeRecent([inspection(3)], many);
    expect(merged).toHaveLength(RECENT_LIMIT);
    expect(merged[0]?.id).toBe(20);
    expect(new Set(merged.map((i) => i.id)).size).toBe(RECENT_LIMIT);
  });
});
