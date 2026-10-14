# Монтаж и композитинг

## Что сюда входит

Программы и библиотеки, которые собирают готовые клипы, кадры и звук в ролик: нелинейные редакторы, узловые композиторы, командные и кодовые сборщики. К классу относятся склейка, переходы, слои с прозрачностью, титры, ретайм и кодирование для YouTube. Графику здесь не создают, а склеивают и накладывают. Карточки класса: 13. Дата проверки всех сведений: 2026-10-14.

## Когда этот класс нужен

- Финальная сборка ролика: кадры или клипы плюс озвучка, кодирование под YouTube.
- Склейка сцен, сделанных в других классах (2D-код, 3D, whiteboard), в одну дорожку с переходами.
- Слои и прозрачность: графика поверх живой съёмки или записи экрана, титры, маски.
- Привязка графики к движущемуся предмету: трекинг, выделение объекта.
- Чистка записи диктора или экрана: паузы, слова-паразиты, субтитры.
- Показ реальной съёмки с графикой поверх (`real-footage`), записей экрана (`screen`), заголовков (`typography`).

## Основные решения

- [DaVinci Resolve](../tools/davinci-resolve.md) — монтаж и Fusion (3D, частицы, трекинг) бесплатно, Studio $295 нужна для внешнего скриптинга. Главный универсальный выбор.
- [Adobe Premiere](../tools/premiere-pro.md) — монтаж по тексту и Morph Cut, подписка US$22.99 в месяц, расширения только внутри приложения.
- [Final Cut Pro](../tools/final-cut-pro.md) — быстрый монтаж на Mac, $299.99 разово или Creator Studio $12.99 в месяц; автоматизация через FCPXML.
- [Kdenlive](../tools/kdenlive.md) — бесплатный редактор на MLT для Linux, ключевые кадры, Lottie; нет скриптового API.
- [Shotcut](../tools/shotcut.md) — бесплатный простой редактор на MLT, шторки и ключевые кадры у фильтров.
- [Natron](../tools/natron.md) — свободный узловой композитор; стабильный выпуск 2022 года, развитие почти остановилось.
- [Nuke](../tools/nuke.md) — отраслевой композитор для VFX, от €3,139 в год; для объясняющих роликов избыточен.
- [FFmpeg](../tools/ffmpeg.md) — командная строка для склейки кадров, переходов `xfade` и кодирования под YouTube; опора пайплайна агента.
- [Editly](../tools/editly.md) — монтаж из JSON-описания через FFmpeg, переходы gl-transitions, MIT; последний стабильный релиз 0.14.2 от 2022 года, кандидат 0.15.0-rc.1 от 2025-01, один автор: годится для шаблонных склеек, для новых проектов рискованно.
- [OpenTimelineIO](../tools/opentimelineio.md) — формат и Python API обмена монтажной информацией между редакторами (Apache-2.0, проект ASWF); не монтирует и не рендерит, поддержку в программах заявляют сами разработчики.
- [MoviePy](../tools/moviepy.md) — Python-библиотека: клип задаётся функцией кадра; версия 2 несовместима с 1.
- [auto-editor](../tools/auto-editor.md) — вырезает паузы из записи, экспортирует таймлайн в редакторы; режет резко.
- [Descript](../tools/descript.md) — облачный монтаж по тексту с API; голосовые функции студия не использует.

Смежные карточки других классов:

- [After Effects](../tools/after-effects.md) — композитинг и анимация Adobe, подробности в карточке.
- [Blender](../tools/blender.md) — Video Sequencer (монтаж) и компоновщик (композитинг) внутри 3D-пакета.
- [OBS Studio](../tools/obs-studio.md) — захват экрана и камеры, подробности в карточке.

## Сравнение

### Потолок качества

