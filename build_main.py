# -*- coding: utf-8 -*-
"""
Master Builder for Planta_Eletrica_Esteira_AmazonVision.html
AmazonVision 4.0 - XXI Feira Tecnológica FUCAPI 2026
"""

import sys
import os

from css_styles import get_css
from light_mode_map import build_light_overrides
from make_blueprint_html import get_header_and_toolbar
from sheet_overview import get_sheet_overview
from sheet_1 import get_sheet_1
from sheet_2 import get_sheet_2
from sheet_3 import get_sheet_3
from sheet_4 import get_sheet_4
from app_js import get_app_js

def build():
    print("Iniciando a compilacao do Caderno de Projeto e Planta Eletrica...")

    css = get_css()
    header_html = get_header_and_toolbar()
    s0_svg = get_sheet_overview()
    s1_svg = get_sheet_1()
    s2_svg = get_sheet_2()
    s3_svg = get_sheet_3()
    s4_svg = get_sheet_4()
    js = get_app_js()

    # As cores claras das folhas sao derivadas do markup real, nao escritas a mao.
    css += "\n" + build_light_overrides(s0_svg + s1_svg + s2_svg + s3_svg + s4_svg)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AmazonVision 4.0 &mdash; Planta Eletrica Industrial &amp; Caderno de Projeto</title>
  <style>
{css}
  </style>
</head>
<!-- theme-light e fixo: a paleta clara e uma camada sobre a escura e esta
     classe e o que a ativa. Nao ha alternancia de tema neste documento. -->
<body class="theme-light">

{header_html}

<main class="cad-viewport">
  <!-- VISAO 00: BANCADA FISICA & GUIA DE LIGACAO -->
  <div class="sheet-container active" id="sheetContainer0">
    <svg class="blueprint-svg" viewBox="0 0 1700 980" xmlns="http://www.w3.org/2000/svg">
{s0_svg}
    </svg>
  </div>

  <!-- FOLHA 01: DISTRIBUICAO E NR-12 -->
  <div class="sheet-container" id="sheetContainer1">
    <svg class="blueprint-svg" viewBox="0 0 1700 980" xmlns="http://www.w3.org/2000/svg">
{s1_svg}
    </svg>
  </div>

  <!-- FOLHA 02: ATUADORES M1 E M2 -->
  <div class="sheet-container" id="sheetContainer2">
    <svg class="blueprint-svg" viewBox="0 0 1700 980" xmlns="http://www.w3.org/2000/svg">
{s2_svg}
    </svg>
  </div>

  <!-- FOLHA 03: SENSORES E ESP32 -->
  <div class="sheet-container" id="sheetContainer3">
    <svg class="blueprint-svg" viewBox="0 0 1700 980" xmlns="http://www.w3.org/2000/svg">
{s3_svg}
    </svg>
  </div>

  <!-- FOLHA 04: BORNES, CABOS E BOM -->
  <div class="sheet-container" id="sheetContainer4">
    <svg class="blueprint-svg" viewBox="0 0 1700 980" xmlns="http://www.w3.org/2000/svg">
{s4_svg}
    </svg>
  </div>
</main>

</div><!-- end .app-shell -->

<script>
{js}
</script>

</body>
</html>
"""

    output_path = os.path.join(os.path.dirname(__file__), "Planta_Eletrica_Esteira_AmazonVision.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Sucesso! Arquivo gerado em: {output_path}")
    print(f"Tamanho do arquivo gerado: {os.path.getsize(output_path)} bytes")

if __name__ == '__main__':
    build()
