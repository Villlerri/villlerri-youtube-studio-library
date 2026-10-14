# SVG, Canvas, WebGL

## Что сюда входит

Графика, которая рисуется в браузере: векторные формы (SVG), 2D-холст (Canvas), 3D и шейдеры на видеокарте (WebGL и WebGPU). Сюда же относятся библиотеки над ними (D3, Three.js, PixiJS, p5.js, Babylon.js, MathBox) и способы превратить такую страницу в видео. Видео браузер сам не делает: анимация идёт по часам страницы, поэтому главный вопрос класса не «чем нарисовать», а «как записать кадр в кадр».

## Когда этот класс нужен

- Графики и диаграммы, которые плавно перетекают при смене данных (`graph`, `diagram`, `map-timeline`).
- Объёмные сцены с непрерывной камерой: устройство предмета, смена масштаба (`mechanism`, `scale`).
- Поля, волны, фракталы и «математическая» красота, считаемая на видеокарте (`field`, `micro`, `formula`).
- Формулы и функции в 3D с постепенным усложнением кадра (`formula`, `graph`).
- Генеративные фоны и частицы под текст и озвучку (`field`, `simulation`, `typography`).
- Всё, что уже существует как веб-страница или интерактив и должно стать роликом.

## Основные решения

- [D3.js](../tools/d3.md) — данные в SVG и Canvas с плавными переходами; лучший выбор для графиков и карт, видео нужно записывать снаружи.
- [Three.js](../tools/three-js.md) — стандарт веб-3D; непрерывная камера и сцены, запись через внешний захват.
- [PixiJS](../tools/pixijs.md) — быстрый 2D на WebGL и WebGPU; нет таймлайна и записи, нужна обвязка.
- [p5.js](../tools/p5js.md) — самый низкий порог входа для эскизов и генеративных сцен; встроенная запись ограничена 15 секундами и 22 к/с.
- [Babylon.js](../tools/babylonjs.md) — 3D-движок с инспектором и встроенной записью в WebM; точные кадры только отдельным приёмом.
- [MathBox](../tools/mathbox.md) — математическая 3D-графика в стиле презентаций; брошен с 2023 года, брать с оговорками.
- [GLSL-шейдеры и Shadertoy](../tools/glsl-shadertoy.md) — метод для полей и фракталов; потолок качества самый высокий, лицензия чужих шейдеров по умолчанию некоммерческая.
- [CCapture.js и захват кадров](../tools/ccapture-js.md) — виртуальные часы страницы и сравнение всех способов записи; версия 2.0 вышла 2026-07-27.
- [cables.gl](../tools/cables-gl.md) — визуальный редактор WebGL, открытый (MIT); запись в реальном времени.

Соседние карточки класса, которые ведут другие исследователи:

- [Remotion](../tools/remotion.md) — сцена как функция номера кадра, покадровый рендер в видео.
- [GSAP](../tools/gsap.md) и [Theatre.js](../tools/theatre-js.md) — таймлайны для веб-анимации; в примерах CCapture есть связка с GSAP.
- [Vivus](../tools/vivus.md) и [Rough.js](../tools/rough-js.md) — рисование контуров и эскизный стиль для SVG и Canvas.
- [Matter.js](../tools/matter-js.md) — 2D-физика для Canvas.
- [Spline](../tools/spline.md) — 3D-редактор для веба.

## Сравнение

### Потолок качества

- GLSL-шейдеры и Shadertoy (5): картинка уровня лучших научно-популярных каналов, показанная в роликах Inigo Quilez; всё зависит от автора.
- Three.js и Babylon.js (4): современные материалы, свет и постобработка; предел задают модели и работа с освещением. Babylon.js в версии 9.0 заявляет, например, Clustered Lighting и Physically Based Atmosphere.
- D3 (4): графики и карты студийного уровня при хорошем дизайне.
- MathBox (4): узнаваемый вид математических диаграмм; но библиотека заброшена.
- p5.js, PixiJS, cables.gl (3): аккуратная учебная графика, интерактивные визуалы.
- CCapture, Remotion и другие способы записи сами качество не создают; потолок задаёт кодек (H.264, VP9, AV1) и сцена.

### Трудность для человека

- p5.js (2): простейший язык, первая анимация за день.
- D3, Three.js, PixiJS, Babylon.js, cables.gl (3): нужен JavaScript и модель сцены; для D3 — привязка данных, для Three.js — основы 3D.
- MathBox, GLSL-шейдеры (4): математика, массивы на GPU, GLSL; документации у MathBox мало.

### Трудность для агента

- D3, Three.js, PixiJS, p5.js, Babylon.js, GLSL (2): сцена целиком в тексте, результат проверяется скриншотом; руки нужны для вкуса и настройки записи. GLSL можно рендерить без браузера через `glslViewer`.
- MathBox (3): мало примеров, расхождения версий Three.js приходится чинить вручную.
- cables.gl (4): патч собирается мышью в редакторе, операторы можно писать на JavaScript.

