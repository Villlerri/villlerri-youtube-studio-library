---
id: javis-jl
name: Javis.jl
class: [2d-code]
kind: library
site: https://juliaanimators.github.io/Javis.jl/stable/
github: JuliaAnimators/Javis.jl
scenes: [diagram, drawing]
quality: 2
human_difficulty: 3
agent_difficulty: 3
automation: 4
reproducibility: 4
cost: 0
maturity: abandoned
platforms: [linux, macos, windows]
export: [gif, mp4]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Javis.jl

Библиотека на Julia для простых анимаций и визуализаций: объекты и действия над ними поверх Luxor и Cairo. Авторы называют вдохновением ролики 3Blue1Brown. Проект не развивается с 2022 года.

## Ссылки

- Документация: https://juliaanimators.github.io/Javis.jl/stable/
- GitHub: https://github.com/JuliaAnimators/Javis.jl
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел):
  - [Первая анимация](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_1/) — красный шар движется по сцене, результат GIF.
  - [Рендер LaTeX](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_4/) — формула из LaTeX через Node-пакет `mathjax-node-cli`.
  - [Талисман Jarvis](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_5/) — появление, исчезновение и перемещение объектов с затуханием.
  - [Следование за путём](https://github.com/JuliaAnimators/Javis.jl/blob/master/examples/follow_path.jl) и [контур логотипа Julia через ряд Фурье](https://github.com/JuliaAnimators/Javis.jl/blob/master/examples/fourier.jl) — код примеров из галереи README.

## Что реально получается

- Модель «объект и действия»: `Object` рисует функцию на отрезке кадров, `Action` меняет его (появление `appear`, исчезновение `disappear`, `rotate_around`, `follow_path`, `change`, обратное воспроизведение `rev`). Хватает для схем и простых траекторий.
- Морфинг: `morph_to` превращает одну форму в другую. Исходный код предупреждает: работает только для простых форм, не для нескольких полигонов и не для заливок.
- Рисование линий: через Luxor и действие по пути; готового «рисования контура» как в Manim не нашёл.
- Формулы: LaTeX через Node-пакет `mathjax-node-cli`. Нативного LaTeX в Julia нет (документация).
- Камера, непрерывная сцена и плавные переходы между сценами: отдельных средств не нашёл. Всё живёт в одном `Video` с кадрами.
- Типографика и голос: текст можно рисовать, синхронизации с озвучкой нет.
- В примерах и галерее README результат — небольшие GIF. Уровня роликов 3Blue1Brown или Motion Canvas в примерах нет.

## Слабые стороны

- Проект заброшен: релиз 0.9.0 от 2022-05-26, последний коммит 2022-10-06.
- В трекере открыты ошибки установки и загрузки на новых версиях: precompile (январь 2023), ошибка Gtk (август 2023), неопределённые `Javis.Background` и `@JShape` (октябрь 2023). Работает ли пакет на текущей версии Julia, не проверял.
- Для LaTeX нужен Node.js и пакет из npm.
- Нет редактора, переходов, камеры и средств под озвучку.
- Мало примеров и мало сообщества по сравнению с [manim-ce](manim-ce.md).

## Сложность

- Для человека (3 из 5): нужны Julia и знание Luxor; задача простая, но документация старая, примеры могут не запускаться.
- Для агента (3 из 5): код на Julia агент пишет и запускает из командной строки (`render(...)` пишет GIF или MP4). Риск: пакет может не собираться на свежей версии Julia, и тогда чинить зависимости придётся вручную.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): сцена — скрипт Julia, `render(video; pathname="x.mp4")`, параметры `framerate`, `ffmpeg_loglevel`. Есть режим стриминга. Пакетный рендер скриптом.
- Воспроизводимость (4 из 5): код под git, `Project.toml` фиксирует зависимости. Через несколько лет зависимости (Cairo, Gtk, VideoIO) могут не собраться.

## Платформа и оборудование

Julia (в документации Julia 1.7), Cairo, Luxor, FFmpeg через пакет. Для LaTeX нужен Node.js. Работает на Linux, macOS, Windows, видеокарта не нужна.

## Экспорт

GIF и MP4 (расширение выбирается по имени файла в `render`). В туториалах чаще GIF. Прозрачный фон и последовательность кадров в прочитанной документации не описаны.

## Стоимость

Проверено 2026-10-14 по [документации](https://juliaanimators.github.io/Javis.jl/stable/). Бесплатно.

## Лицензия и права

- Код или программа: MIT (Ole Kröger и участники, 2020).
- Результат: MIT не накладывает ограничений на анимации, монетизацию и водяные знаки.
- Ассеты в комплекте: GIF-иллюстрации в README и документации; их условия не проверял.

## Активность и зрелость

<!-- gh-stats:JuliaAnimators/Javis.jl -->
- Звёзды GitHub: 845
- Последний коммит в основной ветке: 2022-08-09
- Последний релиз или тег: v0.9.0 (2022-05-26)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория JuliaAnimators/Javis.jl, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `abandoned`. Последний релиз по ленте GitHub и реестру Julia General — 0.9.0 (2022-05-26). Последний коммит основной ветки — 2022-10-06. Документация собрана 2022-05-26 на Julia 1.7.3. Последняя активность в issue — октябрь 2023. Заявлений о закрытии проекта нет. По идее родственна [manim-ce](manim-ce.md), но намного меньше.

## Когда брать и когда нет

- Брать: только для экспериментов на Julia, если задача проста и пакет собирается.
- Не брать: для рабочего канала. Для того же круга задач лучше [manim-ce](manim-ce.md) или [motion-canvas](motion-canvas.md); для научной визуализации на Julia смотрите [makie](makie.md).

## Источники

- [README](https://github.com/JuliaAnimators/Javis.jl) — назначение, галерея, установка, LaTeX через Node. Проверено 2026-10-14.
- [Документация](https://juliaanimators.github.io/Javis.jl/stable/) и [туториал 1](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_1/), [4](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_4/), [5](https://juliaanimators.github.io/Javis.jl/stable/tutorials/tutorial_5/) — дата сборки, `render`, формат. Проверено 2026-10-14.
- [Исходный код `Javis.jl`](https://github.com/JuliaAnimators/Javis.jl/blob/master/src/Javis.jl) и [`morphs.jl`](https://github.com/JuliaAnimators/Javis.jl/blob/master/src/morphs.jl) — GIF и MP4, ограничения морфинга. Проверено 2026-10-14.
- [Релизы](https://github.com/JuliaAnimators/Javis.jl/releases), [коммиты](https://github.com/JuliaAnimators/Javis.jl/commits/master) и [реестр Julia General](https://github.com/JuliaRegistries/General/tree/master/J/Javis) — версия 0.9.0, даты. Проверено 2026-10-14.
- [Issue 499](https://github.com/JuliaAnimators/Javis.jl/issues/499), [497](https://github.com/JuliaAnimators/Javis.jl/issues/497), [501](https://github.com/JuliaAnimators/Javis.jl/issues/501) — ошибки на новых версиях. Проверено 2026-10-14 (читал только названия).
- [LICENSE](https://github.com/JuliaAnimators/Javis.jl/blob/master/LICENSE) — MIT. Проверено 2026-10-14.

## Неизвестно

- Запускается ли пакет на текущей версии Julia: код не запускался.
- Есть ли ответы мейнтейнеров в трекере: читал только названия issue.
- Прозрачный вывод и последовательность кадров не описаны в прочитанных страницах.
