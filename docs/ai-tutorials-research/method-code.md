# Приложение: код сбора и расчётов

Код, которым собраны данные и посчитаны таблицы. Приведён для проверки и повторения; в проект как программа не сохраняется. Запуск: Python 3.14, пакеты `yt-dlp==2026.08.19`, `pytrends`, `pillow`. Скрипты лежали в `tmp/scripts/`, сырые ответы — в `tmp/research/raw/`, таблицы — в `tmp/research/out/`; оттуда скопированы в [data](data/).

Порядок: запросы (1), сбор поиска и каналов (2), Trends (3), подсказки (4), таблицы (5), точные даты и превью (6), затем повторный запуск таблиц (5).

Известные особенности:

- Сбор каналов запускался партиями по 200 (`collect.py 200`): процесс без партий рос в памяти, и системный сторож памяти его останавливал. На данные это не влияет: скрипт продолжает с места остановки.
- Темп «видео в месяц» для каналов, у которых все 30 видео моложе 7 дней, считается на 7 дней и даёт 130,5: это массовые каналы.
- Разметка превью сделана вручную; её кода нет.

## 1. Сегменты и запросы

Файл `segments.json`.

```json
[
 {"id":"en_beginner","lang":"en","gl":"US","kind":"lesson","group":"beginner","q":["chatgpt tutorial for beginners","how to use ai for beginners"]},
 {"id":"en_assistants","lang":"en","gl":"US","kind":"lesson","group":"beginner","q":["claude ai tutorial","gemini tutorial"]},
 {"id":"en_prompting","lang":"en","gl":"US","kind":"lesson","group":"beginner","q":["prompt engineering tutorial","chatgpt prompts tutorial"]},
 {"id":"en_office","lang":"en","gl":"US","kind":"lesson","group":"professional","q":["chatgpt excel tutorial","ai for data analysis tutorial"]},
 {"id":"en_coding","lang":"en","gl":"US","kind":"lesson","group":"professional","q":["ai coding tutorial","claude code tutorial"]},
 {"id":"en_marketing","lang":"en","gl":"US","kind":"lesson","group":"professional","q":["ai for marketing tutorial","chatgpt for content creation"]},
 {"id":"en_image","lang":"en","gl":"US","kind":"lesson","group":"creative","q":["midjourney tutorial","ai image generator tutorial"]},
 {"id":"en_video","lang":"en","gl":"US","kind":"lesson","group":"creative","q":["ai video generator tutorial","ai video editing tutorial"]},
 {"id":"en_automation","lang":"en","gl":"US","kind":"lesson","group":"automation","q":["n8n tutorial","make.com ai automation tutorial"]},
 {"id":"en_agents","lang":"en","gl":"US","kind":"lesson","group":"automation","q":["ai agents tutorial","build ai agent tutorial"]},
 {"id":"en_local","lang":"en","gl":"US","kind":"lesson","group":"automation","q":["ollama tutorial","run llm locally tutorial"]},
 {"id":"en_business","lang":"en","gl":"US","kind":"lesson","group":"work_business","q":["ai for small business","chatgpt for business tutorial"]},
 {"id":"en_work","lang":"en","gl":"US","kind":"lesson","group":"work_business","q":["how to use ai at work","ai for job search"]},
 {"id":"en_teachers_students","lang":"en","gl":"US","kind":"lesson","group":"audience","q":["ai for teachers","notebooklm tutorial"]},
 {"id":"en_seniors","lang":"en","gl":"US","kind":"lesson","group":"audience","q":["ai for seniors","chatgpt for seniors"]},
 {"id":"en_money","lang":"en","gl":"US","kind":"hype","group":"money","q":["make money with ai","ai side hustle"]},
 {"id":"en_news","lang":"en","gl":"US","kind":"news","group":"news","q":["ai news this week","ai news today"]},
 {"id":"en_reviews","lang":"en","gl":"US","kind":"review","group":"reviews_lists","q":["best ai tools","ai tools review"]},
 {"id":"ru_beginner","lang":"ru","gl":"RU","kind":"lesson","group":"beginner","q":["нейросети для начинающих","как пользоваться chatgpt"]},
 {"id":"ru_access","lang":"ru","gl":"RU","kind":"lesson","group":"beginner","q":["chatgpt в россии","нейросети без vpn"]},
 {"id":"ru_work","lang":"ru","gl":"RU","kind":"lesson","group":"professional","q":["нейросети для работы","нейросеть для excel"]},
 {"id":"ru_coding","lang":"ru","gl":"RU","kind":"lesson","group":"professional","q":["нейросеть для программирования","cursor ai уроки"]},
 {"id":"ru_image","lang":"ru","gl":"RU","kind":"lesson","group":"creative","q":["нейросеть для создания картинок","midjourney урок"]},
 {"id":"ru_video","lang":"ru","gl":"RU","kind":"lesson","group":"creative","q":["нейросеть для видео","как сделать видео нейросетью"]},
 {"id":"ru_automation","lang":"ru","gl":"RU","kind":"lesson","group":"automation","q":["n8n уроки","ии агент как создать"]},
 {"id":"ru_business","lang":"ru","gl":"RU","kind":"lesson","group":"work_business","q":["нейросети для бизнеса","нейросети для маркетинга"]},
 {"id":"ru_students","lang":"ru","gl":"RU","kind":"lesson","group":"audience","q":["нейросети для учебы","нейросеть для студентов"]},
 {"id":"ru_money","lang":"ru","gl":"RU","kind":"hype","group":"money","q":["заработок на нейросетях","как заработать с помощью нейросетей"]},
 {"id":"ru_news","lang":"ru","gl":"RU","kind":"news","group":"news","q":["новости нейросетей","новости ии"]},
 {"id":"ru_reviews","lang":"ru","gl":"RU","kind":"review","group":"reviews_lists","q":["лучшие нейросети","обзор нейросетей"]}
]
```

