

// ========================================================
// BANCO DE DADOS DE COMPONENTES DO INSPECTOR DRAWER
// ========================================================
const INSPECTOR_DB = {
  "PS1": {
    "tag": "PS1",
    "name": "Fonte Chaveada Colmeia 12V 10A (120W) — MONO-FONTE PRINCIPAL",
    "model": "Mean Well LRS-120-12 (ou equivalente industrial 12V 10A)",
    "funcao": "Única fonte primária de alimentação de toda a bancada industrial (Arquitetura Mono-Fonte 12V). Alimenta diretamente o motorredutor da esteira (12V), a luminária Ring Light (12V) e o relé de segurança K1 (12V). Também supre os conversores Buck U2 (rebaixando para 6,0V p/ servo MG996R) e U4 (rebaixando para 5,0V p/ ESP32 e sensores ópticos E18-D80NK).",
    "eletrica": "Entrada: 100–240V AC 60Hz | Saída: 12,0V DC ±1% / 10A (Pico 12A / 120W) | Eficiência: 88% | Proteção contra sobrecarga, sobretensão e curto-circuito.",
    "checklist": [
      "Borne L (AC): Conectar fio Fase vindo do disjuntor bipolar Q0 / Filtro RFI S_MAIN (Anilha L01 - 1,0 mm²).",
      "Borne N (AC): Conectar fio Neutro vindo do disjuntor Q0 / Filtro RFI S_MAIN (Anilha N01 - 1,0 mm²).",
      "Borne PE (Terra): Conectar condutor Verde/Amarelo (1,5 mm²) diretamente à barra PE do trilho DIN TS-35.",
      "Borne -V (0V): Conectar à barra central 0V_COMUM no borne X1:8/X1:9 (referência unificada de potência e lógica).",
      "Borne +V (+12V): Conectar ao porta-fusível geral F1 (10A) antes da distribuição para o barramento contínuo +12V_CONT."
    ]
  },
  "Q0": {
    "tag": "Q0",
    "name": "Disjuntor Bipolar Termomagnético 10A Curva C",
    "model": "Schneider Electric Acti9 iK60N 2P 10A / IEC 60947-2",
    "funcao": "Proteção geral de entrada contra curto-circuitos e sobrecargas na alimentação AC da bancada. Secciona simultaneamente Fase e Neutro.",
    "eletrica": "Tensão nominal: 230/400V AC | Corrente nominal: 10A | Capacidade de ruptura: 4,5 kA | Curva de disparo: C (5 a 10 × In).",
    "checklist": [
      "Bornes Superiores 1 e 3: Entrada da rede AC (Fase e Neutro) vindos do plugue NBR 14136.",
      "Bornes Inferiores 2 e 4: Saída para os módulos DPS de proteção de surto e chave geral S_MAIN."
    ]
  },
  "S_MAIN": {
    "tag": "S_MAIN",
    "name": "Filtro de Linha RFI/EMI + Chave Geral Bipolar 10A",
    "model": "Corcom / Schurter Entrada IEC C14 com Filtro Integrado e Chave Bipolar Iluminada",
    "funcao": "Filtragem de ruídos eletromagnéticos de alta frequência da rede AC e chaveamento manual de energização da bancada com indicação luminosa.",
    "eletrica": "Tensão: 115–250V AC 50/60Hz | Corrente nominal: 10A | Atenuação RFI > 40 dB (150 kHz a 30 MHz).",
    "checklist": [
      "Bornes de Entrada: Conectados aos bornes 2 e 4 pós-disjuntor Q0.",
      "Bornes de Saída: Distribuem Fase e Neutro filtrados unicamente para a fonte chaveada PS1 (12V 10A).",
      "Terminal de Aterramento: Conectado diretamente à barra de proteção PE no trilho DIN."
    ]
  },
  "F1": {
    "tag": "F1",
    "name": "Fusível Geral de Proteção 12V DC (10A Tipo Lâmina)",
    "model": "Littelfuse ATO Fast-Acting 10A (Vermelho) com Porta-Fusível DIN",
    "funcao": "Proteção geral contra sobrecorrente e curto-circuito na saída de 12V da fonte colmeia PS1 antes da derivação dos barramentos.",
    "eletrica": "Tensão nominal: até 32V DC | Corrente nominal: 10A | Capacidade de interrupção: 1000A @ 32VDC.",
    "checklist": [
      "Terminal de Entrada: Conectado diretamente ao polo +V da Fonte PS1 (Cabo Vermelho 1,5 mm²).",
      "Terminal de Saída: Alimenta o barramento contínuo +12V_CONT e a entrada de potência do relé K1."
    ]
  },
  "DPS": {
    "tag": "DPS",
    "name": "Dispositivo de Proteção contra Surtos Classe II (2x)",
    "model": "Clamper Front Tec 275V / 20kA (Montagem DIN)",
    "funcao": "Drena para a terra (PE) transitórios de sobretensão causados por manobras na rede da feira ou descargas atmosféricas indiretas, protegendo a fonte chaveada PS1.",
    "eletrica": "Tensão máxima de operação contínua (Uc): 275V AC | Corrente de descarga nominal (In): 10kA | Corrente máxima (Imax): 20kA.",
    "checklist": [
      "Módulo 1: Entrada ligada na Fase (L) pós-disjuntor Q0; Saída inferior conectada à barra PE.",
      "Módulo 2: Entrada ligada no Neutro (N) pós-disjuntor Q0; Saída inferior conectada à barra PE."
    ]
  },
  "S0": {
    "tag": "S0",
    "name": "Botão de Parada de Emergência Ø22 mm com Trava Mecânica (NR-12)",
    "model": "Siemens Sirius / Steck com Bloco de Contatos 1 NF + 1 NA",
    "funcao": "Comando de Parada de Emergência Fail-Safe conforme NR-12. Seccionamento físico instantâneo dos atuadores mecânicos (motor e servo) e aviso digital de interrupção ao ESP32.",
    "eletrica": "Contatos: 1 NF (Abertura positiva forçada) + 1 NA | Tensão de isolamento: 600V | Corrente térmica Ith: 10A.",
    "checklist": [
      "Terminal NF 11: Entrada de +12V_CONT vinda do borne X2:7 (Cabo W206 - Vermelho 0,5 mm²).",
      "Terminal NF 12: Saída para a bobina A1 do Relé K1 via borne X2:8 (Cabo W207 - Vermelho 0,5 mm²).",
      "Terminal NA 13: Conectar à referência 0V_COMUM via borne X2:9.",
      "Terminal NA 14: Conectar ao pino GPIO 27 (PIN_ESTOP) do ESP32 via borne X2:10 (Cabo W205 - Violeta)."
    ]
  },
  "K1": {
    "tag": "K1",
    "name": "Relé Auxiliar de Segurança 12V DC 40A + Soquete DIN",
    "model": "DNI / Bosch Standard 5 Pinos Automotivo com Supressor",
    "funcao": "Elemento de corte eletromecânico do barramento seccionável de atuadores (+12V_AT). Garante abertura rápida dos contatos sem risco de soldagem por arco em caso de inrush do motor.",
    "eletrica": "Bobina: 12V DC (Resistência ~85 Ω / Corrente ~140 mA) | Contatos de potência: 30 e 87 (NA) suportam até 40A contínuos.",
    "checklist": [
      "Terminal A1 (Bobina): Conectar ao fio vindo do contato NF 12 do botão S0.",
      "Terminal A2 (Bobina): Conectar ao 0V_COMUM com diodo 1N4007 em antiparalelo (Catodo no A1, Anodo no A2).",
      "Terminal 30 (Comum Potência): Conectar ao barramento contínuo +12V_CONT pós-fusível F1 (1,0 mm²).",
      "Terminal 87 (NA Potência): Conecta ao barramento seccionável +12V_AT (alimenta F2 e F3)."
    ]
  },
  "U1": {
    "tag": "U1",
    "name": "Microcontrolador ESP32 DevKit V1 (ESP-WROOM-32)",
    "model": "Espressif Systems Dual-Core Xtensa LX6 240 MHz (30 Pinos)",
    "funcao": "Cérebro em tempo real da bancada. Lê os sensores ópticos reflexivos IR via GPIOs 25 e 26 com clamp de proteção Schottky BAT54S e resistor série de 1 kΩ (INPUT_PULLUP), controla a velocidade da esteira (GPIO 19), gera PWM de 50Hz para o empurrador (GPIO 18) e comunica via serial com o notebook de IA.",
    "eletrica": "Alimentação externa: 5,0V DC no pino VIN (via Buck U4) | Nível lógico de I/O: 3,3V CMOS (Máx 40mA por pino) | Consumo: ~180 mA com Wi-Fi inativo.",
    "checklist": [
      "Pino VIN: Alimentar com +5,0V DC vindo da saída do conversor Buck U4 (Anilha W08 - barramento +5V_ESP).",
      "Pino GND: Conectar à barra central 0V_COMUM.",
      "Pino GPIO 25 (PIN_SENSOR_S1): Conectar ao sinal clampado do Sensor S1 via borne X2:3 (BAT54S + 1 kΩ).",
      "Pino GPIO 26 (PIN_SENSOR_S2): Conectar ao sinal clampado do Sensor S2 via borne X2:6 (BAT54S + 1 kΩ).",
      "Pino GPIO 27 (PIN_ESTOP): Conectar ao terminal NA 14 do botão de emergência S0 via borne X2:10.",
      "Pino GPIO 18 (PIN_SERVO): Conectar ao terminal de sinal PWM (Laranja) do servo MG996R via borne X3:6.",
      "Pino GPIO 19 (PIN_MOTOR_ONOFF): Conectar ao terminal TRIG do módulo MOSFET D4184.",
      "Porta USB: Conectar cabo especial com via VBUS (+5V) cortada para ligar ao notebook host."
    ]
  },
  "U2": {
    "tag": "U2",
    "name": "Conversor Step-Down Buck DC-DC XL4015 (5A)",
    "model": "XLSEMI XL4015 E1 com dissipador de calor e trimpot multivoltas",
    "funcao": "Rebaixa os 12V da esteira (+12V_AT) para 6,00V DC dedicados exclusivamente à alimentação de potência do servomotor MG996R, garantindo torque máximo e estabilidade.",
    "eletrica": "Entrada: 12V DC (via fusível F2 de 3A) | Saída ajustada: 6,00V DC ±0,05V / até 5A contínuos | Rendimento: 92% | Fsw: 180 kHz.",
    "checklist": [
      "Terminal IN+: Conectar ao barramento +12V_AT pós-fusível F2 (Cabo W104 - 0,75 mm²).",
      "Terminal IN-: Conectar ao barramento 0V_COMUM (Cabo W105 - 0,75 mm²).",
      "Terminal OUT+: Fornece +6,0V DC para o servo via borne X3:4 (com capacitor C1 de 1000 µF soldado em paralelo).",
      "Terminal OUT-: Conectar ao retorno 0V do servo via borne X3:5 e ao 0V_COMUM."
    ]
  },
  "U4": {
    "tag": "U4",
    "name": "Conversor Buck Miniaturizado 12V → 5,0V DC (2A)",
    "model": "Módulo MP1584EN Step-Down Ultra Compacto",
    "funcao": "Alimenta localmente o microcontrolador ESP32 DevKit V1 e os dois sensores ópticos reflexivos E18-D80NK com 5,0V limpos e estabilizados a partir do barramento contínuo de 12V (+12V_CONT).",
    "eletrica": "Entrada: 12V DC contínuo (+12V_CONT) | Saída: 5,02V DC / até 2A | Ripple < 30 mV | Proteção térmica integrada.",
    "checklist": [
      "Terminal IN+: Conectar ao barramento contínuo +12V_CONT pós-fusível F1.",
      "Terminal IN-: Conectar ao barramento 0V_COMUM.",
      "Terminal OUT+: Alimenta o pino VIN do ESP32 e gera o barramento +5V_ESP que alimenta os sensores S1 e S2 nos bornes X2:1 e X2:4.",
      "Terminal OUT-: Conectar ao pino GND do ESP32 e à barra 0V_COMUM."
    ]
  },
  "D4184": {
    "tag": "D4184",
    "name": "Módulo Driver MOSFET Duplo AOD4184 (40V / 15A / 400W)",
    "model": "Módulo MOSFET Dual N-Channel com Optoacoplador e Pull-down",
    "funcao": "Chaveia a alimentação negativa do motorredutor da esteira em alta velocidade a partir do comando digital de 3,3V do ESP32 (GPIO 19), com resistência de condução quase nula.",
    "eletrica": "Tensão de carga: até 40V DC | Corrente nominal: 15A contínuos (Pico 30A) | Rds(on) < 8.5 mΩ | Tensão de trigger: 3,3V a 20V.",
    "checklist": [
      "Borne LOAD- (Dreno): Conectar ao polo negativo do motorredutor (MOT-) via borne X3:2.",
      "Borne GND-IN (Source): Conectar ao barramento 0V_COMUM (Cabo W103 - 1,0 mm²).",
      "Terminal TRIG: Conectar ao pino GPIO 19 (PIN_MOTOR_ONOFF) do ESP32 (Cabo W201).",
      "Terminal GND (Sinal): Conectar ao GND lógico do microcontrolador."
    ]
  },
  "M1": {
    "tag": "M1",
    "name": "Motorredutor DC 12V de Alto Torque (Esteira 70 cm)",
    "model": "Bohao / GA37-550 DC 12V 60 RPM com Caixa de Redução Metálica",
    "funcao": "Aciona o rolete de tração da correia transportadora de 70 cm. Mantém velocidade uniforme (~0,15 m/s) para transporte suave dos frutos (tucumã e castanha).",
    "eletrica": "Tensão nominal: 12V DC | Corrente nominal em carga: 1,2A | Corrente de partida (travado): ~4,5A | Torque: 12 kgf·cm nominal (15 kgf·cm stall).",
    "checklist": [
      "Terminal Positivo (MOT+): Conectar ao borne X3:1 (+12V_AT via fusível F3 de 5A).",
      "Terminal Negativo (MOT-): Conectar ao borne X3:2 (Dreno do MOSFET D4184).",
      "Diodo Schottky 1N5822: Soldar em antiparalelo direto nos bornes do motor (Catodo na faixa branca no MOT+, Anodo no MOT-)."
    ]
  },
  "M2": {
    "tag": "M2",
    "name": "Mecanismo Empurrador Linear (Servo MG996R + Biela-Manivela)",
    "model": "TowerPro MG996R Metal Gear + Mecanismo Biela-Manivela com Sapata Retilínea",
    "funcao": "Expulsa em linha reta os frutos defeituosos/rejeitados da esteira para a rampa lateral. A fruta aprovada passa direto com a sapata recolhida em 0 mm.",
    "eletrica": "Alimentação: 6,0V DC (via Buck XL4015) | Curso linear: 0 mm (recolhido) a 120 mm (avanço total) | Torque do servo: 11 kgf·cm @ 6V | Sinal: PWM 50Hz no GPIO 18.",
    "checklist": [
      "Fio Vermelho (+VCC): Conectar ao borne X3:4 (+6,0V DC regulados do Buck U2).",
      "Fio Marrom/Preto (GND): Conectar ao borne X3:5 (0V_COMUM).",
      "Fio Laranja/Amarelo (PWM): Conectar ao borne X3:6 (Sinal do pino GPIO 18 do ESP32)."
    ]
  },
  "B1": {
    "tag": "S1",
    "name": "Sensor Óptico Retangular IR 5V (S1 — Câmera)",
    "model": "Diymore / E18-D80NK (genérico) 5V NPN NA",
    "funcao": "Instalado na posição X = -150 mm antes da câmera. Detecta a aproximação do fruto na esteira e sinaliza a GPIO 25 do ESP32 para parada suave e disparo de captura da imagem na cúpula de visão computacional.",
    "eletrica": "Alimentação: 5,0V DC (via barramento +5V_ESP do Buck U4) | Consumo: < 25 mA | Distância ajustável: 3 a 80 cm | Saída: NPN Coletor Aberto NA (0V ativo / pull-up interno 10kΩ a 5V) | Proteção: Clamp BAT54S + R=1kΩ para 3,3V no ESP32.",
    "checklist": [
      "Fio Marrom (BN): Conectar ao borne X2:1 (Barramento +5V_ESP regulado por Buck U4).",
      "Fio Azul (BU): Conectar ao borne X2:2 (Barramento central 0V_COMUM).",
      "Fio Preto (BK): Conectar ao borne X2:3 (Ligado ao circuito de proteção R1=1kΩ + clamp BAT54S para a GPIO 25 do ESP32 com pinMode INPUT_PULLUP).",
      "Trimpot traseiro: Girar para calibrar alcance em ~70 mm focalizado no centro da correia transportadora."
    ]
  },
  "B2": {
    "tag": "S2",
    "name": "Sensor Óptico Retangular IR 5V (S2 — Desvio)",
    "model": "Diymore / E18-D80NK (genérico) 5V NPN NA",
    "funcao": "Instalado na posição X = +100 mm no alinhamento do Empurrador Linear. Detecta o fruto defeituoso e sinaliza a GPIO 26 do ESP32 para gatilhar o avanço milimétrico da sapata retilínea expulsando o fruto para a rampa.",
    "eletrica": "Alimentação: 5,0V DC (via barramento +5V_ESP do Buck U4) | Consumo: < 25 mA | Distância ajustável: 3 a 80 cm | Saída: NPN Coletor Aberto NA (0V ativo / pull-up interno 10kΩ a 5V) | Proteção: Clamp BAT54S + R=1kΩ para 3,3V no ESP32.",
    "checklist": [
      "Fio Marrom (BN): Conectar ao borne X2:4 (Barramento +5V_ESP regulado por Buck U4).",
      "Fio Azul (BU): Conectar ao borne X2:5 (Barramento central 0V_COMUM).",
      "Fio Preto (BK): Conectar ao borne X2:6 (Ligado ao circuito de proteção R2=1kΩ + clamp BAT54S para a GPIO 26 do ESP32 com pinMode INPUT_PULLUP).",
      "Trimpot traseiro: Calibrar alcance para detecção estável de frutos verdes, maduros e defeituosos."
    ]
  },
  "S1": {
    "tag": "S1",
    "name": "Sensor Óptico Retangular IR 5V (S1 — Câmera)",
    "model": "Diymore / E18-D80NK (genérico) 5V NPN NA",
    "funcao": "Instalado na posição X = -150 mm antes da câmera. Detecta a aproximação do fruto na esteira e sinaliza a GPIO 25 do ESP32 para parada suave e disparo de captura da imagem na cúpula de visão computacional.",
    "eletrica": "Alimentação: 5,0V DC (via barramento +5V_ESP do Buck U4) | Consumo: < 25 mA | Distância ajustável: 3 a 80 cm | Saída: NPN Coletor Aberto NA (0V ativo / pull-up interno 10kΩ a 5V) | Proteção: Clamp BAT54S + R=1kΩ para 3,3V no ESP32.",
    "checklist": [
      "Fio Marrom (BN): Conectar ao borne X2:1 (Barramento +5V_ESP regulado por Buck U4).",
      "Fio Azul (BU): Conectar ao borne X2:2 (Barramento central 0V_COMUM).",
      "Fio Preto (BK): Conectar ao borne X2:3 (Ligado ao circuito de proteção R1=1kΩ + clamp BAT54S para a GPIO 25 do ESP32 com pinMode INPUT_PULLUP).",
      "Trimpot traseiro: Girar para calibrar alcance em ~70 mm focalizado no centro da correia transportadora."
    ]
  },
  "S2": {
    "tag": "S2",
    "name": "Sensor Óptico Retangular IR 5V (S2 — Desvio)",
    "model": "Diymore / E18-D80NK (genérico) 5V NPN NA",
    "funcao": "Instalado na posição X = +100 mm no alinhamento do Empurrador Linear. Detecta o fruto defeituoso e sinaliza a GPIO 26 do ESP32 para gatilhar o avanço milimétrico da sapata retilínea expulsando o fruto para a rampa.",
    "eletrica": "Alimentação: 5,0V DC (via barramento +5V_ESP do Buck U4) | Consumo: < 25 mA | Distância ajustável: 3 a 80 cm | Saída: NPN Coletor Aberto NA (0V ativo / pull-up interno 10kΩ a 5V) | Proteção: Clamp BAT54S + R=1kΩ para 3,3V no ESP32.",
    "checklist": [
      "Fio Marrom (BN): Conectar ao borne X2:4 (Barramento +5V_ESP regulado por Buck U4).",
      "Fio Azul (BU): Conectar ao borne X2:5 (Barramento central 0V_COMUM).",
      "Fio Preto (BK): Conectar ao borne X2:6 (Ligado ao circuito de proteção R2=1kΩ + clamp BAT54S para a GPIO 26 do ESP32 com pinMode INPUT_PULLUP).",
      "Trimpot traseiro: Calibrar alcance para detecção estável de frutos verdes, maduros e defeituosos."
    ]
  },
  "X1": {
    "tag": "Régua X1",
    "name": "Régua de Bornes TS-35: Alimentação e 6 Barramentos Oficiais",
    "model": "Bornes de Passagem tipo Mola / Parafuso SAK / WAGO (10 Vias)",
    "funcao": "Concentra as entradas de alimentação AC e distribui com total segurança os 6 barramentos de tensão DC (+12V_CONT, +12V_AT, +6V_SRV, +5V_ESP, 0V_COMUM e PE).",
    "eletrica": "Tensão de isolamento: 800V | Corrente nominal: até 24A | Bitola admitida: 0,5 mm² a 2,5 mm².",
    "checklist": [
      "X1:1 (L - Fase) | X1:2 (N - Neutro) | X1:3 (PE - Terra com contato direto ao trilho DIN)",
      "X1:4 (+12V_CONT Barramento Contínuo) | X1:5 (+12V_AT Atuadores seccionado por K1 via NR-12)",
      "X1:6 (+6V_SRV Potência Servo MG996R) | X1:7 (+5V_ESP Alimentação ESP32 e Sensores IR Retangulares)",
      "X1:8 e X1:9 (0V_COMUM Retorno Unificado de Potência e Lógica) | X1:10 (Reserva Técnica)"
    ]
  },
  "X2": {
    "tag": "Régua X2",
    "name": "Régua de Bornes TS-35: Campo e Sensores IR Retangulares / S0",
    "model": "Bornes de Passagem Industriais (10 Vias)",
    "funcao": "Interface de conexão para os cabos de campo: sensores ópticos reflexivos IR retangulares (S1 e S2) e botão de parada de emergência cogumelo S0.",
    "eletrica": "Tensão nominal: 5V DC / 12V DC | Grau de proteção: IP20.",
    "checklist": [
      "X2:1 (+5V_ESP S1) | X2:2 (0V S1) | X2:3 (Sinal BK S1 ➔ R1kΩ ➔ BAT54S ➔ GPIO 25)",
      "X2:4 (+5V_ESP S2) | X2:5 (0V S2) | X2:6 (Sinal BK S2 ➔ R2kΩ ➔ BAT54S ➔ GPIO 26)",
      "X2:7 (S0 NF 11) | X2:8 (S0 NF 12 p/ Bobina K1)",
      "X2:9 (S0 NA 13 - 0V) | X2:10 (S0 NA 14 p/ GPIO 27)"
    ]
  },
  "X3": {
    "tag": "Régua X3",
    "name": "Régua de Bornes TS-35: Atuadores e Iluminação",
    "model": "Bornes de Passagem Industriais (8 Vias)",
    "funcao": "Interface de ligação dos cabos do motorredutor da esteira, do mecanismo empurrador linear e da luminária Ring Light da cúpula.",
    "eletrica": "Tensão nominal: 12V DC / 6V DC | Corrente máx: 10A.",
    "checklist": [
      "X3:1 (MOT+ 12V pós-F3) | X3:2 (MOT- retorno chaveado pelo D4184) | X3:3 (PE Terra da estrutura metálica)",
      "X3:4 (SRV_+6V potência servo) | X3:5 (SRV_GND retorno servo) | X3:6 (SRV_PWM sinal GPIO 18)",
      "X3:7 (LED_+12V Ring Light pós-F5) | X3:8 (LED_GND retorno 0V)"
    ]
  },
  "BAT54S": {
    "tag": "D2/D3",
    "name": "Diodo Schottky Duplo em Série (Clamp de Sobretensão 3,3V)",
    "model": "Nexperia / ON Semi BAT54S (SOT-23)",
    "funcao": "Proteção ativa contra sobretensão na entrada GPIO do ESP32. O sensor óptico IR possui pull-up interno SMD de 10 kΩ ligado a +5V, o que levaria a GPIO a 5V em repouso. O BAT54S grampeia a tensão máxima em 3,3V + Vf (Schottky ~0,25V) ≈ 3,55V, mantendo o nível lógico dentro do limite absoluto de segurança (3,6V).",
    "eletrica": "Tensão reversa máxima (Vr): 30V | Corrente contínua direta (If): 200 mA | Queda de tensão direta (Vf): 240 mV @ 0,1mA / 320 mV @ 1mA | Tempo de recuperação reversa (trr): < 5 ns.",
    "checklist": [
      "Pino 1 (Catodo 1): Conectar ao barramento lógico +3,3V do ESP32 (clamp superior).",
      "Pino 2 (Anodo 2): Conectar ao barramento 0V_COMUM / GND (clamp inferior contra transientes negativos).",
      "Pino 3 (Anodo 1 / Catodo 2 Comum): Conectar ao nó de sinal entre o resistor de 1 kΩ e a GPIO (25 ou 26)."
    ]
  },
  "R_PROTECAO": {
    "tag": "R1/R2",
    "name": "Resistor Série Limitador de Corrente de Clamp (1 kΩ 1/4W)",
    "model": "Resistor Filme Metálico 1 kΩ 1/4W 1% (ou SMD 0805/1206)",
    "funcao": "Instalado em série na linha de sinal BK do sensor óptico IR ANTES do clamp Schottky BAT54S. Limita a corrente de condução do clamp a menos de 2 mA durante o nível alto (repouso de 5V do pull-up de 10k do sensor), evitando aquecimento do diodo e sobrecorrente no barramento 3,3V.",
    "eletrica": "Resistência: 1,00 kΩ ±1% | Potência nominal: 0,25W (1/4W) | Coeficiente térmico: ±50 ppm/°C | Tensão máxima de trabalho: 250V.",
    "checklist": [
      "Terminal de Entrada: Conectar ao borne de sinal BK do sensor (X2:3 para S1 ou X2:6 para S2).",
      "Terminal de Saída: Conectar ao pino 3 do diodo duplo BAT54S e à respectiva GPIO do ESP32 (GPIO 25 para S1 / GPIO 26 para S2)."
    ]
  }
};

