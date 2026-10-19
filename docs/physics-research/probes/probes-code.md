# Код проб P1–P5

Код лежит в `tmp/probes/src/`. Проект не хранит файлы кода, поэтому здесь каждый файл целиком. Чтобы запустить, создайте файлы под теми же именами в `tmp/probes/src/`.

## Как перезапустить

Каталоги: `tmp/probes/{src,out,frames,data,media,js,venv}`. Все команды из `tmp/probes/`.

- JS-зависимости (bun): в `js/` стоят `three@0.186.1`, `playwright-core@1.64.1`, `roughjs@4.6.6`, `katex@0.19.0`. Установка: `cd js && bun add three playwright-core roughjs katex`.
- Python: `venv/` с `numpy 2.5.4`, `scipy 1.18.1`, `opencv-python-headless 5.0.0.93`, `colour-science 0.4.7`. Запуск всегда с `-I`.
- Браузер: headless shell из Playwright (Chrome for Testing 156.0.8078.4), путь в `capture.mjs`. WebGL программный: ANGLE + SwiftShader, GPU нет.
- ffmpeg 6.0.1: `/home/boardagent/.explainer/bin/ffmpeg`.

Видео:

- P1: `bun src/capture.mjs src/p1.html out/P1.mp4 300 --png-dir frames/p1`
- P2: `venv/bin/python -I src/p2_compute.py`, затем `bun src/capture.mjs src/p2.html out/P2.mp4 270 --png-dir frames/p2`
- P3: `bun src/capture.mjs src/p3.html out/P3.mp4 240 --png-dir frames/p3`
- P3-sound: `venv/bin/python -I src/p6_sound.py`, затем `ffmpeg -y -i out/P3.mp4 -i data/p6.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/P3-sound.mp4`
- P4: нужен `media/exp65_excerpt_2470s.mp4` (вырезка 41:10–41:46 из оригинала NASA, `-c copy`). Затем `venv/bin/python -I -u src/p4_track.py`, затем `bun src/capture.mjs src/p4.html out/P4.mp4 240 --png-dir frames/p4out`
- P5: `bun src/capture.mjs src/p5.html out/P5.mp4 300 --png-dir frames/p5`

Если Chromium падает ("Target crashed"), `capture.mjs` перезапускает его и продолжает с того же кадра: готовые PNG пропускаются. Если кодирование из bun упало (exit 255), кодируйте вручную: `ffmpeg -y -framerate 30 -i frames/p1/f%04d.png -frames:v 300 -c:v libx264 -preset medium -crf 17 -threads 2 -pix_fmt yuv420p -r 30 -movflags +faststart out/P1.mp4`.

Превью и кадры:

- WebP: `ffmpeg -y -ss START -t 4 -i out/Pn.mp4 -an -vf "setpts=PTS/SPEED,fps=15,scale=960:-1:flags=lanczos" -c:v libwebp_anim -q:v 55 -compression_level 5 -loop 0 Pn.webp` (P1: START 0, SPEED 2.5 и `-t 10`; P2: 4.5; P3: 3.3; P4: 2.0; P5: 1.0; SPEED 1).
- PNG: `ffmpeg -y -i out/Pn.mp4 -vf "select=eq(n\,N)" -frames:v 1 Pn-still.png`. Кадры N: P1 255, P2 262, P3 239, P4 239, P5 299. Для P4 палитра 256 цветов (Pillow quantize), иначе файл больше 1,5 МБ.

## capture.mjs

Общий захват кадров: страница отдаёт renderFrame(i), скрипт снимает PNG и кодирует mp4. Возобновляется после падения Chromium.

````js
// Deterministic frame-by-frame capture: the page exposes window.renderFrame(i) (may be async);
// this script screenshots each frame and pipes PNGs into ffmpeg. No real-time clock is used anywhere.
// If the renderer crashes (low memory on a shared host), the browser is relaunched and capture resumes
// at the same frame index into the same ffmpeg process, so the video has no gaps.
// usage: bun capture.mjs <page.html> <out.mp4> <frames> [--fps 30] [--w 1920] [--h 1080]
//        [--png-dir dir] [--only 0,10,20 (PNG only, no video)]
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
const ROOT = resolve(dirname(page_), '..');           // tmp/probes
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css', '.bin': 'application/octet-stream', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

let browser, page;
async function open() {
  browser = await chromium.launch({
    executablePath: '/home/boardagent/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',
      args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
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

for (let a = 0; ; a++) { try { await open(); break; } catch (e) { if (a >= 20) throw e; console.error(`[initial open failed ${a + 1}] ${String(e.message).split('\n')[0]}`); try { await browser.close(); } catch {} await new Promise(r => setTimeout(r, 15000)); } }
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
  if (done > 0 && done % CHUNK === 0) { try { await browser.close(); } catch {} await open(); }
  let buf;
  try { buf = await shot(i); }
  catch (e) {
    if (++restarts > 40) throw e;
    console.error(`[restart ${restarts}] frame ${i}: ${String(e.message).split('\n')[0]}`);
    try { await browser.close(); } catch {}
    await new Promise(r => setTimeout(r, 15000));   // let host memory recover
    for (;;) { try { await open(); break; } catch (e2) { if (++restarts > 40) throw e2; console.error(`[reopen failed ${restarts}]`); try { await browser.close(); } catch {} await new Promise(r => setTimeout(r, 15000)); } }
    i--; continue;
  }
  writeFileSync(f, buf); done++;
  if (i % 30 === 0) console.error(`frame ${i}/${N} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
const tc = (Date.now() - t0) / 1000;
try { await browser.close(); } catch {}
const t1 = Date.now();
const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', join(dir, 'f%04d.png'), '-frames:v', String(N),
  '-c:v', 'libx264', '-preset', 'medium', '-threads', '2', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps), '-movflags', '+faststart', out],
  { stdio: ['ignore', 'inherit', 'inherit'] });
const code = await new Promise(r => ff.on('close', r));
const te = (Date.now() - t1) / 1000;
console.error(`DONE frames=${N} rendered_now=${done} capture=${tc.toFixed(1)}s (${(tc / Math.max(done, 1)).toFixed(3)} s/frame) encode=${te.toFixed(1)}s restarts=${restarts} ffmpeg_exit=${code}`);
process.exit(code);
````

## common.css

Общая палитра и теги (одна палитра на все пробы).

````css
/* Shared look for all probes: one palette = one meaning across the series. */
:root {
  --bg: #0a0e17;
  --panel: #111827;
  --ink: #e9eef6;
  --ink2: #9ba8bb;
  --ink3: #5d6a7e;
  --blue: #5aa9ff;      /* short wavelengths / scattered blue light */
  --red: #ff6a4d;       /* long wavelengths / transmitted red light */
  --sun: #fff1d6;       /* white sunlight */
  --n2: #c9d3e3;        /* nitrogen */
  --o2: #8fd6b4;        /* oxygen */
  --model: #f5c46a;     /* tag: model / not to scale */
  --exact: #7ee0a1;     /* tag: to scale / computed */
}
html, body { margin: 0; padding: 0; background: var(--bg); width: 1920px; height: 1080px; overflow: hidden; }
body { font-family: 'Lato', sans-serif; color: var(--ink); font-variant-numeric: tabular-nums; -webkit-font-smoothing: antialiased; }
.abs { position: absolute; }
.tag { display: inline-flex; align-items: center; gap: 10px; font-size: 21px; font-weight: 700; letter-spacing: 0.06em;
  text-transform: uppercase; padding: 6px 12px; border-radius: 6px; white-space: nowrap; }
.tag.model { color: var(--model); border: 2px dashed var(--model); background: rgba(245, 196, 106, 0.07); }
.tag.exact { color: var(--exact); border: 2px solid var(--exact); background: rgba(126, 224, 161, 0.07); }
.tag .rest { text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--ink); opacity: 0.9; }
.h1 { font-size: 40px; font-weight: 700; letter-spacing: -0.01em; }
.h2 { font-size: 26px; font-weight: 400; color: var(--ink2); }
.num { font-weight: 700; }
````

## p1.html

P1: 3D-спуск от Земли к молекулам (three.js).

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="/src/common.css">
<style>
  canvas { position: absolute; left: 0; top: 0; }
  .lab { position: absolute; font-size: 27px; white-space: nowrap; color: var(--ink); text-shadow: 0 0 8px rgba(5,7,12,0.9), 0 0 2px rgba(5,7,12,0.9); opacity: 0; }
  .lab small { font-size: 21px; color: var(--ink2); }
  #scale { position: absolute; left: 72px; top: 960px; font-size: 24px; color: var(--ink); text-shadow: 0 0 6px rgba(0,0,0,0.9); }
  #fov { position: absolute; left: 72px; top: 1004px; font-size: 20px; color: var(--ink2); text-shadow: 0 0 6px rgba(0,0,0,0.9); }
  .chip { position: absolute; opacity: 0; }
  .tag { background: rgba(10,14,23,0.8) !important; }
  .lab { background: rgba(10,14,23,0.62); padding: 4px 12px; border-radius: 7px; }
</style></head>
<body>
<canvas id="gl" width="1920" height="1080"></canvas>
<canvas id="ov" width="1920" height="1080"></canvas>
<div id="scale"></div><div id="fov"></div>
<div class="lab" id="lAtm">≈100 km of air<br><small>Earth radius 6,371 km</small></div>
<div class="lab" id="lSun" style="color:#fff1d6">sunlight</div>
<div class="lab" id="lCube0"></div><div class="lab" id="lCube1"></div><div class="lab" id="lCube2"></div><div class="lab" id="lCube3"></div>
<div class="lab" id="lN2" style="color:var(--n2)">N₂</div>
<div class="lab" id="lO2" style="color:var(--o2)">O₂</div>
<div class="lab" id="lWave" style="color:var(--blue)">blue light, λ ≈ 450 nm</div>
<div class="lab" id="lDip"><span style="color:var(--blue)">driven electrons re-radiate</span><br><small>each molecule = a tiny oscillating dipole</small></div>
<div class="chip" id="cScale" style="left:1210px; top:984px;"><span class="tag exact">To scale <span class="rest">Earth and air from a computed render</span></span></div>
<div class="chip" id="cModel" style="left:620px; top:984px;"><span class="tag model">Model <span class="rest">molecules ×250 larger, ~140× sparser · time slowed 5×10¹⁴×</span></span></div>

<script type="importmap">{"imports":{"three":"/js/node_modules/three/build/three.module.js"}}</script>
<script type="module">
import * as THREE from 'three';
const FPS = 30, NF = 300;
// ---------------------------------------------------------------- physical constants (km)
const R = 6371, HTOP = 100, HS = 8.0, hL = 2.0;           // Earth radius, top of air for the render, scale height, target altitude
const RA = R + HTOP;
const BETA = [5.802e-3, 13.558e-3, 33.1e-3];              // Rayleigh scattering at sea level, 1/km, for 680/550/440 nm
const Lp = [0, R + hL, 0];                                // target point in the air
const nrm = v => { const l = Math.hypot(...v); return v.map(x => x / l); };
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const add = (a, b) => a.map((x, i) => x + b[i]), sub = (a, b) => a.map((x, i) => x - b[i]), mul = (a, k) => a.map(x => x * k);
const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const SUN = nrm([-1, 0.3, 0.25]);                         // direction to the sun (16 deg above the horizon at the target)
const VF = 30, TV = Math.tan(VF / 2 * Math.PI / 180), TH = TV * 16 / 9;   // vertical fov 30 deg

// ---------------------------------------------------------------- camera path (deterministic in t)
const cl = x => Math.max(0, Math.min(1, x));
const sm = x => { x = cl(x); return x * x * x * (x * (6 * x - 15) + 10); };
const outq = x => { x = cl(x); const a = x * x; return 1 - Math.pow(1 - a, 3); };   // ease in, long ease out
const Z0 = Math.log10(30200), Z1 = 2.86, Z2 = Math.log10(2.8e-9), Z3 = Math.log10(2.55e-9);
function zAt(t) {                                          // log10(field of view at the target, km)
  if (t < 0.4) return Z0;
  if (t < 4.3) return Z0 + (Z1 - Z0) * outq((t - 0.4) / 3.9);
  if (t < 7.3) return Z1 + (Z2 - Z1) * sm((t - 4.3) / 3.0);
  return Z2 + (Z3 - Z2) * sm((t - 7.3) / 2.7);
}
function camAt(t) {
  const W = Math.pow(10, zAt(t)), d = W / (2 * TH);
  const sl = sm((t - 0.4) / 2.4);                          // look-at slides from Earth's centre to the target
  const A = mul(Lp, sl);
  const phi = 14 * Math.PI / 180 * sm((t - 7.0) / 3.0);   // slow orbit at the end: parallax shows depth
  const back = [Math.sin(phi), 0, Math.cos(phi)];
  const pos = add(A, mul(back, d));
  const fwd = mul(back, -1), right = nrm(crs(fwd, [0, 1, 0])), up = crs(right, fwd);
  return { W, d, pos, rel: sub(pos, Lp), fwd, right, up, A };
}
// world point (km, double) -> camera space normalised by d (three.js camera at origin looking -z)
function toCam(c, p) { const q = sub(p, c.pos); return [dot(q, c.right) / c.d, dot(q, c.up) / c.d, -dot(q, c.fwd) / c.d]; }
// camera-relative offset given relative to the target point L, in km (keeps precision at micro scale)
function relToCam(c, m) { const q = sub(m, c.rel); return [dot(q, c.right) / c.d, dot(q, c.up) / c.d, -dot(q, c.fwd) / c.d]; }
function proj(p) { if (p[2] > -1e-6) return null; return [960 + 960 * (p[0] / -p[2]) / TH, 540 - 540 * (p[1] / -p[2]) / TV]; }

// ---------------------------------------------------------------- renderer
const gl = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true });
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;   // shaders write display-encoded values themselves
renderer.autoClear = false;

// transmittance LUT: optical depth (in units of sea-level air km) from altitude h toward cos-zenith mu
const LW = 256, LH = 256, lut = new Float32Array(LW * LH);
for (let j = 0; j < LH; j++) {
  const mu = -0.3 + 1.3 * j / (LH - 1);
  for (let i = 0; i < LW; i++) {
    const h = HTOP * Math.pow(i / (LW - 1), 2), r = R + h;
    const disc = r * r * (mu * mu - 1) + R * R;
    let od;
    if (mu < 0 && disc >= 0) od = 1e4;                     // ray hits the ground: no direct sun
    else {
      const tt = -r * mu + Math.sqrt(r * r * (mu * mu - 1) + RA * RA), n = 300; od = 0;
      for (let k = 0; k < n; k++) { const s = (k + 0.5) / n * tt; const rr = Math.sqrt(r * r + s * s + 2 * r * mu * s); od += Math.exp(-(rr - R) / HS) * tt / n; }
    }
    lut[j * LW + i] = od;
  }
}
const lutTex = new THREE.DataTexture(lut, LW, LH, THREE.RedFormat, THREE.FloatType);
lutTex.minFilter = lutTex.magFilter = THREE.LinearFilter; lutTex.needsUpdate = true;

const skyMat = new THREE.ShaderMaterial({
  uniforms: { uRel: { value: new THREE.Vector3() }, uL: { value: new THREE.Vector3(...Lp) }, uRt: { value: new THREE.Vector3() },
    uUp: { value: new THREE.Vector3() }, uFw: { value: new THREE.Vector3() }, uSun: { value: new THREE.Vector3(...SUN) },
    uKE: { value: hL * (2 * R + hL) }, uKA: { value: (hL - HTOP) * (2 * R + hL + HTOP) }, uLut: { value: lutTex },
    uDark: { value: 0 }, uExp: { value: 1.0 }, uTan: { value: new THREE.Vector2(TH, TV) } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`,
  fragmentShader: `
    precision highp float;
    varying vec2 vUv;
    uniform vec3 uRel, uL, uRt, uUp, uFw, uSun; uniform float uKE, uKA, uDark, uExp; uniform vec2 uTan; uniform sampler2D uLut;
    const float R = ${R.toFixed(1)}, HT = ${HTOP.toFixed(1)}, HS = ${HS.toFixed(2)};
    const vec3 BETA = vec3(${BETA.join(',')});
    // altitude of point p given relative to the target L, without large cancellations
    float alt(vec3 p, out float rad){ float r2m = dot(p,p) + 2.0*dot(p,uL) + uKE; rad = sqrt(r2m + R*R); return r2m / (rad + R); }
    float od(float h, float mu){ return texture2D(uLut, vec2(sqrt(clamp(h/HT,0.0,1.0)), (mu + 0.3)/1.3)).r; }
    float hash(vec3 p){ p = fract(p*0.3183099 + .1); p *= 17.0; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
    float noise(vec3 x){ vec3 i = floor(x), f = fract(x); f = f*f*(3.0-2.0*f);
      return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x), mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
                 mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x), mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z); }
    float fbm(vec3 p){ float a = 0.5, s = 0.0; for (int k = 0; k < 5; k++){ s += a*noise(p); p *= 2.03; a *= 0.5; } return s; }
    void main(){
      vec2 ndc = vUv*2.0 - 1.0;
      vec3 d = normalize(uFw + ndc.x*uTan.x*uRt + ndc.y*uTan.y*uUp);
      vec3 o = uRel;
      float B = dot(d,o) + dot(d,uL);
      float oo = dot(o,o) + 2.0*dot(o,uL);
      float CA = oo + uKA, CE = oo + uKE;
      float dA = B*B - CA, dE = B*B - CE;
      vec3 col = vec3(0.0); vec3 Tv = vec3(1.0);
      float tG = -1.0;
      if (dE > 0.0) { float t0 = -B - sqrt(dE); if (t0 > 0.0) tG = t0; }
      if (dA > 0.0) {
        float ta = max(0.0, -B - sqrt(dA)), tb = -B + sqrt(dA);
        if (tG > 0.0) tb = min(tb, tG);
        if (tb > ta) {
          const int N = 24; float ds = (tb - ta)/float(N);
          float cth = dot(d, uSun); float ph = 0.0596831*(1.0 + cth*cth);   // 3/(16 pi)(1+cos^2)
          for (int k = 0; k < N; k++){
            vec3 p = o + d*(ta + (float(k)+0.5)*ds);
            float rad; float h = alt(p, rad);
            float rho = exp(-h/HS);
            vec3 tau = BETA*rho*ds;
            float mu = (dot(p,uSun) + dot(uL,uSun))/rad;
            vec3 Ts = exp(-BETA*od(max(h,0.0), mu));
            col += Tv * Ts * BETA*rho*ph*ds;
            Tv *= exp(-tau);
          }
        }
      }
      if (tG > 0.0) {
        vec3 p = o + d*tG; vec3 n = normalize(p + uL);
        float mu = dot(n, uSun);
        vec3 Ts = exp(-BETA*od(0.0, mu));
        // stylised surface: ocean, a little land, clouds (procedural; kept clear near the target)
        float far = smoothstep(0.004, 0.03, length(n - normalize(uL)));
        float land = smoothstep(0.60, 0.64, fbm(n*3.2 + 1.7)) * far;
        float cloud = smoothstep(0.52, 0.72, fbm(n*7.0 + vec3(4.1,0.3,2.2))) * far;
        vec3 alb = mix(vec3(0.008, 0.022, 0.050), vec3(0.085, 0.072, 0.040), land);
        alb = mix(alb, vec3(0.50), cloud*0.8);
        col += Tv * alb * Ts * max(mu, 0.0) * 0.318 + Tv*alb*0.004;
      }
      vec3 c = 1.0 - exp(-col * uExp * 11.0);
      c = mix(c, vec3(0.0), 0.0);
      vec3 enc = mix(c*12.92, 1.055*pow(c, vec3(1.0/2.4)) - 0.055, step(0.0031308, c));
      vec3 bg = vec3(0.039, 0.055, 0.090);
      enc = max(enc, bg*(1.0 - smoothstep(0.0, 0.08, c.b + c.g)));     // space = the series background colour
      gl_FragColor = vec4(mix(enc, bg, uDark), 1.0);
    }`,
  depthTest: false, depthWrite: false,
});
const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), skyMat);
const skyScene = new THREE.Scene(); skyScene.add(quad);
const orthoCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

