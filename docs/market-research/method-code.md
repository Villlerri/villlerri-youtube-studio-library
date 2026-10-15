# Приложение: код сбора данных и расчётов

Код, которым собраны данные и посчитаны таблицы исследования. Приведён для проверки и повторения; в проект как программа не сохраняется. Запуск: Python 3.14, пакеты `yt-dlp==2026.08.19`, `pytrends`; каждый скрипт читает и пишет файлы рядом с собой (`raw/`, `out/`) и в `docs/market-research/data/`.

Порядок: сбор (1–3), метрики (4–8), сборка данных (9), отсев, рейтинг и сценарии (10–12). Рейтинг версии 2 заменил прежний `scores.py`. Файл `niches.json` — те же запросы, что в [data/niches.csv](data/niches.csv).

Известные особенности:

- Первый проход Trends запрашивал и общемировые данные; они совпали с США до сотых и не используются.
- В `analyze.py` признак «новый канал» требует меньше 30 видео на вкладке «Видео» (иначе первая загрузка неизвестна).
- В `scores2.py` риск и допущения по длительности просмотра, часам и RPM — оценка исследования; обоснование в concepts.md и method.md.

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

## 10. Отсев выборок ниш (рейтинг версии 2, шаг 1)

`screening.py` пишет `data/screening.csv`.

```python
"""Step 1 of ranking v2: every niche sample gets a decision. Rule: shortlist when the small-channel long median
(age 7-30 days, channels <10k) is at least 1,000 views with n >= 10; earlier concepts stay for comparison.
Exclusions name the reason. Writes data/screening.csv."""
import csv, os
ROOT=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(ROOT,'..','..','docs','market-research','data')
M=list(csv.DictReader(open(os.path.join(D,'niche-matched.csv'))))
NAMES={r['niche']:r['name_ru'] for r in csv.DictReader(open(os.path.join(D,'niches.csv')))}
DEC={
 'sleep_docs':('шорт-лист','Lantern Library',''),
 'ambient_nature':('шорт-лист','Taiga Hours','для концепции взяты только названия без слов о музыке'),
 'fantasy_ambience':('шорт-лист','Boreal Hearth','только названия без слов о музыке; n=5'),
 'sim_shorts':('шорт-лист','Sandbox Trials',''),
 'study_music':('оценена, отсев по риску','Study music scenes','ценность в музыке: источник музыки, Content ID, риск взаимозаменяемого контента'),
 'reddit_stories':('оценена, отсев по риску','Reddit stories','повторно используемый контент и права на чужие посты'),
 'sleep_docs_de':('вариант','Lantern Library, German variant','то же производство, немецкий голос'),
 'ambient_nature_de':('подкрепляет','Taiga Hours, Boreal Hearth','эмбиент без речи не зависит от языка'),
 'space_scale':('для сравнения','Honest Scale','прежняя концепция'),
 'history_maps':('для сравнения','The Moving Atlas','прежняя концепция'),
 'myth_folklore':('для сравнения','Thrice-Nine Tales','прежняя концепция'),
 'language_ci':('для сравнения','Story Steps English','прежняя концепция; голос теперь доступен'),
 'eng_howitworks':('для сравнения','Opened Up','прежняя концепция'),
 'science_ja':('исключена','','качество японского текста команда не проверит; японских голосов 656'),
 'kids_edu':('исключена','','ограничения контента для детей; меньше 1 000'),
 'ai_tools':('исключена','','в выборке нет длинных видео малых каналов'),
 'wildlife_stock':('исключена','','риск повторно используемого контента; n меньше 10'),
 'top10_compilations':('исключена','','меньше 1 000; риск повторно используемого контента'),
 'math_vis':('исключена','','меньше 1 000; пересекается с отложенным проектом по физике'),
 'physics_anim':('исключена','','меньше 1 000; пересекается с отложенным проектом по физике'),
}
rows=[]
for r in M:
  n=int(r['long_subs_lt10k_n'] or 0); v=r['long_subs_lt10k_median']
  dec,concept,why=DEC.get(r['niche'],('исключена','','медиана меньше 1 000 просмотров или n меньше 10'))
  rows.append({'niche':r['niche'],'name_ru':NAMES.get(r['niche'],''),'long_7_30d_n':r['long_n'],'long_7_30d_median':r['long_median'],
    'subs_lt10k_n':n,'subs_lt10k_median':v,'decision':dec,'concept':concept,'reason':why})
with open(os.path.join(D,'screening.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter; print(Counter(r['decision'] for r in rows))
```

