# tmp/mock/gen.py

Первые макеты названий: 1-countable-ai, 2-guess-machine, 3-ai-since-1948. Картинки — в папке mock-img.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/gen.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Build three self-contained channel mockups: docs/channel-concepts/ai-tutorials/mockups/<n>-<slug>.html"""
import base64, json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '../../docs/channel-concepts/ai-tutorials/mockups')
def img(n): return 'data:image/webp;base64,' + base64.b64encode(open(f'{ROOT}/img/{n}.webp', 'rb').read()).decode()

TOPICS = [  # (title, hook words for thumbnail, year for the archive look, source)
  ('Why AI Makes Things Up — We Counted It by Hand', None, '1948', 'Shannon 1948; Kalai et al. 2025'),
  ('What "Training" Really Means: Fit 4 Points by Hand', ['4 dots', '1 line'], '1805', 'Legendre 1805, least squares'),
  ('Why AI Can\'t Count the R\'s in "Strawberry"', ['straw|berry', 'r = ?'], '1994', 'Gage 1994, byte pair encoding'),
  ('How Noise Becomes a Picture', ['noise', '→ picture'], '2015', 'Sohl-Dickstein et al. 2015'),
  ('Words as Points: How AI Knows "King" Is Like "Queen"', ['king', '≈ queen'], '2013', 'Mikolov et al. 2013, word2vec'),
  ('One Artificial Neuron, Worked Out on Paper', ['1 neuron', '3 numbers'], '1958', 'Rosenblatt 1958, perceptron'),
]

V = [
 dict(n=1, slug='countable-ai', name='Countable AI', handle='@CountableAI', slogan='How AI works, checked with a pencil.',
  fonts='family=Patrick+Hand&family=Atkinson+Hyperlegible:wght@400;700', head="'Patrick Hand',cursive", body="'Atkinson Hyperlegible',sans-serif", mono="'Patrick Hand',cursive",
  c=dict(bg='#FBF8F0', surface='#FFFFFF', text='#2A2E33', muted='#5E646B', line='#DCE6EF', accent='#C23B2A', extra='#FFE98A', ok='#2E7D4F'),
  sw=[('#FBF8F0','бумага'),('#DCE6EF','клетка'),('#2A2E33','графит'),('#C23B2A','ошибка'),('#FFE98A','стикер'),('#2E7D4F','верно')],
  fl=[('Patrick Hand','рукописный текст на листе'),('Atkinson Hyperlegible','субтитры, подписи, описание')],
  intro='Лист в клетку и карандаш. Всё, что показано, зритель пересчитает сам.',
  thumb='n1t', stills=['n1a','n1b','n1c','n1d'],
  cap=[('Three true sentences.','Три верных предложения: обучающий текст игрушки.'),('After "of": France 1, Italy 1, Peru 1.','Счёт чёрточками: что шло после «of».'),('It wrote "Italy".','Кубик выбрал Italy. Ложь в 2 случаях из 3.'),('What this toy leaves out.','Стикер «Что упрощено» со ссылкой на статью.')],
  thumb_bg="background-color:#FBF8F0;background-image:linear-gradient(#DCE6EF 1px,transparent 1px),linear-gradient(90deg,#DCE6EF 1px,transparent 1px);background-size:24px 24px"),
 dict(n=2, slug='guess-machine', name='The Guess Machine', handle='@TheGuessMachine', slogan='How AI works, one part at a time.',
  fonts='family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;700', head="'Space Grotesk',sans-serif", body="'Space Grotesk',sans-serif", mono="'JetBrains Mono',monospace",
  c=dict(bg='#12233B', surface='#1C3354', text='#E9EEF5', muted='#A9B6C8', line='#36507A', accent='#FFB547', extra='#FF6B5B', ok='#59D18C'),
  sw=[('#12233B','фон'),('#1C3354','панель'),('#F4F1E8','плитка'),('#FFB547','фокус'),('#FF6B5B','ложь'),('#4CC9F0','France'),('#B392F0','Peru')],
  fl=[('Space Grotesk','заголовки, субтитры'),('JetBrains Mono','плитки слов, счётчики')],
  intro='Машина из понятных деталей: плитки слов, корзины счётов, колесо выбора.',
  thumb='n2t', stills=['n2a','n2b','n2c','n2d'],
  cap=[('Paris is the capital of Italy.','Холодное начало: ошибка машины и штамп FALSE.'),('Three bins, one word each.','Корзины счётов после «of».'),('Then it spins.','Колесо: доля равна счёту.'),('Toy model · simplified.','Плашка «Что упрощено».')],
  thumb_bg="background-color:#12233B;background-image:radial-gradient(#36507A 1.2px,transparent 1.2px);background-size:22px 22px"),
 dict(n=3, slug='ai-since-1948', name='AI Since 1948', handle='@AISince1948', slogan='How AI works, from the papers that built it.',
  fonts='family=Courier+Prime:wght@400;700&family=Libre+Caslon+Text:wght@400;700&family=Atkinson+Hyperlegible:wght@400;700', head="'Libre Caslon Text',serif", body="'Atkinson Hyperlegible',sans-serif", mono="'Courier Prime',monospace",
  c=dict(bg='#EFE6D2', surface='#F8F2E3', text='#2B241B', muted='#6E604B', line='#C9B99A', accent='#9E2B25', extra='#7A6B55', ok='#4F6B3A'),
  sw=[('#EFE6D2','бумага'),('#F8F2E3','карточка'),('#2B241B','чернила'),('#7A6B55','выцветший'),('#9E2B25','штамп'),('#C9B99A','линейка')],
  fl=[('Libre Caslon Text','заголовки, выходные данные'),('Courier Prime','машинопись, цитаты'),('Atkinson Hyperlegible','субтитры, описание')],
  intro='Каждая идея — от статьи, где её впервые описали. Затем игрушка, затем современная статья.',
  thumb='n3t', stills=['n3a','n3b','n3c','n3d'],
  cap=[('Shannon, 1948.','Результат Шеннона дословно, из раздела 3.'),('Each word pair came from a real book.','Каждая пара слов — из книги. Целое — бессмыслица.'),('Every pair was seen in true text.','Игрушка на карточке: ложное предложение из верных пар.'),('What the toy leaves out.','Карточка со статьёй 2025 года, дословно.')],
  thumb_bg="background:#F8F2E3"),
]

def avatar(v, px):
  c = v['c']
  if v['n'] == 1:
    art = f'''<circle cx="50" cy="50" r="49" fill="{c['bg']}"/><g stroke="{c['line']}" stroke-width="1">{''.join(f'<path d="M{x} 0V100M0 {x}H100"/>' for x in range(10,100,12))}</g>
<g stroke="{c['text']}" stroke-width="5" stroke-linecap="round"><path d="M30 28V72M44 26V72M58 28V73"/></g><path d="M70 30 L74 74" stroke="{c['text']}" stroke-width="5" stroke-linecap="round"/>
<path d="M20 52 L82 46" stroke="{c['accent']}" stroke-width="5" stroke-linecap="round"/>'''
  elif v['n'] == 2:
    art = f'''<circle cx="50" cy="50" r="49" fill="{c['bg']}"/><g transform="translate(50 54)"><path d="M0 0L0 -34A34 34 0 0 1 29.4 17Z" fill="#4CC9F0"/><path d="M0 0L29.4 17A34 34 0 0 1 -29.4 17Z" fill="#FFB547"/><path d="M0 0L-29.4 17A34 34 0 0 1 0 -34Z" fill="#B392F0"/><circle r="6" fill="{c['bg']}"/></g><path d="M43 8H57L50 19Z" fill="{c['text']}"/>'''
  else:
    art = f'''<circle cx="50" cy="50" r="49" fill="{c['bg']}"/><rect x="18" y="26" width="64" height="48" fill="{c['surface']}" stroke="{c['line']}" stroke-width="1.5" transform="rotate(-4 50 50)"/>
<text x="50" y="58" text-anchor="middle" font-family="Courier Prime,monospace" font-weight="700" font-size="21" fill="{c['text']}" transform="rotate(-4 50 50)">1948</text><path d="M24 66H76" stroke="{c['accent']}" stroke-width="2.5" transform="rotate(-4 50 50)"/>'''
  return f'<svg class="av" viewBox="0 0 100 100" width="{px}" height="{px}" role="img" aria-label="аватар {v["name"]}">{art}</svg>'

def thumb(v, i):
  t, hook, year, _ = TOPICS[i]; c = v['c']
  if hook is None:
    return f'<div class="thumb"><img src="{img(v["thumb"])}" alt=""><span class="tag">PILOT</span></div>'
  a, b = hook
  if v['n'] == 1:
    inner = f'<div class="h1t" style="color:{c["text"]}">{a}</div><div class="h2t" style="color:{c["accent"]};border:3px solid {c["accent"]};border-radius:50%;padding:0 .4em">{b}</div>'
  elif v['n'] == 2:
    inner = f'<div class="tiles"><span>{a}</span><span class="hot">{b}</span></div>'
  else:
    inner = f'<div class="yr">{year}</div><div class="h3t">{a} {b}</div>'
  return f'<div class="thumb" style="{v["thumb_bg"]}"><div class="tin">{inner}</div></div>'

def short(v):
  if v['n'] == 1:
    body = '<div class="l" style="font-size:18px;color:var(--muted)">after "of": France 1 · Italy 1 · Peru 1</div><div class="l big">Paris is the capital of <span class="ring">Italy</span></div><div class="l" style="color:var(--accent)">false in 2 of 3 rolls</div>'
  elif v['n'] == 2:
    body = '<div class="tiles"><span>Paris</span><span>is</span><span>the</span><span>capital</span><span class="hot">of</span><span>Italy.</span></div><div class="stamp" style="color:#FF6B5B;border-color:#FF6B5B">FALSE</div><div class="l" style="font-size:17px;color:var(--muted)">reads only "of" · 1 chance in 3 of the truth</div>'
  else:
    body = '<div class="l" style="font-size:16px;color:var(--muted)">OUR TOY · three true sentences</div><div class="l">after "of": France 1 Italy 1 Peru 1</div><div class="l big" style="font-weight:700">Paris is the capital of Italy.</div><div class="stamp">FALSE</div>'
  return body + '<div class="st">Every sentence it learned was true.</div>'

def page(v):
  c = v['c']
  vids = ''.join(f'<div class="video">{thumb(v,i)}<h4>{t}</h4><p class="vmeta">{src}</p></div>' for i,(t,_,_,src) in enumerate(TOPICS))
  frames = ''.join(f'<figure><img src="{img(s)}" alt="кадр пробы"><figcaption><strong>{en}</strong>{ru}</figcaption></figure>' for s,(en,ru) in zip(v['stills'], v['cap']))
  sw = ''.join(f'<div><div class="swatch" style="background:{h}"></div><p>{h}<br><small>{d}</small></p></div>' for h,d in v['sw'])
  fl = ''.join(f'<div class="font-row"><b style="font-family:\'{f}\'">{f}</b><span>{d} · OFL 1.1</span></div>' for f,d in v['fl'])
  return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{v['name']} — подача {v['n']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?{v['fonts']}&display=swap" rel="stylesheet">
<style>
:root{{--bg:{c['bg']};--surface:{c['surface']};--text:{c['text']};--muted:{c['muted']};--line:{c['line']};--accent:{c['accent']};--extra:{c['extra']}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:{v['body']}}}
main{{max-width:1280px;margin:auto;padding:40px 32px 64px}}
.meta{{display:flex;justify-content:space-between;font-size:12px;letter-spacing:1px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}}
h1{{font-family:{v['head']};font-size:76px;line-height:1.05;margin:36px 0 12px;font-weight:700}}
.slogan{{font-size:22px;margin:0 0 8px}}.intro{{color:var(--muted);font-size:17px;line-height:1.6;max-width:640px}}
section{{border-top:1px solid var(--line);padding:32px 0 40px}}
h2{{font-family:{v['head']};font-size:28px;margin:0 0 6px;font-weight:700}}.note{{color:var(--muted);font-size:14px;margin:0 0 24px}}
.avatars{{display:flex;align-items:end;gap:48px;flex-wrap:wrap}}.avatars p{{font-size:12px;color:var(--muted);text-align:center}}
.banner{{position:relative;aspect-ratio:2560/1440;{v['thumb_bg']};border:1px solid var(--line);overflow:hidden}}
.safe{{position:absolute;left:19.8%;top:35.3%;width:60.4%;height:29.4%;border:1px dashed var(--muted);display:flex;align-items:center;justify-content:center;gap:4%;padding:2%}}
.safe .bn{{font-family:{v['head']};font-size:clamp(18px,4.2vw,54px);font-weight:700;white-space:nowrap}}.safe .bs{{font-size:clamp(9px,1.4vw,18px);color:var(--muted)}}
.cap{{font-size:12px;color:var(--muted);margin-top:8px}}
.channel{{border:1px solid var(--line);background:var(--surface);padding:28px}}
.ch{{display:flex;gap:20px;align-items:center;flex-wrap:wrap}}.ch h3{{font-family:{v['head']};font-size:32px;margin:0}}.ch p{{margin:4px 0;color:var(--muted)}}
.sub{{margin-left:auto;background:var(--text);color:var(--bg);border-radius:20px;padding:10px 20px;font-size:14px}}
.tabs{{display:flex;gap:28px;border-bottom:1px solid var(--line);margin:24px 0;font-size:14px;overflow-x:auto}}.tabs span{{padding:12px 0}}.tabs span:first-child{{border-bottom:2px solid var(--text)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 20px}}
.thumb{{position:relative;aspect-ratio:16/9;overflow:hidden;border:1px solid var(--line);border-radius:8px}}.thumb img{{width:100%;height:100%;object-fit:cover;display:block}}
.tag{{position:absolute;right:8px;bottom:8px;background:var(--accent);color:#fff;font-size:11px;padding:3px 7px;border-radius:4px;letter-spacing:1px}}
.tin{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6%;text-align:center}}
.h1t,.h2t{{font-family:{v['mono']};font-size:clamp(22px,3vw,40px);line-height:1}}
.tiles{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}}.tiles span{{font-family:{v['mono']};background:#F4F1E8;color:#12233B;border-radius:8px;padding:6px 12px;font-size:clamp(16px,2vw,26px);font-weight:700}}.tiles .hot{{background:var(--accent)}}
.yr{{font-family:'Libre Caslon Text',serif;font-weight:700;font-size:clamp(34px,4.6vw,62px);line-height:1}}.h3t{{font-family:{v['mono']};font-size:clamp(14px,1.6vw,20px);color:var(--accent);border:2px solid var(--accent);padding:2px 10px;transform:rotate(-3deg)}}
.video h4{{font-size:16px;line-height:1.4;margin:10px 0 4px}}.vmeta{{font-size:12px;color:var(--muted);margin:0}}
.frames{{display:grid;grid-template-columns:1fr 1fr;gap:28px 20px}}figure{{margin:0}}figure img{{width:100%;display:block;border:1px solid var(--line)}}figcaption{{font-size:14px;color:var(--muted);margin-top:10px;line-height:1.5}}figcaption strong{{display:block;color:var(--text)}}
.shorts{{display:grid;grid-template-columns:300px 1fr;gap:48px;align-items:center}}.short{{aspect-ratio:9/16;overflow:hidden;border:1px solid var(--line);border-radius:12px}}.short{{position:relative;display:flex;flex-direction:column;justify-content:center;gap:18px;padding:24px 24px 130px}}.short .l{{font-family:{v['mono']};font-size:24px;line-height:1.3}}.short .big{{font-size:34px}}.short .st{{position:absolute;left:16px;right:16px;bottom:56px;text-align:center;background:rgba(20,20,20,.86);color:#fff;font:700 16px 'Atkinson Hyperlegible',sans-serif;padding:8px;border-radius:6px}}.short .ring{{border:3px solid var(--accent);border-radius:50%;padding:0 10px;color:var(--text)}}.short .stamp{{align-self:flex-end;border:3px solid var(--accent);color:var(--accent);font-family:{v['mono']};font-weight:700;padding:2px 12px;transform:rotate(-6deg);border-radius:6px}}
.shorts h3{{font-family:{v['head']};font-size:36px;margin:0 0 12px}}.shorts p{{color:var(--muted);line-height:1.6}}
.sw{{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}}.swatch{{height:72px;border:1px solid var(--line)}}.sw p{{font-size:12px;margin:8px 0}}.sw small{{color:var(--muted)}}
.font-row{{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line);padding:14px 0;align-items:baseline;flex-wrap:wrap}}.font-row b{{font-size:26px;font-weight:400}}.font-row span{{font-size:13px;color:var(--muted)}}
footer{{border-top:1px solid var(--line);padding-top:20px;font-size:13px;color:var(--muted);line-height:1.6}}
@media(max-width:820px){{main{{padding:24px 16px 48px}}h1{{font-size:46px}}.grid,.frames,.shorts{{grid-template-columns:1fr}}.short{{max-width:300px}}.sw{{grid-template-columns:repeat(4,1fr)}}.channel{{padding:16px}}.sub{{margin-left:0}}}}
</style></head><body><main>
<div class="meta"><span>ОФОРМЛЕНИЕ КАНАЛА · ПОДАЧА {v['n']}</span><span>2026-10-17</span></div>
<h1>{v['name']}</h1><p class="slogan">{v['slogan']}</p><p class="intro">{v['intro']} Макет; название рабочее; канал не создан.</p>
<section><h2>Аватар</h2><p class="note">Читается и в 36 px.</p><div class="avatars"><div>{avatar(v,176)}<p>176 px</p></div><div>{avatar(v,88)}<p>88 px</p></div><div>{avatar(v,36)}<p>36 px</p></div></div></section>
<section><h2>Баннер</h2><p class="note">2560 × 1440, уменьшен. Пунктир — зона, видимая на всех устройствах.</p>
<div class="banner"><div class="safe">{avatar(v,96)}<div><div class="bn">{v['name']}</div><div class="bs">{v['slogan']}</div></div></div></div></section>
<section><h2>Страница канала</h2><p class="note">Шесть первых тем. Под каждым видео — источник.</p>
<div class="channel"><div class="ch">{avatar(v,80)}<div><h3>{v['name']}</h3><p>{v['handle']}</p><p>{v['slogan']}</p></div><span class="sub">Subscribe</span></div>
<div class="tabs"><span>Videos</span><span>Shorts</span><span>Sources</span><span>About</span></div><div class="grid">{vids}</div></div></section>
<section><h2>Кадры пробы</h2><p class="note">Из видеопробы 45 секунд. Голоса нет: ElevenLabs не подключён; текст диктора — субтитрами.</p><div class="frames">{frames}</div></section>
<section><h2>Shorts</h2><div class="shorts"><div class="short" style="{v['thumb_bg']}">{short(v)}</div><div><h3>Одна ошибка — один Short</h3><p>Вертикальный кадр 1080 × 1920 из той же сцены. 40 секунд: ошибка, счёт, вывод. Плашка «simplified» остаётся.</p></div></div></section>
<section><h2>Палитра и шрифты</h2><div class="sw">{sw}</div>{fl}</section>
<footer>Шрифты — SIL Open Font License 1.1, проверено в google/fonts 2026-10-17. Изображений, иконок, фото и логотипов нет: всё нарисовано кодом. Темы 2–6 — план, видео не сделаны. Годы и источники под темами — для сценариев; каждый сверяется с первоисточником до записи.</footer>
</main></body></html>'''

for v in V:
  open(f"{OUT}/{v['n']}-{v['slug']}.html", 'w').write(page(v))
  print(v['n'], v['slug'])
````
