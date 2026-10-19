import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Info, Lock } from "lucide-react";
import { type FormEvent, useEffect, useState } from "react";
import { toast } from "sonner";
import { useProducts } from "@/components/station/lot-setup";
import { NeedControl, PageShell, useStation } from "@/components/station/page-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ApiError, apiGet } from "@/lib/api/client";
import type { ConfigurePayload, ProductConfigOut } from "@/lib/api/types";
import { BENCH_GROUPS, type BenchKey, type Draft, FIELDS, toDraft, validate } from "@/lib/bench-fields";
import { controlPut, useControl } from "@/lib/control";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";

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

  const input = (key: BenchKey | "threshold" | "presentation", id: string, extra?: { invalid?: boolean; numeric?: boolean }) => (
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
    </PageShell>
  );
}
