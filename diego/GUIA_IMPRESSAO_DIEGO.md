# GUIA DE IMPRESSÃO 3D INDUSTRIAL — FILA DE PRODUÇÃO: DIEGO
## PROJETO AMAZONVISION 4.0 · ESTEIRA SELETORA 700 MM
**Impressora Alvo:** Bambu Lab P2S (Volume Útil: $256 \times 256 \times 256\text{ mm}$)  
**Responsável Operacional:** Diego  
**Data de Emissão:** 06 de Novembro de 2026  
**Status da Auditoria:** 100% Homologado e Auditado (Arquivos STL Manifold / Watertight / Z=0.00 mm)

---

> [!IMPORTANT]
> **Revisão LT-3D-002 (06/11/2026, noite) — leia antes de imprimir.**
> - Os arquivos **01** (extensões e guias) e **05** (acionamento e empurrador) foram **regerados**. Se você já fatiou a versão das 10:40, descarte e fatie de novo.
> - **01**: a guia `01J` tem agora recorte de **108 mm** para a sapata passar com folga.
> - **05**: suporte do GA37 com furação corrigida (círculo Ø31), pórtico com furo Ø7 entre as buchas, sapata `03H` e trave `03I` refeitas (hastes na direção do empurrão, pivô vertical). **Ainda pendente:** a furação do horn na alavanca `03F` depende da medida do horn metálico real.
> - **Buchas 608:** a montagem nova usa **6** (2 nas cabeceiras dianteiras, 2 no tambor livre, 2 no rolete). A Mesa 14 tem 4, então imprima também **2×** `Kit_Impressao_3D_Esteira_AmazonVision/07_Fixacoes_e_Acessorios/Bucha_608_Substituta_Rolamento_Tambor_8x22x7mm.stl` com o mesmo perfil da Mesa 14.
> - Ordem sugerida: 11 (1 bucha de teste primeiro), 03, 04, 02, 06, 08, 09, 10, 07 (cúpula de cabeça para baixo) e por último 01 e 05.

### 1. RESUMO EXECUTIVO DA SUA CARGA DE TRABALHO
Você é o responsável por imprimir as **extensões do chassi, mesas deslizantes, o sistema cinemático do empurrador biela-manivela, a estação de visão óptica com cúpula, a rampa de descarte, os acessórios de fixação, 2 lotes da correia modular** e o componente crítico de contingência: o **Lote de Buchas Deslizantes Autolubrificadas (Mesa 14)** que substitui 100% dos rolamentos comerciais (caso não encontrados em Manaus).

- **Total de Arquivos / Execuções de Impressão:** 11 pratos de impressão
- **Massa Fatiada Total Estimada:** **≈ 1.200 g** + 2 buchas avulsas (estimativa do script; confirme no Bambu Studio)
- **Tempo Estimado na Bambu P2S (Modo Standard 100%):** ~26h 20m *(a soma das linhas abaixo; a versão anterior dizia 23h05 por erro de soma)*
- **Materiais Necessários:**
  - **PETG Preto:** 1 rolo (consumo ~600 g)
  - **PETG Laranja / Amarelo:** 1 rolo (consumo ~590 g)
  - **PLA Branco Leitoso:** consumo ~15 g (para difusor Ring Light e plaquetas de texto)

---

### 2. FILA DE IMPRESSÃO SEQUENCIAL (ORDEM RECOMENDADA)

Siga exatamente a ordem numérica dos arquivos contidos nesta pasta:

