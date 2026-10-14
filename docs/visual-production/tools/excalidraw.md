---
id: excalidraw
name: Excalidraw (и excalidraw-animate)
class: [whiteboard]
kind: app
site: https://excalidraw.com/
github: excalidraw/excalidraw
scenes: [diagram, drawing]
quality: 3
human_difficulty: 1
agent_difficulty: 3
automation: 3
reproducibility: 4
cost: 0
maturity: stable
platforms: [web]
export: [svg, png, webm]
code_license: MIT
price: бесплатно; Excalidraw+ US$6 за пользователя в месяц
checked: 2026-10-14
---

# Excalidraw (и excalidraw-animate)

Виртуальная доска с «рукописным» стилем линий. Рисуется в браузере, файл `.excalidraw` — текстовый JSON. Анимацию рисования добавляет отдельная утилита excalidraw-animate (автор dai-shi): она проигрывает элементы по порядку и экспортирует SVG или WebM.

## Ссылки

- Официальный сайт: <https://excalidraw.com/>
- GitHub: <https://github.com/excalidraw/excalidraw>
- Документация: <https://docs.excalidraw.com/>
- excalidraw-animate: репозиторий <https://github.com/dai-shi/excalidraw-animate>, сервис <https://dai-shi.github.io/excalidraw-animate>, пакет <https://www.npmjs.com/package/excalidraw-animate>
- Excalidraw+ (платная версия): <https://plus.excalidraw.com/>
- Примеры, проверенные 2026-10-14 (ссылки открываются через oEmbed; содержание описано по названию и описанию ролика, ролики целиком не смотрелись):
  - [How I Animate Excalidraw Drawings for DaVinci Resolve](https://www.youtube.com/watch?v=9Myynuhy86g) — канал Patrick Scheibe. Рабочий процесс: Excalidraw, excalidraw-animate, OBS и Fusion в Resolve, стрелки и подписи появляются в такт озвучке.
  - [Excalimate Demo](https://www.youtube.com/watch?v=z-OV8lezk2Y) — канал David Szakacs. Сторонний проект Excalimate: анимации на ключевых кадрах поверх Excalidraw (появление, сдвиг, масштаб, поворот, draw-on), экспорт в MP4, WebM, GIF и анимированный SVG, есть MCP-сервер для агентов. Лицензию и состояние проекта не проверял.

## Что реально получается

Опора: README обоих репозиториев, документация, ролики выше.

- Схемы, блок-диаграммы, подписанные рисунки в едином «карандашном» стиле. Стиль даёт библиотека Rough.js (roughjs 4.6.4 в зависимостях пакета).
- Анимация рисования: excalidraw-animate превращает рисунок в анимацию. Элементы появляются в порядке создания или по заданному порядку (поле Order) и длительности (Duration). По умолчанию 500 мс на элемент, группа 5 секунд на всех участников. Линии, стрелки, свободное рисование, текст, изображения, библиотеки элементов поддерживаются (списки в README и заметках проекта).
- Экспорт анимации: SVG и WebM. Сам автор пишет: экспорт WebM «не идеален», при сбоях используйте запись экрана.
- Непрерывность: объекты появляются на одном холсте, ничего не превращается друг в друга. Камеры и плавного наезда нет. В ролике Patrick Scheibe камеру и сведение с речью делают в Fusion.
- Синхронизация с голосом: порядок и длительность элементов задаются вручную. Привязки к тексту нет. Агент может выставить Order и Duration по меткам времени (идея, не проверено).
- Типографика: рукописный стиль текста. Формулы LaTeX в проверенных источниках не упомянуты.

## Слабые стороны

- Единственный стиль: рукописные схемы. Для эффектной графики не подходит.
- Анимация внешняя и с ограничениями: WebM экспортируется нестабильно, SVG потом нужно превратить в видео (запись экрана, [OBS Studio](obs-studio.md), конвертер).
- Файлы, загруженные в режиме Animate, в режиме Edit недоступны (README).
- Нет камеры и переходов между сценами.
- Утилита excalidraw-animate живёт у одного автора. Релизов мало: 0.7.0 (2025-04-10), 0.7.1 (2025-04-14), 0.7.2 (2026-04-24).

## Сложность

- Для человека (1 из 5): рисуется за минуты. Оценка автора карточки.
- Для агента (3 из 5): файл `.excalidraw` — текстовый JSON (type, version, source, elements, appState, files), агент может генерировать его кодом. Анимацию получает через веб-интерфейс excalidraw-animate (командной строки в README нет). Часть работы руками.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): JSON-схема сцен, npm-пакет `@excalidraw/excalidraw` (React-компонент) и пакет `excalidraw-animate`. CLI для анимации в README нет.
- Воспроизводимость (4 из 5): текстовый JSON под git. Совпадают ли «дрожащие» линии при повторном рендере, не проверено (см. «Неизвестно»).

## Платформа и оборудование

- Браузер. Нужен только современный браузер. Локальная установка через npm (React). В репозитории есть Dockerfile и docker-compose.yml.

## Экспорт

- Excalidraw: PNG, SVG, буфер обмена, файл `.excalidraw`. Excalidraw+: ещё PDF и PPTX.
- excalidraw-animate: SVG-анимация и WebM. Другие форматы видео: через запись экрана.
- Прозрачный фон, 4K, частота кадров: не проверено.

## Стоимость

Проверено 2026-10-14 по [странице тарифов Excalidraw+](https://plus.excalidraw.com/pricing) и README.

- Excalidraw и excalidraw-animate: бесплатно.
- Excalidraw+: US$6 в месяц за пользователя, 14 дней пробы, скидка при оплате за год 14%. Добавляет облако, презентации, комментарии, PDF/PPTX, доступ к MCP и REST API (бета).
- Оценка стоимости 0: достаточно бесплатной версии.

## Лицензия и права

- Код или программа: Excalidraw — MIT (Excalidraw). excalidraw-animate — MIT (Daishi Kato).
- Результат: MIT относится к коду. Явного заявления на права на экспортированные рисунки в проверенных страницах нет, на практике кадры ваши. Условия сервиса excalidraw.com и Excalidraw+ не читал.
- Ассеты в комплекте: шрифты и библиотеки элементов сообщества. Их лицензии не проверены.

## Активность и зрелость

<!-- gh-stats:excalidraw/excalidraw -->
- Звёзды GitHub: 133 878
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v0.18.1 (2026-04-21)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория excalidraw/excalidraw, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: stable. Релизы Excalidraw по ленте: v0.17.6 (2024-04-17), v0.18.0 (2025-03-11), v0.18.1 (2026-04-21). Последний коммит 2026-10-14. excalidraw-animate: v0.7.2 (2026-04-24), коммиты до 2026-05-29 (ленты GitHub). Развивает сообщество и компания Excalidraw; утилиту анимации ведёт Daishi Kato.

## Когда брать и когда нет

- Брать: схемы и объяснение «на доске», где важна скорость и текстовый файл под git.
- Брать: чтобы нарисованный рисунок появлялся по шагам в такт речи, а камеру и сведение сделать в [DaVinci Resolve](davinci-resolve.md).
- Не брать: когда нужна выразительная графика, камера, морфинг. Тогда [After Effects](after-effects.md), [Cavalry](cavalry.md).
- Не брать: если нужно точное рисование пером «вживую». Тогда запись экрана ([OBS Studio](obs-studio.md)) или [Lightboard](lightboard.md).

## Источники

- [Репозиторий Excalidraw](https://github.com/excalidraw/excalidraw) — MIT, пакет `@excalidraw/excalidraw`, экспорт PNG и SVG, Dockerfile. Проверено 2026-10-14.
- [Ленты релизов и коммитов Excalidraw](https://github.com/excalidraw/excalidraw/releases.atom) — v0.18.1 2026-04-21, коммиты до 2026-10-14. Проверено 2026-10-14.
- [package.json Excalidraw](https://raw.githubusercontent.com/excalidraw/excalidraw/master/packages/excalidraw/package.json) — зависимость roughjs 4.6.4, MIT. Проверено 2026-10-14.
- [Схема JSON](https://docs.excalidraw.com/docs/codebase/json-schema) — поля файла `.excalidraw`. Проверено 2026-10-14.
- [Excalidraw+: тарифы](https://plus.excalidraw.com/pricing) — Free и Plus, US$6, возможности. Проверено 2026-10-14.
- [Репозиторий excalidraw-animate](https://github.com/dai-shi/excalidraw-animate) — описание, как пользоваться, Order и Duration, WebM «not perfect», MIT. Проверено 2026-10-14.
- [README excalidraw-animate](https://raw.githubusercontent.com/dai-shi/excalidraw-animate/main/README.md) — подробности использования и известные проблемы. Проверено 2026-10-14.
- [Ленты релизов и коммитов excalidraw-animate](https://github.com/dai-shi/excalidraw-animate/tags.atom) — v0.7.2 2026-04-24, коммиты до 2026-05-29. Проверено 2026-10-14.
- [Пакет excalidraw-animate на npm](https://registry.npmjs.org/excalidraw-animate) — версии и даты 0.7.0, 0.7.1, 0.7.2. Проверено 2026-10-14.

## Неизвестно

- Одинаковость рукописных линий при повторном рендере: поле `seed` в документации схемы не описано, проверки не было.
- Условия сервиса excalidraw.com и права на экспортированные рисунки: явного текста не читал.
- Командная строка или программный интерфейс excalidraw-animate: в README не описаны, хотя есть npm-пакет.
- Состояние и лицензия проекта Excalimate: не проверены.
- Поддержка формул и прозрачного фона при экспорте.
- Содержание двух примеров описано по названию и описанию, ролики не просматривались целиком.
