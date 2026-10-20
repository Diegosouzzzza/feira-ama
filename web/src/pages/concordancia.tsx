import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, Users, XCircle } from "lucide-react";
import { useState } from "react";
import { useProducts } from "@/components/station/lot-setup";
import { PageShell } from "@/components/station/page-shell";
import { TONE } from "@/components/station/tone";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ApiError, apiGet, apiPost } from "@/lib/api/client";
import type { AgreementLabelOut, AgreementQueueItem, AgreementSummary, Grade } from "@/lib/api/types";
import { formatPercent } from "@/lib/format";
import { GRADE } from "@/lib/labels";
import { notifyError } from "@/lib/notify";
import { cn } from "@/lib/utils";

const GRADES: Grade[] = ["A", "B", "C"];
const SETUP_KEY = "av-concordancia";
const TAG = /^[A-Za-z0-9][A-Za-z0-9_-]{0,39}$/;
const NAME = /^.{1,60}$/;

interface Setup {
  productId: string;
  session: string;
  reviewer: string;
}

function today(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

function loadSetup(): Setup {
  const fallback = { productId: "tucuma", session: `${today()}-criterios`, reviewer: "" };
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
    // Blocked storage: the form starts from defaults again next time.
  }
}

// ---------------------------------------------------------------- setup

