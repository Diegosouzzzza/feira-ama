import { useQuery } from "@tanstack/react-query";
import { type FormEvent, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { apiGet } from "@/lib/api/client";
import type { LotOut, ProductOut } from "@/lib/api/types";
import { controlPost, useControl } from "@/lib/control";
import { notifyError } from "@/lib/notify";

export function useProducts() {
  return useQuery({
    queryKey: ["products"],
    queryFn: ({ signal }) => apiGet<ProductOut[]>("/products", { signal }),
    staleTime: 60_000,
  });
}

/** Shown when no lot is open: the first thing the operator has to do. */
export function LotSetup({ onNeedControl }: { onNeedControl: () => void }) {
  const products = useProducts();
  const { token, operator } = useControl();
  const [productId, setProductId] = useState<string>("");
  const [typedName, setName] = useState<string | null>(null);
  const name = typedName ?? operator ?? "";
  const [notes, setNotes] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!productId || !name.trim()) return;
    setBusy(true);
    try {
      const lot = await controlPost<LotOut>("/lots", {
        request_id: crypto.randomUUID(),
        product_id: productId,
        operator: name.trim(),
        notes: notes.trim() || null,
      });
      toast.success(`Lote ${lot.id} aberto.`);
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section aria-labelledby="lot-setup-heading" className="mx-auto max-w-xl rounded-lg border bg-card p-8">
      <h2 id="lot-setup-heading" className="font-wide text-2xl font-semibold tracking-tight">
        Abra um lote para começar
      </h2>
      <p className="mt-2 text-muted-foreground">
        Cada lote é de um só produto. O modelo de inspeção desse produto é carregado ao abrir o lote.
      </p>
      {!token ? (
        <div className="mt-6 space-y-3">
          <p>Para abrir um lote, esta tela precisa ter o controle da estação.</p>
          <Button onClick={onNeedControl}>Operar a estação</Button>
        </div>
      ) : (
        <form onSubmit={submit} className="mt-6 space-y-5">
          <div className="space-y-1.5">
            <Label htmlFor="lot-product">Produto</Label>
            <Select value={productId} onValueChange={setProductId}>
              <SelectTrigger id="lot-product" className="w-full">
                <SelectValue placeholder={products.isPending ? "Carregando produtos…" : "Escolha o produto"} />
              </SelectTrigger>
              <SelectContent>
                {products.data?.map((p) => (
                  <SelectItem key={p.id} value={p.id}>
                    {p.name}
                    {p.presentation ? ` (${p.presentation})` : ""}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="lot-operator">Operador responsável</Label>
            <Input id="lot-operator" value={name} onChange={(e) => setName(e.target.value)} maxLength={60} />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="lot-notes">Observações (opcional)</Label>
            <Textarea id="lot-notes" value={notes} onChange={(e) => setNotes(e.target.value)} maxLength={500} rows={2} />
          </div>
          <Button type="submit" size="lg" disabled={!productId || !name.trim() || busy}>
            {busy ? "Abrindo lote…" : "Abrir lote"}
          </Button>
        </form>
      )}
    </section>
  );
}
