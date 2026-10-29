# Приложение: код ролика 2

Код, которым собран [ролик 2](passport.md). Приведён для проверки и пересборки; как программа в проект не входит. Писал ассистент в задаче 127, 2026-10-29. Основа — [код пилота](../pilot/code.md): правила сочинения, громкость и сборка те же; другие инструменты, тональности, темп и сцена.

## Порядок

1. Сэмплы VSCO 2 Community Edition (CC0): 107 файлов пилота ([список](../drafts/code-drafts.md)) и 21 файл флейты и кларнета — список `want2.txt` ниже. Загрузка — `fetch.sh` из [черновиков кода](../drafts/code-drafts.md) с этим списком.
2. `python -I v2.py <samples> out 127 10` — план пьес, сочинение, рендер окнами по 3 минуты, громкость, 24-битный PCM в FFmpeg. Пишет `audio.m4a` (AAC 192 кбит/с), `pcm.sha256`, `pieces.json`, `score.json`, `stats.npz`.
3. `bash loop2.sh 0 2160 video/seg0.mp4` и `bash loop2.sh 2160 4320 video/seg1.mp4` — две половины петли картинки, параллельно.
4. `bash assemble2.sh <начала отрывков в секундах>` — склейка петли, ролик на 10 часов без перекодирования картинки, отрывки для альбома, замер громкости.
5. `python -I check2.py out` — повторы, интервалы мелодии, регистр, паузы, разброс громкости.
6. Обложка: команда в конце этого документа.

Окружение: Python 3.14.4, numpy 2.5.4, scipy 1.18.1, FFmpeg 6.0.1 (libx264, встроенный AAC). Шрифт обложки — Lato (SIL OFL 1.1), системный пакет `fonts-lato`.

## v2.py

