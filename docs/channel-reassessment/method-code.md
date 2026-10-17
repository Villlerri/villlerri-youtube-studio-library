# Приложение: код замера и расчётов

Код, которым собраны данные и посчитаны таблицы. Приведён для проверки и повторения; как программа в проект не входит. Запуск: Python 3.14, пакеты `yt-dlp==2026.08.19`, `pytrends`. Скрипты лежали в `tmp/scripts/`, сырые ответы — в `tmp/research/raw/`, таблицы — в `tmp/research/out/`; оттуда скопированы в [data](data/).

Порядок: сегменты (1), сбор (2), Trends (5), таблицы (4), темп и деньги (3), реестр (6, 7). Код видеопроб — в [probes/source.md](probes/source.md).

## 1. Сегменты и запросы

Файл `segments.json`. Первые 10 сегментов — первый проход, 6 последних — добор по лидерам.

```json
[
 {
  "id": "scale2d",
  "name": "Масштабы и сравнения (Honest Scale, 2D)",
  "lang": "en",
  "gl": "US",
  "q": [
   "size comparison animation",
   "universe size comparison"
  ]
 },
 {
  "id": "folklore_slavic",
  "name": "Славянский фольклор (Thrice-Nine Tales)",
  "lang": "en",
  "gl": "US",
  "q": [
   "slavic mythology",
   "russian fairy tales"
  ]
 },
 {
  "id": "english_stories",
  "name": "Английский через истории (Story Steps English)",
  "lang": "en",
  "gl": "US",
  "q": [
   "learn english through story",
   "english story for listening practice"
  ]
 },
 {
  "id": "learn_russian",
  "name": "Русский язык для иностранцев",
  "lang": "en",
  "gl": "US",
  "q": [
   "learn russian for beginners",
   "russian comprehensible input"
  ]
 },
 {
  "id": "quiz_general",
  "name": "Викторины общих знаний",
  "lang": "en",
  "gl": "US",
  "q": [
   "general knowledge quiz",
   "trivia quiz"
  ]
 },
 {
  "id": "quiz_geo",
  "name": "Географические викторины",
  "lang": "en",
  "gl": "US",
  "q": [
   "guess the country quiz",
   "flag quiz"
  ]
 },
 {
  "id": "brain_seniors",
  "name": "Игры для памяти и внимания (для старших)",
  "lang": "en",
  "gl": "US",
  "q": [
   "brain games for seniors",
   "spot the difference"
  ]
 },
 {
  "id": "russian_lit",
  "name": "Русская классика для англоязычных",
  "lang": "en",
  "gl": "US",
  "q": [
   "dostoevsky explained",
   "russian literature"
  ]
 },
 {
  "id": "chess",
  "name": "Шахматы: партии и дебюты",
  "lang": "en",
  "gl": "US",
  "q": [
   "chess famous games",
   "chess openings explained"
  ]
 },
 {
  "id": "puzzles",
  "name": "Логические задачи и загадки",
  "lang": "en",
  "gl": "US",
  "q": [
   "logic puzzles",
   "riddles with answers"
  ]
 },
 {
  "id": "quiz_pub",
  "name": "Викторины: паб-квиз",
  "lang": "en",
  "gl": "US",
  "q": [
   "pub quiz",
   "trivia questions and answers"
  ]
 },
 {
  "id": "quiz_topic",
  "name": "Викторины: история и наука",
  "lang": "en",
  "gl": "US",
  "q": [
   "history trivia quiz",
   "science trivia quiz"
  ]
 },
 {
  "id": "quiz_seniors",
  "name": "Викторины для старших",
  "lang": "en",
  "gl": "US",
  "q": [
   "trivia for seniors",
   "quiz for seniors"
  ]
 },
 {
  "id": "english_graded",
  "name": "Английский: адаптированные истории",
  "lang": "en",
  "gl": "US",
  "q": [
   "graded reader english",
   "slow english story"
  ]
 },
 {
  "id": "english_level",
  "name": "Английский: истории по уровням",
  "lang": "en",
  "gl": "US",
  "q": [
   "english story level 1",
   "learn english through story a2"
  ]
 },
 {
  "id": "scale_planets",
  "name": "Масштабы: планеты и 2D",
  "lang": "en",
  "gl": "US",
  "q": [
   "planet size comparison",
   "size comparison 2d animation"
  ]
 }
]
```