function SetupForm({ setup, onChange }: { setup: Setup; onChange: (next: Setup) => void }) {
  const products = useProducts();
  return (
    <section aria-label="Quem está rotulando" className="grid grid-cols-1 gap-3 rounded-lg border bg-card p-4 sm:grid-cols-3">
      <div className="space-y-1.5">
        <Label htmlFor="reviewer">Seu nome</Label>
        <Input
          id="reviewer"
          value={setup.reviewer}
          maxLength={60}
          onChange={(e) => onChange({ ...setup, reviewer: e.target.value })}
        />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="product">Produto</Label>
        <Select value={setup.productId} onValueChange={(productId) => onChange({ ...setup, productId })}>
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
        <Label htmlFor="session">Rodada</Label>
        <Input
          id="session"
          value={setup.session}
          maxLength={40}
          aria-invalid={!TAG.test(setup.session)}
          onChange={(e) => onChange({ ...setup, session: e.target.value.trim() })}
        />
        <p className="text-sm text-muted-foreground">
          Combine o mesmo nome de rodada com quem vai rotular junto com você.
        </p>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------- blind labeling

function Labeling({ setup }: { setup: Setup }) {
  const queryClient = useQueryClient();
  const [busy, setBusy] = useState(false);
  const queue = useQuery({
    queryKey: ["agreement-next", setup.productId, setup.session, setup.reviewer],
    queryFn: ({ signal }) =>
      apiGet<AgreementQueueItem | null>(
        `/dataset/agreement/next?product_id=${encodeURIComponent(setup.productId)}&session=${encodeURIComponent(setup.session)}&reviewer=${encodeURIComponent(setup.reviewer)}`,
        { signal },
      ),
  });

  async function choose(label: Grade) {
    if (!queue.data || busy) return;
    setBusy(true);
    try {
      await apiPost<AgreementLabelOut>(`/dataset/agreement/labels`, {
        product_id: setup.productId,
        session: setup.session,
        sample_id: queue.data.sample.id,
        reviewer: setup.reviewer,
        label,
      });
      await queryClient.invalidateQueries({ queryKey: ["agreement-next"] });
      await queryClient.invalidateQueries({ queryKey: ["agreement-summary"] });
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  if (queue.isPending) return <p className="text-muted-foreground">Carregando…</p>;

  if (!queue.data) {
    return (
      <section className="space-y-3 rounded-lg border bg-card p-6 text-center">
        <CheckCircle2 className="mx-auto size-10 text-grade-a" aria-hidden />
        <p className="font-wide text-lg font-semibold">Você rotulou todas as fotos desta rodada.</p>
        <p className="text-muted-foreground">
          Quando a segunda pessoa também terminar, o resumo mais abaixo mostra onde vocês concordaram ou não.
        </p>
      </section>
    );
  }

  const { sample, remaining } = queue.data;
  return (
    <section aria-label="Rotular às cegas" className="space-y-4 rounded-lg border bg-card p-4 sm:p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Peça {sample.physical_sample_id} · {remaining} {remaining === 1 ? "foto restante" : "fotos restantes"}
        </p>
      </div>
      <img
        src={sample.image_url}
        alt={`Peça ${sample.physical_sample_id}, para rotular`}
        className="mx-auto aspect-square w-full max-w-sm rounded-md bg-muted object-cover"
      />
      <p className="text-center text-sm text-muted-foreground">
        Rotule pelo que você vê, sem olhar o rótulo da coleta. Ninguém vê sua resposta até o resumo.
      </p>
      <div className="grid grid-cols-3 gap-3">
        {GRADES.map((grade) => (
          <button
            key={grade}
            type="button"
            disabled={busy}
            aria-label={`Rotular como Classe ${grade}`}
            onClick={() => void choose(grade)}
            className={cn(
              "flex flex-col items-center gap-1 rounded-lg px-2 py-4 text-white transition-opacity disabled:opacity-40",
              "focus-visible:ring-3 focus-visible:ring-ring focus-visible:outline-none",
              TONE[GRADE[grade].tone].solid,
            )}
          >
            <span className="font-display text-5xl leading-none">{grade}</span>
            <span className="text-sm font-medium">{GRADE[grade].meaning}</span>
          </button>
        ))}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------- summary

function Summary({ setup }: { setup: Setup }) {
  const summary = useQuery({
    queryKey: ["agreement-summary", setup.productId, setup.session],
    queryFn: async ({ signal }) => {
      try {
        return await apiGet<AgreementSummary>(
          `/dataset/agreement/summary?product_id=${encodeURIComponent(setup.productId)}&session=${encodeURIComponent(setup.session)}`,
          { signal },
        );
      } catch (error) {
        if (error instanceof ApiError && error.code === "INVALID_STATE") return null;
        throw error;
      }
    },
  });

  if (summary.isPending) return null;
  if (!summary.data) {
    return (
      <section className="rounded-lg border border-dashed p-6 text-center text-muted-foreground">
        <Users className="mx-auto mb-2 size-8" aria-hidden />
        Ainda não há duas pessoas rotulando nesta rodada. Peça para mais alguém entrar com o mesmo nome de rodada.
      </section>
    );
  }
  const data = summary.data;
  return (
    <section aria-labelledby="summary-title" className="space-y-4 rounded-lg border bg-card p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="summary-title" className="font-wide text-xl font-semibold">
          Resumo da rodada
        </h2>
        <p className="text-sm text-muted-foreground">{data.reviewers.join(", ")}</p>
      </div>
      <dl className="grid grid-cols-3 gap-4 text-center">
        <div className="rounded-md bg-muted p-3">
          <dt className="text-sm text-muted-foreground">Comparadas</dt>
          <dd className="font-wide text-2xl font-semibold">{data.compared}</dd>
        </div>
        <div className="rounded-md bg-muted p-3">
          <dt className="text-sm text-muted-foreground">Concordaram</dt>
          <dd className="font-wide text-2xl font-semibold text-grade-a">{data.agreed}</dd>
        </div>
        <div className="rounded-md bg-muted p-3">
          <dt className="text-sm text-muted-foreground">Concordância</dt>
          <dd className="font-wide text-2xl font-semibold">{formatPercent(data.agreement_rate)}</dd>
        </div>
      </dl>
      {data.compared === 0 ? (
        <p className="text-muted-foreground">Nenhuma foto em comum rotulada pelos dois ainda.</p>
      ) : data.disagreements.length === 0 ? (
        <p className="flex items-center gap-2 text-grade-a">
          <CheckCircle2 className="size-5" aria-hidden />
          Concordância total nas fotos comparadas até agora.
        </p>
      ) : (
        <>
          <p className="flex items-center gap-2 font-medium text-grade-c">
            <XCircle className="size-5" aria-hidden />
            Fotos onde vocês discordaram — vale discutir juntos o critério:
          </p>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            {data.disagreements.map((item) => (
              <li key={item.sample.id} className="overflow-hidden rounded-lg border">
                <img
                  src={item.sample.image_url}
                  alt={`Peça ${item.sample.physical_sample_id}`}
                  className="aspect-square w-full object-cover"
                />
                <div className="space-y-1 p-2 text-sm">
                  <p className="font-medium">{item.sample.physical_sample_id}</p>
                  {Object.entries(item.labels).map(([reviewer, label]) => (
                    <p key={reviewer} className="flex items-center justify-between">
                      <span className="text-muted-foreground">{reviewer}</span>
                      <span className={cn("font-display text-lg font-semibold", TONE[GRADE[label].tone].text)}>
                        {label}
                      </span>
                    </p>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

// ---------------------------------------------------------------- page

export function ConcordanciaPage() {
  const [setup, setSetupState] = useState<Setup>(loadSetup);
  function setSetup(next: Setup) {
    setSetupState(next);
    saveSetup(next);
  }
  const ready = NAME.test(setup.reviewer.trim()) && TAG.test(setup.session);

  return (
    <PageShell
      title="Teste de concordância"
      intro="Duas pessoas rotulam as mesmas fotos da coleta sem ver a resposta uma da outra; o resumo mostra onde discordaram, para afinar o critério A/B/C antes da coleta grande."
    >
      <SetupForm setup={setup} onChange={setSetup} />
      {ready ? (
        <>
          <Labeling key={`${setup.productId}-${setup.session}-${setup.reviewer}`} setup={setup} />
          <Summary key={`summary-${setup.productId}-${setup.session}`} setup={setup} />
        </>
      ) : (
        <p className="text-sm text-muted-foreground">Digite seu nome e uma rodada válida para começar.</p>
      )}
    </PageShell>
  );
}
