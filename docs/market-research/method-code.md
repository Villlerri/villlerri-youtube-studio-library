# Приложение: код сбора данных и расчётов

Код, которым собраны данные и посчитаны таблицы исследования. Приведён для проверки и повторения; в проект как программа не сохраняется. Запуск: Python 3.14, пакеты `yt-dlp==2026.08.19`, `pytrends`; каждый скрипт читает и пишет файлы рядом с собой (`raw/`, `out/`) и в `docs/market-research/data/`.

Порядок: сбор (1–3), метрики (4–8), сборка данных (9), рейтинг и сценарии (10–11). Файл `niches.json` — те же запросы, что в [data/niches.csv](data/niches.csv).

Известные особенности:

- Первый проход Trends запрашивал и общемировые данные; они совпали с США до сотых и не используются.
- В `analyze.py` признак «новый канал» требует меньше 30 видео на вкладке «Видео» (иначе первая загрузка неизвестна).
- Баллы денег, производства, затрат, риска и отличия в `scores.py` — оценка исследования, обоснование в concepts.md.

## 1. Сбор выборки поиска и каналов (yt-dlp)

Файл `collect.py`.

```python
"""Collect public YouTube search samples and channel listings. Run: tmp/venv/bin/python -I collect.py"""
import json, sys, time, urllib.parse, concurrent.futures as cf, os, datetime
import yt_dlp
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'raw')
SP_MONTH='EgQIBBAB'  # upload date: this month, type: video
def ydl(n): return yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'extract_flat':'in_playlist','playlistend':n,'skip_download':True,
  'extractor_args':{'youtubetab':{'approximate_date':['']}}, 'socket_timeout':30})
def search(q,lang,gl,n=40):
  url=f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={SP_MONTH}&hl={lang}&gl={gl}"
  for a in range(3):
    try:
      info=ydl(n).extract_info(url,download=False)
      return [{k:e.get(k) for k in ('id','title','channel','channel_id','view_count','duration','timestamp','url')} for e in info.get('entries') or [] if e.get('id') and len(e['id'])==11]
    except Exception as ex: err=str(ex); time.sleep(5)
  return {'error':err}
def channel(key,n=30):
  url=(f"https://www.youtube.com/{key}/videos" if key.startswith('@') else f"https://www.youtube.com/channel/{key}/videos")
  for a in range(3):
    try:
      info=ydl(n).extract_info(url,download=False)
      ents=[{k:e.get(k) for k in ('id','title','view_count','duration','timestamp')} for e in info.get('entries') or []]
      return {'key':key,'channel':info.get('channel'),'channel_id':info.get('channel_id'),'subs':info.get('channel_follower_count'),'url':info.get('channel_url') or url.rsplit('/videos',1)[0],'videos':ents}
    except Exception as ex: err=str(ex); time.sleep(5)
  return {'key':key,'error':err}
def main():
  niches=json.load(open(os.path.join(HERE,'niches.json')))
  now=datetime.datetime.now(datetime.timezone.utc).isoformat()
  sp=os.path.join(RAW,'search.json'); S=json.load(open(sp)) if os.path.exists(sp) else {}
  jobs=[(n['id'],q,n['lang'],n['gl']) for n in niches for q in n['q'] if f"{n['id']}|{q}" not in S]
  with cf.ThreadPoolExecutor(4) as ex:
    for (nid,q,l,g),r in zip(jobs, ex.map(lambda j: search(j[1],j[2],j[3]), jobs)):
      S[f"{nid}|{q}"]={'niche':nid,'query':q,'lang':l,'gl':g,'measured':now,'results':r}
      print('search',nid,q,len(r) if isinstance(r,list) else r,flush=True)
  json.dump(S,open(sp,'w'),ensure_ascii=False)
  keys=set()
  for n in niches: keys.update(n['seeds'])
  for v in S.values():
    if isinstance(v['results'],list): keys.update(e['channel_id'] for e in v['results'] if e.get('channel_id'))
  cp=os.path.join(RAW,'channels.json'); C=json.load(open(cp)) if os.path.exists(cp) else {}
  todo=[k for k in keys if k not in C or 'error' in C[k]]
  print('channels to fetch',len(todo),flush=True)
  with cf.ThreadPoolExecutor(4) as ex:
    for i,(k,r) in enumerate(zip(todo, ex.map(channel,todo))):
      r['measured']=datetime.datetime.now(datetime.timezone.utc).isoformat(); C[k]=r
      if i%50==0: json.dump(C,open(cp,'w'),ensure_ascii=False); print('channels',i,flush=True)
  json.dump(C,open(cp,'w'),ensure_ascii=False); print('done',flush=True)
main()
```

## 2. Google Trends, первый проход (якорь documentary)

