# -*- coding: utf-8 -*-
"""
CSS Styles — Planta Eletrica Industrial AmazonVision 4.0
Documento estatico de montagem para a XXI Feira Tecnologica FUCAPI 2026.

Sem simulacao, sem Inspector, sem tooltips, sem alternancia de tema ou modo.
O tema claro e fixo e ativado por ``body.theme-light`` no build.
"""

def get_css():
    return """
:root {
  /* ── Backgrounds & Surfaces ── */
  --bg-cad: #090e0c;
  --bg-panel: #101713;
  --bg-card: #141d18;
  --bg-surface: #0f1612;
  --border-cad: #1d2c23;
  --border-focus: #00e5ff;

  /* ── Text ── */
  --text-main: #e2ece5;
  --text-muted: #8ba294;
  --text-bright: #ffffff;

  /* ── Barramentos (paleta escura — base sobre a qual a camada clara atua) ── */
  --c-12v-cont: #ff3344;
  --c-12v-at: #ff1744;
  --c-6v: #ff9100;
  --c-5v: #ffd600;
  --c-3v3: #d500f9;
  --c-gnd: #00e676;
  --c-pe: #c6ff00;
  --c-ac-l: #ff80ab;
  --c-ac-n: #80d8ff;
  --c-sig: #b388ff;

  /* ── Accent ── */
  --accent: #00e676;
  --accent-info: #00e5ff;

  /* ── Typography Scale (clamp for tablet) ── */
  --fs-xs:  clamp(10px, 0.65vw + 6px, 12px);
  --fs-sm:  clamp(12px, 0.7vw + 7px, 14px);
  --fs-base: clamp(14px, 0.75vw + 8px, 16px);
  --fs-md:  clamp(16px, 0.85vw + 9px, 20px);
  --fs-lg:  clamp(22px, 1.2vw + 12px, 28px);
  --fs-xl:  clamp(28px, 1.5vw + 16px, 36px);

  /* ── Fonts ── */
  --font-mono: 'Consolas', 'Roboto Mono', 'SF Pro Mono', 'Courier New', monospace;
  --font-sans: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;

  /* ── Layout ── */
  --sidebar-w: 220px;
  --header-h: auto;
}

/* ═══════════════════════════════════════════════════════
   LIGHT THEME — complete override including bus colors.
   Ativado por body.theme-light, que e fixo no build.
   ═══════════════════════════════════════════════════════ */
body.theme-light {
  --bg-cad: #f4f6f5;
  --bg-panel: #ffffff;
  --bg-card: #f0f3f1;
  --bg-surface: #fafbfa;
  --border-cad: #c0cfc6;
  --border-focus: #007799;
  --text-main: #1a2820;
  --text-muted: #4e6056;
  --text-bright: #0d1310;

  /* Bus colors re-tuned for white bg: medium saturation, AA contrast */
  --c-12v-cont: #c0392b;
  --c-12v-at: #b71c1c;
  --c-6v: #d35400;
  --c-5v: #b7950b;
  --c-3v3: #7b1fa2;
  --c-gnd: #1e8449;
  --c-pe: #6c8c21;
  --c-ac-l: #c0547a;
  --c-ac-n: #2471a3;
  --c-sig: #6c3483;

  --accent: #0d8c4e;
  --accent-info: #007799;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--bg-cad);
  color: var(--text-main);
  font-family: var(--font-sans);
  font-size: var(--fs-base);
  line-height: 1.4;
  overflow-x: hidden;
  user-select: none;
}

/* ── Scrollbars ── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg-cad); }
::-webkit-scrollbar-thumb { background: var(--border-cad); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2e4337; }
body.theme-light ::-webkit-scrollbar-thumb:hover { background: #8fa699; }

/* ═══════════════════════════════════════════════════════
   ROTULOS — Planta estatica mostra sempre os tecnicos
   ═══════════════════════════════════════════════════════ */
.tech-only  { display: inline; }
.public-label { display: none !important; }

/* ═══════════════════════════════════════════════════════
   APP HEADER
   ═══════════════════════════════════════════════════════ */
header.app-header {
  background: linear-gradient(180deg, #131b17 0%, #0d1310 100%);
  border-bottom: 2px solid #22352b;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}

body.theme-light header.app-header {
  background: linear-gradient(180deg, #f0f5f2 0%, #e2ebe5 100%);
  border-bottom-color: #a4beaf;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 18px;
  border-bottom: 1px solid #1a2720;
}

body.theme-light .header-top { border-bottom-color: #c5d6cc; }

.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-badge {
  background: var(--accent);
  color: #000;
  font-weight: 800;
  font-size: var(--fs-xs);
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.brand-title h1 {
  font-size: var(--fs-md);
  font-weight: 700;
  color: var(--text-bright);
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-title span.sub {
  font-size: var(--fs-xs);
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 6px;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
}

/* ── View Actions ── */
.view-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-action {
  background: #18231d;
  color: var(--text-main);
  border: 1px solid #283a2f;
  padding: 5px 9px;
  border-radius: 4px;
  font-size: var(--fs-xs);
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: 0.15s;
}

body.theme-light .btn-action {
  background: #ffffff;
  border-color: #b0c4b8;
  color: #17241d;
}

.btn-action:hover {
  background: #23342b;
  color: #fff;
  border-color: var(--accent-info);
}

.btn-print {
  background: #143025;
  border-color: var(--accent);
  color: #c9ffd9;
}
.btn-print:hover {
  background: #194031;
  color: #fff;
  box-shadow: 0 0 12px rgba(0,230,118,0.3);
}

body.theme-light .btn-print {
  background: #e6f5ec;
  border-color: #0d8c4e;
  color: #0d5025;
}

/* ═══════════════════════════════════════════════════════
   SHEET TABS (hidden on desktop — replaced by sidebar)
   ═══════════════════════════════════════════════════════ */
.sheet-tabs {
  background: #0b110e;
  border-bottom: 2px solid #1a2720;
  display: none;
  gap: 2px;
  padding: 4px 18px 0;
  overflow-x: auto;
}

body.theme-light .sheet-tabs {
  background: #e5ece8;
  border-bottom-color: #b8ccc0;
}

.tab-btn {
  background: #131c17;
  color: var(--text-muted);
  border: 1px solid #1e2c24;
  border-bottom: none;
  padding: 9px 16px;
  border-radius: 6px 6px 0 0;
  font-size: var(--fs-xs);
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

body.theme-light .tab-btn { background: #d8e2dc; border-color: #b5c7bd; color: #485c51; }

.tab-btn:hover { background: #1a2620; color: #fff; }

.tab-btn.active {
  background: var(--bg-cad);
  color: var(--accent-info);
  border-color: var(--accent-info);
  border-top: 2px solid var(--accent-info);
  box-shadow: inset 0 2px 8px rgba(0,229,255,0.15);
}

body.theme-light .tab-btn.active {
  background: #f2f5f3;
  color: #007799;
  border-color: #007799;
}

.tab-btn .badge-num {
  background: #1e2d25;
  color: var(--text-main);
  font-size: var(--fs-xs);
  font-family: var(--font-mono);
  padding: 2px 6px;
  border-radius: 3px;
}

.tab-btn.active .badge-num {
  background: var(--accent-info);
  color: #000;
  font-weight: 700;
}

body.theme-light .tab-btn.active .badge-num { background: #007799; color: #fff; }

/* ═══════════════════════════════════════════════════════
   SIDEBAR NAVIGATION (Sticky Left)
   ═══════════════════════════════════════════════════════ */
.sidebar-nav {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--sidebar-w);
  background: #0c1310;
  border-right: 1px solid #1e2c24;
  z-index: 1100;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease;
  overflow-y: auto;
}

body.theme-light .sidebar-nav {
  background: #eaf0ec;
  border-right-color: #b3c6bb;
}

.sidebar-brand {
  padding: 14px 16px 10px;
  border-bottom: 1px solid #1e2c24;
}

body.theme-light .sidebar-brand { border-bottom-color: #c0d1c7; }

.sidebar-brand-text {
  font-family: var(--font-mono);
  font-size: var(--fs-sm);
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.01em;
}

.sidebar-brand-sub {
  font-size: var(--fs-xs);
  color: var(--text-muted);
  margin-top: 2px;
}

.sidebar-list {
  list-style: none;
  padding: 8px 0;
  flex: 1;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  color: var(--text-muted);
  font-size: var(--fs-sm);
}

.sidebar-item:hover {
  background: #15221b;
  color: var(--text-main);
}

body.theme-light .sidebar-item:hover { background: #e5ece8; }

.sidebar-item.active {
  border-left-color: var(--accent-info);
  background: #0f1c16;
  color: var(--accent-info);
}

body.theme-light .sidebar-item.active {
  border-left-color: #007799;
  background: #e0eee6;
  color: #007799;
}

.sidebar-num {
  font-family: var(--font-mono);
  font-size: var(--fs-md);
  font-weight: 800;
  min-width: 28px;
  text-align: center;
  color: var(--text-muted);
}

.sidebar-item.active .sidebar-num { color: var(--accent-info); }
body.theme-light .sidebar-item.active .sidebar-num { color: #007799; }

.sidebar-label {
  font-weight: 600;
  line-height: 1.25;
}

.sidebar-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  fill: currentColor;
}

/* Prev/Next nav at sidebar bottom */
.sidebar-pager {
  display: flex;
  border-top: 1px solid #1e2c24;
  padding: 0;
}

body.theme-light .sidebar-pager { border-top-color: #c0d1c7; }

.sidebar-pager button {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: var(--fs-sm);
  font-weight: 600;
  cursor: pointer;
  transition: 0.15s;
}

.sidebar-pager button:hover { background: #15221b; color: var(--text-main); }
body.theme-light .sidebar-pager button:hover { background: #e5ece8; }
.sidebar-pager button + button { border-left: 1px solid #1e2c24; }
body.theme-light .sidebar-pager button + button { border-left-color: #c0d1c7; }

/* Hamburger button (visible only on tablet/mobile) */
.hamburger-btn {
  display: none;
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1200;
  background: var(--bg-card);
  border: 1px solid var(--border-cad);
  border-radius: 6px;
  padding: 8px;
  cursor: pointer;
  color: var(--text-main);
}

.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1050;
}

/* ═══════════════════════════════════════════════════════
   MAIN VIEWPORT — shifted right for sidebar
   ═══════════════════════════════════════════════════════ */
.app-shell {
  margin-left: var(--sidebar-w);
  transition: margin-left 0.25s;
}

main.cad-viewport {
  position: relative;
  width: 100%;
  min-height: calc(100vh - 165px);
  padding: 20px 24px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-color: var(--bg-cad);
  background-image:
    radial-gradient(#18261e 1px, transparent 1px),
    linear-gradient(to right, rgba(20,32,25,0.4) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(20,32,25,0.4) 1px, transparent 1px);
  background-size: 20px 20px, 100px 100px, 100px 100px;
  overflow: auto;
}

body.theme-light main.cad-viewport {
  background-image:
    radial-gradient(#c8d4cd 1px, transparent 1px),
    linear-gradient(to right, rgba(180,195,188,0.4) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(180,195,188,0.4) 1px, transparent 1px);
}

.sheet-container {
  display: none;
  width: 100%;
  max-width: 1720px;
  background: #0b100d;
  border: 1px solid #1a2720;
  box-shadow: 0 10px 40px rgba(0,0,0,0.8);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  transform-origin: 0 0;
  transition: transform 0.05s ease-out;
}

body.theme-light .sheet-container {
  background: #ffffff;
  border-color: #cbd8d0;
  box-shadow: 0 6px 25px rgba(0,0,0,0.12);
}

.sheet-container.active { display: block; }

svg.blueprint-svg {
  width: 100%;
  height: auto;
  display: block;
  shape-rendering: geometricPrecision;
  text-rendering: geometricPrecision;
}

/* ═══════════════════════════════════════════════════════
   SVG ELEMENTS & IEC SYMBOLS
   ═══════════════════════════════════════════════════════ */
.cad-border { stroke: #2a3d31; stroke-width: 2; fill: none; }
.cad-inner-border { stroke: #1e2c24; stroke-width: 1; fill: none; }
.cad-grid-text { font-family: var(--font-mono); font-size: 11px; fill: #486151; font-weight: 600; }
.cad-title-block { fill: #0f1612; stroke: #2a3d31; stroke-width: 1.5; }
.cad-title-line { stroke: #1e2c24; stroke-width: 1; }

body.theme-light .cad-border { stroke: #7b9485; }
body.theme-light .cad-inner-border { stroke: #a3b8ad; }
body.theme-light .cad-grid-text { fill: #62786b; }
body.theme-light .cad-title-block { fill: #f2f7f4; stroke: #7b9485; }
body.theme-light .cad-title-line { stroke: #c0d1c7; }

.symbol-box { fill: #121a16; stroke: #2c4234; stroke-width: 1.5; rx: 3; }
.symbol-box-accent { fill: #16241c; stroke: var(--accent-info); stroke-width: 1.8; rx: 3; }
.symbol-terminal { fill: #18261e; stroke: #4e6b5a; stroke-width: 1.5; }

body.theme-light .symbol-box { fill: #f9fbf9; stroke: #8ca395; }
body.theme-light .symbol-box-accent { fill: #eef6f3; stroke: #0088a8; }
body.theme-light .symbol-terminal { fill: #ffffff; stroke: #4e6b5a; }

/* ── Technical Labels ── */
.lbl-tag { font-family: var(--font-mono); font-size: var(--fs-sm); font-weight: 700; fill: #ffffff; }
.lbl-desc { font-family: var(--font-sans); font-size: var(--fs-xs); fill: #8fa699; }
.lbl-pin { font-family: var(--font-mono); font-size: var(--fs-xs); fill: #72a88d; font-weight: 600; }
.lbl-spec { font-family: var(--font-mono); font-size: 9px; fill: #5b7968; }
.lbl-wire { font-family: var(--font-mono); font-size: var(--fs-xs); fill: var(--accent-info); font-weight: 600; }

body.theme-light .lbl-tag { fill: #0d1a13; }
body.theme-light .lbl-desc { fill: #3f5448; }
body.theme-light .lbl-pin { fill: #2c4737; }

/* ═══════════════════════════════════════════════════════
   WIRES & BUSES
   ═══════════════════════════════════════════════════════ */
.wire { stroke-linecap: round; stroke-linejoin: round; fill: none; }
.wire-junction { fill: #ffffff; }
body.theme-light .wire-junction { fill: #1a2820; }

.w-ac-l { stroke: var(--c-ac-l); stroke-width: 2.2; }
.w-ac-n { stroke: var(--c-ac-n); stroke-width: 2.2; }
.w-pe { stroke: var(--c-pe); stroke-width: 2.2; stroke-dasharray: 6 3; }

.w-12v-cont { stroke: var(--c-12v-cont); stroke-width: 2.4; }
.w-12v-at { stroke: var(--c-12v-at); stroke-width: 2.5; }
.w-6v { stroke: var(--c-6v); stroke-width: 2.2; }
.w-5v { stroke: var(--c-5v); stroke-width: 2.0; }
.w-3v3 { stroke: var(--c-3v3); stroke-width: 1.8; }
.w-gnd { stroke: var(--c-gnd); stroke-width: 2.4; }
.w-sig { stroke: var(--c-sig); stroke-width: 2.0; }

/* ═══════════════════════════════════════════════════════
   BOM TABLE (Sheet 04)
   ═══════════════════════════════════════════════════════ */
.bom-table-wrap {
  width: 100%;
  height: 100%;
  background: #0f1612;
  border: 1px solid #1e2c24;
  border-radius: 4px;
  overflow-y: auto;
  font-size: 9.5px;
}

body.theme-light .bom-table-wrap { background: #ffffff; border-color: #c0d1c7; }

table.cad-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-sans);
  line-height: 1.15;
}

table.cad-table th {
  background: #16221b;
  color: var(--accent-info);
  font-family: var(--font-mono);
  font-size: 8.5px;
  font-weight: 700;
  text-align: left;
  padding: 2px 5px;
  line-height: 1.12;
  white-space: nowrap;
  border-bottom: 2px solid #22372c;
  border-right: 1px solid #1a2720;
}

table.cad-table th.cad-table-banner {
  background: #14241b;
  color: var(--accent-info);
  text-align: center;
  font-size: 9.5px;
  padding: 3px 6px;
}

body.theme-light table.cad-table th {
  background: #e3ede7;
  color: #006680;
  border-bottom-color: #a4beaf;
  border-right-color: #c5d6cc;
}

body.theme-light table.cad-table th.cad-table-banner {
  background: #d4e3da;
  color: #0d3b2e;
}

table.cad-table td {
  padding: 2px 5px;
  font-size: 8.5px;
  line-height: 1.12;
  white-space: nowrap;
  border-bottom: 1px solid #16201a;
  border-right: 1px solid #16201a;
  color: var(--text-main);
}

body.theme-light table.cad-table td { border-color: #e2ebe6; }

table.cad-table tr:nth-child(even) { background: #0c1310; }
body.theme-light table.cad-table tr:nth-child(even) { background: #f8faf9; }
table.cad-table tr:hover { background: #18241d; }
body.theme-light table.cad-table tr:hover { background: #eaf1ed; }

.tag-badge {
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 8px;
  background: #182820;
  border: 1px solid #2a4033;
  padding: 0px 4px;
  border-radius: 3px;
  color: var(--accent);
  white-space: nowrap;
}

body.theme-light .tag-badge {
  background: #e2f2e9;
  border-color: #92c4a6;
  color: #0b733b;
}

/* ═══════════════════════════════════════════════════════
   BUS LEGEND (Inside Sidebar Footer)
   ═══════════════════════════════════════════════════════ */
.bus-legend {
  width: 100%;
  background: #0c1310;
  border: none;
  border-top: 1px solid #1e2c24;
  border-radius: 0;
  box-shadow: none;
  font-size: var(--fs-xs);
  overflow: hidden;
  margin-top: auto;
}

body.theme-light .bus-legend {
  background: #eaf0ec;
  border-top-color: #c0d1c7;
}

.bus-legend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #1e2c24;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: var(--fs-xs);
  color: var(--text-main);
}

body.theme-light .bus-legend-header { border-bottom-color: #c0d1c7; }

.bus-legend-body {
  padding: 8px 12px;
}

.bus-legend-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 0;
}

.bus-legend-swatch {
  width: 24px;
  height: 4px;
  border-radius: 2px;
  flex-shrink: 0;
}

.bus-legend-label {
  color: var(--text-main);
  font-size: var(--fs-xs);
  line-height: 1.2;
}

/* ═══════════════════════════════════════════════════════
   RESPONSIVE (<= 900px)
   ═══════════════════════════════════════════════════════ */
@media (max-width: 900px) {
  :root { --sidebar-w: 0px; }

  .sidebar-nav {
    transform: translateX(-260px);
    width: 260px;
  }

  .sidebar-nav.open { transform: translateX(0); }

  .sidebar-overlay.open { display: block; }

  .hamburger-btn { display: block; }

  .app-shell { margin-left: 0; }

  .sheet-tabs { display: flex; }

  /* folga a esquerda para o botao hamburger, que e fixo em left:10px */
  header.app-header .header-top { flex-wrap: wrap; gap: 8px; padding: 8px 18px 8px 56px; }
  header.app-header .header-meta { flex-wrap: wrap; }

  main.cad-viewport { padding: 12px 8px; }
}

/* ═══════════════════════════════════════════════════════
   PRINT RULES
   ═══════════════════════════════════════════════════════ */
@media print {
  @page {
    size: A3 landscape;
    margin: 8mm;
  }

  body {
    background: #ffffff !important;
    color: #000000 !important;
  }

  header.app-header,
  .sheet-tabs,
  .view-actions,
  .sidebar-nav,
  .hamburger-btn,
  .bus-legend {
    display: none !important;
  }

  .app-shell { margin-left: 0 !important; }

  main.cad-viewport {
    background: #ffffff !important;
    padding: 0 !important;
    display: block !important;
  }

  .sheet-container {
    display: none !important;
  }
  .sheet-container.active,
  body.print-all .sheet-container {
    display: block !important;
    background: #ffffff !important;
    border: none !important;
    box-shadow: none !important;
    page-break-after: always;
    page-break-inside: avoid;
    margin-bottom: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
  }
  .sheet-container.active:last-child,
  body.print-all .sheet-container:last-child {
    page-break-after: auto;
  }

  .bom-table-wrap {
    overflow: visible !important;
    height: auto !important;
  }

  .cad-border { stroke: #000000 !important; }
  .cad-inner-border { stroke: #000000 !important; }
  .cad-title-block { fill: #f0f0f0 !important; stroke: #000000 !important; }
  .lbl-tag { fill: #000000 !important; }
}
"""
