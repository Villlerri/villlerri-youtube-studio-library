# Код пробных кадров

Кадр 1920×1080 вёрстан в HTML и снят браузером Chromium без окна (Playwright 1.48.2). Шрифты Google Fonts под OFL. Зерно и пятна бумаги — фильтр SVG `feTurbulence`, без файлов текстур.

## Источники

- Дискета: патент US 3,668,658 «Magnetic record disk cover», заявка 1969-12-22, выдан 1972-06-06, изобретатели Ralph Flores и Herbert E. Thompson. Чертёж — лист 2, https://patents.google.com/patent/US3668658A/en
- Скачки частоты: патент US 2,292,387 «Secret communication system», заявка 1941-06-10, выдан 1942-08-11, изобретатели Hedy Kiesler Markey и George Antheil. Чертёж — лист 2, https://patents.google.com/patent/US2292387A/en
- Права: «Subject to limited exceptions reflected in 37 CFR 1.71(d) & (e) and 1.84(s), the text and drawings of a patent are typically not subject to copyright restrictions.» — https://www.uspto.gov/terms-use-uspto-websites , прочитано 2026-10-25.

## Подготовка чертежа

Скан обрезан, белый фон переведён в прозрачность: чертёж ложится на бумагу как краска.

```python
from PIL import Image, ImageOps
im = Image.open('US3668658-drawings-page-3.png').convert('L'); w, h = im.size
im = im.crop((int(w*0.22), int(h*0.18), int(w*0.82), int(h*0.92)))
a = ImageOps.invert(im).point(lambda v: min(255, int(v*1.7)))
o = Image.new('RGBA', im.size, (30, 36, 24, 0)); o.putalpha(a); o.save('floppy_ink.png')
```

## Снимок кадра

```js
import { chromium } from 'playwright';
const [exe, html, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: exe, headless: true });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + html, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.screenshot({ path: out });
await b.close();
```

## Дискета

```html
<!doctype html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;600&family=Playfair+Display:ital,wght@1,700&display=block" rel="stylesheet">
<style>
:root{--paper:#ece2c6;--ink:#1e2418;--green:#3f5a2c;--orange:#d9662a;--yellow:#e8b13a;--red:#b8321f}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;background:var(--paper);color:var(--ink);overflow:hidden;position:relative;font-family:'IBM Plex Mono',monospace}
.grain{position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.6}
.stripes{position:absolute;left:1180px;top:0;bottom:0;width:420px;display:flex}
.stripes i{flex:1}
.panel{position:absolute;left:1020px;top:110px;width:740px;height:860px;background:var(--paper)}
.draw{position:absolute;left:1120px;top:120px;height:840px;mix-blend-mode:multiply}
h1{position:absolute;left:84px;top:36px;font-family:Anton;font-size:330px;line-height:.85;letter-spacing:-6px;text-transform:uppercase;color:var(--green)}
.kicker{position:absolute;left:92px;top:340px;font-size:26px;letter-spacing:8px;text-transform:uppercase}
.sub{position:absolute;left:90px;top:420px;font-family:'Playfair Display';font-style:italic;font-size:76px;line-height:1.02;width:860px}
.sub em{color:var(--orange);font-style:italic}
.facts{position:absolute;left:92px;top:760px;width:820px;border-top:5px solid var(--ink);display:grid;grid-template-columns:1fr 1fr 1fr;font-size:20px;letter-spacing:2px}
.facts div{padding:16px 14px 0 0;border-right:1px solid var(--ink);margin-right:14px}
.facts div:last-child{border:0}
.facts b{display:block;font-size:40px;font-family:Anton;font-weight:400;letter-spacing:1px;margin-top:6px}
.badge{position:absolute;left:1640px;top:820px;width:200px;height:200px;border-radius:50%;background:var(--red);color:var(--paper);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Anton;font-size:64px;line-height:.9;transform:rotate(-12deg)}
.badge small{font-family:"IBM Plex Mono";font-size:16px;letter-spacing:3px;margin-bottom:10px}
.no{position:absolute;left:1640px;top:130px;width:240px;font-family:Anton;font-size:34px;line-height:1.1;letter-spacing:2px}
.foot{position:absolute;left:0;right:0;bottom:0;height:52px;background:var(--ink);color:var(--paper);font-size:18px;letter-spacing:6px;display:flex;align-items:center;padding-left:92px;gap:60px}
</style></head><body>
<div class="stripes"><i style="background:var(--yellow)"></i><i style="background:var(--orange)"></i><i style="background:var(--red)"></i><i style="background:var(--green)"></i></div>
<div class="panel"></div>
<img class="draw" src="floppy_ink.png">
<div class="no">PATENT<br>US 3,668,658<br>FIG. 2</div>
<h1>Floppy</h1>
<div class="kicker">Forgotten tech · File 04</div>
<p class="sub">The plastic sleeve that made <em>data portable</em></p>
<div class="facts">
 <div>FILED<b>22 DEC 1969</b></div>
 <div>GRANTED<b>6 JUN 1972</b></div>
 <div>INVENTORS<b>2</b></div>
</div>
<div class="badge"><small>EST.</small>1972</div>
<div class="foot"><span>THE PATENT FILES</span><span>RETRO TECH IN PRINT</span></div>
<svg class="grain" width="1920" height="1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .4  0 0 0 0 .28  0 0 0 .55 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/>
<filter id="b"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .42  0 0 0 0 .3  0 0 0 .35 0"/></filter><rect width="100%" height="100%" filter="url(#b)"/></svg>
</body></html>
```

