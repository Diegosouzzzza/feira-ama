import { useQuery } from "@tanstack/react-query";
import { Expand, ImageOff, LogOut } from "lucide-react";
import { type CSSProperties, useEffect, useMemo, useState } from "react";
import { Link } from "react-router";
import { ConnectionBanner } from "@/components/station/alerts";
import { Brand, useProductName } from "@/components/station/header";
import { apiGet } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";
import type { Grade, InspectionOut, InspectionPage, ProductConfigOut, SystemStatus } from "@/lib/api/types";
import { formatPercent } from "@/lib/format";
import { DESTINATION, GRADE, MACHINE_STATE, REVIEW_REASON } from "@/lib/labels";
import { useLive } from "@/lib/realtime/store";
import { blockers } from "@/lib/station";
import { cn } from "@/lib/utils";

type ModelOut = components["schemas"]["ModelOut"];

const GRADES: Grade[] = ["A", "B", "C"];
const MURAL_LIMIT_PER_GRADE = 18;
const latencyFormat = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 1 });

/** Sub-millisecond times would round to a misleading "0 ms". */
function formatLatency(ms: number | null): string {
  if (ms === null) return "Não registrado";
  if (ms < 1) return "menos de 1 ms";
  return `${latencyFormat.format(ms)} ms`;
}

