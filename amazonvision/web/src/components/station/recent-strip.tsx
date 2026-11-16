import type { InspectionOut } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { DESTINATION } from "@/lib/labels";
import { cn } from "@/lib/utils";
import { GradeMark } from "./grade-mark";

function outcome(inspection: InspectionOut): string {
  if (inspection.cycle_status === "aborted") return "Interrompido";
  if (inspection.final_decision) return DESTINATION[inspection.final_decision];
  return "Aguardando revisão";
}

export function RecentStrip({ items, className }: { items: InspectionOut[]; className?: string }) {
  return (
    <section aria-labelledby="recent-heading" className={cn("min-w-0 rounded-lg border bg-card p-4", className)}>
      <h2 id="recent-heading" className="font-wide font-semibold">
        Últimas peças
      </h2>
      {items.length === 0 ? (
        <p className="mt-3 text-sm text-muted-foreground">As peças analisadas neste lote aparecem aqui.</p>
      ) : (
        <ol className="mt-3 grid grid-cols-[repeat(auto-fill,minmax(6.5rem,1fr))] gap-3">
          {items.map((item) => (
            <li key={item.id} className="min-w-0">
              <div className="relative overflow-hidden rounded-md border bg-muted">
                <img
                  src={item.image_url}
                  alt={`Inspeção ${item.id}`}
                  loading="lazy"
                  className="aspect-[4/3] w-full object-cover"
                />
                <GradeMark inspection={item} size="sm" className="absolute right-1 bottom-1 text-base" />
              </div>
              <p className="mt-1 truncate text-sm font-medium">{outcome(item)}</p>
              <p className="text-xs text-muted-foreground">{formatTime(item.captured_at)}</p>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