### Автоматизация

- Самые автоматизируемые связки: покадровый рендер из Remotion или HyperFrames, серверный захват puppeteer-capture, `glslViewer` для шейдеров.
- CCapture 2.0: работает внутри открытой страницы, для пакетного запуска нужен Puppeteer или Playwright вокруг.
- p5.js: `saveFrames()` ограничен 15 секундами и 22 к/с, значит нужен внешний захват. Processing ([processing](../tools/processing.md)) в этом смысле надёжнее: `saveFrame()` в `draw()` пишет ровно один кадр на вызов.
- Babylon.js: `VideoRecorder` — реальное время, только WebM; точные кадры — приёмами из форума.
- cables.gl: запись MediaRecorder в реальном времени, покадрового экспорта в проверенной документации нет.

### Запись видео кадр в кадр (главный вопрос класса)

Способы делятся на три типа. Тип 1: время задаёт сам автор, сцена — функция кадра. Тип 2: часы страницы подменяются. Тип 3: запись идёт в реальном времени и повторить кадр нельзя.

- Remotion (тип 1): анимация — функция номера кадра, рендер покадровый, поэтому дёрганья от часов страницы нет; цена — сцена пишется под Remotion. Для Three.js есть `@remotion/three` (рендерер OpenGL по умолчанию не подходит, нужен `angle`). См. [remotion](../tools/remotion.md).
- HyperFrames от HeyGen (тип 1, Apache-2.0, июнь 2026): HTML-композиция; рендерер не вызывает `play()`, а перематывает к каждому моменту; на Linux использует `beginFrame`, на macOS и Windows возвращается к скриншотам с эвристиками. Заточен под агентов, понимает GSAP, Lottie, Three.js, Anime.js. Карточка: [HyperFrames](../tools/hyperframes.md).
- WebCodecs напрямую (тип 1): свой цикл, `VideoFrame(canvas, {timestamp})` и `VideoEncoder`, мультиплексор нужен отдельно. Максимум контроля, больше всего собственного кода.
- CCapture.js 2.0 (тип 2): подменяет `performance.now`, `requestAnimationFrame`, таймеры и `Date`; пишет MP4 и WebM через WebCodecs, умеет размытие движения и звук. Не охватывает CSS-анимации и Web Animations API. Подходит для готовых скетчей p5.js, Three.js, GSAP. См. [ccapture-js](../tools/ccapture-js.md).
- timecut и timesnap (тип 2, BSD-3-Clause): Puppeteer, подмена времени и ffmpeg. Последний релиз 2022-04-03, последний коммит 2022-09-21: считать заброшенными.
- puppeteer-capture (управление композитором, MIT, версия 1.58.0 от 2026-08-07): `HeadlessExperimental.beginFrame` в `chrome-headless-shell`; по README ведёт и CSS-анимации; Linux и Windows. Риск: домен Chrome экспериментальный.
- Скринкаст Playwright и Puppeteer (тип 3): реальное время; у Playwright размер до 800x800 и 25 к/с по умолчанию. Для черновиков.
- MediaRecorder и `captureStream()` (тип 3): запись в реальном времени, пропуски на тяжёлых сценах; у Babylon.js только WebM.
- Запись экрана ([obs-studio](../tools/obs-studio.md), панели NVIDIA и AMD) (тип 3): подходит для интерфейсов и черновиков.

Выбор: новый ролик с агентом — Remotion или HyperFrames; готовый скетч — CCapture 2.0; серверная очередь на Linux с CSS-анимациями — puppeteer-capture; остальное — черновики.

### Стоимость

- D3 (ISC), Three.js, PixiJS, MathBox, CCapture (MIT), Babylon.js (Apache-2.0), p5.js (LGPL-2.1), cables.gl (MIT): бесплатно, ограничений на ролики и монетизацию в текстах лицензий нет.
- Shadertoy: сайт и язык бесплатны, но чужой шейдер по умолчанию под CC BY-NC-SA 3.0, то есть некоммерческий; для монетизируемого канала нужен собственный шейдер или явная разрешающая лицензия.
- Remotion: условия см. в карточке [remotion](../tools/remotion.md).

### Плавность переходов и непрерывность сцены

- D3: присоединение данных (enter, update, exit) и `transition()` меняют одни и те же элементы без склеек. Строки с числами, включая контуры, интерполируются сами.
- Three.js и Babylon.js: одна сцена, камера по пути, объекты остаются; морфинг по целям и анимация клипов есть в ядре Three.js.
- MathBox: диаграмма наращивается как на доске; анимируются параметры настоящих формул. Лучший по замыслу, но заброшен.
- GLSL-шейдеры: бесконечные зумы и непрерывные формы, потому что вся сцена — одна функция времени.
- p5.js и PixiJS: сцена живёт, пока идёт цикл; плавность зависит от кода автора, готового таймлайна нет (таймлайны: GSAP, Theatre.js).
- cables.gl: патч — единый живой граф; запись только в реальном времени.
- Риск всех живых сцен: если запись идёт по реальному времени, переходы дёргаются при просадках. Лекарство — тип 1 или 2 из списка выше.

