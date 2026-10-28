# Пакет выкладки: пилот Countable AI

Поля для YouTube Studio, Shorts, оформление канала и порядок ручной выкладки. Выкладывает автор. Агент ничего не публиковал и канал не регистрировал. Подготовлено 2026-10-18.

Формат пакетов каналов 50–52 в репозитории не найден. Пакет составлен по полям формы загрузки YouTube Studio.

## Файлы

- Альбом «Пилот без голоса» на доске задачи 60: копия пилота с субтитрами в кадре, 1920×1080, 8:51; два Shorts 1080×1920; обложка, аватар, баннер.
- Чистая копия пилота без субтитров, 407 МБ, в альбом не помещается. Она лежит в рабочей копии задачи 60 и удаляется при закрытии задачи. Для выкладки она не нужна: видео с голосом собирается заново.
- [captions-en.srt](captions-en.srt) — субтитры EN, 150 строк.
- [thumbnail.png](thumbnail.png) — обложка 1280×720.
- [avatar.png](avatar.png) — аватар 800×800.
- [banner.png](banner.png) — баннер 2560×1440. Безопасная зона 1546×423 в центре.
- [shorts.md](shorts.md) — поля обоих Shorts и их текст.

## Голос

Голоса нет: ElevenLabs не подключён. Тайминг кадров и субтитров рассчитан по числу букв в словах, около 150 слов в минуту.

После озвучки:
1. ElevenLabs отдаёт время каждого слова. Оно заменяет расчётное время в сборщике кадров.
2. Кадры, субтитры, главы и Shorts пересобираются из того же сценария. Длина может сдвинуться на ±30 с.
3. Главы ниже переписываются по новой длине кадров.

Сборщик кадров — код Python и JS, сохранён документами в [../build/](../build/index.md). Там же порядок пересборки под голос.

## Название

```
Why AI Makes Things Up — We Counted It by Hand
```

## Описание

Ссылку на файлы примера вставляет автор: агент ничего не выкладывал.

```
AI tools sometimes say false things — calmly, in perfect sentences. We build a tiny "AI" from a three-message family chat, count every step with a pencil, and watch it write "Mom is at the gym." Every word is true. The sentence is false. Then we look at why real models guess, using the 2025 paper "Why Language Models Hallucinate".

This is a toy model. Real AI is far bigger; the video shows exactly where the toy stops matching it.

Count it yourself — the sheet, the table, the exam and a script that checks every number:
[LINK TO EXAMPLE FILES]

Chapters
0:00 Cold open: AI says false things calmly
0:40 The toy: a three-message family chat
1:16 Counting by hand: 6 of 9 sentences are false
3:20 Shannon, 1948: the same trick on real English
4:09 What real models do differently
4:54 Why models guess: rare facts and grading
7:27 What this toy leaves out
8:15 What to check in an AI answer
8:39 Count it yourself

Sources
C. E. Shannon, "A Mathematical Theory of Communication", Bell System Technical Journal, 1948, section 3.
T. B. Brown et al., "Language Models are Few-Shot Learners", arXiv:2005.14165, 2020.
A. T. Kalai, O. Nachum, S. S. Vempala, E. Zhang, "Why Language Models Hallucinate", arXiv:2509.04664, 2025.
```

После озвучки дописать в конец описания: «Voice: ElevenLabs.»

## Теги

```
AI hallucination, why AI makes things up, how AI works, language models explained, ChatGPT wrong answers, Claude Shannon, Markov chain, next word prediction, AI for beginners, Countable AI
```

## Закреплённый комментарий

```
Try it: roll a die for "the" — 1–2 store, 3–4 gym, 5–6 park. Start from Mom. How many rolls until you get a false sentence? Post your count.
```

## Прочие поля

- Аудитория: «Нет, это видео не для детей».
- Категория: Education.
- Язык видео и субтитров: English.
- Изменённый или синтетический контент: «Нет». Отметка нужна для реалистичного контента: голос или лицо реального человека, реальные события. Здесь их нет. Если голос ElevenLabs будет клоном реального человека — «Да».
- Субтитры: загрузить `captions-en.srt` после озвучки, пересобранный по голосу. Файл сейчас — по расчётному таймингу.

## Оформление канала

- Название: Countable AI.
- Описание канала:

```
How AI works — on examples small enough to check with a pencil. Every video builds a toy model, counts it by hand, and shows where the toy stops matching real AI. All files are linked, so you can count it yourself.
```

- Аватар и баннер — файлы выше.

## Порядок выкладки

Выполняет автор, в своём аккаунте Google.

1. Создать канал Countable AI в YouTube Studio. Загрузить аватар, баннер, описание канала.
2. Подтвердить канал по телефону. Без этого YouTube не принимает свою обложку.
3. Выложить файлы примера и вставить ссылку в описание вместо `[LINK TO EXAMPLE FILES]`.
4. Загрузить видео с голосом. Видео без голоса — только для проверки, не для выкладки.
5. Заполнить поля по этому пакету, загрузить обложку и субтитры.
6. Видимость «С ограниченным доступом». Проверить главы, обложку, субтитры по ссылке.
7. Перевести в «Открытый доступ» или задать время публикации.
8. Закрепить комментарий.
9. Shorts выложить через 1–3 дня после пилота, по [shorts.md](shorts.md). В каждом Short указать пилот как связанное видео.