## Скачки частоты

```html
<!doctype html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;600&family=Playfair+Display:ital,wght@1,700&display=block" rel="stylesheet">
<style>
:root{--paper:#efe4cc;--ink:#1d1a16;--red:#c8361f;}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;background:var(--paper);color:var(--ink);overflow:hidden;position:relative;font-family:'IBM Plex Mono',monospace}
.grain{position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.55}
.sun{position:absolute;width:620px;height:620px;border-radius:50%;background:var(--red);left:1040px;top:250px}
.dots{position:absolute;left:1040px;top:250px;width:620px;height:620px;border-radius:50%;
  background-image:radial-gradient(var(--ink) 28%,transparent 30%);background-size:14px 14px;opacity:.18;mask-image:linear-gradient(200deg,transparent 35%,#000 90%)}
.draw{position:absolute;left:930px;top:70px;height:940px;mix-blend-mode:multiply}
h1{position:absolute;left:90px;top:40px;font-family:Anton;font-size:300px;line-height:.86;letter-spacing:-4px;text-transform:uppercase}
h1 span{color:var(--red)}
.sub{position:absolute;left:96px;top:600px;font-family:'Playfair Display';font-style:italic;font-size:64px;line-height:1.05;width:760px}
.facts{position:absolute;left:96px;top:800px;width:760px;border-top:4px solid var(--ink);display:grid;grid-template-columns:1fr 1fr 1fr;font-size:20px}
.facts div{padding:14px 12px 0 0;border-right:1px solid var(--ink);margin-right:12px}
.facts div:last-child{border:0}
.facts b{display:block;font-size:34px;font-family:Anton;font-weight:400;letter-spacing:1px;margin-top:6px}
.vert{position:absolute;right:60px;top:80px;writing-mode:vertical-rl;font-size:22px;letter-spacing:6px;text-transform:uppercase}
.no{position:absolute;right:120px;bottom:60px;font-family:Anton;font-size:56px;color:var(--red)}
.bar{position:absolute;left:0;right:0;bottom:0;height:26px;background:var(--ink)}
.tag{position:absolute;left:96px;top:1058px;font-size:15px;letter-spacing:4px;color:var(--paper);z-index:2}
</style></head><body>
<div class="sun"></div><div class="dots"></div>
<img class="draw" src="lamarr_ink.png">
<h1>Secret<br><span>Signal</span></h1>
<p class="sub">The 1942 piano-roll trick Bluetooth still uses</p>
<div class="facts">
 <div>FILED<b>10 JUN 1941</b></div>
 <div>GRANTED<b>11 AUG 1942</b></div>
 <div>CHANNELS<b>88</b></div>
</div>
<div class="vert">Patent drawings · Issue 01</div>
<div class="no">US 2,292,387</div>
<div class="bar"></div><div class="tag">THE PATENT FILES — VOL. 1</div>
<svg class="grain" width="1920" height="1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .38  0 0 0 0 .28  0 0 0 .55 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/>
<filter id="b"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="2"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .4  0 0 0 0 .3  0 0 0 .35 0"/></filter><rect width="100%" height="100%" filter="url(#b)"/></svg>
</body></html>
```
