# tmp/pilot/rend.mjs

Рендер страницы в mp4 сегментами по 30 с.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/rend.mjs` рабочей копии. Порядок — в [index.md](index.md).

````js
// usage: bun rend.mjs <page.html> <out-dir> <seconds> [w h]
// JPEG frames piped into ffmpeg, one mp4 segment per 30 s, a fresh Chromium for each. Finished segments are skipped on rerun.
import { chromium } from '/srv/projects/vmsetup/board/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const [page, out, secs, W = 1920, H = 1080] = process.argv.slice(2);
const FPS = 30, CH = 30 * FPS, N = Math.round(+secs * FPS);
const FF = '/home/boardagent/.explainer/bin/ffmpeg';
fs.mkdirSync(out, { recursive: true });
const segs = [];
for (let c = 0; c * CH < N; c++) {
  const seg = path.join(out, `seg${String(c).padStart(2, '0')}.mp4`); segs.push(seg);
  if (fs.existsSync(seg)) continue;
  const tmp = seg + '.part.mp4';
  // a fresh browser per segment keeps Chromium's memory flat
  const br = await chromium.launch({ args: ['--disable-dev-shm-usage', '--disable-gpu', '--allow-file-access-from-files', '--disable-extensions'] });
  const p = await br.newPage({ viewport: { width: +W, height: +H } });
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load', timeout: 90000 });
  await p.evaluate(() => document.fonts.ready);
  const ff = spawn(FF, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-tune', 'grain', '-crf', '26', '-pix_fmt', 'yuv420p', '-threads', '2', '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((ok, bad) => ff.on('exit', (code) => (code === 0 ? ok() : bad(new Error('ffmpeg exit ' + code)))));
  const t0 = Date.now();
  for (let f = c * CH; f < Math.min(N, (c + 1) * CH); f++) {
    await p.evaluate((t) => render(t), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await done; await br.close(); fs.renameSync(tmp, seg);
  console.log(path.basename(seg), ((Date.now() - t0) / 1000).toFixed(0) + 's');
}
fs.writeFileSync(path.join(out, 'list.txt'), segs.map((s) => `file '${path.basename(s)}'`).join('\n') + '\n');
console.log('done', N, 'frames');
````
