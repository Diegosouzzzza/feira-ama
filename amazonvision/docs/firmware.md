# Firmware do ESP32

## Organização

| Parte | Onde | O que faz |
|---|---|---|
| Lógica | `firmware/lib/av_core/` | Máquina de estados (`av_machine`), protocolo (`av_protocol`) e controlador do ciclo (`av_controller`). C++17 puro, sem Arduino: compila no ESP32 e no PC. |
| Placa | `firmware/src/` | Serial, pinos, servo (LEDC) e drivers do motor (`motor_drivers.h`). Configuração em `board_config.h`. |
| Testes nativos | `firmware/test/native/` | `unit_tests.cpp` (relógio e sensores manuais) e `harness.cpp` (lógica real sobre uma esteira simulada, falando o protocolo por stdin/stdout). |
| Build nativo | `firmware/tools/build_native.py` | Compila os testes com o C++ do pacote `ziglang` (dependência de desenvolvimento do `api/`). |

O controlador não bloqueia: tudo avança em `tick(now_ms)`, chamado a cada ~1 ms. Comandos chegam por linha (`handle_line`).

## Pinos (definitivos)

Fonte: `desenho-eletrico/netlist-geral.csv` e `firmware/src/board_config.h`. ESP32 DevKit V1 alimentado em 5,0 V pelo VIN (Buck LM2596); atuadores em alimentação separada, com o GND em comum.

| Função | GPIO | Sentido | Detalhes |
|---|---|---|---|
| Sensor S1 (entrada / ponto de inspeção) | 25 | Entrada, `INPUT_PULLUP` | Sensor IR NPN 5 V por 1 kΩ + clamp BAT54S. **Ativo em LOW** (peça presente = 0 V). |
| Sensor S2 (separação / saída) | 26 | Entrada, `INPUT_PULLUP` | Mesmo circuito do S1. **Ativo em LOW**. |
| E-STOP (contato NF ao GND) | 27 | Entrada, `INPUT_PULLUP` | Lógica à prova de falha: **normal = LOW** (contato fechado), **emergência ou fio partido = HIGH**. O segundo contato do botão corta a bobina do K1 por hardware. |
| Servo desviador MG996R/MG995 | 18 | Saída PWM | LEDC canal 0, 50 Hz, 16 bits, 500–2500 µs ↔ 0–180°. Sem sinal até o primeiro `CONFIGURE`. |
| Motor da esteira (módulo MOSFET D4184) | 19 | Saída PWM | LEDC canal 2, **20 kHz**, 8 bits, ativo em HIGH. Velocidade por `motor_power_pct`. |
| Relé de segurança K1 (bobina) | 4 | Saída | BC337-40 low-side + pull-down 10 kΩ. HIGH = atuadores energizados. LOW em falha, emergência e desarmada. |
| Buzzer 5 V | 13 | Saída | BC337-40. Intermitente em falha/emergência. |
| LED vermelho (falha/emergência) | 17 | Saída | Painel 22 mm, 330 Ω. |
| LED verde (pronto/operando) | 16 | Saída | Painel 22 mm, 330 Ω. |
| LED amarelo (desarmada/manutenção) | 5 | Saída | Painel 22 mm, 330 Ω. |
| LED da placa | 2 | Saída | Aceso: pronto/ciclo; pisca lento: desarmada/manutenção; pisca rápido: falha/emergência. |
| Reservados ao driver 2 (BTS7960) | 21, 22, 23 | — | Só com `AV_MOTOR_DRIVER=2`. Livres na montagem atual. |

Cuidados com os pinos:

- Evitar os pinos de *strapping* (0, 2, 12, 15) para entradas e os 34–39 (sem pull-up interno). O GPIO 2 e o GPIO 5 são *strapping* usados aqui só como saída de LED; o GPIO 5 emite PWM por um instante no boot (o LED amarelo pisca ao ligar, é normal).
- O **GPIO 4 (K1)** fica em LOW durante o boot graças ao pull-down de 10 kΩ: os atuadores só recebem energia depois que o firmware decide.
- **Canais LEDC dividem o temporizador em pares** (0–1, 2–3...). O servo usa o canal 0 em 50 Hz; por isso o motor usa o canal 2. No canal 1 os 20 kHz do motor mudariam a frequência do servo. `board_config.h` recusa compilar com essa combinação.

Estados do relé e dos sinais (em `update_led`, `src/main.cpp`):

| Estado | K1 | LED | Buzzer |
|---|---|---|---|
| `DISARMED` | desligado | amarelo | — |
| `MAINTENANCE` | ligado (se o E-STOP estiver solto) | amarelo | — |
| `READY` e estados do ciclo | ligado (se o E-STOP estiver solto) | verde | — |
| `FAULT`, `ESTOP` | desligado | vermelho | intermitente |

## Driver do motor

Definido em tempo de compilação por `AV_MOTOR_DRIVER`:

