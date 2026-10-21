# Код ролика: часы GPS и Эйнштейн

Весь код, из которого собран ролик, Shorts, обложки, звук и субтитры. Файлы лежат здесь по разделам: заголовок раздела — путь файла.

## Как пересобрать

1. Разложить блоки по файлам в папку `prod/` с теми же путями. Шрифты и вырезки набора задачи 58 — в `prod/kit/` ([набор стиля](../../physics-research/style-kit/README.md)). Вырезки ролика — `assets/p/` этой папки, в `prod/assets/p/`.
2. Зависимости: bun, playwright-core 1.56.1 и chrome-headless-shell в `prod/js/`; Python с numpy, scipy, pillow, opencv-python-headless; ffmpeg. Пути к chromium и ffmpeg в `capture3.mjs` и `check3.mjs` поправить под место.
3. Текст: `python gps/narr.py script.md gps/narration.txt`, затем `python tools/timing.py gps/narration.txt gps/timing`. С голосом: добавить `--voice <папка с метками ElevenLabs>`.
4. Страница: `python gps/build.py`. Проверка: `bun tools/check3.mjs gps/gps.html` должна напечатать CLEAN.
5. Кадры: `bun tools/capture3.mjs gps/gps.html gps/segs <кадров>`; сегменты склеить `ffmpeg -f concat -c copy`.
6. Звук: `bun tools/info.mjs gps/gps.html gps/events.json`, `python gps/music_plan.py gps/events.json gps/plan.json`, `python tools/sound2.py gps/events.json gps/plan.json gps/snd [gps/timing/narration.json]`. Последний аргумент приглушает музыку под голос.
7. Shorts: `python gps/build_short.py short1`, дальше те же шаги с `--w 1080 --h 1920`.

## lib/chalk.js

Библиотека доски: мел, вырезки, губка, камера, таймлайн. Сделана из набора задачи 58.

```js
// Chalkboard style kit (task 58) as a library: the same filters, board, chalk writing, cut-outs, tape,
// eraser and camera push as chalk-clip.html, generalised to many scenes. A video page builds its DOM
// (.sc scenes with .ck text, svg.draw paths, .cw cut-outs), registers its timeline with Chalk.at / Chalk.cut /
// Chalk.scene, then calls Chalk.start(). Deterministic: no clock, every frame is a pure function of its index.
const Chalk = (() => {
  const NS = 'http://www.w3.org/2000/svg';
  const $ = id => document.getElementById(id);
  const el = (p, t, a) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); p.appendChild(e); return e; };
  const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const out3 = u => 1 - Math.pow(1 - cl(u), 3);
  const outBack = (u, k = 1.7) => { u = cl(u) - 1; return 1 + (k + 1) * u * u * u + k * u * u; };
  const smooth = u => { u = cl(u); return u * u * (3 - 2 * u); };
  const rng = seed => { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; };

  const TL = [], EV = [], CUT = {}, SC = [];
  const cfg = { fps: 30, frames: 0, erase: 0.9, w: 1920, h: 1080, formulas: [], formulasPerScene: 45, texSeed: 77 };
  const at = (t, d, kind, id, x = {}) => { const e = { t, d, kind, id, ...x }; TL.push(e); return e; };
  const cut = (id, c) => { CUT[id] = c; };
  // scene: [id, start, erase start]; opts.push = camera push (scale gain), opts.pushDur, opts.pan = [[t, x, y], ...]
  const scene = (id, t0, te, opts = {}) => SC.push({ id, t0, te, push: 0.02, pushDur: 18, ...opts });
  const event = (t, k, x = {}) => EV.push({ t, k, ...x });

  function chrome(o = {}) {
    Object.assign(cfg, o); const W = cfg.w, H = cfg.h;
    document.documentElement.style.width = document.body.style.width = W + 'px';
    document.documentElement.style.height = document.body.style.height = H + 'px';
    document.body.insertAdjacentHTML('afterbegin', `
<svg width="0" height="0" style="position:absolute">
 <filter id="chalk" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -2.4 1.75" result="holes"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="9" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="3.5" result="d"/>
  <feComposite in="d" in2="holes" operator="in"/>
 </filter>
 <filter id="chalkT" x="-12%" y="-35%" width="130%" height="170%">
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -2.4 1.75" result="holes"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="9" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="3.5" result="d"/>
  <feComposite in="d" in2="holes" operator="in"/>
 </filter>
 <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="2"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .07 0"/></filter>
</svg>
<div class="board"></div>
<svg class="dust" width="${W}" height="${H}"><rect width="${W}" height="${H}" filter="url(#grain)"/>
 <g opacity=".022" stroke="#fff" stroke-linecap="round" fill="none"><path d="M${W*.0625} ${H*.278} C ${W*.3125} ${H*.213} ${W*.469} ${H*.306} ${W*.781} ${H*.231}" stroke-width="90"/><path d="M${W*.156} ${H*.759} C ${W*.417} ${H*.704} ${W*.625} ${H*.796} ${W*.9375} ${H*.722}" stroke-width="120"/></g></svg>
<div class="tex" id="tex"></div>`);
    document.body.insertAdjacentHTML('beforeend', '<div class="rub" id="rub"></div>');
  }

  // screen-space sample points of a drawn path, for keeping formulas and captions off the lines
  function pathPoints(n, step = 18) {
    const out = [];
    try {
      const L = n.getTotalLength(), m = n.getScreenCTM(); if (!m) return out;
      for (let s = 0; s <= L; s += step) { const p = n.getPointAtLength(s); out.push([m.a * p.x + m.c * p.y + m.e, m.b * p.x + m.d * p.y + m.f]); }
    } catch (e) { }
    return out;
  }

  // faint formulas: each scene has its own, whole, inside the frame, off captions, cut-outs, lines and each other
  function buildTex() {
    if (!cfg.formulas.length) return;
    const r2 = rng(cfg.texSeed), T = cfg.formulas;
    for (const sc of document.querySelectorAll('.sc')) {
      if (sc.dataset.notex) continue;
      const layer = document.createElement('div'); layer.className = 'tex'; sc.prepend(layer); sc.style.display = 'block';
      // measure with every timed element in its final state
      const box = [...sc.querySelectorAll('.ck, .lab, .cw, .paper, svg text, svg circle, [data-box]')].map(n => { const b = n.getBoundingClientRect(); return [b.left - 24, b.top - 16, b.right + 24, b.bottom + 16]; });
      const pts = [...sc.querySelectorAll('svg.draw path, svg.draw line, svg.draw polyline, svg.draw rect, svg.draw ellipse')].flatMap(n => pathPoints(n));
      const n = +(sc.dataset.tex || cfg.formulasPerScene);
      for (let k = 0, shown = 0; shown < n && k < 600; k++) {
        const e = document.createElement('span'); e.textContent = T[Math.floor(r2() * T.length)];
        e.style.fontSize = (26 + r2() * 30) + 'px'; e.style.opacity = (0.06 + r2() * 0.07).toFixed(3); e.style.transform = `rotate(${(r2() - .5) * 8}deg)`;
        layer.appendChild(e); const w = e.offsetWidth + 24, h = e.offsetHeight + 16, x = 40 + r2() * (cfg.w - 80 - w), y = 30 + r2() * (cfg.h - 70 - h);
        if (box.some(b => x < b[2] && b[0] < x + w && y < b[3] && b[1] < y + h) ||
          pts.some(([px, py]) => px > x - 14 && px < x + w + 14 && py > y - 14 && py < y + h + 14)) { e.remove(); continue; }
        box.push([x, y, x + w, y + h]); e.style.left = x + 'px'; e.style.top = y + 'px'; shown++;
      }
      sc.style.display = '';
    }
  }

  const len = {};
  function prepare() {
    for (const e of TL) {
      const n = $(e.id); if (!n) throw new Error('timeline id not found: ' + e.id);
      if (e.kind === 'draw') len[e.id] = n.getTotalLength();
      if (e.kind === 'grow') e.p = ['x1', 'y1', 'x2', 'y2'].map(k => +n.getAttribute(k));
      if (n.dataset.tf === undefined) n.dataset.tf = n.style.transform || '';
      if (e.kind === 'fade') n.dataset.op = n.style.opacity || 1;
      const s = n.closest('.sc'); e.sc = s ? s.id : null;
    }
    for (const k in CUT) { const s = $(k).closest('.sc'); CUT[k].sc = s ? s.id : null; }
  }
  function applyEntry(e, t) {
    const n = $(e.id), u = cl((t - e.t) / e.d), on = t >= e.t;
    switch (e.kind) {
      case 'write': n.style.visibility = on ? 'visible' : 'hidden'; n.style.clipPath = u >= 1 ? 'none' : `inset(-40% ${(100 - 125 * u).toFixed(2)}% -40% -15%)`; break;
      case 'wipe': n.style.clipPath = u >= 1 ? 'none' : `inset(-5% ${(100 - 110 * u).toFixed(2)}% -5% -5%)`; break;
      case 'draw': { const L = len[e.id]; n.style.visibility = on ? 'visible' : 'hidden'; n.style.strokeDasharray = `${L} ${L}`; n.style.strokeDashoffset = L * (1 - u); break; }
      case 'grow': { const [x1, y1, x2, y2] = e.p; n.style.visibility = on ? 'visible' : 'hidden'; n.setAttribute('x2', x1 + (x2 - x1) * u); n.setAttribute('y2', y1 + (y2 - y1) * u); break; }
      case 'fade': n.style.opacity = u * (n.dataset.op || 1); break;
      case 'hide': if (on) n.style.opacity = 1 - u; break;
      case 'pop': { n.style.visibility = on ? 'visible' : 'hidden'; const b = n.dataset.tf || ''; n.style.transform = `${b} scale(${(0.4 + 0.6 * outBack(u, 2.2)).toFixed(4)})`; n.style.opacity = cl(u * 3); break; }
      case 'tape': n.style.visibility = on ? 'visible' : 'hidden'; n.style.transform = `${n.dataset.tf} scale(${(1.25 - 0.25 * out3(u)).toFixed(3)}, 1) scaleX(${out3(u).toFixed(3)})`; n.style.transformOrigin = '0 50%'; break;
      case 'fn': e.f(n, u, t, on); break;   // custom: computed counters, moving dots, model animations
    }
  }
  function cutTransform(id, c, t) {
    const n = $(id);
    if (t < c.t) { n.style.visibility = 'hidden'; return; }
    n.style.visibility = 'visible';
    const u = (t - c.t) / 0.75, k = 1 - (c.back ? outBack(u, c.back) : outBack(u, 1.1));
    let dx = c.from[0] * k, dy = c.from[1] * k, dr = c.from[2] * k, sc = 1 + 0.004 * Math.sin(2 * Math.PI * (t - c.t) / 3.1);
    for (const w of c.wig) { const v = t - w; if (v > 0 && v < 1.4) { dr += 3.2 * Math.sin(2 * Math.PI * 3.2 * v) * Math.exp(-3.2 * v); sc += 0.035 * Math.sin(Math.PI * cl(v / 0.25)) * (v < 0.25 ? 1 : 0); } }
    const v = t - c.out; if (v > 0) { const e = Math.pow(cl(v / 0.5), 2), d = c.to || [900, -260, 18]; dx += d[0] * e; dy += d[1] * e; dr += d[2] * e; }
    n.style.transform = `translate(${dx.toFixed(2)}px,${dy.toFixed(2)}px) rotate(${dr.toFixed(3)}deg) scale(${sc.toFixed(4)})`;
  }
  function camera(s, t) {
    let tx = 0, ty = 0;
    if (s.pan) {   // [[t, x, y], ...] in px, smoothstep between keys
      const k = s.pan; tx = k[0][1]; ty = k[0][2];
      for (let i = 0; i + 1 < k.length; i++) if (t >= k[i][0]) { const u = smooth((t - k[i][0]) / Math.max(1e-6, k[i + 1][0] - k[i][0])); tx = k[i][1] + (k[i + 1][1] - k[i][1]) * u; ty = k[i][2] + (k[i + 1][2] - k[i][2]) * u; }
    }
    const z = 1 + s.push * cl((t - s.t0) / s.pushDur);
    return `translate(${tx.toFixed(2)}px,${ty.toFixed(2)}px) scale(${z.toFixed(4)})`;
  }
  const active = new Set();
  function render(t) {
    active.clear();
    for (const s of SC) {
      const n = $(s.id), vis = t >= s.t0 && t < s.te + cfg.erase + 0.6;
      n.style.display = vis ? 'block' : 'none'; if (!vis) continue;
      active.add(s.id);
      n.style.transform = camera(s, t);
      if (n.firstElementChild && n.firstElementChild.classList.contains('tex')) n.firstElementChild.style.opacity = s.t0 === 0 ? 1 : cl((t - s.t0) / 1.2);
      const u = cl((t - s.te) / cfg.erase), p = -15 + 130 * u;  // eraser: leaves a faint ghost, then it fades
      const ghost = 0.06 * (1 - cl((t - s.te - cfg.erase) / 0.6));
      n.style.maskImage = n.style.webkitMaskImage = t < s.te ? 'none' : `linear-gradient(100deg, rgba(0,0,0,${ghost.toFixed(3)}) ${p.toFixed(1)}%, #000 ${(p + 12).toFixed(1)}%)`;
    }
    const rub = $('rub'), er = SC.find(s => t >= s.te && t < s.te + cfg.erase);
    rub.style.display = er ? 'block' : 'none';
    if (er) rub.style.left = (-300 + (cfg.w + 580) * ((t - er.te) / cfg.erase)) + 'px'; rub.style.height = (cfg.h + 200) + 'px';
    for (const e of TL) if (!e.sc || active.has(e.sc)) applyEntry(e, t);
    for (const k in CUT) if (!CUT[k].sc || active.has(CUT[k].sc)) cutTransform(k, CUT[k], t);
    if (window.onFrame) window.onFrame(t, active);
  }
  function collectEvents() {
    for (const k in CUT) { const c = CUT[k]; EV.push({ t: c.t, k: 'drop' }); c.wig.forEach(w => EV.push({ t: w, k: 'wig' })); if (c.out < cfg.frames / cfg.fps) EV.push({ t: c.out, k: 'lift' }); }
    for (const e of TL) if (!e.quiet && e.kind !== 'hide' && e.kind !== 'fn') EV.push({ t: e.t, d: e.d, k: e.kind, note: e.note });
    for (const e of TL) if (e.kind === 'fn' && e.sound) EV.push({ t: e.t, d: e.d, k: e.sound, ...(e.soundArgs || {}) });
    SC.forEach(s => s.te < cfg.frames / cfg.fps && EV.push({ t: s.te, d: cfg.erase, k: 'erase' }));
    EV.sort((a, b) => a.t - b.t);
  }
  async function start(o) {
    document.body.appendChild($('rub'));
    Object.assign(cfg, o);
    await document.fonts.ready;
    await Promise.all([...document.fonts].map(f => f.load().catch(() => { })));   // hidden boards' fonts too, so measurements use the real glyphs
    buildTex();
    await Promise.all([...document.images].map(i => i.decode().catch(() => { })));
    prepare(); collectEvents();
    window.renderFrame = i => render(i / cfg.fps);
    window.info = () => ({ frames: cfg.frames, fps: cfg.fps, events: EV, scenes: SC.map(s => [s.id, s.t0, s.te]) });
    const F = new URLSearchParams(location.search).get('t');
    render(F === null ? 0 : +F); window.ready = true;
  }
  return { $, el, cl, out3, outBack, smooth, rng, at, cut, scene, event, start, chrome, render, cfg, TL, CUT, SC, EV, NS };
})();
```

## lib/chalk.css

Стили доски.

```css
/* Chalkboard style kit (task 58), split out of chalk-clip.html so every video page shares it. */
@font-face{font-family:Caveat;src:url("../kit/fonts/caveat-Caveat[wght].ttf");font-weight:400 700}
@font-face{font-family:SpaceMono;src:url(../kit/fonts/spacemono-SpaceMono-Regular.ttf)}
@font-face{font-family:SpaceMono;src:url(../kit/fonts/spacemono-SpaceMono-Bold.ttf);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#0a0a0b}
.abs{position:absolute}
.board{position:absolute;inset:0;background:
 radial-gradient(ellipse 900px 500px at 30% 40%,rgba(255,255,255,.035),transparent 70%),
 radial-gradient(ellipse 700px 400px at 75% 70%,rgba(255,255,255,.03),transparent 70%),#0a0a0b}
.dust{position:absolute;inset:0;opacity:.5;mix-blend-mode:screen}
.tex{position:absolute;inset:0;font-family:Caveat;color:#fff;filter:url(#chalk)}
.tex span{position:absolute;white-space:nowrap}
.sc{position:absolute;inset:0;display:none;transform-origin:50% 50%}
.ck{font-family:Caveat;color:#f4f1ea;filter:url(#chalkT);position:absolute;white-space:nowrap;line-height:.9}
svg.draw{position:absolute;left:0;top:0;filter:url(#chalk);overflow:visible}
svg.draw *{transform-box:fill-box;transform-origin:center}
.cw{position:absolute;transform-origin:50% 50%}
.cw>img{position:absolute;left:0;top:0;width:100%;filter:drop-shadow(1px 2px 1px rgba(0,0,0,.55)) drop-shadow(4px 14px 22px rgba(0,0,0,.65))}
.tape{position:absolute;width:150px;height:44px;background:rgba(235,230,215,.55);box-shadow:0 1px 2px rgba(0,0,0,.3)}
.lab{font-family:SpaceMono;font-size:20px;color:rgba(255,255,255,.55);letter-spacing:.2em;position:absolute;white-space:nowrap}
.rub{position:absolute;top:-100px;width:260px;height:1280px;pointer-events:none;display:none;
 background:radial-gradient(ellipse 50% 50% at 50% 50%,rgba(255,255,255,.07),transparent 70%)}
/* additions for the long video */
.paper{position:absolute;background:#efe9da;color:#26231f;font-family:SpaceMono;box-shadow:1px 2px 1px rgba(0,0,0,.55),4px 14px 22px rgba(0,0,0,.65)}
.mono{font-family:SpaceMono}
```

## tools/capture3.mjs

Захват кадров страницы в сегменты H.264.

```js
// Segment capture for long videos, built on the kit's capture2.mjs: the page exposes window.renderFrame(i).
// Frames are screenshotted in order, every SEG frames are encoded to one H.264 segment and their PNGs deleted,
// so disk use stays small. Finished segments are skipped on a rerun (resumable). Segments join with
// `ffmpeg -f concat -c copy` because all share one encoder setting.
// usage: bun tools/capture3.mjs <page.html> <outdir> <frames> [--from 0] [--to N] [--seg 300] [--chunk 60] [--fps 30]
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { spawnSync } from 'node:child_process';
import { readFileSync, existsSync, mkdirSync, writeFileSync, rmSync, renameSync } from 'node:fs';
import { resolve, dirname, extname, join } from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const pagePath = resolve(args[0]), outDir = resolve(args[1]), N = +args[2];
const VW = +opt('--w', 1920), VH = +opt('--h', 1080), fps = +opt('--fps', 30), SEG = +opt('--seg', 300), CHUNK = +opt('--chunk', 60);
const FROM = +opt('--from', 0), TO = Math.min(N, +opt('--to', N));
const FFMPEG = '/home/boardagent/.explainer/bin/ffmpeg';
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.svg': 'image/svg+xml', '.ttf': 'font/ttf', '.woff2': 'font/woff2' };
mkdirSync(outDir, { recursive: true });

let browser, page;
async function open() {
  browser = await chromium.launch({
    executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',
    args: ['--disable-gpu', '--disable-gpu-compositing', '--disable-software-rasterizer', '--font-render-hinting=none',
      '--disable-lcd-text', '--disable-extensions', '--disable-gpu-shader-disk-cache', '--renderer-process-limit=1',
      '--disable-dev-shm-usage', '--js-flags=--max-old-space-size=1024'],
  });
  const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  page = await ctx.newPage();
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  await page.route('http://probe.local/**', async route => {
    const p = join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    if (!existsSync(p)) return route.fulfill({ status: 404, body: 'nf' });
    route.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } });
  });
  await page.goto('http://probe.local' + pagePath.slice(ROOT.length));
  await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
}
async function reopen() {
  for (let a = 0; ; a++) {
    try { try { await browser?.close(); } catch { } await open(); return; }
    catch (e) { if (a >= 30) throw e; console.error(`[open failed ${a + 1}] ${String(e.message).split('\n')[0]}`); await new Promise(r => setTimeout(r, 4000)); }
  }
}
const t0 = Date.now();
let rendered = 0, sinceOpen = 1e9;
for (let s = Math.floor(FROM / SEG) * SEG; s < TO; s += SEG) {
  const segName = join(outDir, `seg${String(s).padStart(6, '0')}.mp4`);
  if (existsSync(segName)) continue;
  const e = Math.min(N, s + SEG), dir = join(outDir, `png${s}`);
  mkdirSync(dir, { recursive: true });
  for (let i = s; i < e; i++) {
    const f = join(dir, `f${String(i - s).padStart(4, '0')}.png`);
    if (existsSync(f)) continue;
    if (sinceOpen >= CHUNK) { await reopen(); sinceOpen = 0; }
    try {
      await page.evaluate(i => window.renderFrame(i), i);
      writeFileSync(f, await page.screenshot({ type: 'png', animations: 'disabled', caret: 'hide' }));
      rendered++; sinceOpen++;
    } catch (err) {
      console.error(`[retry] frame ${i}: ${String(err.message).split('\n')[0]}`);
      await new Promise(r => setTimeout(r, 4000)); sinceOpen = 1e9; i--; continue;
    }
  }
  const tmp = segName.replace(/\.mp4$/, '.part.mp4');
  const r = spawnSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', join(dir, 'f%04d.png'),
    '-c:v', 'libx264', '-preset', 'medium', '-threads', '2', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps), tmp], { stdio: 'inherit' });
  if (r.status !== 0) { console.error(`ffmpeg failed on segment ${s}: ${r.status}`); process.exit(2); }
  renameSync(tmp, segName); rmSync(dir, { recursive: true, force: true });
  const el = (Date.now() - t0) / 1000;
  console.error(`SEG ${s}-${e} done; ${rendered} frames in ${el.toFixed(0)} s (${(el / Math.max(1, rendered)).toFixed(3)} s/frame)`);
}
try { await browser?.close(); } catch { }
console.error(`DONE ${FROM}-${TO}`);
```

## tools/check3.mjs

Проверка каждого кадра: обрезка, наложения, линии через текст, фон под надписями.

```js
// Layout check for every frame of a chalk page (stricter than the kit's check-clip.mjs):
//  EDGE  text, labels, drawings or a settled cut-out leave the frame (minus a safe margin)
//  OVER  text over text, text under a cut-out, text over paper notes
//  LINE  a drawn line passes through text (sampled along the visible part of each path)
//  TEX   a faint formula sits under text, a cut-out or a line
// Allowed on purpose: data-bleed on a drawing (may leave the frame), data-allow="id id" on a drawing
// (may cross those texts, e.g. a strike-through), cut-outs while they fly in or out.
// usage: bun tools/check3.mjs <page.html> [--step 1] [--margin 16]   exit 1 when anything is found
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join, extname, dirname } from 'node:path';
const args = process.argv.slice(2), opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.ttf': 'font/ttf' };
const browser = await chromium.launch({ executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--disable-gpu'] });
const VW = +opt('--w', 1920), VH = +opt('--h', 1080);
const page = await (await browser.newContext({ viewport: { width: VW, height: VH } })).newPage();
page.on('pageerror', e => console.error('[pageerror]', e.message));
await page.route('http://probe.local/**', async r => { const p = join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!existsSync(p)) return r.fulfill({ status: 404, body: 'nf' }); r.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } }); });
await page.goto('http://probe.local' + resolve(args[0]).slice(ROOT.length));
await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
const res = await page.evaluate(async ({ step, M }) => {
  const hits = {}, info = window.info(), N = info.frames, fps = info.fps, FW = window.innerWidth, FH = window.innerHeight;
  const note = (k, t) => { const h = hits[k] || (hits[k] = [t, t, 0]); h[1] = t; h[2]++; };
  const vis = n => { for (let e = n; e && e.nodeType === 1; e = e.parentNode) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false; } return true; };
  // path samples in local coordinates, once
  const paths = [...document.querySelectorAll('.sc svg.draw path, .sc svg.draw line, .sc svg.draw polyline, .sc svg.draw circle, .sc svg.draw ellipse, .sc svg.draw rect')].map(n => {
    let pts = [], L = 0; try { L = n.getTotalLength(); for (let s = 0; s <= L; s += 6) { const p = n.getPointAtLength(s); pts.push([s, p.x, p.y]); } } catch (e) { }
    return { n, L, pts, allow: (n.dataset.allow || n.closest('[data-allow]')?.dataset.allow || '').split(/\s+/).filter(Boolean), bleed: n.closest('[data-bleed]') !== null, w: parseFloat(getComputedStyle(n).strokeWidth) || 4 };
  });
  // exact glyph ink box: canvas text metrics placed on the CSS baseline, mapped into the element's screen rect
  const cvs = document.createElement('canvas').getContext('2d');
  const inkBox = (n, r, fs) => {
    const cs = getComputedStyle(n);
    if (n.tagName.toLowerCase() === 'text') return [r.left, r.top, r.right, r.bottom];
    cvs.font = `${cs.fontStyle} ${cs.fontWeight} ${fs}px ${cs.fontFamily}`;
    if ('letterSpacing' in cvs) cvs.letterSpacing = cs.letterSpacing === 'normal' ? '0px' : cs.letterSpacing;
    const lines = (n.innerText || n.textContent).split('\n'); const lh = parseFloat(cs.lineHeight) || fs * 1.2;
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    lines.forEach((L, i) => {
      const m = cvs.measureText(L); if (!L.trim()) return;
      const half = (lh - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2, base = i * lh + half + m.fontBoundingBoxAscent;
      const ox = parseFloat(cs.textAlign === 'center' ? (n.offsetWidth - m.width) / 2 : 0);
      x0 = Math.min(x0, ox - m.actualBoundingBoxLeft); x1 = Math.max(x1, ox + m.actualBoundingBoxRight);
      y0 = Math.min(y0, base - m.actualBoundingBoxAscent); y1 = Math.max(y1, base + m.actualBoundingBoxDescent);
    });
    const w = n.offsetWidth || 1, h = n.offsetHeight || 1, sx = r.width / w, sy = r.height / h;
    // r is the axis-aligned box of the (maybe slightly rotated) element: scale the local ink box into it
    return [r.left + x0 * sx, r.top + y0 * sy, r.left + x1 * sx, r.top + y1 * sy];
  };
  const cuts = typeof Chalk !== 'undefined' ? Chalk.CUT : {}, SCN = typeof Chalk !== 'undefined' ? Chalk.SC : [], ER = typeof Chalk !== 'undefined' ? Chalk.cfg.erase : 0.9;
  // the eraser sweeps left to right; an element of a scene being erased is gone once the sweep passed its right edge
  const erased = (n, r, t) => { const sc = n.closest('.sc'); const s = SCN.find(x => x.id === (sc && sc.id)); if (!s || t < s.te) return false; const p = -15 + 130 * Math.min(1, (t - s.te) / ER); return r.right / FW * 100 < p + 2; };
  for (let f = 0; f < N; f += step) {
    await window.renderFrame(f); const t = f / fps;
    const texts = [], cutsNow = [], papers = [];
    for (const n of document.querySelectorAll('.sc .ck, .sc .lab, .sc svg text')) {
      if (!vis(n)) continue; const r = n.getBoundingClientRect(); if (!r.width || erased(n, r, t)) continue; const fs = parseFloat(getComputedStyle(n).fontSize);
      const ib = inkBox(n, r, fs);
      texts.push({ id: n.id || n.textContent.slice(0, 18), l: ib[0], t: ib[1], r: ib[2], b: ib[3], core: ib });
    }
    for (const n of document.querySelectorAll('.sc .cw')) {
      const img = n.querySelector('img'); if (!img || !vis(img)) continue; const r = img.getBoundingClientRect(), c = cuts[n.id];
      if (erased(n, r, t)) continue;
      const settled = !c || (t >= c.t + 0.75 && t < c.out);
      if (c && t >= c.out + 0.5 && r.right > 0 && r.left < FW && r.bottom > 0 && r.top < FH) note(`STUCK cut ${n.id} still in frame after its exit`, t);
      if (!settled) continue;   // flying in or out: motion, not layout
      cutsNow.push({ id: n.id, l: r.left + 15, r: r.right - 15, t: r.top + 15, b: r.bottom - 15, settled });
    }
    for (const n of document.querySelectorAll('.sc .paper')) { if (!vis(n)) continue; const r = n.getBoundingClientRect(); if (erased(n, r, t)) continue; papers.push({ id: n.id, l: r.left, r: r.right, t: r.top, b: r.bottom }); }
    for (const a of texts) if (a.l < M || a.t < M || a.r > FW - M || a.b > FH - M) note(`EDGE text ${a.id} [${a.l | 0},${a.t | 0},${a.r | 0},${a.b | 0}]`, t);
    for (const a of cutsNow) if (a.settled && (a.l < 0 || a.t < 0 || a.r > FW || a.b > FH)) note(`EDGE cut ${a.id}`, t);
    for (const a of papers) if (a.l < M || a.t < M || a.r > FW - M || a.b > FH - M) note(`EDGE paper ${a.id}`, t);
    const ov = (a, b, m = 4) => Math.min(a.r, b.r) - Math.max(a.l, b.l) > m && Math.min(a.b, b.b) - Math.max(a.t, b.t) > m;
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) if (ov(texts[i], texts[j])) note(`OVER ${texts[i].id} x ${texts[j].id}`, t);
    for (const a of texts) for (const c of cutsNow) if (ov(a, c)) note(`OVER ${a.id} under cut ${c.id}`, t);
    for (const a of texts) for (const p of papers) if (ov(a, p) && !document.getElementById(p.id)?.contains(document.getElementById(a.id))) note(`OVER ${a.id} x paper ${p.id}`, t);
    // drawn lines
    const linePts = [];
    for (const P of paths) {
      const n = P.n; if (!P.pts.length || !vis(n)) continue; if (erased(n, n.getBoundingClientRect(), t)) continue;
      const cw = n.closest('.cw'); if (cw && cuts[cw.id] && !(t >= cuts[cw.id].t + 0.75 && t < cuts[cw.id].out)) continue;   // drawn on a flying cut-out
      const cs = getComputedStyle(n); let upto = P.L;
      if (cs.strokeDasharray && cs.strokeDasharray !== 'none' && n.style.strokeDashoffset !== '') upto = P.L - parseFloat(n.style.strokeDashoffset || 0);
      const m = n.getScreenCTM(); if (!m) continue;
      for (const [s, x, y] of P.pts) {
        if (s > upto + 0.5) break;
        const X = m.a * x + m.c * y + m.e, Y = m.b * x + m.d * y + m.f; linePts.push([X, Y]);
        if (!P.bleed && (X < M || Y < M || X > FW - M || Y > FH - M)) { note(`EDGE line ${n.id || n.tagName}`, t); break; }
      }
      for (const a of texts) {
        if (P.allow.includes(a.id)) continue;
        const pad = P.w / 2 + 2;
        for (const [s, x, y] of P.pts) {
          if (s > upto + 0.5) break;
          const X = m.a * x + m.c * y + m.e, Y = m.b * x + m.d * y + m.f;
          if (X > a.core[0] - pad && X < a.core[2] + pad && Y > a.core[1] - pad && Y < a.core[3] + pad) { note(`LINE ${n.id || n.tagName} through ${a.id}`, t); break; }
        }
      }
    }
    // faint formulas
    for (const n of document.querySelectorAll('.sc .tex span')) {
      if (!vis(n)) continue; const r = n.getBoundingClientRect(); if (erased(n, r, t)) continue; const b = { l: r.left, r: r.right, t: r.top, b: r.bottom };
      if (r.left < 0 || r.top < 0 || r.right > FW || r.bottom > FH) note(`TEX edge ${n.textContent}`, t);
      for (const a of texts) if (ov(a, b, 0)) note(`TEX ${n.textContent} under ${a.id}`, t);
      for (const c of cutsNow) if (c.settled && ov(c, b, 0)) note(`TEX ${n.textContent} under cut ${c.id}`, t);
      for (const [x, y] of linePts) if (x > b.l - 6 && x < b.r + 6 && y > b.t - 6 && y < b.b + 6) { note(`TEX ${n.textContent} on a line`, t); break; }
    }
  }
  return hits;
}, { step: +opt('--step', 1), M: +opt('--margin', 16) });
const keys = Object.entries(res);
for (const [k, [a, b, c]] of keys) console.log(k, a.toFixed(2), '-', b.toFixed(2), `(${c} frames)`);
console.log(keys.length ? `FOUND ${keys.length}` : 'CLEAN');
await browser.close();
process.exit(keys.length ? 1 : 0);
```

## tools/stills.mjs

Отдельные кадры для просмотра.

```js
// Render chosen moments of a chalk page to PNG files (for contact sheets). usage: bun tools/stills.mjs <page.html> <outdir> <t1> [t2 ...] [--w 1920 --h 1080]
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, join, extname, dirname } from 'node:path';
const args = process.argv.slice(2), opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.ttf': 'font/ttf' };
const VW = +opt('--w', 1920), VH = +opt('--h', 1080), out = resolve(args[1]); mkdirSync(out, { recursive: true });
const times = args.slice(2).filter((a, i, A) => !a.startsWith('--') && !(A[i - 1] || '').startsWith('--')).map(Number);
const browser = await chromium.launch({ executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--disable-gpu', '--font-render-hinting=none'] });
const page = await (await browser.newContext({ viewport: { width: VW, height: VH } })).newPage();
page.on('pageerror', e => console.error('[pageerror]', e.message));
await page.route('http://probe.local/**', async r => { const p = join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!existsSync(p)) return r.fulfill({ status: 404, body: 'nf' }); r.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } }); });
await page.goto('http://probe.local' + resolve(args[0]).slice(ROOT.length));
await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
for (const t of times) {
  await page.evaluate(t => window.renderFrame(Math.round(t * window.info().fps)), t);
  writeFileSync(join(out, `t${t.toFixed(1).padStart(6, '0')}.png`), await page.screenshot({ type: 'png' }));
}
console.log(JSON.stringify((await page.evaluate(() => window.info().scenes))));
await browser.close();
```

## tools/info.mjs

Таймлайн событий страницы для звука.

```js
// dump window.info() of a chalk page (frames, fps, sound events, scenes) as JSON
// usage: bun tools/info.mjs <page.html> <out.json>
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { readFileSync, existsSync, writeFileSync } from 'node:fs';
import { resolve, join, extname, dirname } from 'node:path';
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.ttf': 'font/ttf' };
const browser = await chromium.launch({ executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--disable-gpu'] });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
page.on('pageerror', e => console.error('[pageerror]', e.message));
await page.route('http://probe.local/**', async r => { const p = join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!existsSync(p)) return r.fulfill({ status: 404, body: 'nf' }); r.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } }); });
await page.goto('http://probe.local' + resolve(process.argv[2]).slice(ROOT.length));
await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
writeFileSync(process.argv[3], JSON.stringify(await page.evaluate(() => window.info())));
await browser.close();
```

## tools/sound2.py

Музыка и звуки кодом.

```python
"""Procedural sound for chalk videos, generalised from the style kit's clip_sound.py.
Effects come from the page's own timeline (window.info() events), music from a plan of sections.
Everything is synthesised here from sine waves and seeded noise: no samples, no recordings, no model.
Dependencies: numpy, scipy (BSD licences). Output: 48 kHz stereo 16-bit WAV stems and a mix.

usage: python sound2.py events.json plan.json outdir [narration.json]
  plan.json: {"bpm": 96, "sections": [{"t0":0,"t1":20,"mood":"play","chords":[[60,64,67,71],...]}, ...],
              "end": {"t": 58.2, "note": 48}}
  narration.json: [[t0, t1], ...] spoken windows (estimated or from the voice); music ducks under them.
"""
import json, os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