## 11. Баллы концепций и проверка устойчивости (рейтинг версии 2, шаг 2)

`scores2.py` пишет `data/scores.csv`. Допущения по концепциям — в словаре `C`; риск — оценка исследования, обоснование в concepts.md.

```python
"""Ranking v2 under author's conditions (ElevenLabs available, publishing outside Russia).
Criteria: speed to the programme threshold, monthly cash, simplicity, efficiency, risk.
Inputs: niche-matched.csv (data) plus per-concept assumptions below. Writes data/scores.csv."""
import csv, os, math
ROOT=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(ROOT,'..','..','docs','market-research','data')
M={r['niche']:r for r in csv.DictReader(open(os.path.join(D,'niche-matched.csv')))}
HOURS_BUDGET=60        # human hours per month (budget level 2, 10-20 h/week)
THRESHOLD_H=8000       # watch hours in 365 days for new channels from 2027-02-01
EL_CREDITS_PER_MIN=1000; EL_RETAKE=1.3   # ElevenLabs: 1 credit per character, ~1000 characters per minute
def el_cost(credits):  # cheapest public plan (base price, extra minute price) for the monthly credits
  if credits==0: return 0
  plans=[(6,30e3,0.20),(22,121e3,0.18),(99,600e3,0.17),(299,1.8e6,0.17)]
  return round(min(p+max(0,credits-c)/EL_CREDITS_PER_MIN*x for p,c,x in plans))
import re, statistics
MUSIC=re.compile(r'music|jazz|piano|lofi|lo-fi|432|celtic|song|melod|guitar|harp|flute',re.I)
def no_music(niche):  # long videos (>180 s), age 7-30 days, channels <10k, titles without music words; dedup by video id
  seen=set(); xs=[]
  for r in csv.DictReader(open(os.path.join(D,'videos-sample.csv'))):
    if r['niche']!=niche or r['video_id'] in seen: continue
    seen.add(r['video_id'])
    try: a=float(r['age_days_approx']); d=float(r['duration_s']); s=float(r['subs']); v=float(r['views'])
    except: continue
    if 7<=a<=30 and d>180 and s<1e4 and not MUSIC.search(r['title']): xs.append(v)
  return (statistics.median(xs) if xs else 0, len(xs))
# niche, length min, avd (low,base,high) min, human h/video (low,base,high), max videos/month,
# narration min/video, other cash $/month, rpm (low,high), risk 1-5, skill penalty, equipment penalty
C={
 'sleep':  dict(name='Lantern Library',niche='sleep_docs',length=150,avd=(10,20,40),h=(8,10,14),cap=4,narr=150,cash=0,rpm=(1.5,5),risk=3,skill=0,equip=0),
 'sleep_de':dict(name='Lantern Library, German variant',niche='sleep_docs_de',length=150,avd=(10,20,40),h=(9,12,16),cap=4,narr=150,cash=0,rpm=(1.5,5),risk=2.5,skill=0,equip=0,variant=True),
 'hearth': dict(name='Boreal Hearth',niche='fantasy_ambience',length=180,avd=(10,25,50),h=(4,6,8),cap=6,narr=0,cash=10,rpm=(0.5,3),risk=2.5,skill=0,equip=0,nomusic=True),
 'field':  dict(name='Taiga Hours',niche='ambient_nature',length=240,avd=(10,25,50),h=(10,14,18),cap=4,narr=0,cash=110,rpm=(0.5,3),risk=3.5,skill=0.5,equip=0.5,nomusic=True),
 'sim':    dict(name='Sandbox Trials',niche='sim_shorts',length=12,avd=(3,4.8,6.6),h=(6,8,10),cap=2,narr=0,cash=0,rpm=(1,4),risk=3,skill=0,equip=0),
 'scale':  dict(name='Honest Scale',niche='space_scale',length=10,avd=(2.5,3.5,5),h=(12,14,20),cap=4,narr=10,cash=20,rpm=(1.5,6),risk=4,skill=0.5,equip=0.5),
 'maps':   dict(name='The Moving Atlas',niche='history_maps',length=12,avd=(3,4.2,6),h=(8,10,14),cap=4,narr=12,cash=0,rpm=(2,8),risk=3.5,skill=0,equip=0),
 'english':dict(name='Story Steps English',niche='language_ci',length=12,avd=(3,4.8,6.6),h=(4,5,8),cap=8,narr=10,cash=0,rpm=(0.3,1.5),risk=3,skill=0,equip=0),
 'folklore':dict(name='Thrice-Nine Tales',niche='myth_folklore',length=15,avd=(3.5,5.2,7.5),h=(12,16,25),cap=4,narr=15,cash=0,rpm=(1.5,5),risk=4,skill=0.5,equip=0),
 'machines':dict(name='Opened Up',niche='eng_howitworks',length=12,avd=(3,4.2,6),h=(30,35,60),cap=2,narr=12,cash=20,rpm=(2,8),risk=4.5,skill=0.5,equip=0.5),
 'study':  dict(name='Study music scenes',niche='study_music',length=120,avd=(10,30,60),h=(3,4,6),cap=8,narr=0,cash=22,rpm=(0.5,3),risk=1.5,skill=0,equip=0),
 'reddit': dict(name='Reddit stories',niche='reddit_stories',length=20,avd=(4,7,10),h=(1.5,2,3),cap=12,narr=20,cash=0,rpm=(1,4),risk=1,skill=0,equip=0),
}
W={'speed':.30,'cost':.20,'simplicity':.20,'efficiency':.20,'risk':.10}
def b_speed(r):   return 5 if r>=4 else 4 if r>=1.5 else 3 if r>=0.75 else 2 if r>=0.3 else 1
def b_cost(c):    return 5 if c<=10 else 4 if c<=50 else 3 if c<=150 else 2 if c<=300 else 1
def b_simple(h):  return 5 if h<=4 else 4 if h<=8 else 3 if h<=12 else 2 if h<=20 else 1
def b_eff(e):     return 5 if e>=5 else 4 if e>=1.5 else 3 if e>=0.5 else 2 if e>=0.15 else 1
def calc(c, avd_i=1, h_i=1, v_mult=1.0, rpm_free=False):
  m=M[c['niche']]
  if c.get('nomusic'): V,n=no_music(c['niche'])
  else: V,n=float(m['long_subs_lt10k_median'] or 0),int(m['long_subs_lt10k_n'])
  V*=v_mult
  h=c['h'][h_i]; K=max(1,min(c['cap'],math.floor(HOURS_BUDGET/h)))
  avd=c['avd'][avd_i]; vids=12*K
  need=THRESHOLD_H*60/(vids*avd)            # views per video needed for 8000 h in 12 months
  ratio=V/need if need else 0
  credits=K*c['narr']*EL_CREDITS_PER_MIN*EL_RETAKE; el=el_cost(credits); cash=el+c['cash']
  rpm=(c['rpm'][0]+c['rpm'][1])/2
  eff=(V/h) if rpm_free else V*rpm/1000/h   # $ (or views) per human hour, after the programme
  simple=max(1,b_simple(h)-c['skill']-c['equip'])
  s={'speed':b_speed(ratio),'cost':b_cost(cash),'simplicity':simple,'efficiency':(b_eff(eff) if not rpm_free else (5 if eff>=2000 else 4 if eff>=500 else 3 if eff>=150 else 2 if eff>=50 else 1)),'risk':c['risk']}
  return dict(V=V,n=n,K=K,h=h,avd=avd,need=need,ratio=ratio,el=el,cash=cash,eff=eff,s=s)
def total(s,w=W): return sum(s[k]*v for k,v in w.items())/sum(w.values())
rows=[]
for cid,c in C.items():
  r=calc(c); gate=c['risk']<=1.5; var=c.get('variant',False)
  rows.append(dict(concept_id=cid,working_name=c['name'],niche_sample=c['niche'],
    v_basis=('no-music titles' if c.get('nomusic') else 'all titles'),in_subs_lt10k_n=r['n'],in_subs_lt10k_median_views=int(r['V']),conf=('medium' if r['n']>=20 else 'low'),
    as_length_min=c['length'],as_avg_view_min=f"{c['avd'][0]:g}/{c['avd'][1]:g}/{c['avd'][2]:g}",as_human_h_per_video=f"{c['h'][0]:g}/{c['h'][1]:g}/{c['h'][2]:g}",
    videos_per_month=r['K'],views_needed_per_video_8000h_12m=round(r['need']),ratio_observed_to_needed=round(r['ratio'],2),
    narration_min_per_video=c['narr'],elevenlabs_usd_month=r['el'],other_cash_usd_month=c['cash'],cash_usd_month=r['cash'],
    rpm_usd=f"{c['rpm'][0]:g}-{c['rpm'][1]:g}",usd_per_human_hour_after_programme=round(r['eff'],2),
    speed=r['s']['speed'],cost=r['s']['cost'],simplicity=r['s']['simplicity'],efficiency=r['s']['efficiency'],risk=c['risk'],
    weighted_total=round(total(r['s']),2),risk_gate=('excluded' if gate else 'pass'),variant_of=('sleep' if var else '')))
rows.sort(key=lambda r:(r['risk_gate']!='pass' or bool(r['variant_of']),-r['weighted_total']))
k=0
for r in rows:
  if r['risk_gate']=='pass' and not r['variant_of']: k+=1; r['rank']=k
  else: r['rank']=''
fields=['rank']+[k for k in rows[0] if k!='rank']
with open(os.path.join(D,'scores.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
for r in rows: print(r['rank'],r['working_name'],r['weighted_total'],'| sp',r['speed'],'co',r['cost'],'si',r['simplicity'],'ef',r['efficiency'],'ri',r['risk'],'| V',r['in_subs_lt10k_median_views'],'n',r['in_subs_lt10k_n'],'K',r['videos_per_month'],'need',r['views_needed_per_video_8000h_12m'],'ratio',r['ratio_observed_to_needed'],'cash',r['cash_usd_month'],'el',r['elevenlabs_usd_month'],'eff',r['usd_per_human_hour_after_programme'],r['risk_gate'])
# sensitivity
alts={'equal four, no risk':{'speed':1,'cost':1,'simplicity':1,'efficiency':1},
      'speed 50%':{'speed':.5,'cost':.15,'simplicity':.15,'efficiency':.1,'risk':.1},
      'efficiency 40%':{'speed':.2,'cost':.15,'simplicity':.15,'efficiency':.4,'risk':.1},
      'risk 25%':{'speed':.25,'cost':.15,'simplicity':.15,'efficiency':.2,'risk':.25}}
def rank_with(fn):
  out=[]
  for cid,c in C.items():
    if c['risk']<=1.5 or c.get('variant'): continue
    out.append((fn(c),c['name']))
  out.sort(reverse=True); return ' > '.join(f"{n} {v:.2f}" for v,n in out[:6])
for n,ww in alts.items(): print('W',n,'|',rank_with(lambda c: total(calc(c)['s'],ww)))
print('A low avd/high hours |',rank_with(lambda c: total(calc(c,avd_i=0,h_i=2)['s'])))
print('A high avd/low hours |',rank_with(lambda c: total(calc(c,avd_i=2,h_i=0)['s'])))
print('A views x0.25 |',rank_with(lambda c: total(calc(c,v_mult=0.25)['s'])))
print('A rpm-free efficiency |',rank_with(lambda c: total(calc(c,rpm_free=True)['s'])))
```

