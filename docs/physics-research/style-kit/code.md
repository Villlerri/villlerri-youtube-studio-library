# Код набора стиля чёрной доски

Исходники, которыми собран принятый ролик-проба. Хранятся текстом: в docs нельзя класть файлы кода. Чтобы запустить, скопируйте каждый блок в файл с указанным именем.

## capture2.mjs

покадровый захват страницы в PNG и MP4.

```js
// Deterministic frame-by-frame capture: the page exposes window.renderFrame(i) (may be async);
// this script screenshots each frame and pipes PNGs into ffmpeg. No real-time clock is used anywhere.
// If the renderer crashes (low memory on a shared host), the browser is relaunched and capture resumes
// at the same frame index into the same ffmpeg process, so the video has no gaps.
// usage: bun tmp/looks/capture.mjs <page.html> <out.mp4> <frames> [--fps 30] [--w 1920] [--h 1080]
//        [--png-dir dir] [--only 0,10,20 (PNG only, no video)] [--max-new N (stop after N new frames, no encode)]
//        [--audio file.wav (muxed as AAC)]
// Pages live under tmp/looks/<id>/ and are served at http://probe.local/<id>/...; /js/ is tmp/probes/js.
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { spawn } from 'node:child_process';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname, extname, join } from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const page_ = resolve(args[0]);
const out = resolve(args[1]);
const N = +args[2];
const fps = +opt('--fps', 30), W = +opt('--w', 1920), H = +opt('--h', 1080);
const pngDir = opt('--png-dir', null);
const only = opt('--only', null);
const FFMPEG = '/home/boardagent/.explainer/bin/ffmpeg';
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const maxNew = +opt('--max-new', 0), audio = opt('--audio', null);
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.bin': 'application/octet-stream', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

let browser, page;
async function open() {
  browser = await chromium.launch({
    executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',
      args: ['--disable-gpu', '--disable-gpu-compositing', '--disable-software-rasterizer',
           '--font-render-hinting=none', '--disable-lcd-text', '--disable-extensions', '--disable-gpu-shader-disk-cache',
           '--renderer-process-limit=1', '--disable-dev-shm-usage', '--js-flags=--max-old-space-size=1024'],
  });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page = await ctx.newPage();
  page.on('console', m => console.error('[page]', m.type(), m.text()));
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  // Serve tmp/probes/* under a fake origin so ES modules and fetch work without a server process.
  await page.route('http://probe.local/**', async route => {
    const p = join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    if (!existsSync(p)) return route.fulfill({ status: 404, body: 'nf' });
    route.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } });
  });
  await page.goto('http://probe.local' + page_.slice(ROOT.length));
  await page.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
  const info = await page.evaluate(() => window.info ? window.info() : null);
  if (info) console.error('[info]', JSON.stringify(info));
}
async function shot(i) {
  await page.evaluate(i => window.renderFrame(i), i);
  return page.screenshot({ type: 'png', animations: 'disabled', caret: 'hide' });
}

for (let a = 0; ; a++) { try { await open(); break; } catch (e) { if (a >= 20) throw e; console.error(`[initial open failed ${a + 1}] ${String(e.message).split('\n')[0]}`); try { await browser.close(); } catch {} await new Promise(r => setTimeout(r, 4000)); } }
if (only) {
  mkdirSync(pngDir, { recursive: true });
  for (const i of only.split(',').map(Number)) {
    const t = Date.now();
    writeFileSync(join(pngDir, `f${String(i).padStart(4, '0')}.png`), await shot(i));
    console.error(`frame ${i} ${(Date.now() - t)} ms`);
  }
  await browser.close(); process.exit(0);
}
// frames go to PNG files first (resumable after a crash), then one ffmpeg encode
const dir = pngDir || out.replace(/\.mp4$/, '_frames');
mkdirSync(dir, { recursive: true });
const CHUNK = +opt('--chunk', 20);   // fresh browser every CHUNK frames keeps renderer memory low on a shared host
const t0 = Date.now();
let restarts = 0, done = 0;
for (let i = 0; i < N; i++) {
  const f = join(dir, `f${String(i).padStart(4, '0')}.png`);
  if (existsSync(f)) continue;
  if (maxNew && done >= maxNew) { try { await browser.close(); } catch {} console.error(`STOPPED after ${done} new frames; run again to continue`); process.exit(3); }
  if (done > 0 && done % CHUNK === 0) { try { await browser.close(); } catch {} await open(); }
  let buf;
  try { buf = await shot(i); }
  catch (e) {
    if (++restarts > 4000) throw e;
    console.error(`[restart ${restarts}] frame ${i}: ${String(e.message).split('\n')[0]}`);
    try { await browser.close(); } catch {}
    await new Promise(r => setTimeout(r, 4000));   // let host memory recover
    for (;;) { try { await open(); break; } catch (e2) { if (++restarts > 4000) throw e2; console.error(`[reopen failed ${restarts}]`); try { await browser.close(); } catch {} await new Promise(r => setTimeout(r, 4000)); } }
    i--; continue;
  }
  writeFileSync(f, buf); done++;
  if (i % 30 === 0) console.error(`frame ${i}/${N} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
