# GUIA DE IMPRESSÃO 3D INDUSTRIAL — FILA DE PRODUÇÃO: RICLEY
## PROJETO AMAZONVISION 4.0 · ESTEIRA SELETORA 700 MM
**Impressora Alvo:** Bambu Lab P2S (Volume Útil: $256 \times 256 \times 256\text{ mm}$)  
**Responsável Operacional:** Ricley  
**Data de Emissão:** 06 de Novembro de 2026  
**Status da Auditoria:** 100% Homologado e Auditado (Arquivos STL Manifold / Watertight / Z=0.00 mm)

---

> [!IMPORTANT]
> **Revisão LT-3D-002 (06/11/2026, noite) — leia antes de imprimir.**
> - Os arquivos **01** (cabeceiras + carros tensores) e **03** (tambores) foram **regerados**. Se você já fatiou a versão das 10:40, descarte e fatie de novo.
> - **03** agora tem **3 corpos**: tambor motriz, tambor livre e rolete, todos com 118 mm. As polias impressas saíram; as polias GT2 serão **comerciais** (20T furo 6 mm e 40T furo 8 mm).
> - **01**: os 2 "mancais 02D" agora são **carros tensores** com porca M5 cativa (a porca entra por cima, antes da montagem).
> - Novo arquivo **09**: um 6º lote de elos. A correia precisa de **91 elos** (passo real 16,51 mm), e com 6 lotes sobram 17 de reserva.
> - Ordem sugerida: 04, 05, 06, 09 (elos), 08 (TPU), 07, 02 e por último 01 e 03.

### 1. RESUMO EXECUTIVO DA SUA CARGA DE TRABALHO
Você é o responsável por imprimir a **espinha dorsal estrutural e o sistema de tração primário** da esteira, além de **3 dos 5 lotes de elos da correia modular**.

- **Total de Arquivos / Execuções de Impressão:** 9 pratos de impressão
- **Massa Fatiada Total Estimada:** **≈ 1.208 g** (estimativa do script; confirme no Bambu Studio)
- **Tempo Estimado na Bambu P2S (Modo Standard 100%):** ~24h 50m *(estimativa; confirme no Bambu Studio)*
- **Materiais Necessários:**
  - **PETG Preto:** 1 rolo (consumo ~430 g)
  - **PETG Laranja:** 1 rolo (consumo ~575 g)
  - **PETG Verde:** consumo ~83 g *(ou PETG Laranja para a caixa de aprovados)*
  - **TPU 95A Flexível:** consumo ~20,5 g

---

### 2. FILA DE IMPRESSÃO SEQUENCIAL (ORDEM RECOMENDADA)

Siga exatamente a ordem numérica dos arquivos contidos nesta pasta:

