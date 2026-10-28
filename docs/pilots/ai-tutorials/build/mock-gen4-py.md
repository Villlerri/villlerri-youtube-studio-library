# tmp/mock/gen4.py

Принятый стиль Swiss Bold с фактурой: цвета, шрифты, бумага, скотч, зерно. Им пользуется движок пилота.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/gen4.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Swiss Bold, reworked with texture after the author's four references:
docs/channel-concepts/ai-tutorials/mockups/look-2-swiss-rough.html.
Textures are generated here: grain, halftone, scan streaks, torn paper, tape. No photos."""
import json, math, os, random
from gen3 import (OUT, MSGS, TOPICS, T, fit, esc, uid, put, svg, page, avatar, Swiss)

LIME = '#C8FF1E'; INK = '#0B0B0B'; WHITE = '#F4F2EC'; RED = '#FF3B1F'; GRAY = '#8A8A84'
COND = 'font-stretch:62%'; WIDE = 'font-stretch:125%'
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widths.json')))
def tw(s, size, k='cond900'): return sum(W[k].get(ch, 50) for ch in s) * size / 100
BIGH = {'2/3': {0}, '$?': {1}, 'r=?': {0}, '→': {0}, '3×': {0}, '≈': {0}}

DEFS = ('<filter id="grainw" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -.75"/><feComposite in2="SourceGraphic" operator="in"/></filter>'
        '<filter id="worn" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="7" result="w"/>'
        '<feDisplacementMap in="SourceGraphic" in2="w" scale="5" result="d"/><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="2"/>'
        '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -9 6.2" result="m"/><feComposite in="d" in2="m" operator="in"/></filter>'
        '<filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="2" seed="9"/>'
        '<feDisplacementMap in="SourceGraphic" scale="3"/></filter>')

def S(o, F=None): return svg(*o) if F is None else o

def grain(w, h, op=.13): return f'<rect width="{w}" height="{h}" fill="#fff" filter="url(#grainw)" opacity="{op}"/>'

def edge(v, seed, base=.55, a=.07):
  return base + a * math.sin(v * 6.3 + seed) + a * .5 * math.sin(v * 17.1 + seed * 2) + a * .3 * math.sin(v * 41 + seed)

def halftone(x0, y0, w, h, step, col, seed=1, base=.55, soft=.28, flip=False):
  """Dots whose size grows towards the solid side; the border wobbles like ref 1."""
  rnd = random.Random(seed); d = []
  for j in range(int(h / step) + 2):
    for i in range(int(w / step) + 2):
      x = x0 + i * step + (step / 2 if j % 2 else 0); y = y0 + j * step
      u, v = (x - x0) / w, (y - y0) / h
      if flip: u = 1 - u
      t = (u - edge(v, seed, base)) / soft + .5 + (rnd.random() - .5) * .35
      if t <= .05: continue
      if t >= 1: continue
      r = step * .62 * t ** .6
      d.append(f'M{x-r:.1f} {y:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0')
  # solid part beyond the dots
  pts = []
  n = 40
  for k in range(n + 1):
    v = k / n; u = edge(v, seed, base) + soft * .5
    pts.append(((x0 + (1 - u) * w) if flip else (x0 + u * w), y0 + v * h))
  far = x0 if flip else x0 + w + step
  poly = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f' {far:.1f},{y0+h+step:.1f} {far:.1f},{y0-step:.1f}'
  return f'<polygon points="{poly}" fill="{col}"/><path d="{"".join(d)}" fill="{col}"/>'

def streaks(x0, y0, w, h, col, seed=1, base=.55, n=26, flip=False, maxlen=.35):
  """Horizontal scan-glitch lines running out of the halftone border into the dark."""
  rnd = random.Random(seed + 100); o = ''
  for _ in range(n):
    v = rnd.random(); u = edge(v, seed, base) - .12 + rnd.random() * .1
    L = w * (.03 + rnd.random() ** 2 * maxlen); hh = rnd.choice([1, 1, 2, 2, 3, 5]) * h / 360
    x = x0 + u * w - L if not flip else x0 + (1 - u) * w
    o += f'<rect x="{x:.1f}" y="{y0+v*h:.1f}" width="{L:.1f}" height="{hh:.1f}" fill="{col}" opacity="{.5+rnd.random()*.5:.2f}"/>'
  return o

def torn_line(x0, y0, x1, y1, amp, seed, step=None):
  rnd = random.Random(seed); L = math.hypot(x1 - x0, y1 - y0); step = step or max(3, amp * .9)
  n = max(2, int(L / step)); nx, ny = -(y1 - y0) / L, (x1 - x0) / L; pts = []
  for k in range(n + 1):
    t = k / n; j = 0 if k in (0, n) else (rnd.random() - .5) * amp * 2 + math.sin(t * 9 + seed) * amp * .6
    pts.append((x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j))
  return pts

def paper(x, y, w, h, fill, seed=1, amp=4, sides='trbl', rim=None):
  """A sheet with torn sides; `rim` draws the white fibre edge of torn paper."""
  c = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]; pts = []
  for k, s in enumerate('trbl'):
    a, b = c[k], c[(k + 1) % 4]
    seg = torn_line(*a, *b, amp, seed + k) if s in sides else [a, b]
    pts += seg[:-1]
  p = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
  out = ''
  if rim: out += f'<polygon points="{p}" fill="{rim}" transform="translate(1.5 2)"/>'
  return out + f'<polygon points="{p}" fill="{fill}"/>'

def tape(x, y, w, h, rot, seed=1):
  return f'<g transform="rotate({rot} {x+w/2} {y+h/2})" opacity=".78">{paper(x, y, w, h, "#E9E6D8", seed, amp=h*.12, sides="rl")}</g>'

def reg(x, y, r, col):
  return f'<g stroke="{col}" stroke-width="{max(1,r*.12):.1f}" fill="none"><circle cx="{x}" cy="{y}" r="{r*.55:.1f}"/><path d="M{x-r} {y}H{x+r}M{x} {y-r}V{y+r}"/></g>'

def card(cx, cy, w, h, rot, inner, seed=1, fill=WHITE, shadow=True, tp=True):
  """Torn white card, tilted, with tape and a hard shadow; `inner` is drawn in card coords centred at 0,0."""
  o = f'<g transform="translate({cx} {cy}) rotate({rot})">'
  if shadow: o += f'<g transform="translate({w*.035:.1f} {h*.045:.1f})" opacity=".55">{paper(-w/2, -h/2, w, h, "#000", seed, amp=w*.012)}</g>'
  o += paper(-w / 2, -h / 2, w, h, fill, seed, amp=w * .012) + inner
  if tp: o += tape(-w * .2, -h / 2 - h * .06, w * .4, h * .12, -rot * .6 - 3, seed + 5)
  return o + '</g>'

def vtext(x, y, s, size, col, font, rot=-90, anchor='start', ls=2):
  return f'<g transform="translate({x} {y}) rotate({rot})">{T(0, 0, s, size, col, font, 700, anchor, ls)}</g>'

def ttext(x, y, s, size, fill, font, weight=900, anchor='start', ls=0, style=COND, extra=''):
  return T(x, y, s, size, fill, font, weight, anchor, ls, extra=f' style="{style}"{extra}')

def outline(x, y, s, size, hl, font, stroke=WHITE, sw=1.6, lime=LIME, anchor='start', op=1):
  sp = ''.join(f'<tspan fill="{lime}" stroke="none">{esc(ch)}</tspan>' if k in hl else f'<tspan>{esc(ch)}</tspan>' for k, ch in enumerate(s))
  return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="200" text-anchor="{anchor}" fill="none" stroke="{stroke}" '
          f'stroke-width="{sw}" opacity="{op}" style="{WIDE}">{sp}</text>')

def marker(x, y, w, h, rot, seed, col=LIME):
  return f'<g transform="rotate({rot} {x} {y})">{paper(x, y, w, h, col, seed, amp=h*.09, sides="rl")}</g>'

def glitch(x, y, s, size, col, font, seed, slices=5, shift=None, colors=(LIME, RED)):
  """Text cut into horizontal slices, each nudged sideways, with two offset colour ghosts."""
  rnd = random.Random(seed); shift = shift if shift is not None else size * .09; o = ''
  for k, c2 in enumerate(colors):
    o += f'<g opacity=".85">{ttext(x + (k*2-1) * size * .035, y, s, size, c2, font)}</g>'
  top = y - size * .78; hgt = size * .82
  for k in range(slices):
    cid = uid('gs'); y0 = top + hgt * k / slices
    o += (f'<clipPath id="{cid}"><rect x="{x-size*2}" y="{y0:.1f}" width="{size*20}" height="{hgt/slices+.5:.1f}"/></clipPath>'
          f'<g clip-path="url(#{cid})" transform="translate({(rnd.random()-.5)*2*shift:.1f} 0)">{ttext(x, y, s, size, col, font)}</g>')
  return o


class Rough(Swiss):
  slug = 'swiss-rough'; name = 'Swiss Bold — доработка'
  fonts = 'family=Archivo:wdth,wght@62..125,100..900&family=JetBrains+Mono:wght@500;700'
  roles = dict(Swiss.roles, accent=RED, light=WHITE, faint='#DCDAD2', tagink=INK)
  intro = ('Тот же швейцарский плакат: чёрный, белый, лайм, огромные слова. Добавлено по вашим примерам: фактура печати и зерно, растр и полосы сбоя, '
           'рваная бумага, карточки под наклоном со скотчем, тонкие огромные буквы-контуры рядом с узким жирным шрифтом. Сетка нарочно сбита — нет вида шаблонной презентации.')
  takes = ('Из примеров: растр с полосами сбоя — пример 1; огромное тонкое слово с одной лаймовой буквой — пример 2; вертикальный текст и предмет, выходящий за рамку, — пример 3; '
           'рваные края, наклонные карточки, скотч, крупные буквы фоном — пример 4. Отличие от примеров: без фото и 3D-рендеров, вся фактура сгенерирована кодом, '
           'предметы бытовые и нарисованы нами. Ни на одной из 16 разобранных обложек такого нет.')
  risk = ('Риск: фактура может мешать читать. Правило: слова — только плотным цветом на ровном фоне, растр и полосы — за предметом и по краям. '
          'Ещё ближе к примерам можно сделать с фото бумаги и предметов из библиотек CC0 (ambientCG, Poly Haven, StockSnap) — по вашему согласию.')
  sw = [(INK, 'чёрный, фон'), (WHITE, 'бумага, текст'), (LIME, 'лайм: растр, главное'), (RED, 'ошибка'), (GRAY, 'подписи')]
  fl = [('Archivo', 'узкий 900 — заголовки; широкий 200 контуром — огромные буквы фоном'), ('JetBrains Mono', 'номера, подписи, счёт, вертикальные строки')]

  def bg(self, w, h, op=.13): return f'<rect width="{w}" height="{h}" fill="{INK}"/>' + grain(w, h, op)

  def thumb(self, i, tp):
    D = self.disp; M = self.mono; seed = i + 3
    b = self.bg(640, 360)
    b += halftone(300, -10, 360, 380, 8.5, LIME, seed, base=.42, soft=.36) + streaks(300, -10, 360, 380, LIME, seed, base=.42, n=22)
    bs = min(250, 360 * 100 / tw(tp['big'], 100, 'wide200'))
    b += outline(14, 208, tp['big'], bs, BIGH[tp['big']], D, op=.95)
    b += T(24, 34, f'NO.{i+1:02d}', 15, LIME, M, 700, ls=2)
    rot = [-4, 3, -3, 4, -5, 3][i]
    s = 165 if tp['obj'] not in ('map', 'noise', 'dice') else 185
    inner = f'<g filter="url(#worn)">{put(tp["obj"], 0, 6, s, self.roles, self.objfont)}</g>'
    b += card(478, 172, 210, 230, rot, inner, seed)
    # headline: condensed, one word on a torn lime strip
    y0 = 262
    for j, ln in enumerate(tp['w']):
      sz = min(64, 300 / (tw(ln, 100) / 100)); y = y0 + j * sz * .93; cx = 24
      for wd in ln.split(' '):
        if wd == tp['hl']:
          b += marker(cx - 7, y - sz * .8, tw(wd, sz) + 14, sz * .9, -2.5, seed + j)
        b += ttext(cx, y, wd, sz, INK if wd == tp['hl'] else WHITE, D)
        cx += tw(wd + ' ', sz)
    vs = f'COUNTABLE AI — {tp["s"].upper()}'
    b += vtext(626, 20, vs, min(10, 320 / len(vs) / .6 - 1.5 / .6), INK, M, 90, ls=1.5)
    b += reg(616, 340, 7, INK)
    return svg(640, 360, b, DEFS, 'thumbsvg')

  def frames(self):
    D = self.disp; M = self.mono; out = []
    # 1 training data: three torn strips taped to the dark
    b = self.bg(1600, 900) + outline(60, 760, '3/3', 760, set(), D, stroke='#3A3A36', sw=3)
    b += vtext(70, 120, 'TRAINING DATA — EVERYTHING IT EVER READ', 22, LIME, M, 90, ls=4)
    for j, m in enumerate(MSGS):
      cy = 230 + j * 205; rot = [-2.2, 1.6, -1.2][j]; x = 200 + j * 40
      fill = LIME if j == 1 else WHITE
      b += f'<g transform="rotate({rot} 800 {cy})"><g transform="translate(12 16)" opacity=".6">{paper(x, cy-80, 1180, 160, "#000", j+20, amp=6)}</g>{paper(x, cy-80, 1180, 160, fill, j+20, amp=6, rim="#fff")}'
      b += ttext(x + 50, cy + 48, m.upper(), min(132, 940 * 100 / tw(m.upper(), 100)), INK, D) + T(x + 1130, cy + 18, 'TRUE', 30, INK, M, 700, 'end', 3) + '</g>'
      b += tape(x - 40, cy - 100, 150, 46, -14 + j * 8, j + 30)
    b += T(1530, 860, '3 / 3 TRUE', 30, LIME, M, 700, 'end', 3)
    out.append((svg(1600, 900, b, DEFS, 'framesvg'), 'Everything it read: three true messages, torn strips taped to the dark.'))
    # 2 the blank: three tilted cards
    b = self.bg(1600, 900) + halftone(700, -20, 920, 940, 16, LIME, 5, base=.62, soft=.3) + streaks(700, -20, 920, 940, LIME, 5, base=.62, n=34)
    mx = 90 + tw('MOM IS AT THE ', 180)
    b += ttext(90, 190, 'MOM IS AT THE', 180, WHITE, D) + marker(mx, 60, 260, 160, -3, 8, WHITE) + ttext(mx + 130, 192, '?', 170, INK, D, anchor='middle')
    for j, wd in enumerate(['STORE', 'GYM', 'PARK']):
      cx = 300 + j * 480; rot = [-6, 3, -2][j]
      inner = ttext(0, -40, wd, 150, INK, D, anchor='middle') + f'<path d="M-150 10H150" stroke="{INK}" stroke-width="4"/>'
      inner += outline(0, 190, '1/3', 190, {0}, D, stroke=INK, sw=3, lime=RED if j == 1 else INK, anchor='middle')
      inner += reg(-150, -190, 14, INK) + reg(150, -190, 14, INK)
      b += card(cx, 560, 380, 470, rot, inner, j + 40)
    b += vtext(1560, 40, 'IT SEES ONLY THE LAST WORD: "THE"', 22, INK, M, 90, ls=3)
    out.append((svg(1600, 900, b, DEFS, 'framesvg'), 'After "the": store 1 · gym 1 · park 1. Cards are tilted and taped, the lime halftone fades into scan streaks.'))
    # 3 the false sentence: torn lime panel, glitched GYM
    b = self.bg(1600, 900)
    b += paper(-40, -40, 860, 980, LIME, 61, amp=14, sides='r', rim='#fff') + halftone(790, -20, 200, 940, 12, LIME, 61, base=.0, soft=.9, flip=True)
    b += ttext(30, 600, '2/3', 620, INK, D, ls=-10) + ttext(50, 730, 'OF ITS SENTENCES', 84, INK, D) + ttext(50, 820, 'ARE FALSE', 84, INK, D)
    fs = min(150, 500 * 100 / tw('THE GYM.', 100))
    b += ttext(1000, 210, 'MOM IS AT', fs, WHITE, D) + glitch(1000, 210 + fs * .95, 'THE GYM.', fs, WHITE, D, 3)
    b += f'<g transform="rotate(-6 1420 420)">{paper(1310, 385, 220, 70, RED, 70, amp=5, sides="rl")}{T(1420, 434, "FALSE", 40, WHITE, M, 700, "middle", 6)}</g>'
    for j in range(9):
      x = 1000 + (j % 3) * 180; y = 490 + (j // 3) * 128; ok = j % 4 == 0
      rr = (j * 37 % 7 - 3) * .8
      b += f'<g transform="rotate({rr:.1f} {x+82} {y+54})" filter="url(#rough)">{paper(x, y, 165, 108, WHITE if ok else RED, j + 80, amp=3)}{T(x+82, y+68, "TRUE" if ok else "FALSE", 34, INK if ok else WHITE, M, 700, "middle")}</g>'
    out.append((svg(1600, 900, b, DEFS, 'framesvg'), 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false. The error word breaks into glitch slices.'))
    return out

  def short(self):
    D = self.disp; M = self.mono
    b = self.bg(540, 960) + outline(-30, 560, '2/3', 330, set(), D, stroke='#33332F', sw=2)
    hs = 460 * 100 / tw('EVERY WORD', 100)
    b += ttext(36, 120, 'EVERY WORD', hs, WHITE, D) + ttext(36, 120 + hs * .95, 'WAS TRUE.', hs, WHITE, D)
    b += f'<g transform="rotate(-3 270 330)">{paper(30, 280, 480, 110, WHITE, 90, amp=4, sides="rl")}</g>' + ttext(54, 360, 'MOM IS AT THE', 56, INK, D) + glitch(54 + tw('MOM IS AT THE ', 56), 360, 'GYM.', 56, INK, D, 9, colors=(RED, LIME))
    b += tape(220, 262, 110, 34, 6, 91)
    b += paper(-20, 560, 580, 440, LIME, 92, amp=12, sides='t', rim='#fff') + halftone(-10, 470, 560, 120, 9, LIME, 92, base=.7, soft=.6)
    b += ttext(30, 800, '2/3', 280, INK, D, ls=-6) + ttext(34, 905, 'WRONG', 96, INK, D) + T(320, 870, '6 OF 9', 22, INK, M, 700, ls=2) + T(320, 902, 'COUNT IT', 22, INK, M, 700, ls=2)
    b += vtext(520, 600, 'COUNTABLE AI', 16, INK, M, 90, ls=3)
    return svg(540, 960, b, DEFS, 'shortsvg')

  def avatar(self):
    D = self.disp
    return (f'<rect width="100" height="100" fill="{INK}"/>' + halftone(0, 0, 100, 100, 6, LIME, 2, base=.35, soft=.5)
            + ttext(50, 70, 'CA', 54, WHITE, D, anchor='middle') + f'<rect x="58" y="22" width="28" height="56" fill="none"/>')

  def banner(self):
    D = self.disp; M = self.mono
    b = self.bg(2560, 1440, .1) + halftone(1880, 480, 700, 480, 14, LIME, 4, base=.5, soft=.4) + streaks(1880, 480, 700, 480, LIME, 4, base=.5, n=40, maxlen=.7)
    b += halftone(-20, 480, 520, 480, 14, LIME, 6, base=.55, soft=.4, flip=True)
    word = 'COUNTABLE AI'; sz = 1500 * 100 / tw(word, 100, 'wide200')
    b += outline(530, 800, word, round(sz), {10, 11}, D, sw=3)
    b += T(536, 880, 'HOW AI WORKS — ON EXAMPLES SMALL ENOUGH TO CHECK WITH A PENCIL', 30, LIME, M, 700, ls=3)
    b += vtext(538, 560, 'NO.01—06', 18, GRAY, M, 0, ls=4)
    return svg(2560, 1440, b, DEFS, 'bannersvg')


K = Rough(); K.objfont = "'Archivo',sans-serif"
if __name__ == '__main__':
  html = page(K).replace('ВТОРОЙ КРУГ · СТИЛЬ 2 ИЗ 5', 'ДОРАБОТКА СТИЛЯ 2 ПО ПРИМЕРАМ АВТОРА')
  open(f'{OUT}/look-2-swiss-rough.html', 'w').write(html)
  print(len(html))
````
