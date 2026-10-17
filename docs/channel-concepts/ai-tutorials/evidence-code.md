# Приложение: код проверки

Код, которым посчитаны цифры в [проверке исследования 59](evidence-check.md) и [плане](plan.md#название). Python 3.14, без сторонних библиотек, кроме yt-dlp 2026.08.19 для проверки названий. Пути — как на рабочем сервере 2026-10-17.

## Цифра 79% и её пересчёт

Запуск: `python3 check79.py docs/ai-tutorials-research/data` и `python3 check79b.py docs/ai-tutorials-research/data`.

```python
import csv, statistics as st, sys, collections
D=sys.argv[1]
C={r['channel_id']:r for r in csv.DictReader(open(D+'/channels.csv'))}
V=list(csv.DictReader(open(D+'/videos.csv')))
segk={}
for r in csv.DictReader(open(D+'/segment-metrics.csv')): segk[r['segment']]=r['kind']
en_lesson={s for s,k in segk.items() if s.startswith('en_') and k=='lesson'}
print('en lesson segments',len(en_lesson),sorted(en_lesson))
# channels appearing in en lesson segments
rows=[v for v in V if v['segment'] in en_lesson]
app=collections.Counter(v['channel_id'] for v in rows)
new=[cid for cid in app if C.get(cid,{}).get('new_lt12m')=='1']
def med(cid):
    c=C[cid]; m=c['median_views_listed_age_ge30d'] or c['median_views_listed']
    return float(m) if m not in ('',None) else None
vals=[(cid,med(cid)) for cid in new]
vals=[x for x in vals if x[1] is not None]
n=len(vals); lt100=[x for x in vals if x[1]<100]; mid=[x for x in vals if 100<=x[1]<1000]; ge1k=[x for x in vals if x[1]>=1000]
print('new channels',len(new),'with median',n,'lt100',len(lt100),round(len(lt100)/n,3),'100-1k',len(mid),'ge1k',len(ge1k), 'ge10k', sum(1 for x in vals if x[1]>=10000))
# fallback: median_views_listed_age_ge30d empty => used all (young) videos
fb=[cid for cid in new if not C[cid]['median_views_listed_age_ge30d']]
print('new channels where median uses videos younger than 30 days (no >=30d videos):',len(fb))
# listed long videos
ll=[int(float(C[cid]['listed_long_videos'] or 0)) for cid in new]
print('listed long videos among new: median',st.median(ll),'share <10',round(sum(1 for x in ll if x<10)/len(ll),3))
# pace
pace=lambda cid: float(C[cid]['long_uploads_per_month'] or 0)
lp=[pace(c) for c,_ in lt100]; gp=[pace(c) for c,_ in ge1k]
print('pace lt100 median',st.median(lp),'share>=8',round(sum(1 for x in lp if x>=8)/len(lp),2),'| pace ge1k median',st.median(gp))
# total videos (all, incl shorts)
tv=lambda cid: int(float(C[cid]['video_count_all'] or 0))
print('video_count_all lt100 median',st.median([tv(c) for c,_ in lt100]),'| ge1k median',st.median([tv(c) for c,_ in ge1k]))
# appearance weighting: rows in search from lt100 new channels vs all new
r_lt=sum(app[c] for c,_ in lt100); r_all=sum(app[c] for c,_ in vals)
print('search rows from new channels',r_all,'of which lt100 channels',r_lt,round(r_lt/r_all,3),'| all en lesson rows',len(rows))
# top appearing lt100 channels
for c,m in sorted(lt100,key=lambda x:-app[x[0]])[:8]:
    print('  ',app[c],C[c]['channel'],'videos',C[c]['video_count_all'],'pace',C[c]['long_uploads_per_month'],'median',m)
# channel age in months for new channels
ag=[float(C[c]['channel_age_months'] or 0) for c,_ in vals]
print('new channel age months median',st.median(ag))
# first_listed_upload recency
```

```python
import csv, statistics as st, sys, collections
D=sys.argv[1]
C={r['channel_id']:r for r in csv.DictReader(open(D+'/channels.csv'))}
V=list(csv.DictReader(open(D+'/videos.csv')))
segk={r['segment']:r['kind'] for r in csv.DictReader(open(D+'/segment-metrics.csv'))}
en_lesson={s for s,k in segk.items() if s.startswith('en_') and k=='lesson'}
cids={v['channel_id'] for v in V if v['segment'] in en_lesson and v['channel_id'] in C}
def bucket(x): return 'lt100' if x<100 else ('100-1k' if x<1000 else 'ge1k')
for field in ['median_views_listed','median_views_listed_age_ge30d']:
    for grp,cond in [('new',lambda a:a<12),('1-3y',lambda a:12<=a<36),('3y+',lambda a:a>=36)]:
        xs=[float(C[c][field]) for c in cids if C[c][field]!='' and C[c]['channel_age_months']!='' and cond(float(C[c]['channel_age_months']))]
        cnt=collections.Counter(bucket(x) for x in xs)
        print(field,grp,len(xs),dict(cnt), 'ge1k share',round(cnt['ge1k']/len(xs),2) if xs else None)
# new channels by new_lt12m flag and whether >=30d data exists
new=[c for c in cids if C[c]['new_lt12m']=='1']
has=[c for c in new if C[c]['median_views_listed_age_ge30d']!='']
print('new',len(new),'with >=30d median',len(has))
xs=[float(C[c]['median_views_listed_age_ge30d']) for c in has]
print('  among those with >=30d videos:',dict(collections.Counter(bucket(x) for x in xs)))
# first_listed_upload for new
import datetime
fl=[C[c]['first_listed_upload'] for c in new if C[c]['first_listed_upload']]
print('first_listed_upload present',len(fl))
```

## Проверка названий

Запуск: `python3 names.py "Countable AI" "The Guess Machine" "AI Since 1948"`. Поиск каналов YouTube с фильтром «канал» (`sp=EgIQAg%3D%3D`), регион США, без входа; затем открытие адреса `youtube.com/@<имя>`: ответ 404 — адрес свободен.

```python
import sys, json, re, urllib.request, urllib.parse, yt_dlp
names = sys.argv[1:]
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36', 'Cookie': 'CONSENT=YES+1; SOCS=CAI', 'Accept-Language': 'en-US'}
for n in names:
    q = urllib.parse.quote(n)
    url = f'https://www.youtube.com/results?search_query={q}&sp=EgIQAg%253D%253D&hl=en&gl=US'
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'playlistend': 8, 'skip_download': True}) as y:
        try:
            d = y.extract_info(url, download=False)
            ch = [(e.get('channel') or e.get('title'), e.get('channel_follower_count'), e.get('url')) for e in d.get('entries', [])][:8]
        except Exception as ex:
            ch = [('ERR', str(ex)[:80], '')]
    handle = '@' + re.sub(r'[^A-Za-z0-9]', '', n)
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/' + handle, headers=UA), timeout=20)
        page = r.read().decode('utf8', 'ignore')
        hs = 'TAKEN' if '"channelId"' in page or 'og:title' in page else 'unclear'
        t = re.search(r'<meta property="og:title" content="([^"]*)"', page)
        hs += ' (' + (t.group(1) if t else '') + ')'
    except urllib.error.HTTPError as e:
        hs = f'free? HTTP {e.code}'
    print(json.dumps({'name': n, 'handle': handle, 'handle_status': hs, 'channel_search_top': ch}, ensure_ascii=False))
```
