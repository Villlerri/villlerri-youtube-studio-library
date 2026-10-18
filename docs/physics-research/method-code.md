# Код исследования

Скрипты исследования в порядке запуска. Проект не хранит файлы кода, поэтому код здесь целиком. Как повторить — [method.md](method.md#как-повторить).

Окружение: Python 3.14, `pip install yt-dlp==2026.8.19 pytrends==4.9.2 numpy pillow`, ffmpeg 6. Каждый скрипт лежит в `tmp/research/` и пишет сырые данные в `tmp/research/raw/`, таблицы — в `docs/physics-research/data/`. Запуск: `python -I tmp/research/<скрипт>`.

## collect.py

Сбор выдачи поиска, каналов-ориентиров и каналов из выдачи.

```python
"""Collect public YouTube search samples and channel listings for the physics study.
Run: tmp/venv/bin/python -I tmp/research/collect.py [search|seeds|found|all]"""
import json, sys, time, urllib.parse, concurrent.futures as cf, os, datetime
import yt_dlp
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else HERE; RAW = os.path.join(HERE, 'raw')
FILTERS = {'month': 'EgQIBBAB', 'any': 'EgIQAQ%3D%3D'}  # upload date this month + video; video only (relevance)

def ydl(n):
    return yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': 'in_playlist', 'playlistend': n,
                             'skip_download': True, 'extractor_args': {'youtubetab': {'approximate_date': ['']}},
                             'socket_timeout': 30})

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def search(q, sp, n=40):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={sp}&hl=en&gl=US"
    err = None
    for a in range(3):
        try:
            info = ydl(n).extract_info(url, download=False)
            return [{k: e.get(k) for k in ('id', 'title', 'channel', 'channel_id', 'view_count', 'duration', 'timestamp')}
                    for e in info.get('entries') or [] if e.get('id') and len(e['id']) == 11]
        except Exception as ex:
            err = str(ex); time.sleep(5)
    return {'error': err}

def tab(key, kind, n):
    base = f"https://www.youtube.com/{key}" if key.startswith('@') else f"https://www.youtube.com/channel/{key}"
    err = None
    for a in range(3):
        try:
            info = ydl(n).extract_info(f"{base}/{kind}", download=False)
            ents = [{k: e.get(k) for k in ('id', 'title', 'view_count', 'duration', 'timestamp')} for e in info.get('entries') or []]
            return {'channel': info.get('channel'), 'channel_id': info.get('channel_id'), 'subs': info.get('channel_follower_count'),
                    'url': info.get('channel_url') or base, 'entries': ents}
        except Exception as ex:
            err = str(ex)
            if 'does not have a' in err: break
            time.sleep(5)
    return {'error': err}

def channel(key, nv, ns):
    r = {'key': key, 'measured': now()}
    v = tab(key, 'videos', nv)
    if 'error' in v: r['error'] = v['error']
    else: r.update({'channel': v['channel'], 'channel_id': v['channel_id'], 'subs': v['subs'], 'url': v['url'], 'videos': v['entries']})
    if ns:
        s = tab(key, 'shorts', ns)
        r['shorts'] = s.get('entries') if 'entries' in s else {'error': s.get('error')}
    return r

def load(p): return json.load(open(p)) if os.path.exists(p) else {}

def run_channels(keys, path, nv, ns):
    C = load(path)
    todo = [k for k in keys if k not in C or 'error' in C[k]]
    print('channels to fetch', len(todo), flush=True)
    with cf.ThreadPoolExecutor(4) as ex:
        for i, (k, r) in enumerate(zip(todo, ex.map(lambda k: channel(k, nv, ns), todo))):
            C[k] = r
            if i % 25 == 0:
                json.dump(C, open(path, 'w'), ensure_ascii=False); print('channels', i, k, r.get('error', '')[:80], flush=True)
    json.dump(C, open(path, 'w'), ensure_ascii=False)

def main():
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    seeds = json.load(open(os.path.join(HERE, 'seeds.json')))
    sp_path = os.path.join(RAW, 'search.json'); S = load(sp_path)
    if what in ('search', 'all'):
        jobs = [(c, q, f) for c, q in seeds['queries'] for f in FILTERS if f"{f}|{q}" not in S]
        with cf.ThreadPoolExecutor(4) as ex:
            for (c, q, f), r in zip(jobs, ex.map(lambda j: search(j[1], FILTERS[j[2]]), jobs)):
                S[f"{f}|{q}"] = {'cluster': c, 'query': q, 'filter': f, 'measured': now(), 'results': r}
                print('search', f, q, len(r) if isinstance(r, list) else r, flush=True)
        json.dump(S, open(sp_path, 'w'), ensure_ascii=False)
    if what in ('seeds', 'all'):
        run_channels([c[0] for c in seeds['channels'] if c[1] != 'skip'], os.path.join(RAW, 'seeds.json'), 300, 60)
    if what in ('found', 'all'):
        keys = set()
        for v in S.values():
            if isinstance(v['results'], list): keys.update(e['channel_id'] for e in v['results'] if e.get('channel_id'))
        run_channels(sorted(keys), os.path.join(RAW, 'found.json'), 30, 0)
    print('done', what, flush=True)

main()
```

## collect_rev.py

Второй проход по каналам из выдачи в обратном порядке.

```python
"""Second fetcher for discovered channels, reverse order, separate file. Run: tmp/venv/bin/python -I tmp/research/collect_rev.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x', 'none']
src = open(os.path.join(HERE, 'collect.py')).read(); src = src[:src.rindex('main()')]
exec(compile(src, 'collect.py', 'exec'))
S = json.load(open(os.path.join(RAW, 'search.json')))
keys = set()
for v in S.values():
    if isinstance(v['results'], list): keys.update(e['channel_id'] for e in v['results'] if e.get('channel_id'))
keys = sorted(keys, reverse=True)[:1100]
run_channels(keys, os.path.join(RAW, 'found_rev.json'), 30, 0)
print('done rev', flush=True)
```

## suggest.py

Подсказки YouTube.

```python
"""YouTube search suggestions (autocomplete), en/US, for physics stems and stem + letter.
Suggestions show that a query exists in autocomplete, not how often it is searched.
Run: tmp/venv/bin/python -I tmp/research/suggest.py"""
import json, os, time, string, urllib.parse, urllib.request, datetime, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
STEMS = {
 'everyday': ['why is the sky', 'why does ice', 'how does a microwave', 'why do we', 'everyday physics', 'why does water'],
 'light': ['how does light', 'why is light', 'how do lasers', 'why do we see color', 'rainbow'],
 'sound': ['how does sound', 'sound waves', 'resonance', 'why does sound'],
 'magnet': ['how do magnets', 'magnets', 'magnetic field', 'electromagnet'],
 'electric': ['how does electricity', 'what is voltage', 'electricity', 'lightning'],
 'energy': ['what is energy', 'entropy', 'nuclear fusion', 'thermodynamics', 'perpetual motion'],
 'gravity': ['how does gravity', 'gravity', 'why does gravity'],
 'space': ['black hole', 'how big is the universe', 'what is inside a black hole', 'neutron star', 'dark matter', 'the universe'],
 'relativity': ['time dilation', 'theory of relativity', 'speed of light', 'time travel', 'why can\'t we go faster than light'],
 'quantum': ['quantum physics', 'quantum entanglement', 'double slit experiment', 'quantum'],
 'paradox': ['physics paradox', 'paradox', 'what happens if', 'what would happen if'],
 'mechanics': ['how do airplanes fly', 'why do planes', 'gyroscope', 'newton\'s laws', 'friction'],
 'matter': ['superconductor', 'antimatter', 'absolute zero', 'what is an atom', 'states of matter'],
 'general': ['physics', 'physics explained', 'physics experiment', 'physics simulation', 'how does', 'why does'],
}
def suggest(q):
    url = 'https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&hl=en&gl=us&q=' + urllib.parse.quote(q)
    for a in range(3):
        try:
            t = urllib.request.urlopen(url, timeout=20).read().decode('utf-8', 'replace')
            data = json.loads(t[t.index('(') + 1:t.rindex(')')])
            return [s[0] for s in data[1]]
        except Exception as ex:
            err = str(ex); time.sleep(3)
    return {'error': err}
def main():
    jobs = [(c, s + (' ' + l if l else '')) for c, ss in STEMS.items() for s in ss for l in [''] + list(string.ascii_lowercase)]
    R = {'measured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'rows': []}
    with cf.ThreadPoolExecutor(4) as ex:
        for (c, q), r in zip(jobs, ex.map(lambda j: suggest(j[1]), jobs)):
            R['rows'].append({'cluster': c, 'query': q, 'suggestions': r})
    json.dump(R, open(os.path.join(RAW, 'suggest.json'), 'w'), ensure_ascii=False)
    print('done', len(jobs), sum(1 for r in R['rows'] if isinstance(r['suggestions'], dict)), 'errors')
main()
```

## trends.py

Google Trends, первый проход (якорь physics).

```python
"""Google Trends, YouTube Search, US, weekly 5 years. Anchor 'physics' in every batch of 5.
Run: tmp/venv/bin/python -I tmp/research/trends.py"""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
ANCHOR = 'physics'
TERMS = {
 'space': ['black hole', 'how big is the universe', 'neutron star', 'big bang', 'dark matter', 'wormhole', 'multiverse', 'james webb telescope'],
 'quantum': ['quantum physics', 'quantum entanglement', 'double slit experiment', 'schrodinger cat', 'quantum computer'],
 'relativity': ['time dilation', 'theory of relativity', 'speed of light', 'time travel', 'fourth dimension'],
 'light': ['why is the sky blue', 'how lasers work', 'rainbow', 'optical illusion'],
 'magnet': ['how magnets work', 'magnetic field', 'electromagnet'],
 'electric': ['how electricity works', 'tesla coil', 'lightning'],
 'energy': ['entropy', 'nuclear fusion', 'thermodynamics', 'perpetual motion', 'nuclear reactor'],
 'sound': ['sound waves', 'resonance', 'sonic boom'],
 'mechanics': ['how airplanes fly', 'gyroscope', 'newton laws of motion', 'gravity'],
 'matter': ['superconductor', 'antimatter', 'absolute zero', 'plasma'],
 'general': ['physics experiment', 'physics simulation', 'science experiment', 'physics explained'],
}
def main():
    out = os.path.join(RAW, 'trends.json'); R = json.load(open(out)) if os.path.exists(out) else {}
    py = TrendReq(hl='en-US', tz=0, timeout=(10, 30), retries=0)
    flat = [(c, t) for c, ts in TERMS.items() for t in ts]
    batches = [flat[i:i + 4] for i in range(0, len(flat), 4)]
    for b in batches:
        key = '|'.join(t for _, t in b)
        if key in R: continue
        kws = [ANCHOR] + [t for _, t in b]
        for a in range(4):
            try:
                py.build_payload(kws, timeframe='today 5-y', geo='US', gprop='youtube')
                df = py.interest_over_time()
                R[key] = {'measured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                          'clusters': {t: c for c, t in b}, 'kws': kws,
                          'dates': [d.strftime('%Y-%m-%d') for d in df.index],
                          'series': {k: [int(x) for x in df[k].tolist()] for k in kws}}
                print('ok', key, flush=True); break
            except Exception as ex:
                print('err', key, str(ex)[:120], flush=True); time.sleep(60 * (a + 1))
        json.dump(R, open(out, 'w')); time.sleep(20)
    # countries for the anchor, YouTube search worldwide, last 12 months
    if 'regions' not in R:
        for a in range(4):
            try:
                py.build_payload([ANCHOR, 'science'], timeframe='today 12-m', geo='', gprop='youtube')
                df = py.interest_by_region(resolution='COUNTRY', inc_low_vol=False)
                R['regions'] = {'measured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                                'rows': {i: {k: int(df.loc[i, k]) for k in df.columns} for i in df.index}}
                print('ok regions', flush=True); break
            except Exception as ex:
                print('err regions', str(ex)[:120], flush=True); time.sleep(60 * (a + 1))
        json.dump(R, open(out, 'w'))
    print('done', flush=True)
main()
```

## trends2.py

Google Trends, второй проход для редких терминов (якорь speed of light).

```python
"""Second Trends pass: long-tail terms against anchor 'speed of light'; then countries for 'physics' worldwide.
Run: tmp/venv/bin/python -I tmp/research/trends2.py"""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
ANCHOR = 'speed of light'
TERMS = [('light','why is the sky blue'),('light','how lasers work'),('light','optical illusion'),('magnet','how magnets work'),
 ('magnet','magnetic field'),('magnet','electromagnet'),('electric','how electricity works'),('electric','tesla coil'),
 ('mechanics','how airplanes fly'),('mechanics','newton laws of motion'),('matter','superconductor'),('general','physics simulation'),
 ('general','physics experiment'),('quantum','schrodinger cat'),('relativity','theory of relativity'),('relativity','fourth dimension'),
 ('energy','perpetual motion'),('mechanics','gyroscope'),('relativity','time dilation'),('matter','absolute zero'),
 ('space','neutron star'),('energy','nuclear fusion'),('space','how big is the universe'),('quantum','double slit experiment'),
 ('general','physics explained'),('light','why do we see colors'),('everyday','how does a microwave work'),('everyday','why does ice float'),
 ('energy','what is energy'),('gravity','how gravity works'),('sound','sound waves'),('energy','entropy'),('quantum','quantum physics'),
 ('everyday','everyday physics'),('paradox','physics paradox'),('electric','static electricity')]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
def main():
    out = os.path.join(RAW, 'trends2.json'); R = json.load(open(out)) if os.path.exists(out) else {}
    py = TrendReq(hl='en-US', tz=0, timeout=(10, 30), retries=0)
    for i in range(0, len(TERMS), 4):
        b = TERMS[i:i + 4]; key = '|'.join(t for _, t in b)
        if key in R: continue
        kws = [ANCHOR] + [t for _, t in b]
        for a in range(4):
            try:
                py.build_payload(kws, timeframe='today 5-y', geo='US', gprop='youtube'); df = py.interest_over_time()
                R[key] = {'measured': now(), 'clusters': {t: c for c, t in b}, 'kws': kws, 'dates': [d.strftime('%Y-%m-%d') for d in df.index],
                          'series': {k: [int(x) for x in df[k].tolist()] for k in kws}}
                print('ok', key, flush=True); break
            except Exception as ex:
                print('err', key, str(ex)[:120], flush=True); time.sleep(60 * (a + 1))
        json.dump(R, open(out, 'w')); time.sleep(20)
    if 'regions' not in R:
        py2 = TrendReq(hl='en-US', tz=0, timeout=(10, 30), retries=0)
        for a in range(4):
            try:
                py2.build_payload(['physics'], timeframe='today 12-m', geo='', gprop='youtube')
                df = py2.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
                R['regions'] = {'measured': now(), 'rows': {i: {'physics': int(df.loc[i, 'physics']), 'code': df.loc[i, 'geoCode']} for i in df.index}}
                print('ok regions', len(df), flush=True); break
            except Exception as ex:
                print('err regions', str(ex)[:120], flush=True); time.sleep(60 * (a + 1))
        json.dump(R, open(out, 'w'))
    print('done', flush=True)
main()
```

## analyze_trends.py

Сводка Trends.

```python
"""Trends metrics relative to the anchor 'physics'. Run: tmp/venv/bin/python -I tmp/research/analyze_trends.py"""
import json, os, csv, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
R = json.load(open(os.path.join(RAW, 'trends.json')))
rows = []
for key, b in R.items():
    if key == 'regions': continue
    d = b['dates']; a = b['series']['physics']
    for t, c in b['clusters'].items():
        s = b['series'][t]
        last, prev, old = s[-52:], s[-104:-52], s[-156:-104]
        al = st.mean(a[-52:])
        mon = {}
        for dt, v in zip(d, s): mon.setdefault(int(dt[5:7]), []).append(v)
        mm = {m: st.mean(v) for m, v in mon.items()}
        mean_all = st.mean(s)
        rows.append({'term': t, 'cluster': c, 'measured': b['measured'][:10], 'weeks': len(s), 'first_week': d[0], 'last_week': d[-1],
                     'mean_52w_vs_anchor_physics': round(st.mean(last) / al, 3) if al else '',
                     'mean_52w_raw': round(st.mean(last), 1), 'anchor_mean_52w_raw': round(al, 1),
                     'change_52w_vs_prev_52w': round(st.mean(last) / st.mean(prev) - 1, 3) if st.mean(prev) else '',
                     'change_52w_vs_2y_before': round(st.mean(last) / st.mean(old) - 1, 3) if st.mean(old) else '',
                     'peak_month': max(mm, key=mm.get), 'low_month': min(mm, key=mm.get),
                     'seasonal_amplitude': round((max(mm.values()) - min(mm.values())) / mean_all, 2) if mean_all else '',
                     'max_week': d[s.index(max(s))], 'max_week_value': max(s)})
rows.sort(key=lambda r: -(r['mean_52w_vs_anchor_physics'] or 0))
with open(os.path.join(OUT, 'trends.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['term']:28} {r['cluster']:10} rel={r['mean_52w_vs_anchor_physics']:<6} yoy={r['change_52w_vs_prev_52w']:<7} 2y={r['change_52w_vs_2y_before']:<7} peak={r['peak_month']:>2} low={r['low_month']:>2} amp={r['seasonal_amplitude']} max={r['max_week']}")
reg = R.get('regions')
if reg:
    rr = sorted(reg['rows'].items(), key=lambda x: -x[1]['physics'])[:20]
    print('regions', reg['measured']); print([(k, v['physics'], v['science']) for k, v in rr])
    with open(os.path.join(OUT, 'trends-regions.csv'), 'w', newline='') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(['country', 'physics_share_index', 'science_share_index', 'measured'])
        for k, v in sorted(reg['rows'].items(), key=lambda x: -x[1]['physics']):
            if v['physics'] or v['science']: w.writerow([k, v['physics'], v['science'], reg['measured'][:10]])
```

## analyze_trends2.py

Пересчёт второго прохода на шкалу physics.

```python
"""Merge Trends passes onto one scale: interest relative to 'physics' (YouTube search, US, last 52 weeks).
Pass 2 terms are measured against 'speed of light' and multiplied by speed of light's ratio to 'physics' from pass 1.
Run: tmp/venv/bin/python -I tmp/research/analyze_trends2.py"""
import json, os, csv, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
P1 = json.load(open(os.path.join(RAW, 'trends.json'))); P2 = json.load(open(os.path.join(RAW, 'trends2.json')))
def metrics(d, s, a):
    al = st.mean(a[-52:]); last, prev, old = s[-52:], s[-104:-52], s[-156:-104]
    mon = {}
    for dt, v in zip(d, s): mon.setdefault(int(dt[5:7]), []).append(v)
    mm = {m: st.mean(v) for m, v in mon.items()}; ma = st.mean(s)
    return {'rel_anchor': st.mean(last) / al if al else None, 'nonzero_weeks_52': sum(1 for x in last if x > 0),
            'chg_1y': st.mean(last) / st.mean(prev) - 1 if st.mean(prev) else None, 'chg_2y': st.mean(last) / st.mean(old) - 1 if st.mean(old) else None,
            'peak_month': max(mm, key=mm.get) if ma else '', 'low_month': min(mm, key=mm.get) if ma else '',
            'amp': (max(mm.values()) - min(mm.values())) / ma if ma else None}
sol = None; rows = {}
for k, b in P1.items():
    if k == 'regions': continue
    for t, c in b['clusters'].items():
        m = metrics(b['dates'], b['series'][t], b['series']['physics'])
        rows[t] = dict(m, term=t, cluster=c, pass_='1', anchor='physics', rel_physics=m['rel_anchor'], measured=b['measured'][:10])
        if t == 'speed of light': sol = m['rel_anchor']
for k, b in P2.items():
    if k == 'regions': continue
    for t, c in b['clusters'].items():
        m = metrics(b['dates'], b['series'][t], b['series']['speed of light'])
        r = dict(m, term=t, cluster=c, pass_='2', anchor='speed of light', rel_physics=m['rel_anchor'] * sol if m['rel_anchor'] is not None else None, measured=b['measured'][:10])
        if t not in rows or (rows[t]['nonzero_weeks_52'] < 40 and r['nonzero_weeks_52'] > rows[t]['nonzero_weeks_52']):
            r['pass1_rel_physics'] = rows.get(t, {}).get('rel_physics')
            rows[t] = r
        else:
            rows[t]['pass2_rel_physics'] = r['rel_physics']
out = sorted(rows.values(), key=lambda r: -(r['rel_physics'] or 0))
cols = ['term', 'cluster', 'pass_', 'anchor', 'rel_physics', 'nonzero_weeks_52', 'chg_1y', 'chg_2y', 'peak_month', 'low_month', 'amp', 'pass1_rel_physics', 'pass2_rel_physics', 'measured']
with open(os.path.join(OUT, 'trends-merged.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='ignore'); w.writeheader()
    for r in out: w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
print('speed of light vs physics', sol)
for r in out: print(f"{r['term']:28} {r['cluster']:10} p{r['pass_']} rel={r['rel_physics'] and round(r['rel_physics'],4)!s:8} nz={r['nonzero_weeks_52']:2} 1y={r['chg_1y'] and round(r['chg_1y'],2)!s:6} 2y={r['chg_2y'] and round(r['chg_2y'],2)!s:6} peak={r['peak_month']} low={r['low_month']} amp={r['amp'] and round(r['amp'],2)} p2check={r.get('pass2_rel_physics') and round(r['pass2_rel_physics'],4)}")
```

## analyze_suggest.py

Разметка подсказок.

```python
"""Autocomplete suggestion mix per cluster. Suggestions show that a query exists, not its volume.
Run: tmp/venv/bin/python -I tmp/research/analyze_suggest.py"""
import json, os, sys, csv, re
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
from topics import tag
PHYS = {'light', 'sound', 'magnet', 'electric', 'heat_energy', 'nuclear_particle', 'quantum', 'relativity_time', 'space', 'gravity', 'mechanics', 'fluids_flight', 'matter'}
MARK = {'kids': r"\bkids?\b|for children|preschool|storybots|dr binocs|peekaboo|cocomelon|aumsum|sid the science",
        'school': r"class \d+|\b1[0-2]th\b|grade \d+|a level|gcse|igcse|\bjee\b|\bneet\b|ncert|cbse|\bap physics|\bboard exam|\bbsc\b|\bmsc\b|1st year|2nd year|lecture|\bunit \d|chapter",
        'india': r"physics wallah|\bpw\b|alakh|hindi|\bsir\b|ncert|cbse|\bjee\b|\bneet\b|class \d+",
        'explained': r"explain|for dummies|simpl|in \d+ minutes|for beginners|basics|introduction",
        'experiment': r"experiment|\bdiy|at home|project|demo|test",
        'creator': r"veritasium|kurzgesagt|vsauce|action lab|minutephysics|pbs|sabine|neil degrasse|tyson|brian cox|feynman|kaku|floathead|float head|mark rober|steve mould|3blue1brown|smarter every ?day",
        'shorts_viral': r"#shorts|shorts\b|tiktok|meme|funny|satisfying",
        'question': r"^(why|how|what|is|can|does|do|will|where|when)\b"}
RX = {k: re.compile(v, re.I) for k, v in MARK.items()}
R = json.load(open(os.path.join(RAW, 'suggest.json')))
per = {}
for r in R['rows']:
    if isinstance(r['suggestions'], list):
        for s in r['suggestions']:
            per.setdefault(r['cluster'], set()).add(s)
rows, allp = [], []
for c, ss in sorted(per.items()):
    p = sorted(s for s in ss if (PHYS & set(tag(s))) or re.search(r'physic|scien', s, re.I))
    allp += [(c, s) for s in p]
    row = {'cluster': c, 'measured': R['measured'][:10], 'suggestions_unique': len(ss), 'physics_like': len(p)}
    for k, rx in RX.items(): row['share_' + k] = round(sum(1 for s in p if rx.search(s)) / len(p), 3) if p else ''
    rows.append(row)
with open(os.path.join(OUT, 'suggest-clusters.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, 'suggest-physics.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['cluster', 'suggestion', 'markers', 'measured'])
    for c, s in allp: w.writerow([c, s, ';'.join(k for k, rx in RX.items() if rx.search(s)), R['measured'][:10]])
for r in rows: print(r)
```

## analyze_search.py

Показатели выдачи.

```python
"""Search sample metrics per query and per cluster. Run: tmp/venv/bin/python -I tmp/research/analyze_search.py"""
import json, os, csv, statistics as st, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
def load(n):
    p = os.path.join(RAW, n); return json.load(open(p)) if os.path.exists(p) else {}
S = load('search.json')
CH = {}
for n in ('found.json', 'found_rev.json', 'seeds.json'):
    for k, r in load(n).items():
        if 'error' in r: continue
        cid = r.get('channel_id') or k
        CH[cid] = r
def med(xs):
    xs = [x for x in xs if x is not None]; return st.median(xs) if xs else None
def ts(iso): return datetime.datetime.fromisoformat(iso).timestamp()
def first_upload(r):
    vs = [v for v in r.get('videos', []) if v.get('timestamp')]
    if not vs or len(r.get('videos', [])) >= 30: return None
    return min(v['timestamp'] for v in vs)
rows, vids = [], []
for key, s in S.items():
    if not isinstance(s['results'], list): continue
    m = ts(s['measured'])
    res = []
    for rank, e in enumerate(s['results'], 1):
        ch = CH.get(e.get('channel_id'), {})
        subs = ch.get('subs'); fu = first_upload(ch) if ch else None
        age = (m - e['timestamp']) / 86400 if e.get('timestamp') else None
        new = (m - fu) / 86400 <= 365 if fu else None
        x = dict(e, rank=rank, subs=subs, age=age, new=new, cluster=s['cluster'], query=s['query'], filter=s['filter'], measured=s['measured'][:10])
        res.append(x); vids.append(x)
    longs = [x for x in res if (x.get('duration') or 0) > 180]
    row = {'cluster': s['cluster'], 'query': s['query'], 'filter': s['filter'], 'measured': s['measured'][:10], 'n_results': len(res),
           'share_short_le180s': round(sum(1 for x in res if x.get('duration') and x['duration'] <= 180) / len(res), 2) if res else ''}
    if s['filter'] == 'month':
        L = [x for x in longs if x['age'] is not None and 7 <= x['age'] <= 30]
        sm = [x for x in L if x['subs'] is not None and x['subs'] < 10_000]
        nw = [x for x in L if x['new']]
        row.update({'long_7_30d_n': len(L), 'long_7_30d_median_views': med([x['view_count'] for x in L]),
                    'long_7_30d_subs_lt10k_n': len(sm), 'long_7_30d_subs_lt10k_median': med([x['view_count'] for x in sm]),
                    'long_7_30d_new_channel_n': len(nw), 'long_7_30d_new_channel_median': med([x['view_count'] for x in nw]),
                    'long_7_30d_lt100k_ge10k_views': sum(1 for x in L if (x['subs'] or 0) < 100_000 and (x['view_count'] or 0) >= 10_000)})
    else:
        T = [x for x in res[:20] if x.get('view_count') is not None and x['age']]
        row.update({'top20_median_views': med([x['view_count'] for x in T]),
                    'top20_median_age_years': round(med([x['age'] for x in T]) / 365, 1) if T else '',
                    'top20_median_views_per_year': round(med([x['view_count'] / max(x['age'] / 365, 0.1) for x in T])) if T else '',
                    'top20_share_subs_ge1m': round(sum(1 for x in T if (x['subs'] or 0) >= 1_000_000) / len(T), 2) if T else '',
                    'top20_share_subs_lt100k': round(sum(1 for x in T if x['subs'] is not None and x['subs'] < 100_000) / len(T), 2) if T else '',
                    'top20_share_older_3y': round(sum(1 for x in T if x['age'] > 3 * 365) / len(T), 2) if T else '',
                    'top20_share_younger_1y': round(sum(1 for x in T if x['age'] <= 365) / len(T), 2) if T else '',
                    'top1_title': res[0]['title'] if res else '', 'top1_channel': res[0]['channel'] if res else '',
                    'top1_views': res[0]['view_count'] if res else '', 'top1_url': f"https://www.youtube.com/watch?v={res[0]['id']}" if res else ''})
    rows.append(row)
cols = []
for r in rows:
    for k in r:
        if k not in cols: cols.append(k)
rows.sort(key=lambda r: (r['filter'], r['cluster'], r['query']))
with open(os.path.join(OUT, 'search-queries.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n'); w.writeheader(); w.writerows(rows)
vc = ['filter', 'cluster', 'query', 'rank', 'id', 'title', 'channel', 'channel_id', 'subs', 'view_count', 'duration', 'age', 'new', 'measured']
with open(os.path.join(OUT, 'search-videos.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=vc, lineterminator='\n', extrasaction='ignore'); w.writeheader()
    for x in vids: w.writerow(dict(x, age=round(x['age'], 1) if x['age'] is not None else ''))
# per cluster
agg = {}
for x in vids: agg.setdefault((x['filter'], x['cluster']), []).append(x)
print('cluster month: n long7-30 / median / <10k n / <10k med / new n / new med ;; any top20: med views, med age y, views/yr, share>=1M, share<100k, share>3y')
for c in sorted({k[1] for k in agg}):
    M = [x for x in agg.get(('month', c), []) if (x.get('duration') or 0) > 180 and x['age'] is not None and 7 <= x['age'] <= 30]
    sm = [x for x in M if x['subs'] is not None and x['subs'] < 10_000]; nw = [x for x in M if x['new']]
    A = [x for x in agg.get(('any', c), []) if x['rank'] <= 20 and x.get('view_count') is not None and x['age']]
    print(f"{c:11} {len(M):4} {med([x['view_count'] for x in M])!s:>8} {len(sm):4} {med([x['view_count'] for x in sm])!s:>7} {len(nw):3} {med([x['view_count'] for x in nw])!s:>7} ;; "
          f"{med([x['view_count'] for x in A])!s:>9} {round(med([x['age'] for x in A]) / 365, 1) if A else ''} {round(med([x['view_count'] / max(x['age'] / 365, .1) for x in A])) if A else ''} "
          f"{round(sum(1 for x in A if (x['subs'] or 0) >= 1e6) / len(A), 2) if A else ''} {round(sum(1 for x in A if x['subs'] is not None and x['subs'] < 1e5) / len(A), 2) if A else ''} {round(sum(1 for x in A if x['age'] > 1095) / len(A), 2) if A else ''}")
print('channels known', len(CH))
```

## newchannels.py

Полный список роликов кандидатов в новые каналы.

```python
"""Find new and rising physics channels among discovered channels.
Step 1 (default): list candidates; channels whose 30 latest videos all fall inside 365 days get a deep fetch (up to 500 videos).
Run: tmp/venv/bin/python -I tmp/research/newchannels.py [deep]"""
import json, os, sys, csv, statistics as st, datetime, re
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
from topics import tag
PHYS = {'light', 'sound', 'magnet', 'electric', 'heat_energy', 'nuclear_particle', 'quantum', 'relativity_time', 'space', 'gravity',
        'mechanics', 'fluids_flight', 'matter'}
def load(n):
    p = os.path.join(RAW, n); return json.load(open(p)) if os.path.exists(p) else {}
def ts(iso): return datetime.datetime.fromisoformat(iso).timestamp()
def med(xs):
    xs = [x for x in xs if x is not None]; return st.median(xs) if xs else None
def day(t): return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%d') if t else ''
F = load('found.json'); D = load('deep.json')
S = load('search.json')
hits = {}
for s in S.values():
    if isinstance(s['results'], list):
        for e in s['results']:
            hits.setdefault(e.get('channel_id'), set()).add(f"{s['filter']}:{s['query']}")
rows, need_deep = [], []
for k, r in F.items():
    if 'error' in r or not r.get('videos'): continue
    m = ts(r['measured'])
    vids = [v for v in r['videos'] if v.get('timestamp')]
    if not vids: continue
    titles = [v.get('title') or '' for v in r['videos']]
    phys_share = sum(1 for t in titles if PHYS & set(tag(t))) / len(titles)
    ascii_share = sum(1 for t in titles if sum(c.isascii() for c in t) >= 0.9 * max(len(t), 1)) / len(titles)
    oldest30 = min(v['timestamp'] for v in vids)
    complete = len(r['videos']) < 30
    d = D.get(k)
    if d and 'error' not in d and d.get('videos'):
        dv = [v for v in d['videos'] if v.get('timestamp')]
        first = min(v['timestamp'] for v in dv) if dv and len(d['videos']) < 500 else None
        total_listed = len(d['videos'])
    else:
        first = oldest30 if complete else None; total_listed = len(r['videos']) if complete else None
    if not complete and (m - oldest30) / 86400 <= 365 and not d:
        need_deep.append(k)
    age_ch = (m - first) / 86400 if first else None
    ok = [v for v in r['videos'] if v.get('timestamp') and (m - v['timestamp']) / 86400 >= 7 and v.get('view_count') is not None]
    rec, older = ok[:10], ok[10:]
    rows.append({'channel_id': k, 'channel': r.get('channel'), 'url': r.get('url'), 'subs': r.get('subs'), 'measured': r['measured'][:10],
                 'first_upload_known': day(first), 'channel_age_days': round(age_ch) if age_ch else '', 'videos_listed': total_listed or '',
                 'new_le_365d': 'yes' if age_ch is not None and age_ch <= 365 else ('no' if age_ch is not None or (m - oldest30) / 86400 > 365 else 'unknown'),
                 'physics_title_share': round(phys_share, 2), 'english_title_share': round(ascii_share, 2),
                 'median_views_latest10_ge7d': med([v['view_count'] for v in rec]), 'median_views_older20': med([v['view_count'] for v in older]),
                 'rising_ratio': round(med([v['view_count'] for v in rec]) / med([v['view_count'] for v in older]), 2) if rec and older and med([v['view_count'] for v in older]) else '',
                 'max_views_30': max((v['view_count'] or 0) for v in r['videos']),
                 'max_title': max(r['videos'], key=lambda v: v.get('view_count') or 0).get('title'),
                 'uploads_in_30_span_days': round((m - oldest30) / 86400),
                 'search_hits': len(hits.get(k, ())), 'example_query': sorted(hits.get(k, ['']))[0]})
with open(os.path.join(OUT, 'found-channels.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print('rows', len(rows), 'need deep', len(need_deep))
if len(sys.argv) > 1 and sys.argv[1] == 'deep':
    sys.argv = ['x', 'none']
    src = open(os.path.join(HERE, 'collect.py')).read(); src = src[:src.rindex('main()')]
    g = {'__file__': os.path.join(HERE, 'collect.py')}; exec(compile(src, 'collect.py', 'exec'), g)
    # deep only for English physics-leaning candidates
    cand = [x['channel_id'] for x in rows if x['channel_id'] in need_deep and x['physics_title_share'] >= 0.3 and x['english_title_share'] >= 0.8 and 1000 <= (x['subs'] or 0) <= 3000000]
    print('deep fetch', len(cand), flush=True)
    g['run_channels'](cand, os.path.join(RAW, 'deep.json'), 500, 0)
```

## agecheck.py

Проверка возраста кандидатов в новые каналы: дата регистрации, полный список публичных загрузок, дата самой старой.

```python
"""Confirm the age of new-channel candidates: English physics-leaning channels from the search sample whose age was 'yes' or 'unknown'.
For each channel: the /about page (join date, public video count), then, unless it joined under 365 days ago, the full flat listing
of the channel's uploads playlist (UU + id: videos, shorts and streams together, newest first, up to 5000) and the exact publish date
of its last, oldest entry (watch page). The first 94 channels were listed per tab (videos, shorts, streams; up to 1000 each): same result, three times slower.
Resumes from raw/age.json; one batch per run.
Run: tmp/venv/bin/python -I tmp/research/agecheck.py [batch_size]"""
import concurrent.futures as cf, csv, datetime, json, os, re, sys, time, urllib.request
import yt_dlp
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
PATH = os.path.join(RAW, 'age.json'); CAP = 5000
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def now(): return datetime.datetime.now(datetime.timezone.utc)

def about(cid):
    req = urllib.request.Request(f'https://www.youtube.com/channel/{cid}/about?hl=en&gl=US',
                                 headers={'User-Agent': UA, 'Cookie': 'CONSENT=YES+1; SOCS=CAI', 'Accept-Language': 'en-US'})
    for a in range(3):
        try:
            h = urllib.request.urlopen(req, timeout=30).read().decode()
            j = h.find('joinedDateText')
            if j < 0: return {'error': 'no about data'}
            s = h[h.rfind('aboutChannelViewModel', 0, j):j + 3000]
            f = dict(re.findall(r'"(videoCountText|joinedDateText)":(?:\{"content":)?"([^"]*)"', s))
            joined = datetime.datetime.strptime(f['joinedDateText'].replace('Joined ', ''), '%b %d, %Y').date().isoformat()
            vc = re.sub(r'\D', '', f.get('videoCountText', '')) or None
            return {'joined': joined, 'video_count': int(vc) if vc else (0 if 'No videos' in f.get('videoCountText', '') else None)}
        except Exception as ex:
            err = str(ex); time.sleep(5)
    return {'error': err}

def published(vid):
    req = urllib.request.Request(f'https://www.youtube.com/watch?v={vid}&hl=en', headers={'User-Agent': UA, 'Cookie': 'CONSENT=YES+1; SOCS=CAI'})
    for a in range(3):
        try:
            m = re.search(r'"publishDate":"([^"]+)"', urllib.request.urlopen(req, timeout=30).read().decode())
            return m.group(1)[:10] if m else 'error: no publishDate'
        except Exception as ex:
            err = str(ex); time.sleep(5)
    return 'error: ' + err[:100]

def uploads(cid):
    for a in range(3):
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'extract_flat': 'in_playlist', 'playlistend': CAP, 'skip_download': True, 'socket_timeout': 30}) as y:
                info = y.extract_info('https://www.youtube.com/playlist?list=UU' + cid[2:], download=False)
            ents = info.get('entries') or []
            r = {'n': len(ents), 'last_id': ents[-1]['id'] if ents else None}
            if ents: r['last_date'] = published(ents[-1]['id'])  # newest first: the last entry is the oldest public upload
            return r
        except Exception as ex:
            err = str(ex)
            if 'does not exist' in err or 'no videos' in err.lower(): return {'n': 0, 'last_id': None, 'note': err[:120]}
            time.sleep(5)
    return {'error': err[:200]}

def check(cid):
    r = {'measured': now().isoformat(timespec='seconds'), 'about': about(cid)}
    j = r['about'].get('joined')
    if j and (now().date() - datetime.date.fromisoformat(j)).days < 365: return r
    r['uploads'] = uploads(cid)
    return r

if __name__ == '__main__':
    fc = list(csv.DictReader(open(os.path.join(OUT, 'found-channels.csv'))))
    keys = [r['channel_id'] for r in fc if r['new_le_365d'] in ('yes', 'unknown')
            and float(r['physics_title_share']) >= 0.3 and float(r['english_title_share']) >= 0.8]
    A = json.load(open(PATH)) if os.path.exists(PATH) else {}
    todo = [k for k in keys if k not in A or 'error' in A[k]['about'] or any('error' in t or str(t.get('last_date', '')).startswith('error') for t in list(A[k].get('tabs', {}).values()) + [A[k].get('uploads', {})])]
    todo = todo[:int(sys.argv[1]) if len(sys.argv) > 1 else 150]
    print('scope', len(keys), 'todo now', len(todo), flush=True)
    with cf.ThreadPoolExecutor(12) as ex:
        for i, (k, r) in enumerate(zip(todo, ex.map(check, todo))):
            A[k] = r
            if i % 10 == 0: json.dump(A, open(PATH, 'w')); print(i, k, r['about'], flush=True)
    json.dump(A, open(PATH, 'w'))
    print('done', len(A), flush=True)
```

## relevance_batches.py

Входные файлы слепой проверки релевантности кандидатов и правило разметки.

```python
"""Inputs for the blind relevance check of new-channel candidates (the same 1011 channels as agecheck.py).
Each channel: id, name and up to 15 latest titles; no views, subscribers or age. Order shuffled (seed 3), 100 channels per file.
Two readers labelled the files by hand (batch00-05 -> result-a.csv, batch06-10 -> result-b.csv) with one rule for all:
- relevant = yes: most titles in English and the main subject is explaining physics or physical science to a general audience
  (physics, space science, how physical things and machines work, experiments, physics simulations, science-for-sleep narration;
  mixed science channels count if physical science is a large part);
- relevant = no, one reason: nonenglish; exam (exam or homework coaching, syllabus lectures); fiction (sci-fi stories, drama, films, game lore);
  offtopic (kids songs, music, ambient sound, news, religion, self-help, finance, health, history without physics, trivia, pseudo-science, reviews);
- judged only from the name and titles; when genuinely unsure, the closer option and unsure = yes.
Run: tmp/venv/bin/python -I tmp/research/relevance_batches.py [out_dir]"""
import csv, json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, 'relevance')
fc = list(csv.DictReader(open(os.path.join(OUT, 'found-channels.csv'))))
F = json.load(open(os.path.join(HERE, 'raw', 'found.json')))
keys = [r for r in fc if r['new_le_365d'] in ('yes', 'unknown') and float(r['physics_title_share']) >= 0.3 and float(r['english_title_share']) >= 0.8]
random.Random(3).shuffle(keys)  # order unrelated to success
os.makedirs(dst, exist_ok=True)
for b in range(0, len(keys), 100):
    with open(os.path.join(dst, f'batch{b // 100:02d}.txt'), 'w') as f:
        for r in keys[b:b + 100]:
            titles = [v.get('title') or '' for v in F[r['channel_id']]['videos']][:15]
            f.write(f"### {r['channel_id']} | {r['channel']}\n" + ''.join(f"- {t}\n" for t in titles) + "\n")
print(len(keys))
```

## analyze.py

Показатели каналов и роликов: обычный результат, ролик против соседей.

```python
"""Build channel registry, video registry and topic metrics from raw data.
Run: tmp/venv/bin/python -I tmp/research/analyze.py"""
import json, os, csv, statistics as st, datetime, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
from topics import tag, CLUSTERS
os.makedirs(OUT, exist_ok=True)

def ts(iso): return datetime.datetime.fromisoformat(iso).timestamp()
def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None
def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs: return None
    k = (len(xs) - 1) * p; f = int(k); c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)
def day(t): return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%d') if t else ''
def tier(s):
    if s is None: return 'unknown'
    return 'big' if s >= 1_000_000 else 'mid' if s >= 100_000 else 'small' if s >= 10_000 else 'micro'
def write(name, rows, cols):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='ignore'); w.writeheader(); w.writerows(rows)

seeds = json.load(open(os.path.join(HERE, 'seeds.json')))
meta = {c[0]: (c[1], c[2]) for c in seeds['channels']}
C = json.load(open(os.path.join(RAW, 'seeds.json')))

chan_rows, vid_rows = [], []
for key, (grp, kind) in meta.items():
    r = C.get(key)
    if not r or 'error' in r:
        chan_rows.append({'key': key, 'group': grp, 'kind': kind, 'error': (r or {}).get('error', 'not fetched')[:200]}); continue
    m = ts(r['measured'])
    vids = [v for v in r['videos'] if v.get('view_count') is not None and v.get('timestamp')]
    for v in vids: v['age'] = (m - v['timestamp']) / 86400
    vids.sort(key=lambda v: v['timestamp'])
    # rolling typical: median of up to 10 nearest uploads by order, excluding self, only videos >= 14 days old
    old = [v for v in vids if v['age'] >= 14]
    for i, v in enumerate(old):
        nb = old[max(0, i - 5):i] + old[i + 1:i + 6]
        v['typical'] = med([x['view_count'] for x in nb]) if len(nb) >= 4 else None
        v['ratio'] = v['view_count'] / v['typical'] if v.get('typical') else None
    complete = len(r['videos']) < 300
    y1 = [v for v in vids if 30 <= v['age'] <= 365]
    y13 = [v for v in vids if 365 < v['age'] <= 3 * 365]
    last365 = [v for v in vids if v['age'] <= 365]
    longs = [v for v in vids if (v.get('duration') or 0) > 180]
    durs = [v['duration'] for v in vids[-30:] if v.get('duration')]
    sh = r.get('shorts') if isinstance(r.get('shorts'), list) else []
    top = max(vids, key=lambda v: v['view_count']) if vids else None
    rec = [v for v in old if v['age'] <= 365 and v.get('ratio')]
    best = max(rec, key=lambda v: v['ratio']) if rec else None
    worst = min(rec, key=lambda v: v['ratio']) if rec else None
    typ1, typ13 = med([v['view_count'] for v in y1]), med([v['view_count'] for v in y13])
    last = vids[-1] if vids else None
    row = {
        'key': key, 'group': grp, 'kind': kind, 'channel': r['channel'], 'url': r['url'], 'subs': r['subs'], 'tier': tier(r['subs']),
        'measured': r['measured'][:10], 'videos_fetched': len(r['videos']), 'list_complete': 'yes' if complete else 'no',
        'first_upload_if_complete': day(vids[0]['timestamp']) if complete and vids else '',
        'last_upload': day(last['timestamp']) if last else '',
        'uploads_last_365d': len(last365), 'uploads_per_month_365d': round(len(last365) / 12, 1),
        'median_duration_min_last30': round(med(durs) / 60, 1) if durs else '',
        'share_over_20min_last30': round(sum(1 for d in durs if d > 1200) / len(durs), 2) if durs else '',
        'typical_views_30_365d': typ1, 'n_30_365d': len(y1),
        'typical_views_1_3y': typ13, 'n_1_3y': len(y13),
        'trajectory_recent_vs_1_3y': round(typ1 / typ13, 2) if typ1 and typ13 else '',
        'shorts_listed': len(sh), 'shorts_median_views': med([s.get('view_count') for s in sh]),
        'top_title': top['title'] if top else '', 'top_url': f"https://www.youtube.com/watch?v={top['id']}" if top else '',
        'top_views': top['view_count'] if top else '', 'top_age_days': round(top['age']) if top else '',
        'best_recent_title': best['title'] if best else '', 'best_recent_url': f"https://www.youtube.com/watch?v={best['id']}" if best else '',
        'best_recent_views': best['view_count'] if best else '', 'best_recent_ratio': round(best['ratio'], 2) if best else '',
        'weak_recent_title': worst['title'] if worst else '', 'weak_recent_url': f"https://www.youtube.com/watch?v={worst['id']}" if worst else '',
        'weak_recent_views': worst['view_count'] if worst else '', 'weak_recent_ratio': round(worst['ratio'], 2) if worst else '',
        'error': ''}
    chan_rows.append(row)
    for v in vids:
        vid_rows.append({'channel': r['channel'], 'key': key, 'group': grp, 'kind': kind, 'subs': r['subs'],
                         'video_id': v['id'], 'url': f"https://www.youtube.com/watch?v={v['id']}", 'title': v['title'],
                         'duration_s': v.get('duration'), 'format': 'long' if (v.get('duration') or 0) > 180 else 'short_or_unknown',
                         'approx_upload': day(v['timestamp']), 'age_days': round(v['age']), 'views': v['view_count'],
                         'views_per_day': round(v['view_count'] / max(v['age'], 1), 1),
                         'channel_typical_neighbours': v.get('typical'), 'ratio_to_typical': round(v['ratio'], 2) if v.get('ratio') else '',
                         'clusters': ';'.join(tag(v['title'])), 'measured': r['measured'][:10]})

CCOLS = ['key', 'group', 'kind', 'channel', 'url', 'subs', 'tier', 'measured', 'videos_fetched', 'list_complete', 'first_upload_if_complete',
         'last_upload', 'uploads_last_365d', 'uploads_per_month_365d', 'median_duration_min_last30', 'share_over_20min_last30',
         'typical_views_30_365d', 'n_30_365d', 'typical_views_1_3y', 'n_1_3y', 'trajectory_recent_vs_1_3y', 'shorts_listed', 'shorts_median_views',
         'top_title', 'top_url', 'top_views', 'top_age_days', 'best_recent_title', 'best_recent_url', 'best_recent_views', 'best_recent_ratio',
         'weak_recent_title', 'weak_recent_url', 'weak_recent_views', 'weak_recent_ratio', 'error']
write('seed-channels.csv', chan_rows, CCOLS)
write('seed-videos.csv', vid_rows, list(vid_rows[0].keys()))

# topic popularity inside channels: English channels, long videos 30 days .. 5 years old with a ratio
EN_SKIP = {'other-market', 'institutional', 'shorts'}
pool = [v for v in vid_rows if v['kind'] not in EN_SKIP and v['ratio_to_typical'] != '' and 30 <= v['age_days'] <= 5 * 365 and v['format'] == 'long']
base_med = med([v['ratio_to_typical'] for v in pool]); base_out = sum(1 for v in pool if v['ratio_to_typical'] >= 2) / len(pool)
PHYS = {'physics-general', 'physics-deep', 'physics-animation', 'physics-news', 'physics-opinion', 'physics-history', 'physics-interview',
        'experiments', 'simulation', 'science-animation', 'science-general', 'education', 'math-physics', 'space', 'space-news'}
def ci(vs, n=2000):
    rnd = random.Random(7); xs = [v['ratio_to_typical'] for v in vs]; ms = []
    for _ in range(n): ms.append(st.median(rnd.choices(xs, k=len(xs))))
    ms.sort(); return round(ms[int(.05 * n)], 2), round(ms[int(.95 * n)], 2)
trows = []
for c in list(CLUSTERS) + ['(none)']:
    vs = [v for v in pool if (c in v['clusters'].split(';') if c != '(none)' else v['clusters'] == '')]
    if not vs: continue
    big = [v for v in vs if (v['subs'] or 0) >= 1_000_000]
    phys = [v for v in vs if v['kind'] in PHYS]
    trows.append({'cluster': c, 'n_videos': len(vs), 'n_channels': len({v['key'] for v in vs}),
                  'median_ratio': round(med([v['ratio_to_typical'] for v in vs]), 2),
                  'p75_ratio': round(q([v['ratio_to_typical'] for v in vs], .75), 2),
                  'share_ratio_ge2': round(sum(1 for v in vs if v['ratio_to_typical'] >= 2) / len(vs), 3),
                  'n_big_channels_videos': len(big), 'median_ratio_big': round(med([v['ratio_to_typical'] for v in big]), 2) if big else '',
                  'n_physics_core': len(phys), 'median_ratio_physics_core': round(med([v['ratio_to_typical'] for v in phys]), 2) if phys else '',
                  'median_ratio_ci90_low': ci(vs)[0], 'median_ratio_ci90_high': ci(vs)[1],
                  'median_views_per_day': round(med([v['views_per_day'] for v in vs]), 1),
                  'top_example': max(vs, key=lambda v: v['ratio_to_typical'])['title'],
                  'top_example_url': max(vs, key=lambda v: v['ratio_to_typical'])['url']})
write('topic-in-channel.csv', trows, list(trows[0].keys()))
print('pool', len(pool), 'base median ratio', round(base_med, 2), 'base share>=2', round(base_out, 3))
for t in sorted(trows, key=lambda t: -t['median_ratio']):
    print(f"{t['cluster']:18} n={t['n_videos']:5} ch={t['n_channels']:3} med={t['median_ratio']:.2f} p75={t['p75_ratio']:.2f} ge2={t['share_ratio_ge2']:.3f} core={t['median_ratio_physics_core']}")
```

## topics.py

Темы по словарю в названиях; прежний расчёт data/topics.csv.

```python
"""Topic clusters by title keywords. One title may get several clusters."""
import re
CLUSTERS = {
 'light': r"\blight\b|colou?r|rainbow|laser|sky (is )?blue|blue sky|mirror|lens|optic|photon|prism|refract|reflect|shadow|ultraviolet|infrared|sunset|invisib|glow|camera|polari",
 'sound': r"\bsound|acoustic|resonan|vibrat|\becho|sonic|ultrasound|\bnoise|\bmusic|frequenc|speaker|\bloud|guitar|\bpitch\b",
 'magnet': r"magnet|electromagn|compass|maglev|levitat",
 'electric': r"electric|electron(?!ic)|voltage|current|battery|batteries|lightning|tesla coil|circuit|static|\bcharge|wire|power grid|transformer|capacitor|spark|\bvolt|amp\b|\bac\b|\bdc\b",
 'heat_energy': r"energy|\bheat|temperature|entrop|thermo|\bfire\b|flame|\bhot\b|\bcold|freez|\bice\b|\bboil|steam|perpetual|absolute zero|solar panel|insulat|cool(ing)?\b|melt",
 'nuclear_particle': r"nuclear|\batom|particle|quark|neutrino|higgs|radiat|radioact|fusion|fission|reactor|antimatter|proton|neutron(?! star)|collider|uranium|plutonium|isotope",
 'quantum': r"quantum|entangl|superposition|double.slit|schr(o|ö)dinger|uncertainty|wave ?function|qubit|tunnel(l)?ing",
 'relativity_time': r"relativit|einstein|time dilation|speed of light|faster than light|spacetime|space-time|time travel|twin paradox|dimension|lorentz",
 'space': r"black hole|universe|galax|\bstars?\b|\bsun\b|planet|\bmoon|\bmars\b|jupiter|saturn|\bearth\b|orbit|\bspace\b|cosmo|big bang|dark matter|dark energy|neutron star|supernova|telescope|webb|asteroid|comet|light.year|solar system|nasa|alien|exoplanet|pulsar|quasar|wormhole|multiverse",
 'gravity': r"gravit|weightless|free.?fall|\bmass\b|\bweight",
 'mechanics': r"motion|\bforce|newton|momentum|friction|\bspin|gyroscop|pendulum|\bfall|projectile|\bspeed|accelerat|inertia|rotat|bicycle|collision|bounce|balance|centrifug|torque|\bwheel|\bjump|\bthrow",
 'fluids_flight': r"water|fluid|\bair\b|flight|\bfly|plane\b|airplane|aircraft|\blift\b|\bwing|\bboat|\bfloat|buoyan|pressure|vacuum|bubble|ocean|\bdrag\b|aerodynam|wind|tornado|vortex|siphon|\bwave",
 'matter': r"material|metal|crystal|\bsolid|liquid|\bgas\b|plasma|superconduct|\bglass|steel|diamond|state of matter|states of matter|graphene|rubber|\bfoam",
 'paradox_puzzle': r"paradox|puzzle|impossible|myth|wrong|mistake|misconcept|you think|actually|nobody|no one|secret|counterintuit|weird|strange|mystery|why can.t|can you|riddle",
 'everyday': r"kitchen|microwave|fridge|refrigerator|toilet|shower|coffee|phone|cook|everyday|daily life|household|\bcar\b|cars\b|shoe|umbrella|soap|\begg|bread|candle|\bbike|clothes|\btoast",
 'experiment': r"experiment|\btested|\btest\b|i (made|built|tried)|we (made|built|tried)|slow.?mo|hydraulic press|\bvs\.?\b|satisfying|\bdemo|built a|making a|homemade|diy",
 'engineering': r"how (it|they|does .* )?works?|engine\b|engines|machine|bridge|motor|turbine|mechanism|invent|\bdesign|engineer|rocket|nuclear plant|dam\b|building",
 'math': r"\bmath|equation|prime|geometr|calculus|\bnumber|infinit|probabil|\bpi\b|fourier|topolog|algebra",
 'history_people': r"history|discover|feynman|tesla\b|genius|scientist|nobel|newton.s|einstein.s|who (invented|discovered)|century",
 'news': r"\bnew\b|breakthrough|just (found|discovered|announced|happened)|\b202[4-6]\b|study (finds|shows)|scientists (just|have)|first ever|record",
 'scale': r"size comparison|how big|how small|scale|largest|smallest|biggest|tiny|zoom",
}
RX = {k: re.compile(v, re.I) for k, v in CLUSTERS.items()}
def tag(title):
    t = title or ''
    return [k for k, r in RX.items() if r.search(t)]
```

## topics_v2.py

Исправленный словарь тем после первой ручной проверки.

```python
"""Topic clusters, version 2: the version 1 dictionary (topics.py) corrected after the manual check of 270 titles (data/tag-check.csv).
Changes: narrower words where the check found false matches, a few missed words added, and exclusion rules
(mechanics and matter are dropped when a title is about quantum, relativity, particles or space; 'Lightning Round', 'dark energy' and similar).
Version 1 stays in topics.py: it also selects physics channels (title share), which the corrections do not change."""
import re
from topics import CLUSTERS as V1
CLUSTERS = dict(V1)
CLUSTERS.update({
 'light': r"\blights?\b|\bcolou?rs?\b|rainbow|laser|sky (is )?blue|blue sky|mirror|\blens(es)?\b|optic|photon|prism|refract|reflect|shadow|ultraviolet|infrared|sunset|invisib|glow|polari",
 'sound': r"\bsound|acoustic|resonan|vibrat|\becho|sonic|ultrasound|\bnoise|frequenc|speaker|\bloud|guitar|\bpitch\b",
 'electric': r"electric|electron(?!ic)|voltage|current|battery|batteries|lightning(?! round)|tesla coil|circuit|static|\bcharge|wire|power grid|transformer|capacitor|spark|\bvolt|amp\b|\bac\b|\bdc\b|\bemf\b|solenoid|servo",
 'heat_energy': r"(?<!dark )(?<!vacuum )\benergy|\bheat|temperature|entrop|thermo|\bfire\b|flame|\bhot\b|\bcold|freez|\bice\b|\bboil|steam|perpetual|absolute zero|solar panel|insulat|cool(ing)?\b|melt",
 'nuclear_particle': r"nuclear|\batoms?\b|\batomic (bomb|energy|nucle|structure)|nucleus|particle|quark|neutrino|higgs|radiat|radioact|\bfusion|fission|reactor|antimatter|proton|neutron(?! star)|collider|uranium|plutonium|isotope",
 'relativity_time': r"relativit|\beinstein\b(?!.{0,3}condensate)|time dilation|speed of light|faster than light|spacetime|space-time|time travel|twin paradox|\bdimensions?\b|lorentz|what is time|time (start|began|begin|end)|arrow of time",
 'mechanics': r"motion|\bforces?\b|newton|momentum|friction|\bspin|gyroscop|pendulum|\bfall|projectile|\bspeed|inertia|\brotat(e|es|ing|ion)\b|bicycle|collision|bounce|balance|centrifug|torque|\bwheel|\bjump|\bthrow|\brails?\b",
 'fluids_flight': r"water|fluid|\bair\b|flight|\bfly\b(?! apart)|plane\b|airplane|aircraft|\blift\b|\bwing|\bboat|\bfloat|buoyan|pressure|vacuum|bubble|ocean|\bdrag\b|aerodynam|wind|tornado|vortex|siphon|\bwave|hurricane|\bfans?\b",
 'matter': r"material|metal|crystal|\bsolid\b|liquid|\bgas\b|plasma|superconduct|\bglass\b|steel|diamond|state of matter|states of matter|graphene|rubber(?! sheet)|\bfoam|\bbrick",
 'everyday': r"kitchen|microwave|fridge|refrigerator|toilet|shower|coffee|\bphones?\b|smartphone|cook|everyday|daily life|household|\bcar\b|cars\b|shoe|umbrella|soap|\begg|bread|candle|\bbike|\btoast|smartwatch",
 'experiment': r"experiment|\btested|\btest\b|i (made|built|tried)|we (made|built|tried)|slow.?mo|hydraulic press|\bvs\.?\b|satisfying|built a|making a|homemade|diy",
 'math': r"\bmath|equation|prime|geometr|calculus|\bnumber|infinit|probabil|\bpi\b|fourier|topolog|algebra|logarithm|counting",
 'history_people': r"history of (physics|science|the atom|electricity|light|magnet)|who (invented|discovered)|feynman|tesla\b|\bgenius|nobel|newton.s|einstein.s|\bcentury|discovery of|physicist (who|that)|(was|were) discovered|\b1[6-9]\d\d\b",
 'news': r"breakthrough|just (found|discovered|announced|happened|built|broke)|\b202[4-6]\b|study (finds|shows)|scientists (just|have|may)|first ever|record|new (study|discovery|evidence|research|results?|finding|paper|measurement)",
 'scale': r"size comparison|how big|how small|\bscale\b|zoom (in|into|out)|from (the )?(smallest|tiniest)|smallest (thing|particle|object)|largest (thing|star|object|structure|number)|powers of (ten|10)",
})
RX = {k: re.compile(v, re.I) for k, v in CLUSTERS.items()}
NOT_MECH = re.compile(r"(fundamental|strong|weak|electric|magnetic|induced|nuclear) forces?|meme", re.I)
NOT_MATTER = re.compile(r"rubber sheet|safety glass", re.I)
def tag(title):
    t = title or ''
    ks = [k for k, r in RX.items() if r.search(t)]
    if 'mechanics' in ks and ({'quantum', 'relativity_time', 'nuclear_particle'} & set(ks) or NOT_MECH.search(t)): ks.remove('mechanics')
    if 'matter' in ks and ({'space', 'nuclear_particle', 'quantum'} & set(ks) or NOT_MATTER.search(t)): ks.remove('matter')
    return ks
```

## topics_cluster.py

Темы с выборкой каналов целиком и поправкой на 21 сравнение.

```python
"""Topic popularity inside channels with channel-level resampling.
Same pool as analyze.py: English reference channels, long videos 30 days..5 years old with a neighbour ratio.
Intervals: resample whole channels with replacement (videos of one channel stay together), 100 000 rounds per seed, seeds 7, 8 and 9.
ci90 = plain 90% interval; ci_adj = Bonferroni for 21 clusters (family 90%: each interval at 1-0.10/21; about 238 rounds in each tail).
Stability: each bound is reported for seed 7 and as the largest spread across the three seeds.
Run once per dictionary: v1 = clusters column of videos.csv (topics.py), v2 = corrected dictionary (topics_v2.py).
Also: median ratio inside three age bands, and the share of channels (3+ videos in the cluster) whose own median is above 1.
Run: tmp/venv/bin/python -I tmp/research/topics_cluster.py"""
import csv, os, statistics as st, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
sys.path.insert(0, HERE)
from topics import CLUSTERS
import topics_v2
SKIP = {'other-market', 'institutional', 'shorts'}
pool = [r for r in csv.DictReader(open(os.path.join(DOCS, 'videos.csv')))
        if r['kind'] not in SKIP and r['ratio_to_typical'] and r['format'] == 'long' and 30 <= int(r['age_days']) <= 5 * 365]
chs = sorted({r['channel'] for r in pool}); ci = {c: i for i, c in enumerate(chs)}
for r in pool:
    r['x'] = float(r['ratio_to_typical']); r['v1'] = set(r['clusters'].split(';')) - {''}; r['v2'] = set(topics_v2.tag(r['title']))
K = len(CLUSTERS); N = 100_000; SEEDS = (7, 8, 9); CHUNK = 2000
Q = {'ci90_low': .05, 'ci90_high': .95, 'ci_adj21_low': .10 / K / 2, 'ci_adj21_high': 1 - .10 / K / 2}
COUNTS = {s: np.random.default_rng(s).multinomial(len(chs), [1 / len(chs)] * len(chs), size=N).astype(np.int32) for s in SEEDS}

def boot_medians(x, ch, counts):
    """Median of the resampled multiset for every round: each video counts as many times as its channel was drawn."""
    o = np.argsort(x); x, ch = x[o], ch[o]; out = np.full(len(counts), np.nan)
    for a in range(0, len(counts), CHUNK):
        w = counts[a:a + CHUNK][:, ch]; cs = np.cumsum(w, axis=1); t = cs[:, -1]; ok = t > 0
        lo = (cs >= ((t - 1) // 2 + 1)[:, None]).argmax(axis=1); hi = (cs >= (t // 2 + 1)[:, None]).argmax(axis=1)
        out[a:a + CHUNK] = np.where(ok, (x[lo] + x[hi]) / 2, np.nan)
    return out[~np.isnan(out)]

def run(ver):
    rows = []
    for c in CLUSTERS:
        vs = [r for r in pool if c in r[ver]]
        if not vs: continue
        x = np.array([r['x'] for r in vs]); ch = np.array([ci[r['channel']] for r in vs])
        q = {s: np.quantile(boot_medians(x, ch, COUNTS[s]), list(Q.values()), method='lower') for s in SEEDS}
        cv = {}
        for r in vs: cv.setdefault(r['channel'], []).append(r['x'])
        band = {}
        for name, a, b in (('30-365d', 30, 365), ('1-3y', 366, 3 * 365), ('3-5y', 3 * 365 + 1, 5 * 365)):
            xs = [r['x'] for r in vs if a <= int(r['age_days']) <= b]
            band[name] = (round(st.median(xs), 2) if len(xs) >= 20 else '', len(xs))
        own = [st.median(v) for v in cv.values() if len(v) >= 3]
        row = {'dictionary': ver, 'cluster': c, 'n_videos': len(vs), 'n_channels': len(cv), 'median_ratio': round(st.median(r['x'] for r in vs), 2)}
        for i, k in enumerate(Q):
            row[k] = round(q[7][i], 2); row[k + '_seed_spread'] = round(max(q[s][i] for s in SEEDS) - min(q[s][i] for s in SEEDS), 3)
        row.update({'median_30_365d': band['30-365d'][0], 'n_30_365d': band['30-365d'][1], 'median_1_3y': band['1-3y'][0], 'n_1_3y': band['1-3y'][1],
                    'median_3_5y': band['3-5y'][0], 'n_3_5y': band['3-5y'][1], 'channels_3plus': len(own),
                    'share_channels_above_1': round(sum(1 for m in own if m > 1) / len(own), 2) if own else ''})
        rows.append(row); print(row, flush=True)
    return sorted(rows, key=lambda r: -r['median_ratio'])

rows = run('v1') + run('v2')
with open(os.path.join(DOCS, 'topics-by-channel-resampling.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print('pool', len(pool), 'channels', len(chs), 'all median', round(st.median(r['x'] for r in pool), 2))
```

## tagcheck_sample.py

Случайная выборка для ручной проверки разметки тем.

```python
"""Random sample for a manual check of title tagging: 10 tagged titles per cluster and 60 untagged titles, seed 11.
Writes docs/physics-research/data/tag-check.csv with an empty 'correct' column filled by hand.
Run: tmp/venv/bin/python -I tmp/research/tagcheck_sample.py"""
import csv, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
sys.path.insert(0, HERE)
from topics import CLUSTERS
SKIP = {'other-market', 'institutional', 'shorts'}
pool = [r for r in csv.DictReader(open(os.path.join(DOCS, 'videos.csv')))
        if r['kind'] not in SKIP and r['ratio_to_typical'] and r['format'] == 'long' and 30 <= int(r['age_days']) <= 5 * 365]
rnd = random.Random(11); out = []
for c in CLUSTERS:
    vs = [r for r in pool if c in r['clusters'].split(';')]
    for r in rnd.sample(vs, min(10, len(vs))): out.append({'check': 'tagged', 'cluster': c, 'title': r['title'], 'all_clusters': r['clusters'], 'url': r['url']})
for r in rnd.sample([r for r in pool if not r['clusters']], 60):
    out.append({'check': 'untagged', 'cluster': '', 'title': r['title'], 'all_clusters': '', 'url': r['url']})
with open(os.path.join(DOCS, 'tag-check.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['check', 'cluster', 'title', 'all_clusters', 'url', 'correct', 'missed_cluster'], lineterminator='\n')
    w.writeheader(); w.writerows(out)
for i, r in enumerate(out): print(i, r['cluster'] or '-', '|', r['title'])
```

## tagcheck_v2.py

Вторая ручная проверка разметки, по исправленному словарю.

```python
"""Second manual check, for the corrected dictionary (topics_v2.py): a fresh random sample, seed 12, of 10 tagged titles per cluster
and 60 untagged titles, none of them from the first check. Manual verdicts are listed below by sample index (the check was done by
reading each title). Writes docs/physics-research/data/tag-check-v2.csv.
Run: tmp/venv/bin/python -I tmp/research/tagcheck_v2.py"""
import csv, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
sys.path.insert(0, HERE)
from topics_v2 import tag, CLUSTERS
SKIP = {'other-market', 'institutional', 'shorts'}
pool = [r for r in csv.DictReader(open(os.path.join(DOCS, 'videos.csv')))
        if r['kind'] not in SKIP and r['ratio_to_typical'] and r['format'] == 'long' and 30 <= int(r['age_days']) <= 5 * 365]
seen = {r['url'] for r in csv.DictReader(open(os.path.join(DOCS, 'tag-check.csv')))}
for r in pool: r['v2'] = tag(r['title'])
WRONG = {0, 3, 5, 7, 10, 11, 13, 17, 18, 24, 26, 33, 37, 42, 47, 50, 53, 54, 58, 77, 84, 90, 92, 93, 94, 99, 100, 102, 103, 105, 106, 107,
         110, 111, 116, 117, 118, 124, 125, 126, 127, 130, 132, 139, 142, 143, 146, 148, 158, 159, 161, 163, 165, 169, 176, 178,
         180, 182, 184, 196, 197, 199, 203, 205, 206}
MISSED = {210: 'math', 211: 'sound', 215: 'space', 218: 'space', 220: 'nuclear_particle', 227: 'engineering', 229: 'electric', 232: 'math',
          233: 'engineering', 239: 'nuclear_particle', 240: 'engineering', 241: 'heat_energy', 242: 'math', 250: 'electric', 252: 'math',
          255: 'space', 256: 'engineering', 257: 'electric', 260: 'engineering', 261: 'space', 265: 'history_people', 267: 'math'}
rnd = random.Random(12); out = []
for c in CLUSTERS:
    for r in rnd.sample([r for r in pool if c in r['v2'] and r['url'] not in seen], 10):
        out.append({'check': 'tagged', 'cluster': c, 'title': r['title'], 'all_clusters': ';'.join(r['v2']), 'url': r['url']})
for r in rnd.sample([r for r in pool if not r['v2'] and r['url'] not in seen], 60):
    out.append({'check': 'untagged', 'cluster': '', 'title': r['title'], 'all_clusters': '', 'url': r['url']})
for i, r in enumerate(out):
    r['correct'] = ('no' if i in WRONG else 'yes') if r['check'] == 'tagged' else ('no' if i in MISSED else 'yes')
    r['missed_cluster'] = MISSED.get(i, '')
with open(os.path.join(DOCS, 'tag-check-v2.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator='\n'); w.writeheader(); w.writerows(out)
print('tagged correct', sum(r['correct'] == 'yes' for r in out if r['check'] == 'tagged'), 'of', sum(r['check'] == 'tagged' for r in out),
      '| untagged with a missed cluster', len(MISSED), 'of 60')
```

## title_phrases.py

Формулировки названий.

```python
"""Title wording inside physics-core reference channels: median ratio to neighbours by title pattern,
with channel-level resampling (4000 rounds, seed 7) and Bonferroni for 8 patterns.
Run: tmp/venv/bin/python -I tmp/research/title_phrases.py"""
import csv, os, random, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
PHYS = {'physics-general', 'physics-deep', 'physics-animation', 'physics-news', 'physics-opinion', 'physics-history', 'physics-interview',
        'experiments', 'simulation', 'science-animation', 'science-general', 'education', 'math-physics', 'space', 'space-news'}
PAT = {'what is / explained / basics': r"^what is\b|explained|\bbasics\b|for beginners",
       'impossible / strange / mind': r"impossible|strange|\bmind",
       'superlative': r"\b(most|biggest|largest|smallest|fastest|strongest|hottest|coldest|deadliest|craziest|weirdest)\b",
       'lie / wrong / myth': r"\blies?\b|\bwrong\b|\bmyths?\b", 'starts with why': r"^why\b", 'starts with how': r"^how\b", 'starts with what if': r"^what if\b", 'starts with this': r"^this\b"}
pool = [r for r in csv.DictReader(open(os.path.join(DOCS, 'videos.csv')))
        if r['kind'] in PHYS and r['ratio_to_typical'] and r['format'] == 'long' and 30 <= int(r['age_days']) <= 5 * 365]
for r in pool: r['x'] = float(r['ratio_to_typical'])
chs = sorted({r['channel'] for r in pool}); rnd = random.Random(7); N = 4000
draws = [[rnd.choice(chs) for _ in chs] for _ in range(N)]
a = 0.10 / len(PAT) / 2
def qt(xs, p): xs = sorted(xs); return xs[min(len(xs) - 1, max(0, int(p * len(xs))))]
rows = []
for name, rx in PAT.items():
    vs = [r for r in pool if re.search(rx, r['title'].strip(), re.I)]
    cv = {}
    for r in vs: cv.setdefault(r['channel'], []).append(r['x'])
    meds = [st.median(xs) for d in draws if (xs := [x for ch in d for x in cv.get(ch, ())])]
    own = [st.median(x) for x in cv.values() if len(x) >= 3]
    rows.append({'pattern': name, 'n_videos': len(vs), 'n_channels': len(cv), 'median_ratio': round(st.median(r['x'] for r in vs), 2),
                 'ci90_low': round(qt(meds, .05), 2), 'ci90_high': round(qt(meds, .95), 2), 'ci_adj_low': round(qt(meds, a), 2), 'ci_adj_high': round(qt(meds, 1 - a), 2),
                 'channels_3plus': len(own), 'share_channels_above_1': round(sum(m > 1 for m in own) / len(own), 2) if own else ''})
with open(os.path.join(DOCS, 'title-wording.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print('pool', len(pool), 'channels', len(chs), 'median', st.median(r['x'] for r in pool))
for r in rows: print(r)
```

## newdenom.py

Знаменатель новых каналов: возраст и релевантность кандидатов, порог заметности, форматы.

```python
"""Denominators for new channels. Scope: English physics-leaning channels from the search sample whose age was 'yes' or 'unknown'
after the first pass (30 latest videos, deep list under 500): the same 1011 channels as agecheck.py and the relevance check.
Age (raw/age.json, agecheck.py): confirmed new = joined under 365 days ago, or a complete list of public uploads (count not below the
/about count, under the list cap) whose oldest upload is under 365 days old; not new = an upload 365+ days old; otherwise unconfirmed.
Relevance (out/relevance/result-*.csv): one blind check of every channel by its titles, traction hidden: yes / exam / offtopic / fiction / nonenglish, plus an unsure flag.
Shares are given three ways: relevant as labelled; strict (unsure 'yes' counted as not relevant); loose (unsure 'no' counted as relevant).
Threshold: median of the latest 10 videos (7+ days old) >= 1000 views, or >= 10000 subscribers. Formats: title words in 30%+ of a channel's titles.
Run: tmp/venv/bin/python -I tmp/research/newdenom.py"""
import csv, json, os, re, statistics as st, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
FMT = {'sleep': r'for sleep|sleep|fall asleep|bedtime|relax|calm',
       'every_type': r'every type|every kind|all types|types of',
       'simulation': r'simulat|satisfying',
       'how_it_works': r'actually work|how .* works?\b|how does'}
fc = list(csv.DictReader(open(os.path.join(OUT, 'found-channels.csv'))))
F = json.load(open(os.path.join(RAW, 'found.json')))
A = json.load(open(os.path.join(RAW, 'age.json')))
L = {}
for fn in ('result-a.csv', 'result-b.csv'):
    for r in csv.DictReader(open(os.path.join(OUT, 'relevance', fn))): L[r['channel_id']] = r

def age(a):
    """(status, oldest public upload, public uploads listed, source)"""
    if not a or 'error' in a['about']: return 'unconfirmed', '', '', 'about page not read'
    m = datetime.date.fromisoformat(a['measured'][:10]); j = datetime.date.fromisoformat(a['about']['joined'])
    if (m - j).days < 365: return 'new', '', '', 'joined under 365 days ago'
    lists = list(a['tabs'].values()) if 'tabs' in a else [a.get('uploads', {})]
    cap = 1000 if 'tabs' in a else 5000
    dates = [t['last_date'] for t in lists if re.match(r'\d{4}-', str(t.get('last_date', '')))]
    n = sum(t.get('n', 0) for t in lists); oldest = min(dates) if dates else ''
    src = 'tabs videos, shorts, streams' if 'tabs' in a else 'uploads playlist'
    if oldest and (m - datetime.date.fromisoformat(oldest)).days >= 365: return 'not new', oldest, n, src
    if any('error' in t or str(t.get('last_date', '')).startswith('error') for t in lists): return 'unconfirmed', oldest, n, src + ': read error'
    if any(t.get('n', 0) >= cap for t in lists): return 'unconfirmed', oldest, n, src + f': list cap {cap}'
    vc = a['about'].get('video_count')
    if vc is None or n < vc or not oldest: return 'unconfirmed', oldest, n, src + f': listed {n} of {vc}'
    return 'new', oldest, n, src + ': complete list'

rows = []
for r in fc:
    if r['new_le_365d'] not in ('yes', 'unknown') or float(r['physics_title_share']) < 0.3 or float(r['english_title_share']) < 0.8: continue
    a = A.get(r['channel_id']); status, oldest, n, src = age(a)
    titles = ' | '.join(v.get('title') or '' for v in F.get(r['channel_id'], {}).get('videos', []))
    passed = float(r['median_views_latest10_ge7d'] or 0) >= 1000 or int(r['subs'] or 0) >= 10000
    f = {k: len(re.findall(v, titles, re.I)) for k, v in FMT.items()}
    nv = max(1, len(F.get(r['channel_id'], {}).get('videos', [])))
    l = L[r['channel_id']]
    rows.append({'channel_id': r['channel_id'], 'channel': r['channel'], 'url': r['url'], 'subs': r['subs'],
                 'first_pass_new': r['new_le_365d'], 'age_status': status, 'joined': a['about'].get('joined', '') if a else '',
                 'about_video_count': a['about'].get('video_count', '') if a else '', 'public_uploads_listed': n, 'oldest_public_upload': oldest,
                 'age_source': src, 'age_measured': a['measured'] if a else '',
                 'relevant': l['relevant'], 'relevance_reason': l['reason'], 'relevance_unsure': l['unsure'],
                 'median_views_latest10_ge7d': r['median_views_latest10_ge7d'], 'passed_threshold': 'yes' if passed else 'no',
                 'title_format_30pct': ';'.join(k for k in FMT if f[k] / nv >= 0.3)})
with open(os.path.join(DOCS, 'new-channels-all.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
from collections import Counter
print('scope', len(rows), Counter(r['age_status'] for r in rows), 'first pass yes', Counter(r['age_status'] for r in rows if r['first_pass_new'] == 'yes'))
print('unconfirmed reasons', Counter(re.sub(r'\d+', 'N', r['age_source']) for r in rows if r['age_status'] == 'unconfirmed'))
REL = {'as labelled': lambda r: r['relevant'] == 'yes',
       'strict': lambda r: r['relevant'] == 'yes' and r['relevance_unsure'] != 'yes',
       'loose': lambda r: r['relevant'] == 'yes' or r['relevance_unsure'] == 'yes'}
old = [r for r in rows if r['first_pass_new'] == 'yes']
print('first pass (automatic only):', sum(r['passed_threshold'] == 'yes' for r in old), 'of', len(old))
for name, ok in REL.items():
    for st_ in ('new', 'new or unconfirmed'):
        g = [r for r in rows if ok(r) and (r['age_status'] == 'new' or (st_ != 'new' and r['age_status'] == 'unconfirmed'))]
        p = sum(r['passed_threshold'] == 'yes' for r in g)
        xs = [float(r['median_views_latest10_ge7d']) for r in g if r['median_views_latest10_ge7d']]
        print(f'{name:12} {st_:20} channels {len(g)} passed {p} share {p / len(g):.3f} median latest10 {st.median(xs) if xs else ""}')
main = [r for r in rows if REL['as labelled'](r) and r['age_status'] == 'new']
for k in list(FMT) + ['(none)']:
    g = [r for r in main if (k in r['title_format_30pct'].split(';') if k != '(none)' else not r['title_format_30pct'])]
    p = sum(r['passed_threshold'] == 'yes' for r in g)
    print('format', k, 'channels', len(g), 'passed', p, f'{p / len(g):.2f}' if g else '')
print('new (all labels):', sum(r['age_status'] == 'new' for r in rows), 'of them account older than 365 days, all public uploads younger:',
      sum(r['age_status'] == 'new' and r['age_source'] != 'joined under 365 days ago' for r in rows))
print('relevant new: account older than 365 days', sum(1 for r in main if r['age_source'] != 'joined under 365 days ago'))
for name, ok in REL.items():  # stricter age: the account itself joined under 365 days ago
    g = [r for r in rows if ok(r) and r['age_status'] == 'new' and r['age_source'] == 'joined under 365 days ago']
    p = sum(r['passed_threshold'] == 'yes' for r in g)
    print(f'{name:12} joined <365d          channels {len(g)} passed {p} share {p / len(g):.3f}')
xs = sorted(float(r['median_views_latest10_ge7d']) for r in main if r['median_views_latest10_ge7d'])
print('relevant new with views', len(xs), 'median', st.median(xs), 'quartiles', st.quantiles(xs, n=4), 'top 10% from', st.quantiles(xs, n=10)[-1])

# Denominator for small-channel videos in "this month" results: unique long videos aged 7..30 days of channels under 100k subscribers
sv = {}
for r in csv.DictReader(open(os.path.join(DOCS, 'search-videos.csv'))):
    if r['filter'] == 'month': sv.setdefault(r['id'], r)
v = [r for r in sv.values() if r['duration'] and float(r['duration']) > 180 and r['age'] and 7 <= float(r['age']) <= 30 and r['subs'] and int(r['subs']) < 100000 and r['view_count']]
hit = [r for r in v if int(r['view_count']) >= 10000]
nv = [r for r in v if r['new'] == 'True']
print('small-channel videos 7-30d', len(v), 'with 10k+', len(hit), 'median views', st.median(int(r['view_count']) for r in v))
print('of them from new channels', len(nv), 'with 10k+', sum(int(r['view_count']) >= 10000 for r in nv), 'median views', st.median(int(r['view_count']) for r in nv))
print('10k+ videos by channel age: new', sum(r['new'] == 'True' for r in hit), 'not new', sum(r['new'] == 'False' for r in hit), 'unknown', sum(r['new'] not in ('True', 'False') for r in hit))
```

## topicmap.py

Тематическая карта.

```python
"""Combine the three indicators per topic cluster into data/topic-map.csv. Run: tmp/venv/bin/python -I tmp/research/topicmap.py"""
import csv, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
# cluster names differ per source; map them onto one list
MAP = {  # topic map cluster: (trends clusters, search clusters, in-channel tags)
 'space_scale': (['space'], ['space'], ['space', 'scale']),
 'relativity_time': (['relativity'], ['relativity'], ['relativity_time']),
 'quantum': (['quantum'], ['quantum'], ['quantum']),
 'magnetism': (['magnet'], ['magnet'], ['magnet']),
 'electricity': (['electric'], ['electric'], ['electric']),
 'light_colour': (['light'], ['light'], ['light']),
 'energy_heat': (['energy'], ['energy'], ['heat_energy']),
 'mechanics_flight': (['mechanics'], ['mechanics', 'fluids'], ['mechanics', 'fluids_flight']),
 'gravity': (['gravity'], ['gravity'], ['gravity']),
 'sound_waves': (['sound'], ['sound'], ['sound']),
 'matter_particles': (['matter'], ['matter', 'particle'], ['matter', 'nuclear_particle']),
 'everyday': (['everyday'], ['everyday'], ['everyday']),
 'paradox_myth': (['paradox'], ['paradox'], ['paradox_puzzle']),
 'simulation_experiment': (['general'], ['general'], ['experiment']),
}
# priority waves are research hypotheses for a pilot, not proven wins (see topics.md#приоритеты)
WAVE = {'relativity_time': '1', 'quantum': '1', 'space_scale': '1 (only with a clear difference)', 'magnetism': '1 (weak: few channels)',
        'electricity': '2', 'energy_heat': '2', 'mechanics_flight': '2', 'light_colour': '2',
        'matter_particles': '2', 'paradox_myth': 'format, not a topic', 'simulation_experiment': 'format, not a topic',
        'gravity': '3', 'sound_waves': '3', 'everyday': 'hypothesis: hook to a deeper topic; demand of the whole topic not measured'}
T = list(csv.DictReader(open(os.path.join(D, 'trends.csv'))))
S = list(csv.DictReader(open(os.path.join(D, 'search-queries.csv'))))
IV = {}  # dictionary version -> cluster -> row; v1 = topics.py, v2 = corrected topics_v2.py
for r in csv.DictReader(open(os.path.join(D, 'topics-by-channel-resampling.csv'))): IV.setdefault(r['dictionary'], {})[r['cluster']] = r
TCV = {}  # dictionary version -> cluster -> manual verdicts of 10 tagged titles
for v, fn in (('v1', 'tag-check.csv'), ('v2', 'tag-check-v2.csv')):
    for r in csv.DictReader(open(os.path.join(D, fn))):
        if r['check'] == 'tagged': TCV.setdefault(v, {}).setdefault(r['cluster'], []).append(r['correct'] == 'yes')
def f(x):
    try: return float(x)
    except: return None
def md(xs, n=3):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), n) if xs else ''
AMBIG = {'rainbow', 'lightning', 'gravity', 'resonance', 'plasma'}  # many meanings outside physics (songs, games, films)
rows = []
for k, (tc, sc, ic) in MAP.items():
    tt = [r for r in T if r['cluster'] in tc and f(r['rel_physics']) is not None and r['term'] not in AMBIG]
    sa = [r for r in S if r['cluster'] in sc and r['filter'] == 'any']
    sm = [r for r in S if r['cluster'] in sc and r['filter'] == 'month']
    ii = [IV['v1'][c] for c in ic if c in IV['v1']]; i2 = [IV['v2'][c] for c in ic if c in IV['v2']]
    best = max(tt, key=lambda r: f(r['rel_physics'])) if tt else None
    rows.append({'topic': k,
        'trends_terms': len(tt), 'trends_top_term': best['term'] if best else '', 'trends_top_rel_physics': best['rel_physics'] if best else '',
        'trends_median_rel_physics': md([f(r['rel_physics']) for r in tt], 4),
        'trends_median_change_1y': md([f(r['chg_1y']) for r in tt]),
        'search_queries': len(sa), 'search_top20_median_views_per_year': md([f(r['top20_median_views_per_year']) for r in sa], 0),
        'search_top20_share_older_3y': md([f(r['top20_share_older_3y']) for r in sa], 2),
        'search_month_small_channel_median_views': md([f(r['long_7_30d_subs_lt10k_median']) for r in sm], 0),
        'in_channel_tags': ';'.join(ic), 'in_channel_videos': sum(int(r['n_videos']) for r in ii),
        'in_channel_median_ratio': ';'.join(r['median_ratio'] for r in ii),
        'in_channel_ci90_by_channel': ';'.join(f"{r['ci90_low']}-{r['ci90_high']}" for r in ii),
        'in_channel_ci_bonferroni21': ';'.join(f"{r['ci_adj21_low']}-{r['ci_adj21_high']}" for r in ii),
        'in_channel_share_channels_above_1': ';'.join(str(r['share_channels_above_1']) for r in ii),
        'tag_precision_of_10': ';'.join(str(sum(TCV['v1'].get(c, []))) for c in ic),
        'in_channel_median_ratio_v2': ';'.join(r['median_ratio'] for r in i2),
        'in_channel_ci_bonferroni21_v2': ';'.join(f"{r['ci_adj21_low']}-{r['ci_adj21_high']}" for r in i2),
        'tag_precision_of_10_v2': ';'.join(str(sum(TCV['v2'].get(c, []))) for c in ic),
        'priority_wave': WAVE[k], 'measured': '2026-10-16',
        'note': 'search interest = Google Trends YouTube Search US, share vs physics; views = public totals, not retention or revenue; in-channel = video vs 10 neighbours of the same channel, intervals resample whole channels, 100000 rounds; v1 = first word dictionary, v2 = corrected one, both about 70% precise; trends = single terms, not demand of the whole topic'})
with open(os.path.join(D, 'topic-map.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
for r in rows: print(r['topic'], r['trends_top_term'], r['trends_median_rel_physics'], r['search_top20_median_views_per_year'], r['in_channel_median_ratio'], r['priority_wave'])
```

## thumbs.py

Листы обложек для чтения стиля; в проекте не хранятся.

```python
"""Contact sheets of public thumbnails for a qualitative look at visual style. Not stored in docs.
Run: /home/boardagent/.explainer/venv/bin/python -I tmp/research/thumbs.py <out.png> <key> [<key> ...]"""
import json, os, sys, io, urllib.request, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
C = {}
for n in ('seeds.json', 'found.json', 'deep.json'):
    p = os.path.join(RAW, n)
    if os.path.exists(p):
        for k, r in json.load(open(p)).items():
            if 'error' not in r: C[k] = r; C[r.get('channel_id') or k] = r
out, keys = sys.argv[1], sys.argv[2:]
W, H = 320, 180
def get(vid):
    try: return Image.open(io.BytesIO(urllib.request.urlopen(f'https://i.ytimg.com/vi/{vid}/mqdefault.jpg', timeout=20).read())).convert('RGB').resize((W, H))
    except Exception: return Image.new('RGB', (W, H), (60, 0, 0))
rows = []
for k in keys:
    r = C[k]; vs = [v for v in r['videos'] if (v.get('duration') or 0) > 180][:3]
    top = max(r['videos'], key=lambda v: v.get('view_count') or 0)
    rows.append((r['channel'], [v['id'] for v in vs] + [top['id']]))
sheet = Image.new('RGB', (W * 4 + 200, H * len(rows)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
with cf.ThreadPoolExecutor(8) as ex:
    for i, (name, ids) in enumerate(rows):
        d.text((6, i * H + 8), name[:26], fill=(255, 255, 255))
        for j, im in enumerate(ex.map(get, ids)): sheet.paste(im, (200 + j * W, i * H))
sheet.save(out); print(out, sheet.size)
```

## frames.py

Кадры из самих роликов ключевых каналов; видео удаляется сразу.

```python
"""Representative frames: for each key channel take its latest long video at least 14 days old
(not its best one) lasting at least half the channel's median duration and grab 8 frames at 6..94% of the duration, tiled 4x2.
Run: tmp/venv/bin/python -I tmp/research/frames.py  (needs yt-dlp and ffmpeg; downloads each 360p video, then deletes it)"""
import csv, json, os, subprocess, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
OUT = os.path.join(HERE, '..', 'frames'); os.makedirs(OUT, exist_ok=True)
FF = '/home/boardagent/.explainer/bin/ffmpeg'
KEY = ['Kurzgesagt – In a Nutshell', 'Veritasium', 'Steve Mould', 'The Action Lab', 'AlphaPhoenix', 'Sebastian Lague', 'Primer',
       'ScienceClic English', 'FloatHeadPhysics', 'Science ABC', 'The Engineering Mindset', 'MetaBallStudios', 'Looking Glass Universe',
       'Physics Videos by Eugene', 'minutephysics', '3Blue1Brown', 'Branch Education', 'PBS Space Time', 'Sleep On Physics', 'Bluntly Explained',
       'Animated Physics', 'Hardwired YouTube', '2D Satisfying', 'The Overview Effekt', 'Sabins', 'Imagine the Physics', 'Sabin Civil', 'Science Time']
chan = {r['channel'].strip(): r for r in csv.DictReader(open(os.path.join(DOCS, 'channels.csv')))}
vids = {}
for r in csv.DictReader(open(os.path.join(DOCS, 'videos.csv'))):
    vids.setdefault(r['channel'].strip(), []).append(r)
raw = {}
for n in ('found.json', 'deep.json'):
    for k, v in json.load(open(os.path.join(RAW, n))).items():
        if 'error' not in v and v.get('videos'): raw[k] = v
picked = []
for name in KEY:
    cands = [k for k in chan if k.startswith(name)]
    if not cands: print('no channel', name); continue
    c = chan[cands[0]]; cid = c['url'].rsplit('/', 1)[-1]
    if cands[0] in vids:
        md = float(c['median_duration_min_last30'] or 0) * 60
        vs = [v for v in vids[cands[0]] if v['format'] == 'long' and int(v['age_days']) >= 14 and float(v['duration_s'] or 0) >= md / 2]
        vs.sort(key=lambda v: int(v['age_days']))
        if vs: picked.append((cands[0], vs[0]['video_id'], vs[0]['title'], int(float(vs[0]['duration_s'])))); continue
    r = raw.get(cid)
    if not r: print('no raw', name); continue
    m = datetime.datetime.fromisoformat(r['measured']).timestamp()
    vs = [v for v in r['videos'] if (v.get('duration') or 0) > 180 and v.get('timestamp') and (m - v['timestamp']) / 86400 >= 14]
    vs.sort(key=lambda v: -v['timestamp'])
    if vs: picked.append((cands[0], vs[0]['id'], vs[0]['title'], int(vs[0]['duration'])))
    else: print('no long video', name)
import time
log, fails = [], 0
for name, vid, title, dur in picked:
    slug = ''.join(ch for ch in name if ch.isalnum())[:24]
    dst = os.path.join(OUT, f'{slug}-{vid}.jpg')
    if os.path.exists(dst): log.append((name, vid, title, dur, 'cached')); continue
    u = os.path.join(OUT, f'_{vid}.mp4')
    try:
        subprocess.run([os.path.join(os.path.dirname(sys.executable), 'yt-dlp'), '-q', '--no-warnings', '-f', 'bv*[height<=360][ext=mp4]/bv*[height<=360]',
                        '-o', u, f'https://www.youtube.com/watch?v={vid}'], timeout=900)
    except Exception as e:
        log.append((name, vid, title, dur, f'download error {e}')); continue
    time.sleep(45)  # YouTube asks to sign in after a burst of downloads; go slowly, never sign in
    if not os.path.exists(u):
        log.append((name, vid, title, dur, 'download failed')); print(log[-1], flush=True); fails += 1
        if fails >= 3: print('stopped: 3 failures in a row', flush=True); break
        continue
    fails = 0
    parts = []
    for i, p in enumerate((.06, .18, .30, .42, .54, .66, .80, .94)):
        f = os.path.join(OUT, f'_{i}.jpg')
        subprocess.run([FF, '-v', 'error', '-y', '-ss', str(int(dur * p)), '-i', u, '-frames:v', '1', '-vf', 'scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2', f], timeout=120)
        if os.path.exists(f): parts.append(f)
    if len(parts) == 8:
        subprocess.run([FF, '-v', 'error', '-y'] + sum((['-i', p] for p in parts), []) +
                       ['-filter_complex', ''.join(f'[{i}]' for i in range(8)) + 'xstack=inputs=8:layout=0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0', dst])
    for p in parts: os.remove(p)
    os.remove(u)
    log.append((name, vid, title, dur, 'ok' if os.path.exists(dst) else f'{len(parts)} frames'))
    print(log[-1], flush=True)
with open(os.path.join(OUT, 'frames.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['channel', 'video_id', 'title', 'duration_s', 'status']); w.writerows(log)
```

## registry.py

Реестр каналов data/channels.csv.

```python
"""Build the channel registry and the video registry for docs/physics-research/data.
Run: tmp/venv/bin/python -I tmp/research/registry.py"""
import json, os, csv, statistics as st, datetime, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(HERE, 'out')
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
sys.path.insert(0, HERE)
from topics import tag
PHYS = {'light', 'sound', 'magnet', 'electric', 'heat_energy', 'nuclear_particle', 'quantum', 'relativity_time', 'space', 'gravity', 'mechanics', 'fluids_flight', 'matter'}
def load(n):
    p = os.path.join(RAW, n); return json.load(open(p)) if os.path.exists(p) else {}
def med(xs):
    xs = [x for x in xs if x is not None]; return st.median(xs) if xs else None
def ts(iso): return datetime.datetime.fromisoformat(iso).timestamp()
def day(t): return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%d') if t else ''
def tier(s):
    if s is None: return 'неизвестно'
    return 'от 1 млн' if s >= 1_000_000 else '100 тыс.–1 млн' if s >= 100_000 else '10–100 тыс.' if s >= 10_000 else 'меньше 10 тыс.'

# Qualitative notes: judged from public thumbnails and titles of recent videos on 2026-10-16; videos were not watched in full.
# Channels in FRAMES were also checked on 8 frames of one recent typical video (tmp/research/frames.py). Voice and sound were not checked.
FRAMES = {}
_fp = os.path.join(HERE, '..', 'frames', 'frames.csv')
if os.path.exists(_fp):
    for _r in csv.DictReader(open(_fp)):
        if _r['status'] in ('ok', 'cached'): FRAMES[_r['channel'].strip()] = _r['video_id']
STYLE = {
 '@veritasium': ('ведущий и интервью на выездах, рисованная 2D-анимация, чистые схемы, архивные газеты', 'длинные расследования 20–40 мин'),
 '@kurzgesagt': ('плоская векторная иллюстрация, насыщенная палитра, студийная анимация, без ведущего', '10–15 мин, редкий выпуск'),
 '@minutephysics': ('рисунок маркером на белом и реальная съёмка, короткие объяснения', '3–8 мин'),
 '@pbsspacetime': ('ведущий и космические VFX, неоновые титры, глубокая теория', '15–20 мин'),
 '@SteveMould': ('настольные опыты на светлом фоне, крупные планы, чистые 2D-схемы, ведущий и гости в кадре', '10–20 мин'),
 '@smartereveryday': ('ведущий, высокоскоростная съёмка, выезды', '15–35 мин'),
 '@physicsgirl': ('ведущая и опыты; канал почти не выходит', 'нет свежих'),
 '@SabineHossenfelder': ('говорящая голова, новости физики и мнения, частый выпуск', '6–8 мин, 16 в месяц'),
 '@ScienceAsylum': ('ведущий и рисование от руки, юмор', '8–12 мин'),
 '@TheActionLab': ('ведущий в студии, опыты, простая 2D и 3D-графика', '8–10 мин'),
 '@3blue1brown': ('код-анимация Manim, превращения объектов в одной сцене', '20–30 мин'),
 '@PrimerBlobs': ('Blender-симуляции с персонажами-каплями (по обложкам); в проверенном ролике ведущий в белой студии и графики данных', 'редкий выпуск'),
 '@AlphaPhoenixChannel': ('ведущий в кадре, выезд в лабораторию, замедленная съёмка, графики симуляций, страницы статей', '20–25 мин, редкий'),
 '@kylehill': ('ведущий в студии, монтаж с архивом и графикой', '15–20 мин'),
 '@upandatom': ('ведущая в кадре и 2D-графика', '15–20 мин'),
 '@LookingGlassUniverse': ('ведущая, квантовая физика; в проверенном ролике только говорящая голова', '15–20 мин'),
 '@ScienceClicEN': ('3D-визуализация пространства-времени и полей, без ведущего', '10–15 мин, редкий'),
 '@ArvinAsh': ('ведущий и CGI, «почему» до фундаментального уровня', '15 мин'),
 '@astrumspace': ('космос: рендеры и снимки миссий, диктор', '20–30 мин'),
 '@DomainofScience': ('карты науки, рисунок', 'редкий'),
 'UCGfFUc6eWxfbtjYeun6r9xg': ('ведущий-ученик в кадре, анимированные мысленные опыты, «I finally understood»', '20–25 мин'),
 '@HuygensOptics': ('оптические опыты в мастерской', '25 мин'),
 '@BranchEducation': ('фотореалистичные 3D-разрезы устройств', '20 мин, редкий'),
 '@Animagraffs': ('технические 3D-рендеры механизмов', '30 мин, редкий'),
 'UCqZQJ4600a9wIfMPbYc60OQ': ('простая 3D-анимация строительства, ведущий вырезан поверх сцены (бывший Lesics)', '12 мин'),
 'UCk0fGHsCEzGig-rSzkfCjMw': ('плоские 2D-схемы на синей сетке-чертеже, электротехника', ''),
 '@JaredOwen': ('3D-анимация «как устроено»', '15 мин, редкий'),
 '@MinuteEarth': ('рисованная 2D-анимация', '4 мин'),
 '@SciShow': ('ведущие и стоковые кадры', '11 мин, 17 в месяц'),
 '@TEDEd': ('разные иллюстраторы, 2D', '6 мин'),
 'UC7BhHN8NyMMru2RUygnDXSg': ('коллаж, мемы, уровни сложности', '12 мин'),
 '@EugeneKhutoryansky': ('3D-анимация полей и волн без ведущего', '8 мин, редкий'),
 '@PhysicswithElliot': ('ведущий и формулы, для студентов', '17 мин'),
 '@melodysheep': ('кинематографичная CGI, музыка, масштаб времени', '8 мин, редкий'),
 '@SebastianLague': ('визуализации кода, модели Blender, сборка устройства в кадре', '33 мин'),
 '@ScienceABC': ('подробные иллюстрации с персонажами, генеративные на вид, бытовые вопросы', '4 мин'),
 '@RealScience': ('документальный монтаж и графика', '23 мин'),
 '@CleoAbram': ('ведущая, оптимистичная техника', '18 мин'),
 '@MetaBallStudios': ('3D-сравнения масштаба', '7 мин'),
 '@ScienceTime24': ('реалистичная CGI космоса с подписями расстояний; в проверенном ролике без интервью', '12 мин'),
 'UC9Ep0Y4T5rvUuIfjKN1wqTw': ('драматичные иллюстрации, космос и катастрофы', '19 мин'),
 '@PhysicsExplainedVideos': ('формулы и чистые схемы, история открытий', '40 мин'),
}
NEWNOTES = {
 'Bluntly Explained': 'сетки «every type of X», генеративные на вид картинки, рисованный персонаж',
 'Imagine the Physics': 'стоковые кадры и крупные субтитры; на обложках образ Фейнмана, опирается на чужой образ',
 'Orbitimbre': 'мультяшные планеты-персонажи, «X против Y»',
 'Mr. Physik': 'новости физики, архивные статьи, 2D/3D',
 'Animated Physics': '3D-сцены в реалистичном окружении, лучи и формулы поверх, архивные рукописи',
 'Hardwired YouTube': 'схемы и анимация частиц на тёмной сетке, моноширинные подписи, архивные портреты, «how it actually works»',
 'Secrets of Everyday Things': '«How It’s Made» бытовых вещей, генеративные на вид обложки',
 'ExhaustTV': 'авиация, схемы и рендеры со стрелками',
 'Sleep On Physics': 'физика для сна 1,5–2 ч, стоковые космические фоны',
 'Calm Science': 'физика для сна, генеративные на вид картинки',
 'The Roger Physics': 'образ Роджера Пенроуза на обложках',
 'Feynman Reborn': 'образ Фейнмана на обложках',
 'ResCom Contractors': 'чистые схемы-разрезы домашних систем',
 'Space Dude': 'списки «chilling reasons», генеративные на вид картинки',
 'Mr Space Explainer': 'списки и масштабы космоса',
 'The Overview Effekt': 'пастельные 3D-модели масштаба и времени, архивные фото миссий, схемы, цитаты',
 'braintruffle': 'чистые 2D-схемы механики и жидкостей',
 'Sabins': 'простая 3D-анимация: учёные прошлого и их опыты, формулы; ведущий-преподаватель в кадре',
 'But Why?': '3D-персонаж и физика, семейный тон',
 'Klonusk': 'простые учебные схемы',
 'What The Physics?!': 'ведущий PBS и графика',
 '2D Satisfying': 'симуляции «шарики в круге» на чёрном со счётчиками',
}

seeds = json.load(open(os.path.join(HERE, 'seeds.json')))
meta = {c[0]: (c[1], c[2]) for c in seeds['channels']}
SEG_KIND = {'other-market': 'другой рынок', 'visual-ref': 'визуальный ориентир', 'simulation': 'визуальный ориентир',
            'engineering-animation': 'визуальный ориентир', 'scale-comparison': 'визуальный ориентир', '3d-shorts': 'визуальный ориентир'}
DIRECT = {'@minutephysics', '@ScienceAsylum', '@upandatom', 'UCGfFUc6eWxfbtjYeun6r9xg', '@ScienceClicEN', 'UC7BhHN8NyMMru2RUygnDXSg',
          '@PhysicsExplainedVideos', '@ArvinAsh', '@ScienceABC', '@EugeneKhutoryansky', '@LookingGlassUniverse', '@physicsgirl', '@SteveMould', '@TheActionLab'}
sc = {r['key']: r for r in csv.DictReader(open(os.path.join(OUT, 'seed-channels.csv')))}
rows = []
for key, (grp, kind) in meta.items():
    r = sc.get(key)
    if not r or r['error']: continue
    subs = int(r['subs']) if r['subs'] else None
    seg = 'прямой конкурент' if key in DIRECT else SEG_KIND.get(kind) or ('крупный ориентир' if (subs or 0) >= 1_000_000 else 'средний')
    s = STYLE.get(key, ('', ''))
    rows.append({'segment': seg, 'channel': r['channel'], 'url': r['url'], 'source': 'ориентир (список исследования)', 'kind': kind, 'subs': subs,
                 'subs_tier': tier(subs), 'measured': r['measured'], 'first_upload_known': r['first_upload_if_complete'],
                 'new_le_12_months': 'нет' if r['first_upload_if_complete'] or r['list_complete'] == 'no' else '',
                 'uploads_per_month_12m': r['uploads_per_month_365d'], 'median_duration_min_last30': r['median_duration_min_last30'],
                 'typical_views_30_365d': r['typical_views_30_365d'], 'typical_views_1_3y': r['typical_views_1_3y'],
                 'recent_vs_older': r['trajectory_recent_vs_1_3y'], 'shorts_median_views': r['shorts_median_views'],
                 'top_video': r['top_title'], 'top_url': r['top_url'], 'top_views': r['top_views'], 'top_age_days': r['top_age_days'],
                 'strong_recent': r['best_recent_title'], 'strong_recent_url': r['best_recent_url'], 'strong_recent_views': r['best_recent_views'], 'strong_recent_x_neighbours': r['best_recent_ratio'],
                 'weak_recent': r['weak_recent_title'], 'weak_recent_url': r['weak_recent_url'], 'weak_recent_views': r['weak_recent_views'], 'weak_recent_x_neighbours': r['weak_recent_ratio'],
                 'style_notes': s[0], 'format_notes': s[1], 'style_source': ('обложки, названия и 8 кадров ролика ' + FRAMES[r['channel'].strip()]) if r['channel'].strip() in FRAMES else ('обложки и названия' if s[0] else ''), 'flags': ''})
# discovered channels: new (first upload within 12 months), English, physics-leaning, with traction; plus rising named ones
F = load('found.json'); D = load('deep.json')
fc = {r['channel_id']: r for r in csv.DictReader(open(os.path.join(OUT, 'found-channels.csv')))}
seed_ids = {sc[k]['url'].rsplit('/', 1)[-1] for k in sc if not sc[k]['error']}
# age and relevance of new-channel candidates: data/new-channels-all.csv (newdenom.py: agecheck.py + one blind relevance check for all)
NC = {r['channel_id']: r for r in csv.DictReader(open(os.path.join(DOCS, 'new-channels-all.csv')))}
def is_new(cid): return cid in NC and NC[cid]['age_status'] == 'new'
def relevant(cid): return cid in NC and NC[cid]['relevant'] == 'yes'
# comparison group: a seeded random sample of 40 confirmed new, relevant channels that did not pass the traction threshold
import random
_weak = sorted(cid for cid, r in fc.items() if r['channel'] not in NEWNOTES and is_new(cid) and relevant(cid)
               and not (float(r['median_views_latest10_ge7d'] or 0) >= 1000 or int(r['subs'] or 0) >= 10000))
WEAK = set(random.Random(5).sample(_weak, min(40, len(_weak))))
print('comparable new channels below threshold', len(_weak))
for cid, r in fc.items():
    named = r['channel'] in NEWNOTES
    phys, eng = float(r['physics_title_share']), float(r['english_title_share'])
    lat = float(r['median_views_latest10_ge7d'] or 0); subs = int(r['subs'] or 0); mx = int(r['max_views_30'] or 0)
    new = is_new(cid)
    if named and not new and subs < 10000: continue
    weak = not named and new and relevant(cid) and not (lat >= 1000 or subs >= 10000)
    if weak and cid not in WEAK: continue
    if not named and not weak and not (new and relevant(cid) and (lat >= 1000 or subs >= 10000)): continue
    if r['url'] and any(r['url'].endswith(s) for s in seed_ids): continue
    raw = D.get(cid) if D.get(cid) and 'error' not in D.get(cid) else F.get(cid)
    m = ts(raw['measured'])
    vids = [v for v in raw.get('videos', []) if v.get('timestamp') and v.get('view_count') is not None]
    y1 = [v['view_count'] for v in vids if 30 <= (m - v['timestamp']) / 86400 <= 365]
    last365 = [v for v in vids if (m - v['timestamp']) / 86400 <= 365]
    durs = [v['duration'] for v in vids[:30] if v.get('duration')]
    top = max(vids, key=lambda v: v['view_count']) if vids else None
    flags = []
    if subs and mx and subs > 20 * mx: flags.append('подписчиков намного больше просмотров: возможно, перепрофилированный старый канал')
    if r['channel'] in ('Imagine the Physics', 'Feynman Reborn', 'The Roger Physics', "Feynman's Mindset", 'Susskind Speaks', 'The Physics According to Feynman'):
        flags.append('использует имя или образ реального учёного')
    win = new and relevant(cid) and (lat >= 1000 or subs >= 10000)
    if named and new and not win:
        flags.append('пример из отчёта вне сравнения: ' + ('по разметке не про физику' if not relevant(cid) else 'ниже порога заметности'))
    rows.append({'segment': 'новый, ниже порога (сравнение)' if weak else 'новый растущий' if win else 'новый, пример вне сравнения' if new else 'растущий средний', 'channel': r['channel'], 'url': r['url'], 'source': 'выдача поиска: ' + r['example_query'],
                 'kind': '', 'subs': subs or None, 'subs_tier': tier(subs or None), 'measured': r['measured'], 'first_upload_known': (NC[cid]['oldest_public_upload'] if cid in NC else '') or r['first_upload_known'],
                 'new_le_12_months': 'да' if new else ('не подтверждено' if cid in NC and NC[cid]['age_status'] == 'unconfirmed' else 'нет'),
                 'uploads_per_month_12m': round(len(last365) / 12, 1) if len(vids) < 500 else '', 'median_duration_min_last30': round(med(durs) / 60, 1) if durs else '',
                 'typical_views_30_365d': med(y1), 'typical_views_1_3y': '', 'recent_vs_older': r['rising_ratio'], 'shorts_median_views': '',
                 'top_video': top['title'] if top else '', 'top_url': f"https://www.youtube.com/watch?v={top['id']}" if top else '', 'top_views': top['view_count'] if top else '',
                 'top_age_days': round((m - top['timestamp']) / 86400) if top else '',
                 'strong_recent': '', 'strong_recent_url': '', 'strong_recent_views': '', 'strong_recent_x_neighbours': '',
                 'weak_recent': '', 'weak_recent_url': '', 'weak_recent_views': '', 'weak_recent_x_neighbours': '',
                 'style_notes': NEWNOTES.get(r['channel'], ''), 'format_notes': '', 'style_source': ('обложки, названия и 8 кадров ролика ' + FRAMES[r['channel'].strip()]) if r['channel'].strip() in FRAMES else ('обложки и названия' if NEWNOTES.get(r['channel']) else ''), 'flags': '; '.join(flags)})
cols = list(rows[0].keys())
order = ['крупный ориентир', 'средний', 'прямой конкурент', 'визуальный ориентир', 'новый растущий', 'новый, ниже порога (сравнение)', 'новый, пример вне сравнения', 'растущий средний', 'другой рынок']
rows.sort(key=lambda r: (order.index(r['segment']), -(r['subs'] or 0)))
with open(os.path.join(DOCS, 'channels.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n'); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r['segment'] for r in rows))
# video registry: seed videos
vr = list(csv.DictReader(open(os.path.join(OUT, 'seed-videos.csv'))))
vcols = ['channel', 'group', 'kind', 'subs', 'video_id', 'url', 'title', 'duration_s', 'format', 'approx_upload', 'age_days', 'views', 'views_per_day',
         'channel_typical_neighbours', 'ratio_to_typical', 'clusters', 'measured']
with open(os.path.join(DOCS, 'videos.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=vcols, lineterminator='\n', extrasaction='ignore'); w.writeheader(); w.writerows(vr)
print('videos', len(vr))
```

## exact.py

Точные просмотры свежих роликов: снимок a и снимок b через 24 часа.

```python
"""Exact view counts of recent videos (7-60 days) of seed channels, for a two-point growth measure.
Run: tmp/venv/bin/python -I tmp/research/exact.py <tag>"""
import json, os, sys, datetime, concurrent.futures as cf
import yt_dlp
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
tag = sys.argv[1]
B = json.load(open(os.path.join(RAW, 'seeds2.json')))
ids = []
for k, b in B.items():
    if 'error' in b: continue
    m = datetime.datetime.fromisoformat(b['measured']).timestamp()
    rec = [v for v in b['videos'] if v.get('timestamp') and 7 <= (m - v['timestamp']) / 86400 <= 60 and (v.get('duration') or 0) > 180][:5]
    ids += [(k, v['id']) for v in rec]
y = yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'skip_download': True, 'socket_timeout': 30})
def get(j):
    k, vid = j
    for a in range(2):
        try:
            i = y.extract_info(f'https://www.youtube.com/watch?v={vid}', download=False, process=False)
            return {'key': k, 'id': vid, 'title': i.get('title'), 'views': i.get('view_count'), 'likes': i.get('like_count'), 'comments': i.get('comment_count'),
                    'upload_date': i.get('upload_date'), 'duration': i.get('duration'), 'channel_subs': i.get('channel_follower_count'),
                    'measured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
        except Exception as ex: err = str(ex)[:200]
    return {'key': k, 'id': vid, 'error': err}
with cf.ThreadPoolExecutor(4) as ex: R = list(ex.map(get, ids))
json.dump(R, open(os.path.join(RAW, f'exact-{tag}.json'), 'w'), ensure_ascii=False)
print(tag, len(R), sum(1 for r in R if 'error' in r), 'errors')
```

## growth_exact.py

Прирост просмотров между снимками за фактический интервал.

```python
"""Views gained by recent videos between two exact snapshots (A and B), over the actual interval, no extrapolation. Writes data/growth.csv.
Run: tmp/venv/bin/python -I tmp/research/growth_exact.py"""
import json, os, csv, statistics as st, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
A = {r['id']: r for r in json.load(open(os.path.join(RAW, 'exact-a.json'))) if 'error' not in r}
B = {r['id']: r for r in json.load(open(os.path.join(RAW, 'exact-b.json'))) if 'error' not in r}
S = json.load(open(os.path.join(RAW, 'seeds2.json')))
def ts(iso): return datetime.datetime.fromisoformat(iso).timestamp()
rows, per = [], {}
for vid, a in A.items():
    b = B.get(vid)
    if not b or a['views'] is None or b['views'] is None: continue
    hrs = (ts(b['measured']) - ts(a['measured'])) / 3600
    up = datetime.datetime.strptime(a['upload_date'], '%Y%m%d').replace(tzinfo=datetime.timezone.utc)
    age = (ts(a['measured']) - up.timestamp()) / 86400
    gain = b['views'] - a['views']
    ch = S.get(a['key'], {}).get('channel', a['key'])
    rows.append({'channel': ch, 'video_id': vid, 'url': f'https://www.youtube.com/watch?v={vid}', 'title': a['title'], 'upload_date': up.strftime('%Y-%m-%d'),
                 'age_days_at_a': round(age, 1), 'views_a': a['views'], 'views_b': b['views'], 'hours_between': round(hrs, 2),
                 'views_gained': gain, 'avg_views_per_day_since_upload': round(a['views'] / max(age, 1)),
                 'likes_b': b.get('likes'), 'comments_b': b.get('comments'), 'measured_a': a['measured'], 'measured_b': b['measured']})
    per.setdefault(ch, []).append(gain)
rows.sort(key=lambda r: (r['channel'], r['upload_date']))
with open(os.path.join(DOCS, 'growth.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print('videos', len(rows), 'channels', len(per))
for ch, v in sorted(per.items(), key=lambda x: -st.median(x[1]))[:40]:
    print(f"{ch[:30]:30} n={len(v)} median views gained={round(st.median(v)):>8}")
```

## export_raw.py

Выгрузка исходных данных в data/.

```python
"""Export raw JSON answers to CSV for checking: weekly Trends series and video lists of channels found in search.
Run: tmp/venv/bin/python -I tmp/research/export_raw.py"""
import csv, json, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
DOCS = os.path.join(HERE, '..', '..', 'docs', 'physics-research', 'data')
with open(os.path.join(DOCS, 'trends-weekly.csv'), 'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['pass', 'batch', 'anchor', 'term', 'week', 'value', 'measured'])
    for n, p in (('trends.json', 1), ('trends2.json', 2)):
        for batch, b in json.load(open(os.path.join(RAW, n))).items():
            if 'series' not in b: continue
            for term, vals in b['series'].items():
                for d, v in zip(b['dates'], vals): w.writerow([p, batch, b['kws'][0], term, d, v, b['measured']])
def day(t): return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%d') if t else ''
n = 0
with open(os.path.join(DOCS, 'found-videos.csv'), 'w', newline='') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['list', 'channel_id', 'video_id', 'title', 'views', 'duration_s', 'approx_upload'])  # channel name, subscribers and time of measurement: found-channels.csv
    for name, label in (('found.json', 'latest 30'), ('deep.json', 'full up to 500')):
        for cid, r in json.load(open(os.path.join(RAW, name))).items():
            if 'error' in r: continue
            for v in r.get('videos') or []:
                w.writerow([label, r.get('channel_id') or cid, v.get('id'), v.get('title'), v.get('view_count'), v.get('duration'), day(v.get('timestamp'))]); n += 1
print('found videos rows', n)
import shutil; shutil.copy(os.path.join(HERE, 'out', 'found-channels.csv'), os.path.join(DOCS, 'found-channels.csv'))
```