## 2. Сбор поиска и каналов (yt-dlp, страница «О канале»)

Файл `collect.py`.

```python
"""Collect public YouTube search samples (two passes) and channel listings + about pages.
Run: tmp/venv/bin/python -I tmp/scripts/collect.py  (writes tmp/research/raw/)"""
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

## 3. Google Trends

Файл `trends.py`.

```python
"""Google Trends, weekly, 5 years. Each batch has its own anchor; levels compare only inside a batch,
growth ratios are per term and do not depend on the anchor. Writes tmp/research/raw/trends.json"""
import json, time, os, datetime
from pytrends.request import TrendReq
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'..','research','raw','trends.json')
B=[
 ('US','youtube',['documentary','chatgpt','ai tutorial','ai news','ai tools']),
 ('US','youtube',['chatgpt tutorial','n8n','ai agent','claude code','midjourney']),
 ('US','youtube',['chatgpt tutorial','ai video','prompt engineering','notebooklm','ollama']),
 ('US','youtube',['chatgpt tutorial','make money with ai','ai for beginners','gemini','cursor ai']),
 ('RU','youtube',['нейросеть','chatgpt','нейросети','n8n','midjourney']),
 ('RU','youtube',['нейросеть','нейросеть для видео','заработок на нейросетях','deepseek','гигачат']),
 ('RU','',['нейросеть','chatgpt','n8n','нейросеть для видео','deepseek']),
 ('RU','',['youtube','rutube','вк видео','дзен']),
]
R=json.load(open(OUT)) if os.path.exists(OUT) else {}
py=TrendReq(hl='en-US',tz=0,timeout=(10,30))
for geo,gp,kw in B:
  key=f"{geo}|{gp or 'web'}|{'|'.join(kw)}"
  if key in R: continue
  for a in range(4):
    try:
      py.build_payload(kw,timeframe='today 5-y',geo=geo,gprop=gp)
      df=py.interest_over_time()
      R[key]={'geo':geo,'property':gp or 'web','terms':kw,'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
              'weeks':[d.strftime('%Y-%m-%d') for d in df.index],'values':{k:[int(x) for x in df[k]] for k in kw}}
      print('ok',key,len(df),flush=True); break
    except Exception as ex:
      print('err',key,repr(ex)[:200],flush=True); time.sleep(60*(a+1))
  json.dump(R,open(OUT,'w'),ensure_ascii=False); time.sleep(20)
