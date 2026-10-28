# tmp/mock/shot.mjs

Снимки страниц макетов.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/shot.mjs` рабочей копии. Порядок — в [index.md](index.md).

````js
// usage: bun shot.mjs <out-dir> <width> <page.html>...  full-page PNG screenshots
import { chromium } from '/srv/projects/vmsetup/board/node_modules/playwright/index.mjs';
import path from 'node:path';
const [out, w, ...pages] = process.argv.slice(2);
const b = await chromium.launch({ args: ['--single-process', '--no-zygote', '--disable-dev-shm-usage', '--disable-gpu', '--allow-file-access-from-files', '--disable-extensions', '--js-flags=--max-old-space-size=256'] });
const p = await b.newPage({ viewport: { width: Number(w), height: 900 } });
for (const f of pages) {
  await p.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 90000 });
  await p.evaluate(() => document.fonts.ready);
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  await p.screenshot({ path: path.join(out, path.basename(f, '.html') + '-' + w + '.png'), fullPage: true, timeout: 90000 });
  console.log(f, 'scrollWidth', sw);
}
await b.close();
````
