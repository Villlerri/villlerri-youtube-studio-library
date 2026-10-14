---
id: final-cut-pro
name: Final Cut Pro
class: [edit-composite]
kind: app
site: https://www.apple.com/final-cut-pro/
github: none
scenes: [real-footage, typography, screen]
quality: 4
human_difficulty: 2
agent_difficulty: 4
automation: 2
reproducibility: 3
cost: 2
maturity: standard
platforms: [macos, ios]
export: [mp4, mov, prores]
code_license: proprietary
price: Mac $299.99 разово; подписка Apple Creator Studio $12.99/мес (в неё входит версия для iPad)
checked: 2026-10-14
---

# Final Cut Pro

Монтажная программа Apple для Mac и iPad. Версия для Mac 12.4 от 29 сентября 2026. В поле `platforms` значение `ios` означает iPadOS.

## Ссылки

- Официальный сайт: <https://www.apple.com/final-cut-pro/>
- GitHub: открытого кода нет.
- Требования: <https://www.apple.com/final-cut-pro/specs/>
- Заметки о выпусках: <https://support.apple.com/en-us/102825>
- Формат обмена FCPXML: <https://developer.apple.com/documentation/professional-video-applications/fcpxml-reference>
- Примеры, проверенные 2026-10-14 (ссылка открывается через oEmbed; содержание по названию):
  - [Final Cut Pro 11 • Complete Guide To The Magnetic Mask](https://www.youtube.com/watch?v=X8DZgSRsvF4) — канал Dylan Bates • The Final Cut Bro. Выделение человека или предмета без хромакея, часть про трекинг.
  - [Final Cut Pro 11 - NEW FEATURES IN-DEPTH](https://www.youtube.com/watch?v=4a2dIouFr70) — канал Ripple Training. Обзор новинок 11-й версии. Сегодня текущая версия 12.4, ролик устарел по версии.

## Что реально получается

Опора: страница продукта, пресс-релиз Apple Creator Studio, заметки о выпусках.

- Магнитная маска (Magnetic Mask): отделяет человека и предметы от фона без зелёного экрана. Для ролика это способ оставить объект на месте, пока меняется фон.
- Трекер объектов (Object Tracker): привязывает графику к движущемуся предмету. FCPXML описывает такие данные (`object-tracker`).
- Поиск по расшифровке (Transcript Search) и поиск по картинке (Visual Search): находят место по фразе или описанию. Только Apple silicon и американский английский. Для русской озвучки не годится.
- Автосубтитры (Generate Captions, 12.3): только американский английский (по пересказу заметок о выпуске в поисковой выдаче, заметки целиком не читал).
- Smooth Slo-Mo, автокадрирование, Beat Detection (ритм музыки на таймлайне): перечислены на странице продукта.
- Переходы и титры из комплекта. Список в источниках не открыл.
- Непрерывная сцена, морфинг, рисование линий: встроенных инструментов нет. Графику делают в [Apple Motion](apple-motion.md), он продаётся отдельно за $49.99 и входит в Apple Creator Studio.
- Синхронизация с голосом: ручная. Beat Detection привязывает монтаж к музыке, не к голосу.

## Слабые стороны

- Только Apple. Нет Windows и Linux.
- Нет открытого API скриптинга. Автоматизация идёт через обмен файлами FCPXML и расширения (Workflow Extensions, введены в 10.4.4, 2018). Рендер без интерфейса не найден.
- Умные функции требуют Apple silicon и работают на американском английском.
- Для сложного композитинга нужен второй продукт.

## Сложность

- Для человека (2 из 5): базовый монтаж за дни. Это оценка автора карточки, не источник.
- Для агента (4 из 5): агент может генерировать FCPXML (медиа, клипы, переходы, маркеры) и импортировать в программу. Дальше нужны руки: открыть, проверить, нажать экспорт. Скрипт API нет.

## Автоматизация и воспроизводимость

- Автоматизация (2 из 5): FCPXML 1.14 (с 12.0). Apple: FCPXML описывает не все стороны проекта и не заменяет библиотеку Final Cut Pro. Рендера из командной строки не нашёл.
- Воспроизводимость (3 из 5): FCPXML текстовый и лежит под git, но настоящий проект хранится в двоичной библиотеке.

## Платформа и оборудование

- Mac: macOS 15.6 или новее (для полного набора функций macOS 26), 8 ГБ памяти (рекомендуется 16 ГБ), 7,2 ГБ диска. Видеокарта с Metal нужна на Intel-Mac. Часть функций требует Apple silicon.
- iPad: iPadOS 18.6 или новее, чип M1 и новее, iPad (A16), iPad mini (A17 Pro).
- Заметки к 12.4 упоминают эффекты Cinematic на macOS 27 (по поисковой выдаче заметок, текст страницы не просматривался).

## Экспорт

- H.264, HEVC, QuickTime, MXF (через Compressor), пресеты для YouTube, Instagram, TikTok, Vimeo (страница требований). MXF-кодеки включают ProRes.
- Альфа-канал и частоты кадров: не проверены.

## Стоимость

Проверено 2026-10-14 по [странице продукта](https://www.apple.com/final-cut-pro/) и [пресс-релизу Apple](https://www.apple.com/newsroom/2026/01/introducing-apple-creator-studio-an-inspiring-collection-of-creative-apps/).

- Final Cut Pro для Mac: $299.99 разово (Mac App Store).
- Apple Creator Studio: $12.99 в месяц или $129 в год. Входят Final Cut Pro для Mac и iPad, Logic Pro, Pixelmator Pro, Motion, Compressor, MainStage. Месяц пробного периода для новых подписчиков.
- Студенты и преподаватели: $2.99 в месяц или $29.99 в год.
- Отдельная цена версии для iPad не указана, она входит в Creator Studio.
- Motion $49.99, Compressor $49.99 при разовой покупке.

## Лицензия и права

- Код или программа: проприетарная (Apple). Лицензионное соглашение (PDF) не удалось прочитать.
- Результат: условия о правах на ролики и монетизации не проверены, см. «Неизвестно».
- Ассеты в комплекте: титры, эффекты, звуки из комплекта. Условия не проверены.

## Активность и зрелость

Зрелость: standard. Релизы 2026: 12.0 (28 января), 12.2 (9 апреля), 12.3 (30 июня), 12.4 (29 сентября). Развивает Apple.

## Когда брать и когда нет

- Брать: студия работает на Mac и хочет быстрый монтаж без подписки Adobe.
- Брать вместе с Motion: для анимированных заголовков и графики внутри FCP.
- Не брать: Linux или Windows, агент без Mac, рендер из кода.

## Источники

- [Страница Final Cut Pro](https://www.apple.com/final-cut-pro/) — цены, Creator Studio, функции, требования. Проверено 2026-10-14.
- [Требования](https://www.apple.com/final-cut-pro/specs/) — macOS, память, форматы экспорта. Проверено 2026-10-14.
- [Пресс-релиз Apple Creator Studio](https://www.apple.com/newsroom/2026/01/introducing-apple-creator-studio-an-inspiring-collection-of-creative-apps/) — цены, разовые покупки, дата 28 января. Проверено 2026-10-14.
- [Final Cut Pro release notes](https://support.apple.com/en-us/102825) — версия 12.4 от 29 сентября 2026, FCPXML 1.14, Workflow Extensions. Проверено 2026-10-14.
- [FCPXML Reference](https://developer.apple.com/documentation/professional-video-applications/fcpxml-reference.md) — что описывает FCPXML и чего нет. Проверено 2026-10-14.

## Неизвестно

- Права на результат: лицензионное соглашение Apple (PDF) не читается стандартными средствами, страница условий не найдена.
- Рендер без интерфейса и командная строка.
- Текст заметок 12.3 и 12.4 прочитан частично (страница длинная), требования к macOS 27 взяты из поисковой выдачи.
- Содержание обоих роликов описано по названию, целиком не просматривалось.