print('done',len(R))
```

## 4. Подсказки поиска YouTube

Файл `suggest.py`.

```python
"""YouTube search autocomplete (public endpoint) for seed phrases. Writes tmp/research/raw/suggest.json"""
import json, os, urllib.request, urllib.parse, time, datetime
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'..','research','raw','suggest.json')
SEEDS=[('en','US',s) for s in ['how to use chatgpt for','how to use ai for','ai for','chatgpt for','claude for','n8n','ai agent for','ai tutorial','ai video','how to use ai to']]+\
      [('ru','RU',s) for s in ['нейросеть для','как использовать нейросеть для','нейросети для','chatgpt для','как сделать в нейросети','n8n','ии агент']]
R={}
for hl,gl,s in SEEDS:
  u='https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&hl=%s&gl=%s&q=%s'%(hl,gl,urllib.parse.quote(s))
  t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode('utf-8','replace')
  j=json.loads(t[t.index('(')+1:t.rindex(')')])
  R[f'{hl}|{s}']={'hl':hl,'gl':gl,'seed':s,'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),'suggestions':[x[0] for x in j[1]]}
  time.sleep(1)
json.dump(R,open(OUT,'w'),ensure_ascii=False,indent=0)
for k,v in R.items(): print(k,'=>','; '.join(v['suggestions']))
```

## 5. Таблицы и метрики

Файл `analyze.py`.

```python
"""Build CSVs from tmp/research/raw/{search,channels,trends}.json into tmp/research/out/.
Run: tmp/venv/bin/python -I tmp/scripts/analyze.py"""
import json, os, re, csv, statistics as st, datetime as dt
from collections import defaultdict, Counter
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'..','research','raw'); OUT=os.path.join(HERE,'..','research','out')
os.makedirs(OUT,exist_ok=True)
SEG={s['id']:s for s in json.load(open(os.path.join(HERE,'segments.json')))}
S=json.load(open(os.path.join(RAW,'search.json'))); C=json.load(open(os.path.join(RAW,'channels.json')))
def ts(x): return dt.datetime.fromisoformat(x)
def med(a): a=[x for x in a if x is not None]; return round(st.median(a)) if a else ''
def pct(a,q):
  a=sorted(x for x in a if x is not None)
  return a[min(len(a)-1,int(q*(len(a)-1)+0.5))] if a else ''
def num(s):
  if not s: return None
  m=re.match(r'([\d.,]+)\s*([KMB]?)',s.replace(',','') if 'K' not in s and 'M' not in s else s)
  if not m: return None
  v=float(m.group(1).replace(',','')); return int(v*{'':1,'K':1e3,'M':1e6,'B':1e9}[m.group(2)])
def joined(s):
  try: return dt.datetime.strptime(s,'%b %d, %Y').date()
  except Exception: return None
CLS=[('news',r'\bnews\b|this week|\btoday\b|\bupdates?\b|released|just (dropped|launched)|announc|новост|вышл|релиз|обновлен'),
     ('money',r'make money|\$\s?\d|side hustle|passive income|\bearn|заработ|доход|миллион'),
     ('review',r'\bbest\b|\btop\s?\d|\d+\s+(free\s+)?(ai|new)\s+(tools|apps|websites)|\breview|\bvs\.?\b|versus|compar|\btested\b|i tried|ranking|обзор|лучш|\bтоп|сравн|протестир'),
     ('lesson',r'tutorial|how to|course|guide|step[- ]by[- ]step|beginner|\blearn|masterclass|walkthrough|\bbuild|set ?up|explained|урок|\bкак\b|курс|гайд|инструкц|пошагов|начинающ|настро|созда|обучени|научи')]
def tclass(t):
  t=(t or '').lower()
  for k,p in CLS:
    if re.search(p,t): return k
  return 'other'
