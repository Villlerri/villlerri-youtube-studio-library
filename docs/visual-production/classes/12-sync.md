# Синхронизация со сценарием и озвучкой

## Что сюда входит

Класс связывает по времени сценарий, голос и картинку: озвучка, метки времени слов, выравнивание текста по аудио, субтитры и черновой аниматик. Сам по себе он ничего не рисует. Он даёт времена, на которые вешают ключевые кадры в [Manim](../tools/manim-ce.md), [Motion Canvas](../tools/motion-canvas.md) и [Remotion](../tools/remotion.md). Правило студии: озвучка делается только через ElevenLabs. Другие синтезаторы речи библиотека не рассматривает по этому правилу, карточек на них нет.

## Когда этот класс нужен

- Линия, формула или стрелка должны появиться ровно на слове диктора: вывод формул, рисование и объяснение «вживую».
- Смена кадра и смысловой шаг сцены привязаны к фразе, а не к таймеру. Так видно, где сцена развивается, а где повторяет один кадр в другой крупности.
- Субтитры и кинетическая типографика, которые идут вместе со словами.
- Проверка ритма ролика на эскизах до начала анимации (аниматик под голос).
- Живая запись диктора или готовый файл без текста, к которым нужны метки слов.
- Сцены с персонажем: движение губ по фонемам.

## Основные решения

- [ElevenLabs](../tools/elevenlabs.md) — единственный разрешённый голос. Метки времени дают синтез с метками (по символам) и Forced Alignment (по словам). Коммерческое право на результат с тарифа Starter ($6 в месяц).
- [manim-voiceover](../tools/manim-voiceover.md) — закладки в тексте запускают анимацию Manim на слове. Связка с ElevenLabs держится на старом SDK и не проверена, метки слов берутся через Whisper.
- [WhisperX](../tools/whisperx.md) — метки слов для любой записи, локально, лучше с видеокартой. Нужен для живого диктора и проверки меток.
- [Montreal Forced Aligner](../tools/montreal-forced-aligner.md) — выравнивание известного сценария, слова и фонемы, есть русская модель. Тяжёлая установка через conda.
- [aeneas](../tools/aeneas.md) — старый выравниватель по фрагментам текста. Заброшен: последний релиз 2017 года.
- [Whisper и whisper.cpp](../tools/whisper-cpp.md) — офлайн-распознавание на любом железе. Пословные метки помечены как экспериментальные.
- [Aegisub](../tools/aegisub.md) — ручной тайминг по звуку и ASS-караоке. Версия 3.5.0 вышла в октябре 2026.
- [Storyboarder](../tools/storyboarder.md) — быстрый аниматик на эскизах под голос. Заброшен с 2022 года, лицензия не определена.

Смежные карточки других классов:

- [Remotion](../tools/remotion.md) — пакет `@remotion/captions` даёт общий формат `Caption` и преобразователи из whisper.cpp, OpenAI Whisper и распознавания ElevenLabs.
- [Motion Canvas](../tools/motion-canvas.md) — «time events»: именованные метки на таймлайне, `waitUntil` ждёт метку. Время правится в редакторе, а не в коде.
- [Descript](../tools/descript.md) — монтаж видео правкой текстовой расшифровки (на сайте «Text-based video editing»).
- [auto-editor](../tools/auto-editor.md) — командная строка, которая вырезает паузы по громкости: первый проход монтажа.

### Как решения складываются в процесс

1. Сценарий. Вручную. Текст по сценам. Числа и сокращения пишут так, как их читает голос: иначе метки и текст расходятся. Для терминов и ударений у ElevenLabs есть словари произношения (до трёх на запрос), их проверяют на слух.
2. Озвучка. Запрос в ElevenLabs по сценам автоматический, прослушивание человек. Аудио и ответ сохраняют в проекте: повторная генерация даёт другую запись.
3. Метки времени. Автоматически: символьные метки из синтеза с метками или Forced Alignment для готового аудио. Слова собирают из символов. Для проверки и для живой записи запускают [WhisperX](../tools/whisperx.md) или [Montreal Forced Aligner](../tools/montreal-forced-aligner.md). Результат — один JSON на сцену.
4. Анимация по словам. Человек выбирает слова-опоры («здесь появляется линия»). Дальше автоматически: метки превращаются в ключевые кадры, через закладки [manim-voiceover](../tools/manim-voiceover.md) или через свой JSON в Manim, Remotion и Motion Canvas. Смена озвучки пересчитывается без ручной подгонки.
5. Аниматик. Вручную: эскизы под голос в [Storyboarder](../tools/storyboarder.md) или черновой рендер на низком качестве. Проверяют ритм и развитие сцены, повтор одного кадра в разной крупности.
6. Субтитры. Автоматически из меток (SRT, VTT), правка и оформление вручную в [Aegisub](../tools/aegisub.md).

