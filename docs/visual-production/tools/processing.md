---
id: processing
name: Processing
class: [procedural]
kind: app
site: https://processing.org
github: processing/processing4
scenes: [graph, field, simulation, drawing]
quality: 3
human_difficulty: 2
agent_difficulty: 2
automation: 4
reproducibility: 4
cost: 0
maturity: stable
platforms: [windows, macos, linux]
export: [png-sequence, mp4, gif, svg, pdf]
code_license: GPL-2.0 (редактор), LGPL (библиотека core)
price: бесплатно
checked: 2026-10-14
---

# Processing

Настольная среда творческого кодинга: язык на основе Java, редактор (PDE) и библиотека рисования. Принципы Processing перенесены в веб в [p5js](p5js.md). Рисует в 2D и 3D, экспортирует кадры, SVG и PDF. Надёжнее веб-вариантов для офлайн-вывода, потому что каждый вызов `draw()` даёт ровно один кадр.

## Ссылки

- Официальный сайт: https://processing.org
- GitHub: https://github.com/processing/processing4
- Документация: https://processing.org/reference и https://processing.org/tutorials
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел):
  - [Примеры Processing](https://processing.org/examples) — официальная галерея скетчей с кодом.
  - [saveFrame()](https://processing.org/reference/saveFrame_.html) — запись нумерованных кадров; для видео отсылает к Movie Maker.
  - [Changes in 4.0](https://github.com/processing/processing4/wiki/Changes-in-4.0) — вики-страница об изменениях четвёртой версии, включая Movie Maker на основе ffmpeg.
  - [Movie Maker tool issues](https://discourse.processing.org/t/movie-maker-tool-issues/46767) — обсуждение проблем инструмента в версии 4.4.4 (форум сообщества).

## Что реально получается

- Графики, поля, частицы, симуляции, рисование линий, генеративные узоры. Сцены `graph`, `field`, `simulation`, `drawing`.
- Рендереры (справочник `size()`): по умолчанию Java2D (выше качество 2D, но медленнее для некоторых задач), P2D и P3D на OpenGL, FX2D на JavaFX, PDF и SVG прямо в файл. В выпуске 4.5.7 в заметках упомянут рендерер WebGPU.
- Непрерывность: пока скетч живёт, сцена течёт без склеек. Морфинг и камера делаются кодом; таймлайна нет.
- Типографика и голос: есть текст и звук в библиотеках; привязки к озвучке нет.
- Запись: `saveFrame()` — «saves a numbered sequence of images, one image each time the function is run», по умолчанию `screen-0000.tif`, имя можно задать шаблоном `####` (например `line-######.png`); форматы TIFF, TGA, JPEG, PNG. Для сборки видео справочник отсылает к инструменту Movie Maker. Основное окно сохраняется непрозрачным; для прозрачного фона нужен `createGraphics()`.
- Потолок качества (3 из 5): аккуратная учебная графика; стиль задаёт автор, готовых эффектов уровня студий нет.

## Слабые стороны

- Движение лучше привязывать к `frameCount`, а не к реальному времени, иначе видео зависит от скорости компьютера.
- Movie Maker больше не входит в состав: в 2025 году пользователи форума пишут, что он убран, ставится через Contribution Manager и в версии 4.4.4 на Windows падает при создании фильма из-за ffmpeg без расширения `.exe` (обходной путь: положить свой `ffmpeg.exe`). Один из участников отметил, что инструмент «работает с 4.3.4». Состояние в 4.5.7 не проверял.
- Нужна Java-среда и окно с графикой: для запуска на сервере нужен виртуальный дисплей. Режим безголового запуска в проверенной документации не описан.
- В основной ветке готовится версия Processing 5; в 4.x принимаются только исправления.

## Сложность

- Для человека (2 из 5): простой язык, десятки примеров. Первая анимация за день, хорошая подача — недели.
- Для агента (2 из 5): код целиком, запуск из командной строки (`processing cli` с версии 4.4.3: «removes the need to distribute multiple binaries or scripts»), кадры падают на диск и просматриваются. Руки нужны для оценки вкуса и установки.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): запуск скетча без IDE, `saveFrame()` в `draw()`, склейка кадров через [ffmpeg](ffmpeg.md). Общую схему покадровой записи сравнивает обзор [Процедурная графика](../classes/09-procedural.md).
- Воспроизводимость (4 из 5): проект — текст под git, один вызов `draw()` даёт один кадр независимо от скорости. Случайность нужно фиксировать (`randomSeed`). Различия JVM и драйверов GPU возможны.

## Платформа и оборудование

macOS, Windows, Linux, а также Raspberry Pi (страница загрузки). Для P2D и P3D нужна видеокарта с OpenGL.

## Экспорт

- Кадры: TIFF, TGA, JPEG, PNG через `saveFrame()`. Векторы: SVG и PDF (библиотеки). Видео и GIF: инструмент Movie Maker на основе ffmpeg («animated GIFs as well as high-resolution lossless MPEG videos», вики 4.0) или внешний ffmpeg.
- Разрешение и частота кадров задаются скетчем. Прозрачность: только через `createGraphics()`.

## Стоимость

Проверено 2026-10-14 по [странице загрузки](https://processing.org/download). Бесплатно.

## Лицензия и права

- Код или программа: GPL v2 для частей, написанных проектом; библиотека core — LGPL (файл LICENSE.md репозитория).
- Результат: ограничений на ролики в тексте лицензий нет. Официальный FAQ о коммерческом использовании в проверенных источниках не прочёл (через поиск видна только зеркальная копия и форум).
- Ассеты в комплекте: примеры в поставке; их условия не проверял.

## Активность и зрелость

<!-- gh-stats:processing/processing4 -->
- Звёзды GitHub: 515
- Последний коммит в основной ветке: 2026-09-25
- Последний релиз или тег: processing-1435-4.5.7 (2026-09-24)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория processing/processing4, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Текущий выпуск — Processing 4.5.7 (2026-09-24, помечен Latest), перед ним 4.5.7 RC1 (2026-09-18). Последний коммит — 2026-09-25. README: «Processing 5.0 development is underway on `main`»; исправления для четвёртой версии идут в ветку 4.x. Основатели Бен Фрай и Кейси Риз вели проект до 2023 года (README).

## Когда брать и когда нет

- Брать: надёжный офлайн-вывод кадров генеративной графики, схем и симуляций; команда, которой комфортнее Java, чем веб.
- Не брать: формулы и вывод выкладок ([manim-ce](manim-ce.md)), веб-интерактив ([p5js](p5js.md)), большие 3D-сцены ([blender](blender.md)), видеомонтаж.

## Источники

- [Репозиторий processing4](https://github.com/processing/processing4) — описание, примечание о Processing 5, ветка 4.x. Проверено 2026-10-14.
- [LICENSE.md](https://raw.githubusercontent.com/processing/processing4/main/LICENSE.md) — GPL v2, core под LGPL. Проверено 2026-10-14.
- [Страница загрузки](https://processing.org/download) — версия 4.5.7, macOS, Windows, Linux, Raspberry Pi. Проверено 2026-10-14.
- [Релизы](https://github.com/processing/processing4/releases) и [лента](https://github.com/processing/processing4/releases.atom) — 4.5.7, 2026-09-24. Проверено 2026-10-14.
- [saveFrame()](https://processing.org/reference/saveFrame_.html) — имя, форматы, прозрачность, Movie Maker. Проверено 2026-10-14.
- [size()](https://processing.org/reference/size_.html) — рендереры. Проверено 2026-10-14.
- [Changes in 4.0](https://github.com/processing/processing4/wiki/Changes-in-4.0) — Movie Maker. Проверено 2026-10-14.
- [Command line](https://github.com/processing/processing4/wiki/Command-Line) — `processing cli` с 4.4.3. Проверено 2026-10-14.
- [Форум: Movie Maker tool issues](https://discourse.processing.org/t/movie-maker-tool-issues/46767) и [How to export video on 4.4.1](https://discourse.processing.org/t/how-to-export-video-on-4-4-1/46324/8) — вторичные источники (сообщения пользователей). Проверено 2026-10-14.

## Неизвестно

- Входит ли Movie Maker в Processing 4.5.7 по умолчанию, работает ли он на Windows: данные только из форума за 2025 год.
- Безголовый запуск на сервере без дисплея: страницы командной строки слова «headless» не используют.
- Официальный FAQ о коммерческом использовании скетчей: не открылся, нашёл лишь пересказ форума.
- Состояние WebGPU-рендерера (экспериментальный или нет): упомянут только в заметках выпуска.
- Условия на примеры и библиотеки в поставке не проверял.
