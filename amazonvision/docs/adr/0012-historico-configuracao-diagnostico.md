# ADR 0012 — Histórico, Configuração e Diagnóstico

Data: 2026-10-19 · Situação: aceita

## Decisões

1. **Histórico com filtros no servidor** (`/api/inspections`): produto, lote, classe prevista, desfecho (`approved`, `rejected`, `pending_review`, `inconclusive`, `reviewed`) e período (`from` inclusivo, `to` exclusivo). A tela usa o dia local inteiro como fim do período.
2. **CSV para planilha em português**: UTF-8 com BOM, separador `;`, vírgula decimal, datas no fuso do computador e o SHA-256 da foto para rastrear a peça. Toda célula que começa com `=`, `+`, `-`, `@`, tab ou retorno recebe `'` na frente: o arquivo nunca executa fórmulas.
3. **Correção pelo histórico** usa a mesma rota de revisão: grava quem, por quê e a decisão anterior; a previsão do modelo nunca é alterada.
4. **Distribuição de classes por lote** desenhada em CSS com a tabela equivalente ao lado, em vez de Chart.js: menos uma dependência e a mesma informação acessível.
5. **Configuração por produto** (`/api/products/{id}/config`): apresentação, limiar e a calibração da bancada (os mesmos campos e limites do `CONFIGURE` do protocolo serial). Só com a esteira parada e sem lote aberto daquele produto; o lote congela os valores ao abrir, então a mudança vale para o próximo. Bloqueio otimista por `version`: duas telas não sobrescrevem uma à outra sem saber. Cada alteração vira `CONFIG_CHANGED` com o antes e o depois.
6. **Sem calibração**, a configuração mostra os valores da bancada simulada como ponto de partida; no modo real a máquina continua recusando armar até alguém salvar uma calibração.
7. **Limiar manual de 0,40 a 0,99**, o mesmo intervalo que o treinamento usa para calibrar; assim um limiar vindo do modelo sempre pode ser salvo de novo.
8. **Modo manutenção pela API** (`/api/machine/maintenance/*`), usando os comandos que o protocolo e o firmware já tinham (`ENTER_MAINTENANCE`, `TEST_MOTOR`, `TEST_SERVO`, `EXIT_MAINTENANCE`). Entrar exige a esteira parada; de `READY` a máquina é desarmada antes. Os testes ficam no registro de eventos com o operador.

## Evidências

- Testes da API: filtros e período, CSV (BOM, colunas, vírgula decimal, proteção contra fórmula), configuração (padrão simulado, salvar e valer no próximo lote, versão desatualizada, valores incoerentes, bloqueio com lote aberto, evento com antes/depois), manutenção (testes recusados fora dela, motor e servo na placa simulada, recusa com a esteira rodando, saída idempotente).
- Testes de navegador: histórico com filtro e CSV, configuração salvando e bloqueando, diagnóstico com manutenção e eventos, telas novas sem rolagem horizontal no celular.
