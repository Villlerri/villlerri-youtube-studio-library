---
id: vpython
name: VPython и GlowScript (Web VPython)
class: [simulation]
kind: library
site: https://vpython.org/
github: vpython/vpython-jupyter
scenes: [simulation, mechanism, field]
quality: 2
human_difficulty: 1
agent_difficulty: 3
automation: 2
reproducibility: 2
cost: 0
maturity: declining
platforms: [linux, macos, windows, web]
export: [png, html]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# VPython и GlowScript (Web VPython)

Учебная среда для простой 3D-графики в реальном времени: пишешь `sphere()` и получаешь управляемую 3D-сцену. Две формы: пакет `vpython` для обычного Python (показывает сцену в браузере или блокноте Jupyter) и Web VPython на сайте glowscript.org (раньше GlowScript VPython), который запускает код прямо в браузере.

## Ссылки

- Официальный сайт: <https://vpython.org/>
- Web VPython: <https://www.glowscript.org/> (он же webvpython.org)
- GitHub: <https://github.com/vpython/vpython-jupyter> (пакет для Python); ядро GlowScript: <https://github.com/vpython/glowscript>
- Документация: <https://www.glowscript.org/docs/VPythonDocs/index.html>
- Примеры, проверенные 2026-10-14:
  - [GlowScript Demos: Examples](https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/) — каталог примеров, открывается в браузере.
  - [Visualizing Physics Using VPython](https://www.youtube.com/watch?v=Y-XGB9TSvzE) — Bruce Sherwood (автор VPython) показывает навигируемые 3D-анимации физических систем, канал Matter & Interactions, около часа.
  - [Python Physics: Using Web VPython to Illustrate a Physics Question](https://www.youtube.com/watch?v=JB0CGWdSDKk) — анимация падения шарика с движущейся окружности, канал Dot Physics, около 20 минут.
  - [Simulation of Pendulum: VPython Tutorial 3](https://www.youtube.com/watch?v=snOkw1zzLGw) — любительский урок по маятнику.

## Что реально получается

Сквозной пример (магнит на холодильнике). Прямого расчёта поля магнита нет. Можно нарисовать стрелки поля по аналитической формуле и показать стрелку компаса в поле, как в школьных демонстрациях. Для линий поля сложного магнита лучше [magpylib](magpylib.md) и [pyvista](pyvista.md).

Что умеет для объясняющего видео:

- Простые объекты (шар, ящик, стрелка, спираль, кривая, график), готовое освещение, мышью можно вращать и приближать камеру. Движение задаётся циклом с численным интегрированием: физику пишете вы.
- Живая демонстрация: сцену можно управлять мышью и клавишами прямо во время записи экрана. Рисование «вживую» — шарик оставляет след (кривая).
- Движение камеры: вручную мышью или кодом (свойства сцены). Плавных переходов между сценами нет.
- Стилистика: простые гладкие геометрические тела, цвета по умолчанию «школьные».
- Сохранение: кадр в PNG (`scene.capture("имя")`, файл идёт в папку загрузок браузера). Видео встроенной функции нет, только запись экрана, например OBS Studio, см. [obs-studio](obs-studio.md).
- Голос: нет.

## Слабые стороны

- Нет экспорта видео. Запись экрана в реальном времени даёт нестабильную частоту кадров. `scene.capture` сохраняет одиночные PNG в папку загрузок браузера.
- Графическое качество невысокое. Это учебный инструмент, не рендер.
- Web VPython: чтобы сохранять программы на сайте, нужна учётная запись. Мы вход не использовали.
- Пакет `vpython` на PyPI: последний стабильный релиз 7.6.5 от 2024-03-26. Актуальная версия 7.6.6.dev0 от 2026-08-15 помечена как экспериментальная (для Pyodide).
- В блокноте Jupyter перезапуск программы требует перезапуска ядра или `scene = canvas()` в начале (README).

## Сложность

- Для человека (1 из 5): работает за час, без знаний графики. Это самый короткий путь к 3D-анимации.
- Для агента (3 из 5): код пишет сам, но запуск идёт в браузере с WebGL. Вывод картинок и видео требует автоматизации браузера и записи экрана.

## Автоматизация и воспроизводимость

- Автоматизация (2 из 5): код в Python или JavaScript, но выполнение в браузере, нет командной строки для рендера и нет записи видео.
- Воспроизводимость (2 из 5): код под git, но результат — живая сцена в реальном времени, кадры зависят от скорости машины.

## Платформа и оборудование

Web VPython — любой современный браузер с WebGL и видеокартой. Пакет `vpython` — Python 3.7+ на Linux, macOS, Windows (по данным PyPI).

## Экспорт

PNG-снимок холста (`scene.capture`, имя файла и счётчик), экспорт программы на свою веб-страницу (в README GlowScript). Видео — только запись экрана.

## Стоимость

Проверено 2026-10-14. Бесплатно. На glowscript.org программы хранятся в облаке бесплатно (по тексту сайта).

## Лицензия и права

- Код или программа: MIT (vpython-jupyter, Copyright 2015 Coady, Chabay, Sherwood; glowscript, Copyright 2011 Scherer, Sherwood).
- Результат: MIT не накладывает условий на картинки и ролики.
- Ассеты в комплекте: ассетов нет. Примеры с glowscript.org принадлежат авторам, лицензия каждой программы не проверялась.

## Активность и зрелость

<!-- gh-stats:vpython/vpython-jupyter -->
- Звёзды GitHub: 166
- Последний коммит в основной ветке: 2026-08-16
- Последний релиз или тег: v7.6.6.dev0 (2026-08-15)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория vpython/vpython-jupyter, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: declining. Стабильный релиз 7.6.5 вышел в марте 2024, с тех пор вышла только dev-сборка 7.6.6.dev0 (август 2026, «Pyodide pure-wheel pin (experimental)»). Репозиторий glowscript получал коммиты в августе 2026. Разработка идёт, но редко. Авторы по README — John Coady, Ruth Chabay, Matt Craig и Bruce Sherwood; разработку частично поддерживал грант NSF (сайт vpython.org).

## Когда брать и когда нет

- Брать: быстрые учебные демонстрации в браузере, показать ученикам, как устроено движение по закону Ньютона, и записать экран.
- Не брать: нужны красивый рендер, воспроизводимое видео, точная физика поля. Тогда [pyvista](pyvista.md), [matplotlib](matplotlib.md) или [blender](blender.md).

## Источники

- [vpython.org](https://vpython.org/) — назначение, Web VPython (раньше GlowScript VPython). Проверено 2026-10-14.
- [glowscript.org](https://www.glowscript.org/) — Web VPython, версия 3.2, вход для хранения. Проверено 2026-10-14.
- [VPython: canvas, Screen Capture](https://www.glowscript.org/docs/VPythonDocs/canvas.html) — `scene.capture`. Проверено 2026-10-14.
- [vpython-jupyter, README](https://github.com/vpython/vpython-jupyter) — работа в браузере и Jupyter. Проверено 2026-10-14.
- [vpython на PyPI](https://pypi.org/pypi/vpython/json) — 7.6.5 от 2024-03-26, 7.6.6.dev0 от 2026-08-15. Проверено 2026-10-14.
- [Релизы vpython-jupyter](https://github.com/vpython/vpython-jupyter/releases.atom) — 7.6.6.dev0 «Pyodide pure-wheel pin (experimental)». Проверено 2026-10-14.
- [Лицензия vpython-jupyter](https://raw.githubusercontent.com/vpython/vpython-jupyter/master/LICENSE.txt) — MIT. Проверено 2026-10-14.
- [GlowScript README](https://github.com/vpython/glowscript) — описание, экспорт на свою страницу. Проверено 2026-10-14.

## Неизвестно

- Есть ли в GlowScript встроенная запись видео: в проверенной документации canvas есть только `scene.capture` для PNG.
- Условия использования программ-примеров на glowscript.org: не нашли.
- Возможность автоматического запуска без экрана: не проверялась.
- Лицензия glowscript проверена по файлу LICENSE репозитория, что именно входит в сторонние библиотеки внутри — нет.
