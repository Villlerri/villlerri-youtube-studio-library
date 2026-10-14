---
id: davinci-resolve
name: DaVinci Resolve (с Fusion)
class: [edit-composite, motion-design]
kind: app
site: https://www.blackmagicdesign.com/products/davinciresolve
github: none
scenes: [real-footage, typography, screen]
quality: 5
human_difficulty: 4
agent_difficulty: 3
automation: 3
reproducibility: 3
cost: 2
maturity: standard
platforms: [linux, macos, windows]
export: [mp4, mov]
code_license: proprietary
price: бесплатная версия; Studio $295 разово (США)
checked: 2026-10-14
---

# DaVinci Resolve (с Fusion)

Монтаж, цвет, звук и узловой композитинг (страница Fusion) в одном приложении Blackmagic Design. Текущая версия на сайте: 21. Бесплатная версия есть для Mac, Windows и Linux.

## Ссылки

- Официальный сайт: <https://www.blackmagicdesign.com/products/davinciresolve>
- Страница Fusion: <https://www.blackmagicdesign.com/products/davinciresolve/fusion>
- GitHub: открытого кода нет.
- Документация: в приложении, Help > Documentation > Developer (путь по [ArchWiki](https://wiki.archlinux.org/title/Davinci), вторичный источник). Копия официального README скриптинга от 7 мая 2025: <https://gist.github.com/Manouchehri/e32461dccd824167bac8358bb21c8040>.
- Список кодеков (PDF, ссылка жива, текст не прочитан): <https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_Supported_Codec_List.pdf>
- Примеры, проверенные 2026-10-14 (ссылки открываются через oEmbed; содержание описано по названию, ролики целиком не смотрелись):
  - [Create a PARTICLE TEXT REVEAL in DaVinci Resolve Fusion](https://www.youtube.com/watch?v=q6t36eEqV_c) — канал Visual Nova. Частицы собираются в текст в Fusion.
  - [Blackmagic Fusion - Particle Text Morphing](https://www.youtube.com/watch?v=Mq3YPDGUrkM) — канал A Blackbird Called Sue. Морфинг текста через частицы, есть шаблоны. Ролик старый (эпоха Resolve 15), узлы могли измениться.

## Что реально получается

Опора: страница Fusion, страница «Что нового в 21», примеры выше.

- Узловой композитинг в Fusion: «сотни 2D- и 3D-инструментов», 3D-сцена с моделями, текстом, частицами, светом и камерами, 2D-трекинг, планарный трекинг, трекинг 3D-камеры.
- Текст: Text+ (2D) и Text 3D (выдавливание, фаска). Параметры анимируются ключевыми кадрами, кривые лёгкости правятся в редакторе сплайнов.
- Непрерывная сцена. Камера в 3D и ключевые кадры ведут одну сцену без склеек. Это возможность инструмента, готового примера «объяснение одной непрерывной сценой» я не нашёл.
- Морфинг. Текст и объекты «рассыпаются» и «собираются» частицами (примеры выше). Морфинга одной картинки в другую готовым узлом на официальных страницах нет.
- Движение камеры. 3D-камера Fusion, трекинг камеры по реальной съёмке.
- Рисование линий. Готового «рисования от руки» на официальных страницах не нашёл. Вывод: линию можно выводить маской или формой с ключевыми кадрами, это ручная работа.
- Синхронизация с голосом. В Resolve 21 в Fusion есть модификатор Fairlight Animator для анимации от звука. Речь студия озвучивает только через ElevenLabs, встроенный AI-генератор речи Resolve 21 не использовать.
- Монтаж: на странице Cut больше 100 переходов и эффектов, 2D и 3D шаблоны титров, быстрый экспорт на YouTube и Vimeo.
- Ретайм: оптический поток (Optical Flow) среди вариантов качества, продвинутый Speed Warp только в Studio.
- Графика из других инструментов: в 21 добавлена поддержка Lottie и OGraf (HTML-графика) на таймлайне, плюс библиотека Krokodove (больше 70 график) в Fusion.

## Слабые стороны

- Бесплатная версия: 8-бит, до 60 к/с, до 3840 x 2160. Studio: 10-бит, до 120 к/с, до 32K.
- Кодеки на Linux. По ArchWiki бесплатная версия не декодирует и не кодирует H.264 и H.265, AAC нет ни в Free, ни в Studio. Официальный список кодеков не прочитан (PDF). YouTube просит H.264 в MP4 ([см. FFmpeg](ffmpeg.md)). Вывод: на бесплатной Linux-версии рендерить в промежуточный кодек и перекодировать FFmpeg.
- Внешний скриптинг только в Studio (см. «Сложность»).
- Linux официально поддерживает Rocky Linux, остальные дистрибутивы неофициально (ArchWiki, вторичный источник).
- Проект хранится в базе Resolve, двоичный.
- Fusion требует навыков узлового композитинга. Графики и формулы в нём собирать долго.

## Сложность

- Для человека (4 из 5): монтаж на страницах Cut и Edit осваивается за дни, Fusion с 3D и частицами за месяцы. Это оценка автора карточки, не источник.
- Для агента (3 из 5): оценка для Studio. Есть Python и Lua API: создание проекта, импорт и экспорт проектов, медиапул, пресеты рендера, объект Fusion. Работает безголовый режим `-nogui` (README скриптинга). В бесплатной версии внешний скриптинг недоступен, агенту остаются скрипты из консоли и меню Workspace > Scripts, это 4 из 5. Проверить результат агент может только отрендерив кадры.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): Python и Lua. README: по умолчанию скрипты запускаются из консоли страницы Fusion или из командной строки, настройка в Preferences. README написан для DaVinci Resolve Studio. ArchWiki: бесплатная версия запускает скрипты только внутри Resolve, Studio ещё и извне (Preferences > System > General > External scripting using). Нужен запущенный Resolve. Очередь рендера есть.
- Воспроизводимость (3 из 5): проект двоичный (база или архив), тот же проект даёт тот же результат на той же версии. Под git не ложится.

## Платформа и оборудование

- Mac, Windows, Linux (официальная страница продукта).
- Нужна видеокарта с OpenCL или CUDA (ArchWiki, вторичный источник). Studio поддерживает несколько GPU.
- Требования к памяти на официальных страницах не найдены.

## Экспорт

- Страница Deliver: «полный контроль над кодированием и форматами», очередь рендера, быстрый экспорт на YouTube, Vimeo и X.
- Бесплатная версия: до UHD 3840 x 2160, до 60 к/с, 8-бит. Studio: 10-бит, до 120 к/с, до 32K.
- Конкретные контейнеры и альфа-канал не проверены (список кодеков в PDF не прочитан). Значения `mp4` и `mov` в поле `export` не подтверждены официальными страницами.

## Стоимость

Проверено 2026-10-14 по [странице Studio](https://www.blackmagicdesign.com/products/davinciresolve/studio).

- Бесплатная версия: $0. Страница Fusion говорит, что Fusion встроен в Resolve, и ведёт на бесплатную загрузку. Перечень инструментов Fusion только для Studio не найден.
- Studio: $295 (разово, цена США без налога и доставки). Сторонний обзор для Resolve 20 называл $325, на официальной странице сейчас $295.
- Оценка стоимости 2 учитывает Studio: без него нет внешнего скриптинга. Для ручной работы хватает бесплатной версии.
- Studio добавляет: AI Neural Engine (изоляция голоса, ремиксер музыки, Super Scale, изоляция и трекинг объектов), 45 дополнительных Resolve FX, несколько GPU, Dolby Vision и HDR10+.

## Лицензия и права

- Код или программа: проприетарная (Blackmagic Design). Текст EULA не удалось открыть, см. «Неизвестно».
- Результат: условия на права на ролики и водяной знак не найдены на официальных страницах. Вывод не делаю.
- Ассеты в комплекте: шаблоны титров, эффекты и библиотека Krokodove идут с программой. Условия их использования в роликах не найдены.

## Активность и зрелость

Зрелость: standard. Resolve 21 вышел публично в апреле (бета) и в начале июня 2026 (финал), 21.1 в сентябре, по сторонним сообщениям ([CINED](https://www.cined.com/davinci-resolve-21-final-release-now-available-new-photo-page-expanded-ai-toolset-krokodove-in-fusion-and-wide-raw-support/), страница при загрузке вернула 403, даты взяты из поисковой выдачи). Официального пресс-релиза с датой не нашёл. Развивает Blackmagic Design.

## Когда брать и когда нет

- Брать: монтаж плюс композитинг в одной программе без подписки, 3D-камера и частицы в Fusion, трекинг графики по съёмке, Linux-рабочая станция.
- Брать Studio: если агент должен собирать таймлайны через API.
- Не брать: если нужен чистый код под git и рендер без GUI. Для этого [FFmpeg](ffmpeg.md) и [MoviePy](moviepy.md).
- Не брать: если ролик собирается из готовых кадров без анимации. Хватит Kdenlive или FFmpeg.

## Источники

- [Страница продукта](https://www.blackmagicdesign.com/products/davinciresolve) — версия 21, Studio $295, бесплатная версия, лимиты (8-бит, 60 к/с, UHD), Linux. Проверено 2026-10-14.
- [Страница Studio](https://www.blackmagicdesign.com/products/davinciresolve/studio) — различия Free и Studio (120 к/с, 32K, 45 FX, AI, GPU, кодеки). Проверено 2026-10-14.
- [Что нового в 21](https://www.blackmagicdesign.com/products/davinciresolve/whatsnew) — Lottie и OGraf, Krokodove, Fairlight Animator, редакторы ключевых кадров. Проверено 2026-10-14.
- [Fusion](https://www.blackmagicdesign.com/products/davinciresolve/fusion) — узлы, 3D, частицы, трекинг, Text+, Python и Lua, ключевые кадры. Проверено 2026-10-14.
- [Страница Edit](https://www.blackmagicdesign.com/products/davinciresolve/edit) — Speed Warp только в Studio, Optical Flow среди вариантов ретайма. Проверено 2026-10-14.
- [Страница Cut](https://www.blackmagicdesign.com/products/davinciresolve/cut) — больше 100 переходов и эффектов, быстрый экспорт. Проверено 2026-10-14.
- [Страница Deliver](https://www.blackmagicdesign.com/products/davinciresolve/deliver) — очередь рендера, быстрый экспорт. Проверено 2026-10-14.
- [README скриптинга (копия)](https://gist.github.com/Manouchehri/e32461dccd824167bac8358bb21c8040) — Python и Lua, консоль Fusion, `-nogui`, пути Linux, права внешнего доступа. Проверено 2026-10-14.
- [ArchWiki: DaVinci Resolve](https://wiki.archlinux.org/title/Davinci) — вторичный источник: Free запускает скрипты только внутри, Rocky Linux как официальный, нет H.264 и H.265 в Free. Проверено 2026-10-14.
- [CINED: Resolve 21 final](https://www.cined.com/davinci-resolve-21-final-release-now-available-new-photo-page-expanded-ai-toolset-krokodove-in-fusion-and-wide-raw-support/) — вторичный источник, дата финала по поисковой выдаче. Проверено 2026-10-14.

## Неизвестно

- Текст EULA: права на результат, водяной знак, условия для монетизации не найдены (страница `/company/eula` вернула общую страницу компании).
- Список кодеков и контейнеров Free и Studio для Linux: PDF не прочитан. H.264 и H.265 в Free на Linux известны только из ArchWiki.
- Какие инструменты Fusion доступны только в Studio: на официальных страницах не перечислено.
- Официальный текст руководства о запрете внешнего скриптинга в бесплатной версии не открылся. Известно из заголовка README («for DaVinci Resolve Studio») и ArchWiki.
- Точная дата выхода Resolve 21: официальных дат нет, только сторонние сообщения.
- Smooth Cut (переход для скачков в говорящей голове) в официальных страницах не найден.
- Требования Resolve к памяти и видеокарте на официальных страницах не найдены.
- Содержание двух примеров описано по названию, ролики не просматривались целиком.
