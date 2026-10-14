---
id: moviepy
name: MoviePy
class: [edit-composite]
kind: library
site: https://zulko.github.io/moviepy/
github: Zulko/moviepy
scenes: [real-footage, typography, screen]
quality: 3
human_difficulty: 2
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: declining
platforms: [linux, macos, windows]
export: [mp4, gif]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# MoviePy

Python-библиотека для монтажа и композитинга. Резка, склейка, титры, наложение слоёв, свои эффекты. Текущая версия 2.2.1 от 21 мая 2025.

## Ссылки

- Официальный сайт и документация: <https://zulko.github.io/moviepy/>
- GitHub: <https://github.com/Zulko/moviepy>
- Переход с 1.x на 2.x: <https://zulko.github.io/moviepy/getting_started/updating_to_v2.html>
- PyPI: <https://pypi.org/project/moviepy/>
- Примеры, проверенные 2026-10-14 (ссылка открывается через oEmbed; содержание по названию, версию API в роликах не проверял):
  - [Create Your Own Custom MoviePy Animations](https://www.youtube.com/watch?v=io46L1Nl3hU) — канал NeuralNine. Свои анимации через функцию кадра.
  - [Automated Video Editing with MoviePy in Python](https://www.youtube.com/watch?v=Q2d1tYvTjRw) — канал NeuralNine. Автоматическая сборка ролика.

## Что реально получается

Опора: документация MoviePy 2, README, список эффектов.

- Клип можно задать функцией: `VideoClip(frame_function=None, is_mask=False, duration=None, has_constant_size=True)`. Функция принимает время `t` и возвращает кадр как массив ширина x высота x 3 (RGB). Значит, анимацию можно рисовать кодом (NumPy, Pillow), а MoviePy склеит и закодирует.
- Резка, склейка, титры, слои (`CompositeVideoClip`), маски. Эффекты в `moviepy.video.fx`: CrossFadeIn, CrossFadeOut, FadeIn, FadeOut, SlideIn, SlideOut, AccelDecel, Freeze, Loop, Resize, Rotate, Scroll, Margin, Crop, HeadBlur и другие.
- Переходы: в списке эффектов только растворение (CrossFade), затухание и въезд/выезд (Slide). Готового набора шторок нет, в отличие от [FFmpeg](ffmpeg.md) `xfade`.
- Рисование линий и морфинг: готовых эффектов нет, делаются функцией кадра. Свою анимацию пишет автор.
- Синхронизация с голосом: через время `t`. Привязка к словам делается своим кодом по таймкодам.
- Непрерывная сцена: целиком зависит от того, что вернёт функция кадра. Библиотека сама ничего не интерполирует.
- Скорость: README признаёт, что MoviePy медленнее прямого вызова FFmpeg из-за импорта и экспорта данных.

## Слабые стороны

- Версия 2 несовместима с 1: `moviepy.editor` удалён, импорт из `moviepy`. Методы `.set_*` переименованы в `.with_*`, большинство методов возвращает копию. Эффекты стали классами `Effect`, применяются через `with_effects()`, `clip.fx` удалён. `resize` стал `resized`, `crop` стал `cropped`, `rotate` стал `rotated`. Удалены зависимости ImageMagick, PyGame, OpenCV, scipy и др. (работа с картинками на Pillow), удалены модули `moviepy.video.tools.tracking` и `segmenting`. У `TextClip` изменились аргументы, путь к файлу шрифта обязателен.
- Большинство уроков в сети написано для версии 1 (пример поисковой выдачи: код с `moviepy.editor`). Агенту, обученному на старых примерах, легко сгенерировать нерабочий код.
- Нет релизов с 21 мая 2025 (2.2.1), коммиты в основную ветку есть (последний 26 августа 2026). README просит помощи: «библиотека держалась только на участии мейнтейнеров».
- В списке эффектов нет оптического потока, морфинга и 3D.

## Сложность

- Для человека (2 из 5): нужен Python, базовая работа за дни.
- Для агента (2 из 5): всё код, результат сам проверяется рендером. Оценка 2, не 1, из-за несовместимости версий 1 и 2 и частых устаревших примеров.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): всё из Python, пакетный запуск, `write_videofile` с параметрами `codec`, `fps`, `preset`, `ffmpeg_params`, `pixel_format`.
- Воспроизводимость (4 из 5): код в текстовом файле под git. Результат зависит от версий MoviePy, Pillow и FFmpeg.

## Платформа и оборудование

Windows, macOS, Linux. Python 3.9 и новее (README). Для кодирования использует FFmpeg (документация `write_videofile`).

## Экспорт

- `write_videofile(filename, fps, codec, bitrate, audio, preset, ffmpeg_params, pixel_format, ...)`: любой кодек, поддерживаемый FFmpeg, например `libx264`, `mpeg4`. Параметры YouTube см. в карточке [FFmpeg](ffmpeg.md), передавать через `ffmpeg_params`.
- GIF читается и пишется (README).
- Альфа-канал и последовательности изображений: не проверены.

## Стоимость

Проверено 2026-10-14. Бесплатно, MIT. Оценка стоимости 0.

## Лицензия и права

- Код или программа: MIT ([README](https://github.com/Zulko/moviepy), PyPI).
- Результат: лицензия кода на результат не накладывает ограничений. Кодирование идёт через FFmpeg, его сборка может быть LGPL или GPL (см. [FFmpeg](ffmpeg.md)). Не юридическая консультация.
- Ассеты в комплекте: нет.

## Активность и зрелость

<!-- gh-stats:Zulko/moviepy -->
- Звёзды GitHub: 14 983
- Последний коммит в основной ветке: 2026-08-26
- Последний релиз или тег: v2.2.1 (2025-05-21)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория Zulko/moviepy, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: declining. Версии: 2.0.0 (20 ноября 2024), 2.1.0 и 2.1.1 (24 и 25 ноября 2024), 2.1.2 (10 января 2025), 2.2.0 и 2.2.1 (21 мая 2025). Релизов после этого нет, коммиты в основной ветке продолжаются. Мейнтейнеры: Zulko, @osaajani, @tburrows13, @keikoro.

## Когда брать и когда нет

- Брать: Python-сценарий собирает ролик из кадров, рисует кадры функцией, накладывает титры, нужен быстрый прототип.
- Не брать: нужна скорость и сотни переходов ([FFmpeg](ffmpeg.md)), графический интерфейс ([Kdenlive](kdenlive.md)), оптический поток, 3D, морфинг ([DaVinci Resolve](davinci-resolve.md)).
- Предупреждение агенту: использовать документацию версии 2, не копировать примеры с `moviepy.editor`.

## Источники

- [Документация MoviePy](https://zulko.github.io/moviepy/) — MIT, версия 2, переход с 1.x. Проверено 2026-10-14.
- [Updating from v1.X to v2.X](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html) — несовместимости. Проверено 2026-10-14.
- [README MoviePy](https://github.com/Zulko/moviepy) — возможности, Python 3.9+, MIT, мейнтейнеры, нехватка рук, скорость. Проверено 2026-10-14.
- [VideoClip и write_videofile](https://zulko.github.io/moviepy/reference/reference/moviepy.video.VideoClip.VideoClip.html) — подпись конструктора и параметры кодирования. Проверено 2026-10-14.
- [moviepy.video.fx](https://zulko.github.io/moviepy/reference/reference/moviepy.video.fx.html) — список эффектов. Проверено 2026-10-14.
- [PyPI: moviepy](https://pypi.org/pypi/moviepy/json) — версия 2.2.1, даты выпусков. Проверено 2026-10-14.
- [Коммиты MoviePy (Atom)](https://github.com/Zulko/moviepy/commits/master.atom) — последнее обновление 2026-08-26. Проверено 2026-10-14.

## Неизвестно

- Кодирует ли MoviePy альфа-канал и пишет ли последовательности изображений: в документации не проверено.
- Содержание обоих роликов описано по названию, версия MoviePy в них не проверена.
- Будет ли выпуск 2.3 или 3.0: планов не нашёл.