## Другие решения

- [Paper.js](http://paperjs.org) — скриптинг векторной графики на Canvas; последний релиз v0.12.18 (2024-07-17), развитие замедлилось.
- [Two.js](https://two.js.org) — 2D API, один код на SVG, Canvas и WebGL (MIT); релиз 0.8.24 от 2026-08-29.
- [Anime.js](https://animejs.com) — библиотека анимации с таймлайнами, морфингом SVG и рисованием линий; v4.5.0 от 2026-06-22.
- [regl](https://github.com/regl-project/regl) — функциональный WebGL; релиз npm 2.1.1 (2024-11-12); сайт regl.party при проверке не открылся.
- [OGL](https://github.com/oframe/ogl) — минимальная WebGL-библиотека; npm 1.0.11 от 2025-01-27, лицензия Unlicense.
- [Use.GPU](https://usegpu.live) — реактивная WebGPU-среда автора MathBox, бета; пакеты MIT по метаданным npm.
- [Observable Plot](https://github.com/observablehq/plot) — лаконичный API для графиков (ISC); релиз 0.6.17 от 2025-02-14.
- [Vello](https://github.com/linebender/vello) — 2D-векторные рендереры на Rust (CPU, GPU, compute; у GPU-варианта есть бэкенды WebGL2 и wgpu), лицензия Apache-2.0 или MIT; готового конвейера под ролики нет.
- [Hydra](https://hydra.ojack.xyz) — живое кодирование видеосинтеза в браузере (AGPL по npm); в README помечена как экспериментальная.
- [puppeteer-capture](https://github.com/alexey-pelykh/puppeteer-capture) — покадровый захват через `beginFrame` (MIT).
- [timecut](https://github.com/tungs/timecut) — захват с подменой времени; заброшен с 2022 года.

## Вывод для объясняющих видео

Для графиков, карт и схем берите D3 или Three.js и записывайте их покадровым способом, а не скринкастом: тогда переходы идут без дёрганья и один объект живёт между кадрами. Для нового ролика под агента надёжнее всего Remotion (или HyperFrames), потому что время задаёт сцена; CCapture 2.0 нужен, когда скетч уже есть. Шейдеры дают самую выразительную картинку полей и масштабов, но чужие шейдеры Shadertoy для канала с монетизацией брать нельзя без проверки лицензии. MathBox годится как образец подхода, а не как основа. Запись экрана и `MediaRecorder` оставьте для черновиков.

## Источники

- [Страница CCapture 2.0](https://spite.github.io/ccapture.js/) и [README](https://github.com/spite/ccapture.js) — виртуальные часы, форматы, ограничения. Проверено 2026-10-14.
- [HyperFrames: пост HeyGen](https://www.heygen.com/research/html-to-video) (2026-06-22) и [репозиторий](https://github.com/heygen-com/hyperframes) — перемотка, `beginFrame`, Apache-2.0, релизы до v0.8.157 (2026-10-14). Проверено 2026-10-14.
- [puppeteer-capture](https://github.com/alexey-pelykh/puppeteer-capture) и [npm](https://registry.npmjs.org/puppeteer-capture) — 1.58.0, 2026-08-07, MIT. Проверено 2026-10-14.
- [timecut](https://github.com/tungs/timecut), [релизы](https://github.com/tungs/timecut/releases.atom), [коммиты](https://github.com/tungs/timecut/commits/HEAD.atom) — 0.3.3 от 2022-04-03, последний коммит 2022-09-21. Проверено 2026-10-14.
- [Playwright: видео](https://playwright.dev/docs/videos) и [testOptions.video](https://playwright.dev/docs/api/class-testoptions) — 800x800, 25 к/с. Проверено 2026-10-14.
- [MDN: WebCodecs](https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API) и [MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder). Проверено 2026-10-14.
- [Remotion: renderFrames](https://www.remotion.dev/docs/render-frames), [@remotion/three](https://www.remotion.dev/docs/three), [основы](https://www.remotion.dev/docs/the-fundamentals). Проверено 2026-10-14.
- Другие решения: [Two.js](https://two.js.org), [Anime.js](https://animejs.com), [Paper.js на GitHub](https://github.com/paperjs/paper.js), [Hydra README](https://raw.githubusercontent.com/hydra-synth/hydra/main/README.md), [Vello README](https://raw.githubusercontent.com/linebender/vello/main/README.md), [Observable Plot](https://github.com/observablehq/plot), [Use.GPU](https://usegpu.live); версии и лицензии — по [реестру npm](https://registry.npmjs.org/) (two.js, animejs, paper, ogl, regl, hydra-synth, @observablehq/plot) и лентам релизов GitHub. Проверено 2026-10-14.
