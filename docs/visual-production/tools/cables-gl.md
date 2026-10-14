---
id: cables-gl
name: cables.gl
class: [procedural, web-graphics]
kind: app
site: https://cables.gl
github: cables-gl/cables
scenes: [field, typography, diagram]
quality: 3
human_difficulty: 3
agent_difficulty: 4
automation: 2
reproducibility: 3
cost: 0
maturity: young
platforms: [web, windows, macos, linux]
export: [html, webm]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# cables.gl

Визуальная среда в браузере: операторы соединяют «кабелями» и получают WebGL-сцену, звук и интерактив. Работает в вебе и как автономное приложение без интернета. Проект стал открытым (MIT). Видео из него записывается в реальном времени; покадрового экспорта в проверенной документации нет.

## Ссылки

- Официальный сайт: https://cables.gl
- GitHub: https://github.com/cables-gl/cables (ядро и операторы); редактор — https://github.com/cables-gl/cables_ui, автономное приложение — https://github.com/cables-gl/cables_electron
- Документация: https://cables.gl/docs
- Примеры, проверенные 2026-10-14 (ролики проверены через oEmbed, видео не смотрел):
  - [Introduction to cables.gl: data-driven gradient from geo-located weather](https://www.youtube.com/watch?v=xnObNRv8n9I) — канал Kirell Benzi; градиент по данным погоды.
  - [Introduction to Cables.gl (1/13)](https://www.youtube.com/watch?v=VsS4gaJ7pMw) — канал Decode GL; первая часть вводного курса из 13 уроков.
  - [Using Cables.GL to make a live visuals application](https://www.youtube.com/watch?v=__QxceKIT1c) — канал Steve's Peeves; приложение для живых визуалов.
  - [cables: web based visual programming language for WebGL and Web Audio](https://www.youtube.com/watch?v=32xHw6BWIRI) — доклад Tim Pulver (Web Audio Conf).
  - [Страница оператора MediaRecorder](https://cables.gl/op/Ops.Gl.MediaRecorder) — запись видео.

## Что реально получается

- Живая WebGL-графика: шейдерные фоны, частицы, текст, 3D-объекты, данные из сети. Сцены `field`, `typography`, `diagram`.
- Анимация: операторы времени, кривые и параметры; готового таймлайна под ролик нет.
- Непрерывность: патч — один живой граф; сцена течёт без склеек.
- Камера, морфинг, рисование линий: собираются из операторов; готового «рисования вживую» нет.
- Голос: операторы работают со звуком Web Audio; привязки к озвучке нет.
- Потолок качества (3 из 5): красивые интерактивные визуалы, но научно-популярной эстетики из коробки нет; эффекты зависят от вкуса автора и браузерного WebGL.

## Слабые стороны

- Запись видео: оператор MediaRecorder пишет через браузер «в любой видеокодек, который поддерживает ваш браузер» (формат выбирается по Mimetype). На странице оператора предупреждено, что скачанное видео «не имеет длительности и перематываемой шкалы» и может потребовать перекодирования для видеоредакторов. Запись идёт в реальном времени, пропуски кадров возможны. Покадровый точный экспорт в проверенной документации не найден.
- Оператор Download Texture сохраняет изображение (кадры) в нужном разрешении по запросу, но не последовательностью автоматически.
- Версии нулевые: автономное приложение 0.12.0, ядро v0.6.0; частые изменения.
- Нет формул, графиков с осями и подписями, вывода выкладок.
- Проекты — файлы `.cables`; формат не изучал.

## Сложность

- Для человека (3 из 5): визуальные операторы понятны за неделю, но для красивого результата нужны WebGL-знания и вкус. Есть курсы, в том числе серия из 13 уроков.
- Для агента (4 из 5): патч собирается в редакторе мышью, операторы можно писать на JavaScript. Командная строка `cables-cli` относится к экспорту. Сборка сцены агентом по умолчанию невозможна без работы руками.

## Автоматизация и воспроизводимость

- Автоматизация (2 из 5): есть экспорт в архив ZIP, GitHub Pages, автономный exe и командную строку `cables-cli` (по оглавлению документации), встраивание в сайт. Страница экспорта через командную строку не говорит, что именно экспортируется. Покадровой записи видео не нашёл.
- Воспроизводимость (3 из 5): патч хранится файлом `.cables`, экспорт включает информацию о лицензиях библиотек. Версионирование через git возможно (экспорт на GitHub), но формат файла не проверял.

## Платформа и оборудование

Веб-редактор в браузере с WebGL; автономная версия для Linux, Windows и macOS (отдельные сборки для Intel и Apple M1/M2), работает без интернета. Системные требования на странице загрузок не указаны.

## Экспорт

- Для сайтов: экспорт патча как архив с кодом только использованных операторов («a .zip file containing only the code of the operators you used»).
- Видео: оператор MediaRecorder (кодек по браузеру, битрейт, Max FPS и Force FPS, запись по сигналу, звук из аудиоузла). Результат без метки длительности.
- Кадры: оператор Download Texture (v2) сохраняет изображения и скриншоты в выбранном разрешении.

## Стоимость

Проверено 2026-10-14 по [FAQ о лицензии](https://cables.gl/docs/faq/licence_payment/licence/licence). «There is no need to buy a license when using cables.» Бесплатно; поддержку проекта собирают через Patreon (по главной странице).

## Лицензия и права

- Код или программа: MIT. Ядро: поле `license: MIT` в `package.json` репозитория `cables`. Редактор `cables_ui`: файл LICENCE (MIT, «2019-present undefined development»). Автономное приложение `cables_electron`: MIT. Документация: «Everything needed to run a cables patch is licensed under the MIT License».
- Результат: на главной странице: «Cables will always be free for everybody to use and anything you make with cables is yours». Экспорт содержит сведения о лицензиях подключённых библиотек.
- Ассеты в комплекте: библиотеки и операторы сообщества могут иметь иные условия; в экспортах перечислены лицензии библиотек. Не проверял.

## Активность и зрелость

<!-- gh-stats:cables-gl/cables -->
- Звёзды GitHub: 568
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.6.0 (2025-06-17)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория cables-gl/cables, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `young` (версии 0.x, открытый код с 2024 года по данным CDM). Релизы ядра: v0.6.0 (2025-06-17), v0.5.0 (2024-12-17). Автономное приложение: версии 0.12.0 (2026-10-14), 0.11.3 (2026-09-22). Последние коммиты в `cables` и `cables_ui` — 2026-10-14. Разрабатывает студия undev с сообществом (README).

## Когда брать и когда нет

- Брать: быстрые интерактивные WebGL-визуалы и фоны, прототипы для сайтов, живые выступления; бесплатно и без установки.
- Не брать: основной конвейер ролика с точной покадровой записью, формулы и графики. Для сравнения: [touchdesigner](touchdesigner.md) (запись без потери кадров, платный), [vvvv](vvvv.md) (Windows), [three-js](three-js.md) с [ccapture-js](ccapture-js.md) (код и точная запись).

## Источники

- [Главная страница cables.gl](https://cables.gl/) — «cables is now open source», «anything you make with cables is yours», автономная версия, экспорт в ZIP. Проверено 2026-10-14.
- [FAQ: What license do I need](https://cables.gl/docs/faq/licence_payment/licence/licence) — MIT, бесплатно. Проверено 2026-10-14.
- [Загрузки](https://cables.gl/downloads) — автономное приложение 0.12.0, MIT, Linux, Windows, macOS. Проверено 2026-10-14.
- [FAQ: Recording](https://cables.gl/docs/faq/features/recording/recording) — операторы Download Texture (v2) и Media Recorder. Проверено 2026-10-14.
- [Оператор MediaRecorder](https://cables.gl/op/Ops.Gl.MediaRecorder) — кодек по браузеру, Max FPS, Force FPS, видео без длительности. Проверено 2026-10-14.
- [Экспорт через командную строку](https://cables.gl/docs/4_export_embed/dev_embed/export_cli/export_cli) — Node/npm и ключ API. Проверено 2026-10-14.
- [Репозиторий cables](https://github.com/cables-gl/cables), [README](https://raw.githubusercontent.com/cables-gl/cables/develop/README.md), [package.json](https://raw.githubusercontent.com/cables-gl/cables/develop/package.json) — ядро и операторы, MIT, undev. Проверено 2026-10-14.
- [LICENCE в cables_ui](https://raw.githubusercontent.com/cables-gl/cables_ui/develop/LICENCE) — MIT. Проверено 2026-10-14.
- [Релизы cables](https://github.com/cables-gl/cables/releases.atom) и [cables_electron](https://github.com/cables-gl/cables_electron/releases.atom) — версии и даты. Проверено 2026-10-14.
- [CDM: cables.gl open offline](https://cdm.link/2024/08/cables-gl-open-offline/) — открытый код и MIT, август 2024 (вторичный источник, по результатам поиска). Проверено 2026-10-14.
- Ролики: [xnObNRv8n9I](https://www.youtube.com/watch?v=xnObNRv8n9I), [VsS4gaJ7pMw](https://www.youtube.com/watch?v=VsS4gaJ7pMw), [__QxceKIT1c](https://www.youtube.com/watch?v=__QxceKIT1c), [32xHw6BWIRI](https://www.youtube.com/watch?v=32xHw6BWIRI) — живые по oEmbed. Проверено 2026-10-14.

## Неизвестно

- Точная дата открытия кода: первоисточник (запись в блоге cables.gl) не найден; август 2024 — по статье CDM.
- Есть ли покадровый (офлайн) экспорт видео: в проверенной документации нет, может быть в операторах сообщества.
- Формат файла `.cables`: JSON или иной; страница экспорта автономного приложения не уточняет.
- Системные требования автономного приложения не указаны на странице загрузок.
- Полный список возможностей `cables-cli` не изучал (страница отсылает к репозиторию `cables-cli`).
- Условия на ассеты, включённые в операторы и примеры, не проверял.
