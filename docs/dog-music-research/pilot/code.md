# Приложение: код пилотного ролика

Код, которым собран [пилотный ролик](passport.md). Приведён для проверки и пересборки; как программа в проект не входит. Писал ассистент в задаче 93, 2026-10-22. Основа — код [пробы музыки](../trial/code.md): правила сочинения, сэмплы и звук те же.

## Порядок

1. Сэмплы — те же 107 файлов VSCO 2 Community Edition (CC0), что в пробе: список и источник в [trial/code.md](../trial/code.md#сэмплы).
2. `python -I pilot.py <samples> out 93 10` — план из 155 пьес, сочинение, рендер окнами по 3 минуты, громкость, 24-битный PCM в FFmpeg. Пишет `audio.m4a` (AAC 256 кбит/с), `pcm.sha256`, `pieces.json`, `score.json`, `stats.npz`.
3. `bash loop.sh 0 4320 video/seg0.mp4` и `bash loop.sh 4320 8640 video/seg1.mp4` — две половины петли картинки, параллельно.
4. `bash assemble.sh <начала отрывков в секундах>` — склейка петли, ролик на 10 часов без перекодирования картинки, отрывки для альбома, замер громкости.
5. `python -I check.py out` — повторы, интервалы мелодии, регистр, паузы, разброс громкости.
6. Обложка: команда в конце этого документа.

Окружение: Python 3.14.4, numpy 2.5.4, scipy 1.18.1, FFmpeg 6.0.1 (libx264, встроенный AAC). Шрифт обложки — Lato (SIL OFL 1.1), системный пакет `fonts-lato`.

## pilot.py

```python
"""Pilot audio for the dog channel: 10 hours, every piece new, composed by code and played with VSCO 2 CE samples (CC0).

Run: python -I pilot.py <samples_dir> <out_dir> [seed] [hours]
Writes <out_dir>/audio.m4a (AAC 256 kbit/s, through ffmpeg on PATH), pcm.sha256 (hash of the 24-bit PCM before AAC),
pieces.json, score.json, stats.npz.
Rules and sound are those of the trial (tmp/trial/trial.py, heard and accepted by Villlerri on 2026-10-22); new here:
a plan of ~165 pieces with their own key, tempo, metre and texture; loudness processed in 5-minute windows,
so 10 hours never sit in memory; fade-in 30 s, fade-out 12 min (stage2.md, section 3).
"""
import sys, os, json, warnings, hashlib, subprocess, collections
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import maximum_filter1d

warnings.simplefilter('ignore', wavfile.WavFileWarning)
SR = 48000
SAMPLES, OUT = sys.argv[1], sys.argv[2]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 93
HOURS = float(sys.argv[4]) if len(sys.argv) > 4 else 10
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
_shift, CACHE_BYTES = collections.OrderedDict(), 300e6
# Piano notes never sound longer than 6.7 s (last bar 5.5 s + release, pitch shift), so 8 s of sample is enough.
MAXLEN = {'piano_dyn1': 8, 'piano_dyn2': 8, 'harp': 7, 'cello': 9, 'viola': 9, 'violin': 9}


def load(path, maxlen):
    """Read a sample as float32 stereo at SR, starting at its attack, at most maxlen seconds with a fade at the end."""
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
    """Nearest sample pitch-shifted to midi (FFT resampling); least recently used notes leave the cache."""
    lst = SMAP[inst]
    m0, p = min(lst, key=lambda e: (abs(e[0] - midi), e[0]))
    k = (p, midi - m0)
    if k in _shift:
        _shift.move_to_end(k)
        return _shift[k]
    x = load(p, MAXLEN[inst])
    n = int(round(len(x) / 2 ** ((midi - m0) / 12)))
    y = x if n == len(x) else signal.resample(x, n, axis=0).astype(np.float32)
    _shift[k] = y * GAIN[p]
    while sum(v.nbytes for v in _shift.values()) > CACHE_BYTES: _shift.popitem(last=False)
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
            r = self.bass_root(root, prev, 36, 47); prev = r   # 36: C major needs C2
            third = (self.chord_pcs(root, '')[1] - r) % 12
            beat = blen / self.meter
            for k, (bt, iv) in enumerate(pat):
                semis = {'T': third + 12, 'T2': third + 24}.get(iv, iv)
                self.add(t0 + bt * beat, 3.5, r + semis, vel * (1.1 if k == 0 else 0.95) * self.rng.uniform(0.92, 1.05), 'harp', 0.01)


R4 = [[2, 2], [3, 1], [1, 1, 2], [2, 1, 1], [1, 2, 1], [1.5, 0.5, 2], [2, 1.5, 0.5]]
E4 = [[4], [2, 2], [1, 1, 2], [3, 1]]
R3 = [[2, 1], [1, 2], [3], [1, 1, 1], [1.5, 0.5, 1]]
E3 = [[3], [1, 2], [2, 1]]
# Left hand: the trial's piece A patterns, then piece C patterns; 3/4 versions are new.
LH4 = [[(0, 0), (0.5, 7), (1, 'T'), (1.5, 7), (2, 'O'), (2.5, 7), (3, 'T'), (3.5, 7)],
       [(0, 0), (1, 7), (1.5, 'T'), (2, 'N'), (3, 7)],
       [(0, 0), (1, 'T'), (2, 7), (3, 'S')],
       [(0, 0), (1, 7), (2, 'T'), (3, 7)],
       [(0, 0), (1.5, 'T'), (2, 7), (3, 'O')]]
LH3 = [[(0, 0), (1, 7), (2, 'T')],
       [(0, 0), (0.5, 7), (1, 'T'), (1.5, 7), (2, 'O'), (2.5, 7)],
       [(0, 0), (1, 'T'), (2, 7)],
       [(0, 0), (1, 7), (1.5, 'T'), (2, 'O')]]
# Harp: the trial's piece B patterns (3/4); 4/4 versions are new.
HARP3 = [[(0, 0), (0.5, 7), (1, 12), (1.5, 'T'), (2, 19), (2.5, 'T')],
         [(0, 0), (1, 7), (1.5, 'T'), (2, 12)],
         [(0, 0), (0.5, 'T'), (1, 19), (2, 'T2')]]
HARP4 = [[(0, 0), (0.5, 7), (1, 12), (1.5, 'T'), (2, 19), (2.5, 'T'), (3, 12), (3.5, 7)],
         [(0, 0), (1, 7), (1.5, 'T'), (2, 12), (3, 'T')],
         [(0, 0), (0.5, 'T'), (1, 19), (2, 'T2'), (3, 19)]]
HM3, HE3 = [[3], [2, 1], [1, 2]], [[3]]
HM4, HE4 = [[4], [2, 2], [3, 1], [2, 1, 1]], [[4]]

# Textures of the trial: A piano solo, B harp with cellos and violas, C piano with strings.
TEXTURES = {'piano': (0.4, (56, 64), 0.7), 'harp': (0.3, (50, 56), 0.3), 'piano_strings': (0.3, (60, 66), 0.7)}  # share, BPM, P(4/4)
KEYS = [0, 2, 3, 4, 5, 7, 8, 9, 10]                      # C D Eb E F G Ab A Bb major
KEY_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def choose_spec(rng, prev):
    """Texture other than the previous piece's; key other than the previous two; tempo and metre per texture."""
    tex = [t for t in TEXTURES if not prev or t != prev[-1]['texture']]
    w = np.array([TEXTURES[t][0] for t in tex]); t = tex[rng.choice(len(tex), p=w / w.sum())]
    keys = [k for k in KEYS if k not in [q['key'] for q in prev[-2:]]]
    lo, hi = TEXTURES[t][1]
    return {'texture': t, 'key': int(keys[rng.integers(len(keys))]), 'bpm': int(rng.integers(lo, hi + 1)),
            'meter': 4 if rng.random() < TEXTURES[t][2] else 3}


def make_piece(rng, s):
    p = Piece(rng, s['key'], s['bpm'], s['meter'])
    bars = p.plan(s['sections']); times = p.timeline(len(bars))
    m3, lo = s['meter'] == 3, 61 + s['key'] % 3
    if s['texture'] == 'piano':
        p.melody(bars, times, lo, lo + 17, 'piano', 0.5, R3 if m3 else R4, E3 if m3 else E4[:3])
        p.piano_lh(bars, times, LH3 if m3 else LH4)
    elif s['texture'] == 'harp':
        p.harp_arp(bars, times, HARP3 if m3 else HARP4)
        hl = 69 + s['key'] % 2
        p.melody(bars, times, hl, hl + 14, 'harp', 0.42, HM3 if m3 else HM4, HE3 if m3 else HE4, rest_p=0.3)
        p.strings(bars, times, [('cello', 38, 52, 0), ('viola', 50, 64, 2)], 0.26)
    else:
        p.melody(bars, times, lo + 1, lo + 18, 'piano', 0.48, R3 if m3 else R4, E3 if m3 else E4[:3])
        p.piano_lh(bars, times, LH3 if m3 else LH4[3:], 0.27)
        s0 = s['strings_from']
        p.strings(bars[s0:], times[s0:], [('cello', 36, 50, 0), ('viola', 52, 64, 1), ('violin', 62, 74, 2)], 0.22)
    return p, times, bars


# ---------- rendering ----------

ATTACK = {'piano': 0.0, 'harp': 0.0, 'cello': 0.9, 'viola': 0.9, 'violin': 1.1}
RELEASE = {'piano': 0.45, 'harp': 0.9, 'cello': 1.6, 'viola': 1.6, 'violin': 1.8}
LEVEL = {'piano': 1.0, 'harp': 0.9, 'cello': 0.55, 'viola': 0.5, 'violin': 0.38}
PAN = {'piano': 0.0, 'harp': -0.2, 'cello': 0.3, 'viola': 0.1, 'violin': -0.25}
RING = 5.0
REF, CEIL = -18.0, -2.5
FADE_IN, FADE_OUT = 30.0, 720.0


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


# ---------- loudness (ITU-R BS.1770), as in tmp/trial/finish.py ----------

KW = (([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]),
      ([1, -2, 1], [1, -1.99004745483398, 0.99007225036621]))   # BS.1770 shelf + RLB high-pass, 48 kHz
CH = 10 * SR                                                     # chunk for long arrays, keeps memory low


def kw_power(y):
    """Sum over channels of the K-weighted signal squared; filters run in chunks with carried state."""
    z = np.zeros(len(y))
    for ch in range(y.shape[1]):
        zi = [np.zeros(2), np.zeros(2)]
        for c0 in range(0, len(y), CH):
            u = y[c0:c0 + CH, ch].astype(np.float64)
            for j, (b, a) in enumerate(KW): u, zi[j] = signal.lfilter(b, a, u, zi=zi[j])
            z[c0:c0 + CH] += u * u
    return z


def blocks(y, win, hop):
    """Loudness (LUFS) of windows of win seconds every hop seconds."""
    c = np.cumsum(kw_power(y)); n, h = int(win * SR), int(hop * SR)
    ms = (c[n::h] - c[:-n:h][:len(c[n::h])]) / n
    return -0.691 + 10 * np.log10(np.maximum(ms, 1e-12))


def integrated(y):
    L = blocks(y, 0.4, 0.1)
    L = L[L > -70]
    rel = -0.691 + 10 * np.log10(np.mean(10 ** ((L + 0.691) / 10))) - 10
    L = L[L > rel]
    return -0.691 + 10 * np.log10(np.mean(10 ** ((L + 0.691) / 10)))


LP = signal.butter(8, 15500, 'lowpass', fs=SR, output='sos')
HP = signal.butter(2, 35, 'highpass', fs=SR, output='sos')


def piece_mix(p, times, ir):
    """One piece with hall, 6 s swell-in from -8 dB, filters, and its loudness set to REF."""
    dry = render(p.notes, times[-1][0] + RING + 4)
    mix = dry * 0.82
    for c in range(2):
        mix[:, c] += signal.oaconvolve(dry[:, c], ir[:, c])[:len(dry)].astype(np.float32) * 0.42
    del dry
    k = 6 * SR
    mix[:k] *= (0.4 + 0.6 * (1 - np.cos(np.linspace(0, np.pi, k, dtype=np.float32))) / 2)[:, None]
    for c in range(2):
        mix[:, c] = signal.sosfilt(HP, signal.sosfilt(LP, mix[:, c]))
    loud = integrated(mix)
    return mix * np.float32(10 ** ((REF - loud) / 20)), loud


def limiter(x):
    """True-peak limiter on the 4x oversampled peak: 30 ms look-ahead and hold, 8 ms smoothing, 150 ms release."""
    pk = np.zeros(len(x), np.float32)
    step, pad = 10 * SR, 2000
    for ch in range(2):
        for s0 in range(0, len(x), step):
            a0, b0 = max(0, s0 - pad), min(len(x), s0 + step + pad)
            u = np.abs(signal.resample_poly(x[a0:b0, ch], 4, 1)).reshape(-1, 4).max(1)
            pk[s0:s0 + step] = np.maximum(pk[s0:s0 + step], u[s0 - a0: s0 - a0 + step][:len(pk[s0:s0 + step])])
    r = np.maximum(0, np.log(np.maximum(pk, 1e-9) / 10 ** (CEIL / 20)))
    env = np.ones(len(x), np.float32)
    over = np.flatnonzero(r > 0)
    if not len(over): return env
    # Gain reduction only around peaks over the ceiling: regions with 2 s margin, where hold, smoothing and release settle.
    m = 2 * SR
    cuts = np.flatnonzero(np.diff(over) > 2 * m)
    for lo, hi in zip(np.r_[over[0], over[cuts + 1]], np.r_[over[cuts], over[-1]]):
        lo, hi = max(0, lo - m), min(len(x), hi + m)
        rr = r[lo:hi]
        hold = maximum_filter1d(rr, 2 * int(0.03 * SR) + 1)
        a1 = np.exp(-1 / (0.008 * SR)); sm = signal.filtfilt([1 - a1], [1, -a1], hold)
        rel = np.exp(-1 / (0.15 * SR)); rl = signal.lfilter([1 - rel], [1, -rel], sm)
        env[lo:hi] = np.exp(-np.maximum(np.maximum(rr, sm), rl))
    return env


def main():
    rng = np.random.default_rng(SEED)
    total = HOURS * 3600
    ir = reverb_ir(np.random.default_rng(SEED + 1))

    # 1. Plan and compose every piece (notes only). The last pieces are sized so the programme reaches `total`.
    plan, start = [], 0.0
    while start < total - RING:
        s = choose_spec(rng, plan)
        bar = s['meter'] * 60 / s['bpm']
        remaining = total - start - RING
        target = remaining if remaining <= 330 else remaining / 2 if remaining < 480 else min(rng.uniform(190, 290), remaining - 200)
        n = (target / bar - 2.5) / 8
        s['sections'] = max(3, int(np.ceil(n))) if remaining <= 330 else int(np.clip(round(n), 5, 9))
        s['strings_from'] = 16 if s['texture'] == 'piano_strings' and s['sections'] >= 5 and rng.random() < 0.4 else 8
        p, times, bars = make_piece(rng, s)
        pedal(p.notes, times)
        s.update(start_s=round(start, 3), end_s=round(start + times[-1][0] + RING + 4, 3), bars=len(bars), notes=len(p.notes),
                 bar_starts=[round(t, 4) for t, _ in times], chords=[list(b) for b in bars], piece=p, times=times)
        plan.append(s)
        start += times[-1][0] + RING
    length = start + 2
    nsamp = int(round(length * SR))
    print('pieces', len(plan), 'length', round(length, 1), 's', flush=True)

    # 2. Render in 3-minute windows with 30 s of context each side: leveller, fades, limiter, dither, 24-bit PCM to ffmpeg.
    W, C, hop = 180 * SR, 30 * SR, 0.5
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 's24le', '-ar', str(SR), '-ac', '2', '-i', 'pipe:0',
                            '-c:a', 'aac', '-b:a', '256k', os.path.join(OUT, 'audio.m4a')], stdin=subprocess.PIPE)
    sha, cache, loud = hashlib.sha256(), {}, {}
    st_rms, st_short, st_gain, st_lim = [], [], [], []
    fi, fo = int(FADE_IN * SR), int(FADE_OUT * SR)
    for k in range(int(np.ceil(nsamp / W))):
        a0, b0 = k * W, min(nsamp, (k + 1) * W)
        a, b = max(0, a0 - C), min(nsamp, b0 + C)
        x = np.zeros((b - a, 2), np.float32)
        for i, s in enumerate(plan):
            i0, i1 = int(round(s['start_s'] * SR)), int(round(s['end_s'] * SR))
            if i1 <= a or i0 >= b: continue
            if i not in cache: cache[i], loud[i] = piece_mix(s['piece'], s['times'], ir)
            m = cache[i]
            lo, hi = max(a, i0), min(b, i0 + len(m))
            x[lo - a:hi - a] += m[lo - i0:hi - i0]
        for i in [i for i in cache if int(round(plan[i]['end_s'] * SR)) <= b0 - C]: del cache[i]   # next window starts at b0 - C
        # Slow leveller: short-term loudness (3 s) pulled 70% toward REF, at most 5 dB, 6 s smoothing.
        S = blocks(x, 3.0, hop)
        g = np.clip((REF - S) * 0.7, -5, 5)
        kk = int(6 / hop); g = np.convolve(np.pad(g, kk, mode='edge'), np.ones(2 * kk + 1) / (2 * kk + 1), 'valid')
        t_g = (np.arange(len(g)) * hop + 1.5) * SR
        for c0 in range(0, len(x), CH):
            t = np.arange(c0, min(len(x), c0 + CH))
            fade = np.minimum(np.clip((t + a) / fi, 0, 1) ** 2, np.clip((nsamp - t - a) / fo, 0, 1) ** 2)
            x[c0:c0 + CH] *= (10 ** (np.interp(t, t_g, g) / 20) * fade).astype(np.float32)[:, None]
        env = limiter(x)
        x *= env[:, None]
        y = x[a0 - a:b0 - a]
        # TPDF dither (seed per window) and 24-bit little-endian PCM.
        r2 = np.random.default_rng(930 + k)
        q = 2 ** 23
        for c0 in range(0, len(y), CH):
            u = y[c0:c0 + CH].astype(np.float64)
            d = r2.random(u.shape) - r2.random(u.shape)
            pcm = np.clip(np.round(u * (q - 1) + d), -q, q - 1).astype('<i4')
            raw = pcm.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
            sha.update(raw); enc.stdin.write(raw)
        sec = y[:len(y) // SR * SR].reshape(-1, SR, 2)
        st_rms.append(10 * np.log10(np.maximum((sec ** 2).mean(1), 1e-12)))
        st_short.append(S[(a0 - a) // int(hop * SR):][:len(y) // int(hop * SR)])
        st_gain.append(g[(a0 - a) // int(hop * SR):][:len(y) // int(hop * SR)])
        st_lim.append([float((env[a0 - a:b0 - a] < 0.999).mean()), float(-20 * np.log10(env[a0 - a:b0 - a].min()))])
        print(f'window {k}: {a0 / SR / 3600:.2f} h, cached pieces {len(cache)}', flush=True)
    enc.stdin.close()
    if enc.wait() != 0: sys.exit('ffmpeg failed')
    open(os.path.join(OUT, 'pcm.sha256'), 'w').write(sha.hexdigest() + '  pcm_s24le_48000_stereo\n')
    np.savez(os.path.join(OUT, 'stats.npz'), rms=np.concatenate(st_rms), short=np.concatenate(st_short),
             gain=np.concatenate(st_gain), lim=np.array(st_lim))
    notes_all = []
    for i, s in enumerate(plan):
        notes_all += [dict(n, t=round(n['t'] + s['start_s'], 4), piece=i) for n in s.pop('piece').notes]
        s.pop('times'); s['loudness_before'] = round(float(loud.get(i, 0)), 2)
    json.dump({'seed': SEED, 'hours': HOURS, 'length_s': round(length, 2), 'pieces': plan}, open(os.path.join(OUT, 'pieces.json'), 'w'))
    json.dump(notes_all, open(os.path.join(OUT, 'score.json'), 'w'))
    print('done; sha256', sha.hexdigest())


if __name__ == '__main__':
    main()
```

## scene.py

```python
"""Scene for the dog-channel pilot: a moonlit lake drawn by code, 1920x1080, 24 fps, seamless 6-minute loop.

Run: python -I scene.py still <t_seconds> <out.rgb>      one frame as raw RGB24 (ffmpeg makes the PNG)
     python -I scene.py loop <n0> <n1> | ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 24 -i - ...   frames n0..n1-1 to stdout
Requirements from docs/dog-music-research/stage2.md, section 3: blue, yellow and grey tones; dark, low contrast;
no flashes, stripes or flicker; no animals or people; slow smooth motion (clouds, water).
Motion repeats exactly every LOOP seconds: cloud layers move one texture period, ripple periods divide LOOP.
"""
import sys
import numpy as np

W, H, FPS, LOOP = 1920, 1080, 24, 360
HOR = 700                                   # shore line
rng = np.random.default_rng(93)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def mix(c0, c1, f):
    return np.asarray(c0, np.float32) * (1 - f[..., None]) + np.asarray(c1, np.float32) * f[..., None]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def cloud_texture(h, period, beta, stretch, seed):
    """Tileable (periodic) noise by FFT filtering: power ~ 1/f^beta, elongated horizontally; scaled to 0..1."""
    r = np.random.default_rng(seed)
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.rfftfreq(period)[None, :] * stretch
    f = np.sqrt(fx ** 2 + fy ** 2); f[0, 0] = 1
    spec = (r.standard_normal(f.shape) + 1j * r.standard_normal(f.shape)) / f ** (beta / 2)
    spec[0, 0] = 0
    n = np.fft.irfft2(spec, s=(h, period)).astype(np.float32)
    return (n - n.min()) / (n.max() - n.min())


# ---------- static layers ----------

# Sky: deep blue at the top, grey-blue in the middle, a faint warm grey above the hills.
v = yy[:HOR] / HOR
sky = mix((0.030, 0.045, 0.095), (0.075, 0.100, 0.175), smoothstep(0.0, 0.75, v))
sky = mix(sky, (0.165, 0.165, 0.180), smoothstep(0.62, 1.0, v) * 0.75)
MOON = (1390.0, 250.0, 34.0)                 # x, y, radius
d = np.hypot(xx[:HOR] - MOON[0], yy[:HOR] - MOON[1])
glow = (np.exp(-np.maximum(d - MOON[2], 0) / 140) * 0.10 + np.exp(-np.maximum(d - MOON[2], 0) / 18) * 0.10).astype(np.float32)
sky += glow[..., None] * np.array([0.85, 0.80, 0.60], np.float32)
disc = smoothstep(MOON[2] + 1.5, MOON[2] - 1.5, d)
craters = 1 - 0.07 * smoothstep(0.55, 0.75, cloud_texture(128, 128, 2.6, 1, 7))[
    np.clip((yy[:HOR] - MOON[1] + 64).astype(int), 0, 127), np.clip((xx[:HOR] - MOON[0] + 64).astype(int), 0, 127)]
moon = mix(sky, (0.80, 0.76, 0.60), disc) * np.where(disc > 0, craters, 1)[..., None]

# Cloud layers: texture rows map to sky rows [top, top + h); the far layer is thinner and slower.
CLOUDS = []
for top, h, period, alpha, col, seed, beta in ((40, 420, 3840, 0.60, (0.185, 0.195, 0.245), 11, 3.0),
                                                (170, 420, 5760, 0.75, (0.145, 0.155, 0.205), 12, 3.2)):
    tex = cloud_texture(h, period, beta, 3.0, seed)
    band = np.sin(np.pi * np.clip((np.arange(h) / h), 0, 1)) ** 1.5
    q1, q2 = np.quantile(tex, [0.55, 0.92])                            # about a third of the band is cloud
    a = (smoothstep(q1, q2, tex) * band[:, None] * alpha).astype(np.float32)
    lit = glow[top:top + h] * 1.6                                      # clouds near the moon catch its light
    CLOUDS.append((top, h, period, a, np.asarray(col, np.float32), lit))

# Hills: far range in haze, near shore darker; static.
x = np.arange(W) / W
far = 610 + 26 * np.sin(2 * np.pi * (x * 1.3 + 0.2)) + 14 * np.sin(2 * np.pi * (x * 3.1 + 0.6)) + 6 * np.sin(2 * np.pi * (x * 7.3))
near = 668 + 12 * np.sin(2 * np.pi * (x * 2.2 + 0.4)) + 7 * np.sin(2 * np.pi * (x * 5.7 + 0.1)) + 3 * np.sin(2 * np.pi * (x * 13.1))
hill_far = smoothstep(-1.2, 1.2, yy[:HOR] - far[None, :])
hill_near = smoothstep(-1.2, 1.2, yy[:HOR] - near[None, :])
FAR_COL = mix(np.broadcast_to(np.float32([0.085, 0.100, 0.145]), (HOR, W, 3)), (0.060, 0.072, 0.110), smoothstep(600, 700, yy[:HOR]))
NEAR_COL = np.float32([0.030, 0.038, 0.060])

# Water: mirrored sky rows, darker toward the viewer; a soft moon path under the moon.
wy = yy[HOR:] - HOR                                       # 0 at shore
src = np.clip(HOR - 1 - wy, 0, HOR - 1).astype(int)        # mirror row
depth = wy / (H - HOR)
WATER_DIM = (0.62 - 0.22 * depth).astype(np.float32)
WATER_TINT = np.float32([0.020, 0.032, 0.060])
path = np.exp(-((xx[HOR:] - MOON[0]) / (26 + 120 * depth)) ** 2) * (0.10 + 0.06 * depth) * smoothstep(0, 40, wy)
AMP = (0.6 + 7.0 * depth ** 1.5)[:, 0].astype(np.float32)   # ripple amplitude in px per water row
WL = (5 + 28 * depth ** 1.3)[:, 0].astype(np.float32)        # ripple wavelength in rows

# Static: soft vignette and fixed fine grain against banding (same every frame, so no flicker).
vig = (1 - 0.28 * smoothstep(0.45, 1.25, np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)))).astype(np.float32)
GRAIN = (rng.random((H, W, 1), np.float32) - rng.random((H, W, 1), np.float32)) * (1.2 / 255)
del d, disc, craters


def frame(t):
    t = t % LOOP
    img = moon.copy()
    for top, h, period, a, col, lit in CLOUDS:
        s = (t / LOOP) * period                             # one full period per loop
        i0 = int(np.floor(s)); f = np.float32(s - i0)
        idx = (np.arange(W) + i0) % period
        al = a[:, idx] * (1 - f) + a[:, (idx + 1) % period] * f
        c = col[None, None, :] + lit[..., None] * np.float32([0.9, 0.85, 0.7])
        seg = img[top:top + h]
        img[top:top + h] = seg * (1 - al[..., None]) + c * al[..., None]
    img = img * (1 - hill_far[..., None]) + FAR_COL * hill_far[..., None]
    img = img * (1 - hill_near[..., None]) + NEAR_COL * hill_near[..., None]
    # Water: each row of the mirror shifted sideways by two slow ripples (periods 9 s and 12 s, both divide LOOP).
    rows = np.arange(H - HOR, dtype=np.float32)
    dx = AMP * (0.65 * np.sin(2 * np.pi * (rows / WL - t / 9.0)) + 0.35 * np.sin(2 * np.pi * (rows / (WL * 1.7) - t / 12.0) + 1.3))
    xs = np.arange(W, dtype=np.float32)[None, :] + dx[:, None]
    x0 = np.floor(xs).astype(int); fx = (xs - x0)[..., None]
    x0 = np.clip(x0, 0, W - 1); x1 = np.clip(x0 + 1, 0, W - 1)
    refl = img[src[:, :1], x0] * (1 - fx) + img[src[:, :1], x1] * fx
    shimmer = 1 + 0.12 * np.sin(2 * np.pi * (rows / (WL * 0.8) + t / 9.0))[:, None]   # slow, low-contrast moon path
    water = refl * WATER_DIM[..., None] + WATER_TINT + (path * shimmer)[..., None] * np.float32([0.75, 0.70, 0.52])
    out = np.concatenate([img, water], 0) * vig[..., None]
    out = out * 1.35 / (1 + 0.35 * out) + GRAIN               # lift the darks ~30%, keep the moon below white
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        open(sys.argv[3], 'wb').write(frame(float(sys.argv[2])).tobytes())
    else:
        o = sys.stdout.buffer
        for n in range(int(sys.argv[2]), int(sys.argv[3])):
            o.write(frame(n / FPS).tobytes())
```

## loop.sh

```bash
#!/bin/bash
# Render frames n0..n1-1 of the scene loop and encode them (H.264, BT.709, CRF 23).
# Run: bash loop.sh <n0> <n1> <out.mp4>
set -euo pipefail
nice -n 10 ../venv/bin/python -I scene.py loop "$1" "$2" 2>/dev/null | nice -n 10 ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 24 -i - \
  -vf scale=out_color_matrix=bt709:out_range=tv -c:v libx264 -preset medium -crf 23 -g 240 -threads 2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$3"
```

## assemble.sh

```bash
#!/bin/bash
# Assemble the 10-hour pilot: join the loop halves, repeat the loop under the audio without re-encoding,
# cut listening excerpts for the board album, measure loudness of the final file.
# Run from tmp/pilot after pilot.py (out/audio.m4a) and loop.sh (video/seg0.mp4, video/seg1.mp4).
set -euo pipefail
cd video
printf "file 'seg0.mp4'\nfile 'seg1.mp4'\n" > loop.txt
ffmpeg -v error -y -f concat -safe 0 -i loop.txt -c copy loop.mp4
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ../out/audio.m4a)
# -t sets the length: with -stream_loop -1 the file would never end on its own.
nice -n 5 ffmpeg -v error -y -stream_loop -1 -i loop.mp4 -i ../out/audio.m4a -map 0:v -map 1:a -c copy -t "$T" dog-pilot-10h.mp4
# Excerpts, 150 s each, 1280x720 for the album: start, three places inside, the fade-out.
for s in "$@"; do
  nice -n 5 ffmpeg -v error -y -ss "$s" -i dog-pilot-10h.mp4 -t 150 -vf scale=1280:720 -c:v libx264 -preset medium -crf 26 \
    -pix_fmt yuv420p -c:a aac -b:a 160k "excerpt-$s.mp4"
done
nice -n 5 ffmpeg -hide_banner -nostats -i dog-pilot-10h.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | tail -12 > loudness.txt
sha256sum dog-pilot-10h.mp4 loop.mp4 thumbnail.png > sha256.txt
```

## check.py

```python
"""Checks of the pilot audio: repeats across the whole programme, melody intervals, register, pieces, silence, loudness range.

Run: python -I check.py <out_dir>   (reads pieces.json, score.json, stats.npz written by pilot.py)
A bar's signature is its notes: instrument, MIDI pitch, position in quarter-beats. Same signature = same bar heard again.
"""
import json, sys, collections
import numpy as np

OUT = sys.argv[1]
P = json.load(open(OUT + '/pieces.json'))
S = json.load(open(OUT + '/score.json'))
pieces = P['pieces']
by_piece = collections.defaultdict(list)
for n in S: by_piece[n['piece']].append(n)

full, top = [], []                      # per bar across the programme, piece boundaries kept
for i, p in enumerate(pieces):
    starts = [p['start_s'] + t for t in p['bar_starts']]
    ends = starts[1:] + [starts[-1] + 60]
    beat = [(e - s) / p['meter'] for s, e in zip(starts, ends)]
    f, m = [[] for _ in starts], [[] for _ in starts]
    for n in by_piece[i]:
        b = max(0, int(np.searchsorted(starts, n['t'] + 0.05, 'right')) - 1)
        key = (n['inst'], n['midi'], round((n['t'] - starts[b]) / beat[b] * 4) / 4)
        f[b].append(key)
        if n['role'] == 'mel': m[b].append(key)
    full.append([tuple(sorted(x)) for x in f]); top.append([tuple(sorted(x)) for x in m])


def dup(sig, w):
    """Windows of w bars (inside one piece) whose notes equal an earlier window anywhere in the programme."""
    seen, d, same_piece = {}, 0, 0
    for i, bars in enumerate(sig):
        for b in range(len(bars) - w + 1):
            k = tuple(bars[b:b + w])
            if not any(k): continue
            if k in seen:
                d += 1; same_piece += seen[k] == i
            else: seen[k] = i
    return d, same_piece


nbars = sum(len(x) for x in full)
print('pieces', len(pieces), 'bars', nbars, 'notes', len(S), 'length h', round(P['length_s'] / 3600, 3))
for w in (1, 2, 4):
    print(f'same {w} bar(s): full texture {dup(full, w)}, melody {dup(top, w)}  (total, inside the same piece)')
mel = [np.array([n['midi'] for n in sorted(by_piece[i], key=lambda n: n['t']) if n['role'] == 'mel']) for i in range(len(pieces))]
iv = np.concatenate([np.abs(np.diff(m)) for m in mel])
print('melody intervals: n', len(iv), 'steps<=2', round(float((iv <= 2).mean()), 3), 'of them same note', round(float((iv == 0).mean()), 3),
      'thirds', round(float(((iv >= 3) & (iv <= 4)).mean()), 3), 'fourths-fifths', round(float(((iv >= 5) & (iv <= 7)).mean()), 3), '>7', int((iv > 7).sum()))
for inst in ('piano', 'harp', 'cello', 'viola', 'violin'):
    ms = [n['midi'] for n in S if n['inst'] == inst]
    mm = [n['midi'] for n in S if n['inst'] == inst and n['role'] == 'mel']
    hz = lambda m: round(440 * 2 ** ((m - 69) / 12))
    print(inst, 'notes', len(ms), 'range', min(ms), max(ms), f'({hz(min(ms))}-{hz(max(ms))} Hz)', 'melody top', max(mm) if mm else '-', f'({hz(max(mm))} Hz)' if mm else '')
tex = collections.Counter(p['texture'] for p in pieces)
dur = [p['end_s'] - p['start_s'] - 9 for p in pieces]
print('textures', dict(tex), '| bpm', min(p['bpm'] for p in pieces), max(p['bpm'] for p in pieces),
      '| metre 3/4 share', round(float(np.mean([p['meter'] == 3 for p in pieces])), 2),
      '| keys', dict(collections.Counter(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'][p['key']] for p in pieces)))
print('piece length s: min', round(min(dur)), 'median', round(float(np.median(dur))), 'max', round(max(dur)))
same_next = sum(a['texture'] == b['texture'] for a, b in zip(pieces, pieces[1:]))
print('consecutive pieces with the same texture', same_next)

st = np.load(OUT + '/stats.npz')
rms = st['rms']                                          # dBFS per second, per channel
body = rms[30:-int(720)]
print('seconds below -45 dBFS outside fade-in (30 s) and fade-out (12 min):', int((body.mean(1) < -45).sum()))
lr = body[:, 0] - body[:, 1]
print('left minus right dB: median', round(float(np.median(lr)), 2), 'p5', round(float(np.percentile(lr, 5)), 2), 'p95', round(float(np.percentile(lr, 95)), 2))
sh = st['short']
s = sh[sh > -70]; s = s[s > 10 * np.log10(np.mean(10 ** (s / 10))) - 20]
print('loudness range (3 s blocks, 10th-95th percentile, LU):', round(float(np.percentile(s, 95) - np.percentile(s, 10)), 1))
print('leveller gain dB min/max', round(float(st['gain'].min()), 1), round(float(st['gain'].max()), 1),
      '| limiter: max share of window reduced', round(float(st['lim'][:, 0].max()), 4), 'max reduction dB', round(float(st['lim'][:, 1].max()), 2))
```

## Обложка

```bash
F=/usr/share/fonts/truetype/lato
python -I scene.py still 120 f120.rgb
ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -i f120.rgb f120.png
ffmpeg -i f120.png -vf "scale=1280:720:flags=lanczos,eq=brightness=0.03:gamma=1.15,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='CALM PIANO':fontsize=96:fontcolor=0xEDE3B8:x=80:y=230,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='& HARP FOR DOGS':fontsize=64:fontcolor=0xEDE3B8:x=84:y=338,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='10 hours · quiet music while you are away':fontsize=34:fontcolor=0xB9C4DA:x=86:y=428" \
  -frames:v 1 thumbnail.png
```