```python
"""Video 2 audio for the dog channel: 10 hours, every piece new, composed by code and played with VSCO 2 CE samples (CC0).

Run: python -I v2.py <samples_dir> <out_dir> [seed] [hours]
Writes <out_dir>/audio.m4a (AAC 256 kbit/s, through ffmpeg on PATH), pcm.sha256 (hash of the 24-bit PCM before AAC),
pieces.json, score.json, stats.npz.
Rules and sound are those of the trial (tmp/trial/trial.py, heard and accepted by Villlerri on 2026-10-22); new here:
a plan of ~165 pieces with their own key, tempo, metre and texture; loudness processed in 5-minute windows,
so 10 hours never sit in memory; fade-in 30 s, fade-out 12 min (stage2.md, section 3).
Video 2 (task 127, 2026-10-29) is the pilot's code with other instruments: the melody is a flute or a clarinet,
alternating piece by piece, over the pilot's piano left hand or its sustained cellos and violas; other keys and tempi;
AAC 192 kbit/s (stage3.md, section 4). Default seed 127.
"""
import sys, os, json, warnings, hashlib, subprocess, collections
import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import maximum_filter1d

warnings.simplefilter('ignore', wavfile.WavFileWarning)
SR = 48000
SAMPLES, OUT = sys.argv[1], sys.argv[2]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 127
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
    # Woodwinds, soft layer v1 only; names use C3 = middle C (checked by pitch detection up to A4 and F4).
    for inst, sub in (('flute', 'Flute/susNV'), ('clarinet', 'Clarinet/susLong')):
        d = os.path.join(SAMPLES, 'Woodwinds', sub)
        m[inst] = sorted((midi_of(f.split('_')[2], c4=3), os.path.join(d, f)) for f in os.listdir(d) if '_v1_' in f)
    return m


WINDS = ('flute', 'clarinet')
SMAP = sample_map()
_shift, CACHE_BYTES = collections.OrderedDict(), 300e6
# Piano notes never sound longer than 6.7 s (last bar 5.5 s + release, pitch shift), so 8 s of sample is enough.
MAXLEN = {'piano_dyn1': 8, 'piano_dyn2': 8, 'harp': 7, 'cello': 9, 'viola': 9, 'violin': 9, 'flute': 8, 'clarinet': 8}


def load(path, maxlen, mono=False):
    """Read a sample as float32 stereo at SR, starting at its attack, at most maxlen seconds with a fade at the end.
    mono: keep only the louder channel; several VSCO flute samples have left and right in opposite phase,
    which would cancel in a phone or TV speaker, and the clarinet's left/right balance drifts within a note."""
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / (2 ** 31 if x.dtype == np.int32 else 2 ** 15)
    if x.ndim == 1: x = np.stack([x, x], 1)
    if mono:
        c = int(np.argmax((x[:2 * sr] ** 2).mean(0))); x = np.stack([x[:, c], x[:, c]], 1)
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
        r = {p: float(np.sqrt((load(p, MAXLEN[inst], inst in WINDS)[:SR] ** 2).mean())) for _, p in lst}
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
    x = load(p, MAXLEN[inst], inst in WINDS)
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
                ln = d * beat
                if inst in WINDS: ln *= 0.88 if final else 0.96          # a short breath at the phrase end, slight gaps elsewhere
                self.add(t0 + beat_pos * beat, ln, m, v, inst, role='mel')
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

# Textures of video 2: melody instrument + accompaniment (piano left hand, or cellos and violas).
TEXTURES = {'flute_piano': (0.3, (54, 62), 0.6), 'clarinet_piano': (0.25, (52, 60), 0.6),
            'flute_strings': (0.2, (52, 58), 0.4), 'clarinet_strings': (0.25, (50, 56), 0.4)}  # share, BPM, P(4/4)
KEYS = [0, 2, 3, 5, 7, 9, 10]                            # C D Eb F G A Bb major
KEY_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def choose_spec(rng, prev):
    """Melody instrument other than the previous piece's; key other than the previous two; tempo and metre per texture."""
    tex = [t for t in TEXTURES if not prev or t.split('_')[0] != prev[-1]['texture'].split('_')[0]]
    w = np.array([TEXTURES[t][0] for t in tex]); t = tex[rng.choice(len(tex), p=w / w.sum())]
    keys = [k for k in KEYS if k not in [q['key'] for q in prev[-2:]]]
    lo, hi = TEXTURES[t][1]
    return {'texture': t, 'key': int(keys[rng.integers(len(keys))]), 'bpm': int(rng.integers(lo, hi + 1)),
            'meter': 4 if rng.random() < TEXTURES[t][2] else 3}


def make_piece(rng, s):
    p = Piece(rng, s['key'], s['bpm'], s['meter'])
    bars = p.plan(s['sections']); times = p.timeline(len(bars))
    m3 = s['meter'] == 3
    lead, acc = s['texture'].split('_')
    lo = (64 if lead == 'flute' else 57) + s['key'] % 3        # flute E4..A5, clarinet A3..D5 at most
    # Long notes suit the winds: the slower rhythm banks of the harp melody, with some pilot piano rhythms mixed in.
    rh = (HM3 + R3[:2]) if m3 else (HM4 + R4[:2])
    p.melody(bars, times, lo, lo + 15, lead, 0.46, rh, HE3 if m3 else HE4 + [[2, 2]], rest_p=0.08)
    if acc == 'piano':
        p.piano_lh(bars, times, LH3 if m3 else LH4[2:], 0.26)
    else:
        p.strings(bars, times, [('cello', 36, 50, 0), ('viola', 48, 60, 1 if lead == 'flute' else 2)], 0.24)
    return p, times, bars


# ---------- rendering ----------

ATTACK = {'piano': 0.0, 'harp': 0.0, 'cello': 0.9, 'viola': 0.9, 'violin': 1.1, 'flute': 0.14, 'clarinet': 0.12}
RELEASE = {'piano': 0.45, 'harp': 0.9, 'cello': 1.6, 'viola': 1.6, 'violin': 1.8, 'flute': 0.4, 'clarinet': 0.4}
LEVEL = {'piano': 1.0, 'harp': 0.9, 'cello': 0.55, 'viola': 0.5, 'violin': 0.38, 'flute': 0.3, 'clarinet': 0.3}
PAN = {'piano': 0.0, 'harp': -0.2, 'cello': 0.15, 'viola': -0.15, 'violin': -0.25, 'flute': -0.1, 'clarinet': -0.1}
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
    """Synthetic hall: decaying noise in three bands, darker as it decays; 18 ms pre-delay.
    Video 2: left and right share 90% of the noise (correlation 0.9). With fully independent channels a held
    clarinet or flute note leaned up to 10 dB left or right, depending on its pitch."""
    n = int(sec * SR); t = np.arange(n) / SR
    ir = np.zeros((n, 2), np.float32)
    for (lo, hi), rt in (((60, 700), 2.4), ((700, 3500), 1.9), ((3500, 9000), 0.9)):
        sos = signal.butter(4, [lo, hi], 'bandpass', fs=SR, output='sos')
        g = rng.standard_normal((n, 3))
        src = np.stack([0.9487 * g[:, 0] + 0.3162 * g[:, 1], 0.9487 * g[:, 0] + 0.3162 * g[:, 2]], 1)
        noise = signal.sosfilt(sos, src, axis=0)
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
                            '-c:a', 'aac', '-b:a', '192k', os.path.join(OUT, 'audio.m4a')], stdin=subprocess.PIPE)
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
        r2 = np.random.default_rng(SEED * 10 + k)
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

## scene2.py

```python
"""Scene for dog-channel video 2: mountain ridges at dusk with slow mist, drawn by code, 1920x1080, 12 fps, seamless 6-minute loop.

Run: python -I scene2.py still <t_seconds> <out.rgb>      one frame as raw RGB24 (ffmpeg makes the PNG)
     python -I scene2.py loop <n0> <n1> | ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 12 -i - ...   frames n0..n1-1 to stdout
Requirements from docs/dog-music-research/stage2.md, section 3: blue, yellow and grey tones; dark, low contrast;
no flashes, stripes or flicker; no animals or people; slow smooth motion. Different from the pilot's moonlit lake:
no moon, no water; a dim amber afterglow on the horizon, layered blue ridges, mist drifting in the valleys.
Motion repeats exactly every LOOP seconds: mist and cloud layers move one texture period, star twinkle periods divide LOOP.
"""
import sys
import numpy as np

