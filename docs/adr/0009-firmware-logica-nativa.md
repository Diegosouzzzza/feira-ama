# ADR 0009 — Lógica do firmware portátil e testada no PC

Data: 2026-10-19 · Situação: aceita

## Contexto

O firmware precisa seguir exatamente a tabela de estados e o protocolo do servidor, mas a bancada ainda não existe e o motor da esteira não foi escolhido.

## Decisões

1. **Lógica separada da placa**: `lib/av_core` não depende do Arduino. A placa entra por `av::Hal` (sensores, servo, aleatório) e `av::MotorDriver` (motor). Isso permite testar no PC e trocar o driver sem tocar na lógica.
2. **Motor plugável em tempo de compilação**: driver 1 (liga/desliga) e driver 2 (BTS7960) já existem; o padrão é o 1 até a pendência 2 ser resolvida.
3. **Compilador nativo via `ziglang`** (dependência de desenvolvimento do `api/`, versão 0.13.0.post1, a última com pacote para Windows). Nada é instalado no sistema; `uv sync` traz o compilador. O PlatformIO `native` foi descartado porque exige GCC no PATH.
4. **Harness por stdin/stdout + `ProcessLink`**: a mesma interface `Link` do coordenador serve para o simulador Python, o harness nativo e, no futuro, a porta serial. Os testes de sistema usam a lógica real do firmware.
5. **ArduinoJson 7.4.3 fixado**, C++17 (`-std=gnu++17`) no ESP32.
6. **Servo sem sinal até `CONFIGURE`**: na inicialização o firmware não comanda posição nenhuma, para não mexer a pá antes de saber o repouso calibrado.
7. **Emergência**: o corte é por hardware; a entrada do ESP32 é informativa (ativa em nível baixo, pino solto lê "solta").

## Consequências

- Divergência entre firmware e servidor aparece nos testes do `api/` (tabela, exemplos de contrato e ciclos completos).
- A física do harness é simplificada (posição × velocidade da esteira); a calibração real continua obrigatória na bancada.
