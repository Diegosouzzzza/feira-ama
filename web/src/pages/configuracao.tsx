import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, HardDriveDownload, Info, Lock, RefreshCw, Trash2 } from "lucide-react";
import { type FormEvent, useEffect, useState } from "react";
import { toast } from "sonner";
import { useProducts } from "@/components/station/lot-setup";
import { NeedControl, PageShell, useStation } from "@/components/station/page-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ApiError, apiGet } from "@/lib/api/client";
import type { BackupOut, ConfigurePayload, ProductConfigOut, PurgeOut } from "@/lib/api/types";
import { BENCH_GROUPS, type BenchKey, type Draft, FIELDS, type RoiKey, toDraft, toRoi, validate } from "@/lib/bench-fields";
import { controlDelete, controlPost, controlPut, useControl } from "@/lib/control";
import { formatBytes, formatDateTime } from "@/lib/format";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------- backups and cleanup

function BackupsPanel({ controller }: { controller: boolean }) {
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState<"backup" | "purge" | null>(null);
  const backups = useQuery({
    queryKey: ["backups"],
    queryFn: ({ signal }) => apiGet<BackupOut[]>("/backups", { signal }),
  });

  async function createBackup() {
    setBusy("backup");
    try {
      await controlPost<BackupOut>("/backups");
      toast.success("Backup criado. Baixe e guarde numa unidade separada (pendrive).");
      await queryClient.invalidateQueries({ queryKey: ["backups"] });
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(null);
    }
  }

  async function removeBackup(name: string) {
    try {
      await controlDelete<void>(`/backups/${encodeURIComponent(name)}`);
      await queryClient.invalidateQueries({ queryKey: ["backups"] });
    } catch (error) {
      notifyError(error);
    }
  }

  async function purgeImages() {
    setBusy("purge");
    try {
      const result = await controlPost<PurgeOut>("/images/purge");
      toast.success(
        result.purged > 0
          ? `${result.purged} foto(s) de inspeções antigas apagada(s), ${formatBytes(result.freed_bytes)} liberados.`
          : "Nenhuma foto antiga para apagar.",
      );
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(null);
    }
  }

  return (
    <section aria-labelledby="backups-title" className="space-y-4 rounded-lg border bg-card p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="backups-title" className="font-wide text-lg font-semibold">
          Backups e limpeza
        </h2>
        {controller && (
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" size="sm" disabled={busy !== null} onClick={() => void purgeImages()}>
              <Trash2 aria-hidden />
              Limpar fotos antigas
            </Button>
            <Button size="sm" disabled={busy !== null} onClick={() => void createBackup()}>
              <HardDriveDownload aria-hidden />
              {busy === "backup" ? "Gerando…" : "Fazer backup agora"}
            </Button>
          </div>
        )}
      </div>
      <p className="text-sm text-muted-foreground">
        O backup inclui uma cópia consistente do banco, as fotos de inspeção, os modelos instalados e a coleta de
        treinamento. A limpeza apaga fotos de inspeções antigas de lotes já encerrados (o lote aberto nunca é
        tocado); o registro de cada peça continua no histórico e no CSV, só a foto sai.
      </p>
      {!controller && <NeedControl action="fazer backup ou limpar fotos" />}
      {backups.isPending ? (
        <p className="text-sm text-muted-foreground">Carregando…</p>
      ) : backups.data?.length === 0 ? (
        <p className="text-sm text-muted-foreground">Nenhum backup ainda.</p>
      ) : (
        <ul className="divide-y rounded-md border text-sm">
          {backups.data?.map((backup) => (
            <li key={backup.name} className="flex flex-wrap items-center gap-3 px-3 py-2">
              <div className="min-w-0 flex-1">
                <p className="font-medium">{formatDateTime(backup.created_at)}</p>
                <p className="text-muted-foreground">
                  {formatBytes(backup.size_bytes)} · {backup.inspections} inspeções · {backup.dataset_photos} fotos
                  de coleta
                </p>
              </div>
              <Button variant="outline" size="sm" asChild>
                <a href={`/api/backups/${encodeURIComponent(backup.name)}/file`} download>
                  <Download aria-hidden />
                  Baixar
                </a>
              </Button>
              {controller && (
                <Button
                  variant="ghost"
                  size="sm"
                  aria-label={`Apagar backup de ${formatDateTime(backup.created_at)}`}
                  onClick={() => void removeBackup(backup.name)}
                >
                  <Trash2 aria-hidden />
                </Button>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- ROI (inspection window)

function RoiPreview({ draft }: { draft: Draft }) {
  const [attempt, setAttempt] = useState(0);
  const [failed, setFailed] = useState(false);
  const x = Number(draft.roiX) || 0;
  const y = Number(draft.roiY) || 0;
  const width = Number(draft.roiWidth) || 0;
  const height = Number(draft.roiHeight) || 0;

  return (
    <div className="space-y-2">
      <div className="relative aspect-video overflow-hidden rounded-md bg-brand-deep">
        {failed ? (
          <p className="grid h-full place-items-center p-4 text-center text-sm text-white/75">
            Sem imagem da câmera agora.
          </p>
        ) : (
          <img
            key={attempt}
            src={`/api/camera/snapshot?n=${attempt}`}
            alt="Último quadro da câmera, para posicionar o recorte"
            className="h-full w-full object-contain"
            onError={() => setFailed(true)}
          />
        )}
        {!failed && draft.roiEnabled && (
          <div
            aria-hidden
            className="absolute border-2 border-brand-bright shadow-[0_0_0_9999px_rgba(0,0,0,0.5)]"
            style={{
              left: `${x}%`,
              top: `${y}%`,
              width: `${width}%`,
              height: `${height}%`,
            }}
          />
        )}
      </div>
      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={() => {
          setFailed(false);
          setAttempt((n) => n + 1);
        }}
      >
        <RefreshCw aria-hidden />
        Atualizar imagem
      </Button>
    </div>
  );
}

function ProductForm({ productId, controller }: { productId: string; controller: boolean }) {
  const queryClient = useQueryClient();
  const { operator } = useControl();
  const config = useQuery({
    queryKey: ["product-config", productId],
    queryFn: ({ signal }) => apiGet<ProductConfigOut>(`/products/${productId}/config`, { signal }),
  });
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (config.data) setDraft(toDraft(config.data));
  }, [config.data]);

  if (!config.data || !draft) return <p className="text-muted-foreground">Carregando…</p>;
  const current = config.data;
  const errors = validate(draft);
  const valid = Object.keys(errors).length === 0;
  const changed = JSON.stringify(draft) !== JSON.stringify(toDraft(current));
  const locked = !current.editable || !controller;

  async function save(event: FormEvent) {
    event.preventDefault();
    if (!draft || !valid || locked) return;
    setSaving(true);
    const bench = Object.fromEntries(
      FIELDS.map((f) => [f.key, draft[f.key].trim() === "" ? null : Number(draft[f.key])]),
    ) as unknown as ConfigurePayload;
    try {
      await controlPut<ProductConfigOut>(`/products/${productId}/config`, {
        expected_version: current.product.version,
        presentation: draft.presentation.trim() || null,
        decision_threshold: Number(draft.threshold.replace(",", ".")),
        bench,
        roi: toRoi(draft),
      });
      toast.success("Configuração salva. Vale a partir do próximo lote deste produto.");
      await queryClient.invalidateQueries({ queryKey: ["product-config", productId] });
      await queryClient.invalidateQueries({ queryKey: ["products"] });
    } catch (error) {
      if (error instanceof ApiError && error.code === "CONFLICT") {
        await queryClient.invalidateQueries({ queryKey: ["product-config", productId] });
      }
      notifyError(error);
    } finally {
      setSaving(false);
    }
  }

  const input = (key: BenchKey | RoiKey | "threshold" | "presentation", id: string, extra?: { invalid?: boolean; numeric?: boolean }) => (
    <Input
      id={id}
      value={draft[key]}
      disabled={locked}
      inputMode={extra?.numeric ? "numeric" : undefined}
      aria-invalid={extra?.invalid}
      onChange={(e) => setDraft({ ...draft, [key]: e.target.value })}
    />
  );

  return (
    <form onSubmit={save} className="space-y-6">
      {current.bench_is_default && (
        <p className="flex items-start gap-2 rounded-md bg-review-soft p-3 text-sm text-review">
          <Info className="mt-0.5 size-4 shrink-0" aria-hidden />
          <span>
            Bancada ainda não calibrada para este produto: os valores abaixo são o ponto de partida da bancada
            simulada. No modo real a máquina só arma depois que uma calibração for salva aqui.
          </span>
        </p>
      )}
      {current.locked_reason ? (
        <p className="flex items-start gap-2 rounded-md bg-muted p-3 text-sm">
          <Lock className="mt-0.5 size-4 shrink-0" aria-hidden />
          {current.locked_reason}
        </p>
      ) : (
        !controller && <NeedControl action="alterar a configuração" />
      )}

      <section className="grid gap-4 rounded-lg border bg-card p-4 md:grid-cols-2" aria-labelledby={`${productId}-profile`}>
        <h3 id={`${productId}-profile`} className="font-wide font-semibold md:col-span-2">
          Perfil
        </h3>
        <div className="space-y-1.5">
          <Label htmlFor={`${productId}-presentation`}>Apresentação</Label>
          {input("presentation", `${productId}-presentation`)}
          <p className="text-sm text-muted-foreground">Ex.: com casca, sem casca.</p>
        </div>
        <div className="space-y-1.5">
          <Label htmlFor={`${productId}-threshold`}>Limiar de decisão</Label>
          {input("threshold", `${productId}-threshold`, { invalid: Boolean(errors.threshold) })}
          <p className={cn("text-sm", errors.threshold ? "text-grade-c" : "text-muted-foreground")}>
            {errors.threshold ??
              "Abaixo desta confiança a peça vai para revisão. Ao ativar um modelo, o limiar calibrado substitui este."}
          </p>
        </div>
      </section>

      {BENCH_GROUPS.map((group) => (
        <section key={group.title} className="space-y-4 rounded-lg border bg-card p-4" aria-label={group.title}>
          <h3 className="font-wide font-semibold">{group.title}</h3>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {group.fields.map((f) => {
              const id = `${productId}-${f.key}`;
              const error = errors[f.key];
              return (
                <div key={f.key} className="space-y-1.5">
                  <Label htmlFor={id}>
                    {f.label} <span className="font-normal text-muted-foreground">({f.unit})</span>
                  </Label>
                  {input(f.key, id, { invalid: Boolean(error), numeric: true })}
                  <p className={cn("text-sm", error ? "text-grade-c" : "text-muted-foreground")}>{error ?? f.help}</p>
                </div>
              );
            })}
          </div>
        </section>
      ))}

      <section className="space-y-4 rounded-lg border bg-card p-4" aria-labelledby={`${productId}-roi`}>
        <h3 id={`${productId}-roi`} className="font-wide font-semibold">
          Região de inspeção (ROI)
        </h3>
        <p className="text-sm text-muted-foreground">
          Recorta o quadro da câmera antes de analisar, para o modelo ver só a área da esteira onde a peça fica,
          sem a esteira e o fundo ao redor. Vale a partir do próximo treino: use estes mesmos valores no comando de
          treinamento (a tela Coleta já inclui isso ao exportar).
        </p>
        <label className="flex items-center gap-2 text-sm font-medium">
          <input
            type="checkbox"
            className="accent-primary size-4"
            checked={draft.roiEnabled}
            disabled={locked}
            onChange={(e) => setDraft({ ...draft, roiEnabled: e.target.checked })}
          />
          Recortar a imagem (desmarcado: usa o quadro inteiro)
        </label>
        {draft.roiEnabled && (
          <div className="grid gap-4 md:grid-cols-2">
            <div className="grid grid-cols-2 gap-4">
              {(
                [
                  ["roiX", "Da esquerda"],
                  ["roiY", "Do topo"],
                  ["roiWidth", "Largura"],
                  ["roiHeight", "Altura"],
                ] as const
              ).map(([key, label]) => {
                const id = `${productId}-${key}`;
                const error = errors[key];
                return (
                  <div key={key} className="space-y-1.5">
                    <Label htmlFor={id}>
                      {label} <span className="font-normal text-muted-foreground">(%)</span>
                    </Label>
                    {input(key, id, { invalid: Boolean(error), numeric: true })}
                    {error && <p className="text-sm text-grade-c">{error}</p>}
                  </div>
                );
              })}
            </div>
            <RoiPreview draft={draft} />
          </div>
        )}
      </section>

      {!locked && (
        <div className="sticky bottom-0 flex flex-wrap items-center gap-3 border-t bg-background/95 py-3 backdrop-blur">
          <Button type="submit" disabled={!valid || !changed || saving}>
            {saving ? "Salvando…" : "Salvar configuração"}
          </Button>
          <Button type="button" variant="ghost" disabled={!changed || saving} onClick={() => setDraft(toDraft(current))}>
            Desfazer alterações
          </Button>
          <p className="text-sm text-muted-foreground">
            Versão {current.product.version}. Fica registrado como alteração de {operator}.
          </p>
        </div>
      )}
    </form>
  );
}

export function ConfiguracaoPage() {
  const { controller } = useStation();
  const products = useProducts();
  const [selected, setSelected] = useState<string | null>(null);
  const productId = selected ?? products.data?.[0]?.id ?? null;

  return (
    <PageShell
      title="Configuração"
      intro="Perfil de cada produto: apresentação, limiar de decisão e a calibração da bancada (prazos, posições do desviador e motor). As mudanças valem a partir do próximo lote e ficam no registro de eventos."
    >
      <div role="tablist" aria-label="Produto" className="flex flex-wrap gap-1 rounded-lg bg-muted p-1 sm:w-fit">
        {(products.data ?? []).map((p) => (
          <button
            key={p.id}
            type="button"
            role="tab"
            aria-selected={productId === p.id}
            onClick={() => setSelected(p.id)}
            className={cn(
              "rounded-md px-4 py-1.5 font-medium",
              productId === p.id ? "bg-background shadow-sm" : "text-muted-foreground hover:text-foreground",
            )}
          >
            {p.name}
          </button>
        ))}
      </div>
      {productId && <ProductForm key={productId} productId={productId} controller={controller} />}
      <BackupsPanel controller={controller} />
    </PageShell>
  );
}
