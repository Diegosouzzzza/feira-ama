# ADR 0003 — Stack do frontend

Data: 2026-10-18 · Situação: aceita

## Decisão

| Uso | Escolha |
|---|---|
| Base | React 19 + TypeScript + Vite |
| Rotas | React Router |
| Dados HTTP | TanStack Query |
| Tempo real (Bloco 3+) | WebSocket alimentando store Zustand |
| Estilo | Tailwind CSS 4 com tokens da paleta AmazonVision (`src/styles/index.css`) |
| Componentes | shadcn/ui (código copiado em `src/components/ui`, sobre Radix) |
| Ícones / fonte | lucide-react; Inter empacotada localmente (@fontsource) |
| Tipos da API | openapi-typescript a partir de `api/openapi.json` |
| Testes | Vitest; Playwright para fluxos (Bloco 5) |
| Gerenciador | pnpm |

O Node é usado **somente no desenvolvimento**. O `pnpm build` gera arquivos estáticos em `web/dist`, servidos pelo FastAPI.

## Observações

- **TypeScript fixado em 6.x.** O TypeScript 7 (compilador nativo) não expõe a API JavaScript usada pelo openapi-typescript. Reavaliar quando as ferramentas do ecossistema suportarem a versão 7.
- O `shadcn add` instalou o pacote `cn`. Os componentes foram apontados para `@/lib/utils` (clsx + tailwind-merge) e o pacote foi removido. Ao adicionar novos componentes, repetir essa troca.
- Cores de resultado (A, B, C, revisão, falha, dado antigo) são tokens próprios e sempre aparecem acompanhadas de texto.