// ========================================================
// ESTADO GLOBAL DA SIMULAÇÃO ELÉTRICA INDUSTRIAL
// ========================================================
const SimState = {
  mainPower: true,      // Chave Geral AC Ligada/Desligada
  estopTripped: false,  // Botão S0 NR-12 Pressionado
  sensorS1: false,      // Sensor Fotoelétrico Câmera (X = -150mm)
  sensorS2: false,      // Sensor Fotoelétrico Desvio (X = +100mm)
  motorRun: true,       // Comando de Partida Esteira (GPIO 19)
  pusherExtended: false,// Empurrador Linear: false = 0 mm (Recolhido), true = 120 mm (Avançado)
  lightOn: true,        // Iluminação Ring Light 12V 6000K
  currentSheet: 0,      // Prancha Ativa (0..4) - Inicia na VISÃO 00
  theme: 'dark',        // Tema 'dark' ou 'light'
  isCycleRunning: false,// Flag de ciclo automático em andamento
  zoomLevel: 1.0,       // Nível de Zoom
  panX: 0,              // Deslocamento Pan X
  panY: 0,              // Deslocamento Pan Y
  isPanning: false,
  startX: 0,
  startY: 0
};

// ========================================================
// CONTROLES MANUAIS E INTERATIVIDADE
// ========================================================