## 2. Сбор поиска и каналов

Файл `collect.py` — код сбора задачи 59 без изменений логики. Запуск партиями по 200 каналов (`run_collect.sh`): так процесс не растёт в памяти.

```python
"""Collect public YouTube search samples (two passes) and channel listings + about pages.
Run: tmp/venv/bin/python -I tmp/scripts/collect.py [batch]  (writes tmp/research/raw/)"""
import json, time, urllib.parse, urllib.request, concurrent.futures as cf, os, datetime, re, sys
import yt_dlp
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'..','research','raw')
PASSES={'month':'EgQIBBAB','all':'EgIQAQ%3D%3D'}  # month: upload date this month + type video; all: type video only
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
def ydl(n): return yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'extract_flat':'in_playlist','playlistend':n,'skip_download':True,
  'extractor_args':{'youtubetab':{'approximate_date':['']}},'socket_timeout':30})
def search(q,lang,gl,sp,n=40):
  url=f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={sp}&hl={lang}&gl={gl}"
  err=''
  for a in range(3):
    try:
      with ydl(n) as y: info=y.extract_info(url,download=False)
      return [{k:e.get(k) for k in ('id','title','channel','channel_id','view_count','duration','timestamp')} for e in info.get('entries') or [] if e.get('id') and len(e['id'])==11]
    except Exception as ex: err=str(ex); time.sleep(5)
  return {'error':err}
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def about(cid):
  req=urllib.request.Request(f'https://www.youtube.com/channel/{cid}/about?hl=en',headers={'User-Agent':UA,'Accept-Language':'en-US,en','Cookie':'CONSENT=YES+1; SOCS=CAI'})
  for a in range(3):
    try:
      h=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','replace')
      m=re.search(r'"aboutChannelViewModel":\{(.{0,6000})',h)
      if not m: return {'error':'no aboutChannelViewModel'}
      s=m.group(1); g=lambda p:(re.search(p,s) or [None,None])[1]
      return {'joined':g(r'"joinedDateText":\{"content":"Joined ([^"]+)"'),'total_views':g(r'"viewCountText":"([^"]+)"'),
              'video_count':g(r'"videoCountText":"([^"]+)"'),'subs_text':g(r'"subscriberCountText":"([^"]+)"'),'country':g(r'"country":"([^"]+)"'),
              'handle':g(r'"canonicalChannelUrl":"http://www.youtube.com/([^"]+)"')}
    except Exception as ex: err=str(ex); time.sleep(5)
  return {'error':err}
def channel(cid,n=30):
  err=''
  for a in range(3):
    try:
      with ydl(n) as y: info=y.extract_info(f"https://www.youtube.com/channel/{cid}/videos",download=False)
      ents=[{k:e.get(k) for k in ('id','title','view_count','duration','timestamp')} for e in info.get('entries') or []]
      r={'channel':info.get('channel'),'subs':info.get('channel_follower_count'),'videos':ents}; break
    except Exception as ex: err=str(ex); time.sleep(5)
  else: r={'error':err}
  r['about']=about(cid); r['measured']=now(); return r
def main():
  segs=json.load(open(os.path.join(HERE,'segments.json')))
  sp_=os.path.join(RAW,'search.json'); S=json.load(open(sp_)) if os.path.exists(sp_) else {}
  jobs=[(s['id'],q,s['lang'],s['gl'],p) for s in segs for q in s['q'] for p in PASSES if f"{s['id']}|{q}|{p}" not in S or 'error' in S[f"{s['id']}|{q}|{p}"]['results']]
  with cf.ThreadPoolExecutor(4) as ex:
    futs={ex.submit(search,q,l,g,PASSES[p]):(sid,q,l,g,p) for sid,q,l,g,p in jobs}
    for f in cf.as_completed(futs):
      sid,q,l,g,p=futs[f]; r=f.result()
      S[f"{sid}|{q}|{p}"]={'segment':sid,'query':q,'lang':l,'gl':g,'pass':p,'measured':now(),'results':r}
      print('search',sid,q,p,len(r) if isinstance(r,list) else r,flush=True)
  json.dump(S,open(sp_,'w'),ensure_ascii=False)
  keys=set(e['channel_id'] for v in S.values() if isinstance(v['results'],list) for e in v['results'] if e.get('channel_id'))
  cp=os.path.join(RAW,'channels.json'); C=json.load(open(cp)) if os.path.exists(cp) else {}
  todo=[k for k in keys if k not in C or 'error' in C[k] or 'error' in C[k].get('about',{})]
  todo=todo[:int(sys.argv[1])] if len(sys.argv)>1 else todo
  print('channels to fetch',len(todo),flush=True)
  with cf.ThreadPoolExecutor(3) as ex:
    for i,(k,r) in enumerate(zip(todo, ex.map(channel,todo))):
      C[k]=r
      if i%50==0: json.dump(C,open(cp,'w'),ensure_ascii=False); print('channels',i,flush=True)
  json.dump(C,open(cp,'w'),ensure_ascii=False); print('done',len(C),flush=True)
main()
```

