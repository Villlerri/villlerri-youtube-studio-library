# Покадровая, векторная и скелетная анимация

## Что сюда входит

Программы, где аниматор рисует кадры или двигает нарисованного персонажа: покадровая рисованная анимация, векторная анимация с твинингом, кукольная (cut-out) и скелетная анимация на костях. Результат зависит от рук и вкуса аниматора, а не от формулы. Это единственный класс библиотеки, который даёт настоящую рисованную игру персонажа.

Ролик собирают из рендеров этих программ в монтаже ([davinci-resolve](../tools/davinci-resolve.md), [kdenlive](../tools/kdenlive.md)) или в композитинге ([after-effects](../tools/after-effects.md)). Дальше от класса стоят три инструмента из соседних классов. [Blender Grease Pencil](../tools/blender-grease-pencil.md) рисует штрихи в 3D-сцене с камерой. [After Effects](../tools/after-effects.md) собирает слои и двигает камеру. [Glaxnimate](../tools/glaxnimate.md) — простой бесплатный редактор векторной анимации с выводом в Lottie.

## Когда этот класс нужен

- Персонаж-проводник или собеседник, который говорит под озвучку и играет эмоцию.
- Рукотворный стиль: линия с характером, «бурлящий» контур, бумажная фактура.
- Рисованные переходы: превращение одного нарисованного объекта в другой за несколько кадров, смазывание движения (smear), растяжение и сжатие.
- Метафоры и юмор: оживший атом, механизм-герой, эмоции предмета.
- Серия роликов с одним героем: один раз нарисовали и собрали риг, потом используют во многих сценах.
- Рисование «вживую» от руки, когда нужна именно рукописная нестабильность ([krita](../tools/krita.md), [procreate-dreams](../tools/procreate-dreams.md)). Для чистого «рисуется на глазах» чаще хватает кода, см. ниже.

## Основные решения

- [rive](../tools/rive.md) — векторные сцены, кости, сетки, Trim Path; сцена пишется текстом RML, CLI и агент проверяют кадры; видео только через облачный рендер платного тарифа. Лучший старт для агента.
- [adobe-animate](../tools/adobe-animate.md) — классика мультяшных объясняющих роликов (твины, кости, камера), но по FAQ Adobe (обновлён 2026-06-08) в режиме поддержки без новых функций.
- [toon-boom-harmony](../tools/toon-boom-harmony.md) — студийный стандарт: рисованная анимация, куклы, мультиплан-камера, узлы; самый сильный набор и самый высокий порог входа.
- [moho](../tools/moho.md) — векторные кости и умные кости за разовую плату; Lua-скрипты; Windows и macOS.
- [opentoonz](../tools/opentoonz.md) — бесплатный студийный пакет Toonz; мощный, но тяжёлый интерфейс и редкие выпуски.
- [tahoma2d](../tools/tahoma2d.md) — форк OpenToonz с простым интерфейсом, липсинком Rhubarb, MP4 из коробки; ежемесячные выпуски.
- [krita](../tools/krita.md) — бесплатная рисовалка с покадровой растровой анимацией; для рукописных вставок и записи процесса рисования.
- [synfig](../tools/synfig.md) — бесплатный векторный твининг и кости, проект в XML, рендер из командной строки; ветка 1.5 числится «development».
- [spine](../tools/spine.md) — игровая скелетная анимация: один риг, много движений; видео AVI и MOV; порог дохода $500 000 для обычных лицензий.
- [pencil2d](../tools/pencil2d.md) — самая простая рисовалка кадров; для набросков и аниматика.
- [tvpaint](../tools/tvpaint.md) — растровая «бумажная» анимация высшего класса; дорого и вручную.
- [clip-studio-paint](../tools/clip-studio-paint.md) — рисовалка с ячейками, векторными слоями и камерой по кривой; анимация длиннее 24 кадров (3 секунды при 8 кадрах в секунду) только в редакции EX ($76.99 в год или $277 разово); нет командной строки.
- [cascadeur](../tools/cascadeur.md) — 3D-анимация персонажа с физикой, автопозой и межкадрием; Free без коммерции, Indie $96 в год; рендера ролика нет, анимация уходит в Blender или Unreal.
- [procreate-dreams](../tools/procreate-dreams.md) — iPad, $12,99 единоразово; быстрые рисованные вставки.
- [cartoon-animator](../tools/cartoon-animator.md) — быстрые кукольные говорящие персонажи с липсинком; Windows, $149.

