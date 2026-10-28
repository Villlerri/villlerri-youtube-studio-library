# Приложение прежнего направления: код прогона чеков

Код прогона 20 чеков локальной моделью и подсчёта оценок. Направление «бесплатный ИИ на обычном компьютере», 2026-10-17. Результаты — в [pilot/example/results.md](pilot/example/results.md).

## Прогон чеков

Запрос к запущенному `llama-server` и сохранение ответов. Запуск: `python3 run_receipts.py <порт> <метка> <папка> nothink prompt.txt`. Итог, который печатает этот скрипт, — черновой: он не разбирает строки со сдвигом. Оценки в документах — из `score.py` ниже.

```python
"""Send the 4 receipt batches to a running llama-server, save raw answers and score them.

usage: python3 run_receipts.py <port> <model_label> <out_dir> [think]
"""
import csv, json, re, sys, time, urllib.request, pathlib

port, label, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
think = 'think' in sys.argv[4:]
pfile = next((a for a in sys.argv[4:] if a.startswith('prompt')), 'prompt.txt')
EX = pathlib.Path('/srv/projects/youtube-studio-library/worktrees/youtube-2-work/docs/pilots/ai-tutorials/example/receipts')
prompt = (EX / pfile).read_text()
text = (EX / 'receipts.txt').read_text()
batches = re.split(r'#{10} BATCH \d+ #{10}\n', text)[1:]
key = {r['receipt']: r for r in csv.DictReader(open(EX / 'answer-key.csv'))}
receipt_text = {m.group(1): m.group(2) for m in re.finditer(r'=== Receipt (\d\d) ===\n(.*?)(?=\n=== Receipt|\n#{10}|\Z)', text, re.S)}
out.mkdir(parents=True, exist_ok=True)

def ask(content):
    body = {'messages': [{'role': 'user', 'content': content}], 'temperature': 0, 'seed': 1,
            'max_tokens': 3000 if think else 900, 'chat_template_kwargs': {'enable_thinking': think}}
    req = urllib.request.Request(f'http://127.0.0.1:{port}/v1/chat/completions', json.dumps(body).encode(),
                                 {'Content-Type': 'application/json'})
    t = time.time()
    d = json.load(urllib.request.urlopen(req, timeout=1800))
    return d, time.time() - t

def norm(s):
    return re.sub(r'[^a-z0-9& ]', '', s.lower()).replace('&', 'and').split()

def money(s):
    s = s.replace('$', '').replace(',', '').strip()
    try:
        return round(float(s), 2)
    except ValueError:
        return None

rawp = out / f'{label}-raw.json'
runs = json.loads(rawp.read_text()) if rawp.exists() else []
done = {r['batch'] for r in runs}
for i, b in enumerate(batches, 1):
    if i in done:
        continue
    d, secs = ask(prompt + '\n' + b.strip())
    msg = d['choices'][0]['message']
    runs.append({'batch': i, 'seconds': round(secs, 1), 'content': msg.get('content'),
                 'reasoning': msg.get('reasoning_content'), 'usage': d.get('usage'), 'timings': d.get('timings')})
    runs.sort(key=lambda r: r['batch'])
    rawp.write_text(json.dumps(runs, indent=1, ensure_ascii=False))
    print(f'batch {i}: {secs:.1f}s', d.get('timings', {}).get('predicted_per_second'), flush=True)
rows = []
for run in runs:
    for line in csv.reader((run.get('content') or '').splitlines()):
        if len(line) >= 4 and re.fullmatch(r'\d{1,2}', line[0].strip()):
            rows.append([c.strip() for c in line[:5]] + [''] * (5 - len(line[:5])))
if len(runs) < len(batches):
    sys.exit(3)

got = {}
for r in rows:
    got.setdefault(r[0].zfill(2), r)
score = []
for n, k in key.items():
    r = got.get(n)
    if not r:
        score.append({'receipt': n, 'answered': 0, 'vendor_ok': 0, 'date_ok': 0, 'total_ok': 0,
                      'model_vendor': '', 'model_date': '', 'model_total': '', 'model_total_line': '',
                      'line_check': 'missing', 'right_total': k['total'], 'trap': k['trap']})
        continue
    kv, mv = norm(k['vendor']), norm(r[1])
    vendor_ok = int(bool(kv) and all(w in mv for w in kv if w not in ('the', 'and')))
    date_ok = int(r[2] == k['date'])
    total_ok = int(money(r[3]) is not None and money(r[3]) == money(k['total']))
    quoted = r[4]
    src = receipt_text.get(n, '')
    in_receipt = bool(quoted) and quoted.lower() in src.lower()
    amount = money(r[3])
    has_amount = amount is not None and (f'{abs(amount):.2f}' in quoted)
    line_check = 'pass' if in_receipt and has_amount else ('line not in receipt' if not in_receipt else 'number not in line')
    score.append({'receipt': n, 'answered': 1, 'vendor_ok': vendor_ok, 'date_ok': date_ok, 'total_ok': total_ok,
                  'model_vendor': r[1], 'model_date': r[2], 'model_total': r[3], 'model_total_line': quoted,
                  'line_check': line_check, 'right_total': k['total'], 'trap': k['trap']})
with open(out / f'{label}-scored.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(score[0]))
    w.writeheader(); w.writerows(score)
tot = lambda f: sum(s[f] for s in score)
caught = sum(1 for s in score if s['answered'] and not s['total_ok'] and s['line_check'] != 'pass')
print(json.dumps({'model': label, 'answered': tot('answered'), 'vendor_ok': tot('vendor_ok'), 'date_ok': tot('date_ok'),
                  'total_ok': tot('total_ok'), 'wrong_totals_caught_by_line_check': caught,
                  'seconds': round(sum(r['seconds'] for r in runs), 1)}))
```

