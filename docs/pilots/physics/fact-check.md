# Научная сверка: часы GPS и Эйнштейн

Проверен сценарий `docs/pilots/physics/script.md` (12 разделов), дата сверки 2026-10-21. Всего 29 утверждений: 19 из списка задачи и 10 найденных при просмотре текста. Правка нужна в 8 пунктах: 6 обязательных (1, 15, 17, 20, 21, 22) и 2 небольших (11, 16). Не подтверждены 2 пункта (19, 29). Остальные 19 верны. Цитаты английские, до 25 слов, с разделом или страницей. Числа пересчитаны скриптом в конце.

Все 8 правок внесены в сценарий 21.10.2026. Пункт 19 тоже учтён: в тексте теперь «на телефоне с Android». В ролике числа NTS-2 взяты из первичного отчёта NRL: 443,1 и 445,0, разница меньше половины процента.

## 1. Телефон находит позицию за секунды, с точностью в несколько шагов

- В сценарии: "Found in seconds, to within a few steps." Перевод: «с точностью до пары шагов».
- Вердикт: верно с уточнением. 4,9 м — это 6–7 шагов, не «пара».
- Источник: [1] GPS.gov (правительство США), «GPS Accuracy», без даты, https://www.gps.gov/gps-accuracy, вопрос «How Accurate is GPS?». Для «секунд»: [26] u-blox, «A-GNSS AssistNow», вендор, вторичный источник, https://www.u-blox.com/en/technologies/agnss-assistnow.
- Цитата: "GPS-enabled smartphones are typically accurate to within a 4.9 m (16 ft.) radius under open sky" ([1]). "With A-GNSS, GNSS receivers can determine their position in seconds, even under poor signal conditions." ([26]).
- Расчёт: 4,9 м = 16,1 ft. Шаг 0,75 м (наше допущение) даёт 6,5 шага. Холодный старт без помощи: кадр 1500 бит при 50 бит/с = 30 с ([6] §20.3.2, §3.2.2). «Секунды» верно для горячего старта и A-GNSS.
- Правка: EN: "Found in seconds, to within about sixteen feet." RU: «Нашёлся за секунды, с точностью около пяти метров.»

## 2. Звук: миля за 5 секунд, километр за 3

- В сценарии: "Every five seconds is about a mile." Перевод: «Каждые три секунды — примерно километр.»
- Вердикт: верно.
- Источник: [17] NWS (NOAA), «Understanding Lightning: Thunder», https://www.weather.gov/safety/lightning-science-thunder. [18] NASA Glenn, «Speed of Sound», https://www.grc.nasa.gov/www/k-12/BGP/sound.html.
- Цитата: "it takes the sound of thunder about 5 seconds to travel a mile" ([17]). "a = sqrt [g * R * T]" ([18]).
- Расчёт: воздух, 20 °C: sqrt(1,4 × 287,05 × 293,15) = 343,2 м/с. Миля = 4,69 с. Километр = 2,91 с. Правило «5 с на милю» — округление с ошибкой 6 %.

## 3. Каждый спутник передаёт своё время и своё положение

- В сценарии: "Every satellite keeps shouting two things: exactly what time it is, and exactly where it is."
- Вердикт: верно. «Exactly» — это метры и наносекунды.
- Источник: [6] IS-GPS-200N (2022), https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §3.2.2 (с. 12), §20.3.3.4.1 (с. 103). [4] GPS.gov, «GPS», https://www.gps.gov/gps.
- Цитата: "The legacy navigation (LNAV) data, D(t), includes SV ephemerides, system time, SV clock behavior data" ([6] §3.2.2). "transmit one-way signals that give the current GPS satellite position and time" ([4]).

## 4. Сигнал идёт меньше десятой доли секунды

- В сценарии: "That message takes less than a tenth of a second to reach you."
- Вердикт: верно. Речь о времени пролёта сигнала. Навигационное сообщение целиком читается 30 с, но в ролике это не нужно.
- Источник: [2] GPS.gov, «Space Segment», https://www.gps.gov/space-segment, раздел «Constellation Arrangement».
- Цитата: "GPS satellites fly in medium Earth orbit (MEO) at an altitude of approximately 20,200 km (12,550 miles)." ([2]).
- Расчёт: a = 26 561,75 км, R = 6 378,137 км. Зенит: (a − R)/c = 0,0673 с. Горизонт: sqrt(a² − R²) = 25 785 км, это 0,0860 с. Диапазон 0,067–0,086 с, меньше 0,1 с. Атмосфера не учтена.

## 5. Три сферы дают две точки, одна в космосе; четвёртый спутник чинит часы приёмника

- В сценарии: "Hear three, and the balls cross in just two spots. One is way out in space. The other one is you. A fourth one fixes your phone's own clock"
- Вердикт: верно. Это учебное упрощение: три дальности при верных часах, четвёртая убирает ошибку часов. «Ball» — точнее, поверхность сферы.
- Источник: [20] ESA Navipedia, «An intuitive approach to the GNSS positioning», 2011, https://gssc.esa.int/navipedia/index.php/An_intuitive_approach_to_the_GNSS_positioning. [19] FAA, «Satellite Navigation - GPS - How It Works», https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/gps/howitworks. [7] N. Ashby, «Relativity in the Global Positioning System», Living Reviews in Relativity 6, 1 (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §1, с. 6.
- Цитата: "For a ground receiver, one of such solutions is on the earth's surface and the other far away in the space." ([20]). "by taking a measurement from a fourth satellite, the receiver avoids the need for an atomic clock" ([19]). "These four equations can be solved for the unknown space-time coordinates {r, t} of the reception event." ([7] §1, с. 6).

