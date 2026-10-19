import { CircleCheck, CircleX, LoaderCircle, Server } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useHealth } from "@/lib/api/health";

function ServiceStatus() {
  const health = useHealth();

  if (health.isPending) {
    return (
      <p className="flex items-center gap-2 text-muted-foreground">
        <LoaderCircle className="size-5 animate-spin" aria-hidden />
        Verificando serviço local…
      </p>
    );
  }

  if (health.isError) {
    return (
      <div className="flex items-start gap-3 rounded-lg bg-fault-soft p-4 text-fault">
        <CircleX className="mt-0.5 size-5 shrink-0" aria-hidden />
        <div>
          <p className="font-semibold">Serviço local sem resposta</p>
          <p className="text-sm">
            Inicie a API com <code className="font-mono">scripts/dev.ps1</code> e aguarde alguns
            segundos.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <span className="flex items-center gap-2 font-semibold text-grade-a">
        <CircleCheck className="size-5" aria-hidden />
        Serviço local ativo
      </span>
      <Badge variant="secondary">versão {health.data.version}</Badge>
      <Badge variant="outline" className="capitalize">
        modo {health.data.mode}
      </Badge>
    </div>
  );
}

export function InicioPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">Estação de inspeção</h1>
        <p className="mt-1 text-muted-foreground">
          Fundação do sistema. As telas de operação entram nos próximos blocos.
        </p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Server className="size-5 text-primary" aria-hidden />
            Sistema
          </CardTitle>
          <CardDescription>Situação do serviço local que coordena câmera, IA e bancada.</CardDescription>
        </CardHeader>
        <CardContent>
          <ServiceStatus />
        </CardContent>
      </Card>
    </div>
  );
}
