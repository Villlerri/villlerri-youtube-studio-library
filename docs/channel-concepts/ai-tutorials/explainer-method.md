# Метод: выдача YouTube по запросам «как устроен ИИ»

Для Villlerri. 2026-10-17. Данные для концепции «Countable AI».

## Что собрано

- 8 английских запросов: how ai works; how neural networks work; neural network explained; how chatgpt works; how large language models work; how ai image generators work; why does ai hallucinate; machine learning explained simply.
- Две выдачи на запрос: по релевантности и «за этот месяц». Регион US, язык en, без входа в аккаунт.
- Первые 30 видео каждой выдачи, без Shorts. Всего 480 строк, 422 разных видео.
- Время замера: 2026-10-17, 10:32–10:34 UTC выдачи, затем страницы видео.

## Как собрано

1. Выдача: yt-dlp, плоский список страницы поиска.
2. Каждое видео: yt-dlp, страница видео — дата, просмотры, длительность, канал, подписчики.
3. Подписчики каналов меньше 10 тыс. перепроверены по странице канала. Причина: страница видео иногда теряет приставку K или M. Пример: freeCodeCamp.org — 119 на странице видео, 11,9 млн на странице канала. Значение со страницы канала заменяет значение со страницы видео.
4. Сборка трёх таблиц одним скриптом; ниже его код.

8 видео из 422 недоступны («This video is not available»); их даты и подписчики пусты. Проверок «вы не робот» — 0. Платных вызовов — 0.

## Файлы

- data/explainer-videos.csv — одна строка на видео в выдаче: запрос, выдача, место, канал, подписчики, просмотры, дата, возраст в днях, длительность, время замера.
- data/explainer-metrics.csv — на выдачу: медиана и квартили просмотров, медиана возраста, доли свежих и старых видео, доли малых каналов, число прорывов малых каналов, разнообразие каналов. Строки ALL — по разным видео всех запросов.
- data/explainer-channels.csv — каналы из выдач по релевантности: сколько раз встречаются, в скольких запросах, медиана просмотров, последнее видео.

## Ограничения

- Выдача без входа и истории. Зритель с историей видит другое.
- Просмотры — накопленные на дату замера. Это не скорость роста.
- Подписчики YouTube округляет.
- 30 видео на выдачу — первая страница и чуть больше. Глубже не смотрели.

## Код

Повторный запуск из корня репозитория, с yt-dlp в tmp/venv-yt.

### Выдача
```python
"""Flat search listings: 8 queries x (relevance, this_month), first 30 videos. Resumes from tmp/explainer/listings.json."""
import json, os, time, datetime, urllib.parse
import yt_dlp
P='tmp/explainer/listings.json'
QS=["how ai works","how neural networks work","neural network explained","how chatgpt works","how large language models work","how ai image generators work","why does ai hallucinate","machine learning explained simply"]
SP={'relevance':'','this_month':'&sp=EgQIBBAB'}
L=json.load(open(P)) if os.path.exists(P) else {}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
for q in QS:
  for lst,sp in SP.items():
    k=f'{q}|{lst}'
    if k in L and 'error' not in L[k]: continue
    url=f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}{sp}&hl=en&gl=US"
    opts={'quiet':True,'no_warnings':True,'extract_flat':'in_playlist','playlistend':60,'skip_download':True,'socket_timeout':30,
          'extractor_args':{'youtubetab':{'approximate_date':['']}}}
    try:
      with yt_dlp.YoutubeDL(opts) as y: info=y.extract_info(url,download=False)
      vids=[]
      for e in info.get('entries') or []:
        i=e.get('id') or ''
        if len(i)!=11 or '/shorts/' in (e.get('url') or '') or e.get('ie_key') not in (None,'Youtube'): continue
        vids.append({k:e.get(k) for k in ('id','title','channel','channel_id','view_count','duration','url')})
        if len(vids)==30: break
      L[k]={'query':q,'listing':lst,'measured':now(),'results':vids}
      print(k,len(vids),flush=True)
    except Exception as ex:
      L[k]={'error':str(ex)[:300],'measured':now()}; print(k,'ERROR',str(ex)[:200],flush=True)
    json.dump(L,open(P,'w'),ensure_ascii=False); time.sleep(3)
```

