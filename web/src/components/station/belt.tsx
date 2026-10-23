import type { Destination, SystemStatus } from "@/lib/api/types";
import { MACHINE_STATE } from "@/lib/labels";
import { type PiecePosition, piecePosition } from "@/lib/station";
import { cn } from "@/lib/utils";

// Wide, short drawing: text stays near its CSS size from notebook to Full HD.
const WIDTH = 1600;
const HEIGHT = 176;
const Y_MAIN = 58;
const Y_REJECT = 136;
const X = { entry: 70, camera: 560, sorter: 1020, fork: 1110, end: 1540 };

function piecePoint(position: PiecePosition, destination: Destination | null): [number, number] {
  switch (position) {
    case "to-camera":
      return [(X.entry + X.camera) / 2, Y_MAIN];
    case "at-camera":
      return [X.camera, Y_MAIN];
    case "to-sorter":
      return [(X.camera + X.sorter) / 2, Y_MAIN];
    case "at-sorter":
      return [X.sorter, Y_MAIN];
    case "leaving":
      if (destination === "APPROVED") return [1440, Y_MAIN];
      if (destination === "REJECTED") return [1440, Y_REJECT];
      return [1160, Y_MAIN];
    default:
      return [X.entry, Y_MAIN];
  }
}

const SEGMENTS: { id: string; from: number; to: number; active: PiecePosition[] }[] = [
  { id: "a", from: X.entry, to: X.camera, active: ["to-camera"] },
  { id: "b", from: X.camera, to: X.sorter, active: ["to-sorter"] },
];

function Station({
  x,
  label,
  sensor,
  sensorOn,
  here,
}: {
  x: number;
  label: string;
  sensor?: string;
  sensorOn?: boolean;
  here: boolean;
}) {
  return (
    <g>
      <circle
        cx={x}
        cy={Y_MAIN}
        r={18}
        className={cn("stroke-[3]", here ? "fill-card stroke-primary" : "fill-card stroke-border")}
      />
      <text x={x} y={Y_MAIN + 52} textAnchor="middle" className="fill-foreground text-[21px] font-medium">
        {label}
      </text>
      {sensor && (
        <g>
          <circle
            cx={x + 34}
            cy={Y_MAIN - 32}
            r={8}
            className={sensorOn ? "fill-grade-a" : "fill-muted stroke-border"}
          />
          <text x={x + 50} y={Y_MAIN - 25} className="fill-muted-foreground text-[18px]">
            {sensor}
          </text>
        </g>
      )}
    </g>
  );
}

function BeltDiagram({ status, destination }: { status: SystemStatus; destination: Destination | null }) {
  const position = piecePosition(status.machine.state);
  const [px, py] = piecePoint(position, destination);
  const sensors = status.machine.sensors;
  const exiting = position === "at-sorter" || position === "leaving";
  const approvedLit = exiting && destination === "APPROVED";
  const rejectedLit = exiting && destination === "REJECTED";

  return (
    <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="h-auto w-full" role="img" aria-labelledby="belt-title">
      <title id="belt-title">Esquema da esteira com a posição atual da peça</title>
      <line x1={X.entry} y1={Y_MAIN} x2={X.end} y2={Y_MAIN} className="stroke-muted stroke-[12]" strokeLinecap="round" />
      <path
        d={`M ${X.fork} ${Y_MAIN} C ${X.fork + 100} ${Y_MAIN}, ${X.fork + 80} ${Y_REJECT}, ${X.fork + 190} ${Y_REJECT} L ${X.end} ${Y_REJECT}`}
        className={cn("fill-none stroke-[12]", rejectedLit ? "stroke-grade-c" : "stroke-muted")}
        strokeLinecap="round"
      />
      {SEGMENTS.map((s) => (
        <line
          key={s.id}
          x1={s.from}
          y1={Y_MAIN}
          x2={s.to}
          y2={Y_MAIN}
          strokeLinecap="round"
          className={cn("stroke-[12]", s.active.includes(position) ? "stroke-primary" : "stroke-transparent")}
        />
      ))}
      {approvedLit && (
        <line x1={X.fork} y1={Y_MAIN} x2={X.end} y2={Y_MAIN} strokeLinecap="round" className="stroke-grade-a stroke-[12]" />
      )}

      <Station x={X.entry} label="Entrada" here={position === "none"} />
      <Station
        x={X.camera}
        label="Câmera"
        sensor="S1"
        sensorOn={sensors?.s1}
        here={position === "at-camera"}
      />
      <Station x={X.sorter} label="Pá" sensor="S2" sensorOn={sensors?.s2} here={position === "at-sorter"} />

      <text x={X.end} y={Y_MAIN - 22} textAnchor="end" className={cn("text-[21px] font-medium", approvedLit ? "fill-grade-a" : "fill-muted-foreground")}>
        Aprovados
      </text>
      <text x={X.end} y={Y_REJECT - 22} textAnchor="end" className={cn("text-[21px] font-medium", rejectedLit ? "fill-grade-c" : "fill-muted-foreground")}>
        Rejeitados
      </text>

      {position !== "none" && (
        <g style={{ transform: `translate(${px}px, ${py}px)`, transition: "transform 700ms ease-in-out" }}>
          <ellipse rx={20} ry={14} className="fill-piece stroke-[3] stroke-card" />
        </g>
      )}
    </svg>
  );
}

const STEPS: { position: PiecePosition[]; label: string }[] = [
  { position: ["to-camera"], label: "Indo para a câmera" },
  { position: ["at-camera"], label: "Na câmera" },
  { position: ["to-sorter"], label: "Indo para a pá" },
  { position: ["at-sorter"], label: "Na pá" },
  { position: ["leaving"], label: "Saindo" },
];

function BeltCompact({ status }: { status: SystemStatus }) {
  const position = piecePosition(status.machine.state);
  const current = STEPS.findIndex((s) => s.position.includes(position));
  return (
    <ol className="grid grid-cols-5 gap-1" aria-label="Etapas da peça na esteira">
      {STEPS.map((step, i) => (
        <li key={step.label} className="space-y-1">
          <div className={cn("h-1.5 rounded-full", i <= current && current >= 0 ? "bg-primary" : "bg-muted")} />
          <p className={cn("text-xs leading-tight", i === current ? "font-semibold" : "text-muted-foreground")}>
            {step.label}
          </p>
        </li>
      ))}
    </ol>
  );
}

export function Belt({
  status,
  destination,
  className,
}: {
  status: SystemStatus;
  destination: Destination | null;
  className?: string;
}) {
  const state = status.machine.state;
  const cycle = status.current_cycle;
  const sensors = status.machine.sensors;
  return (
    <section aria-labelledby="belt-heading" className={cn("rounded-lg border bg-card px-5 py-4", className)}>
      <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1">
        <h2 id="belt-heading" className="font-wide text-lg font-semibold">
          {state ? MACHINE_STATE[state] : "Estado da esteira desconhecido"}
        </h2>
        <p className="text-sm text-muted-foreground">
          {cycle ? `Peça ${cycle.seq_in_lot} do lote` : "Nenhuma peça na esteira"}
          <span className="sr-only">
            {sensors ? `. Sensor S1 ${sensors.s1 ? "ativo" : "livre"}, sensor S2 ${sensors.s2 ? "ativo" : "livre"}.` : ""}
          </span>
        </p>
      </div>
      <div className="mt-2 hidden lg:block">
        <BeltDiagram status={status} destination={destination} />
      </div>
      <div className="mt-3 lg:hidden">
        <BeltCompact status={status} />
      </div>
    </section>
  );
}
