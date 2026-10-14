---
id: three-js
name: Three.js
class: [web-graphics, 3d]
kind: library
site: https://threejs.org
github: mrdoob/three.js
scenes: [mechanism, scale, field, simulation]
quality: 4
human_difficulty: 3
agent_difficulty: 2
automation: 4
reproducibility: 4
cost: 0
maturity: standard
platforms: [web]
export: [html]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Three.js

Самая распространённая JavaScript-библиотека для 3D в браузере. Строит сцену из объектов, камер, света и материалов и рисует её через WebGL или WebGPU. Видео сама не пишет: кадры берёт внешний захват.

## Ссылки

- Официальный сайт: https://threejs.org
- GitHub: https://github.com/mrdoob/three.js
- Документация: https://threejs.org/docs/ и руководство https://threejs.org/manual/
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел; ролики проверены через oEmbed):
  - [Официальные примеры](https://threejs.org/examples/) — галерея сцен с кодом (в списке примеров 14 разделов, от WebGL и WebGPU до физики и аудио).
  - [webgl_morphtargets_horse](https://threejs.org/examples/#webgl_morphtargets_horse) — морфинг формы меша по целям (morph targets); имя примера есть в списке `examples/files.json`.
  - [webgl_animation_keyframes](https://threejs.org/examples/#webgl_animation_keyframes) — анимация модели по ключевым кадрам из файла glTF.
  - [bruno-simon.com](https://bruno-simon.com) — портфолио-игра на Three.js: машина едет по 3D-миру. Показывает, как держится большая непрерывная сцена в реальном времени.
  - [New car - New portfolio - Devlog 3](https://www.youtube.com/watch?v=5i_-p4ET2JE) — канал Bruno Simon; разбор модели машины, материалов и свечения (bloom) для этого портфолио.
  - [@remotion/three](https://www.remotion.dev/docs/three) — как вести Three.js покадрово из Remotion.

## Что реально получается

- Устройство предметов, масштаб, поля: 3D-модели (glTF и другие форматы), материалы PBR, тени, постобработка. Сцены `mechanism`, `scale`, `field`, `simulation`.
- Непрерывность сцены: один объект живёт в одной сцене, камера движется по пути без склеек. Это то, чего не хватало прошлым роликам: развитие сцены вместо смены кадров.
- Анимация: в ядре есть `AnimationMixer` с клипами и действиями (`AnimationClip`, `AnimationAction`). Сложные таймлайны делают через [gsap](gsap.md) или [theatre-js](theatre-js.md).
- Шейдеры: `WebGPURenderer` по умолчанию берёт бэкенд WebGPU и при его отсутствии переходит на WebGL 2. Для шейдеров рекомендован TSL; `ShaderMaterial` и `RawShaderMaterial` в этом рендерере не поддержаны (руководство по WebGPURenderer, по результатам поиска). Шейдеры Shadertoy переносятся отдельно, см. [glsl-shadertoy](glsl-shadertoy.md).
- Рисование линий и подписи: линии из геометрии, текст через дополнения. «Рисования вживую» как готового приёма нет.
- Голос: нет привязки к аудио в ядре. Синхронизация делается снаружи (например, покадровый рендер под озвучку).
- Потолок качества (4 из 5): физически корректные материалы и постобработка дают кадр на уровне хорошего научно-популярного 3D; планку ограничивает работа автора над моделями и светом, а не движок.

## Слабые стороны

- Нет собственного экспорта в видео. Запись в реальном времени даёт пропуски кадров при тяжёлой сцене; нужен детерминированный захват: [ccapture-js](ccapture-js.md), [remotion](remotion.md) и другие, сравнение в обзоре [SVG, Canvas, WebGL](../classes/03-web-graphics.md).
- В Remotion рендер Three.js работает не с рендерером OpenGL по умолчанию: документация рекомендует `angle` (настройка Chromium).
- Красивая сцена требует модели, света, материалов. Библиотека даёт конструктор, а не готовый стиль.
- Версии выходят ежемесячно (r186 в сентябре 2026), старые примеры из сети могут не запуститься на новых.
- Миграция на WebGPU ломает кастомные шейдеры (`onBeforeCompile`, `ShaderMaterial`).

## Сложность

- Для человека (3 из 5): нужны JavaScript и основы 3D: сцена, камера, материалы, координаты. Простая сцена за день, чистая подача с камерой и светом — недели.
- Для агента (2 из 5): код и браузер. Агент пишет сцену, снимает скриншоты headless-браузером и сам видит результат. Для GPU-эффектов в headless-режиме нужны настройки рендерера (в Remotion — `angle`). Руки нужны для моделей и вкуса.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): сцена — код, видео получают скриптом: Remotion (`@remotion/three`), Puppeteer-захват или CCapture. У самой библиотеки команды рендера нет.
- Воспроизводимость (4 из 5): проект — текст под git. Состояние кадра зависит только от времени, если движение берётся из `performance.now` или номера кадра, а не от накопленных шагов; CCapture держит такое время виртуальным. Различия драйверов GPU могут дать мелкие расхождения пикселей.

## Платформа и оборудование

Браузер на любой ОС, нужен WebGL 2 или WebGPU. Видеокарта желательна. Для серверного рендера нужен headless Chromium с поддержкой WebGL (в Remotion — флаг `gl: angle`).

## Экспорт

- Сама библиотека: HTML и JS-страница. Для видео внешний захват: MP4 или WebM (CCapture), покадровый рендер в видео (Remotion).
- Альфа-канал и разрешение определяются инструментом записи, а не Three.js.

## Стоимость

Проверено 2026-10-14 по [LICENSE](https://github.com/mrdoob/three.js/blob/dev/LICENSE). Бесплатно.

## Лицензия и права

- Код или программа: MIT («The MIT License, Copyright © 2010-2026 three.js authors»).
- Результат: лицензия MIT относится к коду. Ограничений на ролики, коммерцию и монетизацию в тексте нет.
- Ассеты в комплекте: примеры и модели в репозитории могут иметь свои условия; перед использованием каждого файла нужна отдельная проверка.

## Активность и зрелость

<!-- gh-stats:mrdoob/three.js -->
- Звёзды GitHub: 116 410
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: r186 (2026-09-24)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория mrdoob/three.js, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `standard`. Релизы идут примерно раз в месяц: r186 (2026-09-24), r185 и r184 (2026-09-04). Последний коммит в основной ветке — 2026-10-14. Ведёт сообщество вокруг автора mrdoob.

## Когда брать и когда нет

- Брать: 3D-сцены с непрерывной камерой, устройство механизмов, масштабные «от кухни до атома», если команда пишет JavaScript. Связка с покадровым рендером даёт плавные ролики без дёрганья.
- Не брать: формулы и графики (проще [manim-ce](manim-ce.md), [mathbox](mathbox.md), [d3](d3.md)), если нужен готовый редактор без кода (смотри [blender](blender.md) и [spline](spline.md)).

## Источники

- [Репозиторий three.js](https://github.com/mrdoob/three.js) — лицензия MIT, WebGL и WebGPU в сборках, SVG и CSS3D как дополнения. Проверено 2026-10-14.
- [LICENSE](https://github.com/mrdoob/three.js/blob/dev/LICENSE) — MIT, © 2010–2026. Проверено 2026-10-14.
- [Лента релизов](https://github.com/mrdoob/three.js/releases.atom) и [npm: three](https://registry.npmjs.org/three) — r186, 0.186.1, 2026-09-24. Проверено 2026-10-14.
- [Список примеров files.json](https://threejs.org/examples/files.json) — имена примеров (morphtargets, animation_keyframes, postprocessing). Проверено 2026-10-14.
- [WebGPURenderer](https://threejs.org/docs/pages/WebGPURenderer.html) — бэкенд WebGPU и запасной WebGL 2. Проверено 2026-10-14.
- [Документация: AnimationMixer](https://threejs.org/docs/pages/AnimationMixer.html) — проигрыватель анимации. Проверено 2026-10-14.
- [Remotion: @remotion/three](https://www.remotion.dev/docs/three) — `ThreeCanvas`, покадровая модель, рекомендация `angle`. Проверено 2026-10-14.
- [Bruno Simon: Devlog 3](https://www.youtube.com/watch?v=5i_-p4ET2JE) — ролик живой по oEmbed (название и канал совпали). Проверено 2026-10-14.

## Неизвестно

- Содержание руководства по WebGPURenderer (поддержка `ShaderMaterial`, TSL) взято из пересказа результатов поиска: страница руководства `manual/en/webgpurenderer.html` при проверке отвечала 404.
- Совместимость сторонних дополнений (MathBox, постобработка) с r186 не проверялась.
- Условия на модели и текстуры из примеров не изучал.