info = json.load(open(sys.argv[1])); EV = info['events']
plan = json.load(open(sys.argv[2])); OUT = sys.argv[3]
NAR = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else []
os.makedirs(OUT, exist_ok=True)
SR = 48000; DUR = info['frames'] / info['fps']; n = int(DUR * SR); t = np.arange(n) / SR
rng = np.random.default_rng(int(plan.get('seed', 20261019)))


class Bus:
    def __init__(self):
        self.L = np.zeros(n); self.R = np.zeros(n)

    def add(self, x, t0, gain=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= n or i + len(x) <= 0:
            return
        if i < 0:
            x = x[-i:]; i = 0
        x = x[:n - i]
        self.L[i:i + len(x)] += x * gain * np.sqrt((1 - pan) / 2) * 1.414
        self.R[i:i + len(x)] += x * gain * np.sqrt((1 + pan) / 2) * 1.414


sfx, mus = Bus(), Bus()


def env_ad(m, a, d):
    tt = np.arange(m) / SR; return (1 - np.exp(-tt / a)) * np.exp(-tt / d)


def tone(f, dur, a=0.005, d=0.3, harm=(1, .3, .1)):
    m = int(dur * SR); tt = np.arange(m) / SR
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * tt) for k, h in enumerate(harm)) * env_ad(m, a, d)


def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def bp(x, f0, f1, o=2): return sosfilt(butter(o, [f0, f1], 'band', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)


N = lambda m: 440 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- effects (kit, unchanged in character)
def whoosh(dur, f0, f1, gain=0.3):
    m = int(dur * SR); noise = rng.standard_normal(m); out = np.zeros(m); k = 30; seg = m // k
    for s in range(k):
        fc = f0 * (f1 / f0) ** (s / (k - 1)); a, b = s * seg, ((s + 1) * seg if s < k - 1 else m)
        out[a:b] = bp(noise, max(40, fc * 0.4), min(SR / 2 - 100, fc * 1.6), 2)[a:b]
    out *= np.sin(np.pi * np.linspace(0, 1, m)) ** 2; return out / (np.max(np.abs(out)) + 1e-9) * gain


def scratch(t0, dur, gain=0.17, f0=2200, f1=6500, rate=9):
    m = int(dur * SR)
    if m < 32: return
    x = bp(rng.standard_normal(m), f0, f1, 2); tt = np.arange(m) / SR
    ph = np.cumsum(rate * (1 + 0.3 * np.sin(2 * np.pi * 0.7 * tt)) / SR)
    chop = 0.45 + 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * ph)) ** 0.6
    e = np.minimum(1, tt / 0.03) * np.minimum(1, (dur - tt) / 0.05)
    sfx.add(x * chop * e * gain, t0, 1.0, rng.uniform(-0.25, 0.25))


def pluck(f, dur=0.7, g=0.2):
    m = int(dur * SR); tt = np.arange(m) / SR
    return (np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.18) + 0.35 * np.sin(2 * np.pi * f * 4 * tt) * np.exp(-tt / 0.04)) * g * (1 - np.exp(-tt / 0.002))


def thud(t0, g=0.32):
    m = int(0.25 * SR); tt = np.arange(m) / SR
    sfx.add(np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-tt * 40)) / SR) * np.exp(-tt / 0.06) * g, t0, 1.0)
    sfx.add(bp(rng.standard_normal(m), 300, 2500) * env_ad(m, 0.002, 0.03) * g * 0.6, t0, 1.0, 0.2)


def rip(t0, g=0.22):
    m = int(0.32 * SR); x = bp(rng.standard_normal(m), 900, 7000); crack = (rng.random(m) < 0.004).astype(float)
    crack = np.convolve(crack, np.exp(-np.arange(200) / 30), 'same'); e = np.sin(np.pi * np.linspace(0, 1, m)) ** 0.7
    sfx.add(x * (0.35 + crack) * e * g, t0, 1.0, 0.3)


def pop(t0, f=300, g=0.3):
    m = int(0.18 * SR); tt = np.arange(m) / SR; ff = f * (1 + 2.2 * np.exp(-tt * 30))
    sfx.add(np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-tt / 0.045) * g, t0, 1.0, rng.uniform(-0.3, 0.3))


def boing(t0, g=0.16):
    m = int(0.45 * SR); tt = np.arange(m) / SR
    sfx.add(np.sin(2 * np.pi * np.cumsum(330 + 260 * np.exp(-tt * 6) * np.sin(tt * 34)) / SR) * np.exp(-tt / 0.16) * g, t0, 1.0, 0.4)


def rub(t0, dur, g=0.2):
    m = int(dur * SR); tt = np.arange(m) / SR; x = bp(rng.standard_normal(m), 250, 1800)
    strokes = 0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 2.6 * tt)) ** 0.8
    sfx.add(x * strokes * np.sin(np.pi * np.linspace(0, 1, m)) ** 0.6 * g, t0, 1.0, -0.1)


# new effects for the long video
def tick(t0, g=0.14, f=2600, pan=0.0):
    """mechanical clock tick: a short resonant click"""
    m = int(0.06 * SR); tt = np.arange(m) / SR
    x = bp(rng.standard_normal(m), f * 0.7, f * 1.3) * np.exp(-tt / 0.006) + np.sin(2 * np.pi * f * 1.5 * tt) * np.exp(-tt / 0.01) * 0.4
    sfx.add(x * g, t0, 1.0, pan)


def ping(t0, midi=84, g=0.1, pan=0.0):
    sfx.add(tone(N(midi), 1.2, 0.002, 0.35, (1, .25, .05)) * g, t0, 1.0, pan)


def rumble(t0, dur=2.5, g=0.35):
    """distant thunder: low noise with a slow, uneven swell"""
    m = int(dur * SR); tt = np.arange(m) / SR
    x = lp(rng.standard_normal(m), 160, 4) + 0.4 * lp(rng.standard_normal(m), 600, 2) * np.exp(-tt / 0.3)
    e = np.minimum(1, tt / 0.08) * np.exp(-tt / (dur * 0.35)) * (0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * tt) ** 2)
    sfx.add(x / (np.max(np.abs(x)) + 1e-9) * e * g, t0, 1.0, 0.0)


def flash(t0, g=0.12):
    """lightning crack, short and bright"""
    m = int(0.25 * SR); tt = np.arange(m) / SR
    sfx.add(hp(rng.standard_normal(m), 1500) * np.exp(-tt / 0.03) * g, t0, 1.0, -0.2)


def counter(t0, dur, g=0.05):
    """digits running: fast soft ticks slowing down"""
    k, tt = 0, 0.0
    while tt < dur:
        tick(t0 + tt, g, 3400, 0.2 * np.sin(k)); k += 1
        tt += 0.035 + 0.09 * (tt / max(dur, 1e-6)) ** 2


CUES = {
    'write': lambda e: scratch(e['t'] + 0.03, e['d'] * 0.95, 0.17),
    'draw': lambda e: (sfx.add(tone(N([88, 84, 81, 79, 76, 72][e['note'] % 6]), 0.5, 0.002, 0.18, (1, .3)) * 0.12, e['t'] + e['d'] * 0.8, 1.0, -0.4 + 0.15 * (e['note'] % 6)), scratch(e['t'], e['d'], 0.10, 3000, 7500, 14))
    if e.get('note') is not None else scratch(e['t'], max(0.12, e['d']), 0.11, 2800, 7000, 12),
    'grow': lambda e: scratch(e['t'], e['d'], 0.10, 2500, 6000, 6),
    'wipe': lambda e: scratch(e['t'], e['d'], 0.07, 2500, 6000, 5),
    'drop': lambda e: (sfx.add(whoosh(0.5, 300, 2600, 0.16), e['t'] - 0.15, 1.0, 0.3), thud(e['t'] + 0.32)),
    'tape': lambda e: rip(e['t'] - 0.05),
    'wig': lambda e: boing(e['t']),
    'lift': lambda e: sfx.add(whoosh(0.45, 2000, 400, 0.14), e['t'], 1.0, 0.4),
    'erase': lambda e: rub(e['t'] - 0.05, e['d'] + 0.2),
    'pop': lambda e: pop(e['t'], 280),
    'fade': lambda e: None,
    'tick': lambda e: [tick(e['t'] + i * e.get('every', 0.5), e.get('g', 0.12), e.get('f', 2600), e.get('pan', 0)) for i in range(int(e.get('n', 1)))],
    'ping': lambda e: ping(e['t'], e.get('midi', 84), e.get('g', 0.1)),
    'rumble': lambda e: rumble(e['t'], e.get('d', 2.5)),
    'flash': lambda e: flash(e['t']),
    'counter': lambda e: counter(e['t'], e.get('d', 1.0)),
    'whoosh': lambda e: sfx.add(whoosh(e.get('d', 0.6), e.get('f0', 300), e.get('f1', 2600), e.get('g', 0.14)), e['t'], 1.0, e.get('pan', 0)),
    'count': lambda e: sfx.add(np.sin(2 * np.pi * np.cumsum(N(79) * (N(55) / N(79)) ** ((np.arange(int(e['d'] * SR)) / SR) / e['d'])) / SR)
                                * np.sin(np.pi * (np.arange(int(e['d'] * SR)) / SR) / e['d']) ** 0.5 * 0.06, e['t'], 1.0, 0.3),
}
unknown = set()
for e in EV:
    f = CUES.get(e['k'])
    if f is None:
        unknown.add(e['k']); continue
    f(e)
if unknown:
    print('no sound for event kinds:', sorted(unknown))


# ---------------------------------------------------------------- music
BPM = plan.get('bpm', 96); BEAT = 60 / BPM


def pad(freqs, dur, gain):
    m = int((dur + 1.4) * SR); tt = np.arange(m) / SR; x = np.zeros(m)
    for f in freqs:
        for dt in (-0.004, 0.0, 0.005):
            f2 = f * (1 + dt); x += np.sin(2 * np.pi * f2 * tt + rng.random() * 6) + 0.2 * np.sin(4 * np.pi * f2 * tt + rng.random() * 6)
    return lp(x / len(freqs) / 3, 1300) * np.minimum(1, tt / 1.0) * np.minimum(1, (dur + 1.4 - tt) / 1.3) * gain


def bass(f, dur, g):
    m = int(dur * SR); tt = np.arange(m) / SR
    x = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) + 0.08 * np.sin(6 * np.pi * f * tt)
    return lp(x, 900) * (1 - np.exp(-tt / 0.008)) * np.exp(-tt / 0.45) * np.minimum(1, (dur - tt) / 0.04).clip(0, 1) * g


def shaker(g):
    m = int(0.09 * SR); tt = np.arange(m) / SR
    return hp(rng.standard_normal(m), 5000) * (1 - np.exp(-tt / 0.01)) * np.exp(-tt / 0.025) * g


def soft_kick(g):
    m = int(0.3 * SR); tt = np.arange(m) / SR
    return np.sin(2 * np.pi * np.cumsum(48 + 70 * np.exp(-tt * 30)) / SR) * np.exp(-tt / 0.12) * g


def bell(f, g):
    m = int(2.5 * SR); tt = np.arange(m) / SR
    mod = np.sin(2 * np.pi * f * 3.5 * tt) * 2.0 * np.exp(-tt / 0.4)
    return np.sin(2 * np.pi * f * tt + mod) * np.exp(-tt / 0.9) * (1 - np.exp(-tt / 0.002)) * g


MOOD = {  # gains: pad, pluck, bass, shaker, kick, pluck step pattern
    'calm': dict(pad=0.2, pluck=0.055, bass=0.0, shaker=0.0, kick=0.0),
    'play': dict(pad=0.15, pluck=0.06, bass=0.07, shaker=0.012, kick=0.0),
    'drive': dict(pad=0.14, pluck=0.06, bass=0.08, shaker=0.016, kick=0.05),
    'tense': dict(pad=0.18, pluck=0.035, bass=0.05, shaker=0.0, kick=0.0),
    'reveal': dict(pad=0.24, pluck=0.045, bass=0.06, shaker=0.0, kick=0.0, bell=0.05),
    'hold': dict(pad=0.12, pluck=0.0, bass=0.0, shaker=0.0, kick=0.0),
}
for sec in plan['sections']:
    a, b, chords = sec['t0'], min(sec['t1'], DUR), sec['chords']
    mo = dict(MOOD[sec.get('mood', 'calm')]); mo.update(sec.get('gains', {}))
    seg = (b - a) / len(chords)
    for i, ch in enumerate(chords):
        ta = a + i * seg
        if mo['pad'] > 0: mus.add(pad([N(m - 12) for m in ch], seg, mo['pad']), ta)
        if mo.get('bell'): mus.add(bell(N(ch[-1] + 12), mo['bell']), ta + 0.05, 1.0, 0.25)
        if mo['pluck'] > 0:   # the kit's motif: chord tones in a lilting 2-3 pattern
            k, tt = 0, ta + 0.5
            while tt < ta + seg - 0.3:
                mus.add(pluck(N(ch[[0, 2, 1, 3, 2, 1][k % 6]] + 12), 0.8, mo['pluck']), tt, 1.0, ((k % 5) - 2) * 0.2)
                tt += 0.6 if k % 3 == 2 else 0.3 * (2 + (k % 2)); k += 1
        if mo['bass'] > 0:    # root on beat 1, fifth on beat 3
            bt = ta
            j = 0
            while bt < ta + seg - 0.1:
                f = N(ch[0] - 24) if j % 2 == 0 else N(ch[0] - 24 + 7)
                mus.add(bass(f, min(BEAT * 1.8, ta + seg - bt), mo['bass']), bt, 1.0, -0.05)
                bt += BEAT * 2; j += 1
        if mo['shaker'] > 0 or mo['kick'] > 0:
            k = 0; bt = ta
            while bt < ta + seg - 0.05:
                if mo['shaker'] > 0: mus.add(shaker(mo['shaker'] * (1.0 if k % 2 == 0 else 0.6)), bt + (0.02 if k % 2 else 0), 1.0, 0.35)
                if mo['kick'] > 0 and k % 4 == 0: mus.add(soft_kick(mo['kick']), bt)
                bt += BEAT / 2; k += 1
if plan.get('end'):
    mus.add(tone(N(plan['end']['note']), 3.0, 0.01, 1.2, (1, .5, .25)) * 0.2, plan['end']['t'], 1.0)


# ---------------------------------------------------------------- room, ducking, mix
def room(bus, mix=0.18):
    imp = rng.standard_normal(int(0.45 * SR)) * np.exp(-np.arange(int(0.45 * SR)) / (0.12 * SR)); imp /= np.sum(np.abs(imp)) / 3
    wl = fftconvolve(bus.L, imp)[:n]; wr = fftconvolve(bus.R, imp[::-1])[:n]
    bus.L = (1 - mix) * bus.L + mix * wl; bus.R = (1 - mix) * bus.R + mix * wr


room(sfx, 0.18); room(mus, 0.22)
duck = np.ones(n)
DUCK_DB = plan.get('duck_db', -8.0)
for a, b in NAR:   # music dips under speech, 0.25 s ramps
    i0, i1 = int(max(0, a - 0.25) * SR), int(min(DUR, b + 0.35) * SR)
    duck[i0:i1] = np.minimum(duck[i0:i1], 10 ** (DUCK_DB / 20))
if NAR:
    k = int(0.25 * SR); kern = np.ones(k) / k; duck = np.convolve(duck, kern, 'same')
fade = np.minimum(1, np.minimum(t / 0.05, (DUR - t) / 1.2))
mL, mR = mus.L * duck * fade, mus.R * duck * fade
sL, sR = sfx.L * fade, sfx.R * fade


def write(path, L, R, peak=None):
    st = np.stack([L, R], 1)
    pk = peak if peak else np.max(np.abs(st)) * 1.12 + 1e-9
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st / pk, -1, 1) * 32767).astype('<i2').tobytes())
    return pk


pk = np.max(np.abs(np.stack([mL + sL, mR + sR], 1))) * 1.12 + 1e-9
write(os.path.join(OUT, 'mix.wav'), mL + sL, mR + sR, pk)
write(os.path.join(OUT, 'music.wav'), mL, mR, pk)   # stems share the mix scale, so they sum back to it
write(os.path.join(OUT, 'sfx.wav'), sL, sR, pk)
print('ok', len(EV), 'cues', round(DUR, 2), 's')
```

## tools/timing.py

Время строк и слов: оценка по тексту или метки ElevenLabs. Субтитры EN.

```python
"""Narration timing before the voice exists, and after it.

Input: a narration file. '## <scene>' starts a scene, each other non-empty line is one spoken line
(id = <scene>.<n>), '[pause 0.8]' adds silence, a blank line ends a paragraph (longer gap).
Estimate (no voice): 2.6 words per second, the rate the board's explainer toolkit uses for ElevenLabs English,
plus pauses for punctuation. With --voice <alignment.json> (ElevenLabs with-timestamps character alignment,
one file per line id) the real times replace the estimate.

Outputs (in outdir): timeline.json (lines with t0/t1 and per-word times), narration.json (spoken windows for
music ducking), en.srt (subtitles), summary.txt (duration at slow / estimate / fast speech rates).
usage: python timing.py narration.txt outdir [--wps 2.6] [--lead 1.0] [--voice voicedir]
"""
import json, os, re, sys

args = sys.argv[1:]
src, out = args[0], args[1]
opt = lambda k, d: type(d)(args[args.index(k) + 1]) if k in args else d
WPS, LEAD = opt('--wps', 2.6), opt('--lead', 1.0)
VOICE = opt('--voice', '')
os.makedirs(out, exist_ok=True)

PAUSE = {',': 0.12, ';': 0.2, ':': 0.2, '—': 0.18, '.': 0.32, '?': 0.36, '!': 0.32, '…': 0.45}
PARA_GAP, SCENE_GAP = 0.55, 1.4   # scene gap: eraser sweep (0.9 s) plus a breath before the next board


def words(text):
    return re.findall(r"[^\s]+", text)


