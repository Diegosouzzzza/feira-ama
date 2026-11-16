import type { Destination, Grade, MachineState, ReviewReason } from "@/lib/api/types";

export const MACHINE_STATE: Record<MachineState, string> = {
  DISARMED: "Desarmada",
  READY: "Pronta",
  TO_S1: "Levando a peça à câmera",
  SETTLING: "Estabilizando a peça",
  INSPECTING: "Analisando a imagem",
  REVIEW_HOLD: "Aguardando revisão",
  TO_S2: "Levando à separação",
  SORTING: "Separando",
  RELEASING: "Liberando a saída",
  FAULT: "Em falha",
  ESTOP: "Emergência acionada",
  MAINTENANCE: "Em manutenção",
};

export type Tone = "a" | "b" | "c" | "review" | "fault" | "neutral";

export const GRADE: Record<Grade, { title: string; meaning: string; tone: Tone }> = {
  A: { title: "Classe A", meaning: "Dentro do padrão visual", tone: "a" },
  B: { title: "Classe B", meaning: "Defeito visual", tone: "b" },
  C: { title: "Classe C", meaning: "Refugo ou fora do padrão", tone: "c" },
};

export const DESTINATION: Record<Destination, string> = {
  APPROVED: "Aprovados",
  REJECTED: "Rejeitados",
};

export const REVIEW_REASON: Record<ReviewReason, string> = {
  LOW_CONFIDENCE: "Confiança abaixo do limite",
  AMBIGUOUS: "Duas classes empatadas",
  INVALID_IMAGE: "Imagem sem condições de análise",
};

export const PRODUCT_FALLBACK = "Produto";
