# tmp/pilot/engine.py

Движок таймлайна: расчёт времени слов, кадры, элементы, субтитры.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/engine.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Timeline engine for the silent pilot: shots with narration, elements with cues, captions.
Times come from narration word counts (about 150 wpm); a voice track later replaces word times."""
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../mock'))
from gen4 import (DEFS, INK, WHITE, LIME, RED, GRAY, T, tw, ttext, outline, paper, tape, card, reg, vtext,
                  halftone, streaks, marker, K, uid, esc, COND, WIDE)

D = K.disp; M = K.mono
FPS = 30
DUR = dict(none=0, fade=.4, slideL=.55, slideR=.55, drop=.5, rise=.5, stamp=.22, pop=.35, zoom=.3, draw=1.2, type=1, wipe=.35, flick=.45)

SHOTS = []

def mw(s, size, ls=0): return len(s) * (.6 * size + ls)

class Shot:
  def __init__(self, n, sec, narr, tr='glitch', hold=0., lead=.3, tail=.5):
    self.n, self.sec, self.narr, self.tr, self.hold, self.lead, self.tail = n, sec, narr, tr, hold, lead, tail
    self.body = ''; self.els = []; SHOTS.append(self)

  def add(self, svg): self.body += svg; return self

  def E(self, i, body, cx=800, cy=450, a='fade', at=0., d=None, fx=None, o=None, mv=None, **p):
    i = f's{self.n}_{i}'
    self.body += f'<g id="{i}" data-c="{cx:.1f} {cy:.1f}">{body}</g>'
    self.els.append(dict(id=i, a=a, at=at, d=DUR[a] if d is None else d, fx=fx or {}, o=o, mv=mv, p=p))
    return i

# ---------- narration timing ----------
def tokens(narr):
  out = []
  for para in narr.strip().split('\n'):
    for w in para.split():
      out.append(w)
    if out: out[-1] = out[-1] + '¶'
  return out

def letters(w):
  core = re.sub(r'[^A-Za-z0-9%]', '', w)
  n = sum(3 if c.isdigit() else (6 if c == '%' else 1) for c in core)
  return n

def word_times(narr, t0):
  """Start and end time of each token; tokens without letters are pauses."""
  out = []; t = t0
  for w in tokens(narr):
    n = letters(w); s = t
    if n: t += .11 + .054 * n
    e = t
    tail = w.rstrip('¶"”\')')
    if w in ('—', '–'): t += .25
    elif tail.endswith(('.', '?', '!', '…')): t += .4
    elif tail.endswith(':'): t += .25
    elif tail.endswith((',', ';', '—')): t += .2
    if w.endswith('¶'): t += .3
    out.append((w.rstrip('¶'), s, e))
  return out, t

def norm(w): return re.sub(r'[^a-z0-9%\-]', '', w.lower())

def build():
  t = 0.; caps = []; els = []; shots = []
  for sh in SHOTS:
    wt, tend = word_times(sh.narr, t + sh.lead)
    t1 = tend + sh.tail + sh.hold
    t1 = round(t1 * FPS) / FPS
    cur = 0
    def cue(spec):
      nonlocal cur
      if isinstance(spec, (int, float)): return t + spec
      if spec.startswith('e'): return t1 + float(spec[1:])
      m = re.match(r'w:([^+#]+)(?:#(\d+))?((?:\+-?[\d.]+)*)$', spec)
      if not m: raise SystemExit(f"shot {sh.n}: bad cue {spec!r}")
      word, skip = m.group(1).lower(), int(m.group(2) or 1)
      off = sum(float(x) for x in m.group(3).split('+') if x)
      k = cur
      while k < len(wt):
        if norm(wt[k][0]) == norm(word):
          skip -= 1
          if skip == 0: break
        k += 1
      if k >= len(wt): raise SystemExit(f'shot {sh.n}: cue {spec!r} not found after token {cur}')
      cur = k
      return wt[k][1] + off
    def peek(spec):
      nonlocal cur
      c = cur; v = cue(spec); cur = c; return v
    for e in sh.els:
      t_at = cue(e['at']); d = e['d']
      if isinstance(d, str): d = peek(d) - t_at
      e2 = dict(id=e['id'], a=e['a'], t=round(t_at, 3), d=round(d, 3))
      for key, v in e['fx'].items():
        e2[key] = [round(peek(x), 3) if isinstance(x, str) else x for x in v] if isinstance(v, list) else v
      if e['o']: e2['o'] = [round(peek(e['o'][0]), 3), e['o'][1]]
      if e['mv']: e2['mv'] = [round(peek(e['mv'][0]), 3)] + list(e['mv'][1:])
      e2.update(e['p'])
      els.append(dict(e2, s=sh.n))
    shots.append(dict(n=sh.n, sec=sh.sec, t0=round(t, 3), t1=round(t1, 3), tr=sh.tr, words=len([w for w in wt if letters(w[0])])))
    caps += captions(wt)
    t = t1
  return shots, els, caps

def captions(wt, maxc=84):
  """Sentence chunks of at most two 42-character lines, timed by their words."""
  sents = []; cur = []
  for w in wt:
    cur.append(w)
    if re.search(r'[.?!…]["”\')]*$', w[0]): sents.append(cur); cur = []
  if cur: sents.append(cur)
  out = []
  for s in sents:
    for ch in split_chunk(s, maxc):
      words = [w for w in ch if letters(w[0]) or w[0] in ('—',)]
      text = ' '.join(w[0] for w in ch)
      out.append([ch[0][1], ch[-1][2] + .25, text])
  return out

def split_chunk(ws, maxc):
  text = ' '.join(w[0] for w in ws)
  if len(text) <= maxc: return [ws]
  best = None
  for k in range(1, len(ws)):
    a = ' '.join(w[0] for w in ws[:k]); b = ' '.join(w[0] for w in ws[k:])
    score = abs(len(a) - len(b)) - (40 if re.search(r'[,;:—]$', ws[k-1][0]) or ws[k][0] == '—' else 0)
    if best is None or score < best[0]: best = (score, k)
  k = best[1]
  return split_chunk(ws[:k], maxc) + split_chunk(ws[k:], maxc)

def srt(caps):
  def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
  out = []
  for k, (a, b, text) in enumerate(caps):
    if k + 1 < len(caps): b = min(b, caps[k + 1][0] - .04)
    b = max(b, a + .9)
    out.append(f'{k+1}\n{ts(a)} --> {ts(b)}\n{wrap(text)}\n')
  return '\n'.join(out)

def wrap(text, w=42):
  if len(text) <= w: return text
  best = None
  sp = [m.start() for m in re.finditer(' ', text)]
  for k in sp:
    sc = max(k, len(text) - k - 1)
    if best is None or sc < best[0]: best = (sc, k)
  return text[:best[1]] + '\n' + text[best[1] + 1:]

# ---------- drawing helpers ----------
def bg(): return f'<rect width="1600" height="900" fill="{INK}"/>'

def strip(x, y, w, h, fill, seed, text='', size=None, col=INK, rot=0, shadow=True, pad=40, mono=False, ls=0, rim='#fff'):
  o = f'<g transform="rotate({rot} {x+w/2:.1f} {y+h/2:.1f})">'
  if shadow: o += f'<g transform="translate(10 13)" opacity=".6">{paper(x, y, w, h, "#000", seed, amp=5)}</g>'
  o += paper(x, y, w, h, fill, seed, amp=5, rim=rim)
  if text:
    if mono:
      size = min(size or h * .5, (w - 2 * pad) / len(text) / .6 - ls / .6)
      o += T(x + pad, y + h / 2 + size * .36, text, size, col, M, 700, ls=ls)
    else:
      size = min(size or h * .78, (w - 2 * pad) * 100 / tw(text, 100))
      o += ttext(x + pad, y + h / 2 + size * .36, text, size, col, D)
  return o + '</g>'

def gl(x, y, s, size, col, ghosts=(LIME, RED), anchor='start'):
  """Glitch-ready text: two colour ghosts and five slices the script shifts sideways."""
  o = ''.join(f'<g class="gh" data-k="{k*2-1}">{ttext(x, y, s, size, c, D, anchor=anchor)}</g>' for k, c in enumerate(ghosts))
  top = y - size * .78; h = size * .82
  for k in range(5):
    cid = uid('cl'); y0 = top + h * k / 5
    o += (f'<clipPath id="{cid}"><rect x="-400" y="{y0:.1f}" width="2600" height="{h/5+.6:.1f}"/></clipPath>'
          f'<g clip-path="url(#{cid})"><g class="sl">{ttext(x, y, s, size, col, D, anchor=anchor)}</g></g>')
  return o

def clipped(body, x, y, w, h):
  """Body revealed left to right by a growing clip rect (type and wipe animations)."""
  cid = uid('rv')
  return f'<clipPath id="{cid}"><rect class="rv" x="{x:.1f}" y="{y:.1f}" width="0" height="{h:.1f}" data-w="{w:.1f}"/></clipPath><g clip-path="url(#{cid})">{body}</g>'

def stamp(cx, cy, text, rot=-6, fill=RED, col=WHITE, size=40, seed=70):
  w = mw(text, size, 6) + 60; h = size * 1.75
  return f'<g transform="rotate({rot} {cx} {cy})">{paper(cx-w/2, cy-h/2, w, h, fill, seed, amp=5, sides="rl")}{T(cx, cy+size*.36, text, size, col, M, 700, "middle", 6)}</g>'

def tally(x, y, n, h=54, col=INK, seed=0):
  o = ''
  for k in range(n):
    xx = x + k * 20; j = ((seed + k) * 37 % 7 - 3)
    o += f'<path d="M{xx} {y} L{xx + j * .8:.1f} {y - h}" stroke="{col}" stroke-width="7" stroke-linecap="round" filter="url(#rough)"/>'
  return o

def frame(x, y, w, h, col=LIME, sw=6):
  return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" filter="url(#rough)"/>'

def die_faces(cx, cy, s, final=4):
  pip = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
         5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
  o = f'<g transform="translate(14 18)" opacity=".6"><rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" rx="{s*.14}" fill="#000"/></g>'
  o += f'<rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" rx="{s*.14}" fill="{WHITE}" filter="url(#rough)"/>'
  for f in range(1, 7):
    dots = ''.join(f'<circle cx="{cx + dx * s * .27:.1f}" cy="{cy + dy * s * .27:.1f}" r="{s*.085:.1f}" fill="{RED if f == final else INK}"/>' for dx, dy in pip[f])
    o += f'<g class="cf" data-i="{f-1}">{dots}</g>'
  return o

def ghost(x, y, s, size, stroke='#34342F', sw=3, anchor='start'):
  return outline(x, y, s, size, set(), D, stroke=stroke, sw=sw, anchor=anchor)

def edge_ht(side='r', seed=3, w=260, step=14, col=LIME, n=36):
  if side == 'r':
    return halftone(1600 - w, -20, w + 20, 940, step, col, seed, base=.45, soft=.45) + streaks(1600 - w, -20, w + 20, 940, col, seed, base=.45, n=n, maxlen=.6)
  return halftone(-20, -20, w, 940, step, col, seed, base=.55, soft=.45, flip=True)
````
