import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 375, height: 800 } });
await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
const p = await ctx.newPage(); await p.goto('http://127.0.0.1:8720/GUIA-SEM20.html', { waitUntil: 'load' });
await p.evaluate(() => [...document.querySelectorAll('nav button')].find(b => (b.getAttribute('onclick')||'').includes("'sal'")).click());
const r = await p.evaluate(() => [...document.querySelectorAll('#tab-sal *')].filter(e => { const x = e.getBoundingClientRect(); return x.right > 376 && !e.closest('.tbl-wrap table'); }).slice(0, 8).map(e => e.tagName + '.' + e.className + ' right=' + Math.round(e.getBoundingClientRect().right) + ' ' + (e.textContent||'').slice(0,50)));
console.log(r.join('\n')); await b.close();