W, H, FPS, LOOP = 1920, 1080, 12, 360
rng = np.random.default_rng(127)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def mix(c0, c1, f):
    return np.asarray(c0, np.float32) * (1 - f[..., None]) + np.asarray(c1, np.float32) * f[..., None]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def noise2(h, period, beta, stretch, seed):
    """Tileable (periodic) noise by FFT filtering: power ~ 1/f^beta, elongated horizontally; scaled to 0..1."""
    r = np.random.default_rng(seed)
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.rfftfreq(period)[None, :] * stretch
    f = np.sqrt(fx ** 2 + fy ** 2); f[0, 0] = 1
    spec = (r.standard_normal(f.shape) + 1j * r.standard_normal(f.shape)) / f ** (beta / 2)
    spec[0, 0] = 0
    n = np.fft.irfft2(spec, s=(h, period)).astype(np.float32)
    return (n - n.min()) / (n.max() - n.min())


def ridge(seed, base, amp, rough):
    """Mountain profile: 1/f noise along x (not periodic, the ridges do not move), peak-to-peak amp px around base."""
    r = np.random.default_rng(seed)
    f = np.fft.rfftfreq(W * 2)[1:]
    spec = np.zeros(W + 1, complex)
    spec[1:] = (r.standard_normal(len(f)) + 1j * r.standard_normal(len(f))) / f ** rough
    spec[1:4] *= 0.5                                                   # fewer giant slopes
    y = np.fft.irfft(spec, W * 2)[:W]
    y = (y - y.min()) / (y.max() - y.min())
    return (base - amp * (y - 0.5)).astype(np.float32)


