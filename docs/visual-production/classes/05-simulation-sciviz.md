# Физические симуляции и научная визуализация

## Что сюда входит

Инструменты, которые считают физику или принимают её результаты и превращают их в картинку: поле магнита, течение, частицы, столкновения, упругие тела. Три группы. Расчётные решатели (Magpylib, Radia, FEMM, Elmer, COMSOL, Taichi, Box2D, Matter.js). Программы визуализации данных (ParaView, PyVista, Matplotlib, Makie). Готовые интерактивные демонстрации (PhET, Falstad, VPython). Соседние карточки других классов закрывают рендер и процедурные симуляции: [Houdini](../tools/houdini.md) делает жидкости, частицы и разрушения с лучшим рендером; [Blender Geometry Nodes](../tools/blender-geometry-nodes.md) строит процедурную геометрию и линии из данных; [Molecular Nodes](../tools/molecular-nodes.md) показывает молекулы и структуры в Blender; [ElectroMag Nodes](../tools/electromag-nodes.md) рисует линии электрического и магнитного поля в Blender; [Manim CE](../tools/manim-ce.md) рисует анимацию графиков, формул и векторных полей кодом.

## Когда этот класс нужен

- Невидимые явления: линии и карта поля магнита, поток, волны. Сквозной пример библиотеки: магнит на холодильнике и полосатый (многополюсный) гибкий магнит с односторонним полем.
- Физически правдоподобное движение: стопки, цепные реакции, рычаги, маятники, шарики вместо молекул.
- Показ результатов расчёта: сетка, изоповерхности, линии тока, срезы, облёт камеры вокруг 3D-поля.
- Интерактивные сцены для образования как референс или запись экрана (с оговорками по правам, см. PhET).
- Сцены, в которых цифры должны быть настоящими: сила притяжения, зависимость поля от расстояния, насыщение стали.

## Основные решения

- [Magpylib](../tools/magpylib.md) — аналитический расчёт поля магнитов в Python, быстрее всех начать, готовый пример чередующихся зон феррита; сталь только идеализированно.
- [FEMM](../tools/femm.md) — бесплатный 2D-решатель со сталью и насыщением, Lua-скрипты, снимки в BMP; Windows (Linux через Wine), FEMM 5 пока тестовый.
- [Radia](../tools/radia.md) — 3D-магнитостатика методом граничных интегралов (ESRF): постоянные магниты, катушки и железо с кривой намагничивания, силы через `FldFrc`, Python-интерфейс; собирается из исходников, оригинал мало обновляется, на выходе числа, а не картинки.
- [Elmer FEM](../tools/elmer-fem.md) — открытый 2D/3D-решатель с постоянными магнитами, вывод VTU в ParaView; настройка тяжёлая, сайт блокирует запросы.
- [COMSOL Multiphysics](../tools/comsol.md) — коммерческая платформа с готовым экспортом анимаций (GIF, AVI, WebM, PNG); цена не публикуется.
- [ParaView](../tools/paraview.md) — стандарт визуализации 3D-данных: линии тока, срезы, камера по ключевым кадрам, пакетный рендер.
- [PyVista](../tools/pyvista.md) — тот же движок VTK из Python, безголовый рендер и mp4, лучший спутник Magpylib.
- [Matplotlib (анимация)](../tools/matplotlib.md) — 2D-карты и линии поля, формулы, `FuncAnimation` и FFmpeg; первый выбор для агента.
- [ElectroMag Nodes](../tools/electromag-nodes.md) — платный набор Geometry Nodes для Blender ($1 или $15), рисует силовые линии, стрелки и плоскость модуля поля токов и зарядов; постоянных магнитов и железа не умеет, числа наружу не выводит.
- [Makie.jl](../tools/makie.md) — гладкая анимация данных на Julia через `record`; готовых магнитных пакетов нет.
- [VPython и GlowScript](../tools/vpython.md) — самая простая 3D-демонстрация в браузере; видео экспортировать нельзя.
- [PhET](../tools/phet.md) — готовые школьные симуляции магнитов, но с 2026-03-29 лицензия CC BY-NC: монетизированный YouTube требует платной лицензии.
- [Апплеты Falstad](../tools/falstad.md) — наглядная 3-D магнитостатика, скриншоты разрешены, видео для коммерческого канала нужно согласовать.
- [Taichi Lang](../tools/taichi.md) — быстрые собственные симуляции частиц и сред, но активность в репозитории прекратилась в июле 2025.
- [Matter.js](../tools/matter-js.md) — 2D-механика в браузере для мультяшных аналогий; релиз 0.20.0 от июня 2024.
- [Box2D](../tools/box2d.md) — 2D-механика с заявленным кросс-платформенным детерминизмом; нужен свой рендер.

