# Пакеты выкладки: шортсы Event 1

Три вертикальных шортса из официального прогона. Состояние на 2026-10-16, после правок ассистента. Загрузка — только после согласования итогового видео, самих шортсов и разрешения на публикацию.

Общее для всех трёх:

- Кадр 1080×1920, 60 кадров в секунду. Черновики без голоса: podium 28,6 с, hex 28,8 с, favourite 25,7 с. С голосом длина уточнится. YouTube принимает шортсы до 3 минут.
- Только кадры и цифры официального прогона и 1 000 тестовых прогонов. Ничего не дорисовано.
- Субтитры EN вшиты в кадр, рядом файл SRT.
- Голос — тот же голос ElevenLabs, что в итоговом видео. Текст шортсов — 805 знаков на три ролика, около $0,06. Нужно отдельное разрешение Villlerri на этот платный вызов.
- Сборка: `bun render/shorts.ts out/switchback-sprint 612826258 trials/switchback-sprint.shorts.json`. Файлы: out/switchback-sprint/shorts/<id>/<id>.mp4 и <id>.en.srt. Обложки — upload/shorts/<id>-cover.png, 1080×1920, до 210 КБ.
- Субтитры черновиков — по расчётному темпу. После синтеза голоса их заменят файлы с точными метками.

## Откуда цифры

Все файлы — в папке log/event-1.

- Тестовые прогоны: test-runs-1-1000.csv, 1 000 прогонов итоговой трассы, зёрна 1–1000. Записаны до заморозки, их хеш — в журнале заморозки freeze.md. В каждой строке имена идут в порядке финиша.
  - GLIDE: 290 побед из 1 000, 29,0%.
  - ANVIL: 30 из 1 000, 3,0%.
  - HEX: 97 из 1 000, 9,7%.
  - HEX на 11-м или 12-м месте: 232 из 1 000, 23,2%.
- Это доли этой выборки на этой трассе, не общие вероятности. Поэтому в тексте прошедшее время и «of our thousand test runs».
- Официальный прогон: result-612826258.json и лист событий events-612826258.json.
  - Итог: HEX, COMET, ANVIL. GLIDE четвёртый, на 0,132 с позади ANVIL: поле gaps.
  - ANVIL восьмой через 1 с после ворот: поле earlyOrder. Третий на отметках 16,07 с и 24,10 с: поле marks.
  - GLIDE позади ANVIL с 1,75 с заезда и до финиша. Проверено по журналу кадров frames-612826258.bin тем же правилом порядка, что у счётчика мест в кадре.
  - Обороты: от ворот до своего финиша HEX сделал 8,0 оборота на 178 м, шар ECHO — 53,7 на 179 м. Поле turns: сумма поворотов по журналу кадров. Это наблюдение одного прогона, о скольжении текст ничего не утверждает.

## 1. podium — рекомендую первым

- Название: `0.132 Seconds for the Podium #shorts` — 36 знаков.
- Сюжет: одно место на пьедестале, две фигуры. ANVIL вышел из кучи восьмым и стал третьим, GLIDE идёт следом и не обходит. Фотофиниш: ANVIL на 0,132 с. Итог тестовых прогонов: GLIDE 290 побед из 1 000, ANVIL 30.
- Экран статистики: «GLIDE WON 290», «ANVIL won 30.», «Tonight: GLIDE 4th.», над ними «1,000 TEST RUNS BEFORE THE OFFICIAL ONE».
- Текст диктора, 280 знаков:
  1. "One podium spot. Two shapes." — Одно место на пьедестале. Две фигуры.
  2. "ANVIL came out of the pile eighth. Now it is third." — ANVIL вышел из кучи восьмым. Теперь он третий.
  3. "GLIDE, the favourite, is right behind. It never gets past." — GLIDE, фаворит, сразу за ним. Обойти не может.
  4. "ANVIL, by a hundred and thirty-two thousandths." — ANVIL, на сто тридцать две тысячных.
  5. "Of our thousand test runs, GLIDE won twenty-nine percent. ANVIL, three." — Из нашей тысячи тестовых прогонов GLIDE выиграл двадцать девять процентов. ANVIL — три.
  6. "Full race on the channel." — Весь заезд — на канале.
- Описание:

```
One podium spot, two shapes, one locked seed. ANVIL takes third by 0.132 s.
In our 1,000 test runs before the official one, GLIDE won 290 and ANVIL 30.
Full race: [link to Event 1]
Game physics (Box2D), not a lab model. Narration: synthetic voice made with ElevenLabs.
```

## 2. hex

- Название: `The Hexagon That Barely Turned Won the Race #shorts` — 51 знак.
- Сюжет: HEX выходит вперёд на 8,6 с и ведёт до финиша. От ворот до финиша он сделал 8 оборотов, шар ECHO — около 54. HEX побеждает. В тестовых прогонах: 97 побед из 1 000 и 232 раза на двух последних местах.
- Заголовок в начале: «WATCH HOW LITTLE IT TURNS.». Экран статистики: «BOOM OR BUST», «HEX won 97.», «Last two places: 232.», над ними «1,000 TEST RUNS BEFORE THE OFFICIAL ONE».
- Текст диктора, 283 знака:
  1. "Watch the hexagon." — Следите за шестиугольником.
  2. "HEX is in front. It hardly turns." — HEX впереди. Он почти не вращается.
  3. "From gate to finish, HEX makes eight full turns. ECHO, a ball, makes about fifty-four." — От ворот до финиша HEX делает восемь полных оборотов. ECHO, шар, — около пятидесяти четырёх.
  4. "HEX wins." — HEX побеждает.
  5. "Of our thousand test runs, HEX won about one in ten. And it finished in the last two places in almost a quarter." — Из нашей тысячи тестовых прогонов HEX выиграл примерно один из десяти. И почти в четверти финишировал на двух последних местах.
  6. "Full race on the channel." — Весь заезд — на канале.
