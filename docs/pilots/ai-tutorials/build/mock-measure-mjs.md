# tmp/mock/measure.mjs

Замер ширин букв шрифтов в widths.json.

Исходник сборщика пилота Countable AI, задача 60. Восстановить: блок кода — в файл `tmp/mock/measure.mjs` рабочей копии. Порядок — в [index.md](index.md).

````js
// usage: bun measure.mjs > widths.json   advance widths at 100px for the fonts gen4 uses
import { chromium } from '/srv/projects/vmsetup/board/node_modules/playwright/index.mjs';
const b = await chromium.launch({ args: ['--single-process', '--no-zygote', '--disable-dev-shm-usage', '--disable-gpu'] });
const p = await b.newPage();
await p.setContent(`<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet"><span style="font-family:Archivo">x</span>`);
await p.evaluate(() => Promise.all([document.fonts.load('900 100px Archivo'), document.fonts.load('ultra-condensed 900 100px Archivo'), document.fonts.load('expanded 200 100px Archivo')]).then(() => document.fonts.ready));
const chars = [...new Set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,'’\"?!$=/→≈×-—_:")];
const res = await p.evaluate((chars) => {
  const ns = 'http://www.w3.org/2000/svg'; const sv = document.createElementNS(ns, 'svg'); document.body.appendChild(sv); const out = {};
  for (const [k, w, st] of [['cond900', 900, '62%'], ['wide200', 200, '125%']]) {
    out[k] = {};
    for (const ch of chars) {
      const t = document.createElementNS(ns, 'text'); t.setAttribute('font-family', "'Archivo',sans-serif"); t.setAttribute('font-size', '100'); t.setAttribute('font-weight', w);
      t.setAttribute('style', 'font-stretch:' + st); t.setAttribute('xml:space', 'preserve'); t.textContent = 'H' + ch + 'H'; sv.appendChild(t);
      const h = document.createElementNS(ns, 'text'); for (const a of t.getAttributeNames()) h.setAttribute(a, t.getAttribute(a)); h.textContent = 'HH'; sv.appendChild(h);
      out[k][ch] = Math.round((t.getComputedTextLength() - h.getComputedTextLength()) * 10) / 10;
    }
  }
  return out;
}, chars);
console.log(JSON.stringify(res));
await b.close();
````
