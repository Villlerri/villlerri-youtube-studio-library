# Whiteboard и рисование вживую

## Что сюда входит

Способы показать, как объяснение рисуется на глазах у зрителя. Есть четыре пути. Конструкторы «рука рисует картинку» (VideoScribe, Doodly). Программное вычерчивание своих линий (Vivus, Rough.js, excalidraw-animate, Excalimate, tldraw, а также Create и Write в Manim). Запись настоящего рисования пером (OBS Studio, Krita, Clip Studio Paint, Procreate Dreams, Grease Pencil). Физический метод: лектор пишет на стеклянной доске лицом к камере (Lightboard). Класс решает задачу «объяснение вживую», но разные пути дают разное качество.

## Когда этот класс нужен

- Схемы, блок-диаграммы и процессы, которые собираются шаг за шагом вместе с речью (`diagram`).
- Рисование линий вживую: контур вырастает, пока идёт объяснение (`drawing`).
- Вывод формул рукой или «как на доске» (`formula`).
- Лектор в кадре, который пишет и показывает на доске (`drawing`, `real-footage`).
- Короткие рисованные пояснения внутри ролика: стрелки, обводки, подписи от руки.
- Быстрые наброски идей до того, как делается чистая графика.

## Основные решения

- [VideoScribe](../tools/videoscribe.md) — конструктор «рука рисует клипарт»; от US$150 в год, ролики до 5, 10 или 20 минут по тарифам; для научно-популярного канала выглядит дёшево.
- [Doodly](../tools/doodly.md) — то же в настольном приложении; US$49 в месяц; библиотека персонажей и реквизита, путь рисования задаётся автоматически.
- [Excalidraw (и excalidraw-animate)](../tools/excalidraw.md) — рукописные схемы в текстовом JSON, анимация появления элементов в SVG или WebM; MIT.
- [Excalimate](../tools/excalimate.md) — независимый анимационный редактор поверх Excalidraw: ключи, камера, экспорт в MP4, WebM, GIF, SVG и Lottie, MCP-сервер для агента; MIT; молодой проект с оговоркой автора про код, написанный ИИ.
- [tldraw](../tools/tldraw.md) — SDK бесконечного холста с анимацией фигур и камеры; лицензия не свободная, в боевой среде нужен ключ.
- [Vivus](../tools/vivus.md) — вычерчивание SVG-контуров; `setFrameProgress` даёт покадровый контроль; развитие остановлено с 2021 года.
- [Rough.js](../tools/rough-js.md) — «карандашный» стиль линий на Canvas и SVG; сам не анимирует; релизов нет с 2023 года.
- [OBS Studio](../tools/obs-studio.md) — запись окна рисования, камеры и голоса; сцены, WebSocket, ключи запуска; не рисует сам.
- [Lightboard](../tools/lightboard.md) — стеклянная доска с подсветкой, лектор лицом к камере; открытый проект Northwestern, около US$8 тыс. на студию.
- [Blender Grease Pencil](../tools/blender-grease-pencil.md) — штрихи в 3D с модификатором Build («рисуется на глазах») и камерой; бесплатно.
- [Krita](../tools/krita.md) — растровая рисовалка с покадровой анимацией и Recorder, который записывает ускоренный процесс рисования.
- [Procreate Dreams](../tools/procreate-dreams.md) — рисованная покадровая анимация на iPad; US$12.99 разово.
- [Clip Studio Paint](../tools/clip-studio-paint.md) — рисовалка с покадровой анимацией и камерой по кривой; чтобы анимация длиннее 3 секунд, нужна редакция EX ($76.99 в год или $277 разово); без командной строки.
- [Manim CE](../tools/manim-ce.md) — `Create`, `Write` и `DrawBorderThenFill`: линия вырастает вдоль контура, текст пишется вживую; код под git.
- [Motion Canvas](../tools/motion-canvas.md) — у линии свойства `start` и `end` (доля длины), по ним она вырастает; релизов нет с февраля 2025 года.

## Сравнение

Оценки взяты из карточек, шкалы описаны в [методике](../method.md).