Файл `trends.py`.

```python
"""Google Trends, YouTube Search, weekly 5 years. Anchor 'documentary' in every batch."""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE=os.path.dirname(os.path.abspath(__file__))
T={"eng_howitworks":"how it works","math_vis":"math","physics_anim":"physics","space_scale":"universe","history_maps":"history",
"geo_explainers":"geography","sleep_docs":"history for sleep","ambient_nature":"rain sounds","ambient_places":"ambience","fantasy_ambience":"cozy ambience",
"study_music":"study music","finance_econ":"economics","tech_systems":"system design","psych_phil":"philosophy","myth_folklore":"mythology",
"mystery_docs":"unsolved mysteries","aviation_maritime":"plane crash","art_history":"art history","language_ci":"learn english","biology_body":"human body",
"sim_shorts":"simulation","data_vis":"comparison","urbanism":"urban planning","kids_edu":"learning videos for kids","linguistics":"linguistics",
"music_theory":"music theory","ai_tools":"ai tools","reddit_stories":"reddit stories","top10_compilations":"top 10","wildlife_stock":"wildlife"}
ANCHOR="documentary"
out={'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(),'anchor':ANCHOR,'source':'Google Trends, YouTube Search, weekly, today 5-y','geo':{}}
p=TrendReq(hl='en-US',tz=0)
items=list(T.items())
for geo in ['US','']:
  res={}
  for i in range(0,len(items),4):
    batch=items[i:i+4]; kw=[t for _,t in batch]+[ANCHOR]
    for a in range(4):
      try:
        p.build_payload(kw,timeframe='today 5-y',geo=geo,gprop='youtube'); d=p.interest_over_time(); break
      except Exception as ex: print('retry',geo,kw,ex,flush=True); time.sleep(30*(a+1)); d=None
    if d is None: continue
    for nid,t in batch:
      res[nid]={'term':t,'dates':[x.strftime('%Y-%m-%d') for x in d.index],'values':[int(v) for v in d[t]],'anchor':[int(v) for v in d[ANCHOR]]}
    print('ok',geo or 'WW',kw,flush=True); time.sleep(8)
  out['geo'][geo or 'WW']=res
  json.dump(out,open(os.path.join(HERE,'raw','trends.json'),'w'),ensure_ascii=False)
print('done')
```

## 3. Google Trends, второй проход (якорь philosophy)

Файл `trends2.py`.

```python
"""Second pass: low-volume terms vs mid anchor 'philosophy', US, YouTube Search, 5y weekly."""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE=os.path.dirname(os.path.abspath(__file__))
TERMS=["how it works","geography","history for sleep","cozy ambience","economics","system design","mythology","unsolved mysteries","art history","learn english",
"human body","urban planning","learning videos for kids","linguistics","music theory","ai tools","slavic mythology","baba yaga","folklore","sleep documentary",
"boring history","nature sounds","forest sounds","english story","size comparison","marble race","history map","how things work"]
ANCHOR="philosophy"
out={'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(),'anchor':ANCHOR,'source':'Google Trends, YouTube Search, US, weekly, today 5-y','terms':{}}
p=TrendReq(hl='en-US',tz=0)
for i in range(0,len(TERMS),4):
  kw=TERMS[i:i+4]+[ANCHOR]; d=None
  for a in range(4):
    try: p.build_payload(kw,timeframe='today 5-y',geo='US',gprop='youtube'); d=p.interest_over_time(); break
    except Exception as ex: print('retry',kw,ex,flush=True); time.sleep(30*(a+1))
  if d is None: continue
  for t in kw[:-1]: out['terms'][t]={'dates':[x.strftime('%Y-%m-%d') for x in d.index],'values':[int(v) for v in d[t]],'anchor':[int(v) for v in d[ANCHOR]]}
  print('ok',kw,flush=True); time.sleep(8)
json.dump(out,open(os.path.join(HERE,'raw','trends2.json'),'w'),ensure_ascii=False); print('done')
```

## 4. Метрики первого прохода Trends

Файл `trends_an.py`.

