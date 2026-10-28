# Методика: доска, замер, пробы

Как получены цифры [записки](index.md). Платных вызовов моделей нет. Голос не синтезировался, картинки не генерировались.

## Доска Pinterest

- Адрес: https://ru.pinterest.com/villlerriv/ютуб-идеи/ , открыт 2026-10-25 без входа. Счётчик доски — 42 пина.
- Страница без входа показывает окно входа поверх доски, но пины видны. Список пинов получен запросом страницы `BoardFeedResource` из того же браузера: 41 пин и 2 «истории».
- Картинки скачаны в размере 736 px и просмотрены вручную. Совпадают побайтно три пары, разных картинок 38.
- Картинки доски чужие: в репозиторий они не сохранены.

## Замер спроса и конкуренции

Тот же код и те же определения, что в задаче 64: [channel-reassessment/method.md](../channel-reassessment/method.md), код — [channel-reassessment/method-code.md](../channel-reassessment/method-code.md), разделы 2, 2а, 4 и 5. Код сбора и таблиц не менялся; новые только запросы ниже и пакеты Trends.

- Источник: поиск YouTube без входа, `hl=en`, `gl=US`, по релевантности, два прохода на запрос: «в этом месяце» и «за всё время», первые 40 видео.
- Каналы: подписчики, 30 последних длинных видео, дата создания со страницы «О канале». Ошибок нет ни у одного из 1 005 каналов.
- Инструмент: yt-dlp 2026.08.19, Python 3.14.
- Время замера по записям сбора: 2026-10-25 10:18:07 — 10:23:52 UTC.

Группы каналов: новый — создан меньше 12 месяцев назад; малый старый — до 10 тыс. подписчиков и создан раньше; средний — 10–100 тыс.; большой — от 100 тыс. Неизвестно — нет даты или подписчиков: 11 каналов.

Метрики:

- Сопоставимые видео: длиннее 3 минут, возраст 7–30 дней, проход «в этом месяце». Медиана и `n` по группам.
- Типичное видео канала: медиана просмотров его длинных видео старше 30 дней из 30 последних.
- `n` — всегда число видео, если не написано «каналов». При `n` меньше 15 медиана ненадёжна.

Запросы (файл `segments.json`):

```json
[
 {"id":"brand_history","name":"История брендов и продуктов","lang":"en","gl":"US","q":["brand history documentary","how this brand became famous"]},
 {"id":"ad_marketing","name":"Маркетинг через знаменитые рекламные кампании","lang":"en","gl":"US","q":["famous ad campaigns explained","marketing psychology explained"]},
 {"id":"patents","name":"Изобретения и патенты","lang":"en","gl":"US","q":["history of inventions","patent history explained"]},
 {"id":"everyday_objects","name":"История обычных вещей","lang":"en","gl":"US","q":["history of everyday objects","origin of everyday things"]},
 {"id":"food_history","name":"История еды и напитков","lang":"en","gl":"US","q":["food history documentary","history of snacks"]},
 {"id":"retro_tech","name":"Ретро-техника и поп-культура","lang":"en","gl":"US","q":["history of video game consoles","retro tech history"]},
 {"id":"etymology","name":"Происхождение слов","lang":"en","gl":"US","q":["etymology explained","word origins"]},
 {"id":"design_history","name":"История дизайна, логотипов и плакатов","lang":"en","gl":"US","q":["graphic design history","logo history explained"]},
 {"id":"psychology","name":"Психология и когнитивные искажения","lang":"en","gl":"US","q":["cognitive biases explained","psychology of persuasion"]}
]
```

## Google Trends

Свойство «YouTube», США, 5 лет по неделям. Код — раздел 5 кода задачи 64; заменён только список пакетов:

```python
B=[['documentary','brand history','marketing psychology','history of inventions','food history'],
   ['documentary','etymology','graphic design history','cognitive biases','retro tech'],
   # second pass without the large anchor: growth ratios comparable, levels only inside the batch
   ['brand history','marketing psychology','history of inventions','food history','etymology'],
   ['graphic design history','cognitive biases','retro tech','vintage ads','logo history']]
```

Отношение роста — среднее за последние 52 недели к среднему за предыдущие 52, только во втором проходе без крупного якоря. Фраза годна, если ненулевых недель за два года не меньше 90%. Годны 4 фразы из 10; остальные помечены `no: sparse` в [data/trends.csv](data/trends.csv).

## Пределы

- Поиск без входа и из одного региона. Выдача у зрителя с историей другая.
- По два запроса на тему. Тема шире своих запросов: цифра описывает выдачу по ним, не весь рынок.
- Просмотры публичные. Удержания, CTR и доходов чужих каналов нет.
- Часы людей на ролик — допущение, не замер.

## Данные

- [data/segment-metrics.csv](data/segment-metrics.csv): метрики по 9 темам.
- [data/examples.csv](data/examples.csv): лидер, обычное, лучшее и худшее видео новых и малых каналов по каждой теме.
- [data/videos.csv](data/videos.csv): 1 440 строк выдачи.
- [data/channels.csv](data/channels.csv): 1 005 каналов.
- [data/trends.csv](data/trends.csv): Google Trends.
