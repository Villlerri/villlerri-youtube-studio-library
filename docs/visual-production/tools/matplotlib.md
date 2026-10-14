---
id: matplotlib
name: Matplotlib (анимация)
class: [simulation]
kind: library
site: https://matplotlib.org/
github: matplotlib/matplotlib
scenes: [graph, field, formula, simulation]
quality: 3
human_difficulty: 2
agent_difficulty: 1
automation: 5
reproducibility: 5
cost: 0
maturity: standard
platforms: [linux, macos, windows]
export: [mp4, gif, png-sequence, svg, html]
code_license: Matplotlib License (на основе PSF)
price: бесплатно
checked: 2026-10-14
---

# Matplotlib (анимация)

Базовая Python-библиотека научных графиков. Анимация строится классами `FuncAnimation` и `ArtistAnimation` и сохраняется в видео через FFmpeg. Лучший первый выбор для 2D-графиков, карт поля и линий потока.

## Ссылки

- Официальный сайт: <https://matplotlib.org/>
- GitHub: <https://github.com/matplotlib/matplotlib>
- Документация анимаций: <https://matplotlib.org/stable/api/animation_api.html>
- Галерея анимаций: <https://matplotlib.org/stable/gallery/animation/index.html>
- Примеры, проверенные 2026-10-14:
  - [Double pendulum](https://matplotlib.org/stable/gallery/animation/double_pendulum.html) — двойной маятник, численное интегрирование в каждом кадре.
  - [Animated line plot](https://matplotlib.org/stable/gallery/animation/simple_anim.html) — минимальный `FuncAnimation`.
  - [Rain simulation](https://matplotlib.org/stable/gallery/animation/rain.html) — анимация набора кругов, меняющих размер и цвет.
  - [Streamplot](https://matplotlib.org/stable/gallery/images_contours_and_fields/plot_streamplot.html) — линии потока векторного поля, основа для линий магнитного поля. Так же Magpylib строит 2D-линии: [пример](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_mpl_streamplot.html).
  - [Python for Physics: Animating Interacting Particles](https://www.youtube.com/watch?v=X2MBh3GzdDY) — частицы с потенциалом Леннарда-Джонса, анимация на Matplotlib (канал Angry Physicist, около 18 минут).
  - [Animate Scientific Data in Python | Matplotlib Animation Tutorial for Researchers](https://www.youtube.com/watch?v=GEuEEYSjw-M) — разбор `FuncAnimation` и сохранения (канал Youven, около 41 минуты).

## Что реально получается

Сквозной пример (магнит на холодильнике). Поле даёт [magpylib](magpylib.md) или данные расчёта из [femm](femm.md). Matplotlib рисует карту модуля поля (`contourf`, `imshow`), линии поля (`streamplot`), стрелки (`quiver`), подписи и формулы. Анимация: магнит сдвигается, на каждом кадре пересчитывается поле, обновляются данные артистов. Полученная картинка чистая, как в учебнике.

Что даёт для объясняющего видео:

- Плавное движение и смена параметров: функция кадра получает номер или время, всё меняется непрерывно. Интерполяция делается самим кодом.
- Формулы: mathtext рисует выражения вида `$\vec{B}$` прямо в графике.
- Графики данных: кривые, диаграммы, поля векторов, поверхности. Для объёмной сцены `mplot3d` слабее, чем [pyvista](pyvista.md).
- Видео: `FuncAnimation.save("file.mp4", writer=...)`. Писатели: `FFMpegWriter` (поток кадров в ffmpeg через pipe), `PillowWriter` и `ImageMagickWriter` для GIF, `HTMLWriter` для HTML. Параметры `FFMpegWriter`: `fps` (по умолчанию 5), `codec` (по умолчанию h264), `bitrate`, `extra_args`.
- Качество для YouTube: размер кадра задаётся `figsize` и `dpi`, например 1920×1080. Рекомендуется писать PNG-последовательность и собирать в FFmpeg, особенно если нужны управляемые кодек и цветовое пространство, см. [ffmpeg](ffmpeg.md).
- Рисование линий: штрих растёт, если в каждом кадре показывать больший срез данных (`set_data`).
- Камера: у 2D нет камеры, но `xlim` и `ylim` меняются по кадрам, получается наезд и панорама. У `mplot3d` есть углы обзора.
- Голос: нет. Время кадров задаётся кодом, метки времени озвучки можно превратить в номера кадров.

## Слабые стороны

- Медленный рендер: каждый кадр рисуется заново на CPU, длинные ролики на 4K идут долго. Режим blit ускоряет только живой показ, при сохранении не помогает.
- Внешний вид «графика из статьи». Для роликов нужны свои темы, шрифты, цвета.
- 3D-графика ограниченная: сортировка глубины, нет настоящих теней и материалов.
- `FFMpegWriter` требует установленный `ffmpeg` в системе. Без него остаётся GIF, который для YouTube неприемлем.
- Сложные переходы между сценами и композитинг в Matplotlib не делаются, этим занимается монтаж.

## Сложность

- Для человека (2 из 5): базовый график делается за час. Плавная красивая анимация требует знаний `FuncAnimation`, но примеров очень много.
- Для агента (1 из 5): всё кодом, результат агент проверяет, открывая сохранённые кадры. Руки не нужны.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): скриптом, без окна (бэкенд Agg), пакетный рендер.
- Воспроизводимость (5 из 5): текстовый скрипт под git, кадры одинаковы при тех же версиях библиотеки и шрифтов. Шрифты и версии стоит фиксировать.

## Платформа и оборудование

Python, Linux, macOS, Windows. Видеокарта не нужна. Для mp4 нужен установленный `ffmpeg`.

## Экспорт

MP4 и другие форматы через FFmpeg, GIF через Pillow, HTML5-видео и JSHTML для блокнотов, PNG-последовательность, векторные SVG и PDF для статичных кадров. Альфа-канал: PNG с прозрачностью (`savefig(transparent=True)`), для видео с альфой требуется свой кодек и аргументы FFmpeg, в документации не проверялось.

## Стоимость

Проверено 2026-10-14. Бесплатно.

## Лицензия и права

- Код или программа: лицензия Matplotlib на основе PSF License ([текст](https://matplotlib.org/stable/project/license.html)). Разрешены использование, изменение, распространение с сохранением уведомления.
- Результат: лицензия не накладывает условий на графики и ролики.
- Ассеты в комплекте: шрифты DejaVu и набор цветовых карт; отдельные условия лежат в каталоге лицензий пакета.

## Активность и зрелость

<!-- gh-stats:matplotlib/matplotlib -->
- Звёзды GitHub: 23 368
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v3.11.2 (2026-09-11)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория matplotlib/matplotlib, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: standard. Версия 3.11.2 вышла 2026-09-11, 3.11.1 — 2026-07-18, 3.11.0 — 2026-06-12. Фундаментальная библиотека экосистемы Python, проект NumFOCUS.

## Когда брать и когда нет

- Брать: 2D-графики, карты поля, линии потока, формулы в подписях, быстрые прототипы. Первый выбор для агента.
- Не брать: нужны красивые 3D-материалы, мягкие тени и сложная камера — [pyvista](pyvista.md), [blender](blender.md). Нужна анимация геометрии, формул и подписей как у 3Blue1Brown — [manim-ce](manim-ce.md).

## Источники

- [Animation API](https://matplotlib.org/stable/api/animation_api.html) — FuncAnimation, ArtistAnimation, писатели FFMpegWriter, PillowWriter, HTMLWriter, ImageMagickWriter. Проверено 2026-10-14.
- [FFMpegWriter](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FFMpegWriter.html) — fps, codec, bitrate, extra_args. Проверено 2026-10-14.
- [Лицензия Matplotlib](https://matplotlib.org/stable/project/license.html) — текст лицензии, PSF-основа. Проверено 2026-10-14.
- [Matplotlib на PyPI](https://pypi.org/pypi/matplotlib/json) — версия 3.11.2, даты. Проверено 2026-10-14.
- [Mathtext](https://matplotlib.org/stable/users/explain/text/mathtext.html) — формулы в подписях. Проверено 2026-10-14.
- [Streamplot](https://matplotlib.org/stable/gallery/images_contours_and_fields/plot_streamplot.html) — линии потока. Проверено 2026-10-14.

## Неизвестно

- Как быстро Matplotlib рисует 1800 кадров 1920×1080 с картой поля: не измерялось.
- Условия на шрифты и цветовые карты из комплекта: отдельные файлы лицензий не вычитывались.
- Корректный способ получить видео с альфа-каналом из `FFMpegWriter`: не проверено.