// ---------------------------------------------------------------- micro scene (camera space, units of d)
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(VF, 16 / 9, 0.003, 3000);
let seed = 20261016; const rnd = () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const UM = 1e-9;                                          // 1 micrometre in km
const NM = 6500, RA_UM = 0.032, SEP_UM = 0.040, CLOUD_UM = 0.075, EDISP_UM = 0.03;
const mols = [];
for (let k = 0; k < NM; k++) {
  const p = [(rnd() - 0.5) * 20, (rnd() - 0.5) * 12, -9.5 + rnd() * 10.5];   // um, around the target
  const ax = nrm([rnd() - 0.5, rnd() - 0.5, rnd() - 0.5]);
  mols.push({ p, ax, o2: rnd() < 0.21 });
}
const LAM = 0.45, AMP = 0.08, T_OSC = 0.8;                // wave: 450 nm, drawn amplitude 0.16 um, period on screen 0.8 s
const PROP = mul(SUN, -1);                                // light travels away from the sun
const EP = nrm(crs([0, 0, 1], PROP));                    // field direction: perpendicular to travel and to the view axis
// distance past the target where the drawn sunbeam meets the ground: |L + u PROP| = R
const GROUND = (() => { const b = dot(Lp, PROP), cc = dot(Lp, Lp) - R * R; return -b - Math.sqrt(b * b - cc); })();
const phaseAt = (p, t) => 2 * Math.PI * (dot(p, PROP) / LAM - t / T_OSC);
// sphere impostors for atoms
const atomGeo = new THREE.InstancedBufferGeometry();
atomGeo.setAttribute('position', new THREE.Float32BufferAttribute([-1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 1, 0], 3));
atomGeo.setIndex([0, 1, 2, 0, 2, 3]);
const NA = NM * 2;
const aPos = new THREE.InstancedBufferAttribute(new Float32Array(NA * 3), 3); aPos.setUsage(THREE.DynamicDrawUsage);
const aCol = new THREE.InstancedBufferAttribute(new Float32Array(NA * 4), 4); aCol.setUsage(THREE.DynamicDrawUsage);
atomGeo.setAttribute('iPos', aPos); atomGeo.setAttribute('iCol', aCol); atomGeo.instanceCount = NA;
const atomMat = new THREE.ShaderMaterial({
  uniforms: { uRad: { value: 0 }, uLight: { value: new THREE.Vector3() } },
  vertexShader: `attribute vec3 iPos; attribute vec4 iCol; uniform float uRad; varying vec2 vQ; varying vec4 vC;
    void main(){ vQ = position.xy; vC = iCol; vec4 mv = vec4(iPos + vec3(position.xy*uRad, 0.0), 1.0); gl_Position = projectionMatrix * mv; }`,
  fragmentShader: `uniform vec3 uLight; varying vec2 vQ; varying vec4 vC;
    void main(){ float r2 = dot(vQ,vQ); if (r2 > 1.0 || vC.a < 0.003) discard; vec3 n = vec3(vQ, sqrt(1.0-r2));
      float l = 0.28 + 0.72*max(dot(n, uLight), 0.0); float rim = pow(1.0 - n.z, 3.0)*0.35;
      vec3 c = vC.rgb*l + rim; gl_FragColor = vec4(c, vC.a); }`,
  transparent: true, depthWrite: true,
});
const atoms = new THREE.Mesh(atomGeo, atomMat); atoms.frustumCulled = false; scene.add(atoms);
// electron clouds (additive glow), offset along the field
const cloudGeo = new THREE.InstancedBufferGeometry(); cloudGeo.copy(atomGeo); cloudGeo.instanceCount = NM;
const cPos = new THREE.InstancedBufferAttribute(new Float32Array(NM * 3), 3); cPos.setUsage(THREE.DynamicDrawUsage);
const cA = new THREE.InstancedBufferAttribute(new Float32Array(NM * 4), 4); cA.setUsage(THREE.DynamicDrawUsage);
cloudGeo.setAttribute('iPos', cPos); cloudGeo.setAttribute('iCol', cA);
const cloudMat = new THREE.ShaderMaterial({
  uniforms: { uRad: { value: 0 } },
  vertexShader: atomMat.vertexShader,
  fragmentShader: `varying vec2 vQ; varying vec4 vC; void main(){ float r2 = dot(vQ,vQ); if (r2 > 1.0) discard; float g = exp(-r2*3.0)*(1.0-r2); gl_FragColor = vec4(vC.rgb*g*vC.a, 1.0); }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
const clouds = new THREE.Mesh(cloudGeo, cloudMat); clouds.frustumCulled = false; clouds.renderOrder = 2; scene.add(clouds);
// re-radiated wavelets: rings with a dipole pattern (no emission along the oscillation axis)
const NR = 40;
const ringGeo = new THREE.InstancedBufferGeometry(); ringGeo.copy(atomGeo); ringGeo.instanceCount = NR;
const rPos = new THREE.InstancedBufferAttribute(new Float32Array(NR * 3), 3); rPos.setUsage(THREE.DynamicDrawUsage);
const rA = new THREE.InstancedBufferAttribute(new Float32Array(NR * 4), 4); rA.setUsage(THREE.DynamicDrawUsage);
ringGeo.setAttribute('iPos', rPos); ringGeo.setAttribute('iCol', rA);
const ringMat = new THREE.ShaderMaterial({
  uniforms: { uAx: { value: new THREE.Vector2(0, 1) } },
  vertexShader: `attribute vec3 iPos; attribute vec4 iCol; varying vec2 vQ; varying vec4 vC;
    void main(){ vQ = position.xy; vC = iCol; vec4 mv = vec4(iPos + vec3(position.xy*iCol.x, 0.0), 1.0); gl_Position = projectionMatrix * mv; }`,
  fragmentShader: `uniform vec2 uAx; varying vec2 vQ; varying vec4 vC;
    void main(){ float r = length(vQ); float w = vC.y; float e = exp(-pow((r - (1.0 - w))/w, 2.0)*2.0);
      vec2 dir = vQ/max(r,1e-4); float s = 1.0 - pow(dot(dir, uAx), 2.0);
      gl_FragColor = vec4(vec3(0.353,0.663,1.0)*e*s*vC.z, 1.0); }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
const rings = new THREE.Mesh(ringGeo, ringMat); rings.frustumCulled = false; rings.renderOrder = 3; scene.add(rings);
// the light ray / wave: a triangle strip of constant pixel width, rebuilt every frame
const NW = 2400;
const wGeo = new THREE.BufferGeometry();
const wPosA = new THREE.Float32BufferAttribute(new Float32Array(NW * 2 * 3), 3); wPosA.setUsage(THREE.DynamicDrawUsage);
const wIdx = []; for (let k = 0; k < NW - 1; k++) { const a = 2 * k; wIdx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
wGeo.setAttribute('position', wPosA); wGeo.setIndex(wIdx);
const wMat = new THREE.ShaderMaterial({ uniforms: { uC: { value: new THREE.Vector4(1, 0.95, 0.84, 1) } },
  vertexShader: `void main(){ gl_Position = projectionMatrix * vec4(position, 1.0); }`,
  fragmentShader: `uniform vec4 uC; void main(){ gl_FragColor = vec4(uC.rgb, uC.a); }`, transparent: true, depthWrite: false, side: THREE.DoubleSide });
const wave = new THREE.Mesh(wGeo, wMat); wave.frustumCulled = false; wave.renderOrder = 1; scene.add(wave);

// emitters: molecules closest to the drawn ray near the target
const emit = mols.map((m, k) => { const u = dot(m.p, PROP); const perp = sub(m.p, mul(PROP, u)); return { k, u, dist: Math.hypot(...perp) }; })
  .filter(e => Math.abs(e.u) < 2.2 && e.dist < 0.9 && mols[e.k].p[2] > -2.5).sort((a, b) => a.dist - b.dist).slice(0, 3);
// labelled molecules: one N2 and one O2 in front of the target
const pickLabel = o2 => mols.map((m, k) => ({ k, m })).filter(e => e.m.o2 === o2 && e.m.p[2] > -0.6 && e.m.p[2] < 0.4 && Math.abs(e.m.p[1]) < 0.9 && e.m.p[0] > (o2 ? 0.3 : -2.2) && e.m.p[0] < (o2 ? 2.0 : -0.6)).sort((a, b) => Math.abs(a.m.p[1] - 0.45) - Math.abs(b.m.p[1] - 0.45))[0];
const lblN2 = pickLabel(false), lblO2 = pickLabel(true);

// ---------------------------------------------------------------- overlay helpers
const ov = document.getElementById('ov'), g = ov.getContext('2d');
const $ = id => document.getElementById(id);
function place(id, xy, a, dx = 0, dy = 0) { const el = $(id); if (!xy || a <= 0.002) { el.style.opacity = 0; return; } el.style.opacity = a;
  const w = el.offsetWidth || 200; el.style.left = Math.min(Math.max(xy[0] + dx, 24), 1896 - w) + 'px'; el.style.top = Math.min(Math.max(xy[1] + dy, 24), 900) + 'px'; }
function fmtLen(km) {
  const m = km * 1000;
  if (m >= 1000) return `${(m / 1000).toLocaleString('en-US')} km`; if (m >= 1) return `${m} m`;
  if (m >= 1e-3) return `${+(m * 1e3).toPrecision(3)} mm`; if (m >= 1e-6) return `${+(m * 1e6).toPrecision(3)} µm`; return `${+(m * 1e9).toPrecision(3)} nm`;
}
function niceLen(W) {                                     // a 1-2-5 length that is 7-17 % of the frame width
  const target = W * 0.12, e = Math.floor(Math.log10(target)), b = target / Math.pow(10, e);
  const m = b < 1.5 ? 1 : b < 3.5 ? 2 : b < 7.5 ? 5 : 10; return m * Math.pow(10, e);
}
const CUBES = [{ a: 1, txt: '1 km of air' }, { a: 1e-3, txt: '1 m: 2×10²⁵ molecules' }, { a: 1e-6, txt: '1 mm: 2×10¹⁶ molecules' }, { a: 1e-9, txt: '1 µm: 2×10⁷ molecules in real air' }];
const cubeRot = (() => { const a = 0.45, b = 0.3; return p => { let [x, y, z] = p; [x, z] = [x * Math.cos(a) - z * Math.sin(a), x * Math.sin(a) + z * Math.cos(a)]; [y, z] = [y * Math.cos(b) - z * Math.sin(b), y * Math.sin(b) + z * Math.cos(b)]; return [x, y, z]; }; })();

function drawSeg(c, A, B) {                                // camera-space segment clipped at the near plane
  const zn = -0.02; let a = A, b = B;
  if (a[2] > zn && b[2] > zn) return;
  if (a[2] > zn) { const t = (zn - b[2]) / (a[2] - b[2]); a = add(b, mul(sub(a, b), t)); }
  if (b[2] > zn) { const t = (zn - a[2]) / (b[2] - a[2]); b = add(a, mul(sub(b, a), t)); }
  const p = proj(a), q = proj(b); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
}

// ---------------------------------------------------------------- frame
window.renderFrame = (i) => {
  const t = i / FPS, c = camAt(t), W = c.W, lw = Math.log10(W);
  // ---- sky / Earth pass (camera relative to the target, km). Inside the air below ~0.5 km the view no longer changes.
  const relS = c.d > 0.5 ? c.rel : mul(c.rel, 0.5 / c.d);
  const U = skyMat.uniforms;
  U.uRel.value.set(...relS); U.uRt.value.set(...c.right); U.uUp.value.set(...c.up); U.uFw.value.set(...c.fwd);
  const dark = sm((-lw - 7.7) / 0.7);                      // W from ~20 um to ~4 um: darken the sky behind the model
  U.uDark.value = 0.86 * dark;
  renderer.setRenderTarget(null); renderer.clear(); renderer.render(skyScene, orthoCam);

  // ---- micro scene
  const micro = sm((-lw - 7.7) / 0.5);                     // molecules appear from W ~ 20 um
  const um = UM;
  const light = toCamDir(c, SUN);
  atomMat.uniforms.uLight.value.set(...light);
  atomMat.uniforms.uRad.value = RA_UM * um / c.d;
  cloudMat.uniforms.uRad.value = CLOUD_UM * um / c.d;
  const tw = Math.max(0, t - 5.0);                         // wave clock (only visible at the micro end)
  const epc = toCamDir(c, EP);
  for (let k = 0; k < NM; k++) {
    const m = mols[k];
    const pc = relToCam(c, mul(m.p, um));
    const depth = -pc[2] * c.d / um;                       // distance from camera in um
    const fade = micro * cl(1.25 - depth / 9.0) * cl((depth - 0.35) / 0.4);
    const col = m.o2 ? [0.561, 0.839, 0.706] : [0.788, 0.827, 0.890];
    for (let s = 0; s < 2; s++) {
      const off = mul(m.ax, (s ? 0.5 : -0.5) * SEP_UM);
      const pa = relToCam(c, mul(add(m.p, off), um));
      aPos.array.set(pa, (2 * k + s) * 3); aCol.array.set([...col, fade], (2 * k + s) * 4);
    }
    const E = Math.cos(phaseAt(m.p, tw));
    const pcl = relToCam(c, mul(add(m.p, mul(EP, EDISP_UM * E)), um));
    cPos.array.set(pcl, k * 3); cA.array.set([0.35, 0.66, 1.0, 0.38 * fade], k * 4);
  }
  aPos.needsUpdate = aCol.needsUpdate = cPos.needsUpdate = cA.needsUpdate = true;
  // rings
  let ri = 0;
  for (const e of emit) {
    const m = mols[e.k];
    // emission starts when the drawn crest first reaches this molecule, one ring per period
    const t0 = (dot(m.p, PROP) / LAM) * T_OSC;            // phase 0 at tw = t0 (mod period)
    for (let j = 0; j < 3 && ri < NR; j++) {
      const te = t0 + T_OSC * (Math.ceil((2.6 - t0) / T_OSC) + j);   // first emission after tw = 2.6 s
      const age = tw - te; const pc = relToCam(c, mul(m.p, um));
      if (age <= 0) { rA.array.set([0, 0.1, 0, 0], ri * 4); ri++; continue; }
      const rad = age * LAM / T_OSC;                       // wavelets travel one wavelength per period
      const a = micro * cl(age / 0.25) * cl(1 - rad / 1.7) * 0.75;
      const radPx = rad * um / W * 1920;
      rPos.array.set(pc, ri * 3); rA.array.set([rad * um / c.d, Math.min(0.5, 3.0 / Math.max(radPx, 1)), a, 0], ri * 4); ri++;
    }
  }
  for (; ri < NR; ri++) rA.array.set([0, 0.1, 0, 0], ri * 4);
  rPos.needsUpdate = rA.needsUpdate = true;
  ringMat.uniforms.uAx.value.set(epc[0], epc[1]).normalize();

  // ---- the ray / wave
  const lamPx = LAM * um / W * 1920;                       // wavelength in pixels
  const resolv = sm((lamPx - 6) / 30);
  const ampKm = AMP * um * resolv;
  const rayA = sm((t - 2.7) / 0.8);
  const U2 = 30 * c.d;
  const pxPerD = 540 / TV;                                 // pixels per unit at depth 1 (normalised camera space)
  const hw = 1.6 + 1.2 * resolv;                           // half width in px
  const ground = GROUND;                                   // km past the target where the ray meets the ground
  for (let k = 0; k < NW; k++) {
    const v = -1 + 2 * k / (NW - 1);
    let u = U2 * Math.sign(v) * Math.pow(Math.abs(v), 3);
    u = Math.min(u, ground);
    const reveal = -U2 + (U2 + ground) * 1.0;
    const uu = rayA < 1 ? Math.min(u, -U2 + (U2 + 2 * c.d) * rayA) : u;
    const ph = 2 * Math.PI * (uu / (LAM * um) - tw / T_OSC);
    const pk = add(mul(PROP, uu), mul(EP, ampKm * Math.sin(ph)));
    const pc = relToCam(c, pk);
    // tangent for the width offset
    const uu2 = uu + Math.max(Math.abs(uu) * 1e-4, LAM * um * 0.01);
    const pk2 = add(mul(PROP, uu2), mul(EP, ampKm * Math.sin(2 * Math.PI * (uu2 / (LAM * um) - tw / T_OSC))));
    const pc2 = relToCam(c, pk2);
    const z = Math.min(pc[2], -1e-4);
    const sx = pc2[0] / Math.min(pc2[2], -1e-4) - pc[0] / z, sy = pc2[1] / Math.min(pc2[2], -1e-4) - pc[1] / z;
    const ln = Math.hypot(sx, sy) || 1; const nx = -sy / ln, ny = sx / ln;
    const off = hw / pxPerD * (-z);
    wPosA.array.set([pc[0] + nx * off, pc[1] + ny * off, pc[2], pc[0] - nx * off, pc[1] - ny * off, pc[2]], k * 6);
  }
  wPosA.needsUpdate = true;
  const wc = [1 + (0.353 - 1) * resolv, 0.945 + (0.663 - 0.945) * resolv, 0.84 + (1.0 - 0.84) * resolv];
  wMat.uniforms.uC.value.set(...wc, 0.92 * rayA);
  renderer.render(scene, cam);

  // ---- overlay: target marker, atmosphere bracket, cubes, scale bar, labels
  g.clearRect(0, 0, 1920, 1080);
  const pL = proj(toCam(c, Lp));
  // target marker before the dive starts
  const mk = sm((t - 0.3) / 0.5) * (1 - sm((t - 2.6) / 0.5));
  if (pL && mk > 0) { g.strokeStyle = `rgba(233,238,246,${0.85 * mk})`; g.lineWidth = 2; g.beginPath(); g.arc(pL[0], pL[1], 16 + 6 * (1 - mk), 0, 7); g.stroke(); }
  // bracket: ground to 100 km on the limb, drawn from the projected 3D points (to scale)
  const br = sm((t - 2.9) / 0.6) * (1 - sm((t - 4.3) / 0.4));
  const pG = proj(toCam(c, [0, R, 0])), pT = proj(toCam(c, [0, R + 100, 0]));
  if (pG && pT && br > 0) {
    const x = pG[0] + 70; g.strokeStyle = `rgba(126,224,161,${br})`; g.lineWidth = 3; g.beginPath();
    g.moveTo(x - 14, pG[1]); g.lineTo(x, pG[1]); g.lineTo(x, pT[1]); g.lineTo(x - 14, pT[1]); g.stroke();
    place('lAtm', [x + 18, (pG[1] + pT[1]) / 2 - 36], br);
  } else place('lAtm', null, 0);
  $('cScale').style.opacity = br;
  // nested cubes of air with molecule counts (sea-level-like density at 2 km: ~2x10^25 per m^3)
  CUBES.forEach((cb, k) => {
    const rel = Math.log10(cb.a / W);                       // cube size relative to the frame
    const a = sm((rel + 1.3) / 0.35) * (1 - sm((rel + 0.55) / 0.25)) * (t > 4.0 ? 1 : 0) * (k === 3 ? 1 - sm((micro - 0.3) / 0.5) : 1);
    const id = 'lCube' + k;
    if (a <= 0.01) { place(id, null, 0); return; }
    const h = cb.a / 2; const V = [];
    for (const sx of [-1, 1]) for (const sy of [-1, 1]) for (const sz of [-1, 1]) V.push(relToCam(c, cubeRot([sx * h, sy * h, sz * h])));
    g.strokeStyle = `rgba(233,238,246,${0.75 * a})`; g.lineWidth = 2; g.beginPath();
    for (const [p, q] of [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]]) drawSeg(g, V[p], V[q]);
    g.stroke();
    const pts = V.filter(v => v[2] < -0.02).map(proj); if (!pts.length) { place(id, null, 0); return; }
    const top = pts.reduce((m, p) => p[1] < m[1] ? p : m, pts[0]);
    $(id).textContent = cb.txt; place(id, [Math.min(Math.max(top[0], 20), 1400), Math.max(top[1], 60)], a, 12, -42);
  });
  // scale bar
  const Lb = niceLen(W), px = Lb / W * 1920;
  g.fillStyle = 'rgba(10,14,23,0.6)'; g.beginPath(); g.roundRect(56, 914, Math.max(px, 210) + 34, 122, 10); g.fill();
  g.strokeStyle = 'rgba(233,238,246,0.95)'; g.lineWidth = 3; g.beginPath();
  g.moveTo(72, 940); g.lineTo(72 + px, 940); g.moveTo(72, 930); g.lineTo(72, 950); g.moveTo(72 + px, 930); g.lineTo(72 + px, 950); g.stroke();
  $('scale').textContent = fmtLen(Lb);
  $('fov').textContent = 'frame width ' + fmtLen(+W.toPrecision(2));
  // labels on the ray and the molecules
  const sunPt = proj(relToCam(c, mul(PROP, -0.55 * c.d)));
  place('lSun', sunPt, rayA * (1 - sm((t - 4.4) / 0.4)), 10, -46);
  const mlab = sm((t - 7.4) / 0.5);
  const wavePt = proj(relToCam(c, mul(PROP, -0.9 * um)));
  place('lWave', wavePt ? [Math.max(wavePt[0], 40), Math.max(wavePt[1], 70)] : null, mlab * resolv, -20, -100);
  if (lblN2) place('lN2', proj(relToCam(c, mul(lblN2.m.p, um))), mlab, 18, -50);
  if (lblO2) place('lO2', proj(relToCam(c, mul(lblO2.m.p, um))), mlab, 18, -50);
  const e0 = emit[0] ? proj(relToCam(c, mul(mols[emit[0].k].p, um))) : null;
  place('lDip', e0 ? [Math.min(Math.max(e0[0], 40), 1380), Math.min(Math.max(e0[1], 80), 800)] : null, sm((t - 8.0) / 0.5), 40, 60);
  $('cModel').style.opacity = mlab;
};
function toCamDir(c, v) { return [dot(v, c.right), dot(v, c.up), -dot(v, c.fwd)]; }
window.info = () => ({ frames: NF, emitters: emit.length, n2: !!lblN2, o2: !!lblO2 });
window.ready = true;
</script>
</body></html>
````

## p2_compute.py

P2, шаг 1: расчёт цвета неба и спектров (numpy, colour-science) в data/p2.json.

````python
"""P2 compute step: clear-sky Rayleigh model of a sunset.

Inputs (all in code, no fitting):
  * Sun above the air: Planck blackbody at 5772 K (an approximation of the solar spectrum).
  * Rayleigh optical depth of the whole air column: tau(lambda) = 0.0088 * lambda_um**-4.05.
  * Relative air mass: Kasten & Young (1989), m = 1 / (cos z + 0.50572 * (96.07995 - z_deg)**-1.6364).
  * Direct sun at the ground: S * exp(-tau * m_sun).
  * Sky radiance, single scattering, plane-parallel column, observer on the ground:
      L = S * P(theta)/(4 pi) * m_v * exp(-tau m_v) * (1 - exp(-tau (m_s - m_v))) / (m_s - m_v),
    P = 3/4 (1 + cos^2 theta). P does not depend on wavelength, so the sky colour for a pixel is
    P(theta) * LUT(view zenith) and the LUT is all the page needs.
  * Colour: CIE 1931 2-degree colour matching functions (colour-science tables), XYZ -> linear sRGB (D65),
    out-of-gamut colours are desaturated toward their own luminance (no hue shift), then sRGB encoding.
Output: tmp/probes/data/p2.json (per frame) and a printed table of sRGB values.
"""
import json, math, sys, os
import numpy as np
import colour

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'p2.json')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

FPS, NF = 30, 270
lam = np.arange(380, 781, 5).astype(float)              # nm, 81 samples
cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer'].copy().align(colour.SpectralShape(380, 780, 5))
CMF = cmfs.values                                      # (81, 3) xbar ybar zbar
assert CMF.shape == (81, 3)

h, c, k = 6.62607015e-34, 2.99792458e8, 1.380649e-23
def planck(l_nm, T):
    l = l_nm * 1e-9
    return 2 * h * c**2 / l**5 / np.expm1(h * c / (l * k * T))
S = planck(lam, 5772.0); S /= S.max()
tau = 0.0088 * (lam / 1000.0) ** -4.05

def airmass(elev_deg):
    z = 90.0 - np.asarray(elev_deg, float)
    return 1.0 / (np.cos(np.radians(z)) + 0.50572 * (96.07995 - z) ** -1.6364)

M = np.array([[3.2404542, -1.5371385, -0.4985314],      # XYZ -> linear sRGB (D65), IEC 61966-2-1
              [-0.9692660, 1.8760108, 0.0415560],
              [0.0556434, -0.2040259, 1.0572252]])
def xyz(spec):           # spec (..., 81) -> XYZ, Riemann sum at 5 nm
    return spec @ CMF * 5.0
def lin_rgb(X):
    return X @ M.T
def gamut_map(rgb, Y):
    """If a channel < 0, mix with grey of the same luminance until it is 0 (keeps hue and Y)."""
    rgb = np.array(rgb, float); out_of_gamut = rgb.min() < 0
    if out_of_gamut:
        t = -rgb.min() / (Y - rgb.min())
        rgb = rgb + t * (Y - rgb)
    return rgb, out_of_gamut
def encode(v):
    v = np.clip(v, 0, 1)
    return np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055)
