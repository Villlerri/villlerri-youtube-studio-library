---
id: montreal-forced-aligner
name: Montreal Forced Aligner
class: [sync]
kind: cli
site: https://montreal-forced-aligner.readthedocs.io/en/latest/
github: MontrealCorpusTools/Montreal-Forced-Aligner
scenes: [formula, diagram, drawing, character]
quality: 4
human_difficulty: 4
agent_difficulty: 2
automation: 5
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [textgrid, json, csv]
code_license: MIT
price: бесплатно
checked: 2026-10-14
---

# Montreal Forced Aligner

Принудительное выравнивание (forced alignment) на базе Kaldi: по звуку и готовому тексту находит границы слов и фонем. Не распознаёт речь, а сверяет её с вашим сценарием. Для русского есть готовые акустическая модель и словарь.

## Ссылки

- Официальный сайт и документация: https://montreal-forced-aligner.readthedocs.io/en/latest/
- GitHub: https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner
- Примеры, проверенные 2026-10-14 (страницы открывались, ролики YouTube прошли oEmbed, смотрел только описание):
  - [Пример выравнивания демонстрационного корпуса](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/alignment_example.html) — команды скачивания модели и словаря и запуск `mfa align` для английского, японского и мандаринского.
  - [Русская акустическая модель v3.1.0](https://mfa-models.readthedocs.io/en/latest/acoustic/Russian/Russian%20MFA%20acoustic%20model%20v3_1_0.html) — состав обучающих данных, лицензия, оговорки.
  - [Phonetic forced alignment with the Montreal Forced Aligner](https://www.youtube.com/watch?v=Zhj-ccMDj_w) — онлайн-семинар Элеоноры Ходрофф, 2021, около трёх часов. Работа с TextGrid и практика запуска.
  - [Auto Lip-sync with Montreal Forced Aligner](https://www.youtube.com/watch?v=OLXrlcnndBs) — автор Yuting Hsueh. Метки MFA ведут губы персонажа в Maya, транскрипция сделана отдельным сервисом. Пример для сцен с персонажем.

## Что реально получается

- Метки слов и фонем. Результат по умолчанию — TextGrid с двумя слоями, слова и фонемы (`--output_format`: `long_textgrid`, `short_textgrid`, `json`, `csv`). Слова идут для анимации «на слове», фонемы — для движения губ.
- Русский. Доступны акустические модели Russian MFA v2.0.0, v2.0.0a, v3.1.0 и Russian CV v2.0.0, словарь Russian MFA v3.1.0 на 452 397 слов. Модель v3.1.0 обучена 2024-06-15. Данные: Common Voice Russian v17.0 (218 ч, 2 858 дикторов), Russian LibriSpeech (98 ч, 13 дикторов), M-AILABS Russian (47 ч, 3 диктора), Multilingual TEDx Russian и GlobalPhone Russian v3.1 ([страница модели](https://mfa-models.readthedocs.io/en/latest/acoustic/Russian/Russian%20MFA%20acoustic%20model%20v3_1_0.html)).
- Работа со сценарием. Вход — папка с аудио и текстовыми файлами того же имени. Слова вне словаря (OOV) обрабатывает модель G2P (`--g2p_model_path`) или команда пропускает файл (`--ignore_oovs`).
- Роль в конвейере студии. Озвучка идёт из [ElevenLabs](elevenlabs.md), у него есть свои метки слов. MFA нужен для проверки, для записанного диктора и когда нужны фонемы. Текст для MFA должен совпадать с произнесённым: числа и сокращения записывают так, как их читает голос (у ElevenLabs это поле `normalized_alignment`).
- Скорость. Выравнивание идёт на процессоре, параллельно (`-j`). GPU для самого выравнивания не нужен. Видеокарта упомянута только при установке SpeechBrain для задач с дикторами.
- Непрерывность сцены, морфинг и камера — не его задача: он даёт времена.

## Слабые стороны

- Нужен словарь произношений. Редкие слова, имена и термины без G2P-модели не выравниваются. Для русских научных терминов потребуется докладывать произношения вручную или обучать G2P.
- Расхождение текста и аудио ломает выравнивание. Лишнее или пропущенное слово сдвигает соседей.
- Модели обучены на чтении в тихой обстановке. Документация предупреждает: на шумной и спонтанной речи будут сбои, а акустическая модель «не уровня современных систем распознавания».
- Установка через conda (Kaldi собран как пакет conda-forge). Без conda не поставить.
- Ударения и интонация меток не дают.
- Сложнее по ощущению, чем облачный Forced Alignment: корпус, словарь, модели, формат TextGrid.

## Сложность

- Для человека (4 из 5): нужны conda, командная строка, понимание словаря и TextGrid. Первый запуск по примеру — несколько часов, свой корпус и OOV — дни.
- Для агента (2 из 5): всё командами `mfa model download`, `mfa validate`, `mfa align`. Агент разбирает TextGrid или JSON и сам проверяет покрытие. Руки нужны при установке окружения и при подборе произношений для редких слов.

## Автоматизация и воспроизводимость

- Автоматизация (5 из 5): командная строка, пакетная обработка, форматы JSON и CSV, модели скачиваются командой, поддержка Docker (в документации).
- Воспроизводимость (4 из 5): версии модели и словаря закрепляются, расчёт детерминирован при тех же версиях. Результат зависит от версии MFA и модели (в документации указана совместимая версия).

## Платформа и оборудование

Linux, macOS и Windows через conda (`conda create -n aligner -c conda-forge montreal-forced-aligner`). Видеокарта для выравнивания не нужна. Минимальных требований к памяти в документации не нашёл. Пакет на PyPI называется `Montreal-Forced-Aligner` (3.4.3), но документация предписывает установку через conda.

## Экспорт

TextGrid (длинный и короткий), JSON, CSV. Метки слов и фонем с границами в секундах.

## Стоимость

Проверено 2026-10-14. Бесплатно: программа MIT, модели CC BY 4.0 и CC0. Платных тарифов нет.

## Лицензия и права

- Код или программа: MIT (LICENSE, 2016 Montreal Corpus Tools; PyPI).
- Результат: метки времени принадлежат автору, лицензия MIT ограничений на коммерческое использование не накладывает.
- Ассеты в комплекте: модели и словарь скачиваются отдельно. Русская акустическая модель v3.1.0 и русский словарь v3.1.0 — CC BY 4.0, модель Russian CV v2.0.0 — CC0 ([страница моделей](https://mfa-models.readthedocs.io/en/latest/acoustic/Russian/index.html)). CC BY требует указывать авторство при распространении моделей. Метки времени, полученные с их помощью, моделью не являются.

Это сведения из лицензий, не юридическая консультация.

## Активность и зрелость

<!-- gh-stats:MontrealCorpusTools/Montreal-Forced-Aligner -->
- Звёзды GitHub: 1 903
- Последний коммит в основной ветке: 2026-10-08
- Последний релиз или тег: v3.4.3 (2026-10-08)
- Лицензия по данным GitHub: MIT
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория MontrealCorpusTools/Montreal-Forced-Aligner, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Релизы на PyPI: 3.3.9 (2026-02-02), 3.3.10 (2026-07-06), 3.4.0 (2026-07-06), 3.4.1 (2026-07-11), 3.4.2 (2026-08-20), 3.4.3 (2026-10-08). С версии 3.4 появились новые форматы моделей с интеграцией Hugging Face. Развивает Montreal Corpus Tools. Статья: McAuliffe et al., Interspeech 2017 ([DOI 10.21437/Interspeech.2017-1386](https://doi.org/10.21437/interspeech.2017-1386)).

## Когда брать и когда нет

- Брать: сценарий известен, голос чистый (синтез или студийная запись), нужны слова и фонемы, например для губ персонажа. Нужна проверка меток другого инструмента.
- Не брать: когда нужен быстрый результат без окружения (тогда Forced Alignment в [ElevenLabs](elevenlabs.md)). Когда речь с шумом. Когда нужно распознать текст без сценария (тогда [WhisperX](whisperx.md) или [whisper.cpp](whisper-cpp.md)).

## Источники

- [Документация, главная](https://montreal-forced-aligner.readthedocs.io/en/latest/) — версия 3.4, модели на Hugging Face. Проверено 2026-10-14.
- [Установка](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html) — conda, SpeechBrain с GPU или процессором. Проверено 2026-10-14.
- [Команда align](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/alignment.html) — форматы вывода, OOV, G2P, параллелизм. Проверено 2026-10-14.
- [Пример выравнивания](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/alignment_example.html) — команды скачивания и запуска. Проверено 2026-10-14.
- [Русская акустическая модель v3.1.0](https://mfa-models.readthedocs.io/en/latest/acoustic/Russian/Russian%20MFA%20acoustic%20model%20v3_1_0.html) — дата обучения, данные, CC BY 4.0, оговорки. Проверено 2026-10-14.
- [Русские акустические модели](https://mfa-models.readthedocs.io/en/latest/acoustic/Russian/index.html) — список и лицензии. Проверено 2026-10-14.
- [Русский словарь v3.1.0](https://mfa-models.readthedocs.io/en/latest/dictionary/Russian/Russian%20MFA%20dictionary%20v3_1_0.html) — 452 397 слов, CC BY 4.0. Проверено 2026-10-14.
- [PyPI: Montreal-Forced-Aligner](https://pypi.org/project/Montreal-Forced-Aligner/) — версии, MIT, даты. Проверено 2026-10-14.
- [LICENSE](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/blob/main/LICENSE) — MIT. Проверено 2026-10-14.

## Неизвестно

- Точность меток на русском синтезированном голосе ElevenLabs: запуск не выполнялся.
- Обрабатывает ли русский словарь ударения и формы слов, и как с числами: в описании нет.
- Время выравнивания длинного ролика на обычном ноутбуке.
- Работа на Windows без WSL: в документации есть путь для Docker, цифр нет.
- Минимальные требования к памяти.