## Подсчёт оценок

Та же логика, что у страницы check.html. Запуск: `python3 score.py <ответы.json> <разбор.csv>`.

```python
"""Score raw model answers the same way check.html does. Line i of the answer is receipt i.

usage: python3 score.py <raw.json> <out.csv>   (prints a JSON summary)
"""
import csv, json, re, sys

EX = '/srv/projects/youtube-studio-library/worktrees/youtube-2-work/docs/pilots/ai-tutorials/example/receipts'
KEY = list(csv.DictReader(open(f'{EX}/answer-key.csv')))
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def split_csv(line):
    out, cur, q = [], '', False
    for ch in line:
        if ch == '"': q = not q
        elif ch == ',' and not q: out.append(cur.strip()); cur = ''
        else: cur += ch
    out.append(cur.strip()); return out

def words(s):
    return [w for w in re.sub(r'[^a-z0-9 ]', ' ', s.lower().replace('&', ' and ')).split() if w not in ('the', 'and')]

def vendor_ok(got, want):
    g = words(got); return all(any(w in x for x in g) for w in words(want))

def dates_in(t):
    t = t.lower(); f = set()
    for m in re.finditer(r'(\d{4})-(\d{1,2})-(\d{1,2})', t): f.add(f'{m[1]}-{int(m[2]):02d}-{int(m[3]):02d}')
    for m in re.finditer(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', t):
        y = '20' + m[3] if len(m[3]) == 2 else m[3]; f.add(f'{y}-{int(m[1]):02d}-{int(m[2]):02d}')
    for m in re.finditer(r'([a-z]{3,9})\.?\s+(\d{1,2}),?\s+(\d{4})', t):
        i = next((k for k, x in enumerate(MONTHS) if x.startswith(m[1][:3])), None)
        if i is not None: f.add(f'{m[3]}-{i + 1:02d}-{int(m[2]):02d}')
    return f

def money(s):
    s = re.sub(r'[$,\s]', '', s or '')
    return f'{float(s):.2f}' if re.fullmatch(r'-?\d+(\.\d+)?', s) else None

def amounts_in(t):
    t = re.sub(r',(?=\d{3}\b)', '', t)
    return {f'{float(re.sub(r"[$ ]", "", m)):.2f}' for m in re.findall(r'-?\$?\s?\d+\.\d{2}', t)}

runs = json.load(open(sys.argv[1]))
lines = [l.strip() for r in sorted(runs, key=lambda r: r['batch']) for l in (r['content'] or '').splitlines()
         if l.strip() and re.search(r'\d', l)]
rows, s = [], dict(format=0, total_col=0, total_any=0, date_any=0, vendor_any=0)
for i, k in enumerate(KEY):
    l = lines[i] if i < len(lines) else ''
    c = split_csv(l) if l else []
    want = f"{float(k['total']):.2f}"
    num_ok = bool(c) and re.fullmatch(r'\d{1,2}', c[0]) is not None and int(c[0]) == int(k['receipt'])
    fmt = len(c) == 5 and num_ok and re.fullmatch(r'\d{4}-\d{2}-\d{2}', c[2]) is not None and money(c[3]) is not None
    r = dict(receipt=k['receipt'], answer_line=l, format_ok=int(fmt), total_col_ok=int(len(c) > 3 and money(c[3]) == want),
             total_any_ok=int(want in amounts_in(l)), date_any_ok=int(k['date'] in dates_in(l)),
             vendor_ok=int(vendor_ok(l, k['vendor'])), right_total=want, right_date=k['date'], trap=k['trap'])
    for a, b in [('format', 'format_ok'), ('total_col', 'total_col_ok'), ('total_any', 'total_any_ok'), ('date_any', 'date_any_ok'), ('vendor_any', 'vendor_ok')]:
        s[a] += r[b]
    rows.append(r)
with open(sys.argv[2], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
s['lines'] = len(lines); s['seconds'] = round(sum(r['seconds'] for r in runs), 1)
s['gen_tok_s'] = [round(r['timings']['predicted_per_second'], 1) for r in sorted(runs, key=lambda r: r['batch'])]
print(json.dumps(s))
```