def hexs(rgb8):
    return '#%02X%02X%02X' % tuple(int(round(x)) for x in rgb8)
def colour_of(spec):
    """Chromaticity at normalised brightness: scale so the largest linear channel is 1."""
    X = xyz(spec); rgb = lin_rgb(X)
    rgb, oog = gamut_map(rgb, X[1])
    rgb = rgb / rgb.max()
    return encode(rgb) * 255, oog, X

def sky_lut(m_s, vz_deg):
    """Spectral sky radiance factor (without P/(4pi)) for view zenith angles -> linear sRGB, XYZ."""
    m_v = airmass(90.0 - vz_deg)[:, None]
    t = tau[None, :]
    dm = (m_s - m_v)
    with np.errstate(divide='ignore', invalid='ignore'):
        g = np.where(np.abs(dm) < 1e-6, t, -np.expm1(-t * dm) / dm)
    L = S[None, :] * m_v * np.exp(-t * m_v) * g / (4 * math.pi)
    X = xyz(L)
    return L, X, lin_rgb(X)

# Sun elevation schedule (degrees). Time is compressed; easing spends more time near the horizon,
# where the colour changes fastest per degree.
def elev_at(i):
    t = i / FPS
    t0, t1 = 0.6, 7.6                                  # hold 0.6 s at start, reach horizon at 7.6 s, hold
    u = min(max((t - t0) / (t1 - t0), 0.0), 1.0)
    u = u * u * (3 - 2 * u)                            # smoothstep: no jerk at start or end
    return 60.0 * (1 - u) ** 1.6

