# 30-секундная проба стиля: маяк в сумерках

Код лежит текстом в [code.md](code.md): сохранение в проект принимает только документы. Сначала восстановить файлы по инструкции оттуда.

Проба главного риска варианта A: хватает ли качества рисунка кодом. Голоса нет. Звук — море и ветер из отфильтрованного шума, сделан кодом.

## Что в кадре

1. 0:00–0:04. Пламя-заставка «Lantern Library» на тёмном. Камера отъезжает, пламя совпадает с окном дома смотрителя.
2. 0:04–0:13. Общий план: остров, дом, башня, материк с ельником, снег, море. Титр «A Winter Night in a Lighthouse», «Maine, 1891».
3. 0:13–0:18. Медленный наезд на башню. Небо темнеет весь ролик.
4. 0:18–0:20. Стена башни раскрывается в разрез сверху вниз: кирпичная кладка в сечении, винтовая лестница, вахтенная комната.
5. 0:20–0:24. Смотритель-силуэт поднимается с ручным фонарём. Свет фонаря идёт с ним по стене.
6. 0:24–0:26. Лампа загорается: короткое мерцание, свечение линзы, ореол, плоская полоса света к горизонту, отражение в воде. Ручной фонарь гаснет: в кадре не больше двух тёплых источников.
7. 0:26–0:30. Камера отходит, наплыв в темноту.

Факты в пробе не утверждаются: дом, башня, линза, лестница — собирательные. Точный облик выбранного маяка рисуется по проверенным чертежам на этапе раскадровки.

## Как собрать

Из этой папки, на сервере с Bun и сетью (пакеты и браузер для рендера ставятся в `node_modules`):

```
bun install
python3 -I tools/grain.py public/grain.png
python3 -I tools/ambience.py public/ambience.wav
bunx remotion render src/index.ts LighthouseProbe out/lighthouse-probe.mp4 --codec=h264 --crf=18 --concurrency=2
bunx remotion still src/index.ts ThumbA out/thumb-A.png --scale=0.6667
```

Версии закреплены точно: Remotion 4.0.530, React 18.3.1, шрифты Fontsource (OFL). Шум бумаги `public/grain.png` и звук `public/ambience.wav` делаются кодом с фиксированным зерном и повторяются байт в байт.

## Глава 1 и оформление канала

Тот же код рисует всю главу 1 «Dusk» (композиция `Chapter1`) и оформление канала.

```
python3 tools/timeline.py ../script/chapter-1-dusk.md src/chapter1.json ../script/chapter-1-dusk.estimated.srt
python3 -I tools/ambience_chapter.py src/chapter1.json public/chapter1-ambience.wav
tools/render_chapter.sh out/ch1
tools/mux_chapter.sh out/ch1 out/chapter1.mp4
python3 -I tools/check.py out/chapter1.mp4
bunx remotion still src/index.ts Avatar out/brand/avatar.png --image-format=png
bunx remotion still src/index.ts Banner out/brand/banner.jpg --scale=1.0667 --image-format=jpeg
```

- `tools/timeline.py` — сцены и реплики из сценария. Без голоса время рассчитано: 115 слов в минуту плюс паузы сценария. С голосом то же время берётся из меток ElevenLabs.
- `tools/ambience_chapter.py` — море и ветер на всю главу, блоками по 20 секунд; внутри помещений звук глуше, к концу главы на 4 дБ тише.
- `tools/render_chapter.sh` — рендер кусками без звука (первые 3 минуты, затем по 5 минут), время каждого куска пишется в `out/ch1/times.txt`.
- `tools/mux_chapter.sh` — склейка кусков без перекодирования и звук, один раз: только звук места или голос со звуком места на 6 дБ ниже (`voice`).
- `tools/voice.py` — голос ElevenLabs через счётчик трат студии. Платно: только после разрешения. `count` считает знаки без вызовов; результаты кэшируются, первая ошибка останавливает запуск.
- `tools/voice_mix.py` — дорожка голоса по таймлайну, уровень −21 LUFS.

С голосом сборка такая:

```
python3 -I tools/voice.py chapter <VOICE_ID>
python3 tools/timeline.py ../script/chapter-1-dusk.md src/chapter1.json ../script/chapter-1-dusk.srt voice/ch1
python3 -I tools/ambience_chapter.py src/chapter1.json public/chapter1-ambience.wav
python3 -I tools/voice_mix.py src/chapter1.json voice/ch1 public/chapter1-voice.wav
tools/render_chapter.sh out/ch1v '{"audio":false,"captions":false}'
tools/mux_chapter.sh out/ch1v out/chapter1-voice.mp4 voice
```
- `src/Chapter.tsx` — таймлайн главы: камера, небо, лампа, разрез, путь смотрителя, вставки, субтитры. Ключевые моменты привязаны к репликам, а не к секундам: после синтеза всё сдвинется само.
- `src/Inserts.tsx` — крупные планы: лампа на кухне, банки масла, пальто и фартук, утренняя чистка линзы, фонарь с линзой и занавесками, журнал, страница правил.
- `src/Branding.tsx` — аватар и баннер канала. `BannerBackground` и `BannerText` — слои баннера по отдельности, `BannerSafeAreaCheck` — баннер с рамками областей показа.

## Файлы

- `src/Probe.tsx` — мир, камера, свет, лестница, линза, снег, заставка.
- `src/Thumbnails.tsx` — три варианта обложки из того же мира.
- `src/palette.ts` — палитра канала из концепции.
- `tools/ambience.py` — море и ветер; `tools/grain.py` — шум бумаги.