const tc = (Date.now() - t0) / 1000;
try { await browser.close(); } catch {}
const t1 = Date.now();
const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', join(dir, 'f%04d.png'),
  ...(audio ? ['-i', resolve(audio), '-c:a', 'aac', '-b:a', '192k', '-shortest'] : []), '-frames:v', String(N),
  '-c:v', 'libx264', '-preset', 'medium', '-threads', '2', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps), '-movflags', '+faststart', out],
  { stdio: ['ignore', 'inherit', 'inherit'] });
const code = await new Promise(r => ff.on('close', r));
const te = (Date.now() - t1) / 1000;
console.error(`DONE frames=${N} rendered_now=${done} capture=${tc.toFixed(1)}s (${(tc / Math.max(done, 1)).toFixed(3)} s/frame) encode=${te.toFixed(1)}s restarts=${restarts} ffmpeg_exit=${code}`);
process.exit(code);
```

## check-clip.mjs

проверка выхода за край и наложений.

```js
// layout check for v1-clip.html: anything leaving the frame, text under a cut-out, text over text
// usage (from tmp/looks): bun styles/check-clip.mjs styles/v1-clip.html
import { chromium } from '../js/node_modules/playwright-core/index.mjs';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join, extname, dirname } from 'node:path';
const ROOT = resolve(dirname(new URL(import.meta.url).pathname), '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.woff2': 'font/woff2', '.ttf': 'font/ttf' };
const browser = await chromium.launch({ executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell', args: ['--disable-gpu'] });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
page.on('pageerror', e => console.error('[pageerror]', e.message));
await page.route('http://probe.local/**', async r => { const p = join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!existsSync(p)) return r.fulfill({ status: 404, body: 'nf' }); r.fulfill({ status: 200, body: readFileSync(p), headers: { 'content-type': MIME[extname(p)] || 'application/octet-stream' } }); });
await page.goto('http://probe.local' + resolve(process.argv[2]).slice(ROOT.length));
await page.waitForFunction(() => window.ready === true);
const res = await page.evaluate(() => {
  const hits = {};
  const vis = n => { for (let e = n; e && e.nodeType === 1; e = e.parentNode) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false; } return true; };
  const note = (k, t) => { const h = hits[k] || (hits[k] = [t, t]); h[1] = t; };
  for (let f = 0; f < 1800; f += 5) {
    window.renderFrame(f); const t = f / 30;
    const items = [];
    for (const n of document.querySelectorAll('.sc .ck, .sc .lab, .sc svg text')) {
      if (!vis(n)) continue; const r = n.getBoundingClientRect(), fs = parseFloat(getComputedStyle(n).fontSize);
      items.push({ id: n.id || n.textContent.slice(0, 20), kind: 'text', l: r.left - .05 * fs, r: r.right + .15 * fs, t: r.top - .2 * fs, b: r.bottom + .25 * fs });
    }
    for (const n of document.querySelectorAll('.sc .cw > img')) { if (!vis(n)) continue; const r = n.getBoundingClientRect(); items.push({ id: n.parentNode.id, kind: 'cut', l: r.left + 15, r: r.right - 15, t: r.top + 15, b: r.bottom - 15 }); }
    for (const n of document.querySelectorAll('.sc svg.draw path, .sc svg.draw line, .sc svg.draw circle')) {
      if (!vis(n) || ['c_earth'].includes(n.id) || n.closest('#ssatm')) continue; const r = n.getBoundingClientRect(); if (!r.width && !r.height) continue;
      items.push({ id: n.id || 'draw', kind: 'draw', l: r.left, r: r.right, t: r.top, b: r.bottom });
    }
    for (const a of items) {
      const busy = a.kind !== 'cut' || t > 0;
      if (a.l < 0 || a.t < 0 || a.r > 1920 || a.b > 1080) note(`EDGE ${a.kind} ${a.id} @${t.toFixed(1)} [${a.l | 0},${a.t | 0},${a.r | 0},${a.b | 0}]`, t);
    }
    for (const a of items) for (const b of items) {
      if (a === b || a.kind !== 'text' || b.kind === 'draw' && true) continue;
      if (b.kind === 'text' && a.id >= b.id) continue;
      const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l), oy = Math.min(a.b, b.b) - Math.max(a.t, b.t);
      if (ox > 4 && oy > 4) note(`OVER ${a.id} x ${b.id} (${ox | 0}x${oy | 0})`, t);
    }
  }
  return hits;
});
for (const [k, [a, b]] of Object.entries(res)) console.log(k, a.toFixed(1), '-', b.toFixed(1));
await browser.close();
```

## clip_sound.py

процедурный звук по событиям кадра.

```python
"""Procedural sound for the chalkboard clip (v1-clip.html). numpy/scipy only, no voice.
Every cue comes from the page's own timeline (clip-events.json), so sound and picture stay in sync."""
import json, os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__))
info = json.load(open(sys.argv[1])); EV = info['events']
SR = 48000; DUR = info['frames'] / info['fps']; n = int(DUR * SR); t = np.arange(n) / SR
rng = np.random.default_rng(20261018)
L = np.zeros(n); R = np.zeros(n)
def add(x, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= n: return
    x = x[:n - i]; L[i:i + len(x)] += x * gain * np.sqrt((1 - pan) / 2) * 1.414; R[i:i + len(x)] += x * gain * np.sqrt((1 + pan) / 2) * 1.414
def env_ad(m, a, d):
    tt = np.arange(m) / SR; return (1 - np.exp(-tt / a)) * np.exp(-tt / d)
def tone(f, dur, a=0.005, d=0.3, harm=(1, .3, .1)):
    m = int(dur * SR); tt = np.arange(m) / SR; return sum(h * np.sin(2 * np.pi * f * (k + 1) * tt) for k, h in enumerate(harm)) * env_ad(m, a, d)
def lp(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def bp(x, f0, f1, o=2): return sosfilt(butter(o, [f0, f1], 'band', fs=SR, output='sos'), x)
def hp(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
N = lambda m: 440 * 2 ** ((m - 69) / 12)
def whoosh(dur, f0, f1, gain=0.3):
    m = int(dur * SR); noise = rng.standard_normal(m); out = np.zeros(m); k = 30; seg = m // k
    for s in range(k):
        fc = f0 * (f1 / f0) ** (s / (k - 1)); a, b = s * seg, ((s + 1) * seg if s < k - 1 else m)
        out[a:b] = bp(noise, max(40, fc * 0.4), min(SR / 2 - 100, fc * 1.6), 2)[a:b]
    out *= np.sin(np.pi * np.linspace(0, 1, m)) ** 2; return out / (np.max(np.abs(out)) + 1e-9) * gain
def scratch(t0, dur, gain=0.17, f0=2200, f1=6500, rate=9):
    """chalk on slate: band noise chopped into strokes"""
    m = int(dur * SR); x = bp(rng.standard_normal(m), f0, f1, 2); tt = np.arange(m) / SR
    ph = np.cumsum(rate * (1 + 0.3 * np.sin(2 * np.pi * 0.7 * tt)) / SR)
    chop = 0.45 + 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * ph)) ** 0.6
    e = np.minimum(1, tt / 0.03) * np.minimum(1, (dur - tt) / 0.05)
    add(x * chop * e * gain, t0, 1.0, rng.uniform(-0.25, 0.25))
def pluck(f, dur=0.7, g=0.2):
    m = int(dur * SR); tt = np.arange(m) / SR
    return (np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.18) + 0.35 * np.sin(2 * np.pi * f * 4 * tt) * np.exp(-tt / 0.04)) * g * (1 - np.exp(-tt / 0.002))