def est_line(text, wps):
    """seconds for one spoken line and per-word (start, end) offsets"""
    ws = words(text)
    base = len(ws) / wps
    pauses = sum(PAUSE.get(w[-1], 0) for w in ws[:-1]) + (0.05 if ws else 0)
    total = base + pauses
    weights = [len(re.sub(r'\W', '', w)) + 2 for w in ws]
    sw = sum(weights) or 1
    t, spans = 0.0, []
    for w, k in zip(ws, weights):
        d = base * k / sw
        spans.append((round(t, 3), round(t + d, 3)))
        t += d + PAUSE.get(w[-1], 0) if w is not ws[-1] else d
    return total, spans


def parse(path):
    lines, scene, n = [], None, 0
    for raw in open(path, encoding='utf-8'):
        s = raw.strip()
        if s.startswith('## '):
            scene, n = s[3:].strip(), 0
            lines.append({'kind': 'scene', 'scene': scene})
        elif not s:
            lines.append({'kind': 'para'})
        elif s.startswith('[pause'):
            lines.append({'kind': 'pause', 'd': float(re.findall(r'[\d.]+', s)[0])})
        elif s.startswith('#'):
            continue
        else:
            n += 1
            lines.append({'kind': 'line', 'id': f'{scene}.{n}', 'scene': scene, 'text': s})
    return lines


def layout(items, wps):
    t, tl, first = LEAD, [], True
    for it in items:
        if it['kind'] == 'scene':
            if not first: t += SCENE_GAP
            first = False
        elif it['kind'] == 'para':
            t += PARA_GAP
        elif it['kind'] == 'pause':
            t += it['d']
        else:
            vfile = os.path.join(VOICE, it['id'] + '.json') if VOICE else ''
            if vfile and os.path.exists(vfile):
                al = json.load(open(vfile))   # ElevenLabs alignment: characters, character_start_times_seconds, ..._end_...
                d, spans = voice_spans(it['text'], al)
            else:
                d, spans = est_line(it['text'], wps)
            tl.append({**it, 't0': round(t, 3), 't1': round(t + d, 3),
                       'words': [{'w': w, 't0': round(t + a, 3), 't1': round(t + b, 3)} for w, (a, b) in zip(words(it['text']), spans)]})
            t += d + 0.12
    return tl, t + 1.5


def voice_spans(text, al):
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    spans, i, cur = [], 0, None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur: spans.append(cur); cur = None
        else:
            cur = [a, b] if cur is None else [cur[0], b]
    if cur: spans.append(cur)
    return (en[-1] if en else 0.0), [tuple(s) for s in spans]


def srt_time(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'


def cues(tl, maxc=42, cps=17):
    """split each line into cues of at most two lines of maxc chars, at word boundaries"""
    out = []
    for L in tl:
        ws = L['words']; i = 0
        while i < len(ws):
            j, length = i, 0
            while j < len(ws) and length + len(ws[j]['w']) + 1 <= maxc * 2:
                length += len(ws[j]['w']) + 1; j += 1
            j = max(j, i + 1)
            chunk = ws[i:j]; text = ' '.join(w['w'] for w in chunk)
            if len(text) > maxc:   # break into two balanced lines
                best = min(range(1, len(chunk)), key=lambda k: abs(len(' '.join(w['w'] for w in chunk[:k])) - len(text) / 2))
                text = ' '.join(w['w'] for w in chunk[:best]) + '\n' + ' '.join(w['w'] for w in chunk[best:])
            a, b = chunk[0]['t0'], chunk[-1]['t1']
            b = max(b, a + len(text) / cps)   # long enough to read
            out.append([a, b, text]); i = j
    for k in range(len(out) - 1):   # no overlaps
        out[k][1] = min(out[k][1], out[k + 1][0] - 0.04)
    return out


items = parse(src)
tl, total = layout(items, WPS)
json.dump({'wps': WPS, 'lead': LEAD, 'total': round(total, 2), 'voice': bool(VOICE), 'lines': tl}, open(os.path.join(out, 'timeline.json'), 'w'), indent=1)
json.dump([[L['t0'], L['t1']] for L in tl], open(os.path.join(out, 'narration.json'), 'w'))
with open(os.path.join(out, 'en.srt'), 'w', encoding='utf-8') as f:
    for k, (a, b, text) in enumerate(cues(tl), 1):
        f.write(f'{k}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n\n')
nw = sum(len(words(L['text'])) for L in tl)
rows = []
for w in (2.3, WPS, 2.9):
    _, tt = layout(items, w)
    rows.append(f'{w:.1f} words/s: {int(tt // 60)}:{int(tt % 60):02d}')
open(os.path.join(out, 'summary.txt'), 'w').write(f'{nw} words, {sum(len(L["text"]) for L in tl)} characters, {len(tl)} lines\n' + '\n'.join(rows) + '\n')
print(open(os.path.join(out, 'summary.txt')).read())
```

## tools/cuts.py

Рваные вырезки из фото.

```python
"""Rough magazine cut-outs: the style kit's roughcut() (prep.py) with local paths. Classical image ops, no ML.
usage: python tools/cuts.py   (makes assets/p/<name>.png from assets/src/<key>.jpg, list JOBS below)"""
import cv2, numpy as np, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
C, P = D + '/src/', D + '/p/'
os.makedirs(P, exist_ok=True)
def clean(a, close=9, minfrac=0.01):
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(close,close))
    a=cv2.morphologyEx(a,cv2.MORPH_CLOSE,k); a=cv2.morphologyEx(a,cv2.MORPH_OPEN,k)
    n,lab,st,_=cv2.connectedComponentsWithStats((a>127).astype(np.uint8))
    out=np.zeros_like(a)
    if n>1:
        big=1+np.argmax(st[1:,4])
        for i in range(1,n):
            if st[i,4]>=max(st[big,4]*0.04, 1): out[lab==i]=255
    # fill holes
    inv=255-out; ff=inv.copy(); h,w=ff.shape; mask=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,mask,(0,0),0)
    out=out|ff
    return out
def soft(a, feather=2.0):
    a=cv2.GaussianBlur(a,(0,0),feather)
    return a
