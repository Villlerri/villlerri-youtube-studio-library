# Текст для ElevenLabs: часы GPS и Эйнштейн

Текст для озвучки, отдельно от сценария. Синтеза ещё не было: ElevenLabs не подключён, проб не делали.

## Как озвучивать

- Один запрос на строку: 108 строк, 4697 знаков. Номер строки — имя файла и ключ для картинки, например `s05b.3`.
- Запрос `with-timestamps`: в ответе время каждого символа. По нему встанут кадры и субтитры ([план подгонки](timing-plan.md)).
- Модель: Multilingual v2. Метки времени для неё описаны в справочнике. Для v3 и v4 это не подтверждено.
- Голос выбирает автор после пробы 2–3 голосов на строках `s01.1`–`s01.6`. Тон живой, весёлый, на «ты».
- Начальные настройки для пробы: stability 0.40, similarity 0.75, style 0.30, speaker boost включён, скорость 1.0. Это стартовая точка, не проверено на слух.
- Между строками и досками паузы держим мы. Теги пауз в текст не вставлять.
- Числа уже написаны словами, как их надо произнести. «GPS» читается по буквам.
- Аудио и метки каждой строки хранить: повторная генерация даёт другой результат.

## Произношение

- «ten point two two nine nine nine nine nine nine nine five four» — медленно и ровно, это шутка про длинное число.
- «One Mississippi, two Mississippi, three...» — счёт с паузами, как в грозу.
- «Nope.», «Wrong.», «Twice.», «Boom.» — отдельные короткие реплики, с ударением.

## s01 · Крючок

- `s01.1` You open a map.
- `s01.2` There's the blue dot.
- `s01.3` That's you.
- `s01.4` Found in seconds, to within about sixteen feet.
- `s01.5` You probably think your phone is just smart.
- `s01.6` Nope.
- `s01.7` Your phone is listening to clocks.
- `s01.8` Clocks in space.
- `s01.9` And every one of those clocks would be wrong, if nobody had listened to Einstein.
- `s01.10` A guy who died before the first satellite ever launched is keeping your map honest.
- `s01.11` Let's see how.

## s02 · Гроза

- `s02.1` You already know the trick GPS uses.
- `s02.2` Thunderstorm.
- `s02.3` Flash.
- `s02.4` You start counting.
- `s02.5` One Mississippi, two Mississippi, three...
- `s02.6` Boom.
- `s02.7` Every five seconds is about a mile.
- `s02.8` The sound came late, and the delay told you how far away the lightning was.

## s03 · Спутник кричит время

- `s03.1` GPS does the same thing, only with light instead of sound.
- `s03.2` Every satellite keeps shouting two things: exactly what time it is, and exactly where it is.
- `s03.3` That message takes less than a tenth of a second to reach you.
- `s03.4` Your phone checks how late it arrived.
- `s03.5` The delay is your distance.

## s03b · Три шара

- `s03b.1` Hear one satellite, and you're somewhere on a giant ball around it.
- `s03b.2` Hear three, and the balls cross in just two spots.
- `s03b.3` One is way out in space.
- `s03b.4` The other one is you.
- `s03b.5` A fourth one fixes your phone's own clock, which, let's be honest, is cheap.

## s04 · Подвох: свет быстрый

- `s04.1` Here's the catch.
- `s04.2` Light is fast.
- `s04.3` In one billionth of a second, it goes about one foot.
- `s04.4` So if a satellite's clock is off by just one millionth of a second, your distance to it is off by a thousand feet.
- `s04.5` That's why every GPS satellite carries atomic clocks, good to a few billionths of a second a day.
- `s04.6` Simple plan: put perfect clocks in the sky, sync them with the ground, done.
- `s04.7` A second up there is a second down here.
- `s04.8` Right?
- `s04.9` Wrong.
- `s04.10` Twice.

## s05 · Ошибка первая: скорость

- `s05.1` Wrong number one: speed.
- `s05.2` GPS satellites race around the Earth at about eight thousand seven hundred miles an hour.
- `s05.3` Twice a day around the whole planet.

## s05b · Световые часы

