import { ArrowDownRight, ArrowRight, CircleAlert, Hand } from "lucide-react";
import { type FormEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import type { Destination, InspectionOut, ReviewOut } from "@/lib/api/types";
import { controlPost, useControl } from "@/lib/control";
import { formatPercent } from "@/lib/format";
import { DESTINATION, GRADE, REVIEW_REASON } from "@/lib/labels";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";
import { GradeMark, inspectionTone } from "./grade-mark";
import { TONE } from "./tone";

function Headline({ inspection, large }: { inspection: InspectionOut; large: boolean }) {
  const review = inspection.auto_decision === "REVIEW";
  const decided = review && inspection.decided_by === "operator";
  const suggestion = inspection.predicted_grade
    ? ` O modelo sugeriu ${GRADE[inspection.predicted_grade].title}.`
    : "";
  const title = decided
    ? "Decidida pelo operador"
    : review
      ? "Inconclusivo"
      : inspection.predicted_grade
        ? GRADE[inspection.predicted_grade].title
        : "Sem classe";
  const meaning = review
    ? `${REVIEW_REASON[inspection.review_reason ?? "LOW_CONFIDENCE"]}.${suggestion}`
    : inspection.predicted_grade
      ? GRADE[inspection.predicted_grade].meaning
      : "";
  return (
    <div className="min-w-0">
      <p
        className={cn(
          "font-wide font-bold tracking-tight",
          TONE[inspectionTone(inspection)].text,
          large ? "text-[clamp(2.75rem,6vh,4rem)] leading-none" : "text-3xl leading-none sm:text-4xl",
        )}
      >
        {title}
      </p>
      <p className={cn("mt-2 text-muted-foreground", large ? "text-2xl" : "text-lg")}>{meaning}</p>
    </div>
  );
}

function Confidence({ inspection, large }: { inspection: InspectionOut; large: boolean }) {
  if (inspection.confidence === null) return null;
  return (
    <div>
      <div className={cn("flex items-baseline justify-between gap-3", large ? "text-xl" : "text-base")}>
        <span className="text-muted-foreground">Confiança estimada do modelo</span>
        <span className="font-semibold">{formatPercent(inspection.confidence)}</span>
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" aria-hidden>
        <div
          className={cn("h-full", TONE[inspectionTone(inspection)].solid)}
          style={{ width: `${Math.round(inspection.confidence * 100)}%` }}
        />
      </div>
    </div>
  );
}

function Route({ inspection, large }: { inspection: InspectionOut; large: boolean }) {
  if (inspection.cycle_status === "aborted") {
    return (
      <p className={cn("flex items-center gap-2 text-fault", large ? "text-xl" : "text-base")}>
        <CircleAlert className="size-5 shrink-0" aria-hidden />
        Ciclo interrompido: a separação desta peça não foi concluída.
      </p>
    );
  }
  if (!inspection.final_decision) return null;
  const Icon = inspection.final_decision === "APPROVED" ? ArrowRight : ArrowDownRight;
  return (
    <div className={cn("flex items-center gap-3", large ? "text-2xl" : "text-lg")}>
      <Icon className={cn("shrink-0", large ? "size-8" : "size-6")} aria-hidden />
      <span>
        Destino comandado: <strong className="font-semibold">{DESTINATION[inspection.final_decision]}</strong>
        {inspection.decided_by === "operator" && (
          <span className="text-muted-foreground"> (decisão do operador)</span>
        )}
      </span>
    </div>
  );
}

function ReviewForm({ inspection }: { inspection: InspectionOut }) {
  const { token, operator } = useControl();
  const [reason, setReason] = useState("");
  const [sending, setSending] = useState<Destination | null>(null);
  const ready = reason.trim().length >= 3;

  async function decide(decision: Destination) {
    if (!ready || !operator) return;
    setSending(decision);
    try {
      await controlPost<ReviewOut>(`/inspections/${inspection.id}/review`, {
        request_id: crypto.randomUUID(),
        decision,
        reviewer: operator,
        reason: reason.trim(),
      });
    } catch (error) {
      notifyError(error);
    } finally {
      setSending(null);
    }
  }

  if (!token) {
    return (
      <p className="flex items-start gap-2 rounded-md bg-review-soft p-3 text-review">
        <Hand className="mt-0.5 size-5 shrink-0" aria-hidden />A peça está parada esperando a decisão
        do operador. Assuma o controle da estação para decidir.
      </p>
    );
  }

  return (
    <form
      className="space-y-3 rounded-md border border-review/40 bg-review-soft p-4"
      onSubmit={(e: FormEvent) => e.preventDefault()}
    >
      <p className="font-medium text-review">A peça está parada esperando sua decisão.</p>
      <div className="space-y-1.5">
        <Label htmlFor="review-reason">O que você observou na peça?</Label>
        <Textarea
          id="review-reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Ex.: mancha escura na lateral"
          maxLength={200}
          rows={2}
          className="bg-card"
        />
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Button
          type="button"
          size="lg"
          disabled={!ready || sending !== null}
          onClick={() => decide("APPROVED")}
          className="bg-grade-a text-white hover:bg-grade-a/90"
        >
          {sending === "APPROVED" ? "Enviando…" : "Aprovar peça"}
        </Button>
        <Button
          type="button"
          size="lg"
          disabled={!ready || sending !== null}
          onClick={() => decide("REJECTED")}
          className="bg-grade-c text-white hover:bg-grade-c/90"
        >
          {sending === "REJECTED" ? "Enviando…" : "Rejeitar peça"}
        </Button>
      </div>
      {!ready && <p className="text-sm text-muted-foreground">Descreva o motivo para liberar a decisão.</p>}
    </form>
  );
}

/** Result of the latest inspection. `large` is the fair-mode scale, read from 2–3 m. */
export function Verdict({
  inspection,
  pendingReview,
  large = false,
  interactive = false,
  className,
}: {
  inspection: InspectionOut | null;
  pendingReview: boolean;
  large?: boolean;
  interactive?: boolean;
  className?: string;
}) {
  return (
    <section
      aria-labelledby="verdict-title"
      className={cn("flex min-h-0 flex-col gap-6 rounded-lg border bg-card p-6", className)}
    >
      <h2 id="verdict-title" className="sr-only">
        Resultado da inspeção
      </h2>
      {inspection ? (
        <div aria-live="polite" className="flex flex-col gap-6">
          <div className="flex items-center gap-4 sm:gap-5">
            <GradeMark inspection={inspection} size={large ? "feira" : "xl"} />
            <Headline inspection={inspection} large={large} />
          </div>
          <Confidence inspection={inspection} large={large} />
          <Route inspection={inspection} large={large} />
          {interactive && pendingReview && <ReviewForm inspection={inspection} />}
          {!interactive && pendingReview && (
            <p className={cn("text-review", large ? "text-2xl" : "text-base")}>
              O operador está conferindo esta peça.
            </p>
          )}
        </div>
      ) : (
        <p className={cn("text-muted-foreground", large ? "text-2xl" : "text-lg")}>
          Nenhuma peça analisada neste lote ainda.
        </p>
      )}
    </section>
  );
}
