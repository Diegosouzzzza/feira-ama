import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Camera, CameraOff, ChevronLeft, ChevronRight, Copy, FileDown, SkipForward } from "lucide-react";
import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { useIsController } from "@/components/station/action-bar";
import { ConnectionBanner } from "@/components/station/alerts";
import { ControlDialog } from "@/components/station/control-dialog";
import { StationHeader } from "@/components/station/header";
import { useProducts } from "@/components/station/lot-setup";
import { TONE } from "@/components/station/tone";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { apiGet } from "@/lib/api/client";
import type {
  DatasetExportOut,
  DatasetSampleOut,
  DatasetSamplePage,
  DatasetSummary,
  Grade,
  SampleStatus,
} from "@/lib/api/types";
import { controlPatch, controlPost } from "@/lib/control";
import { formatTime } from "@/lib/format";
import { GRADE } from "@/lib/labels";
import { notifyError } from "@/lib/notify";
import { useLive } from "@/lib/realtime/store";
import { nextPiece } from "@/lib/collection";
import { cn } from "@/lib/utils";

const GRADES: Grade[] = ["A", "B", "C"];
const PAGE_SIZE = 24;
const SETUP_KEY = "av-coleta";

const STATUS_LABEL: Record<SampleStatus, string> = {
  pending: "Sem rótulo",
  labeled: "Rotulada",
  ambiguous: "Ambígua",
  unusable: "Inutilizável",
};

// ---------------------------------------------------------------- collection setup

interface Setup {
  productId: string;
  session: string;
  piece: string;
}

