import { Presentation } from "lucide-react";
import { Link, NavLink } from "react-router";
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

const SCREENS = [
  { to: "/", label: "Operação" },
  { to: "/historico", label: "Histórico" },
  { to: "/coleta", label: "Coleta" },
  { to: "/concordancia", label: "Concordância" },
  { to: "/modelos", label: "Modelos" },
  { to: "/configuracao", label: "Configuração" },
  { to: "/diagnostico", label: "Diagnóstico" },
];

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
    <p className="flex shrink-0 items-center gap-2 rounded-md bg-white/8 px-3 py-1.5 text-sm whitespace-nowrap text-white">
      <span className={cn("size-2.5 rounded-full", tone)} aria-hidden />
      <span className="font-medium">{label}</span>
      {status.mode === "simulado" && (
        <span className="border-l border-white/20 pl-2 text-signal-review">Simulada</span>
      )}
    </p>
  );
}

export function StationHeader({ status }: { status: SystemStatus | null }) {
  const lot = status?.active_lot;
  const product = useProductName(lot?.product_id);
  return (
    <header className="bg-brand-deep text-white">
      <div className="mx-auto flex max-w-[120rem] flex-wrap items-center gap-x-5 gap-y-2 px-4 pt-3 pb-2 sm:px-6 min-[1380px]:flex-nowrap min-[1380px]:pb-3">
        <Brand />
        <nav
          aria-label="Telas"
          className="order-last -mx-1 w-full overflow-x-auto min-[1380px]:order-none min-[1380px]:mx-0 min-[1380px]:w-auto min-[1380px]:overflow-visible"
        >
          <ul className="flex gap-0.5 px-1 min-[1380px]:px-0">
            {SCREENS.map((item) => (
              <li key={item.to} className="shrink-0">
                <NavLink
                  to={item.to}
                  end
                  className={({ isActive }) =>
                    cn(
                      "block rounded-md px-2.5 py-1.5 text-sm font-medium whitespace-nowrap",
                      isActive ? "bg-white/15 text-white" : "text-white/70 hover:bg-white/10 hover:text-white",
                    )
                  }
                >
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="ml-auto flex min-w-0 items-center gap-3">
          <div
            className="min-w-0 text-right leading-tight max-sm:hidden"
            title={lot ? `Lote ${lot.id}, aberto às ${formatTime(lot.started_at)} por ${lot.operator}` : undefined}
          >
            {lot ? (
              <>
                <p className="truncate font-semibold">{product}</p>
                <p className="text-sm text-white/65">Lote {lot.id}</p>
              </>
            ) : (
              <p className="text-sm text-white/65">Nenhum lote aberto</p>
            )}
          </div>
          {status && <StateChip status={status} />}
          <Link
            to="/feira"
            title="Abrir o modo feira"
            className="flex shrink-0 items-center gap-2 rounded-md px-2.5 py-1.5 text-sm font-medium text-white ring-1 ring-white/25 hover:bg-white/10"
          >
            <Presentation className="size-4" aria-hidden />
            <span className="max-2xl:sr-only">Modo feira</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