```python
import json, os, csv, statistics as st
HERE=os.path.dirname(os.path.abspath(__file__)); T=json.load(open(os.path.join(HERE,'raw','trends.json')))
rows=[]
MON='янв фев мар апр май июн июл авг сен окт ноя дек'.split()
for geo,res in T['geo'].items():
  for nid,r in res.items():
    v=r['values']; a=r['anchor']; d=r['dates']
    if len(v)<160: continue
    l52=v[-52:]; p52=v[-104:-52]; o52=v[-208:-156]
    rel=(st.mean(l52)/st.mean(a[-52:])) if st.mean(a[-52:]) else None
    yoy=(st.mean(l52)/st.mean(p52)) if st.mean(p52) else None
    y3=(st.mean(l52)/st.mean(o52)) if st.mean(o52) else None
    bym={}
    for di,vi in zip(d,v): bym.setdefault(int(di[5:7]),[]).append(vi)
    mm={m:st.mean(x) for m,x in bym.items()}; mean=st.mean(mm.values()) or 1
    peak=max(mm,key=mm.get); low=min(mm,key=mm.get)
    rows.append({'geo':geo,'niche':nid,'term':r['term'],'measured':T['measured'][:10],'level_vs_documentary_52w':round(rel,2) if rel is not None else None,
      'change_52w_vs_prev_52w':round(yoy,2) if yoy else None,'change_52w_vs_3y_ago':round(y3,2) if y3 else None,
      'season_peak_month':MON[peak-1],'season_low_month':MON[low-1],'season_amplitude':round((mm[peak]-mm[low])/mean,2)})
os.makedirs(os.path.join(HERE,'out'),exist_ok=True)
with open(os.path.join(HERE,'out','trends.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
  if r['geo']=='US': print(r['niche'].ljust(20),r['term'].ljust(26),r['level_vs_documentary_52w'],r['change_52w_vs_prev_52w'],r['change_52w_vs_3y_ago'],r['season_peak_month'],r['season_low_month'],r['season_amplitude'])
```

## 5. Метрики второго прохода Trends

Файл `trends2_an.py`.

```python
"""Metrics for the second Trends pass (anchor 'philosophy'). Writes out/trends-low-volume.csv"""
import json, csv, statistics as st, os
HERE=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(HERE,'raw','trends2.json')))
MON='янв фев мар апр май июн июл авг сен окт ноя дек'.split()
rows=[]
for t,r in T['terms'].items():
  v=r['values']; a=r['anchor']; d=r['dates']
  l52=v[-52:]; p52=v[-104:-52]; o52=v[-208:-156]
  rel=st.mean(l52)/st.mean(a[-52:]); yoy=st.mean(l52)/st.mean(p52) if st.mean(p52) else None; y3=st.mean(l52)/st.mean(o52) if st.mean(o52) else None
  bym={}
  for di,vi in zip(d,v): bym.setdefault(int(di[5:7]),[]).append(vi)
  mm={m:st.mean(x) for m,x in bym.items()}; mean=st.mean(mm.values()) or 1
  pk=max(mm,key=mm.get); lo=min(mm,key=mm.get)
  rows.append({'geo':'US','term':t,'anchor':'philosophy','measured':T['measured'][:10],'level_vs_anchor_52w':round(rel,2),'change_52w_vs_prev_52w':round(yoy,2) if yoy else None,'change_52w_vs_3y_ago':round(y3,2) if y3 else None,'season_peak_month':MON[pk-1],'season_low_month':MON[lo-1],'season_amplitude':round((mm[pk]-mm[lo])/mean,2),'weeks_nonzero':sum(1 for x in v if x>0)})
with open(os.path.join(HERE,'out','trends-low-volume.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
```

## 6. Описательные метрики ниш, таблицы видео и каналов

Файл `analyze.py`.