- Потолок качества. Выше остальных [Manim CE](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md) и [Blender Grease Pencil](../tools/blender-grease-pencil.md) (по 4): чистое вычерчивание своих линий и камера. Следом [Excalidraw](../tools/excalidraw.md), [Excalimate](../tools/excalimate.md), [tldraw](../tools/tldraw.md), [Vivus](../tools/vivus.md), [Rough.js](../tools/rough-js.md), [OBS Studio](../tools/obs-studio.md), [Lightboard](../tools/lightboard.md), [Krita](../tools/krita.md), [Procreate Dreams](../tools/procreate-dreams.md) (по 3), а [Clip Studio Paint](../tools/clip-studio-paint.md) выше них (4) по линии и кистям: аккуратная учебная графика или живое рисование, но без выразительной режиссуры. Ниже всех [VideoScribe](../tools/videoscribe.md) и [Doodly](../tools/doodly.md) (по 2): общий клипарт и автоматический путь рисования.
- Что выглядит дёшево. В [VideoScribe](../tools/videoscribe.md) и [Doodly](../tools/doodly.md) рука «закрашивает» готовую картинку из общей библиотеки по автоматическому пути (у Doodly для каждой картинки заранее задан путь рисования, FAQ). Те же значки у тысяч роликов, зритель узнаёт жанр рекламы. Объекты не превращаются друг в друга, камера прыгает от объекта к объекту, сцена не развивается. Это оценка автора. Лечится своими иллюстрациями в одном стиле и вычерчиванием собственных контуров ([Vivus](../tools/vivus.md), [Manim CE](../tools/manim-ce.md), [Grease Pencil](../tools/blender-grease-pencil.md)) или настоящим пером ([OBS Studio](../tools/obs-studio.md), [Lightboard](../tools/lightboard.md)).
- Трудность для человека. Легче всех [VideoScribe](../tools/videoscribe.md), [Doodly](../tools/doodly.md), [Excalidraw](../tools/excalidraw.md) (по 1): ролик или схема за час. [OBS Studio](../tools/obs-studio.md), [Krita](../tools/krita.md), [Procreate Dreams](../tools/procreate-dreams.md), [Vivus](../tools/vivus.md), [Rough.js](../tools/rough-js.md), [Excalimate](../tools/excalimate.md) (по 2): настройка сцены, немного кода или шаблоны и ключи в браузере. [Clip Studio Paint](../tools/clip-studio-paint.md) (3): умение рисовать и покадровая работа. Тяжелее [tldraw](../tools/tldraw.md) (React и TypeScript), [Lightboard](../tools/lightboard.md) (стройка студии и работа лектора), [Manim CE](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md), [Grease Pencil](../tools/blender-grease-pencil.md) (по 3).
- Трудность для агента. Проще всех [Manim CE](../tools/manim-ce.md) (1): код и командный рендер. [Vivus](../tools/vivus.md) и [Rough.js](../tools/rough-js.md) (по 2): агент пишет HTML и SVG, кадры снимает браузером. [Excalidraw](../tools/excalidraw.md), [Excalimate](../tools/excalimate.md), [tldraw](../tools/tldraw.md), [OBS Studio](../tools/obs-studio.md), [Grease Pencil](../tools/blender-grease-pencil.md), [Motion Canvas](../tools/motion-canvas.md) (по 3): JSON, MCP, API редактора, WebSocket или Python, но часть шагов в интерфейсе (у Excalimate экспорт видео кнопкой в браузере). [Krita](../tools/krita.md) (4). Только руками: [VideoScribe](../tools/videoscribe.md), [Doodly](../tools/doodly.md), [Lightboard](../tools/lightboard.md), [Procreate Dreams](../tools/procreate-dreams.md), [Clip Studio Paint](../tools/clip-studio-paint.md) (по 5).
- Автоматизация. Максимум у [Manim CE](../tools/manim-ce.md) (5). [Vivus](../tools/vivus.md), [Rough.js](../tools/rough-js.md), [OBS Studio](../tools/obs-studio.md) (по 4): весь код, встроенный WebSocket и ключи запуска у OBS. [Excalidraw](../tools/excalidraw.md) (JSON, npm-пакет, но нет командной строки для анимации), [Excalimate](../tools/excalimate.md) (MCP-сервер, рендер в файл только из браузера), [tldraw](../tools/tldraw.md), [Grease Pencil](../tools/blender-grease-pencil.md), [Krita](../tools/krita.md) (по 3). [Motion Canvas](../tools/motion-canvas.md) (2): командного рендера нет. Нет вовсе: [VideoScribe](../tools/videoscribe.md), [Doodly](../tools/doodly.md), [Lightboard](../tools/lightboard.md), [Procreate Dreams](../tools/procreate-dreams.md) (по 1); [Clip Studio Paint](../tools/clip-studio-paint.md) (2): записанные цепочки Auto Actions, API нет.
- Стоимость. Бесплатны: [Excalidraw](../tools/excalidraw.md), [Excalimate](../tools/excalimate.md), [Vivus](../tools/vivus.md), [Rough.js](../tools/rough-js.md), [OBS Studio](../tools/obs-studio.md), [Grease Pencil](../tools/blender-grease-pencil.md), [Krita](../tools/krita.md), [Manim CE](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md). [tldraw](../tools/tldraw.md): разработка бесплатно, боевая среда по лицензии (hobby по заявке с водяным знаком, проба 100 дней, коммерческая по запросу). [Procreate Dreams](../tools/procreate-dreams.md): US$12.99 разово. [Clip Studio Paint](../tools/clip-studio-paint.md): PRO $26.99 и EX $76.99 в год, бессрочно $63 и $277 (без скидки). [VideoScribe](../tools/videoscribe.md): от US$150 в год, для длинных роликов без водяного знака US$255–320. [Doodly](../tools/doodly.md): US$49 в месяц или US$490 в год. [Lightboard](../tools/lightboard.md): около US$8 тыс. на студию.
- Права. У [VideoScribe](../tools/videoscribe.md) после окончания подписки нельзя продавать проекты и получать плату за их использование, а контент Sparkol разрешено использовать только внутри программы; ответа про монетизацию YouTube нет. У [Doodly](../tools/doodly.md) FAQ говорит, что результат принадлежит пользователю, а картинки и звуки из поставки лицензируются по EULA, которое не прочитано. У [tldraw](../tools/tldraw.md) водяной знак обязателен при hobby-лицензии.
- Плавность переходов и непрерывность сцены. Лучше всего [Manim CE](../tools/manim-ce.md) и [Motion Canvas](../tools/motion-canvas.md): линия вырастает внутри одной сцены, объекты остаются в кадре и превращаются друг в друга. [Grease Pencil](../tools/blender-grease-pencil.md): штрихи в 3D, свободная камера, модификатор Build. [tldraw](../tools/tldraw.md): анимация фигур и камеры (`zoomToFit` с анимацией), но не штрихов. [Excalidraw](../tools/excalidraw.md): элементы появляются по порядку на одном холсте, камеры и переходов нет. [Excalimate](../tools/excalimate.md): те же схемы с камерой (панорама, масштаб, поворот) и переходом между сохранёнными состояниями схемы (Smart Transition): элементы остаются теми же, меняются положение и видимость; в Lottie прорисовка линий не сохраняется. [Clip Studio Paint](../tools/clip-studio-paint.md): ячейки и камера по кривой над рисунком, превращений нет, их рисуют руками. [Vivus](../tools/vivus.md): вычерчивание контуров, морфинга и камеры нет. [VideoScribe](../tools/videoscribe.md): единственный механизм непрерывности — камера по одному холсту. [OBS Studio](../tools/obs-studio.md) и [Lightboard](../tools/lightboard.md): непрерывность даёт сам человек, стёртое пропадает.

