import { ImageOff } from "lucide-react";
import { type CSSProperties, type ReactNode, useState } from "react";
import { visibleAnomalyRegions } from "@/lib/anomaly";
import type { InspectionOut, ProductConfigOut } from "@/lib/api/types";
import { formatTime } from "@/lib/format";
import { GRADE } from "@/lib/labels";
import { cn } from "@/lib/utils";

function altText(inspection: InspectionOut): string {
  const grade = inspection.predicted_grade
    ? `${GRADE[inspection.predicted_grade].title}, ${GRADE[inspection.predicted_grade].meaning.toLowerCase()}`
    : "sem classe prevista";
  return `Foto da peça analisada na inspeção ${inspection.id}: ${grade}.`;
}

function percent(fraction: number): string {
  return `${fraction * 100}%`;
}

/** Proportional frame keeping ROI and anomaly boxes aligned to the photo's natural aspect. */
export function InspectionStage({
  inspection,
  roi = null,
  showAnomalyRegions = true,
  scanning = false,
  hud,
  alt,
  highPriority = false,
  onError,
  className,
}: {
  inspection: InspectionOut;
  roi?: ProductConfigOut["roi"];
  showAnomalyRegions?: boolean;
  scanning?: boolean;
  hud?: ReactNode;
  alt: string;
  highPriority?: boolean;
  onError?: () => void;
  className?: string;
}) {
  const [aspect, setAspect] = useState(4 / 3);
  const regions = scanning ? [] : visibleAnomalyRegions(inspection, showAnomalyRegions);
  // Same rule as the verdict: before the board confirms, a confident rejection is already red.
  const destination =
    inspection.final_decision ?? (inspection.auto_decision === "REVIEW" ? null : inspection.auto_decision);
  const reviewTone = destination !== "REJECTED";

  return (
    <div className={cn("fair-photo__image-wrap bg-photo-mat", className)}>
      <div className="fair-photo__frame" style={{ "--photo-aspect": aspect } as CSSProperties}>
        <img
          key={inspection.id}
          src={inspection.image_url}
          alt={alt}
          fetchPriority={highPriority ? "high" : undefined}
          onLoad={(event) => {
            const { naturalWidth, naturalHeight } = event.currentTarget;
            if (naturalWidth > 0 && naturalHeight > 0) setAspect(naturalWidth / naturalHeight);
          }}
          onError={onError}
          className="block size-full object-contain"
        />
        {roi ? (
          <span
            className="fair-photo__roi"
            style={{
              left: percent(roi.x),
              top: percent(roi.y),
              width: percent(roi.width),
              height: percent(roi.height),
            }}
            aria-hidden="true"
          />
        ) : null}
        {regions.map((region, index) => (
          <span
            key={`${inspection.id}-reg-${index}`}
            className={cn("fair-photo__anomaly", reviewTone && "fair-photo__anomaly--review")}
            style={{
              left: percent(region.x),
              top: percent(region.y),
              width: percent(region.width),
              height: percent(region.height),
            }}
            aria-hidden="true"
          >
            {index === 0 ? (
              <em>{regions.length === 1 ? "Desvio detectado" : `${regions.length} regiões`}</em>
            ) : null}
          </span>
        ))}
        {scanning ? <span className="fair-photo__scan" aria-hidden="true" /> : null}
      </div>
      {hud}
    </div>
  );
}

/** The photo the model actually analysed: never a newer live frame with an older label. */
export function InspectionPhoto({
  inspection,
  onBelt,
  roi = null,
  className,
}: {
  inspection: InspectionOut | null;
  onBelt: boolean;
  roi?: ProductConfigOut["roi"];
  className?: string;
}) {
  const [failed, setFailed] = useState<number | null>(null);
  const regions = visibleAnomalyRegions(inspection);

  return (
    <figure
      className={cn(
        "relative flex min-h-0 flex-col overflow-hidden rounded-lg border bg-card",
        className,
      )}
    >
      {inspection && failed !== inspection.id ? (
        <InspectionStage
          inspection={inspection}
          roi={roi}
          alt={altText(inspection)}
          onError={() => setFailed(inspection.id)}
          className="aspect-[4/3] min-h-0 flex-1 xl:aspect-auto"
        />
      ) : (
        <div className="relative grid min-h-0 flex-1 place-items-center bg-photo-mat">
          {inspection ? (
            <p className="flex items-center gap-2 p-6 text-muted-foreground">
              <ImageOff className="size-5" aria-hidden />A imagem desta inspeção não está disponível.
            </p>
          ) : (
            <p className="max-w-xs p-8 text-center text-muted-foreground">
              Aguardando a primeira peça do lote. A foto aparece aqui assim que a câmera a capturar.
            </p>
          )}
        </div>
      )}
      {inspection && (
        <figcaption className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-t px-4 py-2.5 text-sm">
          <span className="font-medium">
            {onBelt ? "Peça na esteira agora" : "Última peça analisada"}
            {regions.length > 0 ? ` · ${regions.length} ${regions.length === 1 ? "região destacada" : "regiões destacadas"}` : ""}
          </span>
          <span className="text-muted-foreground">
            Inspeção {inspection.id}, foto das {formatTime(inspection.captured_at)}
          </span>
        </figcaption>
      )}
    </figure>
  );
}
