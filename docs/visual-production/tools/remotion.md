---
id: remotion
name: Remotion
class: [2d-code, web-graphics, sync]
kind: framework
site: https://www.remotion.dev/
github: remotion-dev/remotion
scenes: [typography, diagram, graph, screen, real-footage]
quality: 4
human_difficulty: 3
agent_difficulty: 1
automation: 5
reproducibility: 5
cost: 2
maturity: stable
platforms: [linux, macos, windows, web]
export: [mp4, webm, mov, prores]
code_license: proprietary
price: бесплатно для одиночек и команд до 3 человек; компании от 4 человек платят (от $25 в месяц за место)
checked: 2026-10-14
---

# Remotion

Видео как React-компонент: на вход номер кадра, на выходе любая вёрстка (HTML, SVG, Canvas, WebGL). Рендер локально, на сервере или в AWS Lambda. Выделяется тем, что вся веб-экосистема (React, three.js, Lottie, GSAP, SVG-пути) доступна как графика, а документация написана и для агентов.

## Ссылки

- Официальный сайт: https://www.remotion.dev/
- GitHub: https://github.com/remotion-dev/remotion
- Документация: https://www.remotion.dev/docs
- Цены и лицензия: https://www.remotion.pro/license
- Примеры, проверенные 2026-10-14 (ролики открывались через oEmbed, содержание описано по названию, не смотрел):
  - [This video was made with code. But how?](https://www.youtube.com/watch?v=deg8bOoziaE) — Fireship, разбор Remotion; ссылка из списка ресурсов самой документации.
  - [Recreating Spotify Wrapped 2025 in Remotion!](https://www.youtube.com/watch?v=WAjO-M_Q9C0) — Jonny Burger, туториал из списка ресурсов Remotion: анимированные итоги с графиками и типографикой.
  - [Creating F1 graphics in JavaScript](https://www.youtube.com/watch?v=sA-X0Bw_7Gg) — Jonny Burger, телевизионная графика с данными.
  - [Страница ресурсов](https://www.remotion.dev/docs/resources) — шаблоны, ролики, библиотеки сообщества. Витрина [Showcase](https://www.remotion.dev/showcase) подгружается скриптом, карточек в тексте страницы нет, заявки на неё сейчас не принимаются.

## Что реально получается

- Непрерывная сцена: композиция идёт по кадрам, любой элемент зависит от `useCurrentFrame()`. Анимацию пишут `interpolate`, `spring` и CSS. Нет автоматического морфинга объектов и нет камеры: двигают контейнер трансформацией или камеру three.js.
- Переходы: пакет `@remotion/transitions` (`TransitionSeries`) с fade, slide, wipe, flip, clockWipe и своими презентациями. Сцены лежат в одной композиции, переходы перекрывают их по времени. Дёрганые жёсткие склейки можно заменить на ровные, но сквозное превращение объекта в другой автор строит сам.
- Рисование линий: `evolvePath()` из `@remotion/paths` отдаёт `strokeDasharray` и `strokeDashoffset` для SVG-пути, линия «вырастает» от 0 до 1. В пакете есть и код из d3-interpolate-path.
- 3D: `@remotion/three` (`ThreeCanvas`) — React Three Fiber с кадровым временем. Рендеру нужен ANGLE (`chromiumOptions.gl: 'angle'`).
- Lottie: `@remotion/lottie` играет анимации через lottie-web. Выражения After Effects могут давать мерцание, потому что рендер идёт через `goToAndStop()`.
- GSAP: `@remotion/gsap` строит поставленный на паузу таймлайн GSAP и ставит его на текущий кадр, результат детерминирован.
- Субтитры и голос: `@remotion/captions` (тип `Caption`, `createTikTokStyleCaptions`, разбор SRT, интеграции Whisper.cpp и ElevenLabs). Метки слов берут из [whisperx](whisperx.md) или [elevenlabs](elevenlabs.md). Редактора меток по озвучке нет: тайминги задаются данными или кодом.
- Типографика и данные: титры, подписи по словам, графики на SVG или D3, заставки; ровный движок тайминга по кадрам.
- Видео поверх графики и экран: `<Video>`, `<Audio>`, шаблоны для видео из реальной съёмки с подписями.

## Слабые стороны

- Нет математических примитивов, формул и морфинга как в [manim-ce](manim-ce.md). Формулы надо подключать через KaTeX или SVG и анимировать вручную.
- Лицензия платная для команд от 4 человек и меняется в версии 5.0 (черновик: учитываются подрядчики).
- Рендер идёт через headless Chromium. В безголовом режиме GPU по умолчанию выключен, и это сильно замедляет WebGL, тени, размытия. На Lambda GPU нет.
- Remotion Lambda ограничен: видео до 80 минут в Full HD, вывод до 5 ГБ, AV1 недоступен.
- Выглядеть красиво по умолчанию не будет: это конструктор, качество определяет дизайн автора.

## Сложность

- Для человека (3 из 5): нужны React и TypeScript, понимание кадровой модели. Studio с предпросмотром упрощает отладку. Для оформления нужен веб-дизайн.
- Для агента (1 из 5): всё в коде, есть CLI (`npx remotion render`), Studio, документация в формате Markdown для агентов (добавить `.md` к адресу), Agent Skills и плагины для Claude Code, Codex и других. Агент сам рендерит и сверяет кадры. Руки нужны только для оценки вкуса.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): CLI, серверный рендер `renderMedia()`, параметризованные видео, Lambda для параллельного рендера, шаблоны для связки «текст в видео».
- Воспроизводимость (5 из 5): проект — код под git, каждый кадр чистая функция от номера кадра. Оговорка: версия Chromium, шрифты и выражения Lottie могут менять результат; пакеты Remotion нужно держать на одной точной версии.

## Платформа и оборудование

Linux, macOS, Windows; Node.js или Bun. Studio — локальный веб-сервер на порту 3000. Для тяжёлых сцен нужна видеокарта на машине рендера с флагом `--gl`. Облако: AWS Lambda (нужен аккаунт AWS и права для Remotion). Пример затрат с официальной страницы (регион us-east-1, 2048 МБ, версия 4.0.381): минута видео из ролика около $0.013 на вычисления, HelloWorld около $0.001. Без учёта хранения в S3, трафика и лицензии.

## Экспорт

- Кодеки: h264 (по умолчанию, .mp4, .mov, .mkv), h265, vp8, vp9, av1, prores (.mov). Параметры CRF, битрейт.
- Прозрачность: WebM с альфой — кадры PNG, кодек VP8 или VP9, формат пикселя `yuva420p`.
- Разрешение и частоту кадров композиция задаёт сама. Есть параллельное кодирование: кадры кодируются, пока рендерятся другие.

## Стоимость

Проверено 2026-10-14 по [странице лицензий](https://www.remotion.pro/license).

- Free: одиночки и команды до 3 человек, коммерческое использование разрешено.
- Company License для компаний от 4 человек. Remotion for Creators: $25 в месяц за место, по одному месту на пользователя. Remotion for Automators: $0.01 за рендер, минимум $100 в месяц; для компаний, которые строят приложения и системы автоматического создания видео.
- Enterprise: от $500 в месяц, с индивидуальными условиями.
- Платные добавки в магазине: Editor Starter $600, Timeline $300 и другие.

На Lambda команда от 4 человек платит лицензию отдельно от расходов AWS ([пример затрат](https://www.remotion.dev/docs/lambda/cost-example)). Как складываются места и рендеры в итоговой сумме, страница объясняет только примером на $100 в месяц.

## Лицензия и права

- Код или программа: пакет `remotion` под Remotion License (источник открыт, но не OSI-лицензия). Бесплатно для: одиночки, коммерческая организация до 3 сотрудников, некоммерческая организация, оценка без коммерческого применения. Остальным нужна Company License. Запрещено копировать код Remotion, чтобы продавать собственную производную. Пакеты `@remotion/three`, `@remotion/captions`, `@remotion/paths`, `@remotion/gsap` — MIT (npm); `@remotion/lottie` и `@remotion/transitions` — по Remotion License (документация).
- Результат: лицензия разрешает использовать ПО для создания видео и изображений, в том числе в коммерческих проектах. Отдельных ограничений на ролики, монетизацию YouTube и водяных знаков в тексте нет.
- Ассеты в комплекте: условия шаблонов, Elements и платных добавок из магазина (Editor Starter, Timeline, Colors and Shapes и другие) не проверял.
- Готовится Remotion 5.0 с новой версией лицензии (черновик PR 3750, не принят): в команду из 3 человек включают подрядчиков, добавлен запрет открывать сервис рендера, куда пользователи загружают свой код Remotion.

## Активность и зрелость

<!-- gh-stats:remotion-dev/remotion -->
- Звёзды GitHub: 64 088
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v4.0.535 (2026-10-12)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория remotion-dev/remotion, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Версия 4.0.535 вышла 2026-10-12, релизы каждые несколько дней, последний коммит 2026-10-14. Развивает компания Remotion AG (подвал сайта). Есть Discord, шаблоны, страница экспертов.

## Когда брать и когда нет

- Брать: титры и подписи по словам, графики с данными, схемы, шаблонные серии роликов, серверный рендер, связка Lottie, three.js и GSAP в одном видео, работа агента без рук. Хороший каркас для сборки итогового видео с озвучкой.
- Не брать: если нужны формулы с морфингом и математические объекты (лучше [manim-ce](manim-ce.md)); если нужен редактор меток по голосу ([motion-canvas](motion-canvas.md)); если команда от 4 человек и не готова платить лицензию.

## Источники

- [LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) (адрес remotion.dev/license перенаправляет сюда) — условия Free и Company License. Проверено 2026-10-14.
- [remotion.pro/license](https://www.remotion.pro/license) — цены. Проверено 2026-10-14.
- [Черновик PR 3750](https://github.com/remotion-dev/remotion/pull/3750) — изменения лицензии в 5.0. Проверено 2026-10-14.
- [Основная идея](https://www.remotion.dev/docs/the-fundamentals), [Studio](https://www.remotion.dev/docs/studio), [кодеки](https://www.remotion.dev/docs/encoding), [прозрачное видео](https://www.remotion.dev/docs/transparent-videos), [GPU](https://www.remotion.dev/docs/gpu) — модель, вывод, рендер. Проверено 2026-10-14.
- [Lambda](https://www.remotion.dev/docs/lambda) и [пример затрат](https://www.remotion.dev/docs/lambda/cost-example) — работа, ограничения, цена рендера. Проверено 2026-10-14.
- [Переходы](https://www.remotion.dev/docs/transitions), [three](https://www.remotion.dev/docs/three), [lottie](https://www.remotion.dev/docs/lottie), [captions](https://www.remotion.dev/docs/captions), [paths](https://www.remotion.dev/docs/paths), [evolvePath](https://www.remotion.dev/docs/paths/evolve-path), [GSAP](https://www.remotion.dev/docs/gsap), [AI](https://www.remotion.dev/docs/ai) — пакеты и работа с агентами. Проверено 2026-10-14.
- [Страница ресурсов](https://www.remotion.dev/docs/resources) — ссылки на ролики. Названия и авторы роликов проверены через oEmbed YouTube 2026-10-14.
- npm-реестр: `remotion` 4.0.535 от 2026-10-12, лицензии пакетов. Проверено 2026-10-14.

## Неизвестно

- Содержание витрины Showcase: карточки загружаются скриптом и не читаются. Примеров научно-популярных каналов на Remotion не нашёл.
- Как именно складываются места Creators и рендеры Automators в итоговой цене: страница лицензии показывает только пример.
- Какие условия действуют для облачного рендера (Cloud Rendering Units) за пределами примера: подробности не проверял.
- Лицензии платных добавок магазина (Editor Starter, Timeline).