vz = np.linspace(0, 90, 91)                            # LUT over view zenith angle, 1 degree
Y_noon = xyz(S * np.exp(-tau * airmass(90.0)))[1]
P_zen_ref = None
frames = []
for i in range(NF):
    e = elev_at(i)
    m_s = float(airmass(e))
    direct = S * np.exp(-tau * m_s)
    sun8, sun_oog, Xs = colour_of(direct)
    L, X, rgb = sky_lut(m_s, vz)
    cos_th = math.sin(math.radians(e))                 # zenith view: scattering angle = sun zenith angle
    P = 0.75 * (1 + cos_th ** 2)
    zen_spec = L[0] * P
    zen8, zen_oog, Xz = colour_of(zen_spec)
    frames.append(dict(
        e=round(e, 4), m=round(m_s, 4),
        T450=float(np.exp(-tau[lam == 450][0] * m_s)), T650=float(np.exp(-tau[lam == 650][0] * m_s)),
        sun=[round(float(x), 2) for x in sun8], sun_hex=hexs(sun8), sun_oog=bool(sun_oog),
        sunY=float(Xs[1] / Y_noon),
        zen=[round(float(x), 2) for x in zen8], zen_hex=hexs(zen8), zen_oog=bool(zen_oog),
        zenY=float(Xz[1]),
        direct=[round(float(x / direct.max()), 5) for x in direct],
        zspec=[round(float(x / zen_spec.max()), 5) for x in zen_spec],
        lut=[[float(v) for v in row] for row in rgb],   # linear sRGB without P, per view zenith deg
    ))

# monochromatic strip colours for the plot axis (same pipeline, each wavelength at normalised brightness)
strip = []
for j in range(len(lam)):
    X = CMF[j]; rgb = lin_rgb(X); rgb, _ = gamut_map(rgb, X[1]); rgb = np.clip(rgb / max(rgb.max(), 1e-9), 0, 1)
    strip.append([round(float(x), 2) for x in encode(rgb) * 255 * min(1.0, 0.25 + 3.0 * X[1] ** 0.5)])

data = dict(fps=FPS, nf=NF, lam=lam.tolist(), S=[round(float(x), 5) for x in S], tau=tau.tolist(),
            strip=strip, vz=vz.tolist(), frames=frames)
with open(OUT, 'w') as f:
    json.dump(data, f)

print('written', OUT, os.path.getsize(OUT), 'bytes')
print('tau(450)=%.4f tau(550)=%.4f tau(650)=%.4f  ratio tau450/tau650=%.2f' % (
    tau[lam == 450][0], tau[lam == 550][0], tau[lam == 650][0], tau[lam == 450][0] / tau[lam == 650][0]))
print('elev  airmass  T450   T650   sun sRGB (hex)        zenith sRGB (hex)      sun Y/noon  oog(sun,zen)')
for e in [60, 30, 20, 10, 5, 2, 1, 0]:
    m_s = float(airmass(e)); direct = S * np.exp(-tau * m_s)
    s8, so, Xs = colour_of(direct)
    L, X, rgb = sky_lut(m_s, vz); P = 0.75 * (1 + math.sin(math.radians(e)) ** 2)
    z8, zo, _ = colour_of(L[0] * P)
    print('%4.0f  %7.2f  %.4f %.4f  %s %-14s %s %-14s %.4f  %s,%s' % (
        e, m_s, math.exp(-tau[lam == 450][0] * m_s), math.exp(-tau[lam == 650][0] * m_s),
        hexs(s8), str(tuple(int(round(x)) for x in s8)), hexs(z8), str(tuple(int(round(x)) for x in z8)),
        Xs[1] / Y_noon, so, zo))
````

## p2.html

