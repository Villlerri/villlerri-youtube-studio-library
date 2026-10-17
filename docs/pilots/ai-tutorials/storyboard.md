# Раскадровка пилота

К [сценарию](script-en.md). Подача 1 «Countable AI»: лист в клетку, карандаш, счёт чёрточками, кубик, стикер. Карточка источника — из подачи 3. 1920×1080, 30 кадров в секунду. Время — по тексту при темпе около 150 слов в минуту, с паузами на счёт и кубик; итог около 8:45. Точное время задаст голос ElevenLabs.

Общие правила кадра:
- Один лист без склеек; новое дописывается на глазах, старое сдвигается вверх.
- Субтитры — Atkinson Hyperlegible, внизу, белым по тёмной плашке.
- Рукописный текст — Patrick Hand. Красный #C23B2A — только для ошибки.
- В углу всё видео: «toy model».

## 0:00–0:40 Начало

1. 0:00. Чистый лист. Карандаш пишет «Paris is the capital of Italy.» Красный круг вокруг «Italy», подпись «false».
2. 0:12. Слово «hallucination» в кавычках, зачёркнуто одной линией; рядом «not a mystery».
3. 0:22. Лист сворачивается в угол; новый лист, сверху «one sheet · one pencil · one die».
4. 0:32. Стикер «toy» приклеивается в угол листа.

## 0:40–1:20 Игрушка

5. 0:40. Карандаш пишет три предложения. Галочка у каждого.
6. 0:52. Подпись над ними: «training text — all true».
7. 1:00. Рамка вокруг последнего слова строки; подпись «reads only this».
8. 1:10. Заголовок таблицы: «word → next word · count».

## 1:20–3:15 Считаем вручную

9. 1:20. Стрелки от «Paris», «Rome», «Lima» к «is»; три строки таблицы, по чёрточке.
10. 1:38. Строки «is → the ||| », «the → capital |||», «capital → of |||».
11. 1:57. Три стрелки от каждого «of» к France, Italy, Peru; по одной чёрточке. Обвести блок.
12. 2:11. Итог: «9 rows». Подпись «check it: under a minute».
13. 2:20. Строка «Paris is the capital of ___». Рамка только вокруг «of».
14. 2:29. Рядом таблица «1–2 France · 3–4 Italy · 5–6 Peru». Бросок кубика, выпало 4.
15. 2:38. Вписано «Italy», красный круг, «false».
16. 2:47. Подчеркнуть пять пар: каждая с галочкой «seen in true text».
17. 3:01. Сетка 3×3 возможных предложений: три зелёных галочки, шесть красных крестов. Итог: «false: 2 in 3».

## 3:15–4:10 Карточка источника 1948

18. 3:15. Наезжает карточка картотеки из подачи 3: «1948 · C. E. Shannon · A Mathematical Theory of Communication · section 3».
19. 3:30. Схема Шеннона: открытая книга, слово, стрелка к следующему слову, другая страница.
20. 3:45. Цитата печатается машинкой, Courier Prime, дословно; подпись «his result, as printed».
21. 4:05. Штамп «NONSENSE». Подпись: «every pair is real English».

## 4:10–7:20 Настоящие модели

22. 4:21. Лист: «toy reads 1 word» против «real models read the whole question». Рамка расширяется на всю строку; «Italy» сменяется на «France».
23. 4:52. Плашка: «not a table of counts — a neural network trained to predict the next piece of text». Ссылка внизу: «Brown et al., 2020».
24. 5:13. Карточка источника: «2025 · Kalai, Nachum, Vempala, Zhang · Why Language Models Hallucinate · arXiv:2509.04664». Два пункта: «1. rare facts», «2. grading».
25. 5:29. Цитата о днях рождения печатается машинкой, дословно.
26. 5:50. Строка «Oslo is the capital of ___». В таблице строки «Oslo» нет: пустое место, знак вопроса.
27. 6:06. Лист экзамена: 6 вопросов, по 3 варианта. Три первых — галочки «seen», три последних — «never seen».
28. 6:22. Две колонки: «honest» и «guesser». У честной на вопросах 4–6 «I don't know».
29. 6:38. Правило «right +1 · wrong 0 · IDK 0». Счёт: honest 3, guesser «3 + 3 × ⅓ = 4 on average». Подпись «guesser wins in 19 of 27».
30. 6:54. Цитата «language models are optimized to be good test-takers…» с карточкой источника.
31. 7:04. Правило зачёркнуто, новое: «right +1 · wrong −1 · IDK 0». Счёт: honest 3, guesser «2 on average».
32. 7:15. Подпись: «the paper's proposal: state the confidence needed, penalize wrong answers».

## 7:20–8:10 Что упрощено

33. 7:20. Жёлтый стикер «What this toy leaves out»; пять пунктов из сценария пишутся по одному.
34. 7:58. Под стикером: «what carries over: always continue + rewarded for guessing → fluent false statements».

## 8:10–8:45 Что делать

35. 8:10. Список «date · name · number · quote · reference» с пометкой «check against a source».
36. 8:28. Возврат к кадру 15: «Paris is the capital of Italy.», красный круг. Подпись «fluent ≠ true».
37. 8:39. Финальный лист: «files below: sheet · table · exam · check script». Название канала.

## Shorts из пилота

- «Every word pair was true. The sentence was false.» — кадры 13–17, 40 секунд.
- «Why guessing wins on tests» — кадры 27–31, 45 секунд.

Вертикальный кадр 1080×1920 из тех же листов. Стикер «simplified» остаётся.
