# План сборки и рендера

Как из спецификации испытания получить готовый ролик. Повторяется на любом Linux с Bun и GCC. Состояние на 2026-10-15.

## Версии

- Box2D 3.1.1, архив исходников с GitHub, sha256 fb6ef914b50f4312d7d921a600eabc12318bb3c55a0b8c0b90608fa4488ef2e4. Сборка проверяет хеш.
- GCC 15.2, флаги -O2 -std=gnu17 -ffp-contract=off, как в сборке самого Box2D для повторяемости.
- Bun 1.4.2. Пакеты закреплены в bun.lock: @napi-rs/canvas 1.0.9, ffmpeg-static 5.3.0 (FFmpeg 7.0.2, libx264).
- Шрифты: файлы лежат в assets/fonts вместе с лицензиями. sha256: BarlowCondensed-Medium 262bd143292ce479ee0cd09a42b47ab173fca8e9c6eb5ed0b5c8a845bc371d17, BarlowCondensed-SemiBold 7b619d14bc2327509a9ef32b0890f709626f7ecc9ff61191c2a4314c5499d2d9, BarlowCondensed-Bold e476562ec9c1e16cf16475895b511f08c804f438cc9a9f80a44ea50a0eeb5b65, JetBrainsMono-Variable 48715a42ec242c21e9f02692891e147d022299a52e48d5e413e1a942193ffeda.

## Файлы

- league/roster.json — 12 постоянных участников: форма, размер, плотность, трение, упругость, цвет. Не меняется весь сезон.
- trials/<событие>.json — спецификация испытания: трасса, старт, правила.
- sim/league.c — расчёт на Box2D. sim/build-scene.ts — геометрия из спецификации.
- render/render.ts — кадры и сборка видео. render/sound.ts — звук из журнала.
- out/ — результаты расчёта и рендера, в git не хранятся, повторяются командами ниже.

## Шаги

Команды запускаются из папки projects/pilots/sandbox-trials.

