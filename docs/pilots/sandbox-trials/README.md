# Sandbox Trials: пилот Event 1 · Switchback Sprint

Записка на 28 октября 2026. Задача 51 на паузе, пока не подключат ElevenLabs. Продолжение — в новой задаче.

## Сделано

- Тема Switchback Sprint, приняла Villlerri 15 октября.
- Официальный прогон: зерно 612826258 из раунда drand 6555429, хеш итоговых позиций 5aaf2fa57acde9da. Журнал — log/event-1.
- Черновик выпуска без голоса, 2:51. Черновики трёх шортсов без голоса: podium, hex, favourite.
- Обложки, оформление канала, пакеты выкладки выпуска и шортсов.
- Пилот и пакет оформления приняла Villlerri 16 октября в 15:41 UTC. Она же разрешила синтез голоса выпуска в лимите $1.
- Текст выпуска и шортсов принял ассистент Villlerri 16 октября. Его уточнения внесены.
- Платных вызовов 0, потрачено $0.

## Осталось

1. Голос выпуска ElevenLabs: 1 580 знаков, около $0,16, один запуск. Разрешён в лимите $1.
2. Сборка с голосом, проверки по quality.md. SRT и главы в upload/event-1.md уточнить по голосу.
3. Приёмка итогового видео — за Villlerri.
4. Голос шортсов: 805 знаков, около $0,06. Нужно отдельное разрешение Villlerri. Затем шортсы с голосом.
5. Открытые решения — в plan.md, разделы «Решения для ассистента» и «Решения для Villlerri».

Публикация не разрешена, канал не создан. Голос — только ElevenLabs.

## С чего продолжить

1. Проверить, что ElevenLabs подключён к доске: маршрут трат отвечает 200, а не 503 `voice_unconfigured`.
2. Восстановить рабочую папку. Команды — из корня репозитория:

```bash
mkdir -p projects/pilots/sandbox-trials
cp -r docs/pilots/sandbox-trials/. projects/pilots/sandbox-trials/
cd projects/pilots/sandbox-trials
awk '/^## /&&!out{path=substr($0,4);next} /^~~~~/{if(out){close(out);out="";path=""}else if(path){out=path;system("mkdir -p $(dirname " out ")");printf "">out}next} out{print>out}' code.md
find . -name '*.json.txt' -o -name '*.srt.txt' | while read -r f; do mv "$f" "${f%.txt}"; done
chmod +x sim/build.sh
G=https://raw.githubusercontent.com/google/fonts/main/ofl
for w in Medium SemiBold Bold; do curl -sSfL -o assets/fonts/BarlowCondensed-$w.ttf $G/barlowcondensed/BarlowCondensed-$w.ttf; done
curl -sSfL -o assets/fonts/JetBrainsMono-Variable.ttf "$G/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
sha256sum -c <<'EOF'
262bd143292ce479ee0cd09a42b47ab173fca8e9c6eb5ed0b5c8a845bc371d17  assets/fonts/BarlowCondensed-Medium.ttf
7b619d14bc2327509a9ef32b0890f709626f7ecc9ff61191c2a4314c5499d2d9  assets/fonts/BarlowCondensed-SemiBold.ttf
e476562ec9c1e16cf16475895b511f08c804f438cc9a9f80a44ea50a0eeb5b65  assets/fonts/BarlowCondensed-Bold.ttf
48715a42ec242c21e9f02692891e147d022299a52e48d5e413e1a942193ffeda  assets/fonts/JetBrainsMono-Variable.ttf
EOF
bun install --frozen-lockfile
sim/build.sh
```

3. Повторить расчёт и черновик по build.md, шаги 2, 7–14. Официальный прогон должен дать тот же хеш 5aaf2fa57acde9da. Не совпал — выпуск не делается.
4. Голос и сборка с голосом — build.md, шаги 15–16. Синтез — один раз, только через маршрут трат доски.
5. Итоговое видео — на приёмку Villlerri.

Восстановление проверено 28 октября в чистой папке: код и данные совпали байт в байт, хеш прогона, лист событий и текст для ElevenLabs — тоже.

## Что где

- Записки по этапам: topic.md, probe.md, rights.md, build.md, sound-voice.md, quality.md, budget.md, plan.md, covers.md, branding.md.
- Сценарий выпуска с переводом — script.md. Текст для ElevenLabs — voice-event-1.txt.
- Пакеты выкладки — upload/event-1.md и upload/shorts.md, обложки и черновые субтитры — рядом.
- Журнал выпуска — log/event-1: заморозка, ответ drand, 1 000 тестовых прогонов, итог и лист событий.
- Спецификации — league/roster.json.txt и trials/. Код — code.md.
- Оформление канала — brand/. Черновые кадры раскадровки и экранов — drafts/.
- Видео — в альбомах задачи 51: «Видео пилота», «Черновики шортсов», «Проба стиля». В репозиторий видео не кладутся. Черновик выпуска пересобирается за 2,3–2,6 минуты, три шортса — за 2–3 минуты.
- Не сохранены и восстанавливаются командами: шрифты, журнал кадров, звук, видео.
