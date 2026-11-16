import { type FormEvent, useState } from "react";
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
import { useControl } from "@/lib/control";
import { notifyError } from "@/lib/notify";

/** Take the station's single operator seat; taking it from someone else needs a second step. */
export function ControlDialog({
  open,
  onOpenChange,
  holder,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  holder: string | null;
}) {
  const { claim, lastOperator } = useControl();
  const [name, setName] = useState(lastOperator ?? "");
  const [busy, setBusy] = useState(false);
  const takeover = holder !== null;

  async function submit(event: FormEvent) {
    event.preventDefault();
    const operator = name.trim();
    if (!operator) return;
    setBusy(true);
    try {
      await claim(operator, takeover);
      onOpenChange(false);
    } catch (error) {
      notifyError(error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <form onSubmit={submit} className="space-y-5">
          <DialogHeader>
            <DialogTitle>{takeover ? "Assumir o controle" : "Operar a estação"}</DialogTitle>
            <DialogDescription>
              {takeover
                ? `O controle está com ${holder}. Ao assumir, a tela dessa pessoa passa a só acompanhar.`
                : "Só uma tela opera a esteira por vez. As outras acompanham sem poder comandar."}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-1.5">
            <Label htmlFor="operator-name">Seu nome</Label>
            <Input
              id="operator-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              maxLength={60}
              autoComplete="name"
              autoFocus
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
            <Button type="submit" disabled={!name.trim() || busy}>
              {takeover ? "Assumir o controle" : "Operar a estação"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