P2, шаг 2: рисует кадры по data/p2.json.

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="/src/common.css">
<link rel="stylesheet" href="/js/node_modules/katex/dist/katex.min.css">
<style>
  canvas { position: absolute; left: 0; top: 0; }
  .row { display: flex; justify-content: space-between; align-items: baseline; font-size: 27px; color: var(--ink2); margin: 0 0 14px 0; }
  .row .num { color: var(--ink); font-size: 34px; }
  .sw { display: inline-block; width: 30px; height: 30px; border-radius: 50%; vertical-align: -6px; margin-right: 12px; border: 1px solid rgba(255,255,255,0.25); }
  .hex { font-family: 'DejaVu Sans Mono', monospace; font-size: 22px; color: var(--ink); letter-spacing: 0.02em; }
  .lbl { font-size: 22px; color: var(--ink2); }
  .bar { height: 10px; border-radius: 5px; background: #1c2536; position: relative; overflow: hidden; width: 170px; display: inline-block; vertical-align: 2px; margin-left: 12px; }
  .bar i { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 5px; }
  .katex { font-size: 1.0em; }
</style></head>
<body>
<canvas id="cv" width="1920" height="1080"></canvas>

<div class="abs" style="left:72px; top:34px;">
  <span class="h1">Sunset, computed</span>
  <span class="h2" style="margin-left:18px;">clear air, Rayleigh scattering only</span>
</div>

<!-- sky window labels -->
<div class="abs lbl" id="zenLbl" style="top:104px; padding:2px 10px; border-radius:6px; background:rgba(10,14,23,0.7); color:var(--ink);"></div>
<div class="abs lbl" style="left:84px; top:812px; color:#8796ab;">horizon</div>
<div class="abs" id="ozone" style="left:648px; top:160px; padding:10px 14px; border-radius:8px; background:rgba(10,14,23,0.78); font-size:21px; color:var(--model); opacity:0; line-height:1.3;">
  Zenith goes pale in this model: it has no ozone.<br>Real twilight zenith stays blue (ozone absorbs orange).</div>

<!-- right panel -->
<div class="abs" style="left:1236px; top:112px; width:612px;">
  <div class="row"><span>Sun elevation</span><span class="num" id="vElev"></span></div>
  <div class="row"><span>Path through air <span class="lbl">(air mass)</span></span><span class="num" id="vAM"></span></div>
  <div class="row" style="margin-top:22px;"><span>Direct light reaching you</span></div>
  <div class="row"><span><span style="color:var(--blue)">blue 450 nm</span><span class="bar"><i id="b450" style="background:var(--blue)"></i></span></span><span class="num" id="v450"></span></div>
  <div class="row"><span><span style="color:var(--red)">red 650 nm</span><span class="bar"><i id="b650" style="background:var(--red)"></i></span></span><span class="num" id="v650"></span></div>
  <div class="row" style="margin-top:22px;"><span>Sun brightness <span class="lbl">vs overhead</span></span><span class="num" id="vSunY"></span></div>
  <div class="row"><span>Zenith brightness <span class="lbl">vs start</span></span><span class="num" id="vZenY"></span></div>
  <div style="display:flex; gap:34px; margin-top:20px;">
    <div><span class="sw" id="swSun"></span><span class="lbl">sun disc </span><span class="hex" id="hSun"></span></div>
    <div><span class="sw" id="swZen"></span><span class="lbl">zenith </span><span class="hex" id="hZen"></span></div>
  </div>
</div>
<div class="abs lbl" style="left:1236px; top:906px; width:612px; display:flex; justify-content:space-between;">
  <span>380</span><span>wavelength, nm</span><span>780</span></div>
<div class="abs" id="legend" style="left:1236px; top:560px; width:612px; font-size:20px; color:var(--ink2); line-height:1.45;"></div>

<div class="abs" style="left:72px; top:990px; display:flex; gap:14px; align-items:center;">
  <span class="tag model">Model <span class="rest">single scattering, no aerosols or ozone · sun = 5772 K blackbody · <span id="ktau"></span> · air mass: Kasten &amp; Young 1989</span></span>
</div>
<div class="abs" style="left:72px; top:930px; display:flex; gap:14px;">
  <span class="tag exact">Computed <span class="rest">CIE 1931 2° colour matching → sRGB</span></span>
  <span class="tag model">Display <span class="rest">auto exposure · sun disc ×6 · time compressed</span></span>
</div>

<script type="module">
import katex from '/js/node_modules/katex/dist/katex.mjs';
katex.render('\\tau(\\lambda)=0.0088\\,\\lambda_{\\mu m}^{-4.05}', document.getElementById('ktau'), { throwOnError: true });
const D = await (await fetch('/data/p2.json')).json();
const cv = document.getElementById('cv'), g = cv.getContext('2d');
// sky window geometry: equirectangular, 8.44 px per degree, elevation 0..90, azimuth +-65
const WX = 72, WY = 96, WW = 1104, HOR = 856, PX = (HOR - WY) / 90;
const CX = WX + WW / 2;
const img = g.createImageData(WW, HOR - WY);
const enc = v => v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
const ENC = new Uint8ClampedArray(4096); for (let i = 0; i < 4096; i++) ENC[i] = Math.round(255 * enc(i / 4095));
let zenY0 = null;
const NPIX = WW * (HOR - WY);
const BUF = { Y: new Float32Array(NPIX), R: new Float32Array(NPIX), G: new Float32Array(NPIX), B: new Float32Array(NPIX) };   // allocated once
const smooth = x => x * x * (3 - 2 * x);
const clamp01 = x => Math.max(0, Math.min(1, x));

function drawSky(f) {
  const e = f.e * Math.PI / 180, se = Math.sin(e), ce = Math.cos(e);
  const lut = f.lut, data = img.data, H = HOR - WY;
  const Y = BUF.Y, R = BUF.R, G = BUF.G, B = BUF.B;
  for (let y = 0; y < H; y++) {
    const el = (HOR - (WY + y + 0.5)) / PX, elr = el * Math.PI / 180, vz = 90 - el;
    const i0 = Math.min(89, Math.floor(vz)), t = vz - i0, a = lut[i0], b = lut[i0 + 1];
    const lr = a[0] + (b[0] - a[0]) * t, lg = a[1] + (b[1] - a[1]) * t, lb = a[2] + (b[2] - a[2]) * t;
    const sel = Math.sin(elr), cel = Math.cos(elr);
    for (let x = 0; x < WW; x++) {
      const az = ((WX + x + 0.5) - CX) / PX * Math.PI / 180;
      const c = sel * se + cel * ce * Math.cos(az);
      const P = 0.75 * (1 + c * c), k = y * WW + x;
      R[k] = P * lr; G[k] = P * lg; B[k] = P * lb;
      Y[k] = 0.2126 * R[k] + 0.7152 * G[k] + 0.0722 * B[k];
    }
  }
  // auto exposure: median luminance of the window -> 0.55 before a soft shoulder on luminance
  const s = []; for (let k = 0; k < Y.length; k += 37) s.push(Y[k]); s.sort((p, q) => p - q);
  const ex = 0.55 / s[Math.floor(s.length * 0.5)];
  for (let k = 0; k < Y.length; k++) {
    // tone-map luminance only (hue preserved), then clip by the largest channel (hue preserved)
    const yk = Math.max(Y[k], 1e-12), sc = (1 - Math.exp(-yk * ex)) / yk;
    let r = R[k] * sc, gg = G[k] * sc, bb = B[k] * sc;
    const m = Math.max(r, gg, bb); if (m > 1) { r /= m; gg /= m; bb /= m; }
    const o = k * 4;
    data[o] = ENC[Math.max(0, Math.round(r * 4095))]; data[o + 1] = ENC[Math.max(0, Math.round(gg * 4095))];
    data[o + 2] = ENC[Math.max(0, Math.round(bb * 4095))]; data[o + 3] = 255;
  }
  g.save();
  g.beginPath(); g.roundRect(WX, WY, WW, HOR - WY + 64, 18); g.clip();
  g.putImageData(img, WX, WY);
  // sun disc, enlarged x6 (true 0.53 deg -> drawn 3.2 deg)
  const sy = HOR - f.e * PX, r = 0.53 * 6 / 2 * PX;
  const sc = `rgb(${f.sun.map(Math.round).join(',')})`;
  const glow = g.createRadialGradient(CX, sy, r * 0.9, CX, sy, r * 2.6);
  glow.addColorStop(0, `rgba(${f.sun.map(Math.round).join(',')},0.35)`); glow.addColorStop(1, `rgba(${f.sun.map(Math.round).join(',')},0)`);
  g.fillStyle = glow; g.beginPath(); g.arc(CX, sy, r * 2.6, 0, 7); g.fill();
  g.fillStyle = sc; g.beginPath(); g.arc(CX, sy, r, 0, 7); g.fill();
  // thin outline so the disc stays readable when the normalised sky around it is as bright as the disc
  g.strokeStyle = 'rgba(10,14,23,0.55)'; g.lineWidth = 2; g.beginPath(); g.arc(CX, sy, r + 1, 0, 7); g.stroke();
  // ground: flat dark band; drawn after the sun so the horizon hides the part of the disc below it
  g.fillStyle = '#06080d'; g.fillRect(WX, HOR, WW, 64);
  g.strokeStyle = 'rgba(255,255,255,0.18)'; g.lineWidth = 1; g.beginPath(); g.moveTo(WX, HOR + 0.5); g.lineTo(WX + WW, HOR + 0.5); g.stroke();
  g.restore();
  // window frame
  g.strokeStyle = 'rgba(255,255,255,0.10)'; g.lineWidth = 2; g.beginPath(); g.roundRect(WX, WY, WW, HOR - WY + 64, 18); g.stroke();
  // zenith marker: small ring at the top centre
  g.strokeStyle = 'rgba(10,14,23,0.8)'; g.lineWidth = 3; g.beginPath(); g.arc(CX, WY + 34, 16, 0, 7); g.stroke();
  g.strokeStyle = 'rgba(255,255,255,0.9)'; g.lineWidth = 1.5; g.beginPath(); g.arc(CX, WY + 34, 16, 0, 7); g.stroke();
}

function drawPlot(f) {
  const X0 = 1236, X1 = 1848, Y0 = 668, Y1 = 880;
  const lam = D.lam, n = lam.length, xs = i => X0 + (X1 - X0) * (lam[i] - 380) / 400;
  // spectral strip under the axis
  for (let i = 0; i < n - 1; i++) { g.fillStyle = `rgb(${D.strip[i].map(Math.round).join(',')})`; g.fillRect(xs(i), Y1 + 6, xs(i + 1) - xs(i) + 0.6, 12); }
  g.strokeStyle = 'rgba(255,255,255,0.18)'; g.lineWidth = 1;
  g.beginPath(); g.moveTo(X0, Y1 + 0.5); g.lineTo(X1, Y1 + 0.5); g.stroke();
  for (const L of [450, 550, 650]) { const x = X0 + (X1 - X0) * (L - 380) / 400; g.beginPath(); g.moveTo(x + 0.5, Y0); g.lineTo(x + 0.5, Y1); g.setLineDash([2, 5]); g.stroke(); g.setLineDash([]); }
  const curve = (arr, color, w, dash, fill) => {
    g.beginPath();
    for (let i = 0; i < n; i++) { const x = xs(i), y = Y1 - (Y1 - Y0) * arr[i]; i ? g.lineTo(x, y) : g.moveTo(x, y); }
    if (fill) { const p = new Path2D(); for (let i = 0; i < n; i++) { const x = xs(i), y = Y1 - (Y1 - Y0) * arr[i]; i ? p.lineTo(x, y) : p.moveTo(x, y); } p.lineTo(X1, Y1); p.lineTo(X0, Y1); p.closePath(); g.fillStyle = fill; g.fill(p); }
    g.strokeStyle = color; g.lineWidth = w; g.setLineDash(dash || []); g.lineJoin = 'round'; g.stroke(); g.setLineDash([]);
  };
  curve(D.S, 'rgba(200,210,225,0.65)', 2, [7, 6]);
  curve(f.zspec, `rgb(${f.zen.map(Math.round).join(',')})`, 4, null, `rgba(${f.zen.map(Math.round).join(',')},0.10)`);
  curve(f.direct, `rgb(${f.sun.map(Math.round).join(',')})`, 4, null, `rgba(${f.sun.map(Math.round).join(',')},0.10)`);
}

const pct = v => v >= 0.1 ? (v * 100).toFixed(0) + '%' : v >= 0.01 ? (v * 100).toFixed(1) + '%' : (v * 100).toFixed(2) + '%';
const $ = id => document.getElementById(id);
window.renderFrame = (i) => {
  const f = D.frames[i];
  if (zenY0 === null) zenY0 = D.frames[0].zenY;
  g.fillStyle = '#0a0e17'; g.fillRect(0, 0, 1920, 1080);
  drawSky(f); drawPlot(f);
  $('vElev').textContent = f.e.toFixed(1) + '°';
  $('vAM').textContent = f.m.toFixed(1) + '×';
  $('v450').textContent = pct(f.T450); $('v650').textContent = pct(f.T650);
  $('b450').style.width = (f.T450 * 100) + '%'; $('b650').style.width = (f.T650 * 100) + '%';
  $('vSunY').textContent = pct(f.sunY); $('vZenY').textContent = pct(f.zenY / zenY0);
  $('swSun').style.background = f.sun_hex; $('swZen').style.background = f.zen_hex;
  $('hSun').textContent = f.sun_hex; $('hZen').textContent = f.zen_hex;
  $('zenLbl').innerHTML = '';
  const zl = $('zenLbl'); zl.style.left = (CX + 26) + 'px'; zl.style.top = (WY + 18) + 'px';
  zl.innerHTML = `zenith`;
  $('ozone').style.opacity = smooth(clamp01((4.5 - f.e) / 2.0));
  $('legend').innerHTML =
    `<span style="color:rgba(200,210,225,0.8)">- - sunlight above the air</span> &nbsp; ` +
    `<span style="color:${f.sun_hex}">━ direct sun</span> &nbsp; <span style="color:${f.zen_hex}">━ zenith sky</span><br>` +
    `<span style="font-size:18px">each curve scaled to its own peak</span>`;
};
window.info = () => ({ frames: D.nf });
window.ready = true;
</script>
</body></html>
````

## p3_timeline.json

P3 и P3-sound: общие часы (секунды) для картинки и звука.

````json
{
  "fps": 30,
  "frames": 240,
  "note": "seconds; shared by p3.html (picture) and p6_sound.py (sound) so both follow one clock",
  "hue":      [1.0, 2.6],
  "gap":      [1.0, 3.3],
  "collapse": [2.0, 3.3],
  "axes":     [3.3, 4.3],
  "bend":     [4.3, 6.3],
  "mark450":  6.45,
  "mark650":  6.75,
  "ratio":    7.0,
  "captions": [[0.0, 2.0], [2.0, 4.3], [4.3, 8.0]]
}
````

## p3.html

P3: полоса неба, спектр, кривая λ^-4 (морфинг).

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="/src/common.css">
<link rel="stylesheet" href="/js/node_modules/katex/dist/katex.min.css">
<style>
  canvas { position: absolute; left: 0; top: 0; }
  .cap { position: absolute; left: 240px; top: 92px; font-size: 46px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
  .sub { font-size: 26px; font-weight: 400; color: var(--ink2); margin-top: 6px; }
  .tick { position: absolute; font-size: 24px; color: var(--ink2); transform: translateX(-50%); }
  .axl { position: absolute; font-size: 24px; color: var(--ink2); }
  .mk { position: absolute; font-size: 26px; font-weight: 700; white-space: nowrap; }
  .katex { font-size: 1.05em; }
</style></head>
<body>
<canvas id="cv" width="1920" height="1080"></canvas>
<div class="cap" id="c0">Sky light<div class="sub">colour computed in P2: clear air, sun 60° high</div></div>
<div class="cap" id="c1">is a mix of wavelengths<div class="sub">the visible spectrum, 380–750 nm</div></div>
<div class="cap" id="c2" style="left:900px; top:300px;"><span>Air scatters short waves far more</span><div class="sub" id="kform" style="font-size:44px; color:var(--ink); margin-top:14px;"></div></div>
<div id="ticks"></div>
<div class="axl" id="xl" style="left:1500px; top:850px;">wavelength, nm</div>
<div class="axl" id="yl" style="left:266px; top:160px;">scattered light (relative)</div>
<div class="mk" id="m450" style="color:var(--blue)">450 nm</div>
<div class="mk" id="m650" style="color:var(--red)">650 nm</div>
<div class="mk" id="mratio" style="color:var(--ink); font-weight:400; font-size:28px;"></div>
<div class="abs" style="left:240px; top:990px; display:flex; gap:14px;">
  <span class="tag exact">Exact <span class="rest">curve height ∝ λ<sup>−4</sup> · strip colours CIE 1931 → sRGB</span></span>
  <span class="tag model">Visual link <span class="rest">the band does not physically turn into a graph</span></span>
</div>
<script type="module">
import katex from '/js/node_modules/katex/dist/katex.mjs';
katex.render('I_{\\text{scattered}}\\;\\propto\\;\\lambda^{-4}', document.getElementById('kform'), { throwOnError: true });
const T = await (await fetch('/src/p3_timeline.json')).json();
const D = await (await fetch('/data/p2.json')).json();
const cv = document.getElementById('cv'), g = cv.getContext('2d');
const acc = document.createElement('canvas'); acc.width = 1920; acc.height = 1080; const ga = acc.getContext('2d');

// ---------- geometry ----------
const L0 = 380, L1 = 750, X0 = 240, X1 = 1680, BASE = 800, HB = 560, HS = 70;  // band 1440 x 560, strip 70 tall
const xOf = l => X0 + (X1 - X0) * (l - L0) / (L1 - L0);
const lOf = x => L0 + (L1 - L0) * (x - X0) / (X1 - X0);
const curveH = l => HB * Math.pow(L0 / l, 4);                 // exact 1/lambda^4, 380 nm -> full height
// ---------- colours ----------
const dec = v => v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
const enc = v => v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(Math.max(v, 0), 1 / 2.4) - 0.055;
const lin = c => c.map(v => dec(v / 255));
const css = (c, a = 1) => `rgba(${c.map(v => Math.round(255 * enc(v))).join(',')},${a})`;
const mono = l => {                                            // P2 strip: 5 nm samples from 380 nm, linear interp
  const f = (l - 380) / 5, i = Math.min(Math.floor(f), D.strip.length - 2), t = f - i;
  const a = lin(D.strip[i]), b = lin(D.strip[i + 1]); return a.map((v, k) => v + (b[k] - v) * t);
};
// sky column colours from the P2 model (frame 0, sun 60 deg), seen 90 deg in azimuth from the sun, zenith -> 5 deg
const f0 = D.frames[0], e0 = f0.e * Math.PI / 180;
const skyAt = el => {                                          // linear sRGB, before exposure
  const vz = 90 - el, i = Math.min(89, Math.floor(vz)), t = vz - i, a = f0.lut[i], b = f0.lut[i + 1];
  const elr = el * Math.PI / 180, c = Math.sin(elr) * Math.sin(e0), P = 0.75 * (1 + c * c);
  return [0, 1, 2].map(k => P * (a[k] + (b[k] - a[k]) * t));
};
const skyStops = []; { const raw = []; for (let k = 0; k <= 16; k++) raw.push(skyAt(90 - k * 85 / 16));
  const Ys = raw.map(c => 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]); const ex = 0.55 / Ys[8];
  raw.forEach((c, k) => { const y = Ys[k], s = (1 - Math.exp(-y * ex)) / y; let v = c.map(q => q * s); const m = Math.max(...v); if (m > 1) v = v.map(q => q / m); skyStops.push(v); }); }
const NC = 74, cw = (X1 - X0) / NC;                             // 74 columns of 5 nm
const specGrad = (() => { const gr = g.createLinearGradient(X0, 0, X1, 0); for (let k = 0; k <= 74; k++) { const l = L0 + 5 * k; gr.addColorStop(k / 74, css(mono(l))); } return gr; })();
const specGradA = (() => { const gr = ga.createLinearGradient(X0, 0, X1, 0); for (let k = 0; k <= 74; k++) { const l = L0 + 5 * k; gr.addColorStop(k / 74, css(mono(l))); } return gr; })();

// ---------- easing ----------
const cl = x => Math.max(0, Math.min(1, x));
const sm = x => { x = cl(x); return x * x * x * (x * (6 * x - 15) + 10); };      // smootherstep: zero velocity and acceleration at both ends
const ph = (t, [a, b]) => sm((t - a) / (b - a));
const lerp = (a, b, t) => a + (b - a) * t;

// ---------- scene at continuous time t (seconds) ----------
function draw(c, t, grad) {
  c.fillStyle = '#0a0e17'; c.fillRect(0, 0, 1920, 1080);
  const sGap = (t - T.gap[0]) / (T.gap[1] - T.gap[0]);
  const gap = sGap > 0 && sGap < 1 ? 6 * Math.sin(Math.PI * sm(sGap)) : 0;     // columns part, then close again
  const sCol = ph(t, T.collapse), sBend = ph(t, T.bend);
  const topAt = x => {                                          // height of the band top above BASE at x
    const hFlat = lerp(HB, HS, sCol);
    return sBend > 0 ? lerp(hFlat, curveH(lOf(x)), sBend) : hFlat;
  };
  const skyG = c.createLinearGradient(0, BASE - lerp(HB, HS, sCol), 0, BASE);
  skyStops.forEach((v, k) => skyG.addColorStop(k / 16, css(v)));
  for (let i = 0; i < NC; i++) {
    // whole-pixel column edges: no anti-aliasing seams between touching columns
    const xa = Math.round(X0 + i * cw) + gap / 2, xb = Math.round(X0 + (i + 1) * cw) - gap / 2;
    // hue shift sweeps left to right, each column eased on its own
    const p = sm((t - T.hue[0] - 0.55 * (T.hue[1] - T.hue[0]) * i / (NC - 1)) / (0.45 * (T.hue[1] - T.hue[0])));
    c.save(); c.beginPath(); c.moveTo(xa, BASE);
    const n = 6; for (let k = 0; k <= n; k++) { const x = lerp(xa, xb, k / n); c.lineTo(x, BASE - topAt(x)); }
    c.lineTo(xb, BASE); c.closePath(); c.clip();
    c.fillStyle = grad; c.fillRect(xa, 0, xb - xa, BASE + 1);
    if (p < 1) { c.globalAlpha = 1 - p; c.fillStyle = skyG; c.fillRect(xa, 0, xb - xa, BASE + 1); c.globalAlpha = 1; }
    c.restore();
  }
  // strokes: once the strip exists its edges become the axes and its top edge becomes the curve
  const sAx = ph(t, T.axes);
  if (sCol > 0.98 || sAx > 0) {
    const a = cl((sCol - 0.98) / 0.02);
    c.lineCap = 'round'; c.lineJoin = 'round';
    // bottom edge -> x axis, growing outward from the strip ends
    c.strokeStyle = `rgba(233,238,246,${0.9 * a})`; c.lineWidth = 3;
    c.beginPath(); c.moveTo(X0 - 40 * sAx, BASE + 1.5); c.lineTo(X1 + 80 * sAx, BASE + 1.5); c.stroke();
    if (sAx > 0) { const ax = X1 + 80 * sAx; c.beginPath(); c.moveTo(ax - 16 * sAx, BASE + 1.5 - 9 * sAx); c.lineTo(ax, BASE + 1.5); c.lineTo(ax - 16 * sAx, BASE + 1.5 + 9 * sAx); c.stroke(); }
    // left edge -> y axis, growing upward
    const yTop = BASE - lerp(HS, HB + 70, sAx);
    c.beginPath(); c.moveTo(X0 - 1.5, BASE + 1.5); c.lineTo(X0 - 1.5, yTop); c.stroke();
    if (sAx > 0) { c.beginPath(); c.moveTo(X0 - 1.5 - 9 * sAx, yTop + 16 * sAx); c.lineTo(X0 - 1.5, yTop); c.lineTo(X0 - 1.5 + 9 * sAx, yTop + 16 * sAx); c.stroke(); }
    // ticks drop out of the axis
    for (const l of [400, 500, 600, 700]) { const x = xOf(l); c.beginPath(); c.moveTo(x, BASE + 3); c.lineTo(x, BASE + 3 + 12 * sAx); c.stroke(); }
    // top edge -> the 1/lambda^4 curve
    c.strokeStyle = `rgba(255,255,255,${a})`; c.lineWidth = 4; c.beginPath();
    for (let x = X0; x <= X1; x += 4) { const y = BASE - topAt(x); x === X0 ? c.moveTo(x, y) : c.lineTo(x, y); }
    c.stroke();
  }
  // markers at 450 and 650 nm: same colours as in every probe
  for (const [l, tm, col] of [[450, T.mark450, '#5aa9ff'], [650, T.mark650, '#ff6a4d']]) {
    const s = sm((t - tm) / 0.45); if (s <= 0) continue;
    const x = xOf(l), h = curveH(l) * sBend;
    c.strokeStyle = col; c.lineWidth = 3; c.setLineDash([6, 7]);
    c.beginPath(); c.moveTo(x, BASE); c.lineTo(x, BASE - h * s); c.stroke(); c.setLineDash([]);
    c.fillStyle = col; c.beginPath(); c.arc(x, BASE - h * s, 10 * s, 0, 7); c.fill();
    c.strokeStyle = '#0a0e17'; c.lineWidth = 3; c.stroke();
  }
}

// motion blur: average 5 sub-frame samples over a 180-degree shutter
const SUB = 5, SHUTTER = 0.5;
function frame(i) {
  const t = i / T.fps;
  if (i === 0) { draw(g, t, specGrad); return; }
  for (let j = 0; j < SUB; j++) {
    const ts = t + ((j + 0.5) / SUB - 0.5) * SHUTTER / T.fps;
    draw(ga, Math.max(0, ts), specGradA);
    g.globalAlpha = 1 / (j + 1); g.drawImage(acc, 0, 0); g.globalAlpha = 1;
  }
}

// ---------- DOM overlay (captions, tick labels) ----------
const $ = id => document.getElementById(id);
const ticks = $('ticks');
for (const l of [400, 500, 600, 700]) { const d = document.createElement('div'); d.className = 'tick'; d.textContent = l; d.style.left = xOf(l) + 'px'; d.style.top = (BASE + 22) + 'px'; d.dataset.l = l; ticks.appendChild(d); }
function overlay(t) {
  T.captions.forEach(([a, b], k) => {
    const el = $('c' + k), fin = sm((t - a) / 0.5), fout = k < 2 ? sm((t - b + 0.4) / 0.4) : 0;
    el.style.opacity = (k === 0 ? 1 : fin) * (1 - fout);
    el.style.transform = `translateY(${(1 - (k === 0 ? 1 : fin)) * 18 - fout * 18}px)`;
  });
  const sAx = ph(t, T.axes);
  for (const d of ticks.children) d.style.opacity = sm((sAx - 0.4) / 0.6);
  $('xl').style.opacity = sm((sAx - 0.5) / 0.5); $('yl').style.opacity = sm((t - 4.3) / 0.5);  // after caption 2 has left, no text overlap
  const sBend = ph(t, T.bend);
  for (const [id, l, tm] of [['m450', 450, T.mark450], ['m650', 650, T.mark650]]) {
    const s = sm((t - tm - 0.2) / 0.4), el = $(id);
    el.style.opacity = s; el.style.left = (xOf(l) + 18) + 'px'; el.style.top = (BASE - curveH(l) * sBend - 52) + 'px';
  }
  const r = Math.pow(650 / 450, 4);
  const mr = $('mratio'); mr.innerHTML = `450 nm is scattered <b>${r.toFixed(1)}×</b> more than 650 nm`;
  mr.style.opacity = sm((t - T.ratio) / 0.5); mr.style.left = '900px'; mr.style.top = '470px';
}
window.renderFrame = i => { frame(i); overlay(i / T.fps); };
window.info = () => ({ frames: T.frames, ratio_650_450: Math.pow(650 / 450, 4) });
window.ready = true;
</script>
</body></html>
````

## p6_sound.py

P3-sound: процедурный звук по тем же часам (numpy, scipy), data/p6.wav.

````python
"""P6: procedural sound for P3, generated with numpy/scipy only (no samples, no music).

Follows the same clock as the picture (src/p3_timeline.json):
  * 0 - 1.0 s   faint broadband noise: "sky light is a mix" (noise = all frequencies at once)
  * hue phase   the noise narrows to a band that sweeps high -> low in step with the colour sweep
                (short wavelength on the left = high pitch; the map is a sonification, not physics)
  * collapse    the band fades out as the strip settles
  * bend        a soft tone whose pitch is proportional to the height of the curve's left end
                (70 px -> 560 px, x8 = 3 octaves): the tone rises with the 1/lambda^4 curve
  * markers     two pings: pitch proportional to the curve height at 450 nm and 650 nm (ratio 4.35)
Output: data/p6.wav (48 kHz, 16-bit, stereo). Mux: see probes-code.md.
"""
import json, os, wave
import numpy as np
from scipy.signal import stft, istft

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'p3_timeline.json')))
SR = 48000
DUR = T['frames'] / T['fps']
n = int(round(DUR * SR))
t = np.arange(n) / SR
rng = np.random.default_rng(20261016)

