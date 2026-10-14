---
id: hyperframes
name: HyperFrames (HeyGen)
class: [2d-code, web-graphics]
kind: framework
site: https://hyperframes.heygen.com/
github: heygen-com/hyperframes
scenes: [typography, diagram, graph, screen, map-timeline]
quality: 4
human_difficulty: 3
agent_difficulty: 1
automation: 5
reproducibility: 4
cost: 0
maturity: young
platforms: [linux, macos, windows]
export: [mp4, mov, prores, webm, gif, png-sequence]
code_license: Apache-2.0
price: бесплатно, без платы за рендер; облачный рендер HeyGen и приложение Studio требуют аккаунта HeyGen
checked: 2026-10-14
---

# HyperFrames (HeyGen)

Видео как HTML-файл: разметка задаёт, когда элемент на экране, таймлайн GSAP, Lottie, Three.js или CSS задаёт, как он движется. Рендерер перематывает страницу к каждому кадру в headless Chrome и кодирует результат через FFmpeg. Выделяется лицензией Apache-2.0 и тем, что проект сразу делали под ИИ-агента. Идея близка к [remotion](remotion.md), но вместо React обычный HTML.

## Ссылки

- Официальный сайт и документация: https://hyperframes.heygen.com/introduction
- GitHub: https://github.com/heygen-com/hyperframes
- Studio (браузерная и настольная): https://www.hyperframes.dev/studio
- Сравнение с Remotion от авторов: https://hyperframes.heygen.com/guides/hyperframes-vs-remotion
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики внутри не смотрел):
  - [Витрина Showcase](https://hyperframes.heygen.com/showcase) — готовые фильмы, у многих есть исходный проект: запуск продукта, карточки данных, кинетическая типографика, шейдерные эффекты, ролик по pull request.
  - [SpaceX explainer](https://github.com/heygen-com/hyperframes-launches/tree/main/spacex-launch) — «данные и движение», исходник проекта в репозитории hyperframes-launches. Ближайший к объясняющему видео пример.
  - [Faceless explainer](https://hyperframes.heygen.com/guides/faceless-explainer) — руководство: из заметок или статьи получается ролик без съёмки, все визуалы придумывает модель (типографика, абстракции, схемы, графики).
  - [HTML to Video Was Not Easy](https://www.heygen.com/research/html-to-video) — разбор HeyGen (2026-06-22), как добились детерминизма.

## Что реально получается

- Непрерывная сцена. Одна композиция-страница с одним таймлайном: элементы живут между сценами, никто не пересоздаёт кадр. Навык keyframes советует для переезда объекта из одного места в другое один непрерывный tween или FLIP, а не серию склеек: каждый сегмент с новой скоростью читается как рывок. Для сквозного превращения формы есть `MorphSVGPlugin`, для роста линии `DrawSVGPlugin` или `stroke-dasharray` (из текста навыка; плагины GSAP см. [gsap](gsap.md)).
- Камера. В 2D камера — это перемещение и масштаб обёртки: панорама, Ken Burns, цепочка отметок на одном таймлайне. Настоящая камера есть в сцене Three.js через адаптер: орбита и наезд следуют по кадровому времени (`window.__hfThreeTime`, событие `hf-seek`). Подробнее о Three.js: [three-js](three-js.md).
- Переходы между сценами. В каталоге есть шейдерные переходы (WebGL) и переходы на CSS. Документация советует брать шейдер для двух-трёх важных стыков, а не для каждой склейки. Для объясняющего ролика это удобно: основной ход держит один таймлайн, красивый стык ставят там, где меняется тема.
- Lottie. Готовые `.lottie` и JSON-анимации перематываются по кадрам через адаптер, см. [lottie](lottie.md).
- Типографика и данные. Каталог блоков: диаграмма (`data-chart`), блок-схема (`flowchart`), подписи по словам, логотипы, наложения. Есть блок Figma для переноса дизайна.
- Озвучка и синхронизация. `hyperframes tts` генерирует речь локальной моделью Kokoro-82M, `hyperframes transcribe` даёт слова с таймингом (Parakeet, иначе Whisper). Тайминги слов превращаются в моменты анимации данными или кодом. Редактора меток под голос, как в [motion-canvas](motion-canvas.md), нет: Studio правит клипы и ключи на таймлайне. Правки тайминга подписей в Studio не переживают перезагрузку: сохраняются только визуальные правки слов, тайминг правят в источнике подписей (страница Studio captions).
- Звук. Свой аудио-микшер: подавление музыки под голос по частотам («voiceover carve»), эффекты, автоматизация громкости.

Рисования «вживую» в виде руки или маркера нет. Линию можно вырастить по SVG-пути. Формул и математических объектов нет: формулы подключаются через KaTeX или SVG вручную.

## Слабые стороны

- Версия 0.8.x, релизы идут по несколько в день (с 11 по 14 октября 2026 вышло 10 релизов в ленте). API и правила композиции могут меняться: версию надо фиксировать.
- Детерминизм полный только на Linux. Режим `beginFrame` работает в Linux с chrome-headless-shell. На macOS и Windows рендер идёт через скриншоты с эвристиками «кадр дорисован». Для повторяемости документация советует `--docker`. Источник: пост HeyGen и руководство по детерминизму.
- Правила хрупкие. Таймлайн должен быть на паузе и зарегистрирован в `window.__timelines`, нельзя `Date.now()`, `requestAnimationFrame` и несеянный `Math.random()`. Нарушение даёт замороженный кадр или разные результаты, а не ошибку (авторы пишут это сами в сравнении с Remotion).
- Нет математического слоя как у [manim-ce](manim-ce.md): морфинг формул, оси, графики функций надо собирать из SVG и D3 самому.
- Облачный рендер HeyGen и приложение Studio идут через аккаунт HeyGen, условия и цены я не нашёл.
- Меньше шаблонов, туториалов и опыта в продакшене, чем у Remotion. Это признают сами авторы.

## Сложность

- Для человека (3 из 5): нужны HTML, CSS и немного JavaScript, понимание паузы-перемотки. Порог ниже, чем у React-проекта. Приложение Studio для Mac и Linux позволяет менять ролик текстом, рисунком и комментариями через агента. Оформление всё равно требует вкуса.
- Для агента (1 из 5): один HTML, CLI без вопросов (`init`, `lint`, `check`, `snapshot`, `render`), 21 готовый навык для Claude Code, Codex, Cursor и других, плагин для Claude Code. `check` сам ищет проблемы раскладки, движения, медиа и контраста. Агент рендерит и сверяет кадры сам, руки нужны для оценки вкуса.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): CLI, серверный API `@hyperframes/producer`, переменные и шаблоны (один ролик — много версий, пакеты из JSONL), облако HeyGen, AWS Lambda, Google Cloud Run, шаблоны для Vercel, Cloudflare, Modal.
- Воспроизводимость (4 из 5): проект — HTML, JS и медиа под git, кадр определяется только его номером. Пока рендер вне Docker или вне Linux, картинка может сдвинуться на пиксель из-за шрифтов и версии Chrome. В готовом MP4 тег `hyperframes_version` (метаданные контейнера, не водяной знак).

## Платформа и оборудование

Node.js 22 или новее и FFmpeg. CLI работает на Linux, macOS и Windows (в журнале изменений правки для Windows). Приложение Studio: Mac и Linux x86_64 (AppImage). Видеокарта не обязательна. Предпросмотр идёт в реальном времени и может тормозить, рендер идёт покадрово и кадры не теряет. Облако: HeyGen Cloud, AWS Lambda, Cloud Run.

## Экспорт

- MP4, MOV (ProRes 4444 с альфой), WebM (VP9, с альфой), GIF, PNG-последовательность, HLS.
- Разрешение: 1080p по умолчанию, 4K отдельным руководством; частота кадров 1–240 (в облаке), по умолчанию 30 или `data-fps` композиции. HDR: 10-бит H.265 для источников BT.2020.
- В облаке HeyGen 4K тарифицируется как 1.5 от обычного и только в MP4; архив проекта не больше 200 МБ.

## Стоимость

Проверено 2026-10-14 по [README](https://github.com/heygen-com/hyperframes) и [руководству по облаку](https://hyperframes.heygen.com/deploy/cloud). Код бесплатен, README: «no per-render fees or commercial-use thresholds». Локальный рендер, Docker, собственный AWS Lambda или Cloud Run стоят только вычислений. Управляемый облачный рендер HeyGen работает через вход в аккаунт HeyGen или ключ API. Цену рендера документация не называет, только множитель 1.5 для 4K. В отличие от [remotion](remotion.md), где команды от 4 человек платят от $25 в месяц за место, платы за места нет.

## Лицензия и права

- Код или программа: Apache-2.0 ([LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE)). Коммерческое использование без порогов по числу людей. Это главное отличие от Remotion License.
- Результат: лицензия Apache-2.0 регулирует код, на ролики условий не накладывает. Водяного знака нет. В контейнер MP4 пишутся два тега: имя рендерера и версия, их можно стереть командой `ffmpeg -map_metadata -1`. Условия облака HeyGen и приложения Studio не проверял.
- Ассеты в комплекте: блоки каталога, шаблоны дизайнов (frame.md), SFX и музыка из `media-use`, модель удаления фона (документация указывает Apache-2.0 как у U-2-Net). Лицензии отдельных блоков, шрифтов и звуков каталога не проверял, перед публикацией читать лицензию конкретного блока.

## Активность и зрелость

<!-- gh-stats:heygen-com/hyperframes -->
- Звёзды GitHub: 63 589
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.8.158 (2026-10-14)
- Лицензия по данным GitHub: Apache-2.0
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория heygen-com/hyperframes, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `young`. Журнал изменений начинается с v0.6.52 от 2026-05-27, статья-анонс от 2026-06-22, последний релиз в ленте v0.8.158 от 2026-10-14, версий 1.0 ещё нет. Развивает HeyGen, проект там работает в продакшене. Среди пользователей в ADOPTERS: HeyGen, tldraw (автоматические ролики по pull request), TanStack.

## Когда брать и когда нет

- Брать: агент собирает ролик из текста и данных; нужен Apache-2.0 без порога по людям; уже есть HTML, GSAP или Lottie; нужны быстрые шаблонные серии, подписи, диаграммы; один непрерывный таймлайн с Three.js-камерой.
- Не брать: формулы и математика (лучше [manim-ce](manim-ce.md)); редактор меток под голос ([motion-canvas](motion-canvas.md)); нужен зрелый облачный рендер и большая экосистема (лучше [remotion](remotion.md)); рендер на macOS или Windows без Docker, если важна побитовая повторяемость.

## Источники

- [README HyperFrames](https://github.com/heygen-com/hyperframes) — описание, Apache-2.0, требования Node 22 и FFmpeg, сравнение с Remotion, навыки. Проверено 2026-10-14.
- [LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE) — Apache License 2.0. Проверено 2026-10-14.
- [HyperFrames or Remotion?](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion) — отличия, слабые места, миграция. Проверено 2026-10-14.
- [Deterministic Rendering](https://hyperframes.heygen.com/concepts/determinism) — правила детерминизма, Docker. Проверено 2026-10-14.
- [HTML to Video Was Not Easy](https://www.heygen.com/research/html-to-video) — перемотка вместо воспроизведения, beginFrame только на Linux, откат на скриншоты на macOS и Windows, 2026-06-22. Проверено 2026-10-14.
- [Render from the command line](https://hyperframes.heygen.com/guides/rendering) — форматы, прозрачность, метаданные. Проверено 2026-10-14.
- [Cloud rendering](https://hyperframes.heygen.com/deploy/cloud) и [Choose a rendering path](https://hyperframes.heygen.com/deploy/overview) — облако, множитель 4K, архив 200 МБ. Проверено 2026-10-14.
- [Runtimes and 3D](https://hyperframes.heygen.com/prompting/runtimes-and-3d) — Three.js как камера, Lottie, шейдерные переходы. Проверено 2026-10-14.
- [Навык hyperframes-keyframes](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-keyframes/SKILL.md) — FLIP, MorphSVG, DrawSVG, камера. Проверено 2026-10-14.
- [CLI](https://hyperframes.heygen.com/packages/cli) — `tts` на Kokoro-82M, `transcribe`, `cloud`. Проверено 2026-10-14.
- [Get the HyperFrames Studio app](https://hyperframes.heygen.com/studio-app) — Mac и Linux, вход через HeyGen. Проверено 2026-10-14.
- [Changelog](https://hyperframes.heygen.com/changelog) и [лента релизов](https://github.com/heygen-com/hyperframes/releases) — даты и версии, правки для Windows. Проверено 2026-10-14.
- [ADOPTERS.md](https://github.com/heygen-com/hyperframes/blob/main/ADOPTERS.md) — кто применяет. Проверено 2026-10-14.

## Неизвестно

- Цена и условия управляемого облачного рендера HeyGen и приложения Studio: документация отсылает к аккаунту, цифр не публикует. Условия использования HeyGen для таких роликов не проверял.
- Лицензии отдельных блоков каталога, шаблонов дизайна и звуков `media-use`.
- Реальная скорость рендера 10-минутного ролика: код не запускался.
- Работает ли непрерывный морфинг сложных форм через `MorphSVGPlugin` внутри перемотки без артефактов: в документации есть рекомендация, готового примера объясняющего ролика с морфингом не нашёл.
- Содержание роликов Showcase и SpaceX explainer я не смотрел, описано по подписям.