## 2а. Запуск партиями

```bash
#!/bin/bash
# Search once, then channels in batches of 200 until none left (memory guard).
cd "$(dirname "$0")/../.."
for i in $(seq 1 12); do
  out=$(tmp/venv/bin/python -I tmp/scripts/collect.py 200 2>&1 | tee -a tmp/research/collect.log | grep 'channels to fetch')
  echo "$out"
  n=$(echo "$out" | awk '{print $4}')
  [ "$n" = "0" ] && break
done
echo ALLDONE >> tmp/research/collect.log
```

## 3. Темп и деньги

Файл `economics.py`.

```python
"""Pace, watch-hour need and money per shortlisted direction under explicit assumptions.
Writes docs/channel-reassessment/data/economics.csv. Observed views come from direction-metrics.csv."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
DM = {r['direction']: r for r in csv.DictReader(open(os.path.join(HERE, '..', 'research', 'out', 'direction-metrics.csv')))}
# id, direction, length_min, avd low/base/high (assumption), human h per video low/base/high (assumption), videos/month at base,
# voice minutes per video, other cash per month, rpm range (assumption)
A = [
 ('quiz', 'quiz_pub_general', 22, (5, 8, 12), (3, 4, 6), 6, 0, 0, '1-4'),
 ('quiz_voiced', 'quiz_pub_general', 22, (5, 8, 12), (3, 4, 6), 6, 9, 0, '1-4'),
 ('english', 'english_stories_all', 30, (6, 10, 15), (3, 4, 6), 6, 30, 0, '0.3-1.5'),
 ('scale2d', 'scale_all', 8, (2.5, 3.5, 5), (4, 6, 8), 4, 8, 0, '1.5-6'),
 ('geo', 'quiz_geo', 10, (3, 4, 6), (2, 2.5, 4), 8, 0, 0, '1-4'),
]
# ElevenLabs public prices (task 45, checked 2026-10-14): Starter $6/30k, Creator $22/121k, Pro $99/600k credits; over plan ~$0.18 per 1k chars.
# 1 credit per character, ~1000 characters per minute of speech, +30% for retakes.
def voice_usd(chars):
    if chars == 0: return 0
    opts = [6 + max(0, chars - 30000) / 1000 * 0.18 if chars <= 30000 else 1e9, 22 + max(0, chars - 121000) / 1000 * 0.18, 99 + max(0, chars - 600000) / 1000 * 0.18]
    return round(min(opts))
rows = []
for cid, d, L, avd, hh, vpm, vmin, other, rpm in A:
    m = DM[d]
    need = round(8000 * 60 / (12 * vpm * avd[1]))
    obs_new, obs_small = m['new_median'], m['small_old_median']
    chars = round(vmin * 1000 * 1.3 * vpm)
    rows.append({'id': cid, 'direction': d, 'length_min': L, 'avd_min_low_base_high': '/'.join(map(str, avd)), 'human_h_per_video_low_base_high': '/'.join(map(str, hh)),
                 'videos_per_month_base': vpm, 'human_h_per_month_base': hh[1] * vpm,
                 'views_needed_per_video_8000h_12m_base': need,
                 'views_needed_low_avd': round(8000 * 60 / (12 * vpm * avd[0])), 'views_needed_high_avd': round(8000 * 60 / (12 * vpm * avd[2])),
                 'observed_new_median': obs_new, 'observed_new_n': m['new_n'], 'observed_small_old_median': obs_small, 'observed_small_old_n': m['small_old_n'],
                 'ratio_new_to_needed': round(int(obs_new) / need, 2) if obs_new else '', 'ratio_small_old_to_needed': round(int(obs_small) / need, 2) if obs_small else '',
                 'voice_chars_per_month': chars, 'voice_usd_month': voice_usd(chars), 'other_usd_month': other, 'cash_usd_month': voice_usd(chars) + other, 'rpm_usd_assumption': rpm})
out = os.path.join(ROOT, 'docs', 'channel-reassessment', 'data', 'economics.csv')
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
```

