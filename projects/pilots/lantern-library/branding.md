# Оформление канала Lantern Library

Пакет на согласование вместе с пилотом. Канал не создан. Требования YouTube — по официальным страницам, проверены 2026-10-15: [список с цитатами](research/youtube-requirements.md).

## Название и адрес

- Название канала: Lantern Library (решено 2026-10-15).
- Адрес (handle): рекомендую @LanternLibraryHistory, запасной — @LanternLibrarySleep. Оба без страницы канала на 2026-10-15, 20:32 UTC. Свободен ли адрес, покажет только Studio при создании.
- Уже заняты: @LanternLibrary (книжные рекомендации, 29 подписчиков), @TheLanternLibrary (истории о тайнах), @LanternLibraryStories (уютные истории для сна, 9 подписчиков, 2 видео). [Подробно](research/youtube-requirements.md#проверка-адресов-lantern-library).
- Риск: в поиске YouTube рядом окажутся маленькие каналы с тем же именем, один — тоже истории для сна. Название оставляю, как решено; адрес с «History» отличает нас по теме. Если Villlerri захочет другое имя, сменить его можно дважды за 14 дней.

## Описание канала (английский)

```
Quiet, true-to-history stories for falling asleep.

Each story is one night in one place in the past. You are there, doing the small work of the evening, while the world grows dark around you. The first story: a lighthouse keeper's winter night on the coast of Maine, 1892.

The places, the rules and the work are real, and every video lists its sources. Where a story imagines a thought or the weather of one night, it says so. "You" are a composite character, never a real person.

Original drawings made for each story. Narration: synthetic voice.

No sudden sounds, no rising music, no hurry. One quiet night in another century.
```

633 знаков из 1 000 допустимых.

## Аватар

- Ручной фонарь на ночном синем, тёплое пламя — тот же янтарь, что у огня в роликах.
- Файл: [avatar.png](branding/avatar.png), 800×800, PNG. YouTube показывает аватар кругом 98×98; допускает JPG, PNG до 15 МБ.
- Читается в круге 98 и 40 точек: [проверка](branding/avatar-check.jpg).

## Баннер

- Ночной мир Fort Point: дом с тёплым окном, башня с горящим фонарём, звёзды. Надпись «Lantern Library» и строка «One quiet night in another century».
- Файл: [banner.jpg](branding/banner.jpg), 2560×1440 — рекомендованный размер YouTube; минимум 2048×1152, до 6 МБ.
- Безопасная область для текста и логотипа — 1235×338 при 2048×1152, то есть 1544×423 при 2560×1440. Надпись и фонарь внутри неё: [проверка](branding/banner-safe-area-check.jpg).
- Как YouTube режет баннер на телефоне и компьютере, официально в цифрах не сказано. Всё важное — в безопасной области, остальное — фон.
- Рамок, теней и обводок у картинки нет: YouTube просит их не добавлять.

## Исходники

- Код: [Branding.tsx](probe/code.md). Цвета — [palette.ts](probe/code.md), шрифты Cormorant Garamond и Nunito Sans (OFL).
- Слои баннера для любого редактора: [фон без надписи](branding/banner-background.jpg) и [надпись на прозрачном](branding/banner-text.png), оба 2560×1440.
- Аватар на прозрачном фоне: [avatar-transparent.png](branding/avatar-transparent.png).
- Пересборка: команды в [README пробы](probe/README.md#глава-1-и-оформление-канала).

## Как применить

1. Создать канал «Lantern Library» в аккаунте студии. Создание и выбор адреса — решение Villlerri.
2. YouTube Studio → Customization → Branding: Picture — avatar.png; Banner image — banner.jpg. В окне обрезки ничего не сдвигать: рамка уже по безопасной области.
3. Customization → Basic info: имя, адрес, описание из блока выше. Язык канала — English.
4. Проверить вид канала на компьютере и телефоне: надпись баннера не обрезана, аватар читается.