function toggleMainPower(enabled) {
  SimState.mainPower = enabled;
  const lbl = document.getElementById('lblMainPower');
  if (lbl) {
    lbl.textContent = enabled ? 'LIGADA' : 'DESLIGADA';
    lbl.style.color = enabled ? '#00e676' : '#ff3344';
  }
  updateSimulationUI();
}

function toggleEstop() {
  SimState.estopTripped = !SimState.estopTripped;
  updateSimulationUI();
}

function setSensorS1(active) {
  SimState.sensorS1 = active;
  updateSimulationUI();
}

function toggleSensorS1Click() {
  SimState.sensorS1 = true;
  updateSimulationUI();
  setTimeout(() => {
    SimState.sensorS1 = false;
    updateSimulationUI();
  }, 1000);
}

function setSensorS2(active) {
  SimState.sensorS2 = active;
  updateSimulationUI();
}

function toggleSensorS2Click() {
  SimState.sensorS2 = true;
  updateSimulationUI();
  setTimeout(() => {
    SimState.sensorS2 = false;
    updateSimulationUI();
  }, 1000);
}

function toggleMotor() {
  SimState.motorRun = !SimState.motorRun;
  updateSimulationUI();
}

function toggleServo() {
  SimState.pusherExtended = !SimState.pusherExtended;
  updateSimulationUI();
}

