---
id: paraview
name: ParaView
class: [simulation]
kind: app
site: https://www.paraview.org/
github: Kitware/ParaView
scenes: [field, simulation, micro]
quality: 3
human_difficulty: 3
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: standard
platforms: [linux, macos, windows]
export: [png-sequence, avi, mp4, ogv, pvd, vtk]
code_license: BSD-3-Clause
price: бесплатно
checked: 2026-10-14
---

# ParaView

Открытое приложение Kitware для анализа и визуализации научных данных на движке VTK. Читает результаты почти любого расчётного кода, строит срезы, изоповерхности, линии тока, стрелки и анимирует их по времени и камере. Можно работать мышью или скриптами `pvpython` и `pvbatch`.

## Ссылки

- Официальный сайт: <https://www.paraview.org/>
- GitHub: <https://github.com/Kitware/ParaView> (зеркало: основной репозиторий и трекер на [GitLab Kitware](https://gitlab.kitware.com/paraview/paraview)).
- Документация: <https://docs.paraview.org/en/latest/>
- Python API: <https://www.paraview.org/paraview-docs/latest/python/paraview.simple.html>
- Примеры, проверенные 2026-10-14:
  - [Visualizing Magnetic Field Lines (Streamlines) in ParaView](https://www.youtube.com/watch?v=44zhhQCjfUg) — выбор векторного поля, затравочные линии и облако точек, линии магнитного поля. Канал TRAFOLO, около 4 минут.
  - [[Paraview Tutorial 5] Vector Visualization and Streamlines](https://www.youtube.com/watch?v=1jml3j3BmUg) — фильтр Stream Tracer, настройка линий.
  - [[Paraview Tutorial 10] Property Animation and Camera Orbiting](https://www.youtube.com/watch?v=sLAMXfkJk7U) — ключевые кадры свойств и облёт камеры.
  - [ParaView/OpenFOAM tutorial: Create animated streamlines with StreamlinesRepresentation](https://www.youtube.com/watch?v=LHhd_NHMt4M) — анимированные линии тока, плагин StreamlinesRepresentation.
  - [[Radia/Python/PyVISTA] 3D magnetic field visualization from Radia Python by PyVISTA and ParaView](https://www.youtube.com/watch?v=_gQ6Rq8Thuc) — 3D-поле многополюсного вигглера (чередующиеся полюса) из Radia, показано в ParaView.

## Что реально получается

Сквозной пример (магнит на холодильнике). Поле считает другой инструмент: [elmer-fem](elmer-fem.md) (выход VTU, рекомендованный формат для ParaView), [magpylib](magpylib.md) через [pyvista](pyvista.md) (сетка сохраняется в VTK), COMSOL после экспорта данных. В ParaView: карта модуля поля на срезе, линии поля фильтром Stream Tracer, стрелки Glyph, цветовая шкала. Затравка линий — линия или облако точек. Выход фильтра — полилинии, их можно сделать трубками.

Что даёт для видео:

- Анимация по времени и по ключевым кадрам: свойства фильтров и камера интерполируются, есть облёт камеры и движение по пути («Follow path»). Движение камеры по сцене — самая сильная сторона.
- Скриптование: `SaveAnimation` сохраняет кадры (png, jpg, tif, bmp, ppm) или видео. По документации форматы avi, mp4, ogv зависят от платформы и сборки. Надёжный путь: PNG-последовательность и FFmpeg, см. [ffmpeg](ffmpeg.md).
- Запись трассировки: действия в интерфейсе записываются в Python-скрипт (Trace Recorder), его правит агент. Состояние сцены сохраняется в файл состояния.
- Плавное «выращивание» линий поля: по документации и роликам есть анимация потока вдоль линий (StreamlinesRepresentation, StreakLine). В магнитных примерах не показана.
- Морфинг объектов и текст: нет. Заголовки и пояснения накладываются в монтаже.
- Голос: нет, время кадра задаётся скриптом.

## Слабые стороны

- Вид «научный» по умолчанию. Для ролика нужно настраивать свет, шрифты, фон, толщину линий.
- Формат видео зависит от сборки. В результатах поиска попадались обсуждения на форуме Kitware о том, что mp4 из `pvbatch` на Linux не пишется (страницы не открывались, источник вторичный). Лучше сразу брать PNG.
- Интерфейс сложный, фильтров очень много.
- Для чистого рендера без окна нужна сборка с поддержкой безголового режима (EGL или OSMesa). Готовы ли официальные бинарные пакеты — не проверялось.
- Прозрачный фон: `SaveScreenshot` поддерживает `TransparentBackground`, для видео с альфой нужны PNG и свой монтаж.

## Сложность

- Для человека (3 из 5): базовая работа осваивается за день-два, но качественная сцена с линиями поля и камерой требует недель. Ролики-уроки есть.
- Для агента (2 из 5): Python-скрипт целиком описывает сцену. Трудность — окружение для безголового рендера и подбор вида. Первая настройка сцены удобнее в интерфейсе, потом скрипт.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): `pvpython`, `pvbatch`, `paraview.simple`, пакетный рендер, Catalyst для расчётов. Есть сервер Trame для веб-интерфейса.
- Воспроизводимость (4 из 5): Python-скрипт и файл состояния (`.pvsm`, текст) хранятся в git. Пиксели зависят от версии VTK и драйвера, поэтому не 5.

## Платформа и оборудование

Linux, macOS, Windows. Бинарные сборки версии 6.2.0 лежат на [paraview.org/files](https://www.paraview.org/files/v6.2/): Linux (MPI, Python 3.12), Windows (MSI и ZIP), macOS (Intel и Apple silicon). Нужна видеокарта с OpenGL, большие данные требуют памяти. Есть распределённый режим на кластере.

## Экспорт

PNG, JPG, TIF, BMP, PPM; avi, mp4, ogv по сборке; прозрачность через `TransparentBackground`. Для передачи сцены в другие программы: PVD с геометрией анимации (`WriteAnimationGeometry`), экспорт сцены. Разрешение задаётся `ImageResolution`, 4K возможен.

## Стоимость

Проверено 2026-10-14. Бесплатно. Коммерческая поддержка и обучение продаёт Kitware отдельно, цены на сайте не искали.

## Лицензия и права

- Код или программа: BSD-3-Clause ([README](https://github.com/Kitware/ParaView), файл Copyright.txt).
- Результат: BSD не накладывает условий на картинки и ролики.
- Ассеты в комплекте: примеры данных, отдельные условия не проверялись.

## Активность и зрелость

<!-- gh-stats:Kitware/ParaView -->
- Звёзды GitHub: 1 712
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v6.2.0 (2026-09-29)
- Лицензия по данным GitHub: BSD-3-Clause
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория Kitware/ParaView, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: standard. Версия 6.2.0 вышла 2026-09-29, перед ней 6.1.0 в марте и 6.1.1 в мае 2026. Первая публичная версия датируется 2002 годом, развивают Kitware и государственные лаборатории США.

## Когда брать и когда нет

- Брать: надо облететь камерой 3D-поле, показать линии поля магнита в объёме, обработать результаты Elmer, OpenFOAM и других кодов.
- Не брать: 2D-график или схему проще в [matplotlib](matplotlib.md). Для кинематографичного света и материалов — Blender, см. [blender](blender.md).

## Источники

- [ParaView на GitHub](https://github.com/Kitware/ParaView) — зеркало, лицензия BSD-3-Clause, история с 2002 года. Проверено 2026-10-14.
- [Python API: SaveAnimation](https://www.paraview.org/paraview-docs/latest/python/paraview.simple.__init__.html) — форматы avi, mp4, ogv зависят от платформы и сборки, параметры FrameRate. Проверено 2026-10-14.
- [Руководство пользователя: Animation](https://docs.paraview.org/en/latest/UsersGuide/animation.html) — ключевые кадры, камера, путь. Проверено 2026-10-14.
- [Руководство пользователя: Saving Results](https://docs.paraview.org/en/latest/UsersGuide/savingResults.html) — скриншоты, анимация, состояние. Проверено 2026-10-14.
- [Каталог загрузок, v6.2](https://www.paraview.org/files/v6.2/) — сборки 6.2.0, дата 2026-09-29. Проверено 2026-10-14.
- [Релиз v6.2.0 на GitHub](https://github.com/Kitware/ParaView/releases/tag/v6.2.0) — дата релиза. Проверено 2026-10-14.
- [Elmer Models Manual](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerModelsManual.pdf) — VTU как рекомендуемый формат для ParaView. Проверено 2026-10-14.

## Неизвестно

- Поддерживают ли официальные бинарные сборки 6.2 безголовый рендер без X-сервера: страницу документации об этом не нашли.
- Умеет ли готовая сборка Linux писать mp4: по документации «зависит от сборки», запуском не проверено.
- Цены на поддержку Kitware: не искали.
- Проверенных коротких роликов, где линии магнитного поля растут анимацией в ParaView, не найдено: ролик TRAFOLO показывает настройку линий, а не рост.