DATED=r'20(2[4-7])|gpt[- ]?\d|gemini\s?\d|claude\s?\d|(opus|sonnet|haiku)\s?\d|veo\s?\d|sora\s?\d|midjourney\s?v?\d|kling\s?\d|\bv\d|\bnew\b|нов'
# channels
CH={}
for cid,c in C.items():
  if 'error' in c and 'videos' not in c: continue
  a=c.get('about') or {}; m=ts(c['measured'])
  vids=[v for v in c.get('videos') or [] if v.get('id')]
  ages=[(m.timestamp()-v['timestamp'])/86400 for v in vids if v.get('timestamp')]
  views=[v.get('view_count') for v in vids]
  old=[v.get('view_count') for v in vids if v.get('timestamp') and (m.timestamp()-v['timestamp'])/86400>=30]
  j=joined(a.get('joined'))
  agem=round((m.date()-j).days/30.44,1) if j else ''
  subs=c.get('subs') if c.get('subs') is not None else num(a.get('subs_text'))
  n90=sum(1 for x in ages if x<=90)
  span=max(ages) if ages else 0
  per_month=round(n90/3,1) if span>90 else (round(len(ages)/max(span,7)*30.44,1) if ages else '')
  CH[cid]={'channel_id':cid,'channel_url':f'https://www.youtube.com/channel/{cid}','channel':c.get('channel') or '','handle':a.get('handle') or '',
    'country':a.get('country') or '','subs':subs if subs is not None else '','total_views':num(a.get('total_views')) or '',
    'video_count_all':num(a.get('video_count')) or '','joined':j.isoformat() if j else '','channel_age_months':agem,
    'listed_long_videos':len(vids),'median_views_listed':med(views),'median_views_listed_age_ge30d':med(old),
    'long_uploads_per_month':per_month,'first_listed_upload':(dt.datetime.fromtimestamp(min(v['timestamp'] for v in vids if v.get('timestamp')),dt.timezone.utc).date().isoformat() if len(vids)<30 and any(v.get('timestamp') for v in vids) else ''),
    'measured_utc':c['measured']}
def size(s):
  if s=='' or s is None: return 'unknown'
  return 'lt10k' if s<10000 else ('10k_100k' if s<100000 else 'ge100k')
def isnew(ch): return ch and ch['channel_age_months']!='' and ch['channel_age_months']<12
# videos
V=[]; seen=set()
for key,v in S.items():
  if not isinstance(v['results'],list): continue
  m=ts(v['measured'])
  for rank,e in enumerate(v['results'],1):
    ch=CH.get(e.get('channel_id'),{})
    age=round((m.timestamp()-e['timestamp'])/86400) if e.get('timestamp') else ''
    cm=ch.get('median_views_listed_age_ge30d') or ch.get('median_views_listed')
    V.append({'segment':v['segment'],'lang':v['lang'],'query':v['query'],'pass':v['pass'],'rank':rank,'measured_utc':v['measured'],
      'video_id':e['id'],'url':f"https://www.youtube.com/watch?v={e['id']}",'title':e.get('title') or '','channel':e.get('channel') or ch.get('channel',''),
      'channel_id':e.get('channel_id') or '','channel_url':f"https://www.youtube.com/channel/{e.get('channel_id')}" if e.get('channel_id') else '',
      'views':e.get('view_count') if e.get('view_count') is not None else '','duration_s':e.get('duration') or '',
      'approx_upload_date':dt.datetime.fromtimestamp(e['timestamp'],dt.timezone.utc).date().isoformat() if e.get('timestamp') else '',
      'approx_age_days':age,'views_per_day':round(e['view_count']/max(age,1),1) if age!='' and e.get('view_count') is not None else '',
      'title_class':tclass(e.get('title')),'title_dated':int(bool(re.search(DATED,(e.get('title') or '').lower()))),
      'channel_subs':ch.get('subs',''),'channel_size':size(ch.get('subs')),'channel_joined':ch.get('joined',''),'channel_new_lt12m':int(bool(isnew(ch))),
      'channel_median_views':cm if cm is not None else '','views_vs_channel_median':round(e['view_count']/cm,2) if cm and e.get('view_count') is not None else ''})
