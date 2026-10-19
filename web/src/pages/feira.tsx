import { Expand, LogOut } from "lucide-react";
import { Link } from "react-router";
import { ConnectionBanner } from "@/components/station/alerts";
import { Belt } from "@/components/station/belt";
import { Brand, useProductName } from "@/components/station/header";
import { InspectionPhoto } from "@/components/station/inspection-photo";
import { Totals } from "@/components/station/totals";
import { Verdict } from "@/components/station/verdict";
import { MACHINE_STATE } from "@/lib/labels";
import { useLive } from "@/lib/realtime/store";
import { blockers, currentInspection, decidedDestination } from "@/lib/station";

function requestFullscreen() {
  void document.documentElement.requestFullscreen?.().catch(() => undefined);
}

/** Public, read-only screen for visitors. No controls, readable from 2–3 metres. */
export function FeiraPage() {
  const status = useLive((s) => s.status);
  const recent = useLive((s) => s.recent);
  const product = useProductName(status?.active_lot?.product_id);
  const latest = recent[0] ?? null;
  const problem = blockers(status).find((b) => b.severity === "fault");

  return (
    <div className="feira flex h-dvh flex-col overflow-hidden bg-background text-foreground">
      <ConnectionBanner />
      <header className="flex items-center gap-8 px-8 py-5">
        <Brand
          large
          subtitle="A câmera fotografa cada peça, a inteligência artificial avalia e a esteira separa."
        />
        <div className="ml-auto text-right">
          {product ? (
            <p className="font-wide text-3xl font-semibold">{product}</p>
          ) : (
            <p className="text-2xl text-muted-foreground">Preparando a estação</p>
          )}
          {status?.active_lot && <p className="text-lg text-muted-foreground">Lote {status.active_lot.id}</p>}
        </div>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={requestFullscreen}
            className="rounded-md p-2 text-muted-foreground hover:bg-white/10"
            aria-label="Tela cheia"
          >
            <Expand className="size-5" />
          </button>
          <Link to="/" className="rounded-md p-2 text-muted-foreground hover:bg-white/10" aria-label="Sair do modo feira">
            <LogOut className="size-5" />
          </Link>
        </div>
      </header>

      <main className="flex min-h-0 flex-1 flex-col gap-5 px-8 pb-6">
        <h1 className="sr-only">AmazonVision 4.0, modo feira</h1>
        {problem && (
          <p role="status" className="rounded-lg bg-fault-soft px-6 py-3 text-2xl text-fault">
            {problem.title}
          </p>
        )}
        {status?.active_lot && status.active_lot_summary ? (
          <>
            <div className="grid min-h-0 flex-1 grid-cols-12 gap-6">
              <InspectionPhoto
                inspection={latest}
                onBelt={currentInspection(status, recent) !== null}
                className="col-span-7 h-full"
                dark
              />
              <Verdict
                inspection={latest}
                pendingReview={latest !== null && status.machine.pending_review_inspection_id === latest.id}
                large
                className="col-span-5 justify-center p-10"
              />
            </div>
            <Belt status={status} destination={decidedDestination(status, recent)} className="shrink-0" />
            <Totals summary={status.active_lot_summary} large />
          </>
        ) : (
          <div className="m-auto max-w-3xl text-center">
            <p className="font-wide text-5xl font-semibold">Inspeção visual de produtos da Amazônia</p>
            <p className="mt-6 text-2xl text-muted-foreground">
              {status?.machine.state ? `Esteira ${MACHINE_STATE[status.machine.state].toLowerCase()}. ` : ""}
              A demonstração começa quando a equipe abrir um lote.
            </p>
          </div>
        )}
      </main>

      <footer className="flex justify-between px-8 pb-4 text-base text-muted-foreground">
        <p>Feira Tecnológica FUCAPI 2026</p>
        {status?.mode === "simulado" && <p>Demonstração com bancada simulada</p>}
      </footer>
    </div>
  );
}
