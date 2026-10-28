# tmp/mock/gen3.py

Второй круг стилей (look-1…5, looks-overview) и общие функции, которые берёт gen4.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/gen3.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Five adult style mockups for Countable AI, round 2:
docs/channel-concepts/ai-tutorials/mockups/look-<n>-<slug>.html and looks-overview.html.
All art is SVG drawn here; fonts are Google Fonts (OFL)."""
import os, random
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '../../docs/channel-concepts/ai-tutorials/mockups')

MSGS = ['Mom is at the store.', 'Dad is at the gym.', 'Sam is at the park.']
TOPICS = [
  dict(t='Why AI Makes Things Up — We Counted It by Hand', s='Shannon 1948 · Kalai et al. 2025', big='2/3', w=['TRUE WORDS.', 'FALSE ANSWER.'], hl='FALSE', obj='phone'),
  dict(t='What "Training" Means: Guess the Pizza Price', s='Legendre 1805 · Cauchy 1847', big='$?', w=['GUESS THE', 'PRICE.'], hl='GUESS', obj='pizza'),
  dict(t='Why AI Can\'t Count the R\'s in "Strawberry"', s='Gage 1994 · Sennrich et al. 2016', big='r=?', w=["IT CAN'T", 'SEE THE R.'], hl='R.', obj='berry'),
  dict(t='How AI Turns Static Into a Picture', s='Sohl-Dickstein et al. 2015 · Ho et al. 2020', big='→', w=['NOISE IN.', 'CAT OUT.'], hl='CAT', obj='noise'),
  dict(t='Why AI Gives a Different Answer Every Time', s='Holtzman et al. 2020', big='3×', w=['SAME QUESTION.', 'NEW ANSWER.'], hl='NEW', obj='dice'),
  dict(t='How AI Knows "Pizza" Is Close to "Pasta"', s='Mikolov et al. 2013', big='≈', w=['PIZZA', 'IS NEAR PASTA.'], hl='PASTA.', obj='map'),
]

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
_id = [0]
def uid(p): _id[0] += 1; return f'{p}{_id[0]}'

def T(x, y, s, size, fill, font, weight=400, anchor='start', ls=0, style='', extra=''):
  return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size:.1f}" font-weight="{weight}" fill="{fill}" '
          f'text-anchor="{anchor}" letter-spacing="{ls}" font-style="{style or "normal"}"{extra}>{esc(s)}</text>')

def fit(s, size, maxw, k):
  """Shrink size so that len(s)*k*size fits maxw; k = average glyph width in em."""
  return min(size, maxw / max(1, len(s) * k))

def hlline(x, y, line, hl, size, fill, hfill, font, weight, anchor='start', ls=0, hstyle=''):
  """One line where the word `hl` gets another colour (and style)."""
  parts = line.split(' ')
  sp = ''.join(f'<tspan fill="{hfill if p == hl else fill}"{" font-style=%s" % chr(34)+hstyle+chr(34) if (p == hl and hstyle) else ""}>{esc(p)}{" " if i < len(parts)-1 else ""}</tspan>' for i, p in enumerate(parts))
  return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size:.1f}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}" xml:space="preserve">{sp}</text>'

GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
def grain(w, h, op=.35): return f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="{op}" fill="#000"/>'

# ---------- objects, painted by a role map F ----------
def phone(x, y, s, F, font, msg='Mom is at the gym.', bad=True):
  w, h = .52 * s, s
  o = f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{.08*s:.1f}" fill="{F["dark"]}"{F.get("dstroke","")}/>'
  o += f'<rect x="{x-w/2+.03*s:.1f}" y="{y-h/2+.03*s:.1f}" width="{w-.06*s:.1f}" height="{h-.06*s:.1f}" rx="{.055*s:.1f}" fill="{F["light"]}"/>'
  o += f'<rect x="{x-.07*s:.1f}" y="{y-h/2+.05*s:.1f}" width="{.14*s:.1f}" height="{.03*s:.1f}" rx="{.015*s:.1f}" fill="{F["dark"]}"/>'
  for i in range(2):  # two faint earlier messages
    o += f'<rect x="{x-w/2+.07*s:.1f}" y="{y-h/2+.16*s+i*.1*s:.1f}" width="{(.3-.08*i)*s:.1f}" height="{.065*s:.1f}" rx="{.03*s:.1f}" fill="{F["faint"]}"/>'
  bw, bh = 1.0 * s, .17 * s; bx, by = x - .62 * s, y + .02 * s
  o += F.get('bshadow', '').format(x=bx + .02 * s, y=by + .03 * s, w=bw, h=bh, r=bh / 2)
  o += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{bh/2:.1f}" fill="{F["alt"]}"/>'
  o += T(bx + bh * .45, by + bh * .66, msg, .072 * s, F['onalt'], font, 600)
  if bad:
    r = .085 * s
    o += f'<circle cx="{bx+bw:.1f}" cy="{by:.1f}" r="{r:.1f}" fill="{F["accent"]}"/>' + T(bx + bw, by + r * .45, '!', r * 1.3, '#fff', font, 800, 'middle')
  return o

def pizza(x, y, s, F, font):
  r = s * .45
  o = f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{F["alt"]}"/><circle cx="{x}" cy="{y}" r="{r*.82:.1f}" fill="{F["accent"]}"/>'
  for a, d in [(0, .45), (1.3, .5), (2.6, .38), (3.9, .52), (5.1, .4), (0.6, .15)]:
    import math
    o += f'<circle cx="{x+math.cos(a)*r*d:.1f}" cy="{y+math.sin(a)*r*d:.1f}" r="{r*.1:.1f}" fill="{F["light"]}"/>'
  tx, ty = x + r * .55, y - r * 1.05
  o += f'<path d="M{tx:.1f} {ty:.1f} h{s*.42:.1f} v{s*.22:.1f} h-{s*.42:.1f} l-{s*.1:.1f} -{s*.11:.1f} Z" fill="{F["light"]}" stroke="{F["dark"]}" stroke-width="{s*.012:.1f}"/>'
  o += T(tx + s * .21, ty + s * .16, '$ ?', s * .14, F.get('tagink', F['ink']), font, 800, 'middle')
  return o

def berry(x, y, s, F, font):
  o = f'<path d="M{x-s*.36:.1f} {y-s*.2:.1f} C{x-s*.4:.1f} {y+s*.2:.1f} {x-s*.1:.1f} {y+s*.48:.1f} {x:.1f} {y+s*.5:.1f} C{x+s*.1:.1f} {y+s*.48:.1f} {x+s*.4:.1f} {y+s*.2:.1f} {x+s*.36:.1f} {y-s*.2:.1f} C{x+s*.2:.1f} {y-s*.34:.1f} {x-s*.2:.1f} {y-s*.34:.1f} {x-s*.36:.1f} {y-s*.2:.1f} Z" fill="{F["accent"]}"/>'
  rnd = random.Random(3)
  for i in range(14):
    px = x + (rnd.random() - .5) * s * .5; py = y - s * .12 + rnd.random() * s * .45
    o += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{s*.018:.1f}" ry="{s*.03:.1f}" fill="{F["light"]}"/>'
  o += f'<path d="M{x-s*.3:.1f} {y-s*.24:.1f} L{x-s*.12:.1f} {y-s*.42:.1f} L{x:.1f} {y-s*.28:.1f} L{x+s*.12:.1f} {y-s*.42:.1f} L{x+s*.3:.1f} {y-s*.24:.1f} Z" fill="{F["leaf"]}"/>'
  o += f'<path d="M{x+s*.04:.1f} {y-s*.6:.1f} V{y+s*.62:.1f}" stroke="{F["dark"]}" stroke-width="{s*.025:.1f}" stroke-dasharray="{s*.05:.1f} {s*.035:.1f}"/>'
  return o

def noise(x, y, s, F, font):
  rnd = random.Random(11); n = 8; c = s * .5 / n; o = ''
  for i in range(n):
    for j in range(n):
      o += f'<rect x="{x-s*.55+i*c:.1f}" y="{y-s*.25+j*c:.1f}" width="{c+.5:.1f}" height="{c+.5:.1f}" fill="{rnd.choice(F["noise"])}"/>'
  o += f'<path d="M{x+s*.02:.1f} {y:.1f} h{s*.16:.1f} m-{s*.06:.1f} -{s*.06:.1f} l{s*.06:.1f} {s*.06:.1f} l-{s*.06:.1f} {s*.06:.1f}" stroke="{F["ink"]}" stroke-width="{s*.03:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
  cx, cy = x + s * .45, y + s * .04
  o += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s*.2:.1f}" fill="{F["dark"]}"/><path d="M{cx-s*.19:.1f} {cy-s*.06:.1f} l{s*.03:.1f} -{s*.24:.1f} l{s*.14:.1f} {s*.13:.1f} Z M{cx+s*.19:.1f} {cy-s*.06:.1f} l-{s*.03:.1f} -{s*.24:.1f} l-{s*.14:.1f} {s*.13:.1f} Z" fill="{F["dark"]}"/>'
        f'<ellipse cx="{cx-s*.075:.1f}" cy="{cy-s*.01:.1f}" rx="{s*.03:.1f}" ry="{s*.045:.1f}" fill="{F["accent"]}"/><ellipse cx="{cx+s*.075:.1f}" cy="{cy-s*.01:.1f}" rx="{s*.03:.1f}" ry="{s*.045:.1f}" fill="{F["accent"]}"/>')
  return o

def dice(x, y, s, F, font):
  k = s * .32
  o = (f'<path d="M{x:.1f} {y-k:.1f} L{x+k:.1f} {y-k/2:.1f} L{x:.1f} {y:.1f} L{x-k:.1f} {y-k/2:.1f} Z" fill="{F["light"]}"/>'
       f'<path d="M{x-k:.1f} {y-k/2:.1f} L{x:.1f} {y:.1f} L{x:.1f} {y+k:.1f} L{x-k:.1f} {y+k/2:.1f} Z" fill="{F["alt"]}"/>'
       f'<path d="M{x+k:.1f} {y-k/2:.1f} L{x:.1f} {y:.1f} L{x:.1f} {y+k:.1f} L{x+k:.1f} {y+k/2:.1f} Z" fill="{F["accent"]}"/>')
  o += f'<ellipse cx="{x:.1f}" cy="{y-k/2:.1f}" rx="{k*.16:.1f}" ry="{k*.09:.1f}" fill="{F["dark"]}"/>'
  for dx, dy in [(-.7, .05), (-.3, .45)]: o += f'<ellipse cx="{x+dx*k:.1f}" cy="{y+dy*k:.1f}" rx="{k*.08:.1f}" ry="{k*.12:.1f}" fill="{F["light"]}"/>'
  for dx, dy in [(.3, .05), (.5, .25), (.7, .45)]: o += f'<ellipse cx="{x+dx*k:.1f}" cy="{y+dy*k:.1f}" rx="{k*.08:.1f}" ry="{k*.12:.1f}" fill="{F["light"]}"/>'
  for i, wd in enumerate(['store', 'gym', 'park']):
    bx = x + s * .48; by = y - s * .36 + i * s * .26
    o += f'<rect x="{bx:.1f}" y="{by:.1f}" width="{s*.42:.1f}" height="{s*.18:.1f}" rx="{s*.09:.1f}" fill="{F["alt"] if i != 1 else F["accent"]}"/>' + T(bx + s * .21, by + s * .125, wd, s * .1, F['onalt'] if i != 1 else '#fff', font, 700, 'middle')
  return o

def amap(x, y, s, F, font):
  pts = [('pizza', -.45, -.12, 1), ('pasta', -.2, .08, 1), ('salad', -.4, .32, 0), ('gym', .35, -.3, 0), ('park', .45, .1, 0), ('store', .2, .35, 0)]
  o = f'<ellipse cx="{x-s*.32:.1f}" cy="{y-s*.02:.1f}" rx="{s*.3:.1f}" ry="{s*.2:.1f}" fill="{F["faint"]}" stroke="{F["accent"]}" stroke-width="{s*.012:.1f}" stroke-dasharray="{s*.03:.1f} {s*.02:.1f}"/>'
  for wd, dx, dy, hot in pts:
    o += f'<circle cx="{x+dx*s:.1f}" cy="{y+dy*s:.1f}" r="{s*.035:.1f}" fill="{F["accent"] if hot else F["dark"]}"/>' + T(x + dx * s + s * .055, y + dy * s + s * .03, wd, s * .085, F['ink'], font, 700)
  return o

OBJ = dict(phone=phone, pizza=pizza, berry=berry, noise=noise, dice=dice, map=amap)
CENTER = dict(phone=-.08, pizza=.1, berry=0, noise=.05, dice=.29, map=.07)
def put(name, x, y, s, F, font):
  """Draw an object so that its visual centre lands on x."""
  return OBJ[name](x - CENTER[name] * s, y, s, F, font)

def svg(w, h, body, defs='', cls=''):
  vb = f'0 0 {w} {h}' if cls != 'bannersvg' else '0 508 2560 424'
  return f'<svg class="{cls}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" role="img"><defs>{GRAIN}{defs}</defs>{body}</svg>'

# =============== styles ===============
class Style:
  sub = "'Inter',sans-serif"
  def F(self): return self.roles
  def obj(self, name, x, y, s): return put(name, x, y, s, self.F(), self.objfont)

# ---- 1 Editorial ----
class Editorial(Style):
  n = 1; slug = 'editorial'; name = 'Editorial'
  fonts = 'family=Instrument+Serif:ital@0;1&family=IBM+Plex+Mono:wght@400;600'
  disp = "'Instrument Serif',serif"; mono = "'IBM Plex Mono',monospace"; objfont = "'IBM Plex Mono',monospace"
  c = dict(bg='#F2EDE3', ink='#151515', red='#D3261A', gray='#8C857A', rule='#CFC6B6')
  roles = dict(dark='#151515', light='#FBF8F2', faint='#E4DDD0', alt='#151515', onalt='#FBF8F2', accent='#D3261A', ink='#151515', leaf='#151515', noise=['#151515', '#5A564F', '#A39B8E', '#E4DDD0'])
  intro = 'Как инфографика большого журнала: крупный шрифт с засечками, тонкие линии, подписи «рис. 1», один красный акцент. Взрослый, спокойный, умный тон.'
  takes = 'От лидеров: подсветка одного главного — принцип сигналов Mayer; журнальная инфографика — как у The Pudding и NYT. Ближайший из 16 разобранных — Vox, но у Vox коллаж из чужих изображений; у нас только свои схемы.'
  risk = 'Риск: спокойный стиль хуже кричит в ленте. Обложки держит крупный заголовок и красное слово.'
  sw = [('#F2EDE3', 'бумага'), ('#151515', 'чернила'), ('#D3261A', 'акцент, ошибка'), ('#8C857A', 'подписи'), ('#CFC6B6', 'линии')]
  fl = [('Instrument Serif', 'заголовки, обложки'), ('IBM Plex Mono', 'подписи, числа, слова на экране')]
  def bg(self, w, h): return f'<rect width="{w}" height="{h}" fill="{self.c["bg"]}"/>{grain(w,h,.12)}'
  def thumb(self, i, tp):
    c = self.c; b = self.bg(640, 360)
    b += f'<path d="M28 34H612" stroke="{c["ink"]}" stroke-width="2"/>' + T(28, 26, f'No. {i+1:02d}', 15, c['ink'], self.mono, 600, ls=1)
    b += T(612, 26, 'COUNTABLE AI', 15, c['ink'], self.mono, 600, 'end', ls=1)
    lines = [tp['w'][0].title().replace("'T", "'t"), tp['w'][1].title().replace("'T", "'t")]
    hl = tp['hl'].title()
    for j, ln in enumerate(lines):
      sz = fit(ln, 74, 330, .42)
      b += hlline(28, 120 + j * 76, ln, hl, sz, c['ink'], c['red'], self.disp, 400, hstyle='italic')
    b += f'<path d="M390 58V330" stroke="{c["rule"]}" stroke-width="1.5"/>'
    b += f'<g>{self.obj(tp["obj"], 515, 200, 190 if tp["obj"] not in ("noise","map") else 210)}</g>'
    b += T(28, 330, 'FIG. 1 — ' + ['9 SENTENCES, 6 FALSE', 'ONE LINE, MANY GUESSES', 'TOKENS, NOT LETTERS', '1,000 SMALL STEPS', 'SAME ODDS, NEW ROLL', 'WORDS AS POINTS'][i], 14, c['gray'], self.mono, 600, ls=1)
    return svg(640, 360, b, cls='thumbsvg')
  def frames(self):
    c = self.c; out = []
    b = self.bg(1600, 900) + T(120, 130, 'Everything it ever read', 84, c['ink'], self.disp) + f'<path d="M120 170H1480" stroke="{c["ink"]}" stroke-width="2"/>'
    for j, m in enumerate(MSGS):
      y = 300 + j * 150
      b += T(120, y, f'{j+1}', 40, c['gray'], self.mono, 600) + T(200, y, m, 76, c['ink'], self.disp) + f'<path d="M120 {y+40}H1480" stroke="{c["rule"]}" stroke-width="1.5"/>' + T(1480, y, 'TRUE', 30, c['ink'], self.mono, 600, 'end', ls=2)
    b += T(120, 820, 'FIG. 1 — THE WHOLE TRAINING SET: THREE MESSAGES', 26, c['gray'], self.mono, 600, ls=1)
    out.append((b, 'Everything it read: three true messages.'))
    b = self.bg(1600, 900) + hlline(120, 190, 'Mom is at the ___', 'the', 110, c['ink'], c['red'], self.disp, 400, hstyle='italic')
    b += T(120, 260, 'IT READS ONLY THE LAST WORD', 26, c['red'], self.mono, 600, ls=2)
    for j, wd in enumerate(['store', 'gym', 'park']):
      y = 400 + j * 140
      b += T(120, y + 50, wd, 72, c['ink'], self.disp, style='italic' if j == 1 else '') + f'<rect x="420" y="{y}" width="{900/3*1:.0f}" height="64" fill="{c["red"] if j==1 else c["ink"]}"/>'
      b += f'<path d="M420 {y+90}H1480" stroke="{c["rule"]}" stroke-width="1.5"/>' + T(1480, y + 48, '1 in 3', 44, c['ink'], self.mono, 600, 'end')
    b += T(120, 860, 'FIG. 2 — WHAT CAME AFTER "THE", COUNTED', 26, c['gray'], self.mono, 600, ls=1)
    out.append((b, 'After "the": store 1 · gym 1 · park 1.'))
    b = self.bg(1600, 900) + hlline(120, 220, 'Mom is at the gym.', 'gym.', 150, c['ink'], c['red'], self.disp, 400, hstyle='italic')
    b += f'<path d="M790 240 q150 30 300 -6" stroke="{c["red"]}" stroke-width="6" fill="none"/>' + T(790, 320, '↑ every pair of words was seen in true text', 26, c['red'], self.mono, 600)
    for j in range(9):
      x = 120 + (j % 3) * 120; y = 420 + (j // 3) * 120; ok = j % 4 == 0
      b += f'<rect x="{x}" y="{y}" width="96" height="96" fill="{c["ink"] if ok else "none"}" stroke="{c["ink"] if ok else c["red"]}" stroke-width="4"/>'
      if not ok: b += f'<path d="M{x+18} {y+18}L{x+78} {y+78}M{x+78} {y+18}L{x+18} {y+78}" stroke="{c["red"]}" stroke-width="5"/>'
    b += T(560, 560, '6 of 9', 190, c['red'], self.disp, style='italic') + T(570, 640, 'POSSIBLE SENTENCES ARE FALSE', 34, c['ink'], self.mono, 600, ls=2)
    b += T(570, 700, 'Black squares: the three true ones.', 40, c['gray'], self.disp, style='italic')
    out.append((b, 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false.'))
    return out
  def short(self):
    c = self.c; b = self.bg(540, 960) + T(40, 70, 'COUNTABLE AI', 20, c['ink'], self.mono, 600, ls=2) + f'<path d="M40 86H500" stroke="{c["ink"]}" stroke-width="2"/>'
    b += T(40, 220, 'Every word', 88, c['ink'], self.disp) + T(40, 310, 'was true.', 88, c['ink'], self.disp)
    b += T(40, 470, 'The sentence', 88, c['ink'], self.disp) + hlline(40, 560, 'was false.', 'false.', 88, c['ink'], c['red'], self.disp, 400, hstyle='italic')
    b += f'<path d="M40 640H500" stroke="{c["rule"]}" stroke-width="2"/>' + T(40, 720, 'Mom is at the gym.', 44, c['ink'], self.disp, style='italic') + T(40, 900, '6 OF 9 FALSE', 30, c['red'], self.mono, 600, ls=2)
    return svg(540, 960, b, cls='shortsvg')
  def avatar(self):
    c = self.c
    return f'<rect width="100" height="100" fill="{c["bg"]}"/>' + T(46, 74, 'C', 82, c['ink'], self.disp) + f'<circle cx="76" cy="68" r="8" fill="{c["red"]}"/>'
  def banner(self):
    c = self.c; b = self.bg(2560, 1440)
    b += T(560, 760, 'Countable', 200, c['ink'], self.disp) + T(1350, 760, "AI", 200, c['red'], self.disp, style='italic')
    b += f'<path d="M560 800H2000" stroke="{c["ink"]}" stroke-width="3"/>' + T(560, 860, 'HOW AI WORKS — ON EXAMPLES YOU CAN COUNT', 40, c['ink'], self.mono, 600, ls=3)
    return svg(2560, 1440, b, cls='bannersvg')

# ---- 2 Swiss Bold ----
class Swiss(Style):
  n = 2; slug = 'swiss-bold'; name = 'Swiss Bold'
  fonts = 'family=Archivo:wght@500;800;900&family=JetBrains+Mono:wght@500;700'
  disp = "'Archivo',sans-serif"; mono = "'JetBrains Mono',monospace"; objfont = "'Archivo',sans-serif"
  c = dict(bg='#FFFFFF', ink='#0D0D0D', lime='#D4FF3A', gray='#7A7A7A', rule='#0D0D0D')
  roles = dict(dark='#0D0D0D', light='#FFFFFF', faint='#E6E6E6', alt='#0D0D0D', onalt='#FFFFFF', accent='#FF3B1F', ink='#0D0D0D', leaf='#0D0D0D', noise=['#0D0D0D', '#555', '#AAA', '#EEE'])
  intro = 'Швейцарский плакат: огромные цифры и слова, чёрный, белый и кислотный лайм, жёсткая сетка. Резко, современно, видно с другого конца ленты.'
  takes = 'От лидеров: крупное число и 3–4 слова на обложке — приём сильных обложек в нашей выдаче. Отличие: строгая типографика вместо картинок; лайм не встречается ни на одной из 16 разобранных обложек.'
  risk = 'Риск: холодный тон. Тепло дают бытовые предметы и разговорный голос.'
  sw = [('#0D0D0D', 'чёрный'), ('#FFFFFF', 'белый'), ('#D4FF3A', 'лайм, главное'), ('#FF3B1F', 'ошибка'), ('#7A7A7A', 'подписи')]
  fl = [('Archivo', 'заголовки 900, текст 500'), ('JetBrains Mono', 'номера, подписи, счёт')]
  def thumb(self, i, tp):
    c = self.c; b = f'<rect width="640" height="360" fill="{c["ink"]}"/><rect x="372" width="268" height="360" fill="{c["bg"]}"/>'
    big = tp['big']; bs = fit(big, 200, 320, .62)
    b += T(28, 50, f'{i+1:02d}', 26, c['lime'], self.mono, 700) + T(28, 60 + bs * .78 + 20, big, bs, c['lime'], self.disp, 900, ls=-6)
    for j, ln in enumerate(tp['w']):
      sz = fit(ln, 40, 320, .64)
      b += hlline(28, 290 + j * 44 - (44 if len(tp['w'][0]) > 0 else 0) + 30, ln, tp['hl'], sz, '#FFFFFF', c['lime'], self.disp, 900, ls=-1)
    b += f'<g>{self.obj(tp["obj"], 506, 186, 175 if tp["obj"] != "map" else 200)}</g>'
    b += f'<rect x="372" y="326" width="268" height="34" fill="{c["lime"]}"/>' + T(386, 349, 'COUNTABLE AI', 16, c['ink'], self.mono, 700, ls=1)
    return svg(640, 360, b, cls='thumbsvg')
  def frames(self):
    c = self.c; out = []
    b = f'<rect width="1600" height="900" fill="{c["bg"]}"/>' + ''.join(f'<path d="M{x} 0V900" stroke="#EDEDED" stroke-width="2"/>' for x in range(100, 1600, 200))
    b += T(100, 150, 'TRAINING DATA', 40, c['ink'], self.mono, 700, ls=4) + T(1500, 150, '3 / 3 TRUE', 40, c['ink'], self.mono, 700, 'end')
    for j, m in enumerate(MSGS):
      y = 230 + j * 200
      b += f'<rect x="100" y="{y}" width="1400" height="160" fill="{c["ink"] if j!=1 else c["lime"]}"/>' + T(150, y + 108, m.upper(), 78, c['bg'] if j != 1 else c['ink'], self.disp, 900, ls=-2)
    out.append((b, 'Everything it read: three true messages.'))
    b = f'<rect width="1600" height="900" fill="{c["ink"]}"/>' + T(100, 200, 'MOM IS AT THE', 120, '#FFFFFF', self.disp, 900, ls=-3) + f'<rect x="1080" y="100" width="420" height="120" fill="{c["lime"]}"/>' + T(1290, 192, '?', 110, c['ink'], self.disp, 900, 'middle')
    for j, wd in enumerate(['STORE', 'GYM', 'PARK']):
      x = 100 + j * 470
      b += f'<rect x="{x}" y="330" width="440" height="440" fill="none" stroke="#FFFFFF" stroke-width="4"/>' + T(x + 30, 420, wd, 80, '#FFFFFF', self.disp, 900) + T(x + 30, 720, '1/3', 220, c['lime'], self.disp, 900, ls=-8)
    b += T(100, 850, 'IT SEES ONLY THE LAST WORD: "THE"', 34, c['gray'], self.mono, 700, ls=2)
    out.append((b, 'After "the": store 1 · gym 1 · park 1.'))
    b = f'<rect width="1600" height="900" fill="{c["bg"]}"/><rect width="900" height="900" fill="{c["lime"]}"/>'
    b += T(60, 560, '2/3', 470, c['ink'], self.disp, 900, ls=-20) + T(70, 680, 'OF ITS SENTENCES', 60, c['ink'], self.disp, 900) + T(70, 750, 'ARE FALSE', 60, c['ink'], self.disp, 900)
    b += T(960, 200, 'MOM IS AT', 80, c['ink'], self.disp, 900) + T(960, 290, 'THE GYM.', 80, self.roles['accent'], self.disp, 900)
    for j in range(9):
      x = 960 + (j % 3) * 180; y = 400 + (j // 3) * 150; ok = j % 4 == 0
      b += f'<rect x="{x}" y="{y}" width="160" height="130" fill="{c["ink"] if ok else self.roles["accent"]}"/>' + T(x + 80, y + 88, 'TRUE' if ok else 'FALSE', 34, '#FFFFFF', self.mono, 700, 'middle')
    out.append((b, 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false.'))
    return out
  def short(self):
    c = self.c; b = f'<rect width="540" height="960" fill="{c["ink"]}"/><rect y="560" width="540" height="400" fill="{c["lime"]}"/>'
    b += T(36, 90, 'EVERY WORD', 66, '#FFFFFF', self.disp, 900) + T(36, 160, 'WAS TRUE.', 66, '#FFFFFF', self.disp, 900)
    b += f'<rect x="36" y="250" width="468" height="96" fill="#FFFFFF"/>' + T(56, 312, 'MOM IS AT THE GYM.', 38, c['ink'], self.disp, 900) + f'<rect x="36" y="346" width="468" height="44" fill="{self.roles["accent"]}"/>' + T(56, 377, 'FALSE', 26, '#FFFFFF', self.mono, 700, ls=4)
    b += T(30, 830, '2/3', 300, c['ink'], self.disp, 900, ls=-14) + T(40, 910, 'WRONG', 50, c['ink'], self.disp, 900)
    return svg(540, 960, b, cls='shortsvg')
  def avatar(self):
    c = self.c
    return f'<rect width="100" height="100" fill="{c["lime"]}"/>' + T(50, 47, 'COUN', 27, c['ink'], self.disp, 900, 'middle', -1) + T(50, 72, 'TABLE', 27, c['ink'], self.disp, 900, 'middle', -1) + f'<rect x="22" y="80" width="56" height="5" fill="{c["ink"]}"/>'
  def banner(self):
    c = self.c; b = f'<rect width="2560" height="1440" fill="{c["ink"]}"/><rect x="1800" y="0" width="760" height="1440" fill="{c["lime"]}"/>'
    b += T(480, 730, 'COUNTABLE', 170, '#FFFFFF', self.disp, 900, ls=-6) + T(1840, 730, "AI", 190, c['ink'], self.disp, 900, ls=-6) + T(486, 840, 'HOW AI WORKS. ON EXAMPLES YOU CAN COUNT.', 44, c['lime'], self.mono, 700, ls=2)
    return svg(2560, 1440, b, cls='bannersvg')

# ---- 3 Riso Print ----
class Riso(Style):
  n = 3; slug = 'riso-print'; name = 'Riso Print'
  fonts = 'family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=IBM+Plex+Mono:wght@500;600'
  disp = "'Bricolage Grotesque',sans-serif"; mono = "'IBM Plex Mono',monospace"; objfont = "'Bricolage Grotesque',sans-serif"
  c = dict(bg='#F4EEDF', pink='#FF48B0', blue='#0078BF', ink='#1D2B6B', gray='#6B6A82')
  roles = dict(dark='#0078BF', light='#F4EEDF', faint='#F9B8DA', alt='#0078BF', onalt='#F4EEDF', accent='#FF48B0', ink='#1D2B6B', leaf='#0078BF', noise=['#0078BF', '#FF48B0', '#7A5BA8', '#F4EEDF'])
  intro = 'Плакат двухцветной ризографии: флуоресцентный розовый и синий, наложение красок даёт фиолетовый, зерно и сдвиг печати. Тёплый, ручной, но взрослый — как афиша галереи.'
  takes = 'От лидеров: узнаваемый цвет канала узнаётся в ленте без названия — приём Kurzgesagt. Отличие: печатная фактура вместо гладкого вектора; в теме ИИ так не делает никто из 16 разобранных.'
  risk = 'Риск: фактура требует меры, иначе мешает читать. Слова на экране — только плотным цветом.'
  sw = [('#F4EEDF', 'бумага'), ('#FF48B0', 'флуо-розовый'), ('#0078BF', 'синий'), ('#7A5BA8', 'наложение'), ('#1D2B6B', 'текст')]
  fl = [('Bricolage Grotesque', 'заголовки 800, текст 500'), ('IBM Plex Mono', 'подписи и счёт')]
  def dots(self, w, h, col, op=.5, step=10):
    pid = uid('ht')
    return (f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><circle cx="{step/2}" cy="{step/2}" r="{step*.28}" fill="{col}"/></pattern>', f'<rect width="{w}" height="{h}" fill="url(#{pid})" opacity="{op}"/>')
  def mis(self, body, dx=5, dy=-3):
    """Print the same shapes again in pink, shifted: misregistration."""
    return f'<g style="mix-blend-mode:multiply">{body}</g>'
  def thumb(self, i, tp):
    c = self.c; d, ht = self.dots(640, 360, c['pink'], .22, 9); d2, ht2 = self.dots(640, 360, c['blue'], .9, 8)
    cid = uid('rc')
    b = f'<rect width="640" height="360" fill="{c["bg"]}"/>{ht}'
    d += f'<clipPath id="{cid}"><circle cx="470" cy="300" r="190"/></clipPath>'
    b += f'<g clip-path="url(#{cid})">{ht2}</g>'
    F = dict(self.roles, dark=c['blue'], light=c['bg'], alt=c['pink'], onalt=c['bg'], accent=c['pink'], ink=c['blue'], tagink=c['blue'], faint='#F9B8DA')
    b += put(tp['obj'], 455, 268, 172 if tp["obj"] != "map" else 185, F, self.objfont)
    for j, ln in enumerate(tp['w']):
      sz = fit(ln, 70, 580, .58); y = 92 + j * 70
      b += hlline(36, y, ln, '', sz, c['pink'], c['pink'], self.disp, 800, ls=-1).replace('<text ', '<text transform="translate(4 4)" ')
      b += hlline(32, y, ln, '', sz, c['blue'], c['blue'], self.disp, 800, ls=-1).replace('<text ', '<text style="mix-blend-mode:multiply" ')
    b += T(32, 300, 'COUNTABLE AI', 18, c['blue'], self.mono, 600, ls=2) + T(32, 326, f'no. {i+1}', 18, c['pink'], self.mono, 600)
    b += grain(640, 360, .22)
    return svg(640, 360, b, d, 'thumbsvg')
  def frames(self):
    c = self.c; out = []
    d, ht = self.dots(1600, 900, c['pink'], .22, 16)
    b = f'<rect width="1600" height="900" fill="{c["bg"]}"/>{ht}'
    for j, m in enumerate(MSGS):
      y = 170 + j * 230; x = 140 + j * 90
      b += f'<rect x="{x+10}" y="{y-8}" width="1060" height="170" rx="85" fill="{c["pink"]}" style="mix-blend-mode:multiply"/><rect x="{x}" y="{y}" width="1060" height="170" rx="85" fill="{c["blue"]}" style="mix-blend-mode:multiply"/>'
      b += T(x + 80, y + 112, m, 84, c['bg'], self.disp, 800)
    b += T(1480, 840, 'all true.', 70, c['pink'], self.disp, 800, 'end') + grain(1600, 900, .2)
    out.append((svg(1600, 900, b, d, 'framesvg'), 'Everything it read: three true messages.'))
    d, ht = self.dots(1600, 900, c['blue'], .16, 16)
    b = f'<rect width="1600" height="900" fill="{c["bg"]}"/>{ht}' + T(120, 190, 'Mom is at the …', 120, c['ink'], self.disp, 800)
    for j, wd in enumerate(['store', 'gym', 'park']):
      cx = 330 + j * 470; col = c['pink'] if j == 1 else c['blue']
      b += f'<circle cx="{cx}" cy="530" r="200" fill="{col}" style="mix-blend-mode:multiply"/>' + T(cx, 520, wd, 90, c['bg'], self.disp, 800, 'middle') + T(cx, 610, '1 in 3', 52, c['bg'], self.mono, 600, 'middle')
    b += T(120, 840, 'it only looks at "the"', 52, c['blue'], self.disp, 800) + grain(1600, 900, .2)
    out.append((svg(1600, 900, b, d, 'framesvg'), 'After "the": store 1 · gym 1 · park 1.'))
    d, ht = self.dots(1600, 900, c['pink'], .3, 16)
    b = f'<rect width="1600" height="900" fill="{c["bg"]}"/>{ht}'
    b += T(126, 300, 'Mom is at', 170, c['pink'], self.disp, 800).replace('<text ', '<text style="mix-blend-mode:multiply" ') + T(120, 306, 'Mom is at', 170, c['blue'], self.disp, 800).replace('<text ', '<text style="mix-blend-mode:multiply" ')
    b += T(126, 480, 'the gym.', 170, c['pink'], self.disp, 800)
    b += f'<rect x="1000" y="140" width="460" height="460" rx="230" fill="{c["blue"]}" style="mix-blend-mode:multiply"/>' + T(1230, 420, '6/9', 170, c['bg'], self.disp, 800, 'middle') + T(1230, 500, 'false', 54, c['bg'], self.mono, 600, 'middle')
    b += T(120, 720, 'Every pair of words was true.', 64, c['ink'], self.disp, 800) + T(120, 800, 'The sentence is not.', 64, c['pink'], self.disp, 800) + grain(1600, 900, .2)
    out.append((svg(1600, 900, b, d, 'framesvg'), 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false.'))
    return out
  def short(self):
    c = self.c; d, ht = self.dots(540, 960, c['pink'], .25, 12)
    b = f'<rect width="540" height="960" fill="{c["bg"]}"/>{ht}<circle cx="430" cy="390" r="150" fill="{c["blue"]}" style="mix-blend-mode:multiply"/>'
    b += T(40, 150, 'Every word', 72, c['ink'], self.disp, 800) + T(40, 230, 'was true.', 72, c['ink'], self.disp, 800)
    b += f'<rect x="40" y="420" width="460" height="110" rx="55" fill="{c["pink"]}"/>' + T(80, 492, 'Mom is at the gym.', 44, c['bg'], self.disp, 800)
    b += T(40, 720, 'The sentence', 72, c['blue'], self.disp, 800) + T(40, 800, 'was false.', 72, c['pink'], self.disp, 800) + T(40, 900, '6 of 9 · count it', 30, c['ink'], self.mono, 600) + grain(540, 960, .22)
    return svg(540, 960, b, d, 'shortsvg')
  def avatar(self):
    c = self.c
    return (f'<rect width="100" height="100" fill="{c["bg"]}"/><circle cx="40" cy="50" r="28" fill="{c["blue"]}" style="mix-blend-mode:multiply"/><circle cx="60" cy="50" r="28" fill="{c["pink"]}" style="mix-blend-mode:multiply"/>'
            + T(50, 60, 'CA', 28, c['bg'], self.disp, 800, 'middle'))
  def banner(self):
    c = self.c; d, ht = self.dots(2560, 1440, c['pink'], .2, 22)
    b = f'<rect width="2560" height="1440" fill="{c["bg"]}"/>{ht}<circle cx="2200" cy="300" r="520" fill="{c["blue"]}" style="mix-blend-mode:multiply"/><circle cx="300" cy="1300" r="420" fill="{c["pink"]}" style="mix-blend-mode:multiply"/>'
    b += T(566, 756, 'Countable AI', 210, c['pink'], self.disp, 800).replace('<text ', '<text style="mix-blend-mode:multiply" ') + T(560, 750, 'Countable AI', 210, c['blue'], self.disp, 800).replace('<text ', '<text style="mix-blend-mode:multiply" ')
    b += T(566, 850, 'how AI works — on examples you can count', 52, c['ink'], self.mono, 600) + grain(2560, 1440, .18)
    return svg(2560, 1440, b, d, 'bannersvg')

# ---- 4 Soft 3D ----
class Gloss(Style):
  n = 4; slug = 'soft-3d'; name = 'Soft 3D'
  fonts = 'family=Sora:wght@400;600;800'
  disp = "'Sora',sans-serif"; mono = "'Sora',sans-serif"; objfont = "'Sora',sans-serif"
  c = dict(bg='#0C1030', bg2='#2B1E66', ink='#FFFFFF', cyan='#63E6FF', coral='#FF6B81', gray='#A8ACD6')
  intro = 'Глянцевые объёмные предметы на глубоком сине-фиолетовом градиенте, стеклянные карточки, мягкий свет. Как презентации Apple и сайты технологических компаний — дорогой, современный вид.'
  takes = 'От лидеров: тёмный фон — привычка канала 3Blue1Brown и его последователей; мы берём только глубину цвета. Отличие: вместо светящихся сетей — объёмные бытовые предметы: телефон, пицца, кубик.'
  risk = 'Риск: глянец ближе всех к «технологичному» шаблону. Отличие держат бытовые предметы, без сетей и роботов.'
  sw = [('#0C1030', 'фон'), ('#2B1E66', 'фон 2'), ('#63E6FF', 'главное'), ('#FF6B81', 'ошибка'), ('#A8ACD6', 'подписи')]
  fl = [('Sora', 'всё: заголовки 800, текст 400–600')]
  def defs(self):
    c = self.c
    return (f'<linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>'
            '<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7B6CFF" stop-opacity=".75"/><stop offset="1" stop-color="#7B6CFF" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="gdark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4A4F7A"/><stop offset=".5" stop-color="#1B1E3A"/><stop offset="1" stop-color="#0A0B1A"/></linearGradient>'
            '<linearGradient id="glight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9DDF7"/></linearGradient>'
            '<linearGradient id="galt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9AF0FF"/><stop offset="1" stop-color="#3AA8FF"/></linearGradient>'
            '<linearGradient id="gacc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF9AA8"/><stop offset="1" stop-color="#E8335A"/></linearGradient>'
            '<linearGradient id="gleaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8CF5B5"/><stop offset="1" stop-color="#1FAE6A"/></linearGradient>'
            '<linearGradient id="gcrust" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE08A"/><stop offset="1" stop-color="#E39A2D"/></linearGradient>'
            '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="14"/><feOffset dy="18"/><feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
  roles = dict(dark='url(#gdark)', light='url(#glight)', faint='#C9CEF0', alt='url(#galt)', onalt='#0C1030', accent='url(#gacc)', ink='#FFFFFF', leaf='url(#gleaf)', noise=['#1B1E3A', '#4A4F7A', '#8A8FC0', '#D9DDF7'])
  def F(self):
    f = dict(self.roles); return f
  def bg(self, w, h, gx=.72, gy=.5):
    return f'<rect width="{w}" height="{h}" fill="url(#gbg)"/><circle cx="{w*gx}" cy="{h*gy}" r="{h*.62}" fill="url(#glow)"/>'
  def glass(self, x, y, w, h, r):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#FFFFFF" fill-opacity=".09" stroke="#FFFFFF" stroke-opacity=".28" stroke-width="2"/>'
  def thumb(self, i, tp):
    c = self.c; b = self.bg(640, 360, .5, .68)
    F = dict(self.F(), tagink='#0C1030')
    if tp['obj'] == 'pizza': F = dict(F, alt='url(#gcrust)')
    ln = ' '.join(tp['w']); sz = fit(ln, 40, 590, .62)
    b += hlline(320, 66, ln, tp['hl'], sz, '#FFFFFF', c['cyan'], self.disp, 800, 'middle', -1)
    b += f'<g filter="url(#soft)">{put(tp["obj"], 320, 222, 170 if tp["obj"] != "map" else 190, F, self.objfont)}</g>'
    return svg(640, 360, b, self.defs(), 'thumbsvg')
  def frames(self):
    c = self.c; out = []; F = self.F()
    b = self.bg(1600, 900)
    for j, m in enumerate(MSGS):
      y = 170 + j * 200
      b += self.glass(160, y, 900, 140, 70) + T(230, y + 92, m, 64, '#FFFFFF', self.disp, 600) + f'<circle cx="1130" cy="{y+70}" r="38" fill="url(#gleaf)"/>' + f'<path d="M1112 {y+70} l14 14 l26 -30" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>'
    b += f'<g filter="url(#soft)">{phone(1360, 470, 330, dict(F, alt="url(#glight)"), self.objfont, msg="", bad=False).split("<rect x=\"" + str(1360 - .62 * 330)[:6])[0]}</g>'
    b += T(160, 800, 'Training data: 3 true messages', 40, c['gray'], self.disp, 400)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'Everything it read: three true messages.'))
    b = self.bg(1600, 900) + T(160, 200, 'Mom is at the', 100, '#FFFFFF', self.disp, 800) + self.glass(960, 110, 300, 120, 60) + T(1110, 195, '?', 90, c['cyan'], self.disp, 800, 'middle')
    for j, wd in enumerate(['store', 'gym', 'park']):
      x = 160 + j * 440
      b += self.glass(x, 340, 400, 400, 48) + T(x + 200, 500, wd, 80, '#FFFFFF', self.disp, 800, 'middle')
      b += f'<rect x="{x+60}" y="580" width="280" height="22" rx="11" fill="#FFFFFF" fill-opacity=".15"/><rect x="{x+60}" y="580" width="{280/3:.0f}" height="22" rx="11" fill="{"url(#gacc)" if j==1 else "url(#galt)"}"/>' + T(x + 200, 680, '1 in 3', 48, c['gray'], self.disp, 600, 'middle')
    b += T(160, 830, 'It looks only at the last word: "the"', 40, c['gray'], self.disp, 400)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'After "the": store 1 · gym 1 · park 1.'))
    b = self.bg(1600, 900) + f'<g filter="url(#soft)">{phone(1250, 450, 560, F, self.objfont)}</g>'
    b += T(140, 230, '6 of 9', 170, '#FFFFFF', self.disp, 800) + T(150, 310, 'possible sentences are false', 44, c['coral'], self.disp, 600)
    for j in range(9):
      x = 150 + (j % 3) * 110; y = 400 + (j // 3) * 110; ok = j % 4 == 0
      b += f'<circle cx="{x+40}" cy="{y+40}" r="40" fill="{"url(#gleaf)" if ok else "url(#gacc)"}"/>'
    b += T(150, 790, 'Every pair of words was true.', 40, c['gray'], self.disp, 400)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false.'))
    return out
  def short(self):
    c = self.c; b = self.bg(540, 960) + T(40, 130, 'Every word', 64, '#FFFFFF', self.disp, 800) + T(40, 205, 'was true.', 64, '#FFFFFF', self.disp, 800)
    b += f'<g filter="url(#soft)">{phone(330, 500, 330, self.F(), self.objfont)}</g>'
    b += T(40, 800, 'The sentence', 64, '#FFFFFF', self.disp, 800) + T(40, 875, 'was false.', 64, c['coral'], self.disp, 800)
    return svg(540, 960, b, self.defs(), 'shortsvg')
  def avatar(self):
    return ('<rect width="100" height="100" fill="url(#gbg)"/><circle cx="50" cy="50" r="40" fill="url(#galt)"/><ellipse cx="38" cy="34" rx="16" ry="9" fill="#fff" opacity=".55"/>'
            + T(50, 63, 'C', 40, '#0C1030', self.disp, 800, 'middle'))
  def banner(self):
    c = self.c; b = self.bg(2560, 1440)
    b += f'<g filter="url(#soft)">{dice(2150, 720, 560, self.F(), self.objfont).split("<rect")[0]}{pizza(300, 720, 380, dict(self.F(), alt="url(#gcrust)"), self.objfont).split("<path")[0]}</g>'
    b += T(560, 740, 'Countable AI', 190, '#FFFFFF', self.disp, 800, ls=-4) + T(566, 840, 'How AI works — on examples you can count.', 52, c['cyan'], self.disp, 600)
    return svg(2560, 1440, b, self.defs(), 'bannersvg')

# ---- 5 Noir ----
class Noir(Style):
  n = 5; slug = 'noir'; name = 'Noir'
  fonts = 'family=Bebas+Neue&family=IBM+Plex+Mono:wght@500;600'
  disp = "'Bebas Neue',sans-serif"; mono = "'IBM Plex Mono',monospace"; objfont = "'IBM Plex Mono',monospace"
  c = dict(bg='#0A0A0A', light='#F3E7CC', amber='#FFB000', red='#E5251B', gray='#8D8678')
  roles = dict(tagink='#0A0A0A', dark='#1C1B19', light='#E9DEC4', faint='#B9B09A', alt='#F3E7CC', onalt='#0A0A0A', accent='#E5251B', ink='#F3E7CC', leaf='#6E8B4E', noise=['#0A0A0A', '#3A3732', '#8D8678', '#E9DEC4'], dstroke=' stroke="#5C5648" stroke-width="3"')
  intro = 'Кадр как в детективе: темнота, один предмет в луче света, узкий высокий шрифт, плёночное зерно, бирки «улика». Каждое видео — расследование ошибки ИИ.'
  takes = 'От лидеров: интрига в заголовке — приём самых просматриваемых видео выдачи («Terrifying Line», «Doesn\'t Know Anything»). Отличие: тайну раскрывает счёт на глазах, а не страшилка.'
  risk = 'Риск: мрачность может отпугнуть часть зрителей. Тон голоса — спокойный, без нагнетания.'
  sw = [('#0A0A0A', 'темнота'), ('#F3E7CC', 'свет'), ('#FFB000', 'бирка, главное'), ('#E5251B', 'ошибка'), ('#8D8678', 'подписи')]
  fl = [('Bebas Neue', 'заголовки, только заглавные'), ('IBM Plex Mono', 'бирки, подписи, счёт')]
  def defs(self):
    return ('<radialGradient id="spot" cx=".5" cy=".42" r=".55"><stop offset="0" stop-color="#F3E7CC" stop-opacity=".42"/><stop offset=".55" stop-color="#F3E7CC" stop-opacity=".08"/><stop offset="1" stop-color="#F3E7CC" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>')
  def bg(self, w, h, sx=.7, sy=.5, sr=.6):
    return f'<rect width="{w}" height="{h}" fill="{self.c["bg"]}"/><ellipse cx="{w*sx}" cy="{h*sy}" rx="{h*sr*1.2}" ry="{h*sr}" fill="url(#spot)"/>'
  def end(self, w, h): return f'<rect width="{w}" height="{h}" fill="url(#vig)"/>{grain(w,h,.3)}'
  def tag(self, x, y, s, size, rot=-4):
    w = len(s) * size * .62 + size * 1.2
    return f'<g transform="rotate({rot} {x} {y})"><rect x="{x}" y="{y-size*1.05}" width="{w:.0f}" height="{size*1.5:.0f}" fill="{self.c["amber"]}"/>' + T(x + size * .6, y, s, size, '#0A0A0A', self.mono, 600, ls=1) + '</g>'
  def thumb(self, i, tp):
    c = self.c; b = self.bg(640, 360, .27, .45, .6)
    b += self.obj(tp['obj'], 170, 185, 170 if tp['obj'] != 'map' else 185)
    for j, ln in enumerate(tp['w']):
      sz = fit(ln, 88, 300, .4)
      b += hlline(612, 140 + j * 86, ln, tp['hl'], sz, c['light'], c['amber'], self.disp, 400, 'end', 1)
    b += self.tag(470, 48, f'EXHIBIT {i+1:02d}', 17, -3)
    b += self.end(640, 360)
    return svg(640, 360, b, self.defs(), 'thumbsvg')
  def frames(self):
    c = self.c; out = []
    b = self.bg(1600, 900, .5, .45, .7) + T(120, 150, 'THE EVIDENCE', 110, c['light'], self.disp, ls=4)
    for j, m in enumerate(MSGS):
      x = 140 + j * 470; y = 300 + (j % 2) * 40
      b += f'<g transform="rotate({(-3, 2, -1)[j]} {x+200} {y+150})"><rect x="{x}" y="{y}" width="420" height="300" fill="{c["light"]}"/><rect x="{x+20}" y="{y+20}" width="380" height="200" fill="#D8CCAF"/>'
      b += T(x + 210, y + 135, m.split(' is ')[0], 72, '#0A0A0A', self.disp, anchor='middle') + T(x + 210, y + 270, m, 24, '#0A0A0A', self.mono, 600, 'middle') + '</g>'
      b += self.tag(x + 10, y + 380, f'TRUE · {j+1}', 24, (-3, 2, -1)[j])
    b += T(120, 830, 'ALL IT EVER READ: THREE TRUE MESSAGES.', 36, c['gray'], self.mono, 600) + self.end(1600, 900)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'Everything it read: three true messages.'))
    b = self.bg(1600, 900, .3, .35, .55) + T(120, 250, 'MOM IS AT THE', 170, c['light'], self.disp, ls=3) + f'<rect x="1000" y="120" width="420" height="140" fill="none" stroke="{c["amber"]}" stroke-width="6" stroke-dasharray="20 14"/>' + T(1210, 235, '?', 130, c['amber'], self.disp, anchor='middle')
    for j, wd in enumerate(['STORE', 'GYM', 'PARK']):
      x = 140 + j * 450
      b += T(x, 520, wd, 140, c['amber'] if j == 1 else c['light'], self.disp, ls=3) + f'<path d="M{x} 560H{x+360}" stroke="{c["gray"]}" stroke-width="3"/>' + T(x, 630, 'SEEN 1 TIME · 1 IN 3', 30, c['gray'], self.mono, 600)
    b += T(120, 820, 'SUSPECT LOOKS ONLY AT THE LAST WORD: "THE".', 34, c['gray'], self.mono, 600) + self.end(1600, 900)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'After "the": store 1 · gym 1 · park 1.'))
    b = self.bg(1600, 900, .74, .45, .65) + f'<g>{phone(1290, 470, 470, self.roles, self.objfont)}</g>'
    b += T(120, 280, 'A LIE', 180, c['light'], self.disp, ls=4) + T(120, 460, 'MADE OF', 180, c['light'], self.disp, ls=4) + T(120, 640, 'TRUE WORDS', 180, c['amber'], self.disp, ls=4)
    b += self.tag(130, 820, 'VERDICT: 6 OF 9 SENTENCES FALSE', 30) + self.end(1600, 900)
    out.append((svg(1600, 900, b, self.defs(), 'framesvg'), 'It wrote "Mom is at the gym." 6 of 9 possible sentences are false.'))
    return out
  def short(self):
    c = self.c; b = self.bg(540, 960, .5, .5, .6) + T(40, 170, 'A LIE MADE', 110, c['light'], self.disp, ls=2) + T(40, 280, 'OF TRUE WORDS', 98, c['amber'], self.disp, ls=2)
    b += f'<g>{phone(330, 580, 330, self.roles, self.objfont)}</g>' + self.tag(40, 900, '6 OF 9 FALSE', 28) + self.end(540, 960)
    return svg(540, 960, b, self.defs(), 'shortsvg')
  def avatar(self):
    c = self.c
    return f'<rect width="100" height="100" fill="#0A0A0A"/><ellipse cx="50" cy="42" rx="44" ry="38" fill="url(#spot)"/>' + T(50, 70, 'CA', 58, c['light'], self.disp, anchor='middle', ls=2) + f'<rect x="28" y="78" width="44" height="6" fill="{c["amber"]}"/>'
  def banner(self):
    c = self.c; b = self.bg(2560, 1440, .5, .5, .45)
    b += T(1280, 760, 'COUNTABLE AI', 260, c['light'], self.disp, anchor='middle', ls=10) + self.tag(1000, 870, 'EVERY ANSWER CHECKED BY COUNTING', 40, -2) + self.end(2560, 1440)
    return svg(2560, 1440, b, self.defs(), 'bannersvg')

STYLES = [Editorial(), Swiss(), Riso(), Gloss(), Noir()]

def ensure_svg(k, x):
  """Frame helpers return either a finished <svg> or a bare body."""
  if isinstance(x, str) and x.startswith('<svg'): return x
  return svg(1600, 900, x, getattr(k, 'defs', lambda: '')(), 'framesvg')

def thumbs(k): return [k.thumb(i, tp) for i, tp in enumerate(TOPICS)]

def avatar(k, px):
  d = getattr(k, 'defs', lambda: '')(); cid = uid('cl')
  return f'<svg viewBox="0 0 100 100" style="width:{px}px;height:{px}px;border-radius:50%;display:block;flex:none" role="img" aria-label="аватар"><defs>{d}<clipPath id="{cid}"><circle cx="50" cy="50" r="50"/></clipPath></defs><g clip-path="url(#{cid})">{k.avatar()}</g></svg>'

CSS = '''*{box-sizing:border-box}body{margin:0;background:#F4F4F2;color:#141414;font-family:'Inter',system-ui,sans-serif}
main{max-width:1240px;margin:auto;padding:40px 32px 64px}svg{display:block;width:100%;height:auto}
.meta{display:flex;justify-content:space-between;gap:12px;font-size:12px;letter-spacing:1px;color:#6b6b6b;border-top:1px solid #ddd;padding-top:16px}
h1{font-size:60px;line-height:1.05;margin:28px 0 12px;font-weight:800;letter-spacing:-1px}
.intro{font-size:18px;line-height:1.6;max-width:780px;margin:0 0 16px}
.box{background:#fff;border:1px solid #e2e2e2;border-radius:12px;padding:16px 20px;font-size:15px;line-height:1.6;max-width:860px;margin:0 0 10px}
section{border-top:1px solid #ddd;padding:32px 0 40px}h2{font-size:26px;margin:0 0 6px;font-weight:800}.note{color:#666;font-size:14px;margin:0 0 22px;line-height:1.5}
.yt{background:#fff;border-radius:16px;overflow:hidden;border:1px solid #e2e2e2;font-family:Roboto,Arial,sans-serif}
.yt .in{padding:20px 24px 28px}.ch{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-top:18px}
.ch h3{font-size:30px;margin:0;font-weight:700}.ch p{margin:4px 0;color:#606060;font-size:14px}
.sub{margin-left:auto;background:#0f0f0f;color:#fff;border-radius:20px;padding:10px 18px;font-size:14px}
.tabs{display:flex;gap:28px;border-bottom:1px solid #e5e5e5;margin:18px 0 20px;font-size:15px;overflow-x:auto}.tabs span{padding:12px 0}.tabs span:first-child{border-bottom:2px solid #0f0f0f;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 16px}.thumb{border-radius:12px;overflow:hidden;position:relative}
.dur{position:absolute;right:8px;bottom:8px;background:rgba(0,0,0,.8);color:#fff;font-size:12px;padding:2px 5px;border-radius:4px}
.video h4{font-size:15px;line-height:1.35;margin:10px 0 3px;font-weight:600}.vmeta{font-size:12px;color:#606060;margin:0}
.small{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;max-width:1000px}.small .thumb{border-radius:6px}
.frames{display:grid;gap:26px}figure{margin:0}figure svg{border-radius:10px}figcaption{font-size:14px;margin-top:8px;color:#444}
.shorts{display:grid;grid-template-columns:300px 1fr;gap:48px;align-items:center}.short{border-radius:16px;overflow:hidden;max-width:300px}
.shorts p{color:#555;line-height:1.6}
.sw{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.swatch{height:64px;border-radius:8px;border:1px solid #ddd}.sw p{font-size:12px;margin:8px 0}.sw small{color:#777}
.font-row{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid #e2e2e2;padding:14px 0;align-items:baseline;flex-wrap:wrap}.font-row b{font-size:30px;font-weight:400}.font-row span{font-size:13px;color:#666}
footer{border-top:1px solid #ddd;padding-top:20px;font-size:13px;color:#666;line-height:1.6}
.row{display:grid;grid-template-columns:120px repeat(3,1fr);gap:14px;align-items:center;margin-bottom:22px}.row h3{margin:0;font-size:18px}
@media(max-width:820px){main{padding:24px 16px 48px}h1{font-size:40px}.grid,.shorts{grid-template-columns:1fr}.small{grid-template-columns:repeat(3,1fr)}.sw{grid-template-columns:repeat(3,1fr)}.yt .in{padding:16px}.sub{margin-left:0}.row{grid-template-columns:1fr 1fr}.row h3{grid-column:1/-1}}'''

ALLFONTS = 'family=Inter:wght@400;600;800'

def head(title, fonts):
  return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>'
          f'<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?{ALLFONTS}&{fonts}&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><main>')

def page(k):
  th = thumbs(k)
  durs = ['8:45', '9:30', '7:50', '10:15', '8:20', '9:05']
  vids = ''.join(f'<div class="video"><div class="thumb">{t}<span class="dur">{durs[i]}</span></div><h4>{esc(TOPICS[i]["t"])}</h4><p class="vmeta">{"Pilot · " if i == 0 else "Plan · "}{TOPICS[i]["s"]}</p></div>' for i, t in enumerate(th))
  small = ''.join(f'<div class="thumb">{t}</div>' for t in th)
  frames = ''.join(f'<figure>{ensure_svg(k, sv)}<figcaption>{esc(cp)}</figcaption></figure>' for sv, cp in k.frames())
  sw = ''.join(f'<div><div class="swatch" style="background:{h}"></div><p>{h}<br><small>{d}</small></p></div>' for h, d in k.sw)
  fam = lambda f: f"'{f}'"
  fl = ''.join(f'<div class="font-row"><b style="font-family:{fam(f)}">{f} — Countable AI</b><span>{d} · OFL 1.1</span></div>' for f, d in k.fl)
  return head(f'Countable AI — {k.name}', k.fonts) + f'''
<div class="meta"><span>ОФОРМЛЕНИЕ КАНАЛА · ВТОРОЙ КРУГ · СТИЛЬ {k.n} ИЗ 5</span><span>2026-10-17</span></div>
<h1>{k.name}</h1><p class="intro">{k.intro}</p>
<p class="box"><b>Что берёт у лидеров и чем отличается.</b> {k.takes}</p><p class="box">{k.risk}</p>
<section><h2>Страница канала</h2><p class="note">Так канал выглядит на YouTube. Шесть тем из плана, у каждой бытовой пример; пилот — первая. Название рабочее, канал не создан.</p>
<div class="yt">{k.banner()}<div class="in"><div class="ch">{avatar(k,96)}<div><h3>Countable AI</h3><p>@CountableAI · 6 videos</p><p>How AI works — on examples you can count yourself.</p></div><span class="sub">Subscribe</span></div>
<div class="tabs"><span>Videos</span><span>Shorts</span><span>Playlists</span><span>About</span></div><div class="grid">{vids}</div></div></div></section>
<section><h2>В ленте телефона</h2><p class="note">Обложки в малом размере, как в рекомендациях. Проверка: читаются ли 3–4 слова.</p><div class="small">{small}</div>
<div style="display:flex;gap:28px;align-items:end;margin-top:26px">{avatar(k,176)}{avatar(k,88)}{avatar(k,36)}</div><p class="note" style="margin-top:8px">Аватар: 176, 88 и 36 px.</p></section>
<section><h2>Кадры пилота</h2><p class="note">Три шага одного объяснения. Голос ElevenLabs ведёт объяснение; на экране — только ключевые слова. Полные субтитры — дорожкой YouTube.</p><div class="frames">{frames}</div></section>
<section><h2>Shorts</h2><div class="shorts"><div class="short">{k.short()}</div><div><h3 style="margin:0 0 10px">Одна ошибка — один Short</h3><p>Кадр 1080 × 1920, около 40 секунд: выучила, ошиблась, посчитали. Крупные слова на экране: Shorts часто смотрят без звука — гипотеза, данных нет.</p></div></div></section>
<section><h2>Палитра и шрифты</h2><div class="sw">{sw}</div>{fl}</section>
<footer>Шрифты — SIL Open Font License 1.1, файлы лицензий проверены в google/fonts 2026-10-17. Фото, чужих иллюстраций, иконок и логотипов нет: всё нарисовано кодом. Темы 2–6 — план, видео не сделаны; длительности — оценка. Пример «Mom is at the store» — тот же счёт, что в пилоте: 9 предложений, ложных 6.</footer>
</main></body></html>'''

def overview():
  rows = ''
  fonts = '&'.join(k.fonts for k in STYLES)
  for k in STYLES:
    th = thumbs(k)
    rows += f'<div class="row"><h3>{k.n}. {k.name}</h3>' + ''.join(f'<div class="thumb">{th[i]}</div>' for i in (0, 1, 4)) + '</div>'
  return head('Countable AI — пять стилей', fonts) + f'''
<div class="meta"><span>ОФОРМЛЕНИЕ КАНАЛА · ВТОРОЙ КРУГ</span><span>2026-10-17</span></div>
<h1>Пять стилей рядом</h1><p class="intro">Три обложки каждого стиля: пилот, тема 2, тема 5. Стили отличаются материалом, шрифтом, цветом и композицией. Ни в одном нет пастели, рукописного шрифта, героя-талисмана, сетей и роботов.</p>
<section>{rows}</section>
<footer>Подробно — по слайду на стиль. Всё нарисовано кодом; шрифты — OFL 1.1.</footer></main></body></html>'''

if __name__ == '__main__':
  for k in STYLES:
    open(f'{OUT}/look-{k.n}-{k.slug}.html', 'w').write(page(k))
    print(k.n, k.slug)
  open(f'{OUT}/looks-overview.html', 'w').write(overview())
````
