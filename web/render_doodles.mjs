import fs from 'fs';
import path from 'path';
import { chromium } from '@playwright/test';

const svgs = {
  step02_conveyor: `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="800" height="600" fill="none" stroke="#222222" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <line x1="80" y1="190" x2="60" y2="260" stroke-width="5" />
  <line x1="120" y1="195" x2="105" y2="260" stroke-width="4" />
  <line x1="280" y1="195" x2="295" y2="260" stroke-width="4" />
  <line x1="320" y1="190" x2="340" y2="260" stroke-width="5" />
  <line x1="75" y1="235" x2="325" y2="235" stroke-width="3" stroke-dasharray="8 6" />

  <ellipse cx="80" cy="170" rx="20" ry="30" stroke-width="4.5" fill="#FAF6EE" />
  <path d="M 320 140 C 335 140, 345 155, 345 170 C 345 185, 335 200, 320 200" stroke-width="4.5" fill="#FAF6EE" />

  <path d="M 80 140 L 320 140 C 332 140, 340 152, 340 170 L 320 200 L 80 200" stroke-width="4.5" />
  <path d="M 80 140 C 68 140, 60 153, 60 170 C 60 187, 68 200, 80 200" stroke-width="4.5" />
  
  <line x1="130" y1="145" x2="115" y2="195" stroke-width="2.5" />
  <line x1="175" y1="145" x2="160" y2="195" stroke-width="2.5" />
  <line x1="225" y1="145" x2="210" y2="195" stroke-width="2.5" />
  <line x1="270" y1="145" x2="255" y2="195" stroke-width="2.5" />

  <path d="M 120 215 L 180 215 M 170 210 L 180 215 L 170 220" stroke-width="3" />

  <ellipse cx="195" cy="130" rx="32" ry="28" stroke-width="4.5" fill="#FAF6EE" />
  <path d="M 175 120 C 180 135, 205 145, 215 135" stroke-width="2.5" />
  <path d="M 185 110 C 190 115, 200 118, 208 112" stroke-width="2" />

  <path d="M 285 170 L 285 45 L 210 45" stroke-width="5" />
  <line x1="285" y1="80" x2="265" y2="45" stroke-width="3" />
  <rect x="180" y="35" width="30" height="20" rx="3" stroke-width="4" fill="#222222" />
  <path d="M 190 55 L 190 62 L 200 62 L 200 55" stroke-width="3" fill="#222222" />
  
  <line x1="195" y1="65" x2="175" y2="115" stroke-width="2.5" stroke-dasharray="5 4" />
  <line x1="195" y1="65" x2="215" y2="115" stroke-width="2.5" stroke-dasharray="5 4" />
  
  <path d="M 183 85 C 195 89, 207 89, 217 85" stroke-width="2" stroke-dasharray="3 3" />
  <path d="M 177 100 C 195 106, 215 106, 223 100" stroke-width="2.5" stroke-dasharray="3 3" />
  
  <text x="145" y="48" font-family="sans-serif" font-weight="900" font-size="16" fill="#222222" stroke="none">S1</text>
</svg>
`,

  step03_camera_ai: `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="800" height="600" fill="none" stroke="#222222" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <rect x="130" y="30" width="140" height="85" rx="8" stroke-width="5" fill="#FAF6EE" />
  <line x1="145" y1="30" x2="145" y2="50" stroke-width="3" />
  <line x1="160" y1="30" x2="160" y2="50" stroke-width="3" />
  <line x1="175" y1="30" x2="175" y2="50" stroke-width="3" />
  <path d="M 270 50 L 290 50 L 290 95 L 270 95" stroke-width="4" />
  <path d="M 290 72 C 315 72, 320 95, 335 105" stroke-width="3.5" />

  <path d="M 170 115 L 160 145 L 240 145 L 230 115 Z" stroke-width="4.5" fill="#222222" />
  <ellipse cx="200" cy="145" rx="40" ry="12" stroke-width="4.5" fill="#FAF6EE" />
  <ellipse cx="200" cy="145" rx="22" ry="6" stroke-width="3" fill="#222222" />

  <path d="M 115 180 L 95 180 L 95 200" stroke-width="4.5" />
  <path d="M 285 180 L 305 180 L 305 200" stroke-width="4.5" />
  <path d="M 95 255 L 95 275 L 115 275" stroke-width="4.5" />
  <path d="M 305 255 L 305 275 L 285 275" stroke-width="4.5" />
  <line x1="95" y1="180" x2="305" y2="180" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="95" y1="275" x2="305" y2="275" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="95" y1="180" x2="95" y2="275" stroke-width="2" stroke-dasharray="6 6" />
  <line x1="305" y1="180" x2="305" y2="275" stroke-width="2" stroke-dasharray="6 6" />

  <ellipse cx="200" cy="230" rx="45" ry="32" stroke-width="4.5" fill="#FAF6EE" />
  <path d="M 180 220 C 190 235, 215 240, 225 225" stroke-width="2.5" />

  <rect x="180" y="165" width="125" height="26" rx="4" stroke-width="3" fill="#222222" />
  <text x="187" y="183" font-family="sans-serif" font-weight="800" font-size="12" fill="#FFFFFF" stroke="none">CLASSE A · 98%</text>

  <line x1="160" y1="150" x2="105" y2="210" stroke-width="2" stroke-dasharray="4 4" />
  <line x1="240" y1="150" x2="295" y2="210" stroke-width="2" stroke-dasharray="4 4" />
</svg>
`,

  step04_diverter: `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="800" height="600" fill="none" stroke="#222222" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <path d="M 60 120 L 200 120" stroke-width="4.5" />
  <path d="M 60 180 L 170 180" stroke-width="4.5" />

  <path d="M 230 85 L 340 50" stroke-width="4.5" />
  <path d="M 200 120 L 320 85" stroke-width="4.5" />
  <path d="M 330 65 L 360 55 M 345 50 L 360 55 L 350 70" stroke-width="3.5" />
  <text x="260" y="40" font-family="sans-serif" font-weight="800" font-size="13" fill="#222222" stroke="none">APROVADO (A)</text>

  <path d="M 170 180 L 310 245" stroke-width="4.5" />
  <path d="M 215 210 L 330 270" stroke-width="4.5" />
  <path d="M 325 245 L 350 260 M 345 245 L 350 260 L 335 268" stroke-width="3.5" />
  <text x="250" y="285" font-family="sans-serif" font-weight="800" font-size="13" fill="#222222" stroke="none">REJEITADO (B/C)</text>

  <rect x="180" y="125" width="45" height="45" rx="6" stroke-width="4.5" fill="#FAF6EE" />
  <circle cx="202" cy="147" r="12" stroke-width="4" fill="#222222" />
  <path d="M 180 145 C 160 145, 150 160, 140 160" stroke-width="3" />

  <path d="M 202 147 L 255 105" stroke-width="8" stroke="#222222" stroke-linecap="round" />
  <path d="M 245 90 C 260 115, 255 145, 235 165" stroke-width="2.5" stroke-dasharray="5 5" />
  <path d="M 235 155 L 235 165 L 245 165" stroke-width="2.5" />

  <circle cx="120" cy="150" r="18" stroke-width="4" fill="#FAF6EE" />
  <path d="M 115 145 C 120 152, 128 152, 130 145" stroke-width="2" />
</svg>
`,

  step05_dashboard: `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="800" height="600" fill="none" stroke="#222222" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
  <rect x="60" y="30" width="280" height="190" rx="12" stroke-width="5" fill="#FAF6EE" />
  <line x1="60" y1="65" x2="340" y2="65" stroke-width="3.5" />
  <circle cx="80" cy="48" r="4" fill="#222222" stroke="none" />
  <circle cx="95" cy="48" r="4" fill="#222222" stroke="none" />
  <circle cx="110" cy="48" r="4" fill="#222222" stroke="none" />
  <text x="135" y="53" font-family="sans-serif" font-weight="800" font-size="12" fill="#222222" stroke="none">AMAZONVISION · MODULO FEIRA</text>

  <rect x="80" y="80" width="70" height="45" rx="6" stroke-width="3" />
  <text x="90" y="98" font-family="sans-serif" font-weight="600" font-size="10" fill="#222222" stroke="none">TOTAL</text>
  <text x="90" y="117" font-family="sans-serif" font-weight="900" font-size="16" fill="#222222" stroke="none">1.250</text>

  <rect x="165" y="80" width="70" height="45" rx="6" stroke-width="3" />
  <text x="175" y="98" font-family="sans-serif" font-weight="600" font-size="10" fill="#222222" stroke="none">APROV.</text>
  <text x="175" y="117" font-family="sans-serif" font-weight="900" font-size="16" fill="#222222" stroke="none">94%</text>

  <rect x="250" y="80" width="70" height="45" rx="6" stroke-width="3" />
  <text x="260" y="98" font-family="sans-serif" font-weight="600" font-size="10" fill="#222222" stroke="none">REJEIT.</text>
  <text x="260" y="117" font-family="sans-serif" font-weight="900" font-size="16" fill="#222222" stroke="none">6%</text>

  <line x1="80" y1="195" x2="210" y2="195" stroke-width="3" />
  <line x1="80" y1="195" x2="80" y2="140" stroke-width="3" />
  <rect x="100" y="150" width="22" height="45" stroke-width="2.5" fill="#222222" />
  <rect x="135" y="175" width="22" height="20" stroke-width="2.5" fill="#888888" />
  <rect x="170" y="183" width="22" height="12" stroke-width="2.5" fill="#DDDDDD" />
  <text x="106" y="210" font-family="sans-serif" font-weight="700" font-size="10" fill="#222222" stroke="none">A</text>
  <text x="141" y="210" font-family="sans-serif" font-weight="700" font-size="10" fill="#222222" stroke="none">B</text>
  <text x="176" y="210" font-family="sans-serif" font-weight="700" font-size="10" fill="#222222" stroke="none">C</text>

  <circle cx="270" cy="165" r="28" stroke-width="3.5" />
  <path d="M 258 165 L 267 174 L 285 156" stroke-width="4" />
  <text x="245" y="208" font-family="sans-serif" font-weight="700" font-size="9" fill="#222222" stroke="none">AUDITADO</text>

  <path d="M 180 220 L 170 260 L 230 260 L 220 220" stroke-width="4.5" fill="#FAF6EE" />
  <line x1="150" y1="260" x2="250" y2="260" stroke-width="5" />
</svg>
`
};

async function render() {
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage();
  const outDir = 'C:/Users/ponto/.gemini/antigravity/brain/a479028d-a63f-45e1-b26f-4f749b60fad6/scratch';

  for (const [key, svg] of Object.entries(svgs)) {
    const html = '<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;">' + svg + '</body></html>';
    await page.setContent(html);
    const buffer = await page.locator('svg').screenshot({ omitBackground: true });
    const filePath = path.join(outDir, `${key}.png`);
    fs.writeFileSync(filePath, buffer);
    console.log(`Rendered ${key} -> ${filePath} (${buffer.length} bytes)`);
  }

  await browser.close();
}

render().catch(console.error);
