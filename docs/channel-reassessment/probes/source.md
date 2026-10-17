# Исходники видеопроб

Полный код обеих проб. Проект Remotion 4.0.507: положить файлы по путям из заголовков, шрифты Lato (SIL OFL 1.1) — в `public/fonts/` (Lato-Regular, Lato-Italic, Lato-Bold, Lato-Black). Внешних картинок, звуков и данных нет: всё нарисовано кодом.

Рендер (сервер без видеокарты, Chromium без окна):

```bash
bun install
./node_modules/.bin/remotion render src/index.ts quiz out/quiz-probe.mp4 --gl=swangle --concurrency=3 --timeout=120000
./node_modules/.bin/remotion render src/index.ts story out/story-probe.mp4 --gl=swangle --concurrency=3 --timeout=120000
```

Файлы в папке сжаты повторно для хранения: `ffmpeg -i <файл> -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -an -movflags faststart`. Пустая звуковая дорожка удалена.

## package.json

```json
{
  "name": "channel-probes",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@remotion/cli": "4.0.507",
    "remotion": "4.0.507",
    "react": "19.2.8",
    "react-dom": "19.2.8"
  },
  "devDependencies": {
    "@types/react": "19.2.14",
    "@types/react-dom": "19.2.3",
    "typescript": "5.9.3"
  }
}
```

## tsconfig.json

```json
{"compilerOptions":{"target":"ES2022","module":"ES2022","moduleResolution":"bundler","jsx":"react-jsx","strict":true,"skipLibCheck":true,"esModuleInterop":true,"lib":["DOM","ES2022"]},"include":["src"]}
```

## src/index.ts

```ts
import {registerRoot} from 'remotion';
import {Root} from './Root';
registerRoot(Root);
```

## src/Root.tsx

```tsx
import React from 'react';
import {Composition} from 'remotion';
import {Quiz, QUIZ_FRAMES} from './Quiz';
import {Story, STORY_FRAMES} from './Story';
export const Root: React.FC = () => <>
  <Composition id="quiz" component={Quiz} durationInFrames={QUIZ_FRAMES} fps={30} width={1920} height={1080} />
  <Composition id="story" component={Story} durationInFrames={STORY_FRAMES} fps={30} width={1920} height={1080} />
</>;
```

## src/common.tsx

```tsx
import React from 'react';
import {AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

export const FPS = 30;

export const fontFaces = `
@font-face {font-family: 'Lato'; font-weight: 400; src: url(${staticFile('fonts/Lato-Regular.ttf')});}
@font-face {font-family: 'Lato'; font-weight: 400; font-style: italic; src: url(${staticFile('fonts/Lato-Italic.ttf')});}
@font-face {font-family: 'Lato'; font-weight: 700; src: url(${staticFile('fonts/Lato-Bold.ttf')});}
@font-face {font-family: 'Lato'; font-weight: 900; src: url(${staticFile('fonts/Lato-Black.ttf')});}
`;

export const ease = Easing.bezier(0.33, 0, 0.2, 1);

// 0..1 between two frames with the channel's ease; clamped both sides.
export const ramp = (f: number, a: number, b: number) =>
  interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

export const useSpring = (delay: number, damping = 16, mass = 0.8) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: {damping, mass}});
};

// Future voiceover, shown as text until ElevenLabs is connected.
// Each line: [startFrame, endFrame, text].
export type Line = [number, number, string];
export const VoiceText: React.FC<{lines: Line[]; accent: string; ink?: string; bg?: string}> = ({lines, accent, ink = '#fff', bg = 'rgba(8,10,24,0.78)'}) => {
  const f = useCurrentFrame();
  const cur = lines.find(([a, b]) => f >= a && f < b);
  if (!cur) return null;
  const [a, b, text] = cur;
  const o = Math.min(ramp(f, a, a + 6), 1 - ramp(f, b - 6, b));
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 34, pointerEvents: 'none'}}>
      <div style={{opacity: o, display: 'flex', alignItems: 'center', gap: 18, background: bg, borderRadius: 14, padding: '14px 26px', maxWidth: 1500}}>
        <div style={{fontFamily: 'Lato', fontWeight: 900, fontSize: 17, letterSpacing: 2, color: accent, border: `2px solid ${accent}`, borderRadius: 6, padding: '4px 8px', whiteSpace: 'nowrap'}}>VOICEOVER TEXT</div>
        <div style={{fontFamily: 'Lato', fontWeight: 700, fontSize: 34, color: ink, lineHeight: 1.25}}>{text}</div>
      </div>
    </AbsoluteFill>
  );
};
```

