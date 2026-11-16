import type { Destination, InspectionOut, MachineState, SystemStatus } from "@/lib/api/types";

/** Where the piece is on the belt, derived from the machine state reported by the board. */
export type PiecePosition =
  | "none"
  | "to-camera"
  | "at-camera"
  | "to-sorter"
  | "at-sorter"
  | "leaving";

export function piecePosition(state: MachineState | null | undefined): PiecePosition {
  switch (state) {
    case "TO_S1":
      return "to-camera";
    case "SETTLING":
    case "INSPECTING":
    case "REVIEW_HOLD":
      return "at-camera";
    case "TO_S2":
      return "to-sorter";
    case "SORTING":
      return "at-sorter";
    case "RELEASING":
      return "leaving";
    default:
      return "none";
  }
}

/** Latest inspection, if it belongs to the cycle on the belt right now. */
export function currentInspection(
  status: SystemStatus | null,
  recent: InspectionOut[],
): InspectionOut | null {
  const cycleId = status?.current_cycle?.id;
  const latest = recent[0];
  return cycleId !== undefined && latest?.cycle_id === cycleId ? latest : null;
}

/** Destination already decided for the piece on the belt (null while undecided). */
export function decidedDestination(
  status: SystemStatus | null,
  recent: InspectionOut[],
): Destination | null {
  return currentInspection(status, recent)?.final_decision ?? null;
}

export type StationHealth = "ok" | "attention" | "blocked";

export interface Blocker {
  id: string;
  title: string;
  detail: string | null;
  severity: "fault" | "warning" | "review";
}

/** Everything that currently stops or limits the operation, most severe first. */
export function blockers(status: SystemStatus | null): Blocker[] {
  if (!status) return [];
  const list: Blocker[] = [];
  const { machine, camera, model, storage } = status;
  if (machine.state === "ESTOP") {
    list.push({
      id: "estop",
      title: "Botão de emergência acionado",
      detail: "Solte o botão e use Rearmar para voltar a operar.",
      severity: "fault",
    });
  }
  if (machine.state === "FAULT") {
    list.push({
      id: "fault",
      title: machine.fault_message ?? "A máquina está em falha",
      detail: machine.fault_recovery ?? null,
      severity: "fault",
    });
  }
  if (!machine.link.connected) {
    list.push({
      id: "device",
      title: "Placa da esteira sem comunicação",
      detail: "Verifique o cabo USB e a alimentação da placa.",
      severity: "fault",
    });
  }
  if (storage.status === "error") {
    list.push({
      id: "storage",
      title: "Falha ao gravar dados",
      detail: "Novos ciclos estão bloqueados. Verifique o espaço em disco e reinicie o sistema.",
      severity: "fault",
    });
  } else if (storage.status === "low_space") {
    list.push({
      id: "storage-low",
      title: "Pouco espaço em disco",
      detail: "Libere espaço antes de continuar operando por muito tempo.",
      severity: "warning",
    });
  }
  if (camera.status !== "ok") {
    list.push({
      id: "camera",
      title: camera.status === "stale" ? "Imagem da câmera parada" : "Câmera indisponível",
      detail: "Confira a conexão da câmera.",
      severity: "warning",
    });
  }
  if (status.active_lot && model.status !== "ready") {
    list.push({
      id: "model",
      title: "Modelo do produto não carregado",
      detail: "Encerre e abra o lote de novo, ou confira os modelos instalados.",
      severity: "warning",
    });
  }
  return list;
}
