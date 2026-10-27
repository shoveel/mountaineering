// Approximate local preview of the deck: renders each slide file to a PNG.
// usage: node preview.js <deckRoot> <outDir> [slideId ...]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [root, out, ...only] = process.argv.slice(2);
const deck = JSON.parse(fs.readFileSync(path.join(root, 'project/deck.json'), 'utf8'));
const blobMap = JSON.parse(fs.readFileSync(path.join(root, 'blobmap.json'), 'utf8'));
const faces = Object.values(deck.faces).map(f => f.href ? `<link rel="stylesheet" href="${f.href}">` : '').join('\n');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  fs.mkdirSync(out, { recursive: true });
  const ids = only.length ? only : deck.order;
  for (const id of ids) {
    let html = fs.readFileSync(path.join(root, 'project/slides', id + '.html'), 'utf8');
    html = html.replace(/\/_blob\/([0-9a-f]{32})/g, (m, b) => blobMap[b] ? 'file://' + path.resolve(root, blobMap[b]) : m);
    html = html.replace(/<aside>[\s\S]*?<\/aside>/, '');
    // the deck viewer drops a padding declaration whose values exceed 256px
    html = html.replace(/(<section[^>]*?style="[^"]*?)padding:([^;"]+);?/, (m, pre, v) => v.split(/\s+/).some(x => parseFloat(x) > 256) ? pre : m);
    const doc = `<!doctype html><html><head><meta charset="utf-8">${faces}
<style>*{margin:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden}
section{position:relative;width:1920px;height:1080px;overflow:hidden}
h1,h2,h3,p{margin:0}
table{border-collapse:collapse;width:100%}td,th{padding:.35em .6em;border-bottom:1px solid rgba(128,128,128,.4);vertical-align:top}
x-shape,x-icon{display:block}section>*:not([style*="position:absolute"]){position:relative}</style></head><body>${html}</body></html>`;
    const tmp = path.join(out, '_tmp.html');
    fs.writeFileSync(tmp, doc);
    await page.goto('file://' + path.resolve(tmp));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(out, id + '.png') });
    console.log('rendered', id);
  }
  await browser.close();
})();
