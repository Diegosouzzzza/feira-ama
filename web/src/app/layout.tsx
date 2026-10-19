import { Outlet } from "react-router";
import { ModeBanner } from "@/components/mode-banner";
import { useHealth } from "@/lib/api/health";

function Brand() {
  return (
    <div className="flex items-center gap-3">
      <img src="/favicon.svg" alt="" className="size-9" />
      <div className="leading-tight">
        <p className="text-lg font-semibold tracking-tight text-white">
          Amazon<span className="text-brand-bright">Vision</span> 4.0
        </p>
        <p className="text-xs text-white/60">Inspeção visual de qualidade</p>
      </div>
    </div>
  );
}

export function AppLayout() {
  const health = useHealth();

  return (
    <div className="flex min-h-dvh flex-col">
      <header className="bg-brand-deep">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <Brand />
          <p className="hidden text-sm text-white/60 sm:block">Feira Tecnológica FUCAPI 2026</p>
        </div>
      </header>
      {health.data && <ModeBanner mode={health.data.mode} />}
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-6 sm:py-8">
        <Outlet />
      </main>
    </div>
  );
}