| Seq. | Arquivo STL no Disco | Peças Contidas | Qtd Corpos | Material & Cor | Tempo Est. | Massa (g) | Perfil Bambu Studio |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **01** | `01_Mesa_02_Chassi_6x_Extensoes_e_6x_Guias.stl` | 4x Extensões padrão (`01E`) + 2x Centrais (`01F`) + 6x Guias (`01I`, `01J` com recorte 108 mm) — **rev. LT-3D-002** | 12 | **PETG Preto** | 4h 15m | 224,0 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **02** | `02_Mesa_03_Chassi_2x_Mesas_Deslizantes_01G.stl` | 2x Mesas deslizantes vazadas BedPlate (Pares 1 e 2) | 2 | **PETG Preto** | 1h 45m | 64,8 g | 3 paredes, 25% Gyroid, 4 topo/base |
| **03** | `03_Mesa_06_Elos_Correia_18x_Lote_1de2.stl` | 18 elos modulares 122 mm (Lote 1 de 2) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **04** | `04_Mesa_06_Elos_Correia_18x_Lote_2de2.stl` | 18 elos modulares 122 mm (Lote 2 de 2) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **05** | `05_Mesa_07_Acionamento_GA37_e_Empurrador_MG996R.stl` | Suporte GA37 (`03A`), Guarda-correia, Pórtico 4x LM6UU (`03E`), Biela L110, Sapata R45, Trave — **rev. LT-3D-002** | 8 | **PETG Laranja/Preto** | 3h 40m | 161,8 g | **5 paredes**, 25% Gyroid, **sem suporte** (furos Ø12 fecham em ponte; alargar depois com broca 12) |
| **06** | `06_Mesa_08_Sensores_Clipes_e_Suportes_DIN.stl` | 2x Suportes sensor retangular (`04A`) + 4x Suportes DIN + 12x Clipes + 18x Espaçadores | 38 | **PETG Preto / Cinza** | 3h 30m | 164,0 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **07** | `07_Mesa_09_Cupula_Webcam_e_RingLight.stl` | Cúpula óptica 146mm, Suporte Ring Light, Moldura acrílico, Caixa webcam | 5 | **PETG Preto Fosco** | 3h 10m | 147,4 g | 3 paredes, 20% Gyroid, Zero suporte portais |
| **08** | `08_Mesa_10_Rampa_Descarte_18graus_e_Caixa_NR12.stl` | Rampa descarte 18° + Caixa botoeira emergência NR-12 + Tampa Ø22,5mm | 3 | **PETG Laranja/Amarelo** | 2h 20m | 98,4 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **09** | `09_Mesa_11_Caixa_Coletora_Rejeitados_152mm.stl` | 1x Caixa Coletora Rejeitados $152 \times 152 \times 55\text{ mm}$ | 1 | **PETG Laranja** | 1h 50m | 83,1 g | 3 paredes, 20% Gyroid, 4 topo/base |
| **10** | `10_Mesa_12_Difusor_Optico_e_Plaquetas_PLA.stl` | Difusor óptico leitoso 1mm + Plaqueta Aprovados + Plaqueta Rejeitados | 3 | **PLA Branco Leitoso** | 0h 40m | 15,1 g | 2 paredes, 100% Sólido concêntrico |
| **11** | `11_Mesa_14_Lote_10x_Buchas_Deslizantes_Rolamentos.stl` | **LOTE CRÍTICO: 4x Buchas 608 + 4x Buchas LM6UU + 2x Buchas 623** | 10 | **PETG Preto/Laranja** | 0h 25m | 8,9 g *(15 g sólido)* | 4 paredes, 100% Infill, Ironing ligado |

> [!NOTE]
> Os seus **36 elos** (itens 03 e 04) unidos aos **54 elos** impressos pelo Ricley somam exatamente os **90 elos modulares** do circuito da esteira de 700 mm.

---

### 3. PROTOCOLO ESPECIAL: MESA 14 (BUCHAS EM SUBSTITUIÇÃO A ROLAMENTOS)

Como Manaus apresenta escassez crítica de rolamentos industriais à pronta-entrega, a **Mesa 14** contém o lote completo de buchas autolubrificadas projetadas segundo normas DfAM e tribologia de polímeros:

1. **4× Buchas 608 na Mesa 14 + 2× avulsas = 6 (Substitui Rolamento 608ZZ de 8×22×7 mm):**
   - **Onde vai (rev. LT-3D-002):** 2 nas cabeceiras dianteiras `01A`/`01B` (o eixo motriz gira nelas), 2 no tambor livre traseiro e 2 no rolete central (os dois giram sobre eixo fixo).
   - **Geometria:** $\varnothing_{\text{ext}} = 22{,}0\text{ mm}$, $\varnothing_{\text{int}} = 8{,}25\text{ mm}$ (folga diametral $+0{,}25\text{ mm}$ calculada para rotação macia sem aperto térmico), altura $7{,}0\text{ mm}$ com canal anelar interno de graxa.
