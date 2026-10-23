import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CircleCheck, CircleX, FileText } from "lucide-react";
import { type FormEvent, useState } from "react";
import { toast } from "sonner";
import { useIsController } from "@/components/station/action-bar";
import { ConnectionBanner } from "@/components/station/alerts";
import { ControlDialog } from "@/components/station/control-dialog";
import { StationHeader } from "@/components/station/header";
import { useProducts } from "@/components/station/lot-setup";
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
import { apiGet } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";
import type { ProductOut } from "@/lib/api/types";
import { controlPost, useControl } from "@/lib/control";
import { formatDateTime, formatPercent } from "@/lib/format";
import { notifyError } from "@/lib/notify";
import { useLive } from "@/lib/realtime/store";
import { cn } from "@/lib/utils";

type ModelOut = components["schemas"]["ModelOut"];

const STATUS: Record<ModelOut["validation_status"], { label: string; tone: string }> = {
  pending: { label: "Aguardando validação", tone: "bg-grade-b-soft text-grade-b" },
  validated: { label: "Validado pela equipe", tone: "bg-grade-a-soft text-grade-a" },
  rejected: { label: "Reprovado", tone: "bg-grade-c-soft text-grade-c" },
};

/** Trained on good pieces only (`anomalia` command): A = within standard, C = out of standard. */
function isAnomalyModel(model: ModelOut): boolean {
  return model.architecture.startsWith("anomalia");
}

/** What each kind of model can honestly show from its test set. */
function summaryMetrics(model: ModelOut): { label: string; key: string }[] {
  return isAnomalyModel(model)
    ? [
        { label: "Boas rejeitadas por engano", key: "test_good_rejected_rate" },
        { label: "Outros objetos rejeitados", key: "test_known_anomalies_rejected_rate" },
        { label: "Vão para revisão", key: "test_review_rate" },
      ]
    : [
        { label: "B/C aprovadas por engano", key: "test_defective_false_approval_rate" },
        { label: "B/C rejeitadas sozinhas", key: "test_defective_rejected_rate" },
        { label: "Vão para revisão", key: "test_review_rate" },
      ];
}

function metric(model: ModelOut, key: string): number | null {
  const value = model.metrics?.[key];
  return typeof value === "number" ? value : null;
}

function useModels() {
  return useQuery({
    queryKey: ["models"],
    queryFn: ({ signal }) => apiGet<ModelOut[]>("/models", { signal }),
  });
}

