# -*- coding: utf-8 -*-
"""
Engineering Frame and Title Block (Carimbo) per IEC / ABNT Standards
"""

def get_cad_frame(sheet_num, sheet_title, sheet_subtitle, dwg_code="PE-AV4-2026"):
    # SVG Dimensions: 1700 x 980
    # Outer border: 20, 20, 1660, 940
    # Inner border: 35, 35, 1630, 910
    
    # Columns 1 to 8 markers
    col_x = [135, 335, 535, 735, 935, 1135, 1335, 1535]
    row_y = [110, 255, 400, 545, 690, 835]
    row_lbl = ['A', 'B', 'C', 'D', 'E', 'F']
    
    col_markers = ""
    for i, x in enumerate(col_x):
        col_markers += f'<text x="{x}" y="30" class="cad-grid-text" text-anchor="middle">{i+1}</text>\n'
        col_markers += f'<text x="{x}" y="955" class="cad-grid-text" text-anchor="middle">{i+1}</text>\n'
        col_markers += f'<line x1="{x}" y1="20" x2="{x}" y2="35" class="cad-inner-border"/>\n'
        col_markers += f'<line x1="{x}" y1="945" x2="{x}" y2="960" class="cad-inner-border"/>\n'
        
    row_markers = ""
    for i, y in enumerate(row_y):
        lbl = row_lbl[i]
        row_markers += f'<text x="28" y="{y+4}" class="cad-grid-text" text-anchor="middle">{lbl}</text>\n'
        row_markers += f'<text x="1672" y="{y+4}" class="cad-grid-text" text-anchor="middle">{lbl}</text>\n'
        row_markers += f'<line x1="20" y1="{y}" x2="35" y2="{y}" class="cad-inner-border"/>\n'
        row_markers += f'<line x1="1665" y1="{y}" x2="1680" y2="{y}" class="cad-inner-border"/>\n'

    # Title Block (Carimbo) at bottom-right corner: x=1080, y=825, w=585, h=120
    carimbo = f"""
    <!-- Carimbo de Engenharia Oficial -->
    <g id="carimbo_s{sheet_num}" transform="translate(1080, 825)">
      <!-- Fundo do Carimbo -->
      <rect x="0" y="0" width="585" height="120" class="cad-title-block"/>
      
      <!-- Divisões do Carimbo -->
      <line x1="0" y1="35" x2="585" y2="35" class="cad-title-line"/>
      <line x1="0" y1="75" x2="585" y2="75" class="cad-title-line"/>
      <line x1="380" y1="0" x2="380" y2="120" class="cad-title-line"/>
      <line x1="480" y1="75" x2="480" y2="120" class="cad-title-line"/>
      
      <!-- Linha 1: Instituição e Evento -->
      <text x="12" y="16" font-family="var(--font-mono)" font-size="9" fill="#00e5ff" font-weight="700">FUCAPI — FUNDAÇÃO CENTRO DE ANÁLISE, PESQUISA E INOVAÇÃO TECNOLÓGICA</text>
      <text x="12" y="28" font-family="var(--font-sans)" font-size="10" fill="#a0b8aa" font-weight="600">XXI FEIRA TECNOLÓGICA FUCAPI 2026 — AUTOMAÇÃO INDUSTRIAL 4.0</text>
      
      <!-- Logo/Identificador do Projeto -->
      <text x="390" y="18" font-family="var(--font-mono)" font-size="9" fill="#88a395">DOCUMENTO N°:</text>
      <text x="390" y="30" font-family="var(--font-mono)" font-size="11" fill="#fff" font-weight="700">{dwg_code}-FL{sheet_num:02d}</text>

      <!-- Linha 2: Título do Projeto e da Prancha -->
      <text x="12" y="48" font-family="var(--font-mono)" font-size="9" fill="#00e676" font-weight="700">PROJETO: AMAZONVISION 4.0 — ESTEIRA SELETORA INTELIGENTE</text>
      <text x="12" y="65" font-family="var(--font-sans)" font-size="13" fill="#ffffff" font-weight="700">{sheet_title}</text>
      
      <text x="390" y="50" font-family="var(--font-mono)" font-size="9" fill="#88a395">NORMAS TÉCNICAS:</text>
      <text x="390" y="65" font-family="var(--font-mono)" font-size="10" fill="#00e5ff" font-weight="700">IEC 60617 / NBR 5410 / NR-12</text>

      <!-- Linha 3: Equipe, Escala, Data e Folha -->
      <text x="12" y="88" font-family="var(--font-mono)" font-size="8" fill="#88a395">RESP. TÉCNICO / PROJETISTA:</text>
      <text x="12" y="102" font-family="var(--font-sans)" font-size="10" fill="#e0e8e3" font-weight="600">ENG. ELETRICISTA &amp; ENG. AUTOMAÇÃO</text>
      <text x="12" y="113" font-family="var(--font-mono)" font-size="8" fill="#5c7566">STATUS: APROVADO P/ FEIRA | REV: 3.0 (CONSOLIDADA)</text>
      
      <text x="230" y="88" font-family="var(--font-mono)" font-size="8" fill="#88a395">DATA DE EMISSÃO:</text>
      <text x="230" y="102" font-family="var(--font-mono)" font-size="11" fill="#ffffff" font-weight="600">NOVEMBRO / 2026</text>
      <text x="230" y="113" font-family="var(--font-mono)" font-size="8" fill="#5c7566">ESCALA: S/ ESCALA (DIAGR.)</text>

      <text x="390" y="88" font-family="var(--font-mono)" font-size="8" fill="#88a395">FORMATO:</text>
      <text x="390" y="105" font-family="var(--font-mono)" font-size="12" fill="#00e676" font-weight="700">A3 / A4 PAISAGEM</text>

      <text x="490" y="88" font-family="var(--font-mono)" font-size="8" fill="#88a395">PRANCHA:</text>
      <text x="490" y="108" font-family="var(--font-mono)" font-size="16" fill="#00e5ff" font-weight="800">0{sheet_num} / 04</text>
    </g>
    """

    return f"""
    <!-- Moldura Técnica Perimetral -->
    <rect x="20" y="20" width="1660" height="940" class="cad-border"/>
    <rect x="35" y="35" width="1630" height="910" class="cad-inner-border"/>
    
    <!-- Marcadores de Coordenadas de Projeto -->
    <g id="grid_markers_s{sheet_num}">
      {col_markers}
      {row_markers}
    </g>
    
    {carimbo}
    """
