import type { SystemStatus } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { cn } from "@/lib/utils";

type Level = "ok" | "warn" | "down" | "off";

const DOT: Record<Level, string> = {
  ok: "bg-grade-a",
  warn: "bg-grade-b",
  down: "bg-grade-c",
  off: "bg-stale",
};

function Row({ name, level, value, detail }: { name: string; level: Level; value: string; detail?: string }) {
  return (
    <div className="flex items-start gap-3 py-2">
      <span className={cn("mt-1.5 size-2.5 shrink-0 rounded-full", DOT[level])} aria-hidden />
      <dt className="w-28 shrink-0 text-muted-foreground">{name}</dt>
      <dd className="min-w-0">
        <span className="font-medium">{value}</span>
        {detail && <span className="block text-sm text-muted-foreground">{detail}</span>}
      </dd>
    </div>
  );
}

function gigabytes(bytes: number): string {
  return `${(bytes / 1e9).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} GB livres`;
}

/** Equipment status as observed by the service; stale data is marked as such by the caller. */
export function Equipment({ status, className }: { status: SystemStatus; className?: string }) {
  const { machine, camera, model, storage, mode } = status;
  const link = machine.link;
  const sensors = machine.sensors;
  const simulated = mode === "simulado";

  return (
    <section aria-labelledby="equipment-heading" className={cn("rounded-lg border bg-card p-4", className)}>
      <h2 id="equipment-heading" className="font-wide font-semibold">
        Equipamentos
      </h2>
      <dl className="mt-1 divide-y">
        <Row
          name="Placa"
          level={link.connected ? "ok" : "down"}
          value={link.connected ? (simulated ? "Simulada, conectada" : "Conectada") : "Sem comunicação"}
          detail={
            link.connected
              ? link.firmware_version
                ? `Firmware ${link.firmware_version}`
                : undefined
              : link.last_seen_at
                ? `Última mensagem às ${formatTime(link.last_seen_at)}`
                : "Nenhuma mensagem recebida"
          }
        />
        <Row
          name="Sensores"
          level={!sensors ? "off" : sensors.estop ? "down" : "ok"}
          value={
            sensors
              ? `S1 ${sensors.s1 ? "ocupado" : "livre"}, S2 ${sensors.s2 ? "ocupado" : "livre"}`
              : "Sem leitura"
          }
          detail={sensors?.estop ? "Emergência acionada" : undefined}
        />
        <Row
          name="Câmera"
          level={camera.status === "ok" ? "ok" : camera.status === "stale" ? "warn" : "down"}
          value={
            camera.status === "ok"
              ? simulated
                ? "Simulada"
                : "Capturando"
              : camera.status === "stale"
                ? "Imagem parada"
                : "Indisponível"
          }
          detail={camera.last_frame_at ? `Última foto às ${formatTime(camera.last_frame_at)}` : undefined}
        />
        <Row
          name="Modelo"
          level={model.status === "ready" ? "ok" : model.status === "error" ? "down" : "off"}
          value={
            model.status === "ready"
              ? (model.model_id ?? (simulated ? "Classificador simulado" : "Pronto"))
              : model.status === "loading"
                ? "Carregando"
                : model.status === "error"
                  ? "Com erro"
                  : "Não carregado"
          }
          detail={model.status === "not_loaded" ? "Carregado ao abrir um lote" : undefined}
        />
        <Row
          name="Gravação"
          level={storage.status === "ok" ? "ok" : storage.status === "low_space" ? "warn" : "down"}
          value={storage.status === "error" ? "Com falha" : storage.status === "low_space" ? "Pouco espaço" : "Normal"}
          detail={storage.free_bytes !== null ? gigabytes(storage.free_bytes) : undefined}
        />
      </dl>
    </section>
  );
}
