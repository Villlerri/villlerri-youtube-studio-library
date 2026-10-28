# Сборщик пилота: восстановить и пересобрать

Код, которым собраны пилот без голоса, Shorts, обложка, аватар, баннер и макеты стилей Countable AI. Задача 60, 2026-10-28. Каждый файл кода — отдельный документ: заголовок — путь, блок кода — содержимое. Видео в репозитории нет: оно пересобирается этим кодом.

## Файлы

Пилот и Shorts, папка `tmp/pilot`:
- [pilot-engine-py.md](pilot-engine-py.md) — движок: время слов, кадры, элементы, субтитры.
- [pilot-shots-py.md](pilot-shots-py.md) — 37 кадров по раскадровке.
- [pilot-build-py.md](pilot-build-py.md) — страница пилота, таймлайн, субтитры.
- [pilot-shorts-py.md](pilot-shorts-py.md) — два Shorts из кадров пилота.
- [pilot-art-py.md](pilot-art-py.md) — обложка, аватар, баннер.
- [pilot-rend-mjs.md](pilot-rend-mjs.md) — рендер страницы в mp4.
- [pilot-shot-mjs.md](pilot-shot-mjs.md) — один кадр в PNG.
- [pilot-sheet-py.md](pilot-sheet-py.md) — листы проверки кадров.

Стиль и макеты, папка `tmp/mock`:
- [mock-gen4-py.md](mock-gen4-py.md) — принятый Swiss Bold с фактурой. Движок пилота берёт стиль отсюда.
- [mock-gen3-py.md](mock-gen3-py.md) — второй круг стилей и общие функции для gen4.
- [mock-widths-json.md](mock-widths-json.md) и [mock-measure-mjs.md](mock-measure-mjs.md) — ширины букв шрифтов и их замер.
- [mock-anim-py.md](mock-anim-py.md) — видеопроба Swiss Bold 18 с.
- [mock-gen2-py.md](mock-gen2-py.md) — первый круг стилей.
- [mock-gen-py.md](mock-gen-py.md) — первые макеты названий; картинки — в [mock-img](mock-img/).
- [mock-shot-mjs.md](mock-shot-mjs.md), [mock-cap-mjs.md](mock-cap-mjs.md) — снимки макетов.

Пример с ручным счётом проверяет скрипт из [../example/check.md](../example/check.md#Скрипт).

## Что нужно

- Python 3 с Pillow.
- Bun и Playwright Chromium. Код берёт Playwright из `/srv/projects/vmsetup/board/node_modules/playwright/index.mjs`.
- ffmpeg с libass: `/home/boardagent/.explainer/bin/ffmpeg`, ffprobe рядом.
- Интернет при рендере: страницы грузят шрифты Archivo и JetBrains Mono с Google Fonts.

## Восстановить файлы

Из корня рабочей копии:

```sh
python3 - <<'EOF'
import glob, os, re
for md in glob.glob('docs/pilots/ai-tutorials/build/*-*.md'):
    t = open(md).read()
    path = t.split('\n', 1)[0][2:]
    code = re.search(r'\n````\w*\n(.*)\n````\n', t, re.S).group(1)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(code + '\n')
    print(path)
EOF
mkdir -p tmp/mock/img && cp docs/pilots/ai-tutorials/build/mock-img/*.webp tmp/mock/img/
```

## Пересобрать без голоса

Все команды — из `tmp/pilot`. Рендер и кодирование запускать по одному: вместе Chromium падает от нехватки памяти.

1. `python3 build.py` — `pilot.html`, `timeline.json`, `captions.srt`. Длина пилота — 531,03 с, 150 субтитров.
2. `python3 shorts.py` — `short1-true-pieces.html` 42,7 с и `short2-guessing-wins.html` 50,85 с. Текст Shorts — в `.txt` рядом.
3. `python3 art.py` — страницы в `art/`. Затем PNG:
   - `bun shot.mjs art/thumbnail.html thumbnail.png 1280 720`
   - `bun shot.mjs art/avatar.html avatar.png 800 800`
   - `bun shot.mjs art/banner.html banner.png 2560 1440`
4. `flock render.lock bun rend.mjs pilot.html out/pilot 531.03` — 18 сегментов по 30 с, около 30 мин. Готовые сегменты при повторе пропускаются.
5. Склейка, из `out`: `ffmpeg -y -f concat -safe 0 -i pilot/list.txt -c copy -movflags +faststart pilot-silent.mp4`.
6. Копия с субтитрами в кадре, из `out`, после `cp ../captions.srt .`:

```sh
ffmpeg -y -i pilot-silent.mp4 -vf "subtitles=captions.srt:force_style='FontName=DejaVu Sans,FontSize=15,Bold=1,BorderStyle=3,Outline=2,Shadow=0,BackColour=&H99000000,OutlineColour=&H99000000,MarginV=24'" -c:v libx264 -preset medium -crf 27 -pix_fmt yuv420p -threads 2 -movflags +faststart pilot-review-subs.mp4
```

7. Shorts: `bun rend.mjs short1-true-pieces.html out/short1 42.7 1080 1920`, затем `short2-guessing-wins.html out/short2 50.85 1080 1920`. Склейка — как в шаге 5, из `short1/list.txt` и `short2/list.txt`.

Для альбома доски видео держать до 60 МБ: файл 407 МБ альбом не принял.

## Под голос ElevenLabs

Не проверено: голоса ещё нет.

Сейчас время слов считает `word_times()` в `engine.py`: 0,11 с плюс 0,054 с на букву, паузы на знаках препинания. От этих времён считаются кадры, появление элементов, субтитры, длина Shorts и главы.

Текст для озвучки — narration 37 кадров из `shots.py`: 1 195 слов, 6 484 знака.

Порядок:
1. Озвучить текст в ElevenLabs с метками времени слов.
2. Заменить расчёт в `word_times(narr, t0)` метками голоса. Функция возвращает те же слова, что `tokens(narr)`, по порядку, с началом и концом каждого, и время конца кадра.
3. Пересобрать по шагам 1–7. Длина может сдвинуться на ±30 с.
4. Наложить голос: `ffmpeg -i pilot-silent.mp4 -i voice.mp3 -c:v copy -c:a aac -b:a 192k -shortest pilot.mp4`. Для Shorts — вырезать голос по их границам: `shorts.py` берёт кадры 14–16 и 28–30.
5. Переписать главы в [../upload/index.md](../upload/index.md#Описание) по новым временам кадров; загрузить новый `captions.srt`.