function ReportDialog({ model, onClose }: { model: ModelOut | null; onClose: () => void }) {
  const report = useQuery({
    queryKey: ["model-report", model?.id],
    enabled: model !== null,
    queryFn: async () => {
      const response = await fetch(`/api/models/${model?.id}/report`);
      if (!response.ok) throw new Error("Relatório não encontrado");
      return response.text();
    },
  });
  return (
    <Dialog open={model !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-h-[85dvh] overflow-y-auto sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle>Relatório do modelo</DialogTitle>
          <DialogDescription>{model?.id}</DialogDescription>
        </DialogHeader>
        <pre className="text-sm leading-relaxed whitespace-pre-wrap">
          {report.isPending ? "Carregando…" : report.isError ? "Relatório indisponível." : report.data}
        </pre>
      </DialogContent>
    </Dialog>
  );
}

function ModelRow({
  model,
  controller,
  lotOpenForProduct,
  onReport,
  onValidate,
}: {
  model: ModelOut;
  controller: boolean;
  lotOpenForProduct: boolean;
  onReport: () => void;
  onValidate: (status: "validated" | "rejected") => void;
}) {
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState(false);
  const verdict = model.metrics?.ready_for_bench;
  const ready = verdict === true;

  async function activate() {
    setBusy(true);
    try {
      await controlPost<ModelOut>(`/models/${model.id}/activate`);
      toast.success("Modelo ativado. O próximo lote deste produto já usa este modelo.");
      await queryClient.invalidateQueries();
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <li className={cn("rounded-lg border bg-card p-4", model.active && "border-primary ring-1 ring-primary")}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="font-wide font-semibold break-all">{model.id}</p>
          <p className="text-sm text-muted-foreground">
            Treinado em {formatDateTime(model.created_at)} com {model.dataset_version}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {model.active && (
            <span className="rounded-md bg-primary px-2 py-1 text-sm font-medium text-primary-foreground">
              Ativo
            </span>
          )}
          <span className={cn("rounded-md px-2 py-1 text-sm font-medium", STATUS[model.validation_status].tone)}>
            {STATUS[model.validation_status].label}
            {model.validated_by ? ` (${model.validated_by})` : ""}
          </span>
        </div>
      </div>

      {isAnomalyModel(model) ? (
        <p className="mt-3 flex items-start gap-2 text-sm font-medium text-grade-b">
          <CircleX className="mt-0.5 size-4 shrink-0" aria-hidden />
          Detecção de anomalia: aprendeu só com peças boas. Refaça com fotos da bancada e confira com
          peças ruins antes de deixar decidir sozinho.
        </p>
      ) : typeof verdict === "boolean" ? (
        <p className={cn("mt-3 flex items-center gap-2 text-sm font-medium", ready ? "text-grade-a" : "text-grade-b")}>
          {ready ? <CircleCheck className="size-4" aria-hidden /> : <CircleX className="size-4" aria-hidden />}
          {ready ? "Atingiu as metas do plano no teste" : "Não atingiu as metas do plano no teste"}
        </p>
      ) : (
        <p className="mt-3 text-sm text-muted-foreground">Pacote sem parecer: confira o relatório.</p>
      )}

      <dl className="mt-3 grid grid-cols-2 gap-x-6 gap-y-2 text-sm sm:grid-cols-5">
        {summaryMetrics(model).map((item) => (
          <div key={item.key}>
            <dt className="text-muted-foreground">{item.label}</dt>
            <dd className="font-semibold">{formatPercent(metric(model, item.key), true)}</dd>
          </div>
        ))}
        <div>
          <dt className="text-muted-foreground">Limiar calibrado</dt>
          <dd className="font-semibold">
            {model.recommended_threshold !== null
              ? model.recommended_threshold.toLocaleString("pt-BR", { minimumFractionDigits: 2 })
              : "—"}
          </dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Tempo por peça (p95)</dt>
          <dd className="font-semibold">
            {metric(model, "latency_p95_ms") !== null
              ? `${(metric(model, "latency_p95_ms") ?? 0).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} ms`
              : "—"}
          </dd>
        </div>
      </dl>

      <div className="mt-4 flex flex-wrap gap-2">
        <Button variant="outline" size="sm" onClick={onReport}>
          <FileText aria-hidden />
          Ver relatório
        </Button>
        {controller && model.validation_status === "pending" && (
          <>
            <Button variant="outline" size="sm" onClick={() => onValidate("validated")}>
              Validar
            </Button>
            <Button variant="outline" size="sm" onClick={() => onValidate("rejected")}>
              Reprovar
            </Button>
          </>
        )}
        {controller && !model.active && model.validation_status !== "rejected" && (
          <Button
            size="sm"
            onClick={() => void activate()}
            disabled={busy || lotOpenForProduct}
            title={lotOpenForProduct ? "Encerre o lote deste produto antes de trocar o modelo" : undefined}
          >
            Ativar para este produto
          </Button>
        )}
      </div>
    </li>
  );
}

function ValidationDialog({
  target,
  onClose,
}: {
  target: { model: ModelOut; status: "validated" | "rejected" } | null;
  onClose: () => void;
}) {
  const queryClient = useQueryClient();
  const { operator } = useControl();
  const [typed, setTyped] = useState<string | null>(null);
  const reviewer = typed ?? operator ?? "";
  const approving = target?.status === "validated";

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!target || !reviewer.trim()) return;
    try {
      await controlPost<ModelOut>(`/models/${target.model.id}/validation`, {
        status: target.status,
        reviewer: reviewer.trim(),
      });
      await queryClient.invalidateQueries({ queryKey: ["models"] });
      onClose();
    } catch (error) {
      notifyError(error);
    }
  }

  return (
    <Dialog open={target !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <form onSubmit={submit} className="space-y-5">
          <DialogHeader>
            <DialogTitle>{approving ? "Validar o modelo" : "Reprovar o modelo"}</DialogTitle>
            <DialogDescription>
              {approving
                ? "Confirme só depois de ler o relatório e conferir as métricas com peças reais."
                : "Um modelo reprovado não pode ser ativado."}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-1.5">
            <Label htmlFor="reviewer">Responsável pela decisão</Label>
            <Input id="reviewer" value={reviewer} onChange={(e) => setTyped(e.target.value)} maxLength={60} />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={!reviewer.trim()}>
              {approving ? "Validar" : "Reprovar"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

function InstallForm() {
  const queryClient = useQueryClient();
  const [path, setPath] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!path.trim()) return;
    setBusy(true);
    try {
      const model = await controlPost<ModelOut>("/models/install", { path: path.trim() });
      toast.success(`Modelo ${model.id} instalado.`);
      setPath("");
      await queryClient.invalidateQueries({ queryKey: ["models"] });
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-2 sm:flex-row sm:items-end">
      <div className="flex-1 space-y-1.5">
        <Label htmlFor="model-path">Pasta do pacote gerado pelo treinamento</Label>
        <Input
          id="model-path"
          value={path}
          onChange={(e) => setPath(e.target.value)}
          placeholder="C:\…\modelos-treinados\tucuma-20261019-125107"
        />
      </div>
      <Button type="submit" disabled={!path.trim() || busy}>
        {busy ? "Instalando…" : "Instalar modelo"}
      </Button>
    </form>
  );
}

function ProductSection({
  product,
  models,
  controller,
  lotOpenForProduct,
  onReport,
  onValidate,
}: {
  product: ProductOut;
  models: ModelOut[];
  controller: boolean;
  lotOpenForProduct: boolean;
  onReport: (m: ModelOut) => void;
  onValidate: (m: ModelOut, status: "validated" | "rejected") => void;
}) {
  return (
    <section aria-labelledby={`product-${product.id}`} className="space-y-3">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id={`product-${product.id}`} className="font-wide text-xl font-semibold">
          {product.name}
        </h2>
        <p className="text-sm text-muted-foreground">
          Limiar de decisão em uso:{" "}
          {product.decision_threshold.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
          {product.active_model_id ? "" : ". Sem modelo ativo: a bancada simulada usa o classificador simulado."}
        </p>
      </div>
      {models.length === 0 ? (
        <p className="rounded-lg border border-dashed p-4 text-muted-foreground">
          Nenhum modelo instalado para este produto.
        </p>
      ) : (
        <ul className="space-y-3">
          {models.map((model) => (
            <ModelRow
              key={model.id}
              model={model}
              controller={controller}
              lotOpenForProduct={lotOpenForProduct}
              onReport={() => onReport(model)}
              onValidate={(status) => onValidate(model, status)}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

export function ModelosPage() {
  const status = useLive((s) => s.status);
  const products = useProducts();
  const models = useModels();
  const controller = useIsController(status);
  const [controlOpen, setControlOpen] = useState(false);
  const [report, setReport] = useState<ModelOut | null>(null);
  const [validation, setValidation] = useState<{ model: ModelOut; status: "validated" | "rejected" } | null>(
    null,
  );

  return (
    <div className="flex min-h-dvh flex-col">
      <ConnectionBanner />
      <StationHeader status={status} />
      <main className="mx-auto w-full max-w-6xl flex-1 space-y-8 px-4 py-6 sm:px-6">
        <div className="space-y-2">
          <h1 className="font-wide text-3xl font-semibold tracking-tight">Modelos de inspeção</h1>
          <p className="max-w-3xl text-muted-foreground">
            Cada produto usa o modelo ativo dele. Ao ativar um modelo, o limiar calibrado no treinamento passa a
            valer para os próximos lotes. Valide um modelo só depois de conferir o relatório com peças reais.
          </p>
        </div>

        {controller ? (
          <InstallForm />
        ) : (
          <p className="text-sm">
            Para instalar, validar ou ativar modelos, esta tela precisa ter o controle da estação.{" "}
            <button type="button" className="font-medium text-primary underline" onClick={() => setControlOpen(true)}>
              {status?.control_holder ? "Assumir o controle" : "Operar a estação"}
            </button>
          </p>
        )}

        {products.data?.map((product) => (
          <ProductSection
            key={product.id}
            product={product}
            models={(models.data ?? []).filter((m) => m.product_id === product.id)}
            controller={controller}
            lotOpenForProduct={status?.active_lot?.product_id === product.id}
            onReport={setReport}
            onValidate={(model, s) => setValidation({ model, status: s })}
          />
        ))}
        {(products.isPending || models.isPending) && <p className="text-muted-foreground">Carregando modelos…</p>}
      </main>
      <ReportDialog model={report} onClose={() => setReport(null)} />
      <ValidationDialog target={validation} onClose={() => setValidation(null)} />
      <ControlDialog open={controlOpen} onOpenChange={setControlOpen} holder={status?.control_holder ?? null} />
    </div>
  );
}