def sticker(rgb, alpha, border=14, shrink=1.5):
    """rgb HxWx3 uint8, alpha HxW uint8 -> RGBA with white border (alpha-union), cropped"""
    h,w=alpha.shape
    # slight erode to kill background halo
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(shrink*2)+1,)*2)
    al=cv2.erode(alpha,k)
    al=cv2.GaussianBlur(al,(0,0),1.2)
    pad=border+8
    rgb=cv2.copyMakeBorder(rgb,pad,pad,pad,pad,cv2.BORDER_REPLICATE); al=cv2.copyMakeBorder(al,pad,pad,pad,pad,cv2.BORDER_CONSTANT,value=0)
    kb=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(border*2+1,)*2)
    outer=cv2.dilate((al>100).astype(np.uint8)*255,kb); outer=cv2.GaussianBlur(outer,(0,0),border/6)
    # smooth blobby outline
    outer=cv2.GaussianBlur(outer,(0,0),border/2.2); outer=np.where(outer>120,255,0).astype(np.uint8); outer=cv2.GaussianBlur(outer,(0,0),1.1)
    f=al.astype(np.float32)/255; o=outer.astype(np.float32)/255
    col=rgb.astype(np.float32)*f[...,None]+255*(1-f[...,None])
    res=np.dstack([col,o*255]).clip(0,255).astype(np.uint8)
    ys,xs=np.where(outer>8); res=res[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return res
def save_rgba(path,rgba):  # rgba is RGB order
    bgra=cv2.cvtColor(rgba,cv2.COLOR_RGBA2BGRA); cv2.imwrite(path,bgra)
def load_rgb(p):
    return cv2.cvtColor(cv2.imread(p),cv2.COLOR_BGR2RGB)
def fit(img,maxside):
    h,w=img.shape[:2]; s=maxside/max(h,w)
    return cv2.resize(img,None,fx=s,fy=s,interpolation=cv2.INTER_AREA) if s<1 else img

def crop(img, x0, y0, x1, y1):
    h, w = img.shape[:2]; return img[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]


def halftone(gray, cell=10, angle=45, gamma=1.0, invert=False):
    """gray 0..1 (1 = full ink). Returns ink coverage 0..1, AM dots on a rotated grid, 3x supersampled."""
    ss = 2; h, w = gray.shape
    g = cv2.resize(gray.astype(np.float32), (w*ss, h*ss), interpolation=cv2.INTER_LINEAR)
    g = cv2.GaussianBlur(g, (0, 0), cell*ss*0.35) ** gamma
    if invert: g = 1 - g
    yy, xx = np.mgrid[0:h*ss, 0:w*ss].astype(np.float32); t = np.deg2rad(angle); c = cell*ss
    u = (xx*np.cos(t) + yy*np.sin(t)) / c; v = (-xx*np.sin(t) + yy*np.cos(t)) / c
    d = np.hypot(u - np.round(u), v - np.round(v))           # distance to dot centre, in cells
    r = np.sqrt(np.clip(g, 0, 1) / np.pi) * 1.08                # dot radius for coverage g
    ink = np.clip((r - d) * c * 0.9 + 0.5, 0, 1)
    return cv2.resize(ink, (w, h), interpolation=cv2.INTER_AREA)


def vnoise(h, w, cell, rng):
    """smooth value noise in 0..1, feature size ~cell px"""
    g = rng.random((h // cell + 3, w // cell + 3)).astype(np.float32)
    return cv2.resize(g, ((w // cell + 3) * cell, (h // cell + 3) * cell), interpolation=cv2.INTER_CUBIC)[:h, :w].clip(0, 1)

def fbm(h, w, cells, rng):
    n = sum(vnoise(h, w, c, rng) / (i + 1) for i, c in enumerate(cells)); return (n - n.min()) / (np.ptp(n) + 1e-6)

def roughcut(key, poly, out, maxside=1700, border=22, seed=1, folds=1, ht=0.22, crop_box=None):
    """uneven magazine cut-out: wobbly scissor line into the photo, ragged paper rim of varying width with torn fibres,
    paper grain, print dots, folds and worn edges. Alpha includes the rim; shadow is left to CSS."""
    rng = np.random.default_rng(seed)
    img = fit(load_rgb(C + key + '.jpg'), maxside)
    if crop_box: img = crop(img, *crop_box)
    h, w = img.shape[:2]; pad = int(border * 3)
    img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REPLICATE); H, W = h + 2 * pad, w + 2 * pad
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.array([(pad + x * w, pad + y * h) for x, y in poly], np.int32)], 255)
    dout = cv2.distanceTransform(255 - m, cv2.DIST_L2, 5); din = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    sd = dout - din                                                      # signed distance, >0 outside the polygon
    # photo edge: scissors wander a few px
    photo = sd < (vnoise(H, W, 90, rng) - 0.5) * 9 + (vnoise(H, W, 14, rng) - 0.5) * 2.5
    # paper rim: width varies slowly 0.35..1.6 x border, torn edge adds fibres
    rim = border * (0.35 + 1.25 * fbm(H, W, [160, 70], rng)) + (fbm(H, W, [9, 4, 2], rng) - 0.5) * 9
    sheet = sd < rim
    # paper: warm off-white with grain and fibres
    grain = fbm(H, W, [3, 1], rng); fib = fbm(H, W, [40, 6], rng)
    paper = np.dstack([np.full((H, W), v, np.float32) for v in (240, 235, 222)]) * (0.93 + 0.07 * grain[..., None]) * (0.97 + 0.03 * fib[..., None])
    # photo: magazine print, slight warm fade, dot screen on luminance, grain
    ph = img.astype(np.float32)
    lum = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    dots = halftone(1 - lum, cell=5, angle=45)                           # ink coverage of a black screen
    ph = ph * (1 - ht) + ph * ht * (1 - dots[..., None] * 0.9) + ht * 0.5 * (1 - dots[..., None]) * 40
    ph = ph * 0.94 + np.array([14, 10, 2], np.float32)
    ph = ph * (0.94 + 0.12 * grain[..., None])
    col = np.where(photo[..., None], ph, paper)
    # worn edges: lighter, scuffed paper near the outline and on the photo border
    edge = np.clip(1 - (rim - sd) / (border * 0.9), 0, 1) * sheet
    scuff = (fbm(H, W, [25, 6, 2], rng) > 0.62).astype(np.float32) * np.clip(1 - din / 60, 0, 1) * photo
    col = col + (255 - col) * (0.35 * edge[..., None] + 0.45 * scuff[..., None] * fbm(H, W, [3], rng)[..., None])
    # folds: straight creases with a bright ridge and a shaded side
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for _ in range(folds):
        a = rng.uniform(-0.5, 0.5) + (np.pi / 2 if rng.random() < 0.5 else 0)
        cx, cy = rng.uniform(0.35, 0.65) * W, rng.uniform(0.35, 0.65) * H
        d = (xx - cx) * np.cos(a) + (yy - cy) * np.sin(a) + (vnoise(H, W, 120, rng) - 0.5) * 6
        shade = np.where(d > 0, np.exp(-d / 70) * 0.13, np.exp(d / 25) * -0.05) + np.exp(-(d / 2.5) ** 2) * -0.10
        col = np.where(shade[..., None] > 0, col * (1 - shade[..., None]), col + (255 - col) * -shade[..., None])
    a = cv2.GaussianBlur(sheet.astype(np.float32) * 255, (0, 0), 0.7)
    ys, xs = np.where(a > 8); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    save_rgba(P + out + '.png', np.dstack([col.clip(0, 255).astype(np.uint8), a.astype(np.uint8)])[y0:y1, x0:x1]); print(out, (x1 - x0, y1 - y0))



def tear(seed, notches=3):
    """irregular scissor polygon in 0..1: a slightly skewed quad with a few notches"""
    r = np.random.default_rng(seed); j = lambda a: r.uniform(-a, a)
    base = [(0.02 + j(.02), 0.03 + j(.03)), (0.98 + j(.02), 0.02 + j(.03)), (0.99 + j(.01), 0.97 + j(.02)), (0.01 + j(.01), 0.98 + j(.02))]
    pts = []
    for i in range(4):
        a, b = np.array(base[i]), np.array(base[(i + 1) % 4]); pts.append(tuple(a))
        for k in range(notches):
            f = (k + 1) / (notches + 1) + j(0.08); p = a + (b - a) * f
            nrm = np.array([-(b - a)[1], (b - a)[0]]); nrm /= np.linalg.norm(nrm) + 1e-9
            pts.append(tuple(np.clip(p + nrm * j(0.035), 0, 1)))
    return pts

JOBS = {
    # name: (source key, crop box, polygon or tear seed, maxside, border, seed, folds)
    'cat_flat_rough': ('cat_side_lying', (0.04, 0.36, 0.90, 0.86), 21, 1500, 20, 21, 1),
    'cat_sleep_rough': ('cat_sleep_couch', (0.02, 0.04, 0.98, 0.93), 22, 1300, 18, 22, 1),
    'cat_sideeye_rough': ('cat_lying2', (0.33, 0.04, 0.93, 0.93), 23, 1500, 18, 23, 2),
    'cat_stare_rough': ('cat_staring', (0.08, 0.10, 0.92, 0.70), 24, 1300, 18, 24, 1),
    'cat_black_rough': ('cat_black', (0.22, 0.0, 0.74, 1.0), 25, 1500, 18, 25, 1),
    'cat_yawn_rough': ('cat_yawn_ginger', (0.16, 0.0, 0.86, 1.0), 26, 1500, 18, 26, 1),
    'cat_scream_rough': ('cat_yawn_tux', (0.28, 0.0, 1.0, 0.86), 27, 1500, 18, 27, 2),
    'einstein_rough': ('einstein_1921', (0.10, 0.04, 1.0, 0.78), 31, 1500, 18, 31, 1),
    'lightning_rough': ('lightning_noaa', (0.0, 0.0, 1.0, 1.0), 32, 1500, 18, 32, 1),
    'gps_iif_rough': ('gps_iif_art', (0.0, 0.02, 1.0, 0.98), 33, 1400, 16, 33, 1),
    'gps_navstar_rough': ('gps_navstar2f', (0.04, 0.0, 1.0, 0.86), 34, 1500, 18, 34, 2),
    'nts2_rough': ('nts2', (0.04, 0.04, 0.96, 0.80), 35, 1400, 18, 35, 1),
    'nist_f1_rough': ('nist_f1', (0.0, 0.0, 1.0, 1.0), 36, 900, 12, 36, 1),
    'coffee_rough': ('coffee_mug', (0.12, 0.05, 0.92, 0.95), 37, 1300, 18, 37, 1),
}
if __name__ == '__main__':
    only = sys.argv[1:]
    for name, (key, box, poly, mx, border, seed, folds) in JOBS.items():
        if only and name not in only: continue
        if isinstance(poly, int): poly = tear(poly)
        roughcut(key, poly, name, maxside=mx, border=border, seed=seed, folds=folds, crop_box=box)
```

## tools/commons.py

Поиск и скачивание с Wikimedia Commons с метаданными лицензии.

```python
"""Wikimedia Commons helper: search files, read licence metadata, download. usage:
  commons.py search "<query>" [n]      -> title, licence, size, author for bitmap files
  commons.py get "<File:Title>" <out_prefix>  -> <out>.jpg + <out>.meta.json (API metadata as proof)"""
import json, sys, urllib.parse, urllib.request
API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'studio-asset-check/1.0 (contact: studio agent; licence verification)'}
def api(**p):
    p.update(format='json')
    with urllib.request.urlopen(urllib.request.Request(API + '?' + urllib.parse.urlencode(p), headers=UA), timeout=60) as r:
        return json.load(r)
def meta(titles):
    d = api(action='query', prop='imageinfo', iiprop='url|extmetadata|user|timestamp|size|mime', titles='|'.join(titles), iiurlwidth=2400)
    return list(d['query']['pages'].values())
cmd = sys.argv[1]
if cmd == 'search':
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    d = api(action='query', list='search', srsearch=sys.argv[2] + ' filetype:bitmap', srnamespace=6, srlimit=n)
    titles = [x['title'] for x in d['query']['search']]
    for p in meta(titles):
        ii = p.get('imageinfo', [{}])[0]; em = ii.get('extmetadata', {})
        lic = em.get('LicenseShortName', {}).get('value', '?'); art = em.get('Artist', {}).get('value', '?')
        import re; art = re.sub('<[^>]+>', '', art)[:40]
        print(f"{lic[:22]:22} {ii.get('width')}x{ii.get('height')} {p['title'][:80]} | {art}")
elif cmd == 'get':
    p = meta([sys.argv[2]])[0]; ii = p['imageinfo'][0]
    url = ii.get('thumburl') if ii.get('width', 0) > 2400 else ii['url']
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r: data = r.read()
    open(sys.argv[3] + '.jpg', 'wb').write(data)
    json.dump(p, open(sys.argv[3] + '.meta.json', 'w'), ensure_ascii=False, indent=1)
    em = ii['extmetadata']; print(em.get('LicenseShortName', {}).get('value'), len(data), url)
```

## tools/commons_batch.py

Пакетное скачивание с паузами.

```python
"""download several Commons files politely: pairs 'File:Title|key' on argv; retries 429 with backoff"""
import json, sys, time, urllib.error, subprocess
for i, pair in enumerate(sys.argv[1:]):
    t, k = pair.split('|')
    for attempt in range(6):
        r = subprocess.run([sys.executable, __file__.replace('commons_batch.py', 'commons.py'), 'get', t, k], capture_output=True, text=True)
        if r.returncode == 0: print(k, r.stdout.strip()[:60]); break
        print(k, 'retry', attempt, r.stderr.strip().splitlines()[-1][:80]); time.sleep(20 * (attempt + 1))
    time.sleep(8)
```

## tools/registry.py

Реестр лицензий и паспорта картинок.

```python
"""Licence registry for the GPS video: registry.csv (project template columns), passports.md, metadata copies.
Every row is read from the Commons API metadata saved at download time (assets/src/<key>.meta.json).
usage: python tools/registry.py <docs assets dir> <page.html>   (only cut-outs the page uses are listed)"""
import csv, json, os, re, shutil, sys

OUT, PAGE = sys.argv[1], sys.argv[2]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'docs', 'asset-sources', 'asset-registry-template.csv')
VIDEO = 'Физика простыми словами 01: часы GPS и Эйнштейн (не опубликовано)'
CHANGES = 'рваная вырезка кодом (tools/cuts.py): обрезка, неровный край, бумажная кайма, полутон, сгибы, тень'
PD_BASIS = {'PD US NOAA': ('PD-USGov-NOAA', 'https://commons.wikimedia.org/wiki/Template:PD-USGov-NOAA'),
            'PD NASA': ('PD-USGov-NASA', 'https://commons.wikimedia.org/wiki/Template:PD-USGov-NASA'),
            'PD US Air Force': ('PD-USGov-Military-Air Force', 'https://commons.wikimedia.org/wiki/Template:PD-USGov-Military-Air_Force'),
            'PD US Government': ('PD-USGov', 'https://commons.wikimedia.org/wiki/Template:PD-USGov'),
            'PD US NIST': ('PD-USGov-NIST', 'https://commons.wikimedia.org/wiki/Template:PD-USGov-NIST'),
            'Author died more than 95 years ago public domain images': ('PD-old-95: автор умер в 1928 году; опубликовано в 1921 году', 'https://commons.wikimedia.org/wiki/Template:PD-old-95'),
            'PD-self': ('PD-self: автор передал в общественное достояние', 'https://commons.wikimedia.org/wiki/Template:PD-self')}
# cut-out name -> (source key, what it is, credit line, limits, people/brands/works)
A = {
    'einstein_rough': ('einstein_1921', 'фото: Альберт Эйнштейн у доски, Вена, 1921', 'Photo: Ferdinand Schmutzer, 1921 (public domain)', 'нет',
                       'есть: Альберт Эйнштейн. Права на образ лицензией не покрываются. Наша политика требует согласовать исключение'),
    'lightning_rough': ('lightning_noaa', 'фото: молния ночью', 'Photo: C. Clark, NOAA (public domain)', 'нельзя намекать на одобрение NOAA', 'нет'),
    'gps_iif_rough': ('gps_iif_art', 'рисунок: спутник GPS IIF над Землёй', 'Illustration: NASA (public domain)', 'нельзя эмблемы NASA и намёк на одобрение NASA', 'нет'),
    'gps_navstar_rough': ('gps_navstar2f', 'рисунок: спутник Navstar GPS II-F над Землёй', 'Illustration: U.S. Air Force (public domain)', 'нельзя намекать на одобрение ВВС США', 'нет'),
    'nts2_rough': ('nts2', 'фото: спутник NTS-2 в цеху', 'Photo: U.S. Navy (public domain)', 'нельзя намекать на одобрение ВМС США', 'нет'),
    'nist_f1_rough': ('nist_f1', 'фото: атомные часы NIST-F1', 'Photo: NIST (public domain)', 'нельзя намекать на одобрение NIST', 'нет'),
    'earth_rough': ('earth_as17', 'фото: Земля с Аполлона-17', 'Photo: NASA, Apollo 17 (public domain)', 'нельзя эмблемы NASA и намёк на одобрение NASA', 'нет'),
    'coffee_rough': ('coffee_mug', 'фото: кружка кофе с паром', 'Photo: PedanticNarrativeController (CC0)', 'нет', 'нет'),
    'cat_stare_rough': ('cat_staring', 'фото: кот смотрит в камеру', 'Photo: Zhmila (CC0)', 'нет', 'нет'),
    'cat_scream_rough': ('cat_yawn_tux', 'фото: зевающий чёрно-белый кот', 'Photo: TimVickers (public domain)', 'нет', 'нет'),
    'cat_sideeye_rough': ('cat_lying2', 'фото: кот лёжа косится', 'Photo: Asabae2752 (CC0)', 'нет', 'нет'),
    'cat_flat_rough': ('cat_side_lying', 'фото: кот лежит плашмя на парковке', 'Photo: Gerda Arendt (CC0)', 'нет', 'нет'),
    'cat_sleep_rough': ('cat_sleep_couch', 'фото: рыжий кот спит на диване', 'Photo: TheOmniCommie (CC0)', 'нет', 'нет'),
    'cat_black_rough': ('cat_black', 'фото: чёрный кот', 'Photo: Image Catalog (CC0)', 'нет', 'нет'),
    'cat_yawn_rough': ('cat_yawn_ginger', 'фото: зевающий рыжий кот', 'Photo: David Montolio (CC0)', 'нет', 'нет'),
}
PLAN = sys.argv[3].split(',') if len(sys.argv) > 3 else []   # cut-outs the storyboard plans but the page does not use yet
used = sorted(set(re.findall(r'assets/p/(\w+)\.png', open(PAGE).read())) | set(PLAN), key=list(A).index)
strip = lambda h: re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', h or '')).strip()
os.makedirs(os.path.join(OUT, 'meta'), exist_ok=True); os.makedirs(os.path.join(OUT, 'p'), exist_ok=True)
head = next(csv.reader(open(TEMPLATE, encoding='utf-8-sig')))
rows, md = [], ['# Реестр картинок: часы GPS и Эйнштейн', '',
                'Все картинки ролика — общественное достояние или CC0, с Wikimedia Commons. Лицензия взята со страницы каждого файла через API Commons в день скачивания. Ответ API сохранён в `meta/` как подтверждение. Вырезки сделаны кодом и лежат в `p/`. Сводная таблица в тех же колонках, что шаблон проекта: `registry.csv`.', '']
for i, cut in enumerate(used, 1):
    key, what, credit, limits, people = A[cut]
    meta = json.load(open(os.path.join(SRC, 'src', key + '.meta.json'))); ii = meta['imageinfo'][0]; em = ii['extmetadata']
    lic = strip(em['LicenseShortName']['value']); cats = em.get('Categories', {}).get('value', '').split('|')
    basis = next((PD_BASIS[c] for c in cats if c in PD_BASIS), None)
    lic_url = strip(em.get('LicenseUrl', {}).get('value')) or (basis[1] if basis else '')
    kind = 'CC0' if lic == 'CC0' else 'PD'
    shutil.copy(os.path.join(SRC, 'src', key + '.meta.json'), os.path.join(OUT, 'meta', key + '.meta.json'))
    shutil.copy(os.path.join(SRC, 'p', cut + '.png'), os.path.join(OUT, 'p', cut + '.png'))
    aid = f'PH-2026-{i:04d}'
    r = dict.fromkeys(head, '')
    r.update({'id_ассета': aid, 'что_это': what, 'тип_материала': 'фото' if what.startswith('фото') else 'иллюстрация', 'источник': 'Wikimedia Commons',
              'исходная_ссылка': ii['descriptionurl'], 'id_файла': meta['title'], 'автор': strip(em.get('Artist', {}).get('value'))[:120],
              'дата_скачивания': '2026-10-19' if key.startswith('cat_') else '2026-10-21', 'аккаунт_и_план': 'без аккаунта, API Commons',
              'лицензия': lic + (f' ({basis[0]})' if basis else ''), 'ссылка_на_лицензию': lic_url, 'вид_лицензии': kind,
              'подтверждение_путь': f'docs/pilots/physics/assets/meta/{key}.meta.json', 'сертификат_или_код': 'не нужен',
              'атрибуция_нужна': 'нет, даём по нашей политике', 'текст_атрибуции': credit, 'место_атрибуции_по_лицензии': 'не требуется',
              'где_атрибуция': 'подпись в кадре и описание видео', 'пометка_об_изменениях': 'не требуется', 'ограничения': limits,
              'лица_бренды_произведения': people, 'основание_эмбиент': 'неприменимо', 'создано_ии': 'нет', 'оплата': 'бесплатно',
              'подписка_и_период': 'нет', 'регистрация_у_источника': 'не нужна', 'после_подписки': 'да', 'наши_изменения': CHANGES,
              'видео': VIDEO, 'претензии_content_id': 'нет данных: видео не загружено', 'хранение': f'docs/pilots/physics/assets/p/{cut}.png',
              'примечания': ''})
    rows.append(r)
    md += [f'## {aid}: {what}', '', f'- Файл: [{meta["title"]}]({ii["descriptionurl"]})', f'- Автор: {r["автор"]}',
           f'- Лицензия: {r["лицензия"]}' + (f', {lic_url}' if lic_url else ''), f'- Подтверждение: `meta/{key}.meta.json`, скачано {r["дата_скачивания"]}',
           f'- Подпись в кадре: {credit}', f'- Ограничения: {limits}', f'- Люди, бренды, чужие произведения: {people}', f'- Наши изменения: {CHANGES}',
           f'- Вырезка: `p/{cut}.png`', '']
md += ['## Шрифты', '', '- Caveat и Space Mono: SIL Open Font License 1.1, Google Fonts. Тексты лицензий — в наборе стиля задачи 58, `docs/physics-research/style-kit/fonts/`. Лицензия разрешает использование в видео.', '',
       '## Музыка и звуки', '', '- Свой код, без чужих сэмплов: [музыка](../music.md).', '']
with open(os.path.join(OUT, 'registry.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=head, quoting=csv.QUOTE_ALL); w.writeheader(); w.writerows(rows)
open(os.path.join(OUT, 'passports.md'), 'w', encoding='utf-8').write('\n'.join(md))
print(len(rows), 'assets:', ', '.join(used))
```

## tools/sheet.py

Контактный лист кадров.

```python
"""contact sheet of PNGs: python sheet.py out.jpg cols width a.png b.png ..."""
import sys
from PIL import Image, ImageDraw
out, cols, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); fs = sys.argv[4:]
ims = [Image.open(f).convert('RGB') for f in fs]; h = int(w * ims[0].height / ims[0].width)
rows = (len(ims) + cols - 1) // cols; sh = Image.new('RGB', (cols * (w + 6), rows * (h + 6)), (60, 60, 60))
for i, im in enumerate(ims):
    im = im.resize((w, h)); d = ImageDraw.Draw(im); d.text((8, 6), fs[i].rsplit('/', 1)[-1], fill=(255, 80, 80))
    sh.paste(im, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
sh.save(out, quality=88)
```

## gps/narr.py

Текст для голоса из сценария: строки, доски, паузы.

```python
"""narration.txt from the script's English paragraphs: one line per sentence, boards split where the picture needs a new board,
pauses where the picture needs time. usage: python narr.py script.md narration.txt"""
import re, sys
s = open(sys.argv[1]).read().split('## Сценарий')[1].split('## Где котики')[0]
secs = re.split(r'\*\*(\d+)\. [^*]+\*\*', s)
out = []
for i in range(1, len(secs), 2):
    en = [p.strip() for p in secs[i + 1].strip().split('\n\n') if p.strip()][0]
    out.append(f'## s{int(secs[i]):02d}')
    out += re.split(r'(?<=[.?!])\s+(?=[A-Z])', en)
    out.append('')
t = '\n'.join(out)
for a, b in [("Hear one satellite,", "\n## s03b\nHear one satellite,"),
             ("Let's build the simplest clock there is.", "\n## s05b\nLet's build the simplest clock there is."),
             ("So yes, your head is aging", "\n## s06b\nSo yes, your head is aging"),
             ("Up, down: tock.\n", "Up, down: tock.\n[pause 0.6]\n"),
             ("so it takes a longer, slanted path.\n", "so it takes a longer, slanted path.\n[pause 1.0]\n")]:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(sys.argv[2], 'w').write(t)
```

## gps/narration.txt

Текст для голоса с разметкой досок.

```text
## s01
You open a map.
There's the blue dot.
That's you.
Found in seconds, to within about sixteen feet.
You probably think your phone is just smart.
Nope.
Your phone is listening to clocks.
Clocks in space.
And every one of those clocks would be wrong, if nobody had listened to Einstein.
A guy who died before the first satellite ever launched is keeping your map honest.
Let's see how.

## s02
You already know the trick GPS uses.
Thunderstorm.
Flash.
You start counting.
One Mississippi, two Mississippi, three...
Boom.
Every five seconds is about a mile.
The sound came late, and the delay told you how far away the lightning was.

## s03
GPS does the same thing, only with light instead of sound.
Every satellite keeps shouting two things: exactly what time it is, and exactly where it is.
That message takes less than a tenth of a second to reach you.
Your phone checks how late it arrived.
The delay is your distance.

## s03b
Hear one satellite, and you're somewhere on a giant ball around it.
Hear three, and the balls cross in just two spots.
One is way out in space.
The other one is you.
A fourth one fixes your phone's own clock, which, let's be honest, is cheap.

## s04
Here's the catch.
Light is fast.
In one billionth of a second, it goes about one foot.
So if a satellite's clock is off by just one millionth of a second, your distance to it is off by a thousand feet.
That's why every GPS satellite carries atomic clocks, good to a few billionths of a second a day.
Simple plan: put perfect clocks in the sky, sync them with the ground, done.
A second up there is a second down here.
Right?
Wrong.
Twice.

## s05
Wrong number one: speed.
GPS satellites race around the Earth at about eight thousand seven hundred miles an hour.
Twice a day around the whole planet.

## s05b
Let's build the simplest clock there is.
Two mirrors, one flash of light bouncing between them.
Up, down: tick.
Up, down: tock.
[pause 0.6]
Now put that clock on a satellite.
From down here, the light doesn't go straight up and down anymore.
The mirrors move while it flies, so it takes a longer, slanted path.
[pause 1.0]
And here's what Einstein figured out: the speed of light doesn't care how fast you're going.
Same speed, longer path.
So every tick takes longer.
The moving clock runs slow.
It's not broken.
That's just what time does.
For a GPS satellite, it's about seven millionths of a second lost every day.

## s06
Wrong number two is even weirder.
Gravity slows time down.
The closer you are to something big and heavy, like the Earth, the slower your clock runs.
Go higher, and time speeds up.
You don't have to take that on faith.
In 2010, scientists in Colorado raised one super-precise clock by about a foot.
The raised clock ran faster.

## s06b
So yes, your head is aging faster than your feet.
We did the math: stand for eighty years, and your head ends up almost half a millionth of a second older.
The cat's been lying flat all day.
Now you know why.

## s07
GPS satellites aren't a foot up.
They're over twelve thousand miles up, where Earth's pull is much weaker.
So their clocks run fast: about forty-five millionths of a second ahead, every day.

## s08
Put both together.
Speed: minus seven.
Height: plus forty-five.
Every day, a satellite clock gets ahead of clocks on the ground by about thirty-eight millionths of a second.
Sounds like nothing.
But light covers about seven miles in that time.
For a system that turns time into distance, that's seven miles of mistake.
Added every single day.

## s09
So what did the engineers do?
They didn't argue with Einstein.
They cheated.
They set each satellite clock to run a little slow.
Its heartbeat should be ten point two three million ticks a second.
On the satellite, it's set to ten point two two nine nine nine nine nine nine five four three.
Slower by less than half a part in a billion.
On the ground, that clock would be wrong.
In orbit, once Einstein is done with it, it ticks at just the right rate.
And the team on the ground still checks every clock and sends small corrections up every day.

## s10
Did they trust Einstein?
Not completely.
In 1977, they launched a test satellite with that correction switched off.
Just in case.
For about three weeks they watched its clock run on its own.
It ran fast by about four hundred forty-three parts in a trillion.
Einstein's prediction: about four hundred forty-five.
Within half a percent.
Then they switched the correction on.

## s11
Want to see it yourself?
Go outside, open a GPS status app on an Android phone, and look at the satellites it hears right now.
Find the ones marked GPS.
Every one of them is carrying clocks that were set slow on purpose.

## s12
So next time the blue dot finds you, two of Einstein's ideas just did the math for you.
Speed slows time.
Gravity slows time.
And your phone needs both to find your coffee.
Now go check on the cat.
It's been lying flat this whole time.
Aging very evenly.
```

## gps/ru_lines.txt

Русские субтитры по строкам.

```text
s01.1|Открываешь карту.
s01.2|Вот синяя точка.
s01.3|Это ты.
s01.4|Нашёлся за секунды, с точностью около пяти метров.
s01.5|Ты, наверное, думаешь, что телефон просто умный.
s01.6|Нет.
s01.7|Твой телефон слушает часы.
s01.8|Часы в космосе.
s01.9|И все эти часы врали бы, если бы никто не послушал Эйнштейна.
s01.10|Человек, который умер раньше, чем полетел первый спутник, не даёт твоей карте врать.
s01.11|Давай разберёмся как.
s02.1|Ты уже знаешь трюк, на котором работает GPS.
s02.2|Гроза.
s02.3|Вспышка.
s02.4|Начинаешь считать.
s02.5|Раз, два, три...
s02.6|Бах.
s02.7|Каждые три секунды — примерно километр.
s02.8|Звук опоздал, и опоздание сказало тебе, как далеко ударила молния.
s03.1|GPS делает то же самое, только со светом вместо звука.
s03.2|Каждый спутник всё время кричит две вещи: точное время и где он сам находится.
s03.3|Сообщение летит к тебе меньше десятой доли секунды.
s03.4|Телефон смотрит, насколько оно опоздало.
s03.5|Опоздание — это расстояние.
s03b.1|Слышишь один спутник — ты где-то на огромном шаре вокруг него.
s03b.2|Слышишь три — шары пересекаются всего в двух точках.
s03b.3|Одна далеко в космосе.
s03b.4|Другая — ты.
s03b.5|Четвёртый поправляет часы самого телефона, которые, будем честны, дешёвые.
s04.1|Вот подвох.
s04.2|Свет быстрый.
s04.3|За миллиардную долю секунды он проходит около 30 сантиметров.
s04.4|Если часы спутника ошиблись всего на миллионную долю секунды, расстояние до него ошибётся на 300 метров.
s04.5|Поэтому на каждом спутнике GPS стоят атомные часы: за сутки они уходят лишь на несколько миллиардных секунды.
s04.6|Простой план: повесить идеальные часы в небе, сверить с землёй, готово.
s04.7|Секунда там — секунда здесь.
s04.8|Так?
s04.9|Нет.
s04.10|Дважды нет.
s05.1|Ошибка первая: скорость.
s05.2|Спутники GPS несутся вокруг Земли со скоростью около 14 тысяч километров в час.
s05.3|Дважды в сутки вокруг всей планеты.
s05b.1|Соберём самые простые часы на свете.
s05b.2|Два зеркала, между ними прыгает вспышка света.
s05b.3|Вверх, вниз — тик.
s05b.4|Вверх, вниз — так.
s05b.5|Теперь поставим эти часы на спутник.
s05b.6|Снизу видно: свет уже не ходит прямо вверх-вниз.
s05b.7|Зеркала сдвигаются, пока он летит, и путь становится длиннее и косым.
s05b.8|И вот что понял Эйнштейн: скорости света всё равно, как быстро ты движешься.
s05b.9|Скорость та же, путь длиннее.
s05b.10|Значит, каждый тик дольше.
s05b.11|Движущиеся часы идут медленнее.
s05b.12|Они не сломаны.
s05b.13|Просто так устроено время.
s05b.14|Для спутника GPS это около семи миллионных секунды в сутки.
s06.1|Ошибка вторая ещё страннее.
s06.2|Гравитация замедляет время.
s06.3|Чем ближе ты к чему-то большому и тяжёлому, вроде Земли, тем медленнее идут твои часы.
s06.4|Поднимись выше — и время ускорится.
s06.5|Верить на слово не нужно.
s06.6|В 2010 году учёные в Колорадо подняли одни сверхточные часы примерно на 30 сантиметров.
s06.7|Поднятые часы пошли быстрее.
s06b.1|Так что да, голова стареет быстрее ног.
s06b.2|Мы посчитали: простой восемьдесят лет — и голова станет старше почти на полмиллионной секунды.
s06b.3|Кот весь день лежит плашмя.
s06b.4|Теперь ты знаешь почему.
s07.1|Спутники GPS не на 30 сантиметров выше.
s07.2|Они выше 20 тысяч километров, где притяжение Земли намного слабее.
s07.3|Поэтому их часы спешат: примерно на сорок пять миллионных секунды в сутки.
s08.1|Сложим.
s08.2|Скорость: минус семь.
s08.3|Высота: плюс сорок пять.
s08.4|Каждые сутки часы спутника убегают вперёд от наземных примерно на тридцать восемь миллионных секунды.
s08.5|Звучит как ничто.
s08.6|Но свет за это время проходит около 11 километров.
s08.7|Для системы, которая превращает время в расстояние, это 11 километров ошибки.
s08.8|Каждые сутки заново.
s09.1|Что сделали инженеры?
s09.2|Они не спорили с Эйнштейном.
s09.3|Они схитрили.
s09.4|Они ставят часы каждого спутника чуть медленнее.
s09.5|Их пульс должен быть 10,23 миллиона тиков в секунду.
s09.6|На спутнике он выставлен 10,22999999543 миллиона.
s09.7|Медленнее меньше чем на половину миллиардной доли.
s09.8|На земле такие часы врали бы.
s09.9|На орбите, когда Эйнштейн с ними закончит, они идут с нужной скоростью.
s09.10|А команда на земле всё равно сверяет каждые часы и каждый день шлёт наверх мелкие поправки.
s10.1|Доверяли ли они Эйнштейну?
s10.2|Не до конца.
s10.3|В 1977 году запустили пробный спутник с выключенной поправкой.
s10.4|На всякий случай.
s10.5|Около трёх недель смотрели, как его часы идут сами по себе.
s10.6|Они спешили примерно на 443 триллионных доли.
s10.7|Предсказание Эйнштейна: около 445.
s10.8|Разница меньше половины процента.
s10.9|После этого поправку включили.
s11.1|Хочешь увидеть сам?
s11.2|Выйди на улицу, открой на телефоне с Android приложение со статусом GPS и посмотри, какие спутники он слышит прямо сейчас.
s11.3|Найди те, что помечены GPS.
s11.4|Каждый из них несёт часы, которые нарочно поставили медленнее.
s12.1|Так что в следующий раз, когда синяя точка тебя найдёт, знай: две идеи Эйнштейна только что посчитали за тебя.
s12.2|Скорость замедляет время.
s12.3|Гравитация замедляет время.
s12.4|И телефону нужны обе, чтобы найти твой кофе.
s12.5|А теперь проверь кота.
s12.6|Он всё это время лежал плашмя.
s12.7|Стареет очень равномерно.
```

## gps/srt_ru.py

Русские субтитры на времени английских строк.

```python
"""Russian subtitles on the same line timings as the English track: python srt_ru.py timeline.json ru_lines.txt out.srt"""
import json, sys
tl = json.load(open(sys.argv[1]))['lines']
ru = dict(l.split('|', 1) for l in open(sys.argv[2], encoding='utf-8').read().strip().split('\n'))
def wrap(t, n=42):   # two balanced lines at a word boundary
    if len(t) <= n: return t
    w = t.split(); best = min(range(1, len(w)), key=lambda k: abs(len(' '.join(w[:k])) - len(t) / 2))
    return ' '.join(w[:best]) + '\n' + ' '.join(w[best:])
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'
cues = []
for L in tl:
    t, a, b = ru[L['id']], L['t0'], L['t1']
    parts = [t]
    if len(t) > 84:   # split a long line in two cues at the word nearest the middle, time shared by length
        w = t.split(); k = min(range(1, len(w)), key=lambda k: abs(len(' '.join(w[:k])) - len(t) / 2)); parts = [' '.join(w[:k]), ' '.join(w[k:])]
    tot = sum(len(p) for p in parts); x = a
    for p in parts:
        d = (b - a) * len(p) / tot; cues.append([x, x + d, wrap(p)]); x += d
for k in range(len(cues) - 1): cues[k][1] = min(cues[k][1], cues[k + 1][0] - 0.04)
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    for i, (a, b, t) in enumerate(cues, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n')
print(len(cues), 'cues')
```

## gps/eleven.py

Документ «Текст для ElevenLabs».

```python
"""Text for ElevenLabs from narration.txt: one request per line, ids match the picture timeline.
usage: python eleven.py narration.txt out.md"""
import re, sys
TITLES = {'s01': 'Крючок', 's02': 'Гроза', 's03': 'Спутник кричит время', 's03b': 'Три шара', 's04': 'Подвох: свет быстрый',
          's05': 'Ошибка первая: скорость', 's05b': 'Световые часы', 's06': 'Ошибка вторая: высота', 's06b': 'Голова и ноги',
          's07': 'Спутник высоко', 's08': 'Итог', 's09': 'Как это чинят', 's10': 'Проверка 1977 года', 's11': 'Проверь сам', 's12': 'Финал'}
src, out = sys.argv[1], sys.argv[2]
body, scene, n, chars, total = [], None, 0, 0, 0
for raw in open(src, encoding='utf-8'):
    s = raw.strip()
    if s.startswith('## '):
        scene, n = s[3:].strip(), 0
        body += ['', f'## {scene} · {TITLES.get(scene, "")}', '']
    elif s.startswith('[pause'):
        body.append(f'- пауза {re.findall(r"[0-9.]+", s)[0]} с — не озвучивать, держим мы')
    elif s and not s.startswith('#'):
        n += 1; total += 1; chars += len(s)
        body.append(f'- `{scene}.{n}` {s}')
head = ['# Текст для ElevenLabs: часы GPS и Эйнштейн', '',
        'Текст для озвучки, отдельно от сценария. Синтеза ещё не было: ElevenLabs не подключён, проб не делали.', '',
        '## Как озвучивать', '',
        f'- Один запрос на строку: {total} строк, {chars} знаков. Номер строки — имя файла и ключ для картинки, например `s05b.3`.',
        '- Запрос `with-timestamps`: в ответе время каждого символа. По нему встанут кадры и субтитры ([план подгонки](timing-plan.md)).',
        '- Модель: Multilingual v2. Метки времени для неё описаны в справочнике. Для v3 и v4 это не подтверждено.',
        '- Голос выбирает автор после пробы 2–3 голосов на строках `s01.1`–`s01.6`. Тон живой, весёлый, на «ты».',
        '- Начальные настройки для пробы: stability 0.40, similarity 0.75, style 0.30, speaker boost включён, скорость 1.0. Это стартовая точка, не проверено на слух.',
        '- Между строками и досками паузы держим мы. Теги пауз в текст не вставлять.',
        '- Числа уже написаны словами, как их надо произнести. «GPS» читается по буквам.',
        '- Аудио и метки каждой строки хранить: повторная генерация даёт другой результат.', '',
        '## Произношение', '',
        '- «ten point two two nine nine nine nine nine nine nine five four» — медленно и ровно, это шутка про длинное число.',
        '- «One Mississippi, two Mississippi, three...» — счёт с паузами, как в грозу.',
        '- «Nope.», «Wrong.», «Twice.», «Boom.» — отдельные короткие реплики, с ударением.']
for extra in sys.argv[3:]:   # Shorts: their own lines, same rules
    title = {'short1': 'Short 1: Moving Clocks Run Slow', 'short2': 'Short 2: Your Head Is Older Than Your Feet'}.get(extra.split('/')[-2], extra)
    body += ['', f'## {title}', '']; n = 0; sc = None
    for raw in open(extra, encoding='utf-8'):
        t = raw.strip()
        if t.startswith('## '): sc, n = t[3:].strip(), 0
        elif t.startswith('[pause'): body.append(f'- пауза {re.findall(r"[0-9.]+", t)[0]} с — не озвучивать, держим мы')
        elif t: n += 1; body.append(f'- `{sc}.{n}` {t}')
open(out, 'w', encoding='utf-8').write('\n'.join(head + body) + '\n')
print(total, 'lines', chars, 'chars')
```

## gps/music_plan.py

План музыки по доскам.

```python
"""Music plan for the GPS video from the page's board windows: one section per board, mood by board.
usage: python music_plan.py events.json plan.json"""
import json, sys
info = json.load(open(sys.argv[1])); DUR = info['frames'] / info['fps']
MOOD = {'s01': 'calm', 's02': 'tense', 's03': 'play', 's03b': 'play', 's04': 'tense', 's05': 'drive', 's05b': 'play', 's06': 'tense',
        's06b': 'play', 's07': 'reveal', 's08': 'drive', 's09': 'play', 's10': 'tense', 's11': 'calm', 's12': 'reveal',
        'h1': 'play', 'h1b': 'play', 'h1c': 'reveal', 'h2': 'play', 'h2b': 'tense', 'h2c': 'reveal'}
CH = {'calm': [[60, 64, 67, 71], [57, 60, 64, 67]],
      'play': [[53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 62], [57, 60, 64, 67]],
      'tense': [[50, 53, 57, 60], [46, 50, 53, 57]],
      'drive': [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]],
      'reveal': [[53, 57, 60, 64], [55, 59, 62, 67], [60, 64, 67, 71]]}
SC = info['scenes']; secs = []
for i, (sid, t0, te) in enumerate(SC):
    t1 = SC[i + 1][1] if i + 1 < len(SC) else DUR
    mood = MOOD.get(sid, 'calm'); ch = CH[mood]
    n = max(1, round((t1 - t0) / 5.0))                  # a chord about every 5 s, the progression repeats
    secs.append({'t0': round(t0, 3), 't1': round(t1, 3), 'mood': mood, 'chords': [ch[k % len(ch)] for k in range(n)]})
plan = {'bpm': 96, 'seed': 20261021, 'sections': secs, 'end': {'t': round(DUR - 3.2, 2), 'note': 48}}
json.dump(plan, open(sys.argv[2], 'w'), indent=1)
print(len(secs), 'sections,', round(DUR, 1), 's')
```

## gps/page.tpl.html

Шаблон страницы ролика.

```html
<!doctype html><html><head><meta charset="utf-8"><title>GPS clocks and Einstein</title>
<link rel="stylesheet" href="../lib/chalk.css">
<style>
.flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
</style>
<script src="../lib/chalk.js"></script></head><body>
<script>Chalk.chrome()</script>

{{MARKUP}}
<script>
const { $, el, at, cut, cl, out3 } = Chalk;
// narration timeline (estimate now, ElevenLabs alignment later): every visual is keyed to a line or a word
const TLJ = (() => { const x = new XMLHttpRequest(); x.open('GET', 'timing/timeline.json', false); x.send(); return JSON.parse(x.responseText); })();
const LN = {}; TLJ.lines.forEach(L => LN[L.id] = L);
const T = (id, f = 0) => LN[id].t0 + f * (LN[id].t1 - LN[id].t0);
const E = id => LN[id].t1;
const W = (id, w, k = 0) => { const ws = LN[id].words.filter(x => x.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(w.toLowerCase())); if (!ws[k]) throw new Error(`word ${w} not in ${id}`); return ws[k].t0; };
const lines = s => TLJ.lines.filter(L => L.scene === s);
const FPS = 30, ER = Chalk.cfg.erase;
const SCN = [...new Set(TLJ.lines.map(L => L.scene))].filter(s => $(s));
// scene windows: a board starts once the previous one is erased, and is erased 0.25 s after its last line
const WIN = {}; let prevEnd = 0;
SCN.forEach((s, i) => { const L = lines(s); const t0 = i ? prevEnd : 0, te = L[L.length - 1].t1 + 0.25; WIN[s] = [t0, te]; prevEnd = te + ER + 0.05; });
const FULL = SCN.length === new Set(TLJ.lines.map(L => L.scene)).size;   // false while only the first scenes exist (probe)
const NF = Math.round((FULL ? TLJ.total : WIN[SCN[SCN.length - 1]][1] + ER + 0.5) * FPS);
SCN.forEach((s, i) => Chalk.scene(s, WIN[s][0], FULL && i === SCN.length - 1 ? 1e9 : WIN[s][1]));   // the last board of the film stays
const hold = s => WIN[s][1];   // cut-outs leave just before the eraser

const HOOKS = [];   // per-frame updates of each board
const spin = (id, deg) => { const n = $(id); n.style.transformBox = 'view-box'; n.style.transformOrigin = `${n.dataset.cx}px ${n.dataset.cy}px`; n.style.transform = `rotate(${deg.toFixed(2)}deg)`; };
{{SCRIPT}}
window.onFrame = (t, active) => HOOKS.forEach(h => h(t, active));
const TEX = ['Δt = γΔτ', 'γ = 1/√(1 − v²/c²)', 'v ≈ 3.87 km/s', 'Δf/f = −4.4647·10⁻¹⁰', 'ΔU/c²', 'GM/r', 'c = 299 792 458 m/s', 
  '10.23 MHz', 'r ≈ 26 562 km', 'T ≈ 11 h 58 min', '½ v²/c²', 'd = c·Δt', '1 ns ≈ 30 cm', 'gh/c²', 'L1 1575.42 MHz', 'x² + y² + z²', 'Δt·c'];
Chalk.start({ frames: NF, fps: FPS, formulas: TEX });
</script></body></html>
```

## gps/build.py

Сборка страницы ролика из досок.

```python
"""Assemble gps.html from page.tpl.html and the board parts (parts/<board>.html + .js, in ORDER).
usage: python build.py [out.html] [--only s01,s02]  (--only builds a probe with the first boards)"""
import os, sys
D = os.path.dirname(os.path.abspath(__file__))
ORDER = ['s01', 's03', 's05', 's08', 's10', 's12']   # part files; each may hold several boards
args = sys.argv[1:]; out = next((a for a in args if a.endswith('.html')), os.path.join(D, 'gps.html'))
only = args[args.index('--only') + 1].split(',') if '--only' in args else None
parts = [p for p in ORDER if os.path.exists(os.path.join(D, 'parts', p + '.html')) and (not only or p in only)]
tpl = open(os.path.join(D, 'page.tpl.html')).read()
markup = '\n'.join(open(os.path.join(D, 'parts', p + '.html')).read() for p in parts)
script = '\n'.join(open(os.path.join(D, 'parts', p + '.js')).read() for p in parts)
open(out, 'w').write(tpl.replace('{{MARKUP}}', markup).replace('{{SCRIPT}}', script))
print(out, 'boards from', parts)
```

## gps/parts/s01.html

Доски 1–2: разметка.

```html
<!-- s01 hook: the blue dot listens to clocks in space -->
<div class="sc" id="s01">
 <div class="lab" id="a_lab" style="left:120px;top:56px">PHYSICS, PLAINLY · 01</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  <path id="a_phone" d="M196 150 H 454 Q 500 150 500 196 V 884 Q 500 930 454 930 H 196 Q 150 930 150 884 V 196 Q 150 150 196 150 Z"/>
  <path id="a_slot" d="M290 182 H 360" stroke-width="5"/>
 </g></svg>
 <svg class="draw" width="1920" height="1080" id="a_map"><g fill="none" stroke="#f4f1ea" stroke-width="3" stroke-linecap="round" opacity=".45">
  <path d="M178 330 C 260 350 380 320 472 345"/><path d="M178 470 C 280 480 360 455 472 470"/><path d="M178 760 C 270 740 380 780 472 755"/>
  <path d="M240 210 C 250 400 230 600 260 900"/><path d="M410 210 C 395 420 430 640 400 900"/><path d="M178 610 L 472 690" stroke-dasharray="10 9"/>
 </g></svg>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <circle id="a_acc" cx="330" cy="560" r="64" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="12 10"/>
  <circle id="a_ring" cx="330" cy="560" r="28" stroke="#9fd0ff" stroke-width="4"/>
  <circle id="a_dot" cx="330" cy="560" r="17" fill="#9fd0ff" stroke="none"/>
  <path id="a_w1" d="M530 168 A 60 60 0 0 1 560 222" stroke="#f4f1ea" stroke-width="5"/>
  <path id="a_w2" d="M556 136 A 100 100 0 0 1 604 232" stroke="#f4f1ea" stroke-width="5"/>
  <path id="a_w3" d="M584 104 A 140 140 0 0 1 648 240" stroke="#f4f1ea" stroke-width="5"/>
 </g></svg>
 <svg class="draw" width="1920" height="1080" id="a_clocks"></svg>
 <div class="ck" id="a_smart" style="left:600px;top:300px;font-size:72px">just smart?</div>
 <div class="ck" id="a_nope" style="left:610px;top:380px;font-size:140px;font-weight:700;color:#ffb36b;transform:rotate(-4deg)">Nope.</div>
 <div class="ck" id="a_you" style="left:540px;top:530px;font-size:64px;color:#9fd0ff">← you</div>
 <div class="ck" id="a_5m" style="left:540px;top:612px;font-size:44px;opacity:.85">≈ 5 m (16 ft)</div>
 <div class="ck" id="a_wrong" style="left:1010px;top:262px;font-size:56px;color:#ff8f7a;transform:rotate(-3deg)">all wrong!</div>
 <div class="cw" id="c_cat1" style="left:600px;top:716px;width:300px;height:283px">
  <img src="../assets/p/cat_stare_rough.png" style="transform:rotate(-3deg)">
  <svg class="draw" width="300" height="283" style="left:0;top:0"><g fill="none" stroke="#f4f1ea" stroke-width="5" stroke-linecap="round">
   <circle id="a_g1" cx="118" cy="178" r="30"/><circle id="a_g2" cx="194" cy="178" r="30"/><path id="a_g3" d="M148 176 q 8 -8 16 0"/></g></svg>
 </div>
 <div class="ck" id="a_trust" style="left:920px;top:930px;font-size:46px;transform:rotate(-2deg)">← trusts the phone</div>
 <div class="cw" id="c_ein" style="left:1390px;top:292px;width:420px;height:438px">
  <img src="../assets/p/einstein_rough.png" style="transform:rotate(3deg)">
  <div class="tape" id="a_tape" style="left:140px;top:-22px;transform:rotate(-5deg)"></div>
 </div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-width="6" stroke-linecap="round">
  <path id="a_tl" d="M1300 860 C 1450 856 1650 864 1820 858"/>
  <path id="a_t1" d="M1420 842 V 878"/><path id="a_t2" d="M1660 842 V 878"/>
 </g></svg>
 <div class="ck" id="a_1955" style="left:1382px;top:788px;font-size:44px">1955</div>
 <div class="ck" id="a_died" style="left:1330px;top:890px;font-size:40px;opacity:.85">Einstein dies</div>
 <div class="ck" id="a_1957" style="left:1622px;top:788px;font-size:44px;color:#9fd0ff">1957</div>
 <div class="ck" id="a_sat" style="left:1586px;top:890px;font-size:40px;opacity:.85">first satellite</div>
 <div class="lab" id="a_cred" style="left:1330px;top:1032px;font-size:14px">PHOTO: F. SCHMUTZER, 1921 · PUBLIC DOMAIN</div>
</div>

<!-- s02 the thunderstorm trick -->
<div class="sc" id="s02">
 <div class="cw" id="c_bolt" style="left:110px;top:130px;width:640px;height:423px">
  <img src="../assets/p/lightning_rough.png" style="transform:rotate(-2deg)">
  <div class="tape" id="b_tape" style="left:250px;top:-24px;transform:rotate(4deg)"></div>
 </div>
 <div class="ck" id="b_flash" style="left:600px;top:592px;font-size:84px;color:#ffe48a;transform:rotate(-6deg)">flash!</div>
 <div class="ck" id="b_c1" style="left:880px;top:150px;font-size:80px">1 Mississippi</div>
 <div class="ck" id="b_c2" style="left:880px;top:250px;font-size:80px">2 Mississippi</div>
 <div class="ck" id="b_c3" style="left:880px;top:350px;font-size:80px">3 …</div>
 <div class="ck" id="b_boom" style="left:1380px;top:200px;font-size:180px;font-weight:700;color:#ffb36b;transform:rotate(-6deg)">BOOM</div>
 <div class="ck" id="b_5s" style="left:880px;top:510px;font-size:110px;font-weight:600">5 s ≈ 1 mile</div>
 <div class="lab" id="b_lab" style="left:886px;top:650px;font-size:18px">SOUND: 343 M/S, SO 1 MILE TAKES 4.7 S (COMPUTED)</div>
 <div class="ck" id="b_late" style="left:880px;top:730px;font-size:76px;color:#9fd0ff">late sound = distance</div>
 <div class="cw" id="c_kit1" style="left:170px;top:640px;width:300px;height:260px">
  <img src="../assets/p/cat_scream_rough.png" style="transform:rotate(4deg)">
 </div>
 <div class="ck" id="b_hid" style="left:500px;top:880px;font-size:50px;transform:rotate(-2deg)">← counted to three. hid.</div>
 <div class="lab" id="b_cred" style="left:110px;top:1032px;font-size:14px">PHOTO: C. CLARK, NOAA · PUBLIC DOMAIN</div>
 <div class="flash" id="b_fl"></div>
</div>
```

## gps/parts/s01.js

Доски 1–2: таймлайн.

```js
// ---------- s01
{
  const g = $('a_clocks'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round' };
  [[1060, 180], [1240, 120], [1420, 190], [1600, 130]].forEach(([x, y], i) => {
    el(g, 'circle', { ...S, id: `a_k${i}`, cx: x, cy: y, r: 50, 'stroke-width': 6 });
    for (let j = 0; j < 4; j++) { const a = j * Math.PI / 2; el(g, 'line', { ...S, id: `a_k${i}m${j}`, x1: x + Math.cos(a) * 38, y1: y + Math.sin(a) * 38, x2: x + Math.cos(a) * 46, y2: y + Math.sin(a) * 46, 'stroke-width': 4 }); }
    el(g, 'line', { ...S, id: `a_k${i}h`, x1: x, y1: y, x2: x, y2: y - 24, 'stroke-width': 6, 'data-cx': x, 'data-cy': y });
    el(g, 'line', { ...S, id: `a_k${i}s`, x1: x, y1: y, x2: x, y2: y - 38, 'stroke-width': 3, 'data-cx': x, 'data-cy': y });
  });
}
cut('c_cat1', { t: W('s01.5', 'smart'), from: [0, 420, 0], back: 1.2, wig: [T('s01.6')], out: hold('s01') - 0.6, to: [0, 700, 0] });
cut('c_ein', { t: W('s01.9', 'Einstein'), from: [700, -80, 20], wig: [W('s01.10', 'honest')], out: hold('s01') - 0.6, to: [900, -200, 18] });
at(0.2, 0.6, 'fade', 'a_lab');
at(T('s01.1') - 0.3, 1.5, 'draw', 'a_phone'); at(T('s01.1', .8), 0.25, 'draw', 'a_slot', { quiet: 1 }); at(E('s01.1') - 0.2, 0.9, 'wipe', 'a_map');
at(W('s01.2', 'blue'), 0.35, 'pop', 'a_dot');
at(W('s01.2', 'blue') + 0.1, 0.4, 'fn', 'a_ring', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; const p = ((t - W('s01.2', 'blue')) % 1.6) / 1.6; n.setAttribute('r', 20 + 30 * p); n.style.opacity = on ? (1 - p) * 0.9 : 0; } });
at(W('s01.3', 'you'), 0.6, 'write', 'a_you');
at(W('s01.4', 'within'), 0.9, 'draw', 'a_acc', { quiet: 1 }); at(W('s01.4', 'sixteen'), 1.0, 'write', 'a_5m');
at(W('s01.5', 'smart') - 0.2, 0.9, 'write', 'a_smart');
at(T('s01.6'), 0.4, 'pop', 'a_nope');
['a_w1', 'a_w2', 'a_w3'].forEach((id, i) => at(W('s01.7', 'listening') + i * 0.18, 0.3, 'draw', id, { quiet: i > 0 }));
for (let i = 0; i < 4; i++) {
  at(T('s01.8') + i * 0.22, 0.45, 'draw', `a_k${i}`, { note: i });
  for (let j = 0; j < 4; j++) at(T('s01.8') + i * 0.22 + 0.3, 0.1, 'draw', `a_k${i}m${j}`, { quiet: 1 });
  at(T('s01.8') + i * 0.22 + 0.35, 0.15, 'draw', `a_k${i}h`, { quiet: 1 }); at(T('s01.8') + i * 0.22 + 0.4, 0.15, 'draw', `a_k${i}s`, { quiet: 1 });
}
Chalk.event(T('s01.8') + 1.0, 'tick', { n: 6, every: 0.5, g: 0.1, f: 2800 });
at(W('s01.9', 'wrong'), 0.8, 'write', 'a_wrong');
at(W('s01.5', 'smart') + 1.6, 1.0, 'write', 'a_trust');
at(W('s01.9', 'Einstein') + 0.55, 0.25, 'tape', 'a_tape');
['a_g1', 'a_g2', 'a_g3'].forEach((id, i) => at(W('s01.5', 'smart') + 0.9 + i * 0.2, 0.25, 'draw', id, { quiet: i > 0 }));
at(W('s01.10', 'died') - 0.3, 0.8, 'draw', 'a_tl'); at(W('s01.10', 'died'), 0.15, 'draw', 'a_t1', { quiet: 1 });
at(W('s01.10', 'died') + 0.1, 0.5, 'write', 'a_1955'); at(W('s01.10', 'died') + 0.4, 0.7, 'write', 'a_died');
at(W('s01.10', 'satellite') - 0.2, 0.15, 'draw', 'a_t2', { quiet: 1 }); at(W('s01.10', 'satellite') - 0.1, 0.5, 'write', 'a_1957'); at(W('s01.10', 'satellite') + 0.3, 0.8, 'write', 'a_sat');
at(W('s01.9', 'Einstein') + 1.0, 0.8, 'fade', 'a_cred');
// clock hands: steady until "wrong", then they slip apart
const WRONG = W('s01.9', 'wrong');
const hands = [0, 1, 2, 3].flatMap(i => [[`a_k${i}h`, 6, i], [`a_k${i}s`, 72, i]]);

// ---------- s02
cut('c_bolt', { t: W('s02.2', 'Thunderstorm') - 0.3, from: [-500, -120, -20], wig: [T('s02.3')], out: hold('s02') - 0.6, to: [-900, -200, -18] });
cut('c_kit1', { t: W('s02.6', 'Boom') + 0.15, from: [0, 500, 0], back: 1.2, wig: [W('s02.6', 'Boom') + 1.2], out: hold('s02') - 0.6, to: [0, 700, 0] });
at(W('s02.2', 'Thunderstorm') + 0.4, 0.25, 'tape', 'b_tape');
at(T('s02.3'), 0.35, 'pop', 'b_flash');
at(T('s02.3'), 0.6, 'fn', 'b_fl', { f: (n, u, t, on) => { n.style.opacity = on && u < 1 ? (0.55 * Math.exp(-6 * u)).toFixed(3) : 0; }, sound: 'flash' });
const cnt = LN['s02.5'].words;   // One Mississippi, two Mississippi, three...
at(cnt[0].t0, cnt[1].t1 - cnt[0].t0, 'write', 'b_c1'); at(cnt[2].t0, cnt[3].t1 - cnt[2].t0, 'write', 'b_c2'); at(cnt[4].t0, 0.5, 'write', 'b_c3');
[0, 2, 4].forEach(k => Chalk.event(cnt[k].t0, 'tick', { n: 1, g: 0.14, f: 2400 }));
at(W('s02.6', 'Boom'), 0.45, 'pop', 'b_boom'); Chalk.event(W('s02.6', 'Boom'), 'rumble', { d: 2.2 });
at(W('s02.7', 'five') - 0.1, 1.4, 'write', 'b_5s'); at(E('s02.7') - 0.2, 0.8, 'fade', 'b_lab');
at(W('s02.8', 'delay'), 1.3, 'write', 'b_late');
at(W('s02.6', 'Boom') + 1.4, 1.0, 'write', 'b_hid');
at(W('s02.2', 'Thunderstorm') + 0.8, 0.8, 'fade', 'b_cred');
HOOKS.push((t, active) => {
  if (!active.has('s01')) return;
  for (const [id, rate, i] of hands) {
    const n = $(id), slip = Math.max(0, t - WRONG) * (i - 1.5) * 40;   // after "wrong" each clock drifts its own way
    n.style.transformBox = 'view-box'; n.style.transformOrigin = `${n.dataset.cx}px ${n.dataset.cy}px`;
    n.style.transform = `rotate(${(rate * (t - 15) + i * 50 + (id.endsWith('s') ? slip * 3 : slip)).toFixed(2)}deg)`;
  }
});
```

## gps/parts/s03.html

Доски 3–5: разметка.

```html
<!-- s03 satellites shout the time -->
<div class="sc" id="s03">
 <svg class="draw" width="1920" height="1080" data-bleed="1"><g fill="none" stroke="#f4f1ea" stroke-width="8" stroke-linecap="round">
  <path id="c_earth" d="M-20 1006 A 4600 4600 0 0 1 1940 1006"/></g></svg>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <path id="c_bub" d="M640 200 C 640 120 700 96 940 96 C 1180 96 1260 110 1260 200 C 1260 290 1180 310 940 310 C 800 310 740 306 700 300 L 600 350 L 652 282 C 642 262 640 236 640 200 Z" stroke="#f4f1ea" stroke-width="5"/>
  <path id="c_sig" d="M600 440 L 1180 876" stroke="#9fd0ff" stroke-width="5" stroke-dasharray="14 12"/>
  <circle id="c_pkt" cx="600" cy="440" r="13" fill="#9fd0ff" stroke="none"/>
  <circle id="c_you" cx="1180" cy="891" r="15" fill="#9fd0ff" stroke="none"/>
 </g></svg>
 <div class="ck" id="c_same" style="left:1300px;top:120px;font-size:64px">same trick,</div>
 <div class="ck" id="c_light" style="left:1300px;top:196px;font-size:64px;color:#9fd0ff">with light</div>
 <div class="ck mono" id="c_time" style="left:690px;top:140px;font-size:44px;font-family:SpaceMono">12:00:00.000000000</div>
 <div class="ck" id="c_here" style="left:690px;top:214px;font-size:56px">…and I'm right here</div>
 <div class="ck" id="c_lt" style="left:250px;top:640px;font-size:56px">&lt; 0.1 s</div>
 <div class="ck mono" id="c_cnt" style="left:250px;top:720px;font-size:40px;font-family:SpaceMono;color:#9fd0ff">0.000 s</div>
 <div class="ck" id="c_youl" style="left:1212px;top:812px;font-size:56px;color:#9fd0ff">you</div>
 <div class="ck" id="c_how" style="left:1300px;top:700px;font-size:56px">how late?</div>
 <div class="ck" id="c_eq" style="left:1000px;top:430px;font-size:88px;font-weight:600;color:#ffb36b">delay = distance</div>
 <div class="lab" id="c_lab" style="left:1004px;top:556px;font-size:17px">0.067 S × 299 792 KM/S = 20 200 KM (SATELLITE OVERHEAD, COMPUTED)</div>
 <div class="cw" id="c_sat1" style="left:150px;top:110px;width:420px;height:333px">
  <img src="../assets/p/gps_iif_rough.png" style="transform:rotate(-4deg)">
  <div class="tape" id="c_tape" style="left:150px;top:-22px;transform:rotate(3deg)"></div>
 </div>
 <div class="lab" id="c_cred" style="left:150px;top:1032px;font-size:14px">ILLUSTRATION: NASA · PUBLIC DOMAIN</div>
</div>

<!-- s03b three balls cross in two spots -->
<div class="sc" id="s03b">
 <svg class="draw" width="1920" height="1080" data-bleed="1"><g fill="none" stroke="#f4f1ea" stroke-width="8" stroke-linecap="round">
  <path id="d_earth" d="M-20 1060 A 2400 2400 0 0 1 1540 1060"/></g></svg>
 <svg class="draw" width="1920" height="1080" id="d_g"></svg>
 <div class="ck" id="d_ball" style="left:1440px;top:230px;font-size:52px">one satellite:</div>
 <div class="ck" id="d_ball2" style="left:1440px;top:290px;font-size:52px">you're on a ball</div>
 <div class="ck" id="d_space" style="left:1440px;top:96px;font-size:52px;color:#ff8f7a">way out in space: nope</div>
 <div class="ck" id="d_you" style="left:1440px;top:896px;font-size:64px;color:#9fd0ff">you</div>
 <div class="ck" id="d_4th" style="left:1440px;top:410px;font-size:52px">a 4th one fixes</div>
 <div class="ck" id="d_4th2" style="left:1440px;top:470px;font-size:52px">your phone's clock:</div>
 <div class="ck" id="d_cheap" style="left:1560px;top:556px;font-size:84px;font-weight:700;color:#ffb36b;transform:rotate(-5deg)">cheap.</div>
 <div class="cw" id="c_cat2" style="left:1630px;top:690px;width:250px;height:275px">
  <img src="../assets/p/cat_sideeye_rough.png" style="transform:rotate(-4deg)">
 </div>
</div>

<!-- s04 the catch: light is fast -->
<div class="sc" id="s04">
 <div class="ck" id="e_catch" style="left:120px;top:70px;font-size:90px;font-weight:600">the catch: light is fast</div>
 <div class="ck" id="e_ns" style="left:120px;top:220px;font-size:96px">1 ns → 1 ft</div>
 <div class="ck" id="e_30" style="left:620px;top:246px;font-size:56px;opacity:.8">(30 cm)</div>
 <div class="ck" id="e_us" style="left:120px;top:430px;font-size:96px;color:#ff8f7a">1 µs → 984 ft</div>
 <div class="ck" id="e_300" style="left:700px;top:456px;font-size:56px;opacity:.8;color:#ff8f7a">(300 m)</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <path id="e_rul" d="M124 370 H 424" stroke="#f4f1ea" stroke-width="6"/>
  <path id="e_rt" d="M124 356 V 384 M199 362 V 378 M274 358 V 382 M349 362 V 378 M424 356 V 384" stroke="#f4f1ea" stroke-width="4"/>
  <line id="e_err" x1="124" y1="600" x2="1240" y2="600" stroke="#ff8f7a" stroke-width="8"/>
  <path id="e_errh" d="M1214 584 L 1244 600 L 1214 616" stroke="#ff8f7a" stroke-width="7"/>
  <path id="e_x" data-allow="e_eq" d="M980 790 C 1180 780 1420 800 1660 784" stroke="#ff8f7a" stroke-width="7"/>
 </g></svg>
 <div class="ck" id="e_one" style="left:440px;top:350px;font-size:40px;opacity:.8">one foot</div>
 <div class="ck" id="e_yerr" style="left:1270px;top:578px;font-size:48px;color:#ff8f7a">your error</div>
 <div class="ck" id="e_plan" style="left:120px;top:690px;font-size:64px">simple plan:</div>
 <div class="ck" id="e_p1" style="left:160px;top:780px;font-size:50px">1. perfect clocks in the sky</div>
 <div class="ck" id="e_p2" style="left:160px;top:850px;font-size:50px">2. sync with the ground</div>
 <div class="ck" id="e_p3" style="left:160px;top:920px;font-size:50px">3. done</div>
 <div class="ck" id="e_eq" style="left:980px;top:740px;font-size:60px">1 s up there = 1 s down here</div>
 <div class="ck" id="e_right" style="left:1720px;top:740px;font-size:60px">right?</div>
 <div class="ck" id="e_wrong" style="left:980px;top:840px;font-size:150px;font-weight:700;color:#ff8f7a;transform:rotate(-4deg)">WRONG.</div>
 <div class="ck" id="e_x2" style="left:1520px;top:860px;font-size:120px;font-weight:700;color:#ff8f7a;transform:rotate(-4deg)">×2</div>
 <div class="cw" id="c_nist" style="left:1440px;top:110px;width:320px;height:449px">
  <img src="../assets/p/nist_f1_rough.png" style="transform:rotate(3deg)">
  <div class="tape" id="e_tape" style="left:90px;top:-22px;transform:rotate(-4deg)"></div>
 </div>
 <div class="ck" id="e_atom" style="left:1100px;top:250px;font-size:52px">atomic clock →</div>
 <div class="ck" id="e_few" style="left:1000px;top:330px;font-size:40px;opacity:.9">a few ns off per day</div>
 <div class="lab" id="e_cred" style="left:1180px;top:1032px;font-size:14px">PHOTO: NIST-F1 GROUND CLOCK, NIST · PUBLIC DOMAIN</div>
</div>
```

## gps/parts/s03.js

Доски 3–5: таймлайн.

```js
// ---------- s03
cut('c_sat1', { t: T('s03.1') + 0.1, from: [-500, -200, -25], wig: [W('s03.2', 'shouting')], out: hold('s03') - 0.6, to: [-900, -260, -18] });
at(T('s03.1') + 0.5, 0.25, 'tape', 'c_tape');
at(W('s03.1', 'same'), 0.8, 'write', 'c_same'); at(W('s03.1', 'light'), 0.8, 'write', 'c_light');
at(W('s03.1', 'sound') - 0.2, 1.2, 'draw', 'c_earth', { quiet: 1 });
at(W('s03.2', 'shouting') - 0.2, 0.9, 'draw', 'c_bub');
at(W('s03.2', 'time'), 1.0, 'write', 'c_time');
at(W('s03.2', 'time'), 0.1, 'fn', 'c_time', { f: (n, u, t, on) => { const ns = Math.max(0, t - W('s03.2', 'time')) * 1e9; const s = Math.floor(ns / 1e9); n.textContent = `12:00:${String(s).padStart(2, '0')}.${String(Math.floor(ns % 1e9)).padStart(9, '0')}`; } });
at(W('s03.2', 'where'), 1.0, 'write', 'c_here');
at(T('s03.3') - 0.2, 0.35, 'pop', 'c_you'); at(T('s03.3'), 0.5, 'write', 'c_youl');
const SIG0 = W('s03.3', 'takes'), SIG1 = E('s03.3') - 0.2;
at(SIG0, SIG1 - SIG0, 'draw', 'c_sig', { quiet: 1 });
at(SIG0, SIG1 - SIG0, 'fn', 'c_pkt', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.setAttribute('cx', 600 + 580 * u); n.setAttribute('cy', 440 + 436 * u); }, sound: 'whoosh', soundArgs: { d: 1.2, f0: 2600, f1: 500, g: 0.1 } });
at(SIG0, SIG1 - SIG0, 'fn', 'c_cnt', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.textContent = (0.0673 * u).toFixed(3) + ' s'; }, sound: 'counter', soundArgs: { d: 2.4 } });
at(W('s03.3', 'less'), 0.8, 'write', 'c_lt');
at(W('s03.4', 'late') - 0.3, 0.8, 'write', 'c_how');
at(T('s03.5'), 1.3, 'write', 'c_eq'); at(E('s03.5') - 0.3, 0.6, 'fade', 'c_lab');
at(T('s03.1') + 1.0, 0.8, 'fade', 'c_cred');

