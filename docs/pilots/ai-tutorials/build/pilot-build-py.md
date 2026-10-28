# tmp/pilot/build.py

Сборка страницы пилота: pilot.html, timeline.json, captions.srt.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/build.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Writes pilot.html (driven by render(t)), timeline.json and captions.srt from shots.py."""
import json, os
import shots
from engine import *

FILT = ('<filter id="grainA" x="0" y="0" width="100%" height="100%"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="1" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -.75"/><feComposite in2="SourceGraphic" operator="in"/></filter>'
        '<filter id="gl" x="-10%" y="0" width="120%" height="100%"><feTurbulence id="gturb" type="turbulence" baseFrequency="0 .045" numOctaves="1" seed="1"/>'
        '<feColorMatrix values="1 0 0 0 0  0 0 0 0 .5  0 0 0 0 0  0 0 0 0 1"/><feDisplacementMap id="gdm" in="SourceGraphic" scale="0" xChannelSelector="R" yChannelSelector="G"/></filter>')

JS = r'''
const $ = (i) => document.getElementById(i);
const cl = (x) => Math.max(0, Math.min(1, x));
const p = (t, a, b) => b <= a ? (t >= a ? 1 : 0) : cl((t - a) / (b - a));
const oc = (x) => 1 - Math.pow(1 - x, 3);
const ic = (x) => x * x * x;
const ob = (x) => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const rnd = (n) => { const s = Math.sin(n * 127.1 + 3.7) * 43758.5453; return s - Math.floor(s); };
const SH = DATA.shots, BY = {};
DATA.els.forEach((e) => (BY[e.s] = BY[e.s] || []).push(e));
const G = {}; DATA.els.forEach((e) => { G[e.id] = $(e.id); });
function draw(g, k) { g.querySelectorAll('text, path').forEach((e) => { e.style.strokeDasharray = 2400; e.style.strokeDashoffset = 2400 * (1 - k); }); }
function rv(g, k) { g.querySelectorAll('.rv').forEach((r) => r.setAttribute('width', r.dataset.w * k)); }
function glitch(g, amt, f) {
  g.querySelectorAll('.sl').forEach((s, k) => s.setAttribute('transform', `translate(${(rnd(f * 7 + k) - .5) * 2 * amt} 0)`));
  g.querySelectorAll('.gh').forEach((s) => s.setAttribute('transform', `translate(${s.dataset.k * (amt > 0 ? 4 + amt * .4 : 0)} 0)`));
}
function cycle(g, idx) { g.querySelectorAll('.cf').forEach((c) => c.setAttribute('display', +c.dataset.i === idx ? 'inline' : 'none')); }
function el(e, t, f, sh) {
  const g = G[e.id]; if (!g) return;
  const vis = t >= e.t, k = p(t, e.t, e.t + e.d);
  let x = 0, y = 0, r = 0, s = 1, op = vis ? 1 : 0;
  switch (e.a) {
    case 'none': op = 1; break;
    case 'fade': op = oc(k); break;
    case 'slideL': x = -1900 * (1 - ob(k)); r = -9 * (1 - oc(k)); break;
    case 'slideR': x = 1900 * (1 - ob(k)); r = 9 * (1 - oc(k)); break;
    case 'drop': y = -1100 * (1 - ob(k)); r = 8 * (1 - oc(k)); break;
    case 'rise': y = 300 * (1 - oc(k)); op = cl(k * 2); break;
    case 'stamp': s = 2.2 - 1.2 * oc(k); r = -14 * (1 - k); break;
    case 'pop': s = .3 + .7 * ob(k); break;
    case 'zoom': s = 1.6 - .6 * oc(k); break;
    case 'draw': draw(g, oc(k)); break;
    case 'type': rv(g, Math.floor(k * 36) / 36); break;
    case 'wipe': rv(g, oc(k)); break;
    case 'flick': op = !vis ? 0 : (k >= 1 ? 1 : (rnd(f * 3 + e.t) > .45 ? 1 : .1)); break;
  }
  if (e.glitch) { const [a, amt] = e.glitch; const hot = t >= a && (t < a + .6 || f % 23 < 3); glitch(g, hot ? 30 * amt : 0, f); }
  if (e.shake) { const [a, b, amp] = e.shake; if (t >= a && t < b) { x += (rnd(f) - .5) * 2 * amp; r += (rnd(f + 7) - .5) * amp * .5; } }
  if (e.cycle) { const [a, b, fin] = e.cycle, n = g.querySelectorAll('.cf').length;
    cycle(g, t < a ? (fin + 2) % n : (t < b ? Math.floor(rnd(Math.floor(f / 3) + e.t) * n) % n : fin)); }
  if (e.mv) { const [a, d, dx, dy, ds] = e.mv, q = oc(p(t, a, a + d)); x += dx * q; y += dy * q; s *= 1 + ds * q; }
  if (e.o) { const [a, kind] = e.o, q = p(t, a, a + .35);
    if (kind === 'fade') op *= 1 - q;
    else if (kind === 'fall') { y += 1300 * q * q; r += 25 * q; }
    else if (kind === 'glitch') { if (t >= a) { glitch(g, 45, f); if (t > a + .3) op = 0; } } }
  const [cx, cy] = g.dataset.c.split(' ').map(Number);
  g.setAttribute('transform', `translate(${x} ${y}) translate(${cx} ${cy}) rotate(${r}) scale(${s}) translate(${-cx} ${-cy})`);
  g.setAttribute('opacity', op);
}
let cur = -1;
window.render = (t) => {
  const f = Math.round(t * 30);
  let i = 0; while (i + 1 < SH.length && SH[i + 1].t0 <= t) i++;
  const sh = SH[i];
  if (sh.n !== cur) { SH.forEach((q) => { $('shot' + q.n).style.display = q.n === sh.n ? '' : 'none'; }); $('sec').textContent = sh.sec; cur = sh.n; }
  $('turb').setAttribute('seed', f % 9 + 1);
  (BY[sh.n] || []).forEach((e) => el(e, t, f, sh));
  // cut effects: glitch burst, or a torn lime sheet that crosses the frame
  let gk = 0, tx = 2000;
  for (const q of SH) {
    if (q.n === 1) continue;
    if (q.tr === 'glitch' && t > q.t0 - .12 && t < q.t0 + .25) gk = Math.sin(Math.PI * p(t, q.t0 - .12, q.t0 + .25));
    if (q.tr === 'tear' && t > q.t0 - .35 && t < q.t0 + .35) tx = t < q.t0 ? -1900 + 1800 * oc(p(t, q.t0 - .35, q.t0)) : -100 + 1800 * ic(p(t, q.t0, q.t0 + .35));
  }
  $('root').setAttribute('filter', gk > .02 ? 'url(#gl)' : '');
  $('gdm').setAttribute('scale', gk * 140); $('gturb').setAttribute('seed', f % 13 + 1);
  $('tear').setAttribute('transform', `translate(${tx} 0)`);
  $('tear').setAttribute('display', tx < 1700 ? 'inline' : 'none');
};
render(0);
'''

def tear():
  return (f'<g id="tear" display="none"><g transform="translate(16 0)" opacity=".5">{paper(0, -60, 1800, 1020, "#000", 401, amp=16, sides="rl")}</g>'
          + paper(0, -60, 1800, 1020, LIME, 401, amp=16, sides='rl', rim='#fff')
          + halftone(1500, -20, 300, 940, 14, INK, 402, base=.75, soft=.4) + '</g>')

def hud():
  return (f'<g id="hud"><text id="sec" x="40" y="36" font-family="{M}" font-size="16" font-weight="700" fill="{GRAY}" letter-spacing="3"></text>'
          f'<rect x="1562" y="24" width="26" height="150" fill="{INK}"/>' + vtext(1581, 166, 'TOY MODEL', 16, LIME, M, -90, ls=4) + '</g>')

def page(shots, els, scenes, title, w=1600, h=900, wrap=None, css='', js=''):
  data = json.dumps(dict(shots=shots, els=els), separators=(',', ':'))
  inner = f'<g id="root"><g id="shots">{scenes}</g>{tear()}{hud()}<rect id="grain" width="1600" height="900" fill="#fff" filter="url(#grainA)" opacity=".13"/></g>'
  if wrap: inner = wrap(inner)
  return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>'
          f'<link href="https://fonts.googleapis.com/css2?{K.fonts}&display=swap" rel="stylesheet">'
          f'<style>html,body{{margin:0;background:#0B0B0B;overflow:hidden}}body>svg{{display:block;width:100vw;height:100vh}}{css}</style></head><body>'
          f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs>{DEFS}{FILT}</defs>{inner}</svg>'
          f'<script>const DATA = {data};{JS}{js}</script></body></html>')

if __name__ == '__main__':
  sh, els, caps = build()
  scenes = ''.join(f'<g id="shot{s.n}" style="display:none">{s.body}</g>' for s in SHOTS)
  html = page(sh, els, scenes, 'Countable AI pilot')
  open(os.path.join(HERE, 'pilot.html'), 'w').write(html)
  json.dump(dict(shots=sh, els=els), open(os.path.join(HERE, 'timeline.json'), 'w'), indent=0)
  open(os.path.join(HERE, 'captions.srt'), 'w').write(srt(caps))
  print(len(html), 'bytes;', sh[-1]['t1'], 's;', len(caps), 'captions')
````
