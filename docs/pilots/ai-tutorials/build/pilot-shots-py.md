# tmp/pilot/shots.py

37 кадров пилота по раскадровке, текст — из script-en.md.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/shots.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""The 37 shots of docs/pilots/ai-tutorials/storyboard.md. Narration is script-en.md, split by shot."""
from engine import *

MSG = ['MOM IS AT THE STORE.', 'DAD IS AT THE GYM.', 'SAM IS AT THE PARK.']

def mono(x, y, s, size=26, col=WHITE, anchor='start', ls=3): return T(x, y, s, size, col, M, 700, anchor, ls)

def words_row(s, i, words, x, y, size, col, a='zoom', cue=0, step=.2, d=.25):
  """Big words placed left to right; returns end x and each word's (x, width)."""
  pos = {}
  for k, w in enumerate(words):
    ww = tw(w, size); pos[w] = (x, ww)
    at = cue if a == 'none' else (f'{cue}+{k * step:.2f}' if isinstance(cue, str) else cue + k * step)
    s.E(f'{i}{k}', ttext(x, y, w, size, col, D), x + ww / 2, y - size * .35, a, at=at, d=d)
    x += tw(w + ' ', size)
  return x, pos

def typed(s, i, lines, x, y, size, col, cues, lh, rot=(0, 800, 450)):
  """Mono lines typed one by one; cues = [(start, end), ...] per line."""
  for k, (ln, (a, b)) in enumerate(zip(lines, cues)):
    yy = y + k * lh
    body = clipped(mono(x, yy, ln, size, col, ls=0), x - 4, yy - size, mw(ln, size) + 12, size * 1.4)
    s.E(f'{i}{k}', f'<g transform="rotate({rot[0]} {rot[1]} {rot[2]})">{body}</g>', x + 300, yy, 'type', at=a, d=b)

def tag(x, y, text, fill=LIME, col=INK, size=22, rot=0, seed=5):
  w = mw(text, size, 3) + 30; h = size * 1.7
  return f'<g transform="rotate({rot} {x + w / 2:.1f} {y})">{paper(x, y - h / 2, w, h, fill, seed, amp=3, sides="rl")}{mono(x + 15, y + size * .36, text, size, col)}</g>'

def arrow(x0, y, x1, col=LIME, sw=8):
  return (f'<path d="M{x0} {y}H{x1 - 18}" stroke="{col}" stroke-width="{sw}" filter="url(#rough)"/>'
          f'<path d="M{x1 - 30} {y - 20}L{x1} {y}L{x1 - 30} {y + 20}" fill="none" stroke="{col}" stroke-width="{sw}"/>')

# ===== 0:00 Cold open =====
s = Shot(1, 'COLD OPEN', 'AI tools sometimes say things that are false — calmly, in perfect sentences.', tr='cut', hold=.6, lead=.2)
s.add(bg() + edge_ht('l', 11, 170))
S1 = round(1240 * 100 / tw('MOM IS AT THE GYM.', 100))
x, _ = words_row(s, 'w', ['MOM', 'IS', 'AT', 'THE'], 210, 500, S1, WHITE, cue=.15, step=.22)
s.E('gym', gl(x, 500, 'GYM.', S1, WHITE), x + 140, 430, 'zoom', at=1.05, d=.25, fx=dict(glitch=['w:false', 1]))
s.E('st', stamp(x + 170, 300, 'FALSE', -7, size=46), x + 170, 300, 'stamp', at='w:false+.15')
s.E('m', mono(214, 640, 'SAID CALMLY. IN A PERFECT SENTENCE.'), 600, 630, 'flick', at='w:calmly')

s = Shot(2, 'COLD OPEN', 'Many people call this "hallucination". It sounds mysterious. It isn\'t.', hold=.3)
s.add(bg() + edge_ht('r', 12, 200))
hs = round(1250 * 100 / tw('HALLUCINATION', 100, 'wide200'))
s.E('q', mono(110, 250, 'MANY PEOPLE CALL THIS:', 26, GRAY), 400, 240, 'fade', at='w:Many')
s.E('h', outline(110, 520, 'HALLUCINATION', hs, set(), D, sw=2.4), 800, 450, 'draw', at='w:hallucination', d=1.4)
s.E('m0', mono(110, 640, 'IT SOUNDS MYSTERIOUS.', 26, GRAY), 400, 630, 'fade', at='w:sounds')
s.E('bar', clipped(paper(90, 455, 1300, 56, LIME, 21, amp=6, sides='rl'), 80, 420, 1340, 130), 800, 480, 'wipe', at='w:isn\'t', d=.3)
s.E('m', mono(110, 700, 'NOT A MYSTERY', 40, LIME, ls=6), 400, 690, 'stamp', at='w:isn\'t+.3')

s = Shot(3, 'COLD OPEN', 'Today we build a tiny machine that makes the same kind of mistake. It fits on one sheet of paper. '
         'We\'ll count every step with a pencil, and you can check every number yourself. The files are in the description.', tr='tear')
s.add(bg())
s.E('t', ttext(110, 230, 'A TINY MACHINE', 150, WHITE, D), 500, 170, 'slideL', at='w:tiny')
s.E('t2', mono(116, 300, 'THAT MAKES THE SAME KIND OF MISTAKE', 26, LIME), 500, 290, 'flick', at='w:same')
for k, (w, cw) in enumerate([('ONE SHEET', 'w:sheet'), ('ONE PENCIL', 'w:pencil'), ('ONE DIE', 'w:check')]):
  cx = 330 + k * 470; rot = [-4, 3, -2][k]
  inner = ttext(0, 30, w, 92, INK, D, anchor='middle') + reg(-170, -80, 12, INK)
  s.E(f'c{k}', card(cx, 540, 420, 220, rot, inner, 30 + k), cx, 540, 'drop', at=cw)
s.E('f', mono(110, 810, 'FILES IN THE DESCRIPTION ↓', 28), 400, 800, 'flick', at='w:files')

s = Shot(4, 'COLD OPEN', 'One promise before we start: our machine is a toy. Real AI is far bigger, and I\'ll show you exactly where the toy stops matching it.')
s.add(bg() + edge_ht('r', 14, 260))
s.E('toy', f'<g transform="rotate(-5 570 360)">{paper(300, 250, 540, 230, LIME, 41, amp=8, rim="#fff")}{ttext(570, 435, "TOY", 230, INK, D, anchor="middle")}</g>'
    + tape(360, 220, 180, 54, -18, 42) + tape(720, 440, 170, 50, 14, 43), 570, 360, 'stamp', at='w:toy', d=.25)
s.E('g', ghost(60, 860, 'REAL AI', 380, stroke='#3A3A36'), 800, 700, 'draw', at='w:Real', d=1.4)
s.E('b', mono(310, 600, 'REAL AI: FAR BIGGER', 34, WHITE, ls=4), 600, 590, 'fade', at='w:bigger')
s.E('b2', mono(310, 650, 'WE SHOW WHERE THE TOY STOPS MATCHING', 26, LIME), 600, 640, 'fade', at='w:stops')

