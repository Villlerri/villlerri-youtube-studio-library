# tmp/pilot/sheet.py

Листы проверки 3×3 из PNG-кадров.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/pilot/sheet.py` рабочей копии. Порядок — в [index.md](index.md).

````python
"""Contact sheets: python3 sheet.py <dir> <prefix> — 3x3 tiles of 640x360 with the file name."""
import sys, os
from PIL import Image, ImageDraw
d, pre = sys.argv[1], sys.argv[2]
fs = sorted((f for f in os.listdir(d) if f.endswith('.png') and not f.startswith('sheet')), key=lambda f: float(f[1:-4]) if f[0] == 't' else f)
for k in range(0, len(fs), 9):
  im = Image.new('RGB', (1920, 1080), 'gray')
  for j, f in enumerate(fs[k:k + 9]):
    t = Image.open(os.path.join(d, f)).convert('RGB').resize((636, 356))
    im.paste(t, ((j % 3) * 640 + 2, (j // 3) * 360 + 2)); ImageDraw.Draw(im).text(((j % 3) * 640 + 8, (j // 3) * 360 + 340), f, fill='red')
  im.save(os.path.join(d, f'sheet-{pre}{k // 9}.png'))
````