def thud(t0, g=0.32):
    """paper sheet landing on the board"""
    m = int(0.25 * SR); tt = np.arange(m) / SR
    add(np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-tt * 40)) / SR) * np.exp(-tt / 0.06) * g, t0, 1.0)
    add(bp(rng.standard_normal(m), 300, 2500) * env_ad(m, 0.002, 0.03) * g * 0.6, t0, 1.0, 0.2)
def rip(t0, g=0.22):
    """tape pulled and pressed: crackly band noise"""
    m = int(0.32 * SR); x = bp(rng.standard_normal(m), 900, 7000); crack = (rng.random(m) < 0.004).astype(float)
    crack = np.convolve(crack, np.exp(-np.arange(200) / 30), 'same'); e = np.sin(np.pi * np.linspace(0, 1, m)) ** 0.7
    add(x * (0.35 + crack) * e * g, t0, 1.0, 0.3)
def pop(t0, f=300, g=0.3):
    m = int(0.18 * SR); tt = np.arange(m) / SR; ff = f * (1 + 2.2 * np.exp(-tt * 30))
    add(np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-tt / 0.045) * g, t0, 1.0, rng.uniform(-0.3, 0.3))
def boing(t0, g=0.16):
    m = int(0.45 * SR); tt = np.arange(m) / SR
    add(np.sin(2 * np.pi * np.cumsum(330 + 260 * np.exp(-tt * 6) * np.sin(tt * 34)) / SR) * np.exp(-tt / 0.16) * g, t0, 1.0, 0.4)
