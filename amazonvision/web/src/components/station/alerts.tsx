import { CircleAlert, OctagonAlert, TriangleAlert, Unplug, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { formatTime } from "@/lib/format";
import { useLive } from "@/lib/realtime/store";
import { blockers } from "@/lib/station";
import { cn } from "@/lib/utils";

const COMPONENT: Record<string, string> = {
  device: "Placa",
  camera: "Câmera",
  model: "Modelo",
  storage: "Gravação",
};

/** Service link lost: what is on screen is the last information received, not live. */
export function ConnectionBanner({ className }: { className?: string }) {
  const connection = useLive((s) => s.connection);
  const receivedAt = useLive((s) => s.receivedAt);
  if (connection === "open") return null;
  return (
    <div role="status" className={cn("flex items-start gap-3 bg-stale px-4 py-3 text-white", className)}>
      <Unplug className="mt-0.5 size-5 shrink-0" aria-hidden />
      <p>
        <strong className="font-semibold">Sem conexão com o serviço local.</strong>{" "}
        {receivedAt
          ? `Os dados na tela são a última informação recebida, às ${formatTime(receivedAt)}.`
          : "Ainda não chegou nenhuma informação."}{" "}
        Tentando reconectar.
      </p>
    </div>
  );
}

export function StationAlerts({ className }: { className?: string }) {
  const status = useLive((s) => s.status);
  const rawIncident = useLive((s) => s.incident);
  const dismiss = useLive((s) => s.dismissIncident);
  // Device link problems already appear as a blocker; incidents cover host-side stops.
  const incident = rawIncident?.component === "device" ? null : rawIncident;
  const list = blockers(status);
  if (list.length === 0 && !incident) return null;

  return (
    <div className={cn("space-y-2", className)}>
      {list.map((b) => {
        const Icon = b.id === "estop" ? OctagonAlert : b.severity === "fault" ? CircleAlert : TriangleAlert;
        return (
          <div
            key={b.id}
            role={b.severity === "fault" ? "alert" : "status"}
            className={cn(
              "flex items-start gap-3 rounded-md border px-4 py-3",
              b.severity === "fault"
                ? "border-fault/30 bg-fault-soft text-fault"
                : "border-grade-b/30 bg-grade-b-soft text-grade-b",
            )}
          >
            <Icon className="mt-0.5 size-5 shrink-0" aria-hidden />
            <div>
              <p className="font-semibold">{b.title}</p>
              {b.detail && <p className="text-sm text-foreground/80">{b.detail}</p>}
            </div>
          </div>
        );
      })}
      {incident && (
        <div role="alert" className="flex items-start gap-3 rounded-md border border-fault/30 bg-fault-soft px-4 py-3 text-fault">
          <CircleAlert className="mt-0.5 size-5 shrink-0" aria-hidden />
          <div className="flex-1">
            <p className="font-semibold">
              {COMPONENT[incident.component] ?? "Equipamento"}: {incident.message}
            </p>
            <p className="text-sm text-foreground/80">
              A esteira foi parada às {formatTime(incident.at)}. Resolva a causa e use Rearmar.
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={dismiss} aria-label="Dispensar aviso" className="text-fault">
            <X className="size-4" />
          </Button>
        </div>
      )}
    </div>
  );
}
