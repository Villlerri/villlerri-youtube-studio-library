# Набор стиля Patented & Forgotten

Шаблоны сцен канала в одном файле [kit.html](kit.html). Сцена выбирается якорем: `kit.html#drawing`. Кадры — в [../mockups](../mockups/). Концепция — [../index.md](../index.md).

## Что внутри

- [kit.html](kit.html): 10 сцен — `cover`, `drawing`, `quote`, `number`, `timeline`, `photo`, `chapter`, `thumb`, `avatar`, `banner`.
- [assets/fig2_ink.png](assets/fig2_ink.png): чертёж FIG. 2 патента US 3,668,658, белый фон переведён в прозрачность.
- [assets/photo_dots.png](assets/photo_dots.png): фото 8-дюймовой дискеты, обрезано без логотипов, точечный растр.

## Паспорта материалов

- Чертёж: патент US 3,668,658 «Magnetic record disk cover», лист 2, FIG. 2. Заявка 1969-12-22, выдан 1972-06-06. Изобретатели Ralph Flores и Herbert E. Thompson, правообладатель IBM. https://patents.google.com/patent/US3668658A/en . Права: «the text and drawings of a patent are typically not subject to copyright restrictions» — https://www.uspto.gov/terms-use-uspto-websites , прочитано 2026-10-25.
- Номера деталей и цитата «rugged, inexpensive and mailable» — из текста того же патента. Ткань 3M 550, «pink wipe», — тоже из текста.
- Фото: «8`` floppy disk.jpg», автор Pamporoff, 2010-01-19, общественное достояние. https://commons.wikimedia.org/wiki/File:8%60%60_floppy_disk.jpg . На исходном фото логотипы IZOT, Verbatim и DataTraveler. Обрезка их убирает.
- Даты линии времени и «80 KB, read-only, 23FD, 1971» — статья Wikipedia «History of the floppy disk», прочитано 2026-10-28. Перед выпуском сверить с первоисточниками.
- Шрифты Google Fonts под OFL: Anton, IBM Plex Mono, Playfair Display.

## Как снять кадры

1. Положить рядом с `kit.html` скрипт `shot.mjs` (ниже). Нужен Playwright 1.48.2: `bun add playwright@1.48.2`.
2. `mkdir -p out && bun shot.mjs cover drawing quote number timeline photo chapter thumb avatar banner`.
3. Шрифты грузятся с Google Fonts. Без сети скачать их и подключить локально.

```js
import { chromium } from 'playwright';
const exe = '/home/boardagent/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const sizes = { thumb: [1280, 720], avatar: [800, 800], banner: [2560, 1440] };
const b = await chromium.launch({ executablePath: exe, headless: true });
for (const id of process.argv.slice(2)) {
  const [w, h] = sizes[id] || [1920, 1080];
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto('file://' + process.cwd() + '/kit.html#' + id, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: `out/${id}.png` }); await p.close();
}
await b.close();
```

## Подготовка чертежа и фото

Чертёж: скан листа обрезан, белое — в прозрачность, линии — цвет туши. Фото: обрезка, автоконтраст, сетка 9 px, точка тем крупнее, чем темнее клетка. Светлота поднята, иначе чёрная дискета сливается в пятно.

```python
from PIL import Image, ImageOps, ImageDraw
im = Image.open('US3668658-drawings-page-3.png').convert('L')
w, h = im.size
im = im.crop((int(w*0.24), int(h*0.19), int(w*0.79), int(h*0.885)))
a = ImageOps.invert(im).point(lambda v: min(255, int(v*1.7)))
o = Image.new('RGBA', im.size, (30, 36, 24, 0)); o.putalpha(a); o.save('fig2_ink.png')
p = Image.open('photo8.jpg').convert('L'); k = 1920/900   # фото шириной 1920 px
p = p.crop((int(450*k), int(220*k), int(750*k), int(680*k)))
p = ImageOps.autocontrast(p, cutoff=1); W, H = p.size; c = 9
out = Image.new('L', (W, H), 255); d = ImageDraw.Draw(out)
for y in range(0, H, c):
    for x in range(0, W, c):
        v = sum(p.crop((x, y, x+c, y+c)).getdata()) / (c*c)
        v = 110 + v*0.56; r = (1 - v/255) ** 0.9 * c * 0.75
        if r > 0.4: d.ellipse((x+c/2-r, y+c/2-r, x+c/2+r, y+c/2+r), fill=0)
o = Image.new('RGBA', (W, H), (30, 36, 24, 0)); o.putalpha(ImageOps.invert(out)); o.save('photo_dots.png')
```

## Правила стиля

- Бумага, тушь и один-два акцента в сцене. Четыре полосы акцентов — только обложка и баннер.
- Заголовок — Anton, крупно, на всю ширину. Подзаголовок — курсив Playfair. Подписи и даты — IBM Plex Mono, разрядка.
- Чертёж ложится на бумагу как краска: прозрачный фон, режим `multiply`.
- Выноски на чертеже — красные точки и линии. Номер детали — из текста патента.
- Фото — только в растре цвета туши, подпись автора и лицензии в кадре.
- Чужой логотип в кадр не ставим: обрезка или другой кадр.
- Текст баннера — внутри безопасной зоны 1546×423 в центре.
