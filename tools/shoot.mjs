import { createRequire } from 'module';
const require = createRequire('/Users/davidslv/projects/dsl/lockstep/package.json');
const { chromium, webkit, devices } = require('playwright');
const out = process.argv[2] || '/tmp';
const url = process.argv[3] || 'http://localhost:4012/';
for (const [tag, eng, opts] of [['desktop', chromium, { viewport: { width: 1440, height: 900 } }], ['phone', webkit, devices['iPhone 14 Pro']]]) {
  const b = await eng.launch(); const p = await (await b.newContext(opts)).newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => errs.push('failed ' + r.url()));
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: 'main .block { content-visibility: visible !important; }' }); await p.evaluate(async () => { document.querySelectorAll('img').forEach(i => i.loading = 'eager'); await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  await p.screenshot({ path: `${out}/${tag}-top.png` });
  await p.screenshot({ path: `${out}/${tag}-full.png`, fullPage: true });
  console.log(tag, 'overflow', await p.evaluate(() => document.documentElement.scrollWidth - innerWidth), 'errors', errs, 'font', await p.evaluate(() => document.fonts.check('300 40px Newsreader')));
  await b.close();
}
