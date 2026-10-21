# Приложение: код замера и расчётов

Код, которым собраны данные и посчитаны таблицы. Приведён для проверки и повторения; как программа в проект не входит. Запуск: Python 3.14, пакеты `yt-dlp==2026.08.19`, `pytrends`. Скрипты лежали в `tmp/scripts/`, сырые ответы — в `tmp/research/raw/`, таблицы — в `tmp/research/out/`; оттуда скопированы в [data](data/).

Порядок: сегменты (1), сбор (2), Trends (3), таблицы (4), темы названий (5), время сборки (6).

## 1. Сегменты и запросы

Файл `segments.json`. `lang` — язык интерфейса поиска (`hl`), `gl` — страна выдачи, `qlang` — язык запроса.

```json
[
 {
  "id": "en_music",
  "name": "Музыка для собак (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "music for dogs",
   "relaxing music for dogs"
  ],
  "qlang": "en"
 },
 {
  "id": "en_alone",
  "name": "Собака одна дома, тревога разлуки (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "music for dogs home alone",
   "dog separation anxiety music"
  ],
  "qlang": "en"
 },
 {
  "id": "en_sleep",
  "name": "Сон и долгие ролики (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "dog sleep music",
   "calming music for dogs 10 hours"
  ],
  "qlang": "en"
 },
 {
  "id": "en_noise",
  "name": "Фейерверки и гроза (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "fireworks music for dogs",
   "thunderstorm calming music for dogs"
  ],
  "qlang": "en"
 },
 {
  "id": "en_tv",
  "name": "Видео для собак, Dog TV (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "dog tv",
   "videos for dogs to watch"
  ],
  "qlang": "en"
 },
 {
  "id": "en_cats",
  "name": "Музыка для кошек, для сравнения (en)",
  "lang": "en",
  "gl": "US",
  "q": [
   "music for cats",
   "relaxing music for cats"
  ],
  "qlang": "en"
 },
 {
  "id": "de_music",
  "name": "Музыка для собак (de)",
  "lang": "en",
  "gl": "DE",
  "q": [
   "musik für hunde",
   "entspannungsmusik für hunde"
  ],
  "qlang": "de"
 },
 {
  "id": "es_music",
  "name": "Музыка для собак (es)",
  "lang": "en",
  "gl": "MX",
  "q": [
   "música para perros",
   "musica relajante para perros"
  ],
  "qlang": "es"
 },
 {
  "id": "pt_music",
  "name": "Музыка для собак (pt)",
  "lang": "en",
  "gl": "BR",
  "q": [
   "música para cachorro",
   "musica para cachorro dormir"
  ],
  "qlang": "pt"
 },
 {
  "id": "fr_music",
  "name": "Музыка для собак (fr)",
  "lang": "en",
  "gl": "FR",
  "q": [
   "musique pour chien",
   "musique relaxante pour chien"
  ],
  "qlang": "fr"
 },
 {
  "id": "ru_music",
  "name": "Музыка для собак (ru)",
  "lang": "en",
  "gl": "RU",
  "q": [
   "музыка для собак",
   "успокаивающая музыка для собак"
  ],
  "qlang": "ru"
 },
 {
  "id": "ja_music",
  "name": "Музыка для собак (ja)",
  "lang": "en",
  "gl": "JP",
  "q": [
   "犬 リラックス 音楽",
   "犬 留守番 音楽"
  ],
  "qlang": "ja"
 }
]

```

## 2. Сбор поиска и каналов