| Valor | Classe (`src/motor_drivers.h`) | Uso |
|---|---|---|
| `1` (padrão) | `PwmMosfetMotor` | Módulo MOSFET **D4184** no GPIO 19, PWM 20 kHz. |
| `0` | `OnOffMotor` | Saída só liga/desliga (módulo relé). Ignora `motor_power_pct`. |
| `2` | `Bts7960Motor` | Ponte H BTS7960/IBT-2, só para frente, PWM em RPWM. |

```powershell
cd firmware
pio run                                                        # D4184 com PWM (padrão)
$env:PLATFORMIO_BUILD_FLAGS="-DAV_MOTOR_DRIVER=0"; pio run      # só liga/desliga
$env:PLATFORMIO_BUILD_FLAGS="-DAV_MOTOR_PWM_HZ=2000"; pio run   # PWM mais lento (ver abaixo)
```

Potência (`motor_power_pct` do `CONFIGURE`, campo "Potência do motor" na tela Configuração): 1–100 %. **Vazio ou 0 = potência total** — é o que acontece no `TEST_MOTOR` da Manutenção antes de qualquer `CONFIGURE`. A conta é `av::pwm_duty` (`lib/av_core/src/av_hal.h`), testada no PC.

Se o módulo D4184 tiver optoacoplador na entrada (PC817) e a velocidade não acompanhar a potência configurada, ou o MOSFET esquentar, o optoacoplador não está dando conta dos 20 kHz: recompile com `-DAV_MOTOR_PWM_HZ=2000` (o motor passa a zumbir, mas o controle fica linear). O Motor TT é de 3–6 V: confira a tensão da alimentação dos atuadores antes de usar 100 %.

Um driver novo é uma classe que implementa `av::MotorDriver` em `src/motor_drivers.h`.

## Gravar e acompanhar

```powershell
cd firmware
pio run -t upload
pio device monitor        # 115200; envie {"protocol_version":1,...} para testar à mão
```

Feche o monitor serial antes de subir a API: só um programa por vez abre a porta COM. Se o `pio` do PATH falhar com "uv trampoline failed", use o do instalador oficial: `& "$env:USERPROFILE\.platformio\penv\Scripts\pio.exe" run -t upload` (os scripts em `scripts\` já fazem isso).

### Reset ao abrir a porta (Windows)

No DevKit as linhas DTR/RTS da USB Serial comandam EN e GPIO 0. Abrir a porta COM costuma reiniciar o ESP32: ele leva 1,5–2,5 s para subir e antes disso imprime texto do bootloader em outra velocidade (chega como lixo). A API trata isso em três camadas:

1. `SerialLink` abre a porta com DTR e RTS baixos, o que evita o reset na maioria dos drivers CH340/CP210x.
2. Linhas que não são um objeto JSON completo (lixo do bootloader, linha cortada) são descartadas antes do protocolo.
3. Se a placa reiniciar mesmo assim, o `HELLO` inicial expira; o primeiro *heartbeat* sem sessão válida faz o `Coordinator` enviar `HELLO` de novo. Enquanto não há sessão aceita, os comandos respondem "placa não está respondendo" em vez de `NAK NO_SESSION`.

Na inicialização a placa fica `DISARMED`, motor desligado e servo sem sinal até receber `CONFIGURE`. Nada se move sem `ARM` + `START_CYCLE`.

## Testes

Rodam junto com a suíte da API (`scripts/testar.ps1` ou `uv run pytest` em `api/`):

- **Unitários em C++** (19 casos): ciclo completo, filtro de ruído dos sensores, prazos, idempotência, perda de comunicação, emergência, rearme.
- **Tabela de estados** C++ comparada com a Python.
- **Contrato**: todos os exemplos de `docs/protocolo/exemplos` passam pela lógica real do firmware; cada linha que ela gera é validada pelo Pydantic do servidor.
- **Sistema**: a API completa opera o firmware nativo pelo harness (`ProcessLink`), com ciclos aprovados, rejeitados, revisão de inconclusivo, emergência, retirada de peça e reinício da placa.

Para usar o firmware nativo no lugar do simulador Python ao rodar a API (modo simulado):

```powershell
cd api
uv run python ..\firmware\tools\build_native.py harness
$env:AV_FIRMWARE_HARNESS='["../firmware/.pio/native/harness.exe","--belt-mm-s","200"]'
uv run amazonvision
```

## Ainda não validado

- Leitura real dos sensores IR NPN via clamp BAT54S+R=1kΩ (polaridade e filtro de debounce 25ms).
- Tempos e ângulos reais (calibração no Bloco 9).
- PWM de 20 kHz no módulo D4184 real (linearidade da velocidade, aquecimento) e comportamento da esteira ao parar (inércia).
- Ensaio de 50 ciclos físicos e testes de falha na bancada (cabo USB, S2 ausente, emergência).
