# Приложение: код оформления канала

Код и команды, которыми нарисованы аватар, шапки и обложки канала ([YouTube](youtube-en.md), [ВК и Rutube](vk-rutube-ru.md)). Писал ассистент в задаче 127, 2026-10-29. Фон шапок и обложек — кадры сцен: `scene2.py` из [кода ролика 2](../v2/code.md) и `scene.py` из [кода пилота](../pilot/code.md), кадр на 120-й секунде. Шрифт — Lato (SIL OFL 1.1), системный пакет `fonts-lato`. FFmpeg 6.0.1, Python 3.14.4, numpy 2.5.4.

## avatar.py

```python
"""Channel avatar, drawn by code: amber crescent moon and a cream paw print on deep blue. Square PNG, any size.

Run: python -I avatar.py <size> <out.rgb>   (raw RGB24; ffmpeg makes the PNG)
Platforms crop the avatar to a circle: everything stays inside the central circle.
"""
import sys
import numpy as np

N = int(sys.argv[1]); s = N / 800.0
yy, xx = (np.mgrid[0:N, 0:N].astype(np.float32) + 0.5) / s          # coordinates in an 800-unit square
aa = 1.2 / s                                                          # edge softness: about one pixel


def cover(d):
    """Coverage from a signed distance (negative inside)."""
    return np.clip(0.5 - d / (2 * aa), 0, 1)


def ellipse(cx, cy, rx, ry, ang=0.0):
    c, si = np.cos(ang), np.sin(ang)
    u, v = (xx - cx) * c + (yy - cy) * si, -(xx - cx) * si + (yy - cy) * c
    k = np.hypot(u / rx, v / ry)
    return (k - 1) * min(rx, ry)                                      # approximate distance, fine for soft edges


r = np.hypot(xx - 400, yy - 400) / 400
img = (np.float32([0.060, 0.080, 0.190]) * (1 - r[..., None] * 0.55)).astype(np.float32)
img += (np.exp(-((xx - 330) ** 2 + (yy - 300) ** 2) / (2 * 260 ** 2)) * 0.06)[..., None] * np.float32([0.9, 0.8, 0.6])

moon = np.maximum(np.hypot(xx - 375, yy - 405) - 285, -(np.hypot(xx - 455, yy - 365) - 255))
img = img * (1 - cover(moon)[..., None]) + np.float32([0.93, 0.77, 0.43]) * cover(moon)[..., None]

cx, cy = 470, 420                                                      # paw inside the moon's hollow
pads = [ellipse(cx, cy + 62, 92, 74)]
for dx, dy, ang in ((-112, -30, -0.45), (-44, -96, -0.15), (44, -96, 0.15), (112, -30, 0.45)):
    pads.append(ellipse(cx + dx, cy + dy, 36, 48, ang))
paw = np.minimum.reduce(pads)
img = img * (1 - cover(paw)[..., None]) + np.float32([0.93, 0.89, 0.72]) * cover(paw)[..., None]

open(sys.argv[2], 'wb').write((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
```

## Команды

```bash
F=/usr/share/fonts/truetype/lato
python -I avatar.py 800 a.rgb && ffmpeg -f rawvideo -pix_fmt rgb24 -s 800x800 -i a.rgb avatar-800.png
python -I scene2.py still 120 v2.rgb && ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -i v2.rgb v2-120.png
python -I scene.py still 120 p.rgb && ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -i p.rgb pilot120.png
# YouTube banner: text inside the 1546x423 centre zone
ffmpeg -i v2-120.png -vf "scale=2560:1440:flags=lanczos,eq=brightness=0.02:gamma=1.15,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='Slow Notes for Dogs':fontsize=120:fontcolor=0xEDE3B8:x=(w-text_w)/2:y=600,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='Slow, quiet music for dogs at home · 10-hour videos':fontsize=48:fontcolor=0xB9C4DA:x=(w-text_w)/2:y=770" \
  -frames:v 1 youtube-banner-2560x1440.png
# VK community cover
ffmpeg -i v2-120.png -vf "scale=1920:1080:flags=lanczos,crop=1920:768:0:200,eq=brightness=0.02:gamma=1.15,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='Тихие ноты для собак':fontsize=104:fontcolor=0xEDE3B8:x=(w-text_w)/2:y=270,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='Медленная тихая музыка для собак, пока вас нет дома':fontsize=44:fontcolor=0xB9C4DA:x=(w-text_w)/2:y=410" \
  -frames:v 1 vk-cover-1920x768.png
# Rutube banner, JPEG
ffmpeg -i v2-120.png -vf "scale=2560:1440:flags=lanczos,crop=2560:960:0:260,eq=brightness=0.02:gamma=1.15,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='Тихие ноты для собак':fontsize=130:fontcolor=0xEDE3B8:x=(w-text_w)/2:y=330,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='Медленная тихая музыка для собак, пока вас нет дома':fontsize=56:fontcolor=0xB9C4DA:x=(w-text_w)/2:y=505" \
  -frames:v 1 -q:v 2 rutube-banner-2560x960.jpg
# Russian video covers, 1920x1080
ffmpeg -i pilot120.png -vf "eq=brightness=0.03:gamma=1.15,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='СПОКОЙНОЕ ФОРТЕПИАНО':fontsize=114:fontcolor=0xEDE3B8:x=120:y=345,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='И АРФА ДЛЯ СОБАК':fontsize=90:fontcolor=0xEDE3B8:x=126:y=483,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='тихая музыка, пока вас нет дома':fontsize=51:fontcolor=0xB9C4DA:x=129:y=615" \
  -frames:v 1 ru-cover-v1.png
ffmpeg -i v2-120.png -vf "eq=brightness=0.03:gamma=1.2,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='СПОКОЙНАЯ ФЛЕЙТА':fontsize=129:fontcolor=0xEDE3B8:x=120:y=180,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='И КЛАРНЕТ ДЛЯ СОБАК':fontsize=90:fontcolor=0xEDE3B8:x=126:y=333,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='мягкая музыка для тихого дома':fontsize=51:fontcolor=0xB9C4DA:x=129:y=465" \
  -frames:v 1 ru-cover-v2.png
```
