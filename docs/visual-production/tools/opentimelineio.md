---
id: opentimelineio
name: OpenTimelineIO (OTIO)
class: [edit-composite, hybrid]
kind: library
site: https://opentimelineio.readthedocs.io/
github: AcademySoftwareFoundation/OpenTimelineIO
scenes: [real-footage]
quality: 3
human_difficulty: 3
agent_difficulty: 1
automation: 5
reproducibility: 5
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [otio, edl, fcpxml, aaf]
code_license: Apache-2.0
price: бесплатно
checked: 2026-10-14
---

# OpenTimelineIO (OTIO)

Открытый формат и библиотека (C++ и Python) для обмена монтажным таймлайном: порядок и длина фрагментов, ссылки на файлы, дорожки, переходы, маркеры. Видео внутри не хранит. Создан в Pixar, с 2019 года проект Academy Software Foundation (ASWF). Для библиотеки графики полезен как связка «агент собирает таймлайн кодом — человек доводит в редакторе» и обратно.

## Ссылки

- Документация: https://opentimelineio.readthedocs.io/ (сайт opentimeline.io перенаправляет на GitHub)
- GitHub: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- Адаптеры: https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html
- Организация адаптеров: https://github.com/OpenTimelineIO
- Список инструментов, которые используют OTIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO/wiki/Tools-and-Projects-Using-OpenTimelineIO
- Примеры, проверенные 2026-10-14 (страницы открывались):
  - [Conform New Renders Into The Cut](https://opentimelineio.readthedocs.io/en/latest/use-cases/conform-new-renders-into-cut.html) — сценарий: монтажёр выдаёт EDL и QuickTime, художник переводит EDL в OTIO и подменяет фрагменты своими свежими рендерами. Статус: «Done», в работе на нескольких киностудиях.
  - [otiotool Tutorial](https://opentimelineio.readthedocs.io/en/latest/tutorials/otiotool.html) — командная утилита: отчёты по клипам и дорожкам, объединение и правка `.otio`.
  - [Feature Matrix](https://opentimelineio.readthedocs.io/en/latest/tutorials/feature-matrix.html) — какие возможности переносит каждый адаптер.

## Что реально получается

OTIO не рисует и не рендерит. Он решает одну задачу: переносить решения монтажа между программами и кодом.

- Агент или скрипт собирает `.otio` из готовых рендеров сцен и озвучки (порядок, длительности, переходы, маркеры), человек открывает файл в редакторе и правит.
- Обратный путь: смонтированный человеком таймлайн читается кодом, из него получаются новые длины сцен, и сцены рендерятся заново под монтаж. В документации это прямо сценарий «Animation Shot Frame Ranges Changed» (изменились диапазоны кадров анимации).
- Файл можно хранить в git и сравнивать: JSON-текст.
- Связка с озвучкой: метки слов из [whisperx](whisperx.md) можно превратить в маркеры и разрезы таймлайна, смотрите также [auto-editor](auto-editor.md).

Для научно-популярного ролика с графикой поверх голоса: нарезать склейку не вручную, а скриптом из сценария и меток времени, затем проверить в редакторе. Переносится структура монтажа, не графика.

## Слабые стороны

- Нет эффектов, цветокоррекции и титров как анимации. По Feature Matrix «Audio/Video Effects» не поддерживает даже ядро OTIO, «Fancy Speed Effects» (кривые скорости) не поддерживает никто, линейное изменение скорости есть не везде. Анимацию из After Effects или Motion через OTIO не перенести.
- Поддержка редакторами неодинаковая: переход, вложенность и несколько видеодорожек зависят от формата. Например, EDL не держит несколько видеодорожек и вложенность, FCP7 XML и FCP X — переходы.
- Адаптеры обновляет сообщество, уровень поддержки разный. Начиная с версии после 0.16 основной пакет PyPI содержит только ядро и свои форматы, а AAF, EDL, FCP XML и другие надо ставить из пакета `OpenTimelineIO-Plugins`.
- Последний релиз на PyPI 0.18.1 от 2025-11-09, версия в документации 0.19.0.dev1. Между релизами почти год.
- Это формат, а не редактор. Для просмотра есть встроенный простейший просмотрщик, не пригодный для готового ролика.

## Сложность

- Для человека (3 из 5): нужно понимать устройство таймлайна (дорожки, диапазоны времени, ссылки на медиа) и работать на Python или в командной строке. Для простой конвертации EDL в OTIO хватает одной команды.
- Для агента (1 из 5): текстовый JSON, Python-API, `otiotool` и другие утилиты командной строки. Агент собирает, читает и проверяет таймлайн сам. Руки нужны, чтобы открыть результат в редакторе.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): Python и C++ API, утилиты командной строки, плагины (адаптеры, привязка медиа, скрипты хуков).
- Воспроизводимость (5 из 5): файл `.otio` — текст, один и тот же вход даёт один и тот же файл. Версии схем (ядро и адаптеры) стоит фиксировать, схемы версионируются.

## Платформа и оборудование

Python 3.9 и новее по README, ядро на C++. Linux, macOS, Windows. Установка `pip install opentimelineio` (ядро) и `pip install OpenTimelineIO-Plugins` (адаптеры). Видеокарта не нужна.

## Экспорт

- Собственные форматы: `.otio` (JSON), `.otiod` (папка с медиа), `.otioz` (zip с медиа).
- Встроенные адаптеры пакета с адаптерами: AAF, ALE, burnins, cmx_3600 (EDL), fcp_xml (Final Cut Pro 7), maya_sequencer, svg, xges (GStreamer Editing Services). Дополнительно в списке документации: kdenlive, fcpx_xml, hls_playlist.
- Медиа OTIO не содержит: хранит только ссылки на файлы.

## Стоимость

Проверено 2026-10-14 по [README](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) и [LICENSE](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/LICENSE.txt). Бесплатно, открытый код.

## Лицензия и права

- Код или программа: Apache-2.0.
- Результат: файл таймлайна не содержит медиа. Права на ролик определяют права на исходные кадры, звук и программу, из которой он выгружен.
- Ассеты в комплекте: нет.

## Кто поддерживает

По README: «нативно поддерживается в большинстве нелинейных редакторов». Список с вики проекта (заявлен сообществом, у вендоров не проверял):

- DaVinci Resolve: с версии 18 импорт и экспорт OTIO и OTIOZ, в бесплатной и платной версиях (см. [davinci-resolve](davinci-resolve.md)).
- Kdenlive: по вики с версии 20.04, в карточке [kdenlive](kdenlive.md) указан импорт и экспорт OTIO с 25.04.
- Adobe Premiere Pro: импорт и экспорт таймлайна в бете, см. [premiere-pro](premiere-pro.md).
- Avid Media Composer: экспорт таймлайна, предпросмотр.
- Olive: импорт и экспорт.
- Nuke Studio, Hiero, RV и OpenRV, mrViewer, ftrack cineSync Play, Cezanne: просмотр и разрезка.
- Дополнения: Blender VSE IO и Ubisoft Shot Manager для Blender, плагин для Unreal Engine (соответствие таймлайна и последовательности уровня), экспорт Movie Render Queue для Unreal, плагин для Maya.
- Final Cut Pro: через адаптер `fcpx_xml`, см. [final-cut-pro](final-cut-pro.md).
- Для работы с агентом: в списке есть проект proofcut (MCP-сервер, агент режет таймлайн OTIO по расшифровке и проверяет рендер) — описание из вики, я его не проверял.

## Активность и зрелость

<!-- gh-stats:AcademySoftwareFoundation/OpenTimelineIO -->
- Звёзды GitHub: 2 020
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.18.1 (2025-11-09)
- Лицензия по данным GitHub: Apache-2.0
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория AcademySoftwareFoundation/OpenTimelineIO, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. README называет проект зрелым, API стабильным, но развивающимся. ASWF принял проект 2019-07-29 (на тот момент стадия incubation). PyPI: 0.18.1 от 2025-11-09. Лента релизов GitHub отстаёт от PyPI (последний тег в ленте 18.1 от 2025-11-07).

## Когда брать и когда нет

- Брать: агент собирает монтаж кодом и передаёт человеку в Resolve, Kdenlive или Premiere; обмен между редакторами; автосборка по расшифровке голоса; правка длин сцен после монтажа.
- Не брать: если нужен перенос эффектов и анимированной графики между программами; если монтаж идёт целиком в одном месте (скрипт [ffmpeg](ffmpeg.md) или [moviepy](moviepy.md) проще); если важен сам рендер, а не обмен.

## Источники

- [README OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) — назначение, статус, адаптеры, версии Python. Проверено 2026-10-14.
- [LICENSE.txt](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/blob/main/LICENSE.txt) — Apache 2.0. Проверено 2026-10-14.
- [Adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html) — встроенные и дополнительные адаптеры. Проверено 2026-10-14.
- [Feature Matrix](https://opentimelineio.readthedocs.io/en/latest/tutorials/feature-matrix.html) — что переносит каждый адаптер. Проверено 2026-10-14.
- [Tools and Projects Using OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO/wiki/Tools-and-Projects-Using-OpenTimelineIO) — кто поддерживает (вики проекта, самозаявление). Проверено 2026-10-14.
- [OpenTimelineIO Joins ASWF](https://www.aswf.io/news/opentimelineio-joins-aswf/) — принятие проекта 2019-07-29, Pixar. Проверено 2026-10-14.
- [OpenTimelineIO на PyPI](https://pypi.org/project/OpenTimelineIO/) и [OpenTimelineIO-Plugins](https://pypi.org/project/OpenTimelineIO-Plugins/) — версия 0.18.1, 2025-11-09. Проверено 2026-10-14.
- [Conform New Renders Into The Cut](https://opentimelineio.readthedocs.io/en/latest/use-cases/conform-new-renders-into-cut.html) и [otiotool](https://opentimelineio.readthedocs.io/en/latest/tutorials/otiotool.html) — сценарий и утилита. Проверено 2026-10-14.

## Неизвестно

- Поддержка OTIO в Resolve, Premiere, Avid по сайтам вендоров: взята из вики проекта (самозаявление), страницы вендоров не проверял.
- Текущая стадия проекта в ASWF (инкубация или зрелый): страница проекта на aswf.io не показала.
- Какие именно адаптеры и версии работают с Resolve 20 и новее: не проверял.
- Когда выйдет 0.19: версия числится как dev в документации, даты нет.
