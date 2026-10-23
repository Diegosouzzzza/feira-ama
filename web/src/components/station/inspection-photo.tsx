import { ImageOff } from "lucide-react";
import { useState } from "react";
import type { InspectionOut } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { GRADE } from "@/lib/labels";
import { cn } from "@/lib/utils";

function altText(inspection: InspectionOut): string {
  const grade = inspection.predicted_grade
    ? `${GRADE[inspection.predicted_grade].title}, ${GRADE[inspection.predicted_grade].meaning.toLowerCase()}`
    : "sem classe prevista";
  return `Foto da peça analisada na inspeção ${inspection.id}: ${grade}.`;
}

/** The photo the model actually analysed: never a newer live frame with an older label. */
export function InspectionPhoto({
  inspection,
  onBelt,
  className,
  dark = false,
}: {
  inspection: InspectionOut | null;
  onBelt: boolean;
  className?: string;
  dark?: boolean;
}) {
  const [failed, setFailed] = useState<number | null>(null);

  return (
    <figure
      className={cn(
        "relative flex min-h-0 flex-col overflow-hidden rounded-lg border bg-card",
        className,
      )}
    >
      <div
        className={cn(
          "relative grid min-h-0 flex-1 place-items-center",
          dark ? "bg-black/30" : "bg-photo-mat",
        )}
      >
        {inspection && failed !== inspection.id ? (
          <img
            key={inspection.id}
            src={inspection.image_url}
            alt={altText(inspection)}
            onError={() => setFailed(inspection.id)}
            className="absolute inset-0 size-full object-contain"
          />
        ) : inspection ? (
          <p className="flex items-center gap-2 p-6 text-muted-foreground">
            <ImageOff className="size-5" aria-hidden />A imagem desta inspeção não está disponível.
          </p>
        ) : (
          <p className="max-w-xs p-8 text-center text-muted-foreground">
            Aguardando a primeira peça do lote. A foto aparece aqui assim que a câmera a capturar.
          </p>
        )}
      </div>
      {inspection && (
        <figcaption className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-t px-4 py-2.5 text-sm">
          <span className="font-medium">
            {onBelt ? "Peça na esteira agora" : "Última peça analisada"}
          </span>
          <span className="text-muted-foreground">
            Inspeção {inspection.id}, foto das {formatTime(inspection.captured_at)}
          </span>
        </figcaption>
      )}
    </figure>
  );
}
