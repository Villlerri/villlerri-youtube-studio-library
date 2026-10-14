---
id: blender
name: Blender
class: [3d, edit-composite]
kind: app
site: https://www.blender.org
github: blender/blender
scenes: [mechanism, scale, micro, simulation, character, field, drawing]
quality: 5
human_difficulty: 4
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: standard
platforms: [linux, macos, windows]
export: [mp4, mov, prores, png-sequence, exr-sequence]
code_license: GPL-2.0-or-later
price: бесплатно
checked: 2026-10-14
---

# Blender

Свободный пакет 3D: моделирование, анимация, рендер (Cycles и EEVEE), композитинг, видеомонтаж, 2D-рисование (Grease Pencil). Вся сцена и рендер управляются из Python и командной строки, поэтому это главный кандидат для сцен, которые агент строит кодом.

## Ссылки

- Официальный сайт: https://www.blender.org
- Код: основной репозиторий https://projects.blender.org/blender/blender (скриптом вернул 403, сам не открыл). На GitHub только зеркало: https://github.com/blender/blender, в описании «Official mirror of Blender», заголовок «mirrored from https://projects.blender.org/blender/blender.git».
- Руководство: https://docs.blender.org/manual/en/latest/
- Python API: https://docs.blender.org/api/current/
- Рендер из командной строки: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
- Модуль `bpy` на PyPI: https://pypi.org/project/bpy/
- Примеры, проверенные 2026-10-14:
  - [Simulating Natural Selection (Primer, 2018)](https://www.youtube.com/watch?v=0ZGbIKd0XrM) — в описании «Made with Blender and python.». Симуляции с «блобами»; по описанию — Blender и Python.
  - [Simulating the Evolution of Aggression (Primer, 2019)](https://www.youtube.com/watch?v=YNMkADpvO4w) — в описании «Made with Blender and python.». Позже канал перешёл на Unity (2020–2023), затем на Godot (2024–2025), см. [unity](unity.md) и [godot](godot.md).
  - [SINGULARITY — Painterly Space Adventure (Blender Studio, 2026)](https://www.youtube.com/watch?v=l5OZu-IrXpw) — короткометражка, сделанная в Blender; живописный стиль. Показывает потолок качества.
  - [The Making of SINGULARITY](https://www.youtube.com/watch?v=6qKZw8oPoiE) — как устроен производственный процесс: логи, статьи, файлы проекта лежат в открытом доступе (studio.blender.org/projects/singularity).
  - [What's New in Blender 5.2 LTS (официальный обзор)](https://www.youtube.com/watch?v=g4OXlrxqIx0) — Geometry Nodes и физика с 02:35, Grease Pencil с 07:40, композитинг, секвенсор.
  - [SciExplorer: From Microscopy Data to Interactive Scientific Visualisation (BCON26)](https://www.youtube.com/watch?v=fQrxjh0jhZM) — научные данные микроскопии в Blender.

## Что реально получается

- Механизмы, макро- и микромиры, смена масштаба: единая 3D-сцена, одна непрерывная камера, объекты не «вырезаются» между кадрами. Это прямо отвечает задаче «без дёрганых переходов и повторов одного кадра».
- Морфинг: shape keys, модификаторы и [Geometry Nodes](blender-geometry-nodes.md) меняют форму объекта во времени. Одно тело переходит в другое без монтажной склейки.
- Камера: любые траектории, фокус, глубина резкости. Камеру можно вести по кривой и привязывать к объектам.
- Рисование линий: [Grease Pencil](blender-grease-pencil.md) даёт штрихи прямо в 3D-пространстве, модификатор Build «дорисовывает» линии по кадрам.
- Молекулы и научные данные: аддон [Molecular Nodes](molecular-nodes.md).
- Видео: встроенный секвенсор и композитор (в 5.0 композитор доступен как модификатор секвенсора). Для монтажа это может заменить внешний редактор на простых проектах.
- Голос (оценка): аудио добавляется в секвенсор. Тайминги озвучки агент переводит в кадры (секунды × fps) и расставляет ключи кодом. Готового «синхронизатора по тексту» нет. В 5.2 есть узел Sample Sound Frequencies для анимации от звука.
- Стиль: EEVEE — растеризация в реальном времени с теми же шейдерными узлами, что Cycles; Cycles — трассировка путей. По оценке, первый быстрее и годится для «плоской» учебной графики, второй для фотореализма.

## Слабые стороны

- Сложные органические модели и красивый свет за агента не делаются. По оценке, агент надёжен на геометрии из примитивов, кривых и узлов; остальное берётся из библиотек или делается человеком.
- Cycles без видеокарты, по общему опыту, медленный (оценка). Время рендера в этой проверке не измерялось, код не запускали.
- В руководстве по Python API сказано: модификаторы, типы объектов и шейдерные узлы расширяются только на C/C++, из Python их не создать. Интерфейс Python между мажорными версиями меняется (в заметках 5.0 есть раздел о несовместимых изменениях Python API), скрипты привязаны к версии.
- Модуль `bpy` с PyPI работает только с одной версией Python (3.13 для 5.2.2).
- Правки через GUI не воспроизводятся из текста: если часть сцены сделана руками, она живёт только в двоичном `.blend`.

## Сложность

- Для человека (4 из 5): интерфейс огромный, до уверенной работы недели–месяцы. Простые сцены по готовым рецептам собираются быстрее.
- Для агента (2 из 5): сцену целиком можно построить скриптом и отрендерить `blender -b`, кадры агент проверяет сам. Руки нужны для вкуса (композиция, свет, материалы) и сложного моделирования. Сторонние мосты MCP (например [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp), MIT, «not made by Blender») дают агенту живое управление запущенным Blender.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): `blender -b файл.blend -o путь/кадр_##### -F OPEN_EXR -a` рендерит анимацию без интерфейса; `-E CYCLES`, `-s`, `-e`, `-f` задают движок и кадры; `--python файл.py` и `--python-expr` запускают скрипты. Порядок аргументов важен: `-f` и `-a` ставят последними. Есть пакет `bpy` (PyPI, GPL-3.0, колёса для Linux x86-64, macOS ARM64, Windows x86-64 и ARM64), то есть Blender как библиотека Python.
- Воспроизводимость (4 из 5): сцена, целиком собранная скриптом, лежит в git как текст. Сам `.blend` двоичный. Cycles на GPU не обещает побитового совпадения кадров (оценка, не проверялась).

## Платформа и оборудование

Требования с [страницы](https://www.blender.org/download/requirements/): Windows 8.1 (рекомендуется 11), 4 ядра с SSE4.2, 8 ГБ ОЗУ (рекомендуется 32), видеокарта с 2 ГБ (рекомендуется 8), OpenGL 4.3 и Vulkan 1.3. NVIDIA от GeForce 900, AMD от GCN 4-го поколения, Intel от Kaby Lake. macOS: Blender 5.0 и новее работают только на Apple Silicon (macOS 13+); 4.5 LTS — последняя версия для Intel Mac. Linux: 64-бит, glibc 2.28+. Ускорение Cycles: NVIDIA CUDA и OptiX, AMD HIP, Intel oneAPI, Apple Metal.

## Экспорт

- Видео: кодеки H.264, H.265, AV1 и ProRes; 10 бит для H.264, H.265 и AV1 (по руководству).
- Кадры: последовательности изображений, в том числе многослойный OpenEXR. RGBA (с альфой) доступен не для всех форматов.
- Разрешение и частота кадров заданы сценой, ограничений бесплатной версии нет.

## Стоимость

Проверено 2026-10-14 по [странице лицензии](https://www.blender.org/about/license/). Бесплатно, без тарифов, без ограничений по доходу. Развитие идёт на пожертвования (Development Fund).

## Лицензия и права

- Код или программа: GNU GPL. Исходники «by default» под GPL версии 2 или новее; компоненты совместимы с GPL версии 3 или новее.
- Результат: на странице лицензии сказано: «What you create with Blender is your sole property». Это относится к картинкам, видео и самим `.blend`. Коммерческое использование и монетизация YouTube не ограничены, водяных знаков нет. Заголовок раздела: «Free to Sell Your Work».
- Ассеты в комплекте: условия встроенных ассетов (библиотека Essentials) на проверенных страницах не найдены. Открытые фильмы Blender Studio, в том числе [Singularity](https://studio.blender.org/projects/singularity/), выложены с ассетами «under a Creative Commons Attribution license» (нужно указание автора).

## Активность и зрелость

<!-- gh-stats:blender/blender -->
- Звёзды GitHub: 20 898
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v5.2.2 (2026-09-14)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория blender/blender, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `standard`. Версия на 2026-10-14: 5.2 LTS (вышла 2026-07-14), текущий патч 5.2.2 LTS (2026-09-15). Следующий выпуск 5.3 по странице загрузки ожидается 2026-11-10. График: «каждый релиз поддерживается до следующего, примерно каждые четыре месяца», раз в год выходит LTS с двумя годами поддержки (5.2 LTS — до июля 2028, 4.5 LTS — до июля 2027). Недавние релизы: 5.1 — 2026-03-17, 5.0 — 2025-11-18, 4.5 LTS — 2025-07-15, 4.4 — 2025-03-18, 4.3 — 2024-11-19. Развивают Blender Foundation и сообщество.

## Когда брать и когда нет

- Брать: единая непрерывная 3D-сцена, механизмы, смена масштаба, научная визуализация, рисование линий в 3D; когда агент должен строить и рендерить сцену кодом.
- Не брать: если нужна только плоская векторная анимация формул и графиков (проще [manim-ce](manim-ce.md) или [motion-canvas](motion-canvas.md)); если нет видеокарты и бюджета времени на рендер.

## Источники

- [Лицензия Blender](https://www.blender.org/about/license/) — GPL, «What you create with Blender is your sole property». Проверено 2026-10-14.
- [Загрузка](https://www.blender.org/download/) — 5.2.2 LTS от 2026-09-15, 5.3 ожидается 2026-11-10. Проверено 2026-10-14.
- [Релизы](https://www.blender.org/download/releases/) и [Release notes](https://developer.blender.org/docs/release_notes/) — даты, цикл и поддержка LTS. Проверено 2026-10-14.
- [Системные требования](https://www.blender.org/download/requirements/). Проверено 2026-10-14.
- [Рендер из командной строки](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html) и [аргументы](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html) — `-b`, `-a`, `-f`, `-E`, `--python`. Проверено 2026-10-14.
- [Python API: обзор](https://docs.blender.org/api/current/info_overview.html) и [Quickstart](https://docs.blender.org/api/current/info_quickstart.html) — возможности и пределы Python. Проверено 2026-10-14.
- [bpy на PyPI](https://pypi.org/project/bpy/) — 5.2.2, GPL-3.0, Python 3.13, платформы. Проверено 2026-10-14.
- [Возможности рендера](https://www.blender.org/features/rendering/) и [EEVEE в руководстве](https://docs.blender.org/manual/en/latest/render/eevee/index.html) — Cycles и EEVEE. Проверено 2026-10-14.
- [Параметры вывода](https://docs.blender.org/manual/en/latest/render/output/properties/output.html) — видеокодеки и RGBA. Проверено 2026-10-14.
- [Blender 5.2 LTS](https://www.blender.org/download/releases/5-2/) и [5.0](https://www.blender.org/download/releases/5-0/) — новые функции, Python API. Проверено 2026-10-14.
- [GitHub-зеркало](https://github.com/blender/blender) — «Official mirror of Blender». Проверено 2026-10-14.
- [Singularity на Blender Studio](https://studio.blender.org/projects/singularity/) — открытое содержимое, CC-BY. Проверено 2026-10-14.
- Описания роликов Primer на YouTube (ссылки выше), через oEmbed названия подтверждены. Проверено 2026-10-14.
- [blender-mcp](https://github.com/ahujasid/blender-mcp) — сторонний мост MCP. Проверено 2026-10-14.

## Неизвестно

- Условия встроенных ассетов (Essentials) не нашёл.
- Основной репозиторий projects.blender.org скриптом не открылся (403).
- Время рендера и побитовое совпадение кадров не проверялись: код не запускали.
- Какие инструменты использует Branch Education: в описаниях роликов и на branch.education не названы, поэтому канал не приписан Blender.
