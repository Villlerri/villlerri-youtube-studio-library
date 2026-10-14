---
id: blender-geometry-nodes
name: Blender Geometry Nodes
class: [3d, procedural]
kind: method
site: https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html
github: none
scenes: [field, simulation, mechanism, micro]
quality: 5
human_difficulty: 4
agent_difficulty: 3
automation: 4
reproducibility: 3
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [mp4, png-sequence, exr-sequence]
code_license: GPL-2.0-or-later
price: бесплатно (часть Blender)
checked: 2026-10-14
---

# Blender Geometry Nodes

Процедурная система внутри [Blender](blender.md): геометрия сцены строится и меняется графом узлов. Подходит для полей, частиц, симуляций и анимации, которая считается, а не рисуется. Отдельной программы нет, код лежит в репозитории Blender.

## Ссылки

- Официальный сайт: https://www.blender.org (раздел руководства: https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html)
- GitHub: открытого отдельного репозитория нет; код входит в зеркало https://github.com/blender/blender (см. [blender](blender.md)).
- Документация: [введение](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/introduction.html), [поля](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html), [зона симуляции](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html)
- Примеры, проверенные 2026-10-14:
  - [Gizmos, For-Each Zone and more! NEW Geometry Nodes features — Blender 4.3](https://www.youtube.com/watch?v=Opzk1wUhzCw) — официальный разбор (технический художник Blender Studio) зоны For-Each и гизмо.
  - [What's New in Blender 5.2 LTS](https://www.youtube.com/watch?v=g4OXlrxqIx0) — узловая физика ткани и волос, анимация от звука (с 02:35).
  - [Audio Nodes: Live Sound, Living Geometry (BCON26)](https://www.youtube.com/watch?v=0wpz3oqb0YA) — аддон, превращающий звук в вход для узлов; пример связи геометрии со звуком.
  - [SINGULARITY, страница проекта](https://studio.blender.org/projects/singularity/) — команда Blender Studio расширила библиотеку Brushstroke Tools и применила Geometry Nodes для анимации поведения толпы.
  - [Electric Fields with Geometry Nodes in Blender 4.5 (BlenderNation, 2025-10-07)](https://www.blendernation.com/2025/10/07/turning-physics-into-art-electric-fields-with-geometry-nodes-in-blender-4-5/) — построение силовых линий: направление поля, трассировка линий, поток частиц.
  - [Magnetic Fields in Blender (BlenderNation, 2025-10-27)](https://www.blendernation.com/2025/10/27/magnetic-fields-in-blender-and-they-look-beautiful-detailed-tutorial/) — магнитное поле с нуля, физика объясняется по ходу; видео-ссылки на странице нет.
  - [Закон Био–Савара в Geometry Nodes (80.lv, 2023-07-07)](https://80.lv/articles/an-unusual-application-of-blender-s-geometry-nodes) — поле катушки в любой точке 3D, силовые линии обновляются при деформации катушки.

## Что реально получается

- Поля и линии поля (физические): граф считает вектор поля в точках и трассирует линии. Готовых примеров три (выше), у автора Sam Aldhaher есть платный набор [ElectroMag Nodes](https://blendermarket.com/products/electromag-nodes) (Blender Market, лицензия GPL; Lite и полная версии). Не путать с «полями» (fields) в терминологии Blender: это функции, которые считаются по каждому элементу.
- Симуляция: зона симуляции переносит результат кадра на следующий кадр. В руководстве: «even a set of simple rules can lead to complex results». Например частицы, рои, рост. В руководстве есть отдельный раздел Baking (запекание результата).
- Частицы и толпы: пример в проекте Singularity (поведение толпы).
- Непрерывность: симуляция продолжается на одной сцене и одной камере, можно переходить от макро к микро без склеек.
- Морфинг: геометрия вычисляется из параметров, значит плавно интерполируется любой параметр (число линий, радиус, шум).
- Типографика и формулы: не для этого; текст остаётся обычным объектом.

## Слабые стороны

- Граф узлов нужно читать и отлаживать глазами. Ошибка в одном узле часто выглядит как «ничего не появилось».
- Зона симуляции работает только в контексте модификатора, не в инструментах (по руководству).
- Физическая точность поля зависит от формулы, которую вводит автор. Графы из чужих уроков не гарантируют корректность.
- Новая узловая физика ткани и волос в 5.2 LTS на странице релиза описана как экспериментальная.

## Сложность

- Для человека (4 из 5): нужно мыслить полями и атрибутами. Первые результаты за недели, уверенная работа дольше.
- Для агента (3 из 5): узлы можно создавать из Python (в `bpy.types` есть классы `GeometryNode…`), но осмысленный граф агент собирает на ощупь. Сложные графы он проверяет только по рендеру. Часть работы остаётся за человеком: подобрать готовую группу узлов и настроить.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): граф создаётся и запускается из `bpy`, рендер идёт командной строкой (`blender -b`).
- Воспроизводимость (3 из 5): граф лежит в двоичном `.blend`. Если граф создан скриптом, его можно держать как текст. Запечённый кэш фиксирует результат симуляции.

## Платформа и оборудование

Как у [Blender](blender.md): Windows, macOS (Apple Silicon с 5.0), Linux. Тяжёлые симуляции нагружают процессор и ОЗУ.

## Экспорт

Тот же вывод, что у Blender: видео и последовательности кадров, в том числе EXR. В Geometry Nodes ничего не отдаётся отдельно, кроме запечённого кэша симуляции.

## Стоимость

Проверено 2026-10-14. Входит в [Blender](blender.md), бесплатно. Платные наборы узлов сторонних авторов продаются отдельно.

## Лицензия и права

- Код или программа: GPL (как Blender).
- Результат: принадлежит автору, ограничений на коммерческое использование нет (формулировка со страницы лицензии Blender, см. [blender](blender.md)).
- Ассеты в комплекте: сторонние наборы узлов имеют свои лицензии. Для ElectroMag Nodes на странице указана лицензия GPL.

## Активность и зрелость

Зрелость: `stable`. В руководстве есть разделы Simulation Nodes, Repeat Zone и For Each Geometry Element Zone. В 4.3 добавлены For-Each Zone и гизмо, в 5.0 — «bundles» (передача произвольных данных между узлами и объектами), в 5.2 LTS — Closure и Custom Effector, Mesh Bevel, Sample Sound Frequencies. Развивает команда Blender. Статистика репозитория см. в [blender](blender.md).

## Когда брать и когда нет

- Брать: силовые линии и потоки, рои и частицы, процедурный рост, всё, что считается по правилам и должно плавно меняться без склеек.
- Не брать: быстрая плоская графика; точные научные расчёты (граф рисует, но не заменяет решатель — тогда [pyvista](pyvista.md) или специализированные пакеты).

## Источники

- [Введение в Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/introduction.html) — система для изменения геометрии узлами. Проверено 2026-10-14.
- [Поля](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html) — определение поля как функции; пунктир для полевых соединений. Проверено 2026-10-14.
- [Зона симуляции](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html) — результат кадра влияет на следующий; только контекст модификатора. Проверено 2026-10-14.
- [Blender 5.2 LTS](https://www.blender.org/download/releases/5-2/) — звук, Mesh Bevel, физика, Closure. Проверено 2026-10-14.
- [Blender 5.0](https://www.blender.org/download/releases/5-0/) — bundles. Проверено 2026-10-14.
- [Blender 4.3](https://www.blender.org/download/releases/4-3/) — Grease Pencil и Geometry Nodes. Проверено 2026-10-14.
- [Python API: типы узлов](https://docs.blender.org/api/current/info_quickstart.html) — в оглавлении `bpy.types` есть классы `GeometryNode…`. Проверено 2026-10-14.
- [BlenderNation, электрические поля](https://www.blendernation.com/2025/10/07/turning-physics-into-art-electric-fields-with-geometry-nodes-in-blender-4-5/), [магнитные поля](https://www.blendernation.com/2025/10/27/magnetic-fields-in-blender-and-they-look-beautiful-detailed-tutorial/). Проверено 2026-10-14.
- [80.lv](https://80.lv/articles/an-unusual-application-of-blender-s-geometry-nodes) — Био–Савар. Проверено 2026-10-14.
- [ElectroMag Nodes](https://blendermarket.com/products/electromag-nodes) — платный набор узлов, лицензия GPL. Проверено 2026-10-14.
- [Singularity](https://studio.blender.org/projects/singularity/) — Brushstroke Tools и толпа. Проверено 2026-10-14.

## Неизвестно

- Нет публичного научно-популярного ролика, где автор называет Geometry Nodes инструментом силовых линий; примеры — обучающие материалы и статьи.
- В какой версии появилась зона симуляции, не проверял по первоисточнику. Состав «бандлов» проверен только по заметкам релиза.
- Сколько стоит и как лицензируется полная версия ElectroMag Nodes: цены на странице нечётко отображаются, не записаны.