### Страницы видео
```python
"""Per-video details, one yt-dlp call at a time, saved after every 10 videos; resumes from tmp/explainer/details.json.
Bot check on a video -> mark bot_blocked and skip. HTTP 429 -> stop."""
import json, os, time, datetime, sys
import yt_dlp
P='tmp/explainer/details.json'
L=json.load(open('tmp/explainer/listings.json'))
ids=sorted({e['id'] for v in L.values() for e in v['results']})
D=json.load(open(P)) if os.path.exists(P) else {}
F=('upload_date','view_count','duration','channel','channel_id','channel_follower_count')
n=0
for i in ids:
  if i in D and ('error' not in D[i] or D[i].get('bot_blocked')): continue
  try:
    with yt_dlp.YoutubeDL({'quiet':True,'no_warnings':True,'skip_download':True,'socket_timeout':30}) as y:
      x=y.extract_info(f'https://www.youtube.com/watch?v={i}',download=False,process=False)
    D[i]={k:x.get(k) for k in F}
  except Exception as ex:
    s=str(ex)
    if '429' in s or 'Too Many Requests' in s:
      json.dump(D,open(P,'w')); print('HTTP 429, stop:',s[:200]); sys.exit(2)
    D[i]={'error':s[:300],'bot_blocked':'Sign in to confirm' in s}
  D[i]['measured']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
  n+=1
  if n%10==0: json.dump(D,open(P,'w')); print(n,len(D),flush=True)
  time.sleep(0.5)
json.dump(D,open(P,'w'))
print('done',len(D),'errors',sum('error' in v for v in D.values()),'bot',sum(bool(v.get('bot_blocked')) for v in D.values()))
```

### Подписчики со страницы канала
```bash
#!/bin/bash
# Channel-page subscriber counts for suspect channels; one yt-dlp process per channel; resumable.
cd /srv/projects/youtube-studio-library/worktrees/youtube-2-work
out=tmp/explainer/chsubs.tsv; touch "$out"
while read -r c; do
  grep -q "^$c	" "$out" && continue
  v=$(timeout 90 tmp/venv-yt/bin/yt-dlp --flat-playlist --playlist-end 1 -J "https://www.youtube.com/channel/$c/videos" 2>/dev/null | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(d.get('channel_follower_count'))" 2>/dev/null)
  printf '%s\t%s\t%s\n' "$c" "${v:-ERR}" "$(date -u +%FT%TZ)" >> "$out"
  sleep 1
done < tmp/explainer/suspect.txt
echo done $(wc -l < "$out")
```

