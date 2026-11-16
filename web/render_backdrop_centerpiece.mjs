import fs from 'fs';
import path from 'path';
import { chromium } from '@playwright/test';

const backdropCenterpiece = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="1800" height="640" fill="none">
  <!-- Card 1: Frutos Amazônicos -->
  <g transform="translate(10, 20)">
    <rect x="0" y="0" width="270" height="260" rx="20" fill="#FFFFFF" fill-opacity="0.12" stroke="#FFFFFF" stroke-width="3" />
    <!-- Ícone Fruto / Folha -->
    <circle cx="135" cy="65" r="34" fill="#FFFFFF" fill-opacity="0.2" />
    <path d="M 120 75 C 115 50, 140 45, 150 55 C 155 70, 135 85, 120 75 Z" fill="#FFFFFF" />
    <path d="M 125 72 L 145 58" stroke="#596700" stroke-width="2.5" />
    
    <text x="135" y="130" font-family="'Archivo', 'Arial Black', sans-serif" font-weight="900" font-size="20" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">BIOECONOMIA</text>
    <text x="135" y="160" font-family="sans-serif" font-weight="800" font-size="16" fill="#F4F1EA" text-anchor="middle">Tucumã &amp; Castanha</text>
    <line x1="50" y1="180" x2="220" y2="180" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="2" />
    <text x="135" y="210" font-family="sans-serif" font-weight="600" font-size="14" fill="#E2DDD2" text-anchor="middle">Classificação de Qualidade</text>
    <text x="135" y="232" font-family="sans-serif" font-weight="700" font-size="13" fill="#FFFFFF" text-anchor="middle">Padrões: Classes A · B · C</text>
  </g>

  <!-- Card 2: Inteligência Artificial Local -->
  <g transform="translate(315, 20)">
    <rect x="0" y="0" width="270" height="260" rx="20" fill="#FFFFFF" fill-opacity="0.18" stroke="#FFFFFF" stroke-width="3.5" />
    <!-- Ícone Câmera / IA -->
    <circle cx="135" cy="65" r="34" fill="#FFFFFF" fill-opacity="0.25" />
    <rect x="115" y="52" width="40" height="28" rx="6" fill="#FFFFFF" />
    <circle cx="135" cy="66" r="8" fill="#596700" />
    <circle cx="147" cy="58" r="3" fill="#596700" />
    
    <text x="135" y="130" font-family="'Archivo', 'Arial Black', sans-serif" font-weight="900" font-size="20" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">EDGE AI LOCAL</text>
    <text x="135" y="160" font-family="sans-serif" font-weight="800" font-size="16" fill="#F4F1EA" text-anchor="middle">MobileNetV3 · ONNX</text>
    <line x1="50" y1="180" x2="220" y2="180" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="2" />
    <text x="135" y="210" font-family="sans-serif" font-weight="600" font-size="14" fill="#E2DDD2" text-anchor="middle">Inferência Rápida: ~4 ms</text>
    <text x="135" y="232" font-family="sans-serif" font-weight="700" font-size="13" fill="#FFFFFF" text-anchor="middle">100% Offline · Sem Nuvem</text>
  </g>

  <!-- Card 3: Automação & Rastreabilidade -->
  <g transform="translate(620, 20)">
    <rect x="0" y="0" width="270" height="260" rx="20" fill="#FFFFFF" fill-opacity="0.12" stroke="#FFFFFF" stroke-width="3" />
    <!-- Ícone Engrenagem / Chip ESP32 -->
    <circle cx="135" cy="65" r="34" fill="#FFFFFF" fill-opacity="0.2" />
    <rect x="121" y="51" width="28" height="28" rx="4" fill="#FFFFFF" />
    <line x1="125" y1="46" x2="125" y2="51" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <line x1="135" y1="46" x2="135" y2="51" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <line x1="145" y1="46" x2="145" y2="51" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <line x1="125" y1="79" x2="125" y2="84" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <line x1="135" y1="79" x2="135" y2="84" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    <line x1="145" y1="79" x2="145" y2="84" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" />
    
    <text x="135" y="130" font-family="'Archivo', 'Arial Black', sans-serif" font-weight="900" font-size="20" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">AUTOMAÇÃO</text>
    <text x="135" y="160" font-family="sans-serif" font-weight="800" font-size="16" fill="#F4F1EA" text-anchor="middle">ESP32 + Servomotor</text>
    <line x1="50" y1="180" x2="220" y2="180" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="2" />
    <text x="135" y="210" font-family="sans-serif" font-weight="600" font-size="14" fill="#E2DDD2" text-anchor="middle">Desvio Mecânico Seletivo</text>
    <text x="135" y="232" font-family="sans-serif" font-weight="700" font-size="13" fill="#FFFFFF" text-anchor="middle">Auditoria em Banco SQLite</text>
  </g>
</svg>
`;

async function render() {
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage();
  const outPath = 'C:/Users/ponto/.gemini/antigravity/brain/a479028d-a63f-45e1-b26f-4f749b60fad6/scratch/backdrop_centerpiece.png';

  const html = '<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;">' + backdropCenterpiece + '</body></html>';
  await page.setContent(html);
  const buffer = await page.locator('svg').screenshot({ omitBackground: true });
  fs.writeFileSync(outPath, buffer);
  console.log('Rendered backdrop centerpiece ->', outPath, `(${buffer.length} bytes)`);

  await browser.close();
}

render().catch(console.error);