1. Установка: `bun install`, затем `sim/build.sh`. Скачивает и собирает Box2D, собирает расчёт.
2. Геометрия: `bun sim/build-scene.ts trials/switchback-sprint.json out/switchback-sprint`.
3. Тестовые прогоны: `deps/league out/switchback-sprint/scene.txt batch 1 1000 > out/switchback-sprint/batch-1000.csv`. Доли побед, длительность, отрыв на финише.
4. Настройка трассы только на тестовых зёрнах 1–1000. Параметры участников не трогаются.
5. Заморозка. В журнал выпуска пишутся: sha256 спецификации и scene.txt, версия Box2D, коммит кода, итоги 1 000 тестовых прогонов.
6. Официальное зерно — только после заморозки, по правилу ниже.
7. Официальный прогон: `deps/league out/switchback-sprint/scene.txt run <зерно> out/switchback-sprint/frames-<зерно>.bin out/switchback-sprint/hits-<зерно>.csv > out/switchback-sprint/result-<зерно>.json`.
8. Повторный прогон того же зерна: хеш итоговых позиций должен совпасть. Не совпал — выпуск не делается.
9. Лист событий: `bun sim/events.ts out/switchback-sprint <зерно>`. Лидеры, порядок по четвертям заезда, отрывы, кто сколько мест отыграл. Реплики диктора пишутся только по нему.
10. Сценарий: `bun render/script.ts trials/switchback-sprint.episode.json out/switchback-sprint`. Из реплик и экранов получаются план склейки timeline.json, текст для ElevenLabs voice.txt, тело сценария, подсчёт знаков, субтитры voice.en.srt и текст для копии просмотра subs-review.ass. Длина экрана — по длине реплики при темпе 2,6 слова в секунду.
11. Экраны: `bun render/cards.ts out/switchback-sprint <зерно> log/event-1/test-runs-1-1000.csv`. Цифры — только из тестовых прогонов и итога официального прогона.
12. Отрезок заезда: `bun render/render.ts out/switchback-sprint <зерно> <с, сек> <по, сек> <файл.mp4>`. Кадры 1920×1080, 60 в секунду, H.264, CRF 18. Звук синтезируется из журнала и сводится к −16 LUFS.
13. Черновик выпуска: `bun render/episode.ts out/switchback-sprint <зерно> out/switchback-sprint/timeline.json out/switchback-sprint/draft-episode-1.mp4 out/switchback-sprint/subs-review.ass`. Картинка частей склеивается без перекодирования, звук — по сэмплам и кодируется один раз. Время каждой части пишется в draft-episode-1.timing.json. С пятым аргументом рядом пишется копия для просмотра draft-episode-1-review.mp4: тот же кадр и полоса под ним с текстом диктора.
14. Обложки: `bun render/covers.ts out/switchback-sprint <зерно> trials/switchback-sprint.episode.json`. Настоящий кадр прогона, камера на нужных фигурах.
15. Голос: `bun render/voice.ts trials/switchback-sprint.episode.json voice/event-1 Brian`. Каждая реплика — отдельный запрос ElevenLabs с метками времени знаков, только через ограничитель трат доски. Платный запрос не повторяется: любая ошибка останавливает прогон. Готовая реплика с тем же текстом и голосом не синтезируется второй раз. Аудио и метки хранятся в voice/event-1.
16. Сборка с голосом: `bun render/script.ts trials/switchback-sprint.episode.json out/switchback-sprint voice/event-1`, затем `bun render/episode.ts out/switchback-sprint <зерно> out/switchback-sprint/timeline.json out/switchback-sprint/episode-1.mp4 out/switchback-sprint/subs-review.ass out/switchback-sprint/voice-track.json`. Экраны держатся по настоящей длине реплик, субтитры — по меткам знаков. Звук приглушается под голосом, затем вся дорожка получает одно усиление до −16 LUFS и ограничитель пиков.
17. Шортсы: `bun render/shorts.ts out/switchback-sprint <зерно> trials/switchback-sprint.shorts.json [папка голоса]`. Кадр 1080×1920, камера на выбранных фигурах, субтитры вшиты.
18. Проверки по [критериям качества](quality.md), затем просмотр автором.

## Правило официального зерна

Предлагаю публичный источник случайных чисел drand (League of Entropy), бесплатный и проверяемый.

- В журнале заморозки до старта записывается номер будущего раунда drand.
- Зерно — первые 8 шестнадцатеричных знаков случайного числа этого раунда, переведённые в число.
- До этого раунда зерно не знает никто, включая студию. Подогнать трассу под победителя нельзя.
- Любой зритель может проверить раунд на сайте drand.

Запасного правила нет. Если drand недоступен в нужный момент, официальный прогон ждёт.

## Что уже работает

- Шаги 1–14 и 17 выполнены для Event 1 на официальном зерне 612826258.
- Повторяемость: 300 зёрен, повтор и три сборки с разной оптимизацией, совпадение побитовое. Официальное зерно повторено: тот же хеш 5aaf2fa57acde9da.
- Черновик выпуска без голоса: 2:51, 10 278 кадров. Рендер с нуля — 2,3–2,6 минуты. Копия для просмотра — ещё около 2 минут.
- Черновики трёх шортсов без голоса: 28,2, 28,8 и 25,7 секунды. Рендер трёх — 139–196 секунд.
- Оформление канала: `bun render/branding.ts out/switchback-sprint/scene.json brand`, подробнее — в документе «Оформление канала».
- Журнал выпуска в log/event-1: заморозка, ответ drand, тестовые прогоны, итог и лист событий официального прогона.

## Что ещё не сделано

- Голос (шаги 15–16): разрешён, но у ограничителя трат доски нет голосового маршрута к ElevenLabs. Сборка проверена на подставном сервере: голос встаёт на свои места, громкость −16,0 LUFS, пик −5,7 dBTP.
- Голос шортсов: нужен отдельный платный вызов, около $0,06.
- Проверка повторяемости на другом компьютере.
