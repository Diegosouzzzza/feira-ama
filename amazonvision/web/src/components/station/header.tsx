import { MobileNav } from "@/components/layout/sidebar";
import type { SystemStatus } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { MACHINE_STATE } from "@/lib/labels";
import { cn } from "@/lib/utils";
import { useProducts } from "./lot-setup";

export function Brand({ subtitle, large = false }: { subtitle?: string; large?: boolean }) {
  return (
    <div className="flex shrink-0 items-center gap-3">
      <img src="/favicon.svg" alt="" className={large ? "size-14" : "size-9"} />
      <div className="leading-tight">
        <p className={cn("font-wide font-semibold tracking-tight text-white", large ? "text-3xl" : "text-lg")}>
          AmazonVision <span className="text-brand-bright">4.0</span>
        </p>
        {subtitle && <p className={cn("text-white/65", large ? "mt-1 text-xl" : "text-sm")}>{subtitle}</p>}
      </div>
    </div>
  );
}

export function useProductName(productId: string | undefined): string | undefined {
  const products = useProducts();
  return productId ? (products.data?.find((p) => p.id === productId)?.name ?? productId) : undefined;
}

/** Machine state in one place; the simulated bench is named here so it is never mistaken
 *  for the real one, without a second badge competing for attention. */
function StateChip({ status }: { status: SystemStatus }) {
  const { machine } = status;
  const state = machine.state;
  const tone =
    state === "FAULT" || state === "ESTOP" || !machine.link.connected
      ? "bg-signal-fault"
      : state === "REVIEW_HOLD"
        ? "bg-signal-review"
        : machine.running
          ? "bg-signal-ok"
          : "bg-signal-idle";
  const label = !machine.link.connected ? "Placa sem comunicação" : state ? MACHINE_STATE[state] : "Aguardando a placa";
  return (
    <p className="flex shrink-0 items-center gap-2 rounded-md border px-3 py-1.5 text-sm whitespace-nowrap">
      <span className={cn("size-2.5 rounded-full", tone)} aria-hidden />
      <span className="font-medium">{label}</span>
      {status.mode === "simulado" && <span className="border-l pl-2 text-review">Simulada</span>}
    </p>
  );
}

/** Thin top bar of every team screen: the open lot on the left, machine state on the right. */
export function StationHeader({ status }: { status: SystemStatus | null }) {
  const lot = status?.active_lot;
  const product = useProductName(lot?.product_id);
  return (
    <header className="sticky top-0 z-10 flex h-14 shrink-0 items-center gap-3 border-b bg-background px-4 sm:px-6">
      <MobileNav />
      <div
        className="min-w-0 flex-1 leading-tight"
        title={lot ? `Lote ${lot.id}, aberto às ${formatTime(lot.started_at)} por ${lot.operator}` : undefined}
      >
        {lot ? (
          <p className="flex min-w-0 items-baseline gap-2">
            <span className="truncate font-semibold">{product}</span>
            <span className="shrink-0 text-sm text-muted-foreground max-sm:hidden">Lote {lot.id}</span>
          </p>
        ) : (
          <p className="text-sm text-muted-foreground">Nenhum lote aberto</p>
        )}
      </div>
      {status && <StateChip status={status} />}
    </header>
  );
}