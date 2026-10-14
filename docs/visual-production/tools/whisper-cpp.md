---
id: whisper-cpp
name: Whisper и whisper.cpp
class: [sync]
kind: cli
site: https://github.com/ggml-org/whisper.cpp
github: ggml-org/whisper.cpp
scenes: [typography, screen, diagram]
quality: 3
human_difficulty: 2
agent_difficulty: 2
automation: 5
reproducibility: 3
cost: 0
maturity: stable
platforms: [linux, macos, windows, ios, android, web]
export: [txt, srt, vtt, json, csv, lrc]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Whisper и whisper.cpp

Whisper — модель распознавания речи OpenAI, whisper.cpp — её лёгкая реализация на C и C++ без зависимостей. Работает офлайн на процессоре и на видеокартах разных производителей. Метки слов доступны, но в README названы экспериментальными.

## Ссылки

- Официальный сайт: https://github.com/ggml-org/whisper.cpp (отдельного сайта нет).
- GitHub: https://github.com/ggml-org/whisper.cpp
- Исходная модель Whisper: https://github.com/openai/whisper
- Документация: README и [описание команды whisper-cli](https://github.com/ggml-org/whisper.cpp/tree/master/examples/cli).
- Примеры, проверенные 2026-10-14 (страницы открывались, звук не слушал):
  - [README whisper-cli: пословные метки](https://github.com/ggml-org/whisper.cpp/tree/master/examples/cli) — вывод для отрывка jfk.wav с флагом `-ml 1`: каждое слово в отдельной строке с интервалом, например «ask» 00:00:03.300–00:00:04.140.
  - [WASM-демо в браузере](https://ggml.ai/whisper.cpp/) — распознавание целиком в браузере: загрузить модель ggml и файл, нажать «Transcribe».
  - [Remotion: транскрибирование](https://www.remotion.dev/docs/captions/transcribing) — пакет `@remotion/install-whisper-cpp` запускает whisper.cpp на своём сервере (бесплатно и офлайн) и отдаёт субтитры для сцены.

## Что реально получается

- Распознавание с метками. Команда `whisper-cli` пишет текст с интервалами. Флаг `-ml 1` даёт каждому слову свою строку, `-sow` режет по словам, `-dtw` считает метки на уровне токенов. Для разбора машиной есть `-oj` и `-ojf` (расширенный JSON).
- Форматы: TXT, SRT, VTT, LRC, CSV, JSON. Сценарий «подсвечивать слово при звучании» поддерживает `-owts` (скрипт для караоке-видео).
- Русский. Нужна многоязычная модель (не `.en`) и флаг `-l ru`, по умолчанию язык английский. Whisper знает русский (токенизатор). Точность на русском не проверена.
- Модели: tiny, base, small, medium, large-v1, v2, v3 и large-v3-turbo, есть квантизация. Память по README: tiny ~273 МБ, base ~388 МБ, small ~852 МБ, medium ~2,1 ГБ, large ~3,9 ГБ.
- Роль в конвейере студии. Это распознавание, а не сверка со сценарием. Для живой записи диктора и для готового аудио без текста подходит. Для выравнивания известного сценария смотри [Montreal Forced Aligner](montreal-forced-aligner.md) и Forced Alignment в [ElevenLabs](elevenlabs.md). Озвучка идёт из [ElevenLabs](elevenlabs.md).
- Подключается к Remotion через `@remotion/install-whisper-cpp` (см. [Remotion](remotion.md)).
- Непрерывность сцены, морфинг и камера — не его задача.

## Слабые стороны

- Пословные метки помечены «experimental». Они грубее, чем у специальных выравнивателей ([WhisperX](whisperx.md)).
- Понимает только 16-битные WAV: остальное предварительно конвертируют ffmpeg (`-ar 16000 -ac 1`).
- Свой сценарий не принимает. Начальная подсказка `--prompt` подсказывает слова, но не заставляет следовать тексту.
- Могут быть пропуски, «галлюцинации» и повторы на паузах и музыке. Параметры порогов и температуры меняют результат.
- Качество русского распознавания зависит от размера модели. Маленькие модели путают термины и цифры.
- Сборка из исходников (`cmake`) и модель скачивается отдельно.

## Сложность

- Для человека (2 из 5): собрать программу, скачать модель, конвертировать звук и запустить. Работа в один вечер.
- Для агента (2 из 5): конвертация ffmpeg, запуск командой, JSON и SRT на выходе. Агент сам разбирает метки. Руки не нужны, но слух нужен для проверки слов и пауз.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): командная строка, форматы для машин, Си-API (`whisper.h`), привязки к Java, WASM, Docker.
- Воспроизводимость (3 из 5): код и модель закрепляются, результат при нулевой температуре почти повторяется. При откате температуры (по умолчанию включён, отключается `-nf`) выход может меняться. Метки сохраняют в проекте.

## Платформа и оборудование

macOS (Intel и Apple, оптимизация Metal и Core ML), Linux и FreeBSD, Windows (MSVC и MinGW), iOS, Android, браузер (WASM), Raspberry Pi, Docker. GPU: NVIDIA, AMD (ROCm), Vulkan, OpenVINO, NPU Ryzen AI, Ascend. Работает и только на процессоре. Видеокарта не обязательна, но ускоряет (`-ng` отключает GPU).

## Экспорт

TXT, SRT, VTT, LRC, CSV, JSON (простой и расширенный), скрипт для караоке-видео. Метки слов только при `-ml 1` или `-dtw`.

## Стоимость

Проверено 2026-10-14 по README. Бесплатно. Модели скачиваются бесплатно.

## Лицензия и права

- Код или программа: MIT (LICENSE: «Copyright (c) 2023-2026 The ggml authors»). Исходная модель OpenAI Whisper — MIT (LICENSE, 2022).
- Результат: тексты и метки принадлежат автору. Лицензии MIT ограничений на коммерческое использование не накладывают.
- Ассеты в комплекте: примеры аудио (jfk.wav и другие из Википедии). Условия их использования отдельно не проверял.

Это сведения из лицензий, не юридическая консультация.

## Активность и зрелость

<!-- gh-stats:ggml-org/whisper.cpp -->
- Звёзды GitHub: 54 386
- Последний коммит в основной ветке: 2026-10-12
- Последний релиз или тег: v1.9.5 (2026-10-07)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория ggml-org/whisper.cpp, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Релизы: v1.9.4 (2026-09-11), v1.9.5 (2026-10-06). Последние коммиты в основной ветке — 11–12 октября 2026. Развивает организация ggml-org и сообщество участников. У оригинального Whisper последний релиз на PyPI `openai-whisper` — 20250625 (2025-06-26).

## Когда брать и когда нет

- Брать: офлайн-транскрибация записанного голоса, субтитры, быстрая черновая разметка слов без видеокарты. Хорош в связке с Remotion.
- Не брать: когда нужны точные границы слов по готовому сценарию (тогда [Montreal Forced Aligner](montreal-forced-aligner.md) или [WhisperX](whisperx.md)). Когда метки слов решают результат ролика, а запас по качеству мал.

## Источники

- [README whisper.cpp](https://github.com/ggml-org/whisper.cpp) — возможности, платформы, память моделей, формат WAV, поддержка GPU. Проверено 2026-10-14.
- [whisper-cli README](https://github.com/ggml-org/whisper.cpp/tree/master/examples/cli) — флаги `-ml`, `-sow`, `-dtw`, `-oj`, `-ojf`, `-owts`, `-l`, раздел о словесных метках («experimental»). Проверено 2026-10-14.
- [LICENSE whisper.cpp](https://github.com/ggml-org/whisper.cpp/blob/master/LICENSE) — MIT, 2023–2026. Проверено 2026-10-14.
- [Релизы whisper.cpp](https://github.com/ggml-org/whisper.cpp/releases) — v1.9.5 от 2026-10-06, v1.9.4 от 2026-09-11. Проверено 2026-10-14.
- [Страница коммитов](https://github.com/ggml-org/whisper.cpp/commits/master) — даты последних коммитов. Проверено 2026-10-14.
- [README Whisper](https://github.com/openai/whisper) — размеры моделей, VRAM, модель turbo. Проверено 2026-10-14.
- [LICENSE Whisper](https://github.com/openai/whisper/blob/main/LICENSE) — MIT. Проверено 2026-10-14.
- [Токенизатор Whisper](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py) — русский `ru` среди языков. Проверено 2026-10-14.
- [PyPI: openai-whisper](https://pypi.org/project/openai-whisper/) — последний релиз 20250625. Проверено 2026-10-14.
- [Remotion: транскрибирование](https://www.remotion.dev/docs/captions/transcribing) — `@remotion/install-whisper-cpp`, бесплатно и офлайн. Проверено 2026-10-14.

## Неизвестно

- Точность распознавания и меток слов на русском по моделям разных размеров: запуск не выполнялся, сравнения в README нет.
- Насколько метки `-ml 1` расходятся с реальными границами слов на русской речи диктора.
- Совместимость модели large-v3-turbo со всеми режимами меток (`-dtw`): в README не описано.
- Лицензия и условия использования примеров аудио в репозитории.
