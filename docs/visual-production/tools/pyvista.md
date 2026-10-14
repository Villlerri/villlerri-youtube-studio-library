---
id: pyvista
name: PyVista
class: [simulation, 3d]
kind: library
site: https://docs.pyvista.org/
github: pyvista/pyvista
scenes: [field, simulation, micro, mechanism]
quality: 3
human_difficulty: 2
agent_difficulty: 1
automation: 5
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [mp4, gif, png-sequence]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# PyVista

Python-обёртка над VTK: сетки и облака точек как массивы NumPy, фильтры (срез, изоповерхность, линии тока) и рендер в окне, в Jupyter или без окна. Хорошо стыкуется с Magpylib, Elmer и ParaView.

## Ссылки

- Официальный сайт и документация: <https://docs.pyvista.org/>
- GitHub: <https://github.com/pyvista/pyvista>
- Учебник: <https://tutorial.pyvista.org/>
- Примеры, проверенные 2026-10-14:
  - [Create a MP4 Movie](https://docs.pyvista.org/examples/02-plot/movie.html) — запись mp4 из цикла кадров.
  - [Orbiting](https://docs.pyvista.org/examples/02-plot/orbit.html) — облёт камеры вокруг объекта.
  - [Streamlines](https://docs.pyvista.org/examples/01-filter/streamlines.html) — линии тока векторного поля.
  - [Pyvista 3D Field Lines (Magpylib)](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_pv_streamlines.html) — линии поля цилиндрического магнита трубками из `streamlines_from_source`; разбор есть в [magpylib](magpylib.md).
  - [[Radia/Python/PyVISTA] 3D magnetic field visualization from Radia Python by PyVISTA and ParaView](https://www.youtube.com/watch?v=_gQ6Rq8Thuc) — 3D-поле многополюсного вигглера, вид в PyVista и ParaView.
  - [Bane Sullivan, Tetsuo Koyama, Alexander Kaszynski – 3D Visualization with PyVista](https://www.youtube.com/watch?v=lxgqlNlqR9c) — учебный доклад SciPy 2023 от авторов библиотеки.

## Что реально получается

Сквозной пример (магнит на холодильнике). Поле магнита считает [magpylib](magpylib.md) на регулярной сетке `pv.ImageData`, записывается как массив `B`, дальше `streamlines_from_source` строит линии поля из диска или линии затравок, `tube()` превращает их в трубки, цвет задаёт модуль поля. Магнит рисуется в той же сцене. Это показано в документации Magpylib для одного цилиндрического магнита. Полосатый магнит строится тем же способом из набора кубоидов.

Что даёт для объясняющего видео:

- Камера: орбита по заданной траектории (`orbit_on_path`), любые позиции камеры, плавные пролёты кадром за кадром. Это сильнее, чем у [matplotlib](matplotlib.md).
- Непрерывная сцена: объекты, цвета, сетки меняются между кадрами, в цикле `write_frame`. Морфинг геометрии получается интерполяцией точек сетки между двумя состояниями.
- Видео: `open_movie` пишет mp4 (по умолчанию 24 кадра в секунду, качество 5 из 10), `open_gif` пишет GIF. Для mp4 нужен `imageio` и бэкенд ffmpeg (в списке необязательных зависимостей установки: `imageio-ffmpeg`).
- Безголовый рендер: с VTK 9.5 и выше работает без Xvfb и без `DISPLAY`: `pv.Plotter(off_screen=True)`, нужна системная библиотека `libegl1`. На машине без GPU падает на программный рендер Mesa llvmpipe.
- Внешний вид: физически корректные материалы (PBR), прозрачный фон скриншота (`transparent_background`), настройка света. В галерее есть [пример PBR](https://docs.pyvista.org/examples/02-plot/pbr.html).
- Рисование линий: линии поля — готовые трубки. Эффект «рисования» делается показом всё более длинной части линии от кадра к кадру.
- Голос: нет. Время кадров задаётся кодом, метки от озвучки превращаются в номера кадров вручную.

## Слабые стороны

- Качество картинки — уровень VTK: аккуратная научная графика. До Blender по свету, тени и материалам далеко. Для финальных кадров данные можно вывести в [blender](blender.md).
- Нужен компьютер с поддержкой EGL или Mesa. Программный рендер медленный на больших сценах.
- Для mp4 нужен отдельный пакет `imageio-ffmpeg`. Без него mp4 не запишется.
- Текст: есть `add_text` и 3D-текст, формул средствами PyVista в проверенных страницах нет. Заголовки и формулы удобнее вынести в монтаж.
- Версии VTK ограничены: `vtk>=9.3.1, <9.8`, а `9.4.0` и `9.4.1` исключены.

## Сложность

- Для человека (2 из 5): API похож на NumPy, примеров много. Красивая сцена с трубками и подсветкой — несколько часов работы.
- Для агента (1 из 5): кодом, кадр сохраняется в PNG и агент его просматривает. Руки не нужны.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): скрипты, безголовый рендер, цикл кадров, ничего не требует интерфейса.
- Воспроизводимость (4 из 5): код под git, одинаковые данные дают одинаковую геометрию. Пиксели могут отличаться при смене драйвера или версии VTK, поэтому не 5.

## Платформа и оборудование

Python 3.10+, Linux, macOS, Windows. На сервере без GPU работает через EGL и llvmpipe. Видеокарта ускоряет рендер, обязательной не является.

## Экспорт

PNG (скриншоты, в том числе с прозрачным фоном), mp4 через ffmpeg, GIF. Интерактивный просмотр в Jupyter идёт через trame. Сетки читаются и пишутся во многих форматах, в том числе VTK для ParaView. Разрешение задаётся `window_size`.

## Стоимость

Проверено 2026-10-14. Бесплатно, открытый код под MIT. Коммерческий куратор проекта — CoDimensional PBC. Платных функций в проверенных страницах не упомянуто.

## Лицензия и права

- Код или программа: MIT ([README](https://github.com/pyvista/pyvista), LICENSE).
- Результат: лицензия MIT не накладывает условий на картинки и ролики.
- Ассеты в комплекте: набор встроенных примеров данных скачивается отдельно (библиотека `pooch`). Условия каждого набора данных свои, для ролика нужны собственные данные.

## Активность и зрелость

<!-- gh-stats:pyvista/pyvista -->
- Звёзды GitHub: 3 848
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.49.1 (2026-10-11)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория pyvista/pyvista, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: stable. Версия 0.49.1 вышла 2026-10-11, до неё 0.49.0 (2026-09-08), 0.48.4 и 0.48.3 (май 2026). Проект под зонтом NumFOCUS, API держат стабильным через цикл устаревания (по описанию проекта).

## Когда брать и когда нет

- Брать: 3D-поле, линии тока, облёт камеры, всё из Python одним скриптом, соединение с Magpylib.
- Не брать: нужны тонкие свет и материалы, сложные композиции — тогда [blender](blender.md). Нужен огромный набор фильтров и готовых интерфейсов — тогда [paraview](paraview.md).

## Источники

- [PyVista: документация](https://docs.pyvista.org/) — назначение, MIT, партнёры, версии Python. Проверено 2026-10-14.
- [Установка PyVista](https://docs.pyvista.org/getting-started/installation.html) — безголовый рендер VTK 9.5+, imageio-ffmpeg для видео. Проверено 2026-10-14.
- [Plotter.open_movie](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.open_movie.html) — framerate 24, quality 5, нужен imageio. Проверено 2026-10-14.
- [Plotter.screenshot](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.screenshot.html) — параметр transparent_background. Проверено 2026-10-14.
- [Plotter.orbit_on_path](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.orbit_on_path.html) — облёт камеры. Проверено 2026-10-14.
- [imageio: плагин ffmpeg](https://imageio.readthedocs.io/en/stable/_autosummary/imageio.plugins.ffmpeg.html) — для mp4 нужен `imageio[ffmpeg]`. Проверено 2026-10-14.
- [PyVista на PyPI](https://pypi.org/pypi/pyvista/json) — версии, зависимости, даты. Проверено 2026-10-14.
- [Magpylib: Pyvista 3D Field Lines](https://magpylib.readthedocs.io/en/latest/_pages/user_guide/examples/examples_vis_pv_streamlines.html) — линии поля магнита. Проверено 2026-10-14.

## Неизвестно

- Скорость рендера кадров 1920×1080 с трубками линий на программном рендере: код не запускался.
- Точные условия на встроенные наборы данных из `pooch`: не проверялись.
- Есть ли в PyVista готовый «растущий» штрих линии тока: в документации не найден, делается вручную.