2. **4× Buchas LM6UU (Substitui Rolamento Linear LM6UU de 12×19 mm):**
   - **Onde vai:** No pórtico móvel `03E` do empurrador da maçã (deslizam nas 2 hastes retificadas inox $\varnothing 6\text{ mm}$).
   - **Geometria:** $\varnothing_{\text{ext}} = 12{,}0\text{ mm}$, $\varnothing_{\text{int}} = 6{,}20\text{ mm}$ (folga diametral $+0{,}20\text{ mm}$), comprimento $19{,}0\text{ mm}$ com 2 canais internos de lubrificação.
3. **2× Buchas 623 (Substitui Rolamento 623ZZ de 3×10×4 mm):**
   - **Onde vai:** Na articulação da biela `03G` com a sapata e alavanca do servo MG996R.
   - **Geometria:** $\varnothing_{\text{ext}} = 10{,}0\text{ mm}$, $\varnothing_{\text{int}} = 3{,}20\text{ mm}$ (passagem livre para o parafuso M3), altura $4{,}0\text{ mm}$.

#### Teste obrigatório antes do lote:
Imprima **1 bucha 608 sozinha** e passe o eixo Ø8. Se travar, aumente a compensação de furo X-Y em +0,05 mm e repita (faixa típica: +0,05 a +0,15). Se ficar um pouco justa, passe uma broca de 8,2 mm à mão. Use também compensação de pé de elefante de 0,15 mm.

#### Como fatiar a Mesa 14 para obter qualidade de injeção:
- **Preenchimento (*Infill*):** **100% Sólido** (perímetros concêntricos ou alinhados).
- **Alisamento de Topo (*Ironing*):** Ativado na camada de topo para as faces ficarem espelhadas.
- **Altura de Camada:** 0.16 mm Optimal (para reduzir o efeito degrau cilíndrico interno).
- **Lubrificação na Montagem:** Pingar **1 gota de óleo mineral Singer (óleo de máquina)** ou aplicar uma leve película de **vaselina sólida/pasta de silicone** dentro de cada bucha. A esteira rodará com ruído zero e atrito insignificante (fator $P \cdot v < 1\%$ do limite do PETG).

---

### 4. CONFIGURAÇÕES ESPECÍFICAS DE FATIAMENTO NO BAMBU STUDIO / ORCASLICER

#### A. Parâmetros Globais para PETG (Arquivos 01 a 09, e 11):
- **Bico (*Nozzle*):** 0.4 mm Stainless / Hardened Steel.
- **Mesa (*Build Plate*):** Textured PEI Plate.
- **Altura de Camada:** 0.20 mm Standard.
- **Temperaturas:** Nozzle: 245 °C | Mesa: 75 °C.
- **Ventoinha:** 20% a 50% (ponte e balanço ≥ 80%).
- **Compensação Dimensional:** X-Y Hole Compensation `+0.05 mm` e Elephant Foot `0.15 mm` (igual ao Ricley).
- **Umidade:** seque o PETG a 65 °C por 6–8 h antes (Manaus ~80% de umidade).

#### B. Parâmetros para PLA Branco Leitoso (Arquivo 10 - Difusor e Plaquetas):
- **Temperatura:** Nozzle 220 °C | Mesa 55 °C.
- **Troca de Cor Manual nas Plaquetas (Opcional):**
  - As plaquetas de texto `06C` e `06D` têm as letras em relevo de $Z = 2{,}5$ a $3{,}5\text{ mm}$ (medido na malha).
  - Para letras pretas em fundo branco, adicione uma **Pausa na Camada** na camada que começa em $Z = 2{,}5\text{ mm}$ e troque o filamento para preto.
  - Imprima as plaquetas num prato **separado do difusor**. Senão o aro do difusor (5 mm de altura) também fica preto acima de 2,5 mm.
