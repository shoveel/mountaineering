// Render an HTML art file to PNG. usage: node render-art.js <in.html> <out.png> <w> <h> [scale]
const path = require('path');
const { chromium } = require('playwright');
const [inp, out, w, h, scale] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +(scale || 1) });
  await page.goto('file://' + path.resolve(inp));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  await page.screenshot({ path: out, omitBackground: true });
  await browser.close();
  console.log('art', out);
})();