- Описание:

```
Watch the hexagon. From gate to finish it made 8 full turns. ECHO, a ball, made about 54. HEX won by 1.9 s.
In our 1,000 test runs before the official one, HEX won 97.
Full race: [link to Event 1]
Game physics (Box2D), not a lab model. Narration: synthetic voice made with ElevenLabs.
```

## 3. favourite

- Название: `The Favourite Won 290 of 1,000 Test Runs. Tonight? #shorts` — 58 знаков.
- Сюжет: GLIDE выиграл 290 из 1 000 тестовых прогонов. Сегодня идёт четвёртым, не может обойти ANVIL и финиширует на 0,132 с позади. Пьедестал: HEX, COMET, ANVIL.
- Заголовок в начале: «THE FAVOURITE WON 290», над ним «1,000 TEST RUNS».
- Текст диктора, 242 знака:
  1. "GLIDE won twenty-nine percent of our thousand test runs." — GLIDE выиграл двадцать девять процентов нашей тысячи тестовых прогонов.
  2. "Tonight, the ice ball runs fourth." — Сегодня ледяной шар идёт четвёртым.
  3. "And it cannot get past ANVIL." — И обойти ANVIL он не может.
  4. "Fourth, by a hundred and thirty-two thousandths." — Четвёртый, на сто тридцать две тысячных позади.
  5. "The podium: HEX, COMET, ANVIL. Most is not always." — Пьедестал: HEX, COMET, ANVIL. Чаще — не значит всегда.
  6. "Full race on the channel." — Весь заезд — на канале.
- Описание:

```
GLIDE won 290 of our 1,000 test runs before the official one. Tonight it finished 4th, 0.132 s off the podium.
Full race: [link to Event 1]
Game physics (Box2D), not a lab model. Narration: synthetic voice made with ElevenLabs.
```

## Поля загрузки

- Язык: English. Категория: Gaming. Аудитория: «не для детей», как у итогового видео.
- Поле «AI use»: предложение агента — «Нет», как у итогового видео. Это не принятое решение. Основание — в пакете «Пакет выкладки: Event 1», раздел «Поле «AI use»: основание». Итоговое значение проверить по готовому звуку перед публикацией.
- Связанное видео: Event 1. Ставится в поле «Related video» шортса.
- Значок: upload/shorts/<id>-cover.png, настоящий кадр прогона с заголовком. Что проверить в аккаунте — раздел ниже.

## Своя обложка шортса: что проверить

Справка YouTube, прочитано 2026-10-16: https://support.google.com/youtube/answer/72431

- Своя обложка шортса загружается только в YouTube Studio на компьютере. В приложении на телефоне можно только выбрать кадр ролика.
- Нужен подтверждённый аккаунт: https://www.youtube.com/verify
- Число своих обложек в сутки ограничено. Лимит зависит от страны и истории канала, нарушения правил его снижают.
- Формат: JPG или PNG, 9:16, от 640 px по высоте, до 50 МБ с компьютера. Рекомендуемое разрешение — 2160×3840. Наши обложки — 1080×1920 PNG.

Анонс YouTube от 24 июля 2026: https://blog.youtube/news-and-events/youtube-studio-custom-thumbnail-updates/

- Загрузку своих обложек шортсов открыли сначала участникам Партнёрской программы YouTube. Другим авторам её обещают открывать постепенно, без сроков.
- Справка на 16 октября называет только подтверждение аккаунта, без Партнёрской программы. Есть ли функция у нового канала, ни один источник не подтверждает.
- Поэтому перед загрузкой проверить в Studio: «Контент» → «Shorts» → изменить шортс → «Значок». Есть кнопка «Загрузить файл» — загрузить <id>-cover.png.
- Кнопки нет — значит, функция каналу пока недоступна. На компьютере можно выбрать один из трёх предложенных кадров, в приложении — любой кадр. Кадр с 1-й секунды ролика почти совпадает с <id>-cover.png: тот же заголовок на том же моменте заезда.

## Как загрузить

1. Сначала опубликовать итоговое видео Event 1: шортсы ссылаются на него.
2. YouTube Studio на компьютере → «Создать» → «Добавить видео» → <id>.mp4. Вертикальный ролик до 3 минут YouTube сам считает шортсом.
3. Название и описание из блока выше. В описании заменить [link to Event 1] ссылкой на итоговое видео.
4. «Значок»: по разделу «Своя обложка шортса: что проверить».
5. «Связанное видео» → Event 1.
6. «Субтитры» → «Загрузить файл» → <id>.en.srt.
7. Доступ: сначала «Ограниченный», проверка на телефоне, затем «Открытый».

Рекомендую выпускать по одному шортсу в день или два после итогового видео. Это предложение, данных о том, как лучше, нет.

Время загрузки по расчёту: 5–10 минут на шортс. Не измерено.
