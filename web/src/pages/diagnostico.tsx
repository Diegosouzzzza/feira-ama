import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronLeft, ChevronRight, TriangleAlert, Wrench } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { Equipment } from "@/components/station/equipment";
import { NeedControl, PageShell, useStation } from "@/components/station/page-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { apiGet } from "@/lib/api/client";
import type { EventOut, EventSource, MachineCommandResult, SerialPortOut, Severity, SystemStatus } from "@/lib/api/types";
import { controlPost } from "@/lib/control";
import { formatDateTime, formatTime } from "@/lib/format";
import { MACHINE_STATE } from "@/lib/labels";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 50;
const ALL = "all";

const SEVERITY: Record<Severity, { label: string; tone: string }> = {
  info: { label: "Informação", tone: "bg-muted text-foreground" },
  warning: { label: "Atenção", tone: "bg-grade-b-soft text-grade-b" },
  error: { label: "Erro", tone: "bg-grade-c-soft text-grade-c" },
};

const SOURCE: Record<EventSource, string> = {
  device: "Placa",
  host: "Serviço",
  operator: "Operador",
};

// ---------------------------------------------------------------- live sensors

function Signal({ name, on, onText, offText, danger = false }: { name: string; on: boolean; onText: string; offText: string; danger?: boolean }) {
  return (
    <div className={cn("rounded-lg border p-3", on && (danger ? "border-grade-c bg-grade-c-soft" : "border-primary bg-primary/10"))}>
      <p className="text-sm text-muted-foreground">{name}</p>
      <p className={cn("font-wide text-lg font-semibold", on && danger && "text-grade-c")}>{on ? onText : offText}</p>
    </div>
  );
}

function MachinePanel({ status }: { status: SystemStatus }) {
  const { machine } = status;
  const sensors = machine.sensors;
  return (
    <section aria-labelledby="machine-title" className="space-y-4 rounded-lg border bg-card p-4">
      <h2 id="machine-title" className="font-wide text-lg font-semibold">
        Máquina
      </h2>
      <dl className="grid grid-cols-2 gap-x-6 gap-y-2 text-sm">
        <div>
          <dt className="text-muted-foreground">Estado</dt>
          <dd className="font-semibold">{machine.state ? MACHINE_STATE[machine.state] : "Sem comunicação"}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Porta</dt>
          <dd className="font-semibold">{machine.link.port ?? "—"}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Sessão da placa</dt>
          <dd className="font-mono">{machine.link.boot_id ?? "—"}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Última mensagem</dt>
          <dd className="font-semibold tabular-nums">{formatTime(machine.link.last_seen_at)}</dd>
        </div>
      </dl>
      {machine.fault && (
        <p className="flex items-start gap-2 rounded-md bg-grade-c-soft p-3 text-sm text-grade-c">
          <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
          <span>
            <strong className="font-semibold">{machine.fault_message ?? machine.fault}</strong>
            {machine.fault_recovery && <span className="block">{machine.fault_recovery}</span>}
          </span>
        </p>
      )}
      <div className="grid grid-cols-3 gap-2" aria-live="polite">
        <Signal name="Sensor S1 (câmera)" on={Boolean(sensors?.s1)} onText="Peça" offText="Livre" />
        <Signal name="Sensor S2 (separação)" on={Boolean(sensors?.s2)} onText="Peça" offText="Livre" />
        <Signal name="Emergência" on={Boolean(sensors?.estop)} onText="Acionada" offText="Normal" danger />
      </div>
    </section>
  );
}

// ---------------------------------------------------------------- serial ports