def rub(t0, dur, g=0.2):
    """felt eraser: low, soft noise in back-and-forth strokes"""
    m = int(dur * SR); tt = np.arange(m) / SR; x = bp(rng.standard_normal(m), 250, 1800)
    strokes = 0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 2.6 * tt)) ** 0.8
    add(x * strokes * np.sin(np.pi * np.linspace(0, 1, m)) ** 0.6 * g, t0, 1.0, -0.1)

# ---- music bed: soft pad and a light pluck motif, one chord set per scene
SCN = [(0, 11.2, [[60, 64, 67, 71], [57, 60, 64, 67]]), (11.2, 30.2, [[62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 70], [53, 57, 60, 64]]),
       (30.2, 50.0, [[57, 60, 64, 67], [53, 57, 60, 65], [55, 59, 62, 65], [52, 55, 60, 64]]), (50.0, DUR, [[53, 57, 60, 64], [55, 59, 62, 67], [60, 64, 67, 72]])]
def pad(freqs, dur, gain):
    m = int((dur + 1.4) * SR); tt = np.arange(m) / SR; x = np.zeros(m)
    for f in freqs:
        for dt in (-0.004, 0.0, 0.005):
            f2 = f * (1 + dt); x += np.sin(2 * np.pi * f2 * tt + rng.random() * 6) + 0.2 * np.sin(4 * np.pi * f2 * tt + rng.random() * 6)
    return lp(x / len(freqs) / 3, 1300) * np.minimum(1, tt / 1.0) * np.minimum(1, (dur + 1.4 - tt) / 1.3) * gain
for a, b, chords in SCN:
    seg = (b - a) / len(chords)
    for i, ch in enumerate(chords):
        ta = a + i * seg; add(pad([N(m - 12) for m in ch], seg, 0.2), ta)
        k, tt = 0, ta + 0.5
        while tt < ta + seg - 0.3:
            add(pluck(N(ch[[0, 2, 1, 3, 2, 1][k % 6]] + 12), 0.8, 0.055), tt, 1.0, ((k % 5) - 2) * 0.2)
            tt += 0.6 if k % 3 == 2 else 0.3 * (2 + (k % 2)); k += 1