## Сравнение

Оценки взяты из карточек. Шкалы в [методике](../method.md).

### Потолок качества

- Уровень 5: [tvpaint](../tools/tvpaint.md) (живая растровая рисованная анимация) и [toon-boom-harmony](../tools/toon-boom-harmony.md) (рисованная и кукольная в одном проекте).
- Уровень 4: [rive](../tools/rive.md), [adobe-animate](../tools/adobe-animate.md), [moho](../tools/moho.md), [opentoonz](../tools/opentoonz.md), [tahoma2d](../tools/tahoma2d.md), [spine](../tools/spine.md), [clip-studio-paint](../tools/clip-studio-paint.md) (кисти и линия), [cascadeur](../tools/cascadeur.md) (физика 3D-персонажа). Хороший результат даёт опытный аниматор.
- Уровень 3: [krita](../tools/krita.md), [synfig](../tools/synfig.md), [procreate-dreams](../tools/procreate-dreams.md), [cartoon-animator](../tools/cartoon-animator.md). Аккуратная учебная графика.
- Уровень 2: [pencil2d](../tools/pencil2d.md).

### Трудность для человека

- Легко (1–2): [pencil2d](../tools/pencil2d.md), [krita](../tools/krita.md), [procreate-dreams](../tools/procreate-dreams.md), [cartoon-animator](../tools/cartoon-animator.md). Простота инструмента не заменяет умения рисовать.
- Средне (3): [rive](../tools/rive.md), [adobe-animate](../tools/adobe-animate.md), [moho](../tools/moho.md), [tahoma2d](../tools/tahoma2d.md), [synfig](../tools/synfig.md), [spine](../tools/spine.md), [clip-studio-paint](../tools/clip-studio-paint.md), [cascadeur](../tools/cascadeur.md).
- Тяжело (4–5): [opentoonz](../tools/opentoonz.md), [tvpaint](../tools/tvpaint.md) — 4; [toon-boom-harmony](../tools/toon-boom-harmony.md) — 5.

### Трудность для агента

- Лучше всего [rive](../tools/rive.md) (2): текстовая сцена RML, проект с `AGENTS.md`, проверка и скриншот кадра. Видео-рендер руками.
- [synfig](../tools/synfig.md) (3): проект — XML, рендер из командной строки; позы и дизайн агенту трудно задать вслепую.
- Графический интерфейс, агент помогает только по краям (4): [adobe-animate](../tools/adobe-animate.md), [toon-boom-harmony](../tools/toon-boom-harmony.md), [moho](../tools/moho.md), [opentoonz](../tools/opentoonz.md), [tahoma2d](../tools/tahoma2d.md), [krita](../tools/krita.md), [spine](../tools/spine.md), [pencil2d](../tools/pencil2d.md), [cartoon-animator](../tools/cartoon-animator.md), [cascadeur](../tools/cascadeur.md) (внутри Python-скрипты, но командной строки нет).
- Только руками (5): [tvpaint](../tools/tvpaint.md), [procreate-dreams](../tools/procreate-dreams.md), [clip-studio-paint](../tools/clip-studio-paint.md).

### Автоматизация

- Сильнее всего [rive](../tools/rive.md) и [synfig](../tools/synfig.md) (4): консоль, текстовый проект.
- Скрипты и пакетный экспорт (3): [toon-boom-harmony](../tools/toon-boom-harmony.md) (JavaScript, режим без окна), [moho](../tools/moho.md) (Lua), [opentoonz](../tools/opentoonz.md) (ToonzScript, очередь рендера), [tahoma2d](../tools/tahoma2d.md) (наследует OpenToonz, не проверено), [krita](../tools/krita.md) (Python), [spine](../tools/spine.md) (консольный экспорт).
- Слабая (1–2): [adobe-animate](../tools/adobe-animate.md), [tvpaint](../tools/tvpaint.md), [pencil2d](../tools/pencil2d.md) (консольный экспорт готового), [procreate-dreams](../tools/procreate-dreams.md), [cartoon-animator](../tools/cartoon-animator.md), [clip-studio-paint](../tools/clip-studio-paint.md) (записанные цепочки команд Auto Actions, ни API, ни командной строки), [cascadeur](../tools/cascadeur.md) (скрипты внутри программы).

### Стоимость

