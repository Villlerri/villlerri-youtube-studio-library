# Motion design в визуальных программах

## Что сюда входит

Анимацию делают в графическом редакторе с таймлайном: слои, ключевые кадры, кривые лёгкости, выражения или скрипты, рендер в видео. Сюда входят профессиональные пакеты (After Effects, Cavalry, Apple Motion, Cinema 4D), бесплатные программы (Friction, Glaxnimate), браузерные Jitter и Lottie Creator, редактор Rive, плюс Fusion в DaVinci Resolve и формат Lottie для готовых вставок. Проект обычно двоичный и живёт в интерфейсе. Класс даёт самый высокий потолок качества и самую низкую степень автоматизации.

## Когда этот класс нужен

- Выразительная плоская графика уровня лучших научно-популярных каналов: сотни частей, анимированных вручную (`diagram`, `mechanism`, `micro`, `scale`).
- Кинетическая типографика: заголовки, цитаты, подписи по словам (`typography`).
- Длинная непрерывная сцена с камерой, слоями и параллаксом вместо серии кадров и жёстких склеек (`scale`, `map-timeline`).
- Инфографика и схемы, где блоки и линии появляются вместе с фразой диктора (`diagram`, `graph`).
- Рисование линий: контур обводки растёт, пока идёт объяснение (`drawing`).
- Повторяющиеся шаблонные элементы серии: заставки, плашки, титры (`typography`, `screen`).
- Графика поверх реальной съёмки: титры, указатели, трекинг (`real-footage`), чаще Fusion или After Effects.
- Короткие вставки в Lottie для сайта и интерфейса.

## Основные решения

- [Adobe After Effects](../tools/after-effects.md) — отраслевой стандарт: слои, выражения JavaScript, скрипты, рендер из командной строки, экспорт в Lottie; студия Kurzgesagt работает в нём. Подписка US$22.99 в месяц, только Windows и macOS.
- [Cavalry](../tools/cavalry.md) — процедурный 2D-пакет с JavaScript и MCP для Claude; бесплатен для частных лиц с аккаунтом Canva; командной строки с версии 2.7 нет.
- [Apple Motion](../tools/apple-motion.md) — титры, частицы и поведения для Mac; разовые US$49.99; скриптов в проверенных источниках нет.
- [Friction](../tools/friction.md) — свободный аналог After Effects для простых 2D-сцен и анимированного SVG; версия 1.0 не вышла, проект двоичный.
- [Glaxnimate](../tools/glaxnimate.md) — бесплатный редактор Lottie и SVG от KDE; Python-модуль для сборки кодом; возможности скромные.
- [Jitter](../tools/jitter.md) — браузерный сервис с шаблонами, пакетным созданием из CSV и ИИ-чатом; бесплатный тариф с водяным знаком и 720p; цены не видны без JavaScript.
- [Cinema 4D](../tools/cinema-4d.md) — 3D-пакет Maxon с MoGraph для выразительных заголовков и абстрактных форм; Kurzgesagt по расшифровке своего ролика экспериментирует с ним; подписка.
- [Rive](../tools/rive.md) — векторный редактор со state machines и открытыми рантаймами; видео через облачный рендер редактора; сделан для интерфейсов.
- [DaVinci Resolve (Fusion)](../tools/davinci-resolve.md) — узловой композитинг с 3D-камерой, частицами и трекингом; бесплатная версия есть, внешний скриптинг только в Studio.
- [Lottie](../tools/lottie.md) — формат и проигрыватели для готовых клипов из After Effects; хорош для вставок, не для непрерывных сцен.
- [Lottie Creator](../tools/lottie-creator.md) — браузерный редактор Lottie от LottieFiles с ИИ-помощником и MCP для агента; экспорт Lottie, dotLottie, MP4, WebM, MOV, GIF; для монетизируемого канала нужен тариф Team ($24.99 в месяц за место), на бесплатном и Individual коммерческое использование запрещено условиями.

## Сравнение

Оценки взяты из карточек, шкалы описаны в [методике](../method.md).

