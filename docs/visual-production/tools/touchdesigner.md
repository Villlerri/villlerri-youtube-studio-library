---
id: touchdesigner
name: TouchDesigner
class: [procedural]
kind: app
site: https://derivative.ca
github: none
scenes: [field, simulation, micro, typography]
quality: 5
human_difficulty: 4
agent_difficulty: 4
automation: 3
reproducibility: 3
cost: 3
maturity: standard
platforms: [windows, macos]
export: [mp4, mov, prores, png-sequence, exr-sequence]
code_license: proprietary
price: Non-Commercial бесплатно (до 1280x1280); Commercial от $600 разово; Pro от $2200
checked: 2026-10-14
---

# TouchDesigner

Нодовая среда реального времени от компании Derivative. Строит графику, генеративные сцены, интерактив и инсталляции из связанных операторов. Для видео нужен режим записи: среда рассчитана на живую работу, но умеет рендерить файл без пропусков кадров.

## Ссылки

- Официальный сайт: https://derivative.ca (также https://touchdesigner.com)
- GitHub: открытого кода нет.
- Документация: https://docs.derivative.ca/
- Примеры, проверенные 2026-10-14 (ролики проверены через oEmbed, видео не смотрел):
  - [My TouchDesigner showreel 2023](https://www.youtube.com/watch?v=TPJBla30kHM) — канал TakeCare; подборка генеративных работ, сделанных по урокам и собственным опытам.
  - [Generative graphics showreel 2021-2022](https://www.youtube.com/watch?v=hvaInjBTmaE) — канал Алены Осиповой; генеративная графика в TouchDesigner.
  - [TouchDesigner Tutorial - Export Movie](https://www.youtube.com/watch?v=LcuI5uJAtyU) — канал Bryan Chung; как выгрузить файл.
  - [Export videos with transparent background and with audio](https://www.youtube.com/watch?v=DoQn9ggGgbY) — канал Alexxxxxi; прозрачный фон и звук в выгрузке.
  - [TouchDesigner InSession with Ana Herruzo](https://www.youtube.com/watch?v=gPWQXwhRV8o) — на канале «TouchDesigner» (официальном).

## Что реально получается

- Генеративные поля, частицы, шум, абстрактные 3D и 2D, VJ-графика, данные в реальном времени. Сцены `field`, `simulation`, `micro`, `typography`.
- Анимация: компонент Animation COMP — ключевые кадры каналов с кривыми, привязка к таймлайну или режим последовательности.
- Камера и 3D: Camera COMP, Geometry COMP и остальные операторы; сцена остаётся одним графом, камера двигается без склеек. Непрерывность сцены — свойство среды: всё считается каждый кадр.
- Морфинг и рисование линий: делаются из операторов (шум, смешение, текстуры); готового «морфинга формул» нет.
- Типографика: Text TOP и операторы геометрии; кинетическая типографика строится вручную.
- Шейдеры: GLSL TOP «renders a GLSL shader into a TOP image», шейдеры в духе [glsl-shadertoy](glsl-shadertoy.md) переносятся вручную.
- Звук и голос: оператор Audio Spectrum CHOP и запись звука с Movie File Out TOP. Синхронизация под озвучку делается ключами и сигналами, а не автоматически.
- Потолок качества (5 из 5): картинка уровня студийных VJ-проектов и инсталляций; для научно-популярного ролика — на уровне лучших каналов, если есть художник.

## Слабые стороны

- Бесплатная Non-Commercial ограничена 1280x1280 и не годится для проектов, за которые платят. Выгрузка H.264/H.265/AV1 в документации Movie File Out TOP отнесена к Commercial и Pro (страница загрузки называет эту функцию ещё у Educational); на Windows нужна NVIDIA.
- Файл проекта `.toe` двоичный: git показывает только факт изменения. Сравнение и слияние невозможны.
- Высокий порог входа: сотни операторов, свои соглашения, отдельная мышиная модель управления (нужна мышь с тремя кнопками или колесом).
- Только Windows и macOS. Нет Linux.
- Создание сцены — работа в интерфейсе. Агент может писать Python внутри TouchDesigner, но самостоятельно собрать и проверить сцену не может.
- Правила монетизации YouTube-канала в проверенных страницах не определены, см. «Неизвестно».

## Сложность

- Для человека (4 из 5): нужно освоить типы операторов (TOP, CHOP, SOP, DAT, COMP), принцип «всё пересчитывается каждый кадр», иногда Python и GLSL. Первая сцена за неделю, уверенный стиль — месяцы.
- Для агента (4 из 5): внутри встроен Python 3.11 с модулем `td`, доступным без импорта, сцену можно создавать скриптом. Но проект двоичный, нужен запущенный клиент с лицензией и видеокартой, а результат оценивается глазами. Агент пишет скрипты и сетевые обёртки, человек собирает и проверяет граф.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): Python внутри, `td.run`, Execute DAT, переменные окружения при старте, оператор `Movie File Out` и режим без реального времени. Официальный справочник командной строки для безголового запуска не нашёл (страница `Command_Line_Usage` ответила 404). TouchEngine встраивает `.tox`-компоненты в другие программы, конечному пользователю нужна платная лицензия TouchDesigner или TouchPlayer.
- Воспроизводимость (3 из 5): проект — двоичный `.toe`, но воспроизводит результат. Запись без пропусков делается так: выключить флаг Realtime («Recording a movie without frame drops can be done in non-realtime»), включить Record. Оператор считает пропущенные кадры (Info CHOP, `total_frames_dropped`). Для пошаговой записи есть Pause и Add Frame.

## Платформа и оборудование

- Windows 10 или 11; macOS 13 (Ventura) или новее. Windows: минимум 4 ГБ видеопамяти, рекомендуется 8 ГБ и больше; NVIDIA GeForce 1000-й серии и новее (драйвер 530 и выше; рекомендуется 581 и выше), AMD Radeon 5000 и новее, встроенная Intel серии 500 и новее (не все функции). macOS: Mac с 2020 года и новее; Apple Silicon настоятельно рекомендован; Intel-Mac требуют дискретной AMD.
- Рекомендуется SSD для воспроизведения видео.

## Экспорт

- Оператор Movie File Out TOP: H.264 и H.265 (на Windows только NVIDIA; на macOS H.264 поддержан), Apple ProRes, Hap, Hap Q, GoPro-Cineform, Animation; контейнеры `.mov`, `.mp4`, `.mkv`, `.webm`; последовательности изображений TIFF, JPEG, BMP, OpenEXR, PNG, DDS.
- Прозрачность: Animation, Hap, Hap Q и Cineform принимают RGBA; H.264 и H.265 — только YUV; PNG, TIFF, EXR, BMP, DDS хранят альфу.
- Звук пишется вместе с видео; для него нужен CHOP со стереодорожкой. Если запись идёт медленнее частоты кадров, оператор повторяет видеокадры, чтобы не терять синхронизацию.
- Разрешение: в Non-Commercial до 1280x1280, иначе предел видеокарты.

## Стоимость

Проверено 2026-10-14 по [магазину](https://derivative.ca/shop) и [странице загрузки](https://derivative.ca/download).

- Non-Commercial: бесплатно. «For personal use or learning. Not for paying projects», «Resolution limited to 1280x1280», 10 ключей на аккаунт.
- Educational: от $300, для школ и студентов, не для оплачиваемых проектов.
- Commercial: $600 (плавающая облачная лицензия $900). Для проектов, за которые платят.
- Pro: $2,200 (плавающая облачная $3,300). Все функции Commercial, синхронизация нескольких машин, hardware frame-lock, Pro Support (6 часов).
- Лицензии бессрочные и включают обновления на 1 год. Обновления дальше: Commercial $300 за год или $510 за два; Pro $400 за год или $680 за два. Конвертация Commercial в Pro — $1,600.
- По шкале методики: разовая покупка выше $500, поэтому оценка стоимости 3.

## Лицензия и права

- Код или программа: проприетарная, исходников нет.
- Результат: Non-Commercial запрещает оплачиваемые проекты. Документация: «Anyone compensated for their TouchDesigner work needs a Commercial or Pro license». Водяной знак в проверенных страницах не упомянут.
- Ассеты в комплекте: условия на готовые компоненты и примеры из поставки не проверял.

## Активность и зрелость

Для GitHub-статистики у программы нет репозитория. Зрелость: `standard` — широкий отраслевой инструмент для интерактивных инсталляций и живой графики. Текущая версия на странице загрузки — 2025.33230 с датой 2026-09-01 для Windows и macOS. Разрабатывает Derivative; есть официальный форум и канал TouchDesigner на YouTube.

## Когда брать и когда нет

- Брать: генеративные фоны, поля, абстракции и «живые» сцены на уровне VJ-визуала, ролики, где важен художественный стиль, а не точные формулы; команда с графическим дизайнером; Windows или macOS.
- Не брать: формулы и вывод выкладок ([manim-ce](manim-ce.md)), пакетное производство без человека, бюджет до сотен долларов на проект без лицензии, Linux. Для 3D с процедурными методами смотри также [houdini](houdini.md) и [blender-geometry-nodes](blender-geometry-nodes.md).

## Источники

- [Магазин Derivative](https://derivative.ca/shop) — цены лицензий, обновлений, конвертации. Проверено 2026-10-14.
- [Страница загрузки](https://derivative.ca/download) — версия 2025.33230 (2026-09-01), типы лицензий, ограничение 1280x1280, системные требования. Проверено 2026-10-14.
- [Руководство: обновления](https://derivative.ca/UserGuide/Updates) — «licenses are perpetual and include updates for 1 year». Проверено 2026-10-14.
- [Документация: Licensing](https://docs.derivative.ca/Licensing) — четыре уровня, кому нужна Commercial. Проверено 2026-10-14.
- [Документация: Movie File Out TOP](https://docs.derivative.ca/Movie_File_Out_TOP) — кодеки, контейнеры, альфа, запись без пропусков, звук. Проверено 2026-10-14.
- [Руководство: Movie File Out TOP](https://derivative.ca/UserGuide/Movie_File_Out_TOP) — H.264, H.265, AV1 только для Commercial и Pro, NVIDIA на Windows. Проверено 2026-10-14.
- [Документация: TouchDesigner Products](https://docs.derivative.ca/TouchDesigner_Products) — resolution 1280x1280, Commercial. Проверено 2026-10-14.
- [Документация: Python](https://docs.derivative.ca/Python) — Python 3.11, модуль `td`. Проверено 2026-10-14.
- [Документация: Animation COMP](https://docs.derivative.ca/Animation_COMP) и [GLSL TOP](https://docs.derivative.ca/GLSL_TOP), [TouchEngine](https://docs.derivative.ca/TouchEngine). Проверено 2026-10-14.
- Ролики YouTube: [TPJBla30kHM](https://www.youtube.com/watch?v=TPJBla30kHM), [hvaInjBTmaE](https://www.youtube.com/watch?v=hvaInjBTmaE), [LcuI5uJAtyU](https://www.youtube.com/watch?v=LcuI5uJAtyU), [DoQn9ggGgbY](https://www.youtube.com/watch?v=DoQn9ggGgbY), [gPWQXwhRV8o](https://www.youtube.com/watch?v=gPWQXwhRV8o) — живые по oEmbed. Проверено 2026-10-14.

## Неизвестно

- Можно ли в Non-Commercial лицензии выкладывать на монетизируемый YouTube-канал: Derivative говорит «Not for paying projects», но определение «оплачиваемого проекта» для рекламной выручки в проверенных страницах не найдено.
- Работает ли выгрузка ProRes, Hap и Animation в Non-Commercial и на обеих ОС: страницы ограничения называют только H.264/H.265/AV1.
- Команды запуска без интерфейса (безголовый рендер из командной строки): официальную страницу не нашёл, форум даёт устаревшие ответы.
- Есть ли водяной знак в бесплатной версии: упоминаний не нашёл.
- Будущие обновления: страница загрузки указывает Official и Experimental без номеров; какая сборка считается стабильной, неясно.
