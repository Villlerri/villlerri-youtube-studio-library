---
id: houdini
name: Houdini
class: [3d, procedural, simulation]
kind: app
site: https://www.sidefx.com/products/houdini/
github: none
scenes: [simulation, field, scale, mechanism]
quality: 5
human_difficulty: 5
agent_difficulty: 3
automation: 4
reproducibility: 3
cost: 2
maturity: standard
platforms: [macos, windows]
export: [mp4, exr-sequence, png-sequence]
code_license: proprietary
price: Apprentice бесплатно (некоммерческий), Indie $299 в год или $449 на 2 года, Core и FX цена на странице не указана
checked: 2026-10-14
---

# Houdini

Процедурный 3D-пакет SideFX с узловой логикой во всём: геометрия, анимация, эффекты, симуляции. Эталон для жидкости, дыма, огня, разрушений, частиц и ткани. Самый крутой порог входа среди 3D-пакетов.

## Ссылки

- Официальный сайт: https://www.sidefx.com/products/houdini/
- GitHub: открытого кода программы нет.
- Документация: https://www.sidefx.com/docs/houdini/ ([командная строка и hython](https://www.sidefx.com/docs/houdini/hom/commandline.html), [husk](https://www.sidefx.com/docs/houdini/ref/utils/husk.html), [новости H22](https://www.sidefx.com/docs/houdini/news/22/index.html))
- Примеры, проверенные 2026-10-14:
  - [2025 Houdini Film-TV-Games Reel (канал Houdini)](https://www.youtube.com/watch?v=nMSj-H95eiE) — рил студий и художников. Показывает потолок эффектов и симуляций, но не научно-популярное видео.
  - [2025 Houdini Student Reel](https://www.youtube.com/watch?v=sLkEHjKzA50) — работы студентов; уровень, достижимый за курс обучения.

## Что реально получается

- Симуляции: по странице SideFX Houdini FX даёт «simulating Fluids, Destruction, Pyro FX, Grains, Cloth and more». В заметках H22 отдельные разделы Pyro, Vellum, Rigid body dynamics, Particles and MPM. Если нужно «физически честное» поведение жидкости или дыма, это сильнейший вариант.
- Процедурность: параметры сцены можно менять, и весь граф пересчитывается. Подходит для вариантов одной сцены.
- Непрерывность: симуляция и камера живут в одной сцене. Морфинг любых геометрий через узлы возможен (оценка).
- Рендер: Karma (в Solaris, на основе USD); рендер из командной строки через `husk`. Karma XPU входит в Indie.
- H22 (2026): Gaussian Splats (обучение, правка, рендер), Vulkan-вьюпорт, GPU Pyro в Copernicus, улучшения персонажей (APEX, KineFX).
- Рисование линий, формулы, диаграммы: не для этого.
- Голос: встроенной привязки нет; тайминг задаётся скриптом.

## Слабые стороны

- Очень высокий порог входа, месяцы до свободной работы.
- Apprentice нельзя использовать для монетизируемого канала (только некоммерческие проекты), рендер ограничен 1920×1080 и получает водяной знак, свой формат файла.
- Indie ограничен по доходу и финансированию, свой формат файла, нельзя смешивать с коммерческими Houdini в одном конвейере.
- Нужна мощная машина; симуляции жидкости и дыма тяжёлые (оценка).

## Сложность

- Для человека (5 из 5): профессиональный инструмент, сложные графы, свой язык VEX.
- Для агента (3 из 5): Python (hython, HOM) и командная строка (`husk`) дают скриптуемый рендер и сборку графов. Но осмысленный граф агент собирает с трудом, симуляции нужно настраивать на глаз. Часть работы остаётся за человеком.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): hython (Python), `husk` (рендер USD), PDG (в списке H22), Houdini Engine для других приложений (платный, у Indie отдельная бесплатная версия).
- Воспроизводимость (3 из 5): проектный файл воспроизводит результат, но он двоичный. Цифровые активы (HDA) и скрипты можно версионировать частично.

## Платформа и оборудование

H22: по DigitalProduction, Windows 11 и новее, macOS только на Apple Silicon, Python 3.13.10, USD 26.05, вьюпорт на Vulkan. Страница системных требований SideFX открылась только как ссылка (`sidefx.com/Support/system-requirements/`), я её не читал. Linux в H22 в проверенных источниках не подтверждён, поэтому в поле platforms его нет.

## Экспорт

- Рендер Karma или сторонними движками; последовательности кадров (EXR и др.) и видео через внешние инструменты. Подробный список форматов не проверялся.
- Apprentice: разрешение до 1920×1080; рендер в форматы кроме `.picnc` получает водяной знак (на странице: «wordmarked»); в таблице сравнения у EXR/TIF/JPG стоит «WATERMARK».

## Стоимость

Проверено 2026-10-14 по [странице покупки](https://www.sidefx.com/buy/) и [странице Indie](https://www.sidefx.com/products/houdini-indie/).

- Apprentice: бесплатно, только некоммерческие проекты.
- Indie: $299 на 1 год или $449 на 2 года. Условия: годовой валовой доход коммерческой или контрактной организации не выше $100 тыс. USD; полученное за последние 24 месяца финансирование меньше $1 млн; не более трёх лицензий на студию; лицензия на одного художника.
- Core и FX: на странице покупки цены не указаны, продаются как постоянная лицензия или аренда. Karma входит в Core и FX; лишние Karma-токены по странице сравнения стоят $195. Houdini Engine по странице сравнения $525 в год за рабочее место, Indie Engine бесплатен.
- Вторичный источник (не проверено): Super Renders Farm, чтение страниц SideFX от 2026-10-06 — Houdini FX $3505 за год аренды.

## Лицензия и права

- Код или программа: proprietary, [EULA SideFX](https://www.sidefx.com/legal/license-agreement/).
- Результат: Apprentice — «must be used on Non-commercial projects», подробности на странице отсылают к EULA; заявления о монетизации YouTube на страницах нет. Indie — «Limited Commercial»: коммерческая работа разрешена при условиях выше.
- Ассеты в комплекте: условия не проверены.

## Активность и зрелость

Зрелость: `standard`. Версия H22 вышла в июле 2026 (DigitalProduction от 2026-07-16 сообщает сборку 22.0.368 и срок «примерно три недели после июньского кейноута»; точная дата выпуска на проверенных страницах SideFX не указана). Развивает SideFX.

## Когда брать и когда нет

- Брать: честная физика жидкости, дыма, разрушения; много вариантов одной сцены; студия с бюджетом и временем.
- Не брать: быстрые учебные схемы (там [blender](blender.md), [cinema-4d](cinema-4d.md)); если нужен простой воспроизводимый текстовый проект ([godot](godot.md), [blender](blender.md)).

## Источники

- [Покупка](https://www.sidefx.com/buy/) — Apprentice бесплатно, Indie, лимиты лицензий. Проверено 2026-10-14.
- [Indie](https://www.sidefx.com/products/houdini-indie/) — $299 или $449, $100 тыс., финансирование $1 млн. Проверено 2026-10-14.
- [Apprentice](https://www.sidefx.com/products/houdini-apprentice/) — некоммерческий, 1920×1080, водяной знак, срок лицензии. Проверено 2026-10-14.
- [Сравнение продуктов](https://www.sidefx.com/products/compare/) — Core, FX, Indie, Apprentice; $195 Karma, $525 Engine. Проверено 2026-10-14; структура таблицы читалась неточно, цифры $195 и $525 взяты из пересказа.
- [Главная Houdini](https://www.sidefx.com/products/houdini/) — симуляции, H22. Проверено 2026-10-14.
- [Новости H22](https://www.sidefx.com/docs/houdini/news/22/index.html) — список разделов. Проверено 2026-10-14.
- [DigitalProduction, 2026-07-16](https://digitalproduction.com/2026/07/16/houdini-22-how-right-were-we/) — сборка 22.0.368, возможности H22. Проверено 2026-10-14.
- [Команды hython](https://www.sidefx.com/docs/houdini/hom/commandline.html) и [husk](https://www.sidefx.com/docs/houdini/ref/utils/husk.html). Проверено 2026-10-14.
- [Super Renders Farm](https://superrendersfarm.com/article/what-3d-software-costs-2026) — вторичные цены. Проверено 2026-10-14.
- Ролики Houdini (ссылки выше): названия подтверждены через oEmbed. Проверено 2026-10-14.

## Неизвестно

- Цена Houdini Core и FX (на странице нет).
- Точная дата выхода H22 на сайте SideFX.
- Можно ли монетизировать YouTube-ролик, отрендеренный в Apprentice: ответ в EULA, текст EULA не читался.
- Учитывается ли доход YouTube-канала в лимит $100 тыс. Indie.
- Системные требования H22 (страница не читалась), поддержка Linux.
- Научно-популярный канал, прямо называющий Houdini своим инструментом, не найден.