```python
"""Per-niche metrics from raw/search.json + raw/channels.json. Writes out/niche-metrics.csv, out/videos.csv, out/channels.csv"""
import json, os, csv, statistics as st, datetime
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
N={n['id']:n for n in json.load(open(os.path.join(HERE,'niches.json')))}
S=json.load(open(os.path.join(HERE,'raw','search.json'))); C=json.load(open(os.path.join(HERE,'raw','channels.json')))
def med(x): return st.median(x) if x else None
def q(x,p):
  if not x: return None
  x=sorted(x); return x[min(len(x)-1,int(p*(len(x)-1)+0.5))]
def chan_stats(c):
  v=[e for e in c.get('videos') or [] if e.get('view_count') is not None]
  views=[e['view_count'] for e in v]; ts=[e['timestamp'] for e in v if e.get('timestamp')]
  raw=c.get('videos') or []
  first=min(ts) if ts and len(raw)<30 else None   # only when list is complete (fewer than 30 uploads)
  span=(max(ts)-min(ts))/86400 if len(ts)>1 else None
  return {'n_recent':len(v),'median_recent_views':med(views),'min_recent':min(views) if views else None,
          'complete_list':len(raw)<30,'first_upload':first,'uploads_per_month':round(len(ts)/(span/30.4),1) if span and span>0 else None}
for k,c in C.items(): c['stats']=chan_stats(c) if 'error' not in c else {}
byid={}
for c in C.values():
  if c.get('channel_id'): byid[c['channel_id']]=c
vids={}; vrows=[]
for key,s in S.items():
  if not isinstance(s['results'],list): continue
  m=datetime.datetime.fromisoformat(s['measured']).timestamp()
  for e in s['results']:
    nid=s['niche']; vid=e['id']
    if (nid,vid) in vids: continue
    ch=byid.get(e.get('channel_id'),{}); age=(m-e['timestamp'])/86400 if e.get('timestamp') else None
    r={'niche':nid,'query':s['query'],'lang':s['lang'],'measured':s['measured'][:10],'video_id':vid,'url':f"https://www.youtube.com/watch?v={vid}",
       'title':e.get('title'),'channel':e.get('channel'),'channel_id':e.get('channel_id'),'channel_url':f"https://www.youtube.com/channel/{e.get('channel_id')}",
       'subs':ch.get('subs'),'views':e.get('view_count'),'duration_s':e.get('duration'),'age_days_approx':round(age,1) if age is not None else None,
       'channel_median_recent_views':ch.get('stats',{}).get('median_recent_views'),'channel_new':None}
    st_=ch.get('stats',{})
    if st_.get('first_upload'): r['channel_new']= (m-st_['first_upload'])/86400 < 365
    vids[(nid,vid)]=r; vrows.append(r)
rows=[]
for nid,n in N.items():
  V=[r for r in vrows if r['niche']==nid and r['views'] is not None]
  if not V: continue
  views=[r['views'] for r in V]; mature=[r['views'] for r in V if (r['age_days_approx'] or 0)>=7]
  subs=[r for r in V if r['subs'] is not None]
  small=[r for r in subs if r['subs']<10000]; mid=[r for r in subs if r['subs']<100000]
  chans={}
  for r in V: chans.setdefault(r['channel_id'],0); chans[r['channel_id']]+=r['views']
  tot=sum(chans.values()) or 1; top3=sum(sorted(chans.values(),reverse=True)[:3])/tot
  cs=[byid[c] for c in chans if c in byid]
  typ=[c['stats']['median_recent_views'] for c in cs if c['stats'].get('median_recent_views') is not None and (c['stats'].get('n_recent') or 0)>=5]
  fail=[t for t in typ if t<1000]
  smallc=[c for c in cs if c.get('subs') is not None and c['subs']<100000 and c['stats'].get('median_recent_views') is not None and (c['stats'].get('n_recent') or 0)>=5]
  newc=[c for c in cs if c['stats'].get('first_upload') and (datetime.datetime.now().timestamp()-c['stats']['first_upload'])/86400<365]
  newc_ok=[c for c in newc if (c['stats'].get('median_recent_views') or 0)>=10000]
  dur=[r['duration_s'] for r in V if r['duration_s']]
  rows.append({'niche':nid,'name_ru':n['ru'],'lang':n['lang'],'region_param':n['gl'],'measured':V[0]['measured'],'n_videos':len(V),'n_channels':len(chans),
   'views_median':med(views),'views_p25':q(views,.25),'views_p75':q(views,.75),'views_median_age7d':med(mature),
   'share_videos_subs_lt10k':round(len(small)/len(subs),2) if subs else None,'share_videos_subs_lt100k':round(len(mid)/len(subs),2) if subs else None,
   'breakouts_lt10k_ge10k_views':sum(1 for r in small if r['views']>=10000),'breakouts_lt100k_ge100k_views':sum(1 for r in mid if r['views']>=100000),
   'top3_channel_view_share':round(top3,2),'channels_typical_views_median':med(typ),'share_channels_typical_lt1k':round(len(fail)/len(typ),2) if typ else None,
   'small_channels_typical_views_median':med([c['stats']['median_recent_views'] for c in smallc]),'n_new_channels':len(newc),'n_new_channels_typical_ge10k':len(newc_ok),
   'duration_median_min':round(med(dur)/60,1) if dur else None,'share_le180s':round(sum(1 for d in dur if d<=180)/len(dur),2) if dur else None})
def w(name,rows):
  if not rows: return
  with open(os.path.join(OUT,name),'w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
w('niche-metrics.csv',rows); w('videos.csv',vrows)
crow=[]
for k,c in C.items():
  if 'error' in c: crow.append({'key':k,'channel':None,'channel_url':None,'subs':None,'measured':c.get('measured','')[:10],'n_recent':None,'median_recent_views':None,'min_recent':None,'uploads_per_month':None,'first_upload_if_complete':None,'error':c['error'][:120]}); continue
  s=c['stats']; crow.append({'key':k,'channel':c.get('channel'),'channel_url':c.get('url'),'subs':c.get('subs'),'measured':c.get('measured','')[:10],'n_recent':s.get('n_recent'),
   'median_recent_views':s.get('median_recent_views'),'min_recent':s.get('min_recent'),'uploads_per_month':s.get('uploads_per_month'),
   'first_upload_if_complete':datetime.datetime.fromtimestamp(s['first_upload'],datetime.timezone.utc).strftime('%Y-%m') if s.get('first_upload') else None,'error':None})
w('channels.csv',crow)
print(len(rows),len(vrows),len(crow))
```

