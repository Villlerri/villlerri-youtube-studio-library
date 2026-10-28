# tmp/mock/cap.mjs

Снимки макетов по частям для альбомов.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/cap.mjs` рабочей копии. Порядок — в [index.md](index.md).

````js
// usage: bun cap.mjs <page.html> <out-dir> <fps> <t0> <t1> | bun cap.mjs <page.html> <out-dir> list <t,t,...>
import { chromium } from '/srv/projects/vmsetup/board/node_modules/playwright/index.mjs';
import path from 'node:path';
const [page, out, fps, a, b] = process.argv.slice(2);
const ts = fps === 'list' ? a.split(',').map(Number) : Array.from({ length: Math.round((b - a) * fps) }, (_, i) => +a + i / fps);
const br = await chromium.launch({ args: ['--disable-dev-shm-usage', '--disable-gpu', '--allow-file-access-from-files', '--disable-extensions'] });
const p = await br.newPage({ viewport: { width: +(process.env.VW || 1920), height: +(process.env.VH || 1080) } });
await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 90000 });
await p.evaluate(() => document.fonts.ready);
let i = 0;
for (const t of ts) {
  await p.evaluate((t) => render(t), t);
  const n = fps === 'list' ? 't' + t.toFixed(2) : String(i).padStart(4, '0');
  await p.screenshot({ path: path.join(out, n + '.png') }); i++;
}
await br.close(); console.log(i, 'frames');
````