# ---------- static layers ----------

# Sky: deep blue at the top, grey-blue lower, a dim amber afterglow above the far ridges, brightest right of centre.
v = yy / H
sky = mix((0.022, 0.032, 0.080), (0.062, 0.080, 0.150), smoothstep(0.0, 0.48, v))
glow = (smoothstep(0.22, 0.56, v) * np.exp(-((xx - 1240) / 900) ** 2)).astype(np.float32)
sky = mix(sky, (0.215, 0.170, 0.105), glow * 0.85)
sky = mix(sky, (0.125, 0.120, 0.135), smoothstep(0.40, 0.62, v) * (1 - glow) * 0.5)

# Stars: faint, upper sky only, fading toward the glow; one brighter evening planet low in the afterglow.
NS = 140
sx, sy = rng.uniform(0, W, NS), rng.uniform(0, H * 0.36, NS) ** 1.0
sb = rng.uniform(0.04, 0.16, NS) * (1 - smoothstep(0.15, 0.40, sy / H)) + 0.01
sper = rng.choice([30.0, 40.0, 45.0, 60.0, 72.0, 90.0, 120.0], NS)    # twinkle periods divide LOOP
sph = rng.uniform(0, 2 * np.pi, NS)
STARS = []
for x0, y0, b, per, ph in zip(sx, sy, sb, sper, sph):
    i0, j0 = int(y0) - 3, int(x0) - 3
    if i0 < 0 or j0 < 0 or j0 + 7 > W: continue
    g = np.exp(-((np.arange(7)[:, None] - (y0 - i0)) ** 2 + (np.arange(7)[None, :] - (x0 - j0)) ** 2) / (2 * 0.7 ** 2))
    STARS.append((i0, j0, (g * b).astype(np.float32), per, ph))
PLANET = (1385, 395)
d = np.hypot(xx - PLANET[0], yy - PLANET[1])
sky += ((np.exp(-(d / 1.6) ** 2) * 0.55 + np.exp(-d / 9) * 0.035)[..., None] * np.float32([1.0, 0.93, 0.72]))

# Ridges, far to near: profile, colour (lighter and warmer in the haze far away, dark navy near).
RIDGES = [ridge(31, 560, 110, 1.75), ridge(32, 645, 160, 1.7), ridge(33, 765, 200, 1.6), ridge(34, 910, 210, 1.55)]
RCOL = [(0.105, 0.112, 0.160), (0.074, 0.084, 0.130), (0.046, 0.055, 0.092), (0.022, 0.028, 0.050)]
MASKS = [smoothstep(-1.0, 1.0, yy - r[None, :]) for r in RIDGES]
# Each ridge darkens slightly downward from its crest; far ridges catch a trace of the afterglow on top.
SHADE = [mix(np.broadcast_to(np.float32(c), (H, W, 3)), np.float32(c) * 0.80, smoothstep(0, 260, yy - r[None, :]))
         + (glow * 0.06 * (3 - k) / 3 * np.exp(-np.maximum(yy - r[None, :], 0) / 30))[..., None] * np.float32([1.0, 0.85, 0.6])
         for k, (r, c) in enumerate(zip(RIDGES, RCOL))]

# Mist: a band of drifting noise over ridges 0-2, below each crest, hidden lower down by the ridge in front.
MIST = []
for k, (period, alpha, seed) in enumerate(((5760, 0.22, 41), (4800, 0.32, 42), (3840, 0.38, 43))):
    r = RIDGES[k]
    top = int(r.min()) - 80
    h = int(r.max()) + 220 - top
    # The mist follows a smoothed crest line, so jagged peaks do not cut it into vertical streaks.
    kern = np.exp(-(np.arange(-480, 481) / 160.0) ** 2); kern /= kern.sum()
    crest = np.convolve(np.pad(r, 480, mode='edge'), kern, 'valid').astype(np.float32)
    MIST.append((top, h, period, noise2(h, period, 3.1, 4.0, seed), alpha, crest))