## 7. Сопоставимые метрики: видео 7–30 дней, длинные и короткие, по размеру канала

Файл `analyze2.py`.

```python
"""Age- and format-matched metrics: videos aged 7-30 days, long (>180 s) vs short (<=180 s), by channel size. Writes out/niche-matched.csv"""
import csv, os, statistics as st
HERE=os.path.dirname(os.path.abspath(__file__))
V=list(csv.DictReader(open(os.path.join(HERE,'out','videos.csv'))))
def f(x):
  try: return float(x)
  except: return None
def stats(xs):
  xs=sorted(xs)
  if not xs: return (0,'','','')
  q=lambda p: xs[min(len(xs)-1,int(p*(len(xs)-1)+0.5))]
  return (len(xs),int(st.median(xs)),int(q(.25)),int(q(.75)))
rows=[]
for nid in dict.fromkeys(r['niche'] for r in V):
  vs=[r for r in V if r['niche']==nid and f(r['views']) is not None]
  aged=[r for r in vs if f(r['age_days_approx']) is not None and 7<=f(r['age_days_approx'])<=30]
  long_=[r for r in aged if (f(r['duration_s']) or 0)>180]; short=[r for r in aged if f(r['duration_s']) is not None and f(r['duration_s'])<=180]
  def bucket(rs,lo,hi): return [f(r['views']) for r in rs if f(r['subs']) is not None and lo<=f(r['subs'])<hi]
  row={'niche':nid,'n_all':len(vs),'n_age_7_30d':len(aged),'n_unknown_age':sum(1 for r in vs if f(r['age_days_approx']) is None)}
  for name,rs in [('long',long_),('short',short)]:
    n,m,p25,p75=stats([f(r['views']) for r in rs]); row.update({f'{name}_n':n,f'{name}_median':m,f'{name}_p25':p25,f'{name}_p75':p75})
  for name,lo,hi in [('subs_lt10k',0,1e4),('subs_10k_100k',1e4,1e5),('subs_ge100k',1e5,1e12)]:
    n,m,p25,p75=stats(bucket(long_,lo,hi)); row.update({f'long_{name}_n':n,f'long_{name}_median':m})
  n,m,_,_=stats([f(r['views']) for r in long_ if f(r['subs']) is None]); row.update({'long_subs_unknown_n':n})
  n,m,p25,p75=stats([f(r['views']) for r in long_ if r['channel_new']=='True']); row.update({'long_new_channel_n':n,'long_new_channel_median':m})
  n2=[f(r['views']) for r in long_ if f(r['subs']) is not None and f(r['subs'])<1e5]
  row['long_subs_lt100k_ge10k_views']=sum(1 for x in n2 if x>=1e4)
  rows.append(row)
with open(os.path.join(HERE,'out','niche-matched.csv'),'w',newline='') as fo:
  w=csv.DictWriter(fo,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['niche'][:18]:18} all={r['n_all']:3} aged={r['n_age_7_30d']:3} long n={r['long_n']:3} med={r['long_median']!s:>7} | <10k n={r['long_subs_lt10k_n']:2} med={r['long_subs_lt10k_median']!s:>6} | 10-100k n={r['long_subs_10k_100k_n']:2} med={r['long_subs_10k_100k_median']!s:>6} | >=100k n={r['long_subs_ge100k_n']:2} med={r['long_subs_ge100k_median']!s:>7} | new n={r['long_new_channel_n']:2} med={r['long_new_channel_median']!s:>6} | <100k>=10k: {r['long_subs_lt100k_ge10k_views']:2} | short n={r['short_n']:2} med={r['short_median']}")
```

## 8. Примеры по нишам

Файл `examples.py`.

