import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, CircleAlert, Expand, Eye, ImageOff, LoaderCircle, RotateCcw, Scan, XCircle } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { ConnectionBanner } from "@/components/station/alerts";
import { StationHeader, useProductName } from "@/components/station/header";
import { InspectionStage } from "@/components/station/inspection-photo";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { anomalyScoreRows, isAnomalyModel, visibleAnomalyRegions } from "@/lib/anomaly";
import { apiGet } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";
import type { Grade, InspectionOut, InspectionPage, LotSummary, ProductConfigOut, SystemStatus } from "@/lib/api/types";
import { formatInt, formatPercent, formatTime } from "@/lib/format";
import { DESTINATION, GRADE, MACHINE_STATE, REVIEW_REASON } from "@/lib/labels";
import { useLive } from "@/lib/realtime/store";
import { blockers } from "@/lib/station";
import { cn } from "@/lib/utils";

type ModelOut = components["schemas"]["ModelOut"];

const GRADES: Grade[] = ["A", "B", "C"];
const MURAL_LIMIT_PER_GRADE = 16;
const latencyFormat = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 1 });

/** Sub-millisecond times would round to a misleading "0 ms". */
function formatLatency(ms: number | null): string {
  if (ms === null) return "Não registrado";
  if (ms < 1) return "menos de 1 ms";
  return `${latencyFormat.format(ms)} ms`;
}

function requestFullscreen() {
  if (document.fullscreenElement) {
    void document.exitFullscreen?.().catch(() => undefined);
    return;
  }
  void document.documentElement.requestFullscreen?.().catch(() => undefined);
}

function metric(model: ModelOut | undefined, key: string): number | null {
  const value = model?.metrics?.[key];
  return typeof value === "number" ? value : null;
}

function useFairData(status: SystemStatus | null, inspected: number) {
  const lot = status?.active_lot;
  const productId = lot?.product_id;

  const mural = useQuery({
    queryKey: ["fair-mural", lot?.id],
    // No lot open arrives as null, not undefined: asking for lot_id=null is a 422.
    enabled: lot != null,
    queryFn: ({ signal }) => apiGet<InspectionPage>(`/inspections?lot_id=${lot?.id}&limit=200`, { signal }),
  });
  const models = useQuery({
    queryKey: ["models", productId],
    enabled: productId !== undefined,
    queryFn: ({ signal }) => apiGet<ModelOut[]>(`/models?product_id=${productId}`, { signal }),
  });
  const config = useQuery({
    queryKey: ["product-config", productId],
    enabled: productId !== undefined,
    queryFn: ({ signal }) => apiGet<ProductConfigOut>(`/products/${productId}/config`, { signal }),
  });

  const activeModel = models.data?.find((model) => model.id === lot?.model_id)
    ?? models.data?.find((model) => model.active);

  useEffect(() => {
    if (lot !== undefined && inspected > 0) void mural.refetch();
  }, [inspected, lot?.id, mural.refetch]);

  return { mural: mural.data?.items ?? [], activeModel, roi: config.data?.roi ?? null };
}

type FairDecisionKind = "approved" | "rejected" | "review";

interface FairDecisionInfo {
  kind: FairDecisionKind;
  badge: string;
  headline: string;
  subtitle: string;
  gradeTag: string | null;
  destinationText: string;
}

const DECISION_SURFACE: Record<FairDecisionKind, { card: string; pill: string; text: string }> = {
  approved: {
    card: "border-grade-a/30 bg-grade-a-soft",
    pill: "bg-grade-a text-white",
    text: "text-grade-a",
  },
  rejected: {
    card: "border-grade-c/30 bg-grade-c-soft",
    pill: "bg-grade-c text-white",
    text: "text-grade-c",
  },
  review: {
    card: "border-review/30 bg-review-soft",
    pill: "bg-review text-white",
    text: "text-review",
  },
};