# ===== 0:40 The toy =====
def chat_strips(s, anim):
  for j, m in enumerate(MSG):
    cy = 300 + j * 190; rot = [-2.2, 1.6, -1.2][j]; x = 190 + j * 40; fill = LIME if j == 1 else WHITE
    body = (f'<g transform="rotate({rot} 800 {cy})"><g transform="translate(12 16)" opacity=".6">{paper(x, cy-75, 1160, 150, "#000", j+20, amp=6)}</g>'
            f'{paper(x, cy-75, 1160, 150, fill, j+20, amp=6, rim="#fff")}{ttext(x + 50, cy + 44, m, min(124, 920 * 100 / tw(m, 100)), INK, D)}'
            f'{mono(x + 1110, cy + 14, "TRUE", 28, INK, "end")}</g>')
    cue = ['w:Mom', 'w:Dad', 'w:Sam'][j] if anim else 0
    s.E(f'st{j}', body, 800, cy, 'slideL' if anim else 'none', at=cue)
    s.E(f'tp{j}', tape(x - 40, cy - 95, 150, 46, -14 + j * 8, j + 30), x + 35, cy - 72, 'pop' if anim else 'none', at=(cue + '+.45') if anim else 0, d=.15)

s = Shot(5, 'THE TOY', 'Picture a family group chat. Three messages came in today.\nMom is at the store.\nDad is at the gym.\nSam is at the park.', tr='tear')
s.add(bg())
s.E('h', mono(190, 130, 'FAMILY GROUP CHAT · TODAY · 3 MESSAGES', 26, LIME, ls=4), 500, 120, 'flick', at='w:family')
chat_strips(s, True)

s = Shot(6, 'THE TOY', 'That\'s everything our toy will ever read. Three sentences. All three are true.', tr='cut', hold=.4)
s.add(bg())
s.E('o', ghost(60, 800, '3/3', 820, stroke='#3A3A36'), 800, 450, 'draw', at=0, d=2.2)
s.add(mono(190, 130, 'FAMILY GROUP CHAT · TODAY · 3 MESSAGES', 26, LIME, ls=4))
chat_strips(s, False)
s.E('v', vtext(80, 110, 'TRAINING DATA — EVERYTHING IT EVER READ', 22, LIME, M, 90, ls=4), 90, 450, 'rise', at='w:everything')
s.E('c', mono(1530, 860, '3 / 3 TRUE', 30, LIME, 'end'), 1450, 850, 'flick', at='w:true')

s = Shot(7, 'THE TOY', 'The toy works a bit like the word suggestions on your phone keyboard. It has one rule. It looks at the last word it wrote, and nothing else. '
         'Then it picks a word that came right after that word somewhere in the chat.')
s.add(bg() + edge_ht('r', 17, 200))
s.E('bar', strip(150, 230, 1150, 150, WHITE, 51, rot=-1), 725, 305, 'slideL', at='w:suggestions')
x, pos = words_row(s, 'w', ['MOM', 'IS', 'AT', 'THE'], 200, 345, 110, INK, a='fade', cue='w:suggestions+.3', step=.12, d=.2)
s.E('cur', f'<rect x="{x - 10:.1f}" y="262" width="10" height="96" fill="{INK}"/>', x, 300, 'flick', at='w:phone', d=30)
for k, w in enumerate(['store', 'gym', 'park']):
  bx = 200 + k * 360
  s.E(f'k{k}', f'<rect x="{bx}" y="430" width="330" height="96" fill="#26261F"/><rect x="{bx}" y="430" width="330" height="4" fill="{LIME}"/>'
      + mono(bx + 165, 492, w, 40, WHITE, 'middle', 0), bx + 165, 478, 'rise', at=f'w:keyboard+{k * .12:.2f}', d=.35)
s.E('rule', ttext(150, 720, 'ONE RULE:', 120, LIME, D), 400, 670, 'slideL', at='w:rule')
thx, thw = pos['THE']
s.E('fr', frame(thx - 18, 240, thw + 36, 130), thx + thw / 2, 305, 'pop', at='w:last')
s.E('ro', mono(thx - 18, 225, 'READS ONLY THIS', 24, LIME, ls=4), thx + 100, 215, 'flick', at='w:nothing')
s.E('r2', mono(156, 790, 'LOOK AT THE LAST WORD. PICK A WORD THAT CAME NEXT.', 26, WHITE, ls=2), 700, 780, 'fade', at='w:picks')

# ===== 1:20 Counting by hand: one table on a torn sheet, shots 8–12 =====
TAB_X, TAB_Y, ROW = 150, 175, 80
ROWS = [('MOM', 'IS', 1), ('DAD', 'IS', 1), ('SAM', 'IS', 1), ('IS', 'AT', 3), ('AT', 'THE', 3), ('THE', 'STORE', 1), ('THE', 'GYM', 1), ('THE', 'PARK', 1)]
TROT = '<g transform="rotate(-1.2 630 470)">'

def table_sheet(s, a='none', at=0):
  body = (f'<g transform="translate(14 18)" opacity=".6">{paper(TAB_X - 50, 70, 1000, 800, "#000", 61, amp=6)}</g>'
          + paper(TAB_X - 50, 70, 1000, 800, WHITE, 61, amp=6, rim='#fff') + ttext(TAB_X, 140, 'WORD → NEXT WORD · COUNT', 64, INK, D)
          + f'<path d="M{TAB_X} 165H{TAB_X + 900}" stroke="{INK}" stroke-width="4"/>')
  s.E('sheet', TROT + body + '</g>', 630, 470, a, at=at)

def row(s, k, anim=False, at=0, tal_at=()):
  a, b, n = ROWS[k]; y = TAB_Y + 70 + k * ROW
  body = ttext(TAB_X, y, a, 64, INK, D) + mono(TAB_X + 230, y - 6, '→', 50, INK, ls=0) + ttext(TAB_X + 320, y, b, 64, INK, D)
  if anim: body = clipped(body, TAB_X - 10, y - 70, 640, 90)
  s.E(f'r{k}', TROT + body + '</g>', 400, y - 25, 'wipe' if anim else 'none', at=at, d=.35)
  for q in range(n):
    tb = TROT + tally(TAB_X + 760 + q * 26, y + 4, 1, 58, INK, k * 3 + q) + '</g>'
    s.E(f't{k}_{q}', tb, TAB_X + 770 + q * 26, y - 25, 'pop' if anim else 'none', at=(tal_at[q] if anim else 0), d=.12)

SX, SW = 1170, 310

def side(s, i, y, text, col=WHITE, a='flick', at=0, size=26):
  size = min(size, (SW / len(text) - 3) / .6)
  s.E(i, mono(SX, y, text, size, col), SX + SW / 2, y - 10, a, at=at)

def side_big(s, i, y, text, col=WHITE, a='slideR', at=0, size=104):
  size = min(size, SW * 100 / tw(text, 100))
  s.E(i, ttext(SX, y, text, size, col, D), SX + SW / 2, y - 40, a, at=at)

s = Shot(8, 'COUNTING BY HAND', 'To do that, it needs a table. For every word, we write down which words came next, and how often. Let\'s make that table by hand.')
s.add(bg() + edge_ht('r', 18, 110))
table_sheet(s, 'drop', 'w:table')
side(s, 'm1', 300, 'FOR EACH WORD:', LIME, at='w:every')
side(s, 'm2', 345, 'WHAT CAME NEXT', at='w:next')
side(s, 'm3', 390, 'HOW OFTEN', at='w:often')
side_big(s, 'm4', 540, 'BY HAND.', LIME, a='stamp', at='w:hand', size=110)

s = Shot(9, 'COUNTING BY HAND', 'After "Mom" comes "is". Once. After "Dad": "is". After "Sam": "is". So after a name, the next word is always "is".', tr='cut')
s.add(bg() + edge_ht('r', 18, 110)); table_sheet(s)
for k, w in enumerate(['Mom', 'Dad', 'Sam']):
  row(s, k, True, f'w:{w}', ['w:is+.1'])
side(s, 'n', 330, 'AFTER A NAME →', LIME, at='w:name')
side_big(s, 'n2', 470, 'ALWAYS "IS"', at='w:always')

