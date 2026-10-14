---
id: manim-ce
name: Manim Community Edition
class: [2d-code]
kind: framework
site: https://www.manim.community/
github: ManimCommunity/manim
scenes: [formula, graph, diagram, field, drawing]
quality: 4
human_difficulty: 3
agent_difficulty: 1
automation: 5
reproducibility: 5
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [mp4, mov, webm, gif, png-sequence, png]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Manim Community Edition

Python-фреймворк для математической анимации. Ответвление от кода Гранта Сандерсона (3Blue1Brown), которое ведёт сообщество. Выделяется стабильным API, подробной документацией и плагинами, включая озвучку.

## Ссылки

- Официальный сайт: https://www.manim.community/
- GitHub: https://github.com/ManimCommunity/manim
- Документация: https://docs.manim.community/en/stable/
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел):
  - [Галерея примеров](https://docs.manim.community/en/stable/examples.html) — готовые сцены с кодом: графики, зум-камера, движение по траектории. Один пример прислал автор канала TheoremofBeethoven.
  - [TransformMatchingShapes, пример Anagram](https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html) — буквы фразы «the morse code» перетекают в «here come dots».
  - [Примеры MovingCameraScene](https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.html) — камера плавно отъезжает от текста и возвращается, переезжает от фигуры к фигуре.
  - [Руководство по озвучке](https://docs.manim.community/en/stable/guides/add_voiceovers.html) — длительность анимации берётся из длины аудио прямо в сцене.

## Что реально получается

- Формулы: `MathTex` и `Tex` через LaTeX. `TransformMatchingTex` перетекает одинаковые части формулы, `TransformMatchingShapes` сопоставляет формы подобъектов. Это нужный для канала приём: вывод формулы, где символы переезжают, а не мигают.
- Рисование линий: `Create`, `Write`, `DrawBorderThenFill`, `Uncreate`, `Unwrite`, `TypeWithCursor`. Линия вырастает вдоль контура, текст пишется «вживую».
- Графики и поля: оси, функции, векторные поля (`ArrowVectorField`). Цифры и подписи следуют за объектами через апдейтеры.
- Камера: `MovingCameraScene` двигает и масштабирует кадр через `self.camera.frame.animate`. Есть `ZoomedScene` и `ThreeDScene`.
- Непрерывность: пока объекты живут в одном `construct()`, сцена течёт без склеек. Объект можно превратить в другой и оставить в кадре. Встроенных переходов между отдельными сценами нет, стык делается монтажом.
- Типографика: `Text`, `Paragraph`, `Code`; заголовки и подписи подходят, кинетической типографики уровня After Effects нет.
- Голос: плагин [manim-voiceover](manim-voiceover.md) вешает длительность анимации на длину озвучки. Метки времени дают [elevenlabs](elevenlabs.md) и [whisperx](whisperx.md) вне Manim.

## Слабые стороны

- Нет редактора с таймлайном. Подгонка ритма под голос идёт правкой чисел и перерендером. Для быстрой проверки есть низкое качество (`-ql`, 854x480, 15 к/с).
- Рендер Cairo идёт на процессоре. Сложные сцены с тысячами объектов рендерятся долго.
- LaTeX нужен отдельно (TeX Live, MiKTeX или TinyTeX). С версии 0.21.0 есть необязательная замена: Typst (`manim[typst]`).
- API меняется: в 0.20.0 переписан `MathTex` и сломаны `ImageMobject` и цвет `YELLOW_C`, в 0.22.0 заменены опции вывода и секции конфига. Старый код надо проверять после обновления.
- Код роликов 3Blue1Brown здесь не запускается: у [ManimGL](manimgl.md) другие имена (`ShowCreation` вместо `Create`) и другой пакет.
- OpenGL-рендерер в CE есть (`--renderer=opengl`), но его классы в официальной документации не описаны.
- Выразительность зависит от автора: вид по умолчанию «математический», красивый кадр требует вёрстки вручную.

## Сложность

- Для человека (3 из 5): нужен Python и понимание координат и объектов Manim. Первая сцена за день, свой стиль и ритм — недели.
- Для агента (1 из 5): сцена целиком в коде, рендер одной командой (`manim -ql file.py Scene`). `-s` сохраняет последний кадр как PNG, `--format=png-sequence` пишет все кадры. Агент сам смотрит кадры и правит. Руки нужны только для оценки вкуса и стыков с озвучкой.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): всё из командной строки и конфига, пакетный рендер сцен. С 0.20.0 есть `--seed` для случайности, с 0.22.0 настраиваются кодек и формат (`--format`, `--video-codec`, `--pixel-format`). Есть образ Docker `manimcommunity/manim`.
- Воспроизводимость (5 из 5): проект — текст на Python под git, одинаковый код даёт одинаковый кадр. Оговорка: результат зависит от версии Manim, установленного TeX и шрифтов; кэш `partial_movie_files` учитывает настройки кодировщика.

## Платформа и оборудование

Linux, macOS, Windows. Python 3.11 или новее (PyPI, версия 0.22.0). На Linux нужны заголовки Cairo и Pango, ManimPango собирается из исходников. Видеокарта для Cairo не нужна. Есть Docker, Binder и Colab. LaTeX необязателен, если нужен только простой текст.

## Экспорт

- По умолчанию MP4. `--format` принимает `mp4`, `mov`, `webm`, `gif`, `png` (последний кадр), `png-sequence`.
- Прозрачность: только MOV или WebM. Прозрачный MP4 отклоняется.
- Качество: `-ql` 854x480 15 к/с, `-qm` 1280x720 30, `-qh` 1920x1080 60, `-qp` 2560x1440 60, `-qk` 3840x2160 60.

## Стоимость

Проверено 2026-10-14 по [документации](https://docs.manim.community/en/stable/). Бесплатно, платных тарифов нет.

## Лицензия и права

- Код или программа: MIT. Авторские права держат 3blue1brown LLC и Manim Community Developers (README репозитория).
- Результат: по документации, созданные видео можно свободно распространять, указание Manim желательно, но не обязательно. В тексте MIT нет ограничений на коммерческое использование и монетизацию.
- Ассеты в комплекте: персонажи «Pi creatures» из роликов 3Blue1Brown защищены авторским правом, использовать их в своих работах нельзя (документация).

## Активность и зрелость

<!-- gh-stats:ManimCommunity/manim -->
- Звёзды GitHub: 41 535
- Последний коммит в основной ветке: 2026-10-12
- Последний релиз или тег: v0.22.0 (2026-10-08)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория ManimCommunity/manim, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Релизы по ленте GitHub: 0.19.0 (2025-01-20), 0.19.1 (2025-12-01), 0.19.2 (2026-01-17), 0.20.0 (2026-02-20), 0.20.1 (2026-02-27), 0.21.0 (2026-08-10), 0.22.0 (2026-10-08). Последний коммит в основной ветке — 2026-10-12. Между 0.19.0 и 0.19.1 был перерыв около 10 месяцев. Развивает сообщество волонтёров (организация ManimCommunity).

## Когда брать и когда нет

- Брать: вывод формул, графики, геометрия, поля, схемы с аккуратным рисованием линий, непрерывные сцены с морфингом и движением камеры, голос по тексту через [manim-voiceover](manim-voiceover.md). Лучший первый выбор для агента.
- Не брать: когда нужен ручной таймлайн, видеоподложки с графикой поверх, персонажи, сложный 3D и интерактивная отладка (смотри [manimgl](manimgl.md) и [motion-canvas](motion-canvas.md)).

## Источники

- [README репозитория](https://github.com/ManimCommunity/manim) — лицензия MIT, двойное авторство, происхождение от 3b1b/manim. Проверено 2026-10-14.
- [Главная страница документации](https://docs.manim.community/en/stable/) — версия 0.22.0, права на видео, «Pi creatures». Проверено 2026-10-14.
- [Установка через uv](https://docs.manim.community/en/stable/installation/uv.html) — системные зависимости, LaTeX необязателен. Проверено 2026-10-14.
- [Настройки вывода](https://docs.manim.community/en/stable/tutorials/output_and_config.html) — форматы и качество. Проверено 2026-10-14.
- [Список изменений 0.22.0](https://docs.manim.community/en/stable/changelog/0.22.0-changelog.html) и [0.21.0](https://docs.manim.community/en/stable/changelog/0.21.0-changelog.html) — формат вывода, Typst, ломающие изменения. Проверено 2026-10-14.
- [Раздел OpenGL в FAQ](https://docs.manim.community/en/stable/faq/opengl.html) — флаг и состояние документации. Проверено 2026-10-14.
- [PyPI: manim](https://pypi.org/project/manim/) — версия 0.22.0, Python 3.11 или новее, дата 2026-10-08. Проверено 2026-10-14.
- [Релизы](https://github.com/ManimCommunity/manim/releases) (лента releases.atom) — даты релизов. Проверено 2026-10-14.

## Неизвестно

- Список YouTube-каналов, которые делают ролики именно на CE, первоисточником не подтвердил. Примеров роликов на CE нет, только галерея кода.
- Время рендера типовой сцены на реальном железе не измерял: код не запускался.
- Состав и лицензии шрифтов в поставке не проверял.
