# Пример пилота: файлы и проверка

Пример к [сценарию пилота](../script-en.md). Все числа сценария — отсюда. Проверено 2026-10-17 двумя способами: счёт по таблице вручную и скрипт. Результаты совпали.

## Файлы

- [toy-text.txt](toy-text.txt) — три верных сообщения семейного чата: всё, чему учится игрушка.
- [pairs.csv](pairs.csv) — таблица пар слов: слово, следующее слово, счёт, шанс. 8 строк.
- [sentences.csv](sentences.csv) — все 9 предложений, которые игрушка может написать, с шансом и пометкой «верно».
- [exam.csv](exam.csv) — экзамен: 6 вопросов, по 3 варианта, верный ответ.
- [scores.csv](scores.csv) — баллы честной и угадывающей игрушки по двум правилам оценки.

Скрипт генерирует pairs.csv, sentences.csv и scores.csv из toy-text.txt и exam.csv. Код — ниже, в разделе «Скрипт».

## Правила игрушки

- Слова — через пробел, точка в конце отбрасывается. Пары считаются только внутри предложения.
- Генерация: смотрит только на последнее слово; следующее выбирает с шансом, равным доле в таблице.
- Экзамен: игрушка читает весь вопрос. Знает ответ, если в тексте есть «вопрос + ответ» целиком. Иначе честная говорит «не знаю», угадывающая выбирает вариант наугад.

## Ручной счёт

Сделал агент по таблице, без скрипта, до запуска скрипта. Пересчёт человеком на бумаге не проводился: это шаг автора.

1. Пары. После «Mom», «Dad», «Sam» — «is», по 1. «is → at» 3, «at → the» 3. После «the»: store 1, gym 1, park 1. Итого 8 строк.
2. Предложения. От каждого имени путь один до «the», затем 3 варианта по 1/3. 3 имени × 3 = 9 предложений. Верных 3, ложных 6. Шанс ложного от любого имени — 2/3.
3. Ложное предложение из сценария: «Mom is at the gym.» Все его пары — «Mom is», «is at», «at the», «the gym» — есть в верных сообщениях.
4. Экзамен. Знакомы вопросы 1–3 про Mom, Dad, Sam. Незнакомы 4–6 про Grandma, Leo, Nina: их нет в чате.
   - Правило «верно +1, неверно 0, не знаю 0». Честная: 3. Угадывающая: 3 + 3 × 1/3 = 4 в среднем. Обходит честную, если угадала хотя бы раз: 1 − (2/3)³ = 19/27.
   - Правило «верно +1, неверно −1, не знаю 0». Честная: 3. Угадывающая: 3 + 3 × (1/3 − 2/3) = 2 в среднем. Обходит честную, если угадала 2 или 3 раза: 3 × (1/3)² × 2/3 + (1/3)³ = 6/27 + 1/27 = 7/27.

## Проверка скриптом

Скрипт перебирает все пути генерации и все 27 раскладов догадок; дроби точные. Запуск 2026-10-17, Python 3, стандартная библиотека, код выхода 0; повторный запуск на копиях дал те же файлы. Вывод:

```
sentences 9 true 3 false 6
 start Mom chance of a false sentence 2/3
 start Dad chance of a false sentence 2/3
 start Sam chance of a false sentence 2/3
exam 6 known 3 unknown 3
binary: right +1, wrong 0, IDK 0 | honest 3 | guesser average 4 | guesser beats honest in 19/27 of 27 combos
penalty: right +1, wrong -1, IDK 0 | honest 3 | guesser average 2 | guesser beats honest in 7/27 of 27 combos
```

Совпадение с ручным счётом: все числа.

## Ограничения

- Игрушка — не нейросеть. Пример показывает механизм ошибки, а не устройство настоящих моделей.
- Правило «верно +1, неверно −1» — частный случай предложения статьи Kalai и др.: порог уверенности t = 0,5, штраф t/(1 − t) = 1.
- Экзамен с вариантами ответа — упрощение; настоящие тесты разные.

## Источники