s = Shot(10, 'COUNTING BY HAND', 'After "is" comes "at" — three times out of three. After "at": "the", three out of three.', tr='cut')
s.add(bg() + edge_ht('r', 18, 110)); table_sheet(s)
for k in range(3): row(s, k)
row(s, 3, True, 'w:After', ['w:three', 'w:times', 'w:out'])
row(s, 4, True, 'w:After', ['w:three', 'w:out', 'w:of'])
s.E('n', outline(SX, 520, '3/3', 175, {0}, D, sw=2.4), SX + 150, 450, 'draw', at=1.0, d=1.2)

s = Shot(11, 'COUNTING BY HAND', 'Now the interesting one. After "the", the chat has "store" once, "gym" once, "park" once. Three different words, one tally each.', tr='cut')
s.add(bg() + edge_ht('r', 18, 110)); table_sheet(s)
for k in range(5): row(s, k)
for k, w in enumerate(['store', 'gym', 'park']):
  row(s, 5 + k, True, f'w:{w}', ['w:once'])
y0 = TAB_Y + 70 + 5 * ROW - 75
s.E('fr', TROT + frame(TAB_X - 25, y0, 940, 3 * ROW + 25) + '</g>', 600, y0 + 120, 'pop', at='w:Three')
side(s, 'n', 300, 'THREE DIFFERENT', LIME, at='w:different')
side(s, 'n1', 340, 'WORDS', LIME, at='w:words')
side_big(s, 'n2', 470, 'ONE EACH', at='w:tally')

s = Shot(12, 'COUNTING BY HAND', 'That\'s the whole table. Eight rows. You can check it against the three messages in under a minute.', tr='cut', hold=.5)
s.add(bg() + edge_ht('r', 18, 110)); table_sheet(s)
for k in range(8): row(s, k)
s.E('n', outline(SX + 40, 560, '8', 420, {0}, D, sw=3), SX + 190, 400, 'zoom', at='w:Eight')
side_big(s, 'n2', 690, 'ROWS', at='w:rows', size=120)
side(s, 'n3', 750, 'CHECK IT:', LIME, at='w:minute', size=24)
side(s, 'n4', 785, 'UNDER A MINUTE', LIME, at='w:minute', size=24)

# ===== 2:14 the die =====
s = Shot(13, 'COUNTING BY HAND', 'Now let\'s ask the toy to finish a sentence: "Mom is at the…" The toy looks only at the last word: "the". It doesn\'t see "Mom".')
s.add(bg())
s.E('ht', halftone(700, 380, 920, 560, 16, LIME, 5, base=.62, soft=.3) + streaks(700, 380, 920, 560, LIME, 5, base=.62, n=30), 1200, 650, 'slideR', at=0, d=.8)
s.E('ask', mono(90, 140, 'FINISH THE SENTENCE:', 26, LIME, ls=4), 300, 130, 'flick', at='w:finish')
x, pos = words_row(s, 'w', ['MOM', 'IS', 'AT', 'THE'], 90, 330, 180, WHITE, cue='w:Mom')
s.E('q', marker(x, 200, 260, 160, -3, 8, WHITE) + ttext(x + 130, 332, '?', 170, INK, D, anchor='middle'), x + 130, 280, 'pop', at='w:the+.3')
tx, tww = pos['THE']
s.E('fr', frame(tx - 20, 170, tww + 40, 200), tx + tww / 2, 270, 'pop', at='w:last')
s.E('ro', mono(tx - 20, 155, 'READS ONLY THIS', 24, LIME, ls=4), tx + 80, 145, 'flick', at='w:the')
mx, mww = pos['MOM']
s.E('x', clipped(f'<path d="M{mx - 10} 270 L{mx + mww + 10} 262" stroke="{RED}" stroke-width="14" filter="url(#rough)"/>', mx - 20, 240, mww + 40, 60), mx + mww / 2, 266, 'wipe', at='w:see', d=.25)
s.E('ns', mono(mx, 420, 'NOT SEEN', 24, RED, ls=4), mx + 60, 410, 'flick', at='w:see+.2')

s = Shot(14, 'COUNTING BY HAND', 'In its table, "the" was followed by store, gym and park, once each. So each has the same chance: one in three. '
         'Let\'s roll a die. One or two: store. Three or four: gym. Five or six: park.\nWe rolled a four.', hold=1.0)
s.add(bg() + edge_ht('r', 19, 100) + ttext(80, 150, 'MOM IS AT THE ?', 96, WHITE, D))
LIFT = ['w:four#2+.3', .5, 0, -60, .08]
for j, w in enumerate(['STORE', 'GYM', 'PARK']):
  ccx = 260 + j * 380; rot = [-6, 3, -2][j]
  inner = ttext(0, -50, w, 120, INK, D, anchor='middle') + f'<path d="M-130 0H130" stroke="{INK}" stroke-width="4"/>'
  inner += reg(-125, -160, 12, INK) + reg(125, -160, 12, INK)
  s.E(f'cd{j}', card(ccx, 520, 330, 400, rot, inner, j + 40), ccx, 520, 'drop', at=f'w:{w.lower()}',
      mv=LIFT if j == 1 else None, fx=dict(shake=['w:four#2+.3', 'e0', 4]) if j == 1 else None)
for j in range(3):
  ccx = 260 + j * 380; rot = [-6, 3, -2][j]
  s.E(f'o{j}', f'<g transform="translate({ccx} 520) rotate({rot})">{outline(0, 150, "1/3", 150, {0}, D, stroke=INK, sw=3, lime=RED if j == 1 else INK, anchor="middle")}</g>',
      ccx, 620, 'draw', at=f'w:one+{j * .15:.2f}', d=1.0, mv=LIFT if j == 1 else None, fx=dict(shake=['w:four#2+.3', 'e0', 4]) if j == 1 else None)
s.E('dice', die_faces(1350, 470, 190), 1350, 470, 'drop', at='w:roll', fx=dict(cycle=['w:roll+.3', 'w:four#2', 3], shake=['w:roll+.3', 'w:four#2', 14]))
s.E('map', mono(1350, 640, '1–2 STORE', 26, WHITE, 'middle', 2) + mono(1350, 680, '3–4 GYM', 26, LIME, 'middle', 2) + mono(1350, 720, '5–6 PARK', 26, WHITE, 'middle', 2),
    1350, 680, 'fade', at='w:One')
s.E('four', tag(1250, 320, 'ROLLED: 4', RED, WHITE, 28, -4), 1350, 320, 'stamp', at='w:four#2')

s = Shot(15, 'COUNTING BY HAND', 'The toy writes: "Mom is at the gym."\nThat\'s false. Mom is at the store.')
fs = min(150, 500 * 100 / tw('MOM IS AT', 100))
s.add(bg())
s.E('lp', paper(-40, -40, 860, 980, LIME, 61, amp=14, sides='r', rim='#fff') + halftone(790, -20, 200, 940, 12, LIME, 61, base=.0, soft=.9, flip=True), 400, 450, 'slideL', at=0, d=.45)
s.E('big', ttext(30, 600, '2/3', 620, INK, D, ls=-10), 330, 400, 'zoom', at=.45)
s.E('m', ttext(1000, 210, 'MOM IS AT', fs, WHITE, D), 1200, 160, 'slideR', at='w:Mom')
s.E('g', gl(1000, 210 + fs * .95, 'THE GYM.', fs, WHITE), 1200, 300, 'slideR', at='w:gym', fx=dict(glitch=['w:gym', 1]))
s.E('ft', stamp(1420, 420, 'FALSE', -6, size=40), 1420, 420, 'stamp', at='w:false')
s.E('fix', strip(1000, 560, 520, 110, WHITE, 77, text='MOM IS AT THE STORE.', size=64, rot=2, pad=30)
    + mono(1000, 720, 'WHAT IS TRUE', 22, LIME, ls=4), 1260, 615, 'slideR', at='w:Mom')
