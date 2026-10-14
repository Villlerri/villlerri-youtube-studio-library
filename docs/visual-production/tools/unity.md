---
id: unity
name: Unity
class: [3d]
kind: app
site: https://unity.com/
github: none
scenes: [simulation, mechanism, scale]
quality: 4
human_difficulty: 4
agent_difficulty: 3
automation: 3
reproducibility: 3
cost: 0
maturity: standard
platforms: [linux, macos, windows]
export: [mp4, png-sequence, exr-sequence, gif]
code_license: proprietary
price: Personal бесплатно (доход и финансирование до $200 тыс.), Pro $2310 в год или $210 в месяц
checked: 2026-10-14
---

# Unity

Игровой движок и редактор на C#. Для видео используется как «симулятор плюс камера»: сцена программируется, запись идёт пакетом Recorder. Классический пример — канал Primer, который в 2020–2023 годах делал так симуляции.

## Ссылки

- Официальный сайт: https://unity.com/
- GitHub: открытого кода редактора нет (справочный код C#: https://github.com/Unity-Technologies/UnityCsReference).
- Документация: https://docs.unity3d.com/ ([Recorder 5.1](https://docs.unity3d.com/Packages/com.unity.recorder@5.1/manual/index.html), [командная строка](https://docs.unity3d.com/6000.3/Documentation/Manual/EditorCommandLineArguments.html), [системные требования](https://docs.unity3d.com/6000.3/Documentation/Manual/system-requirements.html))
- Примеры, проверенные 2026-10-14:
  - [Overexplaining the binomial distribution (Primer, 2023-06-17)](https://www.youtube.com/watch?v=6YzrVUVO9M0) — в описании «Made with Unity». Треугольник Паскаля, независимые события, эксперимент; объекты движутся в одной сцене.
  - [How many people might ever exist, calculated (Primer, 2022-08-16)](https://www.youtube.com/watch?v=r6sa_fWQB_4) — в описании «Made with Unity».
  - [How To Catch A Cheater With Math (Primer, 2022-06-25)](https://www.youtube.com/watch?v=XTcP4oo4JI4) — в описании «Made with Unity and Manim»: сочетание двух инструментов, см. [manim-ce](manim-ce.md).
  - [Prototyping UI Toolkit with Unity CLI (Unity, 2026-10-05)](https://www.youtube.com/watch?v=SwuGB3quO2k) — агент строит интерфейс в редакторе через командную строку Unity, получает скриншоты и тесты Play mode.

## Что реально получается

- Симуляции и объекты с поведением: скрипты на C# управляют сотнями объектов. Primer строил так эволюционные модели.
- Камера и свет: непрерывная съёмка сцены, плавные траектории камеры; одна сцена без склеек.
- Запись: Recorder по документации «capture gameplay or a cinematic and save it as a video file, as an animated GIF, or as a sequence of separate image files». Есть накопление подкадров для motion blur и сходимости трассировки путей, вывод AOV в многослойный EXR и запись анимации персонажа или камеры.
- Рисование линий и формулы: не встроено, придётся писать свои компоненты. Primer использовал собственные инструменты в отдельном репозитории (в описаниях роликов: https://github.com/Helpsypoo/PrimerUnity; ссылка при проверке вернула 404).
- Голос: нет встроенной привязки к тексту; аудиотрек добавляется на таймлайн (Timeline) или в монтаже.
- Морфинг: shape keys, скелетная анимация, шейдеры; всё через Unity-механику.

## Слабые стороны

- Тарифы: Personal разрешён по странице цен «для игр и развлечений» и до $200 тыс. дохода и финансирования. Образовательный научный канал может не подпадать под «развлечения» (вопрос, см. «Неизвестно»).
- Recorder работает в режиме Play (по документации) и требует видеокарты и окна; в режиме `-nographics` кадры не отрисовываются (оценка).
- Редактор тяжёлый, сцены хранятся в проекте с кучей служебных файлов.
- Primer перешёл с Unity на Godot (2024–2025), см. [godot](godot.md). Причина в проверенных источниках не названа.

## Сложность

- Для человека (4 из 5): C#, сцены, префабы, пакеты. Полноценная работа через недели.
- Для агента (3 из 5): код на C# пишется текстом, редактор запускается пакетно (`-batchmode -quit -executeMethod Класс.Метод`). С 2026-10-05 у Unity есть CLI для агентов (по ролику). Но настройка сцены в редакторе и запись Recorder требуют запущенного редактора.

## Автоматизация и воспроизводимость

- Автоматизация (3 из 5): пакетный режим `-batchmode`, метод запуска `-executeMethod`, сборка из командной строки; Recorder — пакет с API записи (подробности не проверялись).
- Воспроизводимость (3 из 5): проект воспроизводит результат, но сцены и ассеты в служебных форматах. Режим записи с фиксированной частотой кадров в документации отдельно не проверялся.

## Платформа и оборудование

Редактор работает на Windows, macOS и Linux; рекомендуется не менее 8 ГБ ОЗУ. На Linux видео импортируется только в формате VP8, файловая система чувствительна к регистру. Полный список требований см. страницу Unity.

## Экспорт

Recorder 5.1.7: видеофайл, анимированный GIF, последовательность изображений, EXR с AOV, файл анимации, аудио. Пакет ставится отдельно от редактора. Список видеоформатов не проверялся.

## Стоимость

Проверено 2026-10-14 по [странице цен](https://unity.com/pricing) и [обновлению цен](https://unity.com/products/pricing-updates).

- Personal: бесплатно, для доходов и финансирования до $200 тыс. за 12 месяцев; 1000 ИИ-кредитов в месяц; заставка в Unity 6 по желанию.
- Pro: $2310 в год или $210 в месяц; обязательна выше $200 тыс.
- Enterprise: по запросу, обязательна выше $25 млн.
- Industry: по запросу; обязательна для проектов, не относящихся к играм и развлечениям, при общих финансах выше $1 млн.
- Образование: студенческий план бесплатный.
- Плата за запуск (Runtime Fee) отменена 2024-09-12, по словам Unity «was not implemented».
- Pro и Enterprise подорожали на 5% с 2026-01-12.

## Лицензия и права

- Код или программа: proprietary. Условия: [Unity Editor Software Terms](https://unity.com/legal/terms-of-service/software).
- Результат: в проверенных условиях редактора нет пункта о владении кадрами и роликами. «Industry Customer» определён как любое использование, не относящееся только к играм или развлечениям, порог $1 млн. Применимы ли эти категории к образовательному видео, не выяснил.
- Ассеты в комплекте: Asset Store и шаблоны идут по своим лицензиям; не проверялись.

## Активность и зрелость

Зрелость: `standard`. Страница Unity 6 называет «Unity 6.3 LTS» с поддержкой до декабря 2027; Unity 6.0 LTS поддерживается до октября 2026. Unity 6.5 вышла летом 2026 (CG Channel — 2026-06-22, форум — 2026-07-17), 6.7 в альфе; по этим вторичным данным. Развивает Unity Technologies.

## Когда брать и когда нет

- Брать: интерактивные симуляции с множеством объектов, если команда пишет на C# и есть опыт Unity.
- Не брать: если важны открытая лицензия и текстовый проект (см. [godot](godot.md)), если нужны красивые научные сцены без программирования.

## Источники

- [Планы и цены Unity](https://unity.com/pricing) — Personal, Pro, Enterprise, Industry. Проверено 2026-10-14.
- [Обновление цен](https://unity.com/products/pricing-updates) — $2310 / $210, отмена Runtime Fee, +5% с 2026-01-12. Проверено 2026-10-14.
- [Условия Unity Editor](https://unity.com/legal/terms-of-service/software) — порог $200 тыс., определение Industry Customer. Проверено 2026-10-14.
- [Unity 6](https://unity.com/releases/unity-6) — 6.3 LTS, поддержка. Проверено 2026-10-14.
- [Recorder 5.1.7](https://docs.unity3d.com/Packages/com.unity.recorder@5.1/manual/index.html) — возможности записи. Проверено 2026-10-14.
- [Командная строка редактора](https://docs.unity3d.com/6000.3/Documentation/Manual/EditorCommandLineArguments.html) — `-batchmode`, `-executeMethod`. Проверено 2026-10-14.
- [Системные требования](https://docs.unity3d.com/6000.3/Documentation/Manual/system-requirements.html). Проверено 2026-10-14.
- Описания роликов Primer на YouTube (ссылки выше): названия и фразы «Made with Unity» подтверждены. Проверено 2026-10-14.
- [Ролик о Unity CLI](https://www.youtube.com/watch?v=SwuGB3quO2k). Проверено 2026-10-14.

## Неизвестно

- Попадает ли образовательное видео на YouTube под «gaming and entertainment» в Personal.
- Номер текущей версии Unity и дата выхода 6.5 (источники расходятся).
- Точные списки форматов видео Recorder и поддержка фиксированной частоты кадров.
- Условия Asset Store и встроенных шаблонов.
- Причины перехода Primer на Godot в первоисточнике не найдены.
