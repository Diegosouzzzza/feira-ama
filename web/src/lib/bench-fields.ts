/** Bench calibration fields of the Configuração screen, with the protocol limits. */

import type { ConfigurePayload, ProductConfigOut, RoiOut } from "@/lib/api/types";

export type BenchKey = keyof ConfigurePayload;

export interface Field {
  key: BenchKey;
  label: string;
  unit: "ms" | "°" | "%";
  min: number;
  max: number;
  help: string;
  optional?: boolean;
}

/** Same limits as the serial protocol (api/.../machine/protocol.py, ConfigurePayload). */
export const BENCH_GROUPS: { title: string; fields: Field[] }[] = [
  {
    title: "Sensores e câmera",
    fields: [
      { key: "sensor_debounce_ms", label: "Filtro dos sensores", unit: "ms", min: 1, max: 200, help: "Tempo que o sinal precisa ficar estável para contar." },
      { key: "s1_timeout_ms", label: "Prazo até a câmera (S1)", unit: "ms", min: 500, max: 30000, help: "Sem peça em S1 nesse tempo: falha." },
      { key: "settle_ms", label: "Estabilização antes da foto", unit: "ms", min: 0, max: 5000, help: "Espera a peça parar de balançar." },
      { key: "decision_timeout_ms", label: "Prazo da decisão", unit: "ms", min: 500, max: 30000, help: "Tempo máximo para a análise chegar à placa." },
    ],
  },
  {
    title: "Separação",
    fields: [
      { key: "s2_timeout_ms", label: "Prazo até a separação (S2)", unit: "ms", min: 500, max: 30000, help: "Sem peça em S2 nesse tempo: falha." },
      { key: "servo_rest_deg", label: "Desviador em repouso", unit: "°", min: 0, max: 180, help: "Posição que deixa a peça seguir para aprovados." },
      { key: "servo_reject_deg", label: "Desviador na rejeição", unit: "°", min: 0, max: 180, help: "Posição que manda a peça para rejeitados." },
      { key: "reject_hold_ms", label: "Desviador aberto", unit: "ms", min: 100, max: 5000, help: "Quanto tempo o desviador fica na rejeição." },
      { key: "reject_motor_ms", label: "Esteira ligada na rejeição", unit: "ms", min: 0, max: 10000, help: "Empurra a peça para fora com o desviador aberto." },
    ],
  },
  {
    title: "Saída, comunicação e motor",
    fields: [
      { key: "release_ms", label: "Liberação da saída", unit: "ms", min: 0, max: 10000, help: "Esteira ligada para tirar a peça aprovada." },
      { key: "release_max_ms", label: "Prazo máximo da liberação", unit: "ms", min: 500, max: 30000, help: "Saída ainda ocupada depois disso: falha." },
      { key: "link_timeout_ms", label: "Tempo sem comunicação", unit: "ms", min: 500, max: 10000, help: "A placa para tudo se o computador ficar mudo." },
      { key: "motor_power_pct", label: "Potência do motor", unit: "%", min: 1, max: 100, help: "Só para driver com velocidade (BTS7960). Vazio: potência total.", optional: true },
    ],
  },
];

export const FIELDS = BENCH_GROUPS.flatMap((g) => g.fields);

export const ROI_KEYS = ["roiX", "roiY", "roiWidth", "roiHeight"] as const;
export type RoiKey = (typeof ROI_KEYS)[number];
const ROI_LABEL: Record<RoiKey, string> = {
  roiX: "da esquerda",
  roiY: "do topo",
  roiWidth: "largura",
  roiHeight: "altura",
};

export type Draft = Record<BenchKey, string> &
  Record<RoiKey, string> & { presentation: string; threshold: string; roiEnabled: boolean };

/** Round-trips cleanly: 0.6 -> "60" -> 0.6, never 59.999999999999996. */
function toPercent(fraction: number): string {
  return (Math.round(fraction * 1000) / 10).toString();
}

export function toDraft(config: ProductConfigOut): Draft {
  const bench = Object.fromEntries(
    FIELDS.map((f) => [f.key, config.bench[f.key] === null || config.bench[f.key] === undefined ? "" : String(config.bench[f.key])]),
  ) as Record<BenchKey, string>;
  const roi = config.roi;
  return {
    ...bench,
    presentation: config.product.presentation ?? "",
    threshold: config.product.decision_threshold.toFixed(2).replace(".", ","),
    roiEnabled: roi !== null,
    roiX: roi ? toPercent(roi.x) : "0",
    roiY: roi ? toPercent(roi.y) : "0",
    roiWidth: roi ? toPercent(roi.width) : "100",
    roiHeight: roi ? toPercent(roi.height) : "100",
  };
}

/** Field errors in the operator's words; empty when the draft can be saved. */
export function validate(draft: Draft): Partial<Record<BenchKey | "threshold" | RoiKey, string>> {
  const errors: Partial<Record<BenchKey | "threshold" | RoiKey, string>> = {};
  for (const f of FIELDS) {
    const raw = draft[f.key].trim();
    if (raw === "" && f.optional) continue;
    const value = Number(raw);
    if (raw === "" || !Number.isInteger(value) || value < f.min || value > f.max) {
      errors[f.key] = `Use um número inteiro de ${f.min} a ${f.max}.`;
    }
  }
  if (!errors.servo_reject_deg && draft.servo_reject_deg === draft.servo_rest_deg) {
    errors.servo_reject_deg = "Tem que ser diferente da posição de repouso.";
  }
  if (!errors.release_max_ms && !errors.release_ms && Number(draft.release_max_ms) < Number(draft.release_ms)) {
    errors.release_max_ms = "Não pode ser menor que a liberação da saída.";
  }
  const threshold = Number(draft.threshold.replace(",", "."));
  if (!(threshold >= 0.4 && threshold <= 0.99)) errors.threshold = "Use um valor de 0,40 a 0,99.";

  if (draft.roiEnabled) {
    const values: Record<RoiKey, number> = {
      roiX: Number(draft.roiX),
      roiY: Number(draft.roiY),
      roiWidth: Number(draft.roiWidth),
      roiHeight: Number(draft.roiHeight),
    };
    for (const key of ROI_KEYS) {
      const value = values[key];
      if (!Number.isFinite(value) || value < 0 || value > 100 || (key.endsWith("Width") || key.endsWith("Height") ? value <= 0 : false)) {
        errors[key] = `Use um número de 0 a 100 (${ROI_LABEL[key]}).`;
      }
    }
    if (!errors.roiX && !errors.roiWidth && values.roiX + values.roiWidth > 100) {
      errors.roiWidth = "Posição + largura não pode passar de 100%.";
    }
    if (!errors.roiY && !errors.roiHeight && values.roiY + values.roiHeight > 100) {
      errors.roiHeight = "Posição + altura não pode passar de 100%.";
    }
  }
  return errors;
}

/** Null means "no crop": the API field this becomes when roiEnabled is false. */
export function toRoi(draft: Draft): RoiOut | null {
  if (!draft.roiEnabled) return null;
  return {
    x: Number(draft.roiX) / 100,
    y: Number(draft.roiY) / 100,
    width: Number(draft.roiWidth) / 100,
    height: Number(draft.roiHeight) / 100,
  };
}
