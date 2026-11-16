import type { AnomalyRegionOut, Grade, InspectionOut } from "@/lib/api/types";
import { formatPercent } from "@/lib/format";

const ANOMALY_ROWS: { grade: Extract<Grade, "A" | "C">; label: string }[] = [
  { grade: "A", label: "Dentro do padrão (A)" },
  { grade: "C", label: "Fora do padrão (C)" },
];

export function isAnomalyModelId(modelId: string | null | undefined): boolean {
  if (!modelId) return false;
  return modelId.includes("-anomalia-") || modelId.startsWith("anomalia");
}

export function isAnomalyModel(
  model: { architecture: string } | null | undefined,
  modelId?: string | null,
): boolean {
  return Boolean(model?.architecture.startsWith("anomalia") || isAnomalyModelId(modelId));
}

export function anomalyScoreRows(
  scores: Record<string, number>,
): { grade: Grade; label: string; score: number }[] {
  return ANOMALY_ROWS.map((row) => ({
    grade: row.grade,
    label: row.label,
    score: scores[row.grade] ?? 0,
  }));
}

/** Avoids showing the fixed `-30` logit Class B (always ~0%) on anomaly models. */
export function formatModelScoresText(scores: Record<string, number>, anomaly: boolean): string {
  if (anomaly) {
    return ANOMALY_ROWS.map((row) => `${row.label} ${formatPercent(scores[row.grade] ?? 0)}`).join(" · ");
  }
  return (["A", "B", "C"] as Grade[]).map((g) => `${g} ${formatPercent(scores[g] ?? 0)}`).join(" · ");
}

export function visibleAnomalyRegions(
  inspection: InspectionOut | null | undefined,
  enabled = true,
): AnomalyRegionOut[] {
  if (!enabled || !inspection?.anomaly_regions?.length) return [];
  if (inspection.final_decision === "APPROVED") return [];
  return inspection.anomaly_regions;
}
