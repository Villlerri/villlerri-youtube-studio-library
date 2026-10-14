---
id: magpylib
name: Magpylib
class: [simulation]
kind: library
site: https://magpylib.readthedocs.io/en/latest/
github: magpylib/magpylib
scenes: [field, simulation, graph]
quality: 3
human_difficulty: 2
agent_difficulty: 1
automation: 5
reproducibility: 5
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [png-sequence, gif, html]
code_license: BSD-2-Clause
price: бесплатно
checked: 2026-10-14
---

# Magpylib

Python-библиотека для аналитического расчёта статических магнитных полей постоянных магнитов и токов. Считает поле формулами, без сетки, поэтому карта поля магнита в любой точке и любой кадр анимации получаются за доли секунды.

## Ссылки

- Официальный сайт и документация: <https://magpylib.readthedocs.io/en/latest/>
- GitHub: <https://github.com/magpylib/magpylib>
- Галерея примеров: <https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_index.html>
- Примеры, проверенные 2026-10-14:
  - [Magnetic Scales](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_app_scales.html) — линейная магнитная шкала из 10 чередующихся зон феррита (остаточная индукция 0,3 Тл, длина зоны 1 мм), карты компонент поля на высоте 0,5 мм. Это ближайший готовый пример к полосатому магниту на холодильник.
  - [Halbach Magnets](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_app_halbach.html) — сборка из кубиков с вращающейся поляризацией и линии поля в плоскости симметрии.
  - [Matplotlib Streamplot](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_mpl_streamplot.html) — 2D-линии поля магнита на сетке.
  - [Pyvista 3D Field Lines](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_pv_streamlines.html) — 3D-линии поля цилиндрического магнита трубками, цвет по модулю поля.
  - [Animations](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_animations.html) — анимация движения магнита по траектории, выгрузка в GIF.
  - [Method of Images](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_misc_image_method.html) — магнит рядом с мягкой магнитной пластиной (идеализация для стальной двери холодильника).
  - [Introduction to the open-source project Magpylib](https://www.youtube.com/watch?v=LeUx6cM1vcs) — вводный ролик (канал Thai Pham), по README он о версии 4.0.0, API с тех пор изменился.

## Что реально получается

Сквозной пример (магнит на холодильнике). Полосатый гибкий магнит собирается как набор кубоидов с чередующейся поляризацией, точно как в примере Magnetic Scales. Поле считается на сетке одной командой `getB`. Из сетки делаются карта модуля поля (contourf, pixel field) и линии поля (streamplot для 2D, streamlines PyVista для 3D). В документации нет примера именно для холодильника, но нужные кирпичики есть в трёх разных примерах.

Что даёт для объясняющего видео:

- Карта и линии поля любого набора магнитов: стержень, диск, кольцо, полосатая пластина, сборки Хальбаха.
- Непрерывное движение: позиции и повороты задаются массивами, поле считается по всей траектории одним вызовом. Магнит плавно подъезжает к двери, кадр за кадром меняется карта поля.
- Плавная смена параметров: ширина полос, число полюсов, расстояние. Плавный переход делается интерполяцией параметра между кадрами и пересчётом.
- Встроенные анимации: `show(animation=True)` с бэкендом Plotly даёт интерактивную анимацию в браузере со слайдером. Выгрузка в файл через `animation_output="my.gif"` работает только с бэкендом PyVista (сноска в документации: только gif или mp4). Примера mp4 в документации нет.
- Для видео надёжнее свой цикл: поле считает Magpylib, кадры рисуют Matplotlib или PyVista, склеивает FFmpeg. Камеру ведёт PyVista, см. [pyvista](pyvista.md). Линии растут «рисованием» только если вручную обрезать каждую линию по длине.
- Силы и моменты: `getFT` (новое в 5.2) считает силу и момент на магните. Пример [Magnetic Holding Force](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_force_holding_force.html) в галерее.

Синхронизация с голосом: готовой нет. Время кадра задаётся кодом, поэтому метки из озвучки (см. [whisperx](whisperx.md)) можно превратить в моменты смены сцены.

## Слабые стороны

- Только магнитостатика. Нет вихревых токов и движения проводников.
- Железо и сталь не моделируются напрямую. Дверь холодильника можно идеализировать методом изображений (бесконечная проницаемость). Для реальной стали с насыщением нужен конечно-элементный расчёт: [femm](femm.md), [elmer-fem](elmer-fem.md), [comsol](comsol.md). Есть отдельное расширение [magpylib-material-response](https://github.com/magpylib/magpylib-material-response) для мягких материалов.
- Размагничивание и неоднородную намагниченность реального гибкого магнита идеальная модель не учитывает. Документация оценивает ошибку для хорошо изученных случаев, для магнитов с холодильника оценки нет.
- Внешний вид «из коробки» научный. Для ролика нужна своя настройка цветов, шрифтов и камеры.
- Встроенная выгрузка анимации привязана к PyVista и GIF. GIF для YouTube плох.

## Сложность

- Для человека (2 из 5): несколько строк Python, физика задаётся геометрией и поляризацией. Трудность в том, чтобы выбрать реальные значения поляризации и сделать красивую картинку.
- Для агента (1 из 5): всё кодом, результат проверяется по картинке. Руки не нужны. Нужен Python 3.11 или новее.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): чистый Python, векторизованные вычисления, пакетный рендер кадров без интерфейса.
- Воспроизводимость (5 из 5): расчёт аналитический и детерминированный, проект — текстовый скрипт под git. Внешний вид кадра зависит ещё от бэкенда рисования и его версии.

## Платформа и оборудование

Python 3.11+, зависимости NumPy, SciPy, Matplotlib, Plotly, PyVista опционально. Работает на Linux, macOS, Windows, видеокарта для расчёта не нужна. Для рендера 3D нужен PyVista, см. [pyvista](pyvista.md).

## Экспорт

Свои кадры: PNG-последовательность из Matplotlib или PyVista, дальше FFmpeg в mp4. Встроенно: HTML (Plotly), GIF (PyVista). Альфа-канал: пример «Custom Export Pyvista» в документации показывает, как получить прозрачный фон.

## Стоимость

Проверено 2026-10-14 по [PyPI](https://pypi.org/project/magpylib/) и репозиторию. Бесплатно, открытый код.

## Лицензия и права

- Код или программа: BSD-2-Clause ([README](https://github.com/magpylib/magpylib)).
- Результат: лицензия BSD-2-Clause регулирует распространение программы. Условий на расчёты, картинки и ролики в ней нет.
- Ассеты в комплекте: ассетов нет.

## Активность и зрелость

<!-- gh-stats:magpylib/magpylib -->
- Звёзды GitHub: 382
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: 5.2.3 (2026-05-16)
- Лицензия по данным GitHub: BSD-2-Clause
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория magpylib/magpylib, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: stable. Последний релиз на PyPI 5.2.3 от 2026-05-16, регулярные релизы в 2025–2026 (5.2.0 в октябре 2025, 5.2.1 в октябре 2025, 5.2.2 в феврале 2026). Есть научная статья 2020 года в открытом доступе (ссылка в README).

## Когда брать и когда нет

- Брать: быстрая карта и линии поля магнитов, плавное движение магнита по сцене, полосатые магниты и сборки Хальбаха, силы между магнитами.
- Не брать: когда важна реальная сталь с насыщением, вихревые токи, нелинейные материалы. Берите [femm](femm.md) или [elmer-fem](elmer-fem.md).
- Для финальной картинки с лучшим светом поле можно вынести в Blender: [blender-geometry-nodes](blender-geometry-nodes.md).

## Источники

- [Magpylib: документация](https://magpylib.readthedocs.io/en/latest/) — что считает, функции 5.2 (getFT, TriangleStrip). Проверено 2026-10-14.
- [Magpylib README на GitHub](https://github.com/magpylib/magpylib) — лицензия BSD-2-Clause, возможности, Python 3.11+. Проверено 2026-10-14.
- [Animations](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_animations.html) — animation=True, Plotly, animation_output, GIF только с PyVista. Проверено 2026-10-14.
- [Magnetic Scales](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_app_scales.html) — полосатая шкала из чередующихся зон. Проверено 2026-10-14.
- [Physics and Computation](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/guide_resources_01_physics.html) — идеальные допущения, размагничивание, метод изображений. Проверено 2026-10-14.
- [Graphic output](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/docs/docs_graphics.html) — параметры анимации и бэкенды. Проверено 2026-10-14.
- [Magpylib на PyPI](https://pypi.org/pypi/magpylib/json) — версия 5.2.3, даты релизов. Проверено 2026-10-14.

## Неизвестно

- Реальная скорость расчёта на сетке 1920×1080 кадров: код не запускался, цифр нет.
- Точность идеальной модели для гибкого феррито-полимерного магнита: документация даёт оценку только для примера с магнитной шкалой.
- Работает ли выгрузка mp4 через `animation_output`: в сноске документации mp4 упомянут, в примере показан только GIF.
- Отдельных готовых роликов YouTube в стиле объясняющего видео, сделанных Magpylib, не найдено.
