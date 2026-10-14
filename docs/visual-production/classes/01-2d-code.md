# Программная 2D-анимация (код)

## Что сюда входит

Сцену описывают кодом, видео получают рендером. Сюда относятся математические движки (Manim), TypeScript-движки с редактором или без него (Motion Canvas, Canvas Commons, Revideo), видео из React (Remotion) и из HTML (HyperFrames), анимация в браузере (GSAP, Theatre.js, Lottie) и единичный проект на Julia (Javis.jl). Объект остаётся в кадре и меняется: этим класс отличается от монтажа готовых картинок. Проект — текст под git, поэтому класс удобен агенту и повторяемым сериям.

## Когда этот класс нужен

- Вывод формул и преобразований: символы перетекают друг в друга, а не мигают (`formula`).
- Графики функций и данных, которые строятся и меняются на глазах (`graph`).
- Схемы и процессы, где блок, стрелка и подпись появляются вместе с фразой диктора (`diagram`).
- Поля, потоки и волны, показанные векторами и линиями (`field`).
- Рисование линий «вживую»: контур вырастает, пока идёт объяснение (`drawing`).
- Заголовки, цитаты, подписи по словам (`typography`).
- Код и экран компьютера как графика (`screen`).
- Сквозная сцена с плавным движением камеры вместо серии кадров одного плана и жёстких склеек.

## Основные решения

- [Manim Community Edition](../tools/manim-ce.md) — Python-движок для формул, графиков и полей; стабильный API, команда для агента, озвучка через плагин. Первый выбор для математики.
- [ManimGL](../tools/manimgl.md) — инструмент самого 3Blue1Brown, OpenGL и интерактивная оболочка; лучший вид, но установка из исходников и нестабильный API.
- [Motion Canvas](../tools/motion-canvas.md) — TypeScript и редактор с метками времени под озвучку; сильные переходы между сценами, но релизов нет с февраля 2025 года, официального заявления о прекращении нет.
- [Canvas Commons](../tools/canvas-commons.md) — активный MIT-форк Motion Canvas (0.4.0 от 2026-09-24): редактор меток под озвучку, камера, переходы, переход с оригинала заменой имён пакетов; безголового рендера не подтверждено, поддерживает в основном один автор.
- [Remotion](../tools/remotion.md) — видео из React с серверным рендером и пакетами для three.js, Lottie, GSAP, субтитров; платная лицензия для команд от 4 человек.
- [HyperFrames](../tools/hyperframes.md) — видео из обычного HTML с GSAP, Lottie и three.js; детерминированный рендер через headless Chrome и FFmpeg, навыки для агентов, Apache-2.0 без платы за рендер; молодой проект, версия 0.8, точный кадр только в Linux или Docker.
- [Revideo](../tools/revideo.md) — форк Motion Canvas для безголового рендера и шаблонных роликов; версия 0.x, проект перешёл к компании Midrender.
- [Theatre.js](../tools/theatre-js.md) — редактор кривых для сцен three.js в браузере; видео не рендерит, публичная разработка остановлена.
- [GSAP](../tools/gsap.md) — таймлайны, рисование и морфинг SVG, анимация текста; бесплатна с 2025 года, видео только через обёртку.
- [Lottie](../tools/lottie.md) — формат и проигрыватели для готовых клипов из After Effects; хорош для вставок, не для непрерывных сцен.
- [Javis.jl](../tools/javis-jl.md) — анимации на Julia; не обновлялся с 2022 года, для работы не годится.

## Сравнение

Оценки взяты из карточек, шкалы описаны в [методике](../method.md).