function toggleLight() {
  SimState.lightOn = !SimState.lightOn;
  updateSimulationUI();
}

// ========================================================
// SIMULADOR DE CICLO AUTOMÁTICO PASSO A PASSO
// ========================================================
function runAutomaticCycle(fruitType) {
  if (SimState.isCycleRunning) return;
  if (!SimState.mainPower || SimState.estopTripped) {
    alert("Não é possível iniciar o ciclo: O painel está desligado ou o Botão de Emergência S0 está acionado!");
    return;
  }

  SimState.isCycleRunning = true;
  const isGood = (fruitType === 'good');
  
  // Elementos do banner e visualização
  const bannerTitle = document.getElementById('cycle_banner_title');
  const bannerStep = document.getElementById('cycle_step_text');
  const fruitGroup = document.getElementById('ov_animated_fruit');
  const fruitBody = document.getElementById('ov_fruit_body');
  const fruitLabel = document.getElementById('ov_fruit_label');

  if (fruitBody) {
    fruitBody.setAttribute('fill', isGood ? '#ff6d00' : '#8d6e63');
    fruitBody.setAttribute('stroke', isGood ? '#ffd600' : '#d50000');
  }
  if (fruitLabel) {
    fruitLabel.textContent = isGood ? 'TUCUMÃ' : 'DEFEITO';
  }

  // Passo 1: Partida do fruto na esteira (X = 30)
  if (bannerTitle) bannerTitle.textContent = "PASSO 1/5: FRUTO INSERIDO NA ESTEIRA TRANSPORTADORA (X = 0 mm)";
  if (bannerStep) bannerStep.textContent = "MOTOR LIGADO (1.2A) ➔ TRANSPORTE SUAVE";
  SimState.motorRun = true;
  SimState.sensorS1 = false;
  SimState.sensorS2 = false;
  SimState.pusherExtended = false;
  if (fruitGroup) fruitGroup.setAttribute('transform', 'translate(30, 70)');
  updateSimulationUI();

  // Passo 2: Fruto viaja até Sensor S1 (Câmera X = -150 mm) em 1.5s
  setTimeout(() => {
    if (!SimState.mainPower || SimState.estopTripped) { SimState.isCycleRunning = false; return; }
    if (fruitGroup) fruitGroup.setAttribute('transform', 'translate(180, 70)');
    SimState.sensorS1 = true;
    SimState.motorRun = false; // Pausa para captura estável
    if (bannerTitle) bannerTitle.textContent = "PASSO 2/5: S1 ATIVADO (X = -150 mm) ➔ PARADA P/ CAPTURA DA CÂMERA";
    if (bannerStep) bannerStep.textContent = "DISPARO DO SENSOR S1 (E18-D80NK 5V NPN ➔ GPIO 25 LOW)";
    updateSimulationUI();

    // Passo 3: Classificação da IA (1.2s após parada)
    setTimeout(() => {
      if (!SimState.mainPower || SimState.estopTripped) { SimState.isCycleRunning = false; return; }
      if (bannerTitle) {
        bannerTitle.textContent = isGood 
          ? "PASSO 3/5: IA CLASSIFICOU ➔ [TUCUMÃ APROVADO — CLASSE A (CONF: 97.4%)]" 
          : "PASSO 3/5: IA CLASSIFICOU ➔ [FRUTO COM INJÚRIA / REJEITADO (CONF: 94.8%)]";
      }
      if (bannerStep) bannerStep.textContent = isGood ? "DECISÃO: PASSAGEM DIRETA" : "DECISÃO: EXPULSÃO POR DESVIO LINEAR";
      SimState.sensorS1 = false;
      SimState.motorRun = true; // Retoma esteira
      updateSimulationUI();

      // Passo 4: Fruto viaja até Sensor S2 (X = +100 mm) em 1.6s
      setTimeout(() => {
        if (!SimState.mainPower || SimState.estopTripped) { SimState.isCycleRunning = false; return; }
        if (fruitGroup) fruitGroup.setAttribute('transform', 'translate(440, 70)');
        SimState.sensorS2 = true;
        if (bannerTitle) bannerTitle.textContent = "PASSO 4/5: S2 ATIVADO (X = +100 mm) ➔ GATILHO DA ESTAÇÃO DE DESVIO";
        if (bannerStep) bannerStep.textContent = "SINAL NO SENSOR S2 (E18-D80NK 5V NPN ➔ GPIO 26 LOW)";
        updateSimulationUI();

        // Passo 5: Decisão mecânica (Empurrador Linear)
        setTimeout(() => {
          if (!SimState.mainPower || SimState.estopTripped) { SimState.isCycleRunning = false; return; }
          SimState.sensorS2 = false;

          if (isGood) {
            // Fruta boa passa direto para a saída frontal
            if (bannerTitle) bannerTitle.textContent = "PASSO 5/5: EMPURRADOR RECOLHIDO (0 mm) ➔ FRUTA BOA PASSA DIRETO";
            if (bannerStep) bannerStep.textContent = "SAÍDA FRONTAL DE APROVADOS";
            if (fruitGroup) fruitGroup.setAttribute('transform', 'translate(740, 70)');
            updateSimulationUI();
            
            setTimeout(() => {
              if (bannerTitle) bannerTitle.textContent = "CICLO FINALIZADO COM SUCESSO: FRUTA APROVADA REGISTRADA!";
              if (bannerStep) bannerStep.textContent = "PRONTO PARA PRÓXIMO FRUTO";
              SimState.isCycleRunning = false;
            }, 1500);

          } else {
            // Fruta ruim: Empurrador linear avança 120 mm
            if (bannerTitle) bannerTitle.textContent = "PASSO 5/5: EMPURRADOR AVANÇA 120 mm ➔ EXPULSA FRUTA RUIM P/ RAMPA";
            if (bannerStep) bannerStep.textContent = "PULSO PWM 50Hz (2.1 ms) NO GPIO 18 ➔ BIELA AVANÇA";
            SimState.pusherExtended = true;
            updateSimulationUI();

            // Fruta cai na rampa
            setTimeout(() => {
              if (fruitGroup) fruitGroup.setAttribute('transform', 'translate(510, 150)');
              
              // Recolhe o empurrador de volta para 0 mm
              setTimeout(() => {
                SimState.pusherExtended = false;
                if (bannerTitle) bannerTitle.textContent = "CICLO FINALIZADO: FRUTA REJEITADA EXPULSA PELA RAMPA LATERAL!";
                if (bannerStep) bannerStep.textContent = "EMPURRADOR RECOLHIDO EM 0 mm ➔ PRONTO P/ PRÓXIMO";
                updateSimulationUI();
                SimState.isCycleRunning = false;
              }, 900);
            }, 600);
          }
        }, 1000);
      }, 1600);
    }, 1200);
  }, 1500);
}

