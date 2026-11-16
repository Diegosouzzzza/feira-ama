import { createContext, type ReactNode, useContext, useState } from "react";
import { useIsController } from "@/components/station/action-bar";
import { ConnectionBanner } from "@/components/station/alerts";
import { ControlDialog } from "@/components/station/control-dialog";
import { StationHeader } from "@/components/station/header";
import type { SystemStatus } from "@/lib/api/types";
import { useLive } from "@/lib/realtime/store";
import { cn } from "@/lib/utils";

const RequestControl = createContext<() => void>(() => {});

/** Header, connection banner and the control dialog shared by the secondary screens. */
export function PageShell({
  title,
  intro,
  children,
  className,
}: {
  title: string;
  intro?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  const status = useLive((s) => s.status);
  const [controlOpen, setControlOpen] = useState(false);
  return (
    <RequestControl.Provider value={() => setControlOpen(true)}>
      <div className="flex min-h-dvh flex-col">
        <ConnectionBanner />
        <StationHeader status={status} />
        <main className={cn("mx-auto w-full max-w-[100rem] flex-1 space-y-8 px-4 py-6 sm:px-6", className)}>
          <div className="space-y-2">
            <h1 className="font-wide text-3xl font-semibold tracking-tight">{title}</h1>
            {intro && <p className="max-w-3xl text-muted-foreground">{intro}</p>}
          </div>
          {children}
        </main>
        <ControlDialog open={controlOpen} onOpenChange={setControlOpen} holder={status?.control_holder ?? null} />
      </div>
    </RequestControl.Provider>
  );
}

export function useStation(): { status: SystemStatus | null; controller: boolean } {
  const status = useLive((s) => s.status);
  return { status, controller: useIsController(status) };
}

/** Shown in place of controls that need the station's operator seat. */
export function NeedControl({ action }: { action: string }) {
  const requestControl = useContext(RequestControl);
  const { status } = useStation();
  return (
    <p className="text-sm">
      Para {action}, esta tela precisa ter o controle da estação.{" "}
      <button type="button" className="font-medium text-primary underline" onClick={requestControl}>
        {status?.control_holder ? "Assumir o controle" : "Operar a estação"}
      </button>
    </p>
  );
}
