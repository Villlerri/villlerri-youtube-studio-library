---
id: mcp-bridges
name: MCP-мосты агента к программам графики
class: [3d, hybrid]
kind: method
site: https://modelcontextprotocol.io/
github: none
scenes: [mechanism, scale, field]
quality: 3
human_difficulty: 2
agent_difficulty: 2
automation: 3
reproducibility: 2
cost: 0
maturity: young
platforms: [windows, macos, linux]
export: [png-sequence, exr-sequence, mp4]
code_license: MIT (сторонние мосты), GPL-3.0 (официальный Blender), proprietary (встроенные в Cinema 4D и Unreal Engine)
price: мосты бесплатны; платите за программу и за модель агента
checked: 2026-10-14
---

# MCP-мосты агента к программам графики

Model Context Protocol (MCP) — открытый стандарт, по которому ИИ-агент вызывает функции запущенной программы. Мост для 3D-программы состоит из двух частей: дополнения внутри программы и MCP-сервера. Агент называет действия («создай куб», «поставь свет», «покажи вид с камеры»), программа выполняет их в открытой сцене. Метод нужен там, где сцену строят в программе с окном, а не кодом без экрана.

## Ссылки

- Стандарт MCP: https://modelcontextprotocol.io/
- Blender, официальный: [Blender Lab, MCP Server](https://www.blender.org/lab/mcp-server/) (исходники на projects.blender.org/lab/blender_mcp, GPL-3.0)
- Blender, сторонний: [MCP for Blender (бывший blender-mcp)](https://github.com/ahujasid/blender-mcp), сайт https://www.mcp-for-blender.com/
- Unreal Engine, официальный: [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) (UE 5.8, экспериментальный)
- Unreal Engine, сторонние: [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp), [flopperam/unreal-engine-mcp](https://github.com/flopperam/unreal-engine-mcp)
- Cinema 4D, официальный: [Cinema 4D MCP Server (Maxon)](https://www.maxon.net/cinema-4d/features/mcp-server) (с версии 2026.4)
- Cinema 4D, сторонние: [ttiimmaacc/cinema4d-mcp](https://github.com/ttiimmaacc/cinema4d-mcp), [kumoproductions/mcp-cinema4d](https://github.com/kumoproductions/mcp-cinema4d)
- Примеры, проверенные 2026-10-14 (названия и авторы подтверждены через oEmbed, содержание не смотрел):
  - [What is the Cinema 4D MCP Server?](https://www.youtube.com/watch?v=H53drzzUFfo) — Maxon, показ официального моста.
  - [A First Look at Unreal MCP in Unreal Engine 5.8](https://www.youtube.com/watch?v=FON_noub0C0) — канал Unreal Engine.
  - [Getting Started with MCP in Unreal Engine 5.8](https://www.youtube.com/watch?v=k0tgmrBuIJc) — вебинар Epic Games Education.
  - [Blender MCP Demo: AI Prompting a dragon in a dungeon](https://www.youtube.com/watch?v=DqgKuLYUv00) — ahujasid, автор стороннего моста.
  - [Blender MCP: Use Polyhaven assets](https://www.youtube.com/watch?v=I29rn92gkC4) — тот же автор, ассеты Poly Haven.

## Что есть по программам

### Blender

- Официальный мост Blender Lab. Автор — Blender Foundation (проект Blender Lab, объявлен 2025-11-07, мост описан в отчёте Lab Q1 2026). Лицензия GPL-3.0 (файл LICENSE в репозитории). Нужен Blender 5.1 и новее, дополнение v1.0.3, плюс MCP-сервер, который запускает клиент. Вдобавок есть бандл `.mcpb` для клиентов, которые его принимают. Репозиторий называет себя «намеренно маленьким»: инструменты для анализа сцены, сведения о файле, поиск по встроенной документации API и руководства, скриншоты окна и областей, снимок и рендер вида, переключение вкладок. Есть `execute_blender_code` и версия для фонового процесса Blender без окна (`execute_blender_code_for_cli`). Примеры самого Blender: анализ полигонов по размеру на экране, переименование блоков данных, объяснение схемы Geometry Nodes.
- Сторонний мост MCP for Blender (бывший blender-mcp). Автор — Siddharth Ahuja (ahujasid). Не официальный: README пишет «third-party integration, not made by Blender». Лицензия MIT (LICENSE в репозитории). Выпуски на PyPI: `mcp-for-blender` 2.1.9 от 2026-10-06 (пакет `blender-mcp` продолжает работать). Девять инструментов: `execute_blender_code`, `look` (вид из окна, камеры, с нескольких сторон, полоса кадров анимации, режимы solid, rendered, wireframe), `get_scene_info`, `generate_3d` (Tripo, Hunyuan3D, Hyper3D Rodin), поиск и импорт ассетов (Poly Haven, Sketchfab, Poly Pizza). Есть платный Premium: с $10 в месяц генерации 3D-моделей без своих ключей (страница mcp-for-blender.com/premium). Сам мост и дополнение бесплатны.

### Unreal Engine

- Официальный Unreal MCP. Автор — Epic Games, плагин `ModelContextProtocol` (название в списке плагинов Unreal MCP) входит в UE 5.8. Статус «Experimental»: Epic пишет, что функции неполны, API и форматы меняются, и просит осторожно использовать при выпуске проектов. Лицензия — условия Unreal Engine (см. [unreal-engine](unreal-engine.md)). Сервер внутри процесса редактора, HTTP на `127.0.0.1:8000/mcp`, только петля (localhost), без проверки подлинности. Через «наборы инструментов» (Toolsets, плагин All Toolsets) агент расставляет акторов, настраивает свет, создаёт экземпляры материалов, смотрит виджеты Slate, запускает автотесты. Свои инструменты пишутся на Python или C++. Инструменты вызываются по одному, перекрывающиеся вызовы не допускаются. Генерация конфигурации для Claude Code, Cursor, VS Code, Gemini, Codex одной командой консоли. Телеметрия `EnableAnalytics` включена по умолчанию.
- Сторонний chongdashu/unreal-mcp. Автор — chongdashu. Не официальный. README указывает MIT, файла LICENSE в корне нет. Статус «Experimental», UE 5.5 и новее. Плагин и Python-сервер, работа с акторами, Blueprint, узлами и камерой окна. Последний релиз в ленте не найден.
- Сторонний flopperam/unreal-engine-mcp. README: проект куплен компанией Aura, основной продукт — размещённый MCP-сервер Flop MCP (50+ инструментов) с отдельным плагином. Открытая локальная часть (MIT по README) — базовая. Условия размещённого сервиса не проверял.

### Cinema 4D

- Официальный MCP Server. Автор — Maxon, встроен в Cinema 4D 2026.4 (2026-09-30), ничего ставить не нужно, включается в Preferences → MCP. Выключен по умолчанию. Maxon поддерживает Claude Desktop и ChatGPT Desktop, другие клиенты «должны работать», но не проверялись. Бесплатно, входит в программу. Вокруг него: токен доступа, выбор групп инструментов, раздельные переключатели для выполнения Python (`Allow exec_python Command`) и для объектов с Python (`Allow Python-Bearing Operations`), журнал команд в папке настроек, откат через Undo. Доступ по сети выключен, при включении трафик не шифруется. Можно подключить локальную модель (например, через LM Studio). Работает через Python API Cinema 4D, поэтому возможный пробел в покрытии API или отдельный плагин могут быть недоступны. Условия лицензии Maxon запрещают использовать ассеты Capsules для обучения ИИ.
- Сторонний ttiimmaacc/cinema4d-mcp. Автор — Tim Mac. Не официальный. MIT. Плагин `.pyp` в сокет-сервер плюс Python-сервер MCP, есть инструмент `execute_python`. Версии: основной ориентир — Cinema 4D 2025.0 и новее. Последний коммит в основной ветке по ленте: 2026-03-07.
- Сторонний kumoproductions/mcp-cinema4d. Автор — kumo.productions, Inc. Не официальный, MIT. Нужен Cinema 4D 2026.0.0 и новее. README прямо говорит: с 2026.4 встроенный сервер Maxon основной вариант, а этот остаётся для 2026.0–2026.3, режима нескольких процессов и открытого кода. Произвольный Python (`exec_python`) выключен по умолчанию и включается переменной на обеих сторонах. Не регистрировать оба сервера в одном клиенте: наборы инструментов пересекаются.

## Риски

- Выполнение произвольного кода. Во всех мостах есть инструмент, который запускает Python в программе с правами вашей учётной записи: `execute_blender_code`, `execute_python`, Python-наборы в Unreal. Официальный Blender предупреждает: сервер выполняет сгенерированный моделью код «без ограничений», данные могут быть удалены или отправлены наружу, рекомендуют виртуальную машину или систему без чувствительных данных. README стороннего моста советует всегда сохранять работу перед запуском.
- Сетевой доступ. Unreal MCP слушает только localhost и без проверки подлинности, открывать его наружу небезопасно. У Cinema 4D удалённый доступ выключен, а при включении трафик без шифрования.
- Данные. Сцена, скриншоты и коды уходят провайдеру модели. Стороннее дополнение для Blender по умолчанию собирает обезличенную статистику использования, содержимое (запросы, код, кадры) только по согласию. Telemetry у Unreal MCP включена по умолчанию (`EnableAnalytics`).
- Внедрение инструкций через сцену. Файл сцены, ассет или имя объекта чужого происхождения могут содержать текст, который модель примет за команду. Maxon советует проверять незнакомые сцены и не обменивать сцены с Python внутри.
- Сбои. Вызовы идут по одному и могут зависать, пока вы работаете руками. Maxon советует не трогать программу, пока агент работает. Результат модель описывает уверенно, но он не всегда верен: проверять кадр глазами.
- Поддержка. Сторонние проекты ведут один-два человека, Unreal MCP экспериментальный, официальные Maxon и Blender Lab новые.

## Что реально получается

- Агент строит и правит сцену в программе с окном и сам смотрит результат: скриншот вида, кадры анимации, рендер. Это снимает часть ручной работы. Для Blender `look` у стороннего моста даёт мультиракурс и полосу кадров анимации.
- Непрерывная сцена, камера, морфинг и рисование линий определяет сама программа: Blender (Geometry Nodes, Grease Pencil), Cinema 4D (MoGraph, Takes), Unreal (Sequencer). Мост передаёт команды, а не добавляет возможностей. Агент пишет скрипт анимации камеры и ключей, затем рендерит. Хороший результат зависит от модели и точности запроса.
- Синхронизация с голосом: нет в мостах. Метки времени из озвучки нужно превратить в ключи сам (см. [whisperx](whisperx.md)).
- Сквозной пример (магнит на холодильнике): агент в Blender строит сцену с магнитом и дверью, ставит камеру и свет, импортирует линии поля из расчёта [magpylib](magpylib.md) и рендерит кадры. Физику поля мост не считает.

## Слабые стороны

- Результат не воспроизводим: живой диалог с моделью меняет сцену, сохраняется двоичный проект. Воспроизводимость даёт только сохранённый скрипт, а не сам диалог.
- Без окна программа не работает (кроме фонового режима Blender у официального моста). Для очереди рендера на сервере проще чистый скрипт.
- Для чисто кодовых сцен мост не нужен: Blender ведётся скриптом без окна (`blender -b`), см. [blender](blender.md).
- Качество и стабильность определяет модель, а не мост. Длинные задачи надо делить на шаги.

## Сложность

- Для человека (2 из 5): установка занимает минуты (официальные Cinema 4D и Unreal включаются в настройках, Blender ставится дополнением). Качество картинки всё равно требует знания программы.
- Для агента (2 из 5): общение через инструменты, есть скриншоты для самопроверки. Руки нужны для запуска программы, подтверждения вызовов в клиенте и оценки вкуса.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): управление живой программой, фоновый режим только у официального моста Blender (`_for_cli`). Пакетный рендер на сервере через мост не настраивается.
- Воспроизводимость (2 из 5): проект двоичный, диалог не сохраняется. Выполненный код можно сохранить, тогда сцену воспроизведёт скрипт.

## Платформа и оборудование

- Blender: Linux, macOS, Windows. Официальный мост требует Blender 5.1 и новее, сторонний ставится через `uvx` и дополнение.
- Unreal Engine: официальный плагин UE 5.8, редактор Unreal на Windows (см. [unreal-engine](unreal-engine.md)).
- Cinema 4D: версия 2026.4 и новее, полное приложение с лицензией и десктопный клиент агента на том же компьютере. Платформы для MCP на странице Maxon не названы (DigitalProduction пишет: Windows и macOS).
- Клиенты агента: Claude Desktop, Claude Code, Codex, Cursor, VS Code, ChatGPT Desktop и другие, смотря по мосту.

## Экспорт

Определяет программа: PNG и EXR последовательности, MP4 из Blender; рендер Cinema 4D и Unreal через очередь рендера. Сами мосты файлов не создают.

## Стоимость

Проверено 2026-10-14 по страницам [Maxon](https://www.maxon.net/cinema-4d/features/mcp-server) (бесплатно, входит в программу), [Blender Lab](https://www.blender.org/lab/mcp-server/), [Unreal MCP](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) и [Premium MCP for Blender](https://www.mcp-for-blender.com/premium). Мосты бесплатны. Отдельно оплачиваются: программа (Cinema 4D платный, см. [cinema-4d](cinema-4d.md); Blender бесплатный, [blender](blender.md)), модель агента (токены или подписка клиента) и, если нужно, Premium стороннего Blender-моста (от $10 в месяц).

## Лицензия и права

- Код или программа: официальный Blender — GPL-3.0; MCP for Blender, cinema4d-mcp, mcp-cinema4d — MIT; chongdashu/unreal-mcp — MIT по README; официальные мосты Maxon и Epic — часть коммерческих программ и их лицензий.
- Результат: сами мосты не накладывают прав на кадры и ролики. Права определяют программа (Cinema 4D, Unreal, Blender), провайдер модели и ассеты, которые агент вставляет. Poly Haven — CC0 по описанию README, ассеты Sketchfab, Poly Pizza, сгенерированные модели имеют свои условия. Maxon прямо запрещает использовать Capsules для обучения ИИ.
- Ассеты в комплекте: у официальных мостов нет. Maxon Capsules доступны через навыки официального Cinema 4D MCP (лицензированы для коммерческих проектов, но не для обучения ИИ).

## Активность и зрелость

GitHub-блок не нужен: у карточки нет одного репозитория.

Зрелость: `young`. Официальные мосты новые: Cinema 4D 2026.4 вышла 2026-09-30, Unreal MCP в UE 5.8 помечен как экспериментальный, Blender Lab MCP версия 1.0.3 (требует Blender 5.1). Сторонний MCP for Blender развивается быстро: 2.1.9 от 2026-10-06, 2.0.0 для пакета `blender-mcp` от 2026-09-16, первая версия 2025-03-08.

## Когда брать и когда нет

- Брать: работа в программе с окном, где агент ставит свет, камеру, материалы и сам смотрит результат; Cinema 4D 2026.4 и новее (официальный мост); Unreal 5.8 с готовым плагином; быстрые черновики сцен для человека.
- Не брать: основной конвейер ролика с очередью рендера и git: используйте скрипты Blender без окна ([blender](blender.md)) и кодовые движки ([manim-ce](manim-ce.md), [remotion](remotion.md)).
- Не брать: для сцен с данными, которые нельзя отдавать провайдеру модели, и на машине с важными файлами без изоляции.
- Сторонний мост Cinema 4D берите только для версий 2026.0–2026.3; на 2026.4 и новее используйте встроенный.

## Источники

- [Blender Lab: MCP Server](https://www.blender.org/lab/mcp-server/) — официальный мост Blender, требования, предупреждение о безопасности. Проверено 2026-10-14.
- [Blender MCP: readme и LICENSE](https://projects.blender.org/lab/blender_mcp/raw/branch/main/readme.md), [LICENSE](https://projects.blender.org/lab/blender_mcp/raw/branch/main/LICENSE), [список инструментов](https://projects.blender.org/lab/blender_mcp/raw/branch/main/readme_tools.rst) — GPL-3.0, состав моста. Проверено 2026-10-14.
- [Blender Lab Activity Report Q1 2026](https://www.blender.org/development/blender-lab-activity-report-q1-2026/) и [Introducing Blender Lab](https://www.blender.org/news/introducing-blender-lab/) — статус проекта. Проверено 2026-10-14.
- [MCP for Blender (README)](https://github.com/ahujasid/blender-mcp) и [LICENSE](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/LICENSE) — автор, MIT, инструменты, предупреждение о коде, телеметрия. Проверено 2026-10-14.
- [mcp-for-blender на PyPI](https://pypi.org/project/mcp-for-blender/) и [blender-mcp на PyPI](https://pypi.org/project/blender-mcp/) — даты выпусков. Проверено 2026-10-14.
- [MCP for Blender: Premium](https://www.mcp-for-blender.com/premium) — платные тарифы. Проверено 2026-10-14.
- [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor) — официальный плагин, localhost, без проверки подлинности. Проверено 2026-10-14.
- [Заметки о выпуске Unreal Engine 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes) — MCP Server (Experimental). Проверено 2026-10-14.
- [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) и [flopperam/unreal-engine-mcp](https://github.com/flopperam/unreal-engine-mcp) — сторонние мосты Unreal, лицензии по README. Проверено 2026-10-14.
- [Cinema 4D MCP Server](https://www.maxon.net/cinema-4d/features/mcp-server) — официальный мост Maxon, FAQ, безопасность, права. Проверено 2026-10-14.
- [DigitalProduction: Cinema 4D 2026.4 MCP](https://digitalproduction.com/2026/10/01/cinema-4d-2026-4-mcp/) — Windows и macOS, ограничения демонстраций (вторичный источник). Проверено 2026-10-14.
- [ttiimmaacc/cinema4d-mcp](https://github.com/ttiimmaacc/cinema4d-mcp) и [kumoproductions/mcp-cinema4d](https://github.com/kumoproductions/mcp-cinema4d) — сторонние мосты, MIT, исходные оговорки. Проверено 2026-10-14.

## Неизвестно

- Платформы встроенного моста Cinema 4D по первоисточнику: страница Maxon не называет, указание Windows и macOS взято из вторичного источника.
- Лицензия Epic на плагин Unreal MCP отдельно от общих условий Unreal Engine: не искал.
- Условия размещённого сервиса Flop MCP и его цена.
- Реальная надёжность мостов на долгих сценах: код не запускался, оценки по описаниям авторов.
- Дата выпуска и точная версия официального моста Blender Lab помимо v1.0.3 из ссылки на странице.
- Есть ли готовые научно-популярные ролики, снятые через такие мосты: не нашёл.
