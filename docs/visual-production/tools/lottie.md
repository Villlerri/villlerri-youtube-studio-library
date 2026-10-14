---
id: lottie
name: Lottie (lottie-web, Bodymovin, dotLottie)
class: [2d-code, motion-design]
kind: library
site: https://lottie.airbnb.tech/
github: airbnb/lottie-web
scenes: [diagram, typography, character]
quality: 3
human_difficulty: 3
agent_difficulty: 3
automation: 3
reproducibility: 4
cost: 1
maturity: standard
platforms: [web, ios, android, macos, windows]
export: [lottie, html]
code_license: MIT
price: проигрыватели бесплатно; создание через After Effects или LottieFiles от $19.99 в месяц
checked: 2026-10-14
---

# Lottie (lottie-web, Bodymovin, dotLottie)

Формат векторной анимации в JSON и набор проигрывателей. Анимацию рисуют в After Effects, плагин Bodymovin выгружает её в JSON, а lottie-web или проигрыватель dotLottie показывает на странице, в приложении или внутри видеосборки. Формат хорош для маленьких повторяющихся элементов: значки, схемы, заставки, петли.

## Ссылки

- Документация Lottie: https://lottie.airbnb.tech/ (адрес airbnb.io/lottie перенаправляет сюда)
- GitHub lottie-web и Bodymovin: https://github.com/airbnb/lottie-web
- dotLottie (формат и проигрыватели): https://dotlottie.io/ и https://github.com/LottieFiles/dotlottie-web
- Спецификация формата (Lottie Animation Community): https://lottie.github.io/lottie-spec/latest/ и https://github.com/lottie/lottie-spec
- Примеры, проверенные 2026-10-14:
  - [Живой просмотр dotLottie](https://lottiefiles.github.io/dotlottie-web/) — загрузка `.json` и `.lottie` и воспроизведение в браузере, видны темы и состояния.
  - [Витрина сообщества Lottie](https://lottie.airbnb.tech/#/community-showcase) — приложения и сайты с Lottie-анимациями.
  - [How to export an animation with Bodymovin](https://www.youtube.com/watch?v=5XMUJdjI0L8) — автор плагина Hernan Torrisi, показан путь «After Effects, Bodymovin, JSON» (по названию, ролик не смотрел).
  - [Таблица поддерживаемых возможностей After Effects](https://lottie.airbnb.tech/#/supported-features) — что воспроизводится в вебе, а что нет.

## Что реально получается

- Готовые формы и петли: движение форм, масками, прозрачностью, обрезкой контура (Trim Path), текстом с диапазонными селекторами. Подходит для значков, анимированных подписей, лоадеров, маленьких схем.
- Рисование линий: Trim Path вырисовывает контур. Работает во всех веб-рендерерах (SVG, Canvas, HTML).
- Типографика: текст с разбиением на глифы, по буквам, на пути текста, с покадровыми селекторами. Работает в вебе.
- Морфинг формы: ключи на пути формы в After Effects, интерполяция идёт в проигрывателе. Превращение целых объектов друг в друга надо анимировать в After Effects.
- Камера и 3D: в таблице поддерживаемых возможностей 3D-слои и камера не упомянуты. Непрерывную сцену с камерой этот формат не обещает. Каждый файл — отдельный клип; ровные стыки делаются снаружи (в [remotion](remotion.md) или монтаже).
- dotLottie v2: в одном файле `.lottie` несколько анимаций, темы, конечные автоматы состояний, звук. Нужен интерактив и смена тем без перевыгрузки.
- Синхронизация с голосом: проигрыватели умеют маркеры, сегменты, скорость и точное положение по кадру. Привязку к озвучке строит внешний код.

## Слабые стороны

- Это формат доставки, а не инструмент создания: анимацию нужно нарисовать в After Effects ([after-effects](after-effects.md), платный) или в редакторе LottieFiles. Для научно-популярной «живой» графики с нуля неудобно.
- Из эффектов After Effects в таблице совместимости перечислены только Fill, Stroke, Tint, Tritone, Levels, Gaussian blur, Drop Shadow; для Gaussian blur и Drop Shadow в вебе стоит «не проверено». Остальные эффекты (свечение, искажения, частицы и т. п.) в списке не упомянуты — рассчитывать на них нельзя.
- В вебе не поддерживаются: Merge Paths, режимы масок Lighten, Darken, Difference, Feather и Intersect; маски Luma — «не проверено». Платформы отличаются (iOS, Android, Windows поддерживают меньше).
- Выражения (Expressions): в вебе заявлены, но при покадровом рендере в Remotion из-за `goToAndStop()` результат может мерцать. Этот риск возникает при рендере в видео.
- Растровые изображения раздувают файл; сложные сцены тяжелы для проигрывателя.
- Сам lottie-web развивается медленно (см. «Активность и зрелость»).

## Сложность

- Для человека (3 из 5): после настройки After Effects Bodymovin прост, но нужен мастер motion-дизайна, чтобы получить хорошую анимацию. Для встраивания достаточно нескольких строк JavaScript.
- Для агента (3 из 5): подключить и проиграть готовый файл, собрать видео с Lottie в Remotion, менять темы dotLottie агент может сам. Создание новой сложной анимации идёт руками в After Effects; JSON вручную агент пишет плохо.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): проигрыватели управляются из кода (скорость, сегменты, маркеры, темы, события). Для видео есть `@remotion/lottie`, Puppeteer-обёртки и онлайн-конвертеры LottieFiles. Создание файла нельзя автоматизировать полностью.
- Воспроизводимость (4 из 5): итоговый JSON — текст, под git; исходник After Effects двоичный. При воспроизведении без выражений кадр стабилен.

## Платформа и оборудование

Проигрыватели: веб (lottie-web, dotlottie-web), iOS, Android, React Native, Windows. Плагин Bodymovin работает в After Effects (Windows, macOS). dotLottie-web использует ядро на Rust и WASM с рендерером ThorVG и режимами Software, WebGL2, WebGPU (экспериментальный). Видеокарта не обязательна.

## Экспорт

- Из After Effects: JSON (Bodymovin) или `.lottie` (dotLottie, плагин LottieFiles).
- В видео: нет штатной выгрузки. `@remotion/lottie` (через lottie-web), `puppeteer-lottie` (PNG, последовательность, MP4 через ffmpeg, GIF через gifski; признаки поддержки неясны), онлайн-инструменты LottieFiles (на странице цен указаны экспорты GIF, MP4, прозрачные WebM и MOV, тариф не уточнён).

## Стоимость

Проверено 2026-10-14 по [странице цен LottieFiles](https://lottiefiles.com/pricing) и документации. Проигрыватели и формат бесплатны (MIT). Создание: After Effects (платный, см. [after-effects](after-effects.md)) или LottieFiles. У LottieFiles бесплатный уровень (просмотр, тестирование, общий доступ, бесплатная библиотека, базовые правки); Individual $19.99 в месяц за пользователя при оплате на год; Team $24.99; Team+ и Enterprise по запросу.

## Лицензия и права

- Код или программа: lottie-web — MIT; dotlottie-web и сайт dotLottie — MIT (© LottieFiles); спецификация формата — Community Specification License 1.0.
- Результат: ваши файлы и ролики принадлежат вам; ограничений на коммерческое использование и монетизацию в лицензиях проигрывателей нет.
- Ассеты в комплекте: бесплатные анимации библиотеки LottieFiles идут по Lottie Simple License. Разрешено скачивать, менять, публиковать и распространять, в том числе коммерчески; производные выпускать на тех же условиях; нельзя собирать файлы, чтобы построить похожий конкурирующий сервис; указание автора желательно, но не обязательно. Про перепродажу и обучение ИИ лицензия молчит.

## Активность и зрелость

<!-- gh-stats:airbnb/lottie-web -->
- Звёзды GitHub: 32 226
- Последний коммит в основной ветке: 2024-11-19
- Последний релиз или тег: v5.13.0 (2024-11-19)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория airbnb/lottie-web, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `standard` для формата и экосистемы, но сам lottie-web замедлился. Релиз v5.13.0 и последний коммит в репозитории — 2024-11-19; в npm 5.13.0 датирован 2025-05-21; открыто 788 issue. Документация сообщает, что проект поддерживают несколько человек в свободное время по ночам и выходным. Экосистема живая: `@lottiefiles/dotlottie-web` 0.81.0 вышел 2026-10-06, спецификация формата: версия 1.0 от 2024-09-23, 1.0.1 от 2025-06-26, коммиты в 2026 году. Спецификация пока неполная: в ней только часть возможностей, утверждённая Lottie Animation Community.

## Когда брать и когда нет

- Брать: значки, петли, анимированные подписи, схемы из After Effects, короткие вставки, интерактивные страницы; Lottie как кирпичик внутри [remotion](remotion.md).
- Не брать: основной способ делать объясняющие сцены с камерой, формулами, рисованием «на ходу»; сложные эффекты After Effects. Для длинных непрерывных сцен лучше [manim-ce](manim-ce.md), [motion-canvas](motion-canvas.md) или Remotion.

## Источники

- [Документация Lottie](https://lottie.airbnb.tech/) и [таблица поддерживаемых возможностей](https://lottie.airbnb.tech/supported-features.md) (исходный текст) — что поддерживается в вебе. Проверено 2026-10-14.
- [Страница After Effects](https://lottie.airbnb.tech/after-effects.md) и [Спонсорство](https://lottie.airbnb.tech/sponsorship.md) — Bodymovin, автор Hernan Torrisi, поддержка в свободное время. Проверено 2026-10-14.
- [README lottie-web](https://github.com/airbnb/lottie-web) — MIT, рендереры svg, canvas, html, плагин, установка. Проверено 2026-10-14.
- [Релизы](https://github.com/airbnb/lottie-web/releases) и [коммиты](https://github.com/airbnb/lottie-web/commits/master) — 2024-11-19. Проверено 2026-10-14.
- [npm: lottie-web](https://registry.npmjs.org/lottie-web) и [npm: @lottiefiles/dotlottie-web](https://registry.npmjs.org/@lottiefiles/dotlottie-web) — версии, даты, MIT. Проверено 2026-10-14.
- [README dotlottie-web](https://github.com/LottieFiles/dotlottie-web) — ядро Rust и WASM, ThorVG, рендереры, темы, состояния. Проверено 2026-10-14.
- [dotLottie](https://dotlottie.io/) — формат v2, MIT. Проверено 2026-10-14.
- [Спецификация формата](https://lottie.github.io/lottie-spec/latest/) и [репозиторий](https://github.com/lottie/lottie-spec) — статус, лицензия Community Specification, релизы 1.0 и 1.0.1. Проверено 2026-10-14.
- [Lottie в Remotion](https://www.remotion.dev/docs/lottie) — что не поддерживается, выражения. Проверено 2026-10-14.
- [puppeteer-lottie](https://github.com/transitive-bullshit/puppeteer-lottie) — рендер в кадры, MP4, GIF. Проверено 2026-10-14.
- [Lottie Simple License](https://lottiefiles.com/page/license) и [цены LottieFiles](https://lottiefiles.com/pricing) — условия и тарифы. Проверено 2026-10-14.
- Название и автор ролика проверены через oEmbed YouTube 2026-10-14.

## Неизвестно

- Какой тариф LottieFiles включает экспорт в MP4 и прозрачные форматы.
- Поддерживается ли `puppeteer-lottie` сейчас: даты последнего коммита не видно.
- Полный перечень неподдерживаемых эффектов After Effects: в документации только таблица перечисленных, остальное выведено из отсутствия в списке.
- К какому фонду относится Lottie Animation Community: на страницах спецификации не нашёл.
