# Приложение: код пробы музыки

Код, которым собрана [проба музыки](music.md). Приведён для проверки и пересборки; как программа в проект не входит. Писал ассистент в задаче 93, 2026-10-22.

## Порядок

1. Скачать 107 сэмплов VSCO 2 Community Edition (CC0) из репозитория [sgossner/VSCO-2-CE](https://github.com/sgossner/VSCO-2-CE), ветка master, 265 МБ. Список папок ниже.
2. `python -I trial.py <samples> <out> 93` — сочиняет три пьесы и пишет `master_float.wav`, `score.json` (каждая нота), `pieces.json` (аккорды и начало пьес).
3. `python -I finish.py <out>` — выравнивает громкость и пишет `trial.wav`, 48 кГц, 24 бита.
4. `python -I repcheck.py <out>` — считает повторы тактов и интервалы мелодии.
5. Проверка громкости: `ffmpeg -i trial.wav -af ebur128=peak=true -f null -`.
6. Ролик для альбома: `ffmpeg -f lavfi -i "color=c=0x1d2b53:s=1280x720:r=1" -i trial.wav -map 0:v -map 1:a -c:v libx264 -tune stillimage -crf 30 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest dog-music-trial.mp4`.

Окружение: Python 3.14.4, numpy 2.5.4, scipy 1.18.1, FFmpeg 6.0.1. Время на сервере студии (4 ядра): сочинение и рендер 14 с, громкость 23 с.

## Сэмплы

Из каждой папки взяты все файлы, кроме отмеченного:

- `Keys/Upright Piano`: 46 (только тихие слои `dyn1`, `dyn2`)
- `Strings/Cello Section/susvib`: 14 (только слой `v1`)
- `Strings/Harp`: 23
- `Strings/Viola Section/susvib`: 13 (только слой `v1`)
- `Strings/Violin Section/susVib`: 11 (только слой `v1`)

Названия нот проверены определением высоты. Клавиша фортепиано = 21 + 2 × номер файла. В названиях арфы среднее «до» — C4, у струнных — C3.

## trial.py

```python
"""Music trial for the dog channel: 10 minutes, three pieces, composed by code and played with VSCO 2 CE samples (CC0).

Run: python -I trial.py <samples_dir> <out_dir> [seed]
Writes <out_dir>/master_float.wav (48 kHz, 32-bit float, before loudness), score.json (every note), pieces.json.
Requirements from docs/dog-music-research/stage2.md, section 3: piano, harp and soft strings; 52-66 BPM;
mid register; no repeated passage; nothing above 16 kHz; even loudness; soft start and end.
"""
import sys, os, json, warnings
import numpy as np
from scipy.io import wavfile
from scipy import signal

warnings.simplefilter('ignore', wavfile.WavFileWarning)
SR = 48000
SAMPLES, OUT = sys.argv[1], sys.argv[2]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 93
os.makedirs(OUT, exist_ok=True)
PC = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


def midi_of(name, c4=4):
    """'F#3' -> MIDI number; c4 is the octave number the library gives middle C (harp 4, strings 3)."""
    return 12 * (int(name[-1]) + 1 + (4 - c4)) + PC[name[:-1]]


# ---------- sample library ----------

def sample_map():
    """inst -> list of (midi, file). Note names were checked by pitch detection: piano key = 21 + 2n,
    harp names use C4 = middle C, VSCO string names use C3 = middle C."""
    m = {}
    d = os.path.join(SAMPLES, 'Keys', 'Upright Piano')
    for layer in ('dyn1', 'dyn2'):
        m['piano_' + layer] = sorted((21 + 2 * int(f[-7:-4]), os.path.join(d, f)) for f in os.listdir(d) if f.startswith(f'Player_{layer}_'))
    d = os.path.join(SAMPLES, 'Strings', 'Harp')
    m['harp'] = sorted((midi_of(f.split('_')[1]), os.path.join(d, f)) for f in os.listdir(d))
    for inst, sub, pos in (('cello', 'Cello Section/susvib', 1), ('viola', 'Viola Section/susvib', 2), ('violin', 'Violin Section/susVib', 2)):
        d = os.path.join(SAMPLES, 'Strings', sub)
        m[inst] = sorted((midi_of(f.split('_')[pos], c4=3), os.path.join(d, f)) for f in os.listdir(d))
    return m


SMAP = sample_map()
_raw, _shift = {}, {}
MAXLEN = {'piano_dyn1': 12, 'piano_dyn2': 12, 'harp': 7, 'cello': 9, 'viola': 9, 'violin': 9}


def load(path, maxlen):
    """Read a sample as float32 stereo at SR, starting at its attack, at most maxlen seconds with a fade at the end."""
    if path in _raw: return _raw[path]
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / (2 ** 31 if x.dtype == np.int32 else 2 ** 15)
    if x.ndim == 1: x = np.stack([x, x], 1)
    a = np.abs(x).max(1)
    i = max(0, int(np.argmax(a > 0.003 * a.max())) - int(0.002 * sr))
    x = x[i:i + int(maxlen * sr)]
    if sr != SR: x = signal.resample_poly(x, SR // 300, sr // 300, axis=0).astype(np.float32)
    r = np.sqrt((x[:2 * SR] ** 2).mean(0)) + 1e-9
    x = x * (r.mean() / r)                               # equal left/right level: mic placement differs per note
    mid, side = x.mean(1), (x[:, 0] - x[:, 1]) / 2
    x = np.stack([mid + 0.7 * side, mid - 0.7 * side], 1).astype(np.float32)   # narrower stereo
    f = min(len(x), int(0.5 * SR)); x[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
    _raw[path] = x
    return x


def level_gains():
    """Even out recording level across notes: each sample scaled to its layer's median RMS of the first second."""
    g = {}
    for inst, lst in SMAP.items():
        r = {p: float(np.sqrt((load(p, MAXLEN[inst])[:SR] ** 2).mean())) for _, p in lst}
        med = float(np.median(list(r.values())))
        g.update({p: med / v for p, v in r.items()})
    return g


GAIN = level_gains()


def note_audio(inst, midi):
    """Nearest sample pitch-shifted to midi (FFT resampling), cached."""
    lst = SMAP[inst]
    m0, p = min(lst, key=lambda e: (abs(e[0] - midi), e[0]))
    k = (p, midi - m0)
    if k not in _shift:
        x = load(p, MAXLEN[inst])
        n = int(round(len(x) / 2 ** ((midi - m0) / 12)))
        y = x if n == len(x) else signal.resample(x, n, axis=0).astype(np.float32)
        _shift[k] = y * GAIN[p]
    return _shift[k]


# ---------- composition ----------

MAJOR = [0, 2, 4, 5, 7, 9, 11]
HALF = [[5, 3, 0, 4], [3, 0, 1, 4], [0, 5, 1, 4], [0, 3, 5, 4], [0, 3, 1, 4], [0, 2, 3, 4]]   # end on V
FULL = [[1, 4, 0, 0], [5, 1, 4, 0], [3, 4, 0, 0], [0, 2, 3, 0], [5, 3, 4, 0], [3, 1, 4, 0]]   # end on I
OPEN = [[0, 4, 5, 3], [3, 4, 2, 5], [5, 2, 3, 0], [0, 5, 3, 4]]


class Piece:
    def __init__(self, rng, key, bpm, meter):
        self.rng, self.key, self.bpm, self.meter = rng, key, bpm, meter
        self.notes, self.used = [], []

    def scale(self, lo, hi):
        return [m for m in range(lo, hi + 1) if (m - self.key) % 12 in MAJOR]

    def chord_pcs(self, root, color):
        degs = [root, root + 2, root + 4] + ({'7': [root + 6], '9': [root + 1]}.get(color, []))
        return [(self.key + MAJOR[d % 7]) % 12 for d in degs]

    def pick(self, bank):
        c = [p for p in bank if p not in self.used[-3:]]
        p = c[self.rng.integers(len(c))]
        self.used.append(p)
        return p

    def plan(self, sections):
        """List of bars: (root degree, colour). Sections of 8 bars: antecedent on V, consequent on I;
        every third section opens away from the tonic. Two closing bars on I."""
        bars = []
        for s in range(sections):
            first = self.pick(OPEN if s % 3 == 2 else HALF)
            for r in first + self.pick(FULL):
                bars.append((r, self.rng.choice(['', '', '9', '7']) if r in (0, 3) else ''))
        return bars + [(0, '9'), (0, '')]

    def timeline(self, nbars):
        """Bar start times with gentle rubato and a closing ritardando."""
        beat = 60 / self.bpm
        t, out = 0.0, []
        for b in range(nbars):
            f = 1 + 0.015 * np.sin(2 * np.pi * b / 8) + (0.06 if b == nbars - 3 else 0.14 if b >= nbars - 2 else 0)
            out.append((t, self.meter * beat * f))
            t += self.meter * beat * f
        return out

    def add(self, t, dur, midi, vel, inst, jitter=0.007, role='acc'):
        self.notes.append({'t': round(float(t + self.rng.normal(0, jitter)), 4), 'dur': round(float(dur), 4),
                           'midi': int(midi), 'vel': round(float(vel), 3), 'inst': inst, 'role': role})

    def melody(self, bars, times, lo, hi, inst, vel, rhythms, end_rhythms, rest_p=0.12):
        """Melody over the chord plan: chord tones on strong beats, steps between, an arch per 4-bar phrase,
        a cadence on the 2nd/5th degree (half cadence) or tonic/3rd (full); bars 5-6 of a section reuse
        the rhythm of bars 1-2 with new pitches."""
        rng, sc = self.rng, self.scale(lo, hi)
        cur = sc[len(sc) // 2]
        sect_rh = []
        for b, ((root, color), (t0, blen)) in enumerate(zip(bars, times)):
            pos = b % 8
            beat = blen / self.meter
            last = pos in (3, 7) or b >= len(bars) - 2
            if b >= len(bars) - 2:
                rh = [self.meter] if b == len(bars) - 1 else end_rhythms[0]
            elif pos in (4, 5) and len(sect_rh) > pos - 4:
                rh = sect_rh[pos - 4]
            else:
                bank = end_rhythms if last else rhythms
                rh = list(bank[rng.integers(len(bank))])
                if not last and rng.random() < rest_p: rh = [-rh[0]] + rh[1:]
            if pos < 2: sect_rh = (sect_rh if pos == 1 else []) + [rh]
            chord = self.chord_pcs(root, color)
            phrase_pos = (b % 4) / 3
            peak = lo + (hi - lo) * (0.55 + 0.25 * np.sin(np.pi * ((b // 4) % 3) / 2))
            target = lo + (hi - lo) * 0.35 + (peak - lo - (hi - lo) * 0.35) * np.sin(np.pi * phrase_pos)
            beat_pos = 0.0
            for i, d in enumerate(rh):
                if d < 0: beat_pos += -d; continue
                strong = beat_pos == 0 or (self.meter == 4 and beat_pos == 2)
                final = last and i == len(rh) - 1
                if final:
                    tones = [m for m in sc if m % 12 in chord]
                    rest = (0, 4) if (pos == 7 or b >= len(bars) - 2) else (2, 7)
                    cand = [m for m in tones if (m - self.key) % 12 in rest] or tones
                elif strong:
                    cand = [m for m in sc if m % 12 in chord]
                else:
                    j = sc.index(min(sc, key=lambda m: abs(m - cur)))
                    cand = sc[max(0, j - 2): j + 3]
                    cand = [m for m in cand if m != cur] or cand
                def cost(m):
                    leap = abs(m - cur)
                    return (abs(m - target) * 0.35 + leap * (0.25 if leap <= 7 else 0.7) + (1.3 if m == cur else 0)
                            + rng.random() * 1.6)
                m = min(cand, key=cost)
                v = vel * (0.92 + 0.12 * (m - lo) / (hi - lo)) * (0.85 if final else 1) * rng.uniform(0.94, 1.04)
                self.add(t0 + beat_pos * beat, d * beat, m, v, inst, role='mel')
                cur, beat_pos = m, beat_pos + d

    def bass_root(self, root, prev, lo, hi):
        pc = (self.key + MAJOR[root % 7]) % 12
        c = [m for m in range(lo, hi + 1) if m % 12 == pc]
        return min(c, key=lambda m: abs(m - prev)) if prev else c[0]

    def piano_lh(self, bars, times, pattern_bank, vel=0.3):
        """Broken-chord left hand. Pattern items: (beat, interval above the root); 'T' = tenth, 'N' = ninth."""
        prev, pat = None, None
        for b, ((root, color), (t0, blen)) in enumerate(zip(bars, times)):
            if b % 8 == 0: pat = pattern_bank[self.rng.integers(len(pattern_bank))]
            if b >= len(bars) - 2: pat = [(0, 0), (1, 7), (2, 'T')] if b == len(bars) - 2 else [(0, 0), (0, 7), (0, 'T')]
            r = self.bass_root(root, prev, 36, 47); prev = r
            third = (self.chord_pcs(root, '')[1] - r) % 12
            beat = blen / self.meter
            for k, (bt, iv) in enumerate(pat):
                semis = {'T': third + 12, 'N': 14, 'O': 12, 'S': 11 if third == 4 else 10}.get(iv, iv)
                if iv == 'S' and color != '7': semis = 12
                if iv == 'N' and color != '9': semis = 7
                self.add(t0 + bt * beat, blen - bt * beat, r + semis, vel * (1.12 if k == 0 else 1) * self.rng.uniform(0.92, 1.05), 'piano', 0.005)

    def strings(self, bars, times, voices, vel=0.3):
        """Sustained chord per bar; a voice keeps a common tone instead of re-bowing."""
        held = {}
        for b, ((root, color), (t0, blen)) in enumerate(zip(bars, times)):
            pcs = self.chord_pcs(root, '')
            for inst, lo, hi, which in voices:
                pc = pcs[which]
                c = [m for m in range(lo, hi + 1) if m % 12 == pc]
                prev = held.get(inst)
                m = min(c, key=lambda x: abs(x - prev['midi'])) if prev else c[len(c) // 2]
                if prev and prev['midi'] == m and prev['dur'] + blen < 8.0:
                    prev['dur'] += blen; continue
                self.add(t0, blen + 0.25, m, vel * self.rng.uniform(0.95, 1.03), inst, 0.02)
                held[inst] = self.notes[-1]

    def harp_arp(self, bars, times, pattern_bank, vel=0.32):
        prev, pat = None, None
        for b, ((root, color), (t0, blen)) in enumerate(zip(bars, times)):
            if b % 8 == 0: pat = pattern_bank[self.rng.integers(len(pattern_bank))]
            if b == len(bars) - 1: pat = [(0, 0), (0.25, 7), (0.5, 12), (0.75, 'T'), (1, 19)]
            r = self.bass_root(root, prev, 38, 47); prev = r
            third = (self.chord_pcs(root, '')[1] - r) % 12
            beat = blen / self.meter
            for k, (bt, iv) in enumerate(pat):
                semis = {'T': third + 12, 'T2': third + 24}.get(iv, iv)
                self.add(t0 + bt * beat, 3.5, r + semis, vel * (1.1 if k == 0 else 0.95) * self.rng.uniform(0.92, 1.05), 'harp', 0.01)


R4 = [[2, 2], [3, 1], [1, 1, 2], [2, 1, 1], [1, 2, 1], [1.5, 0.5, 2], [2, 1.5, 0.5]]
E4 = [[4], [2, 2], [1, 1, 2], [3, 1]]
R3 = [[2, 1], [1, 2], [3], [1, 1, 1], [1.5, 0.5, 1]]
E3 = [[3], [1, 2], [2, 1]]


def piece_a(rng):
    """Solo piano, F major, 60 BPM, 4/4."""
    p = Piece(rng, 5, 60, 4)
    bars = p.plan(7); times = p.timeline(len(bars))
    p.melody(bars, times, 62, 79, 'piano', 0.5, R4, E4[:3])
    p.piano_lh(bars, times, [[(0, 0), (0.5, 7), (1, 'T'), (1.5, 7), (2, 'O'), (2.5, 7), (3, 'T'), (3.5, 7)],
                             [(0, 0), (1, 7), (1.5, 'T'), (2, 'N'), (3, 7)],
                             [(0, 0), (1, 'T'), (2, 7), (3, 'S')]])
    return p, times, bars


def piece_b(rng):
    """Harp with soft cello and viola, D major, 52 BPM, 3/4."""
    p = Piece(rng, 2, 52, 3)
    bars = p.plan(6); times = p.timeline(len(bars))
    p.harp_arp(bars, times, [[(0, 0), (0.5, 7), (1, 12), (1.5, 'T'), (2, 19), (2.5, 'T')],
                             [(0, 0), (1, 7), (1.5, 'T'), (2, 12)],
                             [(0, 0), (0.5, 'T'), (1, 19), (2, 'T2')]])
    p.melody(bars, times, 70, 84, 'harp', 0.42, [[3], [2, 1], [1, 2]], [[3]], rest_p=0.3)
    p.strings(bars, times, [('cello', 38, 52, 0), ('viola', 50, 64, 2)], 0.26)
    return p, times, bars


def piece_c(rng, sections):
    """Piano with soft strings, E-flat major, 66 BPM, 4/4. Strings enter after 8 bars."""
    p = Piece(rng, 3, 66, 4)
    bars = p.plan(sections); times = p.timeline(len(bars))
    p.melody(bars, times, 63, 80, 'piano', 0.48, R4, E4[:3])
    p.piano_lh(bars, times, [[(0, 0), (1, 7), (2, 'T'), (3, 7)], [(0, 0), (1.5, 'T'), (2, 7), (3, 'O')]], 0.27)
    s0 = 8
    p.strings(bars[s0:], times[s0:], [('cello', 36, 50, 0), ('viola', 52, 64, 1), ('violin', 62, 74, 2)], 0.22)
    return p, times, bars


# ---------- rendering ----------

ATTACK = {'piano': 0.0, 'harp': 0.0, 'cello': 0.9, 'viola': 0.9, 'violin': 1.1}
RELEASE = {'piano': 0.45, 'harp': 0.9, 'cello': 1.6, 'viola': 1.6, 'violin': 1.8}
LEVEL = {'piano': 1.0, 'harp': 0.9, 'cello': 0.55, 'viola': 0.5, 'violin': 0.38}
PAN = {'piano': 0.0, 'harp': -0.2, 'cello': 0.3, 'viola': 0.1, 'violin': -0.25}


def pedal(notes, times):
    """Piano sustain pedal: change at each bar line, 80 ms after the new bar starts; last bar rings 5.5 s."""
    ends = [t + d for t, d in times]
    for n in notes:
        if n['inst'] != 'piano': continue
        b = max(i for i, (t, _) in enumerate(times) if t <= n['t'] + 0.05)
        n['dur'] = (ends[b] + 0.08 - n['t']) if b < len(times) - 1 else 5.5


def render(notes, length):
    out = np.zeros((int(length * SR), 2), np.float32)
    for n in notes:
        inst = n['inst']
        layer = inst if inst != 'piano' else ('piano_dyn1' if n['vel'] < 0.42 else 'piano_dyn2')
        x = note_audio(layer, n['midi'])
        a, r = ATTACK[inst], RELEASE[inst]
        dur = max(n['dur'], 3.0) if inst == 'harp' else n['dur']
        L = min(len(x), int((dur + r) * SR))
        env = np.ones(L, np.float32)
        ka = min(L, int(a * SR))
        if ka: env[:ka] = np.linspace(0, 1, ka) ** 1.5
        kr = min(L, int(r * SR)); env[L - kr:] *= np.linspace(1, 0, kr) ** 2
        v = n['vel'] ** 1.4 * LEVEL[inst] * (2.2 if layer == 'piano_dyn1' else 1.0)
        pan = PAN[inst]
        g = np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)], np.float32) * np.sqrt(2)
        i = int(max(0, n['t']) * SR)
        seg = x[:L] * env[:, None] * (v * g)
        j = min(len(out), i + L)
        out[i:j] += seg[:j - i]
    return out


def reverb_ir(rng, sec=3.2):
    """Synthetic hall: decaying noise in three bands, darker as it decays; 18 ms pre-delay."""
    n = int(sec * SR); t = np.arange(n) / SR
    ir = np.zeros((n, 2), np.float32)
    for (lo, hi), rt in (((60, 700), 2.4), ((700, 3500), 1.9), ((3500, 9000), 0.9)):
        sos = signal.butter(4, [lo, hi], 'bandpass', fs=SR, output='sos')
        noise = signal.sosfilt(sos, rng.standard_normal((n, 2)), axis=0)
        ir += (noise * np.exp(-6.91 * t / rt)[:, None]).astype(np.float32)
    ir = np.concatenate([np.zeros((int(0.018 * SR), 2), np.float32), ir])
    return ir / np.sqrt((ir ** 2).sum(0))


def main():
    rng = np.random.default_rng(SEED)
    total, ring = 600.0, 5.0
    ir = reverb_ir(np.random.default_rng(SEED + 1))
    master = np.zeros((int((total + 12) * SR), 2), np.float32)
    pieces, notes_all, start = [], [], 0.0
    for name, fn in (('A: фортепиано', piece_a), ('B: арфа, виолончели, альты', piece_b), ('C: фортепиано и струнные', piece_c)):
        if fn is piece_c:
            bar = 4 * 60 / 66
            fn = lambda r, n=int(round(((total - start - ring) / bar - 2.5) / 8)): piece_c(r, n)
        p, times, bars = fn(rng)
        pedal(p.notes, times)
        dry = render(p.notes, times[-1][0] + ring + 4)
        wet = np.stack([signal.oaconvolve(dry[:, c], ir[:, c])[:len(dry)] for c in range(2)], 1).astype(np.float32)
        mix = dry * 0.82 + wet * 0.42
        k = 6 * SR                                       # each piece swells in over 6 s from -8 dB
        mix[:k] *= (0.4 + 0.6 * (1 - np.cos(np.linspace(0, np.pi, k, dtype=np.float32))) / 2)[:, None]
        i = int(start * SR); j = min(len(master), i + len(mix))
        master[i:j] += mix[:j - i]
        pieces.append({"name": name, "start_s": round(float(start), 1), 'bars': len(bars), 'bpm': p.bpm, 'meter': p.meter,
                       'key_pc': p.key, 'notes': len(p.notes), 'chords': [list(b) for b in bars]})
        notes_all += [dict(n, t=round(n['t'] + start, 4), piece=name[0]) for n in p.notes]
        start += times[-1][0] + ring
    length = min(total, start + 2)
    master = master[:int(length * SR)]
    lp = signal.butter(8, 15500, 'lowpass', fs=SR, output='sos')
    hp = signal.butter(2, 35, 'highpass', fs=SR, output='sos')
    for c in range(2):
        master[:, c] = signal.sosfilt(hp, signal.sosfilt(lp, master[:, c]))
    fi, fo = int(20 * SR), int(30 * SR)
    master[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None] ** 2
    master[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None] ** 2
    wavfile.write(os.path.join(OUT, 'master_float.wav'), SR, master)
    json.dump({'seed': SEED, 'length_s': round(length, 2), 'pieces': pieces}, open(os.path.join(OUT, 'pieces.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(notes_all, open(os.path.join(OUT, 'score.json'), 'w'), ensure_ascii=False)
    print('length', round(length, 1), 's; pieces', [(q['name'], q['start_s'], q['bars'], q['notes']) for q in pieces])


if __name__ == '__main__':
    main()

```

## finish.py

```python
"""Loudness for the trial: slow leveller, -18 LUFS, true-peak limit -2.5 dBTP, 24-bit WAV.

Run: python -I finish.py <out_dir>   (reads master_float.wav from trial.py, writes trial.wav)
Loudness follows ITU-R BS.1770 (K-weighting, 400 ms blocks, gating); ffmpeg ebur128 gives the official numbers.
"""
import sys, os
import numpy as np
from scipy.io import wavfile
from scipy import signal

OUT = sys.argv[1]
TARGET, CEIL = -18.0, -2.5
sr, x = wavfile.read(os.path.join(OUT, 'master_float.wav'))
x = x.astype(np.float32)


def kweight(y):
    """BS.1770 pre-filter (shelf + RLB high-pass), coefficients for 48 kHz."""
    y = signal.lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585], y, axis=0)
    return signal.lfilter([1, -2, 1], [1, -1.99004745483398, 0.99007225036621], y, axis=0)


def blocks(y, win, hop):
    """Loudness (LUFS) of windows of win seconds every hop seconds."""
    z = sum(kweight(y[:, ch].astype(np.float64)) ** 2 for ch in range(y.shape[1]))
    c = np.cumsum(z); n, h = int(win * sr), int(hop * sr)
    ms = (c[n::h] - c[:-n:h][:len(c[n::h])]) / n
    return -0.691 + 10 * np.log10(np.maximum(ms, 1e-12))


def integrated(y):
    L = blocks(y, 0.4, 0.1)
    L = L[L > -70]
    rel = -0.691 + 10 * np.log10(np.mean(10 ** ((L + 0.691) / 10))) - 10
    L = L[L > rel]
    return -0.691 + 10 * np.log10(np.mean(10 ** ((L + 0.691) / 10)))


# 1. Slow leveller: short-term loudness (3 s) pulled 70% toward the programme level, at most 5 dB, 6 s smoothing.
#    Fade-in (20 s) and fade-out (30 s) keep the gain of their edges, so the fades stay fades.
hop = 0.5
S = blocks(x, 3.0, hop)
I0 = integrated(x)
g = np.clip((I0 - S) * 0.7, -5, 5)
a, b = int(23 / hop), len(g) - int(33 / hop)
g[:a], g[b:] = g[a], g[b]
k = int(6 / hop); g = np.convolve(np.pad(g, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
t_g = (np.arange(len(g)) * hop + 1.5) * sr
gain = 10 ** (np.interp(np.arange(len(x)), t_g, g) / 20)
x *= gain[:, None]

# 2. Programme loudness to -18 LUFS.
x *= 10 ** ((TARGET - integrated(x)) / 20)

# 3. Limiter on the 4x oversampled peak: 30 ms look-ahead and hold, 8 ms smoothing, 150 ms release.
from scipy.ndimage import maximum_filter1d
pk = np.zeros(len(x), np.float32)
step, pad = 10 * sr, 2000
for ch in range(2):
    for s0 in range(0, len(x), step):
        a0, b0 = max(0, s0 - pad), min(len(x), s0 + step + pad)
        u = np.abs(signal.resample_poly(x[a0:b0, ch], 4, 1)).reshape(-1, 4).max(1)
        pk[s0:s0 + step] = np.maximum(pk[s0:s0 + step], u[s0 - a0: s0 - a0 + step][:len(pk[s0:s0 + step])])
ceil = 10 ** (CEIL / 20)
r = np.maximum(0, np.log(np.maximum(pk, 1e-9) / ceil))
hold = maximum_filter1d(r, 2 * int(0.03 * sr) + 1)
a1 = np.exp(-1 / (0.008 * sr)); sm = signal.filtfilt([1 - a1], [1, -a1], hold)
rel = np.exp(-1 / (0.15 * sr)); rl = signal.lfilter([1 - rel], [1, -rel], sm)
env = np.exp(-np.maximum(np.maximum(r, sm), rl)).astype(np.float32)
x *= env[:, None]
print('limiter: share of time reduced %.4f, max reduction dB %.2f' % ((env < 0.999).mean(), -20 * np.log10(env.min())))

# 4. TPDF dither (fixed seed) and 24-bit write.
rng = np.random.default_rng(930)
q = 2 ** 23
d = (rng.random(x.shape) - rng.random(x.shape))
y = np.clip(np.round(x.astype(np.float64) * (q - 1) + d), -q, q - 1).astype(np.int32)
wavfile.write(os.path.join(OUT, 'trial.wav'), sr, (y << 8).astype(np.int32))
print('leveller gain dB min %.1f max %.1f; integrated before %.1f' % (g.min(), g.max(), I0))

```

## repcheck.py

```python
"""Repetition check of the trial score: identical bars and identical 2- and 4-bar passages, full texture and top voice."""
import json, sys, numpy as np, collections
S = json.load(open(sys.argv[1] + '/score.json')); P = json.load(open(sys.argv[1] + '/pieces.json'))['pieces']
for p in P:
    n, beat = p['bars'], 60 / p['bpm']
    t, starts = p['start_s'], []
    for b in range(n):
        f = 1 + 0.015 * np.sin(2 * np.pi * b / 8) + (0.06 if b == n - 3 else 0.14 if b >= n - 2 else 0)
        starts.append((t, p['meter'] * beat * f)); t += p['meter'] * beat * f
    notes = [s for s in S if s['piece'] == p['name'][0]]
    full, top = collections.defaultdict(list), collections.defaultdict(list)
    for s in notes:
        b = max(i for i, (t0, _) in enumerate(starts) if t0 <= s['t'] + 0.05)
        t0, bl = starts[b]
        key = (s['inst'], s['midi'], round((s['t'] - t0) / (bl / p['meter']) * 4) / 4)
        full[b].append(key)
        if s['role'] == 'mel': top[b].append(key)
    def dup(sig, w):
        seen, d = {}, 0
        for b in range(n - w + 1):
            k = tuple(tuple(sorted(sig[b + i])) for i in range(w))
            if not any(k): continue
            if k in seen: d += 1
            else: seen[k] = b
        return d
    print(p['name'], 'bars', n, '| full texture: same bar', dup(full, 1), ', same 2 bars', dup(full, 2), ', same 4 bars', dup(full, 4),
          '| melody: same bar', dup(top, 1), ', same 2 bars', dup(top, 2), ', same 4 bars', dup(top, 4))
iv = np.concatenate([np.abs(np.diff([s['midi'] for s in sorted(S, key=lambda s: s['t']) if s['role'] == 'mel' and s['piece'] == q])) for q in 'ABC'])
print('melody intervals: n', len(iv), 'steps<=2', round(float((iv <= 2).mean()), 2), 'thirds 3-4', round(float(((iv >= 3) & (iv <= 4)).mean()), 2), 'leaps 5-7', round(float(((iv >= 5) & (iv <= 7)).mean()), 2), '>7', int((iv > 7).sum()), 'same note', round(float((iv == 0).mean()), 2))

```