- 5: [DaVinci Resolve](../tools/davinci-resolve.md) (Fusion: 3D-камеры, частицы, трекинг, Text+) и [Nuke](../tools/nuke.md) (глубокий композитинг, 3D на USD, гауссовы сплаты).
- 4: [Adobe Premiere](../tools/premiere-pro.md) и [Final Cut Pro](../tools/final-cut-pro.md): аккуратный монтаж, маски объектов (Object Mask, Magnetic Mask).
- 3: [Kdenlive](../tools/kdenlive.md), [Shotcut](../tools/shotcut.md), [Natron](../tools/natron.md), [FFmpeg](../tools/ffmpeg.md), [MoviePy](../tools/moviepy.md), [Editly](../tools/editly.md): склейка, слои, переходы по заранее готовой графике. [OpenTimelineIO](../tools/opentimelineio.md) (3) сама ролик не собирает, оценка за точность переноса монтажа.
- 2: [Descript](../tools/descript.md) и [auto-editor](../tools/auto-editor.md): нарезка и чистка записи, не графика.

### Трудность для человека

- 1: [Descript](../tools/descript.md) (правка текста), [auto-editor](../tools/auto-editor.md) (одна команда).
- 2: [Final Cut Pro](../tools/final-cut-pro.md), [Kdenlive](../tools/kdenlive.md), [Shotcut](../tools/shotcut.md), [MoviePy](../tools/moviepy.md) (нужен Python), [Editly](../tools/editly.md) (JSON и Node.js).
- 3: [Adobe Premiere](../tools/premiere-pro.md), [FFmpeg](../tools/ffmpeg.md) (фильтрграфы), [OpenTimelineIO](../tools/opentimelineio.md) (Python и адаптеры).
- 4: [DaVinci Resolve](../tools/davinci-resolve.md) (Fusion), [Natron](../tools/natron.md).
- 5: [Nuke](../tools/nuke.md).

### Трудность для агента

- 1: [FFmpeg](../tools/ffmpeg.md), [auto-editor](../tools/auto-editor.md), [Editly](../tools/editly.md) и [OpenTimelineIO](../tools/opentimelineio.md) (последняя только переносит монтаж): всё из командной строки или кода, результат проверяется без интерфейса.
- 2: [MoviePy](../tools/moviepy.md): код на Python, но много устаревших примеров версии 1.
- 3: [DaVinci Resolve](../tools/davinci-resolve.md) (внешний API только в Studio), [Natron](../tools/natron.md) (Python и запуск без интерфейса), [Nuke](../tools/nuke.md) (Python, коммерческая лицензия), [Descript](../tools/descript.md) (HTTP API и MCP, скачивание через публикацию).
- 4: [Adobe Premiere](../tools/premiere-pro.md) (расширение UXP внутри приложения), [Final Cut Pro](../tools/final-cut-pro.md) (FCPXML, рендер руками), [Kdenlive](../tools/kdenlive.md) и [Shotcut](../tools/shotcut.md) (нет API, есть MLT XML и `melt`).

### Автоматизация

- 5: [FFmpeg](../tools/ffmpeg.md), [MoviePy](../tools/moviepy.md), [auto-editor](../tools/auto-editor.md), [Editly](../tools/editly.md), [OpenTimelineIO](../tools/opentimelineio.md): пакетная работа из кода и командной строки, команды лежат под git.
- 4: [Natron](../tools/natron.md) (XML-проект, Python, запуск без интерфейса), [Nuke](../tools/nuke.md) (Python, Nuke Render для фермы).
- 3: [DaVinci Resolve](../tools/davinci-resolve.md) (Python и Lua, режим `-nogui`, внешний доступ только в Studio), [Descript](../tools/descript.md) (облачный API).
- 2: [Adobe Premiere](../tools/premiere-pro.md), [Final Cut Pro](../tools/final-cut-pro.md), [Kdenlive](../tools/kdenlive.md), [Shotcut](../tools/shotcut.md): ручной интерфейс, автоматизация через файлы обмена.

### Стоимость