- Бесплатно: [opentoonz](../tools/opentoonz.md), [tahoma2d](../tools/tahoma2d.md), [krita](../tools/krita.md), [synfig](../tools/synfig.md), [pencil2d](../tools/pencil2d.md); коммерческое использование разрешено.
- До $20 в месяц или до $100 разово: [rive](../tools/rive.md) (видео с $9 в месяц), [procreate-dreams](../tools/procreate-dreams.md) ($12,99), Moho Debut ($59,99, см. [moho](../tools/moho.md)), [clip-studio-paint](../tools/clip-studio-paint.md) (PRO $26.99 в год, EX $76.99 в год без скидки; бессрочно PRO $63, EX $277), [cascadeur](../tools/cascadeur.md) (Free без коммерции; Indie $96 в год при выручке до $100 тыс., Pro $396 в год).
- $20–100 в месяц или до $500 разово: [adobe-animate](../tools/adobe-animate.md) ($22,99 в месяц), [toon-boom-harmony](../tools/toon-boom-harmony.md) (Essentials и Advanced; Premium дороже), [moho](../tools/moho.md) Pro ($399,99), [spine](../tools/spine.md) Professional ($379 сейчас), [cartoon-animator](../tools/cartoon-animator.md) ($149).
- Дороже: [tvpaint](../tools/tvpaint.md) (от €650 разово).

### Плавность переходов и непрерывность сцены

- Лучшие средства непрерывной сцены: [toon-boom-harmony](../tools/toon-boom-harmony.md) (мультиплан-камера, узловой композитинг), [adobe-animate](../tools/adobe-animate.md) (символы, камера, shape tween), [rive](../tools/rive.md) (одна анимация со state machines, обрезка пути), [synfig](../tools/synfig.md) (векторный твининг форм и слои).
- Кости дают мягкое непрерывное движение одного героя: [moho](../tools/moho.md), [spine](../tools/spine.md), [cartoon-animator](../tools/cartoon-animator.md), [rive](../tools/rive.md). Своей сцены и камеры у [spine](../tools/spine.md) нет.
- Чисто покадровые программы ([tvpaint](../tools/tvpaint.md), [tahoma2d](../tools/tahoma2d.md), [opentoonz](../tools/opentoonz.md), [krita](../tools/krita.md), [pencil2d](../tools/pencil2d.md), [procreate-dreams](../tools/procreate-dreams.md)) гладкость отдают аниматору. Камеры с глубиной в них нет или она проверена слабо.
- [clip-studio-paint](../tools/clip-studio-paint.md): ячейки и таймлайн, камера по кривой над рисунком, но не 3D; сцена длиннее 3 секунд только в EX. [cascadeur](../tools/cascadeur.md): физика и инерция дают мягкое движение одного 3D-персонажа, камера есть, рендер ролика нужен в другой программе.
- Бесшовный проезд камеры по «миру» лучше строить в [after-effects](../tools/after-effects.md) или [blender-grease-pencil](../tools/blender-grease-pencil.md), а рисованные элементы приносить слоями.

### Цена по времени аниматора

Оценка автора обзора, порядок величин, в источниках не подтверждена. Проверять на пилотной сцене.

- Полностью рисованная сцена (около 12 рисунков в секунду, [tvpaint](../tools/tvpaint.md), [tahoma2d](../tools/tahoma2d.md), [toon-boom-harmony](../tools/toon-boom-harmony.md)): порядка 1–3 секунд готового материала в день одного аниматора; минута ролика — недели работы.
- Кукольная сцена на готовом риге ([moho](../tools/moho.md), [spine](../tools/spine.md), [rive](../tools/rive.md), [cartoon-animator](../tools/cartoon-animator.md)): порядка 10–30 секунд в день. Но риг персонажа делают дни, а нового ракурса приходится рисовать заново.
- Схема, график, надпись кодом: после первого построения изменение занимает минуты, см. [manim-ce](../tools/manim-ce.md), [motion-canvas](../tools/motion-canvas.md), [remotion](../tools/remotion.md).

### Где покадровая анимация оправдана, а где её заменит код

- Оправдана: актёрская игра персонажа, юмор, мягкие органичные формы (дым, жидкость), нарисованные переходы с характером, рукописная фактура.
- Заменяется кодом или motion design: схемы, графики, формулы, надписи, «рисуется линия на глазах» ([vivus](../tools/vivus.md), SVG-анимация), параллакс, повторяющиеся движения, тайминг под голос.
- Середина: кукольные риги в [rive](../tools/rive.md) или [synfig](../tools/synfig.md) дают персонажа без покадровой работы, но с меньшей выразительностью.