## Сравнение

Оценки взяты из карточек. Качество меток на русской речи не измерялось нигде: запуски не выполнялись.

- Потолок качества:
  - 4 из 5: [ElevenLabs](../tools/elevenlabs.md) (голос и символьные метки без отдельной программы), [WhisperX](../tools/whisperx.md) (слова по фонемному выравниванию), [Montreal Forced Aligner](../tools/montreal-forced-aligner.md) (слова и фонемы по сценарию).
  - 3 из 5: [manim-voiceover](../tools/manim-voiceover.md) (потолок задают Manim и голос), [whisper.cpp](../tools/whisper-cpp.md) (метки слов экспериментальные), [Aegisub](../tools/aegisub.md) (вручную точно, слова не автоматические).
  - 2 из 5: [aeneas](../tools/aeneas.md) (метод через eSpeak, заброшен), [Storyboarder](../tools/storyboarder.md) (эскизы, не готовая графика).
- Трудность для человека:
  - 1: Storyboarder. 2: ElevenLabs (веб и маленький скрипт для JSON), whisper.cpp (сборка и модель).
  - 3: manim-voiceover (Python и Manim), WhisperX (окружение с CUDA), Aegisub (горячие клавиши, ASS), aeneas (старое окружение).
  - 4: Montreal Forced Aligner (conda, словарь, TextGrid).
- Трудность для агента:
  - 1: ElevenLabs (REST и JSON, агент проверяет покрытие символов). 2: manim-voiceover, WhisperX, Montreal Forced Aligner, whisper.cpp (команды и код, слух нужен человеку).
  - 3: aeneas (поднять старое окружение). 4: Aegisub и Storyboarder (работа в окне, нет API для сборки).
- Автоматизация:
  - 5: ElevenLabs, manim-voiceover, WhisperX, Montreal Forced Aligner, aeneas, whisper.cpp (API или командная строка, пакетная обработка).
  - 2: Aegisub (макросы Lua внутри программы, без пакетного режима). 1: Storyboarder (скриптов нет).
- Стоимость:
  - Бесплатны: manim-voiceover (голос оплачивается отдельно), WhisperX, Montreal Forced Aligner, aeneas, whisper.cpp, Aegisub, Storyboarder.
  - ElevenLabs: коммерческое право только на платных тарифах, минимум Starter $6 в месяц. API без подписки от $0,08 за 1000 знаков; десятиминутный ролик по прикидке около $0,8. На Free монетизируемый ролик публиковать нельзя.
  - Видеокарта нужна для скорости WhisperX и не обязательна для остальных.
- Плавность переходов и непрерывность сцены:
  - Ни один инструмент класса не рисует и не двигает камеру: все дают только времена.
  - Сцену не рвёт [manim-voiceover](../tools/manim-voiceover.md): блоки озвучки живут внутри одного `construct()` Manim, объекты остаются в кадре, темп задаёт голос.
  - В Motion Canvas то же делают «time events», в Remotion общий формат `Caption`.
  - Aegisub двигает слова титров по ASS, Storyboarder показывает ритм смен кадров, но движения внутри кадра в нём нет.

## Другие решения