function today(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

function loadSetup(): Setup {
  const fallback = { productId: "tucuma", session: today(), piece: "T-0001" };
  try {
    const raw = localStorage.getItem(SETUP_KEY);
    return raw ? { ...fallback, ...(JSON.parse(raw) as Partial<Setup>) } : fallback;
  } catch {
    return fallback;
  }
}

function saveSetup(setup: Setup): void {
  try {
    localStorage.setItem(SETUP_KEY, JSON.stringify(setup));
  } catch {
    // Blocked storage: the form simply starts from the defaults next time.
  }
}

const TAG = /^[A-Za-z0-9][A-Za-z0-9_-]{0,39}$/;

// ---------------------------------------------------------------- data

function useSummary(productId: string) {
  return useQuery({
    queryKey: ["dataset-summary", productId],
    queryFn: ({ signal }) =>
      apiGet<DatasetSummary>(`/dataset/summary?product_id=${encodeURIComponent(productId)}`, { signal }),
  });
}

type Filter = "pending" | "labeled" | "ambiguous" | "unusable" | "all";

function useSamples(productId: string, filter: Filter, page: number) {
  const params = new URLSearchParams({
    product_id: productId,
    limit: String(PAGE_SIZE),
    offset: String(page * PAGE_SIZE),
  });
  if (filter !== "all") params.set("status", filter);
  return useQuery({
    queryKey: ["dataset-samples", productId, filter, page],
    queryFn: ({ signal }) => apiGet<DatasetSamplePage>(`/dataset/samples?${params}`, { signal }),
    placeholderData: (previous) => previous,
  });
}

// ---------------------------------------------------------------- live view

function LiveView({ lastCapture }: { lastCapture: DatasetSampleOut | null }) {
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!failed) return;
    const retry = window.setTimeout(() => {
      setFailed(false);
      setAttempt((n) => n + 1);
    }, 3000);
    return () => window.clearTimeout(retry);
  }, [failed]);

  return (
    <section aria-label="Câmera" className="space-y-3">
      <div className="relative aspect-video overflow-hidden rounded-lg bg-brand-deep">
        {failed ? (
          <div className="grid h-full place-items-center p-6 text-center text-white/75">
            <div className="space-y-2">
              <CameraOff className="mx-auto size-10" aria-hidden />
              <p className="font-medium">Câmera sem imagem</p>
              <p className="text-sm">Confira o cabo da câmera. A tela tenta de novo sozinha.</p>
            </div>
          </div>
        ) : (
          <img
            key={attempt}
            src={`/api/camera/stream?n=${attempt}`}
            alt="Imagem ao vivo da câmera da bancada"
            className="h-full w-full object-contain"
            onError={() => setFailed(true)}
          />
        )}
        {!failed && (
          <span className="absolute top-3 left-3 flex items-center gap-1.5 rounded-md bg-black/55 px-2 py-1 text-xs font-medium text-white">
            <span className="size-2 animate-pulse rounded-full bg-[#ff6b6b]" aria-hidden />
            Ao vivo
          </span>
        )}
      </div>
      {lastCapture && (
        <div className="flex items-center gap-3 rounded-lg border bg-card p-2">
          <img src={lastCapture.image_url} alt="" className="size-16 rounded-md object-cover" />
          <div className="min-w-0 text-sm">
            <p className="font-medium">
              Última foto: peça {lastCapture.physical_sample_id}
              {lastCapture.label ? `, classe ${lastCapture.label}` : ", sem rótulo"}
            </p>
            <p className="text-muted-foreground">às {formatTime(lastCapture.created_at)}</p>
          </div>
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- capture panel

function CapturePanel({
  setup,
  onSetup,
  canCapture,
  blockedReason,
  onCaptured,
}: {
  setup: Setup;
  onSetup: (next: Setup) => void;
  canCapture: boolean;
  blockedReason: ReactNode;
  onCaptured: (sample: DatasetSampleOut) => void;
}) {
  const products = useProducts();
  const [busy, setBusy] = useState(false);
  const validTags = TAG.test(setup.session) && TAG.test(setup.piece);

  const capture = useCallback(
    async (label: Grade | null) => {
      if (busy || !canCapture || !validTags) return;
      setBusy(true);
      try {
        const sample = await controlPost<DatasetSampleOut>("/dataset/capture", {
          product_id: setup.productId,
          physical_sample_id: setup.piece,
          collection_session: setup.session,
          label,
        });
        onCaptured(sample);
      } catch (error) {
        notifyError(error);
      } finally {
        setBusy(false);
      }
    },
    [busy, canCapture, validTags, setup, onCaptured],
  );

  // Keyboard: 1/2/3 (or A/B/C) photograph with the class, 0 photographs to label later,
  // N moves to the next piece. Ignored while typing in a field.
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      const target = event.target as HTMLElement | null;
      if (event.ctrlKey || event.metaKey || event.altKey) return;
      if (target?.closest("input, textarea, select, [role=combobox], [role=dialog]")) return;
      const key = event.key.toLowerCase();
      const grade = ({ "1": "A", a: "A", "2": "B", b: "B", "3": "C", c: "C" } as Record<string, Grade>)[key];
      if (grade) {
        event.preventDefault();
        void capture(grade);
      } else if (key === "0") {
        event.preventDefault();
        void capture(null);
      } else if (key === "n") {
        event.preventDefault();
        onSetup({ ...setup, piece: nextPiece(setup.piece) });
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [capture, onSetup, setup]);

  return (
    <section aria-labelledby="capture-title" className="space-y-5 rounded-lg border bg-card p-4 sm:p-5">
      <h2 id="capture-title" className="font-wide text-lg font-semibold">
        Fotografar peça
      </h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="space-y-1.5">
          <Label htmlFor="product">Produto</Label>
          <Select value={setup.productId} onValueChange={(productId) => onSetup({ ...setup, productId })}>
            <SelectTrigger id="product" className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {(products.data ?? []).map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  {p.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5">
          <Label htmlFor="session">Sessão de coleta</Label>
          <Input
            id="session"
            value={setup.session}
            maxLength={40}
            aria-invalid={!TAG.test(setup.session)}
            onChange={(e) => onSetup({ ...setup, session: e.target.value.trim() })}
          />
        </div>
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="piece">Etiqueta da peça física</Label>
        <div className="flex gap-2">
          <Input
            id="piece"
            value={setup.piece}
            maxLength={40}
            aria-invalid={!TAG.test(setup.piece)}
            className="font-display text-lg"
            onChange={(e) => onSetup({ ...setup, piece: e.target.value.trim() })}
          />
          <Button
            type="button"
            variant="outline"
            onClick={() => onSetup({ ...setup, piece: nextPiece(setup.piece) })}
          >
            <SkipForward aria-hidden />
            Próxima peça
          </Button>
        </div>
        <p className="text-sm text-muted-foreground">
          Tire várias fotos da mesma peça girando-a; todas levam a mesma classe. Use letras, números, "-" e "_".
        </p>
      </div>

      {blockedReason && <div className="rounded-md bg-muted p-3 text-sm">{blockedReason}</div>}

      <div className="grid grid-cols-3 gap-3">
        {GRADES.map((grade, i) => (
          <button
            key={grade}
            type="button"
            disabled={!canCapture || !validTags || busy}
            onClick={() => void capture(grade)}
            aria-label={`Fotografar como ${GRADE[grade].title}`}
            className={cn(
              "flex flex-col items-center gap-1 rounded-lg px-2 py-4 text-white transition-opacity disabled:opacity-40",
              "focus-visible:ring-3 focus-visible:ring-ring focus-visible:outline-none",
              TONE[GRADE[grade].tone].solid,
            )}
          >
            <span className="font-display text-5xl leading-none">{grade}</span>
            <span className="text-sm font-medium">{GRADE[grade].meaning}</span>
            <kbd className="rounded bg-black/20 px-1.5 text-xs">{i + 1}</kbd>
          </button>
        ))}
      </div>
      <Button
        variant="outline"
        className="w-full"
        disabled={!canCapture || !validTags || busy}
        onClick={() => void capture(null)}
      >
        <Camera aria-hidden />
        Fotografar e rotular depois
        <kbd className="ml-1 rounded bg-muted px-1.5 text-xs">0</kbd>
      </Button>
      <p className="text-center text-sm text-muted-foreground" aria-live="polite">
        {busy ? "Fotografando…" : "Atalhos: 1, 2, 3 ou 0 fotografam; N passa para a próxima peça."}
      </p>
    </section>
  );
}

// ---------------------------------------------------------------- progress and export

function Progress({ summary, onExport, canExport }: { summary: DatasetSummary | undefined; onExport: () => void; canExport: boolean }) {
  if (!summary) return null;
  const target = summary.target_photos_per_class;
  return (
    <section aria-labelledby="progress-title" className="space-y-4 rounded-lg border bg-card p-4 sm:p-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="progress-title" className="font-wide text-lg font-semibold">
          Progresso da coleta
        </h2>
        <p className="text-sm text-muted-foreground">Meta: {target} fotos rotuladas por classe</p>
      </div>
      <ul className="space-y-3">
        {summary.classes.map((c) => {
          const share = Math.min(1, c.photos / target);
          return (
            <li key={c.label} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="font-medium">{GRADE[c.label].title}</span>
                <span className="text-muted-foreground">
                  {c.photos} {c.photos === 1 ? "foto" : "fotos"} de {c.pieces} {c.pieces === 1 ? "peça" : "peças"}
                </span>
              </div>
              <div
                className="h-2.5 overflow-hidden rounded-full bg-muted"
                role="progressbar"
                aria-label={`${GRADE[c.label].title}: ${c.photos} de ${target} fotos`}
                aria-valuemin={0}
                aria-valuemax={target}
                aria-valuenow={Math.min(c.photos, target)}
              >
                <div className={cn("h-full rounded-full", TONE[GRADE[c.label].tone].solid)} style={{ width: `${share * 100}%` }} />
              </div>
            </li>
          );
        })}
      </ul>
      <p className="text-sm text-muted-foreground">
        {summary.pending} sem rótulo, {summary.ambiguous} ambíguas, {summary.unusable} inutilizáveis. Só as
        rotuladas entram no treinamento.
      </p>
      {canExport && (
        <Button variant="outline" onClick={onExport} disabled={summary.classes.every((c) => c.photos === 0)}>
          <FileDown aria-hidden />
          Exportar para treinamento
        </Button>
      )}
    </section>
  );
}

function ExportDialog({ result, onClose }: { result: DatasetExportOut | null; onClose: () => void }) {
  async function copy() {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result.command);
      toast.success("Comando copiado.");
    } catch {
      toast.error("Não foi possível copiar. Selecione o texto e copie à mão.");
    }
  }
  return (
    <Dialog open={result !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>Manifesto exportado</DialogTitle>
          <DialogDescription>
            {result?.photos} fotos de {result?.pieces} peças físicas. A divisão em treino, validação e teste é feita
            por peça no treinamento.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-3 text-sm">
          <p className="break-all">
            <span className="text-muted-foreground">Arquivo: </span>
            {result?.manifest_path}
          </p>
          <p className="text-muted-foreground">Para treinar, rode na pasta api:</p>
          <pre className="overflow-x-auto rounded-md bg-muted p-3 text-xs whitespace-pre-wrap break-all">
            {result?.command}
          </pre>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => void copy()}>
            <Copy aria-hidden />
            Copiar comando
          </Button>
          <Button onClick={onClose}>Fechar</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

// ---------------------------------------------------------------- review grid

const FILTERS: { value: Filter; label: string }[] = [
  { value: "pending", label: "Sem rótulo" },
  { value: "labeled", label: "Rotuladas" },
  { value: "ambiguous", label: "Ambíguas" },
  { value: "unusable", label: "Inutilizáveis" },
  { value: "all", label: "Todas" },
];

function SampleCard({
  sample,
  controller,
  onChange,
}: {
  sample: DatasetSampleOut;
  controller: boolean;
  onChange: (status: SampleStatus, label?: Grade) => void;
}) {
  const tone = sample.label ? TONE[GRADE[sample.label].tone] : TONE.neutral;
  return (
    <li className="overflow-hidden rounded-lg border bg-card">
      <div className="relative">
        <img src={sample.image_url} alt={`Peça ${sample.physical_sample_id}`} loading="lazy" className="aspect-square w-full object-cover" />
        <span
          className={cn(
            "font-display absolute top-2 right-2 grid size-9 place-items-center rounded-md text-xl text-white",
            sample.status === "labeled" ? tone.solid : "bg-black/55",
          )}
        >
          {sample.status === "labeled" ? sample.label : "?"}
        </span>
      </div>
      <div className="space-y-2 p-2.5">
        <div className="text-sm">
          <p className="font-medium">{sample.physical_sample_id}</p>
          <p className="text-muted-foreground">
            {STATUS_LABEL[sample.status]}
            {sample.status === "labeled" && sample.label_author ? ` por ${sample.label_author}` : ""}
          </p>
        </div>
        {controller && (
          <div className="flex flex-wrap gap-1">
            {GRADES.map((grade) => (
              <Button
                key={grade}
                size="sm"
                variant={sample.status === "labeled" && sample.label === grade ? "default" : "outline"}
                className="w-9 px-0"
                aria-label={`Rotular como ${GRADE[grade].title}`}
                onClick={() => onChange("labeled", grade)}
              >
                {grade}
              </Button>
            ))}
            <Button size="sm" variant="ghost" onClick={() => onChange("ambiguous")} disabled={sample.status === "ambiguous"}>
              Ambígua
            </Button>
            <Button size="sm" variant="ghost" onClick={() => onChange("unusable")} disabled={sample.status === "unusable"}>
              Inutilizável
            </Button>
          </div>
        )}
      </div>
    </li>
  );
}

function ReviewGrid({ productId, controller }: { productId: string; controller: boolean }) {
  const queryClient = useQueryClient();
  const [filter, setFilter] = useState<Filter>("pending");
  const [page, setPage] = useState(0);
  const samples = useSamples(productId, filter, page);
  const total = samples.data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  useEffect(() => setPage(0), [productId, filter]);

  async function change(sample: DatasetSampleOut, status: SampleStatus, label?: Grade) {
    try {
      await controlPatch<DatasetSampleOut>(`/dataset/samples/${sample.id}`, { status, label: label ?? null });
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["dataset-samples"] }),
        queryClient.invalidateQueries({ queryKey: ["dataset-summary"] }),
      ]);
    } catch (error) {
      notifyError(error);
    }
  }

  return (
    <section aria-labelledby="review-title" className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="review-title" className="font-wide text-xl font-semibold">
          Revisão das fotos
        </h2>
        <div role="tablist" aria-label="Filtrar fotos" className="flex flex-wrap gap-1 rounded-lg bg-muted p-1">
          {FILTERS.map((f) => (
            <button
              key={f.value}
              type="button"
              role="tab"
              aria-selected={filter === f.value}
              onClick={() => setFilter(f.value)}
              className={cn(
                "rounded-md px-3 py-1 text-sm font-medium",
                filter === f.value ? "bg-background shadow-sm" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>
      {samples.isPending ? (
        <p className="text-muted-foreground">Carregando fotos…</p>
      ) : total === 0 ? (
        <p className="rounded-lg border border-dashed p-6 text-center text-muted-foreground">Nenhuma foto neste filtro.</p>
      ) : (
        <>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
            {samples.data?.items.map((sample) => (
              <SampleCard
                key={sample.id}
                sample={sample}
                controller={controller}
                onChange={(status, label) => void change(sample, status, label)}
              />
            ))}
          </ul>
          {pages > 1 && (
            <div className="flex items-center justify-center gap-3">
              <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage((p) => p - 1)}>
                <ChevronLeft aria-hidden />
                Anterior
              </Button>
              <span className="text-sm text-muted-foreground">
                Página {page + 1} de {pages}
              </span>
              <Button variant="outline" size="sm" disabled={page + 1 >= pages} onClick={() => setPage((p) => p + 1)}>
                Próxima
                <ChevronRight aria-hidden />
              </Button>
            </div>
          )}
        </>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- page

export function ColetaPage() {
  const queryClient = useQueryClient();
  const status = useLive((s) => s.status);
  const controller = useIsController(status);
  const [controlOpen, setControlOpen] = useState(false);
  const [setup, setSetupState] = useState<Setup>(loadSetup);
  const [lastCapture, setLastCapture] = useState<DatasetSampleOut | null>(null);
  const [exported, setExported] = useState<DatasetExportOut | null>(null);
  const summary = useSummary(setup.productId);
  const exporting = useRef(false);

  const setSetup = useCallback((next: Setup) => {
    setSetupState(next);
    saveSetup(next);
  }, []);

  const onCaptured = useCallback(
    (sample: DatasetSampleOut) => {
      setLastCapture(sample);
      void queryClient.invalidateQueries({ queryKey: ["dataset-summary"] });
      void queryClient.invalidateQueries({ queryKey: ["dataset-samples"] });
    },
    [queryClient],
  );

  async function exportManifest() {
    if (exporting.current) return;
    exporting.current = true;
    try {
      setExported(await controlPost<DatasetExportOut>("/dataset/export", { product_id: setup.productId }));
    } catch (error) {
      notifyError(error);
    } finally {
      exporting.current = false;
    }
  }

  const machineBusy = Boolean(status?.machine.running || status?.current_cycle);
  const blockedReason: ReactNode = !controller ? (
    <>
      Para fotografar, esta tela precisa ter o controle da estação.{" "}
      <button type="button" className="font-medium text-primary underline" onClick={() => setControlOpen(true)}>
        {status?.control_holder ? "Assumir o controle" : "Operar a estação"}
      </button>
    </>
  ) : machineBusy ? (
    "A esteira está em operação. Pare a máquina na tela de Operação para coletar fotos."
  ) : null;

  return (
    <div className="flex min-h-dvh flex-col">
      <ConnectionBanner />
      <StationHeader status={status} />
      <main className="mx-auto w-full max-w-[100rem] flex-1 space-y-8 px-4 py-6 sm:px-6">
        <div className="space-y-2">
          <h1 className="font-wide text-3xl font-semibold tracking-tight">Coleta de fotos</h1>
          <p className="max-w-3xl text-muted-foreground">
            Coloque a peça parada sob a câmera, com a mesma luz da operação, e fotografe já com a classe definida
            pela equipe. Siga o manual de rotulagem: na dúvida, fotografe sem rótulo e decida depois em grupo.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
          <LiveView lastCapture={lastCapture} />
          <div className="space-y-6">
            <CapturePanel
              setup={setup}
              onSetup={setSetup}
              canCapture={controller && !machineBusy}
              blockedReason={blockedReason}
              onCaptured={onCaptured}
            />
            <Progress summary={summary.data} canExport={controller} onExport={() => void exportManifest()} />
          </div>
        </div>
        <ReviewGrid productId={setup.productId} controller={controller} />
      </main>
      <ExportDialog result={exported} onClose={() => setExported(null)} />
      <ControlDialog open={controlOpen} onOpenChange={setControlOpen} holder={status?.control_holder ?? null} />
    </div>
  );
}