const GRADE_TONE: Record<Grade, { text: string; bar: string; badge: string }> = {
  A: { text: "text-grade-a", bar: "bg-grade-a", badge: "bg-grade-a-soft text-grade-a" },
  B: { text: "text-grade-b", bar: "bg-grade-b", badge: "bg-grade-b-soft text-grade-b" },
  C: { text: "text-grade-c", bar: "bg-grade-c", badge: "bg-grade-c-soft text-grade-c" },
};

function resolveFairDecision(inspection: InspectionOut, anomaly: boolean): FairDecisionInfo {
  const grade = inspection.predicted_grade;
  const needsReview = inspection.auto_decision === "REVIEW";
  const decidedByTeam = needsReview && inspection.decided_by === "operator";
  // The piece arrives (INSPECTION_READY) before the board confirms the destination
  // (DECISION_ACCEPTED): until then a confident piece shows its automatic decision, never "review".
  const final = inspection.final_decision ?? (needsReview ? null : inspection.auto_decision);

  if (final === "APPROVED") {
    return {
      kind: "approved",
      badge: "APROVADA",
      headline: decidedByTeam ? "Aprovada pela equipe" : "Aprovada",
      subtitle: decidedByTeam ? "Conferida e liberada para o canal de aprovados" : "Segue pelo canal de aprovados",
      gradeTag: anomaly ? "Dentro do padrão (A)" : grade ? GRADE[grade].title : null,
      destinationText: DESTINATION.APPROVED,
    };
  }

  if (final === "REJECTED") {
    return {
      kind: "rejected",
      badge: "REJEITADA",
      headline: decidedByTeam ? "Rejeitada pela equipe" : "Rejeitada",
      subtitle: decidedByTeam ? "Conferida e desviada para a rampa de descarte" : "Desviada para a rampa de descarte",
      gradeTag: anomaly ? "Fora do padrão (C)" : grade ? GRADE[grade].title : null,
      destinationText: DESTINATION.REJECTED,
    };
  }

  return {
    kind: "review",
    badge: "EM REVISÃO",
    headline: grade ? "Em revisão humana" : "Imagem inconclusiva",
    subtitle: `${REVIEW_REASON[inspection.review_reason ?? "LOW_CONFIDENCE"]}. Equipe confere antes de separar.`,
    gradeTag: grade
      ? anomaly
        ? `Tendência: ${grade === "A" ? "Dentro do padrão" : "Fora do padrão"}`
        : `Sugestão: ${GRADE[grade].title}`
      : null,
    destinationText: "Revisão humana",
  };
}

function FairPhoto({
  inspection,
  roi,
  anomaly,
  showAnomalyRegions,
}: {
  inspection: InspectionOut | null;
  roi: ProductConfigOut["roi"];
  anomaly: boolean;
  showAnomalyRegions: boolean;
}) {
  const [failedId, setFailedId] = useState<number | null>(null);
  const state = useLive((store) => store.status?.machine.state);
  const scanning = state === "SETTLING" || state === "INSPECTING";
  const decision = inspection ? resolveFairDecision(inspection, anomaly) : null;
  const regions = !scanning ? visibleAnomalyRegions(inspection, showAnomalyRegions) : [];

  return (
    <figure className="flex min-h-0 flex-col overflow-hidden rounded-xl border bg-card">
      {inspection && failedId !== inspection.id ? (
        <InspectionStage
          inspection={inspection}
          roi={roi}
          showAnomalyRegions={showAnomalyRegions}
          scanning={scanning}
          highPriority
          onError={() => setFailedId(inspection.id)}
          alt={`Última peça analisada, ${inspection.predicted_grade ? GRADE[inspection.predicted_grade].title : "sem classe prevista"}.`}
          className="aspect-[4/3] min-h-0 flex-1 xl:aspect-auto"
          hud={
            scanning ? (
              <span className="fair-photo__hud fair-photo__hud--scanning">
                <i aria-hidden="true" />
                {state ? MACHINE_STATE[state] : "Analisando"}
              </span>
            ) : decision ? (
              <span className={cn("fair-photo__hud", DECISION_SURFACE[decision.kind].pill)}>{decision.badge}</span>
            ) : null
          }
        />
      ) : (
        <div className="grid min-h-64 flex-1 place-content-center justify-items-center gap-3 bg-photo-mat p-8 text-center text-muted-foreground">
          <ImageOff className="size-8" aria-hidden="true" />
          <p className="max-w-xs text-sm sm:text-base">
            {inspection ? "A foto desta peça não está mais disponível." : "Aguardando a primeira peça do lote."}
          </p>
        </div>
      )}
      <figcaption className="flex flex-wrap items-center justify-between gap-2 border-t px-4 py-2.5 text-sm text-muted-foreground">
        <span>
          {scanning
            ? MACHINE_STATE[state]
            : regions.length > 0
              ? `Região fora do padrão destacada (${regions.length})`
              : inspection
                ? "Foto real usada pela inteligência artificial"
                : "Câmera de inspeção"}
        </span>
        {inspection ? <span>Inspeção {inspection.id} · {formatTime(inspection.captured_at)}</span> : null}
      </figcaption>
    </figure>
  );
}

