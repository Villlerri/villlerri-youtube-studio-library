---
id: godot
name: Godot
class: [3d]
kind: app
site: https://godotengine.org/
github: godotengine/godot
scenes: [simulation, graph, character]
quality: 4
human_difficulty: 3
agent_difficulty: 2
automation: 4
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [avi, png-sequence, ogv]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Godot

Открытый игровой движок (2D и 3D) с режимом Movie Maker: он записывает видео не в реальном времени, с идеальным ритмом кадров. Сцены хранятся как текст, код на GDScript или C#. Канал Primer делает на нём симуляции.

## Ссылки

- Официальный сайт: https://godotengine.org/
- GitHub: https://github.com/godotengine/godot
- Документация: https://docs.godotengine.org/en/stable/ ([запись видео, Movie Maker](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html), [формат сцен .tscn](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html), [требования](https://docs.godotengine.org/en/stable/about/system_requirements.html))
- Примеры, проверенные 2026-10-14:
  - [Simulating a single brain cell (Primer, 2025-09-27)](https://www.youtube.com/watch?v=GkiITbgu0V0) — в описании «Made with Godot» и ссылка на репозиторий https://github.com/Primer-Learning/PrimerTools. 33 минуты: нейрон, веса, графики, манго для классификации.
  - [Simulating the Evolution of Aging (Primer, 2025-02-01)](https://www.youtube.com/watch?v=1_JbJTeLZJs) — в описании «Made with Godot».
  - [Simulating the Evolution of Rock, Paper, Scissors (Primer, 2024-07-13)](https://www.youtube.com/watch?v=tCoEYFbDVoI) — в описании «Made with Godot».

## Что реально получается

- Симуляции с «персонажами» (блобы Primer), объекты ведут себя по правилам, камера идёт по сцене без склеек. Это тот самый стиль «непрерывная сцена + осмысленное развитие».
- Графики и таблицы: Primer хранит в репозитории `PrimerTools` папки Animation, Camera, Graph, LaTeX, Simulation, Table и другие. README автора говорит, что код не рассчитан на других: «given up on the idea of designing this to be usable by others», часть моделей закрыта.
- Запись: `godot --path проект --write-movie out.avi` (или PNG с WAV). Частота задаётся `--fixed-fps`. По документации: «The output video will always have perfect frame pacing; it will never exhibit dropped frames or stuttering.»
- Motion blur: рендер в 240 к/с с последующим смешиванием кадров в FFmpeg (пример из руководства).
- Морфинг: shape keys и анимация параметров; сложные превращения форм нужно писать самому.
- Рисование линий и формулы: встроенных инструментов нет, свои у Primer (например LaTeX).
- Голос: аудио пишется прямо в файл. По документации частота микширования должна делиться нацело на частоту кадров, иначе звук уходит.
- Размер: по странице требований редактору нужно около 200 МБ на диске плюс около 1,3 ГБ шаблонов экспорта.

## Слабые стороны

- Для 3D-качества уступает [blender](blender.md) и Unreal: свет, материалы, отражения проще.
- Нет готовых научных сцен и инструментов формул: всё пишет команда.
- AVI с кодеком MJPEG ограничен 4 ГБ; для длинных роликов рекомендован PNG с WAV и последующая сборка во внешней программе ([ffmpeg](ffmpeg.md)). OGV пишется только в редакторской сборке.
- Звук не слышен во время записи (по документации).
- Документация Movie Maker не описывает запуск без окна (headless); нужна машина с видеокартой и экраном или виртуальным дисплеем (не проверялось).

## Сложность

- Для человека (3 из 5): GDScript простой, но нужно знать узлы и сцены. Дни–недели до первой анимации.
- Для агента (2 из 5): сцены `.tscn` и скрипты `.gd` — текст; запуск и запись из командной строки (`--write-movie`). Агент может писать, запускать и проверять кадры. Руки нужны для сложных ассетов.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): запуск из командной строки, `--fixed-fps`, `--quit-after N`; можно написать свой `MovieWriter` и направить поток в стороннюю программу. Пакетный рендер собирается скриптом.
- Воспроизводимость (4 из 5): сцены и ресурсы в текстовых `.tscn` и `.tres` (при импорте компилируются в бинарные копии в `.godot/imported`), проект ложится в git. Ритм кадров Movie Maker стабилен; детерминизм физики не проверялся.

## Платформа и оборудование

Минимум для редактора: Vulkan 1.0 (интегрированная графика) для Forward+ и Mobile, OpenGL 3.3 для режима Compatibility, 4 ГБ ОЗУ; рекомендовано Vulkan 1.2, 8 ГБ ОЗУ. Windows 10, macOS 10.15 (Forward+/Mobile), Linux не старше 2018–2020 года.

## Экспорт

- AVI (MJPEG и несжатый звук), быстро, до 4 ГБ.
- PNG-последовательность и WAV; прозрачность поддерживается, если включён `transparent_bg`.
- OGV: только в редакторской сборке.
- Видео в MP4/H.264 нужно получать внешней программой.

## Стоимость

Проверено 2026-10-14 по [странице лицензии](https://godotengine.org/license/). Бесплатно, без тарифов и роялти.

## Лицензия и права

- Код или программа: MIT.
- Результат: по странице лицензии «Godot’s license and copyright don’t extend to the content you make with it» — вы владеете правами на созданное. Видео как результат работы движка не распространяет сам движок, поэтому требований об указании MIT нет (вывод из текста страницы); они возникают при распространении собранной игры с бинарником Godot (нужно указать авторские права и текст лицензии).
- Ассеты в комплекте: сторонние библиотеки внутри движка идут по своим лицензиям, совместимым с MIT; список в `COPYRIGHT.txt`.

## Активность и зрелость

<!-- gh-stats:godotengine/godot -->
- Звёзды GitHub: 118 395
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: 3.6.3-stable (2026-08-22)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория godotengine/godot, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Последние релизы по [странице релизов GitHub](https://github.com/godotengine/godot/releases): 4.7.2 (18 августа 2026), 4.7.1 (14 июля), 4.7 (18 июня), 4.6.3 (20 мая); на ту же дату выходил 3.6.3 для старой ветки. Развивает сообщество проекта.

## Когда брать и когда нет

- Брать: симуляции и сцены, где нужны код, свобода лицензии и повторяемая запись; опыт Primer показывает, что это работает для научно-популярных роликов.
- Не брать: фотореализм и сложный свет (смотрите [blender](blender.md)); молекулы ([molecular-nodes](molecular-nodes.md)); если нет разработчика.

## Источники

- [Лицензия Godot](https://godotengine.org/license/) — MIT, права на созданный контент. Проверено 2026-10-14.
- [Создание видео (Movie Maker)](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) — `--write-movie`, `--fixed-fps`, форматы. Проверено 2026-10-14.
- [Формат .tscn](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) — текстовые сцены. Проверено 2026-10-14.
- [Системные требования](https://docs.godotengine.org/en/stable/about/system_requirements.html). Проверено 2026-10-14.
- [Релизы Godot](https://github.com/godotengine/godot/releases) — 4.7.2 и даты. Проверено 2026-10-14.
- [PrimerTools](https://github.com/Primer-Learning/PrimerTools) — состав и README. Проверено 2026-10-14.
- Описания роликов Primer на YouTube: фраза «Made with Godot» и ссылка на репозиторий подтверждены. Проверено 2026-10-14.

## Неизвестно

- Версия Godot, которую использует Primer.
- Работает ли Movie Maker без окна (headless).
- Детерминизм физики и случайных чисел между запусками.
- Пригодность 3D-рендера Godot для сложной научной графики, кроме опыта Primer.