### Сборка таблиц
```python
"""Build the three CSVs from tmp/explainer/listings.json + details.json."""
import json, csv, datetime, statistics as st, collections
D='docs/channel-concepts/ai-tutorials/data/'
L=json.load(open('tmp/explainer/listings.json')); T=json.load(open('tmp/explainer/details.json'))
QS=["how ai works","how neural networks work","neural network explained","how chatgpt works","how large language models work","how ai image generators work","why does ai hallucinate","machine learning explained simply"]
# channel-page counts override video-page counts under 10k (video page sometimes drops the K/M suffix)
import os
CS={l.split('\t')[0]:l.split('\t')[1] for l in open('tmp/explainer/chsubs.tsv').read().splitlines()} if os.path.exists('tmp/explainer/chsubs.tsv') else {}
def subs(cid,v):
  c=CS.get(cid)
  return int(c) if c and c not in ('ERR','None') else v
today=datetime.datetime.now(datetime.timezone.utc).date()
def iso(d): return f'{d[:4]}-{d[4:6]}-{d[6:]}' if d else ''
rows=[]
for q in QS:
  for lst in ('relevance','this_month'):
    for r,e in enumerate(L[f'{q}|{lst}']['results'],1):
      d=T[e['id']]; ok='error' not in d
      ud=d.get('upload_date') if ok else None
      age=(today-datetime.datetime.strptime(ud,'%Y%m%d').date()).days if ud else ''
      rows.append(dict(query=q,listing=lst,rank=r,video_id=e['id'],title=e['title'],
        channel=(d.get('channel') if ok else None) or e.get('channel') or '',
        channel_id=(d.get('channel_id') if ok else None) or e.get('channel_id') or '',
        channel_subs=subs((d.get('channel_id') if ok else None) or e.get('channel_id') or '',d.get('channel_follower_count') if ok and d.get('channel_follower_count') is not None else ''),
        views=(d.get('view_count') if ok else None) if ok and d.get('view_count') is not None else (e.get('view_count') if e.get('view_count') is not None else ''),
        upload_date=iso(ud) if ud else '',age_days=age,
        duration_s=(d.get('duration') if ok and d.get('duration') is not None else e.get('duration')) or '',
        measured_utc=d['measured'],bot_blocked=int(not ok and bool(d.get('bot_blocked')))))
cols=['query','listing','rank','video_id','title','channel','channel_id','channel_subs','views','upload_date','age_days','duration_s','measured_utc']
with open(D+'explainer-videos.csv','w',newline='') as f:
  w=csv.DictWriter(f,cols,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def pct(v,p):
  v=sorted(v); k=(len(v)-1)*p; a=int(k); b=min(a+1,len(v)-1); return v[a]+(v[b]-v[a])*(k-a)
def share(v,f): return round(sum(map(f,v))/len(v),3) if v else ''
def metrics(q,lst,rs):
  num=lambda k:[float(r[k]) for r in rs if r[k]!='']
  vw,ag,sb,du=num('views'),num('age_days'),num('channel_subs'),num('duration_s')
  ch=collections.Counter(r['channel_id'] or r['channel'] for r in rs)
  g=lambda v,f:round(f(v),1) if v else ''
  return dict(query=q,listing=lst,n=len(rs),views_median=g(vw,st.median),views_p25=g(vw,lambda v:pct(v,.25)),views_p75=g(vw,lambda v:pct(v,.75)),
    age_days_median=g(ag,st.median),share_age_lt180d=share(ag,lambda a:a<180),share_age_gt730d=share(ag,lambda a:a>730),
    share_subs_lt100k=share(sb,lambda s:s<1e5),share_subs_lt10k=share(sb,lambda s:s<1e4),
    n_lt10k_ge10k_views=sum(1 for r in rs if r['channel_subs']!='' and r['views']!='' and float(r['channel_subs'])<1e4 and float(r['views'])>=1e4),
    n_lt100k_ge100k_views=sum(1 for r in rs if r['channel_subs']!='' and r['views']!='' and float(r['channel_subs'])<1e5 and float(r['views'])>=1e5),
    distinct_channels=len(ch),top3_channels_share_of_videos=round(sum(c for _,c in ch.most_common(3))/len(rs),3),
    duration_median_min=round(st.median(du)/60,2) if du else '',n_bot_blocked=sum(r['bot_blocked'] for r in rs))
mc=['query','listing','n','views_median','views_p25','views_p75','age_days_median','share_age_lt180d','share_age_gt730d','share_subs_lt100k','share_subs_lt10k','n_lt10k_ge10k_views','n_lt100k_ge100k_views','distinct_channels','top3_channels_share_of_videos','duration_median_min','n_bot_blocked']
M=[metrics(q,l,[r for r in rows if r['query']==q and r['listing']==l]) for q in QS for l in ('relevance','this_month')]
for l in ('relevance','this_month'):
  seen={}
  for r in rows:
    if r['listing']==l: seen.setdefault(r['video_id'],r)
  M.append(metrics('ALL',l,list(seen.values())))
with open(D+'explainer-metrics.csv','w',newline='') as f:
  w=csv.DictWriter(f,mc); w.writeheader(); w.writerows(M)
# channels in relevance listings
C=collections.defaultdict(lambda:dict(names=collections.Counter(),subs=None,app=0,qs=set(),vids={},newest=''))
for r in rows:
  if r['listing']!='relevance': continue
  c=C[r['channel_id'] or r['channel']]; c['names'][r['channel']]+=1; c['app']+=1; c['qs'].add(r['query'])
  if r['channel_subs']!='': c['subs']=int(r['channel_subs'])
  if r['views']!='': c['vids'][r['video_id']]=float(r['views'])
  c['newest']=max(c['newest'],r['upload_date'])
out=[dict(channel=c['names'].most_common(1)[0][0],channel_id=k if k.startswith('UC') else '',subs='' if c['subs'] is None else c['subs'],appearances=c['app'],
  queries_count=len(c['qs']),median_views_of_its_videos=round(st.median(c['vids'].values())) if c['vids'] else '',newest_upload_date=c['newest']) for k,c in C.items()]
out.sort(key=lambda r:-r['appearances'])
with open(D+'explainer-channels.csv','w',newline='') as f:
  w=csv.DictWriter(f,list(out[0])); w.writeheader(); w.writerows(out)
print(len(rows),len(M),len(out))
```
