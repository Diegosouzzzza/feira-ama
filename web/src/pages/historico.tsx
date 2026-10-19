import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronLeft, ChevronRight, Download, UserCheck } from "lucide-react";
import { type FormEvent, useState } from "react";
import { toast } from "sonner";
import { GradeMark } from "@/components/station/grade-mark";
import { useProducts } from "@/components/station/lot-setup";
import { NeedControl, PageShell, useStation } from "@/components/station/page-shell";
import { TONE } from "@/components/station/tone";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { apiGet } from "@/lib/api/client";
import type {
  Destination,
  Grade,
  InspectionOut,
  InspectionOutcome,
  InspectionPage,
  LotSummary,
  ReviewOut,
} from "@/lib/api/types";
import { controlPost, useControl } from "@/lib/control";
import { formatDateTime, formatInt, formatPercent } from "@/lib/format";
import { GRADE, REVIEW_REASON } from "@/lib/labels";
import { notifyError } from "@/lib/notify";
import { ALL, EMPTY, type Filters, filterParams } from "@/lib/history-filters";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 25;
const GRADES: Grade[] = ["A", "B", "C"];

const OUTCOME: Record<InspectionOutcome, string> = {
  approved: "Aprovadas",
  rejected: "Rejeitadas",
  pending_review: "Aguardando revisão",
  inconclusive: "Inconclusivas",
  reviewed: "Revisadas por pessoa",
};

function decisionText(inspection: InspectionOut): { text: string; tone: string } {
  if (inspection.final_decision === null) {
    return inspection.cycle_status === "aborted"
      ? { text: "Ciclo interrompido", tone: "text-muted-foreground" }
      : { text: "Aguardando revisão", tone: "text-review" };
  }
  return {
    text: inspection.final_decision === "APPROVED" ? "Aprovada" : "Rejeitada",
    tone: inspection.final_decision === "APPROVED" ? "text-grade-a" : "text-grade-c",
  };
}

// ---------------------------------------------------------------- filters

