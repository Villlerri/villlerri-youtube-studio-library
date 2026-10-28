# Pilot script (EN): "I Gave 20 Receipts to a Free Offline AI. Here's Every Mistake"

Channel: Plain Laptop Lab (working name). Presentation 1, the test bench, with the step chips of presentation 2. Length: narration about 1 040 words, 7 minutes at 150 words a minute; with on-screen steps about 8:45. Timecodes are estimates. Russian translation for review: [script-ru.md](script-ru.md). Shots: [storyboard.md](storyboard.md).

Status: draft for the author. Numbers in square brackets come from the probe runs on 2026-10-17 ([results](example/results.md)). The pilot is filmed on the studio's test laptop; every bracketed number is replaced with the result of that run before voicing. FILM ON LAPTOP marks something that must really happen on camera. VERIFY ON LAPTOP marks a claim not yet checked; it is cut if the check fails.

Voice: one calm, exact narrator. ElevenLabs only, voice chosen by the author.

---

## 1. Cold open (0:00–0:30)

We gave twenty receipts to a free AI that runs on an ordinary laptop. No account. No subscription. [FILM ON LAPTOP: Wi-Fi switched off on screen.] And no internet.

It found the right total on [nineteen] receipts out of twenty.

And it still handed us a table we couldn't use.

So today we'll do the whole thing together, step by step — and then we'll check every single line. You can download the same twenty receipts and repeat the test yourself. The links are in the description.

## 2. The setup (0:30–1:15)

Here's what we used.

An ordinary laptop: [model name], [8] gigabytes of memory, no gaming graphics card.

One free AI model, called Qwen 3.5, the smallest size. The file is about half a gigabyte. Its license lets anyone use it, even for work.

One free program to run it, called llama.cpp. It opens a simple chat window in your web browser.

And twenty practice receipts. The stores are made up, but the receipts are built like real ones: a handwritten tip, a refund, a gift card, a hotel bill that ends with "balance zero". We know the right answer for every one of them. That's the point: you can't check an AI without an answer key.

## 3. Step 1 of 5 — Download the program (1:15–1:50)

Step one. Download llama.cpp.

On the project's download page, pick the file for your computer. For most Windows laptops, it's the one that ends in "win, cpu, x64". On a newer Mac, it's "macos arm64".

Unzip it into a folder you can find again. That's the whole install. [VERIFY ON LAPTOP: no extra installer needed on Windows and Mac.]

## 4. Step 2 of 5 — Download the model (1:50–2:15)

Step two. Download the model file. Its name is long: "Qwen3.5 0.8B, Q4 K M, dot gguf". The link is in the description.

Put it in the same folder.

Half a gigabyte. On most home connections, that's a minute or two.

## 5. Step 3 of 5 — Start it (2:15–3:15)

Step three. Start the program.

Open the folder, open a terminal there, and paste the line from the description. Here it is on screen.

One part of that line matters a lot: "temp zero". It tells the AI not to improvise. Without it, the chat window picks words with a bit of randomness — and on our first try that gave us garbled store names. With "temp zero", it always picks its most likely answer.

When you see "listening", open your browser and go to the address on screen. That's the chat window. Everything you type stays on this laptop. [VERIFY ON LAPTOP: network monitor shows no outside connections while the chat runs.]

## 6. Step 4 of 5 — Paste the first five receipts (3:15–4:20)

Step four. Open our instructions file, copy all of it, and paste it into the chat. Then copy the first five receipts and paste them under it. Press Enter.

The instructions ask for one line per receipt, with five parts separated by commas: the receipt number, the store, the date, the total, and the exact line where the AI found the total.

On our laptop the answer took about [eight] seconds.

Do the same for the other three batches. Four batches, five receipts each.

## 7. Step 5 of 5 — Check every line (4:20–5:20)

Step five. Check.

Open our free checker page. It's a single file; it works without the internet. Paste the twenty lines the AI wrote, in order, and press Check.

The checker gives you four scores.

"Total anywhere in the line": did the AI find the right number at all?

"Total in the total column": will a spreadsheet see it in the right place?

"Date anywhere in the line."

And "lines in the requested format": five parts, in the right order, ready to paste into a spreadsheet.

Here's ours.

## 8. The scores (5:20–6:00)

Total anywhere in the line: [nineteen] out of twenty.

Date: [twenty] out of twenty.

Total in the right column: [four] out of twenty.

Lines in the requested format: [zero] out of twenty.

So the AI found the numbers. It just couldn't keep the table straight.

We ran the same receipts two more ways, so you can see how much the answer moves.

Sent directly, without the chat window: totals found [twenty] out of twenty. Format: [zero].

And with stricter instructions plus one example line: totals found dropped to [eighteen]. Format: still [zero].

## 9. Every mistake (6:00–7:25)

Let's go through the mistakes one by one.

Mistake one: the extra word. Every line starts with the word "receipt". We never asked for it. One extra word pushes every column one place to the right — so the total lands where the date should be.

Mistake two: the comma in the date. On receipt six the AI wrote "October 7, 2026". The date is right. But a spreadsheet splits lines at commas, so that one date becomes two columns.

Mistake three: the handwritten tip. Receipt two is a restaurant bill. The printed amount is thirty-seven dollars. The diner added a seven-dollar tip by hand, for a total of forty-four. In the chat window, the AI took thirty-seven.

Mistake four, from the stricter instructions: the hotel bill. It ends with "balance zero point zero zero". The AI took that zero as the total, instead of three hundred dollars ninety-six.

Mistake five, also from the stricter instructions: the copied example. Our instructions said "for example, zero seven". Six other lines came back numbered zero seven.

And one thing it never did: copy the line where it found the total. We asked for it every time. It ignored it every time. So that check, which sounds clever, gave us nothing.

## 10. What this means (7:25–8:20)

Here's what we take from this.

A free AI on an ordinary laptop is good at finding numbers on a receipt. In our test it found the right total on [nineteen] out of twenty — including the refund, the gift card and the dry cleaner's two dates.

It is bad at following a format. Not one line out of sixty came back exactly the way we asked.

"Better" instructions are not automatically better. Ours put most dates in one tidy format — and broke two totals and one date.

And the chat window and a direct request gave different answers to the same question. So don't trust our run. Trust your own run — and check it.

The cheapest check is the one we used: twenty receipts where you already know the answer. Run them first. If the AI gets them right, then try your own receipts.

## 11. Files and next time (8:20–8:45)

Everything is in the description: the twenty receipts, the answer key, the instructions, the checker page, and every line the AI wrote. Nothing is edited.

Next time: the same twenty receipts on five different free models — and which one fits an eight-gigabyte laptop.

This is Plain Laptop Lab. Free AI, ordinary laptop, every result checked.
