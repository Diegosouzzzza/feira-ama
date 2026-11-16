# -*- coding: utf-8 -*-
"""
JavaScript da planta estatica do AmazonVision 4.0.

Documento de montagem: nao ha simulacao, Inspector, tooltips, tema ou modo
Visitante. Resta o minimo para ler o desenho na tela — navegar entre as cinco
folhas, aproximar e imprimir.

Sem interpolacao de dados, entao as chaves do JS sao escritas normalmente.
"""


def get_app_js():
    return """
// ========================================================
// ESTADO DE VISUALIZACAO (apenas leitura do desenho)
// ========================================================
const ViewState = {
  currentSheet: 0,
  zoomLevel: 1.0,
  panX: 0,
  panY: 0,
  isPanning: false,
  startX: 0,
  startY: 0
};

// ========================================================
// NAVEGACAO DE PRANCHAS + SIDEBAR
// ========================================================
function switchSheet(sheetNum) {
  if (isNaN(sheetNum) || sheetNum < 0 || sheetNum > 4) return;
  ViewState.currentSheet = sheetNum;

  document.querySelectorAll('.tab-btn').forEach(function(tab, index) {
    tab.classList.toggle('active', index === sheetNum);
  });

  document.querySelectorAll('.sheet-container').forEach(function(sheet, index) {
    sheet.classList.toggle('active', index === sheetNum);
  });

  document.querySelectorAll('.sidebar-item').forEach(function(item, index) {
    item.classList.toggle('active', index === sheetNum);
  });

  resetZoom();
  closeSidebar();
}

function prevSheet() {
  if (ViewState.currentSheet > 0) switchSheet(ViewState.currentSheet - 1);
}

function nextSheet() {
  if (ViewState.currentSheet < 4) switchSheet(ViewState.currentSheet + 1);
}

// Atalhos de teclado: 0-4 vao direto a folha, setas avancam e voltam.
window.addEventListener('keydown', function(e) {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key >= '0' && e.key <= '4') switchSheet(parseInt(e.key, 10));
  if (e.key === 'ArrowRight') nextSheet();
  if (e.key === 'ArrowLeft') prevSheet();
});

// ========================================================
// SIDEBAR (hamburger em telas estreitas)
// ========================================================
function toggleSidebar() {
  var nav = document.getElementById('sidebarNav');
  var overlay = document.getElementById('sidebarOverlay');
  if (nav) nav.classList.toggle('open');
  if (overlay) overlay.classList.toggle('open');
}

function closeSidebar() {
  var nav = document.getElementById('sidebarNav');
  var overlay = document.getElementById('sidebarOverlay');
  if (nav) nav.classList.remove('open');
  if (overlay) overlay.classList.remove('open');
}

// ========================================================
// ZOOM & PAN
// ========================================================
function applyTransform() {
  var activeContainer = document.querySelector('.sheet-container.active');
  if (activeContainer) {
    activeContainer.style.transform =
      'translate(' + ViewState.panX + 'px, ' + ViewState.panY + 'px) scale(' + ViewState.zoomLevel + ')';
  }
}

function zoomIn() {
  ViewState.zoomLevel = Math.min(2.5, ViewState.zoomLevel + 0.15);
  applyTransform();
}

function zoomOut() {
  ViewState.zoomLevel = Math.max(0.6, ViewState.zoomLevel - 0.15);
  applyTransform();
}

function resetZoom() {
  ViewState.zoomLevel = 1.0;
  ViewState.panX = 0;
  ViewState.panY = 0;
  applyTransform();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========================================================
// IMPRESSAO
// ========================================================
function printBlueprint() {
  window.print();
}

function printAllSheets() {
  document.body.classList.add('print-all');
  window.print();
  setTimeout(function() {
    document.body.classList.remove('print-all');
  }, 1000);
}

// ========================================================
// INICIALIZACAO
// ========================================================
document.addEventListener('DOMContentLoaded', function() {
  // Abertura direta numa folha: ?sheet=3 ou #fl3
  var urlParams = new URLSearchParams(window.location.search);
  var hash = window.location.hash;
  if (urlParams.has('sheet')) {
    switchSheet(parseInt(urlParams.get('sheet'), 10));
  } else if (hash.includes('sheet') || hash.includes('fl')) {
    var match = hash.match(/\\d+/);
    if (match) switchSheet(parseInt(match[0], 10));
  }

  var viewport = document.querySelector('.cad-viewport');
  if (!viewport) return;

  viewport.addEventListener('wheel', function(e) {
    if (e.ctrlKey) {
      e.preventDefault();
      if (e.deltaY < 0) zoomIn();
      else zoomOut();
    }
  }, { passive: false });

  viewport.addEventListener('mousedown', function(e) {
    if (e.button === 0 && (e.target.tagName === 'svg' ||
        e.target.classList.contains('cad-viewport') ||
        e.target.classList.contains('cad-border'))) {
      ViewState.isPanning = true;
      ViewState.startX = e.clientX - ViewState.panX;
      ViewState.startY = e.clientY - ViewState.panY;
      viewport.style.cursor = 'grabbing';
    }
  });

  window.addEventListener('mousemove', function(e) {
    if (!ViewState.isPanning) return;
    ViewState.panX = e.clientX - ViewState.startX;
    ViewState.panY = e.clientY - ViewState.startY;
    applyTransform();
  });

  window.addEventListener('mouseup', function() {
    if (ViewState.isPanning) {
      ViewState.isPanning = false;
      viewport.style.cursor = 'default';
    }
  });
});
"""