const SUPERVISED_SCORE_ROWS: { grade: Grade; label: string }[] = [
  { grade: "A", label: "Padrão bom (A)" },
  { grade: "B", label: "Defeito visual (B)" },
  { grade: "C", label: "Refugo (C)" },
];

function ScoreBars({ inspection, anomaly }: { inspection: InspectionOut; anomaly: boolean }) {
  const rows = anomaly && inspection.scores
    ? anomalyScoreRows(inspection.scores)
    : SUPERVISED_SCORE_ROWS.map((row) => ({ ...row, score: inspection.scores?.[row.grade] ?? 0 }));
  return (
    <div className="space-y-2.5" aria-label="Como a inteligência artificial votou">
      <h3 className="text-sm font-semibold text-foreground">Como a IA votou</h3>
      <div className="space-y-2">
        {rows.map(({ grade, label, score }) => {
          const tone = GRADE_TONE[grade];
          return (
            <div className="grid grid-cols-[1.5rem_minmax(7.5rem,auto)_minmax(0,1fr)_3.25rem] items-center gap-3 text-sm" key={grade}>
              <span className={cn("font-display font-bold", tone.text)}>{grade}</span>
              <span className="truncate text-muted-foreground">{label}</span>
              <span className="h-2 overflow-hidden rounded-full bg-muted" aria-hidden="true">
                <span
                  className={cn("block h-full rounded-full transition-[width] duration-300 ease-out", tone.bar)}
                  style={{ width: `${Math.max(1, score * 100)}%` }}
                />
              </span>
              <strong className="text-right font-semibold">{formatPercent(score)}</strong>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function DecisionIcon({ kind }: { kind: FairDecisionKind }) {
  if (kind === "approved") return <CheckCircle2 className="size-4" aria-hidden="true" />;
  if (kind === "rejected") return <XCircle className="size-4" aria-hidden="true" />;
  return <CircleAlert className="size-4" aria-hidden="true" />;
}

function FairVerdict({
  inspection,
  activeModel,
  summary,
}: {
  inspection: InspectionOut | null;
  activeModel: ModelOut | undefined;
  summary: LotSummary;
}) {
  if (!inspection) {
    return (
      <Card className="justify-center gap-2 p-6">
        <p className="text-sm font-medium text-muted-foreground">Resultado da peça</p>
        <h2 className="font-wide text-2xl font-semibold tracking-tight sm:text-3xl">Aguardando análise</h2>
        <p className="text-muted-foreground">
          A próxima peça aparecerá aqui com o veredito, os votos das classes e a confiança do modelo.
        </p>
      </Card>
    );
  }

  const anomaly = isAnomalyModel(activeModel, inspection.model_id);
  const decision = resolveFairDecision(inspection, anomaly);
  const surface = DECISION_SURFACE[decision.kind];
  const accuracy = !anomaly ? metric(activeModel, "test_accuracy") : null;
  const approvalRateText = summary.approval_rate_denominator > 0
    ? `${formatPercent(summary.approval_rate)} (${formatInt(summary.approved)}/${formatInt(summary.approval_rate_denominator)})`
    : "Aguardando decisão";

  return (
    <Card className="min-h-0 justify-between gap-4 p-5" aria-live="polite">
      <div
        key={inspection.id}
        className={cn(
          "fair-decision-enter grid grid-cols-1 gap-4 rounded-lg border p-4 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-center",
          surface.card,
        )}
      >
        <div className="min-w-0 space-y-1.5">
          <span className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-bold tracking-wide", surface.pill)}>
            <DecisionIcon kind={decision.kind} />
            {decision.badge}
          </span>
          <h2 className="font-wide text-2xl font-bold tracking-tight sm:text-3xl">{decision.headline}</h2>
          <p className="text-sm text-foreground/80">{decision.subtitle}</p>
          {decision.gradeTag ? (
            <span className="inline-block rounded-md border border-foreground/15 bg-background/70 px-2 py-0.5 text-xs font-medium text-foreground">
              {decision.gradeTag}
            </span>
          ) : null}
        </div>
        <div className="border-t border-foreground/10 pt-3 sm:border-t-0 sm:border-l sm:pt-0 sm:pl-5 sm:text-right">
          <strong className={cn("font-display block text-3xl sm:text-4xl", surface.text)}>
            {formatPercent(inspection.confidence)}
          </strong>
          <span className="mt-1 block text-xs text-muted-foreground">Confiança do modelo</span>
        </div>
      </div>

      {inspection.scores ? <ScoreBars inspection={inspection} anomaly={anomaly} /> : null}

      <dl className="grid grid-cols-2 gap-3 border-t pt-3 sm:grid-cols-4">
        <div>
          <dt className="text-xs text-muted-foreground">Tempo da análise</dt>
          <dd className="mt-0.5 text-sm font-semibold">{formatLatency(inspection.latency_ms)}</dd>
        </div>
        <div>
          <dt className="text-xs text-muted-foreground">Destino</dt>
          <dd className="mt-0.5 text-sm font-semibold">{decision.destinationText}</dd>
        </div>
        <div>
          <dt className="text-xs text-muted-foreground">Aprovação do lote</dt>
          <dd className="mt-0.5 text-sm font-semibold">{approvalRateText}</dd>
        </div>
        {accuracy !== null ? (
          <div>
            <dt className="text-xs text-muted-foreground">Acurácia nos testes</dt>
            <dd className="mt-0.5 text-sm font-semibold">{formatPercent(accuracy, true)}</dd>
          </div>
        ) : (
          <div>
            <dt className="text-xs text-muted-foreground">Modo da IA</dt>
            <dd className="mt-0.5 text-sm font-semibold">
              {anomaly ? "Detecção de anomalia" : activeModel ? "Classificação A/B/C" : "Bancada simulada"}
            </dd>
          </div>
        )}
      </dl>
    </Card>
  );
}

const PROCESS_STAGES: { label: string; states: NonNullable<SystemStatus["machine"]["state"]>[] }[] = [
  { label: "Sensor detecta", states: ["TO_S1"] },
  { label: "Câmera fotografa", states: ["SETTLING"] },
  { label: "IA classifica", states: ["INSPECTING", "REVIEW_HOLD"] },
  { label: "Esteira separa", states: ["TO_S2", "SORTING", "RELEASING"] },
];

function ProcessRail({ status }: { status: SystemStatus }) {
  const state = status.machine.state;
  const dest = status.current_cycle?.commanded_destination;
  const sortLabel = dest === "APPROVED" ? "Canal de aprovados" : dest === "REJECTED" ? "Rampa de descarte" : "Esteira separa";

  return (
    <section
      className="flex flex-col gap-2.5 rounded-xl border bg-card px-4 py-3 lg:flex-row lg:items-center lg:justify-between lg:gap-6"
      aria-labelledby="fair-process-title"
    >
      <div className="shrink-0">
        <p className="text-xs text-muted-foreground">O que está acontecendo agora</p>
        <h2 id="fair-process-title" className="text-sm font-semibold">{state ? MACHINE_STATE[state] : "Aguardando a bancada"}</h2>
      </div>
      <ol className="grid flex-1 grid-cols-2 gap-2 sm:grid-cols-4">
        {PROCESS_STAGES.map((stage, index) => {
          const active = state !== null && stage.states.includes(state);
          const label = index === 3 ? sortLabel : stage.label;
          const activeStyle =
            active && index >= 2 && dest === "REJECTED"
              ? "border-grade-c/40 bg-grade-c-soft text-grade-c"
              : active && state === "REVIEW_HOLD"
                ? "border-review/40 bg-review-soft text-review"
                : active
                  ? "border-grade-a/40 bg-grade-a-soft text-grade-a"
                  : "border-transparent bg-muted/45 text-muted-foreground";
          return (
            <li
              key={stage.label}
              className={cn("flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm font-medium transition-colors", activeStyle)}
            >
              <span className="grid size-5 shrink-0 place-items-center rounded-full border border-current text-xs font-bold">
                {index + 1}
              </span>
              <span className="truncate">{label}</span>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

function MuralThumbnail({ inspection, newest }: { inspection: InspectionOut; newest: boolean }) {
  const [failed, setFailed] = useState(false);
  return (
    <li
      className={cn(
        "grid size-10 shrink-0 place-items-center overflow-hidden rounded-md border bg-muted sm:size-11",
        newest && "fair-thumb-enter ring-2 ring-primary/30",
      )}
      title={`Inspeção ${inspection.id}`}
    >
      {failed ? (
        <ImageOff className="size-4 text-muted-foreground" aria-label="Foto não disponível" />
      ) : (
        <img src={`/api/inspections/${inspection.id}/thumbnail`} alt="" className="size-full object-cover" loading="lazy" onError={() => setFailed(true)} />
      )}
    </li>
  );
}

function GradeMural({
  inspections,
  newestId,
  reviewed,
  totals,
  anomaly,
}: {
  inspections: InspectionOut[];
  newestId: number | undefined;
  reviewed: number;
  totals: Record<string, number> | null;
  anomaly: boolean;
}) {
  const hasB = (totals?.B ?? 0) > 0 || inspections.some((item) => item.predicted_grade === "B");
  const grades = anomaly && !hasB ? (["A", "C"] as Grade[]) : GRADES;

  return (
    <Card className="gap-2.5 p-4" aria-labelledby="fair-mural-title">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <p className="text-xs text-muted-foreground">Mural do lote</p>
          <h2 id="fair-mural-title" className="text-base font-semibold">
            Cada foto ocupa o lugar da classe escolhida pela IA
          </h2>
        </div>
        <p className="text-xs text-muted-foreground">
          {reviewed > 0 ? `${reviewed} ${reviewed === 1 ? "peça teve" : "peças tiveram"} revisão humana` : "As próximas peças formarão este painel"}
        </p>
      </div>
      <div className="space-y-1.5">
        {grades.map((grade) => {
          const matches = inspections.filter((item) => item.predicted_grade === grade);
          const visible = matches.slice(0, MURAL_LIMIT_PER_GRADE).reverse();
          const total = totals?.[grade] ?? matches.length;
          const grouped = Math.max(0, total - visible.length);
          const tone = GRADE_TONE[grade];
          return (
            <div className="grid grid-cols-[4.5rem_minmax(0,1fr)] items-center gap-3" key={grade}>
              <div className={cn("flex items-center justify-between rounded-md px-2.5 py-1 text-sm font-semibold", tone.badge)}>
                <span className="font-display font-bold">{grade}</span>
                <span>{formatInt(total)}</span>
              </div>
              <ul className="flex min-w-0 items-center gap-1.5 overflow-hidden" aria-label={`Fotos classificadas como classe ${grade}`}>
                {grouped > 0 ? (
                  <li className="grid size-10 shrink-0 place-items-center rounded-md border bg-muted text-xs font-semibold text-muted-foreground sm:size-11">
                    +{grouped}
                  </li>
                ) : null}
                {visible.map((inspection) => <MuralThumbnail key={inspection.id} inspection={inspection} newest={inspection.id === newestId} />)}
                {matches.length === 0 ? <li className="text-xs text-muted-foreground">Nenhuma peça ainda</li> : null}
              </ul>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

function WaitingScene({ product }: { product: string | undefined }) {
  return (
    <Card className="col-span-full items-center justify-center gap-4 p-8 text-center">
      <p className="text-sm font-medium text-muted-foreground">Demonstração interativa</p>
      <h2 className="font-wide text-3xl font-semibold tracking-tight sm:text-4xl">Que classe você daria?</h2>
      <p className="max-w-xl text-base text-muted-foreground">
        {product ? `A próxima ${product.toLowerCase()} será fotografada e classificada em tempo real.` : "A próxima peça será fotografada e classificada em tempo real."}
      </p>
      <ol className="flex flex-wrap justify-center gap-4 text-sm font-medium text-foreground/85" aria-label="Como funciona">
        <li className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full border text-xs font-bold">1</span>Coloque a peça na esteira</li>
        <li className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full border text-xs font-bold">2</span>Câmera e IA analisam ao vivo</li>
        <li className="flex items-center gap-2"><span className="grid size-6 place-items-center rounded-full border text-xs font-bold">3</span>Esteira separa automaticamente</li>
      </ol>
      <span className="rounded-full border border-grade-a/40 bg-grade-a-soft px-4 py-1.5 text-sm font-semibold text-grade-a">
        Coloque uma peça no começo da esteira
      </span>
    </Card>
  );
}

/** Public, read-only fair demonstration view matching the station's minimalist light theme. */
export function FeiraPage() {
  const status = useLive((store) => store.status);
  const recent = useLive((store) => store.recent);
  const connection = useLive((store) => store.connection);
  const product = useProductName(status?.active_lot?.product_id);
  const summary = status?.active_lot_summary ?? null;
  const inspected = summary?.inspected ?? 0;
  const { mural, activeModel, roi } = useFairData(status, inspected);
  const [muralFloorId, setMuralFloorId] = useState(0);
  const [forceWaiting, setForceWaiting] = useState(false);
  const [autoWaiting, setAutoWaiting] = useState(false);
  const [showAnomalyRegions, setShowAnomalyRegions] = useState(true);
  const latest = recent[0] ?? mural[0] ?? null;
  const latestId = latest?.id;
  const anomaly = isAnomalyModel(activeModel, latest?.model_id);

  const allInspections = useMemo(() => {
    const byId = new Map<number, InspectionOut>();
    for (const item of [...recent, ...mural]) byId.set(item.id, item);
    return [...byId.values()].filter((item) => item.id > muralFloorId).sort((a, b) => b.id - a.id);
  }, [mural, muralFloorId, recent]);

  useEffect(() => {
    setAutoWaiting(false);
    if (latestId === undefined) return;
    const timer = window.setTimeout(() => setAutoWaiting(true), 12_000);
    return () => window.clearTimeout(timer);
  }, [latestId]);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (!event.altKey) return;
      const key = event.key.toLowerCase();
      if (key === "m") setMuralFloorId(latestId ?? 0);
      if (key === "e") setForceWaiting((value) => !value);
      if (key === "a") setShowAnomalyRegions((value) => !value);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [latestId]);

  const problem = blockers(status).find((item) => item.severity === "fault");
  const waiting = status?.current_cycle === null && (forceWaiting || autoWaiting);

  return (
    <div className="flex min-h-dvh flex-col xl:h-dvh">
      <ConnectionBanner />
      <StationHeader status={status} />

      <main className="mx-auto flex w-full max-w-[120rem] flex-1 flex-col gap-3.5 px-4 py-4 sm:px-6 xl:min-h-0 xl:overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="font-wide text-2xl font-semibold tracking-tight sm:text-3xl">Modo feira</h1>
            <p className="text-sm text-muted-foreground">Demonstração visual em tempo real</p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {summary ? (
              <dl className="flex items-center gap-4 rounded-lg border bg-card px-3.5 py-1.5 text-sm">
                <div className="flex items-baseline gap-1.5">
                  <dt className="text-muted-foreground">Inspecionadas</dt>
                  <dd className="font-semibold">{formatInt(summary.inspected)}</dd>
                </div>
                <div className="flex items-baseline gap-1.5 border-l pl-4">
                  <dt className="text-muted-foreground">Aprovação</dt>
                  <dd className="font-semibold">
                    {summary.approval_rate_denominator > 0 ? formatPercent(summary.approval_rate) : "—"}
                  </dd>
                </div>
              </dl>
            ) : null}
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setForceWaiting((value) => !value)}
              title="Alternar tela de convite (Alt+E)"
              aria-pressed={forceWaiting}
            >
              <Eye className="size-4" aria-hidden="true" />
              <span className="max-sm:hidden">{waiting ? "Ver resultado" : "Convite"}</span>
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setShowAnomalyRegions((value) => !value)}
              title="Mostrar ou ocultar regiões fora do padrão (Alt+A)"
              aria-pressed={showAnomalyRegions}
            >
              <Scan className="size-4" aria-hidden="true" />
              <span className="max-sm:hidden">Regiões</span>
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setMuralFloorId(latestId ?? 0)}
              title="Limpar mural visualmente (Alt+M)"
            >
              <RotateCcw className="size-4" aria-hidden="true" />
              <span className="max-sm:hidden">Limpar mural</span>
            </Button>
            <Button type="button" variant="outline" size="icon-sm" onClick={requestFullscreen} aria-label="Abrir em tela cheia" title="Tela cheia">
              <Expand className="size-4" aria-hidden="true" />
            </Button>
          </div>
        </div>

        {connection !== "open" || !status ? (
          <Card className="flex-1 items-center justify-center gap-2 p-8 text-center" role="status">
            <LoaderCircle className="size-6 animate-spin text-muted-foreground" aria-hidden="true" />
            <h2 className="text-xl font-semibold">Reconectando ao sistema local</h2>
            <p className="text-sm text-muted-foreground">A demonstração volta automaticamente assim que o serviço responder.</p>
          </Card>
        ) : problem ? (
          <Card className="flex-1 items-center justify-center gap-2 border-fault/40 bg-fault-soft p-8 text-center" role="status">
            <h2 className="text-xl font-semibold text-fault">{problem.title}</h2>
            <p className="text-sm text-foreground/80">{problem.detail ?? "A equipe já pode verificar a bancada."}</p>
          </Card>
        ) : status.active_lot && summary ? (
          <div className="grid flex-1 gap-3.5 xl:min-h-0 xl:grid-rows-[minmax(0,1fr)_auto_auto]">
            <div className="grid min-h-0 grid-cols-1 gap-4 xl:grid-cols-12">
              {waiting ? (
                <WaitingScene product={product} />
              ) : (
                <>
                  <div className="grid min-h-0 xl:col-span-6">
                    <FairPhoto inspection={latest} roi={roi} anomaly={anomaly} showAnomalyRegions={showAnomalyRegions} />
                  </div>
                  <div className="grid min-h-0 xl:col-span-6">
                    <FairVerdict inspection={latest} activeModel={activeModel} summary={summary} />
                  </div>
                </>
              )}
            </div>
            <ProcessRail status={status} />
            <GradeMural
              inspections={allInspections}
              newestId={allInspections[0]?.id}
              reviewed={summary.reviewed}
              totals={muralFloorId === 0 ? summary.by_grade : null}
              anomaly={anomaly}
            />
          </div>
        ) : (
          <Card className="flex-1 items-center justify-center gap-2 p-8 text-center">
            <h2 className="font-wide text-2xl font-semibold">Inspeção visual de produtos da Amazônia</h2>
            <p className="text-muted-foreground">A demonstração começa quando a equipe abrir um lote na tela Operação.</p>
          </Card>
        )}
      </main>
    </div>
  );
}