- Потолок качества. Выше всех [After Effects](../tools/after-effects.md), [Cinema 4D](../tools/cinema-4d.md) и [DaVinci Resolve](../tools/davinci-resolve.md) (по 5). Для первого есть первоисточник: ролик самой студии Kurzgesagt и её класс на Skillshare. Следом [Cavalry](../tools/cavalry.md), [Apple Motion](../tools/apple-motion.md) и [Rive](../tools/rive.md) (по 4): аккуратная выразительная 2D-графика, но готовых научно-популярных примеров на уровне Kurzgesagt в проверенных источниках нет. [Friction](../tools/friction.md), [Jitter](../tools/jitter.md), [Lottie](../tools/lottie.md), [Lottie Creator](../tools/lottie-creator.md) (по 3): аккуратная учебная графика, короткие вставки. [Glaxnimate](../tools/glaxnimate.md) (2): простые векторные анимации.
- Трудность для человека. Легче всех [Glaxnimate](../tools/glaxnimate.md), [Jitter](../tools/jitter.md) и [Lottie Creator](../tools/lottie-creator.md) (по 2): простой интерфейс, день-два на первую работу. [Cavalry](../tools/cavalry.md), [Apple Motion](../tools/apple-motion.md), [Friction](../tools/friction.md), [Rive](../tools/rive.md), [Lottie](../tools/lottie.md) (по 3): недели до своего стиля, у Cavalry непривычная процедурная логика. Тяжелее всех [After Effects](../tools/after-effects.md), [Cinema 4D](../tools/cinema-4d.md), [DaVinci Resolve](../tools/davinci-resolve.md) (по 4): огромный интерфейс, месяцы до свободной работы.
- Трудность для агента. Проще остальных [Rive](../tools/rive.md) (2): текстовый формат сцены и командная строка, но видео только через облако. [After Effects](../tools/after-effects.md), [Cavalry](../tools/cavalry.md), [Glaxnimate](../tools/glaxnimate.md), [Cinema 4D](../tools/cinema-4d.md), [DaVinci Resolve](../tools/davinci-resolve.md), [Lottie](../tools/lottie.md), [Lottie Creator](../tools/lottie-creator.md) (по 3): агент пишет скрипты (ExtendScript, JavaScript, Python) или ведёт редактор через MCP, но программа должна быть запущена и результат проверяется кадром. У Cavalry с 2.8 есть MCP для Claude, у Lottie Creator MCP-мост работает только при открытой вкладке браузера, а экспорт делается кнопкой. [Apple Motion](../tools/apple-motion.md), [Friction](../tools/friction.md), [Jitter](../tools/jitter.md) (по 4): работа в интерфейсе, API и командной строки нет.
- Автоматизация. Максимум в классе у [Rive](../tools/rive.md) (4). [After Effects](../tools/after-effects.md) (3): выражения на каждом свойстве, скрипты `.jsx`, `aerender` из командной строки, шаблоны. [Cavalry](../tools/cavalry.md) (3): JavaScript, скрипты рендера, MCP; командная строка исчезла с 2.7. [Glaxnimate](../tools/glaxnimate.md) (3): Python без интерфейса, но рендера видео нет. [Cinema 4D](../tools/cinema-4d.md), [DaVinci Resolve](../tools/davinci-resolve.md), [Lottie](../tools/lottie.md), [Lottie Creator](../tools/lottie-creator.md) (по 3). [Apple Motion](../tools/apple-motion.md), [Friction](../tools/friction.md), [Jitter](../tools/jitter.md) (по 2): шаблоны, выражения, пакетное создание из CSV, но не скриптовая сборка сцен.
- Стоимость. Бесплатны: [Cavalry](../tools/cavalry.md) (для частных лиц, нужен аккаунт Canva), [Friction](../tools/friction.md), [Glaxnimate](../tools/glaxnimate.md), бесплатная версия [DaVinci Resolve](../tools/davinci-resolve.md) (без внешнего скриптинга). До US$100 разово или до US$20 в месяц: [Apple Motion](../tools/apple-motion.md) (US$49.99 разово или подписка Apple Creator Studio US$12.99 в месяц), [Rive](../tools/rive.md), [Lottie](../tools/lottie.md), [Jitter](../tools/jitter.md) (цены не видны, по стороннему обзору около US$19). От US$20 в месяц или US$100 разово: [After Effects](../tools/after-effects.md) (US$22.99 в месяц отдельно, Creative Cloud Pro US$69.99), [Cinema 4D](../tools/cinema-4d.md), [DaVinci Resolve](../tools/davinci-resolve.md) Studio (US$295 разово), [Lottie Creator](../tools/lottie-creator.md) (Team, US$24.99 в месяц за место при оплате за год; бесплатный и Individual по $19.99 только для некоммерческого использования).
- Плавность переходов и непрерывность сцены. Лучше всего в [After Effects](../tools/after-effects.md): предкомпозиции, null-объекты, time remapping, трек-маски и 3D-камера ведут один длинный кадр (приёмы из класса Kurzgesagt), но готового примера «один кадр на несколько минут» я не нашёл. [DaVinci Resolve](../tools/davinci-resolve.md) (Fusion) и [Cinema 4D](../tools/cinema-4d.md) дают 3D-камеру и частицы. [Cavalry](../tools/cavalry.md): поведения Morph и Blend Shape, утилита Camera, дубликаторы и стаггер; работа этих узлов на реальных формах не проверена. [Apple Motion](../tools/apple-motion.md): поведения и частицы, а не камера. [Friction](../tools/friction.md): эффекты контуров и маски, учебный ролик про морфинг формы. [Rive](../tools/rive.md): один артборд и state machines. [Glaxnimate](../tools/glaxnimate.md): движение по траектории. [Jitter](../tools/jitter.md), [Lottie](../tools/lottie.md) и [Lottie Creator](../tools/lottie-creator.md): короткие клипы без камеры, у Jitter «перо» с морфингом, у Lottie Creator маски, траектории и прорисовка контура. Готовый узел морфинга назван только в списке поведений Cavalry, у Jitter морфинг назван на главной странице, у Friction есть лишь учебный ролик.

