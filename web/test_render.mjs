import { chromium } from '@playwright/test';

async function test() {
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage();
  await page.setContent('<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="none" /></svg>');
  const buffer = await page.locator('svg').screenshot({ omitBackground: true });
  await browser.close();
  console.log('Success, buffer length:', buffer.length);
}

test().catch(console.error);
