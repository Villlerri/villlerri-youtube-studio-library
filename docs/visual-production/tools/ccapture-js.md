---
id: ccapture-js
name: CCapture.js и захват кадров из браузера
class: [web-graphics]
kind: method
site: https://spite.github.io/ccapture.js/
github: spite/ccapture.js
scenes: [graph, field, simulation]
quality: 3
human_difficulty: 2
agent_difficulty: 2
automation: 3
reproducibility: 4
cost: 0
maturity: young
platforms: [web]
export: [mp4, webm, gif, png-sequence]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# CCapture.js и захват кадров из браузера

Главный вопрос веб-графики для видео: как получить из анимации на странице видео кадр в кадр, без пропусков и дёрганья. Карточка описывает CCapture.js (версия 2.0 вышла 2026-07-27) и сравнивает его с другими способами: Remotion, HyperFrames, timecut, puppeteer-capture, записью экрана Playwright, WebCodecs и MediaRecorder.

## Ссылки

- Официальный сайт: https://spite.github.io/ccapture.js/
- GitHub: https://github.com/spite/ccapture.js
- Документация: README репозитория (https://github.com/spite/ccapture.js).
- Примеры, проверенные 2026-10-14 (страницы открывались, видео не смотрел):
  - [Демо-страница CCapture](https://spite.github.io/ccapture.js/) — «Record canvas animations at a fixed framerate», запись одной строкой в цикле.
  - [Каталог examples](https://github.com/spite/ccapture.js/tree/master/examples) — по README: `basic` (2D, все форматы, размытие движения), `three` (Three.js, GPU-размытие), `gsap` (таймлайн GSAP ведёт виртуальные часы), `video` (покадровый `<video>`), `demo`.

## Что реально получается

### CCapture 2.0

- Принцип: подменяет часы страницы. `performance.now`, `requestAnimationFrame`, `setTimeout`, `setInterval` и (по умолчанию) `Date.now` возвращают виртуальное время, которое растёт на фиксированный шаг за кадр. Код анимации «не знает», сколько прошло на самом деле. Кадр на 4K, который рисуется две секунды, всё равно ложится в ровный файл 60 к/с (README).
- Использование: `new CCapture({format: "mp4", framerate: 60})`, `start()`, затем `capture(canvas)` один раз за кадр в обычном цикле. Для p5.js README показывает отдельный приём: `noLoop()` и вызов `redraw()` в своём цикле.
- Форматы: MP4 (H.264 или AV1) и WebM (VP9, VP8, AV1) через WebCodecs, GIF (256 цветов, gifenc; по желанию gifski для качества), PNG, JPG, WebP в архиве TAR.
- Размытие движения: `motionBlurFrames` усредняет подкадры, на GPU (WebGL2) или на CPU.
- Звук: `audio` вмуровывает дорожку (AAC или Opus). `renderAudioFrames()` считает спектр звука офлайн для каждого кадра, чтобы визуализация шла в такт.
- Видео внутри страницы: `<video>` и `<audio>` ведутся покадрово («seeked» перед каждым кадром), он должен быть с того же источника.
- Остановка и части: `timeLimit`, `frameLimit`, `startTime`, `autoSaveTime` (файл частями).
- Не подменяются: Web Animations API (`element.animate`) и CSS-анимации и переходы; Web Audio в реальном времени.
- Потолок качества видео (3 из 5): MP4 (H.264, AV1) или WebM из браузера, без ProRes и без управления цветом в README; потолок задаёт кодек WebCodecs и сама сцена, а не CCapture.

### Сравнение способов получить детерминированное видео

- [Remotion](remotion.md): анимация — функция номера кадра (документация: «a frame number and a blank canvas»). Кадры рендерятся по одному (`renderFrames`), поэтому дёрганья от часов страницы нет. Платой служит переписывание сцены под Remotion. Для Three.js есть `@remotion/three` (покадровый `ThreeCanvas`; рендерер OpenGL по умолчанию не подходит, нужен `angle`).
- HyperFrames (HeyGen, Apache-2.0, июнь 2026): HTML-композиция, рендерер не вызывает `play()`, а перематывает (`seek`) к каждому моменту и снимает кадр. На Linux использует `HeadlessExperimental.beginFrame`, на macOS и Windows возвращается к `captureScreenshot` с эвристиками. Заточен под ИИ-агентов, умеет GSAP, Lottie, Three.js, Anime.js. Карточки пока нет; репозиторий очень активный (релиз v0.8.157, 2026-10-14).
- CCapture 2.0: виртуальные часы. Готов для существующих скетчей на p5.js, Three.js, Canvas, GSAP. Запускается во вкладке; автоматизация требует отдельного headless-браузера (его CCapture не поставляет, но в README есть `record(canvas, render)`: своя плоская петля кадров без цикла страницы).
- timecut и timesnap (Steve Tung, BSD-3-Clause): Puppeteer, подмена времени и ffmpeg. Заброшены: последний релиз 0.3.3 от 2022-04-03, последний коммит 2022-09-21. CSS-анимации не поддержаны, режим конвейера в ffmpeg описан как экспериментальный. Для новых проектов не брать.
- puppeteer-capture (Alexey Pelykh, MIT, версия 1.58.0 от 2026-08-07): использует `HeadlessExperimental.beginFrame` в `chrome-headless-shell`, управляет моментом отрисовки. По его README это единственный механизм Chrome, который планирует кадры на уровне композитора; поэтому в кадр попадают и CSS-анимации. Платформы: Linux и Windows (macOS в таблице README нет). Риск: домен Experimental, не работает в `--headless=new`; сам автор оценивает риск как низкий на год и умеренный на 1–3 года.
- Запись экрана Playwright (и Puppeteer-скринкаст): идёт в реальном времени, не покадрово. Размер по умолчанию — окно в пределах 800x800, частота 25 к/с по умолчанию; Firefox и WebKit до 25 к/с; файл появляется после закрытия контекста. Годится как черновик, не для чистовика.
- WebCodecs напрямую: свой цикл рисует кадр, `new VideoFrame(canvas, {timestamp})` и `VideoEncoder`. Нужен ещё мультиплексор для файла MP4 или WebM (WebCodecs этого не делает, MDN называет Mediabunny). Время полностью в руках автора: детерминированно, если сцена — функция от номера кадра.
- MediaRecorder и `canvas.captureStream()` (например, `VideoRecorder` в [babylonjs](babylonjs.md)): запись в реальном времени, на тяжёлых сценах возможны пропуски, у Babylon только WebM.
- Запись экрана ([obs-studio](obs-studio.md) и игровые панели): реальное время, пропуски при нагрузке, подходит для демонстрации интерфейсов.

Итог выбора:

1. Сцена пишется заново, с агентом: Remotion или HyperFrames (по номеру кадра или перемоткой).
2. Уже есть скетч на Canvas, WebGL, p5.js, Three.js, GSAP: CCapture 2.0.
3. Нужна серверная пакетная запись с CSS-анимациями на Linux: puppeteer-capture.
4. Всё остальное — для черновиков.

## Слабые стороны

- Версия 2.0 переписана с нуля. Предыдущий релиз 1.0.9 вышел 2018-03-21: между ними восемь лет без релизов. API сменился: `format: "ffmpegserver"` и `webm-mediarecorder` убраны, формат по умолчанию теперь MP4, `save()` скачивает файл. Неверсионные CDN-ссылки на старый бандл возвращают 404.
- Подмена `Date.prototype.getTime` ломает любую арифметику с датами на странице, пока идёт запись. Отключается `hookDate: false`; `+new Date()` по умолчанию не подменяется.
- CSS-анимации и Web Animations API не подвластны часам. Такие сцены дрейфуют.
- Кросс-доменный холст «загрязняет» (tainted) и кодирование падает. Видео-тег должен быть с того же источника.
- GIF: 256 цветов, задержки кратны сотым секунды; 60 к/с проигрывается около 50.
- Для WebM и MP4 нужен WebCodecs; без него MP4 даёт ошибку, WebM падает в старый писатель.
- Нет таймлайна и привязки к голосу: время ведёт сама сцена.

## Сложность

- Для человека (2 из 5): добавляется одна строка в цикл. Сложности — в мелочах: часы страницы, `Date`, CSS-анимации, подгрузка ресурсов.
- Для агента (2 из 5): весь код в тексте. Агент сам собирает страницу, но запуск браузера и получение файла (скачивание из вкладки) требует headless-обвязки, которой в CCapture нет.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): библиотека работает внутри открытой страницы; `save()` скачивает файл, `save(callback)` отдаёт Blob. Пакетный запуск требует Puppeteer или Playwright вокруг; поддержка именно headless-запуска README не описывает.
- Воспроизводимость (4 из 5): текстовый проект; фиксированный шаг времени даёт одинаковые кадры при детерминированной сцене. Расхождения возможны из-за GPU, кодека и сторонних источников времени, которые библиотека не охватывает.

## Платформа и оборудование

Браузеры с WebCodecs: по README, свежие Chrome, Edge, Safari и Firefox. GPU-размытию нужны WebGL2 и `EXT_color_buffer_float`, иначе CPU. Для серверного запуска нужен headless-браузер с GPU или программным рендером.

## Экспорт

- MP4 (H.264, AV1), WebM (VP9, VP8, AV1), GIF, PNG/JPG/WebP в TAR. Частота кадров задаётся (30, 60, 240 и так далее). Нечётные размеры холста подгоняются под чётные.
- Звук: AAC или Opus, если поддерживает `AudioEncoder` браузера.
- Альфа-канал и разрешение выше ограничений кодека в README не описаны.

## Стоимость

Проверено 2026-10-14 по [README](https://github.com/spite/ccapture.js). Бесплатно.

## Лицензия и права

- Код или программа: MIT («Copyright (c) 2012-2026 Jaume Sanchez Elias»).
- Результат: водяных знаков нет; ограничений на ролики и коммерцию в MIT нет.
- Ассеты в комплекте: только примеры кода; бандлы gifenc и gifski загружаются отдельно со своими лицензиями (не проверялись).

## Активность и зрелость

<!-- gh-stats:spite/ccapture.js -->
- Звёзды GitHub: 3 774
- Последний коммит в основной ветке: 2026-07-27
- Последний релиз или тег: v2.0.0 (2026-07-27)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория spite/ccapture.js, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `young`. Проект с 2012 года, но версия 2.0.0 (2026-07-27) переписана с нуля, API новый. Предыдущая версия 1.0.9 вышла 2018-03-21. Последний коммит — 2026-07-27. Автор — Jaume Sanchez Elias (spite). Общее сравнение в обзоре [SVG, Canvas, WebGL](../classes/03-web-graphics.md).

## Когда брать и когда нет

- Брать: быстро превратить существующую веб-анимацию в ровное видео, особенно p5.js, Three.js, GSAP, чистый Canvas ([p5js](p5js.md), [three-js](three-js.md), [d3](d3.md), [pixijs](pixijs.md)).
- Не брать: новые проекты под агента (проще Remotion или HyperFrames), сцены на CSS-анимациях (нужен puppeteer-capture или Remotion), большие серверные очереди без доработок.

## Источники

- [README CCapture 2.0](https://github.com/spite/ccapture.js) и [raw README](https://raw.githubusercontent.com/spite/ccapture.js/master/README.md) — принцип, форматы, ограничения, `hookDate`, миграция. Проверено 2026-10-14.
- [Релиз v2.0.0](https://github.com/spite/ccapture.js/releases.atom) — даты 2026-07-27 и 2018-03-21 (v1.0.9). Проверено 2026-10-14.
- [Демо-страница](https://spite.github.io/ccapture.js/) — «canvas capture, rebuilt for 2026». Проверено 2026-10-14.
- [LICENSE](https://raw.githubusercontent.com/spite/ccapture.js/master/LICENSE) — MIT, 2012–2026. Проверено 2026-10-14.
- [timecut](https://github.com/tungs/timecut) и [timesnap](https://github.com/tungs/timesnap) — как работают, ограничения; [релизы](https://github.com/tungs/timecut/releases.atom) и [коммиты](https://github.com/tungs/timecut/commits/HEAD.atom) — последний релиз 2022-04-03, последний коммит 2022-09-21; [npm: timecut](https://registry.npmjs.org/timecut). Проверено 2026-10-14.
- [puppeteer-capture](https://github.com/alexey-pelykh/puppeteer-capture) — beginFrame, платформы, риск; [npm](https://registry.npmjs.org/puppeteer-capture) — 1.58.0, 2026-08-07, MIT. Проверено 2026-10-14.
- [HyperFrames: Write HTML, render video](https://www.heygen.com/research/html-to-video) (2026-06-22) и [репозиторий](https://github.com/heygen-com/hyperframes) — перемотка вместо `play()`, `beginFrame` на Linux, Apache-2.0. Проверено 2026-10-14.
- [Remotion: основы](https://www.remotion.dev/docs/the-fundamentals), [renderFrames](https://www.remotion.dev/docs/render-frames), [@remotion/three](https://www.remotion.dev/docs/three) — покадровая модель, `angle`. Проверено 2026-10-14.
- [Playwright: видео](https://playwright.dev/docs/videos) и [testOptions.video](https://playwright.dev/docs/api/class-testoptions) — размер до 800x800, 25 к/с, запись при закрытии контекста. Проверено 2026-10-14.
- [MDN: WebCodecs API](https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API) — `VideoFrame`, `VideoEncoder`, нет мультиплексирования. Проверено 2026-10-14.
- [MDN: MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) — запись `MediaStream`. Проверено 2026-10-14.
- [Babylon.js: Render to Video](https://doc.babylonjs.com/features/featuresDeepDive/scene/renderToVideo) — `VideoRecorder`, только WebM. Проверено 2026-10-14.

## Неизвестно

- Как CCapture 2.0 ведёт себя с p5.js 2.x, D3 и PixiJS на практике: код не запускался, выводы по README.
- Точность кадров под нагрузкой и на сложных WebGL-сценах не измерена.
- Формат файла Playwright (WebM или другой) на проверенных страницах не указан.
- Как HyperFrames ведёт себя на Windows и macOS в деталях: известно лишь про запасной путь `captureScreenshot` с эвристиками.
- Поддержка прозрачности в CCapture: README не описывает.
- Совместимость puppeteer-capture с Chrome-версиями 2027 года и дальше: автор сам называет домен экспериментальным.