# ---- cues from the page timeline
ARROW = [88, 84, 81, 79, 76, 72]   # violet highest, red lowest: higher = bounces more
for e in EV:
    k, t0, d = e['k'], e['t'], e.get('d', 0)
    if k == 'write': scratch(t0 + 0.03, d * 0.95, 0.17)
    elif k == 'draw':
        if e.get('note') is not None: add(tone(N(ARROW[e['note']]), 0.5, 0.002, 0.18, (1, .3)) * 0.12, t0 + d * 0.8, 1.0, -0.4 + 0.15 * e['note']); scratch(t0, d, 0.10, 3000, 7500, 14)
        else: scratch(t0, max(0.12, d), 0.11, 2800, 7000, 12)
    elif k == 'grow': scratch(t0, d, 0.10, 2500, 6000, 6)
    elif k == 'wipe': scratch(t0, d, 0.07, 2500, 6000, 5)
    elif k == 'drop': add(whoosh(0.5, 300, 2600, 0.16), t0 - 0.15, 1.0, 0.3); thud(t0 + 0.32)
    elif k == 'tape': rip(t0 - 0.05)
    elif k == 'wig': boing(t0)
    elif k == 'lift': add(whoosh(0.45, 2000, 400, 0.14), t0, 1.0, 0.4)
    elif k == 'erase': rub(t0 - 0.05, d + 0.2)
    elif k == 'pop': pop(t0, 280)
    elif k == 'count':   # falling glide while blue fades on the long sunset road
        m = int(d * SR); tt = np.arange(m) / SR; f = N(79) * (N(55) / N(79)) ** (tt / d)
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 0.5 * 0.06, t0, 1.0, 0.3)
add(tone(N(48), 3.0, 0.01, 1.2, (1, .5, .25)) * 0.2, 58.2, 1.0)   # closing note

# ---- small room, master fade
imp = rng.standard_normal(int(0.45 * SR)) * np.exp(-np.arange(int(0.45 * SR)) / (0.12 * SR)); imp /= np.sum(np.abs(imp)) / 3
wl = fftconvolve(L, imp)[:n]; wr = fftconvolve(R, imp[::-1])[:n]; L = 0.82 * L + 0.18 * wl; R = 0.82 * R + 0.18 * wr
fade = np.minimum(1, np.minimum(t / 0.05, (DUR - t) / 1.2))
st = np.stack([L * fade, R * fade], 1); st /= np.max(np.abs(st)) * 1.12
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', len(EV), 'cues', DUR, 's')
```

## prep.py

вырезки: контур, рваный край, растр, сгибы.

```python
# Prepare style-frame assets: classical cut-outs (GrabCut, no ML), halftone ink layers, crops.
import cv2, numpy as np, os, sys
sys.path.insert(0, '/srv/projects/youtube-studio-library/worktrees/youtube-work/tmp/looks/chalk/src')
from cutout import grab, clean, save_rgba, load_rgb, fit
D = os.path.join(os.path.dirname(__file__), '..', 'assets')
C, P = D + '/cache/', D + '/p/'

def crop(img, x0, y0, x1, y1):
    h, w = img.shape[:2]; return img[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]

def cut(key, rect, maxside=1600, feather=1.4, erode=3):
    img = fit(load_rgb(C + key + '.jpg'), maxside); h, w = img.shape[:2]
    r = [rect[0]*w, rect[1]*h, rect[2]*w, rect[3]*h]
    a = clean(grab(img, r, iters=8))
    a = cv2.erode(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode*2+1,)*2))
    a = cv2.GaussianBlur(a, (0, 0), feather)
    ys, xs = np.where(a > 8); img, a = img[ys.min():ys.max()+1, xs.min():xs.max()+1], a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    save_rgba(P + key + '_cut.png', np.dstack([img, a])); print(key, img.shape)

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

def ink_png(name, cov, rgb):
    a = (np.clip(cov, 0, 1) * 255).astype(np.uint8); col = np.zeros(cov.shape + (3,), np.uint8); col[:] = rgb
    save_rgba(P + name + '.png', np.dstack([col, a]))

def tone(img, lo=0.05, hi=0.95):
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    return np.clip((g - lo) / (hi - lo), 0, 1)