- Потолок качества. Выше всех [ManimGL](../tools/manimgl.md) (5): эталон 3Blue1Brown. Следом [Manim CE](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md), [Canvas Commons](../tools/canvas-commons.md), [Remotion](../tools/remotion.md), [HyperFrames](../tools/hyperframes.md), [GSAP](../tools/gsap.md), [Theatre.js](../tools/theatre-js.md) (по 4). У Remotion, HyperFrames и GSAP потолок задаёт дизайн автора: готовых математических или научных примитивов нет. [Revideo](../tools/revideo.md) и [Lottie](../tools/lottie.md) (по 3): нет примеров научно-популярного уровня или это формат для вставок. [Javis.jl](../tools/javis-jl.md) (2): простые формы и GIF.
- Трудность для человека. Легче остальных вход в [Manim CE](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md), [Canvas Commons](../tools/canvas-commons.md), [Remotion](../tools/remotion.md), [HyperFrames](../tools/hyperframes.md), [GSAP](../tools/gsap.md), [Revideo](../tools/revideo.md), [Lottie](../tools/lottie.md), [Javis.jl](../tools/javis-jl.md) (по 3): Python, TypeScript, HTML или Julia, недели до своего стиля. Тяжелее [ManimGL](../tools/manimgl.md) (установка из исходников, OpenGL, короткая документация) и [Theatre.js](../tools/theatre-js.md) (кривые и ключи вручную) — по 4.
- Трудность для агента. Проще всего [Manim CE](../tools/manim-ce.md), [Remotion](../tools/remotion.md) и [HyperFrames](../tools/hyperframes.md) (1): код, командный рендер, у Remotion есть документация для агентов, у HyperFrames 21 навык для агентов. [ManimGL](../tools/manimgl.md) и [Revideo](../tools/revideo.md) (2): рендер кодом, но нужен OpenGL-контекст или есть скудные документы. [Motion Canvas](../tools/motion-canvas.md) и [Canvas Commons](../tools/canvas-commons.md) (3): метки под голос двигают мышью, командного рендера нет (у Canvas Commons безголовый рендер не подтверждён). [GSAP](../tools/gsap.md) (3) требует обвязки для видео, [Lottie](../tools/lottie.md) (3) создаётся в After Effects, [Javis.jl](../tools/javis-jl.md) (3) может не собраться. [Theatre.js](../tools/theatre-js.md) (4): ключи в Studio вручную и нет экспорта.
- Автоматизация. Максимум у [Manim CE](../tools/manim-ce.md), [Remotion](../tools/remotion.md) и [HyperFrames](../tools/hyperframes.md) (5): командная строка, пакетный и облачный рендер (Docker, Lambda; у HyperFrames Docker и облако HeyGen). [ManimGL](../tools/manimgl.md), [Revideo](../tools/revideo.md), [Javis.jl](../tools/javis-jl.md) (4): рендер скриптом. [GSAP](../tools/gsap.md) и [Lottie](../tools/lottie.md) (3): видео получается только с [Remotion](../tools/remotion.md) или [HyperFrames](../tools/hyperframes.md). [Motion Canvas](../tools/motion-canvas.md), [Canvas Commons](../tools/canvas-commons.md) и [Theatre.js](../tools/theatre-js.md) (2): нет командного рендера.
- Стоимость. Бесплатны: [Manim CE](../tools/manim-ce.md), [ManimGL](../tools/manimgl.md), [Motion Canvas](../tools/motion-canvas.md), [Canvas Commons](../tools/canvas-commons.md), [Revideo](../tools/revideo.md), [Theatre.js](../tools/theatre-js.md), [GSAP](../tools/gsap.md) (с 2025 года полностью, включая плагины), [Javis.jl](../tools/javis-jl.md), [HyperFrames](../tools/hyperframes.md) (Apache-2.0, плата за рендер не нужна; облачный рендер HeyGen требует аккаунта, цена неизвестна). [Remotion](../tools/remotion.md): бесплатно для одиночек и команд до 3 человек, дальше от $25 в месяц за место или от $100 в месяц за рендеры, Enterprise от $500. [Lottie](../tools/lottie.md): проигрыватели бесплатны, создание в After Effects или LottieFiles (от $19.99 в месяц).
- Плавность переходов и непрерывность сцены. Лучше всего в [Manim CE](../tools/manim-ce.md) и [ManimGL](../tools/manimgl.md): одна сцена, объекты остаются в кадре, `TransformMatchingTex` и `TransformMatchingShapes` перетекают части формул, камера двигается через `camera.frame` или `self.frame`. [Motion Canvas](../tools/motion-canvas.md), [Canvas Commons](../tools/canvas-commons.md) и [Revideo](../tools/revideo.md): генераторы без склеек, переходы `slideTransition`, `zoomInTransition` и свои, с `finishScene()` анимация идёт сквозь стык; узел `Camera`; формулы перетекают в узле `Latex`. [Remotion](../tools/remotion.md): `TransitionSeries` и `evolvePath()` для линий, превращение объектов строится вручную. [HyperFrames](../tools/hyperframes.md): одна страница с одним таймлайном GSAP, шейдерные переходы и переходы на CSS, камера как масштаб обёртки или камера Three.js; готового ролика с морфингом сложных форм в проверенных источниках нет. [GSAP](../tools/gsap.md): вложенные таймлайны, DrawSVG и MorphSVG. [Theatre.js](../tools/theatre-js.md): плавная камера по кривым в 3D, но без вывода в видео. [Lottie](../tools/lottie.md): отдельные клипы без камеры. [Javis.jl](../tools/javis-jl.md): один видеообъект, морфинг только простых форм.

## Другие решения

