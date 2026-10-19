import { Pause, Play, RotateCcw, Square, UserRound } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { LotOut, MachineCommandResult, MachineState, SystemStatus } from "@/lib/api/types";
import { controlPost, useControl } from "@/lib/control";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";

type Action = "start" | "pause" | "stop" | "rearm";

const CYCLE: MachineState[] = ["TO_S1", "SETTLING", "INSPECTING", "REVIEW_HOLD", "TO_S2", "SORTING", "RELEASING"];

export function startBlockedReason(status: SystemStatus): string | null {
  const { machine } = status;
  if (!status.active_lot) return "Abra um lote para iniciar.";
  if (!machine.link.connected) return "A placa está sem comunicação.";
  if (machine.state === "ESTOP") return "Solte o botão de emergência e use Rearmar.";
  if (machine.state === "FAULT") return "Resolva a falha e use Rearmar.";
  if (machine.state === "MAINTENANCE") return "A máquina está em manutenção.";
  if (machine.pending_review_inspection_id !== null) return "Decida a peça que aguarda revisão.";
  if (status.storage.status === "error") return "A gravação de dados está com falha.";
  if (status.model.status !== "ready") return "O modelo do produto não está carregado.";
  if (status.camera.status !== "ok") return "A câmera está indisponível.";
  return null;
}

export function useIsController(status: SystemStatus | null): boolean {
  const { token, operator } = useControl();
  return Boolean(token && status && status.control_holder === operator);
}

export function ActionBar({ status, onNeedControl }: { status: SystemStatus; onNeedControl: () => void }) {
  const { operator, release } = useControl();
  const controller = useIsController(status);
  const [pending, setPending] = useState<Action | "close" | null>(null);
  const [confirmClose, setConfirmClose] = useState(false);
  const { machine } = status;
  const state = machine.state;
  const inCycle = state !== null && CYCLE.includes(state);
  const lot: LotOut | null = status.active_lot;

  async function run(action: Action) {
    setPending(action);
    try {
      await controlPost<MachineCommandResult>(`/machine/${action}`, { request_id: crypto.randomUUID() });
    } catch (error) {
      notifyError(error);
    } finally {
      setPending(null);
    }
  }

  async function closeLot() {
    if (!lot) return;
    setPending("close");
    try {
      await controlPost<LotOut>(`/lots/${lot.id}/close`);
      toast.success(`Lote ${lot.id} encerrado.`);
      setConfirmClose(false);
    } catch (error) {
      notifyError(error);
    } finally {
      setPending(null);
    }
  }

  const blocked = startBlockedReason(status);
  const can = {
    start: controller && !machine.running && blocked === null,
    pause: controller && machine.running,
    stop: controller && machine.link.connected && (inCycle || state === "READY" || state === "MAINTENANCE"),
    rearm:
      controller &&
      machine.link.connected &&
      !machine.running &&
      (state === "FAULT" || (state === "DISARMED" && lot !== null)),
    close: controller && lot !== null && !machine.running && status.current_cycle === null,
  };
  const hint = controller && !machine.running ? blocked : null;

  return (
    <div className="sticky bottom-0 z-10 border-t bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/85">
      <div className="mx-auto flex max-w-[120rem] flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <UserRound className="size-5 shrink-0 text-muted-foreground" aria-hidden />
          {controller ? (
            <p className="min-w-0 text-sm">
              Operando como <strong className="font-semibold">{operator}</strong>.{" "}
              <button type="button" className="text-muted-foreground underline underline-offset-2" onClick={() => void release()}>
                Liberar controle
              </button>
            </p>
          ) : (
            <p className="min-w-0 text-sm">
              {status.control_holder ? (
                <>
                  Controle com <strong className="font-semibold">{status.control_holder}</strong>. Esta tela só
                  acompanha.
                </>
              ) : (
                "Ninguém está operando. Esta tela só acompanha."
              )}{" "}
              <button type="button" className="font-medium text-primary underline underline-offset-2" onClick={onNeedControl}>
                {status.control_holder ? "Assumir o controle" : "Operar a estação"}
              </button>
            </p>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {hint && <p className="mr-2 hidden text-sm text-muted-foreground md:block">{hint}</p>}
          <Button size="lg" className="max-sm:h-9 max-sm:px-3" disabled={!can.start || pending !== null} onClick={() => void run("start")}>
            <Play aria-hidden />
            {pending === "start" ? "Iniciando…" : "Iniciar"}
          </Button>
          <Button size="lg" className="max-sm:h-9 max-sm:px-3" variant="outline" disabled={!can.pause || pending !== null} onClick={() => void run("pause")}>
            <Pause aria-hidden />
            Pausar
          </Button>
          <Button
            size="lg"
            variant="outline"
            disabled={!can.stop || pending !== null}
            onClick={() => void run("stop")}
            className={cn("max-sm:h-9 max-sm:px-3", can.stop && "border-grade-c text-grade-c hover:bg-grade-c-soft hover:text-grade-c")}
          >
            <Square aria-hidden />
            Parar
          </Button>
          <Button size="lg" className="max-sm:h-9 max-sm:px-3" variant="outline" disabled={!can.rearm || pending !== null} onClick={() => void run("rearm")}>
            <RotateCcw aria-hidden />
            Rearmar
          </Button>
          <Button size="lg" className="max-sm:h-9 max-sm:px-3" variant="ghost" disabled={!can.close || pending !== null} onClick={() => setConfirmClose(true)}>
            Encerrar lote
          </Button>
        </div>
      </div>

      <Dialog open={confirmClose} onOpenChange={setConfirmClose}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Encerrar o lote {lot?.id}?</DialogTitle>
            <DialogDescription>
              O histórico do lote fica guardado. Para inspecionar outro produto, abra um novo lote depois.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfirmClose(false)}>
              Continuar no lote
            </Button>
            <Button onClick={() => void closeLot()} disabled={pending === "close"}>
              Encerrar lote
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