## Другие решения

- Powtoon — https://www.powtoon.com/ — онлайн-платформа для объясняющих роликов, включая whiteboard; бесплатный план с ограничениями (премиальные шаблоны, ИИ, Full HD снимаются платными планами).
- Mango Animate (Mango WM) — https://mangoanimate.com/ — «профессиональная программа для whiteboard-анимации»; цену, платформы и экспорт страница не называет.
- Explain Everything — https://explaineverything.com/ — онлайн-доска для обучения с записью объяснения; веб, iOS, Android, Chromebook; бесплатный старт, цены на странице не указаны.
- Concepts — https://concepts.app/en/ — бесконечный холст для набросков на iOS, Windows, Android, ChromeOS; бесплатный уровень и платные лицензии; экспорт PDF, SVG, PNG, PSD, DXF, видео на странице не упомянуто.
- Xournal++ — https://xournalpp.github.io/ — свободный конспектор с поддержкой планшетов (Wacom, Huion, XP-Pen), слоями и PDF; Windows, macOS, Linux; лицензия на странице не названа.
- Epic Pen — https://epicpen.com/ — рисование поверх любого окна на ПК; бесплатный Basic (ручка, ластик, маркер, фигуры, доска), платный Pro; удобно вместе с записью экрана.
- Saber — https://github.com/saber-notes/saber — свободное приложение для рукописных заметок (GPL-3.0); Android, iOS, Windows, Linux, macOS; коммиты в октябре 2026.
- Rnote — https://github.com/flxzt/rnote — свободное приложение для набросков и рукописных заметок (GPL-3.0-or-later); Linux, macOS, Windows; экспорт SVG и PDF.
- OpenBoard — https://openboard.ch/ — свободная интерактивная доска для школ (GPLv3); Windows, macOS, Linux; запись и экспорт на странице не упомянуты.
- Microsoft Whiteboard — https://support.microsoft.com/en-au/office/sign-up-for-a-new-whiteboard-account-4bb4c46f-0435-43fe-bf97-08dccd04442a — доска Microsoft; браузер, Teams, Windows, iOS, Android, Surface Hub; вход с бесплатной учётной записью Microsoft.