## src/Quiz.tsx

```tsx
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {fontFaces, ramp, useSpring, VoiceText, Line} from './common';

// Probe: a pub-quiz round built entirely in code. Facts and sources are real (checked 2026-10-17).
const C = {bg0: '#0b0f26', bg1: '#1a2150', card: '#1d2452', line: '#33407f', ink: '#f6f1e3', dim: '#9aa3cf', amber: '#ffb648', ok: '#5fd39a', bad: '#e2647a'};
const W = 1920, H = 1080;

type Q = {start: number; n: number; text: string; options: string[]; correct: number; fact: React.FC<{t0: number}>; source: string};

// Timings inside a question, frames from its start.
const T = {card: 0, opts: 20, timer: 40, timerLen: 300, reveal: 340, row: 360, fact: 385, out: 530, len: 545};

const Background: React.FC = () => {
  const f = useCurrentFrame();
  const dots = Array.from({length: 18}, (_, i) => {
    const x = (i * 337) % W, y = (i * 211) % H, r = 120 + (i * 53) % 200;
    const dx = Math.sin(f / 140 + i) * 30, dy = Math.cos(f / 170 + i * 1.7) * 24;
    return <circle key={i} cx={x + dx} cy={y + dy} r={r} fill={i % 3 ? 'url(#soft1)' : 'url(#soft2)'} />;
  });
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 35%, ${C.bg1}, ${C.bg0} 75%)`}}>
      <svg width={W} height={H}>
        <defs>
          <radialGradient id="soft1"><stop offset="0" stopColor="#2c3790" stopOpacity="0.35" /><stop offset="1" stopColor="#2c3790" stopOpacity="0" /></radialGradient>
          <radialGradient id="soft2"><stop offset="0" stopColor="#5a3a8e" stopOpacity="0.3" /><stop offset="1" stopColor="#5a3a8e" stopOpacity="0" /></radialGradient>
        </defs>
        {dots}
      </svg>
    </AbsoluteFill>
  );
};

const Header: React.FC<{q: number}> = ({q}) => {
  const s = useSpring(0);
  return (
    <div style={{position: 'absolute', top: 36, left: 70, right: 70, display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      fontFamily: 'Lato', color: C.ink, opacity: s, transform: `translateY(${(1 - s) * -30}px)`}}>
      <div style={{fontWeight: 900, fontSize: 34, letterSpacing: 3}}>THE QUIZ HOUR<span style={{color: C.amber}}> ●</span></div>
      <div style={{display: 'flex', gap: 34, fontSize: 28, fontWeight: 700, color: C.dim}}>
        <span>ROUND 2 · PLANET EARTH</span>
        <span style={{color: C.ink}}>{q > 0 ? `Q${q} / 10` : '10 QUESTIONS'}</span>
      </div>
    </div>
  );
};

const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const a = useSpring(8), b = useSpring(22), c = useSpring(36);
  const out = 1 - ramp(f, 100, 120);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', fontFamily: 'Lato', color: C.ink, opacity: out}}>
      <div style={{fontSize: 40, fontWeight: 700, letterSpacing: 12, color: C.amber, opacity: a, transform: `translateY(${(1 - a) * 40}px)`}}>ROUND</div>
      <div style={{fontSize: 260, fontWeight: 900, lineHeight: 1, transform: `scale(${0.6 + 0.4 * b})`, opacity: b}}>2</div>
      <div style={{fontSize: 70, fontWeight: 900, letterSpacing: 4, opacity: c, transform: `translateY(${(1 - c) * 40}px)`}}>PLANET EARTH</div>
      <div style={{marginTop: 24, fontSize: 30, color: C.dim, opacity: c}}>10 questions · 10 seconds each · answers after every question</div>
    </AbsoluteFill>
  );
};

