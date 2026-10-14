---
id: mathbox
name: MathBox
class: [web-graphics]
kind: library
site: https://mathbox.org
github: unconed/mathbox
scenes: [formula, graph, field]
quality: 4
human_difficulty: 4
agent_difficulty: 3
automation: 3
reproducibility: 4
cost: 0
maturity: abandoned
platforms: [web]
export: [html]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# MathBox

WebGL-библиотека Стивена Виттенса для математической графики. Строится на Three.js и ShaderGraph; сцена описывается деревом элементов, как разметка. Создана для объясняющих презентаций: диаграмма наращивается постепенно, а не меняется слайдами. Разработка остановлена; автор перешёл на Use.GPU.

## Ссылки

- Официальный сайт: https://mathbox.org (демо и тесты)
- GitHub: https://github.com/unconed/mathbox
- Документация: отдельной страницы справочника на mathbox.org нет; описание идей в статье https://acko.net/blog/mathbox2/, примеры в каталоге `examples` репозитория.
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики не смотрел):
  - [Quaternion Hypersphere](https://mathbox.org/math/quat.html) — демо «Quaternion Hypersphere» из README, интерактивное.
  - [Hopf](https://mathbox.org/math/hopf.html) — демо из раздела Math на mathbox.org.
  - [Audio Visualizer](https://mathbox.org/demo/audio-visualizer.html) — визуализатор звука (демо из README).
  - [Volumetric Vectors](https://mathbox.org/test/volume.html) — демо «Volumetric Vectors» из README.
  - [Making WebGL Dance](https://acko.net/tv/webglmath) — доклад автора (JSConf US 2013) о выборке, линейных преобразованиях и шейдерах.
  - [The Pixel Factory](https://acko.net/files/gltalks/pixelfactory/online.html) — презентация автора, на которую ссылается README.

## Что реально получается

- Формулы и графики в 3D: оси, сетки, кривые, поверхности, точки, векторы, подписи с LaTeX. Каталог демо на mathbox.org включает примеры «Cartesian4», «Surface», «Vector», «Ticks», «Stereographic», «Hopf», «Quat». Сцены `formula`, `graph`, `field`.
- Анимация как математика: статья 2015 года описывает анимацию «по настоящим моделям, а не морфингом картинок»; каждый кадр — корректный пример. Тесты Play, Transition, Grow, Lerp на mathbox.org показывают переходы параметров.
- Презентация: элемент `present` рассчитан на слайды, где диаграмма наращивается. Виттенс критикует «PowerPoint syndrome», когда слайд выбрасывает контекст предыдущего.
- Камера: орбитальная камера Three.js (`camera` в списке тестов).
- Типографика, рисование от руки, голос: нет.
- Непрерывность: сильная сторона — объекты и данные остаются в сцене, меняются параметры.
- Потолок качества (4 из 5): фирменный вид математических диаграмм, подходящий для объясняющих сцен; мешают заброшенность и ручная правка версий.

## Слабые стороны

- Проект заброшен. Последний релиз на GitHub — v2.3.1 (2023-01-21), последний коммит — 2023-01-25, последняя публикация в npm — 2.3.2-rc1 (2023-05-05). Статья автора помечает MathBox как вытесненный Use.GPU.
- Совместимость с Three.js: `peerDependencies` требуют `three >= 0.118.0`, в разработке закреплена 0.139.2, README показывает CDN-версию 0.137.0. Работа с текущим r186 не проверена и вероятно требует правок.
- Небольшая документация, мало примеров от сообщества. Агенту и человеку придётся читать исходники демо.
- Записи видео нет, нужен внешний захват: [ccapture-js](ccapture-js.md), [remotion](remotion.md).
- Только WebGL, без WebGPU.

## Сложность

- Для человека (4 из 5): нужны JavaScript, Three.js, представление о данных на GPU (массивы, операторы) и немного GLSL для нестандартных вещей. Документации мало.
- Для агента (3 из 5): код целиком, но данных для обучения мало, ошибки версий Three.js придётся чинить вручную. Результат проверяется скриншотами.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): сборки видео нет; запись делает внешний захват. Сцена — обычная веб-страница.
- Воспроизводимость (4 из 5): проект — текст под git. Состояние можно вести по времени, подаваемому снаружи. Проверка запуском не проводилась.

## Платформа и оборудование

Браузер с WebGL и видеокартой. Установка через npm (`npm install mathbox three`) или через CDN.

## Экспорт

Сама библиотека видео не экспортирует. Результат — веб-страница; видео и кадры даёт внешний захват.

## Стоимость

Проверено 2026-10-14 по [LICENSE.md](https://github.com/unconed/mathbox/blob/master/LICENSE.md). Бесплатно.

## Лицензия и права

- Код или программа: MIT («Copyright (C) 2013+ Steven Wittens and contributors»; README также называет ShaderGraph).
- Результат: ограничений на ролики, коммерцию и монетизацию в тексте MIT нет.
- Ассеты в комплекте: демо используют свои данные и текстуры; условия не проверял.

## Активность и зрелость

<!-- gh-stats:unconed/mathbox -->
- Звёзды GitHub: 1 505
- Последний коммит в основной ветке: 2023-01-25
- Последний релиз или тег: v2.3.1 (2023-01-21)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория unconed/mathbox, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `abandoned` по правилу методики (нет релизов и коммитов больше двух лет). Релизы: v2.3.1 и v2.3.0 (оба 2023-01-21). Последний коммит — 2023-01-25. Преемник автора — [Use.GPU](https://usegpu.live) (WebGPU, бета, лицензия пакетов MIT).

## Когда брать и когда нет

- Брать: если нужна именно эстетика математических диаграмм Виттенса, а команда готова заморозить версию Three.js вокруг MathBox и чинить код. Для показа на странице, а не для долгой поддержки.
- Не брать: как основу библиотеки. Для видео в Python лучше [manim-ce](manim-ce.md) или [manimgl](manimgl.md); для веб-математики без поддержки старой версии — присмотреться к Use.GPU (карточки нет).

## Источники

- [Репозиторий MathBox](https://github.com/unconed/mathbox) — описание «Presentation-quality WebGL math graphing», MIT, список демо. Проверено 2026-10-14.
- [README](https://raw.githubusercontent.com/unconed/mathbox/master/README.md) и [package.json](https://raw.githubusercontent.com/unconed/mathbox/master/package.json) — зависимости от Three.js, версия 2.3.1. Проверено 2026-10-14.
- [Лента релизов](https://github.com/unconed/mathbox/releases.atom), [лента коммитов](https://github.com/unconed/mathbox/commits/HEAD.atom), [npm: mathbox](https://registry.npmjs.org/mathbox) — даты релизов и коммитов. Проверено 2026-10-14.
- [mathbox.org](https://mathbox.org) — список демо и тестов. Проверено 2026-10-14.
- [MathBox² (acko.net)](https://acko.net/blog/mathbox2/) — устройство библиотеки, анимация по моделям, слайды, примечание о Use.GPU. Проверено 2026-10-14.
- [Use.GPU](https://usegpu.live) и [@use-gpu/core на npm](https://registry.npmjs.org/@use-gpu/core) — бета, версия 0.20.0 (2026-07-16), MIT. Проверено 2026-10-14.

## Неизвестно

- Работает ли MathBox 2.3.1 с Three.js r186: не проверял, код не запускался.
- Есть ли живые форки MathBox: не искал, ссылок на форки нет.
- Условия на данные и текстуры демо не изучал.
- Лицензия самого Use.GPU: сайт её не указывает; MIT взята из метаданных npm-пакета `@use-gpu/core`.