if __name__ == '__main__':
    what = sys.argv[1:] or ['cuts', 'ht']
    if 'cuts' in what:
        cut('cat_blueeyes', (0.02, 0.0, 0.98, 1.0))
        cut('cat_grumpy', (0.03, 0.04, 0.80, 0.70))
        cut('cat_white', (0.0, 0.0, 0.90, 1.0))
        cut('rayleigh_vf', (0.12, 0.10, 0.98, 0.99))
    if 'ht' in what:
        # riso: screaming tux cat, ink = darkness, pink on black paper -> ink = brightness instead
        img = fit(load_rgb(C + 'cat_yawn_tux.jpg'), 1500); img = crop(img, 0.30, 0.0, 1.0, 0.85)
        ink_png('riso_tux_pink', halftone(tone(img, 0.08, 0.9), cell=9, angle=15, gamma=1.1), (255, 72, 110))
        img = fit(load_rgb(C + 'cat_yawn_ginger.jpg'), 1800); img = crop(img, 0.12, 0.0, 0.88, 1.0)
        ink_png('riso_ginger_pink', halftone(tone(img, 0.1, 0.95), cell=10, angle=15), (255, 72, 110))
        img = fit(load_rgb(C + 'iss_sunset.jpg'), 2200)
        t = tone(img, 0.02, 0.9); hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
        warm = ((hsv[..., 0] < 30) | (hsv[..., 0] > 160)).astype(np.float32) * (hsv[..., 1] / 255)
        ink_png('riso_sunset_yellow', halftone(t * np.clip(warm*1.3, 0, 1), cell=8, angle=75), (255, 214, 0))
        ink_png('riso_sunset_pink', halftone(t * np.clip(1 - warm*0.7, 0, 1), cell=8, angle=15), (255, 72, 110))
        ink_png('riso_sunset_blue', halftone(t * (1 - np.clip(warm*1.3, 0, 1)), cell=8, angle=45), (60, 120, 255))
        # space: cyan halftone of the ISS and the Earth limb
        img = fit(load_rgb(C + 'iss_lastrays.jpg'), 2400)
        ink_png('space_limb_cyan', halftone(tone(img, 0.02, 0.85), cell=6, angle=30), (80, 200, 255))
        img = fit(load_rgb(C + 'iss_station.jpg'), 1800)
        ink_png('space_iss_cyan', halftone(tone(img, 0.05, 0.95), cell=6, angle=30), (80, 200, 255))
        img = fit(load_rgb(C + 'cat_black.jpg'), 1800)
        ink_png('space_cat_cyan', halftone(tone(img, 0.0, 0.55), cell=6, angle=30, gamma=0.9), (80, 200, 255))

