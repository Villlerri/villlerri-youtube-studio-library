# tmp/pilot/shorts.py

Два вертикальных Shorts из кадров пилота.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/shorts.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Two vertical Shorts 1080x1920 from pilot shots: title on top, the 16:9 scene, burned-in narration, torn lime bottom."""
import json, os
from build import page
from engine import *

SH, ELS, CAPS = build()
BY = {s['n']: s for s in SH}

SHORTS = [
  dict(slug='short1-true-pieces', shots=(14, 16), title=['EVERY WORD WAS TRUE.', 'THE SENTENCE WAS FALSE.'], big='2/3', big_sub='WRONG',
       notes=['6 OF 9 SENTENCES', 'COUNT IT YOURSELF']),
  dict(slug='short2-guessing-wins', shots=(28, 30), title=['WHY GUESSING', 'WINS ON TESTS'], big='4 > 3', big_sub='GUESSER WINS', start=3.2,
       notes=['IN 19 OF 27 CASES', 'COUNT IT YOURSELF']),
]
W, H, SY = 1080, 1920, 600            # scene: 1080x607.5 at y=SY
CAP_Y = SY + 607.5 + 120

def wrap_for(sd):
  def wrap(inner):
    o = f'<rect width="{W}" height="{H}" fill="{INK}"/>'
    o += T(60, 92, 'COUNTABLE AI · TOY MODEL', 26, LIME, M, 700, ls=5)
    ts = min(130, 960 * 100 / max(tw(x, 100) for x in sd['title']))
    for k, ln in enumerate(sd['title']):
      o += ttext(60, 355 - .1 * ts + k * ts * .98, ln, ts, WHITE if k == 0 else LIME, D)
    o += f'<rect x="0" y="{SY - 6}" width="{W}" height="4" fill="{LIME}"/><rect x="0" y="{SY + 609.5}" width="{W}" height="4" fill="{LIME}"/>'
    o += f'<svg x="0" y="{SY}" width="{W}" height="607.5" viewBox="0 0 1600 900" overflow="hidden">{inner}</svg>'
    o += (f'<text id="cap0" x="{W/2}" y="{CAP_Y}" font-family="{D}" font-weight="900" font-size="50" fill="{WHITE}" text-anchor="middle" style="font-stretch:75%"></text>'
          f'<text id="cap1" x="{W/2}" y="{CAP_Y + 62}" font-family="{D}" font-weight="900" font-size="50" fill="{WHITE}" text-anchor="middle" style="font-stretch:75%"></text>')
    by = 1540
    o += f'<g transform="translate(0 -14)" opacity=".5">{paper(-30, by, W + 60, H - by + 40, "#000", 92, amp=14, sides="t")}</g>'
    o += paper(-30, by, W + 60, H - by + 40, LIME, 92, amp=14, sides='t', rim='#fff') + halftone(-10, by - 90, W + 20, 120, 12, LIME, 92, base=.7, soft=.6)
    bs = min(300, 560 * 100 / tw(sd['big'], 100))
    o += ttext(50, by + 290, sd['big'], bs, INK, D, ls=-6)
    o += ttext(640, by + 210, sd['big_sub'], min(90, 380 * 100 / tw(sd['big_sub'], 100)), INK, D)
    o += ''.join(T(644, by + 260 + k * 36, n, 24, INK, M, 700, ls=2) for k, n in enumerate(sd['notes']))
    o += vtext(1040, by + 60, 'COUNTABLE AI', 20, INK, M, 90, ls=4)
    o += f'<rect width="{W}" height="{H}" fill="#fff" filter="url(#grainA)" opacity=".1"/>'
    return o
  return wrap

def short(sd):
  a, b = sd['shots']
  t0, t1 = BY[a]['t0'] + sd.get('start', .25), BY[b]['t1'] - .15
  caps = [[round(x - t0, 3), round(y - t0, 3), wrap(txt).split('\n')] for x, y, txt in CAPS if x >= t0 - .3 and x < t1]
  for k in range(len(caps) - 1): caps[k][1] = min(caps[k][1], caps[k + 1][0])
  scenes = ''.join(f'<g id="shot{s.n}" style="display:none">{s.body}</g>' for s in SHOTS)
  js = (f'const T0 = {t0}, CAPS = {json.dumps(caps)}; const R0 = window.render;'
        'window.render = (t) => { R0(T0 + t); let c = CAPS.filter((q) => t >= q[0] - .05).pop(); if (c && t > c[1] + .3) c = null;'
        " $('cap0').textContent = c ? c[2][0] : ''; $('cap1').textContent = c && c[2][1] ? c[2][1] : ''; }; render(0);")
  html = page(SH, ELS, scenes, sd['slug'], W, H, wrap_for(sd), css='#hud,#grain{display:none}', js=js)
  open(os.path.join(HERE, sd['slug'] + '.html'), 'w').write(html)
  narr = ' '.join(c[2] for c in CAPS if t0 - .3 <= c[0] < t1)
  open(os.path.join(HERE, sd['slug'] + '.txt'), 'w').write(narr + '\n')
  return round(t1 - t0, 2)

if __name__ == '__main__':
  for sd in SHORTS: print(sd['slug'], short(sd), 's')
````
