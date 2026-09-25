// svgshot.mjs frag.html out-prefix — captura cada <svg> del fragmento para revisar rótulos
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
import fs from 'fs';
const h = fs.readFileSync(process.argv[2], 'utf8');
const svgs = h.match(/<svg[\s\S]*?<\/svg>/g) || [];
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 900, height: 800 } });
for (const [i, s] of svgs.entries()) {
  await p.setContent(`<html><head><style>.fig-svg text{font-family:'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif}</style></head><body style="margin:0">${s.replace(/width="100%"/, 'width="860"')}</body></html>`);
  await p.locator('svg').screenshot({ path: `${process.argv[3]}-${i}.png` });
}
console.log(svgs.length, 'svg'); await b.close();
