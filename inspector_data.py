# -*- coding: utf-8 -*-
"""
Database of electrical components for the Interactive Inspector Drawer
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
Arquitetura Simplificada Mono-Fonte 12V DC (Mono-PS1)
"""

INSPECTOR_DB = {
    "PS1": {
        "tag": "PS1",
        "name": "Fonte Chaveada Colmeia 12V 10A (120W) — MONO-FONTE PRINCIPAL",
        "model": "Mean Well LRS-120-12 (ou equivalente industrial 12V 10A)",
        "funcao": "Única fonte primária de alimentação de toda a bancada industrial (Arquitetura Mono-Fonte 12V). Alimenta diretamente o motorredutor da esteira (12V), a luminária Ring Light (12V) e o relé de segurança K1 (12V). Também supre os conversores Buck U2 (rebaixando para 6,0V p/ servo MG996R) e U4 (rebaixando para 5,0V p/ ESP32 e sensores ópticos IR retangulares (5V NPN)).",
        "funcao_publico": "Fonte de energia principal da esteira. Transforma a energia da tomada (110/220V) em 12V para alimentar o motor, as luzes e todos os circuitos da bancada.",
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
        "funcao_publico": "Chave de protecao geral. Se houver um curto-circuito, ele desliga tudo automaticamente para evitar danos.",
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
        "funcao_publico": "Filtro e chave liga/desliga da bancada. Limpa a energia da tomada de interferencias antes de alimentar o sistema.",
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
        "funcao_publico": "Fusivel de protecao. Se passar corrente demais, ele queima e desliga o circuito para proteger os componentes.",
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
        "funcao_publico": "Protetor contra raios e picos de energia. Se a rede eletrica da feira sofrer uma descarga, ele desvia a energia perigosa para o terra e protege a fonte.",
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
        "funcao_publico": "Botao vermelho de emergencia. Ao pressionar, corta instantaneamente a energia do motor e do empurrador para proteger o operador. Norma NR-12.",
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
        "funcao_publico": "Rele de seguranca. Funciona como um interruptor automatico que liga ou corta a energia do motor e do empurrador quando o botao de emergencia e acionado.",
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
        "funcao_publico": "Cerebro da esteira. Este microcontrolador le os sensores, controla o motor e o empurrador, e conversa com o computador que faz a inteligencia artificial.",
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
        "funcao_publico": "Conversor de tensao para o empurrador. Reduz os 12V da bancada para 6V, que e a tensao ideal para o servo-motor que empurra as frutas rejeitadas.",
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
        "funcao": "Alimenta localmente o microcontrolador ESP32 DevKit V1 e os dois sensores ópticos IR retangulares (5V NPN) com 5,0V limpos e estabilizados a partir do barramento contínuo de 12V (+12V_CONT).",
        "funcao_publico": "Conversor de tensao para o cerebro. Reduz os 12V da fonte para 5V limpos que alimentam o microcontrolador ESP32 e os dois sensores opticos.",
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
        "funcao_publico": "Interruptor eletronico de potencia do motor. Recebe o comando do microcontrolador e liga ou desliga o motor da esteira sem partes mecanicas moveis.",
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
        "funcao_publico": "Motor da esteira. Gira o rolo que movimenta a correia transportadora, levando as frutas (tucuma e castanha) ate a camera e o empurrador.",
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
        "funcao_publico": "Empurrador de frutas ruins. Quando a inteligencia artificial detecta uma fruta defeituosa, este braco mecanico empurra ela para fora da esteira.",
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
        "funcao_publico": "Sensor da camera. Detecta quando a fruta esta chegando e avisa o sistema para tirar a foto usada pela inteligencia artificial.",
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
        "funcao_publico": "Sensor do empurrador. Detecta a fruta defeituosa chegando e avisa o sistema para acionar o empurrador e remove-la da esteira.",
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
        "funcao_publico": "Sensor da camera. Detecta quando a fruta esta chegando e avisa o sistema para tirar a foto usada pela inteligencia artificial.",
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
        "funcao_publico": "Sensor do empurrador. Detecta a fruta defeituosa chegando e avisa o sistema para acionar o empurrador e remove-la da esteira.",
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
        "funcao_publico": "Regua de conexoes principal. Organiza todos os fios de energia em um unico lugar seguro, como uma regua de tomadas industrial.",
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
        "funcao_publico": "Regua de conexoes dos sensores. Liga os dois sensores opticos e o botao de emergencia ao painel de forma organizada e segura.",
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
        "funcao_publico": "Regua de conexoes dos atuadores. Liga o motor da esteira, o empurrador e a luz da camera ao painel eletrico.",
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
        "funcao_publico": "Diodo protetor do microcontrolador. Impede que a tensao de 5V dos sensores queime a entrada do ESP32, que so suporta 3,3V.",
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
        "funcao_publico": "Resistor de protecao. Limita a corrente eletrica que chega ao diodo protetor e ao microcontrolador, evitando que os componentes esquentem.",
        "eletrica": "Resistência: 1,00 kΩ ±1% | Potência nominal: 0,25W (1/4W) | Coeficiente térmico: ±50 ppm/°C | Tensão máxima de trabalho: 250V.",
        "checklist": [
            "Terminal de Entrada: Conectar ao borne de sinal BK do sensor (X2:3 para S1 ou X2:6 para S2).",
            "Terminal de Saída: Conectar ao pino 3 do diodo duplo BAT54S e à respectiva GPIO do ESP32 (GPIO 25 para S1 / GPIO 26 para S2)."
        ]
    }
}