// ---------- s03b: three spheres through the same two points P (you) and Q (out in space)
{
  const g = $('d_g'), S = { fill: 'none', 'stroke-linecap': 'round' };
  const sat = (id, x, y) => { el(g, 'rect', { ...S, id: id + 'b', x: x - 13, y: y - 9, width: 26, height: 18, stroke: '#f4f1ea', 'stroke-width': 4 }); el(g, 'path', { ...S, id: id + 'p', d: `M${x - 15} ${y} H ${x - 44} M${x + 15} ${y} H ${x + 44} M${x - 44} ${y - 8} V ${y + 8} M${x + 44} ${y - 8} V ${y + 8}`, stroke: '#f4f1ea', 'stroke-width': 4 }); };
  [560, 760, 960].forEach((x, i) => { sat(`d_s${i}`, x, 530); el(g, 'circle', { ...S, id: `d_c${i}`, cx: x, cy: 530, r: Math.hypot(x - 760, 400), stroke: ['#f4f1ea', '#9fd0ff', '#f4f1ea'][i], 'stroke-width': 4, opacity: .85 }); });
  sat('d_s3', 1330, 430);
  el(g, 'circle', { id: 'd_q', cx: 760, cy: 130, r: 11, fill: '#ff8f7a' });
  el(g, 'path', { ...S, id: 'd_ql', d: 'M1430 124 L 782 130', stroke: '#ff8f7a', 'stroke-width': 3, 'stroke-dasharray': '10 10' });
  el(g, 'circle', { id: 'd_p', cx: 760, cy: 930, r: 14, fill: '#9fd0ff' });
  el(g, 'path', { ...S, id: 'd_pl', d: 'M1430 930 L 786 930', stroke: '#9fd0ff', 'stroke-width': 3, 'stroke-dasharray': '10 10' });
  el(g, 'circle', { ...S, id: 'd_ck', cx: 1490, cy: 600, r: 34, stroke: '#f4f1ea', 'stroke-width': 4 });
  el(g, 'path', { ...S, id: 'd_ckh', d: 'M1490 600 V 576 M1490 600 L 1506 610', stroke: '#f4f1ea', 'stroke-width': 4 });
}
cut('c_cat2', { t: W('s03b.5', 'cheap') + 0.1, from: [500, 300, 20], wig: [W('s03b.5', 'cheap') + 1.4], out: hold('s03b') - 0.6, to: [700, 600, 18] });
at(T('s03b.1') - 0.3, 1.0, 'draw', 'd_earth', { quiet: 1 });
at(T('s03b.1'), 0.3, 'draw', 'd_s1b'); at(T('s03b.1') + 0.25, 0.3, 'draw', 'd_s1p', { quiet: 1 });
at(T('s03b.1') + 0.2, 0.9, 'write', 'd_ball'); at(W('s03b.1', 'somewhere'), 0.9, 'write', 'd_ball2');
at(W('s03b.1', 'ball') - 0.3, 1.3, 'draw', 'd_c1', { note: 0 });
at(W('s03b.2', 'three') - 0.2, 0.3, 'draw', 'd_s0b', { quiet: 1 }); at(W('s03b.2', 'three'), 0.3, 'draw', 'd_s0p', { quiet: 1 });
at(W('s03b.2', 'three'), 0.3, 'draw', 'd_s2b', { quiet: 1 }); at(W('s03b.2', 'three') + 0.2, 0.3, 'draw', 'd_s2p', { quiet: 1 });
at(W('s03b.2', 'balls'), 1.1, 'draw', 'd_c0', { note: 2 }); at(W('s03b.2', 'balls') + 0.5, 1.1, 'draw', 'd_c2', { note: 4 });
at(T('s03b.3'), 0.35, 'pop', 'd_q'); at(T('s03b.3') + 0.2, 0.6, 'draw', 'd_ql', { quiet: 1 }); at(W('s03b.3', 'space') - 0.3, 0.9, 'write', 'd_space');
at(T('s03b.4'), 0.35, 'pop', 'd_p'); at(T('s03b.4') + 0.2, 0.6, 'draw', 'd_pl', { quiet: 1 }); at(W('s03b.4', 'you') - 0.2, 0.5, 'write', 'd_you');
at(T('s03b.5'), 0.3, 'draw', 'd_s3b'); at(T('s03b.5') + 0.25, 0.3, 'draw', 'd_s3p', { quiet: 1 });
at(T('s03b.5') + 0.3, 0.9, 'write', 'd_4th'); at(W('s03b.5', 'phone'), 0.9, 'write', 'd_4th2');
at(W('s03b.5', 'clock') - 0.1, 0.5, 'draw', 'd_ck', { quiet: 1 }); at(W('s03b.5', 'clock') + 0.3, 0.25, 'draw', 'd_ckh', { quiet: 1 });
at(W('s03b.5', 'cheap'), 0.4, 'pop', 'd_cheap');