// ========================================================
// ATUALIZAÇÃO REATIVA DE TODOS OS ELEMENTOS SVG & PAINÉIS
// ========================================================
function updateSimulationUI() {
  const pwr = SimState.mainPower;
  const estop = SimState.estopTripped;
  const s1 = SimState.sensorS1;
  const s2 = SimState.sensorS2;
  const mRun = SimState.motorRun && pwr && !estop;
  const light = SimState.lightOn && pwr;
  const pusher = SimState.pusherExtended && pwr && !estop;

  const bus12vAt = pwr && !estop;
  const bus12vCont = pwr;
  const bus6v = bus12vAt;
  const bus5v = pwr;

  // 1. Botão de Emergência e Banner NR-12
  const btnEstop = document.getElementById('btnEstop');
  const btnEstopText = document.getElementById('btnEstopText');
  const estopBanner = document.getElementById('estopBanner');
  const sysStatusPill = document.getElementById('sysStatusPill');
  const sysStatusText = document.getElementById('sysStatusText');

  if (estop) {
    if (btnEstop) {
      btnEstop.classList.add('tripped');
      btnEstopText.textContent = 'DESTRAVAR S0 (EMERGÊNCIA ATIVA)';
    }
    if (estopBanner) estopBanner.classList.add('active');
    if (sysStatusPill) {
      sysStatusPill.classList.add('danger');
      sysStatusText.textContent = 'ALERTA: PARADA DE EMERGÊNCIA ATIVA (NR-12)';
    }
  } else {
    if (btnEstop) {
      btnEstop.classList.remove('tripped');
      btnEstopText.textContent = 'EMERGÊNCIA S0 (NORMAL)';
    }
    if (estopBanner) estopBanner.classList.remove('active');
    if (sysStatusPill) {
      sysStatusPill.classList.remove('danger');
      sysStatusText.textContent = pwr ? 'SISTEMA ENERGIZADO (NORMAL)' : 'SISTEMA DESENERGIZADO';
    }
  }

  // 2. Animação Mecânica dos Contatos K1 e S0 nos SVGs
  const k1Contact = document.getElementById('k1_contact_arm');
  const s0ArmNf = document.getElementById('s0_arm_nf');
  const s0ArmNa = document.getElementById('s0_arm_na');
  const s3S0NaArm = document.getElementById('s3_s0_na_arm');
  const ovK1State = document.getElementById('ov_k1_state');

  if (estop || !pwr) {
    if (k1Contact) {
      k1Contact.setAttribute('y2', '2');
      k1Contact.setAttribute('stroke', '#5c7566');
    }
    if (s0ArmNf) {
      s0ArmNf.setAttribute('y2', '-8');
      s0ArmNf.setAttribute('stroke', '#ff1744');
    }
    if (s0ArmNa) {
      s0ArmNa.setAttribute('y2', '5');
      s0ArmNa.setAttribute('stroke', '#00e676');
    }
    if (s3S0NaArm) {
      s3S0NaArm.setAttribute('y2', '10');
      s3S0NaArm.setAttribute('stroke', '#00e676');
    }
    if (ovK1State) {
      ovK1State.textContent = '30-87 ABERTO';
      ovK1State.setAttribute('fill', '#ff1744');
    }
  } else {
    if (k1Contact) {
      k1Contact.setAttribute('y2', '10');
      k1Contact.setAttribute('stroke', '#00e676');
    }
    if (s0ArmNf) {
      s0ArmNf.setAttribute('y2', '0');
      s0ArmNf.setAttribute('stroke', '#00e676');
    }
    if (s0ArmNa) {
      s0ArmNa.setAttribute('y2', '-10');
      s0ArmNa.setAttribute('stroke', '#ff1744');
    }
    if (s3S0NaArm) {
      s3S0NaArm.setAttribute('y2', '0');
      s3S0NaArm.setAttribute('stroke', '#ff1744');
    }
    if (ovK1State) {
      ovK1State.textContent = '30-87 FECHADO';
      ovK1State.setAttribute('fill', '#00e676');
    }
  }

  // 3. Barramento +12V_AT (Linhas Dinâmicas)
  const wire12vAtList = [
    'wire_k1_contact_out', 'wire_12v_at_to_f3', 'wire_12v_at_to_f2', 'wire_f3_out',
    's2_wire_12v_at_entry', 's2_wire_w101', 's2_wire_mot_plus', 's2_wire_12v_at_servo_entry', 's2_wire_w104',
    'wire_ov_motor'
  ];
  wire12vAtList.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      if (bus12vAt) {
        el.classList.remove('off-wire');
        el.style.stroke = '#ff1744';
      } else {
        el.classList.add('off-wire');
        el.style.stroke = '#3b4d42';
      }
    }
  });

  // Linhas do Barramento +6V_SERVO
  const wire6vList = ['wire_6v_bus_out', 's2_wire_6v_out', 'wire_ov_servo'];
  wire6vList.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      if (bus6v) {
        el.classList.remove('off-wire');
        el.style.stroke = '#ff9100';
      } else {
        el.classList.add('off-wire');
        el.style.stroke = '#3b4d42';
      }
    }
  });

  // 4. Status do Motorredutor da Esteira (M1)
  const motorBtn = document.getElementById('btnMotor');
  const motorStatusLbl = document.getElementById('lblMotorStatus');
  const motorCurrentVal = document.getElementById('s2_motor_current_val');
  const motorRotorSpin = document.getElementById('motor_rotor_spin');
  const ovMotorGearSpin = document.getElementById('ov_motor_gear_spin');
  const ovMotorStatusText = document.getElementById('ov_motor_status_text');
  const valGpio19 = document.getElementById('val_gpio_19');

  if (mRun) {
    if (motorBtn) motorBtn.classList.add('active');
    if (motorStatusLbl) {
      motorStatusLbl.textContent = 'RODANDO (1.2A)';
      motorStatusLbl.style.color = '#00e676';
    }
    if (motorCurrentVal) {
      motorCurrentVal.textContent = 'CORRENTE: 1.2A (NOMINAL)';
      motorCurrentVal.style.color = '#00e676';
    }
    if (motorRotorSpin) motorRotorSpin.classList.add('motor-spin');
    if (ovMotorGearSpin) ovMotorGearSpin.classList.add('motor-spin');
    if (ovMotorStatusText) {
      ovMotorStatusText.textContent = 'STATUS: RODANDO (1.2A)';
      ovMotorStatusText.setAttribute('fill', '#00e676');
    }
    if (valGpio19) {
      valGpio19.textContent = '[OUT: HIGH 3,3V]';
      valGpio19.style.color = '#00e676';
    }
  } else {
    if (motorBtn) motorBtn.classList.remove('active');
    if (motorStatusLbl) {
      motorStatusLbl.textContent = estop ? 'PARADO (EMERGÊNCIA)' : (pwr ? 'PARADO' : 'SEM ENERGIA');
      motorStatusLbl.style.color = estop ? '#ff1744' : '#8fa699';
    }
    if (motorCurrentVal) {
      motorCurrentVal.textContent = 'CORRENTE: 0.0A (PARADO)';
      motorCurrentVal.style.color = '#8fa699';
    }
    if (motorRotorSpin) motorRotorSpin.classList.remove('motor-spin');
    if (ovMotorGearSpin) ovMotorGearSpin.classList.remove('motor-spin');
    if (ovMotorStatusText) {
      ovMotorStatusText.textContent = estop ? 'PARADA EMERGÊNCIA' : 'PARADO';
      ovMotorStatusText.setAttribute('fill', estop ? '#ff1744' : '#8fa699');
    }
    if (valGpio19) {
      valGpio19.textContent = '[OUT: LOW 0V]';
      valGpio19.style.color = '#8fa699';
    }
  }

  // 5. Mecanismo Empurrador Linear (M2) — Sapata Retilínea Avança 120 mm
  const lblServoAngle = document.getElementById('lblServoAngle');
  const s2PusherGroup = document.getElementById('s2_pusher_group');
  const s2CrankHorn = document.getElementById('s2_crank_horn');
  const s2ConnectingRod = document.getElementById('s2_connecting_rod');
  const lblS2StrokeText = document.getElementById('lbl_s2_stroke_text');

  const ovPusherShoeGroup = document.getElementById('ov_pusher_shoe_group');
  const ovCrankDisc = document.getElementById('ov_crank_disc');
  const ovConnectingRod = document.getElementById('ov_connecting_rod');
  const ovPusherStatusText = document.getElementById('ov_pusher_status_text');

  const svgPwmPulseWave = document.getElementById('svg_pwm_pulse_wave');
  const lblPwmPulsewidth = document.getElementById('lbl_pwm_pulsewidth');

  if (pusher) {
    if (lblServoAngle) {
      lblServoAngle.textContent = '120 mm (AVANÇO)';
      lblServoAngle.style.color = '#ff9100';
    }
    if (s2PusherGroup) s2PusherGroup.setAttribute('transform', 'translate(45, 0)');
    if (s2CrankHorn) s2CrankHorn.setAttribute('transform', 'translate(60, 75) rotate(90)');
    if (s2ConnectingRod) {
      s2ConnectingRod.setAttribute('x1', '60');
      s2ConnectingRod.setAttribute('y1', '85');
      s2ConnectingRod.setAttribute('x2', '175');
      s2ConnectingRod.setAttribute('y2', '75');
    }
    if (lblS2StrokeText) {
      lblS2StrokeText.textContent = '120 mm [AVANÇO REJEITO]';
      lblS2StrokeText.style.fill = '#ff9100';
    }

    if (ovPusherShoeGroup) ovPusherShoeGroup.setAttribute('transform', 'translate(35, 0)');
    if (ovCrankDisc) ovCrankDisc.setAttribute('transform', 'translate(42, 67) rotate(90)');
    if (ovPusherStatusText) {
      ovPusherStatusText.textContent = '120 mm [AVANÇO REJEITO]';
      ovPusherStatusText.setAttribute('fill', '#ff9100');
    }

    if (svgPwmPulseWave) svgPwmPulseWave.setAttribute('d', 'M 0 50 L 20 50 L 20 15 L 85 15 L 85 50 L 150 50');
    if (lblPwmPulsewidth) lblPwmPulsewidth.textContent = '2.1 ms (120 mm)';
  } else {
    if (lblServoAngle) {
      lblServoAngle.textContent = '0 mm (REC)';
      lblServoAngle.style.color = '#00e676';
    }
    if (s2PusherGroup) s2PusherGroup.setAttribute('transform', 'translate(0, 0)');
    if (s2CrankHorn) s2CrankHorn.setAttribute('transform', 'translate(60, 75) rotate(0)');
    if (s2ConnectingRod) {
      s2ConnectingRod.setAttribute('x1', '70');
      s2ConnectingRod.setAttribute('y1', '75');
      s2ConnectingRod.setAttribute('x2', '135');
      s2ConnectingRod.setAttribute('y2', '75');
    }
    if (lblS2StrokeText) {
      lblS2StrokeText.textContent = '0 mm [RECOLHIDO]';
      lblS2StrokeText.style.fill = '#00e676';
    }

    if (ovPusherShoeGroup) ovPusherShoeGroup.setAttribute('transform', 'translate(0, 0)');
    if (ovCrankDisc) ovCrankDisc.setAttribute('transform', 'translate(42, 67) rotate(0)');
    if (ovPusherStatusText) {
      ovPusherStatusText.textContent = '0 mm [RECOLHIDO]';
      ovPusherStatusText.setAttribute('fill', '#00e676');
    }

    if (svgPwmPulseWave) svgPwmPulseWave.setAttribute('d', 'M 0 50 L 20 50 L 20 15 L 45 15 L 45 50 L 150 50');
    if (lblPwmPulsewidth) lblPwmPulsewidth.textContent = '0.8 ms (0 mm)';
  }

  // 6. Sensor S1 (Câmera)
  const btnSensorS1 = document.getElementById('btnSensorS1');
  const badgeS1 = document.getElementById('badgeS1');
  const s1SensorLed = document.getElementById('s1_sensor_led');
  const ovS1SensorLed = document.getElementById('ov_s1_sensor_led');
  const ovS1Beam = document.getElementById('ov_s1_beam');
  const valGpio25 = document.getElementById('val_gpio_25');
  const wireS1Bk = document.getElementById('s3_wire_s1_bk');

  if (s1 && bus5v) {
    if (btnSensorS1) btnSensorS1.classList.add('active');
    if (badgeS1) {
      badgeS1.textContent = 'DETECTADO';
      badgeS1.style.background = '#00e5ff';
      badgeS1.style.color = '#000';
    }
    if (s1SensorLed) s1SensorLed.setAttribute('fill', '#00e676');
    if (ovS1SensorLed) ovS1SensorLed.setAttribute('fill', '#00e5ff');
    if (ovS1Beam) ovS1Beam.setAttribute('stroke', '#00e676');
    if (wireS1Bk) wireS1Bk.style.stroke = '#00e5ff';
    if (valGpio25) {
      valGpio25.textContent = '[DETECTADO: LOW (0V)]';
      valGpio25.style.color = '#00e5ff';
    }
  } else {
    if (btnSensorS1) btnSensorS1.classList.remove('active');
    if (badgeS1) {
      badgeS1.textContent = 'LIVRE';
      badgeS1.style.background = '#2a3a30';
      badgeS1.style.color = '#fff';
    }
    if (s1SensorLed) s1SensorLed.setAttribute('fill', '#0f1813');
    if (ovS1SensorLed) ovS1SensorLed.setAttribute('fill', '#00e676');
    if (ovS1Beam) ovS1Beam.setAttribute('stroke', '#00e5ff');
    if (wireS1Bk) wireS1Bk.style.stroke = '#8fa699';
    if (valGpio25) {
      valGpio25.textContent = '[INPUT_PULLUP: HIGH (3.3V)]';
      valGpio25.style.color = '#00e676';
    }
  }

  // 7. Sensor S2 (Desvio)
  const btnSensorS2 = document.getElementById('btnSensorS2');
  const badgeS2 = document.getElementById('badgeS2');
  const s2SensorLed = document.getElementById('s2_sensor_led');
  const ovS2SensorLed = document.getElementById('ov_s2_sensor_led');
  const ovS2Beam = document.getElementById('ov_s2_beam');
  const valGpio26 = document.getElementById('val_gpio_26');
  const wireS2Bk = document.getElementById('s3_wire_s2_bk');

  if (s2 && bus5v) {
    if (btnSensorS2) btnSensorS2.classList.add('active');
    if (badgeS2) {
      badgeS2.textContent = 'DETECTADO';
      badgeS2.style.background = '#00e5ff';
      badgeS2.style.color = '#000';
    }
    if (s2SensorLed) s2SensorLed.setAttribute('fill', '#00e676');
    if (ovS2SensorLed) ovS2SensorLed.setAttribute('fill', '#00e5ff');
    if (ovS2Beam) ovS2Beam.setAttribute('stroke', '#00e676');
    if (wireS2Bk) wireS2Bk.style.stroke = '#00e5ff';
    if (valGpio26) {
      valGpio26.textContent = '[DETECTADO: LOW (0V)]';
      valGpio26.style.color = '#00e5ff';
    }
  } else {
    if (btnSensorS2) btnSensorS2.classList.remove('active');
    if (badgeS2) {
      badgeS2.textContent = 'LIVRE';
      badgeS2.style.background = '#2a3a30';
      badgeS2.style.color = '#fff';
    }
    if (s2SensorLed) s2SensorLed.setAttribute('fill', '#0f1813');
    if (ovS2SensorLed) ovS2SensorLed.setAttribute('fill', '#1b2820');
    if (ovS2Beam) ovS2Beam.setAttribute('stroke', '#00e5ff');
    if (wireS2Bk) wireS2Bk.style.stroke = '#8fa699';
    if (valGpio26) {
      valGpio26.textContent = '[INPUT_PULLUP: HIGH (3.3V)]';
      valGpio26.style.color = '#00e676';
    }
  }

  // 8. GPIO 27 Monitoramento Emergência
  const valGpio27 = document.getElementById('val_gpio_27');
  if (valGpio27) {
    if (estop) {
      valGpio27.textContent = '[EMERGÊNCIA: LOW (0V)]';
      valGpio27.style.color = '#ff1744';
    } else {
      valGpio27.textContent = '[NORMAL: HIGH (3.3V)]';
      valGpio27.style.color = '#00e676';
    }
  }

  // 9. Iluminação Ring Light
  const btnLight = document.getElementById('btnLight');
  const lblLightStatus = document.getElementById('lblLightStatus');
  const ringLightGlow = document.getElementById('ring_light_glow');
  const sLedSwitchArm = document.getElementById('s_led_switch_arm');
  const ovRingLight = document.getElementById('ov_ring_light');

  if (light) {
    if (btnLight) btnLight.classList.add('active');
    if (lblLightStatus) {
      lblLightStatus.textContent = 'ON';
      lblLightStatus.style.color = '#00e676';
    }
    if (ringLightGlow) {
      ringLightGlow.setAttribute('fill', '#ffffff');
      ringLightGlow.style.filter = 'drop-shadow(0 0 10px #ffffff)';
    }
    if (ovRingLight) {
      ovRingLight.setAttribute('fill', '#ffffff');
      ovRingLight.style.filter = 'drop-shadow(0 0 12px #00e5ff)';
    }
    if (sLedSwitchArm) sLedSwitchArm.setAttribute('y2', '10');
  } else {
    if (btnLight) btnLight.classList.remove('active');
    if (lblLightStatus) {
      lblLightStatus.textContent = 'OFF';
      lblLightStatus.style.color = '#8fa699';
    }
    if (ringLightGlow) {
      ringLightGlow.setAttribute('fill', '#15241c');
      ringLightGlow.style.filter = 'none';
    }
    if (ovRingLight) {
      ovRingLight.setAttribute('fill', '#101a14');
      ovRingLight.style.filter = 'none';
    }
    if (sLedSwitchArm) sLedSwitchArm.setAttribute('y2', '3');
  }

  // 10. Quadro Sinóptico
  const st12vCont = document.getElementById('status_bar_12v_cont');
  const st12vAt = document.getElementById('status_bar_12v_at');
  const st6v = document.getElementById('status_bar_6v');
  const st5v = document.getElementById('status_bar_5v');

  if (st12vCont) st12vCont.textContent = bus12vCont ? 'STATUS: 12,0V ATIVO' : 'STATUS: DESENERGIZADO';
  if (st12vAt) {
    st12vAt.textContent = bus12vAt ? 'STATUS: 12,0V ENERGIZADO' : (estop ? 'STATUS: CORTADO (NR-12)' : 'STATUS: DESENERGIZADO');
    st12vAt.style.color = bus12vAt ? '#00e676' : '#ff1744';
  }
  if (st6v) {
    st6v.textContent = bus6v ? 'STATUS: 6,00V ESTÁVEL' : 'STATUS: DESENERGIZADO';
    st6v.style.color = bus6v ? '#00e676' : '#8fa699';
  }
  if (st5v) st5v.textContent = bus5v ? 'STATUS: 5,02V REGULADO' : 'STATUS: DESENERGIZADO';
}

