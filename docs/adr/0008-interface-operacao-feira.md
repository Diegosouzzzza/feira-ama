# ADR 0008 — Interface: Operação e Modo feira

Data: 2026-10-19 · Situação: aceita

## Decisões de design

1. **Paleta do briefing**, com papéis fixos: verde = aprovado/ações, âmbar = classe B, vermelho = classe C, anil = revisão, vermelho escuro só para **falha da máquina**. Rejeição é resultado normal e nunca usa o visual de falha.
2. **Archivo** (empacotada localmente, eixo de largura) no lugar da Inter: versão expandida e pesada para a letra da classe e os números grandes, largura normal no resto, algarismos tabulares. Uma família só.
3. **Esquema da esteira** como elemento central (em vez de um "stepper" genérico): Entrada → Câmera (S1) → Pá (S2) → Aprovados/Rejeitados. A posição da peça vem do estado da placa; as luzes de S1/S2 são leituras reais dos sensores. Abaixo de 1024 px vira uma faixa de etapas em texto.
4. **Inconclusivo nunca mostra a letra do modelo**: "?" enquanto ninguém decide; ícone de operador depois. A sugestão do modelo aparece só como texto ("o modelo sugeriu Classe B").
5. **Foto analisada**, não vídeo: a imagem exibida é a mesma que o modelo avaliou, com número da inspeção e horário (America/Manaus). Vídeo ao vivo, se vier, será identificado à parte (Bloco 7).
6. **Modo feira** escuro, somente leitura, sem rolagem em 1920×1080, frase explicativa para o visitante e aviso "Demonstração com bancada simulada" no modo simulado.

## Decisões de funcionamento

1. **Estado só do servidor**: a tela aplica eventos do WebSocket num redutor puro (`lib/realtime/reducer.ts`) e nunca conta nada sozinha.
2. **Cursor de sequência nunca volta**: snapshots reenviados a todos podem chegar depois de eventos mais novos; o redutor guarda o maior `seq`. Sem isso, a tela entrava em loop de reconexão e perdia eventos de inspeção.
3. **Últimas peças** vêm de `GET /api/inspections?lot_id=` ao abrir/reconectar e são completadas pelos eventos.
4. **Abrir/encerrar lote reenvia o snapshot** (o modelo carregado muda fora do fluxo de eventos).
5. **Controle**: token guardado no `localStorage` do navegador; a tela só se considera operadora se o servidor confirmar o mesmo nome como detentor. `CONTROL_LOCKED` em qualquer comando apaga o token local.
6. **Erros** aparecem como aviso com a mensagem e a ação sugerida vindas da API; "Iniciar" bloqueado mostra o motivo na barra.

## Testes

- Vitest: redutor (lacunas, duplicatas, snapshot atrasado, revisão, incidentes) e contrato de tipos.
- Playwright com o **Microsoft Edge instalado** (sem baixar navegadores), contra a API real com bancada simulada (velocidade 15×, semente 9): fluxo do operador, recarregar sem duplicar `MACHINE_START`/`LOT_OPENED`, segunda tela só leitura, Modo feira sem rolagem em Full HD, celular sem rolagem horizontal, tomada de controle e parada.
