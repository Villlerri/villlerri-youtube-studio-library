# tmp/mock/anim.py

Видеопроба Swiss Bold 18 с: страница anim.html.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/anim.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Motion probe for the reworked Swiss Bold: tmp/mock/anim.html, 18 s, driven by render(t).
cap.mjs screenshots it frame by frame; ffmpeg joins the frames."""
from gen4 import (DEFS, INK, WHITE, LIME, RED, GRAY, MSGS, T, tw, ttext, outline, paper, tape, card, reg, vtext,
                  halftone, streaks, marker, K, uid, esc, COND)

D = K.disp; M = K.mono

def g(i, body, cx=0, cy=0, cls=''):
  return f'<g id="{i}" data-c="{cx} {cy}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{body}</g>'

def gl(i, x, y, s, size, col, ghosts=(LIME, RED)):
  """Glitch-ready text: two colour ghosts and five slices the script shifts sideways."""
  o = ''.join(f'<g class="gh" data-k="{k*2-1}">{ttext(x, y, s, size, c, D)}</g>' for k, c in enumerate(ghosts))
  top = y - size * .78; h = size * .82
  for k in range(5):
    cid = uid('cl'); y0 = top + h * k / 5
    o += f'<clipPath id="{cid}"><rect x="{x-200}" y="{y0:.1f}" width="2400" height="{h/5+.6:.1f}"/></clipPath><g clip-path="url(#{cid})"><g class="sl">{ttext(x, y, s, size, col, D)}</g></g>'
  return g(i, o, x, y)

def bg(): return f'<rect width="1600" height="900" fill="{INK}"/>'

# --- scene 1: training data
s1 = bg() + g('o1', outline(60, 760, '3/3', 760, set(), D, stroke='#3A3A36', sw=3), cls='draw')
s1 += g('v1', vtext(70, 120, 'TRAINING DATA — EVERYTHING IT EVER READ', 22, LIME, M, 90, ls=4))
for j, m in enumerate(MSGS):
  cy = 230 + j * 205; rot = [-2.2, 1.6, -1.2][j]; x = 200 + j * 40; fill = LIME if j == 1 else WHITE
  body = (f'<g transform="rotate({rot} 800 {cy})"><g transform="translate(12 16)" opacity=".6">{paper(x, cy-80, 1180, 160, "#000", j+20, amp=6)}</g>'
          f'{paper(x, cy-80, 1180, 160, fill, j+20, amp=6, rim="#fff")}{ttext(x + 50, cy + 48, m.upper(), min(132, 940 * 100 / tw(m.upper(), 100)), INK, D)}'
          f'{T(x + 1130, cy + 18, "TRUE", 30, INK, M, 700, "end", 3)}</g>')
  s1 += g(f'st{j}', body, 800, cy) + g(f'tp{j}', tape(x - 40, cy - 100, 150, 46, -14 + j * 8, j + 30), x + 35, cy - 77)
s1 += g('c1', T(1530, 860, '3 / 3 TRUE', 30, LIME, M, 700, 'end', 3))

# --- scene 2: the blank and three cards
s2 = bg() + g('ht2', halftone(700, -20, 920, 940, 16, LIME, 5, base=.62, soft=.3)) + g('sk2', streaks(700, -20, 920, 940, LIME, 5, base=.62, n=34))
cx = 90
for k, wd in enumerate(['MOM', 'IS', 'AT', 'THE']):
  s2 += g(f'w{k}', ttext(cx, 190, wd, 180, WHITE, D), cx + tw(wd, 180) / 2, 130); cx += tw(wd + ' ', 180)
s2 += g('q2', marker(cx, 60, 260, 160, -3, 8, WHITE) + ttext(cx + 130, 192, '?', 170, INK, D, anchor='middle'), cx + 130, 140)
for j, wd in enumerate(['STORE', 'GYM', 'PARK']):
  ccx = 300 + j * 480; rot = [-6, 3, -2][j]
  inner = ttext(0, -40, wd, 150, INK, D, anchor='middle') + f'<path d="M-150 10H150" stroke="{INK}" stroke-width="4"/>'
  inner += f'<g class="draw">{outline(0, 190, "1/3", 190, {0}, D, stroke=INK, sw=3, lime=RED if j == 1 else INK, anchor="middle")}</g>'
  inner += reg(-150, -190, 14, INK) + reg(150, -190, 14, INK)
  s2 += g(f'cd{j}', card(ccx, 560, 380, 470, rot, inner, j + 40), ccx, 560)
s2 += g('v2', vtext(1560, 40, 'IT SEES ONLY THE LAST WORD: "THE"', 22, INK, M, 90, ls=3))

# --- scene 3: the false sentence
fs = min(150, 500 * 100 / tw('THE GYM.', 100))
s3 = bg() + g('lp', paper(-40, -40, 860, 980, LIME, 61, amp=14, sides='r', rim='#fff') + halftone(790, -20, 200, 940, 12, LIME, 61, base=.0, soft=.9, flip=True))
s3 += g('big3', ttext(30, 600, '2/3', 620, INK, D, ls=-10), 330, 400)
s3 += g('sub3', ttext(50, 730, 'OF ITS SENTENCES', 84, INK, D) + ttext(50, 820, 'ARE FALSE', 84, INK, D))
s3 += g('m3', ttext(1000, 210, 'MOM IS AT', fs, WHITE, D)) + gl('g3', 1000, 210 + fs * .95, 'THE GYM.', fs, WHITE)
s3 += g('ft', f'<g transform="rotate(-6 1420 420)">{paper(1310, 385, 220, 70, RED, 70, amp=5, sides="rl")}{T(1420, 434, "FALSE", 40, WHITE, M, 700, "middle", 6)}</g>', 1420, 420)
for j in range(9):
  x = 1000 + (j % 3) * 180; y = 490 + (j // 3) * 128; ok = j % 4 == 0; rr = (j * 37 % 7 - 3) * .8
  s3 += g(f'gq{j}', f'<g transform="rotate({rr:.1f} {x+82} {y+54})" filter="url(#rough)">{paper(x, y, 165, 108, WHITE if ok else RED, j + 80, amp=3)}{T(x+82, y+68, "TRUE" if ok else "FALSE", 34, INK if ok else WHITE, M, 700, "middle")}</g>', x + 82, y + 54)

# --- scene 4: end card
word = 'COUNTABLE AI'; sz = 1100 * 100 / tw(word, 100, 'wide200')
s4 = bg() + g('h4r', halftone(1390, -20, 230, 940, 14, LIME, 4, base=.5, soft=.4) + streaks(1390, -20, 230, 940, LIME, 4, base=.5, n=40, maxlen=.7))
s4 += g('h4l', halftone(-20, -20, 200, 940, 14, LIME, 6, base=.55, soft=.4, flip=True))
s4 += g('ttl', outline(240, 500, word, round(sz), set(), D, sw=2.5), cls='draw')
ax = 240 + tw('COUNTABLE ', sz, 'wide200')
s4 += g('ai4', f'<text x="{ax:.1f}" y="500" font-family="{D}" font-size="{round(sz)}" font-weight="200" fill="{LIME}" style="font-stretch:125%">AI</text>')
s4 += f'<clipPath id="tgc"><rect id="tgr" x="240" y="540" width="0" height="60"/></clipPath>'
s4 += f'<g clip-path="url(#tgc)">{T(244, 580, "HOW AI WORKS — ON EXAMPLES YOU CAN COUNT", 30, LIME, M, 700, ls=3)}</g>'

FILT = ('<filter id="grainA" x="0" y="0" width="100%" height="100%"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="1" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -.75"/><feComposite in2="SourceGraphic" operator="in"/></filter>'
        '<filter id="gl" x="-10%" y="0" width="120%" height="100%"><feTurbulence id="gturb" type="turbulence" baseFrequency="0 .045" numOctaves="1" seed="1"/>'
        '<feColorMatrix values="1 0 0 0 0  0 0 0 0 .5  0 0 0 0 0  0 0 0 0 1"/><feDisplacementMap id="gdm" in="SourceGraphic" scale="0" xChannelSelector="R" yChannelSelector="G"/></filter>')

JS = r'''
const $ = (i) => document.getElementById(i);
const cl = (x) => Math.max(0, Math.min(1, x));
const p = (t, a, b) => cl((t - a) / (b - a));
const oc = (x) => 1 - Math.pow(1 - x, 3);
const ob = (x) => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const rnd = (n) => { const s = Math.sin(n * 127.1) * 43758.5453; return s - Math.floor(s); };
function tf(i, o) {
  const e = $(i); if (!e) return; const [cx, cy] = e.dataset.c.split(' ').map(Number);
  const { x = 0, y = 0, r = 0, s = 1, op = 1 } = o;
  e.setAttribute('transform', `translate(${x} ${y}) translate(${cx} ${cy}) rotate(${r}) scale(${s}) translate(${-cx} ${-cy})`);
  e.setAttribute('opacity', op);
}
function draw(sel, k) { document.querySelectorAll(sel).forEach((e) => { e.style.strokeDasharray = 2400; e.style.strokeDashoffset = 2400 * (1 - k); }); }
function glitch(i, amt, f) {
  const e = $(i); if (!e) return;
  e.querySelectorAll('.sl').forEach((s, k) => s.setAttribute('transform', `translate(${(rnd(f * 7 + k) - .5) * 2 * amt} 0)`));
  e.querySelectorAll('.gh').forEach((s) => s.setAttribute('transform', `translate(${s.dataset.k * (4 + amt * .4)} 0)`));
}
function scene(n) { for (const k of [1, 2, 3, 4]) $('s' + k).style.display = k === n ? '' : 'none'; }
window.render = (t) => {
  const f = Math.round(t * 30);
  $('turb').setAttribute('seed', f % 9 + 1);
  // whole-frame glitch bursts at the cuts
  const burst = (a, b) => (t >= a && t < b) ? Math.sin(Math.PI * p(t, a, b)) : 0;
  const gk = Math.max(burst(9.35, 9.75), burst(14.75, 15.15), .25 * burst(8.6, 8.8), .25 * burst(8.95, 9.1));
  $('gdm').setAttribute('scale', gk * 140); $('gturb').setAttribute('seed', f % 13 + 1);
  if (t < 4.75) {
    scene(1);
    draw('#o1 text', oc(p(t, 0, 3.5)));
    tf('v1', { y: 300 * (1 - oc(p(t, .1, .8))), op: p(t, .1, .5) });
    for (let j = 0; j < 3; j++) {
      const a = .35 + j * .7, k = p(t, a, a + .55);
      tf('st' + j, { x: -1900 * (1 - ob(k)), r: -9 * (1 - oc(k)) });
      const q = p(t, a + .5, a + .62); tf('tp' + j, { s: .3 + .7 * ob(q), op: q > 0 ? 1 : 0 });
    }
    tf('c1', { op: (t > 3.0 && (f % 4 < 3 || t > 3.4)) ? 1 : 0 });
  } else if (t < 9.55) {
    scene(2);
    tf('ht2', { x: 700 * (1 - oc(p(t, 4.75, 5.4))) });
    tf('sk2', { x: (rnd(f) - .5) * 30 + 500 * (1 - oc(p(t, 4.75, 5.5))) });
    for (let k = 0; k < 4; k++) { const q = p(t, 5.0 + k * .2, 5.2 + k * .2); tf('w' + k, { s: 1.6 - .6 * oc(q), op: q > 0 ? 1 : 0 }); }
    const q2 = p(t, 5.9, 6.1); tf('q2', { s: .2 + .8 * ob(q2), r: 10 * (1 - q2), op: q2 > 0 ? (t > 6.3 && f % 10 < 2 ? .4 : 1) : 0 });
    for (let j = 0; j < 3; j++) {
      const a = 6.2 + j * .3, k = p(t, a, a + .5);
      const lift = j === 1 ? p(t, 8.4, 9.3) : 0;
      tf('cd' + j, { y: -1100 * (1 - ob(k)) - 70 * oc(lift), r: (j - 1) * 14 * (1 - oc(k)) + (j === 1 ? (rnd(f) - .5) * 6 * (t > 8.1 ? 1 : 0) : 0), s: 1 + .08 * lift });
    }
    draw('#s2 .draw text', oc(p(t, 7.1, 8.0)));
  } else if (t < 14.95) {
    scene(3);
    tf('lp', { x: -900 * (1 - oc(p(t, 9.55, 10.0))) });
    const b = p(t, 10.05, 10.3); tf('big3', { s: 1.5 - .5 * oc(b), op: b > 0 ? 1 : 0 });
    tf('sub3', { y: 40 * (1 - oc(p(t, 13.5, 13.9))), op: p(t, 13.5, 13.8) });
    tf('m3', { x: 120 * (1 - oc(p(t, 10.4, 10.8))), op: p(t, 10.4, 10.6) });
    tf('g3', { x: 120 * (1 - oc(p(t, 10.7, 11.1))), op: p(t, 10.7, 10.9) });
    const hot = (t > 10.7 && t < 11.3) || (f % 23 < 3);
    glitch('g3', hot ? 30 : 0, f);
    const s = p(t, 11.4, 11.6); tf('ft', { s: 2.2 - 1.2 * oc(s), r: -14 * (1 - s), op: s > 0 ? 1 : 0 });
    for (let j = 0; j < 9; j++) { const q = p(t, 11.9 + j * .17, 12.05 + j * .17); tf('gq' + j, { s: 1.7 - .7 * oc(q), op: q > 0 ? 1 : 0 }); }
  } else {
    scene(4);
    tf('h4r', { x: 420 * (1 - oc(p(t, 14.95, 15.6))) }); tf('h4l', { x: -320 * (1 - oc(p(t, 14.95, 15.6))) });
    draw('#ttl text', oc(p(t, 15.1, 16.6)));
    tf('ai4', { op: t > 16.5 ? (t < 16.9 && f % 3 === 0 ? .2 : 1) : 0 });
    $('tgr').setAttribute('width', 1300 * p(t, 16.8, 17.5));
  }
};
render(0);
'''

html = (f'<!doctype html><html><head><meta charset="utf-8"><title>Swiss Rough motion</title>'
        f'<link href="https://fonts.googleapis.com/css2?{K.fonts}&display=swap" rel="stylesheet">'
        '<style>html,body{margin:0;background:#0B0B0B;overflow:hidden}svg{display:block;width:100vw;height:100vh}</style></head><body>'
        f'<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg"><defs>{DEFS}{FILT}</defs><g filter="url(#gl)">'
        f'<g id="s1">{s1}</g><g id="s2">{s2}</g><g id="s3">{s3}</g><g id="s4">{s4}</g>'
        '<rect width="1600" height="900" fill="#fff" filter="url(#grainA)" opacity=".13"/></g></svg>'
        f'<script>{JS}</script></body></html>')
open('anim.html', 'w').write(html)
print(len(html))
````
