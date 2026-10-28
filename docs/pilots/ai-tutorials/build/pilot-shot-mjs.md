# tmp/pilot/shot.mjs

Один кадр страницы в PNG.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/shot.mjs` рабочей копии. Порядок — в [index.md](index.md).

````js
// usage: bun shot.mjs <page.html> <out.png> <w> <h> — one still screenshot after fonts load
import { chromium } from '/srv/projects/vmsetup/board/node_modules/playwright/index.mjs';
import path from 'node:path';
const [page, out, w, h] = process.argv.slice(2);
const br = await chromium.launch({ args: ['--disable-dev-shm-usage', '--disable-gpu', '--allow-file-access-from-files', '--disable-extensions'] });
const p = await br.newPage({ viewport: { width: +w, height: +h } });
await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 90000 });
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: out });
await br.close();
````
