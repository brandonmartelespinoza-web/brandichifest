import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const OUT = process.argv[2] || '/home/user/w20/audit';
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
const p = await ctx.newPage(); await p.goto('http://127.0.0.1:8720/GUIA-SEM20.html', { waitUntil: 'load' }); await p.addStyleTag({ content: 'nav{position:static!important}' });
const rep = [];
for (const t of ['cap','boc','len','sal','eso','par','per','est','int']) {
  await p.evaluate(t => [...document.querySelectorAll('nav button')].find(b => (b.getAttribute('onclick')||'').includes("'"+t+"'")).click(), t);
  const n = await p.locator(`#tab-${t} figure.fig`).count();
  for (let i = 0; i < n; i++) {
    const f = p.locator(`#tab-${t} figure.fig`).nth(i);
    const tag = (await f.locator('.fig-tag').textContent()).replace('Figura ','').padStart(2,'0');
    const hasImg = await f.locator('img').count();
    const el = hasImg ? f.locator('img') : f.locator('svg');
    await el.scrollIntoViewIfNeeded();
    const info = hasImg ? await el.evaluate(i => ({ src: (i.getAttribute('data-file') || i.getAttribute('src')).replace('img/',''), nw: i.naturalWidth, dw: Math.round(i.getBoundingClientRect().width) })) : { src: 'svg', nw: 0, dw: 0 };
    rep.push(`${tag} ${t} ${info.src} natural=${info.nw} mostrado=${info.dw}${info.nw && info.dw > info.nw*1.05 ? '  ⚠ AMPLIADA' : ''}`);
    await el.screenshot({ path: `${OUT}/f${tag}-${info.src.replace(/\.(jpg|png)$/,'')}.png` });
  }
}
console.log(rep.join('\n'));
await b.close();