```python
"""Per niche: leader, small-channel breakout, median (ordinary) video, struggling channels, new channels. Writes out/examples.csv"""
import csv, os, statistics as st
HERE=os.path.dirname(os.path.abspath(__file__))
V=list(csv.DictReader(open(os.path.join(HERE,'out','videos.csv'))))
C={r['channel_url'].rsplit('/',1)[-1] if r['channel_url'] else r['key']:r for r in csv.DictReader(open(os.path.join(HERE,'out','channels.csv')))}
def num(x):
  try: return float(x)
  except: return None
rows=[]
for nid in dict.fromkeys(r['niche'] for r in V):
  vs=[r for r in V if r['niche']==nid and num(r['views']) is not None]
  vs.sort(key=lambda r:num(r['views']))
  def add(kind,r,note=''):
    ch=C.get(r['channel_id'],{})
    rows.append({'niche':nid,'kind':kind,'measured':r['measured'],'video_url':r['url'],'title':r['title'],'views':int(num(r['views'])),'age_days_approx':r['age_days_approx'],
      'channel':r['channel'],'channel_url':r['channel_url'],'subs':r['subs'],'channel_typical_views':ch.get('median_recent_views'),'channel_uploads_per_month':ch.get('uploads_per_month'),
      'channel_first_upload_if_known':ch.get('first_upload_if_complete'),'note':note})
  add('leader',vs[-1],'most viewed video in sample')
  add('ordinary',vs[len(vs)//2],'median video in sample')
  sm=[r for r in vs if num(r['subs']) is not None and num(r['subs'])<10000]
  if sm: add('small_breakout',sm[-1],'best video from a channel under 10k subscribers')
  newc=[r for r in vs if r['channel_new']=='True']
  if newc: add('new_channel',newc[-1],'best video from a channel with first upload under 12 months ago (complete upload list only)')
  seen=set(); k=0
  for r in vs:
    ch=C.get(r['channel_id'],{}); t=num(ch.get('median_recent_views')); n=num(ch.get('n_recent'))
    if t is not None and t<1000 and n and n>=10 and r['channel_id'] not in seen:
      seen.add(r['channel_id']); add('struggling',r,'channel with 10+ recent uploads and typical video under 1,000 views'); k+=1
      if k>=2: break
with open(os.path.join(HERE,'out','examples.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
```

## 9. Сборка CSV в папку data

Файл `build_data.py`.

```python
"""Copy and merge outputs into docs/market-research/data: niches.csv, trends.csv (US first pass + second pass), sample CSVs."""
import json, csv, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(HERE,'..','..','docs','market-research','data')
N=json.load(open(os.path.join(HERE,'niches.json')))
with open(os.path.join(D,'niches.csv'),'w',newline='') as f:
  w=csv.writer(f); w.writerow(['niche','name_ru','language','region_param','query_1','query_2','reference_channels','search_filter','measured'])
  for n in N: w.writerow([n['id'],n['ru'],n['lang'],n['gl'],n['q'][0],n['q'][1],'; '.join(n['seeds']),'upload date: this month; type: video; sort: relevance','2026-10-14'])
rows=[]
for r in csv.DictReader(open(os.path.join(HERE,'out','trends.csv'))):
  if r['geo']!='US': continue   # worldwide pass returned values identical to US and is not used
  rows.append({'term':r['term'],'niche':r['niche'],'geo':'US','property':'YouTube Search','window':'2021-10..2026-10 weekly','anchor':'documentary','level_vs_anchor_52w':r['level_vs_documentary_52w'],'change_52w_vs_prev_52w':r['change_52w_vs_prev_52w'],'change_52w_vs_3y_ago':r['change_52w_vs_3y_ago'],'season_peak_month':r['season_peak_month'],'season_low_month':r['season_low_month'],'season_amplitude':r['season_amplitude'],'measured':r['measured'],'note':'low-volume term: values rounded, prefer anchor philosophy row' if float(r['level_vs_documentary_52w'] or 0)<0.05 else ''})
for r in csv.DictReader(open(os.path.join(HERE,'out','trends-low-volume.csv'))):
  rows.append({'term':r['term'],'niche':'','geo':'US','property':'YouTube Search','window':'2021-10..2026-10 weekly','anchor':'philosophy','level_vs_anchor_52w':r['level_vs_anchor_52w'],'change_52w_vs_prev_52w':r['change_52w_vs_prev_52w'],'change_52w_vs_3y_ago':r['change_52w_vs_3y_ago'],'season_peak_month':r['season_peak_month'],'season_low_month':r['season_low_month'],'season_amplitude':r['season_amplitude'],'measured':r['measured'],'note':'term has zero weeks: '+str(262-int(r['weeks_nonzero'])) if int(r['weeks_nonzero'])<250 else ''})
with open(os.path.join(D,'trends.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for src,dst in [('niche-metrics.csv','niche-metrics.csv'),('niche-matched.csv','niche-matched.csv'),('videos.csv','videos-sample.csv'),('channels.csv','channels-sample.csv'),('examples.csv','examples.csv'),('elevenlabs-voices.csv','elevenlabs-voices.csv')]:
  shutil.copy(os.path.join(HERE,'out',src),os.path.join(D,dst))
```

## 10. Баллы концепций и проверка весов

Файл `scores.py`.

