---
id: opentoonz
name: OpenToonz
class: [frame-vector-skeletal]
kind: app
site: https://opentoonz.github.io/e/
github: opentoonz/opentoonz
scenes: [character, drawing]
quality: 4
human_difficulty: 4
agent_difficulty: 4
automation: 3
reproducibility: 2
cost: 0
maturity: stable
platforms: [windows, macos, linux]
export: [png-sequence, mov, gif, mp4, webm]
code_license: BSD-3-Clause
price: бесплатно, в том числе для коммерческих проектов
checked: 2026-10-14
---

# OpenToonz

Открытая версия студийного пакета Toonz (его использовала Studio Ghibli). Рисованная покадровая анимация, очистка сканов, кукольная анимация, эффекты и пакетный рендер. Профессионально, но интерфейс старый и неудобный.

## Ссылки

- Официальный сайт: https://opentoonz.github.io/e/
- GitHub: https://github.com/opentoonz/opentoonz
- Документация: https://opentoonz.readthedocs.io/en/latest/ (руководство для версии 1.7.1)
- Примеры, проверенные 2026-10-14 (ролики открывались через oEmbed, содержание описано по названию, не смотрел; все сторонние):
  - [Studio Ghibli - Animation Open Source - OpenToonz](https://www.youtube.com/watch?v=lGFUtqM8oAs) — канал Penta News, рассказ об использовании в студии.
  - [Indivisible - Animation process (Opentoonz)](https://www.youtube.com/watch?v=54jlcCClBf0) — канал Opentoonz Cartoon, процесс анимации в программе.
  - [OpenToonz Animation Powerhouse Software (Free & Open Source!)](https://www.youtube.com/watch?v=x_kbuQNxzik) — канал Gamefromscratch, обзор программы.

## Что реально получается

- Рисованная анимация на растровых, векторных и «Toonz»-уровнях, калька, раскадровка по листу экспозиции (Xsheet) или временной шкале.
- Кукольная анимация: «Cutout» и инструмент Plastic для деформации картинки по сетке с костями (разделы руководства).
- Эффекты: узловая схема эффектов (FX Schematic), частицы (Particles), справочник FX. Многослойный вывод: один сценарий рендерится в несколько файлов по слоям.
- Камера: несколько камер в сцене, выбирается выходная камера (Output Camera). Мультиплан-камеры нет в просмотренных страницах.
- Плавность: подбор позиции и кривые в таблицах и графиках (Spreadsheet and Curves). Автоматического морфинга одной векторной формы в другую в руководстве не нашёл.
- Голос: звуковая дорожка и покадровая подгонка. Автоматического липсинка нет в просмотренных страницах (в [tahoma2d](tahoma2d.md) он есть).
- Для объясняющего видео это путь к рисованной подаче «как студийный мультфильм». Для схем и графиков он не нужен.

## Слабые стороны

- Интерфейс и справка устарели: руководство написано для 1.7.1, текущая версия 1.8.
- MP4 и WebM требуют отдельной установки FFmpeg. Из коробки нативные форматы: 3GP, AVI, BMP, GIF, JPG, MOV, PNG, RGB, SGI, TGA, TIF, спрайт-лист. 3GP и MOV работают через 32-битный QuickTime.
- Выпуски редкие: 1.7.1 в 2023 году, 1.8 в июне 2026 года, потом ночные сборки.
- Сложнее и менее удобен, чем [tahoma2d](tahoma2d.md), созданный на его основе.

## Сложность

- Для человека (4 из 5): много концепций (уровни, Xsheet, палитры, схема эффектов), документация неполная. Нужен опыт анимации.
- Для агента (4 из 5): графический интерфейс. Есть скрипты ToonzScript и, судя по исходникам, утилиты `tcomposer` и `tcleanupper`, но нет проверенного способа собрать анимацию без рук.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): ToonzScript на основе QtScript с консолью (работа с файлами, уровнями, сценами, векторизацией, рендерером). Рендер ставится в очередь (панель Tasks), есть распределённый рендер Toonz Farm. В репозитории есть каталог `tcomposer`; в готовых сборках его работу из командной строки не проверял.
- Воспроизводимость (2 из 5): сцена хранится в файле `.tnz` с папками уровней. Формат файла не проверял, обычного для git текстового проекта не обещано. Рендер зависит от установленного FFmpeg.

## Платформа и оборудование

Windows, macOS, Linux, FreeBSD, DragonFly BSD (раздел «Installing OpenToonz» руководства). Требований к видеокарте в просмотренных страницах нет.

## Экспорт

- Нативно: 3GP, AVI, BMP, GIF, JPG, MOV, NOL, PNG, RGB, SGI, спрайт-лист, TGA, TIF. 3GP и MOV через 32-битный QuickTime.
- MP4 и WebM (и GIF на Mac) через установленный FFmpeg.
- Вывод с альфа-каналом описан в разделе «Rendering Animations with Alpha Channel Information». Разрешение и частота кадров задаются в настройках вывода.

## Стоимость

Проверено 2026-10-14. Бесплатно; на [сайте проекта](https://opentoonz.github.io/e/) сказано: можно использовать без оплаты в коммерческих и некоммерческих проектах. Платных тарифов нет.

## Лицензия и права

- Код или программа: исходный код под BSD 3-Clause ([LICENSE.txt](https://github.com/opentoonz/opentoonz/blob/master/LICENSE.txt)). Готовые сборки с сайта идут по [Условиям использования](https://opentoonz.github.io/e/download/opentoonz.html) компании Dwango: право использовать, запрет использовать не по документации и нарушать права третьих лиц.
- Результат: в условиях Dwango нет пункта о правах на созданные ролики; сайт разрешает коммерческое использование. Водяных знаков нет.
- Ассеты в комплекте: кисти MyPaint с отдельными лицензиями в `stuff/library/mypaint brushes/Licenses.txt`; третьи библиотеки в `thirdparty`.

## Активность и зрелость

<!-- gh-stats:opentoonz/opentoonz -->
- Звёзды GitHub: 7 822
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: nightly (2026-10-14)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория opentoonz/opentoonz, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Версия 1.8.0 вышла 2026-06-19 (кандидат от 2026-05-29), предыдущая 1.7.1 в 2023 году; ночные сборки выходят ежедневно (последняя 2026-10-14). Развивает компания Dwango вместе с сообществом.

## Когда брать и когда нет

- Брать: бесплатный студийный пайплайн рисованной анимации, если есть опытный аниматор и важна пакетная работа. Хорошо для серии роликов с одним персонажем.
- Не брать: если нужен удобный интерфейс и быстрый старт — берите [tahoma2d](tahoma2d.md). Для векторных кукол с костями — [synfig](synfig.md) или [moho](moho.md). Для коротких схем — код.

## Источники

- [Сайт OpenToonz](https://opentoonz.github.io/e/) — происхождение, бесплатность для коммерческого использования, BSD для исходников. Проверено 2026-10-14.
- [Условия использования](https://opentoonz.github.io/e/download/opentoonz.html) — условия готовых сборок. Проверено 2026-10-14.
- [LICENSE.txt](https://raw.githubusercontent.com/opentoonz/opentoonz/master/LICENSE.txt) — BSD 3-Clause. Проверено 2026-10-14.
- [Releases](https://github.com/opentoonz/opentoonz/releases), [v1.8.0](https://github.com/opentoonz/opentoonz/releases/tag/v1.8.0) — версии и даты. Проверено 2026-10-14.
- [Руководство OpenToonz](https://opentoonz.readthedocs.io/en/latest/), [Previewing and Rendering](https://opentoonz.readthedocs.io/en/latest/rendering_the_animation.html), [FFmpeg](https://opentoonz.readthedocs.io/en/latest/using_ffmpeg_with_opentoonz.html), [ToonzScript](https://opentoonz.readthedocs.io/en/latest/toonzscript.html) — функции, форматы, скрипты. Проверено 2026-10-14.
- [Каталог исходников](https://github.com/opentoonz/opentoonz/tree/master/toonz/sources) — наличие `tcomposer` и `tcleanupper`. Проверено 2026-10-14.
- Названия и авторы роликов проверены через oEmbed YouTube 2026-10-14.

## Неизвестно

- Есть ли в релизе 1.8 командная строка для рендера (утилиты видны только в исходниках) и какие у неё ключи.
- Формат файла `.tnz` и пригодность для git.
- Морфинг векторных форм и липсинк в OpenToonz.
- Различия 1.8 и 1.7.1: руководство описывает 1.7.1.
- Содержание роликов-примеров оценено по названию и описанию.
