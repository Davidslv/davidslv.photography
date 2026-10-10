import { createRequire } from 'module';
const require = createRequire('/Users/davidslv/projects/dsl/lockstep/package.json');
const { chromium, webkit, devices } = require('playwright');
const base = process.argv[2] || 'http://localhost:4012';
const lum = c => { const [r, g, b] = c.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * r + .7152 * g + .0722 * b; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return ((x + .05) / (y + .05)).toFixed(2); };
for (const path of ['/', '/sunday/']) {
  const b = await webkit.launch(); const p = await (await b.newContext(devices['iPhone 14 Pro'])).newPage();
  await p.goto(base + path, { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => {
    const out = {};
    const sample = sel => [...document.querySelectorAll(sel)].slice(0, 1).map(e => { const s = getComputedStyle(e); return { sel, size: s.fontSize, color: s.color, weight: s.fontWeight }; })[0];
    out.text = ['.lbl', 'figcaption', '.part .sub', '.about p', '.more p', 'footer', 'header.site nav a', '.book-text p'].map(sample).filter(Boolean);
    out.targets = [...document.querySelectorAll('a, button')].map(a => { const r = a.getBoundingClientRect(); return { t: (a.textContent || '').trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) }; }).filter(x => x.w && (x.w < 24 || x.h < 24));
    out.headings = [...document.querySelectorAll('h1,h2,h3')].map(h => h.tagName + ' ' + h.textContent.trim().slice(0, 40));
    out.bg = getComputedStyle(document.body).backgroundColor;
    return out;
  });
  console.log('\n==', path, 'phone');
  for (const t of r.text) console.log(t.sel.padEnd(20), t.size, 'w' + t.weight, 'contrast', ratio(t.color, r.bg));
  console.log('small tap targets (<24px):', JSON.stringify(r.targets.slice(0, 12)));
  console.log('headings:', r.headings.join(' | '));
  await b.close();
}
// keyboard: tab through first 6 stops on desktop, check focus is visible
const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
await p.goto(base + '/sunday/');
for (let i = 0; i < 6; i++) { await p.keyboard.press('Tab'); console.log('tab', i + 1, await p.evaluate(() => { const e = document.activeElement; const s = getComputedStyle(e); return e.tagName + ' "' + e.textContent.trim().slice(0, 30) + '" outline=' + s.outlineStyle + ' ' + s.outlineWidth; })); }
// 200% zoom overflow
await p.setViewportSize({ width: 640, height: 800 }); await p.goto(base + '/'); 
console.log('reflow at 320 css px:', await p.evaluate(() => { document.body.style.zoom = '2'; return document.documentElement.scrollWidth > innerWidth + 1 ? 'horizontal scroll' : 'ok'; }));
await b.close();
