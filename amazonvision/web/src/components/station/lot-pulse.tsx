import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api/client";
import type { Grade, InspectionOut, InspectionPage } from "@/lib/api/types";
import { formatPercent, formatTime } from "@/lib/format";
import { DESTINATION, GRADE } from "@/lib/labels";
import { cn } from "@/lib/utils";
import { inspectionTone } from "./grade-mark";
import { TONE } from "./tone";

const GRADES: Grade[] = ["A", "B", "C"];
const SEQUENCE_LENGTH = 24;
const RECENT_WINDOW = 10; // pieces used for rhythm and analysis time
const decimal = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 1 });

/** The lot's latest pieces, refreshed whenever the lot counter moves (the database decides). */
function useSequence(lotId: number, inspected: number) {
  return useQuery({
    queryKey: ["lot-sequence", lotId, inspected],
    queryFn: ({ signal }) =>
      apiGet<InspectionPage>(`/inspections?lot_id=${lotId}&limit=${SEQUENCE_LENGTH}`, { signal }),
    placeholderData: (previous) => previous,
  });
}

function median(values: number[]): number | null {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  const upper = sorted[middle];
  if (upper === undefined) return null;
  return sorted.length % 2 ? upper : ((sorted[middle - 1] ?? upper) + upper) / 2;
}

/** Pieces per minute between the oldest and newest of the recent pieces (pauses included). */
function rhythm(items: InspectionOut[]): number | null {
  const recent = items.slice(0, RECENT_WINDOW);
  const first = recent[0];
  const last = recent.at(-1);
  if (recent.length < 3 || !first || !last) return null;
  const minutes = (Date.parse(first.captured_at) - Date.parse(last.captured_at)) / 60_000;
  return minutes > 0 ? (recent.length - 1) / minutes : null;
}

function formatMs(ms: number | null): string {
  if (ms === null) return "—";
  return ms < 1 ? "menos de 1 ms" : `${decimal.format(ms)} ms`;
}

/** Same symbols as the grade mark: letter, "?" while undecided, ✓/✕ once a person decided. */
function markLetter(item: InspectionOut): string {
  if (item.auto_decision === "REVIEW" && item.decided_by === "operator") {
    return item.final_decision === "APPROVED" ? "✓" : "✕";
  }
  return item.auto_decision === "REVIEW" || !item.predicted_grade ? "?" : item.predicted_grade;
}

function describe(item: InspectionOut): string {
  const grade = item.predicted_grade ? GRADE[item.predicted_grade].title : "sem classe";
  const outcome =
    item.cycle_status === "aborted"
      ? "ciclo interrompido"
      : item.final_decision
        ? `${DESTINATION[item.final_decision].toLowerCase()}${item.decided_by === "operator" ? " pelo operador" : ""}`
        : "aguardando revisão";
  return `Inspeção ${item.id} às ${formatTime(item.captured_at)}: ${grade}, ${outcome}`;
}

function Votes({ inspection }: { inspection: InspectionOut }) {
  if (!inspection.scores) return null;
  return (
    <div>
      <h3 className="text-sm font-medium">Como a IA votou nesta peça</h3>
      <dl className="mt-2 space-y-1.5">
        {GRADES.map((grade) => {
          const score = inspection.scores?.[grade] ?? 0;
          return (
            <div key={grade} className="grid grid-cols-[1.25rem_minmax(0,1fr)_3rem] items-center gap-3">
              <dt className="font-display text-sm">{grade}</dt>
              <dd className="h-1.5 overflow-hidden rounded-full bg-muted" aria-hidden>
                <div
                  className={cn("h-full rounded-full", TONE[GRADE[grade].tone].solid)}
                  style={{ width: `${Math.max(score * 100, score > 0 ? 1.5 : 0)}%` }}
                />
              </dd>
              <dd className="text-right text-sm tabular-nums">
                <span className="sr-only">{GRADE[grade].title}: </span>
                {formatPercent(score)}
              </dd>
            </div>
          );
        })}
      </dl>
    </div>
  );
}

function Sequence({ items }: { items: InspectionOut[] }) {
  const oldestFirst = [...items].reverse();
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3">
        <h3 className="text-sm font-medium">Últimas {items.length} peças do lote</h3>
        <p className="text-xs text-muted-foreground">mais recente à direita</p>
      </div>
      <ol className="mt-2 flex flex-wrap gap-[3px]" aria-label="Sequência de resultados, da mais antiga para a mais recente">
        {oldestFirst.map((item, index) => {
          const newest = index === oldestFirst.length - 1;
          return (
            <li
              key={item.id}
              title={describe(item)}
              className={cn(
                "grid size-6 place-items-center rounded-[4px] text-[11px] leading-none font-bold text-white",
                TONE[inspectionTone(item)].solid,
                item.cycle_status === "aborted" && "opacity-45",
                newest && "ring-2 ring-foreground ring-offset-2 ring-offset-card",
              )}
            >
              <span aria-hidden>{markLetter(item)}</span>
              <span className="sr-only">{describe(item)}</span>
            </li>
          );
        })}
      </ol>
      <ul className="mt-2.5 flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground" aria-label="Legenda">
        {GRADES.map((grade) => (
          <li key={grade} className="flex items-center gap-1.5">
            <span className={cn("size-2.5 rounded-[3px]", TONE[GRADE[grade].tone].solid)} aria-hidden />
            {grade} {GRADE[grade].meaning.toLowerCase()}
          </li>
        ))}
        <li className="flex items-center gap-1.5">
          <span className={cn("size-2.5 rounded-[3px]", TONE.review.solid)} aria-hidden />? revisão, ✓ ✕ decisão da equipe
        </li>
      </ul>
    </div>
  );
}

function Figure({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <div className="min-w-0">
      <dt className="text-xs text-muted-foreground">{label}</dt>
      <dd className="mt-0.5 truncate text-lg font-semibold">{value}</dd>
      <dd className="truncate text-xs text-muted-foreground">{detail}</dd>
    </div>
  );
}

/** Compact lot telemetry under the verdict: why this piece, how the lot is going, how fast. */
export function LotPulse({
  lotId,
  inspected,
  inspection,
}: {
  lotId: number;
  inspected: number;
  inspection: InspectionOut | null;
}) {
  const sequence = useSequence(lotId, inspected);
  const items = sequence.data?.items ?? [];
  if (items.length === 0 && !inspection?.scores) return null;

  const recent = items.slice(0, RECENT_WINDOW);
  const pace = rhythm(items);
  const latency = median(recent.flatMap((item) => (item.latency_ms === null ? [] : [item.latency_ms])));
  const reviewShare = recent.length ? recent.filter((item) => item.auto_decision === "REVIEW").length / recent.length : null;

  return (
    <section aria-label="Resumo do lote" className="space-y-5 border-t pt-5">
      {inspection && <Votes inspection={inspection} />}
      {items.length > 0 && <Sequence items={items} />}
      {items.length > 0 && (
        <dl className="grid grid-cols-3 gap-4 rounded-md bg-muted/60 px-4 py-3">
          <Figure
            label="Ritmo"
            value={pace === null ? "—" : `${decimal.format(pace)} /min`}
            detail={`últimas ${recent.length}`}
          />
          <Figure label="Análise" value={formatMs(latency)} detail="mediana" />
          <Figure
            label="Revisão"
            value={reviewShare === null ? "—" : formatPercent(reviewShare)}
            detail={`das últimas ${recent.length}`}
          />
        </dl>
      )}
    </section>
  );
}
