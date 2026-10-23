import { LoaderCircle } from "lucide-react";
import { useState } from "react";
import { ActionBar } from "@/components/station/action-bar";
import { ConnectionBanner, StationAlerts } from "@/components/station/alerts";
import { Belt } from "@/components/station/belt";
import { ControlDialog } from "@/components/station/control-dialog";
import { Equipment } from "@/components/station/equipment";
import { StationHeader } from "@/components/station/header";
import { InspectionPhoto } from "@/components/station/inspection-photo";
import { LotPulse } from "@/components/station/lot-pulse";
import { LotSetup } from "@/components/station/lot-setup";
import { RecentStrip } from "@/components/station/recent-strip";
import { Totals } from "@/components/station/totals";
import { Verdict } from "@/components/station/verdict";
import { useLive } from "@/lib/realtime/store";
import { currentInspection, decidedDestination } from "@/lib/station";

export function OperacaoPage() {
  const status = useLive((s) => s.status);
  const recent = useLive((s) => s.recent);
  const [controlOpen, setControlOpen] = useState(false);

  if (!status) {
    return (
      <div className="flex min-h-dvh flex-col">
        <ConnectionBanner />
        <StationHeader status={null} />
        <p className="m-auto flex items-center gap-3 text-lg text-muted-foreground">
          <LoaderCircle className="size-5 animate-spin" aria-hidden />
          Conectando ao serviço local…
        </p>
      </div>
    );
  }

  const latest = recent[0] ?? null;
  const onBelt = currentInspection(status, recent) !== null;
  const pendingReview =
    latest !== null && status.machine.pending_review_inspection_id === latest.id;

  return (
    <div className="flex min-h-dvh flex-col">
      <ConnectionBanner />
      <StationHeader status={status} />
      <main className="mx-auto w-full max-w-[120rem] flex-1 space-y-5 px-4 py-5 sm:px-6">
        <h1 className="sr-only">Operação da estação de inspeção</h1>
        <StationAlerts />
        {status.active_lot && status.active_lot_summary ? (
          <>
            <div className="grid grid-cols-1 gap-5 xl:grid-cols-12">
              <InspectionPhoto
                inspection={latest}
                onBelt={onBelt}
                className="aspect-[4/3] xl:col-span-7 xl:aspect-auto xl:min-h-[min(54vh,620px)]"
              />
              <Verdict
                inspection={latest}
                pendingReview={pendingReview}
                interactive
                footer={
                  <LotPulse
                    lotId={status.active_lot.id}
                    inspected={status.active_lot_summary.inspected}
                    inspection={latest}
                  />
                }
                className="xl:col-span-5"
              />
            </div>
            <Belt status={status} destination={decidedDestination(status, recent)} />
            <Totals summary={status.active_lot_summary} />
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
              <RecentStrip items={recent} className="lg:col-span-8" />
              <Equipment status={status} className="lg:col-span-4" />
            </div>
          </>
        ) : (
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
            <div className="lg:col-span-8">
              <LotSetup onNeedControl={() => setControlOpen(true)} />
            </div>
            <Equipment status={status} className="lg:col-span-4 lg:self-start" />
          </div>
        )}
      </main>
      <ActionBar status={status} onNeedControl={() => setControlOpen(true)} />
      <ControlDialog open={controlOpen} onOpenChange={setControlOpen} holder={status.control_holder} />
    </div>
  );
}
