# Рабочий сценарий: часы GPS и Эйнштейн

Первый ролик канала «Физика простыми словами». Тему утвердила Villlerri 21.10.2026. Текст английский, под каждым абзацем перевод; мили и футы в переводе даны в километрах и метрах. Голоса нет: озвучка позже, только ElevenLabs. Числа посчитаны, источники — в научной сверке.

## Тема и почему она

Рабочее название: «Your Phone Has to Know Einstein». Вопрос ролика: почему часы на спутниках GPS нарочно ставят медленнее.

- Исследование: относительность и время — самый устойчивый кандидат внутри каналов, 1,25 к соседям в обоих словарях тем. Интерес к «time travel» и «time dilation» высокий ([темы](../../physics-research/topics.md#приоритеты)).
- Быт: карта в телефоне есть у каждого зрителя. Объяснение идёт от знакомой синей точки.
- Основа «Computed»: световые часы — первая тема из списка концепции B. Все числа выводятся из орбиты спутника: +45, −7, итого +38 микросекунд в сутки.
- Формул в кадре нет: скорость и высота показаны часами и счётчиками.
- Первоисточники крепкие: спецификация сигнала GPS, опыт NIST 2010 года, замер спутника NTS-2 в 1977 году.
- Конкуренты есть: minutephysics (2012) и Stand-up Maths (2019) уже разбирали GPS и относительность. Отличие — посчитанные световые часы, доска с котиками и опыт 1977 года как проверка расчёта.

Оценка длительности: 872 слова, около 6:30 с паузами под картинку, разброс 6:00–7:15 от темпа речи. Точный хронометраж — только после записи голоса.

## Сценарий

**1. Крючок.**

You open a map. There's the blue dot. That's you. Found in seconds, to within about sixteen feet. You probably think your phone is just smart. Nope. Your phone is listening to clocks. Clocks in space. And every one of those clocks would be wrong, if nobody had listened to Einstein. A guy who died before the first satellite ever launched is keeping your map honest. Let's see how.

Открываешь карту. Синяя точка. Это ты. Нашёлся за секунды, с точностью около пяти метров. Ты, наверное, думаешь, что телефон просто умный. Нет. Твой телефон слушает часы. Часы в космосе. И все эти часы врали бы, если бы никто не послушал Эйнштейна. Человек, который умер раньше, чем полетел первый спутник, не даёт твоей карте врать. Давай разберёмся как.

**2. Трюк с грозой.**

You already know the trick GPS uses. Thunderstorm. Flash. You start counting. One Mississippi, two Mississippi, three... Boom. Every five seconds is about a mile. The sound came late, and the delay told you how far away the lightning was.

Ты уже знаешь трюк, на котором работает GPS. Гроза. Вспышка. Начинаешь считать. Раз, два, три... Бах. Каждые три секунды — примерно километр. Звук опоздал, и опоздание сказало тебе, как далеко ударила молния.

**3. Спутники кричат время.**

GPS does the same thing, only with light instead of sound. Every satellite keeps shouting two things: exactly what time it is, and exactly where it is. That message takes less than a tenth of a second to reach you. Your phone checks how late it arrived. The delay is your distance. Hear one satellite, and you're somewhere on a giant ball around it. Hear three, and the balls cross in just two spots. One is way out in space. The other one is you. A fourth one fixes your phone's own clock, which, let's be honest, is cheap.

GPS делает то же самое, только со светом вместо звука. Каждый спутник всё время кричит две вещи: который сейчас точно час и где он сам точно находится. Сообщение летит к тебе меньше десятой доли секунды. Телефон смотрит, насколько оно опоздало. Опоздание — это расстояние. Слышишь один спутник — ты где-то на огромном шаре вокруг него. Слышишь три — шары пересекаются всего в двух точках. Одна далеко в космосе. Другая — ты. Четвёртый поправляет часы самого телефона, которые, будем честны, дешёвые.

**4. Наивная модель.**

Here's the catch. Light is fast. In one billionth of a second, it goes about one foot. So if a satellite's clock is off by just one millionth of a second, your distance to it is off by a thousand feet. That's why every GPS satellite carries atomic clocks, good to a few billionths of a second a day. Simple plan: put perfect clocks in the sky, sync them with the ground, done. A second up there is a second down here. Right? Wrong. Twice.

Вот подвох. Свет быстрый. За миллиардную долю секунды он проходит около 30 сантиметров. Значит, если часы спутника ошиблись всего на миллионную долю секунды, расстояние до него ошибётся на 300 метров. Поэтому на каждом спутнике GPS стоят атомные часы. За сутки они уходят лишь на несколько миллиардных долей секунды. Простой план: повесить идеальные часы в небе, сверить с землёй, готово. Секунда там — секунда здесь. Так? Нет. Дважды нет.

**5. Ошибка первая: скорость.**

Wrong number one: speed. GPS satellites race around the Earth at about eight thousand seven hundred miles an hour. Twice a day around the whole planet. Let's build the simplest clock there is. Two mirrors, one flash of light bouncing between them. Up, down: tick. Up, down: tock. Now put that clock on a satellite. From down here, the light doesn't go straight up and down anymore. The mirrors move while it flies, so it takes a longer, slanted path. And here's what Einstein figured out: the speed of light doesn't care how fast you're going. Same speed, longer path. So every tick takes longer. The moving clock runs slow. It's not broken. That's just what time does. For a GPS satellite, it's about seven millionths of a second lost every day.

Ошибка первая: скорость. Спутники GPS несутся вокруг Земли со скоростью около 14 тысяч километров в час. Дважды в сутки вокруг всей планеты. Соберём самые простые часы на свете. Два зеркала, между ними прыгает вспышка света. Вверх, вниз — тик. Вверх, вниз — так. Теперь поставим эти часы на спутник. Снизу видно: свет уже не ходит прямо вверх-вниз. Зеркала сдвигаются, пока он летит, и путь становится длиннее и косым. И вот что понял Эйнштейн: скорости света всё равно, как быстро ты движешься. Скорость та же, путь длиннее. Значит, каждый тик дольше. Движущиеся часы идут медленнее. Они не сломаны. Просто так устроено время. Для спутника GPS это около семи миллионных секунды в сутки.

**6. Ошибка вторая: высота.**

Wrong number two is even weirder. Gravity slows time down. The closer you are to something big and heavy, like the Earth, the slower your clock runs. Go higher, and time speeds up. You don't have to take that on faith. In 2010, scientists in Colorado raised one super-precise clock by about a foot. The raised clock ran faster. So yes, your head is aging faster than your feet. We did the math: stand for eighty years, and your head ends up almost half a millionth of a second older. The cat's been lying flat all day. Now you know why.

Ошибка вторая ещё страннее. Гравитация замедляет время. Чем ближе ты к чему-то большому и тяжёлому, вроде Земли, тем медленнее идут твои часы. Поднимись выше — и время ускорится. Верить на слово не нужно. В 2010 году учёные в Колорадо подняли одни сверхточные часы примерно на 30 сантиметров. Поднятые часы пошли быстрее. Так что да, голова стареет быстрее ног. Мы посчитали: простой восемьдесят лет — и голова станет старше почти на полмиллионной секунды. Кот весь день лежит плашмя. Теперь ты знаешь почему.

**7. Спутник высоко.**

GPS satellites aren't a foot up. They're over twelve thousand miles up, where Earth's pull is much weaker. So their clocks run fast: about forty-five millionths of a second ahead, every day.

Спутники GPS не на 30 сантиметров выше. Они выше 20 тысяч километров, где притяжение Земли намного слабее. Поэтому их часы спешат: примерно на сорок пять миллионных секунды в сутки.

**8. Итог.**

Put both together. Speed: minus seven. Height: plus forty-five. Every day, a satellite clock gets ahead of clocks on the ground by about thirty-eight millionths of a second. Sounds like nothing. But light covers about seven miles in that time. For a system that turns time into distance, that's seven miles of mistake. Added every single day.

Сложим. Скорость: минус семь. Высота: плюс сорок пять. Каждые сутки часы спутника убегают вперёд от наземных примерно на тридцать восемь миллионных секунды. Звучит как ничто. Но свет за это время проходит около 11 километров. Для системы, которая превращает время в расстояние, это 11 километров ошибки. Каждые сутки заново.

**9. Как это чинят.**

So what did the engineers do? They didn't argue with Einstein. They cheated. They set each satellite clock to run a little slow. Its heartbeat should be ten point two three million ticks a second. On the satellite, it's set to ten point two two nine nine nine nine nine nine five four three. Slower by less than half a part in a billion. On the ground, that clock would be wrong. In orbit, once Einstein is done with it, it ticks at just the right rate. And the team on the ground still checks every clock and sends small corrections up every day.

Что сделали инженеры? Они не спорили с Эйнштейном. Они схитрили. Они ставят часы каждого спутника чуть медленнее. Их пульс должен быть 10,23 миллиона тиков в секунду. На спутнике он выставлен 10,22999999543 миллиона. Медленнее меньше чем на половину миллиардной доли. На земле такие часы врали бы. На орбите, когда Эйнштейн с ними закончит, они идут с нужной скоростью. А команда на земле всё равно сверяет каждые часы и каждый день шлёт наверх мелкие поправки.

**10. Проверка 1977 года.**

Did they trust Einstein? Not completely. In 1977, they launched a test satellite with that correction switched off. Just in case. For about three weeks they watched its clock run on its own. It ran fast by about four hundred forty-three parts in a trillion. Einstein's prediction: about four hundred forty-five. Within half a percent. Then they switched the correction on.

Доверяли ли они Эйнштейну? Не до конца. В 1977 году запустили пробный спутник с выключенной поправкой. На всякий случай. Около трёх недель смотрели, как его часы идут сами по себе. Они спешили примерно на 443 триллионных доли. Предсказание Эйнштейна: около 445. Разница меньше половины процента. После этого поправку включили.

**11. Проверь сам.**

Want to see it yourself? Go outside, open a GPS status app on an Android phone, and look at the satellites it hears right now. Find the ones marked GPS. Every one of them is carrying clocks that were set slow on purpose.

Хочешь увидеть сам? Выйди на улицу, открой на телефоне с Android приложение со статусом GPS и посмотри, какие спутники он слышит прямо сейчас. Найди те, что помечены GPS. Каждый из них несёт часы, которые нарочно поставили медленнее.

**12. Финал.**

So next time the blue dot finds you, two of Einstein's ideas just did the math for you. Speed slows time. Gravity slows time. And your phone needs both to find your coffee. Now go check on the cat. It's been lying flat this whole time. Aging very evenly.

Так что в следующий раз, когда синяя точка тебя найдёт, знай: две идеи Эйнштейна только что посчитали за тебя. Скорость замедляет время. Гравитация замедляет время. И телефону нужны обе, чтобы найти твой кофе. А теперь проверь кота. Он всё это время лежал плашмя. Стареет очень равномерно.

## Где котики

Котики не объясняют физику, они реагируют. Подписи мелом рядом с вырезкой.

- Крючок: кот в меловых очках, «← trusts the phone».
- Гроза: кричащий кот, «← counted to three. hid.»
- Три шара: кот косится на дешёвые часы телефона.
- Световые часы: кот из крючка, уже без очков, следит за светом, «← would chase it».
- Голова и ноги: кот лежит плашмя, «ages evenly →».
- Финал: тот же кот, «← aging very evenly».

## Что ещё не сделано

- Голос: ElevenLabs не подключён. Текст для озвучки готов отдельно.
- Сценарий сверен по первоисточникам 21.10.2026, правки сверки внесены ([научная сверка](fact-check.md)).