def sm(x):
    x = np.clip(x, 0, 1); return x * x * x * (x * (6 * x - 15) + 10)
def ph(a, b):
    return sm((t - a) / (b - a))

# ---- 1. noise: broadband -> sweeping band -> gone ----------------------------------------
noise = rng.standard_normal(n)
f, ts, Z = stft(noise, fs=SR, nperseg=2048, noverlap=2048 - 256)
F = f[:, None]; TT = ts[None, :]
h0, h1 = T['hue']; D = h1 - h0
# column at the sweep front (p = 0.5) as a function of time -> wavelength -> audio frequency
col = np.clip((TT - h0 - 0.225 * D) / (0.55 * D) * 73, 0, 73)
lam = 380 + 5 * col
fc = 600.0 * (750.0 / lam) ** 3                      # 380 nm -> ~4.6 kHz, 750 nm -> 600 Hz
narrow = np.clip((TT - (h0 - 0.2)) / 0.6, 0, 1)      # 0 = broadband, 1 = narrow band
width_oct = 4.0 * (1 - narrow) + 0.35 * narrow
band = np.exp(-0.5 * (np.log2(np.maximum(F, 1.0) / fc) / width_oct) ** 2)
pink = 1.0 / np.sqrt(np.maximum(F, 20.0))             # pink tilt so broadband noise is soft, not hiss
Zf = Z * band * pink
_, whoosh = istft(Zf, fs=SR, nperseg=2048, noverlap=2048 - 256)
whoosh = whoosh[:n]
whoosh /= np.max(np.abs(whoosh)) + 1e-12
c0, c1 = T['collapse']
env_w = (0.15 + 0.85 * ph(h0 - 0.2, h0 + 0.5)) * (1 - ph(c0 + 0.3, c1 + 0.6)) * ph(0.0, 0.5)
whoosh *= env_w * 10 ** (-5 / 20)

# ---- 2. tone rising with the curve --------------------------------------------------------
b0, b1 = T['bend']
HS, HB = 70.0, 560.0
s_b = ph(b0, b1)
h_left = HS + (HB - HS) * s_b                        # height of the curve at 380 nm, as drawn
freq = 165.0 * h_left / HS                           # 165 Hz -> 1320 Hz
phase = 2 * np.pi * np.cumsum(freq) / SR
tone = np.sin(phase) + 0.15 * np.sin(2 * phase) + 0.03 * np.sin(3 * phase)
env_t = ph(b0 - 0.05, b0 + 0.25) * (1 - ph(b1 + 0.05, b1 + 0.6))
tone *= env_t * 10 ** (-21 / 20) / 1.18

# ---- 3. pings at the 450 / 650 nm markers ---------------------------------------------------
def ping(t0, fr, gain_db):
    x = np.zeros(n); m = t >= t0; tt = t[m] - t0
    x[m] = (np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(2 * np.pi * 2 * fr * tt)) * np.exp(-tt / 0.35) * (1 - np.exp(-tt / 0.004))
    return x * 10 ** (gain_db / 20)
h450 = HB * (380 / 450) ** 4; h650 = HB * (380 / 650) ** 4
f450 = 165.0 * h450 / HS; f650 = 165.0 * h650 / HS
pings = ping(T['mark450'], f450, -15) + ping(T['mark650'], f650, -15)
# soft low tick when the axes finish growing out of the strip edges
a1 = T['axes'][1]; tick = np.zeros(n); m = t >= a1 - 0.05; tt = t[m] - (a1 - 0.05)
tick[m] = np.sin(2 * np.pi * 220 * tt) * np.exp(-tt / 0.06) * (1 - np.exp(-tt / 0.002)) * 10 ** (-20 / 20)
pings += tick

# ---- mix: whoosh slightly wide, tone and pings centred -------------------------------------
delay = int(0.011 * SR)
wl = whoosh; wr = np.concatenate([np.zeros(delay), whoosh[:-delay]])
L = wl + tone + pings; R = 0.9 * wr + tone + pings
mix = np.stack([L, R], 1)
fade = np.minimum(1, np.minimum(t / 0.02, (DUR - t) / 0.05))[:, None]
mix *= fade
mix *= 10 ** (-3 / 20) / np.max(np.abs(mix))          # peak -3 dBFS
out = os.path.join(HERE, '..', 'data', 'p6.wav')
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
rms = 20 * np.log10(np.sqrt(np.mean(mix ** 2)))
print(f'written {out}: {DUR:.2f} s, {SR} Hz stereo, peak -3.0 dBFS, rms {rms:.1f} dBFS')
print(f'pings: 450 nm -> {f450:.0f} Hz, 650 nm -> {f650:.0f} Hz (ratio {f450 / f650:.2f}); tone 165 -> {165 * HB / HS:.0f} Hz')
````

## p5_scene.json

P5: сцена диаграммы (фигуры, тексты, времена).