## 4. Таблицы и метрики

Файл `analyze.py`.

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
# trends
T = json.load(open(os.path.join(RAW, 'trends.json'))); TR = []
for k, v in T.items():
    wk = v['weeks']; b0 = k.split('|')[0]
    for t, ser in v['series'].items():
        last = ser[-52:]; prev = ser[-104:-52]; three = ser[-156:-104]
        mon = defaultdict(list)
        for d, x in zip(wk, ser): mon[int(d[5:7])].append(x)
        mm = {m: sum(a) / len(a) for m, a in mon.items()}; mean = sum(mm.values()) / 12 if mm else 0
        TR.append({'batch': k, 'term': t, 'measured_utc': v['measured'], 'geo': 'US', 'property': 'youtube', 'timeframe': f'{wk[0]}..{wk[-1]}',
                   'anchor': b0, 'mean_last52_vs_anchor': round(sum(last) / max(1, sum(v['series'][b0][-52:])), 3),
                   'ratio_last52_prev52': round(sum(last) / sum(prev), 2) if sum(prev) else '',
                   'ratio_last52_3y_ago': round(sum(last) / sum(three), 2) if sum(three) else '',
                   'peak_month': max(mm, key=mm.get) if mm else '', 'low_month': min(mm, key=mm.get) if mm else '',
                   'seasonality_range': round((max(mm.values()) - min(mm.values())) / mean, 2) if mean else ''})
w('trends.csv', TR)
print('videos', len(V), 'channels', len(CH), 'segments', len(M))
# directions: union of segments, one video counted once
DIR = {'quiz_pub_general': ['quiz_general', 'quiz_pub'], 'english_stories_all': ['english_stories', 'english_graded', 'english_level'],
       'scale_all': ['scale2d', 'scale_planets'], 'quiz_geo': ['quiz_geo'], 'quiz_topic_seniors': ['quiz_topic', 'quiz_seniors'],
       'brain_seniors': ['brain_seniors'], 'folklore_slavic': ['folklore_slavic'], 'learn_russian': ['learn_russian'],
       'russian_lit': ['russian_lit'], 'chess': ['chess'], 'puzzles': ['puzzles']}
D = []
for did, segs in DIR.items():
    mv = dedup([r for r in V if r['segment'] in segs and r['pass'] == 'month'])
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
    D.append(row)
w('direction-metrics.csv', D)
```

## 5. Google Trends

Файл `trends.py`.

```python
"""Google Trends, YouTube Search, US, weekly, 5 years. Anchor 'documentary' in every batch.
Writes tmp/research/raw/trends.json. Run: tmp/venv/bin/python -I tmp/scripts/trends.py"""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'..','research','raw','trends.json')
B=[['documentary','trivia quiz','general knowledge quiz','flag quiz','guess the country'],
   ['documentary','learn russian','learn english through story','russian fairy tales','slavic mythology'],
   ['documentary','size comparison','brain games','spot the difference','riddles'],
   ['documentary','chess openings','dostoevsky','logic puzzles','pub quiz'],
   # second pass without the large anchor: growth ratios per term are comparable, levels only inside the batch
   ['trivia quiz','general knowledge quiz','pub quiz','flag quiz','guess the country'],
   ['learn english through story','english story','graded reader','learn russian','size comparison']]