function SerialPortsPanel({ connected }: { connected: boolean }) {
  const ports = useQuery({
    queryKey: ["serial-ports"],
    queryFn: ({ signal }) => apiGet<SerialPortOut[]>("/diagnostics/serial-ports", { signal }),
    refetchInterval: connected ? false : 4000,
  });
  if (connected) return null;
  return (
    <section aria-labelledby="serial-title" className="space-y-3 rounded-lg border bg-card p-4">
      <h2 id="serial-title" className="font-wide text-lg font-semibold">
        Portas USB disponíveis
      </h2>
      <p className="text-sm text-muted-foreground">
        A placa não está respondendo. Encontre a porta da placa aqui e coloque-a em{" "}
        <code className="rounded bg-muted px-1 py-0.5">AV_SERIAL_PORT</code> no <code className="rounded bg-muted px-1 py-0.5">api/.env</code>,
        depois reinicie o serviço.
      </p>
      {ports.isPending ? (
        <p className="text-sm text-muted-foreground">Procurando portas…</p>
      ) : (ports.data ?? []).length === 0 ? (
        <p className="text-sm text-muted-foreground">Nenhuma porta USB encontrada. Confira o cabo.</p>
      ) : (
        <ul className="space-y-1.5 text-sm">
          {ports.data?.map((port) => (
            <li key={port.device} className="flex items-center gap-2 rounded-md border px-3 py-1.5">
              <span className="font-mono font-semibold">{port.device}</span>
              <span className="text-muted-foreground">{port.description ?? "sem descrição"}</span>
              {port.in_use && <span className="ml-auto text-xs font-medium text-review">configurada, sem resposta</span>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- maintenance

function MaintenancePanel({ status, controller }: { status: SystemStatus; controller: boolean }) {
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState(false);
  const [runMs, setRunMs] = useState("1000");
  const [angle, setAngle] = useState("75");
  const [holdMs, setHoldMs] = useState("1000");
  const inMaintenance = status.machine.state === "MAINTENANCE";
  const busyMachine = status.machine.running || status.current_cycle !== null;

  async function send(path: string, body: Record<string, unknown>, done: string) {
    setBusy(true);
    try {
      await controlPost<MachineCommandResult>(`/machine/maintenance/${path}`, {
        request_id: crypto.randomUUID(),
        ...body,
      });
      toast.success(done);
      await queryClient.invalidateQueries({ queryKey: ["events"] });
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  const run = Number(runMs);
  const deg = Number(angle);
  const hold = Number(holdMs);
  const runOk = Number.isInteger(run) && run >= 100 && run <= 5000;
  const servoOk = Number.isInteger(deg) && deg >= 0 && deg <= 180 && Number.isInteger(hold) && hold >= 0 && hold <= 5000;

  return (
    <section aria-labelledby="maint-title" className="space-y-4 rounded-lg border bg-card p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="maint-title" className="font-wide flex items-center gap-2 text-lg font-semibold">
          <Wrench className="size-5" aria-hidden />
          Testes manuais
        </h2>
        {controller &&
          (inMaintenance ? (
            <Button variant="outline" disabled={busy} onClick={() => void send("exit", {}, "Saiu da manutenção.")}>
              Sair da manutenção
            </Button>
          ) : (
            <Button
              disabled={busy || busyMachine || !status.machine.link.connected}
              onClick={() => void send("enter", {}, "Modo manutenção ativo.")}
            >
              Entrar em manutenção
            </Button>
          ))}
      </div>
      {!controller ? (
        <NeedControl action="fazer testes manuais" />
      ) : !inMaintenance ? (
        <p className="text-sm text-muted-foreground">
          {busyMachine
            ? "Pare a máquina na tela de Operação para entrar em manutenção."
            : "Em manutenção a máquina fica desarmada e só aceita os testes abaixo. Retire peças da esteira antes."}
        </p>
      ) : (
        <>
          <p className="flex items-start gap-2 rounded-md bg-grade-b-soft p-3 text-sm text-grade-b">
            <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
            Os testes movem a esteira e o desviador. Mantenha as mãos longe e o botão de emergência ao alcance.
          </p>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2 rounded-md border p-3">
              <p className="font-medium">Motor da esteira</p>
              <div className="space-y-1.5">
                <Label htmlFor="run-ms">Tempo ligado (ms, 100 a 5000)</Label>
                <Input id="run-ms" inputMode="numeric" value={runMs} aria-invalid={!runOk} onChange={(e) => setRunMs(e.target.value)} />
              </div>
              <Button
                variant="outline"
                disabled={busy || !runOk}
                onClick={() => void send("test-motor", { run_ms: run }, "Motor ligado pelo tempo pedido.")}
              >
                Ligar a esteira
              </Button>
            </div>
            <div className="space-y-2 rounded-md border p-3">
              <p className="font-medium">Servo do desviador</p>
              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1.5">
                  <Label htmlFor="servo-angle">Ângulo (0 a 180°)</Label>
                  <Input id="servo-angle" inputMode="numeric" value={angle} onChange={(e) => setAngle(e.target.value)} />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="servo-hold">Segurar (ms)</Label>
                  <Input id="servo-hold" inputMode="numeric" value={holdMs} onChange={(e) => setHoldMs(e.target.value)} />
                </div>
              </div>
              <Button
                variant="outline"
                disabled={busy || !servoOk}
                aria-invalid={!servoOk}
                onClick={() =>
                  void send("test-servo", { angle_deg: deg, hold_ms: hold }, "Servo movido; volta ao repouso sozinho.")
                }
              >
                Mover o servo
              </Button>
            </div>
          </div>
        </>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- event log

function EventLog() {
  const [severity, setSeverity] = useState<string>(ALL);
  const [source, setSource] = useState<string>(ALL);
  const [page, setPage] = useState(0);
  const params = new URLSearchParams({ limit: String(PAGE_SIZE + 1), offset: String(page * PAGE_SIZE) });
  if (severity !== ALL) params.set("severity", severity);
  if (source !== ALL) params.set("source", source);
  const events = useQuery({
    queryKey: ["events", params.toString()],
    queryFn: ({ signal }) => apiGet<EventOut[]>(`/diagnostics/events?${params}`, { signal }),
    refetchInterval: page === 0 ? 5000 : false,
    placeholderData: (previous) => previous,
  });
  const items = (events.data ?? []).slice(0, PAGE_SIZE);
  const hasMore = (events.data?.length ?? 0) > PAGE_SIZE;

  return (
    <section aria-labelledby="events-title" className="space-y-3">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <h2 id="events-title" className="font-wide text-xl font-semibold">
          Registro de eventos
        </h2>
        <div className="flex flex-wrap gap-2">
          <div className="space-y-1">
            <Label htmlFor="ev-severity" className="text-xs">Gravidade</Label>
            <Select value={severity} onValueChange={(v) => { setSeverity(v); setPage(0); }}>
              <SelectTrigger id="ev-severity" className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>Todas</SelectItem>
                {(Object.keys(SEVERITY) as Severity[]).map((s) => (
                  <SelectItem key={s} value={s}>
                    {SEVERITY[s].label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1">
            <Label htmlFor="ev-source" className="text-xs">Origem</Label>
            <Select value={source} onValueChange={(v) => { setSource(v); setPage(0); }}>
              <SelectTrigger id="ev-source" className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>Todas</SelectItem>
                {(Object.keys(SOURCE) as EventSource[]).map((s) => (
                  <SelectItem key={s} value={s}>
                    {SOURCE[s]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
      {events.isPending ? (
        <p className="text-muted-foreground">Carregando…</p>
      ) : items.length === 0 ? (
        <p className="rounded-lg border border-dashed p-6 text-center text-muted-foreground">Nenhum evento.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg border bg-card">
          <table className="w-full min-w-[40rem] text-sm">
            <thead className="border-b bg-muted/50 text-left text-muted-foreground">
              <tr>
                <th scope="col" className="px-3 py-2 font-medium">Quando</th>
                <th scope="col" className="px-3 py-2 font-medium">Gravidade</th>
                <th scope="col" className="px-3 py-2 font-medium">Origem</th>
                <th scope="col" className="px-3 py-2 font-medium">Evento</th>
                <th scope="col" className="px-3 py-2 font-medium">Detalhes</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {items.map((event) => (
                <tr key={event.id}>
                  <td className="px-3 py-2 whitespace-nowrap tabular-nums">{formatDateTime(event.occurred_at)}</td>
                  <td className="px-3 py-2">
                    <span className={cn("rounded px-1.5 py-0.5 text-xs font-medium", SEVERITY[event.severity].tone)}>
                      {SEVERITY[event.severity].label}
                    </span>
                  </td>
                  <td className="px-3 py-2">{SOURCE[event.source]}</td>
                  <td className="px-3 py-2 font-mono text-xs">{event.type}</td>
                  <td className="max-w-md px-3 py-2 font-mono text-xs break-all text-muted-foreground">
                    {[event.lot_id && `lote ${event.lot_id}`, event.cycle_id && `ciclo ${event.cycle_id}`, Object.keys(event.data).length > 0 && JSON.stringify(event.data)]
                      .filter(Boolean)
                      .join(" · ")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {(page > 0 || hasMore) && (
        <div className="flex items-center justify-center gap-3">
          <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage((p) => p - 1)}>
            <ChevronLeft aria-hidden />
            Mais recentes
          </Button>
          <span className="text-sm text-muted-foreground">Página {page + 1}</span>
          <Button variant="outline" size="sm" disabled={!hasMore} onClick={() => setPage((p) => p + 1)}>
            Mais antigos
            <ChevronRight aria-hidden />
          </Button>
        </div>
      )}
    </section>
  );
}

export function DiagnosticoPage() {
  const { status, controller } = useStation();
  return (
    <PageShell
      title="Diagnóstico"
      intro="Estado dos equipamentos em tempo real, testes manuais da esteira e do desviador, e o registro de tudo o que aconteceu."
    >
      {status ? (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <MachinePanel status={status} />
          <Equipment status={status} />
          <SerialPortsPanel connected={status.machine.link.connected} />
          <MaintenancePanel status={status} controller={controller} />
        </div>
      ) : (
        <p className="text-muted-foreground">Aguardando o estado do serviço…</p>
      )}
      <EventLog />
    </PageShell>
  );
}
