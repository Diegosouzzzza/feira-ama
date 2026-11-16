import type { LotSummary } from "@/lib/api/types";
import { formatInt, formatPercent } from "@/lib/format";
import { cn } from "@/lib/utils";

function Figure({
  label,
  value,
  tone,
  large,
}: {
  label: string;
  value: number;
  tone?: string;
  large: boolean;
}) {
  return (
    <div className="min-w-0 px-4 py-3 first:pl-0 max-sm:odd:pl-0 sm:px-6">
      <dt className={cn("text-muted-foreground", large ? "text-xl" : "text-sm")}>{label}</dt>
      <dd
        className={cn(
          "font-display mt-1",
          tone,
          large ? "text-[clamp(2.5rem,5.5vh,3.5rem)]" : "text-4xl",
        )}
      >
        {formatInt(value)}
      </dd>
    </div>
  );
}

/** Lot counters as stored in the database (the browser never counts on its own). */
export function Totals({ summary, large = false }: { summary: LotSummary; large?: boolean }) {
  return (
    <section aria-label="Totais do lote">
      <dl className="grid grid-cols-2 divide-border sm:grid-cols-4 sm:divide-x">
        <Figure label="Inspecionadas" value={summary.inspected} large={large} />
        <Figure label="Aprovadas" value={summary.approved} tone="text-grade-a" large={large} />
        <Figure label="Rejeitadas" value={summary.rejected} tone="text-grade-c" large={large} />
        <Figure
          label="Aguardando revisão"
          value={summary.review_pending}
          tone={summary.review_pending ? "text-review" : undefined}
          large={large}
        />
      </dl>
      <p className={cn("mt-1 text-muted-foreground", large ? "text-lg" : "text-sm")}>
        {summary.approval_rate_denominator > 0
          ? `${formatPercent(summary.approval_rate)} aprovadas entre ${formatInt(summary.approval_rate_denominator)} peças já decididas.`
          : "A taxa de aprovação aparece depois da primeira peça decidida."}
        {summary.cycles_aborted > 0 && ` ${formatInt(summary.cycles_aborted)} ciclo(s) interrompido(s).`}
      </p>
    </section>
  );
}
