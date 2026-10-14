---
id: makie
name: Makie.jl
class: [simulation]
kind: library
site: https://docs.makie.org/stable/
github: MakieOrg/Makie.jl
scenes: [graph, field, simulation]
quality: 4
human_difficulty: 3
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [mp4, mkv, webm, gif, svg, png-sequence]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Makie.jl

Графическая экосистема языка Julia: быстрые интерактивные 2D и 3D графики и анимации на видеокарте (GLMakie), векторная графика для публикаций (CairoMakie), WebGL в браузере (WGLMakie) и экспериментальная трассировка лучей (RPRMakie). Анимация пишется функцией `record`.

## Ссылки

- Официальный сайт и документация: <https://docs.makie.org/stable/>
- GitHub: <https://github.com/MakieOrg/Makie.jl>
- Галерея: <https://beautiful.makie.org/>
- Анимации: <https://docs.makie.org/stable/explanations/animation>
- Примеры, проверенные 2026-10-14:
  - [Streamplot](https://docs.makie.org/stable/reference/plots/streamplot) — линии потока функции-поля в 2D и 3D (подходит для линий поля).
  - [Making animations and interactive applications in Makie.jl](https://www.youtube.com/watch?v=L-gyDvhjzGQ) — урок канала JuliaDynamics, около 19 минут.
  - [Live flow simulation tutorial with Waterlily.jl and Makie.jl](https://www.youtube.com/watch?v=OO0Nz3uWDc8) — расчёт обтекания с живой анимацией (канал Gabe Weymouth), около 18 минут.
  - [What's new with Makie.jl?](https://www.youtube.com/watch?v=rNSmnlNP1J4) — доклад авторов, JuliaCon 2024, около 7 минут.
  - [Beautiful Makie](https://beautiful.makie.org/) — галерея работ на Makie (страница открывается, содержимое галереи не вычитывалось).

## Что реально получается

Сквозной пример (магнит на холодильнике). Готового магнитного пакета для Julia в проверенных страницах не нашли. Поле либо считается аналитически собственным кодом, либо приходит из внешней программы ([femm](femm.md), [magpylib](magpylib.md), [elmer-fem](elmer-fem.md)). Makie рисует карту поля (`heatmap`, `contourf`), стрелки (`arrows`), линии (`streamplot`). Для магнитов Python удобнее: там есть Magpylib.

Что даёт для объясняющего видео:

- Модель анимации: графические атрибуты связаны с `Observable`. Меняете время или параметр, и картинка обновляется. Это очень удобно для непрерывных сцен и плавных изменений.
- `record(fig, "file.mp4", кадры; framerate = 30) do t ... end` пишет видео. Форматы: `.mkv` (по умолчанию, без конвертации), `.mp4`, `.webm` (самый маленький), `.gif` (самое низкое качество). Кодирование делает FFMPEG_jll, отдельно ставить ffmpeg не нужно.
- Камера: 3D-сцены LScene и Axis3, положение и поворот камеры меняются из кода (`translate_cam!`, `rotate_cam!`, страница [Cameras](https://docs.makie.org/stable/explanations/cameras)). Движение камеры на кадрах `record` в документации не показано.
- Качество: GLMakie даёт гладкую картинку на GPU. CairoMakie выдаёт вектор высокого качества для кадров. RPRMakie даёт трассировку лучей, помечена экспериментальной.
- Рисование линий: линия растёт, если добавлять точки в `Observable` (пример «Appending data»).
- Голос: нет. Время кадров задаётся кодом.

## Слабые стороны

- Julia менее распространён, чем Python. Готовых пакетов для магнитов и FEM меньше.
- GLMakie требует OpenGL 3.3 и выше. На сервере без GPU — через виртуальный дисплей `xvfb` (так в CI Makie) или VirtualGL.
- RPRMakie падает на macOS при создании контекста (по документации), на Apple silicon нужна сборка Julia под x86_64.
- Первый запуск и компиляция пакетов медленные (Julia), задержка перед первым кадром. Измерений для этой карточки нет.
- Запись через CairoMakie в проверенных страницах не показана, все примеры анимаций на GLMakie.

## Сложность

- Для человека (3 из 5): Makie проще многих, но нужен Julia. Работа с `Observable` непривычна, зато даёт чистые анимации.
- Для агента (2 из 5): всё кодом. Установка Julia и GPU или xvfb усложняет настройку, затем рендер и проверка полностью автоматические.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): скрипт Julia, `record`, безголовые окружения (xvfb).
- Воспроизводимость (4 из 5): код и `Project.toml` с версиями под git. Растровый вывод GLMakie зависит от драйвера и GPU.

## Платформа и оборудование

Windows, Linux, macOS. GLMakie нужен OpenGL 3.3+. WGLMakie работает в браузере. RPRMakie — Windows и Linux, на macOS не работает без обходных путей.

## Экспорт

Видео: mkv, mp4, webm, gif через `record`. Кадры: PNG через `save`. Вектор: SVG и PDF в CairoMakie. Прозрачный фон описан в разделе «How to save a figure with transparency».

## Стоимость

Проверено 2026-10-14. Бесплатно, открытый код.

## Лицензия и права

- Код или программа: MIT (файл LICENSE.md репозитория: The MIT License, 2018–2021 Simon Danisch, Julius Krumbiegel).
- Результат: MIT не накладывает условий на картинки и ролики.
- Ассеты в комплекте: шрифты и цветовые схемы входят в пакеты. Отдельных условий не проверяли.

## Активность и зрелость

<!-- gh-stats:MakieOrg/Makie.jl -->
- Звёзды GitHub: 2 821
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.24.16 (2026-10-13)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория MakieOrg/Makie.jl, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: stable. Последний тег на GitHub v0.24.16 (регулярные релизы 0.24.x в 2026 году). Версия 0.x, но проект живой. Авторы по статье JOSS 2021 года — Simon Danisch и Julius Krumbiegel.

## Когда брать и когда нет

- Брать: команда уже работает на Julia, нужна чистая анимация данных с гладкой камерой, расчёт и графика в одном языке.
- Не брать: нужен готовый пакет магнитов и стандарт экосистемы — Python со связкой [magpylib](magpylib.md) и [matplotlib](matplotlib.md) или [pyvista](pyvista.md). Для сложной анимации объектов и формул — [manim-ce](manim-ce.md).

## Источники

- [Makie.jl на GitHub](https://github.com/MakieOrg/Makie.jl) — назначение, бэкенды, лицензия MIT. Проверено 2026-10-14.
- [Makie: Animations](https://docs.makie.org/stable/explanations/animation) — `record`, форматы, Observables. Проверено 2026-10-14.
- [Makie: Headless](https://docs.makie.org/stable/explanations/headless) — xvfb, VirtualGL, WGLMakie. Проверено 2026-10-14.
- [GLMakie](https://docs.makie.org/stable/explanations/backends/glmakie) — OpenGL 3.3+. Проверено 2026-10-14.
- [CairoMakie](https://docs.makie.org/stable/explanations/backends/cairomakie) — вектор SVG и PDF. Проверено 2026-10-14.
- [RPRMakie](https://docs.makie.org/stable/explanations/backends/rprmakie) — трассировка лучей, экспериментальный бэкенд, проблемы на macOS. Проверено 2026-10-14.
- [Релизы Makie.jl на GitHub](https://github.com/MakieOrg/Makie.jl/releases) — тег v0.24.16. Проверено 2026-10-14.
- [LICENSE.md](https://raw.githubusercontent.com/MakieOrg/Makie.jl/master/LICENSE.md) — MIT. Проверено 2026-10-14.

## Неизвестно

- Есть ли для Julia готовый пакет расчёта поля постоянных магнитов: не искали глубоко.
- Скорость компиляции и рендера: измерений нет.
- Дата последнего релиза: по странице релизов последний тег v0.24.16, точную дату не фиксировали.
- Условия на шрифты, входящие в пакеты: не проверялись.