// ========================================================
// INSPECTOR DRAWER (PAINEL INTERATIVO AO CLICAR)
// ========================================================
function inspectComponent(tag) {
  const data = INSPECTOR_DB[tag];
  if (!data) return;

  const drawer = document.getElementById('inspectorDrawer');
  const dTag = document.getElementById('drawerTag');
  const dTitle = document.getElementById('drawerTitle');
  const dFuncao = document.getElementById('drawerFuncao');
  const dEletrica = document.getElementById('drawerEletrica');
  const dChecklist = document.getElementById('drawerChecklist');

  if (dTag) dTag.textContent = data.tag;
  if (dTitle) dTitle.textContent = data.name;
  if (dFuncao) dFuncao.textContent = data.funcao;
  if (dEletrica) dEletrica.textContent = data.eletrica;

  if (dChecklist) {
    dChecklist.innerHTML = '';
    data.checklist.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      dChecklist.appendChild(li);
    });
  }

  if (drawer) drawer.classList.add('open');
}

function closeInspector() {
  const drawer = document.getElementById('inspectorDrawer');
  if (drawer) drawer.classList.remove('open');
}

// ========================================================
// NAVEGAÇÃO DE PRANCHAS (VISÃO 00 E FOLHAS 01 A 04)
// ========================================================
function switchSheet(sheetNum) {
  SimState.currentSheet = sheetNum;

  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach((tab, index) => {
    tab.classList.toggle('active', index === sheetNum);
  });

  const sheets = document.querySelectorAll('.sheet-container');
  sheets.forEach((sheet, index) => {
    sheet.classList.toggle('active', index === sheetNum);
  });

  resetZoom();
}