def w(name,rows):
  with open(os.path.join(OUT,name),'w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
w('videos.csv',V)
segs_of=defaultdict(set)
for r in V: segs_of[r['channel_id']].add(r['segment'])
chrows=[]
for cid,ch in CH.items():
  r=dict(ch); r['size_class']=size(ch['subs']); r['new_lt12m']=int(bool(isnew(ch))); r['segments']=';'.join(sorted(segs_of.get(cid,[])))
  r['lang']=';'.join(sorted({SEG[s]['lang'] for s in segs_of.get(cid,[])})); chrows.append(r)
w('channels.csv',chrows)
# segment metrics
M=[]
for sid,s in SEG.items():
  mv=[r for r in V if r['segment']==sid and r['pass']=='month']
  av=[r for r in V if r['segment']==sid and r['pass']=='all']
  def dedup(rows):
    d={}
    for r in rows: d.setdefault(r['video_id'],r)
    return list(d.values())
  mv=dedup(mv); av=dedup(av)
  ml=[r for r in mv if r['duration_s']!='' and r['duration_s']>180 and r['approx_age_days']!='' and 7<=r['approx_age_days']<=30 and r['views']!='']
  ms=[r for r in mv if r['duration_s']!='' and r['duration_s']<=180 and r['approx_age_days']!='' and 7<=r['approx_age_days']<=30 and r['views']!='']
  g=lambda rows,sz:[r['views'] for r in rows if r['channel_size']==sz]
  al=[r for r in av if r['approx_age_days']!='']
  ages=[r['approx_age_days'] for r in al]
  chs=Counter(r['channel_id'] for r in mv+av)
  top3=sum(n for _,n in chs.most_common(3))
  allr=mv+av
  M.append({'segment':sid,'lang':s['lang'],'gl':s['gl'],'kind':s['kind'],'group':s['group'],'queries':' | '.join(s['q']),
    'measured_utc':max(r['measured_utc'] for r in allr) if allr else '',
    'month_long_7_30d_n':len(ml),'month_long_median':med([r['views'] for r in ml]),'month_long_p25':pct([r['views'] for r in ml],.25),'month_long_p75':pct([r['views'] for r in ml],.75),
    'month_long_lt10k_n':len(g(ml,'lt10k')),'month_long_lt10k_median':med(g(ml,'lt10k')),
    'month_long_10k_100k_n':len(g(ml,'10k_100k')),'month_long_10k_100k_median':med(g(ml,'10k_100k')),
    'month_long_ge100k_n':len(g(ml,'ge100k')),'month_long_ge100k_median':med(g(ml,'ge100k')),
    'month_long_new_channel_n':sum(1 for r in ml if r['channel_new_lt12m']),'month_long_new_channel_median':med([r['views'] for r in ml if r['channel_new_lt12m']]),
    'month_long_lt100k_ge10k_views':sum(1 for r in ml if r['channel_size'] in ('lt10k','10k_100k') and r['views']>=10000),
    'month_long_lt10k_ge1k_views':sum(1 for r in ml if r['channel_size']=='lt10k' and r['views']>=1000),
    'month_short_7_30d_n':len(ms),'month_short_median':med([r['views'] for r in ms]),
    'all_n':len(al),'all_median_age_days':med(ages),'all_share_age_lt180d':round(sum(1 for a in ages if a<180)/len(ages),2) if ages else '',
    'all_share_age_gt730d':round(sum(1 for a in ages if a>730)/len(ages),2) if ages else '',
    'all_median_views':med([r['views'] for r in al if r['views']!='']),'all_median_views_per_day':med([r['views_per_day'] for r in al if r['views_per_day']!='']),
    'all_share_channels_lt100k':round(sum(1 for r in al if r['channel_size'] in ('lt10k','10k_100k'))/len(al),2) if al else '',
    'share_title_lesson':round(sum(1 for r in allr if r['title_class']=='lesson')/len(allr),2) if allr else '',
    'share_title_news':round(sum(1 for r in allr if r['title_class']=='news')/len(allr),2) if allr else '',
    'share_title_review':round(sum(1 for r in allr if r['title_class']=='review')/len(allr),2) if allr else '',
    'share_title_money':round(sum(1 for r in allr if r['title_class']=='money')/len(allr),2) if allr else '',
    'share_title_dated':round(sum(r['title_dated'] for r in allr)/len(allr),2) if allr else '',
    'distinct_channels':len(chs),'top3_channels_share':round(top3/len(allr),2) if allr else '',
    'new_channels_lt12m':sum(1 for c in chs if isnew(CH.get(c))),
    'new_channels_lt12m_with_video_ge10k':sum(1 for c in chs if isnew(CH.get(c)) and any(r['views']!='' and r['views']>=10000 for r in allr if r['channel_id']==c))})
w('segment-metrics.csv',M)
# examples
E=[]
def ex(sid,role,r,note):
  ch=CH.get(r['channel_id'],{})
  E.append({'segment':sid,'role':role,'url':r['url'],'title':r['title'],'views':r['views'],'approx_upload_date':r['approx_upload_date'],'approx_age_days':r['approx_age_days'],
    'channel':r['channel'],'channel_url':r['channel_url'],'channel_subs':r['channel_subs'],'channel_joined':r['channel_joined'],
    'channel_median_views':r['channel_median_views'],'views_vs_channel_median':r['views_vs_channel_median'],'long_uploads_per_month':ch.get('long_uploads_per_month',''),
    'measured_utc':r['measured_utc'],'note':note})
for sid in SEG:
  rows={}
  for r in V:
    if r['segment']==sid and r['views']!='': rows.setdefault(r['video_id'],r)
  rows=list(rows.values())
  if not rows: continue
  ex(sid,'leader',max(rows,key=lambda r:r['views']),'most viewed video in segment sample (both passes)')
  ml=sorted([r for r in rows if r['pass']=='month' and r['duration_s']!='' and r['duration_s']>180 and r['approx_age_days']!='' and 7<=r['approx_age_days']<=30],key=lambda r:r['views'])
  if ml: ex(sid,'ordinary',ml[len(ml)//2],'median long video aged 7-30 days')
  sm=[r for r in rows if r['channel_size']=='lt10k']
  if sm: ex(sid,'small_breakout',max(sm,key=lambda r:r['views']),'best video from a channel under 10k subscribers')
  nw=[r for r in rows if r['channel_new_lt12m']]
  if nw: ex(sid,'new_channel',max(nw,key=lambda r:r['views']),'best video from a channel that joined under 12 months ago')
  so=[r for r in rows if r['channel_size']=='lt10k' and CH.get(r['channel_id'],{}).get('channel_age_months') not in ('',None) and CH[r['channel_id']]['channel_age_months']>=36]
  if so: ex(sid,'small_old',max(so,key=lambda r:r['views']),'channel under 10k subscribers that joined 3+ years ago: small is not new')
  st_=[r for r in rows if CH.get(r['channel_id']) and CH[r['channel_id']]['listed_long_videos']>=10 and CH[r['channel_id']]['median_views_listed']!='' and CH[r['channel_id']]['median_views_listed']<1000 and CH[r['channel_id']]['long_uploads_per_month'] not in ('',None) and CH[r['channel_id']]['long_uploads_per_month']>=2]
  for r in sorted({r['channel_id']:r for r in st_}.values(),key=lambda r:CH[r['channel_id']]['median_views_listed'])[:2]:
    ex(sid,'struggling',r,'channel posting 2+ long videos a month with typical video under 1,000 views')
w('examples.csv',E)
# trends
T=[]; TR=json.load(open(os.path.join(RAW,'trends.json'))) if os.path.exists(os.path.join(RAW,'trends.json')) else {}
for key,b in TR.items():
  wk=b['weeks']; anchor=b['terms'][0]
  for t in b['terms']:
    x=b['values'][t]; last=x[-52:]; prev=x[-104:-52]; old=x[-156:-104]
    mean=lambda a:sum(a)/len(a) if a else 0
    al=mean(b['values'][anchor][-52:])
    bym=defaultdict(list)
    for d,val in zip(wk,x): bym[int(d[5:7])].append(val)
    mm={k:mean(v) for k,v in bym.items()}; avg=mean(list(mm.values()))
    T.append({'term':t,'geo':b['geo'],'property':'YouTube Search' if b['property']=='youtube' else 'Web Search','batch_anchor':anchor,'window':f"{wk[0]}..{wk[-1]} weekly",
      'level_vs_anchor_52w':round(mean(last)/al,2) if al else '','change_52w_vs_prev_52w':round(mean(last)/mean(prev),2) if mean(prev) else '',
      'change_52w_vs_2y_before':round(mean(last)/mean(old),2) if mean(old) else '','peak_week':wk[x.index(max(x))],'last_4w_vs_52w_mean':round(mean(x[-4:])/mean(last),2) if mean(last) else '',
      'zero_weeks':sum(1 for v in x if v==0),'measured_utc':b['measured']})
if T: w('trends.csv',T)
print('videos',len(V),'channels',len(chrows),'segments',len(M),'examples',len(E),'trends',len(T))
# suggestions
SG=json.load(open(os.path.join(RAW,'suggest.json'))) if os.path.exists(os.path.join(RAW,'suggest.json')) else {}
rows=[{'lang':v['hl'],'gl':v['gl'],'seed':v['seed'],'rank':i,'suggestion':s,'measured_utc':v['measured']} for v in SG.values() for i,s in enumerate(v['suggestions'],1)]
if rows: w('suggestions.csv',rows)
# exact dates for examples (details.py output), vendor flag; rerun analyze.py after details.py
DP=os.path.join(RAW,'details.json')
if os.path.exists(DP):
  D=json.load(open(DP))
  VENDORS={'Claude','Google DeepMind','Manus AI','OpenAI','Google','Anthropic','Google for Developers','Microsoft','Gemini','Higgsfield AI'}
  for e in E:
    d=D.get(e['url'].split('v=')[1],{})
    e['exact_upload_date']=(d['upload_date'][:4]+'-'+d['upload_date'][4:6]+'-'+d['upload_date'][6:]) if d.get('upload_date') else ''
    e['exact_age_days']=(dt.datetime.fromisoformat(d['measured']).date()-dt.date.fromisoformat(e['exact_upload_date'])).days if e['exact_upload_date'] else ''
    e['views_at_detail']=d.get('view_count','') if d.get('view_count') is not None else ''
    e['detail_measured_utc']=d.get('measured','')
    e['vendor_channel']=int(e['channel'] in VENDORS)
  w('examples.csv',E)
```

## 6. Точные даты примеров и листы превью

Файл `details.py`.

```python
"""Exact upload dates for example videos (yt-dlp, no download) and thumbnail contact sheets.
Run after analyze.py: tmp/venv/bin/python -I tmp/scripts/details.py"""
import json, os, csv, io, urllib.request, concurrent.futures as cf, datetime
import yt_dlp
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__)); RAW=os.path.join(HERE,'..','research','raw'); OUT=os.path.join(HERE,'..','research','out')
E=list(csv.DictReader(open(os.path.join(OUT,'examples.csv'))))
P=os.path.join(RAW,'details.json'); D=json.load(open(P)) if os.path.exists(P) else {}
ids=sorted({e['url'].split('v=')[1] for e in E}-set(D))
def get(i):
  try:
    x=yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'skip_download':True}).extract_info(f'https://www.youtube.com/watch?v={i}',download=False,process=False)
    return i,{'upload_date':x.get('upload_date'),'view_count':x.get('view_count'),'like_count':x.get('like_count'),'comment_count':x.get('comment_count'),
      'duration':x.get('duration'),'measured':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
  except Exception as ex: return i,{'error':str(ex)[:300]}
with cf.ThreadPoolExecutor(4) as ex:
  for i,r in ex.map(get,ids): D[i]=r
json.dump(D,open(P,'w'))
print('details',len(D),sum('error' in v for v in D.values()))
# contact sheets: thumbnails of English and Russian lesson examples (leader, small_breakout, new_channel)
roles=('leader','small_breakout','new_channel')
for lang in ('en','ru'):
  sel=[e for e in E if e['segment'].startswith(lang+'_') and e['role'] in roles]
  W,H,cols=320,180,6; rows=(len(sel)+cols-1)//cols
  sheet=Image.new('RGB',(cols*W,rows*(H+18)),'white'); dr=ImageDraw.Draw(sheet)
  for k,e in enumerate(sel):
    vid=e['url'].split('v=')[1]
    try:
      im=Image.open(io.BytesIO(urllib.request.urlopen(f'https://i.ytimg.com/vi/{vid}/mqdefault.jpg',timeout=20).read())).convert('RGB').resize((W,H))
    except Exception: im=Image.new('RGB',(W,H),'grey')
    x,y=(k%cols)*W,(k//cols)*(H+18); sheet.paste(im,(x,y)); dr.text((x+3,y+H+2),f"{k+1} {e['segment']} {e['role']}"[:52],fill='black')
  sheet.save(os.path.join(OUT,f'thumbs-{lang}.jpg'),quality=80)
  with open(os.path.join(OUT,f'thumbs-{lang}.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['n','segment','role','url','channel'])
    for k,e in enumerate(sel): w.writerow([k+1,e['segment'],e['role'],e['url'],e['channel']])
  print('sheet',lang,len(sel))
```