| Seq. | Arquivo STL no Disco | Peças Contidas | Qtd Corpos | Material & Cor | Tempo Est. | Massa (g) | Perfil Bambu Studio |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **01** | `01_Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl` | 4x Cabeceiras (`01A`–`01D`) + 2x Carros tensores (`02D`, porca M5 cativa) — **rev. LT-3D-002** | 6 | **PETG Preto** | 4h 30m | 234,4 g | **5 paredes**, 22% Gyroid, 4 topo/base |
| **02** | `02_Mesa_04_Chassi_1x_Mesa_8x_Pes_4x_Travessas.stl` | 1x Mesa vazada (`01G3`) + 8x Pés perfil H (`01K`) + 4x Travessas (`01H`) | 13 | **PETG Preto** | 3h 50m | 191,5 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **03** | `03_Mesa_05_Tambores_Motriz_Livre_e_Polias_GT2.stl` | Tambor motriz D60 (preso no eixo por 2 parafusos sem cabeça M3) + Tambor livre D60 + Rolete D50, todos 118 mm — **rev. LT-3D-002** | **3** | **PETG Laranja / Preto** | 4h 40m | 213,3 g | 4 paredes, 25% Gyroid, Brim 5mm |
| **04** | `04_Mesa_06_Elos_Correia_18x_Lote_1de3.stl` | 18 elos modulares 122 mm (Lote 1 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **05** | `05_Mesa_06_Elos_Correia_18x_Lote_2de3.stl` | 18 elos modulares 122 mm (Lote 2 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **06** | `06_Mesa_06_Elos_Correia_18x_Lote_3de3.stl` | 18 elos modulares 122 mm (Lote 3 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **07** | `07_Mesa_11_Caixa_Coletora_Aprovados_152mm.stl` | 1x Caixa Coletora Aprovados $152 \times 152 \times 55\text{ mm}$ | 1 | **PETG Verde** *(ou Laranja)* | 1h 50m | 83,1 g | 3 paredes, 20% Gyroid, 4 topo/base |
| **08** | `08_Mesa_13_Lote_8x_Sapatas_Pes_TPU_95A.stl` | 8x Sapatas antivibração para os pés estruturais | 8 | **TPU 95A** | 1h 00m | 20,5 g | 3 paredes, 22% Gyroid, vel. 30 mm/s |
| **09** | `09_Mesa_06_Elos_Correia_18x_Lote_Extra.stl` | 18 elos modulares 122 mm (6º lote, reserva) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |

> [!NOTE]
> Itens 04, 05, 06 e 09 = **72 elos**. Com os **36** do Diego, ficam **108 elos**. A correia usa **91** (passo real 16,51 mm, tambor de 12 dentes, entre-centros de 652 mm) e sobram 17 de reserva. Os "86 + 4" da versão anterior estavam errados.

---

### 3. CONFIGURAÇÕES ESPECÍFICAS DE FATIAMENTO NO BAMBU STUDIO / ORCASLICER

#### A. Parâmetros Globais para PETG (Arquivos 01 a 07):
- **Bico (*Nozzle*):** 0.4 mm Stainless / Hardened Steel.
- **Mesa (*Build Plate*):** Textured PEI Plate.
- **Altura de Camada (*Layer Height*):** 0.20 mm Standard (primeira camada 0.20 mm).
- **Temperaturas:** Nozzle: 245 °C (primeira camada 250 °C) | Mesa: 75 °C (todas as camadas).
- **Ventoinha de Resfriamento:** 20% a 50% (para garantir máxima adesão entre camadas e resistência mecânica).
- **Compensação Dimensional:** X-Y Hole Compensation: `+0.05 mm` (garante que os furos M4 e M5 entrem sem necessidade de retífica manual).

#### B. Atenção Especial no Arquivo 03 (`03_Mesa_05_Tambores_Motriz_Livre_e_Polias_GT2.stl`):
- Como os tambores são cilíndricos e altos ($137{,}6\text{ mm}$), ative **Brim Externo de 5 mm** (*Outer Brim Only*) para ancorar firmemente as peças na mesa e evitar qualquer descolamento por alavanca térmica.
- As cavidades internas foram desenhadas com **teto cônico a 45°**, portanto **NÃO precisa de suporte interno**.

#### C. Parâmetros Específicos para TPU 95A (Arquivo 08):
- **Desative o AMS:** O filamento TPU flexível deve ser alimentado pelo carretel traseiro direto (ou suporte externo).
- **Velocidade de Impressão:** Reduza para **30 mm/s** em todas as linhas (perímetros e preenchimento).
- **Retração:** Distância de retração máxima de **1.0 mm** (ou desative a retração para não engasgar o extrusor).
- **Temperatura:** Nozzle 230 °C | Mesa 40 °C.

---

### 4. DICAS DE PÓS-PROCESSAMENTO E MONTAGEM
1. **Limpeza das Peças:** Remova os fiapos (*stringing*) eventuais do PETG com ar quente rápido de um soprador térmico ou isqueiro por 1 segundo.
2. **Elos da Correia:** Teste a articulação dos elos passando um pedaço de filamento PETG 1.75 mm pelo furo da dobradiça. O pino deve entrar justo e articular livremente.
3. **Mancais das Cabeceiras (Arquivo 01):** As sedes das cabeceiras dianteiras `01A`/`01B` recebem as buchas 608 impressas pelo Diego, sob leve pressão manual, com o rebaixo voltado para **dentro** do chassi. O eixo dianteiro gira nelas, e o tambor motriz fica preso no eixo.
4. **Carros tensores (Arquivo 01):** encaixe a porca M5 por cima, no rasgo do carro, antes de montar. O carro entra no rasgo da `01C`/`01D` com a aba do lado de **fora**. O parafuso **M5×50** entra pela ponta da cabeceira e, ao apertar, puxa o carro para fora e estica a correia (curso de 26 mm).
5. **Tambores (Arquivo 03):** no motriz, encaixe 1 porca M3 em cada fenda das pontas e rosqueie um parafuso sem cabeça M3×6 pelo furo radial (chave Allen 1,5 mm). Tambor livre e rolete: 1 bucha 608 em cada ponta. O furo central de Ø9 é folga de propósito: só as buchas tocam o eixo.