function FilterBar({ value, onChange }: { value: Filters; onChange: (next: Filters) => void }) {
  const products = useProducts();
  const set = (patch: Partial<Filters>) => onChange({ ...value, ...patch });
  return (
    <section aria-label="Filtros" className="grid grid-cols-2 gap-3 rounded-lg border bg-card p-4 md:grid-cols-3 xl:grid-cols-6">
      <div className="space-y-1.5">
        <Label htmlFor="f-product">Produto</Label>
        <Select value={value.product} onValueChange={(product) => set({ product })}>
          <SelectTrigger id="f-product" className="w-full">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todos</SelectItem>
            {(products.data ?? []).map((p) => (
              <SelectItem key={p.id} value={p.id}>
                {p.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="f-lot">Lote</Label>
        <Input
          id="f-lot"
          inputMode="numeric"
          placeholder="Todos"
          value={value.lot}
          onChange={(e) => set({ lot: e.target.value.replace(/\D/g, "") })}
        />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="f-grade">Classe prevista</Label>
        <Select value={value.grade} onValueChange={(grade) => set({ grade })}>
          <SelectTrigger id="f-grade" className="w-full">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todas</SelectItem>
            {GRADES.map((g) => (
              <SelectItem key={g} value={g}>
                {GRADE[g].title}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="f-outcome">Decisão</Label>
        <Select value={value.outcome} onValueChange={(outcome) => set({ outcome })}>
          <SelectTrigger id="f-outcome" className="w-full">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>Todas</SelectItem>
            {(Object.keys(OUTCOME) as InspectionOutcome[]).map((o) => (
              <SelectItem key={o} value={o}>
                {OUTCOME[o]}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="f-from">De</Label>
        <Input id="f-from" type="date" value={value.from} onChange={(e) => set({ from: e.target.value })} />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="f-to">Até</Label>
        <Input id="f-to" type="date" value={value.to} min={value.from || undefined} onChange={(e) => set({ to: e.target.value })} />
      </div>
    </section>
  );
}

// ---------------------------------------------------------------- lot distribution

function LotDistribution({ lotId }: { lotId: string }) {
  const summary = useQuery({
    queryKey: ["lot-summary", lotId],
    queryFn: ({ signal }) => apiGet<LotSummary>(`/lots/${lotId}/summary`, { signal }),
    retry: false,
  });
  if (summary.isError) return <p className="text-sm text-muted-foreground">Lote {lotId} não encontrado.</p>;
  if (!summary.data) return null;
  const data = summary.data;
  const largest = Math.max(1, ...GRADES.map((g) => data.by_grade[g] ?? 0));
  return (
    <section aria-labelledby="dist-title" className="space-y-4 rounded-lg border bg-card p-4">
      <h2 id="dist-title" className="font-wide text-lg font-semibold">
        Lote {lotId}: classes previstas
      </h2>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-2" aria-hidden>
          {GRADES.map((g) => (
            <div key={g} className="flex items-center gap-3">
              <span className="font-display w-6 text-lg">{g}</span>
              <div className="h-6 flex-1 rounded bg-muted">
                <div
                  className={cn("h-full rounded", TONE[GRADE[g].tone].solid)}
                  style={{ width: `${((data.by_grade[g] ?? 0) / largest) * 100}%` }}
                />
              </div>
              <span className="w-10 text-right tabular-nums">{formatInt(data.by_grade[g] ?? 0)}</span>
            </div>
          ))}
        </div>
        <table className="w-full text-sm">
          <caption className="sr-only">Resumo do lote {lotId}</caption>
          <tbody className="divide-y">
            <tr>
              <th scope="row" className="py-1.5 text-left font-normal text-muted-foreground">Inspecionadas</th>
              <td className="text-right font-semibold tabular-nums">{formatInt(data.inspected)}</td>
            </tr>
            {GRADES.map((g) => (
              <tr key={g}>
                <th scope="row" className="py-1.5 text-left font-normal text-muted-foreground">{GRADE[g].title}</th>
                <td className="text-right font-semibold tabular-nums">{formatInt(data.by_grade[g] ?? 0)}</td>
              </tr>
            ))}
            <tr>
              <th scope="row" className="py-1.5 text-left font-normal text-muted-foreground">Aprovadas / rejeitadas</th>
              <td className="text-right font-semibold tabular-nums">
                {formatInt(data.approved)} / {formatInt(data.rejected)}
              </td>
            </tr>
            <tr>
              <th scope="row" className="py-1.5 text-left font-normal text-muted-foreground">Taxa de aprovação</th>
              <td className="text-right font-semibold tabular-nums">{formatPercent(data.approval_rate)}</td>
            </tr>
            <tr>
              <th scope="row" className="py-1.5 text-left font-normal text-muted-foreground">Revisadas por pessoa</th>
              <td className="text-right font-semibold tabular-nums">{formatInt(data.reviewed)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------- detail

function CorrectionForm({ inspection, onDone }: { inspection: InspectionOut; onDone: () => void }) {
  const queryClient = useQueryClient();
  const { operator } = useControl();
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const pending = inspection.final_decision === null;

  async function decide(event: FormEvent, decision: Destination) {
    event.preventDefault();
    if (reason.trim().length < 3 || !operator) return;
    setBusy(true);
    try {
      await controlPost<ReviewOut>(`/inspections/${inspection.id}/review`, {
        request_id: crypto.randomUUID(),
        decision,
        reviewer: operator,
        reason: reason.trim(),
      });
      toast.success(pending ? "Decisão registrada." : "Correção registrada. A previsão original foi mantida.");
      await queryClient.invalidateQueries({ queryKey: ["history"] });
      onDone();
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="space-y-3 rounded-md border p-3" onSubmit={(e) => e.preventDefault()}>
      <p className="font-medium">{pending ? "Decidir esta peça" : "Corrigir a decisão"}</p>
      {!pending && (
        <p className="text-sm text-muted-foreground">
          A correção fica registrada com seu nome e motivo. A peça não é movida.
        </p>
      )}
      <div className="space-y-1.5">
        <Label htmlFor="correction-reason">Motivo</Label>
        <Textarea id="correction-reason" value={reason} maxLength={200} onChange={(e) => setReason(e.target.value)} />
      </div>
      <div className="flex flex-wrap gap-2">
        {(["APPROVED", "REJECTED"] as Destination[]).map((d) => (
          <Button
            key={d}
            variant="outline"
            disabled={busy || reason.trim().length < 3 || inspection.final_decision === d}
            onClick={(e) => void decide(e, d)}
          >
            {d === "APPROVED" ? "Marcar como aprovada" : "Marcar como rejeitada"}
          </Button>
        ))}
      </div>
    </form>
  );
}

function DetailDialog({ inspection, onClose }: { inspection: InspectionOut | null; onClose: () => void }) {
  const { controller } = useStation();
  const products = useProducts();
  if (!inspection) return <Dialog open={false} />;
  const product = products.data?.find((p) => p.id === inspection.product_id)?.name ?? inspection.product_id;
  const decision = decisionText(inspection);
  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-h-[90dvh] overflow-y-auto sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle>Inspeção {inspection.id}</DialogTitle>
          <DialogDescription>
            {product}, lote {inspection.lot_id}, {formatDateTime(inspection.captured_at)}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-5 md:grid-cols-2">
          <img
            src={inspection.image_url}
            alt={`Foto analisada na inspeção ${inspection.id}`}
            className="aspect-[4/3] w-full rounded-md bg-muted object-contain"
          />
          <dl className="space-y-2 text-sm">
            <div className="flex items-center gap-3">
              <GradeMark inspection={inspection} size="sm" />
              <div>
                <dt className="text-muted-foreground">Classe prevista</dt>
                <dd className="font-semibold">
                  {inspection.predicted_grade ? GRADE[inspection.predicted_grade].title : "Sem previsão"}
                </dd>
              </div>
            </div>
            {inspection.scores && (
              <div>
                <dt className="text-muted-foreground">Escores do modelo</dt>
                <dd className="font-medium tabular-nums">
                  {GRADES.map((g) => `${g} ${formatPercent(inspection.scores?.[g] ?? 0)}`).join(" · ")}
                </dd>
              </div>
            )}
            {inspection.review_reason && (
              <div>
                <dt className="text-muted-foreground">Motivo da revisão</dt>
                <dd className="font-medium">{REVIEW_REASON[inspection.review_reason]}</dd>
              </div>
            )}
            <div>
              <dt className="text-muted-foreground">Decisão final</dt>
              <dd className={cn("font-semibold", decision.tone)}>
                {decision.text}
                {inspection.decided_by === "operator" && " (por pessoa)"}
              </dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Modelo</dt>
              <dd className="font-medium break-all">{inspection.model_id ?? "Classificador simulado"}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Tempo de análise</dt>
              <dd className="font-medium">
                {inspection.latency_ms !== null
                  ? `${inspection.latency_ms.toLocaleString("pt-BR", { maximumFractionDigits: 1 })} ms`
                  : "—"}
              </dd>
            </div>
          </dl>
        </div>
        {controller ? (
          inspection.cycle_status !== "aborted" &&
          !(inspection.final_decision === null && inspection.cycle_status === "running") && (
            <CorrectionForm inspection={inspection} onDone={onClose} />
          )
        ) : (
          <NeedControl action="corrigir uma decisão" />
        )}
        {inspection.final_decision === null && inspection.cycle_status === "running" && (
          <p className="text-sm text-review">Esta peça está parada na esteira: decida pela tela de Operação.</p>
        )}
      </DialogContent>
    </Dialog>
  );
}

// ---------------------------------------------------------------- page

export function HistoricoPage() {
  const [filters, setFilters] = useState<Filters>(EMPTY);
  const [page, setPage] = useState(0);
  const [selected, setSelected] = useState<InspectionOut | null>(null);
  const params = filterParams(filters);
  const listParams = new URLSearchParams(params);
  listParams.set("limit", String(PAGE_SIZE));
  listParams.set("offset", String(page * PAGE_SIZE));

  const history = useQuery({
    queryKey: ["history", listParams.toString()],
    queryFn: ({ signal }) => apiGet<InspectionPage>(`/inspections?${listParams}`, { signal }),
    placeholderData: (previous) => previous,
  });
  const total = history.data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const products = useProducts();
  const productName = (id: string) => products.data?.find((p) => p.id === id)?.name ?? id;

  function change(next: Filters) {
    setFilters(next);
    setPage(0);
  }

  return (
    <PageShell
      title="Histórico de inspeções"
      intro="Todas as peças inspecionadas, com a foto analisada, a previsão do modelo e a decisão final. Clique numa linha para ver os detalhes ou corrigir uma decisão."
    >
      <FilterBar value={filters} onChange={change} />
      {/^\d+$/.test(filters.lot) && <LotDistribution lotId={filters.lot} />}

      <section aria-labelledby="list-title" className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 id="list-title" className="font-wide text-xl font-semibold">
            {history.data ? `${formatInt(total)} ${total === 1 ? "inspeção" : "inspeções"}` : "Inspeções"}
          </h2>
          <div className="flex gap-2">
            {JSON.stringify(filters) !== JSON.stringify(EMPTY) && (
              <Button variant="ghost" onClick={() => change(EMPTY)}>
                Limpar filtros
              </Button>
            )}
            <Button variant="outline" asChild>
              <a href={`/api/exports/inspections.csv?${params}`} download>
                <Download aria-hidden />
                Baixar CSV
              </a>
            </Button>
          </div>
        </div>

        {history.isPending ? (
          <p className="text-muted-foreground">Carregando…</p>
        ) : total === 0 ? (
          <p className="rounded-lg border border-dashed p-6 text-center text-muted-foreground">
            Nenhuma inspeção com estes filtros.
          </p>
        ) : (
          <div className="overflow-x-auto rounded-lg border bg-card">
            <table className="w-full min-w-[46rem] text-sm">
              <thead className="border-b bg-muted/50 text-left text-muted-foreground">
                <tr>
                  <th scope="col" className="px-3 py-2 font-medium">Peça</th>
                  <th scope="col" className="px-3 py-2 font-medium">Data e hora</th>
                  <th scope="col" className="px-3 py-2 font-medium">Produto e lote</th>
                  <th scope="col" className="px-3 py-2 font-medium">Classe prevista</th>
                  <th scope="col" className="px-3 py-2 font-medium">Confiança</th>
                  <th scope="col" className="px-3 py-2 font-medium">Decisão</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {history.data?.items.map((inspection) => {
                  const decision = decisionText(inspection);
                  return (
                    <tr key={inspection.id} className="cursor-pointer hover:bg-muted/40" onClick={() => setSelected(inspection)}>
                      <td className="px-3 py-2">
                        <button
                          type="button"
                          className="flex items-center gap-3 text-left font-medium"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelected(inspection);
                          }}
                        >
                          <img src={inspection.image_url} alt="" loading="lazy" className="size-12 rounded bg-muted object-cover" />
                          Nº {inspection.id}
                        </button>
                      </td>
                      <td className="px-3 py-2 tabular-nums">{formatDateTime(inspection.captured_at)}</td>
                      <td className="px-3 py-2">
                        {productName(inspection.product_id)}
                        <span className="block text-muted-foreground">Lote {inspection.lot_id}</span>
                      </td>
                      <td className="px-3 py-2">
                        <span className="flex items-center gap-2">
                          <GradeMark inspection={inspection} size="sm" />
                          {inspection.auto_decision === "REVIEW" ? "Inconclusiva" : inspection.predicted_grade}
                        </span>
                      </td>
                      <td className="px-3 py-2 tabular-nums">{formatPercent(inspection.confidence)}</td>
                      <td className={cn("px-3 py-2 font-medium", decision.tone)}>
                        <span className="flex items-center gap-1.5">
                          {decision.text}
                          {inspection.decided_by === "operator" && (
                            <UserCheck className="size-4" aria-label="decidida por pessoa" />
                          )}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {pages > 1 && (
          <div className="flex items-center justify-center gap-3">
            <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage((p) => p - 1)}>
              <ChevronLeft aria-hidden />
              Mais recentes
            </Button>
            <span className="text-sm text-muted-foreground">
              Página {page + 1} de {pages}
            </span>
            <Button variant="outline" size="sm" disabled={page + 1 >= pages} onClick={() => setPage((p) => p + 1)}>
              Mais antigas
              <ChevronRight aria-hidden />
            </Button>
          </div>
        )}
      </section>
      <DetailDialog inspection={selected} onClose={() => setSelected(null)} />
    </PageShell>
  );
}
