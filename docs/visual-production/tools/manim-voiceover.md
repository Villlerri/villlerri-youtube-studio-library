---
id: manim-voiceover
name: manim-voiceover
class: [sync, 2d-code]
kind: plugin
site: https://voiceover.manim.community/
github: ManimCommunity/manim-voiceover
scenes: [formula, graph, diagram, drawing, field]
quality: 3
human_difficulty: 3
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: young
platforms: [linux, macos, windows]
export: [mp4, mov, webm, gif, png-sequence]
code_license: MIT
price: плагин бесплатно; голос оплачивается у выбранного сервиса
checked: 2026-10-14
---

# manim-voiceover

Плагин для [Manim](manim-ce.md): озвучка прямо в коде сцены. Длительность анимации берётся из длины голоса, а закладки в тексте запускают анимацию на нужном слове.

## Ссылки

- Официальный сайт и документация: https://voiceover.manim.community/
- GitHub: https://github.com/ManimCommunity/manim-voiceover
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики YouTube прошли oEmbed, смотрел только описание):
  - [Approximating tau with Archimedes' method](https://www.youtube.com/watch?v=xmHzyafJEec) — канал NutronStar45. Пример из галереи плагина: анимация привязана к словам через закладки.
  - [Квадратное уравнение на арабском](https://www.youtube.com/watch?v=Sflx0aoFrVg) — канал SciVerse. Пример из галереи плагина: озвучка не на английском.
  - [Галерея примеров](https://voiceover.manim.community/en/latest/examples.html) — демонстрационный ролик и два ролика выше.
  - [Пример закладок в репозитории](https://github.com/ManimCommunity/manim-voiceover/blob/main/examples/bookmark-example.py) — список из трёх пунктов, каждый пункт появляется на своём слове фразы.
  - [Быстрый старт](https://voiceover.manim.community/en/latest/quickstart.html) — блок `with self.voiceover(...)`, закладки, запись своего голоса.

## Что реально получается

- Блок озвучки. `with self.voiceover(text="...") as tracker:` оборачивает анимацию. Если голос длиннее анимации, Manim ждёт его конца. `tracker.duration` даёт длительность, например для `run_time`. Несколько блоков подряд склеивают фразы без ручной подгонки пауз.
- Закладки. В тексте стоит `<bookmark mark='A'/>` перед словом. В коде `self.wait_until_bookmark("A")` ждёт этого слова, а `tracker.time_until_bookmark("B", limit=1)` отдаёт время до следующего слова. Так линия растёт вместе с фразой «вот здесь».
- Откуда метки слов. Плагин не берёт их у синтезатора. Он расшифровывает готовое аудио через OpenAI Whisper (дополнение `transcribe`: openai-whisper и stable-ts) и по распознаванию находит слова закладок. Это работает и для записанного голоса.
- Движки. В README версии 0.4.0: Gemini Text to Speech, Azure Text to Speech, gTTS, pyttsx3. В документации и дополнениях `pyproject.toml` есть ещё ElevenLabs, OpenAI, Coqui и запись голоса с микрофона (`RecorderService`). Другие синтезаторы речи библиотека не рассматривает по правилу студии: озвучка только через [ElevenLabs](elevenlabs.md).
- ElevenLabs в плагине. `ElevenLabsService` вызывает функции `generate`, `save`, `voices` старой версии SDK (`elevenlabs>=0.2.27,<0.3`). Модель по умолчанию `eleven_monolingual_v1`, параметр `model` — строка, можно подставить многоязычную. Метки слов идут из Whisper (`transcription_model="base"` по умолчанию), а не из ElevenLabs. Текущий SDK на PyPI — 2.72.0, и работает ли закреплённая старая версия с сегодняшним API, не проверено.
- Русский. Язык задаёт модель синтезатора, Whisper русский знает (токенизатор, `ru`). Качество Whisper на русских числах и терминах не проверено.
- Субтитры. Тот же `text` по умолчанию идёт в субтитры сцены, можно задать свой.
- Непрерывность. Плагин не меняет Manim: объекты живут в одном `construct()`, сцена течёт без склеек, а блоки озвучки лишь задают темп. Камера и морфинг берутся из Manim.

## Слабые стороны

- Связка с ElevenLabs устарела: закреплён SDK 0.2.x, по умолчанию английская модель.
- Метки слов зависят от Whisper, а не от точных меток ElevenLabs (`with-timestamps`, Forced Alignment). Свой код придётся писать, если нужны эти метки: в плагине их нет.
- Проект сильно менялся: релиз 0.3.7 (2024-09-29), затем 0.4.0 только через 21 месяц (2026-06-14). В `pyproject.toml` статус «Alpha». API может меняться.
- Python 3.11 или новее, нужен SoX и Manim. Документация «latest» и README расходятся: в документации есть Coqui и OpenAI, в README нет.
- Только сцены Manim. В Motion Canvas и Remotion плагин не работает (см. [motion-canvas](motion-canvas.md), [remotion](remotion.md)).
- Нет таймлайна: ритм правят текстом и перерендером.
- Любая правка текста озвучки означает новую генерацию и расход кредитов (кэш лежит по тексту и настройкам).

## Сложность

- Для человека (3 из 5): нужны Python и понимание сцен Manim. Закладки осваиваются за вечер, ритм и вкус — недели.
- Для агента (2 из 5): сцена и озвучка целиком кодом, рендер одной командой Manim. Агент сам проверяет длительности и кадры. Слух нужен, чтобы оценить интонацию и попадание закладок.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): всё из Python и командной строки Manim, пакетный рендер, кэш озвучки по тексту.
- Воспроизводимость (4 из 5): проект — текст под git. Озвучку кэшируют, и тогда кадр повторяется. Новая генерация ИИ-голоса даёт другое аудио, а с ним и другие времена слов. Поэтому кэш озвучки хранят вместе с проектом.

## Платформа и оборудование

Linux, macOS, Windows. Python 3.11 и новее (`pyproject.toml`), SoX, Manim. Для записи с микрофона нужны PyAudio и pynput. Видеокарта для Manim не нужна. Нужна ли она для Whisper, не проверено: размер модели `base` по умолчанию лёгкий.

## Экспорт

Как у Manim: MP4, MOV, WebM, GIF, последовательность PNG. Озвучка вшита в видео. Отдельного файла с метками слов в документации не нашёл.

## Стоимость

Проверено 2026-10-14 по [документации сервисов](https://voiceover.manim.community/en/latest/services.html). Плагин бесплатный. Голос оплачивается у выбранного сервиса: для студии это ElevenLabs, цены в карточке [elevenlabs](elevenlabs.md). Whisper локальный и бесплатный.

## Лицензия и права

- Код или программа: MIT (README, `pyproject.toml`).
- Результат: ролики и кадры принадлежат автору, лицензия MIT не ограничивает монетизацию. Права на голос определяет сервис синтеза (для ElevenLabs — платный тариф для коммерческого права, см. [elevenlabs](elevenlabs.md)).
- Ассеты в комплекте: голосов и шаблонов нет, поставляются только примеры кода.

## Активность и зрелость

<!-- gh-stats:ManimCommunity/manim-voiceover -->
- Звёзды GitHub: 320
- Последний коммит в основной ветке: 2026-06-15
- Последний релиз или тег: v0.4.0 (2026-06-14)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория ManimCommunity/manim-voiceover, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `young`. До версии 1.0, в `pyproject.toml` классификатор «Development Status :: 3 - Alpha». По PyPI релизы: 0.3.6 (2024-02-25), 0.3.7 (2024-09-29), 0.4.0 (2026-06-14). Последний коммит в основной ветке — 2026-06-15 (по странице коммитов GitHub). В 0.4.0 переход на структуру `src`, служба Gemini, проверка кэша через pydantic. Развивает сообщество Manim Community.

## Когда брать и когда нет

- Брать: ролики на [Manim](manim-ce.md), где линия, формула или стрелка должны появиться ровно на слове. Агент делает всё кодом.
- Не брать: когда нужны точные метки ElevenLabs без повторного распознавания (используйте API ElevenLabs и свой код, см. [elevenlabs](elevenlabs.md)). Когда сцены делаются в Motion Canvas или Remotion. Когда нужен интерфейс с таймлайном.

## Источники

- [README репозитория](https://github.com/ManimCommunity/manim-voiceover) — назначение, MIT, список движков 0.4.0, Whisper для слов. Проверено 2026-10-14.
- [pyproject.toml](https://github.com/ManimCommunity/manim-voiceover/blob/main/pyproject.toml) — версия 0.4.0, Python 3.11 и новее, Alpha, дополнения, закреплённый elevenlabs<0.3. Проверено 2026-10-14.
- [Код ElevenLabsService](https://github.com/ManimCommunity/manim-voiceover/blob/main/src/manim_voiceover/services/elevenlabs.py) — старые вызовы SDK, модель по умолчанию, `transcription_model`. Проверено 2026-10-14.
- [Быстрый старт](https://voiceover.manim.community/en/latest/quickstart.html) — блок озвучки, закладки, субтитры. Проверено 2026-10-14.
- [Справочник API](https://voiceover.manim.community/en/latest/api.html) — `wait_until_bookmark`, `time_until_bookmark`, `transcription_model`. Проверено 2026-10-14.
- [Пример закладок](https://github.com/ManimCommunity/manim-voiceover/blob/main/examples/bookmark-example.py) — синтаксис `<bookmark mark='A'/>`. Проверено 2026-10-14.
- [Сравнение сервисов](https://voiceover.manim.community/en/latest/services.html) — список движков в документации. Проверено 2026-10-14.
- [PyPI: manim-voiceover](https://pypi.org/project/manim-voiceover/) — история релизов, версия 0.4.0. Проверено 2026-10-14.
- [Страница коммитов](https://github.com/ManimCommunity/manim-voiceover/commits/main) — последние коммиты 14–15 июня 2026. Проверено 2026-10-14.
- [PyPI: elevenlabs](https://pypi.org/project/elevenlabs/) — текущая версия SDK 2.72.0 против закреплённой 0.2.27. Проверено 2026-10-14.

## Неизвестно

- Работает ли `ElevenLabsService` с актуальным API ElevenLabs: код не запускался, а SDK закреплён на версии 2023 года.
- Точность закладок на русской озвучке (числа, термины): Whisper-разметку не проверял.
- Нужен ли GPU для Whisper-распознавания при длинных роликах: в документации не нашёл.
- Какой статус у Coqui в 0.4.0: в документации есть, в `pyproject.toml` дополнения нет.
- Кто из авторов роликов в галерее использует ElevenLabs: в галерее движок не назван.