- [stable-ts](https://github.com/jianfch/stable-ts) — MIT. Доработка Whisper для устойчивых меток слов. README: разработка приостановлена на неопределённый срок, последний коммит 2026-05-30.
- [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) — AGPL-3.0. Многоязычное распознавание с метками слов и уверенностью. Последний коммит 2026-09-28.
- [ctc-forced-aligner](https://github.com/MahmoudAshraf97/ctc-forced-aligner) — BSD-2-Clause. Выравнивание моделями CTC с Hugging Face. По README русский и ещё 1126 языков, видеокарта по возможности. Модель по умолчанию под CC-BY-NC 4.0: для коммерческого ролика нужна другая.
- [Gentle](https://github.com/strob/gentle) — MIT. Выравниватель на Kaldi с окном в браузере и REST, приложение для Mac и образ Docker. Языки в README не названы, последний коммит 2025-02-16.
- [Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit) — MIT. Редактор субтитров для Windows, macOS и Linux. В README есть необязательные сторонние сервисы распознавания речи и перевода.
- [Boords](https://boords.com) — облачный сервис для сценариев и раскадровок, «аниматик в один щелчок». Бесплатный план: 5 активных раскадровок. Solo $39 в месяц ($26 при оплате за год).
- [YouTube Studio: автосинхронизация текста](https://support.google.com/youtube/answer/2734796) — загрузить готовый текст, система сама расставит время. Текст должен быть на языке видео и на языке из списка распознавания. Не рекомендуется для роликов длиннее часа и при плохом звуке.
- [Автосубтитры YouTube](https://support.google.com/youtube/answer/6373554) — машинные субтитры, русский в списке языков. Качество зависит от звука и произношения.
- [Gemini API: понимание аудио](https://ai.google.dev/gemini-api/docs/audio) — платный API. В примере запроса метки сегментов в формате MM:SS, пословных меток страница не описывает. Не использовался.
- [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) — MIT. Формы рта 2D-персонажа по записи. Распознаватель PocketSphinx только для английского, для других языков фонетический. Последний коммит 2025-04-03.

## Вывод для объясняющих видео

Озвучку и первые метки времени берём у ElevenLabs. Это единственный разрешённый голос, русский язык поддержан, посимвольные метки приходят без отдельного распознавания. Для монетизации нужен платный тариф с первой генерации. Метки сохраняем в проекте как JSON и от них считаем ключевые кадры в Manim, Remotion или Motion Canvas. Смена озвучки тогда не требует ручной подгонки. [manim-voiceover](../tools/manim-voiceover.md) удобен закладками на словах, но его связку с ElevenLabs надо проверить до работы. WhisperX и Montreal Forced Aligner нужны для живой записи и независимой проверки меток. Aegisub оставляем для субтитров. Storyboarder и aeneas заброшены и дают разве что черновик: ритм сцен проще проверить быстрым рендером самих сцен.

## Источники

- [Remotion: @remotion/captions](https://www.remotion.dev/docs/captions/api) — формат `Caption` и преобразователи из whisper.cpp, OpenAI Whisper, ElevenLabs. Проверено 2026-10-14.
- [Remotion: транскрибирование](https://www.remotion.dev/docs/captions/transcribing) — варианты распознавания: `@remotion/install-whisper-cpp` (бесплатно, офлайн), `@remotion/openai-whisper` и `@remotion/elevenlabs` (платные API). Проверено 2026-10-14.
- [Motion Canvas: time events](https://motioncanvas.io/docs/time-events) — метки на таймлайне, `waitUntil`, правка в редакторе. Проверено 2026-10-14.
- [Descript](https://www.descript.com/) — текстовый монтаж видео, расшифровка, удаление слов-паразитов. Проверено 2026-10-14.
- [README auto-editor](https://github.com/WyattBlue/auto-editor) — командная строка, автомонтаж по громкости, первый проход вырезает «мёртвые» участки. Проверено 2026-10-14.
- [README stable-ts](https://github.com/jianfch/stable-ts) — пометка о приостановке разработки; лицензия MIT; PyPI 2.19.1 от 2025-08-16. Проверено 2026-10-14.
- [README whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) — описание, лицензия AGPL-3.0. Проверено 2026-10-14.
- [README ctc-forced-aligner](https://github.com/MahmoudAshraf97/ctc-forced-aligner) — языки, лицензия BSD-2-Clause, модель по умолчанию CC-BY-NC 4.0. Проверено 2026-10-14.
- [README Gentle](https://github.com/strob/gentle) — Kaldi, окно в браузере, REST, MIT; репозиторий переехал с lowerquality/gentle. Проверено 2026-10-14.
- [README Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit) — платформы, лицензия MIT, необязательные сторонние сервисы. Проверено 2026-10-14.
- [Boords: цены](https://boords.com/pricing) и [главная](https://boords.com/) — планы и аниматик. Проверено 2026-10-14.
- [YouTube: добавление субтитров](https://support.google.com/youtube/answer/2734796) — автосинхронизация текста. Проверено 2026-10-14.
- [YouTube: автоматические субтитры](https://support.google.com/youtube/answer/6373554) — список языков, русский. Проверено 2026-10-14.
- [Gemini API: аудио](https://ai.google.dev/gemini-api/docs/audio) — пример запроса с метками MM:SS. Проверено 2026-10-14.
- [README Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) — распознаватели, лицензия MIT. Проверено 2026-10-14.
- Даты последних коммитов взяты со страниц коммитов GitHub каждого проекта. Проверено 2026-10-14.