- Бесплатно: [FFmpeg](../tools/ffmpeg.md), [MoviePy](../tools/moviepy.md), [auto-editor](../tools/auto-editor.md), [Editly](../tools/editly.md), [OpenTimelineIO](../tools/opentimelineio.md), [Kdenlive](../tools/kdenlive.md), [Shotcut](../tools/shotcut.md), [Natron](../tools/natron.md); у [DaVinci Resolve](../tools/davinci-resolve.md) есть бесплатная версия (Studio $295 разово).
- Низкая: [Descript](../tools/descript.md) от $16 в месяц при оплате за год.
- До $100 в месяц или разово до $500: [Adobe Premiere](../tools/premiere-pro.md) US$22.99 в месяц; [Final Cut Pro](../tools/final-cut-pro.md) $299.99 разово или $12.99 в месяц в Creator Studio.
- Высокая: [Nuke](../tools/nuke.md) €3,139 в год (Indie €449 в год с ограничениями, Non-commercial бесплатно только для некоммерческого использования).

### Плавность переходов и непрерывность сцены

Монтаж и композитинг соединяют готовые кадры, новых состояний сцены не создают. Непрерывность объектов внутри сцены закладывается при создании кадров. Воспринимаемую непрерывность монтажной последовательности монтаж создаёт сам: склейка по движению или форме, сохранение направления, звуковой мост ([раздел о качестве](../craft.md#непрерывность-сцены-и-бесшовные-переходы)). Что дают монтаж и композитинг:

- Match cut (склейка по совпадению): два плана, у которых совпадают композиция, форма, цвет или движение ([Wikipedia: Match cut](https://en.wikipedia.org/wiki/Match_cut), вторичный источник). Склейка выглядит «бесшовной». Вывод автора: монтажёр может сделать match cut только если в исходных кадрах объект уже стоит в том же месте, того же размера, с тем же направлением движения. Это решается при создании кадров. Любой редактор подходит, особых инструментов нет.
- Morph Cut ([Adobe Premiere](../tools/premiere-pro.md)): сглаживает скачок в интервью. Adobe называет условия: один говорящий, неподвижная камера, статичный фон ([Adobe, 2015](https://blog.adobe.com/en/publish/2015/06/18/morph-cut-tips-tricks-for-best-results)). К рисованной графике не относится.
- Оптический поток и интерполяция кадров: ретайм Resolve с Optical Flow, Speed Warp только в Studio ([страница Edit](https://www.blackmagicdesign.com/products/davinciresolve/edit)); в [FFmpeg](../tools/ffmpeg.md) фильтр `minterpolate` с компенсацией движения. Артефакты чаще при быстром движении и больших промежутках между кадрами ([Wikipedia: Motion interpolation](https://en.wikipedia.org/wiki/Motion_interpolation), вторичный источник). Документация FFmpeg: при смене сцены векторы движения случайны. Вывод автора: интерполяция даёт промежуточные кадры между близкими кадрами, а не плавный переход между двумя разными картинками.
- Размытие движения: Resolve 21 добавил Motion Deblur ([что нового](https://www.blackmagicdesign.com/products/davinciresolve/whatsnew)), по названию он убирает размытие, а не добавляет (описание функции не читал). В [FFmpeg](../tools/ffmpeg.md) `tmix` смешивает соседние кадры. Вывод автора: усреднение кадров имитирует размытие, если исходных кадров достаточно много.
- Сохранение объекта между кадрами: выделение и трекинг объекта без хромакея (Magnetic Mask в [Final Cut Pro](../tools/final-cut-pro.md), Object Masking в [Adobe Premiere](../tools/premiere-pro.md), изоляция и трекинг объектов в Studio-версии [DaVinci Resolve](../tools/davinci-resolve.md), планарный трекинг в Fusion, ротоскопия в [Natron](../tools/natron.md)). Слои с прозрачностью: Fusion, Natron, Nuke, `CompositeVideoClip` в [MoviePy](../tools/moviepy.md), клипы с альфа-каналом в [Shotcut](../tools/shotcut.md).
- Движение камеры: 3D-камера в Fusion ([страница Fusion](https://www.blackmagicdesign.com/products/davinciresolve/fusion)) и 3D-система Nuke. В остальных редакторах только масштаб и сдвиг ключевыми кадрами.
- Чего монтаж не исправит (вывод автора, опора на сведения выше): если соседние кадры нарисованы независимо (объект сменил положение, масштаб или стиль), растворение, шторка или интерполяция покажут призрак или скачок. Покадровая смена крупности одного и того же рисунка (`zoompan` в FFmpeg, ключевые кадры масштаба в любом редакторе) воспроизводит приём, который раздражал зрителей прошлых роликов. Непрерывность должна быть заложена в сцену: общий источник кадров, объект на отдельном слое, камера как движение, а не склейка.

## Другие решения

- [Avid Media Composer](https://www.avid.com/media-composer) — коммерческий монтажник для кино и ТВ. Страница Avid при загрузке вернула 403; бесплатная Media Composer First и цены известны только по поисковой выдаче и сторонним обзорам, не проверены.
- [VEGAS Pro](https://www.vegascreativesoftware.com/us/vegas-pro/) — коммерческий монтажник с бесплатной пробой. Цена, версия и платформы на открытых страницах не показаны.
- [OpenShot](https://www.openshot.org/) — свободный (GPLv3) монтажник для Linux, Mac и Windows, ключевые кадры, версия 4.0.1 от 27 сентября 2026.
- [Olive](https://olivevideoeditor.org/) — свободный редактор (GPL-3.0). На сайте «Olive will return», загрузки недоступны. README на GitHub: альфа-версия, «крайне нестабилен». Не брать.
- [Blender Video Sequencer](https://docs.blender.org/manual/en/latest/video_editing/index.html) — встроенный монтаж Blender (руководство 5.2 LTS). Подробнее в карточке [Blender](../tools/blender.md).
- [CapCut](https://www.capcut.com/clause/terms-of-service) — редактор ByteDance. Права на ваш контент остаются у вас, но CapCut получает бессрочную, сублицензируемую лицензию. По Материальной лицензии CapCut обычные шаблоны и стандартные звуки только для личного некоммерческого использования, коммерческие материалы помечены отдельно, повторная правка экспортированного ролика требует повторной оплаты материалов ([Materials License Agreement](https://www.capcut.com/clause/materials-license-agreement)). Для коммерческого канала опасен без чтения условий.
- [LosslessCut](https://github.com/mifi/lossless-cut) — GUI поверх FFmpeg для резки и склейки без перекодирования, GPL-2.0.
- [Flowblade](https://github.com/jliljebl/flowblade) — GPL-3.0, редактор для Linux, версия 2.24 (декабрь 2025).
- [Fusion Studio](https://www.blackmagicdesign.com/products/fusion) — отдельный Fusion от Blackmagic, $295, активируется лицензией DaVinci Resolve.
- [MLT и melt](https://www.mltframework.org/) — движок Kdenlive и Shotcut и командная программа `melt`, LGPL-2.1, версия 7.42.0 от 3 октября 2026. Хороший кандидат на карточку.
- [Pitivi](https://www.pitivi.org/) — свободный редактор для Linux, последний выпуск на сайте 2023.03 от 12 августа 2023.

## Вывод для объясняющих видео

Финальную сборку и кодирование под YouTube брать на [FFmpeg](../tools/ffmpeg.md), а для сценариев на Python добавлять [MoviePy](../tools/moviepy.md) версии 2: агент делает это кодом и сам проверяет рендер. Для композитинга с камерой, слоями и трекингом брать Fusion в [DaVinci Resolve](../tools/davinci-resolve.md): бесплатная версия закрывает ручную работу, Studio за $295 нужна, если агент должен собирать проект через внешний API. Монтаж не лечит дёрганые переходы и повтор одного кадра в разной крупности: непрерывность закладывается в исходные кадры, слои и движение камеры, а редактор лишь склеивает. [Descript](../tools/descript.md) и [auto-editor](../tools/auto-editor.md) годятся для чистки сырых записей, но не для финального монтажа, голос студия получает только из ElevenLabs. [Natron](../tools/natron.md) и [Nuke](../tools/nuke.md) брать лишь при особой причине: у первого почти нет развития, второй дорог и избыточен. [OpenTimelineIO](../tools/opentimelineio.md) нужен только когда монтаж переходит между редакторами (точность переноса переходов и эффектов проверяйте на пилоте). [Editly](../tools/editly.md) годится для шаблонных склеек по JSON, но стабильный релиз 2022 года и один автор: для нового канала надёжнее [FFmpeg](../tools/ffmpeg.md). CapCut для коммерческого канала не брать, пока не прочитаны условия материалов.

## Источники

- [Wikipedia: Match cut](https://en.wikipedia.org/wiki/Match_cut) — определение match cut, графическое совпадение, «бесшовный» эффект. Вторичный источник. Проверено 2026-10-14.
- [Wikipedia: Motion interpolation](https://en.wikipedia.org/wiki/Motion_interpolation) — артефакты интерполяции кадров. Вторичный источник. Проверено 2026-10-14.
- [Adobe: Morph Cut, советы](https://blog.adobe.com/en/publish/2015/06/18/morph-cut-tips-tricks-for-best-results) — условия работы Morph Cut. Проверено 2026-10-14.
- [Документация фильтров FFmpeg](https://ffmpeg.org/ffmpeg-filters.html) — `xfade`, `minterpolate`, `tmix`, `zoompan`. Проверено 2026-10-14.
- [Blackmagic: Edit](https://www.blackmagicdesign.com/products/davinciresolve/edit) — Optical Flow и Speed Warp. Проверено 2026-10-14.
- [Blackmagic: что нового в 21](https://www.blackmagicdesign.com/products/davinciresolve/whatsnew) — Motion Deblur. Проверено 2026-10-14.
- [Blackmagic: Fusion](https://www.blackmagicdesign.com/products/davinciresolve/fusion) — 3D, трекинг. Проверено 2026-10-14.
- [Страница Final Cut Pro](https://www.apple.com/final-cut-pro/) — Magnetic Mask, цены. Проверено 2026-10-14.
- [Объявление Premiere 26.3](https://community.adobe.com/announcements-727/what-s-new-in-adobe-premiere-26-3-june-2026-1628369/index2.html) — Object Masking. Проверено 2026-10-14.
- [CapCut: условия использования](https://www.capcut.com/clause/terms-of-service) — права на контент, лицензия CapCut, Pro. Проверено 2026-10-14.
- [CapCut: Materials License Agreement](https://www.capcut.com/clause/materials-license-agreement) — коммерческое использование материалов. Проверено 2026-10-14.
- [OpenShot](https://www.openshot.org/) и [блог OpenShot](https://www.openshot.org/blog/) — GPLv3, версия 4.0.1 от 27 сентября 2026. Проверено 2026-10-14.
- [Olive на сайте](https://olivevideoeditor.org/) и [GitHub](https://github.com/olive-editor/olive) — «Olive will return», альфа, GPL-3.0. Проверено 2026-10-14.
- [VEGAS Pro](https://www.vegascreativesoftware.com/us/vegas-pro/) — бесплатная проба, цена не показана. Проверено 2026-10-14.
- [Blender: Video Editing](https://docs.blender.org/manual/en/latest/video_editing/index.html) — раздел руководства 5.2 LTS. Проверено 2026-10-14.
- [LosslessCut](https://github.com/mifi/lossless-cut) — назначение, GPL-2.0. Проверено 2026-10-14.
- [Flowblade](https://github.com/jliljebl/flowblade) — GPL-3.0, Linux, 2.24. Проверено 2026-10-14.
- [Fusion Studio](https://www.blackmagicdesign.com/products/fusion) — $295, лицензия Resolve. Проверено 2026-10-14.
- [MLT](https://www.mltframework.org/) — версия 7.42.0 от 3 октября 2026. Проверено 2026-10-14.
- [Pitivi](https://www.pitivi.org/) — выпуск 2023.03. Проверено 2026-10-14.
- [Avid Media Composer](https://www.avid.com/media-composer) — страница не открылась (403); сведения о бесплатной версии и ценах из поисковой выдачи сторонних обзоров, не проверены.