- C. E. Shannon, «A Mathematical Theory of Communication», Bell System Technical Journal, 1948, раздел 3 «The Series of Approximations to English». Цитата и описание метода сверены с текстом статьи 2026-10-17.
- A. T. Kalai, O. Nachum, S. S. Vempala, E. Zhang, «Why Language Models Hallucinate», arXiv:2509.04664, 2025. Аффилиации: OpenAI; Vempala — Georgia Tech. Цитаты сверены: аннотация; раздел 1.1; раздел 4.2 «Explicit confidence targets».
- T. B. Brown и др., «Language Models are Few-Shot Learners», arXiv:2005.14165, 2020: модель GPT-3 описана как авторегрессионная языковая модель.

## Скрипт

Файл check.py. Запуск: `python3 check.py <папка примера>`.

```python
# Second-method check of the pilot example. Reads toy-text.txt and exam.csv,
# writes pairs.csv, sentences.csv, scores.csv, prints the totals.
import csv, itertools, sys
from fractions import Fraction
from pathlib import Path

d = Path(sys.argv[1])
lines = [l.strip().rstrip('.') for l in (d / 'toy-text.txt').read_text().splitlines() if l.strip()]
sents = [l.split() for l in lines]

pairs = {}
for s in sents:
    for a, b in zip(s, s[1:]):
        pairs.setdefault(a, {}).setdefault(b, 0)
        pairs[a][b] += 1
with open(d / 'pairs.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['word', 'next_word', 'count', 'chance'])
    for a in pairs:
        tot = sum(pairs[a].values())
        for b, c in pairs[a].items():
            w.writerow([a, b, c, f'{c}/{tot}'])

# Every sentence the toy can write, starting from each first word.
def walk(path, p):
    nxt = pairs.get(path[-1])
    if not nxt:
        yield path, p
        return
    tot = sum(nxt.values())
    for b, c in nxt.items():
        yield from walk(path + [b], p * Fraction(c, tot))

true = {' '.join(s) for s in sents}
rows = []
for start in dict.fromkeys(s[0] for s in sents):
    for path, p in walk([start], Fraction(1)):
        rows.append((start, ' '.join(path), p, ' '.join(path) in true))
with open(d / 'sentences.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['start', 'sentence', 'chance', 'true'])
    for start, s, p, t in rows:
        w.writerow([start, s + '.', str(p), 'yes' if t else 'no'])
print('sentences', len(rows), 'true', sum(r[3] for r in rows), 'false', sum(not r[3] for r in rows))
for start in dict.fromkeys(r[0] for r in rows):
    print(' start', start, 'chance of a false sentence', sum(p for s0, _, p, t in rows if s0 == start and not t))

# Exam: the honest toy says "I don't know" when it never saw the question;
# the guesser picks one of the options at random. Enumerate every guess.
exam = list(csv.DictReader(open(d / 'exam.csv')))
known = [q for q in exam if q['question'] + ' ' + q['answer'] in true]
unknown = [q for q in exam if q not in known]
print('exam', len(exam), 'known', len(known), 'unknown', len(unknown))
rules = {'binary: right +1, wrong 0, IDK 0': 0, 'penalty: right +1, wrong -1, IDK 0': -1}
out = []
for rule, wrong in rules.items():
    honest = len(known)
    combos = list(itertools.product(*[q['options'].split('|') for q in unknown]))
    scores = [len(known) + sum(1 if g == q['answer'] else wrong for g, q in zip(c, unknown)) for c in combos]
    avg = Fraction(sum(scores), len(scores))
    beats = Fraction(sum(s > honest for s in scores), len(scores))
    out.append((rule, honest, avg, beats, len(combos)))
    print(rule, '| honest', honest, '| guesser average', avg, '| guesser beats honest in', beats, 'of', len(combos), 'combos')
with open(d / 'scores.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['rule', 'honest_score', 'guesser_average', 'guesser_beats_honest_share', 'guess_combinations'])
    for r in out:
        w.writerow([r[0], r[1], str(r[2]), str(r[3]), r[4]])
```