## 6. Свет проходит около фута за наносекунду; 1 мкс даёт около 1000 футов

- В сценарии: "In one billionth of a second, it goes about one foot." и "off by just one millionth of a second, your distance to it is off by a thousand feet."
- Вердикт: верно. Перевод (30 см, 300 м) тоже верен.
- Источник: [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §1, с. 6.
- Цитата: "Timing errors of one ns will lead to positioning errors of the order of 30 cm." ([7] §1, с. 6).
- Расчёт: c = 299 792 458 м/с (точно). 1 нс: 0,2998 м = 0,984 ft. 1 мкс: 299,8 м = 984 ft.

## 7. На каждом спутнике атомные часы (рубидиевые и цезиевые)

- В сценарии: "every GPS satellite carries atomic clocks"
- Вердикт: верно. GPS.gov тип часов не называет. Оба типа названы у Ashby.
- Источник: [5] GPS.gov, «GPS and Telling Time», https://www.gps.gov/gps-and-telling-time. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §1 (с. 5), §5 (с. 17). [11] NIST, «Putting Einstein to the Test», 2025, https://www.nist.gov/atomic-clocks/a-powerful-tool-for-science/putting-einstein-test.
- Цитата: "Each GPS satellite contains multiple atomic clocks that contribute very precise time data to the GPS signals." ([5]). "The plot for Cesium, however, characterizes the best orbiting clocks in the GPS system." ([7] §1, с. 5). "It has become common practice not to apply such offsets to Rubidium clocks" ([7] §5, с. 17). "all carry atomic clocks and are subject to the effects of relativity" ([11]).

## 8. Скорость около 8 700 миль/ч (14 000 км/ч), два оборота в сутки

- В сценарии: "about eight thousand seven hundred miles an hour. Twice a day around the whole planet." Перевод: «около 14 тысяч километров в час. Дважды в сутки».
- Вердикт: верно. На gps.gov скорости нет. Она считана и совпадает с Ashby.
- Источник: [2] GPS.gov, «Space Segment», https://www.gps.gov/space-segment. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §9, с. 27. [8] N. Ashby, «Relativity and the Global Positioning System», Physics Today 55(5), 41 (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 41.
- Цитата: "Each satellite circles the Earth twice a day." ([2]). "v = 3.873947951 × 10^3 m s^-1" ([7] §9, с. 27). "all the satellites have periods of 11 hours and 58 minutes" ([8], с. 41).
- Расчёт: GM = 3,986004418e14 м³/с², a = 26 561,75 км. v = sqrt(GM/a) = 3 873,8 м/с = 13 946 км/ч = 8 666 mph. Период 11,967 ч = 11 ч 58 мин.

## 9. Скорость света одинакова для всех; движущиеся часы идут медленнее

- В сценарии: "the speed of light doesn't care how fast you're going. Same speed, longer path. So every tick takes longer. The moving clock runs slow."
- Вердикт: верно. Принцип и замедление есть в статье 1905 года. Часов с двумя зеркалами там нет: это учебная модель. Сценарий не приписывает её Эйнштейну.
- Источник: [14] A. Einstein, «Zur Elektrodynamik bewegter Körper», Annalen der Physik 322(10), 891–921 (1905), DOI 10.1002/andp.19053221004. Цитаты из английского перевода (издание 1923, электронная версия Fourmilab): https://www.fourmilab.ch/etexts/einstein/specrel/www/, §2 и §4. Немецкий оригинал не открыт (Wiley вернул 403).
- Цитата: "Any ray of light moves in the “stationary” system of co-ordinates with the determined velocity c" ([14] §2). "the clock moved from A to B lags behind the other which has remained at B" ([14] §4).

## 10. Скорость −7, высота +45, итого +38 мкс в сутки

- В сценарии: "Speed: minus seven. Height: plus forty-five. ... about thirty-eight millionths of a second."
- Вердикт: верно: −7,21, +45,79, +38,58 мкс/сут.
- Источник: [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §5, с. 16, Eq. (35)–(36). Ashby делит эффекты иначе. Чисел «7» и «45» мкс/сут в его статье нет, их считаем мы из Eq. (28). Числа 7, 45, 38 даёт [11] NIST (2025), https://www.nist.gov/atomic-clocks/a-powerful-tool-for-science/putting-einstein-test.
- Цитата: "= +2.5046 × 10^-10 − 6.9693 × 10^-10 = −4.4647 × 10^-10" ([7] §5, с. 16, Eq. 35). "The negative sign in this result means that the standard clock in orbit is beating too fast" ([7] §5, с. 16). "Combining the two effects, atomic clocks aboard GPS satellites run 38 microseconds per day faster than earthbound clocks." ([11]).
- Расчёт: v²/(2c²) = 0,835e-10, это −7,21 мкс/сут. Φ0/c² − GM/(ac²) = 6,9693e-10 − 1,6697e-10 = 5,2996e-10, это +45,79 мкс/сут. Итог 4,4647e-10 × 86 400 с = 38,58 мкс. Контроль: 3GM/(2ac²) = 2,5046e-10, как у Ashby. Шар без вращения Земли даёт +45,65.

## 11. Опыт NIST 2010: часы подняли примерно на фут, они пошли быстрее

- В сценарии: "In 2010, scientists in Colorado lifted one super-precise clock about a foot higher than another. The higher one ran faster."
- Вердикт: верно с уточнением. В статье часы подняли на 33 см (до этого они стояли на 17 см ниже). Фразу «на фут выше другого» даёт пресс-релиз, не статья.
- Источник: [9] C. W. Chou, D. B. Hume, T. Rosenband, D. J. Wineland, «Optical Clocks and Relativity», Science 329, 1630–1633 (2010), DOI 10.1126/science.1192720, https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905055, с. 1632. [10] NIST, пресс-релиз 2010-09-23, https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal.
- Цитата: "a clock that is higher by a distance ∆h runs faster by" ([9], с. 1632, Eq. 2). "elevated by 33 cm" ([9], с. 1632, подпись к Fig. 3). "a fractional frequency change of (4.1 ± 1.6) × 10^-17" ([9], с. 1632). "the higher clock ran at a slightly faster rate than the lower clock, exactly as predicted" ([10]).
- Расчёт: gΔh/c² при 0,33 м = 3,6e-17. Измерено (4,1 ± 1,6)e-17. Это согласие в пределах погрешности, значимость около 2,6σ.
- Правка: EN: "In 2010, scientists in Colorado raised one super-precise clock by about a foot. The raised clock ran faster." RU: «В 2010 году учёные в Колорадо подняли одни сверхточные часы примерно на 33 сантиметра. Поднятые часы пошли быстрее.»

## 12. Голова и ноги: 1,6 м за 80 лет дают около 0,44 мкс

- В сценарии: "stand for eighty years, and your head ends up almost half a millionth of a second older."
- Вердикт: верно. Посчитано нами.
- Источник: формула — [9] Chou et al. (2010), https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905055, с. 1632, Eq. (2). Контроль — [10] NIST (2010).
- Цитата: "a clock that is higher by a distance ∆h runs faster by" ([9], с. 1632). "adding up to approximately 90 billionths of a second over a 79-year lifetime" ([10], для 33 см).
- Расчёт: δf/f = gΔh/c². Входы: g = 9,80665 м/с², Δh = 1,6 м (наше допущение о росте), c = 299 792 458 м/с, t = 80 × 365,25 × 86 400 = 2,525e9 с. δf/f = 1,746e-16. Умножить на t: 4,41e-7 с = 0,44 мкс. Контроль метода: 0,33 м за 79 лет = 90 нс, как у NIST.

## 13. Орбита выше 12 000 миль

- В сценарии: "They're over twelve thousand miles up" Перевод: «выше 20 тысяч километров».
- Вердикт: верно.
- Источник: [2] GPS.gov, «Space Segment», https://www.gps.gov/space-segment.
- Цитата: "GPS satellites fly in medium Earth orbit (MEO) at an altitude of approximately 20,200 km (12,550 miles)." ([2]).
- Расчёт: a − R = 26 561,75 − 6 378,137 = 20 183,6 км = 12 542 mi.

## 14. 38 мкс света — около 7 миль (11 км)

- В сценарии: "light covers about seven miles in that time" Перевод: «около 11 километров».
- Вердикт: верно. Точнее 11,56 км. У Ashby «more than 11 km».
- Источник: расчёт. Сверка порядка величины: [8] Ashby (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 42.
- Цитата: "satellite clock errors building up in just one day would cause navigational errors of more than 11 km" ([8], с. 42).
- Расчёт: c × 38,575 мкс = 11,56 км = 7,19 mi.

## 15. Частота: 10,23 МГц, на спутнике 10,22999999543 МГц, Δf/f = −4,4647e-10

- В сценарии: EN: "On the satellite, it's set to ten point two two nine nine nine nine nine nine nine five four." Перевод: «10,22999999543 миллиона».
- Вердикт: EN неверно, RU верно. EN содержит семь «nine» и не имеет «three»: это 10,22999999954, а не 10,22999999543. Отклонение выходит 4,5e-11 вместо 4,5e-10. Фраза «меньше половины миллиардной» верна: 0,446 млрд.
- Источник: [6] IS-GPS-200N (2022), https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §3.3.1.1 «Frequency Plan», с. 13–14. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §5, Eq. (36), с. 16. Изменения IRN-IS-200N-003 и -004 этот раздел не затрагивают (поиск по тексту).
- Цитата: "The nominal frequency of this source -- as it appears to an observer on the ground -- is 10.23 MHz." ([6] §3.3.1.1, с. 13). "The clock rates are offset by Δf/f = -4.4647E-10" ([6], с. 14). "This is equal to 10.2299999954326 MHz." ([6], с. 14). "10.229 999 995 43 MHz" ([7], с. 16).
- Расчёт: 10,23e6 × (1 − 4,4647e-10) = 10 229 999,9954 Гц = 10,22999999543 МГц. Δf = −4,5674e-3 Гц. Английская фраза сценария по скрипту читается как 10,22999999954.
- Правка: EN: "On the satellite, it's set to ten point two two nine nine nine nine nine nine five four three." Русский текст не менять.

## 16. Наземная команда сверяет часы и шлёт поправки

- В сценарии: "And the team on the ground still checks every clock and sends small corrections up, all the time."
- Вердикт: верно с уточнением. Контроль идёт постоянно. Загрузка данных в спутник — обычно раз в сутки.
- Источник: [4] GPS.gov, «GPS», https://www.gps.gov/gps. [3] GPS.gov, «Control Segment», https://www.gps.gov/control-segment. [6] IS-GPS-200N, https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §6.3.2, с. 51. [8] Ashby (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 41.
- Цитата: "maintain the satellites in their proper orbits through occasional command maneuvers, and adjust the satellite clocks" ([4]). "Generates navigation messages for upload to the satellites" ([3]). "Under normal conditions the CS will provide daily uploads to each SV" ([6] §6.3.2). "Even so, the system requires frequent uploads of clock corrections to the satellites." ([8], с. 41).
- Правка: EN: "And the team on the ground still checks every clock and sends small corrections up every day." RU: «А команда на земле всё равно сверяет каждые часы и каждый день шлёт наверх мелкие поправки.»

## 17. Проверка 1977 года: спутник NTS-2

- В сценарии: "In 1977, they launched a test satellite with that correction switched off. ... For about three weeks they watched its clock run on its own. It ran fast by four hundred forty-two and a half parts in a trillion. Einstein's prediction: four hundred forty-six and a half. Within one percent. Then they switched the correction on."
- Вердикт: верно с уточнением. Числа 442,5 и 446,5 взяты у Ashby. Первичный отчёт NRL даёт другие: измерено 443,1 (442,5 — до поправки на часы станции Панама), предсказано 445,0. Все пары укладываются в 1 %.
- Источник: [12] R. L. Easton, J. A. Buisson, T. B. McCaskill, «Initial Results of the NAVSTAR GPS NTS-2 Satellite», NRL Report 8232, 25 May 1978, https://apps.dtic.mil/sti/pdfs/ADA058591.pdf, с. 11 (PDF с. 16). Заголовок и авторы совпадают со ссылкой [11] у Ashby (PTTI-9, 1977). Текст PTTI на NTRS без файла: [13] https://ntrs.nasa.gov/citations/19840071638. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §5, с. 16–17. [8] Ashby (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 45.
- Цитата: "Navigation Technology Satellite 2 (NTS-2) was successfully launched on June 23, 1977" ([12], аннотация). "The (T - O) slope gives the frequency offset of +442.5 pp 10^12 with respect to the Panama clock." ([12], с. 11). "Comparison of this value to the predicted value of the relativistic offset of +445.0 pp 10^12 gives a difference of -1.9 pp 10^12." ([12], с. 11). "On day 215, 1977, the NTS-2 PRN-5 output signal was offset (Fig. 16) through the use of a frequency synthesizer" ([12], с. 11). "it was operated for about 20 days to measure its clock rate before turning on the synthesizer" ([7], с. 16). "while general relativity predicted +446.5 parts in 10^12" ([7], с. 17). "This then gave about a 1% verification" ([7], с. 17). "there were some who doubted that relativistic effects were truths that would need to be incorporated" ([7], с. 16).
- Расчёт: Ashby: (446,5 − 442,5)/446,5 = 0,90 %. NRL: (445,0 − 443,1)/445,0 = 0,43 %. 4,4647e-10 = 446,5e-12, то есть число Ashby совпадает с нашим расчётом. NRL: цезиевый стандарт захвачен на сутки 190 (9 июля 1977), синтезатор включён на сутки 215 (3 августа): 25 суток. Ashby: около 20 суток. Physics Today: три недели. «Около трёх недель» подходит.
- Правка: EN: "It ran fast by about four hundred forty-three parts in a trillion. Einstein's prediction: about four hundred forty-five. Within half a percent." RU: «Они спешили примерно на 443 триллионных доли. Предсказание Эйнштейна: около 445. Разница меньше половины процента.» Допустимо оставить числа Ashby (0,9 %), но тогда ссылаться на Ashby, не на отчёт NRL.
- Доступ: DTIC отдал HTTP 403. Отчёт прочитан по копии Wayback (https://web.archive.org/web/20220524222014/https://apps.dtic.mil/sti/pdfs/ADA058591.pdf). Страницу с числами проверил по изображению.

## 18. Эйнштейн умер до запуска первого спутника

- В сценарии: "A guy who died before the first satellite ever launched is keeping your map honest."
- Вердикт: верно.
- Источник: [15] Nobel Prize, «Albert Einstein – Biographical», https://www.nobelprize.org/prizes/physics/1921/einstein/biographical/. Тот же сайт, «Facts»: https://www.nobelprize.org/prizes/physics/1921/einstein/facts/. [16] NASA (J. Uri), «65 Years Ago: Sputnik Ushers in the Space Age», 2022-10-04, https://www.nasa.gov/history/65-years-ago-sputnik-ushers-in-the-space-age/.
- Цитата: "He died on April 18, 1955 at Princeton, New Jersey." ([15]). "On Oct. 4, 1957, the Soviet Union inaugurated the Space Age with the launch of Sputnik, the world’s first artificial satellite." ([16]).
- Расчёт: от 1955-04-18 до 1957-10-04 прошло 900 суток.

## 19. Приложения со статусом GPS показывают спутники по созвездиям

- В сценарии: "open any GPS status app, and look at the satellites your phone hears right now. Find the ones marked GPS."
- Вердикт: верно с уточнением, вторичные источники. Для Android подтверждено. Для iPhone не проверено: страницы Apple не открылись.
- Источник: [23] EUSPA (агентство ЕС по космической программе), «Test your Android device’s satellite navigation performance», архивная страница без даты, https://www.euspa.europa.eu/newsroom-events/news-archive/test-your-android-devices-satellite-navigation-performance. [24] GPSTest, README (перечень GPS, GLONASS, BeiDou, Galileo), https://github.com/barbeau/gpstest. [25] Android Developers, «GnssStatus», https://developer.android.com/reference/android/location/GnssStatus. Первичного источника нет. Основа — документация приложения и системы.
- Цитата: "The application shows four global constellations: GPS (American flag), Galileo (EU flag), GLONASS (Russian flag) and Beidou (Chinese flag)." ([23]). "Constellation type constant for GPS." ([25]).
- Правка (по желанию, пока iPhone не проверен): EN: "Want to see it yourself? Go outside, open any GNSS status app on an Android phone, and look at the satellites your phone hears right now." RU: «Хочешь увидеть сам? Выйди на улицу, открой на Android любое приложение со статусом GNSS и посмотри, какие спутники телефон слышит прямо сейчас.»

## 20. «Лучшие часы, которые люди умеют запускать»

- В сценарии: "That's why every GPS satellite carries atomic clocks, the best clocks people know how to fly."
- Вердикт: неверно как превосходная степень. Часы Deep Space Atomic Clock у NASA в наземных тестах до 50 раз стабильнее часов GPS.
- Источник: [22] NASA, «Five Things to Know about NASA's Deep Space Atomic Clock», https://www.nasa.gov/missions/tech-demonstration/deep-space-atomic-clock/five-things-to-know-about-nasas-deep-space-atomic-clock/. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §1, с. 5.
- Цитата: "In ground tests, the Deep Space Atomic Clock proved to be up to 50 times more stable than the atomic clocks on GPS satellites." ([22]). "it should be correct to within about 5 parts in 10^14, or 4 nanoseconds" ([7] §1, с. 5, цезиевые часы за сутки).
- Расчёт: 5e-14 × 86 400 с = 4,3 нс.
- Правка: EN: "That's why every GPS satellite carries atomic clocks, good to a few billionths of a second a day." RU: «Поэтому на каждом спутнике GPS стоят атомные часы. За сутки они уходят лишь на несколько миллиардных долей секунды.»

## 21. «Перед запуском часы каждого спутника ставят медленнее»

- В сценарии: "Before launch, every satellite clock is set to run a little slow."
- Вердикт: верно с уточнением. Ashby 2002 пишет «every ... before launch». Ashby 2003 уточняет: к рубидиевым часам смещение до запуска обычно не применяют. Его учитывают после запуска в поправках навигационного сообщения. Для пользователя результат тот же.
- Источник: [8] Ashby (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 45. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §5, с. 16–17. [6] IS-GPS-200N, https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §3.3.1.1, с. 13–14.
- Цитата: "Nowadays the rate of every orbiting GPS clock is adjusted by this “factory offset” before launch." ([8], с. 45). "It has become common practice not to apply such offsets to Rubidium clocks" ([7], с. 17). "are offset to compensate for relativistic effects" ([6] §3.3.1.1, с. 13–14, про частоту и ход часов спутника).
- Правка: EN: "Engineers set each satellite clock to run a little slow." RU: «Инженеры ставят часы каждого спутника чуть медленнее.»

## 22. «На орбите они идут точно»

- В сценарии: "In orbit, once Einstein is done with it, it's exactly right."
- Вердикт: верно с уточнением. «Exactly» — преувеличение. Часы уходят, поэтому нужны поправки. Периодический релятивистский член считает приёмник.
- Источник: [6] IS-GPS-200N, https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §20.3.3.3.3.1, с. 97–98. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §5, с. 17.
- Цитата: "Since these coefficients do not include corrections for relativistic effects, the user's equipment must determine the requisite relativistic correction." ([6] §20.3.3.3.3.1). "The navigation message provides satellite clock frequency corrections for users" ([7], с. 17).
- Расчёт: член F·e·√A при e = 0,01 (допущение) равен 22,9 нс, то есть 6,9 м.
- Правка: EN: "In orbit, once Einstein is done with it, it ticks at just the right rate." RU: «На орбите, когда Эйнштейн с ними закончит, они идут с нужной скоростью.»

## 23. «То же самое, только со светом вместо звука»

- В сценарии: "GPS does the same thing, only with light instead of sound."
- Вердикт: верно. GPS использует радиоволны. Они идут со скоростью света. Правка не нужна.
- Источник: [19] FAA, «Satellite Navigation - GPS - How It Works», https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/gps/howitworks. [6] IS-GPS-200N, https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §3.3.1.1, с. 14.
- Цитата: "Satellite Navigation is based on a global network of satellites that transmit radio signals from medium earth orbit." ([19]). "The nominal carrier frequencies (f0) shall be 1575.42 MHz, and 1227.6 MHz for L1 and L2, respectively." ([6], с. 14).

## 24. Без поправки ошибка растёт на 7 миль каждые сутки

- В сценарии: "that's seven miles of mistake. Added every single day."
- Вердикт: верно.
- Источник: [8] Ashby (2002), https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf, с. 42.
- Цитата: "satellite clock errors building up in just one day would cause navigational errors of more than 11 km" ([8], с. 42).
- Расчёт: 38,58 мкс × c = 11,56 км за сутки. За двое суток около 23 км.

## 25. На орбите притяжение Земли намного слабее

- В сценарии: "where Earth's pull is much weaker."
- Вердикт: верно.
- Источник: закон тяготения Ньютона, расчёт наш.
- Расчёт: g(a)/g(R) = (R/a)² = (6 378,137/26 561,75)² = 0,0577, примерно 1/17.

## 26. Ближе к массе часы идут медленнее, выше — быстрее

- В сценарии: "Gravity slows time down. The closer you are to something big and heavy, like the Earth, the slower your clock runs. Go higher, and time speeds up."
- Вердикт: верно.
- Источник: [9] Chou et al. (2010), https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905055, с. 1630. [11] NIST, «Putting Einstein to the Test», 2025, https://www.nist.gov/atomic-clocks/a-powerful-tool-for-science/putting-einstein-test.
- Цитата: "Another consequence of Einstein’s theory is that clocks run more slowly near massive objects." ([9], с. 1630). "The more strongly you feel the force of gravity, Einstein argued, the slower time passes for you." ([11]).

## 27. Часы телефона дешёвые

- В сценарии: "A fourth one fixes your phone's own clock, which, let's be honest, is cheap."
- Вердикт: верно. Источники говорят о кварцевых часах приёмников вообще. Для телефонов отдельно не проверено.
- Источник: [20] ESA Navipedia, «An intuitive approach to the GNSS positioning», 2011, https://gssc.esa.int/navipedia/index.php/An_intuitive_approach_to_the_GNSS_positioning. [7] Ashby (2003), https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf, §1, с. 5.
- Цитата: "quartz-based clocks, much more economical but with a poorer stability" ([20]). "a Quartz oscillator such as is typically found in a GPS receiver" ([7] §1, с. 5).

## 28. Телефону нужны обе идеи Эйнштейна

- В сценарии: "And your phone needs both to find your coffee."
- Вердикт: верно. Основной сдвиг частоты вносят на спутнике. Приёмник сам добавляет периодическую релятивистскую поправку.
- Источник: [6] IS-GPS-200N, https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf, §20.3.3.3.3.1, с. 97–98.
- Цитата: "the user's equipment must determine the requisite relativistic correction" ([6] §20.3.3.3.3.1).

## 29. Конкуренты: minutephysics (2012) и Stand-up Maths (2019)

- В сценарии (раздел «Тема и почему она»): «minutephysics (2012) и Stand-up Maths (2019) уже разбирали GPS и относительность.»
- Вердикт: не подтверждено. Ролики не открывались. Это не текст озвучки.
- Источник: [27] TheTVDB, список выпусков Stand-up Maths за 2019 год (вторичный), https://thetvdb.com/series/standupmaths/seasons/official/2019. Для minutephysics страница-источник не открылась (AGU вернул 403). По выдаче поиска ролик мог выйти в 2011 году.
- Цитата: "Why didn't GPS crash?" ([27], выпуск S2019E12, 12 апреля 2019). Тема ролика по названию неясна, содержание не проверено.
- Правка: сверить названия, годы и темы роликов на YouTube вручную до публикации плана.

## Источники

1. GPS.gov, «GPS Accuracy». https://www.gps.gov/gps-accuracy. Старый адрес из задачи (`/systems/gps/performance/accuracy/`) отдаёт 404: сайт перестроен.
2. GPS.gov, «Space Segment». https://www.gps.gov/space-segment
3. GPS.gov, «Control Segment». https://www.gps.gov/control-segment
4. GPS.gov, «GPS». https://www.gps.gov/gps
5. GPS.gov, «GPS and Telling Time». https://www.gps.gov/gps-and-telling-time
6. IS-GPS-200 Rev N, «NAVSTAR GPS Space Segment/Navigation User Segment Interfaces», 01-AUG-2022 (текущая ревизия на gps.gov). https://www.gps.gov/sites/default/files/2025-07/IS-GPS-200N.pdf. Страница со списком: https://www.gps.gov/interface-control-documents-icds-interface-specifications-iss. IRN проверены поиском по тексту: IRN-IS-200N-003 (27-SEP-2023) https://www.gps.gov/sites/default/files/2025-07/IRN-IS-200N-003.pdf, IRN-IS-200N-004 (16-JUN-2026) https://gps.gov/sites/default/files/2026-09/IRN-IS-200N-004_RFC519_20260616.pdf. Номера страниц — печатные.
7. N. Ashby, «Relativity in the Global Positioning System», Living Reviews in Relativity 6, 1 (2003), открытый доступ. DOI https://doi.org/10.12942/lrr-2003-1. PDF: https://link.springer.com/content/pdf/10.12942/lrr-2003-1.pdf. Сайт livingreviews.org дал ошибку сертификата, не использовался.
8. N. Ashby, «Relativity and the Global Positioning System», Physics Today 55(5), 41–47 (2002), DOI 10.1063/1.1485583. PDF: https://aip.brightspotcdn.com/PTO.v55.i5.41_1.online.pdf
9. C. W. Chou, D. B. Hume, T. Rosenband, D. J. Wineland, «Optical Clocks and Relativity», Science 329, 1630–1633 (2010), DOI 10.1126/science.1192720. PDF на сайте NIST: https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=905055
10. NIST, «NIST Pair of Aluminum Atomic Clocks Reveal Einstein's Relativity at a Personal Scale», 2010-09-23. https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal
11. NIST, «Putting Einstein to the Test», 2025. https://www.nist.gov/atomic-clocks/a-powerful-tool-for-science/putting-einstein-test
12. R. L. Easton, J. A. Buisson, T. B. McCaskill, «Initial Results of the NAVSTAR GPS NTS-2 Satellite», NRL Report 8232, Naval Research Laboratory, 25 May 1978 (DTIC ADA058591). https://apps.dtic.mil/sti/pdfs/ADA058591.pdf. Прочитано по копии: https://web.archive.org/web/20220524222014/https://apps.dtic.mil/sti/pdfs/ADA058591.pdf
13. NASA NTRS, запись «Initial results of the NAVSTAR GPS NTS-2 satellite», PTTI-9 (1978). https://ntrs.nasa.gov/citations/19840071638. Только описание, файла нет.
14. A. Einstein, «Zur Elektrodynamik bewegter Körper», Annalen der Physik 322(10), 891–921 (1905), DOI 10.1002/andp.19053221004 (данные проверены через Crossref, https://api.crossref.org/works/10.1002/andp.19053221004). Английский перевод, издание 1923, электронная версия Fourmilab: https://www.fourmilab.ch/etexts/einstein/specrel/www/
15. Nobel Prize, «Albert Einstein – Biographical». https://www.nobelprize.org/prizes/physics/1921/einstein/biographical/ и «Facts» https://www.nobelprize.org/prizes/physics/1921/einstein/facts/
16. NASA, J. Uri, «65 Years Ago: Sputnik Ushers in the Space Age», 2022-10-04. https://www.nasa.gov/history/65-years-ago-sputnik-ushers-in-the-space-age/
17. National Weather Service, «Understanding Lightning: Thunder». https://www.weather.gov/safety/lightning-science-thunder
18. NASA Glenn Research Center, «Speed of Sound». https://www.grc.nasa.gov/www/k-12/BGP/sound.html
19. FAA, «Satellite Navigation - GPS - How It Works». https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/gps/howitworks
20. ESA Navipedia, «An intuitive approach to the GNSS positioning», 2011. https://gssc.esa.int/navipedia/index.php/An_intuitive_approach_to_the_GNSS_positioning
21. NASA, «GPS». https://www.nasa.gov/directorates/somd/space-communications-navigation-program/gps/. Открыта, в цитатах не использована; подтверждает 20 200 км (12 550 миль) и «redundant atomic clocks».
22. NASA, «Five Things to Know about NASA's Deep Space Atomic Clock». https://www.nasa.gov/missions/tech-demonstration/deep-space-atomic-clock/five-things-to-know-about-nasas-deep-space-atomic-clock/
23. EUSPA, «Test your Android device’s satellite navigation performance» (архив, вторичный). https://www.euspa.europa.eu/newsroom-events/news-archive/test-your-android-devices-satellite-navigation-performance
24. GPSTest, README (вторичный). https://github.com/barbeau/gpstest
25. Android Developers, «GnssStatus» (вторичный). https://developer.android.com/reference/android/location/GnssStatus
26. u-blox, «A-GNSS AssistNow» (вендор, вторичный). https://www.u-blox.com/en/technologies/agnss-assistnow
27. TheTVDB, Stand-up Maths, 2019 (вторичный). https://thetvdb.com/series/standupmaths/seasons/official/2019

Не открылись: Wiley (немецкий оригинал Эйнштейна, 403); DTIC напрямую (403, прочитано через Wayback); AGU blog (403); форумы Apple (проверка браузера); livingreviews.org (ошибка сертификата); старые адреса gps.gov (404). Ролики minutephysics и Stand-up Maths не открывались.

## Расчёты

Запуск: `python3 -I calc.py`. Скрипт лежит вне репозитория (scratchpad), 36 строк.

```python
from math import sqrt, pi
GM, c, a, Re = 3.986004418e14, 299792458.0, 26561750.0, 6378137.0  # SI; a, Re per Ashby 2003
MI, FT, DAY, YR = 1609.344, 0.3048, 86400.0, 365.25 * 86400.0
v = sqrt(GM / a)
print(f"v = {v:.1f} m/s = {v*3.6:.0f} km/h = {v/MI*3600:.0f} mph")
print(f"altitude = {(a-Re)/1e3:.0f} km = {(a-Re)/MI:.0f} mi; period = {2*pi*sqrt(a**3/GM)/3600:.3f} h")
slow = v**2 / (2 * c**2)                      # speed effect, fraction
phi0 = 6.9693e-10                             # Ashby 2003 Eq. 35: geoid potential / c^2 (incl. rotation)
grav = phi0 - GM / (a * c**2)                 # height effect vs geoid clock
grav_sph = GM / c**2 * (1 / Re - 1 / a)       # same, plain sphere of radius Re (no rotation)
net_ashby = 4.4647e-10                        # Ashby 2003 Eq. 35-36
print(f"speed {-slow*DAY*1e6:.2f}, gravity {grav*DAY*1e6:+.2f} (sphere {grav_sph*DAY*1e6:+.2f}) us/day; net {(grav-slow)*DAY*1e6:.2f} us/day")
print(f"net fraction {grav-slow:.4e} (Ashby {net_ashby}); Ashby 3GM/2ac^2 = {1.5*GM/(a*c**2):.4e}; net/day {net_ashby*DAY*1e6:.2f} us")
print(f"10.23 MHz * (1 - {net_ashby}) = {10.23e6*(1-net_ashby):.4f} Hz; offset {-10.23e6*net_ashby*1e3:.4f} mHz")
print(f"light in 38.58 us = {c*net_ashby*DAY/1e3:.2f} km = {c*net_ashby*DAY/MI:.2f} mi")
print(f"light in 1 ns = {c*1e-9/FT:.3f} ft = {c*1e-9*100:.1f} cm; in 1 us = {c*1e-6/FT:.0f} ft = {c*1e-6:.0f} m")
print(f"signal delay: zenith {(a-Re)/c:.4f} s, horizon {sqrt(a**2-Re**2)/c:.4f} s (slant {sqrt(a**2-Re**2)/1e3:.0f} km)")
cs = sqrt(1.4 * 287.05 * 293.15)              # speed of sound, ideal gas, 20 C
print(f"sound {cs:.1f} m/s: 1 mile = {MI/cs:.2f} s, 1 km = {1000/cs:.2f} s")
g = 9.80665
h80 = g * 1.6 / c**2 * 80 * YR
print(f"head vs feet: g*h/c^2 = {g*1.6/c**2:.3e}; over 80 yr = {h80*1e6:.3f} us")
print(f"check NIST: 0.33 m over 79 yr = {g*0.33/c**2*79*YR*1e9:.0f} ns; shift {g*0.33/c**2:.2e} (Chou measured 4.1e-17)")
print(f"gravity at orbit / surface = {(Re/a)**2:.4f} (1/{(a/Re)**2:.1f})")
print(f"NTS-2: Ashby (446.5-442.5)/446.5 = {(446.5-442.5)/446.5*100:.2f} %; NRL (445.0-443.1)/445.0 = {(445.0-443.1)/445.0*100:.2f} %; 4.4647e-10 = {net_ashby*1e12:.1f} pp1e12")
print(f"NTS-2 days: lockup day 190 -> offset day 215 = {215-190} days")
print(f"4.9 m = {4.9/FT:.1f} ft = {4.9/0.75:.1f} steps of 0.75 m")
print(f"Einstein died 1955-04-18, Sputnik 1957-10-04: gap {(__import__('datetime').date(1957,10,4)-__import__('datetime').date(1955,4,18)).days} days")
D = {"two": "2", "nine": "9", "five": "5", "four": "4", "three": "3"}
say = lambda s: "10." + "".join(D[w] for w in s.split())
spec = f"{10.23 * (1 - net_ashby):.11f}"
print(f"spec 10.23*(1-4.4647e-10) = {spec} MHz")
print(f"script EN reads {say('two two nine nine nine nine nine nine nine five four')} -> offset {1 - float(say('two two nine nine nine nine nine nine nine five four'))/10.23:.3e}")
print(f"fixed EN reads  {say('two two nine nine nine nine nine nine five four three')}; script RU 10.22999999543")
F, A, e = 4.442807633e-10, 26559710.0, 0.01  # IS-GPS-200N sec. 20.3.3.3.3.1 (F); A_ref per IRN-IS-200N-003; e is assumed
print(f"periodic term F*e*sqrt(A) for e={e}: {F*e*sqrt(A)*1e9:.1f} ns = {F*e*sqrt(A)*c:.1f} m")
```

Вывод скрипта:

```text
v = 3873.8 m/s = 13946 km/h = 8666 mph
altitude = 20184 km = 12542 mi; period = 11.967 h
speed -7.21, gravity +45.79 (sphere +45.65) us/day; net 38.58 us/day
net fraction 4.4647e-10 (Ashby 4.4647e-10); Ashby 3GM/2ac^2 = 2.5046e-10; net/day 38.58 us
10.23 MHz * (1 - 4.4647e-10) = 10229999.9954 Hz; offset -4.5674 mHz
light in 38.58 us = 11.56 km = 7.19 mi
light in 1 ns = 0.984 ft = 30.0 cm; in 1 us = 984 ft = 300 m
signal delay: zenith 0.0673 s, horizon 0.0860 s (slant 25785 km)
sound 343.2 m/s: 1 mile = 4.69 s, 1 km = 2.91 s
head vs feet: g*h/c^2 = 1.746e-16; over 80 yr = 0.441 us
check NIST: 0.33 m over 79 yr = 90 ns; shift 3.60e-17 (Chou measured 4.1e-17)
gravity at orbit / surface = 0.0577 (1/17.3)
NTS-2: Ashby (446.5-442.5)/446.5 = 0.90 %; NRL (445.0-443.1)/445.0 = 0.43 %; 4.4647e-10 = 446.5 pp1e12
NTS-2 days: lockup day 190 -> offset day 215 = 25 days
4.9 m = 16.1 ft = 6.5 steps of 0.75 m
Einstein died 1955-04-18, Sputnik 1957-10-04: gap 900 days
spec 10.23*(1-4.4647e-10) = 10.22999999543 MHz
script EN reads 10.22999999954 -> offset 4.497e-11
fixed EN reads  10.22999999543; script RU 10.22999999543
periodic term F*e*sqrt(A) for e=0.01: 22.9 ns = 6.9 m
```
