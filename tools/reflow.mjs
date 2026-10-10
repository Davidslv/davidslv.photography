import { createRequire } from 'module';
const require = createRequire('/Users/davidslv/projects/dsl/lockstep/package.json');
const { chromium } = require('playwright');
const b = await chromium.launch();
for (const path of ['/', '/sunday/']) {
  const p = await (await b.newContext({ viewport: { width: 320, height: 640 } })).newPage();
  await p.goto('http://localhost:4012' + path, { waitUntil: 'networkidle' });
  console.log(path, await p.evaluate(() => {
    const over = document.documentElement.scrollWidth - innerWidth;
    const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).slice(0, 4).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right));
    return { over, wide };
  }));
  // nav over the bright hero: sample pixels behind the nav
  await p.setViewportSize({ width: 390, height: 844 }); await p.goto('http://localhost:4012' + path, { waitUntil: 'networkidle' });
  await p.screenshot({ path: `/tmp/hero${path === '/' ? 'home' : 'sun'}.png`, clip: { x: 0, y: 0, width: 390, height: 120 } });
}
await b.close();
