---
id: blender-grease-pencil
name: Blender Grease Pencil
class: [3d, frame-vector-skeletal, whiteboard]
kind: method
site: https://docs.blender.org/manual/en/latest/grease_pencil/index.html
github: none
scenes: [drawing, diagram, character]
quality: 4
human_difficulty: 3
agent_difficulty: 3
automation: 3
reproducibility: 3
cost: 0
maturity: young
platforms: [linux, macos, windows]
export: [mp4, mov, png-sequence, svg]
code_license: GPL-2.0-or-later
price: бесплатно (часть Blender)
checked: 2026-10-14
---

# Blender Grease Pencil

Объект Blender для рисования штрихов прямо в 3D-пространстве. Подходит для рисования «вживую», покадровой 2D-анимации и сочетания рисунка с 3D-камерой. Отдельной программы нет, это часть [Blender](blender.md).

## Ссылки

- Официальный сайт: https://www.blender.org (раздел руководства: https://docs.blender.org/manual/en/latest/grease_pencil/index.html)
- GitHub: отдельного репозитория нет; код входит в зеркало https://github.com/blender/blender (см. [blender](blender.md)).
- Документация: [введение](https://docs.blender.org/manual/en/latest/grease_pencil/introduction.html), [модификатор Build](https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html)
- Примеры, проверенные 2026-10-14:
  - [What's New in Blender 5.2 LTS (официальный обзор)](https://www.youtube.com/watch?v=g4OXlrxqIx0) — раздел Grease Pencil с 07:40.
  - [Blender 5.0 Grease Pencil: Pen Tool, Motion Blur (Mumu Mundo)](https://www.youtube.com/watch?v=WYZY4n3fRM0) — обзор GP 5.0 от автора сообщества; ссылка есть на странице релиза 5.0.
  - [Blender 5.0 Story Tools (Blender Studio)](https://www.youtube.com/watch?v=RTRF_VseX1k) — раскадровка: Grease Pencil и видеосеквенсор в одном проекте.
  - [Blender 4.3, официальный обзор](https://www.youtube.com/watch?v=KnpvIIfm7uQ) — официальный обзор 4.3, релиза с переписанным Grease Pencil (GPv3).

## Что реально получается

- Рисование штрихов в 3D: по руководству Grease Pencil принимает рисунок от мыши или планшета и «помещает его в трёхмерное пространство как набор точек, то есть штрих». Штрихи можно облететь камерой, поставить на разную глубину, осветить.
- Дорисовка линий (эффект «рисуется на глазах»): модификатор Build по руководству «makes strokes appear or disappear in a frame range to create the effect of animating lines being drawn or erased». Режимы Sequential (по одному штриху), Concurrent (несколько) и Additive. Для схем и подписей это основной приём «рисования вживую».
- Автоматический вариант (оценка): векторный рисунок (SVG) импортируется в Grease Pencil (в заметках 5.2 есть импортёр SVG с настройкой масштаба), а Build рисует его по кадрам. Агент может собрать это кодом. Готового публичного примера такого пайплайна я не нашёл.
- Непрерывность: рисунок и 3D-объекты в одной сцене; камера свободно движется.
- Покадровая 2D-анимация, вырезная анимация, motion graphics, раскадровка (из введения руководства).
- Стиль линий: материалы, модификаторы, эффекты, свет на штрихах. В 5.2 добавлена заливка Delaunay (точная заливка по контуру, автоматическое закрытие зазоров); линии «точки» и «квадраты» получили настройку размещения.
- Морфинг: интерполяция между рисунками (в руководстве раздел Animation › Interpolation). Плавность зависит от аккуратности рисунка.
- Голос: нет встроенной привязки к тексту. Тайминг задаётся кадрами, как в [Blender](blender.md).

## Слабые стороны

- Переписанный движок GPv3 вышел в Blender 4.3 (2024-11-19). Прежние Python-скрипты для Grease Pencil могут не работать: в заметках 4.3 есть «Python API migration guide».
- Красиво рисовать вручную, «как в ролике доски», должен человек. Автоматически получается чистая векторная линия, а не живой почерк.
- Рисующая рука или маркер на экране: такой функции в проверенной документации нет (оценка), штрихи проявляются сами.
- Тяжёлые сцены с тысячами штрихов нагружают видеокарту (оценка, не измерялось).

## Сложность

- Для человека (3 из 5): интерфейс Blender плюс навык рисования; для простого Build-эффекта с готовым SVG достаточно дней.
- Для агента (3 из 5): создание штрихов и слоёв доступно через Python (в 5.2 добавили функции для масок слоёв и свойства штриха). Но внешний вид линий и заливок агент проверяет только по рендеру. Рисование от руки — на человеке.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): штрихи и модификаторы создаются из `bpy`, рендер идёт `blender -b`. Часть настроек (кисти, материалы линий) удобнее готовить руками и подключать как ассеты.
- Воспроизводимость (3 из 5): рисунок хранится в двоичном `.blend`. Если штрихи получены из SVG скриптом, исходник остаётся текстом.

## Платформа и оборудование

Как у [Blender](blender.md). Для рисования нужен планшет с пером (мышь работает, но хуже).

## Экспорт

Те же видео и кадры, что у Blender. Дополнительно экспорт штрихов в SVG и PDF (в 5.0 добавлен экспорт кривых Безье, Catmull-Rom и NURBS в SVG; 5.2: углы в SVG/PDF). Альфа-канал доступен при форматах с RGBA.

## Стоимость

Проверено 2026-10-14. Входит в [Blender](blender.md), бесплатно. Онлайн-библиотека Essentials с 19 новыми кистями Grease Pencil (5.2) тоже бесплатная, условия лицензии кистей не проверены.

## Лицензия и права

- Код или программа: GPL, как у Blender.
- Результат: принадлежит автору («What you create with Blender is your sole property»), ограничений на монетизацию нет.
- Ассеты в комплекте: кисти и материалы из Essentials; лицензия не проверена.

## Активность и зрелость

Зрелость: `young` в части GPv3. Переписанный Grease Pencil вышел в Blender 4.3 (2024-11-19), моложе двух лет; Python API менялся (в заметках 5.0 есть раздел о несовместимых изменениях Python API для Grease Pencil). В 5.0: motion blur, углы штрихов, инструмент Pen. В 5.2 LTS (2026-07-14): заливка Delaunay и настройки линий. Развивает команда Blender.

## Когда брать и когда нет

- Брать: схемы и надписи, которые «рисуются» на глазах в 3D-сцене с движущейся камерой; покадровые вставки; раскадровка.
- Не брать: если нужен имитированный почерк с рукой на доске: смотрите [videoscribe](videoscribe.md), [doodly](doodly.md) или [lightboard](lightboard.md). Если нужен плоский векторный монтаж без 3D: [rive](rive.md) или [synfig](synfig.md).

## Источники

- [Введение в Grease Pencil](https://docs.blender.org/manual/en/latest/grease_pencil/introduction.html) — штрихи в 3D, назначение. Проверено 2026-10-14.
- [Модификатор Build](https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/build.html) — эффект рисования линий. Проверено 2026-10-14.
- [Оглавление руководства Grease Pencil](https://docs.blender.org/manual/en/latest/grease_pencil/index.html) — интерполяция, Line Art, модификаторы. Проверено 2026-10-14.
- [Blender 4.3](https://www.blender.org/download/releases/4-3/) — переписанный Grease Pencil, слои, Geometry Nodes. Проверено 2026-10-14.
- [Blender 5.0](https://www.blender.org/download/releases/5-0/) — motion blur, углы, Pen Tool, экспорт SVG, Story Tools. Проверено 2026-10-14.
- [Blender 5.2 LTS](https://www.blender.org/download/releases/5-2/) — Delaunay fill, Python API, импорт SVG. Проверено 2026-10-14.
- YouTube-ролики (ссылки выше): названия подтверждены через oEmbed. Проверено 2026-10-14.

## Неизвестно

- Публичного научно-популярного ролика, сделанного именно с Grease Pencil и камерой в 3D, я не нашёл. Примеры — релизные обзоры инструмента.
- Работоспособность связки SVG → Grease Pencil → Build на текущей версии не проверялась: код не запускали.
- Лицензия кистей из Essentials не проверена.