## Сравнение

- Потолок качества. Картинку «из коробки» на уровень лучших научно-популярных каналов не делает никто. Лучше всего выглядят Makie (гладкий вектор и GPU) и COMSOL (отшлифованный постпроцессор), около 4 из 5. Magpylib с PyVista, ParaView, Matplotlib, Elmer через ParaView, Radia через PyVista, ElectroMag Nodes (виды Blender без настройки света), Taichi и PhET дают аккуратную учебную графику, около 3. FEMM, Falstad, VPython, Matter.js, Box2D — 2: окно инженерной программы, апплет или каркасы. Лучший приём: считать здесь, финальный свет и материалы делать в [Blender Geometry Nodes](../tools/blender-geometry-nodes.md) или [Houdini](../tools/houdini.md).
- Трудность для человека. Проще всего PhET, Falstad и VPython (1 из 5). Средне Magpylib, FEMM, PyVista, Matplotlib, Matter.js (2). Сложнее ParaView, Makie, Taichi, Box2D, ElectroMag Nodes (3): нужен Blender. Сложнее всех Radia, Elmer и COMSOL (4): постановка задачи, разбиение или сетка, граничные условия, у Radia ещё сборка из исходников.
- Трудность для агента. Легче всех Magpylib, PyVista, Matplotlib (1 из 5): всё кодом, кадр проверяется по картинке. Дальше ParaView, Makie, Taichi, Matter.js (2). FEMM, Elmer, Radia, ElectroMag Nodes, VPython, Box2D (3): нужен установленный Windows или Wine, сетка, сборка из исходников или Blender со своим рендером. Тяжело COMSOL, PhET, Falstad (4): мышь и интерфейс, лицензия или запись экрана.
- Автоматизация. Полностью кодом (5 из 5): Magpylib, ParaView, PyVista, Matplotlib, Makie, Taichi. Почти (4): FEMM (Lua, командная строка), Elmer (`.sif` и ElmerSolver), Radia (Python, пакетные расчёты), Matter.js, Box2D. Частично (3): COMSOL (Java и MATLAB), ElectroMag Nodes (Python Blender, но параметры в узлах). Почти нет: VPython (2), PhET и Falstad (1).
- Стоимость. Бесплатны и открыты Magpylib, FEMM, Elmer, Radia (BSD), ParaView, PyVista, Matplotlib, Makie, VPython, Taichi, Matter.js, Box2D. ElectroMag Nodes: разовая покупка $1 (Lite) или $15 (Pro), лицензия GPL, Blender бесплатный. COMSOL: цена не публикуется, лицензия платная (оценка cost 3 условная). PhET: бесплатно только для некоммерческого образовательного использования, цена коммерческой лицензии не опубликована. Falstad: бесплатно, но коммерческое использование согласуется с автором.
- Плавность переходов и непрерывность сцены. Лучшая — у кодовых инструментов, где время и позиции задаются параметром: Magpylib (магнит едет, поле пересчитывается), PyVista и ParaView (камера летит по пути, ключевые кадры), Makie (`Observable` и `record`), Matplotlib (`FuncAnimation`). Решатели FEMM, Elmer, COMSOL считают серию положений и дают ломаное движение, плавность зависит от числа шагов; COMSOL даёт параметрическую развёртку в анимацию одной кнопкой. Интерактивные PhET, Falstad и VPython плавны в реальном времени, но кадр не воспроизвести. Морфинг объектов, рисование линий и привязка к голосу нигде не встроены: время кадров задают кодом, метки озвучки превращают в номера кадров вручную (см. карточку [WhisperX](../tools/whisperx.md)).
- Магнит на холодильнике (многополюсный полосатый). Magpylib: да; пример Magnetic Scales собирает полосу из 10 чередующихся зон феррита с остаточной индукцией 0,3 Тл и строит карты поля; линии поля через `streamplot` (2D) и PyVista (3D), анимация встроена (Plotly в браузере, GIF через PyVista); сталь двери только методом изображений (идеальная проницаемость). FEMM: да, плоская задача, блоки с чередующимся направлением, сталь с насыщением, линии потока и плотность; готового примера полосатого магнита нет, есть Permanent Magnet Example (брусок). Elmer: да, 2D и 3D, `Magnetization` по телам; в документации подковообразный магнит (учебник 15) вместо полосатого, анимацию делает ParaView. Radia: да, 3D, блоки `ObjRecMag` с заданной намагниченностью и железо `MatSatIso`, сила прижима через `FldFrc`, учёт железа точнее, чем у Magpylib; готового примера полосатого магнита нет, ближайший пример ондулятора и квадруполя, вывод только числа, картинку рисуют PyVista или Matplotlib; границы воздуха не нужны, но у поверхности железа поле искажено подразбиением. ElectroMag Nodes: нет, только токи и заряды, постоянных магнитов и железа нет. COMSOL: да, AC/DC Module с постоянными магнитами и кривой B-H; пример Permanent Magnet и встроенный экспорт GIF, AVI, WebM, PNG; примера полосатого магнита не нашли.

