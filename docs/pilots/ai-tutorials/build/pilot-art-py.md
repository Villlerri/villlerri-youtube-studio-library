# tmp/pilot/art.py

Страницы обложки, аватара и баннера.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/art.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Channel art pages from the accepted mockup (gen4): thumbnail 1280x720, avatar 800x800, banner 2560x1440."""
import os, re
from engine import HERE, K, DEFS
from gen3 import TOPICS

def page(name, svg, w, h):
  html = (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?{K.fonts}&display=swap" rel="stylesheet">'
          f'<style>html,body{{margin:0;background:#0B0B0B;overflow:hidden}}svg{{display:block;width:{w}px;height:{h}px}}</style></head><body>{svg}</body></html>')
  open(os.path.join(HERE, 'art', name + '.html'), 'w').write(html)

os.makedirs(os.path.join(HERE, 'art'), exist_ok=True)
page('thumbnail', K.thumb(0, TOPICS[0]), 1280, 720)
page('avatar', f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs>{DEFS}</defs><style>text{{stroke:#0B0B0B;stroke-width:2.4px;stroke-linejoin:round;paint-order:stroke}}</style>{K.avatar()}</svg>', 800, 800)
page('banner', re.sub(r'viewBox="[^"]*"', 'viewBox="0 0 2560 1440"', K.banner(), count=1), 2560, 1440)
````
