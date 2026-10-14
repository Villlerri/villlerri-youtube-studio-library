---
id: molecular-nodes
name: Molecular Nodes
class: [3d, simulation]
kind: plugin
site: https://bradyajohnston.github.io/MolecularNodes/
github: BradyAJohnston/MolecularNodes
scenes: [micro, simulation, scale]
quality: 5
human_difficulty: 3
agent_difficulty: 2
automation: 4
reproducibility: 4
cost: 0
maturity: stable
platforms: [linux, macos, windows]
export: [mp4, png-sequence, exr-sequence]
code_license: GPL-3.0-or-later
price: бесплатно
checked: 2026-10-14
---

# Molecular Nodes

Аддон Blender для научной визуализации молекул: импортирует структуры и траектории и строит их через [Geometry Nodes](blender-geometry-nodes.md). Подходит для сцен «внутри клетки» и «от кухни до атома».

## Ссылки

- Официальный сайт и документация: https://bradyajohnston.github.io/MolecularNodes/
- GitHub: https://github.com/BradyAJohnston/MolecularNodes (README: «Toolbox for molecular animations in Blender, powered by Geometry Nodes»)
- Страница в Blender Extensions: https://extensions.blender.org/add-ons/molecularnodes/
- Пакет Python: https://pypi.org/project/molecularnodes/
- Примеры, проверенные 2026-10-14 (список составил автор аддона на [странице Examples](https://bradyajohnston.github.io/MolecularNodes/examples/); сами каналы использование не подтверждали отдельно):
  - [AlphaFold — The Most Useful Thing AI Has Ever Done (Veritasium)](https://www.youtube.com/watch?v=P_fHJIYENdI) — в галерее аддона указан как ролик о сворачивании белков.
  - [The Insane Math Of Knot Theory (Veritasium)](https://www.youtube.com/watch?v=8DBhTXM_Br4) — в галерее указан как ролик о топоизомеразах ДНК.
  - [Your Operating System | Eukaryotic Transcription (Clockwork)](https://www.youtube.com/watch?v=HZAmbbTcQ3M) — в галерее указан как ролик о переписывании ДНК в мРНК.
  - [Why do we have to learn about the Krebs cycle? (NanoRooms)](https://www.youtube.com/watch?v=fSUecFhdDLk) — в галерее указан как ролик о цикле Кребса.
  - [How our cells (nearly) perfected making nanobots (NanoRooms)](https://www.youtube.com/watch?v=NiR3j0WNTI0) — указан в галерее аддона.

## Что реально получается

- Молекулы и клетка: структуры из PDB и mmCIF, молекулярно-динамические траектории, карты плотности электронной микроскопии (EM `.map`, `.star`). Стили отображения и выбор атомов задаются узлами.
- Непрерывность: камера Blender облетает молекулу, масштаб меняется без склеек. Траектории дают реальную динамику белков, а не имитацию.
- Анимация: ключи узлов и параметров (например, раскрытие, выделение цветом) плавно интерполируются.
- Аннотации и подписи: в документации есть разделы Annotations и Rendering; точный состав подписей не проверялся.
- Звук и голос: отдельной синхронизации нет, как у [Blender](blender.md).
- Не подходит для: диаграмм, формул, графиков; электронных схем.

## Слабые стороны

- Привязан к версии Blender: сборка 520.2.0 нужна для Blender 5.2 LTS и новее, README указывает Blender 4.2 и новее как минимум. Для старых Blender нужны старые сборки аддона.
- Зависит от Python 3.13 (PyPI: `requires_python ~=3.13.0`), то есть от версии Python в Blender.
- Разрешения: по странице расширения нужен доступ в сеть (скачивание структур из PDB и «AFPDB», как написано на странице) и к файлам (импорт и кэш).
- Часть видеоуроков на YouTube устарела (на сайте документации сказано, что общий порядок работы остался).
- Научная корректность картинки на авторе: аддон показывает данные, выбор стилей и цветов — его задача.

## Сложность

- Для человека (3 из 5): нужны Blender и понимание структур. Простая сцена по уроку собирается за дни.
- Для агента (2 из 5): есть Python API (разделы Molecule, Trajectory, Canvas и Rendering в документации) и пакет на PyPI. Агент может писать скрипт «загрузить структуру, задать стиль, камеру, отрендерить». Красоту кадра проверяет по рендеру.

## Автоматизация и воспроизводимость

- Автоматизация (4 из 5): Python API и командная строка Blender; пакетный рендер. Документация API у проекта отдельная.
- Воспроизводимость (4 из 5): сцена из скрипта и идентификаторов PDB воспроизводима; данные скачиваются по сети. `.blend` двоичный.

## Платформа и оборудование

Как у [Blender](blender.md). На странице расширения указаны Windows, Linux и macOS (Apple Silicon). Для крупных комплексов (вирусы, траектории) нужны ОЗУ и видеокарта (оценка).

## Экспорт

Как у Blender: видео, последовательности кадров, EXR. Аддон ничего не добавляет к форматам вывода.

## Стоимость

Проверено 2026-10-14 по [странице расширения](https://extensions.blender.org/add-ons/molecularnodes/). Бесплатно. Версия 520.2.0, опубликована 2026-09-18 (PyPI подтверждает дату загрузки 2026-09-18). Загрузок на странице: 56 471.

## Лицензия и права

- Код или программа: на странице расширения «GNU General Public License v3.0 or later»; в README указана «GPL-3.0».
- Результат: отдельных условий на изображения и видео в README и на странице расширения не нашёл. Для Blender действует «What you create with Blender is your sole property» (см. [blender](blender.md)). Данные структур: файлы архива PDB доступны по CC0 1.0 (по [политике RCSB](https://rcsb.org/pages/policies)). Авторов структур рекомендуется упоминать. Данные AlphaFold DB — отдельная лицензия, не проверена.
- Ассеты в комплекте: стили и материалы идут с аддоном под той же лицензией; отдельных условий не выявлено.

## Активность и зрелость

<!-- gh-stats:BradyAJohnston/MolecularNodes -->
- Звёзды GitHub: 1 385
- Последний коммит в основной ветке: 2026-10-14
- Последний релиз или тег: v520.2.0 (2026-09-18)
- Лицензия по данным GitHub: GPL-3.0
- Репозиторий в архиве: нет
- Источник: GitHub API и Atom-ленты репозитория BradyAJohnston/MolecularNodes, получено 2026-10-14.
<!-- /gh-stats -->

Зрелость: `stable`. Автор — Brady Johnston. Аддон опубликован в Blender Extensions 2024-06-12, на странице рейтинг 5.0 из 5 (34 отзыва). Свежая сборка 520.2.0 вышла 2026-09-18 (на странице «обновлено три недели назад»). На странице Releases GitHub записей нет.

## Когда брать и когда нет

- Брать: молекулы, белки, ДНК, вирусы, клеточные машины; научный ролик с непрерывным облётом.
- Не брать: если нужны только схемы или формулы; если важна простая схематичная картинка на уровне учебника (смотрите [blender](blender.md) с обычной геометрией или [pyvista](pyvista.md) для научных данных).

## Источники

- [Страница расширения](https://extensions.blender.org/add-ons/molecularnodes/) — версия, лицензия, разрешения. Проверено 2026-10-14.
- [Документация и главная](https://bradyajohnston.github.io/MolecularNodes/) — форматы и возможности. Проверено 2026-10-14.
- [Examples](https://bradyajohnston.github.io/MolecularNodes/examples/) — галерея. Проверено 2026-10-14.
- [GitHub](https://github.com/BradyAJohnston/MolecularNodes) — README, лицензия, требование Blender 4.2. Проверено 2026-10-14.
- [PyPI](https://pypi.org/pypi/molecularnodes/json) — версия 520.2.0, Python ~=3.13, дата 2026-09-18. Проверено 2026-10-14.
- [Политика данных RCSB](https://rcsb.org/pages/policies) — PDB под CC0. Проверено 2026-10-14.

## Неизвестно

- Лицензия данных AlphaFold DB не проверена.
- Использование аддона самими каналами (Veritasium, Clockwork, NanoRooms) подтверждено только галереей аддона, не описаниями роликов.
- Ограничения на крупные системы (миллионы атомов) по памяти не проверялись.
- Состав аннотаций (подписи, шкалы) не изучался.
- Заявления проекта о правах на готовые изображения и видео нет; опираюсь на правила Blender.