## 12. Сценарии первого года

`economics.py` пишет `data/economics.csv`.

```python
"""Year-one scenarios for the four leading concepts of ranking v2, per budget level.
All inputs are research assumptions, not forecasts. Writes docs/market-research/data/economics.csv."""
import csv, os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','docs','market-research','data','economics.csv')
H=8000; SUBS=1000; AFTER=0.25; SUB_RATE=(0.005,0.015)
# per level: (long videos per month, human hours per month, cash $ per month)
C={
 'hearth': dict(name='Boreal Hearth',avd=(10,50),views={'low':100,'mid':2400,'high':20000},rpm=(0.5,3),one_off=(0,150),
   lv={'L1':(4,24,10),'L2':(6,36,10),'L3':(6,36,20)}),
 'sleep':  dict(name='Lantern Library',avd=(10,40),views={'low':100,'mid':3000,'high':20000},rpm=(1.5,5),one_off=(0,0),
   lv={'L1':(1,10,35),'L2':(3,30,99),'L3':(4,40,130)}),
 'sim':    dict(name='Sandbox Trials',avd=(3,6.6),views={'low':300,'mid':3800,'high':20000},rpm=(1,4),one_off=(0,0),
   lv={'L1':(1,20,0),'L2':(2,46,0),'L3':(3,69,0)}),
 'field':  dict(name='Taiga Hours',avd=(10,50),views={'low':100,'mid':3000,'high':20000},rpm=(0.5,3),one_off=(500,900),
   lv={'L1':(1,14,50),'L2':(3,42,110),'L3':(4,56,150)}),
}
rows=[]
for cid,c in C.items():
  for lvl,(pm,hours,cash) in c['lv'].items():
    for sc,v in c['views'].items():
      vids=pm*12; views=vids*v
      hl,hh=views*c['avd'][0]/60, views*c['avd'][1]/60
      sl,sh=views*SUB_RATE[0], views*SUB_RATE[1]
      st='likely' if (hl>=H and sl>=SUBS) else ('possible' if (hh>=H and sh>=SUBS) else 'no')
      rlo=views*AFTER/1000*c['rpm'][0] if st=='likely' else 0
      rhi=views*AFTER/1000*c['rpm'][1] if st!='no' else 0
      clo=cash*12+c['one_off'][0]; chi=cash*12+c['one_off'][1]
      rows.append({'concept':c['name'],'budget_level':lvl,'scenario':sc,'long_videos_per_month':pm,'human_hours_per_month':hours,
        'cash_usd_per_month':cash,'one_off_usd':f"{c['one_off'][0]}-{c['one_off'][1]}",'views_per_video_12m':v,'views_year1':views,
        'avg_view_minutes':f"{c['avd'][0]:g}-{c['avd'][1]:g}",'watch_hours_year1':f"{hl:.0f}-{hh:.0f}",'subscribers_year1':f"{sl:.0f}-{sh:.0f}",
        'threshold_8000h_1000subs_year1':st,'rpm_usd':f"{c['rpm'][0]:g}-{c['rpm'][1]:g}",
        'ad_revenue_year1_usd_payee_in_programme_country':f"{rlo:.0f}-{rhi:.0f}",'ad_revenue_year1_usd_payee_russia':0,
        'direct_costs_year1_usd':f"{clo:.0f}-{chi:.0f}",
        'result_year1_usd_payee_in_programme_country_before_tax':f"{rlo-chi:.0f} to {rhi-clo:.0f}"})
with open(OUT,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
  if r['scenario']!='low': print(r['concept'][:15].ljust(15),r['budget_level'],r['scenario'],r['long_videos_per_month'],r['watch_hours_year1'],r['subscribers_year1'],r['threshold_8000h_1000subs_year1'],r['ad_revenue_year1_usd_payee_in_programme_country'],r['direct_costs_year1_usd'],r['result_year1_usd_payee_in_programme_country_before_tax'])
```
