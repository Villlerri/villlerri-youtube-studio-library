---
id: cinema-4d
name: Cinema 4D
class: [3d, motion-design]
kind: app
site: https://www.maxon.net/en/cinema-4d
github: none
scenes: [typography, diagram, mechanism, scale]
quality: 5
human_difficulty: 4
agent_difficulty: 3
automation: 3
reproducibility: 3
cost: 2
maturity: standard
platforms: [macos, windows]
export: [mp4, mov, prores, png-sequence, exr-sequence]
code_license: proprietary
price: подписка Maxon, около $839 в год или $109 в месяц (по сообщению прессы), бесплатной версии нет
checked: 2026-10-14
---

# Cinema 4D

Коммерческий 3D-пакет Maxon для motion design и графики: MoGraph (клонеры, эффекторы, поля), анимация, рендер Redshift. Сильнее всего там, где нужна быстрая выразительная графика с заголовками и абстрактными формами.

## Ссылки

- Официальный сайт: https://www.maxon.net/en/cinema-4d
- GitHub: открытого кода программы нет. Примеры для Python SDK: https://github.com/PluginCafe/cinema4d_py_sdk_extended
- Документация: https://developers.maxon.net/docs/py/ (Python SDK; страница 2026.2.0 открывается), справка https://help.maxon.net/c4d/en-us/
- Примеры, проверенные 2026-10-14:
  - [Create Oddly Satisfying Spiral Animations in Cinema 4D (Maxon)](https://www.youtube.com/watch?v=F0dtMaFZipE) — процедурная настройка, «умные» циклы; пример MoGraph-подхода.
  - [How to Create a Hypnotic Marble Slide Animation in Cinema 4D (Maxon)](https://www.youtube.com/watch?v=ZHoKYeDx9vg) — разбор анимации шаров (автор Andy Needham).
  - [What is the Cinema 4D MCP Server? (Maxon, 2026-09-30)](https://www.youtube.com/watch?v=H53drzzUFfo) — агент (Claude Desktop, ChatGPT Codex) работает в сцене Cinema 4D 2026.4 и новее.

## Что реально получается

- Выразительная графика: MoGraph по описанию Maxon — «cloners, effectors, fields, and advanced distributions give you systematic control over complex motion». Годится для заголовков, инфографики, абстрактных переходов.
- Сцены-механизмы и смена масштаба в одной сцене с одной камерой: стандартная 3D-работа.
- Рендер: Redshift (GPU) входит в подписку без доплаты. Полноценный фотореализм при достаточной видеокарте.
- Морфинг и переходы: MoGraph и deformers дают плавные превращения форм. Это сильная сторона по сравнению с чистым моделированием (оценка).
- Рисование линий: нет отдельного инструмента вроде [Grease Pencil](blender-grease-pencil.md). Линии строятся сплайнами и MoGraph.
- Голос: нет встроенной привязки к тексту озвучки; аудио можно подключить на временную шкалу.
- Агент: с 2026-09-30 в 2026.4 встроен MCP-сервер. Через него ИИ-ассистент организует сцену, делает варианты материалов и объектов, готовит рендер-проходы, делает UV (по сообщению прессы и описанию Maxon).

## Слабые стороны

- Платная подписка, бесплатной рабочей версии нет. Пробная версия и учебная лицензия запрещают коммерческое использование (см. «Лицензия»).
- Файл `.c4d` двоичный, в git не читается.
- MCP-сервер по сообщению CG Channel недоступен в Lite-версии для After Effects, в Team Render и при рендере из командной строки. Он выключен по умолчанию.
- Агентская автоматизация новая (2026-09-30). В описании DigitalProduction: демонстрации на заготовленных сценах, после первого прохода трекинг пришлось исправлять; режим «автопилот» не обоснован.
- Лицензия на командный рендер (Command Line Render Client) разрешает рендер только своих работ, не услуг для третьих лиц (EULA §6.3).

## Сложность

- Для человека (4 из 5): MoGraph быстрее Blender для графики, но программа профессиональная. Освоение занимает недели.
- Для агента (3 из 5): есть Python SDK и MCP-сервер, значит часть сцены собирается кодом. Но проект двоичный, работа идёт внутри запущенной программы с лицензией. Рендер из командной строки возможен. Часть работы остаётся за человеком.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): Python SDK; в EULA упомянут Command Line Render Client для фермы; MCP-сервер для ИИ-ассистентов.
- Воспроизводимость (3 из 5): проектный файл воспроизводит результат, но он двоичный. Сборка сцены скриптом возможна, но не проверялась.

## Платформа и оборудование

Windows (в том числе Windows on Arm по странице Maxon) и macOS. По CG Channel: Windows 10 и новее, macOS 14.0 и новее. Версия для iPad по странице Maxon выйдет «в конце 2026». Redshift работает на GPU.

## Экспорт

Видео и последовательности кадров через рендер (Redshift). Cineware связывает Cinema 4D с After Effects (входит в Maxon One). Точные списки форматов и ограничения пробной версии не проверялись.

## Стоимость

Проверено 2026-10-14. Цены на странице Maxon подгружаются скриптом, в тексте страницы их нет. Официально подтверждено: «Save 30% or more with Annual billing»; пакеты (bundles) продаются по этой цене на первый год, потом подписка продлевается автоматически; пробная версия 14 дней.

Вторичные данные, не первоисточник:
- CG Channel (2026-09-30): подписка Cinema 4D стоит $109 в месяц или $839 в год.
- Super Renders Farm (чтение страницы Maxon One от 2026-10-06): Maxon One — €1 425,57 за лицензию в год, возможно с НДС.

Maxon One включает Cinema 4D, ZBrush, Redshift, Red Giant, Universe, Autograph, библиотеку Capsules и пять нод Team Render.

## Лицензия и права

- Код или программа: proprietary, [EULA Maxon](https://www.maxon.net/en/legal/eula) от сентября 2026.
- Результат: пробная лицензия даёт право на «testing and evaluating», использование «directly or indirectly for business or commercial purposes … is expressly prohibited» (14 дней). Учебная лицензия для студентов и преподавателей не разрешает «commercial, professional or other profit-making purposes». Платная подписка разрешает коммерческую работу. Пункта о передаче прав на результат Maxon при поиске по тексту EULA не нашёл (не юридический разбор).
- Ассеты в комплекте: Capsules и учебные материалы (Cineversity) идут по условиям подписки; условия отдельных ассетов не проверены.

## Активность и зрелость

Зрелость: `standard`. По DigitalProduction, Cinema 4D 2026.2 вышла 2026-04-15, по CG Channel 2026.4 вышла 2026-09-30 (новое: MCP-сервер). На странице Maxon: «This fall, Cinema 4D 2027.0» (система Scatter и др.). Вышла ли 2027.0 на 2026-10-14, не подтверждено; на канале Maxon 2026-10-14 опубликован ролик про «Fall Release 2026». Развивает Maxon.

## Когда брать и когда нет

- Брать: заголовки, инфографика, абстрактные превращения форм, быстрая итерация в motion design, если есть бюджет на подписку.
- Не брать: если бюджет нулевой или нужен текстовый, воспроизводимый из git проект ([blender](blender.md), [godot](godot.md)); если нужна научная симуляция ([houdini](houdini.md)).

## Источники

- [Cinema 4D на сайте Maxon](https://www.maxon.net/en/cinema-4d) — Redshift в подписке, MoGraph, 2027.0 «this fall», платформы. Проверено 2026-10-14.
- [Maxon One](https://www.maxon.net/en/maxon-one) — состав, пробная версия 14 дней. Проверено 2026-10-14.
- [Страница покупки](https://www.maxon.net/en/buy) — скидка за год; цен в тексте нет. Проверено 2026-10-14.
- [EULA Maxon](https://www.maxon.net/en/legal/eula) — пробная лицензия, учебная лицензия, Command Line Render Client. Проверено 2026-10-14.
- [Учебные лицензии](https://www.maxon.net/en/educational-licenses) — «may not be used for commercial, professional, or other profit-making purposes». Проверено 2026-10-14.
- [CG Channel, 2026-09-30](https://www.cgchannel.com/?p=179009) — Cinema 4D 2026.4, MCP-сервер, цена $109/$839 (вторичный источник). Проверено 2026-10-14.
- [DigitalProduction, 2026-10-01](https://digitalproduction.com/2026/10/01/cinema-4d-2026-4-mcp/) — подробности MCP, ограничения. Проверено 2026-10-14.
- [DigitalProduction, 2026-04-15](https://digitalproduction.com/2026/04/15/maxon-ships-cinema-4d-2026-2-update/) — выход 2026.2. Проверено 2026-10-14 (по результатам поиска, страницу целиком не читал).
- [Super Renders Farm](https://superrendersfarm.com/article/what-3d-software-costs-2026) — Maxon One €1 425,57 (вторичный). Проверено 2026-10-14.
- [Python SDK](https://developers.maxon.net/docs/py/2026_2_0/) — документация Python SDK 2026.2.0. Проверено 2026-10-14.
- Ролики на канале Maxon (ссылки выше): названия подтверждены через oEmbed. Проверено 2026-10-14.

## Неизвестно

- Официальная цена Cinema 4D и Maxon One: страница Maxon показывает её скриптом; записаны вторичные данные.
- Вышла ли версия 2027.0 к 2026-10-14.
- Форматы вывода и ограничения пробной версии.
- Научно-популярный канал, который публично называет Cinema 4D своим инструментом, не найден.
- Как именно работает `c4dpy` и командный рендер (справка Maxon не читалась целиком; в EULA упомянут только Command Line Render Client).