## Другие решения

Заметные альтернативы без карточки. Ссылки ведут на официальные страницы.

- FlipaClip — https://flipaclip.com/ — мобильное приложение для покадровой анимации; сайт заявляет 90 млн пользователей.
- RoughAnimator — https://www.roughanimator.com/ — рисованная покадровая анимация на iPad, Android, Mac и Windows, $7,99 за платформу (по сайту; даты обновлений на странице — апрель 2022).
- Live2D Cubism — https://www.live2d.com/en/ — оживление иллюстрации для 2D-персонажей (редактор и SDK); версии Free и PRO.
- DragonBones и LoongBones — рантайм https://github.com/DragonBones/DragonBonesJS (MIT) и редактор http://www.loongbones.app/ — скелетная анимация для игр; README рантайма рекомендует LoongBones для создания анимации, состояние самого редактора DragonBones не проверялось.
- Blender COA Tools — https://github.com/ndee85/coa_tools — кукольная анимация в Blender (GPL-3.0); последний выпуск 2.0 от 2019-08-15, совместимость с текущим Blender не проверялась.
- Wick Editor — https://www.wickeditor.com/ — бесплатный открытый (GPL-3.0) браузерный инструмент для игр и анимации (https://github.com/Wicklets/wick-editor).
- Adobe Character Animator — https://www.adobe.com/products/character-animator.html — кукла, управляемая веб-камерой и голосом; страница Adobe не открылась для проверки (403), ссылка не проверена.
- Animaker — https://www.animaker.com/ — онлайн-сервис мультяшных роликов из готовых персонажей и шаблонов.
- Vyond — https://www.vyond.com/ — онлайн-платформа корпоративных объясняющих роликов с готовыми персонажами.

## Вывод для объясняющих видео

Покадровая анимация нужна точечно: для персонажа, юмора и рисованных переходов. Основу ролика с графиками и схемами лучше собирать кодом ([manim-ce](../tools/manim-ce.md), [motion-canvas](../tools/motion-canvas.md), [remotion](../tools/remotion.md)) или в motion design ([after-effects](../tools/after-effects.md)), иначе вы платите временем аниматора за то, что делает формула. Для первой пробы персонажа возьмите [rive](../tools/rive.md) (агент собирает сцену текстом и сам проверяет кадр; видео с $9 в месяц) или бесплатные [tahoma2d](../tools/tahoma2d.md) и [synfig](../tools/synfig.md). Если есть аниматор и бюджет, потолок качества у [toon-boom-harmony](../tools/toon-boom-harmony.md) и [tvpaint](../tools/tvpaint.md); если художник рисует в [clip-studio-paint](../tools/clip-studio-paint.md), берите редакцию EX, а персонажу с телом и весом поможет [cascadeur](../tools/cascadeur.md). Новый проект в [adobe-animate](../tools/adobe-animate.md) начинать не стоит: по FAQ Adobe (обновлён 2026-06-08) продукт в режиме поддержки без новых функций. До выбора сделайте пилот на 10–15 секундах и измерьте часы.

## Источники

Факты о программах — в карточках. Здесь только то, чего в карточках нет. Все страницы проверены 2026-10-14.

- [FlipaClip](https://flipaclip.com/) — описание приложения.
- [RoughAnimator](https://www.roughanimator.com/) — платформы и цена $7,99.
- [Live2D Cubism](https://www.live2d.com/en/) — описание продукта.
- [DragonBonesJS](https://github.com/DragonBones/DragonBonesJS) и [README](https://raw.githubusercontent.com/DragonBones/DragonBonesJS/master/README.md) — MIT, рекомендация LoongBones.
- [COA Tools](https://github.com/ndee85/coa_tools) и [Releases](https://github.com/ndee85/coa_tools/releases) — GPL-3.0, выпуск 2.0 от 2019-08-15.
- [Wick Editor на GitHub](https://github.com/Wicklets/wick-editor) — GPL-3.0, описание.
- [Animaker](https://www.animaker.com/) и [Vyond](https://www.vyond.com/) — описание сервисов.
- Оценки времени аниматора — суждение автора обзора без источника. На пилотной сцене их надо проверить.