const Timer: React.FC<{t0: number}> = ({t0}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [t0 + T.timer, t0 + T.timer + T.timerLen], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const left = Math.ceil(10 * (1 - p));
  const appear = ramp(f, t0 + T.opts, t0 + T.timer);
  const gone = ramp(f, t0 + T.reveal, t0 + T.reveal + 15);
  const R = 62, L = 2 * Math.PI * R;
  const last = left <= 3 && p < 1;
  const pulse = last ? 1 + 0.06 * Math.sin(((f - t0) / 30) * Math.PI * 2) : 1;
  return (
    <div style={{position: 'absolute', left: 1640, top: 196, width: 160, height: 160, opacity: appear * (1 - gone), transform: `scale(${pulse})`}}>
      <svg width={160} height={160}>
        <circle cx={80} cy={80} r={R} stroke={C.line} strokeWidth={12} fill={C.card} />
        <circle cx={80} cy={80} r={R} stroke={last ? C.bad : C.amber} strokeWidth={12} fill="none" strokeLinecap="round"
          strokeDasharray={L} strokeDashoffset={L * p} transform="rotate(-90 80 80)" />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', fontFamily: 'Lato', fontWeight: 900, fontSize: 64, color: C.ink}}>{left}</div>
    </div>
  );
};

const Question: React.FC<{q: Q}> = ({q}) => {
  const f = useCurrentFrame();
  const t0 = q.start;
  const card = useSpring(t0 + T.card);
  const out = ramp(f, t0 + T.out, t0 + T.len);
  const rev = ramp(f, t0 + T.reveal, t0 + T.reveal + 10);
  const row = ramp(f, t0 + T.row, t0 + T.row + 30);
  return (
    <AbsoluteFill style={{opacity: 1 - out, transform: `translateX(${-out * 120}px)`}}>
      <div style={{position: 'absolute', left: 120, top: 150, width: 1480, minHeight: 230, background: C.card, border: `3px solid ${C.line}`, borderRadius: 28,
        padding: '34px 48px', boxSizing: 'border-box', fontFamily: 'Lato', color: C.ink, opacity: card, transform: `translateY(${(1 - card) * 60}px)`}}>
        <div style={{fontSize: 30, fontWeight: 900, letterSpacing: 6, color: C.amber}}>QUESTION {q.n}</div>
        <div style={{fontSize: 62, fontWeight: 900, lineHeight: 1.15, marginTop: 10}}>{q.text}</div>
      </div>
      <Timer t0={t0} />
      {q.options.map((o, i) => {
        const s = useSpring(t0 + T.opts + i * 6);
        const isOk = i === q.correct;
        // grid position -> row position after the reveal
        const gx = 120 + (i % 2) * 750, gy = 430 + Math.floor(i / 2) * 170, gw = 730, gh = 150;
        const rx = 120 + i * 375, ry = 420, rw = 355, rh = 104;
        const x = gx + (rx - gx) * row, y = gy + (ry - gy) * row, w = gw + (rw - gw) * row, h = gh + (rh - gh) * row;
        const bg = isOk && rev > 0 ? `rgba(95,211,154,${0.15 + 0.6 * rev})` : C.card;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 22, background: bg,
            border: `3px solid ${isOk && rev > 0 ? C.ok : C.line}`, display: 'flex', alignItems: 'center', gap: 22 - 8 * row, padding: `0 ${28 - 10 * row}px`, boxSizing: 'border-box',
            opacity: s * (isOk ? 1 : 1 - 0.65 * rev - 0.25 * Math.sin(Math.PI * row)), transform: `translateY(${(1 - s) * 50}px) scale(${isOk ? 1 + 0.04 * rev * (1 - row) : 1})`, fontFamily: 'Lato', color: C.ink}}>
            <div style={{width: 74 - 24 * row, height: 74 - 24 * row, borderRadius: 999, background: isOk && rev > 0 ? C.ok : C.amber, color: C.bg0, fontWeight: 900,
              fontSize: 40 - 12 * row, display: 'flex', justifyContent: 'center', alignItems: 'center', flexShrink: 0}}>{isOk && rev > 0.5 ? '✓' : 'ABCD'[i]}</div>
            <div style={{fontSize: 48 - 16 * row, fontWeight: 900, whiteSpace: 'nowrap'}}>{o}</div>
          </div>
        );
      })}
      <q.fact t0={t0} />
      <div style={{position: 'absolute', left: 124, top: 910, fontFamily: 'Lato', fontStyle: 'italic', fontSize: 24, color: C.dim, opacity: ramp(f, t0 + T.fact + 60, t0 + T.fact + 75)}}>{q.source}</div>
    </AbsoluteFill>
  );
};

