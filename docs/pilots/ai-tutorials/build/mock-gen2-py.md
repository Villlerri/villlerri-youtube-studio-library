# tmp/mock/gen2.py

Первый круг стилей: style-1…4.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/gen2.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Four style mockups for Countable AI on an everyday example:
docs/channel-concepts/ai-tutorials/mockups/style-<n>-<slug>.html. All art is SVG drawn here."""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '../../docs/channel-concepts/ai-tutorials/mockups')

MSGS = ['Mom is at the store.', 'Dad is at the gym.', 'Sam is at the park.']
TOPICS = [
  ('Why AI Makes Things Up — We Counted It by Hand', 'Shannon 1948 · Kalai et al. 2025'),
  ('What "Training" Means: Guess the Pizza Price', 'Legendre 1805 · Cauchy 1847'),
  ('Why AI Can\'t Count the R\'s in "Strawberry"', 'Gage 1994 · Sennrich et al. 2016'),
  ('How AI Turns Static Into a Picture', 'Sohl-Dickstein et al. 2015 · Ho et al. 2020'),
  ('Why AI Gives a Different Answer Every Time', 'Holtzman et al. 2020'),
  ('How AI Knows "Pizza" Is Close to "Pasta"', 'Mikolov et al. 2013'),
]

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')

class Kit:
  """Drawing primitives; each style overrides them."""
  W = 1600; H = 900
  def t(self, x, y, s, size, fill=None, font=None, weight=400, anchor='start', rot=0):
    fill = fill or self.c['ink']; font = font or self.hand
    r = f' transform="rotate({rot} {x} {y})"' if rot else ''
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{r}>{esc(s)}</text>'

# ---------- 1. Kitchen Table ----------
class Kitchen(Kit):
  n = 1; slug = 'kitchen-table'; name = 'Kitchen Table'
  hand = "'Caveat',cursive"; ui = "'Nunito',sans-serif"
  fonts = 'family=Caveat:wght@500;700&family=Nunito:wght@400;700;800'
  c = dict(bg='#F3EBDD', surface='#FFFDF8', ink='#1F2A44', muted='#6A6256', line='#E1D5C1', accent='#D7263D', ok='#2E8B57',
           wood='#E7D3B5', grain='#D9C19C', note='#FFE066', pink='#FFB3C1', blue='#9BD3F2')
  intro = 'Стол сверху: стикеры, ручка, кружка, телефон. Рука пишет и считает на глазах.'
  takes = 'От лидеров: рисование на глазах — стиль Khan Academy, по Guo 2014 держит в 1,5–2 раза дольше слайдов. Отличие: вместо доски — предметы с кухонного стола зрителя.'
  sw = [('#E7D3B5', 'стол'), ('#FFE066', 'стикер'), ('#FFB3C1', 'стикер 2'), ('#1F2A44', 'ручка'), ('#D7263D', 'ошибка'), ('#2E8B57', 'верно'), ('#9BD3F2', 'выделение')]
  fl = [('Caveat', 'рукописные стикеры и счёт'), ('Nunito', 'ключевые слова, описание')]
  def bg(self, w, h):
    g = ''.join(f'<path d="M0 {y} C{w*.3} {y-14} {w*.6} {y+16} {w} {y-6}" stroke="{self.c["grain"]}" stroke-width="{2+(i%3)}" fill="none" opacity=".55"/>' for i, y in enumerate(range(20, h, max(28, h//14))))
    return f'<rect width="{w}" height="{h}" fill="{self.c["wood"]}"/>{g}'
  def note(self, x, y, w, h, lines, kind=0, rot=0, size=None):
    col = [self.c['note'], self.c['pink'], self.c['blue'], '#FFFFFF'][kind]
    size = size or h / (len(lines) + 1.2)
    tx = ''.join(self.t(x + w * .08, y + size * (1.05 + i * 1.1), l, size) for i, l in enumerate(lines))
    return f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x+6}" y="{y+8}" width="{w}" height="{h}" fill="#000" opacity=".12"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/><rect x="{x}" y="{y}" width="{w}" height="{h*.12}" fill="#000" opacity=".05"/>{tx}</g>'
  def wrong(self, x, y, w, h):
    return f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2+14}" ry="{h/2+10}" fill="none" stroke="{self.c["accent"]}" stroke-width="{max(3,h/12)}" transform="rotate(-4 {x+w/2} {y+h/2})"/>'
  def tick(self, x, y, s): return f'<path d="M{x} {y} l{s*.35} {s*.35} l{s*.65} -{s*.8}" stroke="{self.c["ok"]}" stroke-width="{s/7}" fill="none" stroke-linecap="round"/>'
  def hero(self, x, y, s):
    return (f'<circle cx="{x}" cy="{y}" r="{s*.5}" fill="#FFFFFF" stroke="{self.c["ink"]}" stroke-width="{s*.04}"/><circle cx="{x}" cy="{y}" r="{s*.36}" fill="#8B5E3C"/>'
            f'<path d="M{x+s*.48} {y-s*.14} q{s*.3} 0 {s*.3} {s*.16} q0 {s*.16} -{s*.3} {s*.16}" stroke="{self.c["ink"]}" stroke-width="{s*.05}" fill="none"/>')
  def avatar(self):
    return (f'<rect width="100" height="100" fill="{self.c["wood"]}"/><g transform="rotate(-6 50 50)"><rect x="20" y="20" width="62" height="62" fill="#000" opacity=".12"/><rect x="17" y="16" width="62" height="62" fill="{self.c["note"]}"/></g>'
            f'{self.t(48, 64, "1/3", 34, weight=700, anchor="middle", rot=-6)}<path d="M26 72 Q48 80 72 68" stroke="{self.c["accent"]}" stroke-width="4" fill="none" stroke-linecap="round"/>')

# ---------- 2. Phone Inside ----------
class Phone(Kit):
  n = 2; slug = 'phone-inside'; name = 'Phone Inside'
  hand = "'Inter',sans-serif"; ui = "'Inter',sans-serif"
  fonts = 'family=Inter:wght@400;600;800'
  c = dict(bg='#F2F3FA', surface='#FFFFFF', ink='#151826', muted='#5F6478', line='#DEE1EE', accent='#FF4D5E', ok='#14A86B',
           me='#2F6BFF', them='#FFFFFF', glow='#C9D6FF', key='#D3D6E3')
  intro = 'Всё происходит внутри телефона: подсказки клавиатуры, сообщения, уведомления. Зритель видит то, чем пользуется каждый день.'
  takes = 'От лидеров: один чистый холст и подсветка главного — как у 3Blue1Brown, принцип сигналов Mayer. Отличие: холст — знакомый экран телефона, а не тёмный фон с сетями.'
  sw = [('#F2F3FA', 'фон'), ('#FFFFFF', 'экран'), ('#2F6BFF', 'моё сообщение'), ('#D3D6E3', 'клавиатура'), ('#FF4D5E', 'ошибка'), ('#14A86B', 'верно'), ('#151826', 'текст')]
  fl = [('Inter', 'весь текст: интерфейс, ключевые слова, описание')]
  def bg(self, w, h):
    return (f'<defs><linearGradient id="pg{w}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E9EDFF"/><stop offset="1" stop-color="#F7F0FF"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#pg{w})"/><circle cx="{w*.88}" cy="{h*.15}" r="{h*.45}" fill="{self.c["glow"]}" opacity=".45"/>')
  def note(self, x, y, w, h, lines, kind=0, rot=0, size=None):
    me = kind in (0, 3); col = self.c['me'] if me else self.c['them']; fc = '#FFFFFF' if me else self.c['ink']
    size = size or h / (len(lines) + 1.4)
    tail = f'<path d="M{x+w-18} {y+h-2} q16 6 26 2 q-12 -6 -12 -20 Z" fill="{col}"/>' if me else f'<path d="M{x+18} {y+h-2} q-16 6 -26 2 q12 -6 12 -20 Z" fill="{col}"/>'
    tx = ''.join(self.t(x + h * .32, y + size * (1.15 + i * 1.2), l, size, fill=fc, weight=600) for i, l in enumerate(lines))
    return f'<g>{tail}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h/2,34)}" fill="{col}"/>{tx}</g>'
  def wrong(self, x, y, w, h):
    r = max(14, h * .32)
    return f'<circle cx="{x+w+r*.2}" cy="{y+h/2}" r="{r}" fill="{self.c["accent"]}"/>{self.t(x+w+r*.2, y+h/2+r*.42, "!", r*1.3, fill="#fff", weight=800, anchor="middle")}'
  def tick(self, x, y, s): return f'<circle cx="{x+s*.45}" cy="{y-s*.1}" r="{s*.55}" fill="{self.c["ok"]}"/><path d="M{x+s*.18} {y-s*.1} l{s*.2} {s*.2} l{s*.36} -{s*.42}" stroke="#fff" stroke-width="{s/8}" fill="none" stroke-linecap="round"/>'
  def bar(self, x, y, w, words, hot=None, size=34):
    cw = w / len(words); out = f'<rect x="{x}" y="{y}" width="{w}" height="{size*2.2}" rx="14" fill="{self.c["key"]}"/>'
    for i, wd in enumerate(words):
      cx = x + cw * i + cw / 2
      if i: out += f'<path d="M{x+cw*i} {y+size*.5} V{y+size*1.7}" stroke="#AEB3C6" stroke-width="2"/>'
      if hot == i: out += f'<rect x="{x+cw*i+8}" y="{y+8}" width="{cw-16}" height="{size*2.2-16}" rx="10" fill="#fff"/>'
      out += self.t(cx, y + size * 1.45, wd, size, anchor='middle', weight=600)
    return out
  def hero(self, x, y, s):
    return (f'<rect x="{x-s*.32}" y="{y-s*.55}" width="{s*.64}" height="{s*1.1}" rx="{s*.1}" fill="{self.c["ink"]}"/><rect x="{x-s*.27}" y="{y-s*.46}" width="{s*.54}" height="{s*.92}" rx="{s*.06}" fill="#fff"/>'
            + ''.join(f'<rect x="{x-s*.24+i*s*.165}" y="{y+s*.24}" width="{s*.15}" height="{s*.1}" rx="{s*.03}" fill="{self.c["me"] if i==1 else self.c["key"]}"/>' for i in range(3)))
  def avatar(self):
    return (f'<rect width="100" height="100" fill="{self.c["me"]}"/><rect x="14" y="38" width="72" height="26" rx="8" fill="#fff"/>'
            f'<rect x="17" y="41" width="20" height="20" rx="5" fill="{self.c["them"]}"/><rect x="40" y="41" width="20" height="20" rx="5" fill="{self.c["glow"]}"/><rect x="63" y="41" width="20" height="20" rx="5" fill="{self.c["them"]}"/>'
            f'{self.t(50, 30, "1 in 3", 15, fill="#fff", weight=800, anchor="middle")}{self.t(50, 84, "next word?", 12, fill="#fff", weight=600, anchor="middle")}')

# ---------- 3. Pop Shapes ----------
class Pop(Kit):
  n = 3; slug = 'pop-shapes'; name = 'Pop Shapes'
  hand = "'Fredoka',sans-serif"; ui = "'Nunito',sans-serif"
  fonts = 'family=Fredoka:wght@500;700&family=Nunito:wght@400;700;800'
  c = dict(bg='#FFF6E5', surface='#FFFFFF', ink='#16163F', muted='#5B5B7A', line='#EADFCB', accent='#FF5A36', ok='#1FB37A',
           sun='#FFC93C', cobalt='#2B50FF', mint='#7BE0B8', lilac='#C7B8FF')
  intro = 'Яркие плоские фигуры, толстый контур, у канала свой герой — кубик Guessy, который угадывает следующее слово.'
  takes = 'От лидеров: узнаваемый герой и плоский цвет — как у Kurzgesagt и CGP Grey. Отличие: герой — кубик, а не робот или мозг; одна сцена на кадр, без студии аниматоров.'
  sw = [('#FFF6E5', 'фон'), ('#FFC93C', 'солнце'), ('#2B50FF', 'кобальт'), ('#7BE0B8', 'мята'), ('#C7B8FF', 'сирень'), ('#FF5A36', 'ошибка'), ('#16163F', 'контур')]
  fl = [('Fredoka', 'заголовки, слова на плашках; только латиница'), ('Nunito', 'описание, подписи')]
  ru = "'Nunito',sans-serif"
  def bg(self, w, h):
    return (f'<rect width="{w}" height="{h}" fill="{self.c["bg"]}"/><circle cx="{w*.92}" cy="{h*.1}" r="{h*.38}" fill="{self.c["sun"]}"/>'
            f'<rect x="{-w*.05}" y="{h*.78}" width="{w*.3}" height="{h*.4}" rx="{h*.06}" fill="{self.c["mint"]}" transform="rotate(-8 0 {h})"/>')
  def note(self, x, y, w, h, lines, kind=0, rot=0, size=None):
    col = [self.c['surface'], self.c['lilac'], self.c['mint'], self.c['sun']][kind]
    size = size or h / (len(lines) + 1.2); sw = max(3, h / 16)
    tx = ''.join(self.t(x + w * .07, y + size * (1.1 + i * 1.12), l, size, weight=500) for i, l in enumerate(lines))
    return f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x+sw*1.6}" y="{y+sw*1.6}" width="{w}" height="{h}" rx="{h*.22}" fill="{self.c["ink"]}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h*.22}" fill="{col}" stroke="{self.c["ink"]}" stroke-width="{sw}"/>{tx}</g>'
  def wrong(self, x, y, w, h):
    cx, cy, r = x + w + h * .3, y - h * .15, h * .55
    import math
    pts = ' '.join(f'{cx+math.cos(a*math.pi/8)*(r if a%2==0 else r*.7):.1f},{cy+math.sin(a*math.pi/8)*(r if a%2==0 else r*.7):.1f}' for a in range(16))
    return f'<polygon points="{pts}" fill="{self.c["accent"]}" stroke="{self.c["ink"]}" stroke-width="{max(3,h/16)}"/>{self.t(cx, cy+r*.2, "NO", r*.62, fill="#fff", weight=700, anchor="middle")}'
  def tick(self, x, y, s): return f'<circle cx="{x+s*.45}" cy="{y-s*.1}" r="{s*.55}" fill="{self.c["ok"]}" stroke="{self.c["ink"]}" stroke-width="{s/12}"/><path d="M{x+s*.18} {y-s*.1} l{s*.2} {s*.2} l{s*.36} -{s*.42}" stroke="#fff" stroke-width="{s/8}" fill="none" stroke-linecap="round"/>'
  def hero(self, x, y, s, look=1):
    k = self.c['ink']; sw = s * .05
    return (f'<g><path d="M{x-s*.5} {y-s*.25} L{x} {y-s*.5} L{x+s*.5} {y-s*.25} L{x} {y} Z" fill="#FFFFFF" stroke="{k}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="M{x-s*.5} {y-s*.25} L{x} {y} L{x} {y+s*.55} L{x-s*.5} {y+s*.3} Z" fill="{self.c["cobalt"]}" stroke="{k}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="M{x+s*.5} {y-s*.25} L{x} {y} L{x} {y+s*.55} L{x+s*.5} {y+s*.3} Z" fill="{self.c["sun"]}" stroke="{k}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<circle cx="{x-s*.33}" cy="{y+s*.08}" r="{s*.06}" fill="#fff"/><circle cx="{x-s*.16}" cy="{y+s*.17}" r="{s*.06}" fill="#fff"/>'
            f'<ellipse cx="{x+s*.18}" cy="{y+s*.12}" rx="{s*.045}" ry="{s*.07}" fill="{k}"/><ellipse cx="{x+s*.34}" cy="{y+s*.04}" rx="{s*.045}" ry="{s*.07}" fill="{k}"/>'
            f'<path d="M{x+s*.17} {y+s*.3} q{s*.1} {s*.06} {s*.18} -{s*.08}" stroke="{k}" stroke-width="{sw*.8}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{x}" cy="-{s*.05}" rx="{s*.07}" ry="{s*.045}" fill="{k}" transform="translate(0 {y-s*.2})"/></g>')
  def avatar(self):
    return f'<rect width="100" height="100" fill="{self.c["bg"]}"/><circle cx="50" cy="50" r="40" fill="{self.c["lilac"]}"/>{self.hero(50, 50, 62)}'

# ---------- 4. Sticker Notebook ----------
class Notebook(Kit):
  n = 4; slug = 'sticker-notebook'; name = 'Sticker Notebook'
  hand = "'Kalam',cursive"; ui = "'Lexend',sans-serif"
  fonts = 'family=Kalam:wght@400;700&family=Lexend:wght@400;600;700&family=Nunito:wght@400;700;800'
  c = dict(bg='#FAFAF7', surface='#FFFFFF', ink='#1E1E1E', muted='#5E5E66', line='#E4E4EC', accent='#E53935', ok='#2E7D32',
           rule='#BFD7F5', margin='#F28B82', hl='#FFF176', hl2='#B9F6CA', hl3='#FFCCE0')
  intro = 'Разлинованный блокнот: маркер-выделитель, наклейки, стрелки от руки. Как конспект хорошего ученика.'
  takes = 'От лидеров: белый лист и простые схемы — как у StatQuest. Отличие: цвет маркера и наклейки; обложки не сливаются с серыми схемами конкурентов.'
  sw = [('#FFFFFF', 'лист'), ('#BFD7F5', 'линейка'), ('#F28B82', 'поля'), ('#FFF176', 'маркер'), ('#B9F6CA', 'маркер 2'), ('#E53935', 'ошибка'), ('#1E1E1E', 'чернила')]
  fl = [('Kalam', 'рукописные пометки и счёт; только латиница'), ('Lexend', 'наклейки, ключевые слова, описание; только латиница')]
  ru = "'Nunito',sans-serif"
  def bg(self, w, h):
    step = max(18, h / 16)
    rules = ''.join(f'<path d="M0 {y:.1f}H{w}" stroke="{self.c["rule"]}" stroke-width="{max(1,h/450)}"/>' for y in [step * 2 + i * step for i in range(int(h / step))])
    return f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>{rules}<path d="M{w*.08} 0V{h}" stroke="{self.c["margin"]}" stroke-width="{max(1.5,h/300)}"/>'
  def note(self, x, y, w, h, lines, kind=0, rot=0, size=None):
    col = [self.c['hl'], self.c['hl2'], self.c['hl3'], '#FFFFFF'][kind]
    size = size or h / (len(lines) + 1.2); b = max(4, h / 12)
    tx = ''.join(self.t(x + w * .07, y + size * (1.1 + i * 1.12), l, size, font=self.ui, weight=600) for i, l in enumerate(lines))
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x-b+3}" y="{y-b+6}" width="{w+2*b}" height="{h+2*b}" rx="{h*.25+b}" fill="#000" opacity=".14"/>'
            f'<rect x="{x-b}" y="{y-b}" width="{w+2*b}" height="{h+2*b}" rx="{h*.25+b}" fill="#fff"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h*.25}" fill="{col}"/>{tx}</g>')
  def hl(self, x, y, w, h, col=None):
    return f'<path d="M{x} {y+h*.15} L{x+w} {y} L{x+w+6} {y+h} L{x+4} {y+h*1.05} Z" fill="{col or self.c["hl"]}" opacity=".85"/>'
  def wrong(self, x, y, w, h):
    s = h * .9; cx = x + w + s * .6; cy = y + h / 2
    return f'<path d="M{cx-s/2} {cy-s/2} L{cx+s/2} {cy+s/2} M{cx+s/2} {cy-s/2} L{cx-s/2} {cy+s/2}" stroke="{self.c["accent"]}" stroke-width="{s/6}" stroke-linecap="round"/>'
  def tick(self, x, y, s): return f'<path d="M{x} {y} l{s*.35} {s*.35} l{s*.65} -{s*.8}" stroke="{self.c["ok"]}" stroke-width="{s/7}" fill="none" stroke-linecap="round"/>'
  def hero(self, x, y, s):
    return (f'<g transform="rotate(-35 {x} {y})"><rect x="{x-s*.5}" y="{y-s*.12}" width="{s*.8}" height="{s*.24}" rx="{s*.05}" fill="{self.c["hl"]}" stroke="{self.c["ink"]}" stroke-width="{s*.03}"/>'
            f'<path d="M{x+s*.3} {y-s*.1} L{x+s*.5} {y-s*.06} L{x+s*.5} {y+s*.06} L{x+s*.3} {y+s*.1} Z" fill="{self.c["ink"]}"/></g>')
  def avatar(self):
    return (f'<rect width="100" height="100" fill="#fff"/>{self.bg(100,100)}{self.hl(16, 40, 66, 22)}'
            f'{self.t(50, 60, "1 of 3", 22, font=self.hand, weight=700, anchor="middle")}<circle cx="50" cy="50" r="47" fill="none" stroke="{self.c["ink"]}" stroke-width="3"/>')

STYLES = [Kitchen(), Phone(), Pop(), Notebook()]

# ---------- shared scenes ----------
def svg(w, h, body, cls=''):
  return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>'

def thumb(k, i):
  W, H = 320, 180; c = k.c; b = k.bg(W, H)
  if i == 0:
    b += k.note(18, 34, 228, 58, ['Mom is at the gym.'], kind=0, rot=-3, size=22) + k.wrong(18, 34, 228, 58)
    b += k.t(30, 150, '2 in 3', 46, fill=c['accent'], weight=700) + k.t(176, 150, 'wrong', 30, weight=700)
  elif i == 1:
    for j, (s, p) in enumerate([(26, '$9'), (36, '$13'), (48, '?')]):
      cx = 54 + j * 92; b += f'<circle cx="{cx}" cy="86" r="{s}" fill="#F4B942" stroke="{c["ink"]}" stroke-width="3"/><circle cx="{cx}" cy="86" r="{s*.78}" fill="#E8553E"/>' + ''.join(f'<circle cx="{cx+dx*s*.35}" cy="{86+dy*s*.35}" r="{s*.12}" fill="#FFF3D6"/>' for dx, dy in [(-1, -1), (1, 0), (0, 1)])
      b += k.t(cx, 156, p, 28, weight=700, anchor='middle', fill=c['accent'] if p == '?' else c['ink'])
  elif i == 2:
    b += k.note(16, 46, 132, 60, ['straw'], kind=1, size=34) + k.note(166, 46, 138, 60, ['berry'], kind=2, size=34)
    b += k.t(160, 156, 'r = ?', 42, weight=700, anchor='middle', fill=c['accent'])
  elif i == 3:
    import random; rnd = random.Random(7)
    b += ''.join(f'<rect x="{24+x*10}" y="{36+y*10}" width="10" height="10" fill="{rnd.choice(["#222","#777","#bbb","#eee"])}"/>' for x in range(11) for y in range(11))
    b += f'<path d="M150 90 h34" stroke="{c["ink"]}" stroke-width="6" stroke-linecap="round"/><path d="M180 78 l14 12 l-14 12" stroke="{c["ink"]}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    b += f'<circle cx="252" cy="96" r="38" fill="{c["ink"]}"/><path d="M220 76 l6 -34 l20 24 Z M284 76 l-6 -34 l-20 24 Z" fill="{c["ink"]}"/><circle cx="238" cy="92" r="6" fill="#fff"/><circle cx="266" cy="92" r="6" fill="#fff"/>'
  elif i == 4:
    b += k.t(20, 40, 'Where is Mom?', 26, weight=700)
    for j, wd in enumerate(['store', 'gym', 'park']):
      b += k.note(22 + j * 98, 70 + (j % 2) * 14, 88, 46, [wd], kind=j % 3, rot=(-4, 3, -2)[j], size=26)
    b += k.t(160, 168, 'same question', 20, anchor='middle', fill=c['muted'], weight=700)
  else:
    pts = [('pizza', 70, 70), ('pasta', 112, 98), ('salad', 92, 140), ('gym', 228, 54), ('park', 236, 120)]
    for wd, x, y in pts: b += f'<circle cx="{x}" cy="{y}" r="7" fill="{c["accent"] if wd in ("pizza","pasta") else c["ink"]}"/>' + k.t(x + 12, y + 7, wd, 22, weight=700)
    b += f'<ellipse cx="94" cy="86" rx="58" ry="40" fill="none" stroke="{c["accent"]}" stroke-width="3" stroke-dasharray="8 6"/>'
  return svg(W, H, b, 'thumbsvg')

def frame(k, f):
  W, H = 1600, 900; c = k.c; b = k.bg(W, H)
  cap = ['Everything it learned: three true messages.', 'After "the": store 1 · gym 1 · park 1.', 'It wrote "Mom is at the gym." Wrong 2 times in 3.'][f]
  if f == 0:
    for j, m in enumerate(MSGS):
      x, y = 260 + j * 30, 150 + j * 210
      b += k.note(x, y, 820, 150, [m], kind=j % 3 if k.n != 2 else 1, rot=(-2, 1.5, -1)[j], size=74) + k.tick(x + 900, y + 95, 70)
    b += k.hero(1430, 720, 210)
  elif f == 1:
    b += k.t(160, 170, 'Mom is at the ___', 92, weight=700)
    if k.n == 2:
      b += k.bar(160, 300, 1280, ['store', 'gym', 'park'], size=60)
      b += ''.join(k.t(160 + 1280 / 3 * j + 1280 / 6, 520, '1 / 3', 72, anchor='middle', weight=800, fill=c['me']) for j in range(3))
    else:
      for j, wd in enumerate(['store', 'gym', 'park']):
        y = 290 + j * 175
        b += k.note(200, y, 420, 130, [wd], kind=j % 3, size=72)
        b += f'<path d="M700 {y+40}V{y+110}" stroke="{c["ink"]}" stroke-width="12" stroke-linecap="round"/>' + k.t(790, y + 100, '1 of 3', 80, weight=700, fill=c['accent'] if j == 1 else c['ink'])
    b += k.t(160, 860, 'It reads only the last word: "the".', 48, font=k.ui, fill=c['muted'], weight=700)
  else:
    b += k.note(180, 170, 1100, 170, ['Mom is at the gym.'], kind=0, rot=-2, size=96) + k.wrong(180, 170, 1100, 170)
    b += k.t(200, 520, 'Every word pair was true.', 70, weight=700) + k.t(200, 620, 'The sentence is false.', 70, weight=700, fill=c['accent'])
    for j in range(9):
      x, y = 200 + j * 110, 720; ok = j % 3 == 0
      b += f'<rect x="{x}" y="{y}" width="90" height="90" rx="16" fill="{c["ok"] if ok else c["accent"]}" opacity="{1 if ok else .85}"/>' + k.t(x + 45, y + 64, '✓' if ok else '✗', 56, fill='#fff', weight=700, anchor='middle', font=k.ui)
    b += k.t(1240, 790, '6 of 9', 80, weight=700, fill=c['accent'])
  b += f'<rect x="{W-230}" y="24" width="206" height="52" rx="26" fill="{c["ink"]}" opacity=".85"/>' + k.t(W - 127, 60, 'toy model', 30, fill='#fff', anchor='middle', font=k.ui, weight=700)
  return svg(W, H, b, 'framesvg'), cap

def short(k):
  W, H = 540, 960; c = k.c; b = k.bg(W, H)
  b += k.t(40, 120, 'It learned only', 44, weight=700) + k.t(40, 172, 'true messages.', 44, weight=700)
  for j, m in enumerate(MSGS): b += k.note(40, 220 + j * 92, 420, 70, [m], kind=1 if k.n == 2 else j % 3, size=34)
  b += k.note(40, 540, 420, 90, ['Mom is at the gym.'], kind=0, rot=-3, size=38) + k.wrong(40, 540, 420, 90)
  b += k.t(40, 740, 'wrong', 64, weight=700, fill=c['accent']) + k.t(40, 810, '2 times in 3', 64, weight=700)
  return svg(W, H, b, 'shortsvg')

def banner(k):
  W, H = 2560, 1440; c = k.c; b = k.bg(W, H)
  b += f'<rect x="507" y="508" width="1546" height="423" fill="none" stroke="{c["muted"]}" stroke-width="4" stroke-dasharray="18 14"/>'
  b += f'<g transform="translate(560 540) scale(3.6)">{k.avatar()}</g>'
  b += k.t(1000, 700, 'Countable AI', 150, weight=700, font=k.hand if k.n != 2 else k.ui) + k.t(1004, 800, 'How AI works — on examples you can check yourself.', 52, font=k.ui, fill=c['muted'], weight=700)
  b += k.note(120, 160, 660, 140, ['Mom is at the store.'], kind=0 if k.n != 2 else 1, rot=-4, size=52) + k.note(1980, 1120, 480, 140, ['1 of 3'], kind=1 if k.n != 2 else 3, rot=3, size=70)
  return svg(W, H, b, 'bannersvg')

def avatar(k, px): return f'<svg viewBox="0 0 100 100" width="{px}" height="{px}" style="border-radius:50%;display:block;width:{px}px;height:{px}px;flex:none" role="img" aria-label="аватар"><defs><clipPath id="cl{px}"><circle cx="50" cy="50" r="50"/></clipPath></defs><g clip-path="url(#cl{px})">{k.avatar()}</g></svg>'

def page(k):
  c = k.c
  vids = ''.join(f'<div class="video"><div class="thumb">{thumb(k,i)}{"<span class=tag>PILOT</span>" if i==0 else ""}</div><h4>{esc(t)}</h4><p class="vmeta">{s}</p></div>' for i, (t, s) in enumerate(TOPICS))
  frames = ''.join(f'<figure>{sv}<figcaption><strong>{esc(cp)}</strong></figcaption></figure>' for sv, cp in (frame(k, f) for f in range(3)))
  sw = ''.join(f'<div><div class="swatch" style="background:{h}"></div><p>{h}<br><small>{d}</small></p></div>' for h, d in k.sw)
  fl = ''.join(f'<div class="font-row"><b style="font-family:\'{f}\'">{f}</b><span>{d} · OFL 1.1</span></div>' for f, d in k.fl)
  return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Countable AI — {k.name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?{k.fonts}&display=swap" rel="stylesheet">
<style>
:root{{--bg:{c['bg']};--surface:{c['surface']};--text:{c['ink']};--muted:{c['muted']};--line:{c['line']};--accent:{c['accent']}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:{getattr(k,'ru',k.ui)}}}
main{{max-width:1280px;margin:auto;padding:40px 32px 64px}}
svg{{display:block;width:100%;height:auto}}
.meta{{display:flex;justify-content:space-between;gap:12px;font-size:12px;letter-spacing:1px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}}
h1{{font-family:{k.hand};font-size:76px;line-height:1.05;margin:36px 0 12px;font-weight:700}}
.slogan{{font-size:22px;margin:0 0 8px}}.intro{{color:var(--muted);font-size:17px;line-height:1.6;max-width:720px}}
.takes{{background:var(--surface);border:1px solid var(--line);border-left:6px solid var(--accent);padding:16px 20px;font-size:16px;line-height:1.6;max-width:820px}}
section{{border-top:1px solid var(--line);padding:32px 0 40px}}
h2{{font-family:{getattr(k,'ru',k.hand)};font-size:30px;margin:0 0 6px;font-weight:800}}.note{{color:var(--muted);font-size:14px;margin:0 0 24px;line-height:1.5}}
.avatars{{display:flex;align-items:end;gap:48px;flex-wrap:wrap}}.avatars p{{font-size:12px;color:var(--muted);text-align:center}}
.banner{{border:1px solid var(--line);overflow:hidden}}
.channel{{border:1px solid var(--line);background:var(--surface);padding:28px}}
.ch{{display:flex;gap:20px;align-items:center;flex-wrap:wrap}}.ch h3{{font-family:{k.hand};font-size:34px;margin:0}}.ch p{{margin:4px 0;color:var(--muted)}}
.sub{{margin-left:auto;background:var(--text);color:var(--bg);border-radius:20px;padding:10px 20px;font-size:14px}}
.tabs{{display:flex;gap:28px;border-bottom:1px solid var(--line);margin:24px 0;font-size:14px;overflow-x:auto}}.tabs span{{padding:12px 0}}.tabs span:first-child{{border-bottom:2px solid var(--text)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 20px}}
.thumb{{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:10px}}
.tag{{position:absolute;right:8px;bottom:8px;background:var(--accent);color:#fff;font-size:11px;padding:3px 7px;border-radius:4px;letter-spacing:1px}}
.video h4{{font-size:16px;line-height:1.4;margin:10px 0 4px}}.vmeta{{font-size:12px;color:var(--muted);margin:0}}
.frames{{display:grid;grid-template-columns:1fr;gap:28px}}figure{{margin:0}}figure svg{{border:1px solid var(--line)}}figcaption{{font-size:15px;margin-top:10px;line-height:1.5}}
.shorts{{display:grid;grid-template-columns:300px 1fr;gap:48px;align-items:center}}.short{{border:1px solid var(--line);border-radius:14px;overflow:hidden;max-width:300px}}
.shorts h3{{font-family:{getattr(k,'ru',k.hand)};font-size:34px;margin:0 0 12px}}.shorts p{{color:var(--muted);line-height:1.6}}
.sw{{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}}.swatch{{height:72px;border:1px solid var(--line)}}.sw p{{font-size:12px;margin:8px 0}}.sw small{{color:var(--muted)}}
.font-row{{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);padding:14px 0;align-items:baseline;flex-wrap:wrap}}.font-row b{{font-size:28px;font-weight:400}}.font-row span{{font-size:13px;color:var(--muted)}}
footer{{border-top:1px solid var(--line);padding-top:20px;font-size:13px;color:var(--muted);line-height:1.6}}
@media(max-width:820px){{main{{padding:24px 16px 48px}}h1{{font-size:46px}}.grid,.shorts{{grid-template-columns:1fr}}.sw{{grid-template-columns:repeat(4,1fr)}}.channel{{padding:16px}}.sub{{margin-left:0}}}}
</style></head><body><main>
<div class="meta"><span>ОФОРМЛЕНИЕ КАНАЛА · СТИЛЬ {k.n} ИЗ 4</span><span>2026-10-17</span></div>
<h1>{k.name}</h1><p class="slogan">Countable AI — how AI works, on examples you can check yourself.</p>
<p class="intro">{k.intro} Макет; название канала рабочее; канал не создан.</p>
<p class="takes">{k.takes}</p>
<section><h2>Аватар</h2><p class="note">Читается и в 36 px.</p><div class="avatars"><div>{avatar(k,176)}<p>176 px</p></div><div>{avatar(k,88)}<p>88 px</p></div><div>{avatar(k,36)}<p>36 px</p></div></div></section>
<section><h2>Баннер</h2><p class="note">2560 × 1440, уменьшен. Пунктир — зона, видимая на всех устройствах.</p><div class="banner">{banner(k)}</div></section>
<section><h2>Страница канала</h2><p class="note">Шесть тем из плана, у каждой бытовой пример. Под видео — первоисточник.</p>
<div class="channel"><div class="ch">{avatar(k,80)}<div><h3>Countable AI</h3><p>@CountableAI</p><p>How AI works, on examples you can check yourself.</p></div><span class="sub">Subscribe</span></div>
<div class="tabs"><span>Videos</span><span>Shorts</span><span>Sources</span><span>About</span></div><div class="grid">{vids}</div></div></section>
<section><h2>Кадры пилота</h2><p class="note">Три кадра одного объяснения. В видео звучит голос ElevenLabs; на экране — только ключевые слова. Полные субтитры — дорожкой YouTube, зритель включает сам.</p><div class="frames">{frames}</div></section>
<section><h2>Shorts</h2><div class="shorts"><div class="short">{short(k)}</div><div><h3>Одна ошибка — один Short</h3><p>Вертикальный кадр 1080 × 1920. 40 секунд: выучила, ошиблась, посчитали. В Shorts крупные слова на экране: их часто смотрят без звука — гипотеза, данных нет.</p></div></div></section>
<section><h2>Палитра и шрифты</h2><div class="sw">{sw}</div>{fl}</section>
<footer>Шрифты — SIL Open Font License 1.1, проверено в google/fonts 2026-10-17. Фото, чужих иллюстраций, иконок и логотипов нет: всё нарисовано кодом. Темы 2–6 — план, видео не сделаны. Пример «Mom is at the store» — тот же счёт, что в пилоте: 9 предложений, ложных 6.</footer>
</main></body></html>'''

for k in STYLES:
  open(f"{OUT}/style-{k.n}-{k.slug}.html", 'w').write(page(k))
  print(k.n, k.slug)
````
