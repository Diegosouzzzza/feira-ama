import fs from 'fs';
import path from 'path';
import { chromium } from '@playwright/test';

const richBackdropSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 720" width="1960" height="1440" fill="none">
  <defs>
    <!-- Gradientes e Sombras -->
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06" />
    </linearGradient>
    <linearGradient id="tucumaGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF9E1B" />
      <stop offset="70%" stop-color="#E66700" />
      <stop offset="100%" stop-color="#A84400" />
    </linearGradient>
    <linearGradient id="castanhaGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8D5B36" />
      <stop offset="100%" stop-color="#4E2F17" />
    </linearGradient>
    <linearGradient id="servoGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1E88E5" />
      <stop offset="100%" stop-color="#0D47A1" />
    </linearGradient>
    <linearGradient id="espGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#263238" />
      <stop offset="100%" stop-color="#10171A" />
    </linearGradient>
    <linearGradient id="goldTraces" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFD54F" />
      <stop offset="100%" stop-color="#FFB300" />
    </linearGradient>
    <linearGradient id="hudLaser" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00E676" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00E676" stop-opacity="0.1" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- ================= FUNDO TRANSLÚCIDO E TRILHAS ================= -->
  <rect x="10" y="10" width="960" height="700" rx="32" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="2.5" filter="url(#shadow)" />

  <!-- Trilhas de Circuito Douradas e Nódulos Tech -->
  <g stroke="url(#goldTraces)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.6">
    <path d="M 60 70 L 140 70 L 170 100 L 260 100" />
    <circle cx="260" cy="100" r="4" fill="#FFD54F" />
    <path d="M 920 70 L 840 70 L 810 100 L 720 100" />
    <circle cx="720" cy="100" r="4" fill="#FFD54F" />
    <path d="M 50 480 L 120 480 L 150 510 L 240 510" />
    <circle cx="50" cy="480" r="4" fill="#FFD54F" />
    <path d="M 930 480 L 860 480 L 830 510 L 740 510" />
    <circle cx="930" cy="480" r="4" fill="#FFD54F" />
  </g>

  <!-- ================= 1. O MASCOTE "ROBÔ ENGENHEIRO" (BONEQUINHO) ================= -->
  <!-- Posicionado no lado esquerdo com atitude amigável e scanner -->
  <g transform="translate(65, 80)" filter="url(#shadow)">
    <!-- Aura do Mascote -->
    <circle cx="100" cy="150" r="95" fill="#FFFFFF" fill-opacity="0.08" />
    
    <!-- Antena -->
    <line x1="100" y1="45" x2="100" y2="15" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" />
    <circle cx="100" cy="12" r="10" fill="#00E676" filter="url(#glow)" />
    <circle cx="100" cy="12" r="5" fill="#FFFFFF" />

    <!-- Cabeça do Robô -->
    <rect x="45" y="45" width="110" height="85" rx="24" fill="#F4F6F7" stroke="#37474F" stroke-width="4.5" />
    <!-- Visor de Vidro Futurista -->
    <rect x="58" y="60" width="84" height="46" rx="14" fill="#1A262C" stroke="#00B0FF" stroke-width="2" />
    <!-- Olhos Digitais Expressivos (Alegres) -->
    <ellipse cx="80" cy="82" rx="10" ry="12" fill="#00E676" filter="url(#glow)" />
    <ellipse cx="120" cy="82" rx="10" ry="12" fill="#00E676" filter="url(#glow)" />
    <circle cx="83" cy="78" r="3.5" fill="#FFFFFF" />
    <circle cx="123" cy="78" r="3.5" fill="#FFFFFF" />
    <!-- Sorrisinho tech -->
    <path d="M 92 98 Q 100 104 108 98" stroke="#00E676" stroke-width="3" stroke-linecap="round" />
    <!-- Fones / Orelhas de parafuso -->
    <rect x="36" y="70" width="10" height="30" rx="4" fill="#78909C" stroke="#37474F" stroke-width="3" />
    <rect x="154" y="70" width="10" height="30" rx="4" fill="#78909C" stroke="#37474F" stroke-width="3" />

    <!-- Pescoço com molas -->
    <rect x="86" y="130" width="28" height="12" rx="3" fill="#90A4AE" stroke="#37474F" stroke-width="3" />
    
    <!-- Corpo / Tronco -->
    <path d="M 40 142 L 160 142 L 148 245 L 52 245 Z" fill="#ECEFF1" stroke="#37474F" stroke-width="4.5" />
    <!-- Detalhe peitoral: Tela de Status / Crachá FUCAPI -->
    <rect x="62" y="156" width="76" height="42" rx="8" fill="#FFFFFF" stroke="#0288D1" stroke-width="2.5" />
    <text x="100" y="172" font-family="'Archivo', sans-serif" font-weight="900" font-size="10" fill="#01579B" text-anchor="middle">FUCAPI</text>
    <text x="100" y="188" font-family="'Archivo', sans-serif" font-weight="800" font-size="9" fill="#00897B" text-anchor="middle">AUTOMAÇÃO</text>
    <!-- Medidor cardíaco / pulso de IA -->
    <path d="M 72 215 L 85 215 L 92 205 L 100 225 L 108 212 L 115 218 L 128 218" stroke="#00E676" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

    <!-- Braço Esquerdo (acenando ou apoiado) -->
    <path d="M 40 155 Q 15 180 28 215" stroke="#37474F" stroke-width="12" stroke-linecap="round" />
    <circle cx="28" cy="215" r="10" fill="#78909C" stroke="#37474F" stroke-width="3" />

    <!-- Braço Direito (segurando Scanner de IA apontando para a esteira) -->
    <path d="M 158 160 Q 185 175 195 190" stroke="#37474F" stroke-width="12" stroke-linecap="round" />
    <!-- Scanner Óptico portado na mão -->
    <g transform="translate(190, 180) rotate(25)">
      <rect x="0" y="-12" width="40" height="24" rx="6" fill="#263238" stroke="#37474F" stroke-width="3" />
      <circle cx="40" cy="0" r="10" fill="#00E676" filter="url(#glow)" />
      <!-- Cone de laser saindo do scanner -->
      <polygon points="45,-6 140,-25 140,25 45,6" fill="url(#hudLaser)" />
      <line x1="45" y1="0" x2="140" y2="0" stroke="#00E676" stroke-width="2" stroke-dasharray="4 3" />
    </g>

    <!-- Base / Rodinhas ou Pernas articuladas -->
    <rect x="62" y="245" width="26" height="25" rx="6" fill="#78909C" stroke="#37474F" stroke-width="3" />
    <rect x="112" y="245" width="26" height="25" rx="6" fill="#78909C" stroke="#37474F" stroke-width="3" />
    <ellipse cx="75" cy="275" rx="20" ry="10" fill="#263238" />
    <ellipse cx="125" cy="275" rx="20" ry="10" fill="#263238" />
    
    <!-- Balão de Fala do Robô -->
    <g transform="translate(145, 15)">
      <path d="M 0 35 L 20 25 L 20 10 Q 20 0 30 0 L 155 0 Q 165 0 165 10 L 165 50 Q 165 60 155 60 L 30 60 Q 20 60 20 50 L 20 35 Z" fill="#FFFFFF" stroke="#37474F" stroke-width="3" />
      <text x="92" y="26" font-family="'Archivo', sans-serif" font-weight="900" font-size="13" fill="#1B5E20" text-anchor="middle">QUALIDADE 100%</text>
      <text x="92" y="44" font-family="'Archivo', sans-serif" font-weight="800" font-size="12" fill="#E65100" text-anchor="middle">INSPECIONADA!</text>
    </g>
  </g>

  <!-- ================= 2. ESTEIRA INDUSTRIAL E VISÃO COMPUTACIONAL ================= -->
  <g transform="translate(365, 85)" filter="url(#shadow)">
    <!-- Base da Esteira Isométrica -->
    <g transform="translate(0, 140)">
      <!-- Perfis de Alumínio e Pés -->
      <line x1="40" y1="50" x2="40" y2="120" stroke="#78909C" stroke-width="8" stroke-linecap="round" />
      <line x1="280" y1="50" x2="280" y2="120" stroke="#78909C" stroke-width="8" stroke-linecap="round" />
      <line x1="520" y1="50" x2="520" y2="120" stroke="#78909C" stroke-width="8" stroke-linecap="round" />
      
      <!-- Corpo da Esteira (Perfil V-Slot) -->
      <rect x="20" y="30" width="520" height="28" rx="6" fill="#37474F" stroke="#263238" stroke-width="3" />
      <line x1="25" y1="44" x2="535" y2="44" stroke="#78909C" stroke-width="2.5" />
      
      <!-- Correia em Movimento -->
      <rect x="25" y="8" width="510" height="24" rx="4" fill="#212121" stroke="#424242" stroke-width="2" />
      <!-- Ranhuras da correia -->
      <line x1="60" y1="8" x2="50" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="120" y1="8" x2="110" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="180" y1="8" x2="170" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="240" y1="8" x2="230" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="300" y1="8" x2="290" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="360" y1="8" x2="350" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="420" y1="8" x2="410" y2="32" stroke="#616161" stroke-width="2.5" />
      <line x1="480" y1="8" x2="470" y2="32" stroke="#616161" stroke-width="2.5" />

      <!-- Frutos na Esteira -->
      <!-- Fruto 1: Castanha-do-Pará chegando -->
      <g transform="translate(70, -10)">
        <ellipse cx="20" cy="15" rx="22" ry="14" fill="url(#castanhaGrad)" stroke="#271406" stroke-width="2.5" transform="rotate(-15, 20, 15)" />
        <path d="M 8 16 C 18 20, 28 12, 34 8" stroke="#D7CCC8" stroke-width="1.5" stroke-linecap="round" />
      </g>

      <!-- Fruto 2: Tucumã sob inspeção da câmera -->
      <g transform="translate(230, -22)">
        <circle cx="28" cy="25" r="28" fill="url(#tucumaGrad)" stroke="#4E2000" stroke-width="3" />
        <path d="M 20 6 Q 28 0 36 6 Q 28 10 20 6" fill="#2E7D32" /> <!-- Folhinha no topo -->
        <circle cx="22" cy="18" r="4" fill="#FFE082" fill-opacity="0.6" /> <!-- Brilho -->

        <!-- Bounding Box HUD com cantoneiras verdes brilhantes -->
        <rect x="-8" y="-12" width="72" height="72" fill="none" stroke="#00E676" stroke-width="2" stroke-dasharray="6 4" filter="url(#glow)" />
        <path d="M -8 3 L -8 -12 L 7 -12" stroke="#00E676" stroke-width="4.5" stroke-linecap="round" />
        <path d="M 49 -12 L 64 -12 L 64 3" stroke="#00E676" stroke-width="4.5" stroke-linecap="round" />
        <path d="M -8 45 L -8 60 L 7 60" stroke="#00E676" stroke-width="4.5" stroke-linecap="round" />
        <path d="M 49 60 L 64 60 L 64 45" stroke="#00E676" stroke-width="4.5" stroke-linecap="round" />
        
        <!-- Badge de Detecção Flutuante -->
        <rect x="4" y="-30" width="105" height="22" rx="4" fill="#00E676" />
        <text x="56" y="-15" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#003314" text-anchor="middle">CLASSE A · 98.4%</text>
      </g>

      <!-- Braço Defletor / Servo Mecânico atuando na saída -->
      <g transform="translate(390, -10)">
        <!-- Servomotor SG90 / MG996R azul metálico -->
        <rect x="25" y="-35" width="46" height="55" rx="6" fill="url(#servoGrad)" stroke="#0D47A1" stroke-width="3" />
        <circle cx="48" cy="-10" r="14" fill="#E0E0E0" stroke="#424242" stroke-width="2.5" />
        <!-- Braço defletor articulado -->
        <line x1="48" y1="-10" x2="85" y2="28" stroke="#FF5722" stroke-width="9" stroke-linecap="round" />
        <circle cx="48" cy="-10" r="5" fill="#212121" />
        <circle cx="85" cy="28" r="5" fill="#212121" />
        <!-- Arco de Movimento do Servo -->
        <path d="M 85 5 Q 98 25 85 45" stroke="#FFD54F" stroke-width="3" stroke-dasharray="4 3" />
      </g>
    </g>

    <!-- Torre e Câmera de Inspeção Industrial Superior -->
    <g transform="translate(210, 0)">
      <!-- Haste / Suporte Metálico -->
      <path d="M 45 130 L 45 40 L 95 40" stroke="#78909C" stroke-width="8" stroke-linecap="round" />
      
      <!-- Câmera Industrial (Design Robusto) -->
      <rect x="75" y="20" width="75" height="50" rx="8" fill="#263238" stroke="#37474F" stroke-width="3.5" />
      <!-- Anel óptico / Lente -->
      <rect x="95" y="70" width="35" height="25" rx="4" fill="#455A64" stroke="#263238" stroke-width="2" />
      <ellipse cx="112" cy="95" rx="18" ry="7" fill="#00B0FF" stroke="#01579B" stroke-width="2.5" filter="url(#glow)" />
      <!-- Laser / Feixe de Inspeção cônico -->
      <polygon points="112,98 55,142 170,142" fill="url(#hudLaser)" />
      
      <!-- Sensor Óptico S1 (lateral) -->
      <circle cx="10" cy="115" r="8" fill="#D32F2F" filter="url(#glow)" />
      <text x="10" y="102" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#FF5252" text-anchor="middle">S1</text>
    </g>
  </g>

  <!-- ================= 3. COMPONENTES ELETRÔNICOS (ESP32 E CHIP) ================= -->
  <!-- Placa ESP32 Ilustrada com Riqueza de Detalhes -->
  <g transform="translate(68, 410)" filter="url(#shadow)">
    <rect x="0" y="0" width="220" height="150" rx="14" fill="url(#espGrad)" stroke="#37474F" stroke-width="3.5" />
    
    <!-- Pinos GPIO dourados nas bordas -->
    <g fill="#FFD54F">
      <!-- Pinos esquerda -->
      <rect x="-6" y="15" width="8" height="6" rx="1" />
      <rect x="-6" y="27" width="8" height="6" rx="1" />
      <rect x="-6" y="39" width="8" height="6" rx="1" />
      <rect x="-6" y="51" width="8" height="6" rx="1" />
      <rect x="-6" y="63" width="8" height="6" rx="1" />
      <rect x="-6" y="75" width="8" height="6" rx="1" />
      <rect x="-6" y="87" width="8" height="6" rx="1" />
      <rect x="-6" y="99" width="8" height="6" rx="1" />
      <rect x="-6" y="111" width="8" height="6" rx="1" />
      <rect x="-6" y="123" width="8" height="6" rx="1" />
      <!-- Pinos direita -->
      <rect x="218" y="15" width="8" height="6" rx="1" />
      <rect x="218" y="27" width="8" height="6" rx="1" />
      <rect x="218" y="39" width="8" height="6" rx="1" />
      <rect x="218" y="51" width="8" height="6" rx="1" />
      <rect x="218" y="63" width="8" height="6" rx="1" />
      <rect x="218" y="75" width="8" height="6" rx="1" />
      <rect x="218" y="87" width="8" height="6" rx="1" />
      <rect x="218" y="99" width="8" height="6" rx="1" />
      <rect x="218" y="111" width="8" height="6" rx="1" />
      <rect x="218" y="123" width="8" height="6" rx="1" />
    </g>

    <!-- Antena PCB em zigue-zague metálica -->
    <rect x="20" y="12" width="55" height="38" rx="4" fill="#B0BEC5" stroke="#78909C" stroke-width="2" />
    <path d="M 28 20 L 68 20 M 28 27 L 68 27 L 68 35 L 28 35 M 28 42 L 50 42" stroke="#FFB300" stroke-width="2.5" stroke-linecap="round" />

    <!-- Blindagem metálica do microprocessador ESP-WROOM-32 -->
    <rect x="90" y="18" width="105" height="95" rx="6" fill="#CFD8DC" stroke="#90A4AE" stroke-width="2" />
    <text x="142" y="48" font-family="'Archivo', sans-serif" font-weight="900" font-size="14" fill="#263238" text-anchor="middle">ESP32</text>
    <text x="142" y="66" font-family="sans-serif" font-weight="700" font-size="9" fill="#455A64" text-anchor="middle">DUAL-CORE 240MHz</text>
    <text x="142" y="80" font-family="sans-serif" font-weight="700" font-size="9" fill="#00838F" text-anchor="middle">AUTOMAÇÃO EM TEMPO REAL</text>
    <!-- Logo Espressif estilizado -->
    <circle cx="142" cy="96" r="6" fill="#D32F2F" />

    <!-- LEDs Indicadores (Power & Comunicação Serial) -->
    <circle cx="28" cy="115" r="4.5" fill="#D32F2F" filter="url(#glow)" /> <!-- LED Power Vermelho -->
    <circle cx="45" cy="115" r="4.5" fill="#00E676" filter="url(#glow)" /> <!-- LED Serial Verde -->
    <text x="28" y="132" font-family="sans-serif" font-weight="800" font-size="8" fill="#B0BEC5" text-anchor="middle">PWR</text>
    <text x="45" y="132" font-family="sans-serif" font-weight="800" font-size="8" fill="#B0BEC5" text-anchor="middle">COM</text>

    <!-- Conector Micro-USB -->
    <rect x="95" y="142" width="30" height="12" rx="2" fill="#78909C" stroke="#37474F" stroke-width="1.5" />
    
    <!-- Etiqueta do Componente -->
    <rect x="15" y="-14" width="190" height="24" rx="6" fill="#004D40" stroke="#00E676" stroke-width="1.5" />
    <text x="110" y="3" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#FFFFFF" text-anchor="middle">CONTROLE DE BANCADA</text>
  </g>

  <!-- ================= 4. CARDS DE DESTAQUES & BADGES DE QUALIDADE ================= -->
  <!-- Card Central: Frutos Amazônicos em Destaque -->
  <g transform="translate(320, 395)" filter="url(#shadow)">
    <rect x="0" y="0" width="340" height="175" rx="16" fill="#FFFFFF" fill-opacity="0.15" stroke="#FFFFFF" stroke-width="2.5" />
    
    <text x="170" y="30" font-family="'Archivo', sans-serif" font-weight="900" font-size="15" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">SOCIOBIODIVERSIDADE</text>
    <text x="170" y="50" font-family="sans-serif" font-weight="700" font-size="12" fill="#FFD54F" text-anchor="middle">Tucumã &amp; Castanha-do-Pará</text>
    
    <!-- Ilustração dos Frutos Lado a Lado -->
    <g transform="translate(50, 65)">
      <!-- Tucumã -->
      <circle cx="45" cy="40" r="30" fill="url(#tucumaGrad)" stroke="#4E2000" stroke-width="2.5" />
      <ellipse cx="38" cy="32" rx="6" ry="12" fill="#FFE082" fill-opacity="0.6" />
      <text x="45" y="86" font-family="'Archivo', sans-serif" font-weight="800" font-size="11" fill="#FFFFFF" text-anchor="middle">TUCUMÃ</text>
    </g>

    <g transform="translate(185, 65)">
      <!-- Ouriço e Castanhas -->
      <circle cx="50" cy="40" r="30" fill="#5D4037" stroke="#3E2723" stroke-width="2.5" />
      <ellipse cx="44" cy="34" rx="12" ry="8" fill="#8D6E63" />
      <ellipse cx="58" cy="45" rx="10" ry="7" fill="#A1887F" />
      <text x="50" y="86" font-family="'Archivo', sans-serif" font-weight="800" font-size="11" fill="#FFFFFF" text-anchor="middle">CASTANHA</text>
    </g>

    <!-- Legenda de Valor Agregado -->
    <rect x="25" y="132" width="290" height="28" rx="6" fill="#1B5E20" stroke="#00E676" stroke-width="1.5" />
    <text x="170" y="151" font-family="'Archivo', sans-serif" font-weight="800" font-size="11" fill="#FFFFFF" text-anchor="middle">VALORIZAÇÃO DA SAFRA AMAZÔNICA</text>
  </g>

  <!-- Card Direito: Badges Oficiais das Classes A, B, C -->
  <g transform="translate(695, 395)" filter="url(#shadow)">
    <rect x="0" y="0" width="220" height="175" rx="16" fill="#FFFFFF" fill-opacity="0.15" stroke="#FFFFFF" stroke-width="2.5" />
    <text x="110" y="28" font-family="'Archivo', sans-serif" font-weight="900" font-size="14" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">PADRÕES DE TRIAGEM</text>
    
    <!-- Badge Classe A (Verde) -->
    <g transform="translate(20, 42)">
      <rect x="0" y="0" width="180" height="34" rx="8" fill="#1B5E20" stroke="#00E676" stroke-width="2" />
      <circle cx="20" cy="17" r="10" fill="#00E676" />
      <text x="20" y="22" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#003314" text-anchor="middle">A</text>
      <text x="100" y="17" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#FFFFFF" text-anchor="middle">PADRÃO EXPORTAÇÃO</text>
      <text x="100" y="28" font-family="sans-serif" font-weight="700" font-size="9" fill="#B9F6CA" text-anchor="middle">Aprovado · Saída Direta</text>
    </g>

    <!-- Badge Classe B (Amarelo/Laranja) -->
    <g transform="translate(20, 84)">
      <rect x="0" y="0" width="180" height="34" rx="8" fill="#E65100" stroke="#FFB300" stroke-width="2" />
      <circle cx="20" cy="17" r="10" fill="#FFB300" />
      <text x="20" y="22" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#3E2723" text-anchor="middle">B</text>
      <text x="100" y="17" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#FFFFFF" text-anchor="middle">DEFEITO VISUAL</text>
      <text x="100" y="28" font-family="sans-serif" font-weight="700" font-size="9" fill="#FFE082" text-anchor="middle">Rejeitado · Subprodutos</text>
    </g>

    <!-- Badge Classe C (Vermelho) -->
    <g transform="translate(20, 126)">
      <rect x="0" y="0" width="180" height="34" rx="8" fill="#B71C1C" stroke="#FF5252" stroke-width="2" />
      <circle cx="20" cy="17" r="10" fill="#FF5252" />
      <text x="20" y="22" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#FFFFFF" text-anchor="middle">C</text>
      <text x="100" y="17" font-family="'Archivo', sans-serif" font-weight="900" font-size="11" fill="#FFFFFF" text-anchor="middle">REFUGO / FRAGMENTO</text>
      <text x="100" y="28" font-family="sans-serif" font-weight="700" font-size="9" fill="#FFCDD2" text-anchor="middle">Descarte Automatizado</text>
    </g>
  </g>

  <!-- ================= 5. FAIXA INFERIOR COM DESTAQUES TÉCNICOS ================= -->
  <g transform="translate(40, 595)">
    <!-- 4 Pills de especificações rápidas -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="205" height="60" rx="14" fill="#004D40" stroke="#00E676" stroke-width="2" />
      <text x="102" y="26" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#00E676" text-anchor="middle">VELOCIDADE DE IA</text>
      <text x="102" y="48" font-family="'Archivo', sans-serif" font-weight="900" font-size="18" fill="#FFFFFF" text-anchor="middle">~4 ms / ciclo</text>
    </g>

    <g transform="translate(230, 0)">
      <rect x="0" y="0" width="205" height="60" rx="14" fill="#004D40" stroke="#00E676" stroke-width="2" />
      <text x="102" y="26" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#00E676" text-anchor="middle">PRECISÃO VALIDADA</text>
      <text x="102" y="48" font-family="'Archivo', sans-serif" font-weight="900" font-size="18" fill="#FFFFFF" text-anchor="middle">98.4% de Acerto</text>
    </g>

    <g transform="translate(460, 0)">
      <rect x="0" y="0" width="205" height="60" rx="14" fill="#004D40" stroke="#00E676" stroke-width="2" />
      <text x="102" y="26" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#00E676" text-anchor="middle">REDE NEURAL LOCAL</text>
      <text x="102" y="48" font-family="'Archivo', sans-serif" font-weight="900" font-size="16" fill="#FFFFFF" text-anchor="middle">MobileNetV3 ONNX</text>
    </g>

    <g transform="translate(690, 0)">
      <rect x="0" y="0" width="205" height="60" rx="14" fill="#004D40" stroke="#00E676" stroke-width="2" />
      <text x="102" y="26" font-family="'Archivo', sans-serif" font-weight="900" font-size="12" fill="#00E676" text-anchor="middle">AUTONOMIA TOTAL</text>
      <text x="102" y="48" font-family="'Archivo', sans-serif" font-weight="900" font-size="18" fill="#FFFFFF" text-anchor="middle">100% Offline</text>
    </g>
  </g>
</svg>
`;

async function render() {
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage();
  const outPath = 'C:/Users/ponto/.gemini/antigravity/brain/a479028d-a63f-45e1-b26f-4f749b60fad6/scratch/super_backdrop_panel.png';

  const html = '<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;">' + richBackdropSvg + '</body></html>';
  await page.setContent(html);
  const buffer = await page.locator('svg').screenshot({ omitBackground: true });
  fs.writeFileSync(outPath, buffer);
  console.log('Rendered super backdrop panel ->', outPath, `(${buffer.length} bytes)`);

  await browser.close();
}

render().catch(console.error);
