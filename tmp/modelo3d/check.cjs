const {chromium}=require('C:/Users/ponto/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Users/ponto/.cache/puppeteer/chrome/win64-131.0.6778.204/chrome-win64/chrome.exe',args:['--allow-file-access-from-files','--enable-webgl','--use-angle=swiftshader','--disable-web-security']});
 const page=await browser.newPage({viewport:{width:1600,height:1000},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const requests=[];page.on('request',r=>requests.push(r.url()));
 await page.goto('file:///'+path.resolve('AmazonVision_4_0_Bancada_3D.html').replaceAll('\\','/'),{waitUntil:'load'});
 await page.waitForFunction(()=>window.__amazonvision?.ready,{timeout:60000});
 await page.screenshot({path:'tmp/modelo3d/overview.png'});
 console.log('READY',await page.evaluate(()=>({components:window.__amazonvision.components,...window.__amazonvision.info()})));
 for(const view of ['electronics','inspection','top','front']){await page.locator(`[data-view="${view}"]`).click();await page.screenshot({path:`tmp/modelo3d/${view}.png`});}
 await page.locator('[data-part="12"]').click();console.log('DETAIL',await page.locator('#detailTitle').textContent(),await page.locator('#detail').isVisible());
 await page.screenshot({path:'tmp/modelo3d/esp32.png'});
 await page.locator('[data-view="overview"]').click();await page.locator('#labelsToggle').click();console.log('LABELS_HIDDEN',await page.locator('.hotspot:visible').count());
 const dl=page.waitForEvent('download');await page.locator('#save').click();console.log('EXPORT',(await dl).suggestedFilename());
 await page.locator('#closeDetail').click();await page.setViewportSize({width:390,height:844});await page.locator('[data-view="overview"]').click();await page.screenshot({path:'tmp/modelo3d/mobile.png'});await page.locator('#menu').click();console.log('MOBILE_MENU',await page.locator('aside').isVisible());
 console.log('ERRORS',JSON.stringify(errors));console.log('EXTERNAL_REQUESTS',JSON.stringify(requests.filter(x=>/^https?:/.test(x))));
 await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1);});
