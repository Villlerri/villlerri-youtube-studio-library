# Pilot script EN: Why AI Makes Things Up — We Counted It by Hand

Channel: Countable AI, Swiss Bold style with the author's rework: black, white, lime, torn paper, halftone, glitch. Length: about 8:45 with pauses, about 1,200 words of narration. Voice: ElevenLabs, not yet connected; no audio exists. Russian translation for review: [script-ru.md](script-ru.md). Shots: [storyboard.md](storyboard.md). Every number below comes from the [example files](example/check.md).

## 0:00 Cold open

AI tools sometimes say things that are false — calmly, in perfect sentences. Many people call this "hallucination". It sounds mysterious. It isn't.

Today we build a tiny machine that makes the same kind of mistake. It fits on one sheet of paper. We'll count every step with a pencil, and you can check every number yourself. The files are in the description.

One promise before we start: our machine is a toy. Real AI is far bigger, and I'll show you exactly where the toy stops matching it.

## 0:40 The toy

Picture a family group chat. Three messages came in today.

Mom is at the store.
Dad is at the gym.
Sam is at the park.

That's everything our toy will ever read. Three sentences. All three are true.

The toy works a bit like the word suggestions on your phone keyboard. It has one rule. It looks at the last word it wrote, and nothing else. Then it picks a word that came right after that word somewhere in the chat.

To do that, it needs a table. For every word, we write down which words came next, and how often. Let's make that table by hand.

## 1:20 Counting by hand

After "Mom" comes "is". Once. After "Dad": "is". After "Sam": "is". So after a name, the next word is always "is".

After "is" comes "at" — three times out of three. After "at": "the", three out of three.

Now the interesting one. After "the", the chat has "store" once, "gym" once, "park" once. Three different words, one tally each.

That's the whole table. Eight rows. You can check it against the three messages in under a minute.

Now let's ask the toy to finish a sentence: "Mom is at the…"

The toy looks only at the last word: "the". It doesn't see "Mom". In its table, "the" was followed by store, gym and park, once each. So each has the same chance: one in three.

Let's roll a die. One or two: store. Three or four: gym. Five or six: park.

We rolled a four. The toy writes: "Mom is at the gym."

That's false. Mom is at the store. But look at what happened. Every pair of words in that sentence — "Mom is", "is at", "at the", "the gym" — appeared in a true message. The toy never saw a false sentence. It built one anyway, out of true pieces.

How often? Starting from "Mom", the toy can write three sentences. One is true, two are false. Same for Dad, same for Sam. Nine possible sentences, three true, six false. The chance of a false answer is two in three. That's the whole calculation. Pencil, eight rows, one die.

## 3:15 Someone did this in 1948

This idea is old. In 1948, Claude Shannon published "A Mathematical Theory of Communication". In section three, he built English one word at a time from word pairs — with no computer. He opened a book, found a word, and wrote down the word that followed it. Then he looked for that new word somewhere else in the book, and repeated.

Here is part of what he got, exactly as printed: "THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD…"

Every pair of words is real English. The whole thing means nothing. Our toy is a small version of Shannon's machine.

## 4:10 What real models do differently

So is a chatbot just Shannon's table, only bigger? No. Here the toy stops matching.

First, real models don't look at one word. They read the whole question. If our toy read all of "Mom is at the", it would have seen that exact phrase once — followed by "store". This error would disappear.

Second, real models don't store a table of counts. They are neural networks trained on huge amounts of text to predict the next piece of text. That's how models like GPT are described in their own papers. What they learn is far richer than our table.

So why do they still make things up?

In 2025, researchers at OpenAI and Georgia Tech published a paper called "Why Language Models Hallucinate". It gives two reasons. Both can be shown with our toy.

Reason one: rare facts. If a fact appears only once in the training text, a model has very little to go on. The paper gives an example: "if 20% of birthday facts appear exactly once in the pretraining data, then one expects base models to hallucinate on at least 20% of birthday facts."

Our toy shows the extreme version. Ask it where Grandma is. Grandma never wrote in the chat. A table can stay silent. But a model built to always produce the next word will produce one.

Reason two: the way models are graded. Let's give our toy an exam. This time it reads the whole question. Six questions, three answer options each. Three questions are about Mom, Dad and Sam — the toy knows those. Three are about Grandma, Leo and Nina — it has never seen them.

Two versions of the toy take the exam. The honest one answers what it knows, and says "I don't know" to the rest. The guesser answers what it knows, and picks a random option for the rest.

Most tests give one point for a right answer and zero for anything else. "I don't know" scores the same as a wrong answer.

The honest toy scores three. The guesser also gets three, plus a one-in-three chance on each unknown question. On average it scores four. It beats the honest toy in 19 of the 27 possible ways its guesses can fall.

So on this test, guessing wins. The paper says it plainly: "language models are optimized to be good test-takers, and guessing when uncertain improves test performance."

Now change the rule. Right answer: plus one. Wrong answer: minus one. "I don't know": zero. The honest toy still scores three. The guesser now averages two. Guessing stops paying.

That's the paper's proposal: tests should state how confident a model must be before it answers, and take points away for wrong answers.

## 7:20 What this toy leaves out

Let's be clear about what we simplified.

- A word-pair table is not a neural network. Real models don't keep counts like ours.
- Real models read the whole question, not one word.
- Real models work with pieces of words called tokens, not whole words.
- Our exam is a toy exam. Real benchmarks are bigger, and many are not multiple choice.
- Not every false answer has these two causes. The paper covers these two; other causes exist.

What carries over: a model trained to always continue the text, and rewarded for guessing, will sometimes produce fluent false statements. And the rarer a fact is, the likelier the guess.

## 8:10 What to do with this

When an AI answer contains a rare, specific fact — a date, a name, a number, a quote, a reference — that's where a guess can hide. Check it against a source before you use it.

Fluent doesn't mean true. Our toy wrote a perfect sentence about Mom, and it was wrong two times out of three.

The sheet, the table, the exam and a script that checks every number are linked below. Count it yourself.
