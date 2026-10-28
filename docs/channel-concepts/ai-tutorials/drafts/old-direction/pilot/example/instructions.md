# Инструкция: как повторить тест «20 чеков»

Две части: для студии — как повторить наш прогон точно; для зрителя — текст для описания видео на английском. Запуск моделей — только после согласия автора на тему А.

## Файлы

- [receipts/receipts.txt](receipts/receipts.txt) — 20 учебных чеков в 4 пачках по 5. Магазины и суммы выдуманы.
- [receipts/answer-key.csv](receipts/answer-key.csv) — правильные продавец, дата и итог по каждому чеку и ловушка, которую чек проверяет.
- [receipts/prompt.txt](receipts/prompt.txt) — простая инструкция для модели.
- [receipts/prompt-v2.txt](receipts/prompt-v2.txt) — строгая инструкция с образцом (прогон 2).
- [check.html](check.html) — страница проверки: открыть в браузере, вставить ответы, нажать Check. Работает без интернета.
- [results/](results/) — ответы модели во всех трёх прогонах и разбор по чекам.

Правила ключа: дата — день оплаты; итог — вся сумма покупки с налогом и чаевыми, после скидок; возврат — с минусом; сдача, экономия, остаток, прошлый долг и часть раздельной оплаты итогом не считаются.

## Для студии: повторить наш прогон

1. Скачать llama.cpp, сборка b11707, файл для своей системы со страницы github.com/ggml-org/llama.cpp/releases/tag/b11707. Мы брали `llama-b11707-bin-ubuntu-x64.tar.gz`, SHA-256 `88879871f765c3dec22260046e10a76e2ed38de5bdf4a7f68049245a8f4056c8`.
2. Скачать модель `Qwen3.5-0.8B-Q4_K_M.gguf` из репозитория huggingface.co/unsloth/Qwen3.5-0.8B-GGUF. SHA-256 `bd258782e35f7f458f8aced1adc053e6e92e89bc735ba3be89d38a06121dc517`.
3. Запустить: `llama-server -m Qwen3.5-0.8B-Q4_K_M.gguf -c 4096 -np 1 -t 3 --reasoning off --temp 0 --seed 1`.
4. Прогоны 1 и 2 (прямой запрос): для каждой пачки отправить на `/v1/chat/completions` одно сообщение — текст инструкции, пустая строка, текст пачки; `temperature` 0, `seed` 1, `chat_template_kwargs: {"enable_thinking": false}`. Код запроса и подсчёта — в [приложении](../../evidence-code.md#прогон-чеков).
5. Прогон 3 (окно чата): открыть адрес из строки «listening», для каждой пачки начать новый чат, вставить инструкцию и пачку, нажать Enter.
6. Собрать 20 строк по порядку, вставить в check.html, нажать Check.
7. Сравнить с [результатами](results.md). При температуре 0 ответы должны совпасть; разброс между запусками мы не проверяли.

Чего ждать от другого компьютера: скорость будет другой. Ответы могут отличаться: порядок вычислений зависит от процессора и числа потоков.

## Для зрителя (текст в описание видео, EN)

Try the same test on your own computer:

1. Download the free program llama.cpp for your computer: github.com/ggml-org/llama.cpp/releases (Windows: the file ending in `win-cpu-x64.zip`; newer Mac: `macos-arm64`).
2. Download the model file `Qwen3.5-0.8B-Q4_K_M.gguf` (about 0.5 GB) and put it in the same folder.
3. Open a terminal in that folder and run:
   `llama-server -m Qwen3.5-0.8B-Q4_K_M.gguf --temp 0 --reasoning off`
4. Open the address shown after "listening" in your browser.
5. Paste `prompt.txt`, then one batch of five receipts from `receipts.txt`. Press Enter. Start a new chat for each batch.
6. Open `check.html`, paste all 20 lines the AI wrote, in order, and press Check.

Your numbers may differ from ours. That's the point: check your own run.

Перед публикацией: шаги 1, 3 и 4 проверить на Windows и Mac на постоянном ноутбуке. Сейчас они проверены только на Linux.