## Другие решения

- Canva — https://www.canva.com/ — онлайн-редактор дизайна; с 2026 владелец Cavalry (FAQ Cavalry); страница при проверке отдала 403, возможности анимации не проверялись.
- Adobe Express — https://www.adobe.com/express/ — браузерный редактор Adobe; готовые анимации текста и графики (Typewriter, Flicker, Slide и другие); формат экспорта не проверен.
- Alight Motion — https://alightmotion.com/ — мобильное приложение для iPhone, iPad и Android; ключевые кадры на всех параметрах, векторная правка, экспорт MP4, GIF и последовательности PNG.
- Tumult Hype — https://tumult.com/hype/ — macOS-приложение для HTML5-анимаций без кода; экспорт HTML5, MP4 без звука и GIF; US$49.99.
- Haiku Animator — https://github.com/HaikuTeam/animator — открытый редактор Lottie и веб-компонентов (AGPL); последний коммит 2021-10-13, развитие остановлено.
- Powtoon — https://www.powtoon.com/ — онлайн-конструктор объясняющих роликов; бесплатный план с ограничениями; для научно-популярного канала слабоват.
- [Natron](../tools/natron.md) — свободный узловой композитинг; карточка в соседнем классе.
- [Blender](../tools/blender.md) — открытый 3D-пакет с композитором и Grease Pencil; карточка в соседнем классе.
- [Synfig Studio](../tools/synfig.md) — свободный векторный редактор с костями; карточка в соседнем классе.

## Вывод для объясняющих видео

Если нужен уровень лучших научно-популярных каналов, берите [After Effects](../tools/after-effects.md): сама студия Kurzgesagt называет его основным инструментом анимации, а выражения и скрипты позволяют собирать серии по шаблону. Для плоской процедурной графики и кинетической типографики без подписки Adobe пробуйте [Cavalry](../tools/cavalry.md): бесплатный, есть JavaScript и MCP для Claude, но без интерфейса он не рендерит. На Mac для титров и частиц пригодится [Apple Motion](../tools/apple-motion.md). [Friction](../tools/friction.md) и [Glaxnimate](../tools/glaxnimate.md) годятся для простых вставок, не для главной графики канала. Формулы, графики и физику точнее и дешевле собирать кодом ([Manim CE](../tools/manim-ce.md)), а программы этого класса брать для оформления и выразительных сцен. Против дёрганых склеек строить сцену как один длинный кадр с камерой и предкомпозициями, а не как серию кадров.

## Источники

- [Canva](https://www.canva.com/) — адрес редактора; страница отдала 403. Принадлежность Cavalry Canva подтверждена на [странице Cavalry](https://cavalry.studio/en/). Проверено 2026-10-14.
- [Adobe Express: анимация текста](https://www.adobe.com/express/feature/design/text-animation) — пресеты анимации текста и графики. Содержание по выдаче поиска. Проверено 2026-10-14.
- [Alight Motion](https://alightmotion.com/) — мобильное приложение, ключевые кадры, векторы, форматы экспорта. Проверено 2026-10-14.
- [Tumult Hype](https://tumult.com/hype/) — macOS, HTML5, экспорт, US$49.99. Проверено 2026-10-14.
- [Haiku Animator на GitHub](https://github.com/HaikuTeam/animator) — AGPL, описание. [Лента коммитов](https://github.com/HaikuTeam/animator/commits.atom) — последний коммит 2021-10-13. Проверено 2026-10-14.
- [Powtoon](https://www.powtoon.com/) — онлайн-платформа объясняющих роликов, бесплатный план с ограничениями. Проверено 2026-10-14.
