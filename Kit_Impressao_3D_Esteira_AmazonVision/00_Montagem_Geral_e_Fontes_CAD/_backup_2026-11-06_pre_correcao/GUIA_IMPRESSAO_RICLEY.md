# GUIA DE IMPRESSÃO 3D INDUSTRIAL — FILA DE PRODUÇÃO: RICLEY
## PROJETO AMAZONVISION 4.0 · ESTEIRA SELETORA 700 MM
**Impressora Alvo:** Bambu Lab P2S (Volume Útil: $256 \times 256 \times 256\text{ mm}$)  
**Responsável Operacional:** Ricley  
**Data de Emissão:** 06 de Novembro de 2026  
**Status da Auditoria:** 100% Homologado e Auditado (Arquivos STL Manifold / Watertight / Z=0.00 mm)

---

### 1. RESUMO EXECUTIVO DA SUA CARGA DE TRABALHO
Você é o responsável por imprimir a **espinha dorsal estrutural e o sistema de tração primário** da esteira, além de **3 dos 5 lotes de elos da correia modular**.

- **Total de Arquivos / Execuções de Impressão:** 8 pratos de impressão
- **Massa Fatiada Total Estimada:** **$1.108{,}8\text{ g}$** (~1,11 kg)
- **Tempo Estimado na Bambu P2S (Modo Standard 100%):** ~22h 35m *(ou ~16h se utilizar o Modo Sport a 125%)*
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
| **01** | `01_Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl` | 4x Cabeceiras (`01A`–`01D`) + 2x Mancais tensores (`02D`) | 6 | **PETG Preto** | 4h 30m | 238,3 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **02** | `02_Mesa_04_Chassi_1x_Mesa_8x_Pes_4x_Travessas.stl` | 1x Mesa vazada (`01G3`) + 8x Pés perfil H (`01K`) + 4x Travessas (`01H`) | 13 | **PETG Preto** | 3h 50m | 191,5 g | 3 paredes, 22% Gyroid, 4 topo/base |
| **03** | `03_Mesa_05_Tambores_Motriz_Livre_e_Polias_GT2.stl` | Tambor motriz D60 + Tambor livre D60 + Rolete D50 + Polia 40T + Polia 20T | 5 | **PETG Laranja / Preto** | 4h 40m | 226,5 g | 4 paredes, 25% Gyroid, Brim 5mm |
| **04** | `04_Mesa_06_Elos_Correia_18x_Lote_1de3.stl` | 18 elos modulares 122 mm (Lote 1 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **05** | `05_Mesa_06_Elos_Correia_18x_Lote_2de3.stl` | 18 elos modulares 122 mm (Lote 2 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **06** | `06_Mesa_06_Elos_Correia_18x_Lote_3de3.stl` | 18 elos modulares 122 mm (Lote 3 de 3) | 18 | **PETG Laranja** | 2h 15m | 116,3 g | 3 paredes, 30% Gyroid, 4 topo/base |
| **07** | `07_Mesa_11_Caixa_Coletora_Aprovados_152mm.stl` | 1x Caixa Coletora Aprovados $152 \times 152 \times 55\text{ mm}$ | 1 | **PETG Verde** *(ou Laranja)* | 1h 50m | 83,1 g | 3 paredes, 20% Gyroid, 4 topo/base |
| **08** | `08_Mesa_13_Lote_8x_Sapatas_Pes_TPU_95A.stl` | 8x Sapatas antivibração para os pés estruturais | 8 | **TPU 95A** | 1h 00m | 20,5 g | 3 paredes, 22% Gyroid, vel. 30 mm/s |

> [!NOTE]
> Ao finalizar os itens 04, 05 e 06, você terá produzido **54 elos da correia modular**. O Diego imprimirá os outros **36 elos** (2 lotes), somando exatamente os **90 elos** necessários para fechar a esteira de 700 mm (86 elos úteis + 4 sobressalentes).

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
3. **Mancais das Cabeceiras (Arquivo 01):** As sedes cilíndricas receberão as buchas autolubrificadas 608 impressas pelo Diego. Elas devem entrar sob leve pressão manual.