s.E('sub', ttext(50, 730, 'OF ITS SENTENCES', 84, INK, D) + ttext(50, 820, 'ARE FALSE', 84, INK, D), 330, 760, 'rise', at='w:store')

s = Shot(16, 'COUNTING BY HAND', 'But look at what happened. Every pair of words in that sentence — "Mom is", "is at", "at the", "the gym" — appeared in a true message. '
         'The toy never saw a false sentence. It built one anyway, out of true pieces.')
s.add(bg() + edge_ht('r', 23, 130))
words_row(s, 'w', ['MOM', 'IS', 'AT', 'THE', 'GYM.'], 200, 210, 140, WHITE, a='zoom', cue='w:look', step=.1)
PAIRS = [('MOM IS', 'w:Mom'), ('IS AT', 'w:is#2'), ('AT THE', 'w:at#2'), ('THE GYM', 'w:the#2')]
for k, (pr, cue) in enumerate(PAIRS):
  px = 200 + (k % 2) * 620; py = 290 + (k // 2) * 190; rot = [-2, 1.5, 1, -1.5][k]
  s.E(f'p{k}', strip(px, py, 520, 120, WHITE, 90 + k, text=pr, size=88, rot=rot), px + 260, py + 60, 'drop', at=cue)
for k in range(4):
  px = 200 + (k % 2) * 620; py = 290 + (k // 2) * 190
  s.E(f'tg{k}', tag(px + 20, py + 150, 'SEEN IN TRUE TEXT', LIME, INK, 20, 0, 95 + k), px + 160, py + 150, 'flick', at=f'w:appeared+{k * .15:.2f}')
s.E('nv', mono(200, 720, 'IT NEVER SAW A FALSE SENTENCE.', 30, WHITE), 600, 710, 'fade', at='w:never')
s.E('tp', ttext(200, 840, 'BUILT FROM TRUE PIECES', 100, LIME, D), 600, 810, 'slideL', at='w:true')

s = Shot(17, 'COUNTING BY HAND', 'How often? Starting from "Mom", the toy can write three sentences. One is true, two are false. Same for Dad, same for Sam. '
         'Nine possible sentences, three true, six false. The chance of a false answer is two in three. That\'s the whole calculation. Pencil, eight rows, one die.')
s.add(bg())
s.E('hd', mono(90, 110, 'EVERY SENTENCE THE TOY CAN WRITE', 24, LIME, ls=4), 400, 100, 'flick', at='w:Starting')
NAMES = ['MOM', 'DAD', 'SAM']; PLACES = ['STORE', 'GYM', 'PARK']; RC = ['w:three', 'w:Dad', 'w:Sam']
for r in range(3):
  for c in range(3):
    ok = r == c; x0 = 90 + c * 300; y0 = 150 + r * 200; rr = ((r * 3 + c) * 37 % 7 - 3) * .7
    cell = (f'<g transform="rotate({rr:.1f} {x0 + 140} {y0 + 85})">{paper(x0, y0, 280, 170, WHITE if ok else RED, 120 + r * 3 + c, amp=3)}'
            f'{ttext(x0 + 140, y0 + 80, f"{NAMES[r]} · {PLACES[c]}", 50, INK if ok else WHITE, D, anchor="middle")}'
            f'{mono(x0 + 140, y0 + 135, "TRUE" if ok else "FALSE", 28, INK if ok else WHITE, "middle", 4)}</g>')
    s.E(f'c{r}{c}', cell, x0 + 140, y0 + 85, 'stamp', at=f'{RC[r]}+{c * .18:.2f}')
s.E('n9', ttext(1040, 260, '9 SENTENCES', 100, WHITE, D), 1250, 220, 'slideR', at='w:Nine')
s.E('n3', mono(1044, 320, '3 TRUE · 6 FALSE', 30, WHITE), 1200, 310, 'flick', at='w:six')
s.E('o', outline(1030, 640, '2/3', 300, {0}, D, sw=3, lime=RED), 1250, 540, 'draw', at='w:chance', d=1.0)
s.E('fl', mono(1044, 710, 'FALSE: 2 IN 3', 34, RED, ls=4), 1200, 700, 'stamp', at='w:two')
s.E('pc', tag(1040, 800, 'PENCIL · 8 ROWS · 1 DIE', LIME, INK, 26, -2), 1250, 800, 'pop', at='w:Pencil')

# ===== 3:15 Shannon 1948 =====
s = Shot(18, 'SHANNON, 1948', 'This idea is old. In 1948, Claude Shannon published "A Mathematical Theory of Communication".', tr='tear', hold=.4)
s.add(bg() + edge_ht('r', 31, 220))
s.E('old', ttext(90, 200, 'THIS IDEA IS OLD.', 120, WHITE, D), 400, 160, 'slideL', at='w:old')
s.E('g', ghost(40, 860, '1948', 640, stroke='#3A3A36'), 800, 600, 'draw', at='w:1948', d=1.8)
inner = (mono(-330, -110, '1948', 30, INK) + mono(-330, -60, 'C. E. SHANNON', 34, INK) + ttext(-330, 30, 'A MATHEMATICAL THEORY', 64, INK, D)
         + ttext(-330, 100, 'OF COMMUNICATION', 64, INK, D) + mono(-330, 165, 'SECTION 3', 26, INK) + reg(320, -130, 14, INK))
s.E('card', card(800, 540, 740, 400, -3, inner, 140), 800, 540, 'drop', at='w:Shannon')

s = Shot(19, 'SHANNON, 1948', 'In section three, he built English one word at a time from word pairs — with no computer. He opened a book, found a word, '
         'and wrote down the word that followed it. Then he looked for that new word somewhere else in the book, and repeated.')
s.add(bg())
s.E('hd', mono(90, 140, 'SECTION 3 · ENGLISH FROM WORD PAIRS', 26, LIME, ls=4), 400, 130, 'flick', at='w:section')
s.E('nc', stamp(1300, 160, 'NO COMPUTER', 4, fill=WHITE, col=INK, size=34), 1300, 160, 'stamp', at='w:computer')
s.E('pn', mono(90, 830, 'A PERSON, A BOOK, A PENCIL', 24, GRAY), 400, 820, 'fade', at='w:opened')
STEPS = [('BOOK', 'w:book'), ('A WORD', 'w:found'), ('NEXT WORD', 'w:followed'), ('ELSEWHERE', 'w:else')]
for k, (w, cue) in enumerate(STEPS):
  bx = 80 + k * 380; rot = [-3, 2, -1.5, 2.5][k]
  body = strip(bx, 380, 300, 150, WHITE if k != 2 else LIME, 150 + k, text=w, size=74, rot=rot, pad=30)
  if k: body = arrow(bx - 70, 455, bx - 8) + body
  s.E(f's{k}', body, bx + 150, 455, 'drop', at=cue)
loop = f'<path d="M1310 560 C1310 720 760 720 610 575" fill="none" stroke="{LIME}" stroke-width="8" filter="url(#rough)"/><path d="M600 620 L608 572 L655 590" fill="none" stroke="{LIME}" stroke-width="8"/>'
s.E('lp', loop + mono(960, 740, 'REPEAT', 30, LIME, 'middle', 6), 960, 650, 'draw', at='w:repeated', d=.9)

QUOTE = ['"THE HEAD AND IN FRONTAL ATTACK ON AN', 'ENGLISH WRITER THAT THE CHARACTER OF', 'THIS POINT IS THEREFORE ANOTHER METHOD…"']
s = Shot(20, 'SHANNON, 1948', 'Here is part of what he got, exactly as printed: "THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD…"', hold=.8)
s.add(bg() + edge_ht('l', 33, 120))
s.E('sh', strip(170, 240, 1300, 330, WHITE, 160, rot=-1.5), 820, 405, 'slideL', at='w:exactly')
s.E('lb', mono(200, 180, 'HIS RESULT, AS PRINTED', 26, LIME, ls=4), 400, 170, 'flick', at='w:printed')
s.E('src', mono(200, 650, 'C. E. SHANNON, 1948 · SECTION 3', 24, GRAY), 400, 640, 'fade', at='w:printed+.4')
typed(s, 'q', QUOTE, 230, 330, 40, INK, [('w:THE', 'w:ENGLISH'), ('w:ENGLISH', 'w:THIS'), ('w:THIS', 'w:METHOD+.6')], 85, (-1.5, 820, 405))

s = Shot(21, 'SHANNON, 1948', 'Every pair of words is real English. The whole thing means nothing. Our toy is a small version of Shannon\'s machine.', tr='cut')
s.add(bg() + edge_ht('l', 33, 120) + strip(170, 240, 1300, 330, WHITE, 160, rot=-1.5)
      + '<g transform="rotate(-1.5 820 405)">' + ''.join(mono(230, 330 + k * 85, ln, 40, INK, ls=0) for k, ln in enumerate(QUOTE)) + '</g>'
      + mono(200, 180, 'HIS RESULT, AS PRINTED', 26, LIME, ls=4))
s.E('rp', mono(200, 650, 'EVERY PAIR IS REAL ENGLISH', 30, WHITE, ls=4), 500, 640, 'flick', at='w:real')
s.E('ns', stamp(1220, 250, 'NONSENSE', -8, size=56), 1220, 250, 'stamp', at='w:nothing')
s.E('ty', tag(200, 760, 'OUR TOY = A SMALL SHANNON MACHINE', LIME, INK, 30, -1.5), 600, 760, 'slideL', at='w:small')

# ===== 4:10 real models =====
s = Shot(22, 'REAL MODELS', 'So is a chatbot just Shannon\'s table, only bigger? No. Here the toy stops matching.\n'
         'First, real models don\'t look at one word. They read the whole question. If our toy read all of "Mom is at the", it would have seen that exact phrase once — followed by "store". This error would disappear.', tr='tear')
s.add(bg() + edge_ht('r', 41, 180))
s.E('q', ttext(800, 400, 'JUST A BIGGER TABLE?', 150, WHITE, D, anchor='middle'), 800, 350, 'zoom', at='w:chatbot', o=['w:First', 'fade'])
s.E('no', stamp(1180, 470, 'NO.', -8, size=70), 1180, 470, 'stamp', at='w:No', o=['w:First', 'fade'])
s.E('hr', mono(800, 580, 'HERE THE TOY STOPS MATCHING', 30, LIME, 'middle', 4), 800, 570, 'flick', at='w:Here', o=['w:First', 'fade'])
s.E('a', strip(100, 110, 760, 120, WHITE, 170, text='TOY READS 1 WORD', size=84, rot=-1.5), 480, 170, 'slideL', at='w:First+.3')
s.E('b', strip(480, 260, 920, 120, LIME, 171, text='REAL MODELS READ THE WHOLE QUESTION', size=72, rot=1), 940, 320, 'slideR', at='w:whole')
SZ = 150; sx = 120
_, pos = words_row(s, 'm', ['MOM', 'IS', 'AT', 'THE'], sx, 640, SZ, WHITE, a='fade', cue='w:If', step=.08, d=.2)
gx = sx + tw('MOM IS AT THE ', SZ)
s.E('gym', gl(gx, 640, 'GYM.', SZ, WHITE), gx + 120, 590, 'fade', at='w:If', o=['w:store', 'glitch'], fx=dict(glitch=['w:If+.2', .6]))
tx, tww = pos['THE']
s.E('f1', frame(tx - 18, 510, tww + 36, 170), tx + tww / 2, 595, 'pop', at='w:If+.3', o=['w:all', 'fade'])
s.E('f2', frame(sx - 22, 505, gx - sx + 10, 180), (sx + gx) / 2, 595, 'pop', at='w:all')
s.E('sn', mono(sx, 760, 'SEEN ONCE: "MOM IS AT THE" → "STORE"', 26, WHITE), 600, 750, 'fade', at='w:exact')
s.E('st', ttext(gx, 640, 'STORE.', SZ, LIME, D), gx + 160, 590, 'pop', at='w:store+.3')
s.E('eg', tag(sx, 830, 'THIS ERROR DISAPPEARS', LIME, INK, 26, -1), 400, 830, 'flick', at='w:disappear')

s = Shot(23, 'REAL MODELS', 'Second, real models don\'t store a table of counts. They are neural networks trained on huge amounts of text to predict the next piece of text. '
         'That\'s how models like GPT are described in their own papers. What they learn is far richer than our table.\nSo why do they still make things up?', hold=.6)
s.add(bg() + edge_ht('r', 43, 200))
mini = ''.join(ttext(-170, -60 + k * 60, f'{a} → {b}', 46, INK, D) + tally(110, -60 + k * 60, n, 40, INK, k) for k, (a, b, n) in enumerate(ROWS[3:6]))
cross = f'<path d="M-200 -130L200 140M200 -130L-200 140" stroke="{RED}" stroke-width="14" filter="url(#rough)"/>'
OUT = ['w:So', 'fade']
s.E('mt', card(300, 330, 440, 300, -4, mini, 180), 300, 330, 'drop', at='w:Second', o=OUT)
s.E('x', f'<g transform="translate(300 330) rotate(-4)">{cross}</g>', 300, 330, 'stamp', at='w:counts', o=OUT)
s.E('nt', mono(90, 560, 'NOT A TABLE OF COUNTS', 30, WHITE, ls=4), 300, 550, 'flick', at='w:counts+.2', o=OUT)
s.E('nn', ttext(640, 300, 'A NEURAL NETWORK', 130, LIME, D), 1000, 250, 'slideR', at='w:neural', o=OUT)
s.E('tr', clipped(mono(646, 370, 'TRAINED TO PREDICT THE NEXT PIECE OF TEXT', 28, WHITE), 640, 340, 900, 45), 1000, 360, 'type', at='w:predict', d=1.4, o=OUT)
s.E('src', mono(646, 440, 'BROWN ET AL., 2020 · GPT-3 PAPER', 22, GRAY), 900, 430, 'fade', at='w:GPT', o=OUT)
s.E('rc', tag(640, 640, 'FAR RICHER THAN OUR TABLE', WHITE, INK, 30, 1.5), 900, 640, 'slideR', at='w:richer', o=OUT)
s.E('why', ttext(800, 420, 'SO WHY DO THEY STILL', 130, WHITE, D, anchor='middle') + ttext(800, 560, 'MAKE THINGS UP?', 130, LIME, D, anchor='middle'), 800, 450, 'zoom', at='w:why')

s = Shot(24, 'WHY MODELS GUESS', 'In 2025, researchers at OpenAI and Georgia Tech published a paper called "Why Language Models Hallucinate". It gives two reasons. Both can be shown with our toy.', tr='tear')
s.add(bg() + edge_ht('l', 45, 140))
s.E('g', ghost(300, 860, '2025', 600, stroke='#3A3A36'), 800, 600, 'draw', at='w:2025', d=1.8)
inner = (mono(-380, -120, '2025 · OPENAI + GEORGIA TECH', 26, INK) + mono(-380, -75, 'KALAI, NACHUM, VEMPALA, ZHANG', 26, INK)
         + ttext(-380, 20, 'WHY LANGUAGE MODELS', 80, INK, D) + ttext(-380, 100, 'HALLUCINATE', 80, INK, D) + mono(-380, 160, 'ARXIV:2509.04664', 26, INK))
s.E('card', card(720, 360, 840, 400, 2.5, inner, 190), 720, 360, 'drop', at='w:researchers')
s.E('r1', strip(260, 650, 470, 110, LIME, 191, text='1. RARE FACTS', size=80, rot=-2), 495, 705, 'slideL', at='w:two')
s.E('r2', strip(800, 670, 420, 110, WHITE, 192, text='2. GRADING', size=80, rot=1.5), 1010, 725, 'slideR', at='w:two+.3')
s.E('bt', mono(260, 840, 'BOTH SHOWN WITH OUR TOY', 26, WHITE), 500, 830, 'flick', at='w:Both')

BQ = ['"if 20% of birthday facts appear exactly', 'once in the pretraining data, then one', 'expects base models to hallucinate on', 'at least 20% of birthday facts."']
s = Shot(25, 'WHY MODELS GUESS', 'Reason one: rare facts. If a fact appears only once in the training text, a model has very little to go on. '
         'The paper gives an example: "if 20% of birthday facts appear exactly once in the pretraining data, then one expects base models to hallucinate on at least 20% of birthday facts."', hold=.8)
s.add(bg())
s.E('h', strip(80, 60, 520, 110, LIME, 200, text='1. RARE FACTS', size=84, rot=-1.5), 340, 115, 'slideL', at=0)
s.E('once', mono(660, 130, 'SEEN ONCE = LITTLE TO GO ON', 28, WHITE, ls=4), 900, 120, 'flick', at='w:little')
s.E('sh', strip(130, 250, 1080, 400, WHITE, 201, rot=1), 670, 450, 'slideR', at='w:example')
s.E('src', mono(150, 720, 'KALAI ET AL., 2025', 22, GRAY), 400, 710, 'fade', at='w:example+.3')
s.E('g', outline(1230, 850, '20%', 300, {0, 1}, D, sw=3), 1400, 750, 'draw', at='w:if', d=1.2)
typed(s, 'q', BQ, 180, 350, 38, INK, [('w:if', 'w:once'), ('w:once', 'w:expects'), ('w:expects', 'w:at'), ('w:at', 'w:facts+.4')], 85, (1, 670, 450))

s = Shot(26, 'WHY MODELS GUESS', 'Our toy shows the extreme version. Ask it where Grandma is. Grandma never wrote in the chat. A table can stay silent. '
         'But a model built to always produce the next word will produce one.')
s.add(bg() + edge_ht('r', 47, 160))
GS = 128
s.E('ex', mono(90, 120, 'THE EXTREME VERSION', 26, LIME, ls=4), 300, 110, 'flick', at='w:extreme')
s.E('s', ttext(90, 300, 'GRANDMA IS AT THE', GS, WHITE, D), 500, 250, 'slideL', at='w:Grandma')
bx = 90 + tw('GRANDMA IS AT THE ', GS)
s.E('bl', clipped(f'<rect x="{bx:.1f}" y="290" width="300" height="12" fill="{WHITE}"/>', bx - 5, 280, 310, 30), bx + 150, 296, 'wipe', at='w:Grandma+.5')
tab = (ttext(-290, -110, 'WORD → NEXT WORD', 52, INK, D) + f'<path d="M-290 -90H290" stroke="{INK}" stroke-width="3"/>'
       + ''.join(ttext(-290, -30 + k * 60, f'{a} → {b}', 46, INK, D) for k, (a, b, n) in enumerate(ROWS[:3]))
       + f'<rect x="-295" y="125" width="590" height="70" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="14 10"/>'
       + ttext(-280, 178, 'GRANDMA → ?', 50, RED, D))
s.E('tb', card(420, 610, 660, 440, -2, tab, 210), 420, 610, 'drop', at='w:never')
s.E('nr', mono(820, 520, 'NO ROW FOR GRANDMA', 26, WHITE, ls=4), 1000, 510, 'flick', at='w:chat')
s.E('sl', tag(820, 600, 'A TABLE CAN STAY SILENT', WHITE, INK, 28, -1), 1050, 600, 'slideR', at='w:silent')
slot = ''.join(f'<g class="cf" data-i="{k}">{ttext(bx, 285, w, GS, LIME, D)}</g>' for k, w in enumerate(['STORE', 'GYM', 'PARK']))
s.E('slot', slot, bx + 150, 240, 'pop', at='w:always', fx=dict(cycle=['w:always', 'e0', 1]))
s.E('al', mono(820, 700, 'A MODEL ALWAYS PRODUCES A WORD', 26, LIME, ls=2), 1050, 690, 'flick', at='w:produce#2')

EXAM = [('MOM', 'STORE · GYM · PARK'), ('DAD', 'STORE · GYM · PARK'), ('SAM', 'STORE · GYM · PARK'),
        ('GRANDMA', 'LIBRARY · POOL · BAKERY'), ('LEO', 'SCHOOL · BEACH · MALL'), ('NINA', 'OFFICE · CLINIC · CAFE')]
s = Shot(27, 'WHY MODELS GUESS', 'Reason two: the way models are graded. Let\'s give our toy an exam. This time it reads the whole question. Six questions, three answer options each. '
         'Three questions are about Mom, Dad and Sam — the toy knows those. Three are about Grandma, Leo and Nina — it has never seen them.', tr='tear')
s.add(bg() + edge_ht('r', 51, 120))
s.E('h', strip(990, 60, 420, 110, WHITE, 230, text='2. GRADING', size=84, rot=1.5), 1200, 115, 'slideR', at=0)
s.E('sheet', '<g transform="translate(14 18)" opacity=".6">' + paper(70, 150, 900, 720, '#000', 220, amp=5) + '</g>' + paper(70, 150, 900, 720, WHITE, 220, amp=5, rim='#fff')
    + ttext(110, 230, 'EXAM · 6 QUESTIONS', 64, INK, D) + f'<path d="M110 255H930" stroke="{INK}" stroke-width="4"/>', 520, 500, 'drop', at='w:exam')
s.E('wq', mono(1010, 250, 'IT NOW READS', 24, WHITE) + mono(1010, 285, 'THE WHOLE QUESTION', 24, WHITE), 1150, 260, 'flick', at='w:whole')
for k, (n, opts) in enumerate(EXAM):
  y = 330 + k * 92
  s.E(f'q{k}', ttext(110, y, f'{k + 1}. WHERE IS {n}?', 50, INK, D) + mono(110, y + 34, opts, 22, INK, ls=1), 400, y, 'fade', at=f'w:Six+{k * .25:.2f}', d=.2)
for k in range(6):
  y = 330 + k * 92
  t = tag(700, y - 14, 'SEEN', LIME, INK, 22, 0, 240 + k) if k < 3 else tag(700, y - 14, 'NEVER SEEN', INK, WHITE, 22, 0, 240 + k)
  s.E(f't{k}', t, 760, y - 14, 'stamp', at=(f'w:knows+{k * .15:.2f}' if k < 3 else f'w:never+{(k - 3) * .15:.2f}'))

s = Shot(28, 'WHY MODELS GUESS', 'Two versions of the toy take the exam. The honest one answers what it knows, and says "I don\'t know" to the rest. '
         'The guesser answers what it knows, and picks a random option for the rest.')
s.add(bg())
COLS = [(110, 'HONEST', WHITE), (870, 'GUESSER', LIME)]
ANS = [['STORE', 'GYM', 'PARK'], [['LIBRARY', 'POOL', 'BAKERY'], ['SCHOOL', 'BEACH', 'MALL'], ['OFFICE', 'CLINIC', 'CAFE']]]
for c, (cx0, name, col) in enumerate(COLS):
  s.E(f'h{c}', strip(cx0, 70, 620, 120, col, 250 + c, text=name, size=100, rot=[-1.5, 1.5][c]), cx0 + 310, 130, 'slideL' if c == 0 else 'slideR', at=['w:honest', 'w:guesser'][c])
  for k in range(6):
    y = 280 + k * 100
    base = mono(cx0, y, f'{k + 1}.', 30, GRAY)
    if k < 3:
      s.E(f'a{c}{k}', base + ttext(cx0 + 70, y + 6, ANS[0][k], 64, WHITE, D), cx0 + 200, y - 15, 'fade', at=f'w:knows+{k * .15:.2f}', d=.2)
    elif c == 0:
      s.E(f'a{c}{k}', base + mono(cx0 + 70, y, 'I DON\'T KNOW', 36, GRAY), cx0 + 200, y - 15, 'flick', at=f'w:I+{(k - 3) * .15:.2f}')
    else:
      cyc = ''.join(f'<g class="cf" data-i="{q}">{ttext(cx0 + 70, y + 6, o + "?", 64, LIME, D)}</g>' for q, o in enumerate(ANS[1][k - 3]))
      s.E(f'a{c}{k}', base + cyc, cx0 + 200, y - 15, 'pop', at=f'w:random+{(k - 3) * .15:.2f}', fx=dict(cycle=[f'w:random+{(k - 3) * .15:.2f}', 'e0', k % 3]))

s = Shot(29, 'WHY MODELS GUESS', 'Most tests give one point for a right answer and zero for anything else. "I don\'t know" scores the same as a wrong answer.\n'
         'The honest toy scores three. The guesser also gets three, plus a one-in-three chance on each unknown question. On average it scores four. '
         'It beats the honest toy in 19 of the 27 possible ways its guesses can fall.', hold=.6)
s.add(bg() + edge_ht('r', 55, 110))
s.E('rl', strip(90, 70, 1100, 120, WHITE, 260, text='RIGHT +1 · WRONG 0 · IDK 0', size=96, rot=-1), 640, 130, 'slideL', at='w:point')
s.E('same', tag(110, 250, '"I DON\'T KNOW" = WRONG', RED, WHITE, 26, -1.5), 300, 250, 'stamp', at='w:same')
s.E('hs', ttext(110, 420, 'HONEST', 90, WHITE, D) + ttext(500, 420, '3', 110, WHITE, D), 300, 390, 'slideL', at='w:honest')
s.E('gs', ttext(110, 560, 'GUESSER', 90, LIME, D) + ttext(500, 560, '3 + 3 × 1/3', 110, LIME, D), 400, 530, 'slideL', at='w:guesser')
s.E('av', ttext(500, 690, '= 4', 130, LIME, D) + mono(720, 670, 'ON AVERAGE', 28, LIME, ls=4), 640, 650, 'stamp', at='w:average')
s.E('o', outline(1010, 780, '19/27', 150, {0, 1}, D, sw=2.6), 1235, 720, 'draw', at='w:19', d=1.0)
s.E('ow', mono(1014, 830, 'GUESSER WINS', 22, WHITE) + mono(1014, 862, 'IN 19 OF 27 CASES', 22, WHITE), 1200, 845, 'flick', at='w:ways')

TQ = ['"language models are optimized to be good', 'test-takers, and guessing when uncertain', 'improves test performance."']
s = Shot(30, 'WHY MODELS GUESS', 'So on this test, guessing wins. The paper says it plainly: "language models are optimized to be good test-takers, and guessing when uncertain improves test performance."', hold=.8)
s.add(bg() + edge_ht('l', 57, 120))
s.E('gw', ttext(200, 220, 'GUESSING WINS', 180, LIME, D), 600, 150, 'zoom', at='w:wins')
s.E('sh', strip(170, 320, 1260, 330, WHITE, 270, rot=-1), 800, 485, 'slideR', at='w:plainly')
s.E('src', mono(200, 730, 'KALAI ET AL., 2025 · WHY LANGUAGE MODELS HALLUCINATE', 22, GRAY), 600, 720, 'fade', at='w:plainly+.4')
typed(s, 'q', TQ, 230, 420, 40, INK, [('w:language', 'w:test-takers'), ('w:test-takers', 'w:improves'), ('w:improves', 'w:performance+.4')], 85, (-1, 800, 485))

s = Shot(31, 'WHY MODELS GUESS', 'Now change the rule. Right answer: plus one. Wrong answer: minus one. "I don\'t know": zero. '
         'The honest toy still scores three. The guesser now averages two. Guessing stops paying.')
s.add(bg() + edge_ht('r', 59, 150))
s.E('old', strip(90, 70, 1100, 120, WHITE, 260, text='RIGHT +1 · WRONG 0 · IDK 0', size=96, rot=-1), 640, 130, 'none', at=0, o=['w:rule', 'fall'])
for k, (txt, col, fg, cue) in enumerate([('RIGHT +1', WHITE, INK, 'w:plus'), ('WRONG −1', RED, WHITE, 'w:minus'), ('IDK 0', WHITE, INK, 'w:zero')]):
  bx = 90 + k * 400
  s.E(f'n{k}', strip(bx, 80, 360, 120, col, 280 + k, text=txt, size=92, col=fg, rot=[-2, 1, -1][k]), bx + 180, 140, 'stamp', at=cue)
s.E('hs', ttext(110, 400, 'HONEST', 90, WHITE, D) + ttext(500, 400, '3', 110, WHITE, D), 300, 370, 'slideL', at='w:honest')
s.E('gs', ttext(110, 540, 'GUESSER', 90, LIME, D) + ttext(500, 540, '2', 110, LIME, D) + mono(580, 520, 'ON AVERAGE', 28, LIME, ls=4), 400, 510, 'slideL', at='w:guesser')
s.E('mt', mono(110, 610, '3 + 3 × (1/3 × (+1) + 2/3 × (−1)) = 2', 26, GRAY, ls=1), 500, 600, 'flick', at='w:averages')
s.E('sp', ttext(110, 790, 'GUESSING STOPS PAYING', 140, WHITE, D), 700, 740, 'slideL', at='w:stops')

s = Shot(32, 'WHY MODELS GUESS', 'That\'s the paper\'s proposal: tests should state how confident a model must be before it answers, and take points away for wrong answers.', hold=.6)
s.add(bg() + edge_ht('l', 61, 140))
s.E('h', ttext(200, 250, "THE PAPER'S PROPOSAL", 150, WHITE, D), 700, 190, 'slideL', at='w:proposal')
s.E('src', mono(200, 780, 'KALAI ET AL., 2025', 22, GRAY), 400, 770, 'fade', at='w:proposal+.4')
s.E('p1', strip(200, 360, 1100, 130, LIME, 290, text='1. STATE THE CONFIDENCE NEEDED', size=92, rot=-1.5), 750, 425, 'slideR', at='w:confident')
s.E('p2', strip(240, 540, 1000, 130, WHITE, 291, text='2. PENALIZE WRONG ANSWERS', size=92, rot=1), 740, 605, 'slideR', at='w:away')

# ===== 7:20 what the toy leaves out =====
LEFT = [('A WORD-PAIR TABLE IS NOT A NEURAL NETWORK', 'w:word-pair'), ('REAL MODELS READ THE WHOLE QUESTION', 'w:whole'),
        ('THEY WORK WITH TOKENS: PIECES OF WORDS', 'w:work'), ('OUR EXAM IS A TOY EXAM', 'w:exam'), ('OTHER CAUSES OF FALSE ANSWERS EXIST', 'w:every')]
s = Shot(33, 'WHAT THIS TOY LEAVES OUT', 'Let\'s be clear about what we simplified.\n'
         'A word-pair table is not a neural network. Real models don\'t keep counts like ours.\n'
         'Real models read the whole question, not one word.\n'
         'Real models work with pieces of words called tokens, not whole words.\n'
         'Our exam is a toy exam. Real benchmarks are bigger, and many are not multiple choice.\n'
         'Not every false answer has these two causes. The paper covers these two; other causes exist.', tr='tear')
s.add(bg())
s.E('h', strip(80, 50, 900, 110, LIME, 300, text='WHAT THIS TOY LEAVES OUT', size=86, rot=-1), 530, 105, 'slideL', at='w:clear')
for k, (txt, cue) in enumerate(LEFT):
  y = 200 + k * 135; rot = [1, -1, 1.5, -.5, 1][k]; w = 60 + tw(txt, 72) + 60; x0 = 140 + (k % 2) * 60
  s.E(f'b{k}', strip(x0, y, w, 105, WHITE, 310 + k, text=txt, size=72, rot=rot, pad=60)
      + mono(x0 - 30, y + 66, f'{k + 1}', 30, LIME, 'end'), x0 + w / 2, y + 52, 'slideL' if k % 2 == 0 else 'slideR', at=cue)

s = Shot(34, 'WHAT THIS TOY LEAVES OUT', 'What carries over: a model trained to always continue the text, and rewarded for guessing, will sometimes produce fluent false statements. '
         'And the rarer a fact is, the likelier the guess.', hold=.6)
s.add(bg() + edge_ht('r', 63, 160))
s.E('h', mono(90, 130, 'WHAT CARRIES OVER', 30, LIME, ls=6), 300, 120, 'flick', at=0)
s.E('a', strip(90, 190, 820, 120, WHITE, 320, text='ALWAYS CONTINUE', size=100, rot=-1.5), 500, 250, 'slideL', at='w:always')
s.E('b', strip(160, 340, 1000, 120, WHITE, 321, text='+ REWARDED FOR GUESSING', size=100, rot=1), 660, 400, 'slideL', at='w:rewarded')
CS = 112
s.E('c', ttext(110, 600, '→ FLUENT', CS, WHITE, D) + ttext(110 + tw('→ FLUENT ', CS), 600, 'FALSE', CS, RED, D)
    + ttext(110 + tw('→ FLUENT FALSE ', CS), 600, 'STATEMENTS', CS, WHITE, D), 700, 550, 'zoom', at='w:fluent')
s.E('d', tag(110, 740, 'RARER FACT → LIKELIER GUESS', LIME, INK, 36, -1), 500, 740, 'slideL', at='w:rarer')

# ===== 8:10 what to do =====
s = Shot(35, 'WHAT TO DO', 'When an AI answer contains a rare, specific fact — a date, a name, a number, a quote, a reference — that\'s where a guess can hide. '
         'Check it against a source before you use it.', tr='tear')
s.add(bg() + edge_ht('r', 65, 130))
s.E('h', ttext(120, 220, 'A RARE, SPECIFIC FACT?', 140, WHITE, D), 600, 170, 'slideL', at='w:rare')
TX = [120, 340, 560, 840, 1060]
for k, w in enumerate(['DATE', 'NAME', 'NUMBER', 'QUOTE', 'REFERENCE']):
  rot = [-4, 3, -2, 4, -3][k]
  s.E(f'w{k}', tag(TX[k], 360 + (k % 2) * 40, w, WHITE, INK, 40, rot, 330 + k), TX[k] + 100, 370, 'stamp', at=f'w:{w.lower()}')
s.E('hd', mono(120, 520, 'A GUESS CAN HIDE HERE', 30, LIME, ls=4), 400, 510, 'flick', at='w:hide')
s.E('ck', strip(110, 600, 1150, 140, LIME, 340, text='CHECK AGAINST A SOURCE', size=110, rot=-1.5), 685, 670, 'slideR', at='w:Check')

s = Shot(36, 'WHAT TO DO', 'Fluent doesn\'t mean true. Our toy wrote a perfect sentence about Mom, and it was wrong two times out of three.', hold=.6)
s.add(bg() + edge_ht('r', 67, 150))
fw = tw('FLUENT', 200)
s.E('f', ttext(90, 260, 'FLUENT', 200, WHITE, D) + mono(130 + fw, 235, '≠', 170, LIME, ls=0) + ttext(280 + fw, 260, 'TRUE', 200, WHITE, D), 600, 190, 'zoom', at='w:Fluent')
fx0 = 90; hd = 'MOM IS AT THE '
s.E('mh', ttext(fx0, 560, hd.strip(), 130, WHITE, D), fx0 + 300, 515, 'slideL', at='w:Our')
gx = fx0 + tw(hd, 130)
s.E('mg', gl(gx, 560, 'GYM.', 130, WHITE), gx + 100, 515, 'slideL', at='w:Our', fx=dict(glitch=['w:wrong', 1]))
s.E('ms', stamp(gx + tw('GYM.', 130) + 130, 470, 'FALSE', -7, size=44), gx + tw('GYM.', 130) + 130, 470, 'stamp', at='w:wrong')
s.E('w2', mono(94, 680, 'WRONG 2 TIMES OUT OF 3', 34, RED, ls=4), 400, 670, 'flick', at='w:two')

s = Shot(37, 'END', 'The sheet, the table, the exam and a script that checks every number are linked below. Count it yourself.', hold=2.4)
word = 'COUNTABLE AI'; esz = round(1100 * 100 / tw(word, 100, 'wide200'))
s.add(bg())
s.E('hr', halftone(1390, -20, 230, 940, 14, LIME, 4, base=.5, soft=.4) + streaks(1390, -20, 230, 940, LIME, 4, base=.5, n=40, maxlen=.7), 1500, 450, 'slideR', at=0, d=.6)
s.E('hl', halftone(-20, -20, 200, 940, 14, LIME, 6, base=.55, soft=.4, flip=True), 80, 450, 'slideL', at=0, d=.6)
s.E('ttl', outline(240, 420, word, esz, set(), D, sw=2.5), 800, 350, 'draw', at=.1, d=1.5)
ax = 240 + tw('COUNTABLE ', esz, 'wide200')
s.E('ai', f'<text x="{ax:.1f}" y="420" font-family="{D}" font-size="{esz}" font-weight="200" fill="{LIME}" style="font-stretch:125%">AI</text>', ax + 100, 350, 'flick', at=1.5)
s.E('tg', clipped(mono(244, 500, 'HOW AI WORKS — ON EXAMPLES YOU CAN COUNT', 30, LIME), 240, 460, 1300, 60), 800, 490, 'wipe', at=1.8, d=.7)
s.E('fb', mono(244, 640, 'FILES BELOW: SHEET · TABLE · EXAM · CHECK SCRIPT', 28, WHITE), 700, 630, 'flick', at='w:linked')
s.E('cy', strip(240, 690, 760, 130, WHITE, 350, text='COUNT IT YOURSELF.', size=100, rot=-1.5), 620, 755, 'stamp', at='w:Count')
````
