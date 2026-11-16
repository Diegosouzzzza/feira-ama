import { describe, expect, it } from "vitest";
import {
  anomalyScoreRows,
  formatModelScoresText,
  isAnomalyModel,
  isAnomalyModelId,
  visibleAnomalyRegions,
} from "@/lib/anomaly";
import type { InspectionOut } from "@/lib/api/types";

const BASE_INSPECTION: InspectionOut = {
  id: 1,
  lot_id: 1,
  cycle_id: 1,
  product_id: "castanha",
  captured_at: "2026-11-15T12:00:00Z",
  image_url: "/api/images/1",
  model_id: "castanha-anomalia-20261115-120000",
  latency_ms: 4.2,
  scores: { A: 0.12, B: 0, C: 0.88 },
  anomaly_regions: [{ x: 0.25, y: 0.3, width: 0.15, height: 0.15, intensity: 0.9 }],
  predicted_grade: "C",
  confidence: 0.88,
  auto_decision: "REJECTED",
  review_reason: null,
  final_decision: "REJECTED",
  decided_by: "auto",
  cycle_status: "completed",
};

describe("anomaly helpers", () => {
  it("identifies anomaly models from model_id or architecture", () => {
    expect(isAnomalyModelId("castanha-anomalia-20261115-120000")).toBe(true);
    expect(isAnomalyModelId("castanha-mobilenetv3-20261115")).toBe(false);
    expect(isAnomalyModelId(null)).toBe(false);
    expect(isAnomalyModel({ architecture: "anomalia_patch_knn_v1" }, null)).toBe(true);
    expect(isAnomalyModel(undefined, "castanha-anomalia-20261115-120000")).toBe(true);
  });

  it("hides class B on anomaly scores and keeps all three classes on supervised models", () => {
    const rows = anomalyScoreRows({ A: 0.94, B: 0, C: 0.06 });
    expect(rows.map((r) => r.grade)).toEqual(["A", "C"]);
    expect(formatModelScoresText({ A: 0.94, B: 0, C: 0.06 }, true)).not.toContain("B ");
    expect(formatModelScoresText({ A: 0.7, B: 0.2, C: 0.1 }, false)).toContain("B 20%");
  });

  it("shows anomaly regions only when enabled and inspection is not approved", () => {
    expect(visibleAnomalyRegions(BASE_INSPECTION, true)).toHaveLength(1);
    expect(visibleAnomalyRegions(BASE_INSPECTION, false)).toEqual([]);
    expect(
      visibleAnomalyRegions({ ...BASE_INSPECTION, final_decision: "APPROVED" }, true),
    ).toEqual([]);
  });
});
