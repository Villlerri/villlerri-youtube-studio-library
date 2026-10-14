---
id: unreal-engine
name: Unreal Engine
class: [3d]
kind: app
site: https://www.unrealengine.com/
github: none
scenes: [mechanism, scale, character]
quality: 5
human_difficulty: 4
agent_difficulty: 3
automation: 4
reproducibility: 3
cost: 0
maturity: standard
platforms: [windows]
export: [png-sequence, exr-sequence]
code_license: proprietary
price: бесплатно при доходе до $1 млн в год; выше — $1850 за место в год для не-игр
checked: 2026-10-14
---

# Unreal Engine

Игровой движок Epic с рендером в реальном времени (Lumen, Nanite) и секвенсором для кинематографа. Подходит для кинематографичных сцен с живой камерой и светом, быстрых итераций и вывода кадров через Movie Render Queue или Movie Render Graph.

## Ссылки

- Официальный сайт: https://www.unrealengine.com/ (для скриптовых запросов отвечает 403, поэтому страницы лицензии читал через архив, см. «Источники»)
- GitHub: по странице лицензии доступ к исходному коду есть, но репозиторий закрыт (https://github.com/EpicGames/UnrealEngine вернул 404 без входа).
- Документация: https://dev.epicgames.com/documentation/en-us/unreal-engine/ ([командный рендер MRQ](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-command-line-rendering-with-move-render-queue-in-unreal-engine), [Unreal MCP](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US), [релиз 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes))
- Примеры, проверенные 2026-10-14:
  - [Agora Studio’s Real-Time Animation Workflow in UE5 (Unreal Fest Chicago 2026)](https://www.youtube.com/watch?v=hc6xf-3uDX8) — анимационный сериал A-COM целиком в Unreal: превиз, риггинг и анимация в движке, главный Level Sequencer.
  - [A First Look at Unreal MCP in Unreal Engine 5.8](https://www.youtube.com/watch?v=FON_noub0C0) — официальный мост MCP для агентов (2026-10-08).
  - [Getting Started with MCP in Unreal Engine 5.8 (Epic Education)](https://www.youtube.com/watch?v=k0tgmrBuIJc) — подключение MCP.

## Что реально получается

- Кинематографичные сцены: свет Lumen, детальные ассеты, непрерывная камера по Level Sequence. Съёмка кадров по таймлайну без монтажных склеек внутри одной сцены.
- Непрерывность: вся сцена остаётся в одной карте. Переходы выполняются камерой и анимацией, а не склейкой (оценка).
- Быстрые итерации: изменения видны в реальном времени, не нужно ждать рендер.
- Вывод кадров: Movie Render Queue с накоплением пространственных и временных сэмплов («Spatial samples» и «Temporal samples» по документации) даёт сглаженный кадр без мерцания. PNG и EXR умеют сохранять альфа-канал (после включения).
- Анимация персонажей: Sequencer, риг в движке. Для научной графики готовых молекулярных инструментов нет.
- Рисование линий и формулы: не для этого.
- Голос: тайминг через Sequencer, привязки к тексту озвучки нет.

## Слабые стороны

- Огромный пакет и требовательность к видеокарте. Для Lumen и MegaLights нужна карта RTX 2000 / RX 6000 / Arc A или новее.
- Движок для игр: для объясняющих схем лишнее. Текстовые и точные научные сцены проще в [blender](blender.md).
- Лицензия для компаний с доходом выше $1 млн требует платить за место (см. «Стоимость»).
- Epic закрывает страницы лицензии и EULA от автоматического чтения.
- Unreal Engine 5.8 по сообщениям прессы — последняя версия ветки 5, затем Unreal Engine 6 (сроки не подтверждены).

## Сложность

- Для человека (4 из 5): Blueprints, Sequencer, материалы, оптимизация. Месяцы до свободной работы, но готовых шаблонов много.
- Для агента (3 из 5): есть официальный MCP-плагин UE 5.8 (экспериментальный), Python и командный рендер MRQ. Агент может расставлять акторов, настраивать свет, материалы. Проверка вида кадра по рендеру, часть настроек руками.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): рендер из командной строки: `UnrealEditor-Cmd.exe проект.uproject карта -game -LevelSequence=… -MoviePipelineConfig=… -windowed -resx=1280 -resy=720 -log`. Режим Level Sequence рендерит одну задачу на одной карте и все шоты последовательности. При передаче сохранённой очереди обрабатываются все её задачи. Есть исполнитель на Python (`-MoviePipelineLocalExecutorClass`, `-ExecutorPythonClass`). Movie Render Graph в 5.8 помечен как production ready.
- Воспроизводимость (3 из 5): проект бинарный (`.uasset`, `.umap`). Рендер MRQ детерминирован настройками, но побитовое совпадение не гарантируется (оценка).

## Платформа и оборудование

Рекомендовано (Windows): Windows 11, четырёхъядерный 2,5 ГГц, 32 ГБ ОЗУ, DirectX 12, 8 ГБ видеопамяти и больше. Минимум: Windows 10 22H2. Lumen и MegaLights: DirectX 12 с SM6, карты AMD RX-6000, Intel Arc A или NVIDIA RTX 2000 и новее. Nanite: DirectX 12 или Vulkan. Страницы для Linux и macOS не читал, поэтому в `platforms` только Windows.

## Экспорт

- Movie Render Queue: изображения (в таблице документации BMP, JPG, PNG, EXR) и звук WAV; кодеки и контейнеры видео в MRQ не проверялись. PNG и EXR могут выводить альфа-канал (после включения).
- Разрешение и частота кадров задаются в конфигурации задачи. Ограничений по плану нет.

## Стоимость

Проверено 2026-10-14 по [странице лицензии](https://www.unrealengine.com/en-US/license) (снимок web.archive.org от 2026-10-08; прямой запрос даёт 403).

- Бесплатно: «Individuals and small businesses (with less than $1 million USD in annual gross revenue)», преподаватели и школы без лимита дохода, игроделы до $1 млн валового дохода продукта. Исходники и все платформы доступны.
- Выше $1 млн, игры и приложения, где код движка работает у конечного пользователя: роялти 5% с выручки продукта выше $1 млн за всё время. Продажи в Epic Games Store без роялти.
- Выше $1 млн и не игра (в том числе линейное видео): нужна платная «seat license»: «$1,850 per seat per year». Условие со страницы: коммерческое использование, более $1 млн за последние 12 месяцев, «not creating a game or application that relies on engine code at runtime». По тексту страницы роялти относятся только к играм и приложениям, где код движка работает у конечного пользователя; для линейного видео роялти нет (вывод из текста).
- Пробный период 30 дней. Для больше 25 мест и особых условий Epic предлагает связаться.
- Вторичный источник (cgpress.org, март 2024): подписка «designed for creating linear content, such as films and TV shows».

## Лицензия и права

- Код или программа: proprietary, EULA Epic (текст недоступен скрипту, не читал). Исходный код доступен лицензиатам.
- Результат: заявление о правах на кадры и ролики в доступных материалах не проверено (см. «Неизвестно»). Роялти за линейное видео по тексту страницы нет.
- Ассеты в комплекте: условия Fab, MetaHuman и других ассетов не проверены.

## Активность и зрелость

Зрелость: `standard`. Версия 5.8 вышла в июне 2026 (по wnhub.io — 2026-06-17 на State of Unreal в Чикаго; Product Hunt указывает 19 июня). По тем же сообщениям, 5.8 — последняя версия ветки 5, ранний доступ UE 6 ожидается в конце 2027. В 5.8 Movie Render Graph, MegaLights и Live Link Hub вышли из экспериментального статуса; MCP остаётся экспериментальным. Развивает Epic Games.

## Когда брать и когда нет

- Брать: кинематографичные сцены с большим количеством ассетов, быстрая проба света и камеры, команда с опытом в Unreal.
- Не брать: если нужны простые схемы, формулы, воспроизводимый текстовый проект (см. [godot](godot.md), [blender](blender.md)) или молекулы ([molecular-nodes](molecular-nodes.md)).

## Источники

- [Лицензия Unreal Engine](https://www.unrealengine.com/en-US/license) — условия и цены; открыта через снимок web.archive.org от 2026-10-08, прямой запрос 403. Проверено 2026-10-14.
- [Командный рендер MRQ](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-command-line-rendering-with-move-render-queue-in-unreal-engine) — флаги, режимы. Проверено 2026-10-14.
- [Rendering High Quality Frames with Movie Render Queue](https://dev.epicgames.com/documentation/en-us/unreal-engine/rendering-high-quality-frames-with-movie-render-queue-in-unreal-engine) — форматы, альфа, сэмплы. Проверено 2026-10-14.
- [Unreal MCP](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US) — экспериментальный, локальный сервер `http://127.0.0.1:8000/mcp`, без аутентификации. Проверено 2026-10-14.
- [Заметки о выпуске UE 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes) — Movie Render Graph, MCP, Lumen Lite. Проверено 2026-10-14.
- [Аппаратные требования](https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine). Проверено 2026-10-14.
- [wnhub.io](https://wnhub.io/news/engines/item-51157) — дата 5.8 и планы UE 6 (вторичный). Проверено 2026-10-14.
- [cgpress.org](https://cgpress.org/archives/unreal-engine-updates-pricing-for-non-game-industries.html) — тариф для не-игр (март 2024, вторичный). Проверено 2026-10-14.
- Ролики Epic (ссылки выше): названия подтверждены через oEmbed. Проверено 2026-10-14.

## Неизвестно

- Текст EULA Epic и права на результат: страницы возвращают 403 для скриптов.
- Условия ассетов (Fab, MetaHuman, Megascans).
- Системные требования для Linux и macOS.
- Научно-популярный канал, который публично называет Unreal своим инструментом, не найден.
- Подтверждена ли дата выхода 5.8 на сайте Epic (источники расходятся: 17, 19 и 23 июня).
- Побитовая детерминированность рендера MRQ.
