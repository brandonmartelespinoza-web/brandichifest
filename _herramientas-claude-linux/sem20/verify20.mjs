// verify19.mjs — verificación funcional de GUIA-SEM20.html en Chromium real (clicks, no llamadas directas)
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
import fs from 'fs';

const URL = 'http://127.0.0.1:8720/GUIA-SEM20.html';
const TABS = ['cap','boc','len','sal','eso','par','per','est','int','test'];
const out = [];
const ok = (c, m) => { out.push((c ? '✅ ' : '❌ ') + m); };

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
let page = await ctx.newPage();
const errors = [];
page.on('pageerror', e => errors.push('pageerror: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
await page.goto(URL, { waitUntil: 'load' });
await page.evaluate(() => localStorage.clear());
await page.reload({ waitUntil: 'load' });

const clickTab = async t => {
  await page.evaluate(t => [...document.querySelectorAll('nav button')].find(b => (b.getAttribute('onclick') || '').includes("'" + t + "'")).click(), t);
};

// 1. pestañas
for (const t of TABS) {
  await clickTab(t);
  const vis = await page.evaluate(() => [...document.querySelectorAll('.tab-content')].filter(d => getComputedStyle(d).display !== 'none').map(d => d.id));
  ok(vis.length === 1 && vis[0] === 'tab-' + t, `pestaña ${t}: visible ${JSON.stringify(vis)}`);
}

// 2. figuras e imágenes
await page.waitForTimeout(1500);
const figInfo = await page.evaluate(async () => {
  const imgs = [...document.querySelectorAll('figure.fig img')];
  await Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
  return { figs: document.querySelectorAll('figure.fig').length, lee: document.querySelectorAll('figure.fig .lee').length,
    imgs: imgs.length, svgs: document.querySelectorAll('figure.fig svg').length,
    broken: imgs.filter(i => i.naturalWidth === 0).map(i => i.getAttribute('src')),
    svgText: document.querySelectorAll('figure.fig svg text').length };
});
ok(figInfo.figs === figInfo.lee && figInfo.figs === figInfo.imgs + figInfo.svgs, `figuras ${figInfo.figs} = .lee ${figInfo.lee} = img ${figInfo.imgs} + svg ${figInfo.svgs}`);
ok(figInfo.broken.length === 0, `imágenes rotas: ${figInfo.broken.length} ${figInfo.broken.join(',')}`);
const raw = fs.readFileSync('/home/user/brandichifest/SEM 20/GUIA-SEM20.html', 'utf8');
const rawText = (raw.match(/<figure class="fig"[\s\S]*?<\/figure>/g) || []).reduce((a, f) => a + (f.match(/<text[\s>]/g) || []).length, 0);
ok(rawText === figInfo.svgText, `SVG <text>: archivo ${rawText} vs DOM ${figInfo.svgText} (sin breakout)`);

// 3. mini-tests: responder bien clickeando labels y el botón real
const mts = await page.evaluate(() => [...document.querySelectorAll('.mini-test')].map(m => ({ id: m.id, tab: m.closest('.tab-content').id.slice(4) })));
for (const { id, tab } of mts) {
  await clickTab(tab);
  const n = await page.evaluate(id => document.querySelectorAll('#' + id + ' .mt-q').length, id);
  for (let i = 0; i < n; i++) {
    const idx = await page.evaluate(([id, i]) => ({ a: 0, b: 1, c: 2, d: 3 })[document.querySelectorAll('#' + id + ' .mt-q')[i].dataset.correct], [id, i]);
    await page.locator(`#${id} .mt-q >> nth=${i}`).locator('label').nth(idx).click();
  }
  await page.locator(`#${id} > button.btn`).click();
  const score = await page.locator(`#${id}-score .mt-score`).textContent();
  const sema = id.replace('mt-', '');
  const unlocked = await page.evaluate(s => !document.getElementById('sem-' + s).classList.contains('sema-locked'), sema);
  ok(score.startsWith(n + '/' + n) && unlocked, `mini-test ${id}: ${score.trim()} · semáforo ${sema} desbloqueado=${unlocked}`);
}

// 4. semáforos: clic en verde/amarillo y persistencia tras reload
const semas = await page.evaluate(() => [...document.querySelectorAll('.semaforo')].map(s => ({ id: s.id.slice(4), tab: s.closest('.tab-content').id.slice(4) })));
const colors = ['green', 'yellow', 'red'];
for (const [k, { id, tab }] of semas.entries()) {
  await clickTab(tab);
  const c = colors[k % 3];
  await page.locator(`#sem-${id} .sema-btn`).nth(k % 3).click();
  const lbl = await page.locator(`#sema-${id}-lbl`).textContent();
  ok(lbl.length > 0 && await page.locator(`#sem-${id} .sema-btn.active-${c}`).count() === 1, `semáforo ${id} → ${c} (${lbl})`);
}
await page.reload({ waitUntil: 'load' });
const persisted = await page.evaluate((colors) => {
  const r = []; document.querySelectorAll('.semaforo').forEach((s, k) => {
    const c = colors[k % 3]; r.push(!s.classList.contains('sema-locked') && !!s.querySelector('.sema-btn.active-' + c));
  }); return r;
}, colors);
ok(persisted.every(Boolean), `semáforos persisten tras reload: ${persisted.filter(Boolean).length}/${persisted.length}`);
const pct = await page.evaluate(() => [...document.querySelectorAll('.pt-pct')].map(e => e.textContent));
ok(pct.every(p => p === '100%'), `progress trackers: ${pct.join(' ')}`);
await page.waitForTimeout(700); // la barra tiene transition .5s: medir cuando terminó la animación
const barW = await page.evaluate(() => document.getElementById('pt-cap-bar').getBoundingClientRect().width);
ok(barW > 50, `barra de progreso visible (ancho ${Math.round(barW)} px)`);

// 5. drag-drops: orden correcto → ✅ ; invertido → ❌ (clic en el botón real)
const dds = await page.evaluate(() => [...document.querySelectorAll('.dragdrop')].map(d => ({ id: d.id, tab: d.closest('.tab-content').id.slice(4) })));
for (const { id, tab } of dds) {
  await clickTab(tab);
  await page.evaluate(id => { const l = document.getElementById(id + '-list'); [...l.children].sort((a, b) => a.dataset.pos - b.dataset.pos).forEach(x => l.appendChild(x)); }, id);
  await page.locator(`#${id} button.btn`).click();
  const good = await page.locator(`#${id}-result`).textContent();
  await page.evaluate(id => { const l = document.getElementById(id + '-list'); [...l.children].sort((a, b) => b.dataset.pos - a.dataset.pos).forEach(x => l.appendChild(x)); }, id);
  await page.locator(`#${id} button.btn`).click();
  const bad = await page.locator(`#${id}-result`).textContent();
  ok(good.includes('✅') && bad.includes('❌'), `drag-drop ${id}: ordenado "${good.slice(0, 20)}" / desordenado "${bad.slice(0, 12)}"`);
}
// arrastre real con el mouse en uno (HTML5 DnD)
await clickTab('par');
await page.evaluate(() => { const l = document.getElementById('dd-pa1-list'); [...l.children].sort((a, b) => a.dataset.pos - b.dataset.pos).forEach(x => l.appendChild(x)); });
const first = page.locator('#dd-pa1-list .drag-item').nth(0), third = page.locator('#dd-pa1-list .drag-item').nth(2);
await first.dragTo(third);
const orderAfter = await page.evaluate(() => [...document.querySelectorAll('#dd-pa1-list .drag-item')].map(x => x.dataset.pos).join(''));
ok(orderAfter !== '123', `arrastre real con mouse cambia el orden: 123 → ${orderAfter}`);

// 6. test final
await clickTab('test');
const nq = await page.locator('#tab-test .quiz-q').count();
for (let i = 0; i < nq; i++) {
  const idx = await page.evaluate(i => ({ a: 0, b: 1, c: 2, d: 3 })[document.querySelectorAll('#tab-test .quiz-q')[i].dataset.correct], i);
  await page.locator('#tab-test .quiz-q').nth(i).locator('label').nth(idx).click();
}
await page.locator('#tab-test button.btn-primary', { hasText: 'Corregir el test' }).click();
const t1 = await page.locator('#score-title').textContent();
ok(t1.startsWith(nq + '/' + nq) && nq === 40, `test final todo correcto: ${t1.trim()}`);
await page.locator('#score-box button').click();
const checked = await page.evaluate(() => document.querySelectorAll('#tab-test input:checked').length);
const boxHidden = await page.evaluate(() => getComputedStyle(document.getElementById('score-box')).display === 'none');
ok(checked === 0 && boxHidden, `resetTest limpia: ${checked} radios marcados, score oculto=${boxHidden}`);
for (let i = 0; i < nq; i++) {
  const idx = await page.evaluate(i => ({ a: 0, b: 1, c: 2, d: 3 })[document.querySelectorAll('#tab-test .quiz-q')[i].dataset.correct], i);
  const pick = i < 30 ? idx : (idx + 1) % 4;
  await page.locator('#tab-test .quiz-q').nth(i).locator('label').nth(pick).click();
}
await page.locator('#tab-test button.btn-primary', { hasText: 'Corregir el test' }).click();
const t2 = await page.locator('#score-title').textContent();
const fbVis = await page.evaluate(() => [...document.querySelectorAll('#tab-test .feedback')].filter(f => getComputedStyle(f).display !== 'none').length);
ok(t2.startsWith('30/40') && fbVis === 40, `test con 10 errores: ${t2.trim()} · feedbacks visibles ${fbVis}`);
const letters = await page.evaluate(() => { const c = { a: 0, b: 0, c: 0, d: 0 }; document.querySelectorAll('#tab-test .quiz-q').forEach(q => c[q.dataset.correct]++); return c; });
ok(Object.values(letters).every(v => v === 10), `reparto de correctas ${JSON.stringify(letters)}`);

// 7. desborde horizontal a 1280 y 375
for (const w of [1280, 375]) {
  await page.setViewportSize({ width: w, height: 900 });
  const bad = [];
  for (const t of TABS) {
    await clickTab(t);
    const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    if (r.sw !== r.cw) bad.push(`${t}:${r.sw}>${r.cw}`);
  }
  ok(bad.length === 0, `sin scroll horizontal a ${w}px ${bad.join(' ')}`);
}

// 8. consola limpia en pestaña nueva, tras clickear todas las pestañas y dar vuelta todas las flashcards
const p2 = await ctx.newPage();
const err2 = [];
p2.on('pageerror', e => err2.push('pageerror: ' + e.message));
p2.on('console', m => { if (m.type() === 'error') err2.push('console: ' + m.text()); });
await p2.setViewportSize({ width: 1280, height: 900 });
await p2.goto(URL, { waitUntil: 'load' });
page = p2;
let flips = 0;
for (const t of TABS) {
  await clickTab(t);
  const n = await p2.locator(`#tab-${t} .fc`).count();
  for (let i = 0; i < n; i++) { await p2.locator(`#tab-${t} .fc`).nth(i).click(); flips++; }
}
const flipped = await p2.evaluate(() => document.querySelectorAll('.fc.flipped').length);
ok(flipped === flips && flips === 180, `flashcards dadas vuelta: ${flipped}/${flips}`);
ok(err2.length === 0, `consola sin errores (pestaña nueva): ${err2.length} ${err2.slice(0, 3).join(' | ')}`);

await browser.close();
console.log(out.join('\n'));
const fails = out.filter(l => l.startsWith('❌')).length;
console.log(`\n${out.length - fails}/${out.length} controles OK`);