// ---------- s04
cut('c_nist', { t: W('s04.5', 'atomic') - 0.2, from: [600, -100, 20], wig: [W('s04.5', 'day')], out: hold('s04') - 0.6, to: [800, -300, 18] });
at(W('s04.5', 'atomic') + 0.4, 0.25, 'tape', 'e_tape'); at(W('s04.5', 'clocks'), 0.9, 'write', 'e_atom'); at(W('s04.5', 'billionths') - 0.2, 1.2, 'write', 'e_few'); at(W('s04.5', 'atomic') + 1.0, 0.8, 'fade', 'e_cred');
at(T('s04.1'), 1.8, 'write', 'e_catch');
at(W('s04.3', 'billionth'), 0.8, 'write', 'e_ns'); at(W('s04.3', 'foot') - 0.3, 0.5, 'draw', 'e_rul'); at(W('s04.3', 'foot'), 0.3, 'draw', 'e_rt', { quiet: 1 });
at(W('s04.3', 'foot') + 0.2, 0.5, 'write', 'e_one'); at(E('s04.3') - 0.3, 0.6, 'write', 'e_30');
at(W('s04.4', 'millionth'), 0.9, 'write', 'e_us'); at(W('s04.4', 'distance'), 2.0, 'grow', 'e_err'); at(W('s04.4', 'distance') + 1.9, 0.2, 'draw', 'e_errh', { quiet: 1 });
at(W('s04.4', 'thousand'), 0.6, 'write', 'e_300'); at(W('s04.4', 'thousand') + 0.3, 0.7, 'write', 'e_yerr');
at(W('s04.6', 'plan') - 0.3, 0.8, 'write', 'e_plan');
at(W('s04.6', 'perfect'), 0.9, 'write', 'e_p1'); at(W('s04.6', 'sync'), 0.9, 'write', 'e_p2'); at(W('s04.6', 'done'), 0.4, 'write', 'e_p3');
at(T('s04.7'), 1.6, 'write', 'e_eq'); at(T('s04.8'), 0.4, 'write', 'e_right');
at(T('s04.9') - 0.1, 0.3, 'draw', 'e_x'); at(T('s04.9'), 0.4, 'pop', 'e_wrong'); at(T('s04.10'), 0.35, 'pop', 'e_x2');
```

## gps/parts/s05.html

Доски 6–10: разметка.

```html
<!-- s05 wrong #1: speed -->
<div class="sc" id="s05">
 <div class="ck" id="f_head" style="left:120px;top:70px;font-size:100px;font-weight:600;color:#ff8f7a">wrong #1: speed</div>
 <div class="cw" id="c_nav" style="left:110px;top:250px;width:560px;height:390px">
  <img src="../assets/p/gps_navstar_rough.png" style="transform:rotate(-3deg)">
  <div class="tape" id="f_tape" style="left:200px;top:-22px;transform:rotate(4deg)"></div>
 </div>
 <div class="ck" id="f_mph" style="left:120px;top:700px;font-size:96px">≈ 8 700 mph</div>
 <div class="ck" id="f_kmh" style="left:130px;top:812px;font-size:52px;opacity:.85">(≈ 14 000 km/h)</div>
 <div class="ck" id="f_laps" style="left:560px;top:890px;font-size:64px;color:#9fd0ff">2 laps a day</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <circle id="f_earth" cx="1340" cy="580" r="110" stroke="#f4f1ea" stroke-width="7"/>
  <circle id="f_orbit" cx="1340" cy="580" r="459" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="14 12"/>
  <circle id="f_sat" cx="1340" cy="121" r="13" fill="#f4f1ea" stroke="none"/>
 </g></svg>
 <div class="ck" id="f_e" style="left:1300px;top:560px;font-size:40px;opacity:.85">Earth</div>
 <div class="lab" id="f_scale" style="left:1560px;top:60px">TO SCALE</div>
 <div class="lab" id="f_cred" style="left:110px;top:1032px;font-size:14px">ILLUSTRATION: U.S. AIR FORCE · PUBLIC DOMAIN</div>
</div>

<!-- s05b the light clock -->
<div class="sc" id="s05b">
 <div class="ck" id="g_head" style="left:120px;top:70px;font-size:80px;font-weight:600">the simplest clock:</div>
 <div data-box="1" style="position:absolute;left:540px;top:212px;width:1380px;height:236px"></div>
 <div data-box="1" style="position:absolute;left:100px;top:446px;width:1800px;height:60px"></div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-linecap="round">
  <path id="g_m1" d="M200 230 H 330" stroke-width="8"/><path id="g_m2" d="M200 430 H 330" stroke-width="8"/>
  <circle id="g_dot" cx="265" cy="424" r="11" fill="#ffe48a" stroke="none"/>
 </g></svg>
 <svg class="draw" width="1920" height="1080" data-bleed="1"><g fill="none" stroke-linecap="round">
  <path id="g_trail" stroke="#ffe48a" stroke-width="4" opacity=".75"/>
  <g id="g_mov"><path id="g_n1" d="M575 230 H 705" stroke="#f4f1ea" stroke-width="8"/><path id="g_n2" d="M575 430 H 705" stroke="#f4f1ea" stroke-width="8"/>
   <circle id="g_ndot" cx="640" cy="424" r="11" fill="#ffe48a" stroke="none"/></g>
 </g></svg>
 <div class="ck" id="g_tick" style="left:350px;top:262px;font-size:56px">tick</div>
 <div class="ck" id="g_tock" style="left:350px;top:330px;font-size:56px">tock</div>
 <div class="ck" id="g_sat" style="left:790px;top:150px;font-size:48px">on a satellite →</div>
 <div class="ck mono" id="g_cs" style="left:120px;top:458px;font-size:34px;font-family:SpaceMono">standing: 0 ticks</div>
 <div class="ck mono" id="g_cm" style="left:1330px;top:458px;font-size:34px;font-family:SpaceMono;color:#ffe48a">moving: 0 ticks</div>
 <div class="ck" id="g_same" style="left:700px;top:520px;font-size:60px;color:#9fd0ff">light's speed: the same for everyone</div>
 <div class="ck" id="g_path" style="left:700px;top:600px;font-size:72px">same speed, longer path</div>
 <div class="ck" id="g_long" style="left:700px;top:690px;font-size:60px">so every tick takes longer</div>
 <div class="ck" id="g_slow" style="left:700px;top:770px;font-size:72px;color:#ffb36b">the moving clock runs slow</div>
 <div class="ck" id="g_nb" style="left:700px;top:860px;font-size:52px;opacity:.9">not broken. that's just time.</div>
 <div class="ck" id="g_7" style="left:1262px;top:914px;font-size:88px;font-weight:700;color:#ff8f7a">−7 µs a day</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round"><path id="g_box" d="M1228 898 C 1440 892 1660 896 1846 900 L 1850 1014 C 1640 1020 1420 1016 1224 1012 Z" stroke="#ff8f7a" stroke-width="5"/></g></svg>
 <div class="cw" id="c_cat3" style="left:100px;top:640px;width:230px;height:297px">
  <img src="../assets/p/cat_black_rough.png" style="transform:rotate(-3deg)">
 </div>
 <div class="ck" id="g_chase" style="left:350px;top:860px;font-size:48px">← would chase it</div>
 <div class="lab" id="g_tilt" style="left:120px;top:1024px;font-size:15px">TILT EXAGGERATED: REAL TILT 0.00074°</div>
</div>

<!-- s06 wrong #2: height -->
<div class="sc" id="s06">
 <div class="ck" id="h_head" style="left:120px;top:70px;font-size:100px;font-weight:600;color:#ff8f7a">wrong #2: height</div>
 <div class="ck" id="h_grav" style="left:120px;top:200px;font-size:72px">gravity slows time</div>
 <svg class="draw" width="1920" height="1080" data-bleed="1"><g fill="none" stroke="#f4f1ea" stroke-linecap="round">
  <path id="h_ground" d="M-20 960 C 400 950 800 966 1200 954 S 1700 958 1940 952" stroke-width="8"/></g></svg>
 <svg class="draw" width="1920" height="1080" id="h_g"></svg>
 <div class="ck" id="h_slow" style="left:420px;top:818px;font-size:52px">slower</div>
 <div class="ck" id="h_fast" style="left:420px;top:378px;font-size:52px;color:#ffb36b">faster</div>
 <div class="ck" id="h_up" style="left:440px;top:590px;font-size:52px">go higher ↑</div>
 <div class="ck" id="h_faith" style="left:900px;top:220px;font-size:56px;opacity:.9">don't take it on faith:</div>
 <div class="ck" id="h_nist" style="left:900px;top:300px;font-size:72px">NIST, Colorado, 2010</div>
 <div class="ck" id="h_33" style="left:1512px;top:832px;font-size:60px">33 cm</div>
 <div class="ck" id="h_ran" style="left:1290px;top:590px;font-size:64px;color:#ffb36b">ran faster</div>
 <div class="lab" id="h_ex" style="left:120px;top:1000px;font-size:15px">CLOCK RATES EXAGGERATED</div>
</div>

<!-- s06b head and feet -->
<div class="sc" id="s06b">
 <svg class="draw" width="1920" height="1080" id="i_g"></svg>
 <div class="ck" id="i_head" style="left:620px;top:110px;font-size:80px;font-weight:600">your head ages faster</div>
 <div class="ck" id="i_feet" style="left:620px;top:210px;font-size:64px;opacity:.9">than your feet</div>
 <div class="ck" id="i_80" style="left:620px;top:360px;font-size:64px">80 years standing:</div>
 <div class="ck" id="i_44" style="left:620px;top:440px;font-size:150px;font-weight:700;color:#ffb36b">+0.44 µs</div>
 <div class="ck" id="i_old" style="left:1190px;top:520px;font-size:56px">older head</div>
 <div class="lab" id="i_calc" style="left:626px;top:620px;font-size:17px">1.6 M × 9.8 M/S² ÷ C² × 80 YEARS (COMPUTED)</div>
 <div class="cw" id="c_cat4" style="left:1180px;top:730px;width:560px;height:259px">
  <img src="../assets/p/cat_flat_rough.png" style="transform:rotate(-2deg)">
 </div>
 <div class="ck" id="i_even" style="left:760px;top:840px;font-size:60px">ages evenly →</div>
</div>

<!-- s07 the satellite is high -->
<div class="sc" id="s07">
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <circle id="j_earth" cx="700" cy="560" r="110" stroke="#f4f1ea" stroke-width="7"/>
  <circle id="j_orbit" cx="700" cy="560" r="459" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="14 12"/>
  <path id="j_alt" d="M700 450 V 112" stroke="#f4f1ea" stroke-width="4"/>
  <path id="j_ah" d="M686 132 L 700 108 L 714 132" stroke="#f4f1ea" stroke-width="4"/>
  <circle id="j_you" cx="700" cy="450" r="9" fill="#9fd0ff" stroke="none"/>
  <circle id="j_sat" cx="700" cy="101" r="14" fill="#f4f1ea" stroke="none"/>
 </g></svg>
 <div class="ck" id="j_foot" style="left:120px;top:70px;font-size:64px">not a foot up:</div>
 <div class="ck" id="j_km" style="left:1250px;top:220px;font-size:96px">20 200 km up</div>
 <div class="ck" id="j_mi" style="left:1260px;top:330px;font-size:56px;opacity:.85">(over 12 500 mi)</div>
 <div class="ck" id="j_weak" style="left:1250px;top:450px;font-size:60px">Earth's pull: much weaker</div>
 <div class="ck" id="j_45" style="left:1250px;top:580px;font-size:120px;font-weight:700;color:#ffb36b">+45 µs a day</div>
 <div class="ck" id="j_ahead" style="left:1260px;top:720px;font-size:56px">clocks run ahead</div>
 <div class="lab" id="j_scale" style="left:1250px;top:1000px;font-size:15px">EARTH AND ORBIT TO SCALE</div>
</div>
```

## gps/parts/s05.js

Доски 6–10: таймлайн.

```js
// ---------- s05
cut('c_nav', { t: T('s05.2') - 0.2, from: [-600, -100, -20], wig: [W('s05.3', 'Twice')], out: hold('s05') - 0.6, to: [-900, -260, -18] });
at(T('s05.2') + 0.3, 0.25, 'tape', 'f_tape'); at(T('s05.2') + 0.8, 0.8, 'fade', 'f_cred');
at(T('s05.1'), 1.4, 'write', 'f_head');
at(W('s05.2', 'eight'), 1.3, 'write', 'f_mph'); at(W('s05.2', 'miles'), 0.9, 'write', 'f_kmh');
at(W('s05.2', 'Earth') - 0.2, 0.7, 'draw', 'f_earth'); at(W('s05.2', 'Earth') + 0.3, 0.5, 'write', 'f_e');
at(W('s05.2', 'race') - 0.2, 1.2, 'draw', 'f_orbit', { quiet: 1 }); at(W('s05.2', 'race') + 0.6, 0.6, 'fade', 'f_scale');
const LAP0 = T('s05.3'), LAP1 = E('s05.3');
at(W('s05.2', 'race') + 0.8, 0.3, 'pop', 'f_sat');
at(LAP0, LAP1 - LAP0, 'fn', 'f_sat', { f: (n, u, t, on) => { const a = -Math.PI / 2 + 4 * Math.PI * u; n.setAttribute('cx', 1340 + 459 * Math.cos(a)); n.setAttribute('cy', 580 + 459 * Math.sin(a)); }, sound: 'whoosh', soundArgs: { d: 2.4, f0: 600, f1: 2400, g: 0.08 } });
at(W('s05.3', 'Twice'), 0.9, 'write', 'f_laps');

// ---------- s05b light clock: drawn light speed C px/s, mirror gap 200 px, satellite speed 0.6 C (real: 1.3e-5 C)
const LC = { C: 800 / 3, gap: 200, v: 0.6 };
const legS = LC.gap / LC.C, legM = legS / Math.sqrt(1 - LC.v * LC.v);           // 0.75 s and 0.9375 s per leg
const dxLeg = LC.v * LC.C * legM;                                                   // 150 px sideways per leg
const STAND0 = W('s05b.2', 'flash'), PASS0 = W('s05b.6', 'light'), NLEG = 7, PASS1 = PASS0 + NLEG * legM;
const bounce = (t, leg) => { const k = Math.floor(t / leg), f = t / leg - k; return k % 2 === 0 ? f : 1 - f; };   // 0 at the bottom mirror
{ let d = 'M640 424'; for (let k = 1; k <= NLEG; k++) d += ` L ${640 + dxLeg * k} ${k % 2 ? 236 : 424}`; $('g_trail').setAttribute('d', d); }
cut('c_cat3', { t: W('s05b.2', 'bouncing'), from: [-500, 300, -20], wig: [T('s05b.4')], out: hold('s05b') - 0.6, to: [-700, 600, -18] });
at(T('s05b.1'), 1.4, 'write', 'g_head');
at(W('s05b.2', 'mirrors') - 0.2, 0.35, 'draw', 'g_m1'); at(W('s05b.2', 'mirrors') + 0.1, 0.35, 'draw', 'g_m2', { quiet: 1 });
at(STAND0, 0.3, 'pop', 'g_dot');
at(STAND0, 0.1, 'fn', 'g_dot', { f: (n, u, t, on) => { if (on) n.setAttribute('cy', 424 - 188 * bounce(t - STAND0, legS)); } });
at(W('s05b.2', 'bouncing') + 1.0, 1.0, 'write', 'g_chase');
at(W('s05b.3', 'tick'), 0.5, 'write', 'g_tick'); at(W('s05b.4', 'tock'), 0.5, 'write', 'g_tock');
for (let k = 1; STAND0 + 2 * k * legS < hold('s05b'); k++) Chalk.event(STAND0 + 2 * k * legS, 'tick', { n: 1, g: 0.08, f: 2600, pan: -0.4 });
at(T('s05b.5'), 0.35, 'draw', 'g_n1'); at(T('s05b.5') + 0.2, 0.35, 'draw', 'g_n2', { quiet: 1 }); at(T('s05b.5') + 0.4, 0.3, 'pop', 'g_ndot');
at(W('s05b.5', 'satellite') - 0.3, 0.9, 'write', 'g_sat');
// the moving clock: parked until the pass, then crosses the board at 0.6 C and drives off the right edge
const movX = t => t < PASS0 ? 0 : t < PASS1 ? dxLeg / legM * (t - PASS0) : dxLeg * NLEG + 900 * Math.pow(t - PASS1, 2);
at(T('s05b.5'), 0.1, 'fn', 'g_mov', { f: (n, u, t, on) => { n.setAttribute('transform', `translate(${movX(t).toFixed(2)},0)`); } });
at(T('s05b.5') + 0.4, 0.1, 'fn', 'g_ndot', { f: (n, u, t, on) => { if (on) n.setAttribute('cy', 424 - 188 * (t < PASS0 ? 0 : t < PASS1 ? bounce(t - PASS0, legM) : bounce(PASS1 - PASS0, legM))); } });
at(PASS0, PASS1 - PASS0, 'draw', 'g_trail', { quiet: 1 });
Chalk.event(PASS1, 'whoosh', { d: 0.6, f0: 400, f1: 2400, g: 0.12, pan: 0.6 });
for (let k = 1; 2 * k * legM <= PASS1 - PASS0 + 1e-6; k++) Chalk.event(PASS0 + 2 * k * legM, 'tick', { n: 1, g: 0.09, f: 1900, pan: 0.4 });
// tick counters over the same window
at(PASS0, PASS1 - PASS0, 'fn', 'g_cs', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.textContent = `standing: ${Math.floor((Math.min(t, PASS1) - PASS0) / (2 * legS) + 1e-6)} ticks`; } });
at(PASS0, PASS1 - PASS0, 'fn', 'g_cm', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.textContent = `moving: ${Math.floor((Math.min(t, PASS1) - PASS0) / (2 * legM) + 1e-6)} ticks`; } });
at(W('s05b.8', 'speed') - 0.2, 1.6, 'write', 'g_same');
at(T('s05b.9'), 1.4, 'write', 'g_path'); at(T('s05b.10'), 1.4, 'write', 'g_long');
at(T('s05b.11'), 1.5, 'write', 'g_slow'); at(T('s05b.12'), 1.6, 'write', 'g_nb');
at(W('s05b.14', 'seven'), 1.2, 'write', 'g_7'); at(W('s05b.14', 'lost'), 0.9, 'draw', 'g_box');
at(E('s05b.7'), 0.8, 'fade', 'g_tilt');

// ---------- s06 gravity
{
  const g = $('h_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round' };
  const clock = (id, x, y, r) => { el(g, 'circle', { ...S, id, cx: x, cy: y, r, 'stroke-width': 6 }); el(g, 'line', { ...S, id: id + 'h', x1: x, y1: y, x2: x, y2: y - r * 0.72, 'stroke-width': 5, 'data-cx': x, 'data-cy': y }); };
  clock('h_c0', 300, 860, 52); clock('h_c1', 300, 640, 52); clock('h_c2', 300, 420, 52);
  el(g, 'path', { ...S, id: 'h_tab', d: 'M960 900 H 1560', 'stroke-width': 6 });
  el(g, 'rect', { ...S, id: 'h_bxA', x: 1000, y: 760, width: 160, height: 140, 'stroke-width': 5 });
  el(g, 'rect', { ...S, id: 'h_blk', x: 1300, y: 830, width: 160, height: 70, 'stroke-width': 5 });
  el(g, 'rect', { ...S, id: 'h_bxB', x: 1300, y: 690, width: 160, height: 140, 'stroke-width': 5 });
  clock('h_cA', 1080, 830, 40); clock('h_cB', 1380, 760, 40);
  el(g, 'path', { ...S, id: 'h_ar', d: 'M1490 830 V 900 M1480 844 L 1490 828 L 1500 844 M1480 886 L 1490 902 L 1500 886', 'stroke-width': 4 });
}
at(T('s06.1'), 1.6, 'write', 'h_head'); at(T('s06.2'), 1.2, 'write', 'h_grav');
at(W('s06.3', 'Earth') - 0.3, 1.0, 'draw', 'h_ground', { quiet: 1 });
['h_c0', 'h_c1', 'h_c2'].forEach((id, i) => { at(W('s06.3', 'closer') + i * 0.5, 0.4, 'draw', id, { note: i }); at(W('s06.3', 'closer') + i * 0.5 + 0.3, 0.2, 'draw', id + 'h', { quiet: 1 }); });
at(W('s06.3', 'slower'), 0.7, 'write', 'h_slow');
at(W('s06.4', 'higher') - 0.2, 0.8, 'write', 'h_up'); at(W('s06.4', 'speeds'), 0.7, 'write', 'h_fast');
at(T('s06.5'), 1.2, 'write', 'h_faith');
at(W('s06.6', '2010'), 1.4, 'write', 'h_nist');
at(W('s06.6', 'raised') - 0.4, 0.5, 'draw', 'h_tab', { quiet: 1 }); at(W('s06.6', 'raised') - 0.2, 0.4, 'draw', 'h_bxA'); at(W('s06.6', 'raised'), 0.3, 'draw', 'h_cA', { quiet: 1 }); at(W('s06.6', 'raised') + 0.2, 0.2, 'draw', 'h_cAh', { quiet: 1 });
at(W('s06.6', 'clock'), 0.4, 'draw', 'h_bxB'); at(W('s06.6', 'clock') + 0.2, 0.3, 'draw', 'h_cB', { quiet: 1 }); at(W('s06.6', 'clock') + 0.4, 0.2, 'draw', 'h_cBh', { quiet: 1 });
at(W('s06.6', 'foot') - 0.2, 0.4, 'draw', 'h_blk'); at(W('s06.6', 'foot'), 0.4, 'draw', 'h_ar', { quiet: 1 }); at(W('s06.6', 'foot') + 0.2, 0.6, 'write', 'h_33');
at(W('s06.7', 'faster') - 0.2, 0.8, 'write', 'h_ran');
at(W('s06.3', 'slower') + 0.6, 0.8, 'fade', 'h_ex');
const GRAV = [['h_c0h', 40], ['h_c1h', 70], ['h_c2h', 100], ['h_cAh', 60], ['h_cBh', 90]];   // deg per second, exaggerated