## Вывод для объясняющих видео

Конструкторы [VideoScribe](../tools/videoscribe.md) и [Doodly](../tools/doodly.md) для научно-популярного канала не берите: рука рисует клипарт, сцена не развивается, а у VideoScribe права ограничены условиями подписки. Линии и формулы, которые вырастают на глазах, делайте кодом: [Manim CE](../tools/manim-ce.md) даёт `Create` и `Write` в одной непрерывной сцене, и агент собирает её из командной строки. Для быстрых «досочных» схем с появлением элементов по шагам берите [Excalidraw](../tools/excalidraw.md) с excalidraw-animate (или молодой [Excalimate](../tools/excalimate.md), где есть камера и MCP для агента) и запись в [OBS Studio](../tools/obs-studio.md), а камеру и сведение с речью делайте в монтаже. Если нужен человек в кадре, который пишет на стекле, это [Lightboard](../tools/lightboard.md), но студия и лектор обойдутся около US$8 тыс. Рукописный стиль линий добавляет [Rough.js](../tools/rough-js.md), вычерчивание SVG даёт [Vivus](../tools/vivus.md), но обе библиотеки не развиваются.

## Источники

- [Powtoon](https://www.powtoon.com/) — онлайн-платформа объясняющих роликов, бесплатный план с ограничениями. Проверено 2026-10-14.
- [Mango Animate](https://mangoanimate.com/) — «Professional Whiteboard Animation Video Software», цены и платформы на странице нет. Проверено 2026-10-14.
- [Explain Everything](https://explaineverything.com/) — платформы, запись, бесплатный старт. Проверено 2026-10-14.
- [Concepts](https://concepts.app/en/) — платформы, форматы экспорта, бесплатный уровень. Проверено 2026-10-14.
- [Xournal++](https://xournalpp.github.io/) — планшеты, слои, платформы. [Лента коммитов](https://github.com/xournalpp/xournalpp/commits.atom) — последний коммит 2026-10-12. Проверено 2026-10-14.
- [Epic Pen](https://epicpen.com/) — рисование поверх приложений, Basic и Pro. Проверено 2026-10-14.
- [Saber на GitHub](https://github.com/saber-notes/saber) — GPL-3.0, платформы. [Лента коммитов](https://github.com/saber-notes/saber/commits.atom) — последний коммит 2026-10-02. Проверено 2026-10-14.
- [Rnote на GitHub](https://github.com/flxzt/rnote) — GPL-3.0-or-later, платформы, экспорт SVG и PDF. Проверено 2026-10-14.
- [OpenBoard](https://openboard.ch/) — GPLv3, платформы. Проверено 2026-10-14.
- [Microsoft Whiteboard: регистрация](https://support.microsoft.com/en-au/office/sign-up-for-a-new-whiteboard-account-4bb4c46f-0435-43fe-bf97-08dccd04442a) — платформы и вход с бесплатной учётной записью. Проверено 2026-10-14.
