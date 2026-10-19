# ADR 0004 — Firmware com PlatformIO

Data: 2026-10-18 · Situação: aceita

## Decisão

PlatformIO com `framework = arduino` em vez da Arduino IDE 2, porque a plataforma e as bibliotecas ficam declaradas em `platformio.ini` e a compilação é reproduzível em qualquer máquina e pela linha de comando.

## Regras já definidas

- Loop não bloqueante (sem `delay()` longo).
- Linhas seriais com tamanho máximo; linha longa demais gera erro, nunca estouro de buffer.
- Ao abrir a porta serial, o computador deve usar `dtr=False, rts=False` para não reiniciar o ESP32.
- O driver DRV8833 citado no PDF não serve para motor de 12 V; o módulo de motor será escolhido após a pendência 2 (`docs/pendencias.md`).

## Versões fixadas

`platform = espressif32@7.0.1`, que traz o **Arduino-ESP32 core 2.0.17**. É a linha estável distribuída oficialmente pelo PlatformIO. O core 3.x só existe no fork comunitário pioarduino e não traz nenhum recurso necessário a este projeto. Consequência: usar a API LEDC antiga (`ledcSetup`/`ledcAttachPin`) ou a biblioteca ESP32Servo compatível com o 2.x.

Primeira compilação (Bloco 1): RAM 6,6 %, flash 20,6 %.