````json
{
 "_doc": "P5 template: one hand-drawn diagram per JSON. Times in seconds. Every element is drawn on stroke by stroke. Change shapes, texts and times; keep the renderer.",
 "fps": 30,
 "duration": 10,
 "seed": 7,
 "elements": [
  {
   "id": "sun",
   "type": "sun",
   "x": 250,
   "y": 470,
   "r": 92,
   "color": "#ffd77a",
   "start": 0.2,
   "dur": 1.0
  },
  {
   "id": "sunL",
   "type": "text",
   "x": 250,
   "y": 640,
   "text": "Sun",
   "color": "#ffd77a",
   "size": 36,
   "anchor": "middle",
   "start": 1.0
  },
  {
   "id": "airBox",
   "type": "rect",
   "x": 600,
   "y": 240,
   "w": 720,
   "h": 470,
   "color": "#5d6a7e",
   "dash": true,
   "start": 0.9,
   "dur": 0.9
  },
  {
   "id": "airL",
   "type": "text",
   "x": 612,
   "y": 226,
   "text": "air: N₂ and O₂ molecules",
   "color": "#9ba8bb",
   "size": 30,
   "start": 1.6
  },
  {
   "id": "mols",
   "type": "molecules",
   "color": "#c9d3e3",
   "r": 9,
   "start": 1.2,
   "dur": 1.4,
   "pts": [
    [
     640,
     300
    ],
    [
     760,
     560
    ],
    [
     700,
     420
    ],
    [
     880,
     330
    ],
    [
     1010,
     620
    ],
    [
     1110,
     300
    ],
    [
     1240,
     420
    ],
    [
     1180,
     560
    ],
    [
     830,
     650
    ],
    [
     1270,
     660
    ],
    [
     1060,
     450
    ],
    [
     660,
     650
    ]
   ]
  },
  {
   "id": "eye",
   "type": "eye",
   "x": 1640,
   "y": 470,
   "w": 170,
   "color": "#e9eef6",
   "start": 1.5,
   "dur": 1.0
  },
  {
   "id": "eyeL",
   "type": "text",
   "x": 1640,
   "y": 580,
   "text": "you",
   "color": "#e9eef6",
   "size": 34,
   "anchor": "middle",
   "start": 2.3
  },
  {
   "id": "beam",
   "type": "arrow",
   "from": [
    356,
    470
   ],
   "to": [
    932,
    470
   ],
   "color": "#fff1d6",
   "width": 5,
   "start": 2.4,
   "dur": 1.0
  },
  {
   "id": "beamL",
   "type": "text",
   "x": 398,
   "y": 440,
   "text": "white sunlight",
   "color": "#fff1d6",
   "size": 30,
   "start": 2.9
  },
  {
   "id": "hit",
   "type": "molecules",
   "color": "#ffffff",
   "r": 13,
   "start": 3.3,
   "dur": 0.3,
   "pts": [
    [
     950,
     470
    ]
   ]
  },
  {
   "id": "b1",
   "type": "arrow",
   "from": [
    950,
    452
   ],
   "to": [
    905,
    305
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 3.6,
   "dur": 0.6
  },
  {
   "id": "b2",
   "type": "arrow",
   "from": [
    966,
    456
   ],
   "to": [
    1075,
    345
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 3.7,
   "dur": 0.6
  },
  {
   "id": "b3",
   "type": "arrow",
   "from": [
    935,
    486
   ],
   "to": [
    850,
    610
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 3.8,
   "dur": 0.6
  },
  {
   "id": "b4",
   "type": "arrow",
   "from": [
    962,
    488
   ],
   "to": [
    1040,
    625
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 3.9,
   "dur": 0.6
  },
  {
   "id": "b5",
   "type": "arrow",
   "from": [
    930,
    462
   ],
   "to": [
    800,
    410
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 4.0,
   "dur": 0.6
  },
  {
   "id": "bL",
   "type": "text",
   "x": 640,
   "y": 272,
   "text": "blue: scattered every way",
   "color": "#5aa9ff",
   "size": 32,
   "start": 4.3
  },
  {
   "id": "r1",
   "type": "arrow",
   "from": [
    970,
    470
   ],
   "to": [
    1530,
    470
   ],
   "color": "#ff6a4d",
   "width": 5,
   "start": 4.6,
   "dur": 1.0
  },
  {
   "id": "r2",
   "type": "arrow",
   "from": [
    957,
    451
   ],
   "to": [
    978,
    398
   ],
   "color": "#ff6a4d",
   "width": 2,
   "start": 4.9,
   "dur": 0.4
  },
  {
   "id": "rL",
   "type": "text",
   "x": 1345,
   "y": 525,
   "text": "red: mostly",
   "color": "#ff6a4d",
   "size": 32,
   "start": 5.2
  },
  {
   "id": "rL2",
   "type": "text",
   "x": 1345,
   "y": 562,
   "text": "goes straight",
   "color": "#ff6a4d",
   "size": 32,
   "start": 5.4
  },
  {
   "id": "rL3",
   "type": "text",
   "x": 1345,
   "y": 598,
   "text": "(scatters too, ~4× less)",
   "color": "#ff6a4d",
   "size": 24,
   "start": 5.6
  },
  {
   "id": "sky",
   "type": "arrow",
   "from": [
    1110,
    312
   ],
   "to": [
    1585,
    432
   ],
   "color": "#5aa9ff",
   "width": 4,
   "start": 6.0,
   "dur": 0.9
  },
  {
   "id": "hit2",
   "type": "molecules",
   "color": "#ffffff",
   "r": 13,
   "start": 5.8,
   "dur": 0.3,
   "pts": [
    [
     1110,
     300
    ]
   ]
  },
  {
   "id": "skyL",
   "type": "text",
   "x": 1350,
   "y": 262,
   "text": "blue reaches you",
   "color": "#5aa9ff",
   "size": 30,
   "start": 6.6
  },
  {
   "id": "skyL2",
   "type": "text",
   "x": 1350,
   "y": 300,
   "text": "from all over the sky",
   "color": "#5aa9ff",
   "size": 30,
   "start": 6.75
  },
  {
   "id": "brace",
   "type": "arrow2",
   "from": [
    360,
    770
   ],
   "to": [
    1530,
    770
   ],
   "color": "#9ba8bb",
   "width": 3,
   "start": 7.2,
   "dur": 0.9
  },
  {
   "id": "braceL",
   "type": "text",
   "x": 945,
   "y": 830,
   "text": "at sunset this path is 10–40× longer: blue is used up, the Sun looks red",
   "color": "#e9eef6",
   "size": 32,
   "anchor": "middle",
   "start": 7.8
  }
 ]
}
````

## p5.html

P5: рисует сцену штрих за штрихом (rough.js).

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="/src/common.css">
<style> canvas { position: absolute; left: 0; top: 0; } </style></head>
<body>
<canvas id="cv" width="1920" height="1080"></canvas>
<div class="abs" style="left:72px; top:44px;"><span class="h1">Why the sky is blue</span><span class="h2" style="margin-left:18px;">sketch template</span></div>
<div class="abs" style="left:72px; top:990px; display:flex; gap:14px;">
  <span class="tag model">Sketch <span class="rest">molecules enlarged, not to scale · arrows show directions, not amounts</span></span>
</div>
<script type="module">
import rough from '/js/node_modules/roughjs/bundled/rough.esm.js';
const S = await (await fetch('/src/p5_scene.json')).json();
await document.fonts.load('32px Lato');
const cv = document.getElementById('cv'), g = cv.getContext('2d');
const gen = rough.generator();
const svgNS = 'http://www.w3.org/2000/svg';
const probe = document.createElementNS(svgNS, 'svg'); probe.style.position = 'absolute'; probe.style.left = '-9999px'; document.body.appendChild(probe);
const pathEl = document.createElementNS(svgNS, 'path'); probe.appendChild(pathEl);

// turn rough.js drawables into polylines (2 px steps) so any prefix of a stroke can be drawn
function polylines(drawable) {
  return gen.toPaths(drawable).map(p => {
    const out = [];
    for (const sub of p.d.split(/(?=M)/)) {
      pathEl.setAttribute('d', sub); const L = pathEl.getTotalLength(); if (L < 0.5) continue;
      const pts = []; for (let s = 0; s <= L; s += 2) { const q = pathEl.getPointAtLength(s); pts.push([q.x, q.y]); }
      const q = pathEl.getPointAtLength(L); pts.push([q.x, q.y]);
      out.push({ pts, len: L, stroke: p.stroke === 'none' ? p.fill : p.stroke, width: p.strokeWidth, fill: p.fill });
    }
    return out;
  }).flat();
}
const base = (el, extra = {}) => ({ seed: S.seed + el.id.length * 13 + el.id.charCodeAt(0), roughness: 1.4, bowing: 1.2,
  stroke: el.color, strokeWidth: el.width || 2.5, ...extra });

// build every element into ordered stroke groups: [{t0, t1, strokes:[...], dash}]
const items = [];
for (const el of S.elements) {
  const t0 = el.start, d = el.dur || 0.4;
  if (el.type === 'text') { items.push({ kind: 'text', el, t0 }); continue; }
  const groups = [];
  if (el.type === 'sun') {
    groups.push({ a: 0, b: 0.45, strokes: polylines(gen.circle(el.x, el.y, el.r * 2, base(el, { strokeWidth: 3 }))) });
    groups.push({ a: 0.35, b: 0.8, strokes: polylines(gen.circle(el.x, el.y, el.r * 2 - 10, base(el, { stroke: 'none', fill: el.color, fillStyle: 'hachure', hachureGap: 13, fillWeight: 2, hachureAngle: -41 }))) });
    const rays = []; for (let k = 0; k < 10; k++) { const a = k * Math.PI / 5 + 0.3; rays.push(...polylines(gen.line(el.x + Math.cos(a) * (el.r + 16), el.y + Math.sin(a) * (el.r + 16), el.x + Math.cos(a) * (el.r + 46), el.y + Math.sin(a) * (el.r + 46), base({ ...el, id: el.id + k }, { strokeWidth: 3 })))); }
    groups.push({ a: 0.6, b: 1, strokes: rays, parallel: true });
  } else if (el.type === 'rect') {
    groups.push({ a: 0, b: 1, strokes: polylines(gen.rectangle(el.x, el.y, el.w, el.h, base(el, { roughness: 1.0, strokeWidth: 2 }))), dash: el.dash });
  } else if (el.type === 'molecules') {
    el.pts.forEach(([x, y], k) => {
      const a = k / el.pts.length, b = Math.min(1, a + 2.5 / el.pts.length);
      groups.push({ a, b, strokes: polylines(gen.circle(x, y, el.r * 2, base({ ...el, id: el.id + k }, { strokeWidth: 2.5, fill: el.color, fillStyle: 'solid' }))), filled: [x, y, el.r, el.color] });
    });
  } else if (el.type === 'eye') {
    const { x, y, w } = el;
    groups.push({ a: 0, b: 0.55, strokes: polylines(gen.path(`M ${x - w / 2} ${y} Q ${x} ${y - 0.62 * w} ${x + w / 2} ${y} Q ${x} ${y + 0.62 * w} ${x - w / 2} ${y}`, base(el, { strokeWidth: 3 }))) });
    groups.push({ a: 0.45, b: 0.85, strokes: polylines(gen.circle(x - 0.06 * w, y, 0.4 * w, base(el, { strokeWidth: 2.5 }))) });
    groups.push({ a: 0.75, b: 1, strokes: polylines(gen.circle(x - 0.06 * w, y, 0.15 * w, base(el, { strokeWidth: 2, fill: el.color, fillStyle: 'solid' }))), filled: [x - 0.06 * w, y, 0.075 * w, el.color] });
  } else if (el.type === 'arrow' || el.type === 'arrow2') {
    const [x0, y0] = el.from, [x1, y1] = el.to, ang = Math.atan2(y1 - y0, x1 - x0), hl = 12 + 3 * (el.width || 3);
    groups.push({ a: 0, b: 0.8, strokes: polylines(gen.line(x0, y0, x1, y1, base(el, { roughness: 1.1 }))) });
    const head = (hx, hy, a0) => [-0.45, 0.45].flatMap(s => polylines(gen.line(hx, hy, hx - Math.cos(a0 + s) * hl, hy - Math.sin(a0 + s) * hl, base({ ...el, id: el.id + s }, { roughness: 0.8 }))));
    const hs = head(x1, y1, ang); if (el.type === 'arrow2') hs.push(...head(x0, y0, ang + Math.PI));
    groups.push({ a: 0.75, b: 1, strokes: hs, parallel: true });
  }
  items.push({ kind: 'shape', el, t0, d, groups });
}

const cl = x => Math.max(0, Math.min(1, x));
const ease = x => { x = cl(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };   // ease in-out cubic
function drawPrefix(st, frac) {
  if (frac <= 0) return;
  const n = st.pts.length, upto = frac * (n - 1), k = Math.floor(upto);
  g.beginPath(); g.moveTo(st.pts[0][0], st.pts[0][1]);
  for (let i = 1; i <= k; i++) g.lineTo(st.pts[i][0], st.pts[i][1]);
  if (k < n - 1) { const f = upto - k, a = st.pts[k], b = st.pts[k + 1]; g.lineTo(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f); }
  g.stroke();
}
function render(t) {
  g.fillStyle = '#0a0e17'; g.fillRect(0, 0, 1920, 1080);
  g.lineCap = 'round'; g.lineJoin = 'round';
  for (const it of items) {
    if (it.kind === 'text') {
      const p = ease((t - it.t0) / 0.4); if (p <= 0) continue;
      const e = it.el; g.globalAlpha = p; g.fillStyle = e.color; g.font = `${e.weight || 400} ${e.size}px Lato`;
      g.textAlign = e.anchor === 'middle' ? 'center' : 'left'; g.fillText(e.text, e.x, e.y + 10 * (1 - p)); g.globalAlpha = 1;
      continue;
    }
    const u = cl((t - it.t0) / it.d); if (u <= 0) continue;
    for (const gr of it.groups) {
      const p = ease((u - gr.a) / (gr.b - gr.a)); if (p <= 0) continue;
      g.setLineDash(gr.dash ? [10, 9] : []);
      if (gr.filled && p > 0.6) { const [x, y, r, c] = gr.filled; g.globalAlpha = cl((p - 0.6) / 0.4); g.fillStyle = c; g.beginPath(); g.arc(x, y, r * 0.92, 0, 7); g.fill(); g.globalAlpha = 1; }
      // strokes of one group are drawn one after another (a pen), unless marked parallel
      const total = gr.strokes.reduce((s, st) => s + st.len, 0); let acc = 0;
      for (const st of gr.strokes) {
        g.strokeStyle = st.stroke; g.lineWidth = st.width;
        const frac = gr.parallel ? p : cl((p * total - acc) / st.len);
        drawPrefix(st, frac); acc += st.len;
      }
      g.setLineDash([]);
    }
  }
}
window.renderFrame = i => render(i / S.fps);
window.info = () => ({ frames: Math.round(S.duration * S.fps), items: items.length });
window.ready = true;
</script>
</body></html>
````

## p4_track.py

P4, шаг 1: измерение и трекинг лимба в видео NASA, кадры и data/p4_track.json.

````python
"""P4 step 1: measure and track the limb in NASA footage, export frames + track.json for the overlay page.

Footage: NASA jsc2022m000172 (Earth from Space in 4K - Expedition 65 Edition), 4096x2160, 29.97 fps.
Excerpt: tmp/probes/media/exp65_excerpt_2470s.mp4 (stream copy of 41:10-41:46); used 41:13.0 + 240 frames.
Frames are rotated 180 deg (Earth below, space above). No other change to the pixels.

Measurement, per frame, on the full 4K picture:
  * y_top(x): top of the visible blue glow = where the blue channel first reaches 12/255 coming down from space
    (followed by >40 within 40 px, so stars do not count), sub-pixel by linear interpolation.
  * y_red(x): where the red channel reaches 30/255 below y_top: the lower, hazy/cloudy air starts to show.
  * Camera model: pinhole (rectilinear lens, no distortion), principal point at the frame centre. The limb is the
    circle of directions at angle rho from nadir, sin(rho) = (R + h) / (R + H_ISS). Fit focal length f and the
    nadir direction to the y_top points (scipy least_squares). f is shared by all frames (median), the nadir
    direction is per frame and smoothed in time (Gaussian, sigma 4 frames).
  * Scale at the limb: 1 px across the limb = D * dtheta km, D = distance to the tangent point.
"""
import json, math, os, subprocess, sys
import numpy as np
import cv2
from scipy.optimize import least_squares
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
SRC = os.path.join(ROOT, 'media', 'exp65_excerpt_2470s.mp4')
OUTD = os.path.join(ROOT, 'frames', 'p4')
os.makedirs(OUTD, exist_ok=True)
FF = '/home/boardagent/.explainer/bin/ffmpeg'
W4, H4, NF, T0 = 4096, 2160, 240, 3.0
CX, CY = (W4 - 1) / 2, (H4 - 1) / 2
R_E, H_ISS = 6371.0, 420.0           # km; ISS mean altitude during Expedition 65 (Apr-Oct 2021) ~420 km (assumption, +-10 km)
XS = np.arange(96, 4001, 48)
CROP_X = 128                         # output = 4K crop x 128..3968 (3840x2160) scaled by 1/2 -> 1920x1080
LOUPE_X4 = 2560                      # column (4K) the loupe follows
LOUPE_W, LOUPE_H, LOUPE_K = 160, 120, 3   # loupe: 160x120 px of the 4K picture shown at 480x360 (3x of 4K, 6x of the 1080p view)

def _frames(start):
    cmd = [FF, '-loglevel', 'error', '-threads', '2', '-ss', f'{T0 + start * 1001 / 30000:.5f}', '-i', SRC, '-frames:v', str(NF - start),
           '-vf', 'hflip,vflip', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W4 * H4 * 3)
    for _ in range(NF - start):
        buf = p.stdout.read(W4 * H4 * 3)
        if len(buf) < W4 * H4 * 3: break
        yield np.frombuffer(buf, np.uint8).reshape(H4, W4, 3)
    p.stdout.close(); p.wait()

def frames():
    """NF frames. If the decoder dies early (it is killed under memory pressure on the shared host), restart it at the next frame."""
    i, tries = 0, 0
    while i < NF:
        n0 = i
        for fr in _frames(i):
            yield fr; i += 1
        if i == n0:
            tries += 1
            if tries > 5: raise RuntimeError(f'decoder gives no frames at {i}')
        else: tries = 0
        if i < NF: print(f'[decoder stopped at frame {i}, restarting]', flush=True)

def cross(v, thr, start):
    """first sub-pixel index >= start where v crosses thr upward"""
    idx = np.nonzero(v[start:] >= thr)[0]
    if not len(idx): return None
    i = start + idx[0]
    if i == 0: return float(i)
    a, b = v[i - 1], v[i]
    return i - 1 + min(max((thr - a) / max(b - a, 1e-6), 0.0), 1.0)   # fraction clamped: a may already be >= thr when i == start

def measure(fr):
    tops, reds = [], []
    for x in XS:
        col = fr[300:1500, x - 2:x + 3].astype(np.float32).mean(1)   # per column: keeps memory small (no 4K float copy)
        B, Rr = col[:, 2], col[:, 0]
        y = None; s = 0
        while True:
            yt = cross(B, 12.0, s)
            if yt is None: break
            j = int(yt)
            if B[j:j + 40].max() > 40: y = yt; break
            s = max(s + 1, j + 1)   # always advance (a crossing right at s gives j < s)
        if y is None: tops.append(np.nan); reds.append(np.nan); continue
        yr = cross(Rr, 30.0, int(y))
        tops.append(300 + y); reds.append(300 + yr if yr is not None else np.nan)
    return np.array(tops), np.array(reds)

def dirs(x, y, f):
    d = np.stack([(x - CX) / f, (y - CY) / f, np.ones_like(x)], -1)
    return d / np.linalg.norm(d, axis=-1, keepdims=True)
def nadir(u, v):
    n = np.array([u, v, 1.0]); return n / np.linalg.norm(n)
def rho_of(h):
    return math.asin((R_E + h) / (R_E + H_ISS))

def fit(x, y, rho, f0=None, uv0=(0.0, 2.7)):
    m = np.isfinite(y)
    x, y = x[m], y[m]
    if f0 is None:
        def res(p): return np.arccos(np.clip(dirs(x, y, p[0]) @ nadir(p[1], p[2]), -1, 1)) - rho
        r = least_squares(res, [3000.0, uv0[0], uv0[1]], x_scale=[1000, 1, 1])
        return r.x, r.fun
    def res(p): return np.arccos(np.clip(dirs(x, y, f0) @ nadir(p[0], p[1]), -1, 1)) - rho
    r = least_squares(res, list(uv0))
    return np.array([f0, *r.x]), r.fun

def limb_y(xq, f, n, rho, y_guess):
    """y on the model limb for columns xq (Newton on the angle)"""
    y = np.full(xq.shape, float(y_guess))
    for _ in range(30):
        a = np.arccos(np.clip(dirs(xq, y, f) @ n, -1, 1)); a2 = np.arccos(np.clip(dirs(xq, y + 0.5, f) @ n, -1, 1))
        y = y - (a - rho) / ((a2 - a) / 0.5)
    return y

# ---------------- pass 1: measure ----------------
TOP, RED = [], []
for i, fr in enumerate(frames()):
    t, r = measure(fr); TOP.append(t); RED.append(r)
    if i % 40 == 0: print(f'measure frame {i}: {np.isfinite(t).sum()} limb points', flush=True)
TOP, RED = np.array(TOP), np.array(RED)
nf = len(TOP)
band_px = RED - TOP                                     # blue-only layer, px (4K), per frame/column
band_med = float(np.nanmedian(band_px))

# self-consistent fit: the glow top sits at altitude h_top = band * km/px above the red edge (taken as ~0 km)
h_top = 0.0
for it in range(4):
    rho = rho_of(h_top)
    P = [fit(XS.astype(float), TOP[i], rho)[0] for i in range(0, nf, 8)]
    f = float(np.median([p[0] for p in P]))
    uv = []; res_all = []
    for i in range(nf):
        p, rr = fit(XS.astype(float), TOP[i], rho, f0=f, uv0=(P[0][1], P[0][2])); uv.append(p[1:]); res_all.append(rr)
    uv = np.array(uv)
    n_mid = nadir(*uv[nf // 2])
    D = math.sqrt((R_E + H_ISS) ** 2 - (R_E + h_top / 2) ** 2)      # tangent distance at mid-layer altitude
    y0 = limb_y(np.array([float(LOUPE_X4)]), f, n_mid, rho, 800)[0]
    a0 = math.acos(dirs(np.array([LOUPE_X4]), np.array([y0]), f)[0] @ n_mid)
    a1 = math.acos(dirs(np.array([LOUPE_X4]), np.array([y0 + 1.0]), f)[0] @ n_mid)
    km_px = D * abs(a1 - a0)
    h_new = band_med * km_px
    print(f'iter {it}: rho={math.degrees(rho):.3f} deg f={f:.0f} px  km/px(4K)={km_px:.4f}  band={band_med:.1f} px = {h_new:.1f} km')
    if abs(h_new - h_top) < 0.5: h_top = h_new; break
    h_top = h_new
res_px = np.concatenate(res_all) / abs(a1 - a0)          # angular residual -> px
print(f'fit residual rms {np.sqrt(np.nanmean(res_px ** 2)):.2f} px over {np.isfinite(res_px).sum()} points')

# focal length -> horizontal field of view of the 4096 px frame
hfov = 2 * math.degrees(math.atan(W4 / 2 / f))
uv_s = np.stack([gaussian_filter1d(uv[:, k], 4, mode='nearest') for k in range(2)], 1)
band_s = gaussian_filter1d(np.nanmedian(band_px[:, 30:60], axis=1), 4, mode='nearest')

# ---------------- pass 2: export frames + track ----------------
track = []
xq = np.arange(0, W4 + 1, 32).astype(float)
for i, fr in enumerate(frames()):
    n = nadir(*uv_s[i])
    yl = limb_y(xq, f, n, rho, 800)
    yc = float(limb_y(np.array([float(LOUPE_X4)]), f, n, rho, 800)[0])
    yr = yc + float(band_s[i])
    bg = cv2.resize(fr[:, CROP_X:CROP_X + 3840], (1920, 1080), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(OUTD, f'bg{i:04d}.jpg'), cv2.cvtColor(bg, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 94])
    # loupe: the glow top sits at 40 % of the loupe height
    ox, oy = int(round(LOUPE_X4 - LOUPE_W / 2)), int(round(yc - 0.40 * LOUPE_H))
    lp = cv2.resize(fr[oy:oy + LOUPE_H, ox:ox + LOUPE_W], (LOUPE_W * LOUPE_K, LOUPE_H * LOUPE_K), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(OUTD, f'lp{i:04d}.png'), cv2.cvtColor(lp, cv2.COLOR_RGB2BGR))
    track.append(dict(
        limb=[[round((x - CROP_X) / 2, 1), round(y / 2, 1)] for x, y in zip(xq, yl)],
        pt=[(LOUPE_X4 - CROP_X) / 2, yc / 2], top_in_loupe=(yc - oy) * LOUPE_K, red_in_loupe=(yr - oy) * LOUPE_K, src=[(ox - CROP_X) / 2, oy / 2]))
    if i % 40 == 0: print(f'export frame {i}', flush=True)

meta = dict(nasa_id='jsc2022m000172_Earth_in_4K_Expedition_65_Edition', excerpt_start_s=2470 + T0, frames=nf,
            f_px_4k=f, hfov_deg=hfov, rho_deg=math.degrees(rho), D_km=D, km_per_px_4k=km_px,
            km_per_px_out=km_px * 2, loupe_k=LOUPE_K, loupe_w=LOUPE_W, loupe_h=LOUPE_H, band_px_4k=band_med, band_km=band_med * km_px,
            h_iss_km=H_ISS, residual_rms_px=float(np.sqrt(np.nanmean(res_px ** 2))), track=track)
json.dump(meta, open(os.path.join(ROOT, 'data', 'p4_track.json'), 'w'))
print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in meta.items() if k != 'track'}, indent=1))
````

## p4.html

P4, шаг 2: подписи, лупа и шкала поверх кадров NASA.

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="/src/common.css">
<style>
  img { position: absolute; display: block; }
  canvas { position: absolute; left: 0; top: 0; }
  .lab { position: absolute; white-space: nowrap; opacity: 0; text-shadow: 0 0 10px rgba(0,0,0,0.9), 0 0 3px rgba(0,0,0,0.9); }
  #lp { border: 2px solid rgba(233,238,246,0.9); box-sizing: border-box; opacity: 0; }
  .chip { position: absolute; opacity: 0; }
  .pill { background: rgba(10,14,23,0.72); padding: 3px 12px; border-radius: 6px; text-shadow: none; }
  .tag { background: rgba(10,14,23,0.82) !important; }
</style></head>
<body>
<img id="bg" style="left:0;top:0;width:1920px;height:1080px">
<img id="lp" style="left:0;top:0;width:480px;height:360px">
<canvas id="cv" width="1920" height="1080"></canvas>

<div class="lab" id="title" style="left:72px; top:48px;"><span class="h1">Earth's edge from the ISS</span><br><span class="h2" style="font-size:24px">NASA footage, pixels unchanged (rotated 180°)</span></div>
<div class="lab" id="lGlow" style="font-size:30px; color:var(--exact); font-weight:700;">visible blue glow<br><span style="font-size:42px">≈ 24 km</span> <span style="font-size:22px; font-weight:400; color:var(--ink2)">thick</span></div>
<div class="lab pill" id="lLimb" style="font-size:22px; color:#cfe6ff;">tracked edge, fit error 1.9 px</div>
<div class="lab" id="lBar" style="font-size:24px; color:var(--ink);">100 km</div>
<div class="lab" id="lLp" style="font-size:24px; color:var(--exact); font-weight:700;">≈ 24 km</div>
<div class="lab" id="lFact" style="left:72px; top:190px; font-size:32px;">24 km is <b>0.4 %</b> of Earth's radius<br><span style="font-size:22px; color:var(--ink2)">radius 6,371 km</span></div>

<div class="chip" id="cMeas" style="left:72px; top:918px;"><span class="tag exact">Measured <span class="rest">edge tracked in all 240 frames · 1.49 km per pixel at the edge (valid at the edge only)</span></span></div>
<div class="chip" id="cAssume" style="left:72px; top:984px;"><span class="tag model">Assumed <span class="rest">ISS altitude 420 ± 10 km · flat lens model · glow ends where the colour threshold is crossed</span></span></div>
<div class="lab pill" id="credit" style="right:40px; top:1046px; font-size:16px; color:var(--ink2);">NASA, JSC · Earth from Space in 4K, Expedition 65 · jsc2022m000172</div>

<script type="module">
const FPS = 30, NF = 240;
const D = await (await fetch('/data/p4_track.json')).json();
const tr = D.track;
const $ = id => document.getElementById(id);
const cl = x => Math.max(0, Math.min(1, x));
const sm = x => { x = cl(x); return x * x * x * (x * (6 * x - 15) + 10); };
const cv = $('cv'), g = cv.getContext('2d');
const bg = $('bg'), lp = $('lp');
const GREEN = '#7ee0a1';
const LK = D.loupe_k, LW = D.loupe_w * LK, LH = D.loupe_h * LK;     // loupe size on screen, px
const INSET = { x: 1340, y: 548, w: LW, h: LH };

async function load(img, src) { img.src = src; await img.decode(); }
function limbY(f, x) {                                              // y of the tracked limb at screen x (polyline, linear)
  const L = f.limb; if (x <= L[0][0]) return L[0][1];
  for (let k = 1; k < L.length; k++) if (x <= L[k][0]) { const a = L[k - 1], b = L[k]; return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]); }
  return L[L.length - 1][1];
}
function put(id, a, x, y) { const el = $(id); el.style.opacity = a; if (x !== undefined) { el.style.left = x + 'px'; el.style.top = y + 'px'; } }

window.renderFrame = async (i) => {
  const t = i / FPS, f = tr[i], n = String(i).padStart(4, '0');
  await load(bg, `/frames/p4/bg${n}.jpg`); await load(lp, `/frames/p4/lp${n}.png`);
  g.clearRect(0, 0, 1920, 1080);
  const [px, py] = f.pt, bandOut = (f.red_in_loupe - f.top_in_loupe) / LK / 2;   // glow thickness in 1080p px

  put('title', sm((t - 0.3) / 0.6) * (1 - sm((t - 4.6) / 0.6)));
  put('credit', sm((t - 0.3) / 0.6));

  // 1. tracked limb draws on from left to right, then fades out when the loupe has taken over
  const dr = sm((t - 0.9) / 1.3), fadeL = 1 - sm((t - 4.6) / 0.7);
  if (dr > 0 && fadeL > 0) {
    const xs = f.limb.filter(p => p[0] <= -64 + dr * 2100);
    g.strokeStyle = `rgba(207,230,255,${0.9 * fadeL})`; g.lineWidth = 3; g.setLineDash([14, 8]); g.beginPath();
    xs.forEach((p, k) => k ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.stroke(); g.setLineDash([]);
    put('lLimb', sm((t - 1.7) / 0.5) * fadeL, 150, limbY(f, 330) + 56);
  } else put('lLimb', 0);

  // 2. bracket across the glow at the loupe column, label above it
  const bk = sm((t - 2.2) / 0.6), grow = sm((t - 2.2) / 0.7);
  if (bk > 0) {
    const y0 = py - 4, y1 = py - 4 + bandOut * grow;
    g.strokeStyle = GREEN; g.globalAlpha = bk; g.lineWidth = 3; g.beginPath();
    g.moveTo(px - 12, y0); g.lineTo(px + 12, y0); g.moveTo(px, y0); g.lineTo(px, y1); g.moveTo(px - 12, y1); g.lineTo(px + 12, y1); g.stroke();
    g.lineWidth = 2; g.beginPath(); g.moveTo(px + 26, y0 + (y1 - y0) / 2); g.lineTo(px + 120, y0 - 56); g.stroke(); g.globalAlpha = 1;
    put('lGlow', sm((t - 2.6) / 0.5), px + 130, y0 - 140);
  } else put('lGlow', 0);

  // 3. loupe: the small rectangle around the bracket grows into the inset; connector lines follow its corners
  const e = sm((t - 3.0) / 1.0);
  const sx = f.src[0], sy = f.src[1], sw = D.loupe_w / 2, sh = D.loupe_h / 2;     // source rectangle on screen (1080p px)
  const r = { x: sx + (INSET.x - sx) * e, y: sy + (INSET.y - sy) * e, w: sw + (INSET.w - sw) * e, h: sh + (INSET.h - sh) * e };
  const la = sm((t - 3.0) / 0.4);
  if (la > 0) {
    g.strokeStyle = `rgba(233,238,246,${0.55 * la})`; g.lineWidth = 2;
    g.strokeRect(sx, sy, sw, sh);
    g.beginPath(); g.moveTo(sx, sy + sh); g.lineTo(r.x, r.y); g.moveTo(sx + sw, sy); g.lineTo(r.x + r.w, r.y); g.stroke();
    lp.style.opacity = 1; lp.style.left = r.x + 'px'; lp.style.top = r.y + 'px'; lp.style.width = r.w + 'px'; lp.style.height = r.h + 'px';
    // the glow measured in the loupe: two edges and a bracket
    const k = r.w / LW, ye = sm((t - 4.0) / 0.6);
    if (ye > 0) {
      const yt = r.y + f.top_in_loupe * k, yr = r.y + f.red_in_loupe * k, bx = r.x + r.w - 56;
      g.strokeStyle = GREEN; g.globalAlpha = ye; g.lineWidth = 3; g.beginPath();
      g.moveTo(bx - 12, yt); g.lineTo(bx + 12, yt); g.moveTo(bx, yt); g.lineTo(bx, yr); g.moveTo(bx - 12, yr); g.lineTo(bx + 12, yr); g.stroke();
      g.lineWidth = 1.5; g.setLineDash([6, 6]); g.beginPath(); g.moveTo(r.x, yt); g.lineTo(bx - 14, yt); g.moveTo(r.x, yr); g.lineTo(bx - 14, yr); g.stroke(); g.setLineDash([]); g.globalAlpha = 1;
      put('lLp', ye, bx - 112, (yt + yr) / 2 - 16);
    } else put('lLp', 0);
  } else { lp.style.opacity = 0; put('lLp', 0); }

  // 4. measured scale bar: 100 km at the limb (1.49 km per px); sits on the tracked limb to the left of the loupe column
  const sb = sm((t - 5.0) / 0.6);
  if (sb > 0) {
    const L100 = 100 / D.km_per_px_out, bx = 560, by = limbY(f, bx + L100 / 2) - 52;
    g.strokeStyle = `rgba(233,238,246,${sb})`; g.lineWidth = 3; g.beginPath();
    g.moveTo(bx, by); g.lineTo(bx + L100, by); g.moveTo(bx, by - 9); g.lineTo(bx, by + 9); g.moveTo(bx + L100, by - 9); g.lineTo(bx + L100, by + 9); g.stroke();
    put('lBar', sb, bx + L100 + 14, by - 15);
  } else put('lBar', 0);

  put('lFact', sm((t - 6.0) / 0.6));
  put('cMeas', sm((t - 3.4) / 0.6)); put('cAssume', sm((t - 3.6) / 0.6));
};
window.info = () => ({ frames: NF, track: tr.length, km_per_px: D.km_per_px_out, band_km: D.band_km });
window.ready = true;
</script>
</body></html>
````
