---
id: babylonjs
name: Babylon.js
class: [web-graphics, 3d]
kind: framework
site: https://www.babylonjs.com
github: BabylonJS/Babylon.js
scenes: [mechanism, scale, simulation, micro]
quality: 4
human_difficulty: 3
agent_difficulty: 2
automation: 3
reproducibility: 4
cost: 0
maturity: stable
platforms: [web]
export: [webm, html]
code_license: Apache-2.0
price: бесплатно
checked: 2026-10-14
---

# Babylon.js

Открытый движок для 3D и рендеринга в браузере. Темы репозитория: webgl2, webgpu, webxr. Выделяется встроенной записью видео и набором инструментов: Playground, редактор материалов, инспектор.

## Ссылки

- Официальный сайт: https://www.babylonjs.com
- GitHub: https://github.com/BabylonJS/Babylon.js
- Документация: https://doc.babylonjs.com/
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел):
  - [Playground](https://playground.babylonjs.com) — онлайн-песочница с запускаемым кодом и общими ссылками.
  - [Витрина сообщества](https://www.babylonjs.com/community/) — проекты на Babylon.js.
  - [Запись в видео](https://doc.babylonjs.com/features/featuresDeepDive/scene/renderToVideo) — документация `VideoRecorder`.
  - [Тема форума: точный покадровый рендер](https://forum.babylonjs.com/t/exact-frame-rendering-of-an-animation-into-a-video/23955) — как делают воспроизводимое видео без пропусков.

## Что реально получается

- 3D-сцены: механизмы, масштабы, макро- и микромир, физика. Главная страница версии 9.0 называет Clustered Lighting, Textured Area Lights, Gaussian Splat, Frame Graph, Dynamic IBL Shadows, Physically Based Atmosphere, OpenPBR, 3D Tiles. Сцены `mechanism`, `scale`, `simulation`, `micro`.
- Инструменты: Playground, Node Material Editor (визуальный редактор шейдеров), Inspector, вкладка записи видео.
- Непрерывность: сцена живёт как одна среда, камера двигается по пути без склеек. Монтажной логики сцен в движке нет.
- Рисование линий, формулы, типографика: готовых приёмов нет, делается кодом.
- Голос: привязки к озвучке нет.
- Потолок качества (4 из 5): PBR-материалы и современные эффекты (см. список возможностей 9.0) дают убедительный реал-тайм кадр; предел задаёт работа автора и запись видео.

## Слабые стороны

- Встроенная запись `VideoRecorder` работает через `MediaRecorder` и `Canvas.captureStream()`: только WebM, формат MP4 и MOV напрямую не поддержан (документация). Запись идёт в реальном времени, на тяжёлой сцене возможны пропуски (отчёты пользователей на форуме). Для роликов нужен покадровый способ.
- Покадровый рендер: на форуме советуют режим `deterministicLockstep` с шагом 1 и вычисление времени по номеру шага, а не по `performance.now()`. Это приём из обсуждения, не из справочника.
- Объём API: цель — игры и общие 3D-приложения, а не объясняющая графика. Подача сцены требует ассетов и работы со светом.
- Мажорные версии вышли быстро (на 2026-10-14 — 9.30.0), примеры из сети старых версий нужно проверять.

## Сложность

- Для человека (3 из 5): JavaScript или TypeScript и основы 3D. Первая сцена за день, отполированная сцена с камерой и светом — недели.
- Для агента (2 из 5): код и браузер, результат проверяется скриншотами. Руки нужны для моделей и оценки внешнего вида.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): запись одной командой не предусмотрена. Реальное время — `VideoRecorder`; точные кадры — свой цикл, скриншоты или WebCodecs (варианты из ответов команды на форуме). Внешний захват: [ccapture-js](ccapture-js.md), [remotion](remotion.md). Сравнение — в обзоре [SVG, Canvas, WebGL](../classes/03-web-graphics.md).
- Воспроизводимость (4 из 5): проект — текст под git; режим `deterministicLockstep` делает движение зависимым от номера шага. Проверка запуском не проводилась.

## Платформа и оборудование

Браузер на любой ОС; WebGL, для WebGPU нужен браузер с его поддержкой. Видеокарта желательна.

## Экспорт

- Встроенно: WebM (`VideoRecorder`: по умолчанию 7 секунд, файл `babylonjs.webm`; `startRecording(fileName, seconds)`; если имя файла `null`, возвращается Blob).
- Скриншоты и кадры — через API движка; видео с точными кадрами — внешним конвейером.

## Стоимость

Проверено 2026-10-14 по [license.md](https://github.com/BabylonJS/Babylon.js/blob/master/license.md). Бесплатно.

## Лицензия и права

- Код или программа: Apache-2.0 (файл `license.md`, поле `license` в npm-пакете `@babylonjs/core`).
- Результат: лицензия Apache-2.0 относится к коду; ограничений на ролики, коммерцию и монетизацию в тексте нет.
- Ассеты в комплекте: модели и текстуры в Playground и примерах имеют собственные условия; не проверял.

## Активность и зрелость

<!-- gh-stats:BabylonJS/Babylon.js -->
- Звёзды GitHub: 26 165
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: 9.30.0 (2026-10-08)
- Лицензия по данным GitHub: Apache-2.0
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория BabylonJS/Babylon.js, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Релизы выходят еженедельно: 9.30.0 (2026-10-08), 9.29.0 (2026-10-01), 9.28.0 (2026-09-24). Последний коммит — 2026-10-14. Главная страница сайта озаглавлена «Welcome to Babylon.js 9.0».

## Когда брать и когда нет

- Брать: если команда уже работает на TypeScript и нужен целостный 3D-движок с инспектором, редактором шейдеров и записью. Подходит для механизмов и масштабных сцен.
- Не брать: когда нужна лёгкая библиотека ([three-js](three-js.md)), формулы ([manim-ce](manim-ce.md)), графики ([d3](d3.md)), либо готовый 3D-редактор без кода ([blender](blender.md)).

## Источники

- [Репозиторий](https://github.com/BabylonJS/Babylon.js) — Apache-2.0, описание «powerful, beautiful, simple, and open game and rendering engine». Проверено 2026-10-14.
- [license.md](https://raw.githubusercontent.com/BabylonJS/Babylon.js/master/license.md) — Apache License 2.0. Проверено 2026-10-14.
- [Главная страница сайта](https://www.babylonjs.com/) — версия 9.0, перечень возможностей, Playground, Node Material Editor. Проверено 2026-10-14.
- [Render to Video](https://doc.babylonjs.com/features/featuresDeepDive/scene/renderToVideo) — `VideoRecorder`, только WebM, поддержка MediaRecorder. Проверено 2026-10-14.
- [Форум: точный покадровый рендер](https://forum.babylonjs.com/t/exact-frame-rendering-of-an-animation-into-a-video/23955) — `deterministicLockstep`, скриншоты, WebCodecs. Проверено 2026-10-14.
- [Лента релизов](https://github.com/BabylonJS/Babylon.js/releases.atom) и [npm: @babylonjs/core](https://registry.npmjs.org/@babylonjs/core) — 9.30.0, 2026-10-08. Проверено 2026-10-14.

## Неизвестно

- Кто финансирует и ведёт проект: на проверенных страницах не указано.
- Фактическая частота кадров `VideoRecorder` и поведение на тяжёлых сценах: данные только из форума.
- Условия на модели из Playground и витрины не изучал.
