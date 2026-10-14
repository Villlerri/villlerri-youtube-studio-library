# Подбор по типу сцены и по качеству и затратам

## Как пользоваться

1. Найти тип сцены ниже. Список типов — в [методике](method.md#типы-сцен).
2. Взять «основной выбор», если нет причины иначе. Остальные пункты — когда есть бюджет, нужен человек без кода или есть риск.
3. Открыть карточку и проверить цену и права на дату.
4. Полный список инструментов по типам сцен, отсортированный по качеству и цене: [tables/by-scene.csv](tables/by-scene.csv).

Цены проверены 2026-10-14. Инструменты голоса и меток времени нужны для любой сцены и здесь не повторяются: [синхронизация](classes/12-sync.md).

## По типу сцены

### Формулы (`formula`)

- Основной выбор: [Manim CE](tools/manim-ce.md). Формула пишется на глазах (`Write`), части перетекают при преобразованиях (`TransformMatchingTex`). Агент делает сам.
- Выше качество: [ManimGL](tools/manimgl.md), инструмент 3Blue1Brown; работа человека в окне, API нестабилен.
- Без кода: [Lightboard](tools/lightboard.md) или рукой на планшете ([живая доска](combos.md#4-живая-доска)).
- Осторожно: формула картинкой в монтаже не даёт анимировать части.

### Графики (`graph`)

- Основной выбор: [Manim CE](tools/manim-ce.md) для графиков функций, [Matplotlib](tools/matplotlib.md) для данных расчёта.
- Данные и инфографика: [D3.js](tools/d3.md) с покадровой записью через [Remotion](tools/remotion.md) или [CCapture.js](tools/ccapture-js.md).
- Без кода: [Cavalry](tools/cavalry.md).
- Осторожно: [MathBox](tools/mathbox.md) заброшен; встроенная запись [p5.js](tools/p5js.md) ограничена 15 секундами.

### Схемы и процессы (`diagram`)

- Основной выбор: [Manim CE](tools/manim-ce.md). Для схем в стиле интерфейса — [Remotion](tools/remotion.md).
- С редактором меток под голос: [Motion Canvas](tools/motion-canvas.md) (релизов нет с февраля 2025 года) или его форк [Canvas Commons](tools/canvas-commons.md).
- Выше качество: [After Effects](tools/after-effects.md).
- Без кода: [Excalidraw](tools/excalidraw.md) с excalidraw-animate.
- Не брать: [VideoScribe](tools/videoscribe.md), [Doodly](tools/doodly.md) — клипарт и «рука рисует».

### Устройство предмета (`mechanism`)

- Основной выбор: [Blender](tools/blender.md) с [Geometry Nodes](tools/blender-geometry-nodes.md).
- Выше качество: [Cinema 4D](tools/cinema-4d.md), [Houdini](tools/houdini.md), [Unreal Engine](tools/unreal-engine.md) для кинематографичного света.
- Без кода и быстро: [Spline](tools/spline.md), видео с тарифа Pro ($25 в месяц).
- Осторожно: модели из [Meshy](tools/meshy.md) или [TRELLIS](tools/trellis.md) годятся для реквизита, но не для деталей, которые объясняют устройство.

### Поля и невидимые явления (`field`)

- Основной выбор: расчёт в [Magpylib](tools/magpylib.md) или другом решателе ([симуляции](classes/05-simulation-sciviz.md)), линии поля в [Manim CE](tools/manim-ce.md) (StreamLines) или [PyVista](tools/pyvista.md).
- Выше качество: [Blender Geometry Nodes](tools/blender-geometry-nodes.md) по данным расчёта; [GLSL-шейдеры](tools/glsl-shadertoy.md).
- Без кода: [After Effects](tools/after-effects.md), но поле тогда рисуется на глаз, не считается.
- Осторожно: запись экрана [PhET](tools/phet.md) и [Falstad](tools/falstad.md) в монетизируемый ролик требует лицензии или согласия автора.

### Микромир (`micro`)

- Основной выбор: [Blender](tools/blender.md); молекулы — [Molecular Nodes](tools/molecular-nodes.md), частицы и домены — [Geometry Nodes](tools/blender-geometry-nodes.md).
- Выше качество: [Houdini](tools/houdini.md).
- Осторожно: картинки [генеративных моделей](classes/10-generative.md) выдумывают структуру вещества.

### Смена масштаба (`scale`)

- Основной выбор: [Blender](tools/blender.md), один непрерывный проезд камеры.
- Выше качество: [Unreal Engine](tools/unreal-engine.md), [Houdini](tools/houdini.md).
- Кодом в браузере: [Three.js](tools/three-js.md) через [Remotion](tools/remotion.md).
- Без кода: [After Effects](tools/after-effects.md), 2.5D-камера.

### Точная симуляция (`simulation`)

- Основной выбор: поля — [Magpylib](tools/magpylib.md), [Matplotlib](tools/matplotlib.md), [PyVista](tools/pyvista.md); 2D-механика — [Box2D](tools/box2d.md) или [Matter.js](tools/matter-js.md); симуляция и рендер в одном движке — [Godot](tools/godot.md) в режиме Movie Maker.
- Выше качество: [Houdini](tools/houdini.md); [Blender Geometry Nodes](tools/blender-geometry-nodes.md) с зонами симуляции.
- Осторожно: у [Taichi](tools/taichi.md) нет коммитов с июля 2025 года.

### Персонажи и сюжет (`character`)

- Основной выбор: [Rive](tools/rive.md) — сцену можно собрать текстом, видео с $9 в месяц. Бесплатно — [Tahoma2D](tools/tahoma2d.md) или [Synfig](tools/synfig.md).
- Выше качество: [Toon Boom Harmony](tools/toon-boom-harmony.md), [TVPaint](tools/tvpaint.md), [After Effects](tools/after-effects.md) с ригами.
- Быстро без кода: [Cartoon Animator](tools/cartoon-animator.md) ($149), [Moho](tools/moho.md).
- Не брать для нового проекта: [Adobe Animate](tools/adobe-animate.md) — в режиме поддержки без новых функций.

### Рисование вживую (`drawing`)

- Основной выбор: «как вживую» кодом — [Manim CE](tools/manim-ce.md) (`Create`, `Write`) или [Blender Grease Pencil](tools/blender-grease-pencil.md) (Build) в 3D-сцене. Правится и пересчитывается под новую озвучку.
- По-настоящему вживую: [Krita](tools/krita.md) или [Procreate Dreams](tools/procreate-dreams.md) и запись в [OBS Studio](tools/obs-studio.md); человек в кадре — [Lightboard](tools/lightboard.md).
- Быстрые схемы: [Excalidraw](tools/excalidraw.md).
- Не брать: [VideoScribe](tools/videoscribe.md), [Doodly](tools/doodly.md).

### Реальная съёмка с графикой (`real-footage`)

- Основной выбор: Fusion в [DaVinci Resolve](tools/davinci-resolve.md), трекинг и композитинг бесплатно.
- Графика поверх: [Manim CE](tools/manim-ce.md) или [Blender](tools/blender.md) с прозрачным фоном ([гибридные пайплайны](classes/11-hybrid.md)).
- Выше качество: [After Effects](tools/after-effects.md); [Nuke](tools/nuke.md) избыточен.
- Осторожно: генеративное «реалистичное» видео нужно раскрывать как синтетическое, а физику в нём модель выдумывает.

### Типографика и титры (`typography`)

- Основной выбор: [Remotion](tools/remotion.md) — текст и метки из JSON, агент делает сам.
- Выше качество: [After Effects](tools/after-effects.md); объёмные заголовки — [Cinema 4D](tools/cinema-4d.md).
- Без кода: [Cavalry](tools/cavalry.md), [Apple Motion](tools/apple-motion.md) ($49,99 разово, только Mac).
- Правила: [раздел о типографике](craft.md#типографика).

### Карты и хронологии (`map-timeline`)

- Основной выбор: [D3.js](tools/d3.md) с покадровой записью через [Remotion](tools/remotion.md).
- Выше качество: [After Effects](tools/after-effects.md).
- Без кода: [Cavalry](tools/cavalry.md).

### Экран и код (`screen`)

- Основной выбор: интерфейс, пересобранный кодом в [Remotion](tools/remotion.md); код на экране — узел `Code` в [Motion Canvas](tools/motion-canvas.md).
- Запись настоящего экрана: [OBS Studio](tools/obs-studio.md), сборка в [DaVinci Resolve](tools/davinci-resolve.md).
- Выше качество: [After Effects](tools/after-effects.md).

## По качеству и затратам

Четыре ступени. Каждая следующая добавляет возможности, но не заменяет решений из [раздела о качестве](craft.md): дорогой инструмент не спасает слабую раскадровку.

### Ступень 1. Бесплатно, делает агент

- Состав: [Manim CE](tools/manim-ce.md), [Magpylib](tools/magpylib.md), [Matplotlib](tools/matplotlib.md), [PyVista](tools/pyvista.md), [FFmpeg](tools/ffmpeg.md), [MoviePy](tools/moviepy.md), [Remotion](tools/remotion.md) для команд до 3 человек, [D3.js](tools/d3.md), [Blender](tools/blender.md) через Python и командную строку.
- Даёт: формулы, графики, схемы, поля, типографику, сборку ролика. Точность и воспроизводимость.
- Не даёт: фактуру, свет и вкус кадра без человека.

### Ступень 2. Бесплатно, нужен человек

- Состав: [Blender](tools/blender.md) с [Grease Pencil](tools/blender-grease-pencil.md) и [Geometry Nodes](tools/blender-geometry-nodes.md), [DaVinci Resolve](tools/davinci-resolve.md), [Krita](tools/krita.md), [OBS Studio](tools/obs-studio.md), [Excalidraw](tools/excalidraw.md), [Cavalry](tools/cavalry.md), [Tahoma2D](tools/tahoma2d.md), [Synfig](tools/synfig.md).
- Даёт: выразительное 3D, рисование вживую, реальную съёмку с графикой, персонажей.

### Ступень 3. Недорогие покупки и подписки

- Обязательно: [ElevenLabs](tools/elevenlabs.md) от $6 в месяц — коммерческое право на голос.
- По сценам: [Procreate Dreams](tools/procreate-dreams.md) $12,99 разово, [Apple Motion](tools/apple-motion.md) $49,99 разово, [Rive](tools/rive.md) от $9 в месяц, [Spline](tools/spline.md) Pro $25 в месяц, [Cartoon Animator](tools/cartoon-animator.md) $149, [DaVinci Resolve](tools/davinci-resolve.md) Studio $295 разово, [Houdini](tools/houdini.md) Indie $299 в год, лицензия [Remotion](tools/remotion.md) для команд от 4 человек — от $25 в месяц за место.
- Даёт: удобство, отсутствие водяных знаков, автоматизацию платных версий, коммерческие права.

### Ступень 4. Профессиональные пакеты

- Состав: [After Effects](tools/after-effects.md) $22,99 в месяц (недорог, но требует профессионала), [Cinema 4D](tools/cinema-4d.md) около $839 в год по данным прессы, [Toon Boom Harmony](tools/toon-boom-harmony.md) от €273 в год, [TVPaint](tools/tvpaint.md) от €650, [TouchDesigner](tools/touchdesigner.md) Commercial $600, [Maya](tools/maya.md) $2010 в год, [Nuke](tools/nuke.md) €3139 в год, [COMSOL](tools/comsol.md) по запросу.
- Даёт: скорость опытной студии, стандартные отраслевые процессы, возможность нанять специалиста под знакомый инструмент.

### Генеративные сервисы

Оплата за генерацию, права на результат и водяные знаки зависят от тарифа. Для физики их не брать. Подробно: [генеративные методы](classes/10-generative.md).
