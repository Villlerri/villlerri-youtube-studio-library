---
id: after-effects
name: Adobe After Effects
class: [motion-design, edit-composite]
kind: app
site: https://www.adobe.com/products/aftereffects.html
github: none
scenes: [diagram, mechanism, field, micro, scale, character, typography, map-timeline, real-footage]
quality: 5
human_difficulty: 4
agent_difficulty: 3
automation: 3
reproducibility: 3
cost: 2
maturity: standard
platforms: [windows, macos]
export: [mov, avi, png-sequence, mp4, lottie]
code_license: proprietary
price: US$22.99/мес отдельно (годовой план, оплата помесячно); Creative Cloud Pro US$69.99/мес
checked: 2026-10-14
---

# Adobe After Effects

Отраслевой стандарт motion design: слои, ключевые кадры, выражения, скрипты, камеры, 3D, огромная база плагинов. Студия Kurzgesagt сама называет After Effects основным инструментом анимации своих роликов.

## Ссылки

- Официальный сайт: <https://www.adobe.com/products/aftereffects.html>
- GitHub: открытого кода нет.
- Документация: <https://helpx.adobe.com/after-effects/user-guide.html> (при проверке страницы Adobe Help отвечали 403, см. «Неизвестно»). Скрипты, объектная модель: <https://ae-scripting.docsforadobe.dev/> (поддерживает сообщество, не Adobe).
- Примеры, проверенные 2026-10-14 (ссылки открываются через oEmbed; содержание описано по названию и описанию ролика, ролики целиком не смотрелись):
  - [How to Make a Kurzgesagt Video in 1200 Hours](https://www.youtube.com/watch?v=uFk0mgljtns) — канал Kurzgesagt – In a Nutshell. Студия показывает свой пайплайн. По расшифровке на LingQ (вторичный источник): иллюстрации в Illustrator, анимация в After Effects, эксперименты с Cinema 4D, в среднем 200 иллюстраций, не меньше 1200 часов на ролик.
  - [Motion Graphics with Kurzgesagt – Part 1 (Skillshare)](https://www.skillshare.com/en/classes/Motion-Graphics-with-Kurzgesagt-%E2%80%93-Part-1/631970755) — класс от самой студии. По выдаче поиска: настройка проекта, выражения, трек-маски, анимация по траектории с null-объектами, Trim Paths, time remapping, настройки рендера. Страница на прямой запрос ответила 403, существование подтверждено выдачей поиска.

## Что реально получается

Опора: страница продукта Adobe, класс Kurzgesagt, ролик студии.

- Плоская векторная графика научно-популярного ролика: сотни частей, импортированных из Illustrator и анимированных вручную (ролик студии). Это уровень Kurzgesagt, лучший ориентир для канала.
- Непрерывная сцена. Приёмы из программы класса Kurzgesagt: null-объекты ведут группы слоёв по траектории, time remapping, трек-маски, предкомпозиции. Из них собирается длинный кадр без склеек. Готового примера «один непрерывный кадр на 3 минуты» я не нашёл.
- Рисование линий: Trim Paths назван в программе класса Kurzgesagt. Штрих «рисуется» по форме без ручных кадров.
- 3D и камера: на странице продукта сказано про «настоящее 3D-пространство» и 3D-объекты рядом с 2D. Версия 26.x по выдаче поиска добавила Substance-материалы, глубину резкости в Advanced 3D (26.3), импорт SVG.
- Типографика: текстовые слои, аниматоры текста, шаблоны Adobe.
- Выражения (JavaScript): связывают анимацию друг с другом и с внешними данными (страница продукта). Из них собираются параметрические сцены, например графики по таблице.
- Морфинг формы в ключевых кадрах пути на проверенных источниках отдельно не описан. Это базовая возможность слоёв-форм, но подтверждения со страниц Adobe у меня нет.
- Синхронизация с голосом: ключевые кадры по звуку вручную или выражениями. Готовой привязки к тексту сценария нет. Голос студия берёт из ElevenLabs, времена слов можно положить в JSON и читать выражением или скриптом.

## Слабые стороны

- Подписка без бессрочной версии. Отказ от подписки лишает возможности открыть проект.
- Требования Adobe называют только Windows и macOS. Linux в них нет.
- Проект двоичный (.aep). В git нормально не диффится.
- Рендер роликов длиннее нескольких минут с тяжёлыми эффектами идёт долго. Многокадровый рендер: на форуме Adobe пользователь сообщал, что aerender в 23.4.0 перестал его использовать (вторичный источник, исправлено ли, не проверял).
- Для сборки сцены с нуля скриптами нужно знать объектную модель ExtendScript. Скрипты запускаются внутри приложения. Как гонять их без интерфейса, я не проверял.
- Связь с голосом сценария ручная. Для канала, где десятки сцен в день, нужны шаблоны.

## Сложность

- Для человека (4 из 5): интерфейс огромный, слои, предкомпозиции, выражения. Базу ролика собирают за недели, свободная работа с выражениями и камерой это месяцы. Оценка автора карточки.
- Для агента (3 из 5): агент пишет скрипты `.jsx` (ExtendScript, расширенный JavaScript) и выражения. Объектная модель скриптов, судя по оглавлению руководства сообщества, включает композиции (CompItem), слои (AVLayer) и очередь рендера (RenderQueue). Визуальную проверку кадра агент делает сам, отрендерив кадр. Нужна установленная лицензионная программа. Тонкая настройка анимации (кривые, кадровка, композиция) остаётся за человеком.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): выражения JavaScript на каждом свойстве, скрипты ExtendScript (`.jsx`), которые умеют работать с композициями, слоями и очередью рендера. Рендер из командной строки: `aerender` (путь `Support Files`, ключи `-project`, `-comp`, `-output`, шаблоны рендера). `aerender` по умолчанию запускает новый экземпляр After Effects, ключ `-reuse` использует уже запущенный. Шаблоны: проект с замещаемыми слоями плюс скрипт. Экспорт в Lottie через плагин Bodymovin (см. [Lottie](lottie.md)). Полностью без запущенного приложения собрать сцену нельзя.
- Воспроизводимость (3 из 5): проект `.aep` воспроизводит результат, но он двоичный. Версии плагинов и шрифтов влияют на кадр.

## Платформа и оборудование

- Windows 11 (v24H2) и macOS Sonoma (14) как минимум. 16 ГБ ОЗУ, 8 ГБ места, SSD, экран от 1440x900. Для Intel Mac с дискретной видеокартой AMD нужно 4 ГБ видеопамяти. Данные по выдаче поиска к странице требований Adobe (обновлена 2026-06-17, версии 26.0 и 26.2).
- Процессор Windows: Intel 6-го поколения и новее или AMD Ryzen 1000 и новее, нужна поддержка AVX2.
- Linux и браузерная версия в требованиях Adobe не названы.

## Экспорт

- Очередь рендера: формат по умолчанию «Lossless», в Windows AVI, на Mac QuickTime. Можно выбрать последовательности PNG и JPEG (звук в них не идёт). Страница обучения Adobe.
- Media Encoder даёт H.264 и пресеты под YouTube, при этом работать в After Effects можно параллельно. Страница обучения Adobe.
- Lottie через плагин Bodymovin или плагин LottieFiles (нужен аккаунт LottieFiles). Не поддерживаются: последовательности изображений, видео, звук (README lottie-web).
- ProRes и альфа-канал в очереди рендера: на открытых страницах не проверены.

## Стоимость

Проверено 2026-10-14 по [странице After Effects](https://www.adobe.com/products/aftereffects.html) и [странице планов](https://www.adobe.com/creativecloud/plans.html).

- After Effects отдельно: US$22.99/мес, план «Annual, billed monthly» (год с помесячной оплатой).
- Месячный план без обязательств на страницах не показан. Сторонние обзоры называют US$34.49/мес, из Adobe это не подтверждено.
- Creative Cloud Pro (все приложения): регулярно US$69.99/мес. Для новых подписчиков US$34.99/мес первые 3 месяца, дальше US$69.99.
- Студенты и преподаватели (Creative Cloud Pro): US$19.99/мес первый год, затем US$39.99.
- Команды: After Effects US$37.99/мес за лицензию, Creative Cloud Pro US$99.99/мес за лицензию.
- Пробная версия 7 дней. Отмена в течение 14 дней дает полный возврат.
- Налоги не включены. Цены в долларах США.

## Лицензия и права

- Код или программа: проприетарная, подписка Adobe.
- Результат: по Общим условиям Adobe (раздел 4.2) вы сохраняете права на свой контент, Adobe прав не заявляет. Ограничений на коммерческое использование и монетизацию YouTube в этом разделе нет. Водяного знака нет. Обучение генеративных моделей Adobe на вашем контенте не использует, кроме материалов, отправленных в Adobe Stock (раздел 4.3).
- Ассеты в комплекте: шаблоны, стоковые материалы и шрифты Adobe Fonts имеют отдельные условия, не читал.

## Активность и зрелость

Зрелость: standard. По выдаче поиска к страницам Adobe Help: 26.0 вышла в январе 2026 (3D, Substance, импорт SVG), 26.3 в июне, 26.5 в сентябре 2026. Сами страницы What's New Adobe отдавали 403. Развивает Adobe.

## Когда брать и когда нет

- Брать: канал с уровнем Kurzgesagt, плотные вектор-сцены, длинная непрерывная анимация с камерой, типографика, экспорт в Lottie.
- Брать: если у студии уже есть Creative Cloud (Illustrator, Premiere Pro).
- Не брать: если сцены должны собираться кодом без интерфейса. Тогда [Manim CE](manim-ce.md), [Motion Canvas](motion-canvas.md).
- Не брать: если нужна бесплатная замена. Смотри [DaVinci Resolve](davinci-resolve.md) (Fusion), Cavalry ([карточка](cavalry.md)), Apple Motion на macOS ([карточка](apple-motion.md)).

## Источники

- [Страница After Effects](https://www.adobe.com/products/aftereffects.html) — цена US$22.99/мес, тарифы, пробная версия 7 дней, выражения, слои-формы, 3D, плагины. Проверено 2026-10-14.
- [Планы Creative Cloud](https://www.adobe.com/creativecloud/plans.html) — CC Pro US$69.99, акция, возврат 14 дней, «Annual, billed monthly». Проверено 2026-10-14.
- [Общие условия Adobe](https://www.adobe.com/legal/terms.html) — разделы 4.2 и 4.3: права на контент, обучение генеративных моделей. Проверено 2026-10-14.
- [Adobe Learn: рендер композиции](https://www.adobe.com/learn/after-effects/web/render-video-composition) — Render Queue, Lossless, последовательности PNG/JPEG, Media Encoder, H.264. Проверено 2026-10-14.
- [Automated rendering and network rendering (Adobe Help)](https://helpx.adobe.com/en/after-effects/using/automated-rendering-network-rendering.html) — aerender, `-reuse`. Страница при прямом запросе вернула 403, содержание по выдаче поиска. Проверено 2026-10-14.
- [Системные требования After Effects (Adobe Help)](https://helpx.adobe.com/hu/after-effects/desktop/get-started/technical-requirements/system-requirements.html) — Windows 11 v24H2, macOS 14, 16 ГБ. Содержание по выдаче поиска. Проверено 2026-10-14.
- [What's new in After Effects (Adobe Help)](https://helpx.adobe.com/ae_en/after-effects/desktop/what-s-new/whats-new.html) — версии 26.0, 26.3, 26.5. Страница вернула 403, содержание по выдаче поиска и [CG Channel](https://www.cgchannel.com/2026/01/adobe-releases-after-effects-26-0-with-native-substance-support/). Проверено 2026-10-14.
- [Тема форума Adobe: aerender и Multi-Frame Rendering](https://community.adobe.com/t5/after-effects-discussions/aerender-exe-not-use-quot-multi-frame-rendering-quot/m-p/13866973) — сообщение пользователя о 23.4.0. Содержание по выдаче поиска. Проверено 2026-10-14.
- [Expression basics (Adobe Help)](https://helpx.adobe.com/en/after-effects/using/expression-basics.html) — выражения как JavaScript на свойстве. Содержание по выдаче поиска. Проверено 2026-10-14.
- [After Effects Scripting Guide](https://ae-scripting.docsforadobe.dev/) — ExtendScript, `.jsx`, объектная модель (сообщество). Проверено 2026-10-14.
- [Kurzgesagt: How to Make a Kurzgesagt Video in 1200 Hours](https://www.youtube.com/watch?v=uFk0mgljtns) — первоисточник пайплайна студии. Проверено 2026-10-14.
- [Расшифровка ролика на LingQ](https://www.lingq.com/en/learn-english-online/courses/689474/how-to-make-a-kurzgesagt-video-in-120-4887128/) — вторичный источник: фразы «We make things move in Adobe After Effects», Cinema 4D. Проверено 2026-10-14.
- [Skillshare: Motion Graphics with Kurzgesagt – Part 1](https://www.skillshare.com/en/classes/Motion-Graphics-with-Kurzgesagt-%E2%80%93-Part-1/631970755) — класс студии про After Effects. Страница вернула 403, содержание по выдаче поиска. Проверено 2026-10-14.
- [LottieFiles: плагин для After Effects](https://lottiefiles.com/plugins/after-effects) — экспорт Lottie JSON и dotLottie, нужен аккаунт, бесплатен с ограничениями. Проверено 2026-10-14.
- [lottie-web README](https://github.com/airbnb/lottie-web) — Bodymovin, что не поддерживается. Проверено 2026-10-14.

## Неизвестно

- Страницы Adobe Help (aerender, требования, What's New, выражения) отвечают 403 на прямые запросы. Факты оттуда взяты из выдачи поиска. Номер последней версии 26.5 (сентябрь 2026) не подтверждён прямым открытием.
- Цена месячного плана без обязательств: на страницах Adobe не показана.
- Интервью со студией Kurzgesagt о работе в After Effects не найдено. Первоисточники: её ролик (по расшифровке стороннего сайта) и класс на Skillshare (по выдаче поиска). Ролик целиком я не смотрел.
- Другие научно-популярные каналы, работающие в After Effects, не подтверждены первоисточниками, имён не называю.
- Шаблоны движения (Essential Graphics, `.mogrt`): страницы Adobe не открылись, подтверждения нет.
- Как запустить `.jsx` без интерфейса: не проверено.
- ProRes и альфа-канал в очереди рендера, список форматов Media Encoder: не проверено.
- Условия на шаблоны, шрифты Adobe Fonts и стоковые материалы в роликах: не читал.
- Содержание двух примеров описано по названию и описанию, ролики не просматривались целиком.