```python
"""Concept scores: demand and entry from data (formulas in method.md), other criteria by judgement. Writes docs/market-research/data/scores.csv"""
import csv, math, os
ROOT=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(ROOT,'..','..','docs','market-research','data')
M={r['niche']:r for r in csv.DictReader(open(os.path.join(ROOT,'out','niche-matched.csv')))}
T={r['term']:r for r in csv.DictReader(open(os.path.join(D,'trends.csv')))}
def band(v):
  return 1 if v<100 else 2 if v<300 else 3 if v<1000 else 4 if v<5000 else 5
W={'demand':.15,'entry':.2,'money':.15,'production_fit':.2,'cost':.1,'risk':.1,'differentiation':.1}
# judgement scores (1-5) with confidence; reasons in concepts.md
J={
 'field':   dict(name='Taiga Hours',niche='ambient_nature',term='rain sounds',money=(3,'low'),production_fit=(4.5,'medium'),cost=(3,'medium'),risk=(3.5,'medium'),differentiation=(4.5,'medium'),pilot_h='25-40',reg_h='8-15 plus travel',pilot_usd='500-900 plus travel',month_usd='travel',voice='none'),
 'scale':   dict(name='Honest Scale',niche='space_scale',term='universe',money=(3,'low'),production_fit=(4.5,'medium'),cost=(2.5,'medium'),risk=(4,'medium'),differentiation=(3,'low'),pilot_h='30-45',reg_h='12-20',pilot_usd='0 plus render hardware',month_usd='0 plus render',voice='optional, own voice'),
 'sleep':   dict(name='Lantern Library',niche='sleep_docs',term='history for sleep',money=(3,'low'),production_fit=(3,'medium'),cost=(3,'medium'),risk=(2.5,'medium'),differentiation=(3.5,'medium'),pilot_h='30-40',reg_h='15-25',pilot_usd='0-200',month_usd='0',voice='own voice, 2-3 h per video'),
 'sim':     dict(name='Sandbox Trials',niche='sim_shorts',term='simulation',money=(2,'medium'),production_fit=(3.5,'medium'),cost=(4.5,'medium'),risk=(3,'medium'),differentiation=(2.5,'low'),pilot_h='15-25',reg_h='1-2 per Short; 6-10 per long',pilot_usd='0',month_usd='0',voice='none'),
 'maps':    dict(name='The Moving Atlas',niche='history_maps',term='history',money=(3,'low'),production_fit=(4.5,'medium'),cost=(3.5,'medium'),risk=(3.5,'medium'),differentiation=(3.5,'medium'),pilot_h='30-40',reg_h='12-18',pilot_usd='0-200',month_usd='0',voice='own voice, 10-15 min per video'),
 'folklore':dict(name='Thrice-Nine Tales',niche='myth_folklore',term='mythology',money=(2.5,'low'),production_fit=(4.5,'medium'),cost=(2.5,'medium'),risk=(4,'medium'),differentiation=(5,'medium'),pilot_h='40-60',reg_h='15-25',pilot_usd='0-300',month_usd='0',voice='own voice'),
 'machines':dict(name='Opened Up',niche='eng_howitworks',term='how it works',money=(3.5,'low'),production_fit=(4,'medium'),cost=(1.5,'medium'),risk=(4.5,'medium'),differentiation=(2,'medium'),pilot_h='40-60',reg_h='30-60',pilot_usd='0-500 models',month_usd='0',voice='own voice'),
 'english': dict(name='Story Steps English',niche='language_ci',term='english story',money=(2.5,'low'),production_fit=(2.5,'medium'),cost=(4,'medium'),risk=(3,'medium'),differentiation=(3,'low'),pilot_h='20-30',reg_h='6-10',pilot_usd='0 plus narrator',month_usd='narrator if hired',voice='native-level English required'),
}
rows=[]
for cid,j in J.items():
  m=M[j['niche']]; t=T[j['term']]
  ln=int(m['long_n']); lmed=float(m['long_median'] or 0)
  n10=int(m['long_subs_lt10k_n']); m10=float(m['long_subs_lt10k_median'] or 0)
  b=int(m['long_subs_lt100k_ge10k_views']); bshare=b/ln if ln else 0
  yoy=float(t['change_52w_vs_prev_52w'] or 1)
  demand=band(lmed)+(0.5 if yoy>=1.2 else -0.5 if yoy<=0.85 else 0); demand=max(1,min(5,demand))
  entry=band(m10)+(0.5 if bshare>=0.25 else -0.5 if bshare<0.05 else 0); entry=max(1,min(5,entry))
  dconf='medium' if ln>=30 else 'low'; econf='medium' if n10>=20 else 'low'
  r={'concept_id':cid,'working_name':j['name'],'niche_sample':j['niche'],
     'in_long_7_30d_n':ln,'in_long_7_30d_median_views':int(lmed),'in_trend_term':j['term'],'in_trend_change_52w':yoy,
     'in_subs_lt10k_n':n10,'in_subs_lt10k_median_views':int(m10),'in_lt100k_ge10k_count':b,'in_lt100k_ge10k_share':round(bshare,2),
     'in_new_channel_n':m['long_new_channel_n'],'in_new_channel_median_views':m['long_new_channel_median'],
     'demand':demand,'demand_conf':dconf,'entry':entry,'entry_conf':econf}
  for k in ['money','production_fit','cost','risk','differentiation']:
    r[k]=j[k][0]; r[k+'_conf']=j[k][1]
  r['weighted_total']=round(sum(r[k]*w for k,w in W.items()),2)
  r.update({'pilot_human_hours':j['pilot_h'],'regular_human_hours':j['reg_h'],'pilot_cash_usd':j['pilot_usd'],'monthly_cash_usd':j['month_usd'],'voice':j['voice']})
  rows.append(r)
rows.sort(key=lambda r:-r['weighted_total'])
for i,r in enumerate(rows,1): r['rank']=i
fields=['rank']+[k for k in rows[0] if k!='rank']
with open(os.path.join(D,'scores.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
for r in rows: print(r['rank'],r['working_name'],r['weighted_total'],'demand',r['demand'],'entry',r['entry'],'| n10',r['in_subs_lt10k_n'],'m10',r['in_subs_lt10k_median_views'],'b',r['in_lt100k_ge10k_share'],'| new',r['in_new_channel_n'],r['in_new_channel_median_views'])
alts={'money 30%':{**W,'money':.3,'entry':.15,'production_fit':.15,'differentiation':.05},'production 30%':{**W,'production_fit':.3,'cost':.15,'demand':.1,'entry':.15},'data only':{'demand':.4,'entry':.6},'equal':{k:1/7 for k in W}}
for n,ww in alts.items():
  s=sorted(((sum(r[k]*v for k,v in ww.items())/sum(ww.values()),r['working_name']) for r in rows),reverse=True)
  print(n,'|',' > '.join(f"{x} {v:.2f}" for v,x in s))
```