MIST_COL = np.float32([0.150, 0.158, 0.190])

# Thin high clouds lit by the afterglow, drifting slowly to the left.
CTOP, CH_, CPER = 150, 300, 7680
CTEX = noise2(CH_, CPER, 3.0, 5.0, 51)
q1, q2 = np.quantile(CTEX, [0.60, 0.95])
CA = (smoothstep(q1, q2, CTEX) * (np.sin(np.pi * np.arange(CH_) / CH_) ** 2)[:, None] * 0.35).astype(np.float32)
CCOL = sky[CTOP:CTOP + CH_].mean(1)[:, None, :] * 1.25 + glow[CTOP:CTOP + CH_, :][..., None].mean(1)[:, None] * np.float32([0.10, 0.07, 0.03])

vig = (1 - 0.30 * smoothstep(0.45, 1.25, np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)))).astype(np.float32)
GRAIN = (rng.random((H, W, 1), np.float32) - rng.random((H, W, 1), np.float32)) * (1.2 / 255)
del d


def frame(t):
    t = t % LOOP
    img = sky.copy()
    for i0, j0, g, per, ph in STARS:
        img[i0:i0 + 7, j0:j0 + 7] += (g * (0.85 + 0.15 * np.sin(2 * np.pi * t / per + ph)))[..., None] * np.float32([0.92, 0.92, 1.0])
    s = (1 - t / LOOP) * CPER                                            # leftward drift, one period per loop
    i = int(np.floor(s)); f = np.float32(s - i)
    idx = (np.arange(W) + i) % CPER
    a = CA[:, idx] * (1 - f) + CA[:, (idx + 1) % CPER] * f
    seg = img[CTOP:CTOP + CH_]
    img[CTOP:CTOP + CH_] = seg * (1 - a[..., None]) + CCOL * a[..., None]
    for k in range(len(RIDGES)):
        m = MASKS[k][..., None]
        img = img * (1 - m) + SHADE[k] * m
        if k < len(MIST):                                                 # mist sits on ridge k, in front of it
            top, h, period, tex, alpha, crest = MIST[k]
            s = (t / LOOP) * period * (1 if k % 2 == 0 else -1)
            i = int(np.floor(s)); f = np.float32(s - i)
            idx = (np.arange(W) + i) % period
            n = tex[:, idx] * (1 - f) + tex[:, (idx + 1) % period] * f
            rows = np.arange(top, top + h, dtype=np.float32)[:, None]
            vert = np.exp(-((rows - crest[None, :] - 30) / 80) ** 2)      # hugs the valley in front of ridge k
            al = smoothstep(0.35, 0.85, n) * vert * alpha
            lo, hi = max(0, top), min(H, top + h)
            al = al[lo - top:hi - top]
            c = MIST_COL + glow[lo:hi, :, None] * np.float32([0.06, 0.045, 0.02])
            img[lo:hi] = img[lo:hi] * (1 - al[..., None]) + c * al[..., None]
    out = img * vig[..., None]
    out = out * 1.35 / (1 + 0.35 * out) + GRAIN                          # lift the darks, as in the pilot
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        open(sys.argv[3], 'wb').write(frame(float(sys.argv[2])).tobytes())
    else:
        o = sys.stdout.buffer
        for n in range(int(sys.argv[2]), int(sys.argv[3])):
            o.write(frame(n / FPS).tobytes())
