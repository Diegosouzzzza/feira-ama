# -*- coding: utf-8 -*-
"""
Generator for Header, Sidebar Nav, Bus Legend and View Actions.
AmazonVision 4.0 - XXI Feira Tecnologica FUCAPI 2026

Documento estatico de montagem: sem simulacao, sem Inspector, sem tooltips,
sem alternancia de tema e sem modo Visitante. Sobram a navegacao entre as
folhas, os controles de leitura (zoom / impressao) e a legenda dos
barramentos, que e parte de como se le o desenho.
"""

def get_header_and_toolbar():
    return """
<!-- ═══════════════════════════════════════════════════
     SIDEBAR NAVIGATION (Sticky Left)
     ═══════════════════════════════════════════════════ -->
<nav class="sidebar-nav" id="sidebarNav">
  <div class="sidebar-brand">
    <div class="sidebar-brand-text">AmazonVision 4.0</div>
    <div class="sidebar-brand-sub">Planta Eletrica Industrial</div>
  </div>
  <ul class="sidebar-list" id="sidebarList">
    <li class="sidebar-item active" onclick="switchSheet(0)" data-sheet="0">
      <span class="sidebar-num">00</span>
      <span class="sidebar-label">Planta Geral</span>
    </li>
    <li class="sidebar-item" onclick="switchSheet(1)" data-sheet="1">
      <span class="sidebar-num">01</span>
      <span class="sidebar-label">Forca e NR-12</span>
    </li>
    <li class="sidebar-item" onclick="switchSheet(2)" data-sheet="2">
      <span class="sidebar-num">02</span>
      <span class="sidebar-label">Potencia M1/M2</span>
    </li>
    <li class="sidebar-item" onclick="switchSheet(3)" data-sheet="3">
      <span class="sidebar-num">03</span>
      <span class="sidebar-label">Comando e Sensores</span>
    </li>
    <li class="sidebar-item" onclick="switchSheet(4)" data-sheet="4">
      <span class="sidebar-num">04</span>
      <span class="sidebar-label">Painel e BOM</span>
    </li>
  </ul>
  <!-- LEGENDA DE BARRAMENTOS (estatica, ancorada no rodape da sidebar) -->
  <div class="bus-legend" id="busLegend">
    <div class="bus-legend-header">
      <span>Legenda de Barramentos</span>
    </div>
    <div class="bus-legend-body" id="busLegendBody">
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-ac-l);"></span>
        <span class="bus-legend-label">Fase AC (L)</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-ac-n);"></span>
        <span class="bus-legend-label">Neutro AC (N)</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-pe);"></span>
        <span class="bus-legend-label">Terra PE</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-12v-cont);"></span>
        <span class="bus-legend-label">+12V Continuo</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-12v-at);"></span>
        <span class="bus-legend-label">+12V Atuadores (NR-12)</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-6v);"></span>
        <span class="bus-legend-label">+6V Servo</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-5v);"></span>
        <span class="bus-legend-label">+5V ESP32 / Sensores</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-3v3);"></span>
        <span class="bus-legend-label">+3,3V Sinais Logicos</span>
      </div>
      <div class="bus-legend-row">
        <span class="bus-legend-swatch" style="background:var(--c-gnd);"></span>
        <span class="bus-legend-label">GND / 0V Comum</span>
      </div>
    </div>
  </div>
  <div class="sidebar-pager">
    <button onclick="prevSheet()" id="btnPrevSheet" title="Folha anterior">&larr; Anterior</button>
    <button onclick="nextSheet()" id="btnNextSheet" title="Proxima folha">Proxima &rarr;</button>
  </div>
</nav>

<!-- Hamburger Button (mobile/tablet only) -->
<button class="hamburger-btn" id="hamburgerBtn" onclick="toggleSidebar()" aria-label="Menu de navegacao">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
</button>

<!-- Sidebar Overlay (mobile) -->
<div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>

<!-- ═══════════════════════════════════════════════════
     APP SHELL (everything right of sidebar)
     ═══════════════════════════════════════════════════ -->
<div class="app-shell" id="appShell">

<header class="app-header">
  <div class="header-top">
    <div class="brand-block">
      <span class="brand-badge">PROJETO OFICIAL</span>
      <div class="brand-title">
        <h1>AMAZONVISION 4.0 <span class="sub">Planta Eletrica Industrial</span></h1>
      </div>
    </div>
    <div class="header-meta">
      <div class="view-actions">
        <button class="btn-action" onclick="zoomIn()" title="Zoom +">+</button>
        <button class="btn-action" onclick="zoomOut()" title="Zoom -">&minus;</button>
        <button class="btn-action" onclick="resetZoom()" title="Ajustar a tela">Ajustar</button>
        <button class="btn-action btn-print" onclick="printBlueprint()" title="Imprimir folha atual">Imprimir</button>
        <button class="btn-action btn-print" onclick="printAllSheets()" title="Imprimir caderno completo">Caderno</button>
      </div>
    </div>
  </div>

  <!-- Abas (visivel apenas em mobile/tablet) -->
  <nav class="sheet-tabs" id="sheetTabs">
    <button class="tab-btn active" onclick="switchSheet(0)">
      <span class="badge-num">VISAO 00</span>
      <span>Planta Geral</span>
    </button>
    <button class="tab-btn" onclick="switchSheet(1)">
      <span class="badge-num">FOLHA 01</span>
      <span>Forca e NR-12</span>
    </button>
    <button class="tab-btn" onclick="switchSheet(2)">
      <span class="badge-num">FOLHA 02</span>
      <span>Potencia M1/M2</span>
    </button>
    <button class="tab-btn" onclick="switchSheet(3)">
      <span class="badge-num">FOLHA 03</span>
      <span>Comando e Sensores</span>
    </button>
    <button class="tab-btn" onclick="switchSheet(4)">
      <span class="badge-num">FOLHA 04</span>
      <span>Painel e BOM</span>
    </button>
  </nav>
</header>
"""
