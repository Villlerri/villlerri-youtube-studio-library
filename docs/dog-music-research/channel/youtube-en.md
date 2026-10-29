# Оформление канала: YouTube, английский

Задача 127, 2026-10-29, для Villlerri. Пакет для YouTube: название, описание, ключевые слова, аватар, шапка, ролики 1 и 2. Тексты для вставки — в рамках, на английском. Обещания — только из разрешённого списка [этапа 2](../stage2.md#названия-и-описания). Канал создаёт и загружает человек.

## Название канала

Варианты. Занятость адреса (@handle) проверена 2026-10-29 по странице youtube.com/@адрес: «свободен» — страницы нет.

1. **Slow Notes for Dogs** — @SlowNotesForDogs, свободен. Выбрано Villlerri 2026-10-29: про музыку и медленный темп, без обещаний эффекта.
2. Gentle Hours for Dogs — @GentleHoursForDogs, свободен. Про длинный формат.
3. Soft Hours for Dogs — @SoftHoursForDogs, свободен.
4. Dusk & Paws — @DuskAndPaws, свободен. Образ, но без слова «музыка».
5. Hush Hound Music — @HushHoundMusic, свободен. Игривее остальных.

Заняты: Quiet Hours For Dogs, Calm Paws Music — существующие каналы. Адрес может занять кто-то другой до создания канала.

Адрес — 3–30 знаков. Длину названия Справка не называет, API ограничивает 30 знаками; все варианты короче. Название и адрес можно менять не больше двух раз за 14 дней ([справка](https://support.google.com/youtube/answer/2972003)).

## Описание канала

До 1 000 знаков, в тексте ниже 883.

```text
Slow, quiet instrumental music for dogs at home: piano, harp, flute, clarinet and soft strings, in long videos for the hours you're away.

Every video is new music: about 150 short pieces, each heard once, with no loops. The tempo is slow (about 50–66 beats per minute), the volume stays even, and there are no voices, percussion, thunder, doorbells or barking. The picture is a dark, slow scene in blues and soft yellows.

What research says: studies in kennels found a small calming effect of quiet classical and piano music on dogs. For dogs at home alone there is no evidence yet. These videos are not a treatment for anxiety or any other condition. If your dog is distressed when left alone, talk to a vet or a qualified behaviourist.

The music is composed by an AI agent with code and played with free (CC0) orchestral samples. Every video is labelled as AI-generated content.
```

## Ключевые слова канала

До 500 знаков суммарно, ниже 202.

```text
music for dogs, dog music, calm music for dogs, quiet music for dogs, music for dogs home alone, piano for dogs, harp for dogs, flute music for dogs, instrumental music for dogs, 10 hours music for dogs
```

«Помогает спать», «снимает тревогу» и подобное в ключевые слова не берём.

## Аватар и шапка

- Аватар: [avatar-800.png](avatar-800.png), 800×800. Жёлтый месяц и светлая лапа на тёмно-синем; всё важное — внутри круга, который показывает YouTube. Нарисован кодом.
- Шапка: [youtube-banner-2560x1440.png](youtube-banner-2560x1440.png), 2560×1440, 1,65 МБ. Сцена ролика 2, название и строка «Slow, quiet music for dogs at home · 10-hour videos». Текст — в безопасной зоне 1546×423 в центре, она видна на всех устройствах.
- Требования YouTube ([справка](https://support.google.com/youtube/answer/10456525)): аватар показывается 98×98, файл до 15 МБ; шапка от 2048×1152, рекомендовано 2560×1440, до 6 МБ.
- Обложка ролика: 16:9, ширина от 640, JPG или PNG, до 50 МБ с компьютера ([справка](https://support.google.com/youtube/answer/72431)). Наши обложки 1280×720 подходят.

## Ролик 1: фортепиано и арфа

- Название: `Calm Piano & Harp for Dogs · 10 Hours of Quiet Music While You're Away`
- Описание, переводы названия и настройки — [паспорт пилота](../pilot/passport.md#описание).
- Теги: `music for dogs, dog music, calm piano for dogs, harp for dogs, quiet music for dogs, dog home alone, 10 hours`
- Обложка: [thumbnail.png пилота](../pilot/thumbnail.png), 1280×720.

## Ролик 2: флейта и кларнет

- Название: `Calm Flute & Clarinet for Dogs · 10 Hours of Soft Music for a Quiet Home`
- Описание, переводы названия и настройки — [паспорт ролика 2](../v2/passport.md#описание).
- Теги: `music for dogs, dog music, calm flute for dogs, clarinet for dogs, quiet music for dogs, dog home alone, 10 hours`
- Обложка: [thumbnail.png ролика 2](../v2/thumbnail.png), 1280×720.

## Порядок загрузки на YouTube

1. Создать канал на аккаунте Google: личный или Brand Account, если канал будут вести несколько человек ([справка](https://support.google.com/youtube/answer/1646861)). Юрлицо не нужно.
2. Подтвердить канал по телефону. Без этого нельзя загружать ролики длиннее 15 минут и ставить свои обложки ([справка](https://support.google.com/youtube/answer/71673)).
3. Оформление: название, адрес, описание, ключевые слова, аватар, шапка — из этого документа.
4. До первой загрузки — проверка паузы «Продолжить просмотр?» на телевизоре и телефоне ([этап 3](../stage3.md#3-длина-ролика)).
5. Загрузка ролика: Studio → «Создать» → «Загрузить видео». Название, описание, теги и обложка — из этого документа.
6. Аудитория: «Нет, это видео не для детей». Возрастное ограничение: нет.
7. «Изменённый или синтетический контент» (AI use): «Да». Раскрытие обязательно, когда ИИ-музыка — основа ролика ([справка](https://support.google.com/youtube/answer/14328491)).
8. Категория: «Животные» (Pets & Animals), как в паспорте пилота.
9. Доступ «Ограниченный» до конца шага «Проверки» (авторские права), затем «Открытый».
10. Автоматическую рекламу в середине выключить.

Лимит загрузки после подтверждения — 12 часов или 256 ГБ: наши ролики на 10 часов и 1,45–2,55 ГБ проходят.