POLY = {
    'cat_blueeyes': [(0.10,0.30),(0.17,0.01),(0.38,0.16),(0.62,0.16),(0.86,0.01),(0.94,0.30),(0.98,0.58),(1.0,1.0),(0.0,1.0),(0.02,0.58)],
    'cat_grumpy': [(0.04,0.20),(0.12,0.09),(0.30,0.12),(0.55,0.08),(0.74,0.01),(0.79,0.20),(0.79,0.45),(0.71,0.63),(0.50,0.69),(0.25,0.71),(0.04,0.67),(0.01,0.40)],
    'cat_white': [(0.0,0.24),(0.06,0.01),(0.28,0.09),(0.50,0.07),(0.67,0.0),(0.75,0.20),(0.89,0.45),(0.93,1.0),(0.0,1.0)],
}
def polycut(key, maxside=1700, border=16):
    """scissor cut along a hand-set polygon + white paper margin (magazine cut-out), and a tight GrabCut seeded by it"""
    img = fit(load_rgb(C + key + '.jpg'), maxside); h, w = img.shape[:2]
    pts = np.array([(x*w, y*h) for x, y in POLY[key]], np.int32)
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [pts], 255)
    pad = border + 4
    im2 = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REPLICATE); m2 = cv2.copyMakeBorder(m, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    outer = cv2.dilate(m2, cv2.getStructuringElement(cv2.MORPH_RECT, (border*2+1,)*2))
    col = np.where(m2[..., None] > 0, im2, 246).astype(np.uint8)
    a = cv2.GaussianBlur(outer, (0, 0), 0.8)
    save_rgba(P + key + '_paper.png', np.dstack([col, a]))
    # tight cut
    gm = np.full((h, w), cv2.GC_BGD, np.uint8); gm[m > 0] = cv2.GC_PR_FGD
    inner = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(w*0.12)|1,)*2)); gm[inner > 0] = cv2.GC_FGD
    s = 0.5; gs = cv2.resize(gm, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST); isml = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    bgd = np.zeros((1, 65)); fgd = np.zeros((1, 65)); cv2.grabCut(isml, gs, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
    a = ((gs == 1) | (gs == 3)).astype(np.uint8)*255; a = cv2.resize(a, (w, h), interpolation=cv2.INTER_LINEAR)
    a = clean(a); a = cv2.GaussianBlur(cv2.erode(a, np.ones((5, 5), np.uint8)), (0, 0), 1.5)
    ys, xs = np.where(a > 8)
    save_rgba(P + key + '_tight.png', np.dstack([img, a])[ys.min():ys.max()+1, xs.min():xs.max()+1]); print(key)

if __name__ == '__main__' and 'poly' in sys.argv:
    for k in POLY: polycut(k)
if __name__ == '__main__' and 'space' in sys.argv:
    for src, name, mx, cell, lo, hi in [('iss_lastrays', 'space_limb_cyan', 1920, 5, 0.02, 0.85), ('iss_station', 'space_iss_cyan', 1500, 5, 0.05, 0.95), ('cat_black', 'space_cat_cyan', 1500, 5, 0.0, 0.5)]:
        img = fit(load_rgb(C + src + '.jpg'), mx)
        ink_png(name, halftone(tone(img, lo, hi), cell=cell, angle=30), (80, 200, 255)); print(name)
if __name__ == '__main__' and 'riso2' in sys.argv:
    img = fit(load_rgb(C + 'cat_yawn_tux.jpg'), 1400); img = crop(img, 0.28, 0.0, 1.0, 0.80)
    ink_png('riso_tux_dark', halftone(1 - tone(img, 0.05, 0.85), cell=8, angle=45, gamma=0.9), (20, 16, 18))
    img = fit(load_rgb(C + 'cat_grumpy.jpg'), 1200); img = crop(img, 0.03, 0.02, 0.82, 0.70)
    ink_png('riso_grumpy_pink', halftone(tone(img, 0.15, 0.8), cell=7, angle=15), (255, 72, 110))
    print('ok')

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

if __name__ == '__main__' and 'rough' in sys.argv:
    roughcut('cat_grumpy', POLY['cat_grumpy'], 'cat_grumpy_rough', seed=3, folds=2)
    roughcut('cat_white', POLY['cat_white'], 'cat_white_rough', maxside=1200, border=18, seed=5, folds=1)
    roughcut('cat_blueeyes', POLY['cat_blueeyes'], 'cat_blueeyes_rough', maxside=1100, border=18, seed=8, folds=1)
    roughcut('iss_sunset', [(0, 0), (1, 0), (1, 1), (0, 1)], 'iss_sunset_rough', maxside=2400, border=26, seed=11, folds=1, ht=0.25, crop_box=(0.18, 0.28, 0.82, 0.66))
```

## cutout.py

вырезание по контуру (GrabCut, без ML).

```python
# classical cut-out: GrabCut (+ threshold hints) -> alpha -> white sticker border. No ML.
import cv2, numpy as np, sys, json, os
A=os.path.join(os.path.dirname(__file__),'..','assets')
def grab(img, rect, fg_hint=None, bg_hint=None, iters=6, scale=0.5):
    h,w=img.shape[:2]; s=cv2.resize(img,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
    m=np.full(s.shape[:2],cv2.GC_PR_BGD,np.uint8)
    x0,y0,x1,y1=[int(v*scale) for v in rect]
    m[:]=cv2.GC_BGD; m[y0:y1,x0:x1]=cv2.GC_PR_FGD
    if fg_hint is not None: m[cv2.resize(fg_hint.astype(np.uint8),(s.shape[1],s.shape[0]),interpolation=cv2.INTER_NEAREST)>0]=cv2.GC_FGD
    if bg_hint is not None: m[cv2.resize(bg_hint.astype(np.uint8),(s.shape[1],s.shape[0]),interpolation=cv2.INTER_NEAREST)>0]=cv2.GC_BGD
    bgd=np.zeros((1,65)); fgd=np.zeros((1,65))
    cv2.grabCut(s,m,None,bgd,fgd,iters,cv2.GC_INIT_WITH_MASK)
    a=((m==cv2.GC_FGD)|(m==cv2.GC_PR_FGD)).astype(np.uint8)*255
    a=cv2.resize(a,(w,h),interpolation=cv2.INTER_LINEAR)
    return a
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
```

