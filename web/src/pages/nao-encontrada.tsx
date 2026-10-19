import { Link } from "react-router";
import { Button } from "@/components/ui/button";

export function NaoEncontradaPage() {
  return (
    <div className="mx-auto max-w-md py-16 text-center">
      <p className="text-sm font-semibold text-primary">Erro 404</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">Página não encontrada</h1>
      <p className="mt-2 text-muted-foreground">Este endereço não existe no painel.</p>
      <Button asChild className="mt-6">
        <Link to="/">Voltar ao início</Link>
      </Button>
    </div>
  );
}
