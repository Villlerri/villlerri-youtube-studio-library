---
id: elmer-fem
name: Elmer FEM
class: [simulation]
kind: app
site: https://www.elmerfem.org/
github: ElmerCSC/elmerfem
scenes: [field, simulation, mechanism]
quality: 3
human_difficulty: 4
agent_difficulty: 3
automation: 4
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, windows, macos]
export: [vtu, vtk, png-sequence]
code_license: GPL-2.0 и LGPL-2.1 (по компонентам)
price: бесплатно
checked: 2026-10-14
---

# Elmer FEM

Открытый конечно-элементный пакет CSC (Финляндия) для мультифизики: механика, потоки, тепло, электромагнетизм. Для магнитов в 2D и 3D есть решатели MagnetoDynamics с заданной намагниченностью. Визуализацию результатов делает ParaView.

## Ссылки

- Официальный сайт: <https://www.elmerfem.org/> (при проверке 2026-10-14 отдавал HTTP 403 на скрипт-запросы, информация взята из репозитория).
- GitHub: <https://github.com/ElmerCSC/elmerfem>
- Документация: учебники и руководства лежат на зеркале CSC, например [ElmerTutorials.pdf](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerTutorials.pdf) и [ElmerModelsManual.pdf](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerModelsManual.pdf).
- Примеры, проверенные 2026-10-14:
  - Учебник 15 из ElmerGUI Tutorials «Magnetostatics – Magnetic field resulting from a permanent magnet» (стр. 97 в [PDF](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerTutorials.pdf), версия 26.1 от января 2026): подковообразный магнит, два конца намагничены в противоположные стороны, решатель MagnetoDynamics2D, сетка Gmsh, воздух с круговой внешней границей.
  - [Elmer FEM Webinar – Coil Modeling with ElmerFEM](https://www.youtube.com/watch?v=Z_MBIt1pApU) — вебинар разработчиков о моделировании катушек (канал elmerfem).
  - [Elmer FEM Webinar – pyelmer: Python interface for Elmer workflow](https://www.youtube.com/watch?v=QIfAa_5pvHU) — запуск Elmer из Python, пригодится для автоматизации.
  - [Elmer FEM Webinar – Overview of Capabilities of Elmer](https://www.youtube.com/watch?v=CloQq_F7O5Q) — обзор возможностей.

## Что реально получается

Сквозной пример (магнит на холодильнике). Решатель MagnetoDynamics принимает ключевое слово `Magnetization` для материала; на границе между магнитом и немагнитным телом по умолчанию ставится нужное условие (Models Manual). Полосатый магнит — набор тел с разными знаками намагничивания, так в учебнике 15 сделана пара «IronPlus» и «IronMinus» с ±750 кА/м. Стальная дверь — тело с относительной проницаемостью. Учебник 15 — плоская задача (поле бесконечно длинного магнита). Models Manual описывает `Magnetization` в общем виде для решателя MagnetoDynamics, готового 3D-примера магнита не нашли. Нелинейная кривая B-H для стали не проверялась, см. «Неизвестно».

Результаты:

- Выход в формате VTU, который в Models Manual назван рекомендуемым для ParaView (`Output Format = vtu`). Дальше поле, линии тока потока (StreamTracer), срезы, анимации делает [paraview](paraview.md) или [pyvista](pyvista.md). Сам Elmer красивых картинок не делает.
- Временная задача: расчёт по шагам даёт файл на каждый шаг, ParaView проигрывает их как анимацию.
- Движение магнита к двери не встроено в простой виде. Реалистично это серия независимых расчётов магнитостатики с разным зазором, из которых собирается плавная последовательность кадров.
- Морфинг, камера, рисование линий, голос: нет в самом Elmer, решаются в ParaView и монтаже.

## Слабые стороны

- Настройка большая: файл `.sif`, сетка (Gmsh, ElmerGrid), выбор решателей и порядок их запуска.
- Сайт блокирует автоматические запросы (403). Документацию надо брать с зеркала CSC или из репозитория.
- Нет готового хорошего рендера. Всё упирается в ParaView.
- Готовые сборки: установщики для Windows, образ WSL, виртуальная машина VirtualBox, PPA для Ubuntu. Для macOS в README указана только сборка из исходников.
- 3D-задачи с магнитами требуют большого воздушного объёма вокруг тела, иначе граница искажает поле (общая особенность метода конечных элементов).

## Сложность

- Для человека (4 из 5): нужны знания метода конечных элементов, уравнений Максвелла и работы с сетками. Освоение — недели.
- Для агента (3 из 5): входные файлы текстовые, решатель запускается из командной строки. Агент пишет `.sif`, запускает `ElmerSolver`, читает VTU. Руки нужны для первой геометрии и сетки, если не писать их в Gmsh-скрипте.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): ElmerSolver и ElmerGrid — программы командной строки; есть модуль Python pyelmer (см. вебинар) и контейнеры Docker. ElmerGUI опционален.
- Воспроизводимость (4 из 5): проект — текстовые файлы `.sif`, `.geo`, `.msh`, подходят для git. Многопоточный расчёт может давать отличия в последних знаках.

## Платформа и оборудование

Linux (пакеты PPA для Ubuntu), Windows (установщики, образ WSL), виртуальная машина VirtualBox, Docker. macOS: в README указана только сборка из исходников. Видеокарта не нужна. Для объёмных 3D-задач нужны много памяти и процессоров, параллельный запуск через MPI поддерживается.

## Экспорт

VTU и VTK (для ParaView), форматы Gmsh, табличный вывод. Видео и PNG делает ParaView, см. [paraview](paraview.md). В 26.2 добавлен вывод в формате ADIOS2/BP5 с описанием Fides для ParaView.

## Стоимость

Проверено 2026-10-14 по [README репозитория](https://github.com/ElmerCSC/elmerfem). Бесплатно. CSC предлагает сервис Elmer для исследователей ([ссылка из README](https://research.csc.fi/service/elmer/)), условия сервиса не проверялись.

## Лицензия и права

- Код или программа: библиотека ElmerSolver и часть модулей под LGPL, ElmerGUI, ElmerGrid и большинство физических модулей под GPL ([политика лицензий](https://github.com/ElmerCSC/elmerfem/blob/devel/license_texts/ElmerLicensePolicy.md)). Общий файл [LICENSE.md](https://github.com/ElmerCSC/elmerfem/blob/devel/LICENSE.md) — GPL 2.0.
- Результат: политика говорит, что при простом использовании открытые лицензии не ограничивают работу. Ограничения возникают при распространении программы и модификаций.
- Ассеты в комплекте: учебные модели и файлы tutorials-GUI-files. Отдельных условий не нашли.

## Активность и зрелость

<!-- gh-stats:ElmerCSC/elmerfem -->
- Звёзды GitHub: 1 735
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: release-26.2.1 (2026-07-30)
- Лицензия по данным GitHub: GitHub не определил, см. «Лицензия и права»
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория ElmerCSC/elmerfem, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: stable. Релиз v26.2.1 опубликован 2026-04-29, до этого v26.1 в январе 2026 и Elmer 9.0. В примечаниях к 26.2 около 128 коммитов за период, вклад вносят сотрудники CSC и сторонние участники. Развивает CSC. Обсуждения идут на форуме и в Discord (ссылки в README).

## Когда брать и когда нет

- Брать: нужно 3D-поле магнитов со сталью и открытый инструмент, не привязанный к Windows. Мультифизика (нагрев катушки, механика).
- Не брать: нужен быстрый плоский расчёт на ходу или аналитика. Тогда [femm](femm.md) или [magpylib](magpylib.md). Нет времени на настройку сеток.

## Источники

- [Репозиторий Elmer FEM, README](https://github.com/ElmerCSC/elmerfem) — назначение, ссылки на сборки, документацию, ParaView. Проверено 2026-10-14.
- [Политика лицензий Elmer](https://github.com/ElmerCSC/elmerfem/blob/devel/license_texts/ElmerLicensePolicy.md) — GPL и LGPL по компонентам. Проверено 2026-10-14.
- [LICENSE.md](https://github.com/ElmerCSC/elmerfem/blob/devel/LICENSE.md) — GPL 2.0. Проверено 2026-10-14.
- [Elmer Models Manual](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerModelsManual.pdf) — Magnetization, VTU, ParaView. Проверено 2026-10-14.
- [Elmer GUI Tutorials](https://www.nic.funet.fi/pub/sci/physics/elmer/doc/ElmerTutorials.pdf) — учебник 15, подковообразный магнит. Проверено 2026-10-14.
- [Релизы Elmer FEM на GitHub](https://github.com/ElmerCSC/elmerfem/releases) — v26.2.1 от 2026-04-29, примечания к релизу. Проверено 2026-10-14.
- [Канал elmerfem на YouTube](https://www.youtube.com/user/elmerfem) — вебинары. Ролики проверены через oEmbed 2026-10-14.

## Неизвестно

- Поддерживает ли MagnetoDynamics нелинейную кривую B-H для стальной двери без дополнительной настройки: в проверенных страницах нашли только постоянную проницаемость.
- Страница elmerfem.org недоступна автоматическим запросам, актуальные новости и список платформ с сайта не получены.
- Время расчёта 3D-задачи с тонкими полосами магнита: не измерялось.
- Наличие готового примера гибкого многополюсного магнита в документации: не найдено, есть только подковообразный.