R=json.load(open(OUT)) if os.path.exists(OUT) else {}
p=TrendReq(hl='en-US',tz=0,timeout=(10,30))
for b in B:
  k='|'.join(b)
  if k in R: continue
  for a in range(4):
    try:
      p.build_payload(b,timeframe='today 5-y',geo='US',gprop='youtube')
      df=p.interest_over_time()
      R[k]={'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'weeks':[d.strftime('%Y-%m-%d') for d in df.index],'anchor':b[0],'series':{t:[int(x) for x in df[t]] for t in b}}
      print('ok',k,flush=True); break
    except Exception as ex:
      print('err',k,ex,flush=True); time.sleep(30*(a+1))
  json.dump(R,open(OUT,'w')); time.sleep(8)
```

## 6. Реестр доказательств

Файл `evidence.py`.

```python
"""Evidence registry: one row per claim used in report.md, with value, n, denominator, date and source.
Writes docs/channel-reassessment/data/evidence.csv and prints Markdown lines for evidence.md."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); OUT = os.path.join(HERE, '..', 'research', 'out')
DM = {r['direction']: r for r in csv.DictReader(open(os.path.join(OUT, 'direction-metrics.csv')))}
SM = {r['segment']: r for r in csv.DictReader(open(os.path.join(OUT, 'segment-metrics.csv')))}
EX = list(csv.DictReader(open(os.path.join(OUT, 'examples.csv'))))
TR = [r for r in csv.DictReader(open(os.path.join(OUT, 'trends.csv')))]
DATE = '2026-10-17'
NAME = {'quiz_pub_general': 'Викторина общих знаний', 'english_stories_all': 'Английский через истории', 'scale_all': 'Масштабы (Honest Scale)',
        'quiz_geo': 'Географическая викторина', 'quiz_topic_seniors': 'Тематические викторины и для старших', 'brain_seniors': 'Игры на память',
        'folklore_slavic': 'Славянский фольклор (Thrice-Nine Tales)', 'learn_russian': 'Русский для иностранцев', 'russian_lit': 'Русская классика',
        'chess': 'Шахматы', 'puzzles': 'Логические задачи'}
rows = []
def add(direction, claim, value, n, denom, source, urls='', note=''):
    rows.append({'id': f'E{len(rows) + 1:03d}', 'direction': direction, 'claim': claim, 'value': value, 'n': n, 'denominator': denom,
                 'measured': DATE, 'source': source, 'urls': urls, 'note': note})
for d, m in DM.items():
    src = 'data/direction-metrics.csv; data/videos.csv'
    add(d, 'Медиана просмотров длинных видео 7–30 дней, все каналы', m['long_7_30d_median'], m['long_7_30d_n'], 'видео', src)
    for g, lab in (('new', 'новые каналы (созданы < 12 мес.)'), ('small_old', 'малые старые каналы (< 10 тыс., созданы ≥ 12 мес.)')):
        if m[f'{g}_n'] != '0':
            add(d, f'Медиана просмотров длинных видео 7–30 дней, {lab}', m[f'{g}_median'], m[f'{g}_n'], 'видео', src,
                note=f"от 1 000: {m[f'{g}_ge1k']} из {m[f'{g}_n']}; меньше 100: {m[f'{g}_lt100']} из {m[f'{g}_n']}" + ('; n < 15, ненадёжно' if int(m[f'{g}_n']) < 15 else ''))
        if m[f'{g}_channels_typical_n'] != '0':
            add(d, f'Типичное видео канала (медиана его длинных видео старше 30 дней), {lab}', m[f'{g}_channels_typical_median'], m[f'{g}_channels_typical_n'], 'каналов',
                'data/direction-metrics.csv; data/channels.csv', note=f"от 1 000: {m[f'{g}_channels_typical_ge1k']}; меньше 100: {m[f'{g}_channels_typical_lt100']}; всего таких каналов в выборке {m[f'{g}_channels']}")
for e in EX:
    seg = e['segment']
    d = next((k for k, v in DM.items() if seg in v['segments'].split(';')), seg)
    role = {'leader': 'лидер выборки (оба прохода)', 'ordinary': 'обычное видео (медиана длинных 7–30 дней)', 'best_new': 'лучшее длинное видео нового канала',
            'weak_new': 'самое слабое длинное видео нового канала, возраст от 7 дней', 'best_small_old': 'лучшее длинное видео малого старого канала',
            'weak_small_old': 'самое слабое длинное видео малого старого канала, возраст от 7 дней'}[e['role']]
    add(d, f"Пример: {role}", e['views'], 1, 'видео', 'data/examples.csv', e['url'],
        f"«{e['title'][:90].strip()}» · канал {e['channel']} · подписчиков {e['channel_subs'] or 'н/д'} · создан {e['channel_joined'] or 'н/д'} · возраст видео {e['approx_age_days']} дн")
for t in TR:
    if t['anchor'] != 'documentary' and t['ratio_last52_prev52']:
        add('trends', f"Интерес на поиске YouTube, США: «{t['term']}», последние 52 недели к предыдущим", t['ratio_last52_prev52'], 52, 'недель', 'data/trends.csv',
            note=f"к трём годам назад: {t['ratio_last52_3y_ago'] or 'н/д'}; пик {t['peak_month']}, спад {t['low_month']}; Google Trends, {t['timeframe']}")
# claims checked by hand or by command, outside the tables above
add('production', 'Средства производства на сервере: есть Remotion 4.0.507, Chromium без окна, FFmpeg 6.0.1, Python с numpy и Pillow; нет Blender, Manim, Godot, видеокарты',
    'есть/нет', '', '', 'команды `command -v`, `nvidia-smi`, `ffmpeg -version` 2026-10-17 (method.md)')
add('english_stories_all', 'Одинаковые названия видео у 3–4 разных каналов английского через истории', '«Nothing Is Free» — 4 канала; «Be Different: Rules To Build Your Own Life» — 3; «The Power of Practice» — 3; «Don’t Underestimate Yourself» — 3',
    '', 'каналов', 'data/videos.csv (поиск по названию без регистра и знаков)')
add('scale_all', 'Доля видео масштабов с пометкой «3D» и «2D» в названии (длинные, 7–30 дней)', '3D: 21; 2D: 4', 51, 'видео', 'data/videos.csv',
    note='«2D»-ролики: 10 002, 962, 629, 37 просмотров; без пометки 3D может быть 3D')
add('probe_quiz', 'Факт пробы: Дунай протекает по территории или по границе 10 стран', '10', '', '', 'UNDP/GEF Danube Regional Project', 'https://archive.iwlearn.net/undp-drp.org/drp/danube.html')
add('probe_quiz', 'Факт пробы: площадь Ватикана 0,44 км², Монако 2,1 км² (округлено)', '0.44; 2.1', '', '', 'Encyclopaedia Britannica', 'https://www.britannica.com/print/article/2245131',
    'другие источники дают Монако 1,99–2,08 км²; в кадре сказано «больше чем в 4 раза» — верно для всех значений')
with open(os.path.join(ROOT, 'docs', 'channel-reassessment', 'data', 'evidence.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
```

## 7. Реестр доказательств в Markdown

Файл `evidence_md.py`.

```python
"""Readable evidence registry from data/evidence.csv -> evidence.md"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', '..', 'docs', 'channel-reassessment')
R = list(csv.DictReader(open(os.path.join(D, 'data', 'evidence.csv'))))
NAME = {'quiz_pub_general': 'Викторина общих знаний', 'english_stories_all': 'Английский через истории', 'scale_all': 'Масштабы (Honest Scale)',
        'quiz_geo': 'Географическая викторина', 'quiz_topic_seniors': 'Тематические викторины и для старших', 'brain_seniors': 'Игры на память',
        'folklore_slavic': 'Славянский фольклор (Thrice-Nine Tales)', 'learn_russian': 'Русский для иностранцев', 'russian_lit': 'Русская классика',
        'chess': 'Шахматы', 'puzzles': 'Логические задачи', 'trends': 'Интерес на поиске YouTube (США)', 'production': 'Средства производства',
        'probe_quiz': 'Факты пробы викторины', 'probe_time': 'Время сборки проб'}
def fmt(v):
    try: return f'{int(v):,}'.replace(',', ' ')
    except Exception: return v
out = ['# Реестр доказательств', '',
       'Каждое утверждение отчёта с числом, знаменателем, датой и источником. Та же таблица для фильтров — [data/evidence.csv](data/evidence.csv). Замер 2026-10-17, поиск YouTube в США; это снимок выдачи, не рынок целиком. Медиана при `n` меньше 15 ненадёжна. Просмотры — не выручка.', '']
order = list(dict.fromkeys(r['direction'] for r in R))
for d in order:
    out += [f'## {NAME.get(d, d)}', '']
    for r in R:
        if r['direction'] != d: continue
        n = f" (`n` {r['n']} {r['denominator']})" if r['n'] not in ('', '1') else ''
        link = f" [ссылка]({r['urls']})" if r['urls'] else ''
        note = f" — {r['note']}" if r['note'] else ''
        out.append(f"- {r['id']}. {r['claim']}: **{fmt(r['value'])}**{n}{note}.{link} Источник: {r['source']}.")
    out.append('')
open(os.path.join(D, 'evidence.md'), 'w').write('\n'.join(out))
print(len(R))
```
