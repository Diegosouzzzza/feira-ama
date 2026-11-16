# ADR 0013 — Link serial real com o ESP32

Data: 2026-10-20 · Situação: aceita

## Contexto

A bancada simulada (Bloco 4) e a lógica do firmware testada no PC (Bloco 6) já falam o protocolo serial; faltava a ligação real pelo cabo USB, única peça de software que impede o modo real de funcionar.

## Decisões

1. **pyserial**, puro Python, sem depender de asyncio nativo (que não tem suporte estável para Windows COM): a leitura roda numa linha de execução própria (como a câmera), empurrando cada linha para uma fila que o coordenador lê de forma assíncrona. `close()` interrompe uma leitura bloqueada fechando a porta a partir de outra linha — forma documentada do pyserial para isso.
2. **Configurado por `AV_SERIAL_PORT`/`AV_SERIAL_BAUD_RATE`** (mesma ideia da câmera via `AV_CAMERA_SOURCE`): fixo na inicialização, não trocável em tempo de execução pela tela. Sem porta configurada, o serviço sobe normalmente, sem placa.
3. **Reconexão automática no coordenador**: quando a leitura falha (cabo solto, porta fechada), o coordenador tenta reabrir o link a cada poucos segundos, até conseguir, sem precisar reiniciar o serviço. Genérico o bastante para também reconectar o executável nativo do firmware (`ProcessLink`) se o processo cair.
4. **`GET /api/diagnostics/serial-ports`** lista as portas USB visíveis ao sistema (nome, descrição, hardware ID), para a equipe descobrir qual é a placa sem abrir o Gerenciador de Dispositivos; a tela Diagnóstico mostra isso automaticamente quando a placa não responde.

## Evidências

- Testes do `SerialLink` com uma porta falsa: leitura, escrita, falha ao abrir, interrupção de leitura bloqueada, reabertura.
- Testes do coordenador: reconecta sozinho após o link cair (mesmo `boot_id`, mesma sessão simulada), e o laço de reconexão para quando o serviço é encerrado.
- 286 testes da API passando com a mudança.
