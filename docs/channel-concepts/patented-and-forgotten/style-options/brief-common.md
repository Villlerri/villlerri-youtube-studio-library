# Common part of every brief

## What this is

A design option for a new English-language YouTube channel, working name "Patented & Forgotten". Each episode tells the story of one forgotten device from the 1950s–2000s through its US patent drawing, laid out like a vintage magazine spread. The example episode for every option is the 8-inch floppy disk.

The channel owner's style, in their words (Russian, translated): "old magazines, big typography, texture, and so on". Their Pinterest board is the main reference: https://ru.pinterest.com/villlerriv/ютуб-идеи/ (a login modal may cover it; the pins are visible behind it). The board pictures are already downloaded for you: contact sheets with numbered pins, and single pins by number.

## Language

The person's request was in Russian. The channel itself is English-language, so all channel content (frame titles, captions, thumbnail text, banner) is in English. Every label on the page that explains the option to the owner (section headings like "Обложка выпуска", "Палитра", "Шрифты", short notes under frames) is in Russian.

## Real content to use (all facts verified, do not invent others)

- Device: 8-inch floppy disk. Patent US 3,668,658 "Magnetic record disk cover". Filed 22 Dec 1969, granted 6 Jun 1972. Inventors Ralph Flores and Herbert E. Thompson, assigned to IBM.
- Quote from the patent text: "A cover ... which additionally is rugged, inexpensive and mailable".
- Parts from FIG. 2 of the patent: 10 flexible disk with magnetic oxide coating; 20 vinyl top sheet, matte outside; 24 dusting fabric 3M 550, "pink wipe"; 27 oval window for the read head; 50 spacing layer between the sheets.
- History: 1967 work starts at IBM in San Jose; 1971 the 8-inch disk ships in the IBM 23FD drive, read-only, 80 KB; 1976 5¼-inch disk; 1982 3½-inch disk; 2011 Sony makes its last new floppy disks.
- Episode title ideas: "Floppy", "The plastic sleeve that made data portable", "80 KB in the mail".
- Channel slogan: "Forgotten tech, one drawing at a time." Monogram: PF.

## Pictures you may use (embed only as data URIs)

Ready data URIs are in text files next to each picture. Paste the file content into `src="..."` or `url(...)`. Use no other images. Never generate images; draw everything else with CSS or inline SVG.

- assets/fig2_ink.png: FIG. 2 exploded view of the floppy, black lines on a transparent background (1276×2369). Use with `mix-blend-mode: multiply` on light paper, or `filter: invert(1)` on dark.
- assets/fig2_full_sheet.png: the whole patent sheet 2 in grey, with "PATENTED JUN 6 1972" and "3,668,658" header (good as a collage or background layer).
- assets/fig1_sheet_gray.png: patent sheet 1, FIG. 1 perspective view, grey, large white margins.
- assets/photo_gray.jpg: public-domain photo crop of a real 8-inch floppy (hub hole and head slot). Credit line in frame: "Photo: Pamporoff, Wikimedia Commons, public domain".
- assets/photo_dots.png: the same photo as a dot halftone, transparent background.

No company logos anywhere (no IBM, Sony logos). Product names as plain text are fine.

## What the page must show

One self-contained HTML page, a style board for this option, about 1920 px wide, scrolling down:

1. Option name and one line on its idea (Russian).
2. Episode cover frame, 16:9, shown at 1600×900 or larger.
3. Drawing scene, 16:9: the patent figure with numbered callouts from the parts list.
4. One more 16:9 scene of your choice: big number, quote, or timeline.
5. Video thumbnail 1280×720, readable at small size.
6. Channel avatar (circle crop) and banner 2560×1440 with the text inside the central 1546×423 safe area (can be shown scaled).
7. Palette with hex codes and the two fonts, with Russian notes on how each is used.

Each 16:9 frame is a fixed-size box drawn with real layout, not a screenshot. Paper grain, halftone and print texture come from CSS or inline SVG filters (for example feTurbulence), not image files.