- `s05b.1` Let's build the simplest clock there is.
- `s05b.2` Two mirrors, one flash of light bouncing between them.
- `s05b.3` Up, down: tick.
- `s05b.4` Up, down: tock.
- пауза 0.6 с — не озвучивать, держим мы
- `s05b.5` Now put that clock on a satellite.
- `s05b.6` From down here, the light doesn't go straight up and down anymore.
- `s05b.7` The mirrors move while it flies, so it takes a longer, slanted path.
- пауза 1.0 с — не озвучивать, держим мы
- `s05b.8` And here's what Einstein figured out: the speed of light doesn't care how fast you're going.
- `s05b.9` Same speed, longer path.
- `s05b.10` So every tick takes longer.
- `s05b.11` The moving clock runs slow.
- `s05b.12` It's not broken.
- `s05b.13` That's just what time does.
- `s05b.14` For a GPS satellite, it's about seven millionths of a second lost every day.

## s06 · Ошибка вторая: высота

- `s06.1` Wrong number two is even weirder.
- `s06.2` Gravity slows time down.
- `s06.3` The closer you are to something big and heavy, like the Earth, the slower your clock runs.
- `s06.4` Go higher, and time speeds up.
- `s06.5` You don't have to take that on faith.
- `s06.6` In 2010, scientists in Colorado raised one super-precise clock by about a foot.
- `s06.7` The raised clock ran faster.

## s06b · Голова и ноги

- `s06b.1` So yes, your head is aging faster than your feet.
- `s06b.2` We did the math: stand for eighty years, and your head ends up almost half a millionth of a second older.
- `s06b.3` The cat's been lying flat all day.
- `s06b.4` Now you know why.

## s07 · Спутник высоко

- `s07.1` GPS satellites aren't a foot up.
- `s07.2` They're over twelve thousand miles up, where Earth's pull is much weaker.
- `s07.3` So their clocks run fast: about forty-five millionths of a second ahead, every day.

## s08 · Итог

- `s08.1` Put both together.
- `s08.2` Speed: minus seven.
- `s08.3` Height: plus forty-five.
- `s08.4` Every day, a satellite clock gets ahead of clocks on the ground by about thirty-eight millionths of a second.
- `s08.5` Sounds like nothing.
- `s08.6` But light covers about seven miles in that time.
- `s08.7` For a system that turns time into distance, that's seven miles of mistake.
- `s08.8` Added every single day.

## s09 · Как это чинят

- `s09.1` So what did the engineers do?
- `s09.2` They didn't argue with Einstein.
- `s09.3` They cheated.
- `s09.4` Engineers set each satellite clock to run a little slow.
- `s09.5` Its heartbeat should be ten point two three million ticks a second.
- `s09.6` On the satellite, it's set to ten point two two nine nine nine nine nine nine five four three.
- `s09.7` Slower by less than half a part in a billion.
- `s09.8` On the ground, that clock would be wrong.
- `s09.9` In orbit, once Einstein is done with it, it ticks at just the right rate.
- `s09.10` And the team on the ground still checks every clock and sends small corrections up every day.

## s10 · Проверка 1977 года

- `s10.1` Did they trust Einstein?
- `s10.2` Not completely.
- `s10.3` In 1977, they launched a test satellite with that correction switched off.
- `s10.4` Just in case.
- `s10.5` For about three weeks they watched its clock run on its own.
- `s10.6` It ran fast by about four hundred forty-three parts in a trillion.
- `s10.7` Einstein's prediction: about four hundred forty-five.
- `s10.8` Within half a percent.
- `s10.9` Then they switched the correction on.

## s11 · Проверь сам

- `s11.1` Want to see it yourself?
- `s11.2` Go outside, open a GPS status app on an Android phone, and look at the satellites it hears right now.
- `s11.3` Find the ones marked GPS.
- `s11.4` Every one of them is carrying clocks that were set slow on purpose.

## s12 · Финал

- `s12.1` So next time the blue dot finds you, two of Einstein's ideas just did the math for you.
- `s12.2` Speed slows time.
- `s12.3` Gravity slows time.
- `s12.4` And your phone needs both to find your coffee.
- `s12.5` Now go check on the cat.
- `s12.6` It's been lying flat this whole time.
- `s12.7` Aging very evenly.