Файлы `collect.py` и `run_collect.sh` — без изменений из [задачи 64](../channel-reassessment/method-code.md#2-сбор-поиска-и-каналов). Запуск партиями по 200 каналов. 10 каналов без вкладки видео повторно не дались; цикл остановлен вручную после трёх пустых повторов.

## 3. Google Trends

Файл `trends.py`.

```python
"""Google Trends, YouTube Search, weekly, 5 years: US batches (with and without anchor 'documentary'),
a worldwide batch across languages, and interest by country for the main term of each language.
Writes tmp/research/raw/trends.json. Run: tmp/venv/bin/python -I tmp/scripts/trends.py"""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'..','research','raw','trends.json')
B=[('US',['documentary','music for dogs','dog music','dog tv','music for cats']),
   ('US',['music for dogs','calming music for dogs','relaxing music for dogs','dog anxiety music','dog sleep music']),
   ('US',['music for dogs','fireworks dogs','thunderstorm dogs','dogs home alone','dog tv']),
   ('',  ['music for dogs','musik für hunde','música para perros','música para cachorro','музыка для собак']),
   ('',  ['music for dogs','musique pour chien','犬 音楽','music for cats','dog tv'])]
REGION=['music for dogs','musik für hunde','música para perros','música para cachorro','музыка для собак','musique pour chien','犬 音楽','dog tv']
R=json.load(open(OUT)) if os.path.exists(OUT) else {}
p=TrendReq(hl='en-US',tz=0,timeout=(10,30))
# pytrends keeps the previous geo when geo='' is passed (self.geo = geo or self.geo): use a fresh client per batch
def client(): return TrendReq(hl='en-US',tz=0,timeout=(10,30))
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
for geo,b in B:
  k=(geo or 'WORLD')+'|'+'|'.join(b)
  if k in R: continue
  for a in range(4):
    try:
      p=client(); p.build_payload(b,timeframe='today 5-y',geo=geo,gprop='youtube')
      df=p.interest_over_time()
      R[k]={'measured':now(),'geo':geo or 'WORLD','weeks':[d.strftime('%Y-%m-%d') for d in df.index],'anchor':b[0],'series':{t:[int(x) for x in df[t]] for t in b}}
      print('ok',k,flush=True); break
    except Exception as ex:
      print('err',k,ex,flush=True); time.sleep(30*(a+1))
  json.dump(R,open(OUT,'w'),ensure_ascii=False); time.sleep(10)
for t in REGION:
  k='REGION|'+t
  if k in R: continue
  for a in range(4):
    try:
      p=client(); p.build_payload([t],timeframe='today 5-y',geo='',gprop='youtube')
      df=p.interest_by_region(resolution='COUNTRY',inc_low_vol=False)
      s=df[t]; s=s[s>0].sort_values(ascending=False)
      R[k]={'measured':now(),'term':t,'timeframe':'today 5-y','by_country':{c:int(v) for c,v in s.items()}}
      print('ok',k,len(s),flush=True); break
    except Exception as ex:
      print('err',k,ex,flush=True); time.sleep(30*(a+1))
  json.dump(R,open(OUT,'w'),ensure_ascii=False); time.sleep(10)

```

## 4. Таблицы и метрики

Файл `analyze.py`. Первая часть (до таблиц Trends) — код задачи 64 без изменений.

```python
"""Build tables from tmp/research/raw/{search,channels,trends}.json into tmp/research/out/.
Run: tmp/venv/bin/python -I tmp/scripts/analyze.py
Channel age comes from the channel's About page ("Joined <date>"), so it is known for every
channel that returned that page, not only for channels with fewer than 30 videos."""
import json, os, re, csv, statistics as st, datetime as dt
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, '..', 'research', 'raw'); OUT = os.path.join(HERE, '..', 'research', 'out')
os.makedirs(OUT, exist_ok=True)
SEG = {s['id']: s for s in json.load(open(os.path.join(HERE, 'segments.json')))}
S = json.load(open(os.path.join(RAW, 'search.json'))); C = json.load(open(os.path.join(RAW, 'channels.json')))


def med(a):
    a = [x for x in a if x is not None and x != '']
    return round(st.median(a)) if a else ''


def num(s):
    if not s: return None
    m = re.match(r'([\d.,]+)\s*([KMB]?)', s)
    if not m: return None
    return int(float(m.group(1).replace(',', '')) * {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9}[m.group(2)])


def joined(s):
    try: return dt.datetime.strptime(s, '%b %d, %Y').date()
    except Exception: return None


CH = {}
for cid, c in C.items():
    a = c.get('about') or {}
    m = dt.datetime.fromisoformat(c['measured'])
    vids = [v for v in c.get('videos') or [] if v.get('id')]
    old = [v.get('view_count') for v in vids if v.get('timestamp') and (m.timestamp() - v['timestamp']) / 86400 >= 30]
    ages = [(m.timestamp() - v['timestamp']) / 86400 for v in vids if v.get('timestamp')]
    j = joined(a.get('joined'))
    subs = c.get('subs') if c.get('subs') is not None else num(a.get('subs_text'))
    n90 = sum(1 for x in ages if x <= 90); span = max(ages) if ages else 0
    per_month = round(n90 / 3, 1) if span > 90 else (round(len(ages) / max(span, 7) * 30.44, 1) if ages else '')
    CH[cid] = {'channel_id': cid, 'channel_url': f'https://www.youtube.com/channel/{cid}', 'channel': c.get('channel') or '',
               'handle': a.get('handle') or '', 'country': a.get('country') or '', 'subs': subs if subs is not None else '',
               'total_views': num(a.get('total_views')) or '', 'video_count_all': num(a.get('video_count')) or '',
               'joined': j.isoformat() if j else '', 'age_months': round((m.date() - j).days / 30.44, 1) if j else '',
               'listed_long_videos': len(vids), 'median_views_age_ge30d': med(old), 'n_age_ge30d': len(old),
               'long_uploads_per_month': per_month, 'measured_utc': c['measured'],
               'error': (c.get('error') or '') + ('; about: ' + a['error'] if a.get('error') else '')}


def group(ch):
    """new: joined < 12 months before measurement (About page). small_old: < 10k subs, joined >= 12 months.
    mid: 10k-100k, big: >= 100k (any age). unknown: no About date or no subscriber count."""
    if not ch or ch['age_months'] == '': return 'unknown'
    if ch['age_months'] < 12: return 'new'
    if ch['subs'] == '': return 'unknown'
    return 'small_old' if ch['subs'] < 10000 else ('mid' if ch['subs'] < 100000 else 'big')


V = []
for key, v in S.items():
    if not isinstance(v['results'], list): continue
    m = dt.datetime.fromisoformat(v['measured'])
    for rank, e in enumerate(v['results'], 1):
        ch = CH.get(e.get('channel_id'), {})
        age = round((m.timestamp() - e['timestamp']) / 86400) if e.get('timestamp') else ''
        V.append({'segment': v['segment'], 'query': v['query'], 'pass': v['pass'], 'rank': rank, 'measured_utc': v['measured'],
                  'video_id': e['id'], 'url': f"https://www.youtube.com/watch?v={e['id']}", 'title': e.get('title') or '',
                  'channel': e.get('channel') or ch.get('channel', ''), 'channel_id': e.get('channel_id') or '',
                  'views': e.get('view_count') if e.get('view_count') is not None else '', 'duration_s': e.get('duration') or '',
                  'approx_upload_date': dt.datetime.fromtimestamp(e['timestamp'], dt.timezone.utc).date().isoformat() if e.get('timestamp') else '',
                  'approx_age_days': age, 'channel_subs': ch.get('subs', ''), 'channel_joined': ch.get('joined', ''),
                  'channel_age_months': ch.get('age_months', ''), 'channel_group': group(ch),
                  'channel_median_views_age_ge30d': ch.get('median_views_age_ge30d', '')})


def w(name, rows):
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)


w('videos.csv', V)
segs_of = defaultdict(set)
for r in V: segs_of[r['channel_id']].add(r['segment'])
w('channels.csv', [dict(ch, group=group(ch), segments=';'.join(sorted(segs_of.get(cid, [])))) for cid, ch in CH.items()])


def dedup(rows):
    d = {}
    for r in rows: d.setdefault(r['video_id'], r)
    return list(d.values())


M, E = [], []
for sid, s in SEG.items():
    mv = dedup([r for r in V if r['segment'] == sid and r['pass'] == 'month'])
    av = dedup([r for r in V if r['segment'] == sid and r['pass'] == 'all'])
    ml = [r for r in mv if r['duration_s'] != '' and r['duration_s'] > 180 and r['approx_age_days'] != '' and 7 <= r['approx_age_days'] <= 30 and r['views'] != '']
    ms = [r for r in mv if r['duration_s'] != '' and r['duration_s'] <= 180 and r['approx_age_days'] != '' and 7 <= r['approx_age_days'] <= 30 and r['views'] != '']
    g = lambda rows, gr: [r['views'] for r in rows if r['channel_group'] == gr]
    chans = {r['channel_id'] for r in mv + av if r['channel_id']}
    newc = [CH[c] for c in chans if c in CH and group(CH[c]) == 'new']
    newc_typ = [c['median_views_age_ge30d'] for c in newc if c['median_views_age_ge30d'] != '']
    smallc = [CH[c] for c in chans if c in CH and group(CH[c]) == 'small_old']
    smallc_typ = [c['median_views_age_ge30d'] for c in smallc if c['median_views_age_ge30d'] != '']
    al = [r for r in av if r['approx_age_days'] != '' and r['views'] != '']
    row = {'segment': sid, 'name_ru': s['name'], 'queries': ' | '.join(s['q']), 'measured_utc': max(r['measured_utc'] for r in mv + av),
           'long_7_30d_n': len(ml), 'long_7_30d_median': med([r['views'] for r in ml])}
    for gr in ('new', 'small_old', 'mid', 'big', 'unknown'):
        row[f'long_7_30d_{gr}_n'] = len(g(ml, gr)); row[f'long_7_30d_{gr}_median'] = med(g(ml, gr))
    row.update({'long_7_30d_new_or_small_ge1k': sum(1 for r in ml if r['channel_group'] in ('new', 'small_old') and r['views'] >= 1000),
                'long_7_30d_new_or_small_n': sum(1 for r in ml if r['channel_group'] in ('new', 'small_old')),
                'short_7_30d_n': len(ms), 'short_7_30d_median': med([r['views'] for r in ms]),
                'all_n': len(al), 'all_median_age_days': med([r['approx_age_days'] for r in al]), 'all_median_views': med([r['views'] for r in al]),
                'all_share_new_or_small': round(sum(1 for r in al if r['channel_group'] in ('new', 'small_old')) / len(al), 2) if al else '',
                'distinct_channels': len(chans), 'new_channels_n': len(newc), 'new_channels_typical_n': len(newc_typ),
                'new_channels_typical_median': med(newc_typ),
                'new_channels_typical_lt100': sum(1 for x in newc_typ if x < 100), 'new_channels_typical_ge1k': sum(1 for x in newc_typ if x >= 1000),
                'small_old_channels_n': len(smallc), 'small_old_typical_n': len(smallc_typ), 'small_old_typical_median': med(smallc_typ),
                'small_old_typical_lt100': sum(1 for x in smallc_typ if x < 100), 'small_old_typical_ge1k': sum(1 for x in smallc_typ if x >= 1000)})
    M.append(row)
    rows = dedup([r for r in V if r['segment'] == sid and r['views'] != ''])

    def ex(role, r, note):
        ch = CH.get(r['channel_id'], {})
        E.append({'segment': sid, 'role': role, 'url': r['url'], 'title': r['title'], 'views': r['views'], 'duration_s': r['duration_s'],
                  'approx_upload_date': r['approx_upload_date'], 'approx_age_days': r['approx_age_days'], 'channel': r['channel'],
                  'channel_url': ch.get('channel_url', ''), 'channel_subs': r['channel_subs'], 'channel_joined': r['channel_joined'],
                  'channel_group': r['channel_group'], 'channel_median_views_age_ge30d': r['channel_median_views_age_ge30d'],
                  'long_uploads_per_month': ch.get('long_uploads_per_month', ''), 'measured_utc': r['measured_utc'], 'note': note})
    ex('leader', max(rows, key=lambda r: r['views']), 'most viewed video in the segment sample, both passes')
    mls = sorted(ml, key=lambda r: r['views'])
    if mls: ex('ordinary', mls[len(mls) // 2], 'median long video aged 7-30 days')
    for gr, lab in (('new', 'new channel (joined < 12 months)'), ('small_old', 'small old channel (< 10k, joined >= 12 months)')):
        cand = [r for r in rows if r['channel_group'] == gr and r['duration_s'] != '' and r['duration_s'] > 180]
        if cand:
            ex(f'best_{gr}', max(cand, key=lambda r: r['views']), f'best long video of a {lab}')
            weak = [r for r in cand if r['approx_age_days'] != '' and r['approx_age_days'] >= 7]
            if weak: ex(f'weak_{gr}', min(weak, key=lambda r: r['views']), f'weakest long video aged >= 7 days of a {lab}')
w('segment-metrics.csv', M)
w('examples.csv', E)
print('videos', len(V), 'channels', len(CH), 'segments', len(M))
# trends: US and worldwide lines, plus interest by country
T = json.load(open(os.path.join(RAW, 'trends.json'))); TR = []; REG = []
for k, v in T.items():
    if k.startswith('REGION|'):
        tot = sum(v['by_country'].values())
        for rank, (c, x) in enumerate(v['by_country'].items(), 1):
            if rank <= 15: REG.append({'term': v['term'], 'rank': rank, 'country': c, 'interest_0_100': x, 'countries_with_data': len(v['by_country']),
                                       'timeframe': v['timeframe'], 'property': 'youtube', 'measured_utc': v['measured']})
        continue
    wk = v['weeks']; b0 = v['anchor']
    for t, ser in v['series'].items():
        last = ser[-52:]; prev = ser[-104:-52]; three = ser[-156:-104]
        mon = defaultdict(list)
        for d, x in zip(wk, ser): mon[int(d[5:7])].append(x)
        mm = {m: sum(a) / len(a) for m, a in mon.items()}; mean = sum(mm.values()) / 12 if mm else 0
        top = sorted(zip(wk, ser), key=lambda z: -z[1])[:3]
        TR.append({'batch': k, 'term': t, 'measured_utc': v['measured'], 'geo': v['geo'], 'property': 'youtube', 'timeframe': f'{wk[0]}..{wk[-1]}',
                   'anchor': b0, 'mean_last52_vs_anchor': round(sum(last) / max(1, sum(v['series'][b0][-52:])), 3),
                   'mean_last52': round(sum(last) / 52, 1),
                   'ratio_last52_prev52': round(sum(last) / sum(prev), 2) if sum(prev) else '',
                   'ratio_last52_3y_ago': round(sum(last) / sum(three), 2) if sum(three) else '',
                   'peak_month': max(mm, key=mm.get) if mm else '', 'low_month': min(mm, key=mm.get) if mm else '',
                   'seasonality_range': round((max(mm.values()) - min(mm.values())) / mean, 2) if mean else '',
                   'top_weeks': '; '.join(f'{d}:{x}' for d, x in top)})
w('trends.csv', TR); w('trends-countries.csv', REG)
DIR = {'en_core': ['en_music', 'en_alone', 'en_sleep'], 'en_noise': ['en_noise'], 'en_tv': ['en_tv'], 'en_cats': ['en_cats'],
       'de': ['de_music'], 'es': ['es_music'], 'pt': ['pt_music'], 'fr': ['fr_music'], 'ru': ['ru_music'], 'ja': ['ja_music'],
       'all_dog': ['en_music', 'en_alone', 'en_sleep', 'en_noise', 'en_tv', 'de_music', 'es_music', 'pt_music', 'fr_music', 'ru_music', 'ja_music']}
D = []
for did, segs in DIR.items():
    mv = dedup([r for r in V if r['segment'] in segs and r['pass'] == 'month'])
    av = dedup([r for r in V if r['segment'] in segs and r['pass'] == 'all'])
    ml = [r for r in mv if r['duration_s'] != '' and r['duration_s'] > 180 and r['approx_age_days'] != '' and 7 <= r['approx_age_days'] <= 30 and r['views'] != '']
    chans = {r['channel_id'] for r in V if r['segment'] in segs and r['channel_id']}
    row = {'direction': did, 'segments': ';'.join(segs), 'long_7_30d_n': len(ml), 'long_7_30d_median': med([r['views'] for r in ml])}
    for gr in ('new', 'small_old', 'mid', 'big', 'unknown'):
        v_ = [r['views'] for r in ml if r['channel_group'] == gr]
        row[f'{gr}_n'] = len(v_); row[f'{gr}_median'] = med(v_)
        row[f'{gr}_ge1k'] = sum(1 for x in v_ if x >= 1000); row[f'{gr}_lt100'] = sum(1 for x in v_ if x < 100)
    for gr in ('new', 'small_old'):
        typ = [CH[c]['median_views_age_ge30d'] for c in chans if c in CH and group(CH[c]) == gr and CH[c]['median_views_age_ge30d'] != '']
        row[f'{gr}_channels'] = sum(1 for c in chans if c in CH and group(CH[c]) == gr)
        row[f'{gr}_channels_typical_n'] = len(typ); row[f'{gr}_channels_typical_median'] = med(typ)
        row[f'{gr}_channels_typical_ge1k'] = sum(1 for x in typ if x >= 1000); row[f'{gr}_channels_typical_lt100'] = sum(1 for x in typ if x < 100)
    # durations: month pass (all ages) and all-time pass
    dm = [r['duration_s'] for r in mv if r['duration_s'] != '']; da = [r['duration_s'] for r in av if r['duration_s'] != '']
    row.update({'month_videos_n': len(dm), 'month_median_duration_h': round(st.median(dm) / 3600, 2) if dm else '',
                'month_share_ge_8h': round(sum(1 for x in dm if x >= 8 * 3600) / len(dm), 2) if dm else '',
                'month_share_ge_3h': round(sum(1 for x in dm if x >= 3 * 3600) / len(dm), 2) if dm else '',
                'alltime_videos_n': len(da), 'alltime_median_duration_h': round(st.median(da) / 3600, 2) if da else '',
                'alltime_share_ge_8h': round(sum(1 for x in da if x >= 8 * 3600) / len(da), 2) if da else '',
                'alltime_median_views': med([r['views'] for r in av if r['views'] != '']),
                'alltime_median_age_days': med([r['approx_age_days'] for r in av if r['approx_age_days'] != '']),
                'alltime_share_new_or_small': round(sum(1 for r in av if r['channel_group'] in ('new', 'small_old')) / len(av), 2) if av else '',
                'alltime_share_big': round(sum(1 for r in av if r['channel_group'] == 'big') / len(av), 2) if av else '',
                'distinct_channels': len(chans)})
    D.append(row)
w('direction-metrics.csv', D)
# top channels by subscribers in the dog sample, and new channels list
dog_segs = set(DIR['all_dog'])
dog_ch = {r['channel_id'] for r in V if r['segment'] in dog_segs and r['channel_id']}
top = sorted([CH[c] for c in dog_ch if c in CH and CH[c]['subs'] != ''], key=lambda c: -c['subs'])
w('top-channels.csv', [dict(c, group=group(c), segments=';'.join(sorted(segs_of.get(c['channel_id'], [])))) for c in top[:40]])
w('new-channels.csv', [dict(c, group='new', segments=';'.join(sorted(segs_of.get(c['channel_id'], [])))) for c in top if group(c) == 'new'] or [{'none': ''}])
print('dog channels', len(dog_ch))

```

## 5. Темы названий

Файл `themes.py`.

```python
"""Title themes and duration buckets over unique dog videos (cats segment excluded).
Run: python3 -I tmp/scripts/themes.py  (reads tmp/research/out/videos.csv)"""
import csv, re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
V = list(csv.DictReader(open(os.path.join(HERE, '..', 'research', 'out', 'videos.csv'))))
U = {}
for r in V:
    if r['segment'] != 'en_cats': U.setdefault(r['video_id'], r)
U = list(U.values()); print('unique dog videos', len(U))
PATS = {'no_ads': r'no ads|no ad\b|without ads|ad[- ]free|no mid|広告なし|sin anuncios|ohne werbung|sem an[uú]ncios|без рекламы|sans pub',
        'anxiety': r'anxiety|angst|ansiedad|ansiedade|anxi[eé]t[eé]|тревог|不安',
        'separation_home_alone': r'separation|home alone|alone|solos? en casa|sozinho|seuls?|allein|одн|留守番',
        'sleep': r'sleep|schlaf|dormir|sono|sommeil|сон|睡眠|眠',
        'ai_in_title': r'\bAI\b|A\.I\.|artificial intelligence'}
for k, p in PATS.items():
    print(k, sum(1 for r in U if re.search(p, r['title'], re.I)), 'of', len(U))
dur = [int(r['duration_s']) for r in U if r['duration_s']]
b = collections.Counter(('<1h' if x < 3600 else '1-3h' if x < 3 * 3600 else '3-8h' if x < 8 * 3600 else '8-12h' if x <= 12 * 3600 + 120 else '>12h') for x in dur)
print(dict(b), 'with duration', len(dur))

```

## 6. Время сборки

FFmpeg 6.0.1-static, 4 ядра, без видеокарты, команды с `nice`. Звук — 10 минут розового шума вместо музыки.

```bash
ffmpeg -f lavfi -i "anoisesrc=d=600:c=pink:a=0.05:r=48000" -ac 2 audio600.wav
ffmpeg -f lavfi -i "color=c=0x1d2b53:s=1920x1080" -frames:v 1 still.png
# статичная картинка, 1 кадр/с
ffmpeg -loop 1 -framerate 1 -i still.png -i audio600.wav -c:v libx264 -tune stillimage -preset medium -crf 20 -pix_fmt yuv420p -r 1 -c:a aac -b:a 192k -shortest static600.mp4
# петля 60 с, 24 кадра/с
ffmpeg -f lavfi -i "gradients=s=1920x1080:c0=0x1d2b53:c1=0xe8c170:speed=0.002:d=60:r=24" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p loop60.mp4
# повтор петли без перекодирования; длину задаёт -t (с -shortest и -stream_loop -1 файл не заканчивается)
ffmpeg -stream_loop -1 -i loop60.mp4 -i audio600.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 600 looped600.mp4
```