## 11. Сценарии первого года

Файл `economics.py`.

```python
"""Year-one scenarios per concept and budget level. Writes docs/market-research/data/economics.csv. All inputs are research assumptions."""
import csv, os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','docs','market-research','data','economics.csv')
C={
 'maps': dict(name='The Moving Atlas',len_min=12,avd=(0.25,0.40),views={'low':300,'mid':2500,'high':15000},rpm=(2.0,8.0),per_month={'L1':2,'L2':3,'L3':4},sub_rate=(0.005,0.02)),
 'field':dict(name='Taiga Hours',len_min=240,avd=(10/240,40/240),views={'low':100,'mid':3000,'high':20000},rpm=(0.5,3.0),per_month={'L1':1,'L2':3,'L3':4},sub_rate=(0.005,0.015)),
 'scale':dict(name='Honest Scale',len_min=10,avd=(0.30,0.50),views={'low':300,'mid':4000,'high':30000},rpm=(1.5,6.0),per_month={'L1':1,'L2':2,'L3':3},sub_rate=(0.005,0.02)),
}
H=8000   # watch-hour threshold for new channels from 2027-02-01
AFTER=0.25  # share of year-one views that come after joining the programme
rows=[]
for cid,c in C.items():
  for lvl,pm in c['per_month'].items():
    for sc,v in c['views'].items():
      vids=pm*12; views=vids*v
      hl,hh=views*c['len_min']*c['avd'][0]/60, views*c['len_min']*c['avd'][1]/60
      sl,sh=views*c['sub_rate'][0], views*c['sub_rate'][1]
      st='likely' if (hl>=H and sl>=1000) else ('possible' if (hh>=H and sh>=1000) else 'no')
      lo=views*AFTER/1000*c['rpm'][0] if st=='likely' else 0
      hi=views*AFTER/1000*c['rpm'][1] if st!='no' else 0
      rows.append({'concept':c['name'],'budget_level':lvl,'scenario':sc,'long_videos_per_month':pm,'videos_year1':vids,'views_per_video_12m':v,'views_year1':views,
        'avg_view_minutes':f"{c['len_min']*c['avd'][0]:.0f}-{c['len_min']*c['avd'][1]:.0f}",'watch_hours_year1':f"{hl:.0f}-{hh:.0f}",'subscribers_year1':f"{sl:.0f}-{sh:.0f}",
        'ypp_8000h_1000subs_year1':st,'rpm_usd':f"{c['rpm'][0]:g}-{c['rpm'][1]:g}",'ad_revenue_year1_usd_payee_russia':0,'ad_revenue_year1_usd_eligible_payee':f"{lo:.0f}-{hi:.0f}"})
with open(OUT,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
```