// Fact 1: the Danube as one line, ten countries lit in order from source to delta.
const Danube: React.FC<{t0: number}> = ({t0}) => {
  const f = useCurrentFrame();
  const a = t0 + T.fact;
  const panel = ramp(f, a, a + 15);
  const draw = ramp(f, a + 5, a + 75);
  const path = 'M 60 170 C 220 120, 300 90, 420 120 S 600 210, 720 150 S 900 60, 1030 140 S 1200 250, 1330 170 S 1480 120, 1560 150';
  const L = 1700;
  const cc = ['DE', 'AT', 'SK', 'HU', 'HR', 'RS', 'RO', 'BG', 'MD', 'UA'];
  const pts = [[110, 152], [290, 103], [420, 120], [560, 178], [690, 160], [820, 105], [990, 118], [1140, 210], [1350, 168], [1520, 140]];
  const count = Math.floor(interpolate(f, [a + 10, a + 78], [0, 10], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  return (
    <div style={{position: 'absolute', left: 120, top: 560, width: 1680, height: 340, background: 'rgba(29,36,82,0.7)', borderRadius: 28, border: `3px solid ${C.line}`, opacity: panel, fontFamily: 'Lato', color: C.ink}}>
      <svg width={1680} height={300} style={{position: 'absolute', top: 40}}>
        <path d={path} stroke="#5fb8ff" strokeWidth={10} fill="none" strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - draw)} />
        {pts.map(([x, y], i) => {
          const s = ramp(f, a + 10 + i * 7, a + 18 + i * 7);
          return (
            <g key={i} opacity={s} transform={`translate(${x} ${y}) scale(${0.4 + 0.6 * s})`}>
              <circle r={24} fill={C.amber} />
              <text y={62} textAnchor="middle" fontFamily="Lato" fontWeight={900} fontSize={30} fill={C.ink}>{cc[i]}</text>
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', right: 40, top: 22, fontSize: 92, fontWeight: 900, color: C.amber}}>{count}<span style={{fontSize: 40, color: C.ink}}> countries</span></div>
    </div>
  );
};

// Fact 2: two squares to scale (area ratio 2.1 / 0.44).
const Smallest: React.FC<{t0: number}> = ({t0}) => {
  const f = useCurrentFrame();
  const a = t0 + T.fact;
  const panel = ramp(f, a, a + 15);
  const g1 = ramp(f, a + 10, a + 45), g2 = ramp(f, a + 40, a + 80);
  const big = 260, small = big * Math.sqrt(0.44 / 2.1);
  return (
    <div style={{position: 'absolute', left: 120, top: 560, width: 1680, height: 340, background: 'rgba(29,36,82,0.7)', borderRadius: 28, border: `3px solid ${C.line}`, opacity: panel, fontFamily: 'Lato', color: C.ink}}>
      <div style={{position: 'absolute', left: 120, bottom: 40, width: small * g1, height: small * g1, background: C.ok, borderRadius: 6}} />
      <div style={{position: 'absolute', left: 120, bottom: 40 + small + 16, fontSize: 30, fontWeight: 900, opacity: g1, whiteSpace: 'nowrap'}}>Vatican City<br /><span style={{color: C.ok}}>0.44 km²</span></div>
      <div style={{position: 'absolute', left: 520, bottom: 40, width: big * g2, height: big * g2, background: 'rgba(255,182,72,0.85)', borderRadius: 6}} />
      <div style={{position: 'absolute', left: 810, bottom: 40, fontSize: 30, fontWeight: 900, opacity: g2}}>Monaco, runner-up<br /><span style={{color: C.amber}}>2.1 km²</span></div>
      <div style={{position: 'absolute', right: 50, top: 40, width: 560, fontSize: 44, fontWeight: 900, lineHeight: 1.2, opacity: ramp(f, a + 85, a + 100)}}>
        Monaco is more than <span style={{color: C.amber}}>4×</span> bigger, and still the second-smallest country.
      </div>
    </div>
  );
};

const QS: Q[] = [
  {start: 120, n: 1, text: 'Which river flows through or along more countries than any other?', options: ['Nile', 'Danube', 'Amazon', 'Rhine'], correct: 1, fact: Danube,
    source: 'Source: UNDP/GEF Danube Regional Project — the Danube flows through or along the borders of 10 countries.'},
  {start: 665, n: 2, text: 'What is the smallest country in the world by area?', options: ['Monaco', 'San Marino', 'Vatican City', 'Liechtenstein'], correct: 2, fact: Smallest,
    source: 'Source: Encyclopaedia Britannica — Vatican City 0.44 km², Monaco 2.1 km² (rounded).'},
];

const EndCard: React.FC<{t0: number}> = ({t0}) => {
  const f = useCurrentFrame();
  const a = useSpring(t0), b = useSpring(t0 + 20), c = useSpring(t0 + 40);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', fontFamily: 'Lato', color: C.ink, opacity: ramp(f, t0, t0 + 10)}}>
      <div style={{fontSize: 36, letterSpacing: 10, color: C.amber, fontWeight: 900, opacity: a}}>END OF ROUND 2</div>
      <div style={{display: 'flex', gap: 30, marginTop: 30}}>
        {['Danube', 'Vatican City'].map((t, i) => (
          <div key={t} style={{background: C.card, border: `3px solid ${C.ok}`, borderRadius: 20, padding: '20px 36px', fontSize: 44, fontWeight: 900,
            opacity: i ? b : a, transform: `translateY(${(1 - (i ? b : a)) * 40}px)`}}>Q{i + 1} · {t}</div>
        ))}
      </div>
      <div style={{marginTop: 50, fontSize: 40, color: C.dim, opacity: c}}>Next: <span style={{color: C.ink, fontWeight: 900}}>Round 3 — Space</span></div>
    </AbsoluteFill>
  );
};

const lines: Line[] = [
  [8, 116, 'Round two: Planet Earth. Ten questions, ten seconds each. Keep your own score.'],
  [125, 245, 'Question one. Which river flows through or along more countries than any other?'],
  [245, 375, 'The Nile, the Danube, the Amazon, or the Rhine? Ten seconds.'],
  [375, 458, 'Three… two… one.'],
  [465, 590, 'It\'s the Danube: ten countries, more than any other river.'],
  [590, 660, 'From the Black Forest in Germany to its delta on the Black Sea, in Romania and Ukraine.'],
  [670, 785, 'Question two. What is the smallest country in the world by area?'],
  [785, 920, 'Monaco, San Marino, Vatican City, or Liechtenstein?'],
  [920, 1003, 'Three… two… one.'],
  [1010, 1135, 'Vatican City: about zero point four four square kilometres.'],
  [1135, 1205, 'Monaco, the runner-up, is more than four times bigger.'],
  [1215, 1345, 'That\'s round two. Note your score. Round three is all about space.'],
];

export const Quiz: React.FC = () => {
  const f = useCurrentFrame();
  const q = f < 120 ? 0 : f < 665 ? 1 : f < 1210 ? 2 : 2;
  return (
    <AbsoluteFill style={{background: C.bg0}}>
      <style>{fontFaces}</style>
      <Background />
      <Header q={q} />
      {f < 125 && <Intro />}
      {QS.map((x) => (f >= x.start && f < x.start + T.len + 2 ? <Question key={x.n} q={x} /> : null))}
      {f >= 1210 && <EndCard t0={1210} />}
      <VoiceText lines={lines} accent={C.amber} />
    </AbsoluteFill>
  );
};
export const QUIZ_FRAMES = 1350;
```

## src/Story.tsx

```tsx
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {fontFaces, ramp} from './common';

// Probe: a graded English story (A2). Original text. Scene drawn in code, camera follows the story.
// Word timing is a placeholder at 100 words per minute; ElevenLabs word timestamps replace it later.
const C = {ink: '#2a2238', paper: '#fbf6ec', dim: '#8c8296', accent: '#e0663a', hl: '#ffe3a3', line: '#e8dcc6'};
const FW = 18; // frames per word (100 wpm)
const GAP = 24; // pause after a sentence

type S = {text: string; cam: [number, number, number]; gloss?: [string, string]};
const SENT: S[] = [
  {text: 'Tom lives in a small house next to a lighthouse.', cam: [560, 760, 0.95], gloss: ['lighthouse', 'a tall tower with a strong light. It helps ships at night.']},
  {text: 'Every night, he climbs one hundred stairs to turn on the light.', cam: [700, 640, 1.0], gloss: ['climb', 'to go up something, step by step']},
  {text: 'His cat, Pepper, always climbs with him.', cam: [470, 920, 1.5]},
  {text: 'But tonight, Pepper is not at the door.', cam: [470, 920, 1.5]},
  {text: 'Tom looks under the bed. He looks in the garden. No cat.', cam: [260, 930, 1.25]},
  {text: 'Then he hears a small sound from the top of the tower.', cam: [700, 400, 1.6], gloss: ['tower', 'a tall, narrow building']},
];
const TITLE = 90;
const starts: number[] = [];
{
  let t = TITLE;
  for (const s of SENT) { starts.push(t); t += s.text.split(' ').length * FW + GAP; }
  starts.push(t);
}
const CHECK = starts[SENT.length];
export const STORY_FRAMES = CHECK + 150;

const useCam = () => {
  const f = useCurrentFrame();
  const keys: [number, [number, number, number]][] = [[0, [1000, 820, 0.62]], ...SENT.map((s, i) => [starts[i] + 4, s.cam] as [number, [number, number, number]]), [CHECK + 10, [900, 780, 0.7]]];
  let cam = keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t, k] = keys[i];
    const p = ramp(f, t, t + 40);
    if (p <= 0) break;
    cam = [cam[0] + (k[0] - cam[0]) * p, cam[1] + (k[1] - cam[1]) * p, cam[2] + (k[2] - cam[2]) * p];
  }
  return cam;
};

const Cat: React.FC<{x: number; y: number; s?: number; o?: number}> = ({x, y, s = 1, o = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} opacity={o} fill="#1d1a26">
    <ellipse cx={0} cy={-18} rx={26} ry={18} />
    <circle cx={22} cy={-40} r={13} />
    <path d="M 14 -50 L 16 -64 L 24 -52 Z M 26 -52 L 33 -63 L 34 -48 Z" />
    <path d="M -24 -14 C -46 -18, -46 -48, -30 -54" stroke="#1d1a26" strokeWidth={6} fill="none" strokeLinecap="round" />
  </g>
);

const Scene: React.FC = () => {
  const f = useCurrentFrame();
  const [cx, cy, z] = useCam();
  const lightOn = ramp(f, starts[1] + FW * 9, starts[1] + FW * 9 + 20); // "turn on the light"
  const dusk = ramp(f, 0, CHECK);
  const beamA = (f / 30) * 40;
  const stars = Array.from({length: 40}, (_, i) => [(i * 211) % 2000, (i * 97) % 600, 1 + (i % 3)]);
  const catAtDoor = f < starts[3] ? ramp(f, starts[2], starts[2] + 12) : 1 - ramp(f, starts[3], starts[3] + 10);
  const catTop = ramp(f, starts[5] + FW * 5, starts[5] + FW * 5 + 15);
  const waves = (k: number) => {
    let d = `M -200 ${1100 + k * 40}`;
    for (let x = -200; x <= 2400; x += 40) d += ` L ${x} ${1100 + k * 40 + Math.sin(x / 90 + f / (18 + k * 4) + k) * (6 + k * 2)}`;
    return d + ' L 2400 2200 L -200 2200 Z';
  };
  return (
    <svg width={1100} height={1080} viewBox="0 0 1100 1080">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={interpolate(dusk, [0, 1], [0, 1]) > 0.5 ? '#2b2a5c' : '#4b4a8c'} />
          <stop offset="0.6" stopColor="#c76b8a" />
          <stop offset="1" stopColor="#f6b26b" />
        </linearGradient>
        <radialGradient id="glow"><stop offset="0" stopColor="#fff3b0" stopOpacity="0.95" /><stop offset="1" stopColor="#fff3b0" stopOpacity="0" /></radialGradient>
        <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#fff6c8" stopOpacity="0.55" /><stop offset="1" stopColor="#fff6c8" stopOpacity="0" /></linearGradient>
      </defs>
      <g transform={`translate(550 540) scale(${z}) translate(${-cx} ${-cy})`}>
        <rect x={-600} y={-400} width={3200} height={2600} fill="url(#sky)" />
        {stars.map(([x, y, r], i) => <circle key={i} cx={x} cy={y} r={r} fill="#fff" opacity={dusk * (0.4 + 0.5 * Math.abs(Math.sin(f / 25 + i)))} />)}
        <circle cx={1500} cy={interpolate(f, [0, STORY_FRAMES], [930, 1010])} r={90} fill="#ffd27a" opacity={0.9} />
        <path d={waves(0)} fill="#3d5a8a" />
        <path d={waves(1)} fill="#2f4a78" />
        <path d={waves(2)} fill="#243c66" />
        <path d="M -400 960 L 180 950 L 420 970 L 860 985 L 1020 1010 L 1100 1120 L 1100 2200 L -400 2200 Z" fill="#3b3346" />
        <path d="M -400 975 L 180 965 L 420 985 L 860 1000 L 1020 1025" stroke="#5c8f5a" strokeWidth={22} fill="none" />
        {/* garden */}
        {[120, 160, 200, 240, 280].map((x) => <rect key={x} x={x} y={925} width={8} height={45} fill="#c9b08a" />)}
        <rect x={110} y={940} width={190} height={6} fill="#c9b08a" />
        {[150, 230].map((x, i) => <circle key={x} cx={x} cy={955} r={26 + i * 4} fill="#4f7a4a" />)}
        {/* house */}
        <rect x={300} y={860} width={260} height={110} fill="#efe2c8" />
        <path d="M 285 865 L 430 785 L 575 865 Z" fill="#a8453a" />
        <rect x={330} y={890} width={60} height={46} fill={`rgba(255,214,120,${0.5 + 0.5 * dusk})`} stroke="#6b5844" strokeWidth={5} />
        <rect x={450} y={895} width={50} height={75} fill="#6b4a36" />
        {/* lighthouse */}
        <path d="M 640 975 L 660 400 L 740 400 L 760 975 Z" fill="#f4efe6" />
        {[0, 1, 2, 3].map((i) => {
          const y0 = 470 + i * 130, y1 = y0 + 55;
          const xl = (y: number) => 640 + ((975 - y) / 575) * 20, xr = (y: number) => 760 - ((975 - y) / 575) * 20;
          return <path key={i} d={`M ${xl(y1)} ${y1} L ${xl(y0)} ${y0} L ${xr(y0)} ${y0} L ${xr(y1)} ${y1} Z`} fill="#c9453b" />;
        })}
        <rect x={645} y={390} width={110} height={14} fill="#2f2a36" />
        <rect x={662} y={330} width={76} height={60} fill="#fff3c4" opacity={0.35 + 0.65 * lightOn} />
        <path d="M 650 330 L 700 290 L 750 330 Z" fill="#2f2a36" />
        {lightOn > 0 && (
          <g opacity={lightOn}>
            <circle cx={700} cy={360} r={120} fill="url(#glow)" />
            <path d={`M 700 360 L ${700 + Math.cos((beamA * Math.PI) / 180) * 1400} ${360 + Math.sin((beamA * Math.PI) / 180) * 160 - 120} L ${700 + Math.cos((beamA * Math.PI) / 180) * 1400} ${360 + Math.sin((beamA * Math.PI) / 180) * 160 + 120} Z`} fill="url(#beam)" />
          </g>
        )}
        <Cat x={505} y={970} s={0.8} o={catAtDoor} />
        <Cat x={738} y={392} s={0.8} o={catTop} />
        {catTop > 0 && <text x={770} y={318} fontFamily="Lato" fontWeight={900} fontSize={30} fill="#fff" opacity={catTop * (0.6 + 0.4 * Math.sin(f / 6))}>meow</text>}
      </g>
    </svg>
  );
};

const Reading: React.FC = () => {
  const f = useCurrentFrame();
  const i = Math.max(0, starts.findIndex((t, k) => f >= t && f < starts[k + 1]));
  const inStory = f >= TITLE && f < CHECK;
  const s = SENT[i];
  const words = s.text.split(' ');
  const t0 = starts[i];
  const read = Math.floor((f - t0) / FW);
  const gl = s.gloss;
  const glIdx = gl ? words.findIndex((w) => w.toLowerCase().startsWith(gl[0])) : -1;
  const glOn = gl && glIdx >= 0 ? ramp(f, t0 + glIdx * FW + 6, t0 + glIdx * FW + 18) : 0;
  const prev = i > 0 && inStory ? SENT[i - 1].text : '';
  const enter = ramp(f, t0 - 2, t0 + 10);
  return (
    <div style={{position: 'absolute', left: 1100, top: 0, width: 820, height: 1080, background: C.paper, fontFamily: 'Lato', color: C.ink, boxSizing: 'border-box', padding: '70px 70px'}}>
      <div style={{display: 'flex', gap: 14, alignItems: 'center'}}>
        <div style={{background: C.accent, color: '#fff', fontWeight: 900, fontSize: 24, borderRadius: 8, padding: '6px 12px'}}>LEVEL 2 · A2</div>
        <div style={{fontSize: 26, color: C.dim, fontWeight: 700}}>The Keeper's Cat · Chapter 1</div>
      </div>
      <div style={{display: 'flex', gap: 6, marginTop: 22}}>
        {SENT.map((_, k) => <div key={k} style={{flex: 1, height: 8, borderRadius: 4, background: k < i || (!inStory && f >= CHECK) ? C.accent : k === i && inStory ? `linear-gradient(90deg, ${C.accent} ${Math.min(100, (read / words.length) * 100)}%, ${C.line} 0)` : C.line}} />)}
      </div>
      {f < TITLE && (
        <div style={{marginTop: 220, opacity: ramp(f, 5, 25) * (1 - ramp(f, TITLE - 12, TITLE))}}>
          <div style={{fontSize: 92, fontWeight: 900, lineHeight: 1}}>The Keeper's Cat</div>
          <div style={{fontSize: 34, color: C.dim, marginTop: 24}}>A short story in easy English · {SENT.reduce((n, x) => n + x.text.split(' ').length, 0)} words</div>
        </div>
      )}
      {inStory && (
        <>
          <div style={{marginTop: 70, minHeight: 90, fontSize: 32, lineHeight: 1.35, color: C.dim, opacity: 0.8 * enter}}>{prev}</div>
          <div style={{marginTop: 18, fontSize: 60, fontWeight: 900, lineHeight: 1.28, display: 'flex', flexWrap: 'wrap', columnGap: 10, rowGap: 6, opacity: enter, transform: `translateY(${(1 - enter) * 20}px)`}}>
            {words.map((w, k) => {
              const done = k < read, cur = k === read;
              const isGl = k === glIdx;
              return (
                <span key={k} style={{color: done || cur ? C.ink : '#b9b0c2', background: cur ? C.hl : 'transparent', borderRadius: 8, padding: '0 4px',
                  borderBottom: isGl && (done || cur) ? `5px solid ${C.accent}` : '5px solid transparent'}}>{w}</span>
              );
            })}
          </div>
          {gl && (
            <div style={{marginTop: 50, background: '#fff', border: `3px solid ${C.line}`, borderLeft: `10px solid ${C.accent}`, borderRadius: 14, padding: '22px 28px',
              opacity: glOn, transform: `translateY(${(1 - glOn) * 24}px)`}}>
              <div style={{fontSize: 34, fontWeight: 900, color: C.accent}}>{gl[0]}</div>
              <div style={{fontSize: 32, marginTop: 6, lineHeight: 1.3}}>{gl[1]}</div>
            </div>
          )}
        </>
      )}
      {f >= CHECK && (
        <div style={{marginTop: 160, opacity: ramp(f, CHECK, CHECK + 15)}}>
          <div style={{fontSize: 30, fontWeight: 900, letterSpacing: 4, color: C.accent}}>STOP AND THINK</div>
          <div style={{fontSize: 64, fontWeight: 900, lineHeight: 1.2, marginTop: 16}}>Where is Pepper? What do you think?</div>
          <div style={{fontSize: 30, color: C.dim, marginTop: 30}}>Say your answer out loud. Chapter 2 tells you.</div>
        </div>
      )}
      <div style={{position: 'absolute', left: 70, bottom: 50, right: 70, fontSize: 22, color: C.dim, display: 'flex', alignItems: 'center', gap: 12}}>
        <span style={{border: `2px solid ${C.dim}`, borderRadius: 6, padding: '3px 8px', fontWeight: 900, letterSpacing: 2, whiteSpace: 'nowrap'}}>VOICEOVER TEXT</span>
        <span>The highlighted text is what the voice will read. Silent probe: no voice yet.</span>
      </div>
    </div>
  );
};

export const Story: React.FC = () => (
  <AbsoluteFill style={{background: '#1d1a26'}}>
    <style>{fontFaces}</style>
    <Scene />
    <Reading />
  </AbsoluteFill>
);
```
