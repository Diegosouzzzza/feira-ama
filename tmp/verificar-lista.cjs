const { chromium } = require('C:/Users/ponto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { resolve } = require('node:path');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Users/ponto/.cache/puppeteer/chrome/win64-131.0.6778.204/chrome-win64/chrome.exe',
    args: ['--allow-file-access-from-files', '--enable-webgl', '--use-angle=swiftshader']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('file:///' + resolve('Lista_de_Materiais_AmazonVision.html').replaceAll('\\', '/'));
  const result = await page.evaluate(() => ({
    title: document.title,
    rows: document.querySelectorAll('tbody tr').length,
    essential: document.querySelectorAll('tbody tr[data-status="Essencial"]').length,
    sections: document.querySelectorAll('.section').length
  }));
  await page.screenshot({ path: 'tmp/lista-materiais-preview.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  const mobile = await page.evaluate(() => ({
    fitsViewport: document.documentElement.scrollWidth <= window.innerWidth,
    rowDisplay: getComputedStyle(document.querySelector('tbody tr')).display,
    viewportWidth: window.innerWidth,
    pageWidth: document.documentElement.scrollWidth
  }));
  await page.screenshot({ path: 'tmp/lista-materiais-mobile.png', fullPage: true });
  await page.screenshot({ path: 'tmp/lista-materiais-mobile-inicio.png' });
  console.log(JSON.stringify({ result, mobile, errors }));
  await browser.close();
  if (errors.length || result.rows < 40 || result.sections !== 5 || !mobile.fitsViewport || mobile.rowDisplay !== 'block') process.exit(1);
})().catch(error => { console.error(error); process.exit(1); });