- manim-slides — https://manim-slides.eertmans.be/latest/ — презентации из сцен Manim с показом в окне или браузере (MIT); версия 5.7.0 от 2026-09-14.
- Reanimate — https://reanimate.github.io/ — декларативные SVG-анимации на Haskell; последний релиз 2022 года, последний коммит 2025-02.
- Penrose — https://penrose.cs.cmu.edu/ — статичные диаграммы по тексту математической записи (MIT); не анимация, но полезно для схем.
- Asymptote — https://asymptote.sourceforge.io/ — язык векторной графики для математических чертежей с подписями в LaTeX; модуль `animation` склеивает кадры в GIF или MPEG через ImageMagick, модуль `animate` даёт PDF-анимацию.
- TikZ и пакет animate — https://tikz.dev/ и https://ctan.org/pkg/animate — анимации PDF и SVG из кадров TikZ в LaTeX; для статей и презентаций, не для видео на YouTube.
- Motion (motion.dev) — https://motion.dev/ — библиотека анимации интерфейсов для JavaScript, React и Vue (бывший Framer Motion, MIT); видео не рендерит.
- Anime.js — https://animejs.com/ — лёгкий движок анимации для JavaScript; видео не рендерит.
- Mafs — https://mafs.dev/ — React-компоненты для интерактивной математики (графики, векторы, MIT); последний релиз 2024-10, для веба, не для видео.
- Animotion — https://animotion.pages.dev/ (код: https://github.com/animotionjs/animotion) — презентации на Svelte и Reveal.js с анимацией кода; релиз 2026-07-23. Сайт animotion.dev — другой проект (японская коллекция интерфейсных анимаций), не этот.
- Diffusion Studio Core — https://github.com/diffusionstudio/core — композитинг видео в браузере на WebCodecs (MPL-2.0); последний релиз 2.0.0 от 2025-02-01.

## Вывод для объясняющих видео

Для сцен с формулами, графиками, полями и схемами первым берите [Manim CE](../tools/manim-ce.md): одна непрерывная сцена, морфинг формул, движение камеры, озвучка через [manim-voiceover](../tools/manim-voiceover.md), и всё делает агент из командной строки. Для сборки итогового видео с титрами, данными, Lottie, three.js и серверным рендером берите [Remotion](../tools/remotion.md), с оговоркой про лицензию для команд от 4 человек; без неё и с обычным HTML вместо React — [HyperFrames](../tools/hyperframes.md), но проект молодой и точный кадр даёт только Linux или Docker. Если нужен редактор меток под голос, используйте [Motion Canvas](../tools/motion-canvas.md) с зафиксированной версией или его активный форк [Canvas Commons](../tools/canvas-commons.md). [ManimGL](../tools/manimgl.md) оставьте человеку, который хочет вид 3Blue1Brown и работает в окне. [Lottie](../tools/lottie.md) и [GSAP](../tools/gsap.md) годятся как вставки, [Theatre.js](../tools/theatre-js.md) и [Javis.jl](../tools/javis-jl.md) для нового канала не берите. Плавность и непрерывность дают Manim (одна сцена с превращениями) и Motion Canvas (переходы без заморозки сцены): против прошлых дёрганых склеек именно они.

## Источники

- [manim-slides](https://manim-slides.eertmans.be/latest/) и [GitHub](https://github.com/jeertmans/manim-slides) — назначение, версия 5.7.0, MIT. Проверено 2026-10-14.
- [Reanimate](https://reanimate.github.io/) и [GitHub](https://github.com/reanimate/reanimate) — Haskell и SVG, релиз 1.1.5.0 от 2022-01-24, коммит 2025-02-06. Проверено 2026-10-14.
- [Penrose](https://penrose.cs.cmu.edu/) и [GitHub](https://github.com/penrose/penrose) — диаграммы по записи, релиз 3.3.1 от 2026-08-30, MIT. Проверено 2026-10-14.
- [Asymptote](https://asymptote.sourceforge.io/) и [модуль animation](https://asymptote.sourceforge.io/doc/animation.html) — язык, анимации GIF, MPEG, PDF. Проверено 2026-10-14.
- [CTAN: animate](https://ctan.org/pkg/animate) и [TikZ](https://tikz.dev/) — PDF и SVG анимации из кадров. Проверено 2026-10-14.
- [Motion](https://motion.dev/) и [GitHub](https://github.com/motiondivision/motion) — библиотека анимации, версия 14.2.0 от 2026-10-13, MIT. Проверено 2026-10-14.
- [Anime.js](https://animejs.com/) — «лёгкая многоцелевая библиотека анимации». Проверено 2026-10-14.
- [Mafs](https://mafs.dev/) и [GitHub](https://github.com/stevenpetryk/mafs) — React-компоненты для математики, релиз 2024-10-20, MIT. Проверено 2026-10-14.
- [Animotion](https://animotion.pages.dev/) и [GitHub](https://github.com/animotionjs/animotion) — презентации на Svelte, релиз 2026-07-23, MIT; [animotion.dev](https://animotion.dev/) — другой сайт. Проверено 2026-10-14.
- [Diffusion Studio Core](https://github.com/diffusionstudio/core) — композитинг на WebCodecs, MPL-2.0, релиз 2025-02-01. Проверено 2026-10-14.