function requestFullscreen() {
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
    enabled: lot !== undefined,
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

function percent(fraction: number): string {
  return `${fraction * 100}%`;
}

function FairPhoto({ inspection, roi }: { inspection: InspectionOut | null; roi: ProductConfigOut["roi"] }) {
  const [failedId, setFailedId] = useState<number | null>(null);
  // Frame follows the photo's own proportions, so the ROI (fractions of the frame) lands on
  // the same pixels the model saw, whatever the camera resolution.
  const [aspect, setAspect] = useState(4 / 3);
  const state = useLive((store) => store.status?.machine.state);
  const scanning = state === "SETTLING" || state === "INSPECTING";

  return (
    <figure className="fair-photo" aria-labelledby="fair-photo-caption">
      {inspection && failedId !== inspection.id ? (
        <div className="fair-photo__image-wrap">
          <div className="fair-photo__frame" style={{ "--photo-aspect": aspect } as CSSProperties}>
            <img
              key={inspection.id}
              src={inspection.image_url}
              alt={`Última peça analisada, ${inspection.predicted_grade ? GRADE[inspection.predicted_grade].title : "sem classe prevista"}.`}
              fetchPriority="high"
              onLoad={(event) => {
                const { naturalWidth, naturalHeight } = event.currentTarget;
                if (naturalWidth > 0 && naturalHeight > 0) setAspect(naturalWidth / naturalHeight);
              }}
              onError={() => setFailedId(inspection.id)}
              className="fair-photo__image"
            />
            {roi ? (
              <span
                className="fair-photo__roi"
                style={{ left: percent(roi.x), top: percent(roi.y), width: percent(roi.width), height: percent(roi.height) }}
                aria-hidden="true"
              />
            ) : null}
            {scanning ? <span className="fair-photo__scan" aria-hidden="true" /> : null}
          </div>
        </div>
      ) : (
        <div className="fair-photo__empty">
          <ImageOff aria-hidden="true" />
          <p>{inspection ? "A foto desta peça não está mais disponível." : "Aguardando a primeira peça."}</p>
        </div>
      )}
      <figcaption id="fair-photo-caption">
        {scanning ? MACHINE_STATE[state] : inspection ? "Foto real usada pela inteligência artificial" : "Câmera de inspeção"}
      </figcaption>
    </figure>
  );
}

function ScoreBars({ inspection }: { inspection: InspectionOut }) {
  return (
    <div className="fair-scores" aria-label="Como a inteligência artificial votou">
      <h3>Como a IA votou</h3>
      {GRADES.map((grade) => {
        const score = inspection.scores?.[grade] ?? 0;
        return (
          <div className="fair-score" key={grade}>
            <span className={`fair-score__grade fair-tone-${grade.toLowerCase()}`}>{grade}</span>
            <span className="fair-score__track" aria-hidden="true">
              <span className={`fair-score__fill fair-tone-${grade.toLowerCase()}`} style={{ width: `${Math.max(1, score * 100)}%` }} />
            </span>
            <strong>{formatPercent(score)}</strong>
          </div>
        );
      })}
    </div>
  );
}

function FairVerdict({ inspection, activeModel }: { inspection: InspectionOut | null; activeModel: ModelOut | undefined }) {
  if (!inspection) {
    return (
      <section className="fair-verdict fair-verdict--empty">
        <p className="fair-kicker">Resultado</p>
        <h2>Aguardando análise</h2>
        <p>A próxima peça aparecerá aqui com os votos das três classes.</p>
      </section>
    );
  }

  const grade = inspection.predicted_grade;
  const accuracy = metric(activeModel, "test_accuracy");
  const needsReview = inspection.auto_decision === "REVIEW";
  const decidedByTeam = needsReview && inspection.decided_by === "operator";
  const destination = inspection.final_decision
    ? DESTINATION[inspection.final_decision]
    : needsReview
      ? "Revisão humana"
      : "Aguardando a separação";

  // An inconclusive piece never shows the model's guess as the result: visitors would read
  // a big "Classe B" as a decision the AI did not make. The guess stays in the vote bars.
  const title = decidedByTeam
    ? "Decidida pela equipe"
    : needsReview
      ? "Em revisão"
      : grade
        ? GRADE[grade].title
        : "Imagem inconclusiva";
  const meaning = needsReview
    ? `${REVIEW_REASON[inspection.review_reason ?? "LOW_CONFIDENCE"]}. ${decidedByTeam ? "Uma pessoa da equipe conferiu e decidiu." : "Uma pessoa da equipe confere antes de separar."}`
    : grade
      ? GRADE[grade].meaning
      : "A imagem não permitiu uma classificação segura.";

  return (
    <section className="fair-verdict" aria-live="polite">
      <div className="fair-verdict__top">
        <div
          key={inspection.id}
          className={cn("fair-stamp", !needsReview && grade && `fair-stamp--${grade.toLowerCase()}`)}
          aria-hidden="true"
        >
          {needsReview || !grade ? "?" : grade}
        </div>
        <div className="min-w-0">
          <p className="fair-kicker">Resultado da peça</p>
          <h2>{title}</h2>
          <p>{meaning}</p>
        </div>
      </div>

      {inspection.scores ? <ScoreBars inspection={inspection} /> : null}

      <dl className="fair-facts">
        <div><dt>Tempo da análise</dt><dd>{formatLatency(inspection.latency_ms)}</dd></div>
        <div><dt>Destino</dt><dd>{destination}</dd></div>
        <div><dt>Acurácia nos testes</dt><dd>{accuracy === null ? "Não publicada" : formatPercent(accuracy, true)}</dd></div>
      </dl>
    </section>
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
  return (
    <section className="fair-process" aria-labelledby="fair-process-title">
      <div>
        <p className="fair-kicker">O que está acontecendo agora</p>
        <h2 id="fair-process-title">{state ? MACHINE_STATE[state] : "Aguardando a bancada"}</h2>
      </div>
      <ol>
        {PROCESS_STAGES.map((stage, index) => {
          const active = state !== null && stage.states.includes(state);
          return <li key={stage.label} className={active ? "is-active" : undefined}><span>{index + 1}</span>{stage.label}</li>;
        })}
      </ol>
    </section>
  );
}

function MuralThumbnail({ inspection, newest }: { inspection: InspectionOut; newest: boolean }) {
  const [failed, setFailed] = useState(false);
  return (
    <li className={cn("fair-thumb", newest && "fair-thumb--new")} title={`Inspeção ${inspection.id}`}>
      {failed ? (
        <span className="fair-thumb__missing" aria-label="Foto não disponível"><ImageOff aria-hidden="true" /></span>
      ) : (
        <img src={`/api/inspections/${inspection.id}/thumbnail`} alt="" width={96} height={96} loading="lazy" onError={() => setFailed(true)} />
      )}
    </li>
  );
}

function GradeMural({
  inspections,
  newestId,
  reviewed,
  totals,
}: {
  inspections: InspectionOut[];
  newestId: number | undefined;
  reviewed: number;
  totals: Record<string, number> | null;
}) {
  return (
    <section className="fair-mural" aria-labelledby="fair-mural-title">
      <div className="fair-mural__heading">
        <div><p className="fair-kicker">Mural do lote</p><h2 id="fair-mural-title">Cada foto ocupa o lugar da classe escolhida pela IA</h2></div>
        <p>{reviewed > 0 ? `${reviewed} ${reviewed === 1 ? "peça teve" : "peças tiveram"} revisão humana` : "As próximas peças formarão este painel"}</p>
      </div>
      <div className="fair-mural__rows">
        {GRADES.map((grade) => {
          const matches = inspections.filter((item) => item.predicted_grade === grade);
          const visible = matches.slice(0, MURAL_LIMIT_PER_GRADE).reverse();
          const total = totals?.[grade] ?? matches.length;
          const grouped = Math.max(0, total - visible.length);
          return (
            <div className="fair-mural__row" key={grade}>
              <div className={`fair-mural__label fair-tone-${grade.toLowerCase()}`}><strong>{grade}</strong><span>{total}</span></div>
              <ul aria-label={`Fotos classificadas como classe ${grade}`}>
                {grouped > 0 ? <li className="fair-thumb fair-thumb--grouped">+{grouped}</li> : null}
                {visible.map((inspection) => <MuralThumbnail key={inspection.id} inspection={inspection} newest={inspection.id === newestId} />)}
                {matches.length === 0 ? <li className="fair-mural__empty">Nenhuma peça ainda</li> : null}
              </ul>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function WaitingScene({ product }: { product: string | undefined }) {
  return (
    <section className="fair-waiting">
      <p className="fair-kicker">Demonstração interativa</p>
      <h2>Que classe você daria?</h2>
      <p>{product ? `A próxima ${product.toLowerCase()} será fotografada e classificada em tempo real.` : "A próxima peça será fotografada e classificada em tempo real."}</p>
      <strong>Coloque uma peça no começo da esteira.</strong>
    </section>
  );
}

/** Public, read-only screen for visitors, composed for a Full HD 42-inch display. */
export function FeiraPage() {
  const status = useLive((store) => store.status);
  const recent = useLive((store) => store.recent);
  const connection = useLive((store) => store.connection);
  const product = useProductName(status?.active_lot?.product_id);
  const inspected = status?.active_lot_summary?.inspected ?? 0;
  const { mural, activeModel, roi } = useFairData(status, inspected);
  const [muralFloorId, setMuralFloorId] = useState(0);
  const [forceWaiting, setForceWaiting] = useState(false);
  const [autoWaiting, setAutoWaiting] = useState(false);
  const latest = recent[0] ?? mural[0] ?? null;
  const latestId = latest?.id;

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
      if (event.key.toLowerCase() === "m") setMuralFloorId(latestId ?? 0);
      if (event.key.toLowerCase() === "e") setForceWaiting((value) => !value);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [latestId]);

  const problem = blockers(status).find((item) => item.severity === "fault");
  const waiting = status?.current_cycle === null && (forceWaiting || autoWaiting);

  return (
    <div className="feira feira-v2 flex h-dvh flex-col overflow-hidden">
      <ConnectionBanner />
      <header className="fair-header">
        <Brand large />
        <p className="fair-header__claim">Visão computacional para classificar produtos da Amazônia</p>
        <div className="fair-header__lot"><strong>{product ?? "Preparando a estação"}</strong>{status?.active_lot ? <span>Lote {status.active_lot.id}</span> : null}</div>
        <button type="button" onClick={requestFullscreen} aria-label="Abrir em tela cheia"><Expand aria-hidden="true" /></button>
        <Link to="/" aria-label="Sair do modo feira"><LogOut aria-hidden="true" /></Link>
      </header>

      <main className="fair-main">
        <h1 className="sr-only">AmazonVision 4.0, demonstração da classificação por inteligência artificial</h1>
        {connection !== "open" || !status ? (
          <section className="fair-message fair-message--fault" role="status"><h2>Reconectando ao sistema local</h2><p>A demonstração volta automaticamente assim que o serviço responder.</p></section>
        ) : problem ? (
          <section className="fair-message fair-message--fault" role="status"><h2>{problem.title}</h2><p>{problem.detail ?? "A equipe já pode verificar a bancada."}</p></section>
        ) : status.active_lot && status.active_lot_summary ? (
          <>
            <div className="fair-live">
              {waiting ? <WaitingScene product={product} /> : <><FairPhoto inspection={latest} roi={roi} /><FairVerdict inspection={latest} activeModel={activeModel} /></>}
            </div>
            <ProcessRail status={status} />
            <GradeMural
              inspections={allInspections}
              newestId={allInspections[0]?.id}
              reviewed={status.active_lot_summary.reviewed}
              totals={muralFloorId === 0 ? status.active_lot_summary.by_grade : null}
            />
          </>
        ) : (
          <section className="fair-message"><h2>Inspeção visual de produtos da Amazônia</h2><p>A demonstração começa quando a equipe abrir um lote.</p></section>
        )}
      </main>

      <footer className="fair-footer">
        <span>Feira Tecnológica FUCAPI 2026</span>
        {status?.mode === "simulado" ? <span>Demonstração simulada</span> : <span>Processamento local</span>}
      </footer>
    </div>
  );
}
