import { Presentation } from "lucide-react";
import { Link } from "react-router";
import type { SystemStatus } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { MACHINE_STATE } from "@/lib/labels";
import { cn } from "@/lib/utils";
import { useProducts } from "./lot-setup";

export function Brand({ subtitle, large = false }: { subtitle?: string; large?: boolean }) {
  return (
    <div className="flex items-center gap-3">
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

function StateChip({ status }: { status: SystemStatus }) {
  const { machine } = status;
  const state = machine.state;
  const tone =
    state === "FAULT" || state === "ESTOP" || !machine.link.connected
      ? "bg-[#ff8f8f]"
      : state === "REVIEW_HOLD"
        ? "bg-[#9fb3ff]"
        : machine.running
          ? "bg-brand-bright"
          : "bg-white/50";
  const label = !machine.link.connected ? "Placa sem comunicação" : state ? MACHINE_STATE[state] : "Aguardando a placa";
  return (
    <p className="flex items-center gap-2 rounded-md bg-white/8 px-3 py-1.5 text-sm text-white">
      <span className={cn("size-2.5 rounded-full", tone)} aria-hidden />
      <span className="font-medium">{label}</span>
      {machine.running && <span className="text-white/65">em operação automática</span>}
    </p>
  );
}

export function StationHeader({ status }: { status: SystemStatus | null }) {
  const lot = status?.active_lot;
  const product = useProductName(lot?.product_id);
  return (
    <header className="bg-brand-deep text-white">
      <div className="mx-auto flex max-w-[120rem] flex-wrap items-center gap-x-8 gap-y-3 px-4 py-3 sm:px-6">
        <Brand />
        <div className="min-w-0 flex-1">
          {lot ? (
            <>
              <p className="font-wide text-lg leading-tight font-semibold">{product}</p>
              <p className="text-sm text-white/65">
                Lote {lot.id}
                <span className="max-sm:hidden">
                  , aberto às {formatTime(lot.started_at)} por {lot.operator}
                </span>
              </p>
            </>
          ) : (
            <p className="text-white/65">Nenhum lote aberto</p>
          )}
        </div>
        {status && <StateChip status={status} />}
        {status?.mode === "simulado" && (
          <p className="rounded-md border border-[#9fb3ff]/50 px-2.5 py-1 text-sm text-[#c9d4ff]">Bancada simulada</p>
        )}
        <Link
          to="/feira"
          className="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium text-white ring-1 ring-white/25 hover:bg-white/10"
        >
          <Presentation className="size-4" aria-hidden />
          Modo feira
        </Link>
      </div>
    </header>
  );
}