// Atalhos de teclado (0 a 4 e setas)
window.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === '0') switchSheet(0);
  if (e.key === '1') switchSheet(1);
  if (e.key === '2') switchSheet(2);
  if (e.key === '3') switchSheet(3);
  if (e.key === '4') switchSheet(4);
  if (e.key === 'ArrowRight' && SimState.currentSheet < 4) switchSheet(SimState.currentSheet + 1);
  if (e.key === 'ArrowLeft' && SimState.currentSheet > 0) switchSheet(SimState.currentSheet - 1);
});

// ========================================================
// CONTROLES REAIS DE ZOOM E PAN
// ========================================================
function applyTransform() {
  const activeContainer = document.querySelector('.sheet-container.active');
  if (activeContainer) {
    activeContainer.style.transform = 'translate(' + SimState.panX + 'px, ' + SimState.panY + 'px) scale(' + SimState.zoomLevel + ')';
  }
}

function zoomIn() {
  SimState.zoomLevel = Math.min(2.5, SimState.zoomLevel + 0.15);
  applyTransform();
}

function zoomOut() {
  SimState.zoomLevel = Math.max(0.6, SimState.zoomLevel - 0.15);
  applyTransform();
}

function resetZoom() {
  SimState.zoomLevel = 1.0;
  SimState.panX = 0;
  SimState.panY = 0;
  applyTransform();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Zoom com roda do mouse na viewport
document.addEventListener('DOMContentLoaded', () => {
  const viewport = document.querySelector('.cad-viewport');
  if (viewport) {
    viewport.addEventListener('wheel', (e) => {
      if (e.ctrlKey) {
        e.preventDefault();
        if (e.deltaY < 0) zoomIn();
        else zoomOut();
      }
    }, { passive: false });

    // Panning com clique e arraste
    viewport.addEventListener('mousedown', (e) => {
      if (e.button === 0 && (e.target.tagName === 'svg' || e.target.classList.contains('cad-viewport') || e.target.classList.contains('cad-border'))) {
        SimState.isPanning = true;
        SimState.startX = e.clientX - SimState.panX;
        SimState.startY = e.clientY - SimState.panY;
        viewport.style.cursor = 'grabbing';
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (!SimState.isPanning) return;
      SimState.panX = e.clientX - SimState.startX;
      SimState.panY = e.clientY - SimState.startY;
      applyTransform();
    });

    window.addEventListener('mouseup', () => {
      if (SimState.isPanning) {
        SimState.isPanning = false;
        viewport.style.cursor = 'default';
      }
    });
  }
});

// ========================================================
// IMPRESSÃO E TEMA
// ========================================================
function printBlueprint() {
  window.print();
}

function printAllSheets() {
  const sheets = document.querySelectorAll('.sheet-container');
  sheets.forEach(s => s.style.display = 'block');
  window.print();
  setTimeout(() => {
    sheets.forEach((s, idx) => {
      s.style.display = (idx === SimState.currentSheet) ? 'block' : 'none';
    });
  }, 1000);
}

function toggleTheme() {
  SimState.theme = (SimState.theme === 'dark') ? 'light' : 'dark';
  document.body.classList.toggle('theme-light', SimState.theme === 'light');
  const btnTheme = document.getElementById('btnTheme');
  if (btnTheme) {
    btnTheme.textContent = SimState.theme === 'light' ? '🌙 Modo Escuro' : '🌓 Modo Claro';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateSimulationUI();
});

