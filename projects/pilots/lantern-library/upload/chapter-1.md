# Пакет выкладки: глава 1 «Dusk»

Черновик к пилоту. Ничего не загружено, разрешения на публикацию нет. Время глав рассчитано по тексту; после синтеза голоса его заменят настоящие метки. Требования YouTube сверены по официальным страницам: [список](../research/youtube-requirements.md).

## Файлы

- Видео: глава 1, MP4, 1920×1080, 30 кадров в секунду, H.264, «fast start»; звук AAC-LC 48 кГц, 384 кбит/с — как рекомендует YouTube. Собирается из папки [probe](../probe/README.md).
- Обложка: [thumb-B.jpg](../frames/thumb-B.jpg), 1280×720, 70 КБ; YouTube принимает от 640 точек по ширине и до 2 МБ с телефона. Запасная для сравнения — [thumb-A.jpg](../frames/thumb-A.jpg).
- Субтитры: [chapter-1-dusk.estimated.srt](../probe/code.md) — английские, по расчётному времени. После синтеза — файл по меткам голоса.

## Название

You Are a Lighthouse Keeper on a Winter Night, 1892 | History for Sleep

69 знаков из 100 допустимых.

## Описание

```
Spend one quiet night in another century.

It is a January evening in 1892, at Fort Point Light on the coast of Maine, where the Penobscot River opens into the bay. You are the keeper, and the lamp must be lit at sunset. In this first part of the night, the afternoon fades, the curtains come down from the lens, and the light goes out over the water.

"You" are a composite character, not a real keeper. The station, the rules and the work come from the sources below. Where the story imagines a thought or the weather of one night, it says so.

Original drawings made for this story. Narration: synthetic voice.

Chapters
00:00 Dusk at Fort Point
01:27 The station on the point
04:48 Lit at sunset: the rule
06:19 Who keeps the light
07:25 The lamp waits in the kitchen
08:52 Oil, drawn by daylight
10:47 Coat, cap and linen apron
12:31 Up the tower
13:47 The curtains come down
15:37 The fourth-order lens
16:58 Lighting the lamp
18:41 Light over the water
20:25 The night ahead
22:36 Rest now

Sources
Instructions to Light-Keepers, U.S. Light-House Board, 1881: https://archive.org/details/1881USLH
Lights and Fog Signals of the United States, Atlantic and Gulf Coasts, 1893: https://archive.org/details/lightlistatlant00servgoog
Official Register of the United States, 1891: https://archive.org/details/sim_united-states-official-register-of-the-united-states_1891-07_1
The Modern Light-House Service, Light-House Board, 1889: https://archive.org/details/modernlighthous00boargoog
Fort Point Light Station, National Register of Historic Places nomination: https://npgallery.nps.gov/GetAsset/ecb5c37d-9cfe-4550-acd2-72b9ce7bc937
U.S. Lighthouse Society archive, Fort Point: https://archives.uslhs.org/places/fort-point-me
Daily Weather Map, January 16, 1892, NOAA Central Library: https://library.oarcloud.noaa.gov/docs.lib/htdocs/rescue/dwm/1892/18920116.pdf
Sun and moon times computed with the U.S. Naval Observatory service: https://aa.usno.navy.mil/data/RS_OneDay
The Fresnel Lens, National Park Service: https://www.nps.gov/caha/learn/historyculture/fresnellens.htm

#HistoryForSleep #SleepStory #Lighthouse
```

Строки о собирательном «вы» и о синтетическом голосе обязательны в каждом описании. Главы в описании YouTube показывает, если первая метка 00:00, меток не меньше трёх и каждая глава не короче 10 секунд: здесь 14 глав, самая короткая около минуты.

## Настройки в YouTube Studio

Аккаунт канала должен быть подтверждён (verified). Без этого YouTube не принимает ролики длиннее 15 минут и свои обложки.

- Аудитория: «No, it's not made for kids». Ролик для взрослых, засыпающих под историю.
- Altered or synthetic content: «No». Рисунок условный, реальных людей и реальных съёмок нет, реалистичных выдуманных сцен нет. Голос синтетический, но не подражает реальному человеку; это раскрыто строкой в описании.
  - Официально про такой голос не сказано. Блог YouTube 2024 года относит к раскрытию синтетический голос человека в разделе о подобии реальных людей.
  - Осторожный вариант — «Yes»: YouTube добавит ярлык о синтетическом содержании. Выбор за ассистентом; рекомендую «No».
- Категория: Education.
- Язык ролика и названия: English. Субтитры: загрузить английский файл .srt.
- Лицензия: Standard YouTube License. Встраивание: разрешено.
- Платная реклама в ролике: нет.
- Теги: history for sleep, sleep story, lighthouse keeper, 1892, Maine, Fort Point Light.
- Обложка: thumb-B.jpg. Если в Studio доступно сравнение обложек, добавить thumb-A.jpg.

## Как загрузить

1. YouTube Studio → Create → Upload videos → выбрать файл главы.
2. Details: вставить название и описание из блоков выше. Загрузить обложку. Audience — «No, it's not made for kids».
3. Show more: Altered content — «No»; язык — English; категория — Education; теги; лицензия.
4. Video elements: субтитры — Upload file → With timing → файл .srt.
5. Checks: дождаться проверки авторских прав. Наш звук и рисунок свои, совпадений быть не должно.
6. Visibility: Private. Публикация или расписание — только после согласования ролика.

## Перед загрузкой

- Критерии качества из [бюджета и критериев](../budget-and-quality.md#критерии-качества) пройдены, отчёт `check.py` приложен.
- Главы в описании совпадают с временем готового ролика.
- Ссылки на источники открываются.
