import { describe, expect, it } from "vitest";
import { toRoi, validate } from "@/lib/bench-fields";
import { filterParams } from "@/lib/history-filters";

const BENCH = {
  sensor_debounce_ms: "20",
  s1_timeout_ms: "15000",
  settle_ms: "400",
  decision_timeout_ms: "5000",
  s2_timeout_ms: "8000",
  servo_rest_deg: "10",
  servo_reject_deg: "75",
  reject_hold_ms: "600",
  reject_motor_ms: "800",
  release_ms: "1200",
  release_max_ms: "4000",
  link_timeout_ms: "2000",
  motor_power_pct: "",
  presentation: "",
  threshold: "0.8",
  roiEnabled: false,
  roiX: "0",
  roiY: "0",
  roiWidth: "100",
  roiHeight: "100",
};

describe("validate (Configuração)", () => {
  it("accepts the simulated bench defaults", () => {
    expect(validate(BENCH)).toEqual({});
  });

  it("uses the protocol limits and the coherence rules", () => {
    const errors = validate({
      ...BENCH,
      settle_ms: "9000",
      servo_reject_deg: "10",
      release_max_ms: "1000",
      threshold: "0,3",
      motor_power_pct: "0",
    });
    expect(Object.keys(errors).sort()).toEqual(
      ["motor_power_pct", "release_max_ms", "servo_reject_deg", "settle_ms", "threshold"].sort(),
    );
  });

  it("accepts a decimal comma in the threshold", () => {
    expect(validate({ ...BENCH, threshold: "0,85" })).toEqual({});
  });

  it("ignores the roi fields when disabled, converts null", () => {
    const draft = { ...BENCH, roiX: "not a number at all" };
    expect(validate(draft)).toEqual({});
    expect(toRoi(draft)).toBeNull();
  });

  it("validates the roi window when enabled, and converts to fractions", () => {
    const enabled = { ...BENCH, roiEnabled: true, roiX: "20", roiY: "10", roiWidth: "60", roiHeight: "80" };
    expect(validate(enabled)).toEqual({});
    expect(toRoi(enabled)).toEqual({ x: 0.2, y: 0.1, width: 0.6, height: 0.8 });

    const overflowing = { ...enabled, roiWidth: "85" }; // 20 + 85 > 100
    expect(Object.keys(validate(overflowing))).toEqual(["roiWidth"]);

    const zeroWidth = { ...enabled, roiWidth: "0" };
    expect(Object.keys(validate(zeroWidth))).toEqual(["roiWidth"]);
  });
});

describe("filterParams (Histórico)", () => {
  it("sends only the filters that are set", () => {
    const params = filterParams({ product: "all", lot: "", grade: "all", outcome: "all", from: "", to: "" });
    expect(params.toString()).toBe("");
  });

  it("makes the end day inclusive", () => {
    const params = filterParams({
      product: "tucuma",
      lot: "12",
      grade: "B",
      outcome: "pending_review",
      from: "2026-10-19",
      to: "2026-10-19",
    });
    expect(params.get("product_id")).toBe("tucuma");
    expect(params.get("lot_id")).toBe("12");
    expect(params.get("grade")).toBe("B");
    expect(params.get("outcome")).toBe("pending_review");
    const from = new Date(params.get("from") ?? "");
    const to = new Date(params.get("to") ?? "");
    expect(to.getTime() - from.getTime()).toBe(24 * 3600 * 1000);
  });
});