## Другие решения

- [Rapier](https://rapier.rs/) — физический движок 2D и 3D на Rust, Apache-2.0, есть сборка для JavaScript.
- [MuJoCo](https://mujoco.org/) — движок многосуставной динамики с контактами от Google DeepMind, Apache-2.0, интерактивная визуализация на OpenGL.
- [Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world) — платформа физической симуляции для ИИ с собственным рендером Nyx, Apache-2.0.
- [NVIDIA Warp](https://developer.nvidia.com/warp-python) — Python-фреймворк для симуляций на GPU, Apache-2.0, ближайший аналог Taichi.
- [OpenFOAM](https://openfoam.org/) (линия Foundation) и [OpenFOAM ESI](https://www.openfoam.com/) — открытая вычислительная гидродинамика, результаты смотрят в ParaView.
- [VisIt](https://visit-dav.github.io/visit-website/) — научная визуализация больших данных от LLNL, BSD-3-Clause, соперник ParaView.
- [Mayavi](https://docs.enthought.com/mayavi/mayavi/) — 3D-визуализация научных данных в Python на VTK, BSD.
- [Plotly для Python](https://plotly.com/python/) — интерактивные графики с анимацией в браузере, MIT; видео из них получить сложнее, чем из Matplotlib.
- [Algodoo](https://www.algodoo.com/) — 2D-песочница физики; на сайте сказано «Algodoo is now FREE!», условия на ролики не проверялись.
- [FEniCSx](https://fenicsproject.org/) — открытая платформа конечных элементов с интерфейсами Python и C++ для своих задач.
- [NGSolve](https://ngsolve.org/) — конечные элементы на Python и C++ вместе с генератором сетки Netgen, LGPL.
- [Gmsh](https://gmsh.info/) — генератор конечно-элементных сеток, связка с Elmer и FEniCS.
- [Pymunk](https://www.pymunk.org/) — 2D-физика твёрдых тел для Python на основе Chipmunk2D, MIT.
- [Box3D](https://github.com/erincatto/box3d) — 3D-движок физики для игр от автора Box2D.

## Вывод для объясняющих видео

В первую очередь брать связку «считает код, рисует код»: [Magpylib](../tools/magpylib.md) для магнитов и [PyVista](../tools/pyvista.md) или [Matplotlib](../tools/matplotlib.md) для карт и линий поля, кадры собирает FFmpeg. Это бесплатно, полностью воспроизводимо и по силам агенту без рук. Когда нужна настоящая сталь с насыщением, подключать [Radia](../tools/radia.md) (3D, метод граничных интегралов; сборка из исходников, оригинал почти не обновляется, выводит только числа) или конечные элементы: [FEMM](../tools/femm.md) для быстрой плоской задачи (на Windows или Wine) или [Elmer FEM](../tools/elmer-fem.md) вместе с [ParaView](../tools/paraview.md) для 3D; [COMSOL](../tools/comsol.md) только при уже имеющейся лицензии. Готовые симуляции PhET нельзя брать в монетизированные ролики без коммерческой лицензии, Falstad только после согласования; их место — референс и черновик. Для 2D-механики подойдут [Matter.js](../tools/matter-js.md) и [Box2D](../tools/box2d.md), для больших систем частиц — [Houdini](../tools/houdini.md) или [Taichi](../tools/taichi.md), но у Taichi с июля 2025 нет новых коммитов. Финальный свет и камеру для главных кадров имеет смысл выносить в [Blender Geometry Nodes](../tools/blender-geometry-nodes.md); для линий поля токов и зарядов в самом Blender есть готовый набор [ElectroMag Nodes](../tools/electromag-nodes.md) ($1–15), но магниты с железом он не считает.

## Источники

- [Rapier на GitHub](https://github.com/dimforge/rapier) — 2D и 3D движки на Rust, лицензия Apache-2.0. Проверено 2026-10-14.
- [MuJoCo на GitHub](https://github.com/google-deepmind/mujoco) — назначение, интерактивная визуализация, Apache-2.0. Проверено 2026-10-14.
- [Genesis World на GitHub](https://github.com/Genesis-Embodied-AI/genesis-world) — платформа, рендер Nyx, Apache-2.0. Проверено 2026-10-14.
- [NVIDIA Warp на GitHub](https://github.com/NVIDIA/warp) — Python-фреймворк для GPU-симуляций, Apache-2.0. Проверено 2026-10-14.
- [OpenFOAM Foundation](https://openfoam.org/) и [OpenFOAM ESI](https://www.openfoam.com/) — две линии пакета. Проверено 2026-10-14.
- [VisIt на GitHub](https://github.com/visit-dav/visit) — приложение научной визуализации, BSD 3-Clause. Проверено 2026-10-14.
- [Mayavi на GitHub](https://github.com/enthought/mayavi) — визуализация 3D-данных в Python. Проверено 2026-10-14.
- [plotly.py на GitHub](https://github.com/plotly/plotly.py) — MIT. Проверено 2026-10-14.
- [Algodoo](https://www.algodoo.com/) — «Algodoo is now FREE!», главная страница. Проверено 2026-10-14.
- [FEniCS Project](https://fenicsproject.org/) — платформа решения уравнений методом конечных элементов. Проверено 2026-10-14.
- [Netgen/NGSolve на GitHub](https://github.com/NGSolve/ngsolve) — лицензия LGPL-2.1. Проверено 2026-10-14.
- [Gmsh](https://gmsh.info/) — генератор сеток. Проверено 2026-10-14.
- [Pymunk](https://www.pymunk.org/en/latest/) — 2D-физика для Python на основе Chipmunk2D. Проверено 2026-10-14.
- [Box3D на GitHub](https://github.com/erincatto/box3d) — 3D-движок. Проверено 2026-10-14.