// ---------- s06b head and feet
{
  const g = $('i_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
  el(g, 'path', { ...S, id: 'i_gr', d: 'M80 960 C 300 954 520 964 700 958', 'stroke-width': 6 });
  el(g, 'circle', { ...S, id: 'i_hd', cx: 320, cy: 290, r: 52, 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 'i_bd', d: 'M320 342 C 316 450 324 560 320 650', 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 'i_lg', d: 'M320 650 L 270 950 M320 650 L 372 950', 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 'i_ar', d: 'M318 400 L 236 560 M322 400 L 404 560', 'stroke-width': 6 });
  for (const [id, x, y] of [['i_k1', 470, 270], ['i_k2', 470, 900]]) {
    el(g, 'circle', { ...S, id, cx: x, cy: y, r: 34, 'stroke-width': 4 });
    el(g, 'line', { ...S, id: id + 'h', x1: x, y1: y, x2: x, y2: y - 24, 'stroke-width': 4, 'data-cx': x, 'data-cy': y });
  }
}
cut('c_cat4', { t: W('s06b.3', 'cat'), from: [600, 200, 15], wig: [W('s06b.4', 'know')], out: hold('s06b') - 0.6, to: [900, 300, 18] });
at(T('s06b.1') - 0.4, 0.4, 'draw', 'i_gr', { quiet: 1 }); at(T('s06b.1') - 0.2, 0.4, 'draw', 'i_hd'); at(T('s06b.1') + 0.1, 0.3, 'draw', 'i_bd', { quiet: 1 });
at(T('s06b.1') + 0.3, 0.3, 'draw', 'i_lg', { quiet: 1 }); at(T('s06b.1') + 0.5, 0.3, 'draw', 'i_ar', { quiet: 1 });
at(W('s06b.1', 'head') - 0.2, 0.4, 'draw', 'i_k1', { note: 1 }); at(W('s06b.1', 'head'), 0.2, 'draw', 'i_k1h', { quiet: 1 });
at(W('s06b.1', 'feet') - 0.2, 0.4, 'draw', 'i_k2', { note: 3 }); at(W('s06b.1', 'feet'), 0.2, 'draw', 'i_k2h', { quiet: 1 });
at(W('s06b.1', 'aging'), 1.4, 'write', 'i_head'); at(W('s06b.1', 'feet') - 0.1, 0.8, 'write', 'i_feet');
at(W('s06b.2', 'eighty') - 0.2, 1.2, 'write', 'i_80');
at(W('s06b.2', 'half') - 0.3, 1.2, 'write', 'i_44'); at(W('s06b.2', 'older') - 0.1, 0.8, 'write', 'i_old'); at(E('s06b.2') - 0.4, 0.8, 'fade', 'i_calc');
at(W('s06b.3', 'flat'), 0.9, 'write', 'i_even');
GRAV.push(['i_k1h', 95], ['i_k2h', 60]);

// ---------- s07 the satellite is high
at(T('s07.1') - 0.2, 0.6, 'draw', 'j_earth'); at(T('s07.1') + 0.2, 0.3, 'pop', 'j_you'); at(T('s07.1'), 1.0, 'write', 'j_foot');
at(W('s07.2', 'twelve') - 0.4, 1.0, 'draw', 'j_alt', { quiet: 1 }); at(W('s07.2', 'twelve') + 0.5, 0.2, 'draw', 'j_ah', { quiet: 1 });
at(W('s07.2', 'twelve') + 0.6, 0.3, 'pop', 'j_sat'); at(W('s07.2', 'twelve') + 0.4, 1.4, 'draw', 'j_orbit', { quiet: 1 });
at(W('s07.2', 'twelve'), 1.3, 'write', 'j_km'); at(W('s07.2', 'miles'), 0.9, 'write', 'j_mi');
at(W('s07.2', 'pull') - 0.2, 1.4, 'write', 'j_weak'); at(W('s07.2', 'pull'), 0.8, 'fade', 'j_scale');
at(W('s07.3', 'forty') - 0.2, 1.3, 'write', 'j_45'); at(W('s07.3', 'ahead') - 0.2, 0.9, 'write', 'j_ahead');
at(W('s07.3', 'fast'), E('s07.3') - W('s07.3', 'fast'), 'fn', 'j_sat', { f: (n, u, t, on) => { if (!on) return; const a = -Math.PI / 2 + 0.6 * (t - W('s07.3', 'fast')); n.setAttribute('cx', 700 + 459 * Math.cos(a)); n.setAttribute('cy', 560 + 459 * Math.sin(a)); } });
HOOKS.push((t, active) => { if (active.has('s06') || active.has('s06b')) GRAV.forEach(([id, r]) => spin(id, r * t)); });
```

## gps/parts/s08.html

Доски 11–12: разметка.

```html
<!-- s08 put both together -->
<div class="sc" id="s08">
 <div class="ck" id="k_head" style="left:120px;top:70px;font-size:80px;font-weight:600">put both together:</div>
 <div class="ck" id="k_sp" style="left:120px;top:220px;font-size:76px;color:#ff8f7a">speed: −7.2 µs</div>
 <div class="ck" id="k_ht" style="left:120px;top:320px;font-size:76px;color:#ffb36b">height: +45.8 µs</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-linecap="round"><path id="k_ul" d="M120 432 C 300 428 520 436 700 430" stroke-width="6"/></g></svg>
 <div class="ck" id="k_net" style="left:120px;top:456px;font-size:110px;font-weight:700">+38.6 µs a day</div>
 <div class="lab" id="k_lab" style="left:126px;top:592px;font-size:17px">SATELLITE CLOCK AHEAD OF GROUND CLOCKS (COMPUTED)</div>
 <div class="ck" id="k_nothing" style="left:120px;top:660px;font-size:52px;opacity:.85">sounds like nothing…</div>
 <div class="ck" id="k_light" style="left:120px;top:750px;font-size:64px;color:#9fd0ff">light in 38.6 µs: 7 miles</div>
 <div class="ck" id="k_km" style="left:130px;top:836px;font-size:48px;opacity:.85">(11.6 km)</div>
 <svg class="draw" width="1920" height="1080" id="k_map"><g fill="none" stroke="#f4f1ea" stroke-width="3" stroke-linecap="round" opacity=".4">
  <path d="M1080 230 C 1300 246 1560 220 1800 238"/><path d="M1080 846 C 1320 830 1560 860 1800 840"/><path d="M1150 160 C 1160 400 1136 640 1166 900"/>
  <path d="M1080 700 C 1200 690 1300 720 1340 900" stroke-dasharray="10 9"/></g></svg>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <path id="k_frame" d="M1070 150 H 1810 V 910 H 1070 Z" stroke="#f4f1ea" stroke-width="5"/>
  <circle id="k_c1" cx="1440" cy="530" r="82" stroke="#ff8f7a" stroke-width="5"/>
  <circle id="k_c2" cx="1440" cy="530" r="164" stroke="#ff8f7a" stroke-width="5" stroke-dasharray="16 10"/>
  <circle id="k_c3" cx="1440" cy="530" r="246" stroke="#ff8f7a" stroke-width="5" stroke-dasharray="6 10"/>
  <circle id="k_you" cx="1440" cy="530" r="14" fill="#9fd0ff" stroke="none"/>
 </g></svg>
 <div class="ck" id="k_d1" style="left:1532px;top:514px;font-size:30px;color:#ff8f7a">day 1</div>
 <div class="ck" id="k_d2" style="left:1614px;top:514px;font-size:30px;color:#ff8f7a">day 2</div>
 <div class="ck" id="k_d3" style="left:1694px;top:514px;font-size:30px;color:#ff8f7a">day 3</div>
 <div class="ck" id="k_mis" style="left:1070px;top:940px;font-size:56px;color:#ff8f7a">a new 7 miles of mistake, every day</div>
 <div class="lab" id="k_scale" style="left:1080px;top:118px;font-size:15px">MAP: 60 MILES ACROSS</div>
</div>

<!-- s09 how they fix it -->
<div class="sc" id="s09">
 <div class="ck" id="l_what" style="left:120px;top:70px;font-size:72px">so what did they do?</div>
 <div class="ck" id="l_cheat" style="left:120px;top:160px;font-size:96px;font-weight:700;color:#ffb36b;transform:rotate(-2deg)">they cheated.</div>
 <div class="ck" id="l_slow" style="left:120px;top:290px;font-size:60px">set slow on purpose:</div>
 <div class="ck" id="l_sh" style="left:120px;top:420px;font-size:56px">should be:</div>
 <div class="ck mono" id="l_n1" style="left:420px;top:414px;font-size:56px;font-family:SpaceMono">10.23000000000 MHz</div>
 <div class="ck" id="l_st" style="left:120px;top:510px;font-size:56px;color:#9fd0ff">set to:</div>
 <div class="ck mono" id="l_n2" style="left:420px;top:504px;font-size:56px;font-family:SpaceMono;color:#9fd0ff">10.22999999543 MHz</div>
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke-linecap="round">
  <path id="l_ul" d="M514 584 C 640 580 780 588 896 582" stroke="#ff8f7a" stroke-width="5"/>
  <path id="l_dish" d="M1560 870 C 1580 930 1660 940 1700 900 Z M1630 912 L 1610 960 M1630 912 L 1650 960 M1596 960 H 1664" stroke="#f4f1ea" stroke-width="5"/>
  <path id="l_up1" d="M1640 860 L 1700 560 M1686 586 L 1702 556 L 1712 590" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="12 10"/>
  <path id="l_sat" d="M1686 520 H 1718 V 540 H 1686 Z M1684 530 H 1650 M1720 530 H 1754" stroke="#f4f1ea" stroke-width="4"/>
 </g></svg>
 <div class="ck" id="l_bil" style="left:120px;top:620px;font-size:60px">0.45 in a billion slower</div>
 <div class="lab" id="l_lab" style="left:126px;top:700px;font-size:17px">OFFSET −4.4647 × 10^−10, GPS SIGNAL SPEC IS-GPS-200</div>
 <div class="ck" id="l_gr" style="left:120px;top:780px;font-size:60px;color:#ff8f7a">on the ground: wrong</div>
 <div class="ck" id="l_or" style="left:740px;top:780px;font-size:60px;color:#9fd0ff">in orbit: just right</div>
 <div class="ck" id="l_cor" style="left:860px;top:930px;font-size:48px">small corrections, every day</div>
 <div class="cw" id="c_ein2" style="left:1420px;top:110px;width:320px;height:333px">
  <img src="../assets/p/einstein_rough.png" style="transform:rotate(-4deg)">
  <div class="tape" id="l_tape" style="left:90px;top:-22px;transform:rotate(5deg)"></div>
 </div>
 <div class="ck" id="l_arg" style="left:1180px;top:470px;font-size:48px">no arguing →</div>
</div>
```

## gps/parts/s08.js

Доски 11–12: таймлайн.

```js
// ---------- s08 the sum and the growing error (map scale: 700 px = 60 miles, so 7 miles = 82 px)
at(T('s08.1'), 1.3, 'write', 'k_head');
at(T('s08.2'), 1.2, 'write', 'k_sp'); at(T('s08.3'), 1.2, 'write', 'k_ht');
at(T('s08.4') + 0.3, 0.6, 'draw', 'k_ul'); at(W('s08.4', 'thirty') - 0.2, 1.4, 'write', 'k_net'); at(W('s08.4', 'second'), 0.8, 'fade', 'k_lab');
at(T('s08.5'), 1.1, 'write', 'k_nothing');
at(W('s08.6', 'light'), 1.6, 'write', 'k_light'); at(W('s08.6', 'miles') + 0.2, 0.6, 'write', 'k_km');
at(W('s08.6', 'light') - 0.3, 0.6, 'draw', 'k_frame', { quiet: 1 }); at(W('s08.6', 'light'), 0.8, 'wipe', 'k_map'); at(W('s08.6', 'light') + 0.5, 0.3, 'pop', 'k_you');
at(W('s08.6', 'light') + 0.4, 0.6, 'fade', 'k_scale');
at(W('s08.7', 'mistake') - 0.4, 0.6, 'draw', 'k_c1', { note: 0 }); at(W('s08.7', 'mistake'), 0.5, 'write', 'k_d1');
at(T('s08.8'), 0.6, 'draw', 'k_c2', { note: 2 }); at(T('s08.8') + 0.4, 0.5, 'write', 'k_d2');
at(W('s08.8', 'single') - 0.1, 0.6, 'draw', 'k_c3', { note: 4 }); at(W('s08.8', 'single') + 0.3, 0.5, 'write', 'k_d3');
at(W('s08.7', 'system'), 1.6, 'write', 'k_mis');

// ---------- s09 the deliberate offset
cut('c_ein2', { t: W('s09.2', 'Einstein') - 0.1, from: [500, -200, 20], wig: [T('s09.3')], out: hold('s09') - 0.6, to: [800, -300, 18] });
at(W('s09.2', 'Einstein') + 0.4, 0.25, 'tape', 'l_tape'); at(W('s09.2', 'argue'), 0.8, 'write', 'l_arg');
at(T('s09.1'), 1.4, 'write', 'l_what'); at(T('s09.3'), 0.5, 'pop', 'l_cheat');
at(W('s09.4', 'set') - 0.2, 1.6, 'write', 'l_slow');
at(W('s09.5', 'should') - 0.1, 0.6, 'write', 'l_sh'); at(W('s09.5', 'ten'), 1.4, 'write', 'l_n1');
at(T('s09.6') + 0.3, 0.5, 'write', 'l_st'); at(W('s09.6', 'ten'), 0.6, 'write', 'l_n2');
at(W('s09.6', 'ten'), W('s09.6', 'four') + 0.3 - W('s09.6', 'ten'), 'fn', 'l_n2', { f: (n, u) => { const full = '10.22999999543'; n.textContent = full.slice(0, 5 + Math.floor(u * (full.length - 5))) + ' MHz'; }, sound: 'counter', soundArgs: { d: 3.0 } });
at(W('s09.6', 'four') + 0.3, 0.6, 'draw', 'l_ul');
at(W('s09.7', 'half') - 0.3, 1.3, 'write', 'l_bil'); at(E('s09.7') - 0.3, 0.6, 'fade', 'l_lab');
at(W('s09.8', 'ground'), 1.0, 'write', 'l_gr'); at(W('s09.9', 'orbit'), 1.2, 'write', 'l_or');
at(W('s09.10', 'team') - 0.2, 0.6, 'draw', 'l_dish'); at(W('s09.10', 'sends'), 0.8, 'draw', 'l_up1', { quiet: 1 }); at(W('s09.10', 'corrections') - 0.3, 0.4, 'draw', 'l_sat', { quiet: 1 });
at(W('s09.10', 'corrections'), 1.4, 'write', 'l_cor');
```

## gps/parts/s10.html

Доски 13–14: разметка.

```html
<!-- s10 the 1977 test -->
<div class="sc" id="s10">
 <div class="cw" id="c_nts" style="left:110px;top:150px;width:380px;height:494px">
  <img src="../assets/p/nts2_rough.png" style="transform:rotate(-3deg)">
  <div class="tape" id="m_tape" style="left:115px;top:-22px;transform:rotate(-4deg)"></div>
 </div>
 <div class="ck" id="m_trust" style="left:580px;top:70px;font-size:72px">did they trust Einstein?</div>
 <div class="ck" id="m_not" style="left:1380px;top:70px;font-size:64px;color:#ffb36b">not completely.</div>
 <div class="ck" id="m_1977" style="left:580px;top:190px;font-size:64px">1977: test satellite NTS-2</div>
 <svg class="draw" width="1920" height="1080" id="m_g"></svg>
 <div class="ck" id="m_off" style="left:780px;top:308px;font-size:60px;color:#ff8f7a">correction: OFF</div>
 <div class="ck" id="m_on" style="left:780px;top:308px;font-size:60px;color:#9fd0ff">correction: ON</div>
 <div class="ck" id="m_case" style="left:1250px;top:316px;font-size:48px;opacity:.85">just in case</div>
 <div class="ck" id="m_3w" style="left:580px;top:440px;font-size:52px">about 3 weeks on its own:</div>
 <div class="ck" id="m_mea" style="left:1100px;top:470px;font-size:48px">measured: 443.1</div>
 <div class="ck" id="m_pre" style="left:1100px;top:610px;font-size:48px;color:#ffb36b">Einstein: 445.0</div>
 <div class="lab" id="m_ppt" style="left:1104px;top:756px;font-size:15px">PARTS PER TRILLION, BARS FROM 400 · NRL REPORT 8232</div>
 <div class="ck" id="m_1pc" style="left:1240px;top:810px;font-size:96px;font-weight:700;color:#9fd0ff">within 0.5%</div>
 <div class="lab" id="m_cred" style="left:110px;top:1032px;font-size:14px">PHOTO: U.S. NAVY · PUBLIC DOMAIN</div>
</div>

<!-- s11 check it yourself -->
<div class="sc" id="s11">
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  <path id="n_phone" d="M196 150 H 454 Q 500 150 500 196 V 884 Q 500 930 454 930 H 196 Q 150 930 150 884 V 196 Q 150 150 196 150 Z"/></g></svg>
 <svg class="draw" width="1920" height="1080" id="n_g"></svg>
 <div class="ck" id="n_see" style="left:620px;top:110px;font-size:80px;font-weight:600">see it yourself:</div>
 <div class="ck" id="n_out" style="left:620px;top:240px;font-size:60px">1. go outside</div>
 <div class="ck" id="n_app" style="left:620px;top:330px;font-size:60px">2. open a GPS status app (Android)</div>
 <div class="ck" id="n_g1" style="left:620px;top:420px;font-size:60px;color:#9fd0ff">3. find the ones marked GPS</div>
 <div class="ck" id="n_slow" style="left:620px;top:560px;font-size:72px;color:#ffb36b">every one: clocks set slow</div>
 <div class="ck" id="n_pur" style="left:620px;top:650px;font-size:72px;color:#ffb36b">on purpose</div>
 <div class="lab" id="n_lab" style="left:620px;top:780px;font-size:16px">SKY PLOT: SATELLITES YOUR PHONE HEARS (ILLUSTRATION)</div>
</div>
```

## gps/parts/s10.js

Доски 13–14: таймлайн.

```js
// ---------- s10 NTS-2: flown with the correction off, measured, then switched on
{
  const g = $('m_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round' };
  el(g, 'rect', { ...S, id: 'm_sw', x: 590, y: 316, width: 150, height: 56, rx: 28, 'stroke-width': 5 });
  el(g, 'circle', { id: 'm_knob', cx: 618, cy: 344, r: 20, fill: '#ff8f7a' });
  for (let k = 0; k < 21; k++) {   // 21 days, 20 crossed out
    const x = 590 + (k % 7) * 64, y = 520 + Math.floor(k / 7) * 64;
    el(g, 'rect', { ...S, id: `m_d${k}`, x, y, width: 52, height: 52, 'stroke-width': 3, opacity: .8 });
    if (k < 20) el(g, 'path', { ...S, id: `m_x${k}`, d: `M${x + 10} ${y + 10} L ${x + 42} ${y + 42} M${x + 42} ${y + 10} L ${x + 10} ${y + 42}`, stroke: '#ff8f7a', 'stroke-width': 3 });
  }
  const bar = (id, y, val, col) => el(g, 'line', { ...S, id, x1: 1104, y1: y, x2: 1104 + (val - 400) * 14, y2: y, stroke: col, 'stroke-width': 34, 'stroke-linecap': 'butt' });
  bar('m_b1', 560, 443.1, '#f4f1ea'); bar('m_b2', 700, 445.0, '#ffb36b');   // bars start at 400: the 4-part gap stays visible
}
cut('c_nts', { t: W('s10.3', 'test') - 0.2, from: [-500, -100, -20], wig: [T('s10.4')], out: hold('s10') - 0.6, to: [-900, -260, -18] });
at(W('s10.3', 'test') + 0.3, 0.25, 'tape', 'm_tape'); at(W('s10.3', 'test') + 0.8, 0.8, 'fade', 'm_cred');
at(T('s10.1'), 1.4, 'write', 'm_trust'); at(T('s10.2'), 0.8, 'write', 'm_not');
at(W('s10.3', '1977'), 1.4, 'write', 'm_1977');
at(W('s10.3', 'correction'), 0.4, 'draw', 'm_sw'); at(W('s10.3', 'switched'), 0.3, 'pop', 'm_knob'); at(W('s10.3', 'off') - 0.2, 0.8, 'write', 'm_off');
at(T('s10.4'), 0.8, 'write', 'm_case');
at(T('s10.5'), 1.2, 'write', 'm_3w');
for (let k = 0; k < 21; k++) at(W('s10.5', 'three') + k * 0.04, 0.12, 'draw', `m_d${k}`, { quiet: 1 });
for (let k = 0; k < 20; k++) at(W('s10.5', 'watched') + k * 0.1, 0.1, 'draw', `m_x${k}`, { quiet: k % 4 > 0 });
at(W('s10.6', 'fast') - 0.1, 0.8, 'write', 'm_mea'); at(W('s10.6', 'four') - 0.2, 1.4, 'grow', 'm_b1', { note: 1 });
at(W('s10.7', 'prediction') - 0.2, 0.8, 'write', 'm_pre'); at(W('s10.7', 'four') - 0.2, 1.4, 'grow', 'm_b2', { note: 3 });
at(E('s10.7') - 0.3, 0.6, 'fade', 'm_ppt'); at(T('s10.8'), 0.5, 'pop', 'm_1pc');
const SW = W('s10.9', 'switched');
at(SW, 0.3, 'fn', 'm_knob', { f: (n, u, t, on) => { n.setAttribute('cx', 618 + 94 * u); n.setAttribute('fill', u > 0.5 ? '#9fd0ff' : '#ff8f7a'); }, sound: 'pop' });
at(SW, 0.2, 'hide', 'm_off'); at(SW + 0.3, 0.6, 'write', 'm_on');

// ---------- s11 sky plot on a phone
{
  const g = $('n_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round' };
  el(g, 'circle', { ...S, id: 'n_sky', cx: 325, cy: 520, r: 140, 'stroke-width': 4 });
  el(g, 'circle', { ...S, id: 'n_sky2', cx: 325, cy: 520, r: 70, 'stroke-width': 3, opacity: .6 });
  el(g, 'path', { ...S, id: 'n_cr', d: 'M185 520 H 465 M325 380 V 660', 'stroke-width': 2, opacity: .5 });
  [[270, 440, 1], [390, 470, 1], [300, 600, 1], [410, 580, 0], [230, 520, 0], [350, 410, 0], [250, 620, 1], [440, 520, 0]].forEach(([x, y, gps], i) =>
    el(g, 'circle', { id: `n_s${i}`, cx: x, cy: y, r: 9, fill: gps ? '#9fd0ff' : '#f4f1ea', opacity: gps ? 1 : .55, 'data-gps': gps }));
}
at(T('s11.1') - 0.2, 1.3, 'draw', 'n_phone'); at(T('s11.1'), 1.4, 'write', 'n_see');
at(W('s11.2', 'outside') - 0.3, 0.9, 'write', 'n_out'); at(W('s11.2', 'app') - 0.6, 1.3, 'write', 'n_app');
at(W('s11.2', 'satellites') - 0.3, 0.6, 'draw', 'n_sky', { quiet: 1 }); at(W('s11.2', 'satellites'), 0.4, 'draw', 'n_sky2', { quiet: 1 }); at(W('s11.2', 'satellites') + 0.2, 0.3, 'draw', 'n_cr', { quiet: 1 });
for (let i = 0; i < 8; i++) at(W('s11.2', 'hears') + i * 0.12, 0.25, 'pop', `n_s${i}`, { quiet: i > 0 });
at(W('s11.2', 'satellites'), 0.8, 'fade', 'n_lab');
at(T('s11.3'), 1.4, 'write', 'n_g1');
for (let i = 0; i < 8; i++) if ($(`n_s${i}`).dataset.gps === '1') at(W('s11.3', 'GPS'), 1.6, 'fn', `n_s${i}`, { f: (n, u, t, on) => { if (on) n.setAttribute('r', 9 + 6 * Math.sin(Math.PI * Math.min(1, u * 2))); } });
at(W('s11.4', 'clocks') - 0.3, 1.4, 'write', 'n_slow'); at(W('s11.4', 'purpose') - 0.2, 0.9, 'write', 'n_pur');
```

## gps/parts/s12.html

Доска 15: разметка.

```html
<!-- s12 finale -->
<div class="sc" id="s12">
 <svg class="draw" width="1920" height="1080"><g fill="none" stroke="#f4f1ea" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  <path id="o_phone" d="M196 150 H 454 Q 500 150 500 196 V 884 Q 500 930 454 930 H 196 Q 150 930 150 884 V 196 Q 150 150 196 150 Z"/></g></svg>
 <svg class="draw" width="1920" height="1080" id="o_map"><g fill="none" stroke="#f4f1ea" stroke-width="3" stroke-linecap="round" opacity=".45">
  <path d="M178 330 C 260 350 380 320 472 345"/><path d="M178 470 C 280 480 360 455 472 470"/><path d="M178 760 C 270 740 380 780 472 755"/>
  <path d="M240 210 C 250 400 230 600 260 900"/><path d="M410 210 C 395 420 430 640 400 900"/></g></svg>
 <svg class="draw" width="1920" height="1080"><g fill="none"><circle id="o_dot" cx="330" cy="560" r="17" fill="#9fd0ff"/></g></svg>
 <div class="ck" id="o_two" style="left:620px;top:110px;font-size:60px">two of Einstein's ideas did the math:</div>
 <div class="ck" id="o_sp" style="left:620px;top:220px;font-size:88px">speed slows time.</div>
 <div class="ck" id="o_gr" style="left:620px;top:330px;font-size:88px;color:#ffb36b">gravity slows time.</div>
 <div class="ck" id="o_cof" style="left:620px;top:480px;font-size:60px">your phone needs both</div>
 <div class="ck" id="o_cof2" style="left:620px;top:556px;font-size:60px">to find your coffee →</div>
 <div class="cw" id="c_cof" style="left:1290px;top:400px;width:440px;height:336px">
  <img src="../assets/p/coffee_rough.png" style="transform:rotate(3deg)">
  <div class="tape" id="o_tape" style="left:140px;top:-22px;transform:rotate(-4deg)"></div>
 </div>
 <div class="cw" id="c_cat5" style="left:620px;top:700px;width:560px;height:259px">
  <img src="../assets/p/cat_flat_rough.png" style="transform:rotate(2deg)">
 </div>
 <div class="ck" id="o_even" style="left:1220px;top:860px;font-size:64px">← aging very evenly</div>
 <div class="lab" id="o_end" style="left:1220px;top:990px">PHYSICS, PLAINLY · 01</div>
</div>
```

## gps/parts/s12.js

Доска 15: таймлайн.

```js
// ---------- s12 finale: the last board stays
cut('c_cof', { t: W('s12.4', 'coffee') - 0.1, from: [600, -100, 20], wig: [W('s12.4', 'coffee') + 1.0], out: 1e9 });
cut('c_cat5', { t: W('s12.5', 'cat') - 0.1, from: [0, 500, 0], back: 1.2, wig: [W('s12.7', 'evenly')], out: 1e9 });
at(T('s12.1') - 0.3, 1.3, 'draw', 'o_phone'); at(T('s12.1') + 0.6, 0.8, 'wipe', 'o_map'); at(W('s12.1', 'dot'), 0.35, 'pop', 'o_dot');
at(W('s12.1', 'two'), 2.0, 'write', 'o_two');
at(T('s12.2'), 1.1, 'write', 'o_sp'); at(T('s12.3'), 1.1, 'write', 'o_gr');
at(W('s12.4', 'phone') - 0.2, 1.0, 'write', 'o_cof'); at(W('s12.4', 'find'), 1.0, 'write', 'o_cof2');
at(W('s12.4', 'coffee') + 0.4, 0.25, 'tape', 'o_tape');
at(W('s12.7', 'Aging'), 1.0, 'write', 'o_even'); at(E('s12.7') + 0.3, 0.8, 'fade', 'o_end');
```

## gps/short.tpl.html

Шаблон вертикальной страницы Shorts.

```html
<!doctype html><html><head><meta charset="utf-8"><title>GPS short</title>
<link rel="stylesheet" href="../../lib/chalk.css">
<style>
.flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
</style>
<script src="../../lib/chalk.js"></script></head><body>
<script>Chalk.chrome({ w: 1080, h: 1920 })</script>

{{MARKUP}}
<script>
const { $, el, at, cut, cl, out3 } = Chalk;
// narration timeline (estimate now, ElevenLabs alignment later): every visual is keyed to a line or a word
const TLJ = (() => { const x = new XMLHttpRequest(); x.open('GET', 'timing/timeline.json', false); x.send(); return JSON.parse(x.responseText); })();
const LN = {}; TLJ.lines.forEach(L => LN[L.id] = L);
const T = (id, f = 0) => LN[id].t0 + f * (LN[id].t1 - LN[id].t0);
const E = id => LN[id].t1;
const W = (id, w, k = 0) => { const ws = LN[id].words.filter(x => x.w.toLowerCase().replace(/[^a-z0-9']/g, '').startsWith(w.toLowerCase())); if (!ws[k]) throw new Error(`word ${w} not in ${id}`); return ws[k].t0; };
const lines = s => TLJ.lines.filter(L => L.scene === s);
const FPS = 30, ER = Chalk.cfg.erase;
const SCN = [...new Set(TLJ.lines.map(L => L.scene))].filter(s => $(s));
// scene windows: a board starts once the previous one is erased, and is erased 0.25 s after its last line
const WIN = {}; let prevEnd = 0;
SCN.forEach((s, i) => { const L = lines(s); const t0 = i ? prevEnd : 0, te = L[L.length - 1].t1 + 0.25; WIN[s] = [t0, te]; prevEnd = te + ER + 0.05; });
const FULL = SCN.length === new Set(TLJ.lines.map(L => L.scene)).size;   // false while only the first scenes exist (probe)
const NF = Math.round((FULL ? TLJ.total : WIN[SCN[SCN.length - 1]][1] + ER + 0.5) * FPS);
SCN.forEach((s, i) => Chalk.scene(s, WIN[s][0], FULL && i === SCN.length - 1 ? 1e9 : WIN[s][1]));   // the last board of the film stays
const hold = s => WIN[s][1];   // cut-outs leave just before the eraser

const HOOKS = [];   // per-frame updates of each board
const spin = (id, deg) => { const n = $(id); n.style.transformBox = 'view-box'; n.style.transformOrigin = `${n.dataset.cx}px ${n.dataset.cy}px`; n.style.transform = `rotate(${deg.toFixed(2)}deg)`; };
{{SCRIPT}}
window.onFrame = (t, active) => HOOKS.forEach(h => h(t, active));
const TEX = ['Δt = γΔτ', 'γ = 1/√(1 − v²/c²)', 'v ≈ 3.87 km/s', 'Δf/f = −4.4647·10⁻¹⁰', 'ΔU/c²', 'GM/r', 'c = 299 792 458 m/s', 
  '10.23 MHz', 'r ≈ 26 562 km', 'T ≈ 11 h 58 min', '½ v²/c²', 'd = c·Δt', '1 ns ≈ 30 cm', 'gh/c²', 'L1 1575.42 MHz', 'x² + y² + z²', 'Δt·c'];
Chalk.start({ frames: NF, fps: FPS, formulas: TEX });
</script></body></html>
```

## gps/build_short.py

Сборка страницы Short.

```python
"""Assemble a vertical Short page: python build_short.py short1  ->  gps/short1/short1.html from short.tpl.html + short1/parts.html + parts.js"""
import os, sys
D = os.path.dirname(os.path.abspath(__file__)); n = sys.argv[1]
tpl = open(os.path.join(D, 'short.tpl.html')).read()
html = open(os.path.join(D, n, 'parts.html')).read(); js = open(os.path.join(D, n, 'parts.js')).read()
open(os.path.join(D, n, n + '.html'), 'w').write(tpl.replace('{{MARKUP}}', html).replace('{{SCRIPT}}', js))
print(os.path.join(D, n, n + '.html'))
```

## gps/short1/narration.txt

Short 1: текст.

```text
## h1
Moving clocks run slow.
And you can prove it with two mirrors.

## h1b
Light bounces between them: up, down, tick.
Now move the clock.
From where you stand, the light has to go sideways too.
[pause 0.8]
Longer path.
But light's speed never changes.
So every tick takes longer.

## h1c
GPS satellites move fast enough to lose seven millionths of a second a day.
Gravity adds back forty-five.
So engineers set their clocks slow on purpose.
Otherwise your map would drift seven miles a day.
```

## gps/short1/parts.html

Short 1: разметка.

```html
<!-- h1 hook -->
<div class="sc" id="h1">
 <div class="lab" id="p_lab" style="left:80px;top:150px">PHYSICS, PLAINLY</div>
 <div class="ck" id="p_mov" style="left:80px;top:290px;font-size:130px;font-weight:600">moving clocks</div>
 <div class="ck" id="p_slow" style="left:80px;top:440px;font-size:150px;font-weight:700;color:#ffb36b">run slow.</div>
 <div class="ck" id="p_proof" style="left:80px;top:680px;font-size:80px;color:#9fd0ff">proof: two mirrors</div>
 <div class="cw" id="c_pcat" style="left:540px;top:860px;width:380px;height:491px">
  <img src="../../assets/p/cat_black_rough.png" style="transform:rotate(-3deg)">
  <div class="tape" id="p_tape" style="left:115px;top:-22px;transform:rotate(4deg)"></div>
 </div>
</div>

<!-- h1b light clock -->
<div class="sc" id="h1b">
 <div class="ck" id="q_head" style="left:80px;top:160px;font-size:80px;font-weight:600">the simplest clock:</div>
 <div data-box="1" style="position:absolute;left:100px;top:740px;width:980px;height:240px"></div>
 <svg class="draw" width="1080" height="1920"><g fill="none" stroke="#f4f1ea" stroke-linecap="round">
  <path id="q_m1" d="M140 330 H 270" stroke-width="8"/><path id="q_m2" d="M140 530 H 270" stroke-width="8"/>
  <circle id="q_dot" cx="205" cy="524" r="11" fill="#ffe48a" stroke="none"/>
 </g></svg>
 <svg class="draw" width="1080" height="1920" data-bleed="1"><g fill="none" stroke-linecap="round">
  <path id="q_trail" stroke="#ffe48a" stroke-width="4" opacity=".75"/>
  <g id="q_mov"><path id="q_n1" d="M140 760 H 270" stroke="#f4f1ea" stroke-width="8"/><path id="q_n2" d="M140 960 H 270" stroke="#f4f1ea" stroke-width="8"/>
   <circle id="q_ndot" cx="205" cy="954" r="11" fill="#ffe48a" stroke="none"/></g>
 </g></svg>
 <div class="ck" id="q_tick" style="left:310px;top:390px;font-size:60px">up, down: tick</div>
 <div class="ck" id="q_move" style="left:310px;top:640px;font-size:60px">now move it →</div>
 <div class="ck mono" id="q_cs" style="left:80px;top:1040px;font-size:34px;font-family:SpaceMono">standing: 0 ticks</div>
 <div class="ck mono" id="q_cm" style="left:80px;top:1094px;font-size:34px;font-family:SpaceMono;color:#ffe48a">moving: 0 ticks</div>
 <div class="ck" id="q_long" style="left:80px;top:1190px;font-size:84px">longer path,</div>
 <div class="ck" id="q_same" style="left:80px;top:1296px;font-size:64px;color:#9fd0ff">same light speed</div>
 <div class="ck" id="q_slow" style="left:80px;top:1386px;font-size:64px;color:#ffb36b">→ every tick takes longer</div>
 <div class="lab" id="q_tilt" style="left:80px;top:1480px;font-size:15px">TILT AND SPEED EXAGGERATED</div>
</div>

<!-- h1c GPS -->
<div class="sc" id="h1c">
 <div class="cw" id="c_psat" style="left:140px;top:150px;width:800px;height:634px">
  <img src="../../assets/p/gps_iif_rough.png" style="transform:rotate(-3deg)">
  <div class="tape" id="r_tape" style="left:320px;top:-22px;transform:rotate(3deg)"></div>
 </div>
 <div class="lab" id="r_cred" style="left:140px;top:820px;font-size:14px">ILLUSTRATION: NASA · PUBLIC DOMAIN</div>
 <div class="ck" id="r_sp" style="left:80px;top:880px;font-size:76px;color:#ff8f7a">speed: −7 µs a day</div>
 <div class="ck" id="r_gr" style="left:80px;top:976px;font-size:76px;color:#ffb36b">gravity: +45 µs a day</div>
 <svg class="draw" width="1080" height="1920"><g fill="none" stroke="#f4f1ea" stroke-linecap="round"><path id="r_ul" d="M80 1084 C 300 1080 560 1088 860 1082" stroke-width="6"/></g></svg>
 <div class="ck" id="r_net" style="left:80px;top:1104px;font-size:96px;font-weight:700">net: +38 µs a day</div>
 <div class="ck" id="r_set" style="left:80px;top:1240px;font-size:72px;color:#9fd0ff">so: set slow on purpose</div>
 <div class="ck" id="r_drift" style="left:80px;top:1340px;font-size:56px">or your map drifts 7 miles a day</div>
 <div class="lab" id="r_end" style="left:80px;top:1470px;font-size:17px">FULL VIDEO: PHYSICS, PLAINLY · 01</div>
</div>
```

## gps/short1/parts.js

Short 1: таймлайн.

```js
// ---------- h1
cut('c_pcat', { t: W('h1.2', 'prove'), from: [0, 600, 0], back: 1.2, wig: [W('h1.2', 'mirrors')], out: hold('h1') - 0.6, to: [0, 1250, 0] });
at(W('h1.2', 'prove') + 0.5, 0.25, 'tape', 'p_tape');
at(0.2, 0.6, 'fade', 'p_lab'); at(T('h1.1'), 0.9, 'write', 'p_mov'); at(W('h1.1', 'slow') - 0.1, 0.6, 'write', 'p_slow');
at(W('h1.2', 'two') - 0.2, 1.0, 'write', 'p_proof');

// ---------- h1b light clock (same model as the long video, 4 legs)
const LC = { C: 800 / 3, gap: 200, v: 0.6 };
const legS = LC.gap / LC.C, legM = legS / Math.sqrt(1 - LC.v * LC.v), dxLeg = LC.v * LC.C * legM;
const STAND0 = W('h1b.1', 'bounces'), PASS0 = W('h1b.3', 'where'), NLEG = 4, PASS1 = PASS0 + NLEG * legM;
const bounce = (t, leg) => { const k = Math.floor(t / leg), f = t / leg - k; return k % 2 === 0 ? f : 1 - f; };
{ let d = 'M205 954'; for (let k = 1; k <= NLEG; k++) d += ` L ${205 + dxLeg * k} ${k % 2 ? 766 : 954}`; $('q_trail').setAttribute('d', d); }
at(T('h1b.1') - 0.3, 1.2, 'write', 'q_head');
at(T('h1b.1'), 0.3, 'draw', 'q_m1'); at(T('h1b.1') + 0.2, 0.3, 'draw', 'q_m2', { quiet: 1 }); at(STAND0, 0.3, 'pop', 'q_dot');
at(STAND0, 0.1, 'fn', 'q_dot', { f: (n, u, t, on) => { if (on) n.setAttribute('cy', 524 - 188 * bounce(t - STAND0, legS)); } });
at(W('h1b.1', 'tick') - 0.6, 1.0, 'write', 'q_tick');
for (let k = 1; STAND0 + 2 * k * legS < hold('h1b'); k++) Chalk.event(STAND0 + 2 * k * legS, 'tick', { n: 1, g: 0.08, f: 2600, pan: -0.3 });
at(T('h1b.2'), 0.3, 'draw', 'q_n1'); at(T('h1b.2') + 0.15, 0.3, 'draw', 'q_n2', { quiet: 1 }); at(T('h1b.2') + 0.3, 0.3, 'pop', 'q_ndot');
at(W('h1b.2', 'move'), 0.9, 'write', 'q_move');
const movX = t => t < PASS0 ? 0 : t < PASS1 ? dxLeg / legM * (t - PASS0) : dxLeg * NLEG + 900 * Math.pow(t - PASS1, 2);
at(T('h1b.2'), 0.1, 'fn', 'q_mov', { f: (n, u, t) => { n.setAttribute('transform', `translate(${movX(t).toFixed(2)},0)`); } });
at(T('h1b.2') + 0.3, 0.1, 'fn', 'q_ndot', { f: (n, u, t, on) => { if (on) n.setAttribute('cy', 954 - 188 * (t < PASS0 ? 0 : t < PASS1 ? bounce(t - PASS0, legM) : bounce(PASS1 - PASS0, legM))); } });
at(PASS0, PASS1 - PASS0, 'draw', 'q_trail', { quiet: 1 });
Chalk.event(PASS1, 'whoosh', { d: 0.6, f0: 400, f1: 2400, g: 0.12, pan: 0.6 });
for (let k = 1; 2 * k * legM <= PASS1 - PASS0 + 1e-6; k++) Chalk.event(PASS0 + 2 * k * legM, 'tick', { n: 1, g: 0.09, f: 1900, pan: 0.4 });
at(PASS0, PASS1 - PASS0, 'fn', 'q_cs', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.textContent = `standing: ${Math.floor((Math.min(t, PASS1) - PASS0) / (2 * legS) + 1e-6)} ticks`; } });
at(PASS0, PASS1 - PASS0, 'fn', 'q_cm', { f: (n, u, t, on) => { n.style.visibility = on ? 'visible' : 'hidden'; n.textContent = `moving: ${Math.floor((Math.min(t, PASS1) - PASS0) / (2 * legM) + 1e-6)} ticks`; } });
at(T('h1b.4'), 0.8, 'write', 'q_long'); at(T('h1b.5'), 1.2, 'write', 'q_same'); at(T('h1b.6'), 1.3, 'write', 'q_slow');
at(PASS1, 0.8, 'fade', 'q_tilt');

// ---------- h1c GPS
cut('c_psat', { t: T('h1c.1') - 0.1, from: [0, -700, -10], wig: [W('h1c.2', 'Gravity')], out: 1e9 });
at(T('h1c.1') + 0.4, 0.25, 'tape', 'r_tape'); at(T('h1c.1') + 0.8, 0.8, 'fade', 'r_cred');
at(W('h1c.1', 'seven') - 0.3, 1.3, 'write', 'r_sp'); at(T('h1c.2'), 1.2, 'write', 'r_gr');
at(E('h1c.2') - 0.2, 0.5, 'draw', 'r_ul'); at(E('h1c.2'), 0.9, 'write', 'r_net');
at(W('h1c.3', 'slow') - 0.4, 1.2, 'write', 'r_set'); at(W('h1c.4', 'map') - 0.2, 1.4, 'write', 'r_drift');
at(E('h1c.4') + 0.2, 0.8, 'fade', 'r_end');
```

## gps/short2/narration.txt

Short 2: текст.

```text
## h2
Your head is older than your feet.
Seriously.
Gravity slows time down, and your feet are closer to the Earth.

## h2b
In 2010, scientists in Colorado raised a super-precise clock by about a foot.
It ran faster.

## h2c
We did the math: stand for eighty years, and your head is almost half a millionth of a second older.
This cat lies flat all day.
Aging very evenly.
```

## gps/short2/parts.html

Short 2: разметка.

```html
<!-- h2 head and feet -->
<div class="sc" id="h2">
 <div class="lab" id="s_lab" style="left:80px;top:150px">PHYSICS, PLAINLY</div>
 <svg class="draw" width="1080" height="1920" id="s_g"></svg>
 <div class="ck" id="s_head" style="left:440px;top:290px;font-size:100px;font-weight:600">your head</div>
 <div class="ck" id="s_old" style="left:440px;top:410px;font-size:100px;font-weight:600;color:#ffb36b">is older</div>
 <div class="ck" id="s_feet" style="left:440px;top:530px;font-size:72px">than your feet.</div>
 <div class="ck" id="s_ser" style="left:440px;top:660px;font-size:64px;color:#ffb36b;transform:rotate(-3deg)">seriously.</div>
 <div class="ck" id="s_grav" style="left:440px;top:820px;font-size:60px">gravity slows time</div>
 <div class="ck" id="s_close" style="left:440px;top:900px;font-size:56px;color:#9fd0ff">feet: closer to Earth</div>
</div>

<!-- h2b NIST -->
<div class="sc" id="h2b">
 <div class="ck" id="t_nist" style="left:80px;top:200px;font-size:84px;font-weight:600">NIST, Colorado, 2010</div>
 <div class="ck" id="t_raise" style="left:80px;top:330px;font-size:64px">one clock raised ~1 foot</div>
 <svg class="draw" width="1080" height="1920" id="t_g"></svg>
 <div class="ck" id="t_33" style="left:806px;top:816px;font-size:52px">33 cm</div>
 <div class="ck" id="t_ran" style="left:540px;top:470px;font-size:76px;color:#ffb36b">ran faster</div>
</div>

<!-- h2c the math -->
<div class="sc" id="h2c">
 <div class="ck" id="u_80" style="left:80px;top:200px;font-size:72px">80 years standing:</div>
 <div class="ck" id="u_44" style="left:80px;top:300px;font-size:170px;font-weight:700;color:#ffb36b">+0.44 µs</div>
 <div class="ck" id="u_old" style="left:80px;top:500px;font-size:64px">older head</div>
 <div class="lab" id="u_calc" style="left:86px;top:600px;font-size:16px">1.6 M × 9.8 M/S² ÷ C² × 80 YEARS (COMPUTED)</div>
 <div class="cw" id="c_scat" style="left:100px;top:760px;width:860px;height:398px">
  <img src="../../assets/p/cat_flat_rough.png" style="transform:rotate(-2deg)">
  <div class="tape" id="u_tape" style="left:360px;top:-22px;transform:rotate(-3deg)"></div>
 </div>
 <div class="ck" id="u_even" style="left:80px;top:1230px;font-size:84px">aging very evenly.</div>
 <div class="lab" id="u_end" style="left:80px;top:1470px;font-size:17px">FULL VIDEO: PHYSICS, PLAINLY · 01</div>
</div>
```

## gps/short2/parts.js

Short 2: таймлайн.

```js
// ---------- h2 a figure with a clock at the head and at the feet
{
  const g = $('s_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
  el(g, 'path', { ...S, id: 's_gr', d: 'M60 1260 C 200 1254 380 1264 520 1258', 'stroke-width': 6 });
  el(g, 'circle', { ...S, id: 's_hd', cx: 230, cy: 420, r: 60, 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 's_bd', d: 'M230 480 C 226 600 234 740 230 860', 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 's_lg', d: 'M230 860 L 170 1250 M230 860 L 292 1250', 'stroke-width': 6 });
  el(g, 'path', { ...S, id: 's_ar', d: 'M228 540 L 140 740 M232 540 L 320 740', 'stroke-width': 6 });
  for (const [id, x, y] of [['s_k1', 360, 360], ['s_k2', 380, 1200]]) {
    el(g, 'circle', { ...S, id, cx: x, cy: y, r: 40, 'stroke-width': 5 });
    el(g, 'line', { ...S, id: id + 'h', x1: x, y1: y, x2: x, y2: y - 28, 'stroke-width': 5, 'data-cx': x, 'data-cy': y });
  }
}
at(0.2, 0.6, 'fade', 's_lab');
at(T('h2.1') - 0.4, 0.4, 'draw', 's_gr', { quiet: 1 }); at(T('h2.1') - 0.2, 0.4, 'draw', 's_hd'); at(T('h2.1'), 0.3, 'draw', 's_bd', { quiet: 1 });
at(T('h2.1') + 0.2, 0.3, 'draw', 's_lg', { quiet: 1 }); at(T('h2.1') + 0.4, 0.3, 'draw', 's_ar', { quiet: 1 });
at(W('h2.1', 'head') - 0.2, 0.7, 'write', 's_head'); at(W('h2.1', 'older') - 0.2, 0.6, 'write', 's_old'); at(W('h2.1', 'feet') - 0.4, 0.8, 'write', 's_feet');
at(W('h2.1', 'head'), 0.4, 'draw', 's_k1', { note: 1 }); at(W('h2.1', 'head') + 0.3, 0.2, 'draw', 's_k1h', { quiet: 1 });
at(W('h2.1', 'feet'), 0.4, 'draw', 's_k2', { note: 3 }); at(W('h2.1', 'feet') + 0.3, 0.2, 'draw', 's_k2h', { quiet: 1 });
at(T('h2.2'), 0.4, 'pop', 's_ser');
at(W('h2.3', 'Gravity'), 1.1, 'write', 's_grav'); at(W('h2.3', 'feet') - 0.2, 1.3, 'write', 's_close');
HOOKS.push((t, active) => { if (active.has('h2')) { spin('s_k1h', 95 * t); spin('s_k2h', 60 * t); } });

// ---------- h2b NIST, Boulder, 2010: one aluminium-ion clock raised 33 cm ran faster
{
  const g = $('t_g'), S = { fill: 'none', stroke: '#f4f1ea', 'stroke-linecap': 'round' };
  const clock = (id, x, y, r) => { el(g, 'circle', { ...S, id, cx: x, cy: y, r, 'stroke-width': 5 }); el(g, 'line', { ...S, id: id + 'h', x1: x, y1: y, x2: x, y2: y - r * 0.72, 'stroke-width': 5, 'data-cx': x, 'data-cy': y }); };
  el(g, 'path', { ...S, id: 't_tab', d: 'M100 900 H 900', 'stroke-width': 6 });
  el(g, 'rect', { ...S, id: 't_bxA', x: 160, y: 700, width: 200, height: 200, 'stroke-width': 5 });
  el(g, 'rect', { ...S, id: 't_blk', x: 560, y: 800, width: 200, height: 100, 'stroke-width': 5 });
  el(g, 'rect', { ...S, id: 't_bxB', x: 560, y: 600, width: 200, height: 200, 'stroke-width': 5 });
  clock('t_cA', 260, 800, 60); clock('t_cB', 660, 700, 60);
  el(g, 'path', { ...S, id: 't_ar', d: 'M790 800 V 900 M780 814 L 790 798 L 800 814 M780 886 L 790 902 L 800 886', 'stroke-width': 4 });
}
at(T('h2b.1'), 1.4, 'write', 't_nist'); at(W('h2b.1', 'raised') - 0.2, 1.3, 'write', 't_raise');
at(W('h2b.1', 'raised') - 0.5, 0.5, 'draw', 't_tab', { quiet: 1 }); at(W('h2b.1', 'raised') - 0.3, 0.4, 'draw', 't_bxA'); at(W('h2b.1', 'raised'), 0.3, 'draw', 't_cA', { quiet: 1 }); at(W('h2b.1', 'raised') + 0.2, 0.2, 'draw', 't_cAh', { quiet: 1 });
at(W('h2b.1', 'clock') - 0.2, 0.4, 'draw', 't_bxB'); at(W('h2b.1', 'clock'), 0.3, 'draw', 't_cB', { quiet: 1 }); at(W('h2b.1', 'clock') + 0.2, 0.2, 'draw', 't_cBh', { quiet: 1 });
at(W('h2b.1', 'foot') - 0.3, 0.4, 'draw', 't_blk'); at(W('h2b.1', 'foot'), 0.4, 'draw', 't_ar', { quiet: 1 }); at(W('h2b.1', 'foot') + 0.2, 0.6, 'write', 't_33');
at(T('h2b.2'), 0.9, 'write', 't_ran');
HOOKS.push((t, active) => { if (active.has('h2b')) { spin('t_cAh', 60 * t); spin('t_cBh', 90 * t); } });

// ---------- h2c the math and the flat cat
cut('c_scat', { t: W('h2c.2', 'cat') - 0.1, from: [0, 800, 0], back: 1.2, wig: [W('h2c.3', 'evenly')], out: 1e9 });
at(W('h2c.2', 'cat') + 0.5, 0.25, 'tape', 'u_tape');
at(W('h2c.1', 'eighty') - 0.2, 1.2, 'write', 'u_80'); at(W('h2c.1', 'half') - 0.3, 1.3, 'write', 'u_44'); at(W('h2c.1', 'older') - 0.1, 0.8, 'write', 'u_old');
at(E('h2c.1') - 0.4, 0.8, 'fade', 'u_calc');
at(W('h2c.3', 'Aging'), 1.1, 'write', 'u_even'); at(E('h2c.3') + 0.2, 0.8, 'fade', 'u_end');
```

## gps/thumbs/thumbs.html

Обложки A, B, C.

```html
<!doctype html><html><head><meta charset="utf-8"><title>GPS thumbnails</title>
<link rel="stylesheet" href="../../lib/chalk.css">
<style>
.flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
</style>
<script src="../../lib/chalk.js"></script></head><body>
<script>Chalk.chrome({ w: 1280, h: 720 })</script>


<!-- A: your phone needs Einstein -->
<div class="sc" id="tA">
 <svg class="draw" width="1280" height="720"><g fill="none" stroke="#f4f1ea" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  <path d="M112 90 H 290 Q 330 90 330 130 V 610 Q 330 650 290 650 H 112 Q 72 650 72 610 V 130 Q 72 90 112 90 Z"/></g>
  <g fill="none" stroke="#f4f1ea" stroke-width="3" opacity=".45"><path d="M92 260 C 160 270 250 250 312 264"/><path d="M92 470 C 170 460 250 480 312 470"/><path d="M150 112 C 160 300 140 480 166 630"/><path d="M262 112 C 250 300 276 480 254 630"/></g>
  <g fill="none" stroke="#9fd0ff"><circle cx="201" cy="370" r="34" stroke-width="5"/><circle cx="201" cy="370" r="58" stroke-width="3" stroke-dasharray="10 8"/></g>
  <circle cx="201" cy="370" r="20" fill="#9fd0ff"/></svg>
 <div class="ck" id="A1" style="left:390px;top:60px;font-size:104px;font-weight:600">your phone</div>
 <div class="ck" id="A2" style="left:390px;top:170px;font-size:104px;font-weight:600">needs</div>
 <div class="ck" id="A3" style="left:390px;top:280px;font-size:170px;font-weight:700;color:#ffb36b">Einstein</div>
 <div class="cw" id="tAs" style="left:930px;top:430px;width:300px;height:238px"><img src="../../assets/p/gps_iif_rough.png" style="transform:rotate(5deg)"><div class="tape" style="left:80px;top:-20px;transform:rotate(-4deg);width:120px;height:36px"></div></div>
 <div class="cw" id="tAc" style="left:560px;top:470px;width:250px;height:236px"><img src="../../assets/p/cat_stare_rough.png" style="transform:rotate(-4deg)">
  <svg class="draw" width="250" height="236" style="left:0;top:0"><g fill="none" stroke="#f4f1ea" stroke-width="4" stroke-linecap="round"><circle cx="98" cy="148" r="25"/><circle cx="162" cy="148" r="25"/><path d="M123 146 q 7 -7 14 0"/></g></svg></div>
</div>

<!-- B: +38 microseconds a day -->
<div class="sc" id="tB">
 <div class="ck" id="B1" style="left:60px;top:70px;font-size:250px;font-weight:700;color:#ffb36b">+38 µs</div>
 <div class="ck" id="B2" style="left:80px;top:330px;font-size:120px;font-weight:600">a day</div>
 <div class="ck" id="B3" style="left:80px;top:500px;font-size:64px;color:#9fd0ff">clocks in space run fast</div>
 <div class="cw" id="tBs" style="left:860px;top:70px;width:370px;height:258px"><img src="../../assets/p/gps_navstar_rough.png" style="transform:rotate(4deg)"><div class="tape" style="left:120px;top:-20px;transform:rotate(-3deg);width:120px;height:36px"></div></div>
 <div class="cw" id="tBc" style="left:930px;top:400px;width:290px;height:252px"><img src="../../assets/p/cat_scream_rough.png" style="transform:rotate(-5deg)"></div>
</div>

<!-- C: Einstein fixed your map (only if the photo is approved) -->
<div class="sc" id="tC">
 <div class="cw" id="tCe" style="left:60px;top:80px;width:500px;height:521px"><img src="../../assets/p/einstein_rough.png" style="transform:rotate(-3deg)"><div class="tape" style="left:180px;top:-22px;transform:rotate(4deg)"></div></div>
 <div class="ck" id="C1" style="left:640px;top:90px;font-size:110px;font-weight:600">he fixed</div>
 <div class="ck" id="C2" style="left:640px;top:210px;font-size:130px;font-weight:700;color:#ffb36b">your map</div>
 <div class="ck" id="C3" style="left:650px;top:390px;font-size:56px;color:#9fd0ff">…before GPS existed</div>
 <svg class="draw" width="1280" height="720"><g fill="none"><circle cx="1110" cy="560" r="46" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="10 8"/><circle cx="1110" cy="560" r="20" fill="#9fd0ff"/></g></svg>
</div>
<script>
const { $ } = Chalk;
Chalk.scene('tA', 0, 10, { push: 0 }); Chalk.scene('tB', 20, 30, { push: 0 }); Chalk.scene('tC', 40, 1e9, { push: 0 });
Chalk.start({ frames: 60 * 30, fps: 30, formulas: ['Δt = γΔτ', 'GM/r', 'c = 299 792 458 m/s', '10.23 MHz', 'r ≈ 26 562 km', '½ v²/c²', 'd = c·Δt', 'gh/c²', 'Δf/f = −4.4647·10⁻¹⁰'], formulasPerScene: 18 });
</script></body></html>
```