```

## loop2.sh

```bash
#!/bin/bash
# Render frames n0..n1-1 of the video 2 scene loop (12 fps) and encode them (H.264, BT.709, CRF 25).
# Run: bash loop2.sh <n0> <n1> <out.mp4>
set -euo pipefail
nice -n 10 ../venv/bin/python -I scene2.py loop "$1" "$2" 2>/dev/null | nice -n 10 ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 12 -i - \
  -vf scale=out_color_matrix=bt709:out_range=tv -c:v libx264 -preset slow -crf 25 -g 240 -threads 2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 "$3"
```

## assemble2.sh

```bash
#!/bin/bash
# Assemble the 10-hour video 2: join the loop halves, repeat the loop under the audio without re-encoding,
# cut listening excerpts for the board album, measure loudness of the final file.
# Run from tmp/v2 after v2.py (out/audio.m4a) and loop2.sh (video/seg0.mp4, video/seg1.mp4).
set -euo pipefail
cd video
printf "file 'seg0.mp4'\nfile 'seg1.mp4'\n" > loop.txt
ffmpeg -v error -y -f concat -safe 0 -i loop.txt -c copy loop.mp4
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ../out/audio.m4a)
# -t sets the length: with -stream_loop -1 the file would never end on its own.
nice -n 5 ffmpeg -v error -y -stream_loop -1 -i loop.mp4 -i ../out/audio.m4a -map 0:v -map 1:a -c copy -t "$T" dog-v2-10h.mp4
# Excerpts, 150 s each, 1280x720 for the album: start, three places inside, the fade-out.
for s in "$@"; do
  nice -n 5 ffmpeg -v error -y -ss "$s" -i dog-v2-10h.mp4 -t 150 -vf scale=1280:720 -c:v libx264 -preset medium -crf 26 \
    -pix_fmt yuv420p -c:a aac -b:a 160k "excerpt-$s.mp4"
done
nice -n 5 ffmpeg -hide_banner -nostats -i dog-v2-10h.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | tail -12 > loudness.txt
sha256sum dog-v2-10h.mp4 loop.mp4 ../thumbnail.png > sha256.txt
```

## check2.py

```python
"""Checks of the video 2 audio (same checks as the pilot): repeats across the whole programme, melody intervals, register, pieces, silence, loudness range.

Run: python -I check.py <out_dir>   (reads pieces.json, score.json, stats.npz written by v2.py)
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
for inst in ('piano', 'flute', 'clarinet', 'cello', 'viola'):
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
same_lead = sum(a['texture'].split('_')[0] == b['texture'].split('_')[0] for a, b in zip(pieces, pieces[1:]))
print('consecutive pieces with the same melody instrument', same_lead)
```

## want2.txt

```text
Woodwinds/Flute/susNV/LDFlute_susNV_A3_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_A4_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_A5_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_C3_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_C4_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_C5_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_C6_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_E3_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_E4_v1_1.wav
Woodwinds/Flute/susNV/LDFlute_susNV_E5_v1_1.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_A#2_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_A#3_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_A#4_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_D2_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_D3_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_D4_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_D5_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_F#5_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_F2_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_F3_v1_rr1_sum.wav
Woodwinds/Clarinet/susLong/DCClar_susLong_F4_v1_rr1_sum.wav
```

## Обложка

```bash
F=/usr/share/fonts/truetype/lato
python -I scene2.py still 120 f120.rgb
ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -i f120.rgb f120.png
ffmpeg -i f120.png -vf "scale=1280:720:flags=lanczos,eq=brightness=0.03:gamma=1.2,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='CALM FLUTE':fontsize=96:fontcolor=0xEDE3B8:x=80:y=120,\
drawtext=fontfile=$F/Lato-Bold.ttf:text='& CLARINET FOR DOGS':fontsize=64:fontcolor=0xEDE3B8:x=84:y=228,\
drawtext=fontfile=$F/Lato-Regular.ttf:text='10 hours · soft music for a quiet home':fontsize=34:fontcolor=0xB9C4DA:x=86:y=318" \
  -frames:v 1 thumbnail.png
```
