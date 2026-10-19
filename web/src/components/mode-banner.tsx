import { FlaskConical } from "lucide-react";
import type { Health } from "@/lib/api/health";

export function ModeBanner({ mode }: { mode: Health["mode"] }) {
  if (mode !== "simulado") return null;
  return (
    <div role="status" className="bg-review-soft text-review">
      <p className="mx-auto flex max-w-7xl items-center gap-2 px-4 py-2 text-sm font-medium sm:px-6">
        <FlaskConical className="size-4 shrink-0" aria-hidden />
        Modo simulado: bancada, câmera e modelo são simulados. Nenhum dado é de operação real.
      </p>
    </div>
  );
}
