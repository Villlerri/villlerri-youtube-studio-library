# Moving Atlas, пилот: код сборки

Весь код папки `probe/` на 2026-10-28: проба стиля, видео пилота, черновик полного выпуска, обложки, ключевые кадры, оформление канала. Remotion 4.0.507, React 19, d3-geo. Один раздел — один файл, заголовок раздела — путь файла.

В код не входят данные карты, шрифты и снимки вставок: их скачивает `probe/scripts/fetch-data.sh`. Видео в проекте не хранятся: они собираются этим кодом, копии — во вложениях задачи 52.

## Как восстановить

Из папки `projects/pilots/moving-atlas/`:

```bash
python3 - code.md <<'PY'
import re, sys, pathlib
text = pathlib.Path(sys.argv[1]).read_text()
for path, body in re.findall(r'^## (probe/\S+)\n\n````[a-z]*\n(.*?)````$', text, re.S | re.M):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
PY
chmod +x probe/scripts/*.sh
```

Дальше — [production.md](production.md): разделы «Как собрать пробу заново» и «Как собрать выпуск 12–16 минут».

## probe/.gitignore

````
node_modules/
out/
public/fonts/
public/ne/
public/relief/
public/region/
public/assets/
public/brand/
````

## probe/package.json

````json
{
  "name": "moving-atlas-probe",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "studio": "remotion studio src/index.ts",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@remotion/cli": "4.0.507",
    "d3-geo": "3.1.1",
    "react": "19.2.8",
    "react-dom": "19.2.8",
    "remotion": "4.0.507"
  },
  "devDependencies": {
    "@types/d3-contour": "3.0.6",
    "@types/d3-geo": "3.1.0",
    "@types/react": "19.2.14",
    "d3-contour": "4.0.2",
    "typescript": "5.9.3"
  }
}
````

## probe/remotion.config.ts

````ts
import {Config} from '@remotion/cli/config';

// Linux / ARM (e.g. Raspberry Pi) support.
// Chrome-for-Testing has no linux-arm64 build, so Remotion can't download a browser there.
// Point it at a system Chromium via env, e.g.:
//   export REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium
// On a GPU-less headless box also set software GL (default 'swangle'); override with REMOTION_GL.
// Both are unset on macOS / x86 → this file is a no-op and Remotion uses its own browser.
const GL_RENDERERS = ['swangle', 'angle', 'egl', 'swiftshader', 'vulkan', 'angle-egl'] as const;
type GlRenderer = (typeof GL_RENDERERS)[number];
const isGlRenderer = (v: string | undefined): v is GlRenderer => (GL_RENDERERS as readonly string[]).includes(v ?? '');

const browser = process.env.REMOTION_BROWSER_EXECUTABLE;
if (browser) {
  Config.setBrowserExecutable(browser);
  const gl = process.env.REMOTION_GL;
  if (gl && !isGlRenderer(gl)) {
    throw new Error(`REMOTION_GL=${gl} is not a valid renderer; use one of: ${GL_RENDERERS.join(' / ')}`);
  }
  Config.setChromiumOpenGlRenderer(isGlRenderer(gl) ? gl : 'swangle');
}
````

## probe/tsconfig.json

````json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["src"]
}
````

## probe/scripts/brand-render.sh

````bash
#!/usr/bin/env bash
# Writes the branding SVG and renders PNG files into ../branding/:
#   scripts/brand-render.sh ["Channel Name"] ["Tagline"]
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
bun scripts/brand.ts "$@"
rm -rf out/bundle-brand
bunx remotion bundle src/index.ts --out-dir out/bundle-brand --log=error
for id in Avatar Banner BannerCheck; do
  name=$(echo "$id" | sed 's/BannerCheck/banner-check/; s/Banner/banner/; s/Avatar/avatar/')
  bunx remotion still out/bundle-brand "$id" "../branding/$name.png" --log=error
done
ls -la ../branding/*.png
````

## probe/scripts/brand.ts

````ts
// Writes the channel branding as editable SVG to ../branding/ and a copy to public/brand/ for rendering:
//   bun scripts/brand.ts ["The Layered Map"] ["History moves on one living map"]
// Fonts: Fraunces and PT Sans Narrow (SIL OFL), installed or loaded by the renderer.
// YouTube rules used (support.google.com/youtube/answer/10456525, read 2026-10-15): banner 2560 x 1440
// recommended, minimum 2048 x 1152, safe area 1235 x 338 at the minimum size, 6 MB or smaller;
// profile picture renders at 98 x 98, square or round, 15 MB or smaller.
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {geoConicConformal, geoPath} from 'd3-geo';

const NAME = process.argv[2] ?? 'The Layered Map';
const TAG = process.argv[3] ?? 'History moves on one living map';
const C = {water: '#C7D3D4', land: '#EFE9DC', relief: '#E2D3B5', ink: '#1E2A2F', accent: '#C4472C', force: '#3E6E8E', river: '#9DB2B6'};
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

// Avatar 800 x 800: three map sheets stacked, the top one carrying a route. Reads at 98 px.
function avatar() {
  const sheet = (cy: number, fill: string) =>
    `<path d="M400,${cy - 120} L640,${cy} L400,${cy + 120} L160,${cy} Z" fill="${fill}" stroke="${C.ink}" stroke-width="14" stroke-linejoin="round"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <rect width="800" height="800" fill="${C.ink}"/>
  ${sheet(520, C.relief)}
  ${sheet(440, C.water)}
  ${sheet(360, C.land)}
  <path d="M262,360 C320,330 360,400 420,372 S520,300 548,346" fill="none" stroke="${C.accent}" stroke-width="22" stroke-linecap="round" stroke-dasharray="1 0"/>
  <circle cx="548" cy="346" r="26" fill="${C.accent}" stroke="${C.land}" stroke-width="8"/>
  <circle cx="262" cy="360" r="16" fill="${C.ink}"/>
</svg>
`;
}

// Banner 2560 x 1440: eastern North America, the first episode's route, name in the safe area.
const SAFE = {w: 1235 * (2560 / 2048), h: 338 * (2560 / 2048)}; // 1543.75 x 422.5 at 2560 wide
function banner(check: boolean) {
  const W = 2560;
  const H = 1440;
  const region = JSON.parse(readFileSync('public/region/east.json', 'utf8'));
  const canal = JSON.parse(readFileSync('public/region/erie-canal-atack.json', 'utf8'));
  // New York State sits right of the name plaque, inside the band every device shows.
  const proj = geoConicConformal().parallels([40.5, 44]).rotate([76, 0]).fitExtent([[1980, 420], [2540, 1020]], {
    type: 'MultiPoint',
    coordinates: [[-80, 40.4], [-72.8, 40.4], [-72.8, 44.6], [-80, 44.6]],
  } as any);
  const path = geoPath(proj).digits(1);
  const hudson = [[-73.755, 42.651], [-73.79, 42.25], [-73.96, 41.92], [-73.94, 41.7], [-74.01, 41.5], [-73.96, 41.39], [-73.93, 41.29], [-73.88, 41.07], [-73.9, 40.94], [-74.015, 40.704]];
  const x0 = (W - SAFE.w) / 2;
  const y0 = (H - SAFE.h) / 2;
  const nyc = proj([-74.015, 40.704]) as [number, number];
  const relief = region.relief.map((r: any) => `<path d="${path(r.geometry)}" fill="${C.relief}" fill-opacity="0.32"/>`).join('');
  const rivers = region.rivers.map((r: any) => path({type: 'LineString', coordinates: r.coords} as any)).join('');
  const guides = check
    ? `<rect x="${x0}" y="${y0}" width="${SAFE.w}" height="${SAFE.h}" fill="none" stroke="#D11" stroke-width="6" stroke-dasharray="24 14"/>
  <text x="${x0 + 12}" y="${y0 - 18}" font-family="PT Sans Narrow" font-size="40" fill="#D11">Safe area for text and logos: 1235 x 338 at 2048 wide = ${SAFE.w.toFixed(0)} x ${SAFE.h.toFixed(0)} here</text>
  <rect x="3" y="3" width="${W - 6}" height="${H - 6}" fill="none" stroke="#D11" stroke-width="6"/>
  <text x="24" y="64" font-family="PT Sans Narrow" font-size="40" fill="#D11">Full image: shown on TV. Other devices crop toward the safe area.</text>`
    : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${C.water}"/>
  <path d="${path(region.land)}" fill="${C.land}"/>
  ${relief}
  <path d="${path(region.lakes)}" fill="${C.water}"/>
  <path d="${rivers}" fill="none" stroke="${C.river}" stroke-width="2.5"/>
  <path d="${path({type: 'LineString', coordinates: hudson} as any)}" fill="none" stroke="${C.accent}" stroke-width="7" stroke-linecap="round"/>
  <path d="${path(canal)}" fill="none" stroke="${C.accent}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="${nyc[0]}" cy="${nyc[1]}" r="16" fill="${C.accent}" stroke="${C.land}" stroke-width="5"/>
  <rect x="${x0 + 40}" y="${y0 + 40}" width="${SAFE.w - 80}" height="${SAFE.h - 80}" fill="${C.land}" fill-opacity="0.9" stroke="${C.ink}" stroke-width="4"/>
  <text x="${W / 2}" y="${y0 + 228}" text-anchor="middle" font-family="Fraunces" font-weight="600" font-size="150" fill="${C.ink}">${esc(NAME)}</text>
  <text x="${W / 2}" y="${y0 + 318}" text-anchor="middle" font-family="PT Sans Narrow" font-weight="700" font-size="54" letter-spacing="9" fill="${C.accent}">${esc(TAG.toUpperCase())}</text>
  ${guides}
</svg>
`;
}

mkdirSync('../branding', {recursive: true});
mkdirSync('public/brand', {recursive: true});
const out: Record<string, string> = {'avatar.svg': avatar(), 'banner.svg': banner(false), 'banner-check.svg': banner(true)};
for (const [f, s] of Object.entries(out)) {
  if (f !== 'banner-check.svg') writeFileSync(`../branding/${f}`, s);
  writeFileSync(`public/brand/${f}`, s);
  console.log(f, (s.length / 1024).toFixed(0), 'KB');
}
````

## probe/scripts/build-region.ts

````ts
// Cuts Natural Earth layers and ETOPO 2022 relief to one map region and writes
// public/region/<name>.json for the composition. Run after fetch-data.sh:
//   bun scripts/build-region.ts            (the probe region, "erie")
//   bun scripts/build-region.ts east       (eastern North America)
import {contours} from 'd3-contour';
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';

type Pt = [number, number];
type Ring = Pt[];
// Data box is wider than the view box so no clip edge shows in frame.
const REGIONS: Record<string, {view: number[]; data: number[]; relief: string; minRiverRank: number}> = {
  erie: {view: [-81, 39.5, -71, 45.5], data: [-84, 37.5, -68, 47.5], relief: 'etopo_ne_us.ascii', minRiverRank: 10},
  east: {view: [-92, 29, -66, 47], data: [-110, 22, -56, 54], relief: 'etopo_east.ascii', minRiverRank: 6},
};
const NAME = process.argv[2] ?? 'erie';
const R = REGIONS[NAME];
const VIEW = R.view;
const [W, S, E, N] = R.data;
const RIVER_SKIP = new Set(['Erie Canal', 'Oneida River - Erie Canal', 'Welland Canal']);
const RELIEF_LEVELS = [150, 300, 500, 800];

const round = (p: Pt): Pt => [Math.round(p[0] * 1e4) / 1e4, Math.round(p[1] * 1e4) / 1e4];
const inside = ([x, y]: Pt) => x >= W && x <= E && y >= S && y <= N;

// Sutherland–Hodgman against the region box, one edge at a time.
function clipRing(ring: Ring): Ring {
  const edges: [(p: Pt) => boolean, (a: Pt, b: Pt) => Pt][] = [
    [(p) => p[0] >= W, (a, b) => [W, a[1] + ((b[1] - a[1]) * (W - a[0])) / (b[0] - a[0])]],
    [(p) => p[0] <= E, (a, b) => [E, a[1] + ((b[1] - a[1]) * (E - a[0])) / (b[0] - a[0])]],
    [(p) => p[1] >= S, (a, b) => [a[0] + ((b[0] - a[0]) * (S - a[1])) / (b[1] - a[1]), S]],
    [(p) => p[1] <= N, (a, b) => [a[0] + ((b[0] - a[0]) * (N - a[1])) / (b[1] - a[1]), N]],
  ];
  let out = ring;
  for (const [isIn, cut] of edges) {
    const src = out;
    out = [];
    for (let i = 0; i < src.length; i++) {
      const cur = src[i];
      const prev = src[(i + src.length - 1) % src.length];
      if (isIn(cur)) {
        if (!isIn(prev)) out.push(cut(prev, cur));
        out.push(cur);
      } else if (isIn(prev)) out.push(cut(prev, cur));
    }
    if (!out.length) return [];
  }
  return out;
}

// d3-geo wants exterior rings clockwise in lon/lat, holes counter-clockwise.
const area = (r: Ring) => r.reduce((s, p, i) => {
  const q = r[(i + 1) % r.length];
  return s + p[0] * q[1] - q[0] * p[1];
}, 0) / 2;
const orient = (r: Ring, exterior: boolean) => ((area(r) < 0) === exterior ? r : [...r].reverse());

function clipPolygon(rings: Ring[]): Ring[] | null {
  const out: Ring[] = [];
  rings.forEach((r, i) => {
    const c = clipRing(r.slice(0, -1) as Ring).map(round);
    if (c.length < 3 || Math.abs(area(c)) < 1e-6) return;
    if (i > 0 && !out.length) return;
    const o = orient(c, i === 0);
    out.push([...o, o[0]]);
  });
  return out.length ? out : null;
}

function clipLine(line: Ring): Ring[] {
  const parts: Ring[] = [];
  let cur: Ring = [];
  for (const p of line) {
    if (inside(p)) cur.push(round(p));
    else if (cur.length) { parts.push(cur); cur = []; }
  }
  if (cur.length) parts.push(cur);
  return parts.filter((l) => l.length > 1);
}

const read = (layer: string) => JSON.parse(readFileSync(`public/ne/${layer}.geojson`, 'utf8')).features as any[];

function polygons(layers: string[]) {
  const polys: Ring[][] = [];
  for (const layer of layers) for (const f of read(layer)) {
    if (!f.geometry) continue;
    const g = f.geometry;
    const list = g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : [];
    for (const rings of list) {
      const c = clipPolygon(rings);
      if (c) polys.push(c);
    }
  }
  return {type: 'MultiPolygon', coordinates: polys};
}

function rivers() {
  const out: {name: string; coords: Ring}[] = [];
  for (const layer of ['ne_10m_rivers_lake_centerlines', 'ne_10m_rivers_north_america']) for (const f of read(layer)) {
    if (!f.geometry || RIVER_SKIP.has(f.properties.name)) continue;
    if (layer.endsWith('north_america') && f.properties.scalerank > 10) continue;
    if (f.properties.scalerank > R.minRiverRank && NAME !== 'erie') continue;
    const g = f.geometry;
    const lines = g.type === 'LineString' ? [g.coordinates] : g.coordinates;
    for (const l of lines) for (const part of clipLine(l)) out.push({name: f.properties.name ?? '', coords: part});
  }
  return out;
}

// ETOPO 2022 60 arc-second subset saved as OPeNDAP ASCII by fetch-data.sh.
function relief() {
  const txt = readFileSync(`public/relief/${R.relief}`, 'utf8');
  const body = txt.split('---------------------------------------------')[1];
  const [zPart, rest] = body.split('z.lat[');
  const [latPart, lonPart] = rest.split('z.lon[');
  const nums = (s: string) => s.split(/[\s,]+/).filter((t) => /^-?\d/.test(t)).map(Number);
  const lat = nums(latPart.slice(latPart.indexOf(']') + 1));
  const lon = nums(lonPart.slice(lonPart.indexOf(']') + 1));
  const rows = zPart.trim().split('\n').slice(1).map((l) => nums(l.slice(l.indexOf(']') + 1)));
  const [ny, nx] = [rows.length, rows[0].length];
  if (ny !== lat.length || nx !== lon.length) throw new Error(`grid ${ny}x${nx} vs ${lat.length}x${lon.length}`);
  const values = rows.flat();
  const toLonLat = ([x, y]: number[]): Pt => {
    const xi = Math.min(Math.max(x - 0.5, 0), nx - 1);
    const yi = Math.min(Math.max(y - 0.5, 0), ny - 1);
    const lerp = (a: number[], t: number) => a[Math.floor(t)] + (a[Math.ceil(t)] - a[Math.floor(t)]) * (t - Math.floor(t));
    return round([lerp(lon, xi), lerp(lat, yi)]);
  };
  return contours().size([nx, ny]).thresholds(RELIEF_LEVELS)(values).map((c) => ({
    level: c.value,
    geometry: {
      type: 'MultiPolygon',
      coordinates: c.coordinates.map((poly) => poly.map((ring, i) => orient(ring.map(toLonLat), i === 0))),
    },
  }));
}

mkdirSync('public/region', {recursive: true});
const out = {
  bbox: VIEW,
  land: polygons(['ne_10m_land']),
  lakes: polygons(['ne_10m_lakes', 'ne_10m_lakes_north_america']),
  rivers: rivers(),
  relief: relief(),
};
writeFileSync(`public/region/${NAME}.json`, JSON.stringify(out));
console.log(`public/region/${NAME}.json`, out.land.coordinates.length, 'land', out.lakes.coordinates.length, 'lakes', out.rivers.length, 'river parts', out.relief.map((r) => r.level).join('/'));
````

## probe/scripts/check-narration.ts

````ts
// Checks that the narration (src/narration.ts) is word for word ../script.md (or its start),
// and prints words, characters and minutes of the whole script: bun scripts/check-narration.ts
import {readFileSync} from 'node:fs';
import {SCENES, WPM} from '../src/narration';

const md = readFileSync(new URL('../../script.md', import.meta.url), 'utf8');
const paras = md.split('\n').filter((l) => l.startsWith('> ') && l.length > 2).map((l) => l.slice(2).trim());
const all = paras.join(' ');
const pilot = SCENES.map((s) => s.text).join(' ');
if (!all.startsWith(pilot)) {
  const i = [...pilot].findIndex((c, n) => c !== all[n]);
  throw new Error(`pilot narration differs from script.md at: "${pilot.slice(i, i + 60)}" vs "${all.slice(i, i + 60)}"`);
}
const words = (s: string) => s.split(/\s+/).filter(Boolean).length;
console.log(`script: ${words(all)} words, ${all.length} characters, ${(words(all) / WPM).toFixed(1)} min at ${WPM} wpm`);
console.log(`narration in src/narration.ts: ${words(pilot)} words, ${pilot.length} characters`);
````

## probe/scripts/env.sh

````bash
# Sourced by the render scripts: browser, GL and temp dirs inside this folder.
PROBE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export REMOTION_BROWSER_EXECUTABLE=$(find "$HOME/.cache/ms-playwright" -maxdepth 3 -type f -name chrome-headless-shell 2>/dev/null | sort -V | tail -1)
export REMOTION_GL=swiftshader
export TMPDIR="$PROBE_DIR/out/tmp"
mkdir -p "$TMPDIR"
````

## probe/scripts/erie-line.py

````python
"""Extracts the Erie Canal line from Jeremy Atack's 19th-century canals
shapefile (official zip, see fetch-data.sh) into a GeoJSON file.
Shapefile polylines are read directly. The file is in USA Contiguous Albers Equal
Area Conic (NAD83, GRS 1980); points are converted back to lon/lat with the
ellipsoidal inverse formulas in Snyder, Map Projections - A Working Manual, p. 101-102.
Usage: python3 erie-line.py <canals.zip> <out.geojson>"""
import json, math, struct, sys, zipfile

A, F = 6378137.0, 1 / 298.257222101
E2 = 2 * F - F * F
E = math.sqrt(E2)
LAT0, LON0, P1, P2 = map(math.radians, (37.5, -96.0, 29.5, 45.5))
m = lambda p: math.cos(p) / math.sqrt(1 - E2 * math.sin(p) ** 2)
q = lambda p: (1 - E2) * (math.sin(p) / (1 - E2 * math.sin(p) ** 2) - (1 / (2 * E)) * math.log((1 - E * math.sin(p)) / (1 + E * math.sin(p))))
N = (m(P1) ** 2 - m(P2) ** 2) / (q(P2) - q(P1))
C = m(P1) ** 2 + N * q(P1)
RHO0 = A * math.sqrt(C - N * q(LAT0)) / N


def inverse(x, y):
    rho = math.hypot(x, RHO0 - y)
    theta = math.atan2(x, RHO0 - y)
    qq = (C - (rho * N / A) ** 2) / N
    phi = math.asin(qq / 2)
    for _ in range(10):
        s = math.sin(phi)
        phi += (1 - E2 * s * s) ** 2 / (2 * math.cos(phi)) * (qq / (1 - E2) - s / (1 - E2 * s * s) + (1 / (2 * E)) * math.log((1 - E * s) / (1 + E * s)))
    return math.degrees(LON0 + theta / N), math.degrees(phi)


z = zipfile.ZipFile(sys.argv[1])
shp = z.read('19thC_Canals_March2017.shp')
dbf = z.read('19thC_Canals_March2017.dbf')
prj = z.read('19thC_Canals_March2017.prj').decode()
assert 'USA_Contiguous_Albers_Equal_Area_Conic' in prj, prj

# dBase table
n, hlen, rlen = struct.unpack('<xxxxIHH', dbf[:12])
fields, off = [], 32
while dbf[off] != 0x0D:
    name = dbf[off:off + 11].split(b'\0')[0].decode()
    fields.append((name, dbf[off + 16]))
    off += 32
rows = []
for i in range(n):
    rec, pos, row = dbf[hlen + i * rlen: hlen + (i + 1) * rlen], 1, {}
    for name, ln in fields:
        row[name] = rec[pos:pos + ln].decode('latin-1').strip()
        pos += ln
    rows.append(row)

# Polyline records (shape type 3)
feats, pos, i = [], 100, 0
while pos < len(shp):
    _, clen = struct.unpack('>II', shp[pos:pos + 8])
    body = shp[pos + 8: pos + 8 + clen * 2]
    pos += 8 + clen * 2
    st = struct.unpack('<i', body[:4])[0]
    row = rows[i]; i += 1
    if st != 3 or row['NAME'] != 'Erie Canal':
        continue
    nparts, npts = struct.unpack('<ii', body[36:44])
    parts = list(struct.unpack(f'<{nparts}i', body[44:44 + 4 * nparts])) + [npts]
    pts = struct.unpack(f'<{2 * npts}d', body[44 + 4 * nparts: 44 + 4 * nparts + 16 * npts])
    lines = [[[round(v, 5) for v in inverse(pts[2 * k], pts[2 * k + 1])] for k in range(parts[j], parts[j + 1])] for j in range(nparts)]
    feats.append({'type': 'Feature', 'properties': {'opened': row['OPENED'], 'closed': row['CLOSED'], 'reference': row['REFERENCE']},
                  'geometry': {'type': 'MultiLineString', 'coordinates': lines}})
out = {'type': 'FeatureCollection', 'source': 'Jeremy Atack, "Historical Geographic Information Systems (GIS) database of Nineteenth Century U.S. Canals." (August 2015), March 2017 edition', 'features': feats}
json.dump(out, open(sys.argv[2], 'w'))
print(len(feats), 'Erie Canal features ->', sys.argv[2])
````

## probe/scripts/fetch-data.sh

````bash
#!/usr/bin/env bash
# Downloads third-party inputs at pinned versions into public/ (git-ignored).
# Fonts: Google Fonts repo, SIL Open Font License 1.1.
# Map data: Natural Earth v5.1.2, public domain.
# Relief: NOAA ETOPO 2022 v1, 60 arc-second surface elevation, CC0 (doi:10.25921/fd45-gt74).
# Canal line: Jeremy Atack, 19th-century U.S. canals (2015, March 2017 edition); free use with credit.
set -euo pipefail
cd "$(dirname "$0")/.."
FONTS_SHA=d47d546884f75bbf718d3ddbb8d4627c68b9c782
NE_TAG=v5.1.2
mkdir -p public/fonts public/ne
gf="https://raw.githubusercontent.com/google/fonts/$FONTS_SHA/ofl"
curl -fsSL -o public/fonts/Fraunces.ttf "$gf/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf"
curl -fsSL -o public/fonts/Fraunces-OFL.txt "$gf/fraunces/OFL.txt"
curl -fsSL -o public/fonts/PTSansNarrow-Regular.ttf "$gf/ptsansnarrow/PT_Sans-Narrow-Web-Regular.ttf"
curl -fsSL -o public/fonts/PTSansNarrow-Bold.ttf "$gf/ptsansnarrow/PT_Sans-Narrow-Web-Bold.ttf"
curl -fsSL -o public/fonts/PTSansNarrow-OFL.txt "$gf/ptsansnarrow/OFL.txt"
ne="https://raw.githubusercontent.com/nvkelso/natural-earth-vector/$NE_TAG/geojson"
for layer in ne_10m_land ne_10m_lakes ne_10m_lakes_north_america ne_10m_rivers_lake_centerlines ne_10m_rivers_north_america; do
  curl -fsSL -o "public/ne/$layer.geojson" "$ne/$layer.geojson"
done
mkdir -p public/relief
# Every 2nd cell of lat 37.5..47.5 N, lon 84..68 W.
etopo="https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO2022/60s/60s_surface_elev_netcdf/ETOPO_2022_v1_60s_N90W180_surface.nc"
curl -fsSL -g -o public/relief/etopo_ne_us.ascii "$etopo.ascii?z[7650:2:8250][5760:2:6720]"
# Every 4th cell of lat 26..50 N, lon 96..62 W.
curl -fsSL -g -o public/relief/etopo_east.ascii "$etopo.ascii?z[6720:4:8640][4200:4:7440]"
mkdir -p public/region
curl -fsSL -o public/region/atack-canals.zip "https://cdn.vanderbilt.edu/t2-my/my-prd/wp-content/uploads/sites/133/2017/03/19thC_Canals_March2017.zip"
python3 -I scripts/erie-line.py public/region/atack-canals.zip public/region/erie-canal-atack.json
mkdir -p public/assets
# Inserts: see ../assets.md for each file's passport.
commons="https://upload.wikimedia.org/wikipedia/commons"
curl -fsSL -A "moving-atlas-probe/0.1" -o public/assets/lockport-c1855.jpg "$commons/e/e3/Erie_Canal%2C_Lockport_New_York%2C_c.1855.jpg"
python3 -c "from PIL import Image; im=Image.open('public/assets/lockport-c1855.jpg'); im.thumbnail((2400,2400)); im.save('public/assets/lockport-c1855-2400.jpg', quality=92)"
met="https://images.metmuseum.org/CRDImages"
curl -fsSL -o public/assets/met-11602-clinton-morse.jpg "$met/ad/original/DT2056.jpg"
curl -fsSL -o public/assets/met-6778-vase-1824.jpg "$met/ad/original/DT8799.jpg"
curl -fsSL -o public/assets/met-6779-vase-1825.jpg "$met/ad/original/DP140833.jpg"
curl -fsSL -o public/assets/met-5963-plate-clinton-eulogy.jpg "$met/ad/original/24304.jpg"
curl -fsSL -o public/assets/met-6144-plate-little-falls.jpg "$met/ad/original/24421.jpg"
curl -fsSL -o public/assets/met-10141-south-street.jpg "$met/ad/original/DT5570.jpg"
curl -fsSL -o public/assets/met-13116-ny-from-weehawk.jpg "$met/ad/original/ap54.90.109.jpg"
curl -fsSL -o public/assets/met-12722-sandy-hook.jpg "$met/ad/original/ap42.95.2.jpg"
curl -fsSL -o public/assets/met-339841-fleet-1825.jpg "$met/dp/original/49G_111R6.jpg"
ua="moving-atlas-probe/0.1"
curl -fsSL -A "$ua" -o public/assets/nypl-1821-map-profile.jpg "$commons/1/18/1821_A_new_map_and_profile_of_the_proposed_canal_from_Lake_Erie_to_Hudson_River_in_the_State_of_New_York%2C_from_the_New_York_Public_Library_-_510d47da-f059-a3d9-e040-e00a18064a99.jpg"
curl -fsSL -A "$ua" -o public/assets/nypl-albany-entrance-1825.jpg "$commons/0/0a/Entrance_of_the_canal_into_the_Hudson_at_Albany_%28NYPL_b13476046-422161%29.jpg"
curl -fsSL -A "$ua" -o public/assets/nypl-rochester-aqueduct-1825.jpg "$commons/c/c8/View_of_the_aqueduct_bridge_at_Rochester_%28NYPL_b13476046-424510%29.jpg"
curl -fsSL -A "$ua" -o public/assets/nypl-lockport-prospect-hill-1825.jpg "$commons/5/51/Lockport_from_Prospect_Hill_%28NYPL_b13476046-421036%29.jpg"
curl -fsSL -A "$ua" -o public/assets/nypl-deep-cutting-lockport-1825.tiff "$commons/6/61/Deep_cutting_Lockport_%28NYPL_b13476046-421034%29.tiff"
curl -fsSL -A "$ua" -o public/assets/nypl-buffalo-harbour-1825.jpg "$commons/1/18/Buffalo_Harbour_from_the_village_%28NYPL_b13476046-424509%29.jpg"
# Right sheet of the 1821 map: title, profile of levels, eastern half of the line.
python3 -c "from PIL import Image; Image.MAX_IMAGE_PIXELS=None; im=Image.open('public/assets/nypl-1821-map-profile.jpg'); c=im.crop((4900,0,im.width,1550)); c.thumbnail((3520,3520)); c.save('public/assets/nypl-1821-map-profile-crop.jpg', quality=90)"
# Episode copies: the Lockport TIFF as JPEG, and every picture at most 3200 pixels wide (`-3200` suffix) so frames render fast.
python3 - <<'PY'
import glob
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
Image.open('public/assets/nypl-deep-cutting-lockport-1825.tiff').convert('RGB').save('public/assets/nypl-deep-cutting-lockport-1825.jpg', quality=90)
for f in glob.glob('public/assets/*.jpg'):
    if f.endswith('-3200.jpg'):
        continue
    im = Image.open(f)
    if im.width > 3200:
        im.thumbnail((3200, 3200 * im.height // im.width + 1))
        im.convert('RGB').save(f[:-4] + '-3200.jpg', quality=88)
PY
sha256sum public/fonts/*.ttf public/ne/*.geojson public/relief/*.ascii public/region/atack-canals.zip public/assets/*.jpg public/assets/*.tiff
````

## probe/scripts/frames.sh

````bash
#!/usr/bin/env bash
# Renders storyboard key frames: scripts/frames.sh [FrameWall,FrameGap,...]
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
IDS=${1:-$(grep -o "\['Frame[A-Za-z0-9]*'" src/Frames.tsx | tr -d "['" | paste -sd, -)}
rm -rf out/bundle-frames
bunx remotion bundle src/index.ts --out-dir out/bundle-frames --log=error
mkdir -p out/frames
for id in ${IDS//,/ }; do
  bunx remotion still out/bundle-frames "$id" "out/frames/$id.png" --log=error
done
````

## probe/scripts/profiles.ts

````ts
// Terrain profiles for the "only low gap" chart: height of the ground along two lines west from the coast.
//   bun scripts/profiles.ts   -> public/region/profiles.json
// A: New York up the Hudson to Albany, then the Erie Canal line (J. Atack) to Buffalo.
// B: Philadelphia to Pittsburgh through Harrisburg, the Juniata valley, Hollidaysburg and Johnstown.
// Ground height: NOAA ETOPO 2022, 60 arc-second grid sampled every 2 cells (about 3.7 km). Each point takes the
// lowest cell within one cell around it, so a line along a narrow valley reads the valley floor, not its sides.
// The same rule is used for both lines.
// Water surfaces (the tidal Hudson) are set to sea level. Line B is drawn by us between towns.
import {readFileSync, writeFileSync} from 'node:fs';
import {hudson} from '../src/erie';

type Pt = [number, number];
const txt = readFileSync('public/relief/etopo_ne_us.ascii', 'utf8');
const body = txt.split('---------------------------------------------')[1];
const [zPart, rest] = body.split('z.lat[');
const [latPart, lonPart] = rest.split('z.lon[');
const nums = (s: string) => s.split(/[\s,]+/).filter((t) => /^-?\d/.test(t)).map(Number);
const lat = nums(latPart.slice(latPart.indexOf(']') + 1));
const lon = nums(lonPart.slice(lonPart.indexOf(']') + 1));
const rows = zPart.trim().split('\n').slice(1).map((l) => nums(l.slice(l.indexOf(']') + 1)));

function height([x, y]: Pt) {
  const i = Math.round(((y - lat[0]) / (lat[lat.length - 1] - lat[0])) * (lat.length - 1));
  const j = Math.round(((x - lon[0]) / (lon[lon.length - 1] - lon[0])) * (lon.length - 1));
  let low = Infinity;
  for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) low = Math.min(low, rows[i + di][j + dj]);
  return low;
}

const miles = (a: Pt, b: Pt) => {
  const r = Math.PI / 180;
  const h = Math.sin(((b[1] - a[1]) * r) / 2) ** 2 + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(((b[0] - a[0]) * r) / 2) ** 2;
  return 2 * 3958.8 * Math.asin(Math.sqrt(h));
};

// Chain the canal segments into one line, starting at the end nearest Albany.
function canalLine(): Pt[] {
  const fc = JSON.parse(readFileSync('public/region/erie-canal-atack.json', 'utf8'));
  let parts: Pt[][] = fc.features.flatMap((f: any) => f.geometry.coordinates);
  const albany: Pt = [-73.755, 42.651];
  const out: Pt[] = [];
  let at = albany;
  while (parts.length) {
    let best = 0;
    let flip = false;
    let d = Infinity;
    parts.forEach((p, i) => {
      const [s, e] = [miles(at, p[0]), miles(at, p[p.length - 1])];
      if (s < d) [d, best, flip] = [s, i, false];
      if (e < d) [d, best, flip] = [e, i, true];
    });
    const p = flip ? [...parts[best]].reverse() : parts[best];
    out.push(...p);
    at = p[p.length - 1];
    parts = parts.filter((_, i) => i !== best);
  }
  return out;
}

function profile(line: Pt[], water: (m: number) => boolean) {
  const xs: number[] = [];
  const ft: number[] = [];
  let total = 0;
  let next = 0;
  for (let i = 1; i < line.length; i++) {
    const seg = miles(line[i - 1], line[i]);
    while (next <= total + seg) {
      const t = seg ? (next - total) / seg : 0;
      const p: Pt = [line[i - 1][0] + (line[i][0] - line[i - 1][0]) * t, line[i - 1][1] + (line[i][1] - line[i - 1][1]) * t];
      xs.push(Math.round(next));
      ft.push(water(next) ? 0 : Math.max(0, Math.round(height(p) * 3.28084)));
      next += 2;
    }
    total += seg;
  }
  return {miles: xs, ft, length: Math.round(total)};
}

const hudsonUp = [...hudson].reverse() as Pt[];
const hudsonMiles = hudsonUp.slice(1).reduce((s, p, i) => s + miles(hudsonUp[i], p), 0);
const a = profile([...hudsonUp, ...canalLine()], (m) => m <= hudsonMiles);
const b = profile(
  [[-75.165, 39.952], [-76.306, 40.038], [-76.884, 40.264], [-77.571, 40.599], [-78.011, 40.485], [-78.389, 40.427], [-78.922, 40.327], [-79.26, 40.43], [-79.996, 40.441]],
  () => false,
);
const max = (p: {ft: number[]}) => Math.max(...p.ft);
const out = {
  source: 'NOAA ETOPO 2022 (60 arc-second, every 2nd cell); canal line J. Atack (2015); line B drawn between towns',
  a: {name: 'New York → Albany → Buffalo', ...a, max: max(a)},
  b: {name: 'Philadelphia → Pittsburgh', ...b, max: max(b)},
};
writeFileSync('public/region/profiles.json', JSON.stringify(out));
console.log(`A ${a.length} mi, max ${out.a.max} ft; B ${b.length} mi, max ${out.b.max} ft; Hudson ${hudsonMiles.toFixed(0)} mi`);
````

## probe/scripts/render-parts.sh

````bash
#!/usr/bin/env bash
# Renders a composition in parts and joins them without re-encoding, printing seconds per part:
#   scripts/render-parts.sh Episode out/episode 0-6896 6897-11801 ...   renders out/episode/<range>.mp4 if missing
#   scripts/render-parts.sh --join out/episode out/episode.mp4            joins the parts in frame order
# Re-render one part after a fix: delete its file and run again.
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
if [ "$1" = "--join" ]; then
  (cd "$2" && ls | grep -E '^[0-9]+-[0-9]+\.mp4$' | sort -n | sed "s|.*|file '$PWD/&'|") > "$2/list.txt"
  bunx remotion ffmpeg -y -loglevel error -f concat -safe 0 -i "$2/list.txt" -c copy "$3"
  exit 0
fi
COMP=$1 DIR=$2
shift 2
mkdir -p "$DIR"
B=out/bundle-parts
# The bundle step is sometimes killed when the shared server runs short of memory: up to 4 tries.
for try in 1 2 3 4; do
  rm -rf "${B:?}"
  bunx remotion bundle src/index.ts --out-dir "$B" --log=error && [ -f "$B/index.html" ] && break
  [ "$try" = 4 ] && exit 1
  sleep 20
done
for r in "$@"; do
  [ -f "$DIR/$r.mp4" ] && continue
  start=$(date +%s)
  bunx remotion render "$B" "$COMP" "$DIR/$r.tmp.mp4" --frames="$r" --codec=h264 --crf=18 --muted --concurrency="${CONC:-3}" --log=error
  mv "$DIR/$r.tmp.mp4" "$DIR/$r.mp4"
  echo "$r render_seconds=$(($(date +%s) - start))"
done
````

## probe/scripts/render.sh

````bash
#!/usr/bin/env bash
# Renders a composition and prints wall-clock seconds:
#   scripts/render.sh [Probe|Pilot] [out file]   (default: Probe to out/style-probe.mp4)
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
rm -rf out/bundle
start=$(date +%s)
bunx remotion bundle src/index.ts --out-dir out/bundle --log=error
bunx remotion render out/bundle "${1:-Probe}" "${2:-out/style-probe.mp4}" --codec=h264 --crf=18 --muted --concurrency="${CONC:-3}" --log=error
end=$(date +%s)
echo "render_seconds=$((end - start))"
````

## probe/scripts/stills.sh

````bash
#!/usr/bin/env bash
# Renders single frames for review: scripts/stills.sh 0,150,330 [out_dir] [composition]
# BUNDLE=out/bundle-x keeps a separate bundle, so two reviews can run at once.
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
OUT=${2:-out/stills}
B=${BUNDLE:-out/bundle-stills}
rm -rf "${B:?}"
bunx remotion bundle src/index.ts --out-dir "$B" --log=error
mkdir -p "$OUT"
for n in ${1//,/ }; do
  bunx remotion still "$B" "${3:-Probe}" "$OUT/f$(printf %04d "$n").png" --frame="$n" --log=error
done
````

## probe/scripts/thumbs.sh

````bash
#!/usr/bin/env bash
# Renders the thumbnail variants to out/thumbs/*.png
set -euo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_DIR"
rm -rf out/bundle
bunx remotion bundle src/index.ts --out-dir out/bundle --log=error
mkdir -p out/thumbs
for id in ThumbA ThumbB ThumbC; do
  bunx remotion still out/bundle "$id" "out/thumbs/$id.png" --log=error
done
````

## probe/scripts/voice-text.ts

````ts
// Writes the voiceover text for ElevenLabs from ../script.md: plain English, one block per chapter,
// no markup. Headings in capitals name the chapter and are not read; each chapter is one request.
//   bun scripts/voice-text.ts   -> ../voiceover-en.txt
import {readFileSync, writeFileSync} from 'node:fs';

const md = readFileSync(new URL('../../script.md', import.meta.url), 'utf8');
const heads: Record<string, string> = {'Холодное начало': 'COLD OPEN', 'Ключ': 'KEY'};
const out: string[] = [];
let chars = 0;
for (const part of md.split(/^## /m).slice(1)) {
  const [head, ...rest] = part.split('\n');
  const paras = rest.filter((l) => l.startsWith('> ') && l.length > 2).map((l) => l.slice(2).trim());
  if (!paras.length) continue;
  const name = heads[head] ?? `CHAPTER ${head.replace(/^(\d+)\. /, '$1. ').toUpperCase()}`;
  out.push(name, '', paras.join('\n\n'), '');
  chars += paras.join(' ').length;
}
writeFileSync(new URL('../../voiceover-en.txt', import.meta.url), out.join('\n'));
console.log(`${out.filter((l) => /^(COLD|KEY|CHAPTER)/.test(l)).length} blocks, ${chars} characters to read`);
````

## probe/src/Brand.tsx

````tsx
// Branding stills: renders the SVG written by scripts/brand.ts with the channel fonts loaded.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {fontFiles} from './theme';

const SvgFile: React.FC<{file: string}> = ({file}) => {
  const [handle] = useState(() => delayRender(file));
  const [svg, setSvg] = useState('');
  useEffect(() => {
    Promise.all([
      fetch(staticFile(`brand/${file}`)).then((r) => r.text()),
      ...fontFiles.map((x) => new FontFace(x.family, `url(${staticFile(x.file)})`, {weight: x.weight}).load()),
    ]).then(([text, ...faces]) => {
      (faces as FontFace[]).forEach((f) => document.fonts.add(f));
      setSvg(text as string);
      continueRender(handle);
    });
  }, [file, handle]);
  return <AbsoluteFill dangerouslySetInnerHTML={{__html: svg}} />;
};

export const Avatar: React.FC = () => <SvgFile file="avatar.svg" />;
export const Banner: React.FC = () => <SvgFile file="banner.svg" />;
export const BannerCheck: React.FC = () => <SvgFile file="banner-check.svg" />;
````

## probe/src/Episode.tsx

````tsx
// The whole episode: part 1 (cold open, key, chapter 1, also the pilot) and chapters 2–6, then the end card.
import {FPS} from './theme';
import {TOTAL} from './narration';
import {makeFilm} from './kit';
import {PART1, V} from './Pilot';
import {PART2} from './ch2';
import {PART3} from './ch3';
import {PART4} from './ch4';
import {PART5} from './ch5';
import {END_CARD, PART6} from './ch6';
import {INSERTS_A} from './pages-a';
import {INSERTS_B} from './pages-b';

export const Episode = makeFilm(
  [PART1, PART2, PART3, PART4, PART5, PART6, {inserts: INSERTS_A}, {inserts: INSERTS_B}],
  V.harbor,
  'Draft · silent, timed for a voiceover',
);
export const EPISODE_FRAMES = Math.ceil((TOTAL + END_CARD) * FPS);
````

## probe/src/Frames.tsx

````tsx
// Storyboard key frames: one still per planned scene type, same style as the probe.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, continueRender, delayRender, staticFile} from 'remotion';
import {geoConicConformal, geoPath} from 'd3-geo';
import east from '../public/region/east.json';
import erie from '../public/region/erie.json';
import canal from '../public/region/erie-canal-atack.json';
import {C, F, H, W, fontFiles} from './theme';
import {hudson} from './erie';

type LonLat = [number, number];
type Region = typeof erie;

const useFonts = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(fontFiles.map((x) => new FontFace(x.family, `url(${staticFile(x.file)})`, {weight: x.weight}).load())).then((faces) => {
      faces.forEach((face) => document.fonts.add(face));
      continueRender(handle);
    });
  }, [handle]);
};

const label: React.CSSProperties = {fontFamily: F.label, letterSpacing: '0.16em', textTransform: 'uppercase'};
const title: React.CSSProperties = {fontFamily: F.title, color: C.ink, fontVariationSettings: '"opsz" 72, "SOFT" 50', lineHeight: 1.05};

const makeProj = (box: number[], rotate: number, parallels: [number, number], bottom = H) =>
  geoConicConformal().parallels(parallels).rotate([rotate, 0]).fitExtent([[0, 0], [W, bottom]], {
    type: 'MultiPoint',
    coordinates: [[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]],
  } as any);

const Base: React.FC<{region: Region; proj: ReturnType<typeof makeProj>; children?: React.ReactNode}> = ({region, proj, children}) => {
  const path = geoPath(proj);
  return (
    <svg width={W} height={H} style={{position: 'absolute'}}>
      <rect width={W} height={H} fill={C.water} />
      <path d={path(region.land as any) ?? ''} fill={C.land} />
      {region.relief.map((r, i) => (
        <path key={i} d={path(r.geometry as any) ?? ''} fill={C.relief} fillOpacity={0.36} />
      ))}
      <path d={path(region.lakes as any) ?? ''} fill={C.water} stroke="#AEC0C3" strokeWidth={1} />
      <path d={path({type: 'GeometryCollection', geometries: region.rivers.map((r) => ({type: 'LineString', coordinates: r.coords}))} as any) ?? ''}
        fill="none" stroke={C.river} strokeWidth={1.8} />
      {children}
    </svg>
  );
};

const Town: React.FC<{p: [number, number]; name: string; dx?: number; dy?: number; anchor?: 'start' | 'end' | 'middle'; big?: boolean}> = ({p, name, dx = 14, dy = 9, anchor = 'start', big}) => (
  <g>
    <circle cx={p[0]} cy={p[1]} r={big ? 10 : 7} fill={C.ink} stroke={C.land} strokeWidth={2.5} />
    <text x={p[0] + dx} y={p[1] + dy} textAnchor={anchor} style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink}>
      {name}
    </text>
  </g>
);

const Ruler: React.FC<{from: number; to: number; at: number; note: string}> = ({from, to, at, note}) => {
  const [x0, x1, y] = [140, 1780, 996];
  const xs = (yr: number) => x0 + ((yr - from) / (to - from)) * (x1 - x0);
  const ticks = Array.from({length: 9}, (_, i) => Math.round(from + (i * (to - from)) / 8));
  return (
    <g>
      <rect x={0} y={H - 116} width={W} height={116} fill={C.paper} />
      <line x1={x0} x2={x1} y1={y} y2={y} stroke={C.ink} strokeWidth={2} />
      {ticks.map((t) => (
        <g key={t}>
          <line x1={xs(t)} x2={xs(t)} y1={y - 8} y2={y + 8} stroke={C.ink} strokeWidth={2} />
          <text x={xs(t)} y={y + 40} textAnchor="middle" style={{...label, fontSize: 24}} fill={C.ink}>{t}</text>
        </g>
      ))}
      <circle cx={xs(at)} cy={y} r={9} fill={C.accent} />
      <text x={xs(at)} y={y - 20} textAnchor="middle" style={{...label, fontSize: 22}} fill={C.accent}>{note}</text>
    </g>
  );
};

const Note: React.FC<{children: React.ReactNode}> = ({children}) => (
  <text x={110} y={H - 140} style={{fontFamily: F.label, fontSize: 22}} fill={C.ink} fillOpacity={0.66}>{children}</text>
);

// 1. The wall: a country of the coast, the mountains behind it.
export const FrameWall: React.FC = () => {
  useFonts();
  const proj = makeProj([-92.5, 28.6, -68, 44.5], 80, [33, 45], H - 116);
  const P = (p: LonLat) => proj(p) as [number, number];
  const flow: LonLat[] = [[-80.0, 40.44], [-82.6, 38.7], [-84.5, 39.1], [-85.8, 38.25], [-87.6, 37.9], [-89.1, 37.0], [-89.6, 35.1], [-91.1, 33.0], [-91.2, 31.3], [-90.07, 29.95]];
  const flowPts = flow.map(P);
  return (
    <AbsoluteFill>
      <Base region={east as Region} proj={proj}>
        <polyline points={flowPts.map((p) => p.join(',')).join(' ')} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray="14 10" strokeLinecap="round" />
        <path d={`M${flowPts[flowPts.length - 2].join(',')} L${flowPts[flowPts.length - 1].join(',')}`} stroke={C.ink} strokeWidth={4} markerEnd="url(#arr)" />
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={C.ink} /></marker>
        </defs>
        <Town p={P([-71.06, 42.36])} name="Boston" />
        <Town p={P([-74.01, 40.71])} name="New York" />
        <Town p={P([-75.16, 39.95])} name="Philadelphia" dx={-14} anchor="end" />
        <Town p={P([-76.61, 39.29])} name="Baltimore" dx={-14} anchor="end" />
        <Town p={P([-90.07, 29.95])} name="New Orleans" dx={16} dy={-12} />
        <text x={P([-83.6, 39.9])[0]} y={P([-83.6, 39.9])[1]} textAnchor="middle" style={{...label, fontSize: 30, fontStyle: 'italic'}} fill={C.ink} fillOpacity={0.75}>Ohio Valley farms</text>
        <text x={P([-81.2, 36.6])[0]} y={P([-81.2, 36.6])[1]} transform={`rotate(-36,${P([-81.2, 36.6])[0]},${P([-81.2, 36.6])[1]})`} textAnchor="middle"
          style={{...label, fontSize: 34, letterSpacing: '0.5em', fontWeight: 700}} fill="#9C8456">Appalachians</text>
        <Ruler from={1790} to={1830} at={1800} note="1800" />
        <Note>Dashed: usual route of western farm goods to market, schematic · modern coastline and rivers · Natural Earth, NOAA ETOPO 2022</Note>
      </Base>
      <div style={{position: 'absolute', left: 110, top: 92}}>
        <div style={{...title, fontSize: 72}}>A country of the coast</div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>The cheapest way to market ran downriver</div>
      </div>
    </AbsoluteFill>
  );
};

// 2. The gap: Hudson and Mohawk, the low road through the mountains.
export const FrameGap: React.FC = () => {
  useFonts();
  const proj = makeProj([-79.8, 40.4, -72.6, 44.9], 76, [40.5, 44]);
  const P = (p: LonLat) => proj(p) as [number, number];
  const path = geoPath(proj);
  const mohawk: LonLat[] = [[-73.7, 42.78], [-73.94, 42.82], [-74.37, 42.95], [-74.86, 43.04], [-75.23, 43.1], [-75.46, 43.21]];
  return (
    <AbsoluteFill>
      <Base region={erie as Region} proj={proj}>
        <path d={path({type: 'LineString', coordinates: hudson} as any) ?? ''} fill="none" stroke={C.force} strokeWidth={9} strokeLinecap="round" strokeOpacity={0.85} />
        <path d={path({type: 'LineString', coordinates: mohawk} as any) ?? ''} fill="none" stroke={C.force} strokeWidth={9} strokeLinecap="round" strokeOpacity={0.85} />
        {[['ADIRONDACKS', [-74.4, 43.72]], ['CATSKILLS', [-74.35, 42.12]], ['ALLEGHENY PLATEAU', [-77.4, 42.1]]].map(([n, at]) => {
          const p = P(at as LonLat);
          return <text key={n as string} x={p[0]} y={p[1]} textAnchor="middle" style={{...label, fontSize: 30, letterSpacing: '0.4em', fontWeight: 700}} fill="#9C8456">{n as string}</text>;
        })}
        <text x={P([-74.75, 42.88])[0]} y={P([-74.75, 42.88])[1] + 46} textAnchor="middle" style={{...label, fontSize: 26, fontStyle: 'italic'}} fill={C.force}>Mohawk Valley</text>
        <text x={P([-73.6, 41.6])[0] + 22} y={P([-73.6, 41.6])[1]} style={{...label, fontSize: 26, fontStyle: 'italic'}} fill={C.force}>Hudson River</text>
        <Town p={P([-73.755, 42.651])} name="Albany" />
        <Town p={P([-74.015, 40.704])} name="New York" />
        <Town p={P([-78.878, 42.886])} name="Buffalo" dx={-14} anchor="end" />
        <Ruler from={1790} to={1830} at={1810} note="1810" />
        <Note>Relief: tan above 150 m · modern coastline and rivers · Natural Earth, NOAA ETOPO 2022</Note>
      </Base>
      <div style={{position: 'absolute', left: 110, top: 92}}>
        <div style={{...title, fontSize: 72}}>The low road west</div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>Hudson and Mohawk, near water level</div>
      </div>
    </AbsoluteFill>
  );
};

// Insert on paper with caption, credit and mini-map.
const Insert: React.FC<{src: string; ratio: number; kicker: string; head: string; body: string; tag: string; credit: string; plaque: string; at: LonLat; imgW?: number}> = (p) => {
  const iw = p.imgW ?? 1120;
  const ih = iw / p.ratio;
  const proj = makeProj([-81, 39.5, -71, 45.5], 76, [40.5, 44]);
  const at = proj(p.at) as [number, number];
  const k = 1.2;
  const path = geoPath(proj);
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <Img src={staticFile(p.src)} style={{position: 'absolute', left: 100, top: (H - ih) / 2 - 10, width: iw, height: ih, outline: `1px solid ${C.rule}`}} />
      <div style={{position: 'absolute', left: 100 + iw + 48, top: 250, width: W - iw - 248, color: C.ink}}>
        <div style={{...label, fontSize: 27, opacity: 0.72}}>{p.kicker}</div>
        <div style={{...title, fontSize: 60, marginTop: 14}}>{p.head}</div>
        <div style={{fontFamily: F.label, fontSize: 38, lineHeight: 1.28, marginTop: 22}}>{p.body}</div>
        <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16}}>{p.tag}</div>
        <div style={{height: 1, background: C.rule, margin: '30px 0 22px'}} />
        <div style={{fontFamily: F.label, fontSize: 28, lineHeight: 1.32}}>{p.credit}</div>
        <div style={{display: 'inline-block', marginTop: 16, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 23, letterSpacing: '0.12em'}}>{p.plaque}</div>
      </div>
      <svg width={220} height={220} style={{position: 'absolute', left: 1650, top: 54}}>
        <defs><clipPath id="mini"><circle cx={110} cy={110} r={100} /></clipPath></defs>
        <g clipPath="url(#mini)">
          <rect width={220} height={220} fill={C.water} />
          <g transform={`translate(${110 - at[0] * k},${110 - at[1] * k}) scale(${k})`}>
            <path d={path(erie.land as any) ?? ''} fill={C.land} />
            <path d={path(erie.lakes as any) ?? ''} fill={C.water} />
            <path d={path(canal as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={3 / k} />
          </g>
          <circle cx={110} cy={110} r={8} fill={C.accent} />
        </g>
        <circle cx={110} cy={110} r={100} fill="none" stroke={C.ink} strokeWidth={2.5} />
      </svg>
    </AbsoluteFill>
  );
};

// 3. The engineers' own drawing: 1821 map and profile.
export const FrameProfile1821: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <Img src={staticFile('assets/nypl-1821-map-profile-crop.jpg')} style={{position: 'absolute', left: 80, top: 150, width: 1760, outline: `1px solid ${C.rule}`}} />
      <div style={{position: 'absolute', left: 80, top: 60, ...label, fontSize: 27, color: C.ink, opacity: 0.72}}>Document · 1821</div>
      <div style={{position: 'absolute', left: 80, top: 760, width: 1100, color: C.ink}}>
        <div style={{...title, fontSize: 58}}>The climb, drawn by the builders</div>
        <div style={{fontFamily: F.label, fontSize: 36, lineHeight: 1.3, marginTop: 16}}>Profile of the levels and lifts of the locks between Lake Erie and the Hudson.</div>
      </div>
      <div style={{position: 'absolute', left: 1240, top: 790, width: 600, color: C.ink}}>
        <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>A New Map and Profile of the Proposed Canal from Lake Erie to Hudson River, 1821. Canal Commissioners of New York.</div>
        <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>From The New York Public Library · Public domain</div>
      </div>
    </AbsoluteFill>
  );
};

// 4. How a lock works: own drawing, side section and plan.
export const FrameLock: React.FC = () => {
  useFonts();
  const [x0, x1, y0] = [400, 1500, 640];
  const lift = 150;
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <div style={{position: 'absolute', left: 110, top: 70}}>
        <div style={{...label, fontSize: 27, color: C.ink, opacity: 0.72}}>Diagram · how a lock works</div>
        <div style={{...title, fontSize: 64, marginTop: 12}}>One step up</div>
      </div>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {/* ground and walls */}
        <path d={`M${x0 - 290},${y0} L${x0},${y0} L${x0},${y0 + 60} L${x1},${y0 + 60} L${x1},${y0 - lift + 20} L${x1 + 260},${y0 - lift + 20} L${x1 + 260},${y0 + 140} L${x0 - 290},${y0 + 140} Z`} fill="#D9CDB4" stroke={C.ink} strokeWidth={2} />
        {/* lower level water */}
        <rect x={x0 - 290} y={y0 - 90} width={290} height={90} fill={C.water} />
        {/* chamber filled to the upper level */}
        <rect x={x0} y={y0 - lift - 50} width={x1 - x0} height={lift + 110} fill={C.water} />
        <rect x={x1} y={y0 - lift - 50} width={260} height={70} fill={C.water} />
        {/* gates */}
        <rect x={x0 - 8} y={y0 - lift - 90} width={16} height={lift + 150} fill={C.ink} />
        <rect x={x1 - 8} y={y0 - lift - 90} width={16} height={lift + 80} fill={C.ink} />
        {/* boat risen to the upper level */}
        <path d={`M${x0 + 420},${y0 - lift - 50} L${x0 + 760},${y0 - lift - 50} L${x0 + 730},${y0 - lift - 10} L${x0 + 450},${y0 - lift - 10} Z`} fill={C.ink} />
        <rect x={x0 + 500} y={y0 - lift - 84} width={180} height={34} rx={3} fill={C.ink} />
        {/* arrows: water in from above, boat rises */}
        <path d={`M${x1 + 200},${y0 - lift - 20} C${x1 + 120},${y0 - lift + 60} ${x1 + 40},${y0 - lift + 60} ${x1 - 60},${y0 - lift + 40}`} fill="none" stroke={C.force} strokeWidth={5} markerEnd="url(#a2)" />
        <path d={`M${x0 + 590},${y0 + 20} L${x0 + 590},${y0 - lift - 100}`} stroke={C.accent} strokeWidth={5} markerEnd="url(#a3)" strokeDasharray="1 0" />
        <defs>
          <marker id="a2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={C.force} /></marker>
          <marker id="a3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={C.accent} /></marker>
        </defs>
        <text x={x1 + 130} y={y0 - lift - 70} textAnchor="middle" style={{...label, fontSize: 26}} fill={C.ink}>upper level</text>
        <text x={x1 - 300} y={y0 - lift + 70} textAnchor="middle" style={{...label, fontSize: 26}} fill={C.force}>water flows in</text>
        <text x={x0 - 270} y={y0 - 110} textAnchor="start" style={{...label, fontSize: 26}} fill={C.ink}>lower level</text>
        <text x={x0 + 620} y={y0 + 40} style={{...label, fontSize: 26}} fill={C.accent}>the boat rises</text>
        <text x={x0} y={y0 - lift - 110} textAnchor="middle" style={{...label, fontSize: 26}} fill={C.ink}>lower gate</text>
        <text x={x1} y={y0 - lift - 110} textAnchor="middle" style={{...label, fontSize: 26}} fill={C.ink}>upper gate</text>
        {/* plan view of the mitre gates */}
        <g transform="translate(1440,905)">
          <rect x={-10} y={-70} width={320} height={140} fill={C.water} />
          <line x1={-10} x2={310} y1={-70} y2={-70} stroke={C.ink} strokeWidth={6} />
          <line x1={-10} x2={310} y1={70} y2={70} stroke={C.ink} strokeWidth={6} />
          <polyline points="120,-70 170,0 120,70" fill="none" stroke={C.ink} strokeWidth={10} />
          <path d="M290,0 L200,0" stroke={C.force} strokeWidth={5} markerEnd="url(#a2)" />
          <text x={150} y={110} textAnchor="middle" style={{...label, fontSize: 22}} fill={C.ink}>seen from above: gates meet in a V</text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 110, top: 900, width: 1300, fontFamily: F.label, fontSize: 30, color: C.ink, opacity: 0.8}}>
        Schematic, not to scale. Heights and lift per lock from the episode fact sheet.
      </div>
    </AbsoluteFill>
  );
};

export const FrameLockport1825: React.FC = () => {
  useFonts();
  return (
    <Insert src="assets/nypl-lockport-prospect-hill-1825.jpg" ratio={3848 / 2791} kicker="Lockport, New York" head="Two staircases in the rock"
      body="One flight of locks for boats going up, one for boats coming down." tag="documented"
      credit="Lockport from Prospect Hill. Plate in Colden's Memoir of the canal celebration, 1825."
      plaque="From The New York Public Library · Public domain" at={[-78.69, 43.171]} imgW={1040} />
  );
};

// 6. Ten days in 1825: the cannon relay, Buffalo to New York. Total time from the fact sheet.
const RELAY = {head: 'Gun to gun in about 80 minutes', sub: 'Buffalo 10:00 · New York 11:19 · Sandy Hook 11:21 · October 26, 1825'};
export const FrameRelay: React.FC = () => {
  useFonts();
  const proj = makeProj([-79.4, 40.45, -72.9, 44.1], 76, [40.5, 44], H - 116);
  const P = (p: LonLat) => proj(p) as [number, number];
  const path = geoPath(proj);
  const guns: LonLat[] = [
    [-78.878, 42.886], [-78.69, 43.171], [-78.194, 43.246], [-77.609, 43.157], [-77.095, 43.047], [-76.703, 43.01], [-76.147, 43.048],
    [-75.456, 43.213], [-75.233, 43.101], [-74.86, 43.043], [-74.374, 42.955], [-73.94, 42.814], [-73.755, 42.651],
    [-73.79, 42.25], [-73.93, 41.93], [-73.92, 41.7], [-73.96, 41.39], [-73.87, 41.08], [-74.015, 40.704],
  ];
  const fired = 9;
  const front = P(guns[fired - 1]);
  return (
    <AbsoluteFill>
      <Base region={erie as Region} proj={proj}>
        <path d={path({type: 'LineString', coordinates: hudson} as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" strokeOpacity={0.5} />
        <path d={path(canal as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" />
        {[1, 2, 3].map((k) => (
          <circle key={k} cx={front[0]} cy={front[1]} r={26 * k} fill="none" stroke={C.accent} strokeWidth={4 - k} strokeOpacity={1 - k * 0.25} />
        ))}
        {guns.map((g, i) => {
          const p = P(g);
          return <circle key={i} cx={p[0]} cy={p[1]} r={9} fill={i < fired ? C.accent : C.land} stroke={C.ink} strokeWidth={2.5} />;
        })}
        <Town p={P([-78.878, 42.886])} name="Buffalo" dx={-18} dy={34} anchor="end" />
        <Town p={P([-75.233, 43.101])} name="Utica" dx={0} dy={52} anchor="middle" />
        <Town p={P([-73.755, 42.651])} name="Albany" dx={18} />
        <Town p={P([-74.015, 40.704])} name="New York" dx={18} />
        <Ruler from={1817} to={1833} at={1825} note="Oct 26, 1825" />
        <Note>Gun positions schematic · canal line J. Atack (2015), approximate · Natural Earth, NOAA ETOPO 2022</Note>
      </Base>
      <div style={{position: 'absolute', left: 110, top: 92}}>
        <div style={{...title, fontSize: 72}}>{RELAY.head}</div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>{RELAY.sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// 7. The flood: city populations, census figures from the fact sheet. Circle area follows population.
const POP: {name: string; at: LonLat; a: number; b: number; dx?: number; anchor?: 'start' | 'end'}[] = [
  {name: 'New York', at: [-74.01, 40.71], a: 123706, b: 813669, anchor: 'end', dx: -40},
  {name: 'Brooklyn', at: [-73.95, 40.65], a: 7175, b: 266661, dx: 40},
  {name: 'Philadelphia', at: [-75.16, 39.95], a: 137097, b: 565529, anchor: 'end'},
  {name: 'Baltimore', at: [-76.61, 39.29], a: 62738, b: 212418, anchor: 'end'},
  {name: 'Boston', at: [-71.06, 42.36], a: 43298, b: 177840},
];
const POP_YEARS = [1820, 1860];
export const FramePopulation: React.FC = () => {
  useFonts();
  const proj = makeProj([-79.5, 37.6, -69.4, 43.4], 76, [37, 43], H - 116);
  const P = (p: LonLat) => proj(p) as [number, number];
  const r = (n: number) => Math.sqrt(n) * 0.12;
  const fmt = (n: number) => n.toLocaleString('en-US');
  return (
    <AbsoluteFill>
      <Base region={east as Region} proj={proj}>
        <path d={geoPath(proj)(canal as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" />
        {POP.map((c) => {
          const p = P(c.at);
          const end = c.anchor === 'end';
          const tx = p[0] + (end ? -1 : 1) * (r(c.b) + 14) + (c.dx ?? 0);
          return (
            <g key={c.name}>
              <circle cx={p[0]} cy={p[1]} r={r(c.b)} fill={C.accent} fillOpacity={0.28} stroke={C.accent} strokeWidth={3} />
              <circle cx={p[0]} cy={p[1]} r={r(c.a)} fill={C.ink} fillOpacity={0.85} />
              <text x={tx} y={p[1] - 6} textAnchor={end ? 'end' : 'start'} style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink}>{c.name}</text>
              <text x={tx} y={p[1] + 26} textAnchor={end ? 'end' : 'start'} style={{fontFamily: F.label, fontSize: 26, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink}>
                {fmt(c.a)} → {fmt(c.b)}
              </text>
            </g>
          );
        })}
        <Ruler from={1790} to={1870} at={POP_YEARS[1]} note={`${POP_YEARS[0]} → ${POP_YEARS[1]}`} />
        <Note>Census, Gibson 1998 (WP27) and Forstall 1996 · Philadelphia: whole county both years · New York: Manhattan · Brooklyn separate until 1898</Note>
      </Base>
      <div style={{position: 'absolute', left: 110, top: 92}}>
        <div style={{...title, fontSize: 72}}>The end of the line grew fastest</div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>People counted by the census, {POP_YEARS[0]} (dark) and {POP_YEARS[1]} (red)</div>
      </div>
    </AbsoluteFill>
  );
};

export const FRAMES = [
  ['FrameWall', FrameWall],
  ['FrameGap', FrameGap],
  ['FrameProfile1821', FrameProfile1821],
  ['FrameLock', FrameLock],
  ['FrameLockport1825', FrameLockport1825],
  ['FrameRelay', FrameRelay],
  ['FramePopulation', FramePopulation],
] as const;
````

## probe/src/Pilot.tsx

````tsx
// Part 1 of the film: cold open, key and chapter 1 ("The Wall"). Also the pilot cut on its own.
// One map and one camera (src/kit.tsx); inserts open from a point of the map through a lens and close back into it.
// No subtitles and no sound: the picture is timed for a later ElevenLabs voice (src/narration.ts).
import React from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import east from '../public/region/east.json';
import erie from '../public/region/erie.json';
import profiles from '../public/region/profiles.json';
import {C, F, FPS, W} from './theme';
import {canal, hudson} from './erie';
import {S, lineWith} from './narration';
import {
  ALBANY, Arrow, BUFFALO, Boat, CUMBERLAND, CUMBERLAND_GAP, Ctx, Flatboat, G, Head, Horse, Ins, Lbl, LonLat, Move, NEW_ORLEANS, NYC,
  Note, P, PHILADELPHIA, Part, PITTSBURGH, PicPage, Picture, ROME, Ripples, SANDY, SideText, TROY, View, WHEELING, Wagon, XY, YearKey,
  cut, label, line, makeFilm, makeYearAt, mkLine, nearest, ramp, scr, segment, smooth, title, win,
} from './kit';

const romeAt = canal.findIndex((p) => p[0] === ROME[0]);
const L = {
  // Path of the keg's water, Sandy Hook back to Lake Erie: harbour, Hudson, canal.
  water: smooth([SANDY, ...[...hudson].reverse(), ...canal.slice(1)], 6),
  digEast: smooth(canal.slice(0, romeAt + 1).reverse()),
  digWest: smooth(canal.slice(romeAt)),
  canal: smooth(canal),
  west: smooth(canal.slice(romeAt)),
  hudsonUp: smooth([...[...hudson].reverse(), TROY], 6),
  // Settler routes over the mountains, schematic: Pennsylvania to the Ohio, Virginia through the Cumberland Gap.
  settlersPa: smooth([PHILADELPHIA, [-77.4, 40.25], PITTSBURGH, [-81.3, 39.95]]),
  settlersVa: smooth([[-78.4, 37.6], [-81.3, 36.85], CUMBERLAND_GAP, [-84.3, 37.2]]),
  road: smooth([CUMBERLAND, [-79.72, 39.9], [-80.25, 40.17], WHEELING]),
  // Ohio from Pittsburgh to Cairo, then the Mississippi to New Orleans (Natural Earth centrelines).
  flatboat: (() => {
    const ohio = east.rivers.filter((r) => r.name === 'Ohio' && r.coords.length > 10).sort((a, b) => b.coords[0][0] - a.coords[0][0]);
    const m1 = east.rivers.find((r) => r.name === 'Mississippi' && r.coords.length === 261)!.coords;
    const m2 = east.rivers.find((r) => r.name === 'Mississippi' && r.coords.length === 387)!.coords;
    const pts = [...ohio.flatMap((r) => r.coords), ...m1.slice(nearest(m1, [-89.18, 37.0])), ...m2.slice(0, nearest(m2, NEW_ORLEANS) + 1)];
    return mkLine(pts.map((c) => P(c as LonLat)));
  })(),
  mohawk: (() => {
    const m = erie.rivers.find((r) => r.name === 'Mohawk')!.coords.slice().reverse();
    const stop = m.findIndex((c) => c[0] <= ROME[0] + 0.05);
    return mkLine(m.slice(0, stop + 1).map((c) => P(c as LonLat)));
  })(),
};


// Camera views of this part; the film starts on the harbor.
export const V: Record<string, View> = {
  harbor: {c: [-74.05, 40.62], k: 7},
  state: {c: [-76.3, 42.25], k: 2.6},
  coast: {c: [-78.6, 38.6], k: 1.2},
  east: {c: [-79, 38.4], k: 1.05},
  west: {c: [-83.2, 38.0], k: 1.25},
  flat: {c: [-84.8, 34.7], k: 1.28},
  ne: {c: [-76.6, 41.7], k: 2.1},
  road: {c: [-79.75, 39.9], k: 4.2},
  ny: {c: [-73.95, 41.65], k: 3.4},
  gap: {c: [-75.0, 42.65], k: 3.1},
  lakes: {c: [-76.9, 42.55], k: 2.35},
};
const MOVES: Move[] = [
  {at: S.keg.start + 0.3, dur: 5, v: V.state},
  {at: S.rivals.start, dur: 3.2, v: V.coast},
  {at: S.whole.start, dur: 3, v: V.east},
  {at: S.coast.start, dur: 2.5, v: V.coast},
  {at: S.settlers.start, dur: 3, v: V.west},
  {at: S.flatboat.start, dur: 3, v: V.flat},
  {at: S.flatboat.end - 1.6, dur: 1.6, v: V.ne},
  {at: S.road.start, dur: 2.4, v: V.road},
  {at: S.hudson.start, dur: 2.2, v: V.ny},
  {at: S.gap.start, dur: 3, v: V.gap},
  {at: line('gap', 1).from, dur: 3.5, v: V.lakes},
];

// Labels in screen space, each with its time window. Part 1 labels fade out as chapter 2 begins.
const END = S.idea.start + 1.2;
const LABELS: Lbl[] = [
  {text: 'Sandy Hook', at: SANDY, from: S.sandy.end - 0.6, to: S.dig.start, dx: 18, dy: 34, dot: true},
  {text: 'New York', at: NYC, from: S.sandy.end - 0.6, to: S.rivals.start + 1.5, dx: 18, dy: -10, dot: true},
  {text: 'Lake Erie', at: [-80.0, 42.25], from: S.keg.start + 6, to: S.rivals.start, size: 30, color: C.force, italic: true, rotate: -30, spacing: '0.28em', anchor: 'middle'},
  {text: 'Buffalo', at: BUFFALO, from: S.keg.start + 9, to: S.rivals.start, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'Albany', at: ALBANY, from: S.keg.start + 4, to: S.rivals.start, dx: 18, dy: 28, dot: true},
  {text: 'Atlantic Ocean', at: [-71.5, 39.75], from: S.keg.start + 3, to: S.rivals.start, size: 26, color: C.force, italic: true, spacing: '0.28em', anchor: 'middle'},
  {text: 'Rome · July 4, 1817', at: ROME, from: S.dig.voice, to: S.rivals.start, dx: 0, dy: -24, anchor: 'middle', dot: true},
  {text: "Clinton's Ditch", at: [-77.1, 42.72], from: lineWith('dig', 'history').from, to: S.rivals.start + 1, size: 36, color: C.accent, italic: true, anchor: 'middle', spacing: '0.2em', bold: true},
  // Ports of 1800 and after.
  {text: 'New York', at: NYC, from: S.rivals.start + 1.5, to: S.flatboat.start + 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Philadelphia', at: [-75.16, 39.95], from: S.rivals.start + 1.5, to: S.flatboat.start + 1, dx: -16, dy: 10, anchor: 'end', dot: true},
  {text: 'Baltimore', at: [-76.61, 39.29], from: S.rivals.start + 1.5, to: S.flatboat.start + 1, dx: -16, dy: 12, anchor: 'end', dot: true},
  {text: 'Boston', at: [-71.06, 42.36], from: S.rivals.start + 1.5, to: S.flatboat.start + 1, dx: 16, dy: 10, dot: true},
  {text: 'Appalachians', at: [-81.4, 36.5], from: S.mountains.voice + 0.6, to: S.flatboat.end, size: 34, color: '#9C8456', rotate: -38, spacing: '0.5em', anchor: 'middle', bold: true},
  {text: 'Ohio · 1803', at: [-82.7, 40.35], from: line('settlers', 1).from, to: line('flatboat', 2).from, size: 29, anchor: 'middle', italic: true},
  {text: 'Kentucky · 1792', at: [-85.2, 37.55], from: line('settlers', 1).from + 0.4, to: line('flatboat', 2).from, size: 29, anchor: 'middle', italic: true},
  {text: 'Tennessee · 1796', at: [-86.4, 35.85], from: line('settlers', 1).from + 0.8, to: line('flatboat', 2).from, size: 29, anchor: 'middle', italic: true},
  {text: 'Wheat · corn · hogs', at: [-84.6, 39.2], from: line('settlers', 2).from, to: S.flatboat.start + 2, size: 28, anchor: 'middle', color: C.ink},
  {text: 'Pittsburgh', at: PITTSBURGH, from: S.flatboat.voice + 2, to: S.flatboat.end - 1, dx: 16, dy: -12, dot: true},
  {text: 'New Orleans', at: NEW_ORLEANS, from: line('flatboat', 2).from + 4, to: S.flatboat.end - 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Buffalo', at: BUFFALO, from: S.flatboat.end - 1, to: S.road.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'New York', at: NYC, from: S.flatboat.end - 1, to: S.road.start + 1, dx: 18, dy: 10, dot: true},
  {text: 'Cumberland', at: CUMBERLAND, from: S.road.start + 2, to: S.horse.end, dx: 16, dy: 30, dot: true},
  {text: 'Wheeling', at: WHEELING, from: line('road', 1).from, to: S.horse.end, dx: -16, dy: -14, anchor: 'end', dot: true, bold: true},
  {text: 'Ohio River', at: [-80.95, 39.55], from: line('road', 1).from, to: S.horse.end, size: 28, color: C.force, italic: true, rotate: -60, anchor: 'middle'},
  {text: 'National Road · 1818', at: [-79.45, 40.32], from: line('road', 1).from + 0.5, to: S.horse.end, size: 28, anchor: 'middle', bold: true},
  {text: 'New York', at: NYC, from: S.hudson.start + 1, to: END, dx: 18, dy: 12, dot: true, bold: true},
  {text: 'Troy', at: TROY, from: line('hudson', 2).from + 2, to: S.gap.start + 6, dx: 16, dy: -8, dot: true},
  {text: 'Tide reaches Troy', at: [-73.42, 41.9], from: line('hudson', 2).from + 2.5, to: S.gap.voice + 0.3, size: 28, color: C.force, italic: true, rotate: -82, anchor: 'middle'},
  {text: 'Albany', at: ALBANY, from: S.gap.voice, to: END, dx: 16, dy: 30, dot: true},
  {text: 'Mohawk Valley', at: [-74.75, 43.3], from: S.gap.voice + 1.5, to: END, size: 28, color: C.force, italic: true, anchor: 'middle'},
  {text: 'Adirondacks', at: [-74.4, 43.85], from: S.gap.voice + 3, to: END, size: 30, color: '#9C8456', spacing: '0.4em', anchor: 'middle', bold: true},
  {text: 'Catskills', at: [-74.3, 41.72], from: S.gap.voice + 4, to: END, size: 30, color: '#9C8456', spacing: '0.4em', anchor: 'end', bold: true},
  {text: 'Allegheny Plateau', at: [-78.0, 41.55], from: S.lowgap.end - 0.3, to: END, size: 30, color: '#9C8456', spacing: '0.4em', anchor: 'middle', bold: true},
  {text: 'Lake Ontario', at: [-77.6, 43.62], from: line('gap', 1).from + 2, to: END, size: 28, color: C.force, italic: true, rotate: -4, spacing: '0.28em', anchor: 'middle'},
  {text: 'Lake Erie', at: [-80.0, 42.25], from: line('gap', 1).from + 2.5, to: END, size: 28, color: C.force, italic: true, rotate: -30, spacing: '0.28em', anchor: 'middle'},
  {text: 'Buffalo', at: BUFFALO, from: line('gap', 1).from + 3, to: END, dx: -18, dy: 10, anchor: 'end', dot: true},
];

// Miles from New York along the keg's water path: 150 up the Hudson to Albany, 363 by canal to Buffalo (Colden, 1825).
const NYC_AT = L.water.len[6] / L.water.total;
const ALBANY_AT = L.water.len[6 * hudson.length] / L.water.total;
const milesAt = (f: number) => (f <= NYC_AT ? 0 : f <= ALBANY_AT ? (150 * (f - NYC_AT)) / (ALBANY_AT - NYC_AT) : 150 + (363 * (f - ALBANY_AT)) / (1 - ALBANY_AT));

// State of every line in this part at time t.
function calc(t: number) {
  const wf = ramp(t, S.keg.start + 2.5, line('keg', 1).to);
  const dig = ramp(t, S.dig.voice + 0.5, line('dig', 0).to + 0.5);
  const ff = ramp(t, line('flatboat', 2).from, line('flatboat', 2).to + 2.5);
  const hf = ramp(t, line('hudson', 2).from + 0.4, line('hudson', 2).to + 0.6);
  const mf = ramp(t, S.gap.voice + 0.5, line('gap', 0).to);
  const wsf = ramp(t, line('gap', 1).from + 1, line('gap', 1).to + 0.3);
  return {
    wf, dig, ff, hf, mf, wsf,
    water: cut(L.water, wf),
    waterOn: 1 - ramp(t, S.dig.start, S.dig.start + 1),
    digE: cut(L.digEast, dig),
    digW: cut(L.digWest, dig),
    canalOn: 1 - ramp(t, S.coast.start, S.coast.start + 1.5),
    pa: cut(L.settlersPa, ramp(t, line('settlers', 1).from - 0.3, line('settlers', 1).to)),
    va: cut(L.settlersVa, ramp(t, line('settlers', 1).from + 0.3, line('settlers', 1).to + 0.6)),
    settleOn: 1 - ramp(t, line('flatboat', 2).from, line('flatboat', 2).from + 1),
    flat: cut(L.flatboat, ff),
    flatOn: 1 - ramp(t, S.flatboat.end - 1, S.flatboat.end),
    road: cut(L.road, ramp(t, S.road.start + 1.5, line('road', 1).to)),
    roadOn: 1 - ramp(t, S.horse.end, S.horse.end + 1),
    wagon: cut(L.road, 0.04 + 0.4 * ramp(t, line('road', 2).from, S.road.end + 0.7)),
    hud: cut(L.hudsonUp, hf),
    tideOn: win(t, line('hudson', 2).from + 1.2, S.gap.start + 3, 0.6),
    moh: cut(L.mohawk, mf),
    west: cut(L.west, wsf),
    // The low route fades into chapter 2, where the real canal line takes over.
    lowOn: 1 - ramp(t, S.idea.start, S.idea.start + 1.5),
    glow: 1 + 0.6 * win(t, lineWith('finish', 'Nature').from, lineWith('finish', 'Nature').to + 0.5, 0.4),
    pulse: win(t, lineWith('finish', 'Someone').from, END, 0.4) * (0.55 + 0.45 * Math.sin(t * Math.PI * 2)),
  };
}
const drawing = (f: number) => f > 0 && f < 1;

// Mountains: the relief bands rise one after another, low to high.
const ground = ({t, fine}: Ctx) => {
  const rise = (i: number) => ramp(t, S.mountains.voice + 0.2 + 0.6 * i, S.mountains.voice + 1.3 + 0.6 * i) * (1 - ramp(t, S.flatboat.end - 1, S.flatboat.end));
  return G.relief.map((d, i) => (rise(i) > 0 ? <path key={`r${i}`} d={d} fill="#CDB68C" fillOpacity={0.4 * rise(i) * (1 - fine)} transform={`translate(0,${(1 - rise(i)) * 14})`} /> : null));
};

const under = ({t}: Ctx) => {
  const s = calc(t);
  return (
    <>
      <path d={s.water.d} fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" opacity={s.waterOn} vectorEffect="non-scaling-stroke" />
      <g opacity={s.canalOn}>
        <path d={s.digE.d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
        <path d={s.digW.d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      </g>
      <g opacity={s.settleOn}>
        <path d={s.pa.d} fill="none" stroke={C.ink} strokeWidth={3.5} strokeDasharray="12 9" strokeDashoffset={-t * 30} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d={s.va.d} fill="none" stroke={C.ink} strokeWidth={3.5} strokeDasharray="12 9" strokeDashoffset={-t * 30} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </g>
      <path d={s.flat.d} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray="14 10" strokeDashoffset={-t * 36} strokeLinecap="round" opacity={s.flatOn} vectorEffect="non-scaling-stroke" />
      <path d={s.road.d} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray="12 9" strokeDashoffset={-t * 14} strokeLinecap="round" opacity={s.roadOn} vectorEffect="non-scaling-stroke" />
      <g opacity={s.lowOn}>
        <path d={s.hud.d} fill="none" stroke={C.force} strokeWidth={8 * s.glow} strokeLinecap="round" strokeOpacity={0.85} vectorEffect="non-scaling-stroke" />
        {s.tideOn > 0
          ? [0, 1, 2].map((i) => {
              const f = ((t * 0.2) + i / 3) % 1;
              return <path key={i} d={segment(L.hudsonUp, f - 0.08, f)} fill="none" stroke="#EAF2F5" strokeWidth={5} strokeLinecap="round" opacity={s.tideOn * 0.9 * Math.min(1, (1 - f) * 8)} vectorEffect="non-scaling-stroke" />;
            })
          : null}
        <path d={s.moh.d} fill="none" stroke={C.force} strokeWidth={8 * s.glow} strokeLinecap="round" strokeOpacity={0.85} vectorEffect="non-scaling-stroke" />
        <path d={s.west.d} fill="none" stroke={C.accent} strokeWidth={6} strokeDasharray="14 10" strokeDashoffset={-t * 30} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d={s.west.d} fill="none" stroke={C.accent} strokeWidth={16} strokeLinecap="round" strokeOpacity={0.25 * s.pulse} vectorEffect="non-scaling-stroke" />
      </g>
    </>
  );
};

const over = ({t, cam, at}: Ctx) => {
  const s = calc(t);
  const yearOn = win(t, S.dig.voice + 0.3, S.rivals.start + 0.5, 0.4);
  const yearPos = scr([-76.1, 42.02], cam);
  const nyPulse = win(t, S.rivals.voice, S.rivals.end + 0.6, 0.4);
  return (
    <>
      {/* heads of lines being drawn */}
      {drawing(s.wf) && s.waterOn > 0 ? Head(at(s.water.head), C.accent) : null}
      {drawing(s.dig) ? [Head(at(s.digE.head), C.accent), Head(at(s.digW.head), C.accent)] : null}
      {drawing(s.hf) ? Head(at(s.hud.head), C.force) : null}
      {drawing(s.mf) ? Head(at(s.moh.head), C.force) : null}
      {s.wsf > 0 && s.lowOn > 0 ? Arrow(at(s.west.head), s.west.dir, C.accent, s.lowOn) : null}
      {s.pa.d && s.settleOn > 0 ? Arrow(at(s.pa.head), s.pa.dir, C.ink, s.settleOn) : null}
      {s.va.d && s.settleOn > 0 ? Arrow(at(s.va.head), s.va.dir, C.ink, s.settleOn) : null}
      {/* mile counter on the keg's water path */}
      {s.wf > NYC_AT && s.waterOn > 0 ? (() => {
        const [x, y] = at(s.water.head);
        return (
          <text x={x - 22} y={y - 26} textAnchor="end" style={{...label, fontSize: 34, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={8} strokeLinejoin="round" fill={C.accent} opacity={s.waterOn * (1 - ramp(t, S.wedding.start - 0.4, S.wedding.start))}>
            {s.wf >= 1 ? '513 miles by water' : `${Math.round(milesAt(s.wf))} miles`}
          </text>
        );
      })() : null}
      {/* years while the canal is dug, then its length */}
      {yearOn > 0 ? (
        <g opacity={yearOn}>
          <text x={yearPos[0]} y={yearPos[1]} textAnchor="middle" style={{fontFamily: F.title, fontSize: 92, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={10} strokeLinejoin="round" fill={C.accent}>
            {Math.round(yearAt(t))}
          </text>
          <text x={yearPos[0]} y={yearPos[1] + 50} textAnchor="middle" style={{...label, fontSize: 30, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.ink} opacity={ramp(t, line('dig', 0).to + 0.4, line('dig', 0).to + 0.9)}>
            363 miles · Albany to Buffalo
          </text>
        </g>
      ) : null}
      {Ripples(scr(NYC, cam), t, nyPulse, C.accent)}
      {/* flatboats: one leads while the route is drawn, then boats keep flowing down to New Orleans */}
      {s.flatOn > 0 && drawing(s.ff) ? Flatboat(at(s.flat.head), s.flat.dir) : null}
      {s.flatOn > 0 && s.ff >= 1
        ? [0, 1, 2, 3].map((i) => {
            const f = ((t - line('flatboat', 2).from) * 0.06 + i / 4) % 1;
            const b = cut(L.flatboat, f);
            return <g key={i}>{Flatboat(at(b.head), b.dir, s.flatOn * Math.min(1, f * 10, (1 - f) * 10))}</g>;
          })
        : null}
      {s.roadOn > 0 && t >= line('road', 2).from ? <g opacity={s.roadOn * ramp(t, line('road', 2).from, line('road', 2).from + 0.4)}>{Wagon(at(s.wagon.head))}</g> : null}
    </>
  );
};

// Time ruler keyframes of this part.
const YEARS: YearKey[] = [
  {at: S.dig.start, dur: 1, y: 1817},
  {at: S.dig.voice + 0.5, dur: line('dig', 0).to - S.dig.voice, y: 1825},
  {at: S.rivals.voice, dur: S.rivals.end - S.rivals.voice, y: 1860},
  {at: S.coast.start, dur: 2, y: 1800},
  {at: line('settlers', 1).from, dur: 3, y: 1803},
  {at: S.cost.start, dur: 1, y: 1817},
  {at: S.road.start + 1, dur: 1.5, y: 1818},
];
const yearAt = makeYearAt(YEARS);

const NOTES: Note[] = [
  {from: S.sandy.end - 0.5, to: S.coast.start, text: 'Canal route simplified, pace of digging schematic · modern coastline and rivers · Natural Earth, NOAA ETOPO 2022'},
  {from: S.coast.start, to: line('settlers', 1).from, text: 'Modern coastline and rivers · relief bands at 150, 300, 500 and 800 m · Natural Earth, NOAA ETOPO 2022'},
  {from: line('settlers', 1).from, to: S.flatboat.voice, text: 'Dashed arrows: settler routes, schematic · Natural Earth, NOAA ETOPO 2022'},
  {from: S.flatboat.voice, to: S.flatboat.end, text: 'Dashed: usual route of western farm goods, schematic · Natural Earth'},
  {from: S.road.start, to: S.horse.start, text: 'Dashed: National Road, approximate line · Natural Earth'},
  {from: S.hudson.start, to: END, text: 'Relief: tan above 150 m · dashed: the low route west, not yet a canal · Natural Earth, NOAA ETOPO 2022'},
];

// Inserts: paper page with a picture or a diagram, caption, source and licence, mini-map.
const CostPage: React.FC<{t: number}> = ({t}) => {
  const from = lineWith('cost', 'Around 1817').from;
  const a = ramp(t, from + 1.2, from + 1.5);
  const count = Math.round(100 * interpolate(t, [from + 1.2, from + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
  const b = ramp(t, lineWith('cost', 'weeks').from, lineWith('cost', 'weeks').from + 0.8);
  // The wagon crawls across the page the whole time the insert is open.
  const go = -560 * (1 - interpolate(t, [S.cost.start + 0.6, S.cost.end], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const road = ramp(t, S.cost.start + 0.4, S.cost.start + 1);
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
        <rect width={1120} height={620} fill="#E6DECD" />
        <text x={70} y={90} style={{...label, fontSize: 30}} fill={C.ink}>Buffalo → New York City · wagon, then river · 1817</text>
        <text x={60} y={330} style={{fontFamily: F.title, fontSize: 250, fontVariationSettings: '"opsz" 144', fontWeight: 600}} fill={C.accent} opacity={a}>≈ ${count}</text>
        <text x={74} y={400} style={{...label, fontSize: 40, fontWeight: 700}} fill={C.ink} opacity={a}>for one ton of goods</text>
        <text x={74} y={450} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink} opacity={a * 0.8}>19.12 cents a ton-mile × 513 miles ≈ $98</text>
        <text x={74} y={515} style={{...label, fontSize: 36, fontWeight: 700}} fill={C.ink} opacity={b}>and weeks on the way</text>
        <g opacity={road}>
          <line x1={70} x2={1050} y1={604} y2={604} stroke={C.ink} strokeWidth={3} strokeDasharray="16 12" />
          <g transform={`translate(${go},14)`}>
            <Horse x={840} y={504} s={0.9} />
            <rect x={680} y={528} width={120} height={46} fill={C.ink} />
            <circle cx={710} cy={584} r={16} fill={C.paper} stroke={C.ink} strokeWidth={5} />
            <circle cx={776} cy={584} r={16} fill={C.paper} stroke={C.ink} strokeWidth={5} />
          </g>
        </g>
      </svg>
      <SideText left={1270} top={300} width={590}
        s={{kicker: 'Freight before the canal', head: 'Slow and expensive', tag: 'reconstructed: 1817 rate × distance', credit: 'Rate: Klein and Matthews, European Review of Economic History, 2026. Distance: Colden, Memoir, 1825.', plaque: 'Own drawing'}} />
    </AbsoluteFill>
  );
};

const MemorialPage: React.FC<{t: number}> = ({t}) => {
  const a = ramp(t, lineWith('horse', 'thirty-two').from, lineWith('horse', 'thirty-two').from + 1.6);
  const b = ramp(t, lineWith('horse', 'promised').from + 0.6, lineWith('horse', 'promised').from + 1.4);
  const unit = 26;
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
        <rect width={1120} height={620} fill="#E6DECD" />
        <text x={60} y={90} style={{...label, fontSize: 30}} fill={C.ink}>One ton, one hundred miles</text>
        <g opacity={ramp(t, S.horse.start + 0.8, S.horse.start + 1.4)}>
          <text x={60} y={190} style={{...label, fontSize: 34, fontWeight: 700}} fill={C.ink}>Over land</text>
          <Horse x={930} y={150} s={0.8} />
          <rect x={60} y={230} width={32 * unit * a} height={70} fill={C.ink} />
          <text x={60 + 32 * unit * a + 14} y={282} style={{fontFamily: F.title, fontSize: 56, fontWeight: 600}} fill={C.ink} opacity={a}>$32</text>
        </g>
        <g opacity={ramp(t, S.horse.start + 0.8, S.horse.start + 1.4)}>
          <text x={60} y={420} style={{...label, fontSize: 34, fontWeight: 700}} fill={C.ink}>By canal, as promised</text>
          <Boat x={930} y={378} />
          <rect x={60} y={460} width={unit * b} height={70} fill={C.accent} />
          <text x={60 + unit + 14} y={512} style={{fontFamily: F.title, fontSize: 56, fontWeight: 600}} fill={C.accent} opacity={b}>$1</text>
        </g>
      </svg>
      <SideText left={1270} top={300} width={590}
        s={{kicker: "Clinton's canal memorial, 1816", head: 'Thirty-two to one', tag: 'an 1816 promise, not a measured price', credit: 'Memorial of the citizens of New York in favour of a canal navigation, 1816. Printed in Hosack, Memoir of De Witt Clinton, 1829.', plaque: 'Own drawing'}} />
    </AbsoluteFill>
  );
};

// Ground height along two ways west from the coast (scripts/profiles.ts): the Hudson and the canal line
// against a line over the Pennsylvania mountains. Same data and the same valley-floor rule for both.
const ProfilePage: React.FC<{t: number}> = ({t}) => {
  const [x0, x1, yb, yt] = [130, 1070, 520, 130];
  const X = (m: number) => x0 + (m / 500) * (x1 - x0);
  const Y = (f: number) => yb - (f / 2400) * (yb - yt);
  const u = 500 * ramp(t, S.lowgap.start + 0.7, S.lowgap.start + 4.2);
  const pts = (p: {miles: number[]; ft: number[]}) => p.miles.map((m, i) => [X(m), Y(p.ft[i])] as XY).filter(([x]) => x <= X(u));
  const poly = (q: XY[]) => q.map((p) => p.join(',')).join(' ');
  const area = (q: XY[]) => (q.length > 1 ? `M${q[0][0]},${yb} L${q.map((p) => p.join(',')).join(' L')} L${q[q.length - 1][0]},${yb} Z` : '');
  const a = pts(profiles.a);
  const b = pts(profiles.b);
  const key = (n: number) => ramp(t, S.lowgap.start + 1 + n * 1.4, S.lowgap.start + 1.6 + n * 1.4);
  const small = {fontFamily: F.label, fontSize: 24};
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
        <rect width={1120} height={620} fill="#E6DECD" />
        <text x={60} y={66} style={{...label, fontSize: 28}} fill={C.ink}>Height of the ground going west from the coast</text>
        {[0, 500, 1000, 1500, 2000].map((f) => (
          <g key={f}>
            <line x1={x0} x2={x1} y1={Y(f)} y2={Y(f)} stroke={C.rule} strokeWidth={1.5} />
            <text x={x0 - 14} y={Y(f) + 8} textAnchor="end" style={small} fill={C.ink}>{f.toLocaleString('en-US')}</text>
          </g>
        ))}
        <text x={x0 - 14} y={Y(2400) + 8} textAnchor="end" style={{...label, fontSize: 20}} fill={C.ink}>feet</text>
        {[0, 100, 200, 300, 400, 500].map((m) => <text key={m} x={X(m)} y={yb + 34} textAnchor="middle" style={small} fill={C.ink}>{m}</text>)}
        <text x={x1} y={yb + 72} textAnchor="end" style={{...label, fontSize: 20}} fill={C.ink}>miles from the coast</text>
        <path d={area(b)} fill={C.relief} />
        <path d={area(a)} fill={C.force} opacity={0.16} />
        <polyline points={poly(b)} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray="14 9" strokeLinejoin="round" />
        <polyline points={poly(a)} fill="none" stroke={C.accent} strokeWidth={5} strokeLinejoin="round" />
        {b.length && u >= profiles.b.length ? <text x={b[b.length - 1][0] + 12} y={b[b.length - 1][1] - 12} style={{...label, fontSize: 22}} fill={C.ink}>Pittsburgh</text> : null}
        {a.length && u >= profiles.a.length ? <text x={a[a.length - 1][0]} y={a[a.length - 1][1] - 22} textAnchor="end" style={{...label, fontSize: 22}} fill={C.ink}>Buffalo · Lake Erie</text> : null}
        <g opacity={key(0)}>
          <line x1={560} x2={630} y1={128} y2={128} stroke={C.accent} strokeWidth={5} />
          <text x={646} y={137} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink}>Hudson and Mohawk: <tspan fontWeight={700} fill={C.accent}>under 600 ft</tspan></text>
        </g>
        <g opacity={key(1)}>
          <line x1={560} x2={630} y1={182} y2={182} stroke={C.ink} strokeWidth={4} strokeDasharray="14 9" />
          <text x={646} y={191} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink}>Pennsylvania: <tspan fontWeight={700}>over 2,000 ft</tspan></text>
        </g>
      </svg>
      <SideText left={1270} top={300} width={590}
        s={{kicker: 'Two ways west · terrain model', head: 'The only low gap', tag: 'lowest ground within about 2 miles of each line', credit: 'Heights: NOAA ETOPO 2022. Canal line: J. Atack, 2015. Line through Pennsylvania drawn by us: Harrisburg, Hollidaysburg, Johnstown.', plaque: 'Own drawing'}} />
    </AbsoluteFill>
  );
};


const INSERTS: Ins[] = [
  {from: 0, to: S.sandy.end, at: SANDY, instant: true, render: (_t, d) => (
    <PicPage src="assets/met-12722-sandy-hook.jpg" w={2255} h={1351} origin="40% 55%" drift={d} at={SANDY}
      s={{kicker: 'Sandy Hook, New York Harbor', head: 'Where the waters met', body: 'The entrance to New York Harbor, where the 1825 fleet gathered.', tag: 'view about 1812, not the ceremony', credit: 'Full Sail off Sandy Hook — Entrance to New York Harbor. Pavel Svinin, 1811 – about 1813. Watercolor.', plaque: 'The Met · Public domain'}} />
  )},
  {from: S.wedding.start, to: S.wedding.end, at: SANDY, render: (_t, d) => (
    <AbsoluteFill style={{background: C.paper}}>
      <Picture src="assets/met-339841-fleet-1825.jpg" w={4000} h={1074} origin="50% 60%" drift={d} wide />
      <div style={{position: 'absolute', left: 100, top: 640, width: 900, color: C.ink}}>
        <div style={{...label, fontSize: 27, opacity: 0.72}}>New York Harbor · November 4, 1825</div>
        <div style={{...title, fontSize: 64, marginTop: 14}}>The Wedding of the Waters</div>
        <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16}}>drawn for the celebration</div>
      </div>
      <div style={{position: 'absolute', left: 1080, top: 650, width: 740, color: C.ink}}>
        <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>Grand Canal Celebration: View of the Fleet Preparing to Form in Line. Lithograph, Anthony Imbert, 1825, for Colden's Memoir of the celebration.</div>
        <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>The Met · Public domain</div>
      </div>
    </AbsoluteFill>
  )},
  {from: S.cost.start, to: S.cost.end, at: BUFFALO, render: (t) => <CostPage t={t} />},
  {from: S.horse.start, to: S.horse.end, at: WHEELING, render: (t) => <MemorialPage t={t} />},
  {from: S.lowgap.start, to: S.lowgap.end, at: ALBANY, render: (t) => <ProfilePage t={t} />},
  {from: line('hudson', 0).to - 0.2, to: line('hudson', 2).from + 0.6, at: NYC, render: (_t, d) => (
    <PicPage src="assets/met-13116-ny-from-weehawk.jpg" w={2109} h={1312} origin="60% 50%" drift={d} at={NYC}
      s={{kicker: 'New York, about 1820–1823', head: 'A city at the mouth of a river', body: 'The harbor, and the Hudson running north.', tag: 'view before the canal', credit: 'New York from Weehawk. William Guy Wall, about 1820–23. Watercolor.', plaque: 'The Met · Public domain'}} />
  )},
];

const KeyCard: React.FC<{t: number}> = ({t}) => {
  const o = win(t, S.key.start, S.key.end, 0.6);
  if (o <= 0) return null;
  const row = (n: number) => ramp(t, line('key', n).from, line('key', n).from + 0.7);
  return (
    <div style={{position: 'absolute', left: 110, top: 250, width: 640, padding: '30px 36px', background: C.paper, outline: `1.5px solid ${C.ink}`, opacity: o}}>
      <div style={{...label, fontSize: 28, color: C.ink, opacity: 0.72}}>Key</div>
      <svg width={570} height={300} style={{marginTop: 12}}>
        <defs>
          <pattern id="hatch" width={12} height={12} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1={0} y1={0} x2={0} y2={12} stroke={C.ink} strokeWidth={3} />
          </pattern>
        </defs>
        <g opacity={row(1)}>
          <line x1={0} x2={130 * row(1)} y1={30} y2={30} stroke={C.accent} strokeWidth={7} strokeLinecap="round" />
          <text x={160} y={42} style={{...label, fontSize: 34}} fill={C.ink}>documented</text>
        </g>
        <g opacity={row(2)}>
          <line x1={0} x2={130 * row(2)} y1={105} y2={105} stroke={C.accent} strokeWidth={7} strokeDasharray="16 11" strokeLinecap="round" />
          <text x={160} y={117} style={{...label, fontSize: 34}} fill={C.ink}>reconstruction</text>
        </g>
        <g opacity={row(3)}>
          <rect x={0} y={155} width={130 * row(3)} height={50} fill="url(#hatch)" stroke={C.ink} strokeWidth={2} />
          <text x={160} y={192} style={{...label, fontSize: 34}} fill={C.ink}>disputed</text>
        </g>
        <g opacity={row(4)}>
          <line x1={0} x2={130} y1={262} y2={262} stroke={C.ink} strokeWidth={2} />
          <circle cx={20 + 90 * ramp(t, line('key', 4).from, S.key.end)} cy={262} r={9} fill={C.accent} />
          <text x={160} y={274} style={{...label, fontSize: 34}} fill={C.ink}>time</text>
        </g>
      </svg>
    </div>
  );
};

const Titles: React.FC<{t: number}> = ({t}) => {
  const ep = win(t, S.whole.voice + 3.6, S.key.start + 0.4, 0.6);
  const ch = win(t, S.coast.start, S.coast.start + 5.5, 0.6);
  const tag = win(t, S.coast.start + 5.5, END, 0.6);
  return (
    <>
      <div style={{position: 'absolute', left: 1180, top: 560, opacity: ep}}>
        <div style={{...title, fontSize: 104}}>Clinton's Ditch</div>
        <div style={{...label, fontSize: 36, color: C.ink, marginTop: 18}}>How a canal made New York</div>
      </div>
      <div style={{position: 'absolute', left: 110, top: 92, opacity: ch}}>
        <div style={{...label, fontSize: 30, color: C.accent, fontWeight: 700}}>Chapter 1</div>
        <div style={{...title, fontSize: 84, marginTop: 8}}>The Wall</div>
      </div>
      <div style={{position: 'absolute', left: 110, top: 60, opacity: tag, ...label, fontSize: 24, color: C.ink}}>1 · The Wall</div>
    </>
  );
};

export const PART1: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  inserts: INSERTS,
  relief: (t) => 0.25 * win(t, S.lowgap.start, END, 1.2),
  flash: (t) => win(t, line('key', 4).from, S.key.end, 0.3),
  ground,
  under,
  over,
  top: (t) => (
    <>
      <Titles t={t} />
      <KeyCard t={t} />
    </>
  ),
};

export const Pilot = makeFilm([PART1], V.harbor, 'Pilot draft · silent, timed for a voiceover');
export const PILOT_FRAMES = Math.ceil(S.finish.end * FPS);
````

## probe/src/Probe.tsx

````tsx
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {geoConicConformal, geoGraticule10, geoPath} from 'd3-geo';
import region from '../public/region/erie.json';
import {C, F, H, W, fontFiles} from './theme';
import {LOCKPORT, LonLat, canal, hudson, towns, waters} from './erie';

type XY = [number, number];

// Base projection: the whole region fills the frame at zoom 1.
const [bw, bs, be, bn] = region.bbox;
const proj = geoConicConformal().parallels([40.5, 44]).rotate([76, 0]).fitExtent(
  [[0, 0], [W, H]],
  {type: 'MultiPoint', coordinates: [[bw, bs], [be, bs], [be, bn], [bw, bn]]},
);
const path = geoPath(proj);
const P = (p: LonLat) => proj(p) as XY;

const geo = {
  land: path(region.land as any) ?? '',
  lakes: path(region.lakes as any) ?? '',
  rivers: region.rivers.map((r) => path({type: 'LineString', coordinates: r.coords} as any) ?? '').join(''),
  relief: region.relief.map((r) => path(r.geometry as any) ?? ''),
  grid: path(geoGraticule10()) ?? '',
};

// Smooth polyline through projected points (Catmull-Rom), with cumulative length.
function smooth(points: LonLat[], steps = 10) {
  const p = points.map(P);
  const out: XY[] = [];
  for (let i = 0; i < p.length - 1; i++) {
    const [a, b, c, d] = [p[Math.max(i - 1, 0)], p[i], p[i + 1], p[Math.min(i + 2, p.length - 1)]];
    for (let s = 0; s < steps; s++) {
      const t = s / steps;
      const t2 = t * t;
      const t3 = t2 * t;
      const f = (k: 0 | 1) => 0.5 * (2 * b[k] + (-a[k] + c[k]) * t + (2 * a[k] - 5 * b[k] + 4 * c[k] - d[k]) * t2 + (-a[k] + 3 * b[k] - 3 * c[k] + d[k]) * t3);
      out.push([f(0), f(1)]);
    }
  }
  out.push(p[p.length - 1]);
  const len = [0];
  for (let i = 1; i < out.length; i++) len.push(len[i - 1] + Math.hypot(out[i][0] - out[i - 1][0], out[i][1] - out[i - 1][1]));
  return {pts: out, len, total: len[len.length - 1]};
}

function cut(line: ReturnType<typeof smooth>, frac: number) {
  const target = Math.max(0, Math.min(1, frac)) * line.total;
  const pts: XY[] = [line.pts[0]];
  let i = 1;
  while (i < line.pts.length && line.len[i] <= target) pts.push(line.pts[i++]);
  let head = pts[pts.length - 1];
  let dir: XY = [1, 0];
  if (i < line.pts.length) {
    const [a, b] = [line.pts[i - 1], line.pts[i]];
    const t = (target - line.len[i - 1]) / (line.len[i] - line.len[i - 1] || 1);
    head = [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
    pts.push(head);
    dir = [b[0] - a[0], b[1] - a[1]];
  }
  return {d: pts.length > 1 ? 'M' + pts.map((q) => q.join(',')).join('L') : '', head, dir};
}

const canalLine = smooth(canal);
const hudsonLine = smooth(hudson, 6);
const fracAt = (lonlat: LonLat) => {
  const q = P(lonlat);
  let best = 0;
  canalLine.pts.forEach((p, i) => {
    if (Math.hypot(p[0] - q[0], p[1] - q[1]) < Math.hypot(canalLine.pts[best][0] - q[0], canalLine.pts[best][1] - q[1])) best = i;
  });
  return canalLine.len[best] / canalLine.total;
};
const LOCK_FRAC = fracAt(LOCKPORT);

// Timeline of the probe, in frames at 30 fps.
const T = {
  titleIn: [10, 30],
  ruler: [20, 80],
  draw1: [90, 300],
  lensRing: [300, 318],
  lensOpen: [318, 350],
  gates: [410, 450],
  lensClose: [560, 592],
  draw2: [600, 650],
  draw3: [640, 700],
  endTitle: [690, 710],
  end: 780,
};
const ease = Easing.inOut(Easing.cubic);
const ramp = (f: number, [a, b]: number[], from = 0, to = 1) =>
  interpolate(f, [a, b], [from, to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

// Camera: centre in base-projection pixels and zoom.
function camera(f: number) {
  const wide = P([-76.0, 42.25]);
  const boatFrac = f < T.draw2[0] ? ramp(f, T.draw1, 0, LOCK_FRAC) : ramp(f, T.draw2, LOCK_FRAC, 1);
  const boat = cut(canalLine, boatFrac).head;
  const follow = ramp(f, [60, 130]) * (1 - ramp(f, [600, 700]));
  let k = Math.exp(Math.log(1) + (Math.log(2.1) - Math.log(1)) * ramp(f, [60, 130]));
  k *= 1 + 0.35 * ramp(f, [260, 310]); // settle on Lockport
  k *= 1 + 0.25 * ramp(f, T.lensOpen) - 0.25 * ramp(f, T.lensClose); // dive with the lens
  k = interpolate(ramp(f, [600, 700]), [0, 1], [k, 1]);
  const cx = wide[0] + (boat[0] - wide[0]) * follow;
  const cy = wide[1] + (boat[1] - wide[1]) * follow;
  return {cx, cy, k, boatFrac};
}
const toScreen = (p: XY, cam: ReturnType<typeof camera>): XY => [
  (p[0] - cam.cx) * cam.k + W / 2,
  (p[1] - cam.cy) * cam.k + H / 2,
];

const label: React.CSSProperties = {fontFamily: F.label, letterSpacing: '0.16em', textTransform: 'uppercase'};

const MapLayer: React.FC<{f: number; cam: ReturnType<typeof camera>}> = ({f, cam}) => {
  const first = cut(canalLine, cam.boatFrac);
  const river = cut(hudsonLine, ramp(f, T.draw3));
  const transform = `translate(${W / 2 - cam.cx * cam.k},${H / 2 - cam.cy * cam.k}) scale(${cam.k})`;
  const boat = toScreen(first.head, cam);
  const angle = (Math.atan2(first.dir[1], first.dir[0]) * 180) / Math.PI;
  const flip = Math.abs(angle) > 90;
  const lensHide = ramp(f, [T.lensRing[0] - 8, T.lensRing[0] + 4]) - ramp(f, [T.lensClose[1], T.lensClose[1] + 10]);
  const boatOn = f >= T.draw1[0] && f < T.draw2[1] + 10 ? (1 - ramp(f, [T.draw2[1], T.draw2[1] + 10])) * (1 - lensHide) : 0;
  return (
    <svg width={W} height={H} style={{position: 'absolute'}}>
      <rect width={W} height={H} fill={C.water} />
      <g transform={transform}>
        <path d={geo.grid} fill="none" stroke={C.ink} strokeOpacity={0.06} strokeWidth={1} vectorEffect="non-scaling-stroke" />
        <path d={geo.land} fill={C.land} />
        {geo.relief.map((d, i) => (
          <path key={i} d={d} fill={C.relief} fillOpacity={0.34} />
        ))}
        <path d={geo.lakes} fill={C.water} stroke="#AEC0C3" strokeWidth={1} vectorEffect="non-scaling-stroke" />
        <path d={geo.rivers} fill="none" stroke={C.river} strokeWidth={1.8} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
        <path d={river.d} fill="none" stroke={C.accent} strokeWidth={3} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d={first.d} fill="none" stroke={C.accent} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      </g>
      {waters.map((w) => {
        const [x, y] = toScreen(P(w.at), cam);
        const vis = w.minZoom ? interpolate(cam.k, [w.minZoom - 0.2, w.minZoom], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
        return (
          <text key={w.name} x={x} y={y} opacity={vis} transform={`rotate(${w.rotate ?? 0},${x},${y})`} textAnchor="middle"
            style={{...label, fontSize: w.size, letterSpacing: '0.28em', fontStyle: 'italic'}} fill={C.force} fillOpacity={0.85}>
            {w.name}
          </text>
        );
      })}
      {towns.map((t) => {
        const at = fracAt(t.at);
        const tf = t.name === 'NEW YORK' ? ramp(f, [T.draw3[1] - 10, T.draw3[1] + 5])
          : t.name === 'ALBANY' ? ramp(f, [T.draw1[0] - 10, T.draw1[0] + 5])
          : interpolate(cam.boatFrac, [at - 0.015, at], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const [x, y] = toScreen(P(t.at), cam);
        return (
          <g key={t.name} opacity={tf}>
            <circle cx={x} cy={y} r={7} fill={C.accent} stroke={C.land} strokeWidth={2.5} />
            <text x={x + (t.dx ?? 0)} y={y + (t.dy ?? 0)} textAnchor={t.anchor ?? 'start'}
              style={{...label, fontSize: 30, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.ink}>
              {t.name}
            </text>
          </g>
        );
      })}
      <g opacity={boatOn} transform={`translate(${boat[0]},${boat[1]}) rotate(${flip ? angle + 180 : angle}) scale(${flip ? -1 : 1},1)`}>
        <path d="M-26,-2 L24,-2 L18,9 L-20,9 Z" fill={C.ink} />
        <rect x={-12} y={-12} width={20} height={10} rx={1.5} fill={C.ink} />
      </g>
    </svg>
  );
};

// Bottom band: time ruler and data note.
const Ruler: React.FC<{f: number}> = ({f}) => {
  const years = [1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825];
  const [x0, x1, y] = [140, 1780, 1022];
  const xs = (yr: number) => x0 + ((yr - 1817) / 8) * (x1 - x0);
  const run = xs(1817 + 8 * ramp(f, T.ruler));
  const show = ramp(f, [0, 20]);
  return (
    <g opacity={show}>
      <rect x={0} y={H - 116} width={W} height={116} fill={C.paper} />
      <line x1={0} x2={W} y1={H - 116} y2={H - 116} stroke={C.rule} strokeWidth={1} />
      <line x1={x0} x2={x1} y1={y - 26} y2={y - 26} stroke={C.ink} strokeWidth={2} />
      {years.map((yr) => (
        <g key={yr}>
          <line x1={xs(yr)} x2={xs(yr)} y1={y - 34} y2={y - 18} stroke={C.ink} strokeWidth={2} />
          <text x={xs(yr)} y={y + 14} textAnchor="middle" style={{...label, fontSize: 24}} fill={yr === 1825 && f > T.ruler[1] ? C.accent : C.ink}>
            {yr}
          </text>
        </g>
      ))}
      <circle cx={run} cy={y - 26} r={9} fill={C.accent} />
      <text x={xs(1817)} y={y - 46} textAnchor="start" style={{...label, fontSize: 22}} fill={C.ink} opacity={ramp(f, [20, 35]) * (1 - ramp(f, [70, 85]))}>
        Digging starts
      </text>
      <text x={xs(1825)} y={y - 46} textAnchor="end" style={{...label, fontSize: 22}} fill={C.accent} opacity={ramp(f, [75, 90])}>
        Canal opens
      </text>
      <text x={110} y={H - 140} textAnchor="start" style={{fontFamily: F.label, fontSize: 22}} fill={C.ink} fillOpacity={0.66}>
        Route between towns simplified · modern coastline and rivers · Natural Earth, NOAA ETOPO 2022
      </text>
    </g>
  );
};

const Titles: React.FC<{f: number}> = ({f}) => {
  const a = ramp(f, T.titleIn) * (1 - ramp(f, [250, 280]));
  const b = ramp(f, T.endTitle);
  return (
    <>
      <div style={{position: 'absolute', left: 110, top: 92, opacity: a, transform: `translateY(${(1 - a) * 12}px)`}}>
        <div style={{fontFamily: F.title, fontSize: 76, color: C.ink, fontVariationSettings: '"opsz" 72, "SOFT" 50', lineHeight: 1.05}}>The Erie Canal</div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>Albany to Buffalo · opened 1825</div>
      </div>
      <div style={{position: 'absolute', left: 110, top: 92, opacity: b, transform: `translateY(${(1 - b) * 12}px)`}}>
        <div style={{fontFamily: F.title, fontSize: 76, color: C.ink, fontVariationSettings: '"opsz" 72, "SOFT" 50', lineHeight: 1.05}}>
          Lake Erie to the Atlantic
        </div>
        <div style={{...label, fontSize: 32, color: C.ink, marginTop: 14}}>Canal to Albany, then down the Hudson</div>
      </div>
    </>
  );
};

// Full-frame insert on paper: engraving, caption, source and licence, mini-map.
const IMG = {w: 1120, h: (1120 * 5008) / 7423, x: 100, y: 0};
IMG.y = (H - IMG.h) / 2 - 10;
const gatesPts: XY[] = [[0.352, 0.705], [0.528, 0.775], [0.68, 0.705]];

const Insert: React.FC<{f: number}> = ({f}) => {
  const drift = 1 + 0.035 * ramp(f, [T.lensOpen[0], T.lensClose[1]]);
  const g = ramp(f, T.gates);
  const pts = gatesPts.map(([u, v]) => [IMG.x + u * IMG.w, IMG.y + v * IMG.h] as XY);
  const segLen = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]) + Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
  const mini = 0.6 + 0.4 * ramp(f, [T.lensOpen[1], T.lensOpen[1] + 15]);
  const pulse = 10 + 8 * Math.abs(Math.sin((f / 30) * Math.PI));
  const lp = P(LOCKPORT);
  const mk = 1.2;
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <div style={{position: 'absolute', left: IMG.x, top: IMG.y, width: IMG.w, height: IMG.h, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
        <Img src={staticFile('assets/lockport-c1855-2400.jpg')} style={{width: '100%', height: '100%', transform: `scale(${drift})`, transformOrigin: '52% 74%'}} />
      </div>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={C.accent} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round"
          strokeDasharray={segLen} strokeDashoffset={segLen * (1 - g)} />
        <g opacity={ramp(f, [T.gates[1] - 10, T.gates[1] + 8])}>
          <line x1={pts[2][0] + 8} y1={pts[2][1] - 6} x2={pts[2][0] + 70} y2={pts[2][1] - 70} stroke={C.accent} strokeWidth={2.5} />
          <rect x={pts[2][0] + 60} y={pts[2][1] - 122} width={204} height={52} fill={C.paper} />
          <text x={pts[2][0] + 76} y={pts[2][1] - 84} style={{...label, fontSize: 31, fontWeight: 700}} fill={C.accent}>Lock gates</text>
        </g>
      </svg>
      <div style={{position: 'absolute', left: 1268, top: 250, width: 590, color: C.ink}}>
        <div style={{...label, fontSize: 27, opacity: 0.72}}>Lockport, New York</div>
        <div style={{fontFamily: F.title, fontSize: 64, lineHeight: 1.06, marginTop: 14, fontVariationSettings: '"opsz" 72, "SOFT" 50'}}>A staircase of locks</div>
        <div style={{fontFamily: F.label, fontSize: 39, lineHeight: 1.28, marginTop: 22}}>
          Here the canal climbed the Niagara Escarpment, one lock at a time.
        </div>
        <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16}}>documented</div>
        <div style={{height: 1, background: C.rule, margin: '30px 0 22px'}} />
        <div style={{fontFamily: F.label, fontSize: 28, lineHeight: 1.32}}>
          Lockport, N.Y., about 1855. Steel engraving published by Herrmann J. Meyer, New York.
        </div>
        <div style={{display: 'inline-block', marginTop: 16, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 23, letterSpacing: '0.12em'}}>
          Public domain · Wikimedia Commons
        </div>
      </div>
      <svg width={220} height={220} style={{position: 'absolute', left: 1650, top: 54, transform: `scale(${mini})`, transformOrigin: '110px 110px'}}>
        <defs>
          <clipPath id="mini">
            <circle cx={110} cy={110} r={100} />
          </clipPath>
        </defs>
        <g clipPath="url(#mini)">
          <rect width={220} height={220} fill={C.water} />
          <g transform={`translate(${110 - lp[0] * mk},${110 - lp[1] * mk}) scale(${mk})`}>
            <path d={geo.land} fill={C.land} />
            <path d={geo.lakes} fill={C.water} />
            <path d={canalLine.pts.length ? 'M' + canalLine.pts.map((q) => q.join(',')).join('L') : ''} fill="none" stroke={C.accent} strokeWidth={3} vectorEffect="non-scaling-stroke" />
          </g>
          <circle cx={110} cy={110} r={pulse} fill="none" stroke={C.accent} strokeWidth={2} opacity={0.7} />
          <circle cx={110} cy={110} r={7} fill={C.accent} />
        </g>
        <circle cx={110} cy={110} r={100} fill="none" stroke={C.ink} strokeWidth={2.5} />
      </svg>
    </AbsoluteFill>
  );
};

export const Probe: React.FC = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(fontFiles.map((x) => new FontFace(x.family, `url(${staticFile(x.file)})`, {weight: x.weight}).load()))
      .then((faces) => {
        faces.forEach((face) => document.fonts.add(face));
        continueRender(handle);
      });
  }, [handle]);

  const f = useCurrentFrame();
  const cam = camera(f);
  const lock = toScreen(P(LOCKPORT), cam);
  const maxR = Math.hypot(Math.max(lock[0], W - lock[0]), Math.max(lock[1], H - lock[1]));
  const ring = ramp(f, T.lensRing) * (1 - ramp(f, [T.lensClose[1], T.lensClose[1] + 14]));
  const r = 66 + (maxR - 66) * (ramp(f, T.lensOpen) - ramp(f, T.lensClose));
  const insertOn = f >= T.lensOpen[0] && f < T.lensClose[1];
  return (
    <AbsoluteFill style={{background: C.water}}>
      <MapLayer f={f} cam={cam} />
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <circle cx={lock[0]} cy={lock[1]} r={66 * ring} fill="none" stroke={C.ink} strokeWidth={3} opacity={ring} />
        <Ruler f={f} />
      </svg>
      <Titles f={f} />
      {insertOn ? (
        <AbsoluteFill style={{clipPath: `circle(${r}px at ${lock[0]}px ${lock[1]}px)`}}>
          <Insert f={f} />
        </AbsoluteFill>
      ) : null}
      {insertOn ? (
        <svg width={W} height={H} style={{position: 'absolute', pointerEvents: 'none'}}>
          <circle cx={lock[0]} cy={lock[1]} r={r} fill="none" stroke={C.ink} strokeWidth={3} opacity={1 - ramp(f, [T.lensOpen[1] - 8, T.lensOpen[1]]) + ramp(f, [T.lensClose[0], T.lensClose[0] + 8])} />
        </svg>
      ) : null}
    </AbsoluteFill>
  );
};

export const PROBE_FRAMES = T.end;
````

## probe/src/Root.tsx

````tsx
import React from 'react';
import {Composition, Still} from 'remotion';
import {Avatar, Banner, BannerCheck} from './Brand';
import {EPISODE_FRAMES, Episode} from './Episode';
import {FRAMES} from './Frames';
import {PILOT_FRAMES, Pilot} from './Pilot';
import {PROBE_FRAMES, Probe} from './Probe';
import {THUMB, ThumbA, ThumbB, ThumbC} from './Thumbs';
import {FPS, H, W} from './theme';

export const Root: React.FC = () => (
  <>
    <Composition id="Episode" component={Episode} durationInFrames={EPISODE_FRAMES} fps={FPS} width={W} height={H} />
    <Composition id="Pilot" component={Pilot} durationInFrames={PILOT_FRAMES} fps={FPS} width={W} height={H} />
    <Composition id="Probe" component={Probe} durationInFrames={PROBE_FRAMES} fps={FPS} width={W} height={H} />
    <Still id="Avatar" component={Avatar} width={800} height={800} />
    <Still id="Banner" component={Banner} width={2560} height={1440} />
    <Still id="BannerCheck" component={BannerCheck} width={2560} height={1440} />
    <Still id="ThumbA" component={ThumbA} {...THUMB} />
    <Still id="ThumbB" component={ThumbB} {...THUMB} />
    <Still id="ThumbC" component={ThumbC} {...THUMB} />
    {FRAMES.map(([id, component]) => (
      <Still key={id} id={id} component={component} width={W} height={H} />
    ))}
  </>
);
````

## probe/src/Thumbs.tsx

````tsx
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Img, continueRender, delayRender, staticFile} from 'remotion';
import {geoConicConformal, geoPath} from 'd3-geo';
import region from '../public/region/erie.json';
import canalLine from '../public/region/erie-canal-atack.json';
import {C, F, fontFiles} from './theme';
import {hudson} from './erie';

// Thumbnails 1280x720. Text is short and large: it must read at 320 px wide.
const TW = 1280;
const TH = 720;

const useFonts = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(fontFiles.map((x) => new FontFace(x.family, `url(${staticFile(x.file)})`, {weight: x.weight}).load())).then((faces) => {
      faces.forEach((face) => document.fonts.add(face));
      continueRender(handle);
    });
  }, [handle]);
};

const MapArt: React.FC<{box: number[]; w: number; h: number; stroke?: number}> = ({box, w, h, stroke = 9}) => {
  const [x0, y0, x1, y1] = box;
  const proj = geoConicConformal().parallels([40.5, 44]).rotate([76, 0]).fitExtent([[0, 0], [w, h]], {
    type: 'MultiPoint',
    coordinates: [[x0, y0], [x1, y0], [x1, y1], [x0, y1]],
  } as any);
  const path = geoPath(proj);
  const nyc = proj([-74.015, 40.704]) as [number, number];
  const buf = proj([-78.878, 42.886]) as [number, number];
  return (
    <svg width={w} height={h} style={{position: 'absolute'}}>
      <rect width={w} height={h} fill={C.water} />
      <path d={path(region.land as any) ?? ''} fill={C.land} />
      {region.relief.map((r, i) => (
        <path key={i} d={path(r.geometry as any) ?? ''} fill={C.relief} fillOpacity={0.4} />
      ))}
      <path d={path(region.lakes as any) ?? ''} fill={C.water} />
      <path d={path({type: 'GeometryCollection', geometries: region.rivers.map((r) => ({type: 'LineString', coordinates: r.coords}))} as any) ?? ''}
        fill="none" stroke={C.river} strokeWidth={1.5} />
      <path d={path({type: 'LineString', coordinates: hudson} as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={stroke * 0.6} strokeLinecap="round" />
      <path d={path(canalLine as any) ?? ''} fill="none" stroke={C.accent} strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={buf[0]} cy={buf[1]} r={stroke * 1.3} fill={C.accent} stroke={C.land} strokeWidth={3} />
      <circle cx={nyc[0]} cy={nyc[1]} r={stroke * 2.2} fill={C.accent} stroke={C.land} strokeWidth={4} />
    </svg>
  );
};

const big: React.CSSProperties = {fontFamily: F.title, color: C.ink, lineHeight: 0.95, fontVariationSettings: '"opsz" 144, "SOFT" 30, "WONK" 0', fontWeight: 600};
const small: React.CSSProperties = {fontFamily: F.label, color: C.ink, letterSpacing: '0.14em', textTransform: 'uppercase', fontWeight: 700};

// A: the map is the picture.
export const ThumbA: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{background: C.water}}>
      <MapArt box={[-79.6, 40.3, -72.6, 43.9]} w={TW} h={TH} />
      <div style={{position: 'absolute', left: 54, bottom: 52, ...big, fontSize: 150}}>One ditch.</div>
      <div style={{position: 'absolute', left: 60, bottom: 26, ...small, fontSize: 30, color: C.accent}}>Lake Erie → New York · 1825</div>
    </AbsoluteFill>
  );
};

// B: the insert is the picture; the map is the hint.
export const ThumbB: React.FC = () => {
  useFonts();
  const iw = 1000;
  const ih = (iw * 5008) / 7423;
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <div style={{position: 'absolute', right: -40, top: -20, width: iw, height: ih, overflow: 'hidden'}}>
        <Img src={staticFile('assets/lockport-c1855-2400.jpg')} style={{width: iw * 1.25, marginLeft: -iw * 0.12, marginTop: -ih * 0.18}} />
      </div>
      <svg width={TW} height={TH} style={{position: 'absolute'}}>
        <polyline points="640,453 860,512 1050,453" fill="none" stroke={C.accent} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div style={{position: 'absolute', left: 0, top: 0, width: 470, height: TH, background: C.paper}} />
      <div style={{position: 'absolute', left: 50, top: 120, width: 400, ...big, fontSize: 118}}>A stair­case for boats</div>
      <div style={{position: 'absolute', left: 54, bottom: 60, ...small, fontSize: 28, color: C.accent}}>Erie Canal · Lockport</div>
    </AbsoluteFill>
  );
};

// C: the person, the line, the question.
export const ThumbC: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{background: C.water}}>
      <MapArt box={[-80.5, 39.4, -70.5, 46.6]} w={TW} h={TH} stroke={7} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 470, height: TH, overflow: 'hidden', borderRight: `6px solid ${C.ink}`}}>
        <Img src={staticFile('assets/met-11602-clinton-morse.jpg')} style={{height: TH * 1.32, marginLeft: -170, marginTop: -40}} />
      </div>
      <div style={{position: 'absolute', left: 500, top: 30, padding: '14px 26px 22px', background: C.land, ...big, fontSize: 112, width: 700}}>Why New York won</div>
      <div style={{position: 'absolute', left: 526, bottom: 40, ...small, fontSize: 28}}>DeWitt Clinton · 1826 portrait</div>
    </AbsoluteFill>
  );
};

export const THUMB = {width: TW, height: TH};
````

## probe/src/ch2.tsx

````tsx
// Chapter 2, "Clinton's Ditch", on the map: the 1790s locks, the planned line, the Ontario route not taken,
// digging from Rome, contract sections and the Montezuma fever, the name. Own-drawing inserts: src/pages-a.tsx.
import React from 'react';
import {C} from './theme';
import {S, lineWith} from './narration';
import {
  ALBANY, ATACK, Arrow, BUFFALO, Ctx, Head, Ins, LITTLE_FALLS, Lbl, LockGlyph, LonLat, MONTEZUMA, MONTREAL, Move, NYC, Note, OSWEGO, P,
  PicPage, Part, QuoteCard, ROME, SCHENECTADY, View, YearKey, chapterTitle, cut, fracAt, label, line, ramp, segment, smooth, win,
} from './kit';

const V: Record<string, View> = {
  mohawk: {c: [-74.75, 42.98], k: 9},
  plan: {c: [-76.3, 42.95], k: 5.2},
  north: {c: [-76.1, 44.15], k: 4.3},
  east: {c: [-75.6, 41.1], k: 3.0},
  rome: {c: [-75.45, 43.17], k: 10},
  west: {c: [-76.2, 42.95], k: 5.6},
};
const MOVES: Move[] = [
  {at: S.idea.start, dur: 3.5, v: V.mohawk},
  {at: S.scale.start, dur: 2.5, v: V.plan},
  {at: S.ontario.start + 0.4, dur: 3, v: V.north},
  {at: S.champion.start + 1, dur: 2, v: V.east},
  {at: S.rome.start, dur: 3, v: V.rome},
  {at: S.labor.start, dur: 3, v: V.west},
  {at: S.name.start, dur: 2.5, v: V.plan},
];

const YEARS: YearKey[] = [
  {at: line('idea', 2).from, dur: 2, y: 1795},
  {at: S.scale.start, dur: 1.5, y: 1817},
  {at: lineWith('labor', 'fever').from, dur: 1, y: 1819},
  {at: S.name.voice, dur: 2, y: 1825},
];

const END = S.problem.start + 1.2;
const ROME_AT = fracAt(ATACK, ROME);
// Ontario route, schematic: Rome to Oswego by Wood Creek, Oneida Lake and the Oswego River, across the lake
// and down the St. Lawrence to Montreal.
const ONTARIO = smooth([ROME, [-75.75, 43.22], [-76.1, 43.25], [-76.35, 43.33], OSWEGO, [-76.55, 43.85], [-76.45, 44.2], [-75.9, 44.42], [-75.2, 44.85], [-74.6, 45.05], [-74.1, 45.3], MONTREAL], 6);

const LABELS: Lbl[] = [
  {text: 'Mohawk River', at: [-74.3, 42.86], from: S.idea.voice, to: S.scale.start + 1, size: 30, color: C.force, italic: true, rotate: -8, anchor: 'middle'},
  {text: 'Schenectady', at: SCHENECTADY, from: S.idea.voice + 0.6, to: S.scale.start + 1, dx: 14, dy: 30, dot: true},
  {text: 'Little Falls', at: LITTLE_FALLS, from: line('idea', 2).from, to: S.scale.start + 1, dx: 0, dy: -30, anchor: 'middle', dot: true, bold: true},
  {text: 'Rome', at: ROME, from: line('idea', 2).from + 1.4, to: S.scale.start + 1, dx: 0, dy: -30, anchor: 'middle', dot: true},
  {text: 'Albany', at: ALBANY, from: S.scale.voice, to: S.ontario.start + 1, dx: 16, dy: 30, dot: true},
  {text: 'Buffalo', at: BUFFALO, from: S.scale.voice + 3, to: S.ontario.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'Lake Erie', at: [-80.0, 42.25], from: S.scale.voice + 3, to: S.champion.start + 1, size: 30, color: C.force, italic: true, rotate: -30, spacing: '0.28em', anchor: 'middle'},
  {text: 'Lake Ontario', at: [-77.6, 43.62], from: S.ontario.voice + 1, to: S.champion.start + 1, size: 30, color: C.force, italic: true, rotate: -4, spacing: '0.28em', anchor: 'middle'},
  {text: 'Oswego', at: OSWEGO, from: line('ontario', 1).from, to: S.champion.start + 1, dx: -16, dy: 10, anchor: 'end', dot: true},
  {text: 'St. Lawrence', at: [-75.35, 44.62], from: line('ontario', 1).from + 2, to: S.champion.start + 1, size: 28, color: C.force, italic: true, rotate: -32, anchor: 'middle'},
  {text: 'Montreal', at: MONTREAL, from: line('ontario', 1).from + 3.5, to: S.champion.start + 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'British Canada', at: [-76.6, 45.05], from: line('ontario', 1).from + 4, to: S.champion.start + 1, size: 34, spacing: '0.4em', anchor: 'middle', color: '#9C8456', bold: true},
  {text: 'New York', at: NYC, from: line('ontario', 2).from, to: S.rome.start + 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Washington', at: [-77.04, 38.9], from: S.veto.start - 1, to: S.veto.start + 0.6, dx: 16, dy: 10, dot: true},
  {text: 'Rome · July 4, 1817', at: ROME, from: line('rome', 2).from, to: S.labor.start + 1, dx: 0, dy: -30, anchor: 'middle', dot: true, bold: true},
  {text: 'Utica', at: [-75.233, 43.101], from: line('rome', 3).from, to: S.labor.start + 1, dx: 0, dy: 40, anchor: 'middle', dot: true},
  {text: 'Oneida Lake', at: [-76.0, 43.29], from: line('rome', 3).from + 0.6, to: S.labor.start + 1, size: 26, color: C.force, italic: true, anchor: 'middle'},
  {text: 'Montezuma marshes', at: MONTEZUMA, from: line('labor', 3).from, to: S.name.start + 1, dx: 0, dy: -72, anchor: 'middle', size: 30, bold: true},
  {text: 'Fever, 1819 · over 1,000 men laid up', at: MONTEZUMA, from: line('labor', 3).from + 1.2, to: S.name.start + 1, dx: 0, dy: 62, anchor: 'middle', size: 28, color: C.accent},
  {text: 'Albany', at: ALBANY, from: S.name.start, to: END, dx: 16, dy: 30, dot: true},
  {text: 'Buffalo', at: BUFFALO, from: S.name.start, to: END, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: "Clinton's Ditch", at: [-76.2, 43.32], from: S.name.voice, to: END, size: 46, color: C.accent, italic: true, anchor: 'middle', spacing: '0.2em', bold: true},
];

const NOTES: Note[] = [
  {from: S.idea.start, to: S.scale.start, text: 'Locks of the 1790s: places only · Natural Earth, NOAA ETOPO 2022'},
  {from: S.scale.start, to: S.ontario.start, text: 'Dashed: the planned line · canal line J. Atack (2015) · Natural Earth'},
  {from: S.ontario.start, to: S.champion.start, text: 'Dashed: the Ontario route, schematic · modern coastline and rivers · Natural Earth'},
  {from: S.rome.start, to: S.labor.start, text: 'Solid: dug · dashed: still to dig · pace of digging schematic · canal line J. Atack (2015)'},
  {from: S.labor.start, to: S.name.start, text: 'Contract sections schematic · marsh area approximate · canal line J. Atack (2015)'},
  {from: S.name.start, to: END, text: 'Canal line J. Atack (2015) · Natural Earth, NOAA ETOPO 2022'},
];

// How much of the line is planned (dashed) and how much is dug (solid), from Rome both ways.
function calc(t: number) {
  const plan = ramp(t, S.scale.voice + 0.3, line('scale', 1).to);
  const dug = 0.04 * ramp(t, line('rome', 2).from + 0.5, line('rome', 3).to) + 0.5 * ramp(t, S.labor.voice, line('labor', 1).to) + 0.46 * ramp(t, line('labor', 2).from, S.name.voice + 0.5);
  const half = (f: number) => [Math.max(0, ROME_AT - f * ROME_AT * 1.1), Math.min(1, ROME_AT + f * (1 - ROME_AT) * 1.1)] as const;
  return {plan, dug, span: half(Math.min(1, dug)), on: win(t, S.scale.start, END, 0.8)};
}

const under = ({t}: Ctx) => {
  const s = calc(t);
  const route = cut(ONTARIO, ramp(t, line('ontario', 1).from, line('ontario', 1).to + 1));
  const routeOn = win(t, line('ontario', 1).from, line('ontario', 3).from + 0.8, 0.5);
  const glow = win(t, S.name.voice, END, 0.6);
  return (
    <>
      <path d={route.d} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray="12 9" strokeDashoffset={-t * 30} strokeLinecap="round" opacity={routeOn} vectorEffect="non-scaling-stroke" />
      <g opacity={s.on}>
        <path d={cut(ATACK, s.plan).d} fill="none" stroke={C.accent} strokeWidth={5} strokeDasharray="12 9" strokeLinecap="round" strokeLinejoin="round" opacity={0.85} vectorEffect="non-scaling-stroke" />
        {s.dug > 0 ? <path d={segment(ATACK, s.span[0], s.span[1])} fill="none" stroke={C.accent} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" /> : null}
        <path d={cut(ATACK, 1).d} fill="none" stroke={C.accent} strokeWidth={18} strokeLinecap="round" strokeLinejoin="round" strokeOpacity={0.22 * glow} vectorEffect="non-scaling-stroke" />
      </g>
    </>
  );
};

const over = ({t, at, cam}: Ctx) => {
  const s = calc(t);
  const head = cut(ATACK, s.plan);
  const routeOn = win(t, line('ontario', 1).from, line('ontario', 3).from + 0.8, 0.5);
  const route = cut(ONTARIO, ramp(t, line('ontario', 1).from, line('ontario', 1).to + 1));
  // 1790s locks around Little Falls and at the Rome carry, as places only.
  const locksOn = win(t, line('idea', 2).from + 0.6, S.scale.start + 1, 0.4);
  const p = (q: LonLat) => at(P(q));
  // Contract sections: short ticks along the dug line, schematic.
  const ticksOn = win(t, S.labor.voice, S.name.start + 0.5, 0.5);
  const ticks = ticksOn > 0 ? Array.from({length: 40}, (_, i) => (i + 0.5) / 40).filter((f) => f >= s.span[0] && f <= s.span[1]) : [];
  const marsh = win(t, line('labor', 3).from, S.name.start + 1, 0.6);
  const mz = p(MONTEZUMA);
  return (
    <>
      {s.plan > 0 && s.plan < 1 ? Head(at(head.head), C.accent) : null}
      {s.plan > 0.02 && s.on > 0 ? (() => {
        const [x, y] = at(head.head);
        return (
          <text x={x} y={y - 30} textAnchor={s.plan < 0.5 ? 'start' : 'end'} style={{...label, fontSize: 34, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={8} strokeLinejoin="round" fill={C.accent} opacity={win(t, S.scale.voice, S.ontario.start + 0.5, 0.4)}>
            {s.plan >= 1 ? '363 miles' : `${Math.round(363 * s.plan)} miles`}
          </text>
        );
      })() : null}
      {routeOn > 0 && route.d ? Arrow(at(route.head), route.dir, C.ink, routeOn) : null}
      {locksOn > 0 ? [LockGlyph(p(LITTLE_FALLS), locksOn, 1.3), LockGlyph(p([-75.5, 43.215]), locksOn * ramp(t, line('idea', 2).from + 1.4, line('idea', 2).from + 1.9), 1.3)] : null}
      {locksOn > 0 ? (
        <text x={p(LITTLE_FALLS)[0]} y={p(LITTLE_FALLS)[1] + 58} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.accent} opacity={locksOn}>
          1790s · a private company's small locks
        </text>
      ) : null}
      {s.dug > 0 && s.dug < 1 && t < S.name.voice ? [Head(at(cut(ATACK, s.span[0]).head), C.accent), Head(at(cut(ATACK, s.span[1]).head), C.accent)] : null}
      {ticks.map((f, i) => {
        const c = cut(ATACK, f);
        const [x, y] = at(c.head);
        const n = Math.hypot(c.dir[0], c.dir[1]) || 1;
        const [nx, ny] = [-c.dir[1] / n, c.dir[0] / n];
        return <line key={i} x1={x - nx * 12} y1={y - ny * 12} x2={x + nx * 12} y2={y + ny * 12} stroke={C.ink} strokeWidth={3} opacity={ticksOn} />;
      })}
      {marsh > 0 ? (
        <g opacity={marsh}>
          <defs>
            <pattern id="marsh" width={12} height={12} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <line x1={0} y1={0} x2={0} y2={12} stroke={C.force} strokeWidth={3} />
            </pattern>
          </defs>
          <ellipse cx={mz[0]} cy={mz[1]} rx={70 * cam.k / 3.3} ry={34 * cam.k / 3.3} fill="url(#marsh)" stroke={C.force} strokeWidth={2.5} />
        </g>
      ) : null}
    </>
  );
};
const Champion: Ins = {
  from: S.champion.start, to: S.champion.end, at: ALBANY, render: (_t, d) => (
    <PicPage src="assets/met-11602-clinton-morse.jpg" w={3106} h={3710} origin="50% 30%" drift={d} at={ALBANY}
      s={{kicker: 'DeWitt Clinton, 1769–1828', head: 'The champion', body: 'Mayor of New York City, canal commissioner from 1810, governor from 1817.', tag: 'portrait painted in 1826', credit: 'DeWitt Clinton. Samuel F. B. Morse, 1826. Oil on canvas.', plaque: 'The Met · Public domain'}} />
  ),
};

export const PART2: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  inserts: [Champion],
  under,
  over,
  top: (t) => (
    <>
      {chapterTitle(2, "Clinton's Ditch", S.idea.start, END)(t)}
      <QuoteCard o={win(t, line('ontario', 2).from, S.ontario.end, 0.6)} quote="When a vessel once descends into Ontario, she will pursue the course ordained by nature." source="Memorial in favour of the canal, 1816 · in Hosack, Memoir of De Witt Clinton, 1829" />
    </>
  ),
};
````

## probe/src/ch3.tsx

````tsx
// Chapter 3, "The Climb", on the map: 83 locks and the long level, the Niagara Escarpment, Lockport,
// the Rochester aqueduct, the middle section paying tolls in 1820. Own-drawing inserts: src/pages-a.tsx, src/pages-b.tsx.
import React from 'react';
import {C} from './theme';
import {S, lineWith} from './narration';
import {
  ALBANY, ATACK, BUFFALO, Ctx, Ins, LITTLE_FALLS, LOCKPORT, Lbl, LonLat, MONTEZUMA, Move, NIAGARA_FALLS, Note, P, PicPage, Part,
  ROCHESTER, SYRACUSE, UTICA, View, YearKey, chapterTitle, cut, fracAt, label, line, ramp, segment, smooth, win,
} from './kit';

const FRANKFORT: LonLat = [-75.07, 43.04];
const V: Record<string, View> = {
  plan: {c: [-76.3, 42.95], k: 5.2},
  west: {c: [-78.35, 43.1], k: 22},
};
const MOVES: Move[] = [
  {at: S.problem.start, dur: 2.5, v: V.plan},
  {at: S.escarpment.start, dur: 3, v: V.west},
  {at: S.sections.start, dur: 2.5, v: V.plan},
];
const YEARS: YearKey[] = [
  {at: line('problem', 1).from, dur: 1.5, y: 1821},
  {at: S.lockport.start, dur: 1.5, y: 1825},
  {at: lineWith('sections', 'tolls').from, dur: 1.5, y: 1820},
  {at: lineWith('sections', 'tolls').to, dur: 1.5, y: 1825},
];

const END = S.opened.start + 1.2;
const at = (q: LonLat) => fracAt(ATACK, q);
const MOHAWK = [0, at(FRANKFORT)] as const;
const LEVEL = [at(FRANKFORT), at(SYRACUSE)] as const;
const MIDDLE = [at(UTICA), at(MONTEZUMA)] as const;
// Niagara Escarpment, approximate and schematic: from the Niagara gorge east through Lockport, where the canal
// climbs it; east of Lockport the canal runs on the plain below it, to the north.
const ESCARPMENT = smooth([[-79.05, 43.14], [-78.88, 43.135], [-78.69, 43.158], [-78.5, 43.14], [-78.28, 43.13], [-78.05, 43.125]], 8);

const LABELS: Lbl[] = [
  {text: 'Albany', at: ALBANY, from: S.locks83.start, to: S.escarpment.start + 1, dx: 16, dy: 30, dot: true},
  {text: 'Buffalo', at: BUFFALO, from: S.locks83.start, to: S.escarpment.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'Mohawk Valley', at: [-74.45, 42.68], from: line('locks83', 1).from, to: S.escarpment.start + 1, size: 30, color: C.force, italic: true, rotate: -6, anchor: 'middle'},
  {text: 'Salina', at: SYRACUSE, from: line('locks83', 2).from + 1, to: S.escarpment.start + 1, dx: 0, dy: 40, anchor: 'middle', dot: true},
  {text: 'Frankfort', at: FRANKFORT, from: line('locks83', 2).from + 1.4, to: S.escarpment.start + 1, dx: 0, dy: 40, anchor: 'middle', dot: true},
  {text: 'Lake Ontario', at: [-78.2, 43.45], from: S.escarpment.start + 1, to: S.sections.start + 1, size: 30, color: C.force, italic: true, spacing: '0.28em', anchor: 'middle'},
  {text: 'Niagara Falls', at: NIAGARA_FALLS, from: line('escarpment', 1).from, to: S.sections.start + 1, dx: -16, dy: 34, anchor: 'end', dot: true},
  {text: 'Niagara Escarpment', at: [-78.2, 43.06], from: S.escarpment.voice + 2.5, to: S.sections.start + 1, size: 32, color: '#8A6F42', anchor: 'middle', spacing: '0.3em', bold: true},
  {text: 'Lockport', at: LOCKPORT, from: S.lockport.start - 0.6, to: S.sections.start + 1, dx: 0, dy: -30, anchor: 'middle', dot: true, bold: true},
  {text: 'Buffalo', at: BUFFALO, from: S.escarpment.start + 1, to: S.sections.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'Rochester', at: ROCHESTER, from: S.aqueduct.start - 0.6, to: S.sections.start + 1, dx: 18, dy: 34, dot: true, bold: true},
  {text: 'Genesee River', at: [-77.67, 42.98], from: line('aqueduct', 1).from, to: S.sections.start + 1, size: 26, color: C.force, italic: true, rotate: -80, anchor: 'middle'},
  {text: 'Utica', at: UTICA, from: lineWith('sections', 'tolls').from, to: END, dx: 0, dy: 40, anchor: 'middle', dot: true},
  {text: 'Seneca River', at: MONTEZUMA, from: lineWith('sections', 'tolls').from + 0.4, to: END, dx: 0, dy: 40, anchor: 'middle', dot: true},
  {text: 'Middle section · tolls from 1820', at: [-75.95, 43.3], from: lineWith('sections', 'tolls').from + 1, to: END, size: 30, color: C.accent, anchor: 'middle', bold: true},
];

const NOTES: Note[] = [
  {from: S.locks83.start, to: S.escarpment.start, text: 'Lock positions not shown · long level: Colden, 1825 · canal line J. Atack (2015)'},
  {from: S.escarpment.start, to: S.sections.start, text: 'Escarpment line approximate · canal line J. Atack (2015) · Natural Earth, NOAA ETOPO 2022'},
  {from: S.sections.start, to: END, text: 'Ends of the middle section approximate · canal line J. Atack (2015)'},
];

const under = ({t}: Ctx) => {
  const on = win(t, S.problem.start, END, 0.8);
  const valley = win(t, line('locks83', 1).from, S.escarpment.start + 0.5, 0.5);
  const level = ramp(t, line('locks83', 2).from + 0.5, line('locks83', 2).to - 1) * (1 - ramp(t, S.escarpment.start, S.escarpment.start + 0.8));
  const middle = ramp(t, lineWith('sections', 'tolls').from, lineWith('sections', 'tolls').from + 2.5);
  const esc = cut(ESCARPMENT, ramp(t, S.escarpment.voice + 0.5, line('escarpment', 0).to));
  const escOn = win(t, S.escarpment.voice, S.sections.start + 0.8, 0.5);
  return (
    <>
      <g opacity={on}>
        <path d={cut(ATACK, 1).d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" opacity={1 - 0.6 * middle * (1 - ramp(t, lineWith('sections', 'tolls').to, lineWith('sections', 'tolls').to + 1.5))} vectorEffect="non-scaling-stroke" />
        <path d={segment(ATACK, MOHAWK[0], MOHAWK[1])} fill="none" stroke={C.accent} strokeWidth={18} strokeLinecap="round" strokeOpacity={0.25 * valley} vectorEffect="non-scaling-stroke" />
        <path d={segment(ATACK, LEVEL[0], LEVEL[0] + (LEVEL[1] - LEVEL[0]) * level)} fill="none" stroke={C.force} strokeWidth={10} strokeLinecap="round" strokeOpacity={0.9} vectorEffect="non-scaling-stroke" />
        <path d={segment(ATACK, MIDDLE[0], MIDDLE[0] + (MIDDLE[1] - MIDDLE[0]) * middle)} fill="none" stroke={C.accent} strokeWidth={10} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </g>
      <path d={esc.d} fill="none" stroke="#8A6F42" strokeWidth={5} strokeDasharray="14 8" strokeLinecap="round" opacity={escOn} vectorEffect="non-scaling-stroke" />
    </>
  );
};

const over = ({t, at: scrAt}: Ctx) => {
  const n = Math.round(83 * ramp(t, S.locks83.voice, line('locks83', 0).to + 0.4));
  const countOn = win(t, S.locks83.voice, S.escarpment.start + 0.5, 0.4);
  const levelOn = win(t, line('locks83', 2).from + 1.5, S.escarpment.start + 0.5, 0.5);
  const lv = cut(ATACK, (LEVEL[0] + LEVEL[1]) / 2).head;
  const [lx, ly] = scrAt(lv);
  // Escarpment hachures: short ticks on the low (north) side, drawn as the line grows.
  const escF = ramp(t, S.escarpment.voice + 0.5, line('escarpment', 0).to);
  const escOn = win(t, S.escarpment.voice, S.sections.start + 0.8, 0.5);
  const ticks = Array.from({length: 26}, (_, i) => (i + 0.5) / 26).filter((f) => f <= escF);
  const [cx, cy] = scrAt(P([-76.0, 42.45]));
  return (
    <>
      {countOn > 0 ? (
        <g opacity={countOn}>
          <text x={cx} y={cy} textAnchor="middle" style={{fontFamily: 'Fraunces', fontSize: 96, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={10} strokeLinejoin="round" fill={C.accent}>{n}</text>
          <text x={cx} y={cy + 48} textAnchor="middle" style={{...label, fontSize: 32, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.ink}>locks · 1825</text>
        </g>
      ) : null}
      {levelOn > 0 ? (
        <text x={lx} y={ly - 34} textAnchor="middle" style={{...label, fontSize: 30, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.force} opacity={levelOn}>
          69.5 miles without a lock
        </text>
      ) : null}
      {escOn > 0
        ? ticks.map((f, i) => {
            const c = cut(ESCARPMENT, f);
            const [x, y] = scrAt(c.head);
            const len = Math.hypot(c.dir[0], c.dir[1]) || 1;
            const [nx, ny] = [c.dir[1] / len, -c.dir[0] / len];
            return <line key={i} x1={x} y1={y} x2={x + nx * 16} y2={y + ny * 16} stroke="#8A6F42" strokeWidth={3} opacity={escOn} />;
          })
        : null}
    </>
  );
};

const Aqueduct: Ins = {
  from: S.aqueduct.start, to: S.aqueduct.end, at: ROCHESTER, render: (_t, d) => (
    <PicPage src="assets/nypl-rochester-aqueduct-1825.jpg" w={2856} h={1902} origin="45% 60%" drift={d} at={ROCHESTER}
      s={{kicker: 'Rochester, on the Genesee', head: 'A bridge that carries water', body: 'Stone aqueduct, 802 feet long, finished in 1823.', tag: 'drawing undated', credit: 'View of the Aqueduct Bridge at Rochester. Drawing by J. Eights.', plaque: 'NYPL · Public domain'}} />
  ),
};

export const PART3: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  inserts: [Aqueduct],
  under,
  over,
  top: chapterTitle(3, 'The Climb', S.problem.start, END),
};
````

## probe/src/ch4.tsx

````tsx
// Chapter 4, "Ten Days in 1825", on the map: Buffalo harbour, the cannon relay from Buffalo to Sandy Hook,
// the nine-day voyage, the victory party. The celebration book, vases and plate: src/pages-b.tsx.
import React from 'react';
import {C, F} from './theme';
import {S, lineWith} from './narration';
import {hudson} from './erie';
import {
  ALBANY, ATACK, BUFFALO, Boat, Ctx, Ins, Lbl, Move, NYC, Note, P, PicPage, Part, ROCHESTER, SANDY, SYRACUSE, UTICA, View, YearKey,
  chapterTitle, cut, fracAt, label, line, mkLine, ramp, win,
} from './kit';

const V: Record<string, View> = {
  state: {c: [-75.3, 41.8], k: 4.4},
  whole: {c: [-79, 38.6], k: 1.08},
};
const MOVES: Move[] = [
  {at: S.opened.start, dur: 2.5, v: V.state},
  {at: S.party.start, dur: 3.5, v: V.whole},
];
const YEARS: YearKey[] = [{at: S.opened.start, dur: 1.5, y: 1825}];
const END = S.twist.start + 1.2;

// The signal's path: down the canal from Buffalo, down the Hudson, out to Sandy Hook.
const PATH = mkLine([...[...ATACK.pts].reverse(), ...hudson.slice(1).map((q) => P(q)), P(SANDY)]);
const NYC_AT = fracAt(PATH, [-74.015, 40.704]);
const ALBANY_AT = fracAt(PATH, ALBANY);

// Relay: the signal leaves Buffalo at 10:00, reaches New York at 11:19 and Sandy Hook at 11:21 (Colden, 1825).
// Between the ends the clock runs in proportion to distance: schematic.
const R0 = line('relay', 1).from;
const R1 = line('relay', 5).from + 2.2;
const R2 = R1 + 1.4;
const relayF = (t: number) => (t <= R1 ? NYC_AT * ramp(t, R0, R1) : NYC_AT + (1 - NYC_AT) * ramp(t, R1, R2));
const clock = (f: number) => {
  const m = f <= NYC_AT ? (79 * f) / NYC_AT : 79 + (2 * (f - NYC_AT)) / (1 - NYC_AT);
  const total = 600 + Math.round(m);
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, '0')}`;
};
// Voyage: Buffalo October 26 to New York November 4; the boat's pace between is schematic.
const B0 = line('voyage', 0).from;
const B1 = line('voyage', 2).from + 2;
const B2 = S.voyage.end - 0.4;
const boatF = (t: number) => (t <= B1 ? NYC_AT * ramp(t, B0, B1) : NYC_AT + (1 - NYC_AT) * ramp(t, B1, B2));

const LABELS: Lbl[] = [
  {text: 'Buffalo', at: BUFFALO, from: S.opened.start + 1, to: S.party.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true, bold: true},
  {text: 'Albany', at: ALBANY, from: S.relay.voice + 1, to: S.party.start + 1, dx: 16, dy: 30, dot: true},
  {text: 'New York', at: NYC, from: S.relay.voice + 1, to: END, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Sandy Hook', at: SANDY, from: S.relay.voice + 1.5, to: S.party.start + 1, dx: 18, dy: 34, dot: true},
  {text: 'Rochester', at: ROCHESTER, from: lineWith('voyage', 'crowds').from, to: S.voyage.end, dx: 0, dy: -24, anchor: 'middle', size: 24, dot: true},
  {text: 'Syracuse', at: SYRACUSE, from: lineWith('voyage', 'crowds').from + 0.3, to: S.voyage.end, dx: 0, dy: 36, anchor: 'middle', size: 24, dot: true},
  {text: 'Utica', at: UTICA, from: lineWith('voyage', 'crowds').from + 0.6, to: S.voyage.end, dx: 0, dy: -24, anchor: 'middle', size: 24, dot: true},
];

const NOTES: Note[] = [
  {from: S.relay.start, to: S.voyage.start, text: 'Times: Colden, Memoir, 1825 · gun positions and clock between the ends schematic · canal line J. Atack (2015)'},
  {from: S.voyage.start, to: S.book.start, text: 'Boat pace between Buffalo and New York schematic · celebrations along the line, places only'},
  {from: S.party.start, to: END, text: 'Canal line J. Atack (2015) · Natural Earth, NOAA ETOPO 2022'},
];

const under = ({t}: Ctx) => {
  const on = win(t, S.opened.start, END, 0.8);
  const rf = relayF(t);
  const relayOn = win(t, R0, S.voyage.start + 0.6, 0.4);
  const glow = win(t, S.party.voice, END, 0.6) * (0.6 + 0.4 * Math.sin(t * Math.PI * 1.5));
  return (
    <g opacity={on}>
      <path d={cut(ATACK, 1).d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <path d={cut(PATH, 1).d} fill="none" stroke={C.accent} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" strokeOpacity={0.25 * glow} vectorEffect="non-scaling-stroke" />
      {rf > 0 ? <path d={cut(PATH, rf).d} fill="none" stroke="#F2C14E" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" opacity={relayOn} vectorEffect="non-scaling-stroke" /> : null}
    </g>
  );
};

const over = ({t, at}: Ctx) => {
  const rf = relayF(t);
  const relayOn = win(t, R0, S.voyage.start + 0.6, 0.4);
  // A gun every 1/28 of the path, firing when the signal passes it: schematic positions.
  const guns = Array.from({length: 29}, (_, i) => i / 28).map((f) => {
    const passed = rf >= f ? (t - (R0 + (f <= NYC_AT ? (f / NYC_AT) * (R1 - R0) : R1 - R0 + ((f - NYC_AT) / (1 - NYC_AT)) * (R2 - R1)))) : -1;
    return {f, age: passed};
  });
  const head = cut(PATH, rf).head;
  const bf = boatF(t);
  const boat = cut(PATH, bf);
  const boatOn = win(t, B0 - 0.4, S.book.start + 0.5, 0.4);
  const day = Math.min(9, Math.floor(9 * ramp(t, B0, B1) + 1));
  const onHudson = bf > ALBANY_AT && bf < NYC_AT;
  const steamer = cut(PATH, Math.min(1, bf + 0.025));
  const parties = [ROCHESTER, SYRACUSE, UTICA, ALBANY].map((q) => ({q, f: fracAt(PATH, q)}));
  const clockOn = win(t, S.relay.voice, S.voyage.start + 0.4, 0.5);
  const dayOn = win(t, B0, S.book.start + 0.4, 0.5);
  return (
    <>
      {relayOn > 0
        ? guns.map(({f, age}, i) =>
            age >= 0 && age < 1.4 ? (() => {
              const [x, y] = at(cut(PATH, f).head);
              const u = age / 1.4;
              return (
                <g key={i}>
                  <circle cx={x} cy={y} r={8 + 46 * u} fill="none" stroke="#E0A32E" strokeWidth={4} opacity={(1 - u) * relayOn} />
                  <circle cx={x} cy={y} r={7 * (1 - u)} fill="#E0A32E" opacity={relayOn} />
                </g>
              );
            })() : null,
          )
        : null}
      {relayOn > 0 && rf > 0 && rf < 1 ? (() => {
        const [x, y] = at(head);
        return <circle cx={x} cy={y} r={11} fill="#F2C14E" stroke={C.ink} strokeWidth={2.5} opacity={relayOn} />;
      })() : null}
      {boatOn > 0 ? (() => {
        const [x, y] = at(boat.head);
        const [sx, sy] = at(steamer.head);
        return (
          <g opacity={boatOn}>
            {onHudson ? (
              <g>
                <line x1={x} y1={y} x2={sx} y2={sy} stroke={C.ink} strokeWidth={2} strokeDasharray="4 4" />
                <g transform={`translate(${sx - 22},${sy - 30}) scale(0.48)`}>
                  <Boat x={0} y={0} />
                  <rect x={40} y={-18} width={9} height={24} fill={C.ink} />
                </g>
              </g>
            ) : null}
            <g transform={`translate(${x - 22},${y - 26}) scale(0.48)`}>
              <Boat x={0} y={0} />
            </g>
          </g>
        );
      })() : null}
      {/* celebrations at towns as the boat passes: places only */}
      {boatOn > 0
        ? parties.map(({q, f}, i) => {
            const age = bf >= f ? (t - (B0 + (f / NYC_AT) * (B1 - B0))) : -1;
            if (age < 0 || age > 2.4) return null;
            const [x, y] = at(P(q));
            const u = (age % 0.8) / 0.8;
            return (
              <g key={i} opacity={1 - age / 2.4}>
                {Array.from({length: 8}, (_, j) => {
                  const a = (j / 8) * Math.PI * 2;
                  return <line key={j} x1={x + Math.cos(a) * 10 * u} y1={y + Math.sin(a) * 10 * u} x2={x + Math.cos(a) * (14 + 26 * u)} y2={y + Math.sin(a) * (14 + 26 * u)} stroke={C.accent} strokeWidth={3} strokeLinecap="round" />;
                })}
              </g>
            );
          })
        : null}
      {clockOn > 0 ? (
        <g opacity={clockOn}>
          <rect x={1440} y={120} width={400} height={190} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
          <text x={1470} y={166} style={{...label, fontSize: 24}} fill={C.ink}>Oct 26, 1825 · gun to gun</text>
          <text x={1490} y={262} style={{fontFamily: F.title, fontSize: 92, fontWeight: 600}} fill={C.accent}>{rf > 0 ? clock(rf) : '10:00'}</text>
          <text x={1730} y={262} style={{...label, fontSize: 28, fontWeight: 700}} fill={C.ink}>a.m.</text>
          <text x={1490} y={296} style={{...label, fontSize: 22}} fill={C.ink}>{rf >= 1 ? 'Sandy Hook: 11:21' : rf >= NYC_AT - 0.001 ? 'New York: 11:19' : rf > 0 ? 'signal on its way' : 'Buffalo'}</text>
        </g>
      ) : null}
      {dayOn > 0 ? (
        <g opacity={dayOn}>
          <rect x={1460} y={120} width={380} height={190} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
          <text x={1490} y={166} style={{...label, fontSize: 24}} fill={C.ink}>Oct 26 → Nov 4, 1825</text>
          <text x={1490} y={248} style={{fontFamily: F.title, fontSize: 92, fontWeight: 600}} fill={C.accent}>Day {day}</text>
          <text x={1490} y={296} style={{...label, fontSize: 22}} fill={C.ink}>{bf >= NYC_AT - 0.001 ? 'New York, November 4' : onHudson ? 'towed by a steamboat' : 'at the pace of a walking horse'}</text>
        </g>
      ) : null}
    </>
  );
};

const Opened: Ins = {
  from: S.opened.voice - 0.4, to: S.opened.end + 0.2, at: BUFFALO, render: (_t, d) => (
    <PicPage src="assets/nypl-buffalo-harbour-1825-3200.jpg" w={3200} h={2296} origin="40% 60%" drift={d} at={BUFFALO}
      s={{kicker: 'Buffalo, October 26, 1825', head: 'Open from end to end', tag: 'drawn for the celebration', credit: 'Buffalo Harbour from the Village. George Catlin, 1825, for Colden’s Memoir of the celebration.', plaque: 'NYPL · Public domain'}} />
  ),
};

export const PART4: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  inserts: [Opened],
  under,
  over,
  top: chapterTitle(4, 'Ten Days in 1825', S.opened.start, END),
};

````

## probe/src/ch5.tsx

````tsx
// Chapter 5, "The Flood", on the map: New York already first in 1810 by city limits, traffic both ways, cities
// along the line, New York 1820–1860, historians' dispute, rivals over the mountains.
// Own-drawing and picture inserts (rates, tolls, South Street): src/pages-b.tsx.
import React from 'react';
import {C, F} from './theme';
import {S, lineWith} from './narration';
import {hudson} from './erie';
import {
  ALBANY, ATACK, BALTIMORE, BUFFALO, Ctx, G, Lbl, LonLat, Move, NYC, Note, P, PHILADELPHIA, PITTSBURGH, Part, ROCHESTER, View,
  WHEELING, YearKey, chapterTitle, cut, label, line, mkLine, ramp, scr, smooth, win,
} from './kit';

const V: Record<string, View> = {
  twoCities: {c: [-74.62, 40.3], k: 9.5},
  state: {c: [-75.8, 42.0], k: 3.6},
  west: {c: [-79.4, 41.9], k: 2.1},
  upstate: {c: [-78.2, 43.0], k: 8},
  city: {c: [-73.98, 40.7], k: 16},
  continent: {c: [-80.5, 41.6], k: 1.3},
  rivals: {c: [-77.6, 40.9], k: 2.7},
};
const MOVES: Move[] = [
  {at: S.twist.start, dur: 3, v: V.twoCities},
  {at: S.twist.end - 2.6, dur: 2.6, v: V.state},
  {at: S.traffic.start, dur: 2.5, v: V.west},
  {at: S.cities.start, dur: 2.5, v: V.upstate},
  {at: S.growth.start, dur: 2.5, v: V.city},
  {at: S.argue.start, dur: 3, v: V.continent},
  {at: S.rivals2.start, dur: 2.5, v: V.rivals},
];
const YEARS: YearKey[] = [
  {at: S.twist.start, dur: 1.5, y: 1810},
  {at: S.cheaper.start, dur: 1.5, y: 1825},
  {at: line('traffic', 3).from, dur: 1, y: 1820},
  {at: line('traffic', 4).from, dur: 1, y: 1827},
  {at: S.tolls.start, dur: 1, y: 1833},
  {at: line('cities', 1).from, dur: 1, y: 1830},
  {at: line('cities', 2).from, dur: 3, y: 1860},
  {at: line('growth', 1).from, dur: 1, y: 1820},
  {at: line('growth', 2).from, dur: 2.5, y: 1860},
  {at: S.reasons.start, dur: 1, y: 1818},
  {at: S.argue.start, dur: 1.5, y: 1860},
];
const END = S.railroads.start + 1.2;

// Water path from Buffalo to New York, for flows.
export const PATH = mkLine([...[...ATACK.pts].reverse(), ...hudson.slice(1).map((q) => P(q))]);
// Lake Erie shipping from the Ohio shore to Buffalo, generalized.
const LAKE = smooth([[-83.4, 41.68], [-82.4, 41.62], [-81.7, 41.55], [-80.8, 41.95], [-79.9, 42.2], BUFFALO], 6);
// The Great Lakes to Buffalo, generalized: Lake Michigan, Lake Huron, the Detroit River, Lake Erie.
export const LAKES_ROAD = smooth([[-87.6, 41.9], [-86.9, 43.6], [-85.6, 45.6], [-84.4, 45.9], [-82.6, 44.6], [-82.4, 43.0], [-83.1, 42.3], [-82.4, 41.7], [-80.8, 41.95], [-79.9, 42.2], BUFFALO], 6);
// Rival routes over the mountains, schematic.
const PENN = smooth([PHILADELPHIA, [-76.88, 40.27], [-77.6, 40.55], [-78.4, 40.45], [-79.2, 40.45], PITTSBURGH], 8);
const BALT = smooth([BALTIMORE, [-77.4, 39.45], [-78.2, 39.62], [-78.76, 39.65], [-79.7, 39.75], WHEELING], 8);

const LABELS: Lbl[] = [
  {text: 'New York', at: NYC, from: S.twist.start + 1, to: S.cheaper.start + 1, dx: 0, dy: -110, anchor: 'middle', size: 30, bold: true},
  {text: 'Philadelphia', at: PHILADELPHIA, from: S.twist.start + 1.4, to: S.cheaper.start + 1, dx: 0, dy: -130, anchor: 'middle', size: 30, bold: true},
  {text: 'Buffalo', at: BUFFALO, from: S.traffic.start + 1, to: S.argue.start, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'New York', at: NYC, from: S.traffic.start + 1, to: S.cities.start + 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Albany', at: ALBANY, from: S.traffic.start + 1, to: S.cities.start + 1, dx: 16, dy: 30, dot: true},
  {text: 'Ohio', at: [-82.6, 40.4], from: line('traffic', 1).from + 2, to: S.cities.start + 1, size: 36, spacing: '0.4em', anchor: 'middle', color: '#9C8456', bold: true},
  {text: 'Lake Erie', at: [-81.2, 42.2], from: line('traffic', 1).from + 2, to: S.cities.start + 1, size: 28, color: C.force, italic: true, rotate: -24, spacing: '0.28em', anchor: 'middle'},
  {text: 'Rochester', at: ROCHESTER, from: S.cities.start + 0.8, to: S.growth.start + 1, dx: 0, dy: 44, anchor: 'middle', dot: true, bold: true},
  {text: 'Lake Ontario', at: [-77.9, 43.5], from: S.cities.start + 1, to: S.growth.start + 1, size: 30, color: C.force, italic: true, spacing: '0.28em', anchor: 'middle'},
  {text: 'Philadelphia', at: PHILADELPHIA, from: S.rivals2.start + 1, to: END, dx: 16, dy: 10, dot: true, bold: true},
  {text: 'Baltimore', at: BALTIMORE, from: S.rivals2.start + 1.3, to: END, dx: 16, dy: 12, dot: true, bold: true},
  {text: 'Pittsburgh', at: PITTSBURGH, from: line('rivals2', 0).from + 2, to: END, dx: -16, dy: -12, anchor: 'end', dot: true},
  {text: 'Ohio River', at: WHEELING, from: line('rivals2', 0).from + 2.4, to: END, dx: -16, dy: 14, anchor: 'end', size: 26, color: C.force, italic: true},
  {text: 'New York', at: NYC, from: S.rivals2.start + 1, to: END, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Appalachians', at: [-79.2, 39.4], from: line('rivals2', 1).from, to: END, size: 32, color: '#9C8456', rotate: -38, spacing: '0.5em', anchor: 'middle', bold: true},
];

const NOTES: Note[] = [
  {from: S.twist.start, to: S.cheaper.start, text: 'Circle area ~ population · census 1810 (Gibson, Census Bureau, 1998) · hatching: depends on how you count'},
  {from: S.traffic.start, to: S.tolls.start, text: 'Flows generalized · flour exports: Koeppel, Encyclopedia of New York City · canal line J. Atack (2015)'},
  {from: S.cities.start, to: S.reasons.start, text: 'Circle area ~ population · census 1830 and 1860 (Gibson, Census Bureau, 1998)'},
  {from: S.argue.start, to: S.rivals2.start, text: 'Hatching: disputed · lake route generalized · Natural Earth'},
  {from: S.rivals2.start, to: END, text: 'Dashed: rival routes over the mountains, schematic · Natural Earth, NOAA ETOPO 2022'},
];

const fmt = (n: number) => Math.round(n).toLocaleString('en-US');
const R = (pop: number, k: number) => Math.sqrt(pop) * 0.29 * (k / 9.5);

const Hatch = () => (
  <defs>
    <pattern id="hatch5" width={12} height={12} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1={0} y1={0} x2={0} y2={12} stroke={C.ink} strokeWidth={2.5} />
    </pattern>
  </defs>
);

const under = ({t}: Ctx) => {
  const on = win(t, S.twist.start, END, 0.8);
  const water = win(t, lineWith('argue', 'water road').from, S.rivals2.start + 0.5, 0.6);
  const lakes = cut(LAKES_ROAD, ramp(t, lineWith('argue', 'water road').from, lineWith('argue', 'water road').to));
  const penn = cut(PENN, ramp(t, line('rivals2', 0).from, line('rivals2', 1).to));
  const balt = cut(BALT, ramp(t, line('rivals2', 0).from + 0.6, line('rivals2', 1).to + 0.6));
  const rivalsOn = win(t, line('rivals2', 0).from, END, 0.5);
  const around = win(t, line('rivals2', 2).from, END, 0.5);
  const lake = cut(LAKE, ramp(t, line('traffic', 1).from + 1, line('traffic', 1).to));
  const lakeOn = win(t, line('traffic', 1).from + 1, S.cities.start, 0.5);
  return (
    <>
      <g opacity={on}>
        <path d={cut(ATACK, 1).d} fill="none" stroke={C.accent} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
        <path d={cut(PATH, 1).d} fill="none" stroke={C.accent} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" strokeOpacity={0.22 * Math.max(water, around)} vectorEffect="non-scaling-stroke" />
      </g>
      <path d={lake.d} fill="none" stroke={C.accent} strokeWidth={4} strokeDasharray="12 9" strokeDashoffset={-t * 30} strokeLinecap="round" opacity={lakeOn} vectorEffect="non-scaling-stroke" />
      <path d={lakes.d} fill="none" stroke={C.accent} strokeWidth={5} strokeDasharray="14 9" strokeDashoffset={-t * 36} strokeLinecap="round" opacity={water} vectorEffect="non-scaling-stroke" />
      {/* relief darkens under the rival routes */}
      {G.relief.map((d, i) => <path key={i} d={d} fill="#CDB68C" fillOpacity={0.3 * win(t, line('rivals2', 1).from, END, 0.8)} />)}
      <g opacity={rivalsOn}>
        <path d={penn.d} fill="none" stroke={C.ink} strokeWidth={4.5} strokeDasharray="12 9" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
        <path d={balt.d} fill="none" stroke={C.ink} strokeWidth={4.5} strokeDasharray="12 9" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </g>
    </>
  );
};

const over = ({t, at, cam}: Ctx) => {
  const k = cam.k;
  const ny = scr(NYC, cam);
  const ph = scr(PHILADELPHIA, cam);
  // 1810: city limits, then Philadelphia's county.
  const c1 = win(t, line('twist', 1).from, S.cheaper.start + 0.3, 0.6);
  const nums = ramp(t, line('twist', 2).from, line('twist', 2).from + 2);
  const county = win(t, line('twist', 3).from, S.cheaper.start + 0.3, 0.6);
  const catchOn = win(t, line('twist', 6).from, S.cheaper.start + 0.3, 0.4);
  // Traffic: flour east, goods and settlers west, as moving dots on the water path.
  const flowOn = win(t, line('traffic', 1).from, S.cities.start + 0.3, 0.5);
  const westOn = win(t, line('traffic', 2).from, S.cities.start + 0.3, 0.5);
  const rankOn = win(t, line('traffic', 3).from, S.cities.start + 0.3, 0.5);
  const rank = t < line('traffic', 4).from ? 3 : t < line('traffic', 4).from + 0.6 ? 2 : 1;
  const dots = (dir: 1 | -1, color: string, o: number, side: number) =>
    o > 0
      ? Array.from({length: 18}, (_, i) => {
          const f = (((dir > 0 ? t * 0.035 : -t * 0.035) + i / 18) % 1 + 1) % 1;
          const c = cut(PATH, f);
          const [x, y] = at(c.head);
          const n = Math.hypot(c.dir[0], c.dir[1]) || 1;
          return <circle key={i} cx={x - (c.dir[1] / n) * side} cy={y + (c.dir[0] / n) * side} r={6} fill={color} stroke={C.land} strokeWidth={1.5} opacity={o} />;
        })
      : null;
  // Cities on the line, 1830 to 1860.
  const cityOn = win(t, S.cities.voice, S.growth.start + 0.4, 0.5);
  const g = ramp(t, line('cities', 2).from, line('cities', 2).to - 0.3);
  const roc = 9207 + (48204 - 9207) * g;
  const buf = 8668 + (81129 - 8668) * g;
  // New York 1820 to 1860, Brooklyn apart.
  const nyOn = win(t, line('growth', 1).from, S.reasons.start + 0.3, 0.5);
  const ng = ramp(t, line('growth', 2).from, line('growth', 2).to + 0.6);
  const nyPop = 123706 + (813669 - 123706) * ng;
  const bk = win(t, line('growth', 2).to, S.reasons.start + 0.3, 0.5);
  const card = (x: number, y: number, w: number, lines: [string, string][], o: number) => (
    <g opacity={o}>
      <rect x={x} y={y} width={w} height={34 + 46 * lines.length} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
      {lines.map(([a, b], i) => (
        <g key={i}>
          <text x={x + 24} y={y + 58 + 46 * i} style={{...label, fontSize: 26}} fill={C.ink}>{a}</text>
          <text x={x + w - 24} y={y + 58 + 46 * i} textAnchor="end" style={{fontFamily: F.title, fontSize: 36, fontWeight: 600}} fill={C.accent}>{b}</text>
        </g>
      ))}
    </g>
  );
  const disputed = win(t, S.argue.voice, line('argue', 1).from + 1, 0.6);
  return (
    <>
      <Hatch />
      {c1 > 0 ? (
        <g opacity={c1}>
          <circle cx={ph[0]} cy={ph[1]} r={R(111210, k) * county} fill="url(#hatch5)" stroke={C.ink} strokeWidth={2} opacity={county} />
          <circle cx={ny[0]} cy={ny[1]} r={R(96373, k) * ramp(t, line('twist', 1).from, line('twist', 1).from + 1)} fill={C.accent} fillOpacity={0.75} stroke={C.ink} strokeWidth={2} />
          <circle cx={ph[0]} cy={ph[1]} r={R(53722, k) * ramp(t, line('twist', 1).from + 0.3, line('twist', 1).from + 1.3)} fill={C.ink} fillOpacity={0.6} stroke={C.ink} strokeWidth={2} />
          <text x={ny[0]} y={ny[1] + R(96373, k) + 44} textAnchor="middle" style={{fontFamily: F.title, fontSize: 40, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={8} fill={C.accent} opacity={nums}>{fmt(96373 * nums)}</text>
          <text x={ph[0]} y={ph[1] + R(111210, k) * Math.max(county, 0.6) + 44} textAnchor="middle" style={{fontFamily: F.title, fontSize: 40, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={8} fill={C.ink} opacity={nums}>{fmt(53722 * nums)}</text>
          <text x={ph[0]} y={ph[1] + R(111210, k) * Math.max(county, 0.6) + 80} textAnchor="middle" style={{...label, fontSize: 24, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={6} fill={C.ink} opacity={county}>county: 111,210</text>
          <text x={ny[0]} y={ny[1] + R(96373, k) + 78} textAnchor="middle" style={{...label, fontSize: 24, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={6} fill={C.ink} opacity={nums}>city limits, 1810</text>
          <text x={(ny[0] + ph[0]) / 2} y={Math.min(ny[1], ph[1]) - 190} textAnchor="middle" style={{fontFamily: F.title, fontSize: 64, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={10} fill={C.accent} opacity={catchOn}>Impossible to catch</text>
        </g>
      ) : null}
      {dots(1, C.accent, flowOn, 9)}
      {dots(-1, C.ink, westOn, -9)}
      {flowOn > 0 ? (() => {
        const [x, y] = at(cut(PATH, 0.35).head);
        return (
          <g opacity={flowOn}>
            <text x={x} y={y - 34} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.accent}>wheat and flour → east</text>
            <text x={x} y={y + 52} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink} opacity={westOn}>← goods and settlers west</text>
          </g>
        );
      })() : null}
      {rankOn > 0 ? card(1380, 130, 460, [['Flour exports, 1820', '3rd'], ['New York, 1827', rank === 1 ? '1st' : rank === 2 ? '2nd' : '3rd']], rankOn) : null}
      {cityOn > 0 ? (
        <g opacity={cityOn}>
          {[[ROCHESTER, roc], [BUFFALO, buf]].map(([q, pop], i) => {
            const [x, y] = scr(q as LonLat, cam);
            return (
              <g key={i}>
                <circle cx={x} cy={y} r={Math.sqrt(pop as number) * 0.29 * (k / 9.5) * 1.6} fill={C.accent} fillOpacity={0.7} stroke={C.ink} strokeWidth={2} />
                <text x={x} y={y - Math.sqrt(pop as number) * 0.29 * (k / 9.5) * 1.6 - 16} textAnchor="middle" style={{fontFamily: F.title, fontSize: 38, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={8} fill={C.accent}>{fmt(pop as number)}</text>
              </g>
            );
          })}
          <text x={scr(ROCHESTER, cam)[0]} y={scr(ROCHESTER, cam)[1] + 84} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink} opacity={win(t, line('cities', 1).from + 1.5, S.growth.start, 0.4)}>“the Flour City”</text>
          <text x={scr(BUFFALO, cam)[0]} y={scr(BUFFALO, cam)[1] + Math.sqrt(81129) * 0.29 * (k / 9.5) * 1.6 + 44} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink} opacity={win(t, line('cities', 2).from + 1, S.growth.start, 0.4)}>Buffalo · lake port</text>
          {card(1380, 130, 460, [['Census', g <= 0 ? '1830' : g >= 1 ? '1860' : '1830 → 1860']], cityOn)}
        </g>
      ) : null}
      {nyOn > 0 ? (
        <g opacity={nyOn}>
          <circle cx={ny[0]} cy={ny[1]} r={Math.sqrt(nyPop) * 0.29 * (k / 9.5) * 0.42} fill={C.accent} fillOpacity={0.72} stroke={C.ink} strokeWidth={2} />
          <text x={ny[0]} y={ny[1] + 12} textAnchor="middle" style={{fontFamily: F.title, fontSize: 56, fontWeight: 600, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={9} fill={C.ink}>{fmt(nyPop)}</text>
          <text x={ny[0]} y={ny[1] + 52} textAnchor="middle" style={{...label, fontSize: 26, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink}>New York City, {ng <= 0 ? '1820' : ng >= 1 ? '1860' : '1820 → 1860'}</text>
          <g opacity={bk}>
            <text x={ny[0] + 250} y={ny[1] + 230} textAnchor="middle" style={{...label, fontSize: 26, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} fill={C.ink}>Brooklyn, a separate city: 266,661</text>
          </g>
        </g>
      ) : null}
      {disputed > 0 ? (
        <g opacity={disputed}>
          <rect x={1260} y={120} width={580} height={250} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
          <rect x={1260} y={120} width={22} height={250} fill="url(#hatch5)" />
          <text x={1306} y={166} style={{...label, fontSize: 24}} fill={C.ink}>Historians disagree</text>
          <text x={1306} y={222} style={{fontFamily: F.title, fontSize: 32}} fill={C.ink}>Burrows and Wallace:</text>
          <text x={1306} y={258} style={{fontFamily: F.label, fontSize: 28}} fill={C.ink}>the canal, above all</text>
          <text x={1306} y={306} style={{fontFamily: F.title, fontSize: 32}} fill={C.ink}>Glaeser:</text>
          <text x={1306} y={342} style={{fontFamily: F.label, fontSize: 28}} fill={C.ink}>it made old advantages stronger</text>
        </g>
      ) : null}
    </>
  );
};

export const PART5: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  under,
  over,
  top: chapterTitle(5, 'The Flood', S.twist.start, END),
};
````

## probe/src/ch6.tsx

````tsx
// Chapter 6, "The Same Gap", on the map: the 1836 enlargement, rail and highway in the same corridor, the 1853
// merger, today's canal, the gap from chapter 1 again. Then the silent end card.
import React from 'react';
import {C, F} from './theme';
import {S, TOTAL, lineWith} from './narration';
import {
  ALBANY, ATACK, BUFFALO, Ctx, Lbl, LonLat, Move, NYC, Note, Part, Ripples, View, XY, YearKey,
  chapterTitle, cut, fracAt, label, line, mkLine, ramp, segment, title, win,
} from './kit';
import {V as V1} from './Pilot';
import {LAKES_ROAD, PATH} from './ch5';

// Seconds of the silent end card after the last line.
export const END_CARD = 20;

const WATERFORD: LonLat = [-73.684, 42.79];
const V: Record<string, View> = {
  corridor: {c: [-76.3, 41.85], k: 4},
  end: {c: [-71.5, 41.6], k: 1.5},
};
const MOVES: Move[] = [
  {at: S.railroads.start, dur: 2.5, v: V.corridor},
  {at: S.gapnow.start, dur: 4, v: V1.east},
  {at: TOTAL, dur: 3, v: V.end},
];
const YEARS: YearKey[] = [
  {at: line('railroads', 1).from, dur: 1.5, y: 1836},
  {at: line('railroads', 3).from, dur: 1.5, y: 1853},
  {at: S.today.start, dur: 2, y: 2026},
];

// Rail and highway: the canal-and-Hudson path from New York, set off to either side (base px). Generalized.
const offset = (l: typeof PATH, d: number) => {
  const p = l.pts;
  const w = 4;
  return mkLine(p.map(([x, y], i) => {
    const [ax, ay] = p[Math.max(0, i - w)];
    const [bx, by] = p[Math.min(p.length - 1, i + w)];
    const n = Math.hypot(bx - ax, by - ay) || 1;
    return [x - ((by - ay) / n) * d, y + ((bx - ax) / n) * d] as XY;
  }));
};
const FROM_NYC = mkLine([...PATH.pts].reverse());
const RAIL = offset(FROM_NYC, 3.4);
const ROAD = offset(FROM_NYC, -3.4);
const RAIL_ALBANY = fracAt(RAIL, ALBANY);
// Ten pieces between Albany and Buffalo: equal lengths, schematic, not the companies' real ends.
const PIECES = Array.from({length: 10}, (_, i) => [RAIL_ALBANY + ((1 - RAIL_ALBANY) * i) / 10, RAIL_ALBANY + ((1 - RAIL_ALBANY) * (i + 1)) / 10]);
const WATER = mkLine([...LAKES_ROAD.pts, ...PATH.pts]);

const LABELS: Lbl[] = [
  {text: 'New York', at: NYC, from: S.railroads.start + 1, to: TOTAL + 1, dx: 18, dy: 10, dot: true, bold: true},
  {text: 'Albany', at: ALBANY, from: S.railroads.start + 1, to: S.gapnow.start + 1, dx: 16, dy: 30, dot: true},
  {text: 'Buffalo', at: BUFFALO, from: S.railroads.start + 1, to: S.gapnow.start + 1, dx: -18, dy: 10, anchor: 'end', dot: true},
  {text: 'Waterford', at: WATERFORD, from: line('today', 1).from, to: S.gapnow.start + 1, dx: 18, dy: 4, dot: true},
  {text: 'Adirondacks', at: [-74.4, 43.95], from: S.gapnow.voice, to: TOTAL, size: 24, color: '#9C8456', spacing: '0.4em', anchor: 'middle', bold: true},
  {text: 'Appalachians', at: [-79.6, 39.4], from: S.gapnow.voice + 0.6, to: TOTAL, size: 26, color: '#9C8456', spacing: '0.4em', rotate: -42, anchor: 'middle', bold: true},
];

const NOTES: Note[] = [
  {from: S.railroads.start, to: S.today.start, text: 'Rail and highway routes generalized · ten equal pieces schematic · enlargement: Whitford, 1906 · canal line J. Atack (2015)'},
  {from: S.today.start, to: S.gapnow.start, text: 'Today’s canal: New York State Canal Corporation · 1825 line J. Atack (2015)'},
  {from: S.gapnow.start, to: TOTAL, text: 'Census 2020 · Natural Earth, NOAA ETOPO 2022 · canal line J. Atack (2015)'},
];

const under = ({t}: Ctx) => {
  const on = win(t, S.railroads.start, TOTAL + END_CARD + 1, 0.8);
  const wide = ramp(t, line('railroads', 1).from, line('railroads', 1).from + 1.5);
  const rail = ramp(t, lineWith('railroads', 'Railroads').from + 0.5, line('railroads', 2).to);
  const merge = ramp(t, lineWith('railroads', 'merged').from, lineWith('railroads', 'merged').to);
  const road = ramp(t, line('railroads', 4).from, line('railroads', 4).to + 0.6);
  const corridor = win(t, S.railroads.voice, S.gapnow.start + 1, 0.6);
  const old = ramp(t, S.today.voice, S.today.voice + 1.2) * (1 - ramp(t, S.gapnow.start, S.gapnow.start + 1.5));
  const glow = win(t, S.gapnow.voice, TOTAL + END_CARD + 1, 0.8);
  const ditch = win(t, lineWith('gapnow', 'ditch').from, lineWith('gapnow', 'ditch').to + 0.6, 0.4);
  const gap = 0.0035 * (1 - merge);
  return (
    <g opacity={on}>
      <path d={cut(PATH, 1).d} fill="none" stroke={C.accent} strokeWidth={26} strokeLinecap="round" strokeLinejoin="round" strokeOpacity={0.22 * glow} vectorEffect="non-scaling-stroke" />
      <path d={cut(ATACK, 1).d} fill="none" stroke={C.accent} strokeWidth={6 + 4 * wide + 6 * ditch} strokeDasharray={old > 0.5 ? '10 8' : undefined} strokeOpacity={1 - 0.45 * old} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
      <g opacity={corridor}>
        {road > 0 ? <path d={cut(ROAD, road).d} fill="none" stroke="#8E8A80" strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" vectorEffect="non-scaling-stroke" /> : null}
        {rail > 0 ? (
          <g>
            <path d={segment(RAIL, 0, Math.min(rail, RAIL_ALBANY))} fill="none" stroke={C.ink} strokeWidth={3} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
            <path d={segment(RAIL, 0, Math.min(rail, RAIL_ALBANY))} fill="none" stroke={C.ink} strokeWidth={11} strokeDasharray="2 9" vectorEffect="non-scaling-stroke" />
            {PIECES.map(([a, b], i) => (rail > a ? (
              <g key={i}>
                <path d={segment(RAIL, a + gap, Math.min(rail, b) - gap)} fill="none" stroke={merge > 0.5 ? C.ink : i % 2 ? '#5B4A3A' : C.ink} strokeWidth={3 + 2 * merge} strokeLinecap="round" vectorEffect="non-scaling-stroke" />
                <path d={segment(RAIL, a + gap, Math.min(rail, b) - gap)} fill="none" stroke={C.ink} strokeWidth={11} strokeDasharray="2 9" vectorEffect="non-scaling-stroke" />
              </g>
            ) : null))}
          </g>
        ) : null}
      </g>
    </g>
  );
};

const over = ({t, at}: Ctx) => {
  const card = (x: number, y: number, w: number, rows: [string, string][], o: number) => (
    <g opacity={o}>
      <rect x={x} y={y} width={w} height={34 + 46 * rows.length} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
      {rows.map(([a, b], i) => (
        <g key={i}>
          <text x={x + 24} y={y + 58 + 46 * i} style={{...label, fontSize: 26}} fill={C.ink}>{a}</text>
          <text x={x + w - 24} y={y + 58 + 46 * i} textAnchor="end" style={{fontFamily: F.title, fontSize: 34, fontWeight: 600}} fill={C.accent}>{b}</text>
        </g>
      ))}
    </g>
  );
  const wideOn = win(t, line('railroads', 1).from, lineWith('railroads', 'Railroads').from + 0.4, 0.5);
  const nycOn = win(t, line('railroads', 3).from, line('railroads', 4).from + 0.4, 0.5);
  const merge = ramp(t, lineWith('railroads', 'merged').from, lineWith('railroads', 'merged').to);
  const routesOn = win(t, line('railroads', 4).from + 0.6, S.today.start + 0.4, 0.5);
  const oldOn = win(t, S.today.voice + 0.6, line('today', 1).from + 0.3, 0.5);
  const todayOn = win(t, line('today', 1).from, S.gapnow.start + 0.6, 0.5);
  // Legend for the three lines in the corridor.
  const legend = (
    <g opacity={routesOn}>
      <rect x={1380} y={130} width={460} height={172} fill={C.paper} stroke={C.ink} strokeWidth={1.5} />
      {[['canal', C.accent, 10], ['railroad', C.ink, 3], ['highway', '#8E8A80', 6]].map(([n, c, w], i) => (
        <g key={i}>
          <line x1={1408} x2={1478} y1={176 + 46 * i} y2={176 + 46 * i} stroke={c as string} strokeWidth={w as number} strokeLinecap="round" />
          {n === 'railroad' ? <line x1={1408} x2={1478} y1={176 + 46 * i} y2={176 + 46 * i} stroke={C.ink} strokeWidth={11} strokeDasharray="2 9" /> : null}
          <text x={1500} y={185 + 46 * i} style={{...label, fontSize: 26}} fill={C.ink}>{n as string}</text>
        </g>
      ))}
    </g>
  );
  // The gap now: New York pulses at the mouth, water flows from the lakes to it.
  const ny = at(cut(PATH, 1).head);
  const nyPulse = win(t, line('gapnow', 1).from, TOTAL, 0.6);
  const flow = win(t, lineWith('gapnow', 'water').from - 0.4, TOTAL + 2, 0.6);
  const dots = flow > 0
    ? Array.from({length: 26}, (_, i) => {
        const f = ((t * 0.03 + i / 26) % 1 + 1) % 1;
        const [x, y] = at(cut(WATER, f).head);
        return <circle key={i} cx={x} cy={y} r={5} fill={C.accent} stroke={C.land} strokeWidth={1.5} opacity={flow} />;
      })
    : null;
  const ditchOn = win(t, lineWith('gapnow', 'ditch').from, line('gapnow', 3).from + 0.4, 0.4);
  const [dx, dy] = at(cut(ATACK, 0.55).head);
  const largest = win(t, line('gapnow', 1).from + 0.8, line('gapnow', 2).from + 0.3, 0.5);
  return (
    <>
      {wideOn > 0 ? card(1380, 130, 460, [['Enlargement begins', '1836'], ['Depth', '4 → 7 ft']], wideOn) : null}
      {nycOn > 0 ? card(1380, 130, 460, [['Lines Albany–Buffalo', merge > 0.5 ? '1' : '10'], ['New York Central', '1853']], nycOn) : null}
      {legend}
      {oldOn > 0 ? card(1380, 130, 460, [['Clinton’s ditch, 1825', ''], ['widened · moved · rebuilt', '']], oldOn) : null}
      {todayOn > 0 ? card(1380, 130, 460, [['Erie Canal today', '338 mi'], ['Waterford → Lake Erie', '']], todayOn) : null}
      {dots}
      {nyPulse > 0 ? Ripples(ny, t, nyPulse, C.accent, 50) : null}
      {largest > 0 ? (
        <text x={ny[0] + 24} y={ny[1] + 48} style={{...label, fontSize: 26, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.ink} opacity={largest}>largest U.S. city · census 2020</text>
      ) : null}
      {ditchOn > 0 ? (
        <text x={dx} y={dy + 48} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700, paintOrder: 'stroke'}} stroke={C.land} strokeWidth={7} strokeLinejoin="round" fill={C.accent} opacity={ditchOn}>4 feet deep</text>
      ) : null}
    </>
  );
};

// End card: the whole line on the map, title and credits on the left, the right side kept calm for end-screen elements.
const endCard = (t: number) => {
  const o = ramp(t, TOTAL + 0.5, TOTAL + 2.5);
  if (o <= 0) return null;
  return (
    <>
      {/* the ruler gives way to the credits */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 116, background: C.paper, opacity: o}} />
      <div style={{position: 'absolute', right: 0, top: 0, bottom: 0, width: 760, background: C.paper, opacity: 0.86 * o, borderLeft: `1.5px solid ${C.rule}`}} />
      <div style={{position: 'absolute', left: 110, top: 92, opacity: o}}>
        <div style={{...label, fontSize: 28, color: C.accent, fontWeight: 700}}>The Layered Map</div>
        <div style={{...title, fontSize: 76, marginTop: 8, width: 980}}>Clinton’s Ditch</div>
        <div style={{fontFamily: F.title, fontSize: 38, marginTop: 6, color: C.ink}}>How a Canal Made New York</div>
      </div>
      <div style={{position: 'absolute', left: 110, bottom: 36, width: 1000, opacity: o * ramp(t, TOTAL + 2, TOTAL + 3.5), fontFamily: F.label, fontSize: 24, lineHeight: 1.4, color: C.ink}}>
        <div>Map: Natural Earth · NOAA ETOPO 2022 · Erie Canal line: J. Atack (2015)</div>
        <div>Pictures: The Metropolitan Museum of Art · The New York Public Library · Wikimedia Commons · public domain</div>
        <div>Sources for every fact: in the description</div>
      </div>
    </>
  );
};

export const PART6: Part = {
  moves: MOVES,
  labels: LABELS,
  years: YEARS,
  notes: NOTES,
  relief: (t) => 0.3 * win(t, S.gapnow.voice, TOTAL + 2, 1),
  under,
  over,
  top: (t) => (
    <>
      {chapterTitle(6, 'The Same Gap', S.railroads.start, TOTAL)(t)}
      {endCard(t)}
    </>
  ),
};
````

## probe/src/erie.ts

````ts
// Probe data for "Clinton's Ditch". Town coordinates are approximate town
// centres; the 1825 line between them is simplified, and the frame says so.
// Full check against a gazetteer goes into the episode fact sheet.
export type LonLat = [number, number];

// 1825 canal, east to west: Hudson at Albany, up to Cohoes, Mohawk valley,
// across the state to the Niagara River and Buffalo.
export const canal: LonLat[] = [
  [-73.755, 42.651], // Albany
  [-73.701, 42.73], // Watervliet
  [-73.7, 42.774], // Cohoes
  [-73.94, 42.814], // Schenectady
  [-74.188, 42.939], // Amsterdam
  [-74.374, 42.955], // Fonda
  [-74.86, 43.043], // Little Falls
  [-74.986, 43.026], // Herkimer
  [-75.233, 43.101], // Utica
  [-75.456, 43.213], // Rome
  [-75.751, 43.08], // Canastota
  [-75.866, 43.045], // Chittenango
  [-76.147, 43.048], // Syracuse
  [-76.473, 43.065], // Jordan
  [-76.624, 43.035], // Port Byron
  [-76.703, 43.01], // Montezuma
  [-76.869, 43.084], // Clyde
  [-76.99, 43.064], // Lyons
  [-77.095, 43.047], // Newark
  [-77.233, 43.064], // Palmyra
  [-77.515, 43.091], // Pittsford
  [-77.609, 43.157], // Rochester
  [-77.804, 43.186], // Spencerport
  [-77.939, 43.214], // Brockport
  [-78.194, 43.246], // Albion
  [-78.387, 43.22], // Medina
  [-78.69, 43.171], // Lockport
  [-78.77, 43.102], // Pendleton
  [-78.88, 43.02], // Tonawanda
  [-78.9, 42.935], // Black Rock
  [-78.878, 42.886], // Buffalo
];

// Hudson River, Albany down to the Battery.
export const hudson: LonLat[] = [
  [-73.755, 42.651],
  [-73.79, 42.25],
  [-73.96, 41.92],
  [-73.94, 41.7],
  [-74.01, 41.5],
  [-73.96, 41.39],
  [-73.93, 41.29],
  [-73.88, 41.07],
  [-73.9, 40.94],
  [-74.015, 40.704],
];

export const towns: {name: string; at: LonLat; dx?: number; dy?: number; anchor?: 'start' | 'end' | 'middle'}[] = [
  {name: 'ALBANY', at: [-73.755, 42.651], dx: 16, dy: 30, anchor: 'start'},
  {name: 'SCHENECTADY', at: [-73.94, 42.814], dx: 0, dy: -22, anchor: 'middle'},
  {name: 'UTICA', at: [-75.233, 43.101], dx: 0, dy: -22, anchor: 'middle'},
  {name: 'SYRACUSE', at: [-76.147, 43.048], dx: 0, dy: 38, anchor: 'middle'},
  {name: 'ROCHESTER', at: [-77.609, 43.157], dx: 0, dy: 38, anchor: 'middle'},
  {name: 'LOCKPORT', at: [-78.69, 43.171], dx: 0, dy: -26, anchor: 'middle'},
  {name: 'BUFFALO', at: [-78.878, 42.886], dx: -18, dy: 10, anchor: 'end'},
  {name: 'NEW YORK', at: [-74.015, 40.704], dx: 18, dy: 10, anchor: 'start'},
];

export const waters: {name: string; at: LonLat; size: number; rotate?: number; minZoom?: number}[] = [
  {name: 'LAKE ERIE', at: [-80.15, 42.3], size: 30, rotate: -30},
  {name: 'LAKE ONTARIO', at: [-77.6, 43.62], size: 30, rotate: -4},
  {name: 'HUDSON R.', at: [-73.6, 41.95], size: 22, rotate: -84},
  {name: 'MOHAWK R.', at: [-74.5, 42.78], size: 22, rotate: -8, minZoom: 1.6},
  {name: 'ATLANTIC OCEAN', at: [-72.6, 40.2], size: 26},
];

export const LOCKPORT: LonLat = [-78.69, 43.171];
````

## probe/src/index.ts

````ts
import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
````

## probe/src/kit.tsx

````tsx
// Shared kit for the episode: one map, one camera, labels, time ruler, inserts through a lens.
// Each part of the film (src/Pilot.tsx for the cold open and chapter 1, src/ch*.tsx for the rest)
// supplies its own camera moves, labels, years, notes, inserts and map overlays; makeFilm puts them together.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {geoConicConformal, geoPath} from 'd3-geo';
import east from '../public/region/east.json';
import erie from '../public/region/erie.json';
import atack from '../public/region/erie-canal-atack.json';
import {C, F, FPS, H, W, fontFiles} from './theme';
import {S} from './narration';

export type LonLat = [number, number];
export type XY = [number, number];

// Base projection: eastern North America fills the frame at zoom 1.
export const proj = geoConicConformal().parallels([33, 45]).rotate([80, 0]).fitExtent([[0, 0], [W, H]], {
  type: 'MultiPoint',
  coordinates: [[-92, 29], [-66, 29], [-66, 47], [-92, 47]],
} as any);
export const path = geoPath(proj);
export const P = (p: LonLat) => proj(p) as XY;
export const lines = (rs: {coords: number[][]}[]) => rs.map((r) => path({type: 'LineString', coordinates: r.coords} as any) ?? '').join('');

export const G = {
  land: path(east.land as any) ?? '',
  lakes: path(east.lakes as any) ?? '',
  rivers: lines(east.rivers),
  relief: east.relief.map((r) => path(r.geometry as any) ?? ''),
  reliefFine: erie.relief.map((r) => path(r.geometry as any) ?? ''),
  riversFine: lines(erie.rivers),
};

// Places. Town centres are approximate; the fact sheet lists the check.
export const SANDY: LonLat = [-74.0, 40.46];
export const NYC: LonLat = [-74.015, 40.704];
export const ALBANY: LonLat = [-73.755, 42.651];
export const TROY: LonLat = [-73.69, 42.73];
export const BUFFALO: LonLat = [-78.878, 42.886];
export const ROME: LonLat = [-75.456, 43.213];
export const WHEELING: LonLat = [-80.72, 40.064];
export const CUMBERLAND: LonLat = [-78.763, 39.653];
export const NEW_ORLEANS: LonLat = [-90.07, 29.95];
export const PITTSBURGH: LonLat = [-79.996, 40.44];
export const PHILADELPHIA: LonLat = [-75.16, 39.95];
export const CUMBERLAND_GAP: LonLat = [-83.67, 36.6];
export const UTICA: LonLat = [-75.233, 43.101];
export const SYRACUSE: LonLat = [-76.147, 43.048];
export const ROCHESTER: LonLat = [-77.611, 43.156];
export const LOCKPORT: LonLat = [-78.69, 43.17];
export const SCHENECTADY: LonLat = [-73.94, 42.814];
export const LITTLE_FALLS: LonLat = [-74.86, 43.043];
export const OSWEGO: LonLat = [-76.51, 43.455];
export const MONTREAL: LonLat = [-73.567, 45.5];
export const QUEBEC: LonLat = [-71.21, 46.81];
export const NIAGARA_FALLS: LonLat = [-79.075, 43.08];
export const MONTEZUMA: LonLat = [-76.7, 43.0];
export const BALTIMORE: LonLat = [-76.61, 39.29];
export const BOSTON: LonLat = [-71.06, 42.36];

// Polyline in base pixels with cumulative length, cut at a fraction of its length.
export type Line = {pts: XY[]; len: number[]; total: number};
export function mkLine(pts: XY[]): Line {
  const len = [0];
  for (let i = 1; i < pts.length; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  return {pts, len, total: len[len.length - 1]};
}
export function smooth(points: LonLat[], steps = 8): Line {
  const p = points.map(P);
  const out: XY[] = [];
  for (let i = 0; i < p.length - 1; i++) {
    const [a, b, c, d] = [p[Math.max(i - 1, 0)], p[i], p[i + 1], p[Math.min(i + 2, p.length - 1)]];
    for (let s = 0; s < steps; s++) {
      const t = s / steps;
      const f = (k: 0 | 1) => 0.5 * (2 * b[k] + (-a[k] + c[k]) * t + (2 * a[k] - 5 * b[k] + 4 * c[k] - d[k]) * t * t + (-a[k] + 3 * b[k] - 3 * c[k] + d[k]) * t * t * t);
      out.push([f(0), f(1)]);
    }
  }
  out.push(p[p.length - 1]);
  return mkLine(out);
}
export function cut(line: Line, frac: number) {
  const target = Math.max(0, Math.min(1, frac)) * line.total;
  const pts: XY[] = [line.pts[0]];
  let i = 1;
  while (i < line.pts.length && line.len[i] <= target) pts.push(line.pts[i++]);
  let head = pts[pts.length - 1];
  const n = line.pts.length;
  let dir: XY = [line.pts[n - 1][0] - line.pts[n - 2][0], line.pts[n - 1][1] - line.pts[n - 2][1]];
  if (i < line.pts.length) {
    const [a, b] = [line.pts[i - 1], line.pts[i]];
    const t = (target - line.len[i - 1]) / (line.len[i] - line.len[i - 1] || 1);
    head = [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
    pts.push(head);
    dir = [b[0] - a[0], b[1] - a[1]];
  }
  return {d: frac > 0 && pts.length > 1 ? 'M' + pts.map((q) => q.join(',')).join('L') : '', head, dir};
}
// Part of a polyline between two fractions of its length.
export function segment(line: Line, a: number, b: number) {
  const [lo, hi] = [Math.max(0, a), Math.min(1, b)];
  if (hi <= lo) return '';
  const pts: XY[] = [cut(line, lo).head];
  for (let i = 0; i < line.pts.length; i++) if (line.len[i] > lo * line.total && line.len[i] < hi * line.total) pts.push(line.pts[i]);
  pts.push(cut(line, hi).head);
  return 'M' + pts.map((q) => q.join(',')).join('L');
}
// The 1825 canal line as mapped by J. Atack (2015), chained from Albany to Buffalo, in base pixels.
export const ATACK: Line = (() => {
  let parts = (atack as any).features.flatMap((f: any) => f.geometry.coordinates) as LonLat[][];
  const out: LonLat[] = [];
  let at: LonLat = [-73.755, 42.651];
  const d = (a: LonLat, b: LonLat) => Math.hypot((a[0] - b[0]) * Math.cos((a[1] * Math.PI) / 180), a[1] - b[1]);
  while (parts.length) {
    let best = 0;
    let flip = false;
    let dist = Infinity;
    parts.forEach((p, i) => {
      if (d(at, p[0]) < dist) [dist, best, flip] = [d(at, p[0]), i, false];
      if (d(at, p[p.length - 1]) < dist) [dist, best, flip] = [d(at, p[p.length - 1]), i, true];
    });
    const p = flip ? [...parts[best]].reverse() : parts[best];
    out.push(...p);
    at = p[p.length - 1];
    parts = parts.filter((_, i) => i !== best);
  }
  return mkLine(out.map((c) => P(c)));
})();
// Fraction of a line's length nearest to a place.
export const fracAt = (l: Line, q: LonLat) => {
  const [x, y] = P(q);
  let best = 0;
  l.pts.forEach((p, i) => {
    if (Math.hypot(p[0] - x, p[1] - y) < Math.hypot(l.pts[best][0] - x, l.pts[best][1] - y)) best = i;
  });
  return l.len[best] / l.total;
};
export const nearest = (coords: number[][], q: LonLat) =>
  coords.reduce((best, c, i) => (Math.hypot(c[0] - q[0], c[1] - q[1]) < Math.hypot(coords[best][0] - q[0], coords[best][1] - q[1]) ? i : best), 0);

// Timing helpers, in seconds.
export const ease = Easing.inOut(Easing.cubic);
export const ramp = (t: number, a: number, b: number) => interpolate(t, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
export const win = (t: number, a: number, b: number, fade = 0.5) => ramp(t, a, a + fade) * (1 - ramp(t, b - fade, b));
export const line = (id: string, n: number) => S[id].lines[n];

// Camera: centre and zoom, moved by keyframes {at, dur}. The camera never rests: a slow drift and a
// slight zoom swell between moves.
export type View = {c: LonLat; k: number};
export type Move = {at: number; dur: number; v: View};
export const makeCamera = (start: View, moves: Move[]) => (t: number) => {
  let c = P(start.c);
  let k = start.k;
  for (const m of moves) {
    if (t <= m.at) break;
    const u = ramp(t, m.at, m.at + m.dur);
    const to = P(m.v.c);
    c = [c[0] + (to[0] - c[0]) * u, c[1] + (to[1] - c[1]) * u];
    k = Math.exp(Math.log(k) + (Math.log(m.v.k) - Math.log(k)) * u);
  }
  k *= 1 + 0.03 * Math.sin((t / 16) * Math.PI * 2);
  return {c: [c[0] + (22 * Math.sin(t / 7)) / k, c[1] + (14 * Math.cos(t / 9)) / k] as XY, k};
};
export type Cam = {c: XY; k: number};
export const scr = (p: LonLat, cam: Cam): XY => [(P(p)[0] - cam.c[0]) * cam.k + W / 2, (P(p)[1] - cam.c[1]) * cam.k + H / 2];

export const label: React.CSSProperties = {fontFamily: F.label, letterSpacing: '0.16em', textTransform: 'uppercase'};
export const title: React.CSSProperties = {fontFamily: F.title, color: C.ink, fontVariationSettings: '"opsz" 72, "SOFT" 50', lineHeight: 1.05};

// Labels in screen space, each with its time window.
export type Lbl = {text: string; at: LonLat; from: number; to: number; dx?: number; dy?: number; anchor?: 'start' | 'middle' | 'end'; size?: number; color?: string; italic?: boolean; rotate?: number; spacing?: string; dot?: boolean; bold?: boolean};
// Shapes drawn in screen space over the map.
export const Head = (p: XY, color: string) => (
  <g>
    <circle cx={p[0]} cy={p[1]} r={20} fill={color} opacity={0.22} />
    <circle cx={p[0]} cy={p[1]} r={8} fill={color} stroke={C.land} strokeWidth={2.5} />
  </g>
);
export const Arrow = (p: XY, dir: XY, color: string, o = 1) => (
  <path d="M-8,-12 L14,0 L-8,12 Z" transform={`translate(${p[0]},${p[1]}) rotate(${(Math.atan2(dir[1], dir[0]) * 180) / Math.PI})`} fill={color} opacity={o} />
);
export const Ripples = (p: XY, t: number, o: number, color: string, size = 60) =>
  o > 0
    ? [0, 1, 2].map((i) => {
        const u = (t / 1.6 + i / 3) % 1;
        return <circle key={i} cx={p[0]} cy={p[1]} r={10 + size * u} fill="none" stroke={color} strokeWidth={3} opacity={o * 0.7 * (1 - u)} />;
      })
    : null;
export const Flatboat = (p: XY, dir: XY, o = 1) => (
  <g transform={`translate(${p[0]},${p[1]}) rotate(${(Math.atan2(dir[1], dir[0]) * 180) / Math.PI})`} opacity={o}>
    <rect x={-13} y={-7} width={26} height={14} rx={2} fill={C.ink} />
    <rect x={-6} y={-4} width={10} height={8} fill={C.paper} />
  </g>
);
export const Wagon = (p: XY) => (
  <g transform={`translate(${p[0]},${p[1] - 16}) scale(1.4)`}>
    <path d="M-14,-3 Q0,-19 14,-3 Z" fill={C.paper} stroke={C.ink} strokeWidth={2.2} />
    <rect x={-15} y={-3} width={30} height={8} fill={C.ink} />
    <circle cx={-9} cy={7} r={4.5} fill={C.paper} stroke={C.ink} strokeWidth={2.2} />
    <circle cx={9} cy={7} r={4.5} fill={C.paper} stroke={C.ink} strokeWidth={2.2} />
  </g>
);
export function Labels(t: number, cam: Cam, labels: Lbl[]) {
  return labels.map((l, i) => {
    const o = win(t, l.from, l.to, 0.5);
    if (o <= 0) return null;
    const [x, y] = scr(l.at, cam);
    const tx = x + (l.dx ?? 0);
    const ty = y + (l.dy ?? 0);
    // Labels pop in; a place dot sends one ripple.
    const age = t - l.from;
    const pop = interpolate(age, [0, 0.45], [0.55, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.back(2.2))});
    const rip = Math.min(1, Math.max(0, age / 0.9));
    return (
      <g key={i} opacity={o}>
        {l.dot && rip < 1 ? <circle cx={x} cy={y} r={7 + 36 * rip} fill="none" stroke={l.bold ? C.accent : C.ink} strokeWidth={3} opacity={0.8 * (1 - rip)} /> : null}
        <g transform={`translate(${x},${y}) scale(${pop}) translate(${-x},${-y})`}>
          {l.dot ? <circle cx={x} cy={y} r={7} fill={l.bold ? C.accent : C.ink} stroke={C.land} strokeWidth={2.5} /> : null}
          <text x={tx} y={ty} textAnchor={l.anchor ?? 'start'} transform={l.rotate ? `rotate(${l.rotate},${tx},${ty})` : undefined}
            style={{...label, fontSize: l.size ?? 28, fontWeight: l.bold ? 700 : 400, fontStyle: l.italic ? 'italic' : 'normal', letterSpacing: l.spacing ?? '0.16em', paintOrder: 'stroke'}}
            stroke={C.land} strokeWidth={l.color === C.force || l.color === '#9C8456' ? 0 : 7} strokeLinejoin="round" fill={l.color ?? C.ink}>
            {l.text}
          </text>
        </g>
      </g>
    );
  });
}

// Time ruler 1790–1870 along the bottom; the marker year moves by keyframes.
export type YearKey = {at: number; dur: number; y: number};
export const makeYearAt = (keys: YearKey[]) => (t: number) => {
  let y = 1825;
  for (const m of keys) {
    if (t <= m.at) break;
    y += (m.y - y) * ramp(t, m.at, m.at + m.dur);
  }
  return y;
};
export const Ruler: React.FC<{yr: number; flash: number}> = ({yr, flash}) => {
  const [x0, x1, y] = [140, 1780, 1000];
  const xs = (v: number) => x0 + ((Math.min(1870, v) - 1790) / 80) * (x1 - x0);
  return (
    <g>
      <rect x={0} y={H - 116} width={W} height={116} fill={C.paper} />
      <rect x={0} y={H - 116} width={W} height={116} fill={C.accent} opacity={0.12 * flash} />
      <line x1={0} x2={W} y1={H - 116} y2={H - 116} stroke={C.rule} strokeWidth={1} />
      <line x1={x0} x2={x1} y1={y} y2={y} stroke={C.ink} strokeWidth={2} />
      {Array.from({length: 9}, (_, i) => 1790 + i * 10).map((v) => (
        <g key={v}>
          <line x1={xs(v)} x2={xs(v)} y1={y - 8} y2={y + 8} stroke={C.ink} strokeWidth={2} />
          <text x={xs(v)} y={y + 40} textAnchor="middle" style={{...label, fontSize: 24}} fill={C.ink}>{v}</text>
        </g>
      ))}
      {/* past 1870 the marker steps off the ruler to "today" */}
      {yr > 1870 ? <line x1={x1} x2={x1 + 80} y1={y} y2={y} stroke={C.ink} strokeWidth={2} strokeDasharray="5 6" /> : null}
      <circle cx={yr > 1870 ? x1 + 80 * Math.min(1, (yr - 1870) / 150) : xs(yr)} cy={y} r={10} fill={C.accent} />
      <text x={yr > 1870 ? x1 + 80 * Math.min(1, (yr - 1870) / 150) : xs(yr)} y={y - 22} textAnchor="middle" style={{...label, fontSize: 24, fontWeight: 700}} fill={C.accent}>{yr <= 1870 ? Math.round(yr) : yr >= 2019 ? 'today' : ''}</text>
    </g>
  );
};
export type Note = {from: number; to: number; text: string};

// Inserts: paper page with a picture or a diagram, caption, source and licence, mini-map.
export type Side = {kicker: string; head: string; body?: string; tag: string; credit: string; plaque: string};
export const MiniMap: React.FC<{at: LonLat}> = ({at}) => {
  const p = P(at);
  const mk = 1.6;
  return (
    <svg width={220} height={220} style={{position: 'absolute', left: 1650, top: 54}}>
      <defs><clipPath id="mini"><circle cx={110} cy={110} r={100} /></clipPath></defs>
      <g clipPath="url(#mini)">
        <rect width={220} height={220} fill={C.water} />
        <g transform={`translate(${110 - p[0] * mk},${110 - p[1] * mk}) scale(${mk})`}>
          <path d={G.land} fill={C.land} />
          {G.relief.map((d, i) => <path key={i} d={d} fill={C.relief} fillOpacity={0.5} />)}
          <path d={G.lakes} fill={C.water} />
          <path d={G.rivers} fill="none" stroke={C.river} strokeWidth={1.5 / mk} />
        </g>
        <circle cx={110} cy={110} r={8} fill={C.accent} />
      </g>
      <circle cx={110} cy={110} r={100} fill="none" stroke={C.ink} strokeWidth={2.5} />
    </svg>
  );
};
export const SideText: React.FC<{s: Side; left: number; top: number; width: number}> = ({s, left, top, width}) => (
  <div style={{position: 'absolute', left, top, width, color: C.ink}}>
    <div style={{...label, fontSize: 27, opacity: 0.72}}>{s.kicker}</div>
    <div style={{...title, fontSize: 60, marginTop: 14}}>{s.head}</div>
    {s.body ? <div style={{fontFamily: F.label, fontSize: 36, lineHeight: 1.28, marginTop: 20}}>{s.body}</div> : null}
    <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16}}>{s.tag}</div>
    <div style={{height: 1, background: C.rule, margin: '26px 0 20px'}} />
    <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>{s.credit}</div>
    <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>{s.plaque}</div>
  </div>
);
export const Picture: React.FC<{src: string; w: number; h: number; drift: number; origin: string; wide?: boolean}> = ({src, w, h, drift, origin, wide}) => {
  const bw = wide ? 1720 : Math.min(1120, (640 * w) / h);
  const bh = (bw * h) / w;
  const top = wide ? 140 : 150;
  return (
    <div style={{position: 'absolute', left: 100, top, width: bw, height: bh, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', transform: wide ? `scale(${1.07 + 0.05 * drift}) translateX(${(0.5 - drift) * 4}%)` : `scale(${1 + 0.1 * drift})`, transformOrigin: origin}} />
    </div>
  );
};
export const PicPage: React.FC<{src: string; w: number; h: number; origin: string; s: Side; at: LonLat; drift: number}> = (p) => {
  const bw = Math.min(1120, (640 * p.w) / p.h);
  return (
    <AbsoluteFill style={{background: C.paper}}>
      <Picture src={p.src} w={p.w} h={p.h} drift={p.drift} origin={p.origin} />
      <SideText s={p.s} left={100 + bw + 50} top={300} width={W - bw - 260} />
      <MiniMap at={p.at} />
    </AbsoluteFill>
  );
};

export const Horse: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`} fill={C.ink}>
    <ellipse cx={50} cy={34} rx={31} ry={14} />
    <path d="M70,30 L84,6 L93,8 L82,38 Z" />
    <path d="M84,6 L102,16 L99,23 L85,17 Z" />
    {[26, 35, 63, 72].map((lx) => <rect key={lx} x={lx} y={40} width={5.5} height={36} rx={2} />)}
    <path d="M20,28 C8,34 8,48 12,58" stroke={C.ink} strokeWidth={5} fill="none" strokeLinecap="round" />
  </g>
);
export const Boat: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g transform={`translate(${x},${y})`} fill={C.ink}>
    <path d="M0,20 L90,20 L80,40 L10,40 Z" />
    <rect x={22} y={4} width={46} height={16} />
  </g>
);
export type Ins = {from: number; to: number; at: LonLat; instant?: boolean; render: (t: number, drift: number) => React.ReactNode};

// One part of the film. Overlays get the frame context: time, camera, a base-to-screen mapper and the
// fine-detail fade (1 when zoomed in on New York State).
export type Ctx = {t: number; cam: Cam; at: (p: XY) => XY; fine: number};
export type Part = {
  moves?: Move[];
  labels?: Lbl[];
  years?: YearKey[];
  notes?: Note[];
  inserts?: Ins[];
  relief?: (t: number) => number; // extra relief opacity on top of 0.3
  flash?: (t: number) => number; // ruler highlight
  ground?: (c: Ctx) => React.ReactNode; // base coordinates, over the relief, under lakes and rivers
  under?: (c: Ctx) => React.ReactNode; // base coordinates, over rivers
  over?: (c: Ctx) => React.ReactNode; // screen coordinates, under labels
  top?: (t: number) => React.ReactNode; // HTML over the map and ruler, under inserts
};

export function makeFilm(parts: Part[], start: View, tag: string): React.FC {
  const moves = parts.flatMap((p) => p.moves ?? []).sort((a, b) => a.at - b.at);
  const labels = parts.flatMap((p) => p.labels ?? []);
  const years = parts.flatMap((p) => p.years ?? []).sort((a, b) => a.at - b.at);
  const notes = parts.flatMap((p) => p.notes ?? []);
  const inserts = parts.flatMap((p) => p.inserts ?? []);
  const camera = makeCamera(start, moves);
  const yearAt = makeYearAt(years);
  const MapLayer: React.FC<{t: number; cam: Cam}> = ({t, cam}) => {
    const k = cam.k;
    const tr = `translate(${W / 2 - cam.c[0] * k},${H / 2 - cam.c[1] * k}) scale(${k})`;
    const at = (p: XY): XY => [(p[0] - cam.c[0]) * k + W / 2, (p[1] - cam.c[1]) * k + H / 2];
    const fine = interpolate(k, [2.6, 3.0], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const relief = 0.3 + parts.reduce((s, p) => s + (p.relief?.(t) ?? 0), 0);
    const ctx: Ctx = {t, cam, at, fine};
    return (
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <rect width={W} height={H} fill={C.water} />
        <g transform={tr}>
          <path d={G.land} fill={C.land} />
          {G.relief.map((d, i) => <path key={i} d={d} fill={C.relief} fillOpacity={relief * (1 - fine)} />)}
          {G.reliefFine.map((d, i) => <path key={`f${i}`} d={d} fill={C.relief} fillOpacity={relief * fine} />)}
          {parts.map((p, i) => <React.Fragment key={i}>{p.ground?.(ctx)}</React.Fragment>)}
          <path d={G.lakes} fill={C.water} stroke="#AEC0C3" strokeWidth={1} vectorEffect="non-scaling-stroke" />
          <path d={G.rivers} fill="none" stroke={C.river} strokeWidth={1.6} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
          <path d={G.riversFine} fill="none" stroke={C.river} strokeWidth={1.4} strokeOpacity={fine} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
          {parts.map((p, i) => <React.Fragment key={i}>{p.under?.(ctx)}</React.Fragment>)}
        </g>
        {parts.map((p, i) => <React.Fragment key={i}>{p.over?.(ctx)}</React.Fragment>)}
        {Labels(t, cam, labels)}
      </svg>
    );
  };
  return () => {
    const [handle] = useState(() => delayRender('fonts'));
    useEffect(() => {
      Promise.all(fontFiles.map((x) => new FontFace(x.family, `url(${staticFile(x.file)})`, {weight: x.weight}).load())).then((faces) => {
        faces.forEach((face) => document.fonts.add(face));
        continueRender(handle);
      });
    }, [handle]);
    const t = useCurrentFrame() / FPS;
    const cam = camera(t);
    const ins = inserts.find((x) => t >= x.from && t < x.to);
    let lens: React.ReactNode = null;
    if (ins) {
      const [x, y] = scr(ins.at, cam);
      const maxR = Math.hypot(Math.max(x, W - x), Math.max(y, H - y));
      const open = ins.instant ? 1 : ramp(t, ins.from, ins.from + 0.7);
      const r = 8 + (maxR - 8) * open * (1 - ramp(t, ins.to - 0.7, ins.to));
      const drift = ramp(t, ins.from, ins.to);
      lens = (
        <>
          <AbsoluteFill style={{clipPath: `circle(${r}px at ${x}px ${y}px)`}}>{ins.render(t, drift)}</AbsoluteFill>
          <svg width={W} height={H} style={{position: 'absolute'}}>
            <circle cx={x} cy={y} r={r} fill="none" stroke={C.ink} strokeWidth={3} />
          </svg>
        </>
      );
    }
    const note = notes.find((n) => t >= n.from && t < n.to);
    const flash = parts.reduce((s, p) => s + (p.flash?.(t) ?? 0), 0);
    return (
      <AbsoluteFill style={{background: C.water}}>
        <MapLayer t={t} cam={cam} />
        <svg width={W} height={H} style={{position: 'absolute'}}>
          <Ruler yr={yearAt(t)} flash={flash} />
          {note ? <text x={110} y={H - 132} style={{fontFamily: F.label, fontSize: 22}} fill={C.ink} fillOpacity={0.66 * win(t, note.from, note.to, 0.4)}>{note.text}</text> : null}
        </svg>
        {parts.map((p, i) => <React.Fragment key={i}>{p.top?.(t)}</React.Fragment>)}
        {lens}
        <div style={{position: 'absolute', right: 40, top: 22, ...label, fontSize: 20, color: C.ink, opacity: 0.7}}>{tag}</div>
      </AbsoluteFill>
    );
  };
}


// Chapter heading: big title for a few seconds at the chapter start, then a small running tag.
export const chapterTitle = (n: number, name: string, from: number, to: number) => (t: number) => {
  const big = win(t, from, from + 5.5, 0.6);
  const tag = win(t, from + 5.5, to - 1.2, 0.6); // gone before the next chapter's title
  return (
    <>
      <div style={{position: 'absolute', left: 110, top: 92, opacity: big}}>
        <div style={{...label, fontSize: 30, color: C.accent, fontWeight: 700}}>Chapter {n}</div>
        <div style={{...title, fontSize: 84, marginTop: 8}}>{name}</div>
      </div>
      <div style={{position: 'absolute', left: 110, top: 60, opacity: tag, ...label, fontSize: 24, color: C.ink}}>
        {n} · {name}
      </div>
    </>
  );
};

// A small lock: a chamber with a gate at each end, in screen space.
export const LockGlyph = (p: XY, o = 1, s = 1) => (
  <g transform={`translate(${p[0]},${p[1]}) scale(${s})`} opacity={o}>
    <rect x={-13} y={-7} width={26} height={14} fill={C.paper} stroke={C.ink} strokeWidth={2.5} />
    <line x1={-13} x2={-13} y1={-11} y2={11} stroke={C.accent} strokeWidth={4} />
    <line x1={13} x2={13} y1={-11} y2={11} stroke={C.accent} strokeWidth={4} />
  </g>
);

// A quotation card in the lower left of the map, with its source.
export const QuoteCard: React.FC<{o: number; quote: string; source: string; width?: number}> = ({o, quote, source, width = 760}) =>
  o > 0 ? (
    <div style={{position: 'absolute', left: 110, bottom: 172, width, padding: '22px 28px', background: C.paper, outline: `1.5px solid ${C.ink}`, opacity: o}}>
      <div style={{fontFamily: F.title, fontSize: 38, lineHeight: 1.22, color: C.ink, fontStyle: 'italic'}}>“{quote}”</div>
      <div style={{fontFamily: F.label, fontSize: 24, color: C.ink, marginTop: 12, opacity: 0.8}}>{source}</div>
    </div>
  ) : null;
````

## probe/src/narration.ts

````ts
// Narration of the whole episode, script.md word for word; the pilot cut is the scenes up to 'finish'.
// Not shown on screen: it times the picture for a later ElevenLabs voice, at 150 words a minute.
export const WPM = 150;

export type Scene = {id: string; text: string; lead?: number; pause?: number};

export const SCENES: Scene[] = [
  {id: 'sandy', lead: 1, pause: 0.5, text: 'On the fourth of November, 1825, a fleet of boats gathered off Sandy Hook, at the entrance to New York Harbor.'},
  {id: 'keg', pause: 0.9, text: 'On one of them, Governor DeWitt Clinton emptied a keg into the Atlantic. The water in that keg came from Lake Erie, more than five hundred miles away by water, on the far side of a mountain range.'},
  {id: 'wedding', lead: 0.5, pause: 1.8, text: 'They called it the Wedding of the Waters.'},
  {id: 'dig', pause: 0.8, text: "Eight years earlier, New York State had started digging a ditch across its own wilderness to make that moment possible. Critics mocked it as the big ditch. It went down in history as Clinton's Ditch."},
  {id: 'rivals', pause: 0.4, text: 'In the decades after that keg was emptied, New York City pulled away from every rival port in the country.'},
  {id: 'whole', pause: 2.6, text: 'So how does a ditch make a city? To see it, we need the whole map.'},
  {id: 'key', pause: 0.8, text: 'A quick key before we start. A solid line is documented. A dashed line is a reconstruction. Hatching marks what is disputed. And time runs along the bottom.'},
  {id: 'coast', lead: 1.4, pause: 0.5, text: 'In 1800, the United States was a country of the coast. Its biggest cities, New York, Philadelphia, Baltimore and Boston, were all seaports. And they were rivals.'},
  {id: 'mountains', pause: 1.2, text: 'Behind them rose the Appalachians: ridge after ridge, from New England down to Alabama.'},
  {id: 'settlers', pause: 0.5, text: 'Beyond the mountains, the country was filling up. Settlers poured into Kentucky, Tennessee and Ohio. They grew wheat and corn, and raised hogs.'},
  {id: 'flatboat', pause: 1.8, text: 'But their harvest had a problem. The cheapest way to market was not east, over the mountains. It was downstream: by flatboat down the Ohio and the Mississippi, all the way to New Orleans. For a farmer in Ohio, the cities of the Atlantic coast might as well have been overseas.'},
  {id: 'cost', lead: 0.7, pause: 1.2, text: 'Over land, everything was slow and expensive. Around 1817, moving one ton of goods from Buffalo to New York City, by wagon and then by river, cost close to a hundred dollars. And it took weeks.'},
  {id: 'road', lead: 0.4, pause: 0.6, text: 'Washington did build one road west, the National Road. It reached the Ohio River at Wheeling in 1818. It helped. But a wagon on a good road was still a wagon.'},
  {id: 'horse', lead: 0.7, pause: 1.2, text: "Water was the answer. In 1816, Clinton's canal petition put it in numbers. Carrying a ton a hundred miles over land cost about thirty-two dollars. By canal, he promised, it would cost one. The question was where water could get through the mountains."},
  {id: 'hudson', lead: 0.8, pause: 0.6, text: 'Look closer at New York. The Hudson River runs north from the harbor for about a hundred and fifty miles, so low that the ocean tide reaches all the way to Troy.'},
  {id: 'gap', lead: 0.6, pause: 1, text: 'At Albany, the Mohawk River comes in from the west, through a valley between the Adirondacks and the Catskills. Follow the Mohawk, then the lowlands beyond it, and you reach the Great Lakes without crossing a mountain ridge.'},
  {id: 'lowgap', lead: 0.8, pause: 2.2, text: 'The way is not flat. But it is the only low gap through the Appalachian wall.'},
  {id: 'finish', lead: 0.4, pause: 3.2, text: 'Nature had drawn most of a line from the Atlantic to the interior. Someone just had to finish it.'},
  // Chapters 2–6: the rest of the episode, one scene per storyboard shot or two.
  {id: 'idea', lead: 2.2, pause: 0.5, text: "The idea was not new. People had dreamed of a canal through this valley for decades. In the 1790s, a private company built a few small locks around the falls of the Mohawk. It helped, but not enough."},
  {id: 'scale', pause: 0.8, text: "What was new was the scale: one artificial river from the Hudson at Albany to Lake Erie at Buffalo. Three hundred and sixty-three miles, through forest, swamp and rock."},
  {id: 'ontario', pause: 1.0, text: "Why go all the way to Lake Erie, when Lake Ontario is closer? Because a boat on Lake Ontario could just as easily sail down the St. Lawrence to Montreal, in British Canada. The planners wanted the trade of the West to have one way out: through New York. So the line runs inland, all the way to Erie."},
  {id: 'champion', lead: 0.7, pause: 0.8, text: "Its champion was DeWitt Clinton: former mayor of New York City, canal commissioner, and, from 1817, governor."},
  {id: 'veto', lead: 0.5, pause: 1.0, text: "Washington would not pay for it. In March 1817, President Madison vetoed a bill that would have funded roads and canals. Thomas Jefferson is said to have called the plan \"little short of madness\". We have that line only from a New York legislator, recalling their meeting years later."},
  {id: 'rome', lead: 0.5, pause: 0.8, text: "So New York paid for it alone. In April 1817, the legislature voted to begin. On the Fourth of July, 1817, digging started at Rome, in the flat middle of the state, where fast progress could convince the doubters."},
  {id: 'section', lead: 0.7, pause: 1.2, text: "The canal itself was modest. Forty feet wide at the surface. Four feet deep. With a towpath alongside for the horses and mules that pulled the boats."},
  {id: 'engineers', lead: 0.5, pause: 1.2, text: "Its engineers had never built a canal. Benjamin Wright and James Geddes were surveyors who learned on the job. A young assistant, Canvass White, went to England to study its canals. Back home, he found a local stone that made cement that hardens under water. That cement held the locks together."},
  {id: 'labor', lead: 0.6, pause: 0.8, text: "The digging was done by hand and by animal, section by section, by local contractors. Most of the laborers were men from nearby farms and towns. Irish immigrants worked alongside them. In 1819, fever in the marshes near Montezuma laid up more than a thousand men."},
  {id: 'name', pause: 1.6, text: "The name Clinton's Ditch stuck. In the end, it stuck as a compliment."},
  {id: 'problem', lead: 2.2, pause: 1.0, text: "Here is the problem the builders faced, drawn by their own hands. In 1821, the canal commissioners published this map. With it comes a profile: the height of the land from the Hudson to Lake Erie."},
  {id: 'rise', lead: 0.6, pause: 1.0, text: "Lake Erie sits about five hundred and sixty-five feet above the Hudson. Water does not run uphill. So the canal had to climb in steps, and each step is a lock."},
  {id: 'lock', lead: 0.6, pause: 1.6, text: "A lock is a box of water with gates at both ends. A boat floats in, and the gate closes behind it. Water flows in from the level above, and the boat rises with it. Then the upper gate opens, and the boat floats out, one step higher. Going down, it all runs in reverse. The gates meet in a shallow V, pointing upstream. The weight of the water presses them shut."},
  {id: 'locks83', lead: 0.6, pause: 0.8, text: "The canal needed eighty-three locks. Many of them climb the Mohawk Valley. In the middle of the state, one level runs for almost seventy miles without a single lock."},
  {id: 'escarpment', pause: 0.8, text: "But at the western end, the land rises in one long wall: the Niagara Escarpment, the same ridge that the Niagara River falls over."},
  {id: 'lockport', lead: 0.6, pause: 1.2, text: "At a place soon called Lockport, the builders cut two staircases of five locks each into the rock, side by side, lifting boats about sixty feet. One staircase for boats going up, one for boats coming down. Above them, crews blasted a channel through solid rock: the Deep Cut."},
  {id: 'aqueduct', lead: 0.6, pause: 1.0, text: "Rivers were the other obstacle. At Rochester, the canal crossed the Genesee River on a stone aqueduct eight hundred feet long: a bridge that carried water instead of a road."},
  {id: 'sections', lead: 0.6, pause: 1.4, text: "Section by section, the line came together. Boats were paying tolls on the finished middle section in 1820, five years before the whole canal was done."},
  {id: 'opened', lead: 2.2, pause: 0.6, text: "On October twenty-sixth, 1825, the canal opened from end to end."},
  {id: 'relay', lead: 0.6, pause: 1.6, text: "At ten in the morning, at Buffalo, Governor Clinton boarded a canal boat called the Seneca Chief. As it set off, a cannon fired. Then another, within earshot down the line. Then another. Cannons placed along the canal and down the Hudson passed the signal from gun to gun. It reached New York City in about an hour and twenty minutes."},
  {id: 'voyage', lead: 0.6, pause: 1.0, text: "The boats themselves moved at the speed of a walking horse, and down the Hudson behind a steamboat. Nine days of crowds, speeches and fireworks. On November fourth they reached New York, and a fleet escorted them out to Sandy Hook."},
  {id: 'book', lead: 0.6, pause: 1.2, text: "New York published a whole book about the celebration, with pictures like this one. New York merchants gave Clinton a pair of silver vases, in thanks for the canal. Potters in England put the canal on dinner plates and sold them to Americans."},
  {id: 'party', lead: 0.5, pause: 1.6, text: "It was a victory party. The real victory came later."},
  {id: 'twist', lead: 2.2, pause: 1.2, text: "First, a twist. Counted within its city limits, New York was already the largest city in America before the canal was dug. In 1810, the census found about ninety-six thousand people in New York, and about fifty-four thousand in Philadelphia. Count Philadelphia's whole county, though, and it was still bigger than New York until the 1820s. The race was not over. The canal did not make New York first. It made New York impossible to catch."},
  {id: 'cheaper', lead: 0.6, pause: 1.2, text: "Once the canal opened, the cost of moving a ton of goods between Buffalo and New York fell by about nine tenths. A trip that took weeks now took days."},
  {id: 'traffic', lead: 0.6, pause: 1.0, text: "Traffic poured in. Wheat and flour came east, first from western New York, and soon from Ohio and beyond. Manufactured goods and settlers went west. In 1820, New York was a distant third among American ports in flour exports. By 1827, it led."},
  {id: 'tolls', lead: 0.6, pause: 1.2, text: "Tolls flowed into the state treasury. Within about a decade, they had paid back what the canal cost to build: about seven million dollars."},
  {id: 'cities', lead: 0.6, pause: 0.8, text: "Along the line, villages became cities. Rochester, with its mills on the falls of the Genesee, became the Flour City. Buffalo grew from a frontier village into a great lake port."},
  {id: 'growth', lead: 0.5, pause: 1.2, text: "And at the end of the line, New York City grew fastest of all. In 1820, about one hundred and twenty-four thousand people lived there. By 1860, more than eight hundred thousand did."},
  {id: 'reasons', lead: 0.7, pause: 1.0, text: "The canal was not the only reason. New York already had a deep, sheltered harbor. From 1818, the Black Ball Line sailed to Liverpool on a fixed schedule. State law favored New York's auction houses, where British goods were sold off cheaply. And cotton from the South passed through New York's merchants and banks."},
  {id: 'argue', lead: 0.6, pause: 1.0, text: "Historians still argue how much of New York's rise belongs to the canal. But the canal gave New York something no rival had: a water road into the heart of the continent. It made every other advantage stronger, because now the produce of the West came to New York's docks."},
  {id: 'rivals2', lead: 0.5, pause: 1.6, text: "Philadelphia and Baltimore fought back with canals and railroads of their own. But they had to climb the mountains. New York had gone around them."},
  {id: 'railroads', lead: 2.2, pause: 1.0, text: "Clinton's ditch was soon too small. The state began to widen and deepen it in 1836. Railroads followed the same route: up the Hudson, along the Mohawk, across the lowlands to Buffalo. In 1853, ten small lines between Albany and Buffalo merged into the New York Central. Later, the highway took the same path."},
  {id: 'today', lead: 0.5, pause: 0.8, text: "Clinton's ditch itself was widened, moved and rebuilt more than once. The canal that runs there today is its successor."},
  {id: 'gapnow', lead: 0.6, pause: 3.0, text: "But the gap in the mountains never moved. And the city at its mouth is still the largest in America. One ditch, four feet deep, did not build New York by itself. But it decided where the water would go. And for a trading city, that was everything."},
];

export type Timed = Scene & {start: number; voice: number; end: number; lines: {text: string; from: number; to: number}[]};

const words = (s: string) => s.split(/\s+/).filter(Boolean).length;

// Sentences time the events on screen; a sentence over 120 characters splits at the comma nearest its middle.
function lines(text: string): string[] {
  const out: string[] = [];
  for (const s of text.split(/(?<=(?<!St)[.?!])\s+/)) {
    if (s.length <= 120) {
      out.push(s);
      continue;
    }
    const commas = [...s.matchAll(/, /g)].map((m) => m.index ?? 0);
    const mid = commas.sort((a, b) => Math.abs(a - s.length / 2) - Math.abs(b - s.length / 2))[0];
    out.push(s.slice(0, mid + 1), s.slice(mid + 2));
  }
  return out;
}

export const TIMED: Timed[] = [];
let t = 0;
for (const s of SCENES) {
  const voice = t + (s.lead ?? 0.3);
  const dur = (words(s.text) / WPM) * 60;
  const ls = lines(s.text);
  const total = ls.reduce((a, l) => a + words(l), 0);
  let at = voice;
  const timed = ls.map((l) => {
    const d = (words(l) / total) * dur;
    const r = {text: l, from: at, to: at + d};
    at += d;
    return r;
  });
  const end = voice + dur + (s.pause ?? 0.4);
  TIMED.push({...s, start: t, voice, end, lines: timed});
  t = end;
}
export const TOTAL = t;
export const lineWith = (id: string, word: string) => {
  const l = TIMED.find((x) => x.id === id)!.lines.find((x) => x.text.includes(word));
  if (!l) throw new Error(`no line with "${word}" in ${id}`);
  return l;
};
export const S = Object.fromEntries(TIMED.map((x) => [x.id, x])) as Record<string, Timed>;
````

## probe/src/pages-a.tsx

````tsx
// Own-drawing inserts of chapters 2 and 3: the veto card, the canal's cross-section, cement and engineers,
// the climb to Lake Erie, how a lock works.
// Every animation is tied to a narrated sentence (line / lineWith), never to absolute seconds.
import React from 'react';
import {AbsoluteFill} from 'remotion';
import profiles from '../public/region/profiles.json';
import {C, F} from './theme';
import {S} from './narration';
import {Horse, Ins, Side, SideText, label, line, ramp, title} from './kit';

const SOIL = '#D9CDB4';
const CARD = '#F7F2E6';
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a: number, b: number, u: number) => a + (b - a) * u;
const txt = (size: number, extra: React.CSSProperties = {}): React.CSSProperties => ({fontFamily: F.label, fontSize: size, ...extra});
const fr = (size: number, extra: React.CSSProperties = {}): React.CSSProperties => ({...title, fontSize: size, ...extra});

// The common page: paper, a 1120x620 panel, side text.
const Page: React.FC<{side: Side; children: React.ReactNode}> = ({side, children}) => (
  <AbsoluteFill style={{background: C.paper}}>
    <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
      <rect width={1120} height={620} fill="#E6DECD" />
      {children}
    </svg>
    <SideText s={side} left={1270} top={300} width={590} />
  </AbsoluteFill>
);

// Water: a body with a gently moving surface.
const waterD = (x0: number, x1: number, top: number, bottom: number, t: number, amp = 2.5, ph = 0) => {
  let d = `M${x0},${bottom} L${x0},${top + amp * Math.sin(x0 / 55 + t * 2 + ph)}`;
  for (let x = x0 + 20; x < x1; x += 20) d += ` L${x},${top + amp * Math.sin(x / 55 + t * 2 + ph)}`;
  return d + ` L${x1},${top + amp * Math.sin(x1 / 55 + t * 2 + ph)} L${x1},${bottom} Z`;
};

// Dimension lines: grow from the middle outwards.
const HDim: React.FC<{x0: number; x1: number; y: number; p: number; text: string; color?: string; size?: number; ext?: [number, number]}> = ({x0, x1, y, p, text, color = C.ink, size = 28, ext}) => {
  if (p <= 0) return null;
  const m = (x0 + x1) / 2;
  const a = m - (m - x0) * p;
  const b = m + (x1 - m) * p;
  return (
    <g opacity={clamp(p * 3)}>
      {ext ? [x0, x1].map((x) => <line key={x} x1={x} x2={x} y1={y + 8} y2={ext[0]} stroke={color} strokeWidth={1.5} strokeDasharray="5 5" opacity={0.7} />) : null}
      <line x1={a} x2={b} y1={y} y2={y} stroke={color} strokeWidth={3} />
      <line x1={a} x2={a} y1={y - 10} y2={y + 10} stroke={color} strokeWidth={3} />
      <line x1={b} x2={b} y1={y - 10} y2={y + 10} stroke={color} strokeWidth={3} />
      <text x={m} y={y - 16} textAnchor="middle" style={{...label, fontSize: size, fontWeight: 700}} fill={color} opacity={ramp(p, 0.5, 1)}>{text}</text>
    </g>
  );
};
const VDim: React.FC<{x: number; y0: number; y1: number; p: number; big: string; small: string; color?: string}> = ({x, y0, y1, p, big, small, color = C.accent}) => {
  if (p <= 0) return null;
  const m = (y0 + y1) / 2;
  const a = m - (m - y0) * p;
  const b = m + (y1 - m) * p;
  return (
    <g opacity={clamp(p * 3)}>
      <line x1={x} x2={x} y1={a} y2={b} stroke={color} strokeWidth={3} />
      <line x1={x - 10} x2={x + 10} y1={a} y2={a} stroke={color} strokeWidth={3} />
      <line x1={x - 10} x2={x + 10} y1={b} y2={b} stroke={color} strokeWidth={3} />
      <g opacity={ramp(p, 0.5, 1)}>
        <text x={x - 18} y={m + 4} textAnchor="end" style={fr(54, {fontWeight: 600})} fill={color}>{big}</text>
        <text x={x - 18} y={m + 36} textAnchor="end" style={{...label, fontSize: 28, fontWeight: 700}} fill={color}>{small}</text>
      </g>
    </g>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 1. Washington says no: the veto card and the disputed quotation.
// ---------------------------------------------------------------------------------------------------------------
const VetoPage: React.FC<{t: number}> = ({t}) => {
  const [l0, l1, l2, l3] = [0, 1, 2, 3].map((n) => line('veto', n));
  const card = ramp(t, S.veto.start + 0.4, S.veto.start + 1.1);
  // Line 0: a coin of federal money sets out for roads and canals and is stopped.
  const go = ramp(t, l0.from + 0.2, l0.from + 1.3);
  const bar = ramp(t, l0.from + 1.0, l0.from + 1.4);
  const back = ramp(t, l0.from + 1.4, l0.from + 1.9);
  const coinX = 120 + 190 * go - 55 * back;
  const shake = bar > 0 && back < 1 ? 3 * Math.sin(t * 40) * (1 - back) : 0;
  const cap = ramp(t, l0.from + 0.9, l0.from + 1.6);
  // Line 1: the date, the bill, the stamp.
  const d1 = ramp(t, l1.from + 0.2, l1.from + 0.8);
  const d2 = ramp(t, l1.from + 0.9, l1.from + 1.5);
  const st = ramp(t, l1.from + 2.2, l1.from + 2.5);
  const stampScale = lerp(2.2, 1, st);
  const dim = 1 - 0.5 * ramp(t, l1.from + 2.4, l1.from + 3);
  // Line 2: the quotation in a hatched box.
  const q = ramp(t, l2.from + 0.1, l2.from + 0.9);
  const shift = 285 * (1 - ramp(t, l2.from - 0.3, l2.from + 0.7));
  const q1 = ramp(t, l2.from + 0.8, l2.from + 1.8);
  const q2 = ramp(t, l2.from + 2.6, l2.from + 3.4);
  // Line 3: where the line comes from.
  const f1 = ramp(t, l3.from + 0.1, l3.from + 0.8);
  const f2 = ramp(t, l3.from + 0.9, l3.from + 2.6);
  const f3 = ramp(t, l3.from + 2.6, l3.from + 3.4);
  const f4 = ramp(t, l3.from + 3.8, l3.from + 4.6);
  return (
    <Page side={{kicker: 'Washington · 1817', head: 'Washington says no', tag: 'quote reported, not verified: Joshua Forman’s recollection, 1828, of a meeting in January 1809', credit: 'Veto: general US history. Quote: Forman’s letter, printed in Hosack, Memoir of De Witt Clinton, 1829.', plaque: 'Own drawing'}}>
      <defs>
        <pattern id="hatchV" width={16} height={16} patternUnits="userSpaceOnUse" patternTransform={`translate(${t * 7},0) rotate(45)`}>
          <line x1={0} y1={0} x2={0} y2={16} stroke={C.ink} strokeWidth={2.4} opacity={0.4} />
        </pattern>
      </defs>
      {/* the document card */}
      <g opacity={card} transform={`translate(${shift},${(1 - card) * 24})`}>
        <rect x={50} y={80} width={520} height={490} fill={CARD} stroke={C.ink} strokeWidth={2.5} />
        <text x={80} y={128} style={{...label, fontSize: 30, fontWeight: 700}} fill={C.ink}>Washington</text>
        <g opacity={dim}>
          <line x1={150} x2={430} y1={205} y2={205} stroke={C.ink} strokeWidth={3} strokeDasharray="14 10" strokeDashoffset={-t * 30} opacity={0.6} />
          <g transform={`translate(${coinX + shake},205)`}>
            <circle r={36} fill={C.paper} stroke={C.ink} strokeWidth={4} />
            <text y={14} textAnchor="middle" style={fr(44, {fontWeight: 700})} fill={C.ink}>$</text>
          </g>
          <rect x={332} y={160} width={14} height={90} fill={C.accent} opacity={bar} transform={`scale(1,${bar})`} style={{transformOrigin: '339px 205px'}} />
          {/* road and canal at the far end */}
          <g transform="translate(450,175)" stroke={C.ink} strokeWidth={4} fill="none">
            <path d="M6,60 L18,0 M44,60 L32,0" />
            <path d="M25,52 L25,40 M25,28 L25,16" strokeDasharray="1 0" />
          </g>
          <g transform="translate(508,180)" stroke={C.force} strokeWidth={5} fill="none">
            <path d="M0,10 Q10,0 20,10 T40,10 M0,30 Q10,20 20,30 T40,30 M0,50 Q10,40 20,50 T40,50" />
          </g>
          <text x={80} y={300} style={txt(30)} fill={C.ink} opacity={cap}>federal money for roads and canals</text>
        </g>
        <line x1={80} x2={540} y1={332} y2={332} stroke={C.rule} strokeWidth={2} />
        <text x={80} y={410} style={fr(60, {fontWeight: 600})} fill={C.ink} opacity={d1}>March 3, 1817</text>
        <text x={80} y={466} style={fr(40)} fill={C.ink} opacity={d2}>Madison vetoes</text>
        <text x={80} y={514} style={fr(40)} fill={C.ink} opacity={d2}>the Bonus Bill</text>
        <g opacity={st} transform={`translate(468,495) rotate(-12) scale(${stampScale})`}>
          <rect x={-88} y={-30} width={176} height={60} fill="none" stroke={C.accent} strokeWidth={5} />
          <text y={15} textAnchor="middle" style={{...label, fontSize: 44, fontWeight: 700, letterSpacing: '0.12em'}} fill={C.accent}>Vetoed</text>
        </g>
      </g>
      {/* the quotation: hatched, because disputed */}
      <g opacity={q} transform={`translate(0,${(1 - q) * 24})`}>
        <rect x={610} y={80} width={460} height={300} fill="url(#hatchV)" stroke={C.ink} strokeWidth={2.5} strokeDasharray="12 7" />
        <rect x={634} y={104} width={412} height={252} fill={CARD} opacity={0.92} />
        <text x={840} y={178} textAnchor="middle" style={fr(48, {fontStyle: 'italic'})} fill={C.ink} opacity={q1}>“little short</text>
        <text x={840} y={238} textAnchor="middle" style={fr(48, {fontStyle: 'italic'})} fill={C.ink} opacity={q1}>of madness”</text>
        <text x={840} y={290} textAnchor="middle" style={txt(32, {fontWeight: 700})} fill={C.ink} opacity={q1}>Thomas Jefferson, as reported</text>
        <text x={840} y={334} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent} opacity={q2}>Disputed</text>
      </g>
      {/* the source of the line: a recollection 19 years after */}
      <g opacity={f1}>
        <text x={610} y={426} style={{...label, fontSize: 28}} fill={C.ink}>Where the line comes from</text>
        <circle cx={650} cy={488} r={11} fill={C.ink} />
        <text x={610} y={536} style={txt(32, {fontWeight: 700})} fill={C.ink}>Jan 1809</text>
        <text x={610} y={570} style={txt(28)} fill={C.ink}>the meeting</text>
      </g>
      <line x1={668} x2={668 + 322 * f2} y1={488} y2={488} stroke={C.accent} strokeWidth={4} strokeDasharray="12 8" />
      <g opacity={f3}>
        <circle cx={1010} cy={488} r={11} fill={C.accent} />
        <text x={1070} y={536} textAnchor="end" style={txt(32, {fontWeight: 700})} fill={C.accent}>1828</text>
        <text x={1070} y={570} textAnchor="end" style={txt(28)} fill={C.ink}>Forman’s letter</text>
      </g>
      <text x={840} y={470} textAnchor="middle" style={txt(28, {fontStyle: 'italic'})} fill={C.ink} opacity={f4}>recalled from memory</text>
    </Page>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 2. Cross-section of the canal (Colden, plan of 1816): 40 ft at the surface, 28 at the bottom, 4 deep.
// ---------------------------------------------------------------------------------------------------------------
const SectionPage: React.FC<{t: number}> = ({t}) => {
  const [l0, l1, l2, l3] = [0, 1, 2, 3].map((n) => line('section', n));
  const [gy, k, bot] = [300, 13, 456]; // ground level, pixels per foot, trench bottom (4 ft drawn x3)
  const [xl, xr] = [170, 690]; // 40 ft at the surface
  const dig = ramp(t, S.section.start + 0.4, l0.to - 0.1);
  const fill = ramp(t, l0.from + 0.9, l0.to + 0.2);
  const dTop = ramp(t, l1.from + 0.1, l1.from + 1.1);
  const dBot = ramp(t, l1.from + 1.2, l1.to + 0.3);
  const dDeep = ramp(t, l2.from + 0.1, l2.to - 0.05);
  const tow = ramp(t, l3.from + 0.1, l3.from + 1.0);
  const horse = ramp(t, l3.from + 1.1, l3.from + 2.3);
  const boat = ramp(t, l3.from + 2.4, l3.from + 3.2);
  const rope = ramp(t, l3.from + 3.4, l3.from + 4.2);
  const bob = Math.sin(t * 2.2) * 2.5;
  const step = Math.sin(t * 6) * 2.2 * horse * (1 - ramp(t, l3.to + 0.6, l3.to + 1.2));
  const cx = 430;
  const hx = 70 + (1 - horse) * 330;
  return (
    <Page side={{kicker: 'Cross-section · plan of 1816', head: 'Forty feet by four', tag: 'schematic: boat and horse not to scale; depth drawn ×3', credit: 'Colden, Memoir, 1825: the canal as planned in 1816.', plaque: 'Own drawing'}}>
      <text x={60} y={66} style={{...label, fontSize: 28}} fill={C.ink}>The canal, cut across</text>
      <text x={1060} y={66} textAnchor="end" style={{...label, fontSize: 24}} fill={C.accent}>vertical scale ×3</text>
      {/* soil with the trench cut out of it */}
      <path d={`M0,${gy} L${xl},${gy} L${xl + 78},${bot} L${xr - 78},${bot} L${xr},${gy} L1120,${gy} L1120,620 L0,620 Z`} fill={SOIL} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" opacity={dig} />
      <clipPath id="trench"><path d={`M${xl},${gy - 8} L${xr},${gy - 8} L${xr},${gy} L${xr - 78},${bot} L${xl + 78},${bot} L${xl},${gy} Z`} /></clipPath>
      <g clipPath="url(#trench)">
        <path d={waterD(xl - 10, xr + 10, lerp(bot, gy, fill), bot + 4, t, 2.4)} fill={C.water} />
      </g>
      {/* the boat, seen end-on */}
        <g opacity={boat} transform={`translate(${cx},${gy + bob + (1 - boat) * -30}) scale(1.1)`} fill={C.ink}>
          <path d="M-78,-32 L78,-32 L58,52 L-58,52 Z" />
          <rect x={-42} y={-66} width={84} height={34} />
          <rect x={-26} y={-58} width={20} height={16} fill={C.paper} />
          <rect x={6} y={-58} width={20} height={16} fill={C.paper} />
        </g>
      <path d={`M${xl},${gy} L${xl + 78},${bot} L${xr - 78},${bot} L${xr},${gy}`} fill="none" stroke={C.ink} strokeWidth={2.5} opacity={dig} />
      {/* towpath, horse, rope */}
      <g opacity={tow}>
        <rect x={xr} y={gy - 4} width={130} height={8} fill={C.accent} opacity={0.85} />
        <line x1={xr} x2={xr + 130} y1={gy + 44} y2={gy + 44} stroke={C.accent} strokeWidth={3} />
        <line x1={xr} x2={xr} y1={gy + 34} y2={gy + 54} stroke={C.accent} strokeWidth={3} />
        <line x1={xr + 130} x2={xr + 130} y1={gy + 34} y2={gy + 54} stroke={C.accent} strokeWidth={3} />
        <text x={xr + 135} y={gy + 100} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>Towpath</text>
        <text x={xr + 135} y={gy + 134} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>about 10 ft</text>
      </g>
      <g opacity={horse} transform={`translate(900,${step}) scale(-1,1)`}>
        <Horse x={hx} y={gy - 91} s={1.2} />
      </g>
      <path d={`M${cx + 86},${gy - 4} Q${(cx + 86 + 716) / 2},${gy + 46} ${lerp(cx + 86, 716, rope)},${lerp(gy - 4, gy - 46, rope)}`} fill="none" stroke={C.ink} strokeWidth={3} opacity={rope * boat} />
      {/* dimensions */}
      <HDim x0={xl} x1={xr} y={gy - 104} p={dTop} text="40 ft at the surface" ext={[gy - 4, 0]} />
      <HDim x0={xl + 78} x1={xr - 78} y={bot + 56} p={dBot} text="28 ft at the bottom" color={C.force} ext={[bot + 4, 0]} />
      <VDim x={xl - 28} y0={gy} y1={bot} p={dDeep} big="4 ft" small="deep" />
      <line x1={xl - 60} x2={xl} y1={gy} y2={gy} stroke={C.accent} strokeWidth={1.5} strokeDasharray="5 5" opacity={dDeep} />
      <line x1={xl - 60} x2={xl + 78} y1={bot} y2={bot} stroke={C.accent} strokeWidth={1.5} strokeDasharray="5 5" opacity={dDeep} />
    </Page>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 3. Engineers and hydraulic cement: a lock wall in section, water rising against the mortar.
// ---------------------------------------------------------------------------------------------------------------
const CementPage: React.FC<{t: number}> = ({t}) => {
  const [l0, l1, l2, l3, l4] = [0, 1, 2, 3, 4].map((n) => line('engineers', n));
  const [wx0, wx1, wt, wb, rows] = [720, 940, 120, 520, 8];
  const rh = (wb - wt) / rows;
  const gap = 8;
  const wallRow = (r: number) => ramp(t, S.engineers.start + 0.5 + r * 0.32, S.engineers.start + 0.9 + r * 0.32);
  const names = [ramp(t, l1.from + 0.1, l1.from + 0.7), ramp(t, l1.from + 1.2, l1.from + 1.8), ramp(t, l1.from + 2.5, l1.from + 3.1)];
  const wh = [ramp(t, l2.from + 0.1, l2.from + 0.7), ramp(t, l2.from + 1.2, l2.from + 1.8), ramp(t, l2.from + 2.5, l2.from + 3.1)];
  const cem = [ramp(t, l3.from + 0.1, l3.from + 0.7), ramp(t, l3.from + 0.8, l3.from + 1.4)];
  const rise = ramp(t, l3.from + 1.2, l3.to - 0.2);
  const lead = ramp(t, l3.from + 0.4, l3.from + 1.2);
  const hi = ramp(t, l3.from + 0.9, l3.from + 1.7);
  const pulse = 0.55 + 0.45 * Math.sin(t * 4.5);
  const joints = hi * (t > l4.from ? pulse : 1);
  const lockLbl = ramp(t, l4.from + 0.1, l4.from + 0.7);
  const level = lerp(wb, 270, rise);
  const blocks: {x: number; w: number; r: number; n: number}[] = [];
  for (let r = 0; r < rows; r++) {
    const off = r % 2 ? 55 : 0;
    const cuts = r % 2 ? [0, 55, 165, 220] : [0, 110, 220];
    for (let i = 0; i < cuts.length - 1; i++) blocks.push({x: wx0 + cuts[i], w: cuts[i + 1] - cuts[i], r, n: i + off});
  }
  const card = (y: number, h: number, o: number) => (
    <rect x={40} y={y} width={440} height={h} fill={CARD} stroke={C.ink} strokeWidth={2.5} opacity={o} />
  );
  return (
    <Page side={{kicker: 'Engineers · 1817–1818', head: 'Cement that sets under water', tag: 'schematic wall section, not a surveyed lock', credit: 'Whitford, History of the Canal System of the State of New York, 1906.', plaque: 'Own drawing'}}>
      <text x={500} y={66} style={{...label, fontSize: 28}} fill={C.ink}>Lock wall · section</text>
      {/* water against the wall */}
      <path d={waterD(500, wx0, level, wb, t, 3)} fill={C.water} />
      <rect x={500} y={wb} width={wx1 + 140 - 500} height={620 - wb} fill={SOIL} stroke={C.ink} strokeWidth={2.5} />
      <rect x={wx1} y={wt + 30} width={140} height={wb - wt - 30} fill={SOIL} stroke={C.ink} strokeWidth={2.5} />
      {/* the wall: mortar behind, stones in front */}
      <rect x={wx0} y={wt} width={wx1 - wx0} height={wb - wt} fill="#E9E1CE" opacity={wallRow(rows - 1) > 0 ? 1 : 0} />
      <rect x={wx0} y={wt} width={wx1 - wx0} height={wb - wt} fill={C.accent} opacity={joints * 0.85} />
      {blocks.map((b, i) => {
        const o = wallRow(rows - 1 - b.r);
        return o > 0 ? (
          <rect key={i} x={b.x + gap / 2} y={wt + b.r * rh + gap / 2 + (1 - o) * -30} width={b.w - gap} height={rh - gap} fill={(b.n + b.r) % 2 ? '#CBBF9F' : '#C2B592'} stroke={C.ink} strokeWidth={1.5} opacity={o} />
        ) : null;
      })}
      <rect x={wx0} y={wt} width={wx1 - wx0} height={wb - wt} fill="none" stroke={C.ink} strokeWidth={2.5} />
      {/* name cards */}
      {card(58, 160, names[0])}
      <g>
        <text x={64} y={110} style={fr(40, {fontWeight: 600})} fill={C.ink} opacity={names[0]}>Benjamin Wright</text>
        <text x={64} y={158} style={fr(40, {fontWeight: 600})} fill={C.ink} opacity={names[1]}>James Geddes</text>
        <text x={64} y={200} style={txt(30)} fill={C.ink} opacity={names[2]}>surveyors who learned on the job</text>
      </g>
      {card(238, 150, wh[0])}
      <text x={64} y={290} style={fr(40, {fontWeight: 600})} fill={C.ink} opacity={wh[0]}>Canvass White</text>
      <text x={64} y={336} style={txt(30)} fill={C.ink} opacity={wh[1]}>went to England to study</text>
      <text x={64} y={372} style={txt(30)} fill={C.ink} opacity={wh[2]}>its canals · 1817–1818</text>
      {card(408, 130, cem[0])}
      <text x={64} y={462} style={fr(38, {fontWeight: 600})} fill={C.accent} opacity={cem[0]}>Hydraulic cement, 1818</text>
      <text x={64} y={510} style={txt(32, {fontWeight: 700})} fill={C.accent} opacity={cem[1]}>hardens under water</text>
      {/* leader from the card to a mortar joint */}
      <path d={`M480,${473} L${480 + (wx0 - 480) * lead},${473 + (wt + 4 * rh - 473) * lead}`} stroke={C.accent} strokeWidth={3} strokeDasharray="10 7" fill="none" />
      <circle cx={wx0} cy={wt + 4 * rh} r={9} fill={C.accent} stroke={C.paper} strokeWidth={3} opacity={lead} />
      <text x={wx0 + 110} y={wt - 14} textAnchor="middle" style={{...label, fontSize: 26, fontWeight: 700}} fill={C.accent} opacity={hi}>mortar joints</text>
      <text x={(wx0 + wx1) / 2} y={wb + 62} textAnchor="middle" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.ink} opacity={lockLbl}>holds the lock together</text>
    </Page>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 4. The climb: the ground from Albany to Lake Erie, then the staircase of locks as a schematic.
// ---------------------------------------------------------------------------------------------------------------
const albanyMile = 138; // in profiles.json the first 139 miles are the Hudson below Albany (sea level)
const GROUND = profiles.a.miles.map((m, i) => [m - albanyMile, profiles.a.ft[i]] as [number, number]).filter(([m]) => m >= 0);
const MAXM = GROUND[GROUND.length - 1][0];
const groundAt = (m: number) => {
  const i = GROUND.findIndex(([mm]) => mm >= m);
  if (i <= 0) return GROUND[0][1];
  const [[m0, f0], [m1, f1]] = [GROUND[i - 1], GROUND[i]];
  return lerp(f0, f1, (m - m0) / (m1 - m0));
};

const RisePage: React.FC<{t: number}> = ({t}) => {
  const [l0, l1, l2] = [0, 1, 2].map((n) => line('rise', n));
  const mv = ramp(t, l2.from, l2.from + 0.9); // the profile makes room for the schematic
  const [x0, x1, yb, yt] = [130, 900, lerp(440, 330, mv), lerp(100, 105, mv)];
  const X = (m: number) => x0 + (m / MAXM) * (x1 - x0);
  const Y = (f: number) => yb - (f / 600) * (yb - yt);
  const draw = ramp(t, S.rise.start + 0.5, l0.to - 0.9);
  const reveal = x0 + (x1 - x0 + 4) * draw;
  const brk = ramp(t, l0.to - 1.0, l0.to - 0.1);
  const pts = GROUND.map(([m, f]) => `${X(m)},${Y(f)}`);
  const area = `M${X(0)},${yb} L${pts.join(' L')} L${X(MAXM)},${yb} Z`;
  // line 1: a drop of water starts for the first hill, cannot climb, slides back
  const u = clamp((t - l1.from) / (l1.to - l1.from));
  const dropM = u < 0.45 ? 14.8 * ramp(u, 0, 0.45) : u < 0.58 ? 14.8 : 14.8 - 11.5 * ramp(u, 0.58, 1);
  const dropOn = ramp(t, l1.from - 0.2, l1.from + 0.1) * (1 - ramp(t, l2.from, l2.from + 0.4));
  const noX = ramp(t, l1.from + 0.9, l1.from + 1.1) * (1 - ramp(t, l1.to + 0.2, l1.to + 0.6));
  // line 2: the schematic staircase, one lock at a time, a boat climbing it
  const [bx0, by0, tread, riser, n] = [170, 566, 130, 18, 6];
  const showBox = ramp(t, l2.from, l2.from + 0.5);
  const stepIn = (i: number) => ramp(t, l2.from + 0.3 + i * 0.35, l2.from + 0.6 + i * 0.35);
  const tp = clamp((t - (l2.from + 2.2)) / (l2.to - l2.from - 2.6), 0, 1) * (n - 1);
  const ti = Math.min(n - 2, Math.floor(tp));
  const tf = tp - ti;
  const boatX = lerp(bx0 + tread * (ti + 0.5), bx0 + tread * (ti + 1.5), ramp(tf, 0, 1));
  const boatY = by0 - riser * ti - riser * ramp(tf, 0.3, 0.6) - 2;
  const steps = Array.from({length: n}, (_, i) => i);
  const stair = `M${bx0},${by0 + 24} ` + steps.map((i) => `L${bx0 + i * tread},${by0 - i * riser} L${bx0 + (i + 1) * tread},${by0 - i * riser}`).join(' ') + ` L${bx0 + n * tread},${by0 + 24} Z`;
  const bob = Math.sin(t * 2.4) * 1.6;
  const dm = dropM;
  return (
    <Page side={{kicker: 'Albany to Buffalo', head: 'Climbing 565 feet', body: 'The real canal climbs and falls: its ups and downs add up to about 662 ft.', tag: 'top: ground along the canal line, not the canal itself. Bottom: schematic', credit: 'Heights: NOAA ETOPO 2022; line: J. Atack, 2015. 565 ft: plan of 1817. 662 ft: Colden, Memoir, 1825.', plaque: 'Own drawing'}}>
      <text x={60} y={58} style={{...label, fontSize: 28}} fill={C.ink}>Height of the ground, Albany to Buffalo</text>
      <clipPath id="rev"><rect x={0} y={0} width={reveal} height={620} /></clipPath>
      {[0, 200, 400, 600].map((f) => (
        <g key={f}>
          <line x1={x0} x2={x1} y1={Y(f)} y2={Y(f)} stroke={C.rule} strokeWidth={1.5} />
          <text x={x0 - 12} y={Y(f) + 8} textAnchor="end" style={txt(26)} fill={C.ink}>{f === 600 ? '600 ft' : f}</text>
        </g>
      ))}
      {[0, 100, 200, 300].map((m) => <text key={m} x={X(m)} y={yb + 34} textAnchor="middle" style={txt(26)} fill={C.ink}>{m}</text>)}
      <text x={x1} y={yb + 66} textAnchor="end" style={{...label, fontSize: 22}} fill={C.ink}>miles from Albany, approximate</text>
      <g clipPath="url(#rev)">
        <path d={area} fill={C.relief} />
        <polyline points={pts.join(' ')} fill="none" stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />
      </g>
      <g opacity={ramp(draw, 0, 0.1)}>
        <line x1={X(0)} x2={X(0)} y1={Y(0)} y2={Y(215)} stroke={C.ink} strokeWidth={2} strokeDasharray="5 5" />
        <text x={X(0) + 8} y={Y(215) - 6} style={{...label, fontSize: 26, fontWeight: 700}} fill={C.ink}>Albany · Hudson</text>
      </g>
      <text x={x1 - 8} y={Y(230)} textAnchor="end" style={{...label, fontSize: 26, fontWeight: 700}} fill={C.ink} opacity={ramp(draw, 0.9, 1)}>Buffalo · Lake Erie</text>
      {/* the 565 ft bracket */}
      <g opacity={brk}>
        <line x1={x0} x2={x1 + 40} y1={Y(565)} y2={Y(565)} stroke={C.accent} strokeWidth={2.5} strokeDasharray="10 8" />
        <path d={`M${x1 + 36},${Y(565)} L${x1 + 46},${Y(565)} L${x1 + 46},${yb} L${x1 + 36},${yb}`} fill="none" stroke={C.accent} strokeWidth={4} />
        <text x={x1 + 62} y={Y(280) + 6} style={fr(44, {fontWeight: 600})} fill={C.accent}>≈ 565 ft</text>
      </g>
      {/* water that will not run uphill */}
      <g opacity={dropOn}>
        <circle cx={X(dm)} cy={Y(groundAt(dm)) - 12} r={10} fill={C.force} stroke={C.paper} strokeWidth={3} />
      </g>
      <g opacity={noX}>
        <path d={`M${X(14.8) + 22},${Y(130) - 52} l30,30 m0,-30 l-30,30`} stroke={C.accent} strokeWidth={7} strokeLinecap="round" />
        <text x={X(14.8) + 66} y={Y(130) - 22} style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>no uphill</text>
      </g>
      {/* schematic inset */}
      <g opacity={showBox}>
        <rect x={120} y={412} width={940} height={192} fill={CARD} stroke={C.ink} strokeWidth={2} />
        <text x={140} y={450} style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>Schematic: one step = one lock</text>
      </g>
      {steps.map((i) => {
        const o = stepIn(i);
        return o > 0 ? (
          <g key={i} opacity={o} transform={`translate(0,${(1 - o) * 16})`}>
            <path d={`M${bx0 + i * tread},${by0 + 24} L${bx0 + i * tread},${by0 - i * riser} L${bx0 + (i + 1) * tread},${by0 - i * riser} L${bx0 + (i + 1) * tread},${by0 + 24} Z`} fill={C.water} />
            <line x1={bx0 + i * tread} x2={bx0 + (i + 1) * tread} y1={by0 - i * riser} y2={by0 - i * riser} stroke={C.ink} strokeWidth={3.5} />
            {i > 0 ? <line x1={bx0 + i * tread} x2={bx0 + i * tread} y1={by0 - i * riser - 12} y2={by0 - (i - 1) * riser + 12} stroke={C.accent} strokeWidth={6} /> : null}
          </g>
        ) : null;
      })}
      <g opacity={ramp(t, l2.from + 2.0, l2.from + 2.4)} transform={`translate(${boatX},${boatY + bob})`} fill={C.ink}>
        <path d="M-28,-8 L28,-8 L20,8 L-20,8 Z" />
        <rect x={-14} y={-20} width={28} height={12} />
      </g>
      <text x={bx0 + n * tread + 14} y={by0 - (n - 1) * riser + 8} style={txt(28, {fontWeight: 700})} fill={C.accent} opacity={stepIn(n - 1)}>lock</text>
    </Page>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 5. How a lock works: side view, one cycle up, the same cycle in reverse; then the gates seen from above.
// ---------------------------------------------------------------------------------------------------------------
const LockPage: React.FC<{t: number}> = ({t}) => {
  const L = [0, 1, 2, 3, 4, 5, 6].map((n) => line('lock', n));
  const [yL, yU, floor, sill, gTop] = [400, 250, 500, 350, 232];
  const [cx0, cx1] = [370, 750];
  // One cycle up, u from 0 to 1: boat in and lower gate shut (0 to 0.3), water in (0.3 to 0.64), upper gate
  // opens (0.64 to 0.72), boat out (0.72 to 1). Going down plays it back.
  const e = (a: number, b: number, u: number) => ramp(u, a, b);
  const seg = (a: number, b: number) => clamp((t - L[a].from) / (L[b].to - L[a].from));
  let u = 0;
  let dir: 1 | -1 = 1;
  if (t >= L[1].from && t < L[2].from) u = lerp(0, 0.3, seg(1, 1));
  else if (t >= L[2].from && t < L[3].from) u = lerp(0.3, 0.64, seg(2, 2));
  else if (t >= L[3].from && t < L[4].from) u = lerp(0.64, 1, seg(3, 3));
  else if (t >= L[4].from) {
    u = 1 - clamp((t - L[4].from - 0.2) / (L[4].to - L[4].from - 0.4)) * 1;
    dir = -1;
  }
  const lowShut = e(0.22, 0.3, u);
  const upOpen = e(0.64, 0.72, u);
  const level = lerp(yL, yU, e(0.3, 0.64, u));
  const bX = u < 0.3 ? lerp(120, 560, e(0, 0.24, u)) : u < 0.7 ? 560 : lerp(560, 930, e(0.72, 1, u));
  const surf = bX < cx0 ? yL : bX > cx1 ? yU : level;
  const bob = Math.sin(t * 2.4) * 2;
  const flowIn = dir === 1 && u > 0.3 && u < 0.64;
  const flowOut = dir === -1 && u > 0.3 && u < 0.64;
  const intro = [ramp(t, S.lock.start + 0.3, S.lock.start + 1.1), ramp(t, L[0].from + 1.2, L[0].from + 2.0), ramp(t, L[0].from + 2.8, L[0].from + 3.4), ramp(t, L[0].from + 3.6, L[0].from + 4.2)];
  const side = 1 - ramp(t, L[5].from - 0.1, L[5].from + 0.5);
  const plan = ramp(t, L[5].from + 0.3, L[5].from + 0.9);
  const heads = ['A box of water', 'Boat in, gate shut', 'Water in, boat up', 'Gate open, boat out', 'Going down', 'Gates in a V', 'Water shuts them'];
  const idx = L.reduce((a, l, i) => (t >= l.from ? i : a), 0);
  const gate = (x: number, y0: number, shut: number) => (
    <g opacity={0.2 + 0.8 * shut}>
      <rect x={x - 8} y={lerp(y0 - 30, gTop, shut)} width={16} height={y0 - lerp(y0 - 30, gTop, shut)} fill={C.ink} />
      <rect x={x - 14} y={lerp(y0 - 30, gTop, shut) - 8} width={28} height={10} fill={C.ink} />
    </g>
  );
  // plan view
  const [px0, px1, pw0, pw1, hx, hy0, hy1] = [40, 1080, 150, 470, 600, 190, 430];
  const open = 1 - ramp(t, L[5].from + 1.7, L[5].from + 3.2);
  const phi = lerp((71.6 * Math.PI) / 180, 0, open);
  const leaf = 126.5;
  const tip = (sgn: 1 | -1): [number, number] => [hx + leaf * Math.cos(phi), sgn === 1 ? hy0 + leaf * Math.sin(phi) : hy1 - leaf * Math.sin(phi)];
  const pb = ramp(t, L[5].from + 0.6, L[5].from + 2.2);
  const press = ramp(t, L[6].from + 0.1, L[6].from + 0.9);
  const flowT = (t * 70) % 60;
  const arrowsY = [235, 272, 310, 348, 385];
  return (
    <Page side={{kicker: 'How a lock works', head: heads[idx], tag: 'schematic, not to scale; lift exaggerated', credit: 'How a lock works: the general principle.', plaque: 'Own drawing'}}>
      <defs>
        <marker id="aw" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={C.force} /></marker>
        <marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={C.accent} /></marker>
      </defs>
      <g opacity={side} style={{display: side > 0 ? undefined : 'none'}}>
        {/* the chamber's far wall, so the box reads as a box */}
        <rect x={cx0} y={gTop} width={cx1 - cx0} height={floor - gTop} fill="#DDD2BB" opacity={intro[0]} />
        <g opacity={intro[0]}>
          <path d={waterD(40, cx0, yL, floor, t, 2.5)} fill={C.water} />
          <path d={waterD(cx1, 1080, yU, sill, t, 2.5, 1)} fill={C.water} />
        </g>
        <path d={waterD(cx0, cx1, level, floor, t, 2.5, 2)} fill={C.water} opacity={intro[0]} />
        <path d={`M0,${floor} L${cx1},${floor} L${cx1},${sill} L1120,${sill} L1120,620 L0,620 Z`} fill={SOIL} stroke={C.ink} strokeWidth={2.5} opacity={intro[0]} />
        {gate(cx0, floor, Math.max(lowShut, 0))}
        {gate(cx1, sill, 1 - upOpen)}
        {/* the boat */}
        <g transform={`translate(${bX},${surf + bob})`} fill={C.ink} opacity={ramp(t, S.lock.start + 0.8, S.lock.start + 1.4)}>
          <path d="M-80,-22 L80,-22 L62,16 L-62,16 Z" />
          <rect x={-42} y={-48} width={84} height={26} />
        </g>
        {/* water flowing in (going up) or out (going down) */}
        {flowIn ? <path d={`M840,${sill - 30} C790,${sill + 30} 770,${floor - 40} 690,${floor - 40}`} fill="none" stroke={C.force} strokeWidth={7} strokeDasharray="16 10" strokeDashoffset={-t * 60} markerEnd="url(#aw)" /> : null}
        {flowOut ? <path d={`M450,${floor - 40} C400,${floor - 40} 360,${floor - 30} 300,${yL + 40}`} fill="none" stroke={C.force} strokeWidth={7} strokeDasharray="16 10" strokeDashoffset={-t * 60} markerEnd="url(#aw)" /> : null}
        {/* labels */}
        <g style={{...label, fontSize: 28, fontWeight: 700}}>
          <text x={190} y={yL + 78} textAnchor="middle" fill={C.ink} opacity={intro[1]}>lower level</text>
          <text x={915} y={yU - 24} textAnchor="middle" fill={C.ink} opacity={intro[1]}>upper level</text>
          <text x={560} y={floor + 52} textAnchor="middle" fill={C.ink} opacity={intro[2]}>lock chamber</text>
          <text x={cx0} y={gTop - 22} textAnchor="middle" fill={C.accent} opacity={intro[3]}>gate</text>
          <text x={cx1} y={gTop - 22} textAnchor="middle" fill={C.accent} opacity={intro[3]}>gate</text>
        </g>
        {dir === -1 ? <text x={560} y={90} textAnchor="middle" style={{...label, fontSize: 30, fontWeight: 700}} fill={C.accent}>going down: the same steps, backwards</text> : null}
        {dir === 1 && u > 0.3 && u < 0.64 ? <text x={560} y={90} textAnchor="middle" style={{...label, fontSize: 30, fontWeight: 700}} fill={C.force}>water flows in from above</text> : null}
      </g>
      {/* plan view */}
      <g opacity={plan} style={{display: plan > 0 ? undefined : 'none'}}>
        <text x={60} y={66} style={{...label, fontSize: 28}} fill={C.ink}>Seen from above</text>
        <rect x={px0} y={hy0} width={px1 - px0} height={hy1 - hy0} fill={C.water} />
        <rect x={px0} y={pw0 - 0} width={px1 - px0} height={hy0 - pw0 + 0} fill="#CFC3A8" stroke={C.ink} strokeWidth={2.5} />
        <rect x={px0} y={hy1} width={px1 - px0} height={pw1 - hy1} fill="#CFC3A8" stroke={C.ink} strokeWidth={2.5} />
        {[...Array(26)].map((_, i) => <line key={i} x1={px0 + 40 * i} x2={px0 + 40 * i} y1={pw0} y2={hy0} stroke={C.ink} strokeWidth={1.2} opacity={0.35} />)}
        {[...Array(26)].map((_, i) => <line key={i} x1={px0 + 40 * i} x2={px0 + 40 * i} y1={hy1} y2={pw1} stroke={C.ink} strokeWidth={1.2} opacity={0.35} />)}
        {/* a boat passes through the open gates */}
        <g transform={`translate(${lerp(240, 900, pb)},${(hy0 + hy1) / 2})`} fill={C.ink} opacity={ramp(t, L[5].from + 0.4, L[5].from + 0.9) * (1 - ramp(t, L[5].from + 2.1, L[5].from + 2.6))}>
          <path d="M-70,-24 L50,-24 L74,0 L50,24 L-70,24 Z" />
          <rect x={-40} y={-14} width={50} height={28} fill={C.paper} />
        </g>
        {/* the gates: two leaves, hinged at the walls, meeting in a shallow V that points upstream */}
        {([1, -1] as const).map((sg) => (
          <g key={sg}>
            <line x1={hx} y1={sg === 1 ? hy0 : hy1} x2={tip(sg)[0]} y2={tip(sg)[1]} stroke={C.ink} strokeWidth={16} strokeLinecap="round" />
            <circle cx={hx} cy={sg === 1 ? hy0 : hy1} r={9} fill={C.paper} stroke={C.ink} strokeWidth={3} />
          </g>
        ))}
        <text x={px1 - 10} y={pw0 - 16} textAnchor="end" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.ink}>upstream: higher water</text>
        <text x={px0 + 10} y={pw0 - 16} style={{...label, fontSize: 28, fontWeight: 700}} fill={C.ink}>downstream</text>
        <g opacity={ramp(t, L[5].from + 3.0, L[5].from + 3.5)}>
          <text x={px0 + 10} y={pw1 + 52} style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>gates close in a V, pointing upstream</text>
        </g>
        {/* water pressing the gates shut */}
        <g opacity={press}>
          {arrowsY.map((ay, i) => (
            <path key={i} d={`M${960 - flowT + 60},${ay} L${700 + (1 - press) * 40},${ay}`} stroke={C.accent} strokeWidth={7} strokeDasharray="30 30" strokeDashoffset={-flowT} fill="none" markerEnd="url(#ar)" />
          ))}
          <text x={px1 - 10} y={pw1 + 52} textAnchor="end" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>the weight of the water</text>
          <text x={px1 - 10} y={pw1 + 88} textAnchor="end" style={{...label, fontSize: 28, fontWeight: 700}} fill={C.accent}>presses the gates shut</text>
        </g>
      </g>
    </Page>
  );
};

export const INSERTS_A: Ins[] = [
  {from: S.veto.start, to: S.veto.end, at: [-77.04, 38.9], render: (t) => <VetoPage t={t} />},
  {from: S.section.start, to: S.section.end, at: [-75.9, 43.05], render: (t) => <SectionPage t={t} />},
  {from: S.engineers.start, to: S.engineers.end, at: [-75.6, 43.15], render: (t) => <CementPage t={t} />},
  {from: S.rise.start, to: S.rise.end, at: [-76.6, 43.0], render: (t) => <RisePage t={t} />},
  {from: S.lock.start, to: S.lock.end, at: [-74.86, 43.043], render: (t) => <LockPage t={t} />},
];
````

## probe/src/pages-b.tsx

````tsx
// Inserts of chapters 3–5: the 1821 map and profile, Lockport, the celebration book, vases and plate,
// freight rates, tolls against cost, South Street.
// Each page is one full-frame sheet; the kit opens and closes it through the lens. Every change on a page is tied to a
// sentence (or a word inside a sentence) of its scene in src/narration.ts.
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile} from 'remotion';
import {C, F} from './theme';
import {S, lineWith} from './narration';
import {ALBANY, BUFFALO, Boat, Horse, Ins, LOCKPORT, MiniMap, NYC, XY, ease, label, ramp, title, win} from './kit';

// ---------------------------------------------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------------------------------------------
const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const mix = (a: number, b: number, u: number) => a + (b - a) * u;
// Time of a word inside its sentence: the share of characters before it, so it follows the sentence when timing changes.
const at = (id: string, word: string) => {
  const l = lineWith(id, word);
  return l.from + (l.to - l.from) * (l.text.indexOf(word) / l.text.length);
};
const fmt = (n: number, d = 0) => n.toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d});

// Camera over a picture: centre and visible width in world units, moved between keys. A key with `lin` is reached
// at constant speed (slow drift); the others ease in and out.
type Cam = {cx: number; cy: number; vw: number};
type Key = Cam & {at: number; lin?: boolean};
const track = (t: number, ks: Key[]): Cam => {
  if (t <= ks[0].at) return ks[0];
  for (let i = 1; i < ks.length; i++) {
    if (t <= ks[i].at) {
      const [a, b] = [ks[i - 1], ks[i]];
      const u0 = clamp((t - a.at) / (b.at - a.at));
      const u = b.lin ? u0 : ease(u0);
      return {cx: mix(a.cx, b.cx, u), cy: mix(a.cy, b.cy, u), vw: Math.exp(mix(Math.log(a.vw), Math.log(b.vw), u))};
    }
  }
  return ks[ks.length - 1];
};
type Box = {left: number; top: number; w: number; h: number};
const mapper = (f: Box, c: Cam) => {
  const s = f.w / c.vw;
  return {s, X: (x: number) => f.w / 2 + (x - c.cx) * s, Y: (y: number) => f.h / 2 + (y - c.cy) * s};
};

// A picture placed in world units: image pixel (0,0) sits at (ox, oy), one image pixel is k world units.
// clip: CSS inset() in image pixels, to hide a scan's dark border.
const Photo: React.FC<{src: string; iw: number; ih: number; f: Box; c: Cam; k?: number; ox?: number; oy?: number; o?: number; clip?: string}> = ({src, iw, ih, f, c, k = 1, ox = 0, oy = 0, o = 1, clip}) => {
  const s = f.w / c.vw;
  return (
    <Img src={staticFile(src)} style={{position: 'absolute', left: 0, top: 0, width: iw, height: ih, maxWidth: 'none', transformOrigin: '0 0', opacity: o, clipPath: clip,
      transform: `translate(${f.w / 2 + (ox - c.cx) * s}px, ${f.h / 2 + (oy - c.cy) * s}px) scale(${s * k})`}} />
  );
};
const Frame: React.FC<{f: Box; children: React.ReactNode; bg?: string}> = ({f, children, bg = '#E6DECD'}) => (
  <div style={{position: 'absolute', left: f.left, top: f.top, width: f.w, height: f.h, overflow: 'hidden', outline: `1px solid ${C.rule}`, background: bg}}>{children}</div>
);
const Over: React.FC<{f: Box; children?: React.ReactNode}> = ({f, children}) => (
  <svg width={f.w} height={f.h} style={{position: 'absolute', left: 0, top: 0}}>{children}</svg>
);

// A red tag on the picture, anchored by (ax, ay) in percent of its own box.
const Chip: React.FC<{x: number; y: number; o?: number; ax?: number; ay?: number; size?: number; solid?: boolean; children: React.ReactNode}> = ({x, y, o = 1, ax = -50, ay = -50, size = 30, solid, children}) =>
  o <= 0 ? null : (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(${ax}%, ${ay}%) scale(${0.85 + 0.15 * o})`, opacity: o, padding: '3px 12px 4px', display: 'flex', alignItems: 'center', gap: 8,
      background: solid ? C.accent : C.paper, color: solid ? C.paper : C.accent, border: `2px solid ${C.accent}`, fontFamily: F.label, fontWeight: 700, fontSize: size, lineHeight: 1.15, whiteSpace: 'nowrap'}}>
      {children}
    </div>
  );
const Arrow = ({up, size = 22}: {up: boolean; size?: number}) => (
  <svg width={size} height={size} viewBox="0 0 20 20">
    <path d={up ? 'M10,2 L18,12 L12,12 L12,18 L8,18 L8,12 L2,12 Z' : 'M10,18 L18,8 L12,8 L12,2 L8,2 L8,8 L2,8 Z'} fill="currentColor" />
  </svg>
);

// Text column in the style of SideText, with parts that can fade in on their own sentence.
type SideO = {all?: number; body?: number; tag?: number};
const Side: React.FC<{left: number; top: number; width: number; kicker: string; head: string; body?: React.ReactNode; tag?: string; credit: string; plaque: string; o?: SideO}> = (p) => {
  const o = {all: 1, body: 1, tag: 1, ...p.o};
  return (
    <div style={{position: 'absolute', left: p.left, top: p.top, width: p.width, color: C.ink, opacity: o.all}}>
      <div style={{...label, fontSize: 27, opacity: 0.72}}>{p.kicker}</div>
      <div style={{...title, fontSize: 60, marginTop: 14}}>{p.head}</div>
      {p.body ? <div style={{fontFamily: F.label, fontSize: 36, lineHeight: 1.28, marginTop: 20, opacity: o.body}}>{p.body}</div> : null}
      {p.tag ? <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16, opacity: o.tag}}>{p.tag}</div> : null}
      <div style={{height: 1, background: C.rule, margin: '26px 0 20px'}} />
      <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>{p.credit}</div>
      <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>{p.plaque}</div>
    </div>
  );
};
// One segment of a page with several pictures: visible from a to b, text fades out before the next one fades in.
const seg = (t: number, a: number, b: number, fade = 0.35) => ramp(t, a, a + fade) * (1 - ramp(t, b - fade, b));
const Paper: React.FC<{children: React.ReactNode}> = ({children}) => <AbsoluteFill style={{background: C.paper}}>{children}</AbsoluteFill>;
const fraunces: React.CSSProperties = {fontFamily: F.title, fontVariationSettings: '"opsz" 144', fontWeight: 600};

// Polylines: cumulative length and the part up to a given length.
const lens = (pts: XY[]) => pts.reduce<number[]>((a, p, i) => [...a, i ? a[i - 1] + Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) : 0], []);
const upto = (pts: XY[], len: number[], l: number): XY[] => {
  if (l <= 0) return [];
  const out: XY[] = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (len[i] <= l) out.push(pts[i]);
    else {
      const u = (l - len[i - 1]) / (len[i] - len[i - 1] || 1);
      out.push([mix(pts[i - 1][0], pts[i][0], u), mix(pts[i - 1][1], pts[i][1], u)]);
      break;
    }
  }
  return out;
};

// ---------------------------------------------------------------------------------------------------------------
// 1. The 1821 map and profile (MA-10), scene 'problem'
// ---------------------------------------------------------------------------------------------------------------
// World units here are pixels of nypl-1821-map-profile-crop-3200.jpg (the right sheet). The whole sheet
// (nypl-1821-map-profile-3200.jpg, 3200 x 744) sits in the same world at 2.024 world units per pixel, from x = -3277.
// The profile of the levels, traced from the scans, flat x, y pairs from Lake Erie (west) to the Hudson (east).
const PROFILE_FLAT = [-3131, 67, -2862, 67, -2862, 206, -1486, 206, -1486, 281, -1148, 281, -1148, 308, -939, 308, -939, 346, -818, 346, -818, 370, -733, 370, -733, 385, -656, 385, -656, 391, -530, 391,
  -530, 397, -474, 397, -474, 364, -403, 364, -403, 359, -231, 359, -231, 339, -59, 339, 33, 330, 1497, 330, 1497, 340, 1509, 340, 1509, 352, 1520, 352, 1520, 363, 1578, 363, 1578, 372, 1584, 372,
  1584, 383, 1638, 383, 1638, 395, 1683, 395, 1683, 408, 1718, 408, 1718, 422, 1729, 422, 1729, 436, 1736, 436, 1736, 451, 1747, 451, 1747, 464, 1760, 464, 1760, 479, 1836, 479, 1836, 491, 1903, 491,
  1903, 502, 1968, 502, 1968, 516, 1997, 516, 1997, 528, 2072, 528, 2072, 539, 2156, 539, 2156, 550, 2284, 550, 2284, 562, 2398, 562, 2398, 570, 2415, 570, 2415, 580, 2421, 580, 2421, 591, 2463, 591,
  2463, 604, 2490, 604, 2490, 617, 2543, 617, 2543, 630, 2706, 630, 2706, 643, 2725, 643, 2725, 656, 2812, 656, 2812, 669, 2826, 669, 2826, 681, 2852, 681, 2852, 694, 2884, 694, 2884, 707, 2921, 707,
  2921, 720, 2959, 720, 2959, 732, 3023, 732, 3023, 747, 3039, 747, 3039, 759, 3051, 759, 3051, 772, 3062, 772, 3062, 952];
// From the Hudson to Lake Erie, the way the sentence reads.
const PROFILE: XY[] = PROFILE_FLAT.reduce<XY[]>((a, v, i) => (i % 2 ? a : [...a, [v, PROFILE_FLAT[i + 1]]]), []).reverse();
const PROFILE_LEN = lens(PROFILE);
const PROFILE_CROP = PROFILE_LEN[PROFILE.findIndex((p) => p[0] < 33)] ?? PROFILE_LEN[PROFILE_LEN.length - 1];

const DOC: Box = {left: 100, top: 140, w: 1720, h: 500};
const Doc1821Page: React.FC<{t: number}> = ({t}) => {
  const L = S.problem.lines;
  const T0 = S.problem.voice - 0.4; // the insert opens here, after the chapter title card
  const tCommissioners = at('problem', 'commissioners');
  const tProfile = at('problem', 'profile');
  const tHudson = at('problem', 'from the Hudson');
  const tErie = at('problem', 'Lake Erie');
  const tEnd = L[2].to + 0.3;
  const cam = track(t, [
    {at: T0, cx: -77, cy: 753, vw: 6560},
    {at: L[1].from, cx: 700, cy: 700, vw: 5000, lin: true},
    {at: L[1].from + (L[1].to - L[1].from) * 0.8, cx: 2050, cy: 420, vw: 2300},
    {at: tProfile, cx: 2250, cy: 700, vw: 1900},
    {at: tProfile + 1.0, cx: 2250, cy: 700, vw: 1900},
    {at: tErie, cx: 1000, cy: 480, vw: 2800, lin: true},
    {at: tEnd, cx: -77, cy: 753, vw: 6560},
  ]);
  const m = mapper(DOC, cam);
  // Red frame around "Contracted by direction of the Canal Commissioners ... 1821".
  const box = ramp(t, tCommissioners - 0.2, tCommissioners + 0.9) * (1 - ramp(t, tProfile - 0.6, tProfile));
  const [bx0, by0, bx1, by1] = [m.X(2205), m.Y(358), m.X(2790), m.Y(440)];
  // The highlight runs from the Hudson end to the Lake Erie end of the profile.
  const head = t < tErie ? PROFILE_CROP * clamp((t - tProfile) / (tErie - tProfile)) : mix(PROFILE_CROP, PROFILE_LEN[PROFILE_LEN.length - 1], ramp(t, tErie, tEnd));
  const part = upto(PROFILE, PROFILE_LEN, head).map(([x, y]) => `${m.X(x)},${m.Y(y)}`);
  const tip = part.length ? part[part.length - 1].split(',').map(Number) : null;
  const pageO = ramp(t, T0, T0 + 0.6);
  return (
    <Paper>
      <Frame f={DOC}>
        <Photo src="assets/nypl-1821-map-profile-3200.jpg" iw={3200} ih={744} f={DOC} c={cam} k={2.02405} ox={-3277} />
        <Photo src="assets/nypl-1821-map-profile-crop-3200.jpg" iw={3200} ih={1036} f={DOC} c={cam} clip="inset(14px 0 0 56px)" />
        <Over f={DOC}>
          {/* the scan's black gap between the map's two sheets, shown as plain paper */}
          <rect x={m.X(-58)} y={0} width={m.X(58) - m.X(-58)} height={DOC.h} fill="#E6DECD" />
          <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={8} fill="none" stroke={C.accent} strokeWidth={5} pathLength={1} strokeDasharray={`${box} 2`} opacity={box > 0 ? 1 : 0} />
          {part.length > 1 ? <polyline points={part.join(' ')} fill="none" stroke={C.accent} strokeWidth={9} strokeOpacity={0.72} strokeLinejoin="round" strokeLinecap="round" /> : null}
          {tip && head < PROFILE_LEN[PROFILE_LEN.length - 1] ? <g><circle cx={tip[0]} cy={tip[1]} r={20} fill={C.accent} opacity={0.22} /><circle cx={tip[0]} cy={tip[1]} r={8} fill={C.accent} stroke={C.paper} strokeWidth={2.5} /></g> : null}
        </Over>
        <Chip x={m.X(3040)} y={m.Y(835)} ax={-100} o={ramp(t, tProfile + 0.1, tProfile + 0.6) * (1 - ramp(t, tProfile + 0.9, tProfile + 1.4))}>Hudson</Chip>
        <Chip x={m.X(3062)} y={m.Y(960)} ax={-100} ay={-120} o={ramp(t, tEnd - 1.4, tEnd - 0.8)}>Hudson</Chip>
        <Chip x={m.X(-3090)} y={m.Y(110)} ax={0} ay={0} o={ramp(t, tErie, tErie + 0.7)}>Lake Erie</Chip>
      </Frame>
      <div style={{position: 'absolute', left: 100, top: 676, width: 900, color: C.ink, opacity: pageO}}>
        <div style={{...label, fontSize: 27, opacity: 0.72}}>Document · 1821</div>
        <div style={{...title, fontSize: 60, marginTop: 14}}>The builders' own drawing</div>
        <div style={{fontFamily: F.label, fontSize: 36, lineHeight: 1.28, marginTop: 20, opacity: ramp(t, L[1].from, L[1].from + 0.6)}}>A profile of the levels and the lifts of the locks between Lake Erie and the Hudson.</div>
        <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16, opacity: ramp(t, L[1].from, L[1].from + 0.6)}}>documented · red line: the profile, traced by us</div>
      </div>
      <div style={{position: 'absolute', left: 1080, top: 700, width: 740, color: C.ink, opacity: pageO}}>
        <div style={{height: 1, background: C.rule, marginBottom: 20}} />
        <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>A New Map and Profile of the Proposed Canal from Lake Erie to Hudson River, 1821. Contracted by direction of the Canal Commissioners from the maps of the engineers.</div>
        <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>From The New York Public Library · Public domain</div>
      </div>
    </Paper>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 2. Lockport (MA-13, MA-14, MA-16), scene 'lockport'
// ---------------------------------------------------------------------------------------------------------------
const LF: Box = {left: 100, top: 150, w: 960, h: 640};
const LockportPage: React.FC<{t: number}> = ({t}) => {
  const [t0, t1] = [S.lockport.start, S.lockport.end];
  const tRing = at('lockport', 'two staircases');
  const tFive = at('lockport', 'five locks');
  const tSixty = at('lockport', 'sixty feet');
  const tUpDown = lineWith('lockport', 'One staircase').from;
  const tB = lineWith('lockport', 'Above them').from;
  const tRock = at('lockport', 'solid rock');
  const tCut = at('lockport', 'Deep Cut');
  const tC = tCut + 0.5; // the 1855 view comes only after the sentence ends on "the Deep Cut"
  // Which picture is on top: B fades in over A at tB, C over B at tC.
  const bIn = ramp(t, tB - 0.3, tB + 0.3);
  const cIn = ramp(t, tC - 0.25, tC + 0.25);

  const ca = track(t, [
    {at: t0, cx: 1555, cy: 1100, vw: 2100},
    {at: tRing, cx: 1600, cy: 1150, vw: 1700},
    {at: tSixty, cx: 1640, cy: 1190, vw: 1150},
    {at: tUpDown + 0.4, cx: 1620, cy: 1170, vw: 1500},
    {at: tB + 0.3, cx: 1700, cy: 1150, vw: 1800, lin: true},
  ]);
  const cb = track(t, [
    {at: tB, cx: 1600, cy: 1065, vw: 2330},
    {at: tC + 0.3, cx: 1750, cy: 1180, vw: 1750, lin: true},
  ]);
  const cc = track(t, [
    {at: tC - 0.3, cx: 1600, cy: 1080, vw: 3100},
    {at: t1, cx: 1680, cy: 1500, vw: 1800, lin: true},
  ]);
  const ma = mapper(LF, ca);
  const mb = mapper(LF, cb);
  const mc = mapper(LF, cc);

  // A: ring around the twin staircase, bracket for the height, arrows.
  const ring = ramp(t, tRing - 0.3, tRing + 0.7) * (1 - bIn);
  const [rx0, ry0, rx1, ry1] = [ma.X(1498), ma.Y(1000), ma.X(1738), ma.Y(1398)];
  const brk = ramp(t, tSixty - 0.2, tSixty + 0.8) * (1 - bIn);
  const [bx, by0, by1] = [ma.X(1785), ma.Y(1000), ma.Y(1398)];
  // C: underline under the gate beams.
  const under = ramp(t, tC + 0.1, tC + 0.8);
  const pts: XY[] = [[1150, 1575], [1690, 1680], [2170, 1590]];
  const ul = upto(pts, lens(pts), under * lens(pts)[2]).map(([x, y]) => `${mc.X(x)},${mc.Y(y)}`);

  const sa = 1 - bIn;
  const sb = seg(t, tB, tC, 0.25);
  const sc = ramp(t, tC - 0.1, tC + 0.25);
  const sideFade = (v: number) => ({all: v});
  return (
    <Paper>
      <Frame f={LF}>
        <Photo src="assets/nypl-lockport-prospect-hill-1825-3200.jpg" iw={3200} ih={2321} f={LF} c={ca} />
        {bIn > 0 ? <Photo src="assets/nypl-deep-cutting-lockport-1825-3200.jpg" iw={3200} ih={2269} f={LF} c={cb} o={bIn} /> : null}
        {cIn > 0 ? <Photo src="assets/lockport-c1855-3200.jpg" iw={3200} ih={2159} f={LF} c={cc} o={cIn} /> : null}
        <Over f={LF}>
          <rect x={rx0} y={ry0} width={rx1 - rx0} height={ry1 - ry0} rx={6} fill="none" stroke={C.accent} strokeWidth={5} pathLength={1} strokeDasharray={`${ring} 2`} opacity={ring > 0 ? 1 : 0} />
          <g opacity={brk} stroke={C.accent} strokeWidth={5} fill="none" strokeLinecap="round">
            <line x1={bx} x2={bx} y1={by1} y2={by1 + (by0 - by1) * brk} />
            <line x1={bx - 14} x2={bx + 14} y1={by1} y2={by1} />
            <line x1={bx - 14} x2={bx + 14} y1={by1 + (by0 - by1) * brk} y2={by1 + (by0 - by1) * brk} />
          </g>
          {ul.length > 1 ? <polyline points={ul.join(' ')} fill="none" stroke={C.accent} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" /> : null}
        </Over>
        <Chip x={(rx0 + rx1) / 2} y={ry0 - 12} ay={-100} o={ramp(t, tRing, tRing + 0.5) * (1 - bIn)}>two staircases</Chip>
        <Chip x={(rx0 + rx1) / 2} y={ry1 + 14} ay={0} o={ramp(t, tFive, tFive + 0.5) * (1 - bIn)}>five locks each</Chip>
        <Chip x={bx + 22} y={(by0 + by1) / 2} ax={0} o={ramp(t, tSixty, tSixty + 0.5) * (1 - bIn)}>about 60 ft</Chip>
        <Chip x={rx0 - 16} y={(ry0 + ry1) / 2} ax={-100} o={ramp(t, tUpDown + 0.3, tUpDown + 0.9) * (1 - bIn)}><Arrow up />boats up<span style={{opacity: 0.5}}>·</span><Arrow up={false} />boats down</Chip>
        <Chip x={mb.X(700)} y={mb.Y(1000)} o={ramp(t, tRock, tRock + 0.5) * (1 - cIn)}>solid rock</Chip>
        <Chip x={mb.X(1480)} y={mb.Y(1560)} size={36} solid o={ramp(t, tCut - 0.5, tCut) * (1 - cIn)}>the Deep Cut</Chip>
        <Chip x={mc.X(1680)} y={mc.Y(1735)} ay={0} o={ramp(t, tC + 0.7, tC + 1.1)}>lock gates</Chip>
        <Chip x={18} y={LF.h - 18} ax={0} ay={-100} size={32} solid o={ramp(t, tC + 0.2, tC + 0.6)}>c. 1855, after enlargement</Chip>
      </Frame>
      <Side left={1110} top={300} width={700} o={sideFade(sa)} kicker="Lockport, New York · 1825" head="Two staircases in the rock"
        body="Five locks each, side by side, lifting boats about sixty feet." tag="documented"
        credit="Lockport from Prospect Hill. Plate in Colden's Memoir of the canal celebration, 1825." plaque="From The New York Public Library · Public domain" />
      <Side left={1110} top={300} width={700} o={sideFade(sb)} kicker="Lockport, New York · 1825" head="The Deep Cut"
        body="A channel blasted through solid rock." tag="documented · sources disagree on its length"
        credit="Deep Cutting, Lockport. Plate in Colden's Memoir of the canal celebration, 1825." plaque="From The New York Public Library · Public domain" />
      <Side left={1110} top={300} width={700} o={sideFade(sc)} kicker="Lockport, New York · c. 1855" head="The gates, after enlargement"
        body="Lock gates at Lockport, after the canal was enlarged." tag="a later view, not the 1825 canal"
        credit="Lockport, N.Y. Engraving, Herrmann J. Meyer, New York, about 1855." plaque="Wikimedia Commons · Public domain" />
      <MiniMap at={LOCKPORT} />
    </Paper>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 3. The book, the vases and the plate (Colden's Memoir plate, MA-02, MA-03, MA-04), scene 'book'
// ---------------------------------------------------------------------------------------------------------------
const BP: Box = {left: 100, top: 150, w: 1120, h: 640};
const BookPage: React.FC<{t: number}> = ({t}) => {
  const [L0, L1, L2] = S.book.lines;
  const tWhole = at('book', 'whole book');
  const tLike = at('book', 'like this one');
  const tMerch = at('book', 'merchants');
  const tPair = at('book', 'a pair');
  const tThanks = at('book', 'in thanks');
  const tPlates = at('book', 'dinner plates');
  const tSold = at('book', 'sold them');
  const s1 = 1 - ramp(t, L1.from - 0.3, L1.from + 0.3); // book out as the vases come in
  const s2 = seg(t, L1.from, L2.from);
  const s3 = ramp(t, L2.from, L2.from + 0.35);
  const pos1 = ramp(t, L1.from - 0.3, L1.from + 0.5);
  const pos3 = ramp(t, L2.from - 0.3, L2.from + 0.5);

  // 1. Memoir plate, 3200 x 2404, shown at 852 x 640 in the middle of the panel.
  const f1: Box = {left: 134, top: 0, w: 852, h: 640};
  const c1 = track(t, [
    {at: S.book.start, cx: 1600, cy: 1202, vw: 3200},
    {at: tWhole, cx: 1600, cy: 1000, vw: 2600},
    {at: tLike + 0.5, cx: 900, cy: 1300, vw: 1700},
    {at: L1.from, cx: 1000, cy: 1350, vw: 1550, lin: true},
  ]);
  const stack = [0, 1, 2].map((i) => ramp(t, tWhole + i * 0.35, tWhole + 0.5 + i * 0.35));
  // 2. Two vases, each its own picture: 2978 x 3722 and 1688 x 2000, both 640 high.
  const fv1: Box = {left: 24, top: 0, w: 512, h: 640};
  const fv2: Box = {left: 556, top: 0, w: 540, h: 640};
  const cv1 = track(t, [
    {at: L1.from, cx: 1489, cy: 1861, vw: 2978},
    {at: tMerch, cx: 1489, cy: 1861, vw: 2800},
    {at: tMerch + 1.2, cx: 1560, cy: 3070, vw: 1250},
    {at: tPair + 0.6, cx: 1500, cy: 2200, vw: 2400},
    {at: L2.from, cx: 1489, cy: 1700, vw: 2200, lin: true},
  ]);
  const cv2 = track(t, [
    {at: L1.from, cx: 844, cy: 1000, vw: 1688},
    {at: tThanks, cx: 844, cy: 1000, vw: 1600},
    {at: L2.from, cx: 844, cy: 900, vw: 1250, lin: true},
  ]);
  const m1 = mapper(fv1, cv1);
  const inscr = ramp(t, tMerch + 0.9, tMerch + 1.6) * (1 - ramp(t, tPair + 0.2, tPair + 0.8));
  const [ix0, iy0, ix1, iy1] = [m1.X(1090), m1.Y(2980), m1.X(2030), m1.Y(3180)];
  // 3. The plate, 588 x 700: the photo part (x 25–560, y 88–612) shown at 600 x 600.
  const f3: Box = {left: 260, top: 20, w: 600, h: 600};
  const c3 = track(t, [
    {at: L2.from, cx: 292, cy: 350, vw: 540},
    {at: L2.to, cx: 290, cy: 335, vw: 410, lin: true},
  ]);
  const quote = 'The Grand Erie Canal, a splendid monument of the enterprise & resources of the State of New York…';
  const typed = Math.floor(quote.length * clamp((t - tPlates) / (tSold + 1.2 - tPlates)));
  const full = '“' + quote + '”';
  const nShown = t < tPlates ? 0 : typed >= quote.length ? full.length : typed + 1;
  const [shown, hidden] = [full.slice(0, nShown), full.slice(nShown)];
  return (
    <Paper>
      <div style={{position: 'absolute', left: BP.left, top: BP.top, width: BP.w, height: BP.h, overflow: 'hidden', outline: `1px solid ${C.rule}`, background: '#E6DECD'}}>
        {/* 1: the book — three pages peek out behind the plate */}
        <div style={{position: 'absolute', inset: 0, opacity: s1}}>
          {[2, 1, 0].map((i) => (
            <div key={i} style={{position: 'absolute', left: f1.left + 10 + (i + 1) * 12 * stack[i], top: f1.top + 8 + (i + 1) * 8 * stack[i], width: f1.w - 20, height: f1.h - 16, background: i % 2 ? '#F4EEE0' : '#EAE2CF', outline: `1px solid ${C.rule}`, opacity: stack[i]}} />
          ))}
          <div style={{position: 'absolute', left: f1.left, top: f1.top, width: f1.w, height: f1.h, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
            <Photo src="assets/met-347709-memoir-1825-3200.jpg" iw={3200} ih={2404} f={f1} c={c1} />
          </div>
          <Chip x={f1.left + 18} y={f1.top + f1.h - 18} ax={0} ay={-100} o={ramp(t, tLike, tLike + 0.6)}>a plate from the book</Chip>
        </div>
        {/* 2: the vases */}
        {pos1 > 0 && 1 - pos3 > 0 ? (
          <div style={{position: 'absolute', inset: 0, opacity: pos1 * (1 - pos3)}}>
            <div style={{position: 'absolute', left: fv1.left - (1 - pos1) * 60, top: 0, width: fv1.w, height: fv1.h, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
              <Photo src="assets/met-6778-vase-1824.jpg" iw={2978} ih={3722} f={fv1} c={cv1} />
              <Over f={fv1}>
                <rect x={ix0} y={iy0} width={ix1 - ix0} height={iy1 - iy0} rx={5} fill="none" stroke={C.accent} strokeWidth={4} pathLength={1} strokeDasharray={`${inscr} 2`} opacity={inscr > 0 ? 1 : 0} />
              </Over>
              <Chip x={fv1.w / 2} y={fv1.h - 16} ay={-100} size={28} o={inscr}>“The Merchants of Pearl Street”</Chip>
            </div>
            <div style={{position: 'absolute', left: fv2.left + (1 - pos1) * 60, top: 0, width: fv2.w, height: fv2.h, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
              <Photo src="assets/met-6779-vase-1825.jpg" iw={1688} ih={2000} f={fv2} c={cv2} />
            </div>
            <Chip x={fv1.left + 14} y={14} ax={0} ay={0} o={ramp(t, L1.from + 0.6, L1.from + 1.1)}>1824</Chip>
            <Chip x={fv2.left + 14} y={14} ax={0} ay={0} o={ramp(t, L1.from + 0.9, L1.from + 1.4)}>1825</Chip>
          </div>
        ) : null}
        {/* 3: the plate */}
        {pos3 > 0 ? (
          <div style={{position: 'absolute', inset: 0, opacity: pos3}}>
            <div style={{position: 'absolute', left: f3.left, top: f3.top, width: f3.w, height: f3.h, overflow: 'hidden', outline: `1px solid ${C.rule}`}}>
              <Photo src="assets/met-5963-plate-clinton-eulogy.jpg" iw={588} ih={700} f={f3} c={c3} />
            </div>
            <Chip x={f3.left + 16} y={f3.top + f3.h - 16} ax={0} ay={-100} o={ramp(t, L2.from + 0.2, L2.from + 0.8)}>English plate · about 1828–1830</Chip>
          </div>
        ) : null}
      </div>
      <Side left={1270} top={300} width={590} o={{all: s1}} kicker="Colden's Memoir · 1825" head="A book of the celebration"
        body="A book about the canal celebration, with pictures." tag="documented"
        credit="Plate from Colden's Memoir of the canal celebration, 1825. The Met, object 347709." plaque="The Met · Public domain" />
      <Side left={1270} top={300} width={590} o={{all: s2, body: ramp(t, tMerch, tMerch + 0.5)}} kicker="Presentation vases · 1824, 1825" head="Silver, in thanks for the canal"
        body="A group of New York merchants commissioned the pair for Clinton." tag="documented · museum text"
        credit="Presentation Vase, Thomas Fletcher, 1824 (left) and 1825 (right). Silver." plaque="The Met · Public domain" />
      <Side left={1270} top={300} width={590} o={{all: s3}} kicker="Plate · about 1828–1830" head="The canal on dinner plates"
        body={<span style={{fontStyle: 'italic'}}>{shown}<span style={{opacity: 0}}>{hidden}</span></span>}
        tag="the museum's photo is black and white"
        credit="Plate honoring the Erie Canal and DeWitt Clinton, about 1828–1830. Printed earthenware." plaque="The Met · Public domain" />
      <MiniMap at={NYC} />
    </Paper>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 4. Freight rates before and after the canal, scene 'cheaper'
// ---------------------------------------------------------------------------------------------------------------
const RatesPage: React.FC<{t: number}> = ({t}) => {
  const [L0, L1] = S.cheaper.lines;
  const tFell = at('cheaper', 'fell by');
  const tNine = at('cheaper', 'nine tenths');
  const tWeeks = at('cheaper', 'weeks');
  const tNow = at('cheaper', 'now took');
  const tDays = at('cheaper', 'days');
  const [per0, per1] = [19.12, 1.68];
  const unit = 760 / per0;
  // Row A grows slowly for the whole first part of the sentence; the dollars count up after it.
  const grow = clamp((t - L0.from) / (tFell - 0.4 - L0.from));
  const aW = 760 * (1 - Math.pow(1 - grow, 2.2));
  const dollarsA = Math.round(98 * ramp(t, L0.from + 2.2, tFell - 0.3));
  // Row B starts at the full length and shrinks as the sentence says "fell".
  const fall = ramp(t, tFell - 0.1, tFell + 2.0);
  const bW = mix(760, per1 * unit, fall);
  const bVal = mix(per0, per1, fall);
  const bO = ramp(t, tFell - 0.5, tFell - 0.1);
  const dollarsB = Math.round(9 * ramp(t, tFell + 1.9, tFell + 2.5));
  const badge = ramp(t, tNine, tNine + 0.7);
  const weeks = ramp(t, tWeeks - 0.3, tWeeks + 0.5);
  const arrow = ramp(t, tNow, tNow + 0.8);
  const days = ramp(t, tDays, tDays + 0.6);
  // the wagon crawls along the whole time, the boat goes faster once "days" is said
  const wagon = 40 + 70 * clamp((t - S.cheaper.start) / (S.cheaper.end - S.cheaper.start));
  const boat = 40 + 200 * ramp(t, tDays, S.cheaper.end);
  return (
    <Paper>
      <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
        <rect width={1120} height={620} fill="#E6DECD" />
        <text x={60} y={66} style={{...label, fontSize: 28}} fill={C.ink}>Freight, Buffalo → New York · cost per ton-mile</text>
        {/* row A: 1817 */}
        <g opacity={ramp(t, S.cheaper.start + 0.2, S.cheaper.start + 0.8)}>
          <text x={60} y={128} style={{...label, fontSize: 30, fontWeight: 700}} fill={C.ink}>Before the canal · 1817</text>
          <rect x={60} y={146} width={Math.max(2, aW)} height={64} fill={C.ink} />
          <text x={60 + aW + 16} y={198} style={{...fraunces, fontSize: 52}} fill={C.ink} opacity={ramp(t, L0.from, L0.from + 0.8)}>{fmt(per0 * (aW / 760), 2)} ¢</text>
          <text x={60} y={250} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink} opacity={ramp(t, L0.from + 2.2, L0.from + 2.8)}>× 513 miles ≈ <tspan fontWeight={700}>${dollarsA}</tspan> for one ton</text>
        </g>
        {/* row B: after the canal */}
        <g opacity={bO}>
          <text x={60} y={318} style={{...label, fontSize: 30, fontWeight: 700}} fill={C.accent}>After the canal</text>
          <rect x={60} y={336} width={Math.max(2, bW)} height={64} fill={C.accent} />
          <text x={60 + bW + 16} y={388} style={{...fraunces, fontSize: 52}} fill={C.accent}>{fmt(bVal, 2)} ¢</text>
          <text x={60} y={440} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink} opacity={ramp(t, tFell + 1.9, tFell + 2.5)}>× 513 miles ≈ <tspan fontWeight={700}>${dollarsB}</tspan> for one ton</text>
        </g>
        <g opacity={badge} transform={`translate(${940},${330}) scale(${0.7 + 0.3 * badge})`}>
          <circle r={72} fill={C.accent} />
          <text y={4} textAnchor="middle" style={{...fraunces, fontSize: 54}} fill={C.paper}>≈ 11×</text>
          <text y={42} textAnchor="middle" style={{...label, fontSize: 24}} fill={C.paper}>less</text>
        </g>
        {/* weeks → days */}
        <line x1={60} x2={1060} y1={470} y2={470} stroke={C.rule} strokeWidth={1.5} opacity={weeks} />
        <g opacity={weeks}>
          <g transform={`translate(${wagon - 40},0)`}><Horse x={0} y={510} s={0.55} /></g>
          <text x={250} y={582} style={{...fraunces, fontSize: 70}} fill={C.ink}>weeks</text>
        </g>
        <path d={`M${480},${562} L${480 + 150 * arrow},${562}`} stroke={C.accent} strokeWidth={6} fill="none" strokeLinecap="round" opacity={arrow} />
        <path d="M-2,-14 L22,0 L-2,14 Z" transform={`translate(${630 + 150 * arrow - 150},562)`} fill={C.accent} opacity={arrow} />
        <g opacity={days}>
          <text x={700} y={582} style={{...fraunces, fontSize: 70}} fill={C.accent}>days</text>
          <g transform={`translate(${boat * 3.2 + 330},505) scale(0.9)`}><Boat x={0} y={0} /></g>
        </g>
      </svg>
      <Side left={1270} top={300} width={590} kicker="Freight, Buffalo to New York" head="About 11 times cheaper" tag="reconstructed: rates × 513 miles"
        credit="Rates: Klein and Matthews, European Review of Economic History, 2026. Distance: Colden, Memoir, 1825." plaque="Own drawing" />
    </Paper>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 5. Tolls against the cost of building, scene 'tolls'
// ---------------------------------------------------------------------------------------------------------------
const TollsPage: React.FC<{t: number}> = ({t}) => {
  const [L0, L1] = S.tolls.lines;
  const tSeven = at('tolls', 'seven million');
  const [x0, x1, ay] = [110, 1010, 360];
  const X = (yr: number) => x0 + ((yr - 1825) / 11) * (x1 - x0);
  // The marker runs 1825 -> 1836 over the second sentence at constant speed; each date appears as it passes.
  const go = clamp((t - L1.from) / (L1.to - 0.3 - L1.from));
  const yr = 1825 + 11 * go;
  const opened = ramp(t, L0.from, L0.from + 0.8);
  const passed = ramp(t, L1.from + (L1.to - 0.3 - L1.from) * ((1832 - 1825) / 11), L1.from + (L1.to - 0.3 - L1.from) * ((1832 - 1825) / 11) + 0.6);
  const seven = ramp(t, tSeven, tSeven + 0.7);
  const paid = ramp(t, L1.from + (L1.to - 0.3 - L1.from) * 0.97, L1.to);
  // coins flow from the boat to the state treasury all the time the page is open
  const flow = (t - S.tolls.start) / 2.4;
  const dots = Array.from({length: 9}, (_, i) => (flow + i / 9) % 1);
  return (
    <Paper>
      <svg width={1120} height={620} style={{position: 'absolute', left: 100, top: 150}}>
        <rect width={1120} height={620} fill="#E6DECD" />
        <text x={60} y={66} style={{...label, fontSize: 28}} fill={C.ink}>Canal tolls and the cost of building · 1825 → 1836</text>
        {/* boat → coins → state treasury */}
        <g opacity={ramp(t, S.tolls.start, L0.from + 0.4)}>
          <g transform="translate(60,112)"><Boat x={0} y={0} /></g>
          <line x1={180} x2={900} y1={150} y2={150} stroke={C.rule} strokeWidth={2} strokeDasharray="4 8" />
          {dots.map((u, i) => <circle key={i} cx={190 + u * 700} cy={150} r={8} fill={C.accent} opacity={Math.min(1, u * 6, (1 - u) * 6)} />)}
          <g transform="translate(920,92)" fill={C.ink}>
            <path d="M0,34 L50,0 L100,34 Z" />
            {[10, 32, 54, 76].map((x) => <rect key={x} x={x} y={42} width={14} height={44} />)}
            <rect x={0} y={92} width={100} height={10} />
          </g>
                    <text x={970} y={222} textAnchor="middle" style={{...label, fontSize: 22}} fill={C.ink}>State treasury</text>
        </g>
        {/* the timeline */}
        <line x1={x0} x2={x1} y1={ay} y2={ay} stroke={C.ink} strokeWidth={3} />
        <line x1={x0} x2={X(yr)} y1={ay} y2={ay} stroke={C.accent} strokeWidth={8} strokeLinecap="round" opacity={opened} />
        {Array.from({length: 12}, (_, i) => 1825 + i).map((v) => (
          <g key={v}>
            <line x1={X(v)} x2={X(v)} y1={ay - 9} y2={ay + 9} stroke={C.ink} strokeWidth={2} />
            <text x={X(v)} y={ay + 40} textAnchor="middle" style={{...label, fontSize: 21, letterSpacing: '0.06em'}} fill={C.ink}>{v}</text>
          </g>
        ))}
        <circle cx={X(yr)} cy={ay} r={13} fill={C.accent} stroke={C.paper} strokeWidth={3} opacity={opened} />
        {/* 1825 */}
        <g opacity={opened}>
          <line x1={X(1825)} x2={X(1825)} y1={ay - 12} y2={ay - 50} stroke={C.ink} strokeWidth={2} />
          <text x={X(1825) - 6} y={ay - 62} style={{fontFamily: F.label, fontSize: 30}} fill={C.ink}><tspan style={{...fraunces, fontSize: 44}}>1825</tspan>  the canal opens, end to end</text>
        </g>
        {/* 1832–33: tolls pass the cost */}
        <rect x={X(1832)} y={ay - 22} width={X(1833) - X(1832)} height={44} fill={C.accent} opacity={0.28 * passed} />
        <g opacity={passed}>
          <line x1={(X(1832) + X(1833)) / 2} x2={(X(1832) + X(1833)) / 2} y1={ay + 62} y2={ay + 88} stroke={C.accent} strokeWidth={3} />
          <text x={(X(1832) + X(1833)) / 2} y={ay + 120} textAnchor="middle" style={{fontFamily: F.label, fontSize: 31, fontWeight: 700}} fill={C.accent}>1832–33: total tolls pass the cost of building</text>
        </g>
        <g opacity={seven}>
          <text x={(X(1832) + X(1833)) / 2} y={ay + 190} textAnchor="middle" style={{...fraunces, fontSize: 60}} fill={C.ink}>about $7 million</text>
          <text x={(X(1832) + X(1833)) / 2} y={ay + 228} textAnchor="middle" style={{fontFamily: F.label, fontSize: 26}} fill={C.ink}>estimates: $6.9–7.7 million</text>
        </g>
        {/* 1836 */}
        <g opacity={paid}>
          <line x1={X(1836)} x2={X(1836)} y1={ay - 12} y2={ay - 50} stroke={C.ink} strokeWidth={2} />
          <text x={X(1836) + 40} y={ay - 62} textAnchor="end" style={{fontFamily: F.label, fontSize: 30}} fill={C.ink}><tspan style={{...fraunces, fontSize: 44}}>1836</tspan>  construction debt paid off</text>
        </g>
      </svg>
      <Side left={1270} top={300} width={590} kicker="Canal tolls · 1825–1836" head="Paid back in about a decade" tag="dated events only · no yearly toll figures"
        credit="Debt paid off by 1836: Whitford, History of the Canal System of the State of New York, 1906. Tolls passing the cost in 1832–33: canal toll tables." plaque="Own drawing" />
    </Paper>
  );
};

// ---------------------------------------------------------------------------------------------------------------
// 6. Why New York, South Street (MA-06), scene 'reasons'
// ---------------------------------------------------------------------------------------------------------------
const RF: Box = {left: 100, top: 150, w: 1000, h: 640};
const REASONS = [
  "deep, sheltered harbor",
  'Black Ball Line to Liverpool · from 1818',
  "state law favored New York's auctions",
  "Southern cotton through New York's merchants and banks",
];
const ReasonsPage: React.FC<{t: number}> = ({t}) => {
  const L = S.reasons.lines;
  const [t1, t2, t3, t4] = [L[1].from, L[2].from, L[3].from, L[4].from];
  // 3200 x 2241: the camera visits the harbor, the ships, the warehouses and the goods on the quay.
  const cam = track(t, [
    {at: S.reasons.start, cx: 1600, cy: 1120, vw: 3000},
    {at: t1, cx: 1500, cy: 1150, vw: 2700, lin: true},
    {at: t1 + 0.9, cx: 900, cy: 950, vw: 1700},
    {at: t2, cx: 950, cy: 1000, vw: 1550, lin: true},
    {at: t2 + 0.9, cx: 1300, cy: 1250, vw: 1700},
    {at: t3, cx: 1350, cy: 1280, vw: 1600, lin: true},
    {at: t3 + 0.9, cx: 2300, cy: 1100, vw: 1700},
    {at: t4, cx: 2350, cy: 1130, vw: 1600, lin: true},
    {at: t4 + 0.9, cx: 1500, cy: 1650, vw: 1800},
    {at: S.reasons.end, cx: 1450, cy: 1650, vw: 1650, lin: true},
  ]);
  const when = [t1, t2, t3, t4];
  const first = ramp(t, S.reasons.start, S.reasons.start + 0.6);
  return (
    <Paper>
      <Frame f={RF}>
        <Photo src="assets/met-10141-south-street-3200.jpg" iw={3200} ih={2241} f={RF} c={cam} />
      </Frame>
      <div style={{position: 'absolute', left: 1150, top: 150, width: 660, color: C.ink, opacity: first}}>
        <div style={{...label, fontSize: 27, opacity: 0.72}}>New York · about 1827</div>
        <div style={{...title, fontSize: 60, marginTop: 14}}>Not only the canal</div>
        <div style={{fontFamily: F.label, fontSize: 28, color: C.accent, marginTop: 16}}>a view about 1827, an illustration of the harbor</div>
      </div>
      {REASONS.map((r, i) => {
        const o = ramp(t, when[i], when[i] + 0.5);
        const lastO = o;
        return (
          <div key={r} style={{position: 'absolute', left: 1150 + (1 - o) * 40, top: 340 + i * 112, width: 660, opacity: lastO, display: 'flex', gap: 18, alignItems: 'flex-start'}}>
            <div style={{flex: 'none', width: 56, height: 56, borderRadius: 28, background: C.accent, color: C.paper, ...fraunces, fontSize: 34, textAlign: 'center', lineHeight: '56px'}}>{i + 1}</div>
            <div style={{fontFamily: F.label, fontSize: 38, lineHeight: 1.18, paddingTop: 2, color: C.ink, borderBottom: `3px solid ${C.accent}`, paddingBottom: 6}}>{r}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 1150, top: 810, width: 660, color: C.ink, opacity: first}}>
        <div style={{height: 1, background: C.rule, margin: '0 0 20px'}} />
        <div style={{fontFamily: F.label, fontSize: 27, lineHeight: 1.32}}>View of South Street, from Maiden Lane, New York City. William James Bennett, about 1827. Watercolor.</div>
        <div style={{display: 'inline-block', marginTop: 14, padding: '6px 12px', border: `1.5px solid ${C.ink}`, ...label, fontSize: 22, letterSpacing: '0.12em'}}>The Met · Public domain</div>
      </div>
      <MiniMap at={NYC} />
    </Paper>
  );
};

export const INSERTS_B: Ins[] = [
  {from: S.problem.voice - 0.4, to: S.problem.end, at: [-76.2, 43.1], render: (t) => <Doc1821Page t={t} />},
  {from: S.lockport.start, to: S.lockport.end, at: LOCKPORT, render: (t) => <LockportPage t={t} />},
  {from: S.book.start, to: S.book.end, at: NYC, render: (t) => <BookPage t={t} />},
  {from: S.cheaper.start, to: S.cheaper.end, at: BUFFALO, render: (t) => <RatesPage t={t} />},
  {from: S.tolls.start, to: S.tolls.end, at: ALBANY, render: (t) => <TollsPage t={t} />},
  {from: S.reasons.start, to: S.reasons.end, at: NYC, render: (t) => <ReasonsPage t={t} />},
];
````

## probe/src/theme.ts

````ts
// Palette and type of variant A, from docs/channel-concepts/moving-atlas/concept.md
// ("Палитра и типографика"). Sizes are for a 1920x1080 frame.
export const C = {
  water: '#C7D3D4',
  land: '#EFE9DC',
  relief: '#E2D3B5',
  ink: '#1E2A2F',
  accent: '#C4472C',
  force: '#3E6E8E',
  river: '#9DB2B6',
  paper: '#EFE9DC',
  rule: '#B9B2A3',
};

export const F = {
  title: 'Fraunces',
  label: 'PT Sans Narrow',
};

export const fontFiles = [
  {family: F.title, file: 'fonts/Fraunces.ttf', weight: '100 900'},
  {family: F.label, file: 'fonts/PTSansNarrow-Regular.ttf', weight: '400'},
  {family: F.label, file: 'fonts/PTSansNarrow-Bold.ttf', weight: '700'},
];

export const W = 1920;
export const H = 1080;
export const FPS = 30;
````

## probe/bun.lock

````
{
  "lockfileVersion": 2,
  "configVersion": 1,
  "workspaces": {
    "": {
      "name": "moving-atlas-probe",
      "dependencies": {
        "@remotion/cli": "4.0.507",
        "d3-geo": "3.1.1",
        "react": "19.2.8",
        "react-dom": "19.2.8",
        "remotion": "4.0.507",
      },
      "devDependencies": {
        "@types/d3-contour": "3.0.6",
        "@types/d3-geo": "3.1.0",
        "@types/react": "19.2.14",
        "d3-contour": "4.0.2",
        "typescript": "5.9.3",
      },
    },
  },
  "packages": {
    "@babel/code-frame": ["@babel/code-frame@7.29.7", "", { "dependencies": { "@babel/helper-validator-identifier": "^7.29.7", "js-tokens": "^4.0.0", "picocolors": "^1.1.1" } }, "sha512-Aup7aUOfpbAUg2ROOJN6Iw5f9DMBlzu0mIkm/malLQFN/YQgO48wCj0Kxa3sEHJvPVFg7siR+qRInwXd2qhQKw=="],

    "@babel/compat-data": ["@babel/compat-data@7.29.7", "", {}, "sha512-locTkQyKvwIEgBzVrn8693ebc97F2U8ZHjbXwDXJ5Fn2TCpNwTlKcaKLkdHop5c/icOFE7qt7Q9JC5hnKNa6Gg=="],

    "@babel/core": ["@babel/core@7.29.7", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/generator": "^7.29.7", "@babel/helper-compilation-targets": "^7.29.7", "@babel/helper-module-transforms": "^7.29.7", "@babel/helpers": "^7.29.7", "@babel/parser": "^7.29.7", "@babel/template": "^7.29.7", "@babel/traverse": "^7.29.7", "@babel/types": "^7.29.7", "@jridgewell/remapping": "^2.3.5", "convert-source-map": "^2.0.0", "debug": "^4.1.0", "gensync": "^1.0.0-beta.2", "json5": "^2.2.3", "semver": "^6.3.1" } }, "sha512-RgHBCvtjbOK2gXSNBNIkNoEc9qoVEtau3hj8gEqKQuL3HZAibKarWFEI3Lfm6EYKkLalOh8eSrj9b+ch9H/VBA=="],

    "@babel/generator": ["@babel/generator@7.29.8", "", { "dependencies": { "@babel/parser": "^7.29.8", "@babel/types": "^7.29.8", "@jridgewell/gen-mapping": "^0.3.12", "@jridgewell/trace-mapping": "^0.3.28", "jsesc": "^3.0.2" } }, "sha512-gZbepsdh3WDtgZKWL+vTPh71LSBrm/Y4/QDZBVCcYfmeTEEuoOYwlSy+G1StfJg+/Zy550u/3TATbm7qDbbMtg=="],

    "@babel/helper-compilation-targets": ["@babel/helper-compilation-targets@7.29.7", "", { "dependencies": { "@babel/compat-data": "^7.29.7", "@babel/helper-validator-option": "^7.29.7", "browserslist": "^4.24.0", "lru-cache": "^5.1.1", "semver": "^6.3.1" } }, "sha512-wem6WaBj4NaVYVdNhLPPVacES6ZJ+KBBfSkTMD3YZxbP3rm3Di85tJU5ljaUNhaOynt+Aj0xruhYuzQBt8n71g=="],

    "@babel/helper-globals": ["@babel/helper-globals@7.29.7", "", {}, "sha512-3nQVUAtvkKH9zahfWgw96Jc/uFOmjACE1kQz82E2lqWmHBgjzbNlsC22nuQTfahmWeQtTq5nQ/4Nnd2A1wj4zA=="],

    "@babel/helper-module-imports": ["@babel/helper-module-imports@7.29.7", "", { "dependencies": { "@babel/traverse": "^7.29.7", "@babel/types": "^7.29.7" } }, "sha512-ejHwrQQYcm9xnTivShn2IDOlIzInN34AXskvq9QicvCtEzq1Vzclu/tKF8Jq1Cg8JG2GL6/EmjgsCT7lXepE3g=="],

    "@babel/helper-module-transforms": ["@babel/helper-module-transforms@7.29.7", "", { "dependencies": { "@babel/helper-module-imports": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7", "@babel/traverse": "^7.29.7" }, "peerDependencies": { "@babel/core": "^7.0.0" } }, "sha512-UPUVSyXbOh627KiCIGQSgwWzGeBKLkaJ9PJEdrngIwMSzxLR4jS4+f1f1jb7VzBbg8nFLaYotvVPFCTqdrmTAg=="],

    "@babel/helper-string-parser": ["@babel/helper-string-parser@7.29.7", "", {}, "sha512-Pb5ijPrZ89GDH8223L4UP8i6QApWxs04RbPQJTeWDV0/keR2E36MeKnyr6LYmUUvqRRI+Iv87SuF1W6ErINzYw=="],

    "@babel/helper-validator-identifier": ["@babel/helper-validator-identifier@7.29.7", "", {}, "sha512-qehxGkRj55h/ff8EMaJ+cYhyaKlHIxqYDn682wQD7RNp9UujOQsHog2uS0r2vzr4pW+sXf90NeeayjcNaX3fFg=="],

    "@babel/helper-validator-option": ["@babel/helper-validator-option@7.29.7", "", {}, "sha512-N9ZErrD+yW5geCDtBqnOoxmR8+tNKiGuxKlDpuJxfsqpa2dFcexaziGAE/qoHLiDDreVNMupxGmSoNlyvsA3gw=="],

    "@babel/helpers": ["@babel/helpers@7.29.10", "", { "dependencies": { "@babel/template": "^7.29.7", "@babel/types": "^7.29.8" } }, "sha512-EMCx3AGZ3WfAl6ht7AyQoPm2Lh+BGYEMdc4Q6Hf7uSCDOZFuLq44qNwL+iaim8VlyYhRAo4X43+weadK8ZB4Yg=="],

    "@babel/parser": ["@babel/parser@7.24.1", "", { "bin": "./bin/babel-parser.js" }, "sha512-Zo9c7N3xdOIQrNip7Lc9wvRPzlRtovHVE4lkz8WEDr7uYh/GMQhSiIgFxGIArRHYdJE5kxtZjAf8rT0xhdLCzg=="],

    "@babel/template": ["@babel/template@7.29.7", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/parser": "^7.29.7", "@babel/types": "^7.29.7" } }, "sha512-puq+Gf35oI24FeN11LkoUQFqv9uwNeWpxXZi/Ji3rRIoKAzKnxRaZ+Gkj0vKS9ZCiTESfng1N9LyOyXvo+m+Gg=="],

    "@babel/traverse": ["@babel/traverse@7.29.10", "", { "dependencies": { "@babel/code-frame": "^7.29.7", "@babel/generator": "^7.29.8", "@babel/helper-globals": "^7.29.7", "@babel/parser": "^7.29.9", "@babel/template": "^7.29.7", "@babel/types": "^7.29.8", "debug": "^4.3.1" } }, "sha512-B3lYAs2nkKskbgQ1nfy8Ma9ao9Q1rntTAQHrzzyDuj+TSO+X3le6PfWwqDvodsb+OumE10eMFfuMCTQSQ5iuIQ=="],

    "@babel/types": ["@babel/types@7.24.0", "", { "dependencies": { "@babel/helper-string-parser": "^7.23.4", "@babel/helper-validator-identifier": "^7.22.20", "to-fast-properties": "^2.0.0" } }, "sha512-+j7a5c253RfKh8iABBhywc8NSfP5LURe7Uh4qpsh6jc+aLJguvmIUBdjSdEMQv2bENrCR5MfRdjGo7vzS/ob7w=="],

    "@emnapi/core": ["@emnapi/core@1.11.3", "", { "dependencies": { "@emnapi/wasi-threads": "1.2.3", "tslib": "^2.4.0" } }, "sha512-zLpS5asjEb7lq8jYLq37N6XKaE41DIexlY1rF/z4/tIl3wo13Sqm28fRyfIsKZD+NZ8mM5RoKkpW/rBcuoSZSg=="],

    "@emnapi/runtime": ["@emnapi/runtime@1.11.3", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-Xz4Tpyki7XyrpbUK1jR1AhdAdaXyhhY4lZ3neLodmhpuWfy2PAQN5B46sAiU4liOXGLkHypn/qU+jvfWSCYYLA=="],

    "@emnapi/wasi-threads": ["@emnapi/wasi-threads@1.2.3", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-ELEBe8PsLvvJ6QMr0zLt8ffvOHW/dc1m3CEzNMg7aJUv3bMaoDtw2TXyDAwkYBuroxxuHEwhRTLJSe5sya547g=="],

    "@esbuild/aix-ppc64": ["@esbuild/aix-ppc64@0.28.1", "", { "os": "aix", "cpu": "ppc64" }, "sha512-Svl7tq8k/08+p6CXPpRjQ1fKX+1odH/BQbb48fV6fj3CWHhsoIOoY87w1oHXm0qEpkIK3ZfVgp0hed3XBXzXMQ=="],

    "@esbuild/android-arm": ["@esbuild/android-arm@0.28.1", "", { "os": "android", "cpu": "arm" }, "sha512-0k2F129Xdio1TdJfzJ8sy1Q47vUD2NnwdhiAf7drUN1EBTfPf4hsFCtmMgu/6m8JSzsBrlmVjudMBQqOfG8usQ=="],

    "@esbuild/android-arm64": ["@esbuild/android-arm64@0.28.1", "", { "os": "android", "cpu": "arm64" }, "sha512-34EGEbCIAgosYz6goLcopX6Mo7NyGv9tfwEM2/7Ce2VcVRk568iSvniGWcUXIy7wEDR1wzolcxcriFVrWYcwBg=="],

    "@esbuild/android-x64": ["@esbuild/android-x64@0.28.1", "", { "os": "android", "cpu": "x64" }, "sha512-dbwY7ltSMDWsRatcRpCnES4F+im88OCUgGZjy52shC7GqHRE/cYlxNbB4Z4UpJswpcc4Qxd2oE/ufM0p61IKng=="],

    "@esbuild/darwin-arm64": ["@esbuild/darwin-arm64@0.28.1", "", { "os": "darwin", "cpu": "arm64" }, "sha512-TZbWkQY7kvTAXbXUT7uVACR5cMHsDiSz9z7ZKAX/RTq/WJEk3QyRr0wZpNhBDX+/0CtdqUIJlOiodQcta6tY3Q=="],

    "@esbuild/darwin-x64": ["@esbuild/darwin-x64@0.28.1", "", { "os": "darwin", "cpu": "x64" }, "sha512-zfdzgK9ACBNZLI/CyHTOx81SyNbM6YXn7rxSgX97VjyiPl9W1i4Ka4fgKECEoFCKGpvBj5qArWIGgQjOwkgskQ=="],

    "@esbuild/freebsd-arm64": ["@esbuild/freebsd-arm64@0.28.1", "", { "os": "freebsd", "cpu": "arm64" }, "sha512-wG2EA8ENdEI0qhkSZMjfqrdY+ziCYCPMmtZjjIwOmXFjmyzEHn+UUxk5of+SYsjtfs3VpnlC7QLzSI5hY/rOAw=="],

    "@esbuild/freebsd-x64": ["@esbuild/freebsd-x64@0.28.1", "", { "os": "freebsd", "cpu": "x64" }, "sha512-i7dZ9vQgnvSCzi/rYCXNgtF/U+eKZNJBzu3eTQbRgHnM7tNSizLOkRFAl3qzVc/Op/u5YkHHa4pf/3DOYHthLQ=="],

    "@esbuild/linux-arm": ["@esbuild/linux-arm@0.28.1", "", { "os": "linux", "cpu": "arm" }, "sha512-qVXBOHQS+d5Y722GwJzJUtOLlX7km3CraOaGormF1pDtPd2C/l1SHRPgjLunLGe51Sh5YYWKMFDyV4SxgMQYTQ=="],

    "@esbuild/linux-arm64": ["@esbuild/linux-arm64@0.28.1", "", { "os": "linux", "cpu": "arm64" }, "sha512-yHs+0uc8+nvEAfAfxrWQKK5peSNzBc4PegcMO0EJ2hT71uA7vB8Ihg2e77R2P7SG5uYjPbHlLLmve4LLLRCf0g=="],

    "@esbuild/linux-ia32": ["@esbuild/linux-ia32@0.28.1", "", { "os": "linux", "cpu": "ia32" }, "sha512-d1z4ZuP0ajrfz/FhGT4vv278rX8KnPPJx8i5+AtK7TYbx9Le9F1hyzurZpkEyjkGa9dUGhQow4C1NmeGvqxN2w=="],

    "@esbuild/linux-loong64": ["@esbuild/linux-loong64@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-M5sRjUVZrkm1OAPR3dlOYzNmN+loZKGVi1VUQGrwuqLcbR6qeAz+famMhjASeH3YVKvZz+zT1jlh/keC3Rj/lg=="],

    "@esbuild/linux-mips64el": ["@esbuild/linux-mips64el@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-mRObBZeHh2OxcBFPWE/FjylkRgZdYuiTR3vaTozquCGOH14iP9oN4x4Ge81CoIDYQrXmIxpFumJBu5MtZpnQJQ=="],

    "@esbuild/linux-ppc64": ["@esbuild/linux-ppc64@0.28.1", "", { "os": "linux", "cpu": "ppc64" }, "sha512-slScBsMAb3GFDcdrCgLwZtPYRoH2H/youv10QiZyRjmsP48fznoveWytSgCI/R0ZcUgpc0ZhIUEx6LHts8yrfQ=="],

    "@esbuild/linux-riscv64": ["@esbuild/linux-riscv64@0.28.1", "", { "os": "linux", "cpu": "none" }, "sha512-kw0owk1o0GFETUJyW0jc0G4Yzs0BHZn0JDZ8JRT088vjJYX777BAs1fDGxAC+q831qOs2DTC96mNsG2opdfyyQ=="],

    "@esbuild/linux-s390x": ["@esbuild/linux-s390x@0.28.1", "", { "os": "linux", "cpu": "s390x" }, "sha512-/lAIjX8aYFRByhh6L5rYtPEDRqa9de/4V/juOXcta5frjvzXO4/sqEtyytse0g3zZFuWu5cDN0MkLz2qRDD2Ag=="],

    "@esbuild/linux-x64": ["@esbuild/linux-x64@0.28.1", "", { "os": "linux", "cpu": "x64" }, "sha512-u/anNYF2mmVOEDwLtnQ1wOr3EZ9sTNGLWrsYGYwHWzGA3Si84IOkHXlbWTD1NB+9/1lcnweYKO54uhxZydNzfA=="],

    "@esbuild/netbsd-arm64": ["@esbuild/netbsd-arm64@0.28.1", "", { "os": "none", "cpu": "arm64" }, "sha512-oks0DYbLwWMmaakTsCb+zL4E+aHRVLom9IJZOAthMQEPiQmydXHkziYEsGYRx0uNV/IjEKGAV941JzH02pflqw=="],

    "@esbuild/netbsd-x64": ["@esbuild/netbsd-x64@0.28.1", "", { "os": "none", "cpu": "x64" }, "sha512-aeL6lAnN89Hz43Mlh1G8ARasbuoYvSITDEx0tHh5b7jJnHcssqgjy9Yx430GDpmCa6OyrKoS0aNRjKundRizGg=="],

    "@esbuild/openbsd-arm64": ["@esbuild/openbsd-arm64@0.28.1", "", { "os": "openbsd", "cpu": "arm64" }, "sha512-MEFJe5C3R8pwXdZ5Y21oo6m7ePiS0d9pWucn99O/wvyJZChoIQKrQDxKrGeW8F5+T0okTHesAmDeiHDTIq0V/Q=="],

    "@esbuild/openbsd-x64": ["@esbuild/openbsd-x64@0.28.1", "", { "os": "openbsd", "cpu": "x64" }, "sha512-i/ZLIOafE0Z8cI/XANJAixoJL/uRAoS2xOA3rb0xN+KK0K177cMAsQYkzHtBrtMXAKuAc7HGgcWiZ/sRC1Nxgw=="],

    "@esbuild/openharmony-arm64": ["@esbuild/openharmony-arm64@0.28.1", "", { "os": "none", "cpu": "arm64" }, "sha512-ge+Z7EXFNt2BO1oAMsVpiQ8EwndV9i1xXerAeTIK7AtPs3bKFXQM7nlRxDSIUIMeueR1CNXxqztLzdNeReKBJg=="],

    "@esbuild/sunos-x64": ["@esbuild/sunos-x64@0.28.1", "", { "os": "sunos", "cpu": "x64" }, "sha512-BEjgtECkL3vY+SaSQ6nzVfiALUeFxpawyp8Jmf5PtYhf1Ug40N1h/hxlhts+f1FvSvarEigdxS3BlSMI2PJLcQ=="],

    "@esbuild/win32-arm64": ["@esbuild/win32-arm64@0.28.1", "", { "os": "win32", "cpu": "arm64" }, "sha512-lCv9eK/H6ZJWbE7bh2nw54CZ9M2nupBxJcTsdk/QQnWkdSjKGuxmmH8/GWrlT1eMmZfn4dGcCjRte397WqfQXA=="],

    "@esbuild/win32-ia32": ["@esbuild/win32-ia32@0.28.1", "", { "os": "win32", "cpu": "ia32" }, "sha512-zvb/mB2bSCoJOpoCBgYKKpX6YM6mJBlBUVUtVj41DlZJVEB6/0CKlRYxP5wWl1C1ILiCoAU5wZZ4q1P3qeS6Eg=="],

    "@esbuild/win32-x64": ["@esbuild/win32-x64@0.28.1", "", { "os": "win32", "cpu": "x64" }, "sha512-bm4Mowrv+GXMlpWX++EcXw/iLyd1o3+bJkC2DkWXYVvgZCqD/bSj9ctZeAMC3cIxgjRVR2Dufaiu4YPxr5gW1A=="],

    "@jridgewell/gen-mapping": ["@jridgewell/gen-mapping@0.3.13", "", { "dependencies": { "@jridgewell/sourcemap-codec": "^1.5.0", "@jridgewell/trace-mapping": "^0.3.24" } }, "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA=="],

    "@jridgewell/remapping": ["@jridgewell/remapping@2.3.5", "", { "dependencies": { "@jridgewell/gen-mapping": "^0.3.5", "@jridgewell/trace-mapping": "^0.3.24" } }, "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ=="],

    "@jridgewell/resolve-uri": ["@jridgewell/resolve-uri@3.1.2", "", {}, "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw=="],

    "@jridgewell/source-map": ["@jridgewell/source-map@0.3.11", "", { "dependencies": { "@jridgewell/gen-mapping": "^0.3.5", "@jridgewell/trace-mapping": "^0.3.25" } }, "sha512-ZMp1V8ZFcPG5dIWnQLr3NSI1MiCU7UETdS/A0G8V/XWHvJv3ZsFqutJn1Y5RPmAPX6F3BiE397OqveU/9NCuIA=="],

    "@jridgewell/sourcemap-codec": ["@jridgewell/sourcemap-codec@1.6.0", "", {}, "sha512-T7jf+5zgsZHwNJ4lvQ7/aezbyk0nNX+zJVWpmHA7VYsEx7a7qr5Rg5IbtJFqkgze5Y2sruq1RUY8Q837Od7iFw=="],

    "@jridgewell/trace-mapping": ["@jridgewell/trace-mapping@0.3.31", "", { "dependencies": { "@jridgewell/resolve-uri": "^3.1.0", "@jridgewell/sourcemap-codec": "^1.4.14" } }, "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw=="],

    "@mediabunny/aac-encoder": ["@mediabunny/aac-encoder@1.50.8", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-A5Se/LZd6RmYq/h36lBMSEsHvsyW8d0toR7FrAwpsFYbK+DVQYf90KiBT1Aw/mzLXx8/ypIOORJnd1sVZqOvJQ=="],

    "@mediabunny/flac-encoder": ["@mediabunny/flac-encoder@1.50.8", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-4cfN03SbEoQaG+eBeYFUAb1R1ALaAHzf43dXFzQTr/oO5ueqzTgBoG3coKrIvBaAMU7Vv36mrBKLX8bvTppdAQ=="],

    "@mediabunny/mp3-encoder": ["@mediabunny/mp3-encoder@1.50.8", "", { "peerDependencies": { "mediabunny": "^1.0.0" } }, "sha512-eBT/H30tTu8AmZXqZ5RTpJ9VmwVlwednajuOrrWp0GS6cbGXsGMQ60Qvr3ZMIE0QDiadlEzb8/ozR+doP+MC1g=="],

    "@module-federation/error-codes": ["@module-federation/error-codes@0.22.0", "", {}, "sha512-xF9SjnEy7vTdx+xekjPCV5cIHOGCkdn3pIxo9vU7gEZMIw0SvAEdsy6Uh17xaCpm8V0FWvR0SZoK9Ik6jGOaug=="],

    "@module-federation/runtime": ["@module-federation/runtime@0.22.0", "", { "dependencies": { "@module-federation/error-codes": "0.22.0", "@module-federation/runtime-core": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-38g5iPju2tPC3KHMPxRKmy4k4onNp6ypFPS1eKGsNLUkXgHsPMBFqAjDw96iEcjri91BrahG4XcdyKi97xZzlA=="],

    "@module-federation/runtime-core": ["@module-federation/runtime-core@0.22.0", "", { "dependencies": { "@module-federation/error-codes": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-GR1TcD6/s7zqItfhC87zAp30PqzvceoeDGYTgF3Vx2TXvsfDrhP6Qw9T4vudDQL3uJRne6t7CzdT29YyVxlgIA=="],

    "@module-federation/runtime-tools": ["@module-federation/runtime-tools@0.22.0", "", { "dependencies": { "@module-federation/runtime": "0.22.0", "@module-federation/webpack-bundler-runtime": "0.22.0" } }, "sha512-4ScUJ/aUfEernb+4PbLdhM/c60VHl698Gn1gY21m9vyC1Ucn69fPCA1y2EwcCB7IItseRMoNhdcWQnzt/OPCNA=="],

    "@module-federation/sdk": ["@module-federation/sdk@0.22.0", "", {}, "sha512-x4aFNBKn2KVQRuNVC5A7SnrSCSqyfIWmm1DvubjbO9iKFe7ith5niw8dqSFBekYBg2Fwy+eMg4sEFNVvCAdo6g=="],

    "@module-federation/webpack-bundler-runtime": ["@module-federation/webpack-bundler-runtime@0.22.0", "", { "dependencies": { "@module-federation/runtime": "0.22.0", "@module-federation/sdk": "0.22.0" } }, "sha512-aM8gCqXu+/4wBmJtVeMeeMN5guw3chf+2i6HajKtQv7SJfxV/f4IyNQJUeUQu9HfiAZHjqtMV5Lvq/Lvh8LdyA=="],

    "@napi-rs/wasm-runtime": ["@napi-rs/wasm-runtime@1.0.7", "", { "dependencies": { "@emnapi/core": "^1.5.0", "@emnapi/runtime": "^1.5.0", "@tybys/wasm-util": "^0.10.1" } }, "sha512-SeDnOO0Tk7Okiq6DbXmmBODgOAb9dp9gjlphokTUxmt8U3liIP1ZsozBahH69j/RJv+Rfs6IwUKHTgQYJ/HBAw=="],

    "@remotion/bundler": ["@remotion/bundler@4.0.507", "", { "dependencies": { "@remotion/media-parser": "4.0.507", "@remotion/studio": "4.0.507", "@remotion/studio-shared": "4.0.507", "@remotion/timeline-utils": "4.0.507", "@rspack/core": "1.7.11", "@rspack/plugin-react-refresh": "1.6.1", "css-loader": "7.1.4", "esbuild": "0.28.1", "react-refresh": "0.18.0", "remotion": "4.0.507", "style-loader": "4.0.0", "webpack": "5.105.0" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-SECbwvydNg9XgHcKQkiiYQM92v4FHBADpTb5xlyGROWQ4qA1wySYdDfdMmd0WVQfCV1Zi9JPRDQAW8nDBW33VQ=="],

    "@remotion/captions": ["@remotion/captions@4.0.507", "", {}, "sha512-mS2fe1nbofJQ5vEc6dV1zJpZ06QUmKj1zqRv1TLyACQmlr8O63IP3NTAqhBQSfLYX7Kad6+83Vt2huv+PgM/+w=="],

    "@remotion/cli": ["@remotion/cli@4.0.507", "", { "dependencies": { "@babel/parser": "7.24.1", "@remotion/bundler": "4.0.507", "@remotion/media-utils": "4.0.507", "@remotion/player": "4.0.507", "@remotion/renderer": "4.0.507", "@remotion/studio": "4.0.507", "@remotion/studio-server": "4.0.507", "@remotion/studio-shared": "4.0.507", "dotenv": "17.3.1", "minimist": "1.2.6", "prompts": "2.4.2", "remotion": "4.0.507", "semver": "7.5.3" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" }, "bin": { "remotion": "remotion-cli.js", "remotionb": "remotionb-cli.js", "remotiond": "remotiond-cli.js" } }, "sha512-A53RU54y2wf7T00X0wcFOGoa4Dvjqc3VJFi+BgwWWtlSGsPvEmkXLsrly31GpZMXqXE1LU4IeDj1YoajY/GBOQ=="],

    "@remotion/compositor-darwin-arm64": ["@remotion/compositor-darwin-arm64@4.0.507", "", { "os": "darwin", "cpu": "arm64" }, "sha512-MNvUNS33X3YCwalX+LbGcYXXxkWnOspX2vB7agzkHE/IKSFAG58sF9iXyp+rn6lJmCjBcaUxO7paJFxfAzjwEw=="],

    "@remotion/compositor-darwin-x64": ["@remotion/compositor-darwin-x64@4.0.507", "", { "os": "darwin", "cpu": "x64" }, "sha512-oz8Wjq42oKZwhTc2N20tBMXx7Ts3K5T+cQH6oo5PEyFgrpx1j5Lm2AQTsunlgiMhOda20Vff0ZLeiXVUR+xtuA=="],

    "@remotion/compositor-linux-arm64-gnu": ["@remotion/compositor-linux-arm64-gnu@4.0.507", "", { "os": "linux", "cpu": "arm64" }, "sha512-K6PCQwPE2wJlV5/nat6UrRVx7XCk5LgCRV4cQsIXyYDCvo7995KMI4KgP4DtKXcvXaQUudz9r9JuFT+KGktPwA=="],

    "@remotion/compositor-linux-arm64-musl": ["@remotion/compositor-linux-arm64-musl@4.0.507", "", { "os": "linux", "cpu": "arm64" }, "sha512-hKgdJm+dGcxUs/GNajUa2uH6RnphjKVvz+zLWWLdRhgPzxvPhm4ZJm9VPoyr1hmY3c84ws5qiXV30AkHtZVIVA=="],

    "@remotion/compositor-linux-x64-gnu": ["@remotion/compositor-linux-x64-gnu@4.0.507", "", { "os": "linux", "cpu": "x64" }, "sha512-5w9iYYlfp0qLohFMAAyHPR00NxiQ3SuhJyx6ck+z9pkLZLgTAKC7EWB0e8HMaC6czxPAH1F+ZbXeA1ukfM7SOQ=="],

    "@remotion/compositor-linux-x64-musl": ["@remotion/compositor-linux-x64-musl@4.0.507", "", { "os": "linux", "cpu": "x64" }, "sha512-tnieQCpBZ1uSL6z9Dk3noNwYG6wGIH3WZpMfRQZgrInJ4LhmRSzzIFx6Bb2l9QZGAkIiGKFadDFHlw0JVsJd1A=="],

    "@remotion/compositor-win32-x64-msvc": ["@remotion/compositor-win32-x64-msvc@4.0.507", "", { "os": "win32", "cpu": "x64" }, "sha512-FCkZDLcPBCO2WO/MyrtMB5tpsIuqqkc7E1nY2lfY6WmRX2quGfykcsz4S9inYx/G+XybKVTgplqnyLtt9wyFnw=="],

    "@remotion/licensing": ["@remotion/licensing@4.0.507", "", {}, "sha512-fdods4YD9c8Ww69wHdnmXpjx7W0rvct6B7gLb92cWsd+ITSUG3hKoh+NqSWXF0GK5bk8IFRmTtBAwJObxow9wA=="],

    "@remotion/media-parser": ["@remotion/media-parser@4.0.507", "", {}, "sha512-BONx6R/0LLUSKjSgRLewb9QjZ9ZulxCct/RGPAFN8TIdeFUWxQ81Yfq1hQmUyXNBUhbfcHBEjdGnjgHCAeJkNw=="],

    "@remotion/media-utils": ["@remotion/media-utils@4.0.507", "", { "dependencies": { "mediabunny": "1.50.8", "remotion": "4.0.507" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-Ncm9ATXVOJ7aFbGXycVAXo+ISp3PFZb2JYSnGBuzat+d03CLR3yyCzGPhovlZqhnP7UIaRJxo15I5DlUkiGxrQ=="],

    "@remotion/player": ["@remotion/player@4.0.507", "", { "dependencies": { "remotion": "4.0.507" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-ZAunyyCfOXSYh5sZrp+vFxZlSPatg5evmh7fHVCndAOWBUPIDVjdUWEM2D4i132MsN6GXasXDByi+6H0H+IkhQ=="],

    "@remotion/renderer": ["@remotion/renderer@4.0.507", "", { "dependencies": { "@remotion/licensing": "4.0.507", "@remotion/streaming": "4.0.507", "execa": "5.1.1", "remotion": "4.0.507", "source-map": "0.8.0", "ws": "8.21.0" }, "optionalDependencies": { "@remotion/compositor-darwin-arm64": "4.0.507", "@remotion/compositor-darwin-x64": "4.0.507", "@remotion/compositor-linux-arm64-gnu": "4.0.507", "@remotion/compositor-linux-arm64-musl": "4.0.507", "@remotion/compositor-linux-x64-gnu": "4.0.507", "@remotion/compositor-linux-x64-musl": "4.0.507", "@remotion/compositor-win32-x64-msvc": "4.0.507" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-2qw3/2va97UNvkc1R/3L471mJwXEL33E5MI+YmBVUeS7TS/G6uoB4fNNrGMFs+DPp2u2dNGAIBEUqn1TWP9zGw=="],

    "@remotion/streaming": ["@remotion/streaming@4.0.507", "", {}, "sha512-RyLYm7/d3w2I0+ZiK/xNUxnDKyIkmpRFfNiSaod2cXnTw2fsbQ7xt5exJZSylvsd581ciDLeOaIN1m/u3425NA=="],

    "@remotion/studio": ["@remotion/studio@4.0.507", "", { "dependencies": { "@jridgewell/trace-mapping": "0.3.31", "@remotion/captions": "4.0.507", "@remotion/media-utils": "4.0.507", "@remotion/player": "4.0.507", "@remotion/renderer": "4.0.507", "@remotion/studio-protocol": "4.0.507", "@remotion/studio-shared": "4.0.507", "@remotion/timeline-utils": "4.0.507", "@remotion/web-renderer": "4.0.507", "@remotion/zod-types": "4.0.507", "mediabunny": "1.50.8", "memfs": "3.4.3", "open": "8.4.2", "remotion": "4.0.507", "semver": "7.5.3", "zod": "4.4.3" }, "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-6Za3v2uKItMqwiZm5Nk8la02KnPZIl+n3ctlVWmZe0kN8c9nsW3raTeYqGZyL9Bc2UXVq4J4IOWPu2etvnP/RQ=="],

    "@remotion/studio-codemods": ["@remotion/studio-codemods@4.0.507", "", { "dependencies": { "@babel/parser": "7.24.1", "@babel/types": "7.24.0", "@remotion/studio-shared": "4.0.507", "ast-types": "0.16.1", "recast": "0.23.11", "remotion": "4.0.507" } }, "sha512-F5xSJ/UXoQqEX/63WLa94G4glUZDR5GwDoMANCjEUJmu+YlV9rVuqTGI99YbbtyL59/WBAJVMYAOHCmCMkSgpg=="],

    "@remotion/studio-protocol": ["@remotion/studio-protocol@4.0.507", "", {}, "sha512-udC5R7gIODKAmMCG808O+uetgsm6aPYXK+g8ztEAAFfPho1pMoUXYUhO20ceLuWXZGMsS3A+sdow0q1eI7BZMQ=="],

    "@remotion/studio-server": ["@remotion/studio-server@4.0.507", "", { "dependencies": { "@babel/parser": "7.24.1", "@babel/types": "7.24.0", "@remotion/bundler": "4.0.507", "@remotion/renderer": "4.0.507", "@remotion/studio-codemods": "4.0.507", "@remotion/studio-protocol": "4.0.507", "@remotion/studio-shared": "4.0.507", "@svgr/core": "8.1.0", "@svgr/plugin-jsx": "8.1.0", "kiwi-schema": "0.5.0", "memfs": "3.4.3", "open": "8.4.2", "prettier": "3.8.1", "recast": "0.23.11", "remotion": "4.0.507", "semver": "7.5.3", "zod": "4.4.3" } }, "sha512-ZEsnEAJR3Y3jenbfO8oUMPkLfxrdI4oUuVmIZNs20xh1SWcsR3wMBPd44dK+u4CcwnJRiLMyVRhfGeK2Am9hjQ=="],

    "@remotion/studio-shared": ["@remotion/studio-shared@4.0.507", "", { "dependencies": { "@remotion/studio-protocol": "4.0.507", "remotion": "4.0.507" } }, "sha512-qFdI5XwIsVFFiKXx8snM+0SHi41/mfOR+tJcVHsPFzqqYTSd4Wq/4jyPfWzx89QHFkEJw1IBsl7ktpJ7pR7yhw=="],

    "@remotion/timeline-utils": ["@remotion/timeline-utils@4.0.507", "", { "dependencies": { "mediabunny": "1.50.8" } }, "sha512-xPn0EIQ3/QoIF1om7g76oW/ifpW9FxU0SuLvDn96ApIbZZ8RdMYJQlCXAUpbbrxd2x6nonj40BaQiB9x+eXPsQ=="],

    "@remotion/web-renderer": ["@remotion/web-renderer@4.0.507", "", { "dependencies": { "@mediabunny/aac-encoder": "1.50.8", "@mediabunny/flac-encoder": "1.50.8", "@mediabunny/mp3-encoder": "1.50.8", "@remotion/licensing": "4.0.507", "mediabunny": "1.50.8", "remotion": "4.0.507" }, "peerDependencies": { "react": ">=18.0.0", "react-dom": ">=18.0.0" } }, "sha512-fH8iZX1e0hmeJ+hPqn3RfqrDBNxMGsZZzfdyX2QpTDZ9F2kKqOkh0dQsRqaU8o+YoE8JNV/+FyYm4yyDAh9o6Q=="],

    "@remotion/zod-types": ["@remotion/zod-types@4.0.507", "", { "dependencies": { "remotion": "4.0.507" } }, "sha512-5Rezxss8eOaWq0n/P2U8GAMBQ1wav1HT+lXarqVkEmEGlv3IG7AFjrRSXnWnvm7h4eI5UhpiQ38tBS878QXSGg=="],

    "@rspack/binding": ["@rspack/binding@1.7.11", "", { "optionalDependencies": { "@rspack/binding-darwin-arm64": "1.7.11", "@rspack/binding-darwin-x64": "1.7.11", "@rspack/binding-linux-arm64-gnu": "1.7.11", "@rspack/binding-linux-arm64-musl": "1.7.11", "@rspack/binding-linux-x64-gnu": "1.7.11", "@rspack/binding-linux-x64-musl": "1.7.11", "@rspack/binding-wasm32-wasi": "1.7.11", "@rspack/binding-win32-arm64-msvc": "1.7.11", "@rspack/binding-win32-ia32-msvc": "1.7.11", "@rspack/binding-win32-x64-msvc": "1.7.11" } }, "sha512-2MGdy2s2HimsDT444Bp5XnALzNRxuBNc7y0JzyuqKbHBywd4x2NeXyhWXXoxufaCFu5PBc9Qq9jyfjW2Aeh06Q=="],

    "@rspack/binding-darwin-arm64": ["@rspack/binding-darwin-arm64@1.7.11", "", { "os": "darwin", "cpu": "arm64" }, "sha512-oduECiZVqbO5zlVw+q7Vy65sJFth99fWPTyucwvLJJtJkPL5n17Uiql2cYP6Ijn0pkqtf1SXgK8WjiKLG5bIig=="],

    "@rspack/binding-darwin-x64": ["@rspack/binding-darwin-x64@1.7.11", "", { "os": "darwin", "cpu": "x64" }, "sha512-a1+TtTE9ap6RalgFi7FGIgkJP6O4Vy6ctv+9WGJy53E4kuqHR0RygzaiVxCI/GMc/vBT9vY23hyrpWb3d1vtXA=="],

    "@rspack/binding-linux-arm64-gnu": ["@rspack/binding-linux-arm64-gnu@1.7.11", "", { "os": "linux", "cpu": "arm64" }, "sha512-P0QrGRPbTWu6RKWfN0bDtbnEps3rXH0MWIMreZABoUrVmNQKtXR6e73J3ub6a+di5s2+K0M2LJ9Bh2/H4UsDUA=="],

    "@rspack/binding-linux-arm64-musl": ["@rspack/binding-linux-arm64-musl@1.7.11", "", { "os": "linux", "cpu": "arm64" }, "sha512-6ky7R43VMjWwmx3Yx7Jl7faLBBMAgMDt+/bN35RgwjiPgsIByz65EwytUVuW9rikB43BGHvA/eqlnjLrUzNBqw=="],

    "@rspack/binding-linux-x64-gnu": ["@rspack/binding-linux-x64-gnu@1.7.11", "", { "os": "linux", "cpu": "x64" }, "sha512-cuOJMfCOvb2Wgsry5enXJ3iT1FGUjdPqtGUBVupQlEG4ntSYsQ2PtF4wIDVasR3wdxC5nQbipOrDiN/u6fYsdQ=="],

    "@rspack/binding-linux-x64-musl": ["@rspack/binding-linux-x64-musl@1.7.11", "", { "os": "linux", "cpu": "x64" }, "sha512-CoK37hva4AmHGh3VCsQXmGr40L36m1/AdnN5LEjUX6kx5rEH7/1nEBN6Ii72pejqDVvk9anEROmPDiPw10tpFg=="],

    "@rspack/binding-wasm32-wasi": ["@rspack/binding-wasm32-wasi@1.7.11", "", { "dependencies": { "@napi-rs/wasm-runtime": "1.0.7" }, "cpu": "none" }, "sha512-OtrmnPUVJMxjNa3eDMfHyPdtlLRmmp/aIm0fQHlAOATbZvlGm12q7rhPW5BXTu1yh+1rQ1/uqvz+SzKEZXuJaQ=="],

    "@rspack/binding-win32-arm64-msvc": ["@rspack/binding-win32-arm64-msvc@1.7.11", "", { "os": "win32", "cpu": "arm64" }, "sha512-lObFW6e5lCWNgTBNwT//yiEDbsxm9QG4BYUojqeXxothuzJ/L6ibXz6+gLMvbOvLGV3nKgkXmx8GvT9WDKR0mA=="],

    "@rspack/binding-win32-ia32-msvc": ["@rspack/binding-win32-ia32-msvc@1.7.11", "", { "os": "win32", "cpu": "ia32" }, "sha512-0pYGnZd8PPqNR68zQ8skamqNAXEA1sUfXuAdYcknIIRq2wsbiwFzIc0Pov1cIfHYab37G7sSIPBiOUdOWF5Ivw=="],

    "@rspack/binding-win32-x64-msvc": ["@rspack/binding-win32-x64-msvc@1.7.11", "", { "os": "win32", "cpu": "x64" }, "sha512-EeQXayoQk/uBkI3pdoXfQBXNIUrADq56L3s/DFyM2pJeUDrWmhfIw2UFIGkYPTMSCo8F2JcdcGM32FGJrSnU0Q=="],

    "@rspack/core": ["@rspack/core@1.7.11", "", { "dependencies": { "@module-federation/runtime-tools": "0.22.0", "@rspack/binding": "1.7.11", "@rspack/lite-tapable": "1.1.0" }, "peerDependencies": { "@swc/helpers": ">=0.5.1" }, "optionalPeers": ["@swc/helpers"] }, "sha512-rsD9b+Khmot5DwCMiB3cqTQo53ioPG3M/A7BySu8+0+RS7GCxKm+Z+mtsjtG/vsu4Tn2tcqCdZtA3pgLoJB+ew=="],

    "@rspack/lite-tapable": ["@rspack/lite-tapable@1.1.0", "", {}, "sha512-E2B0JhYFmVAwdDiG14+DW0Di4Ze4Jg10Pc4/lILUrd5DRCaklduz2OvJ5HYQ6G+hd+WTzqQb3QnDNfK4yvAFYw=="],

    "@rspack/plugin-react-refresh": ["@rspack/plugin-react-refresh@1.6.1", "", { "dependencies": { "error-stack-parser": "^2.1.4", "html-entities": "^2.6.0" }, "peerDependencies": { "react-refresh": ">=0.10.0 <1.0.0", "webpack-hot-middleware": "2.x" }, "optionalPeers": ["webpack-hot-middleware"] }, "sha512-eqqW5645VG3CzGzFgNg5HqNdHVXY+567PGjtDhhrM8t67caxmsSzRmT5qfoEIfBcGgFkH9vEg7kzXwmCYQdQDw=="],

    "@svgr/babel-plugin-add-jsx-attribute": ["@svgr/babel-plugin-add-jsx-attribute@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-b9MIk7yhdS1pMCZM8VeNfUlSKVRhsHZNMl5O9SfaX0l0t5wjdgu4IDzGB8bpnGBBOjGST3rRFVsaaEtI4W6f7g=="],

    "@svgr/babel-plugin-remove-jsx-attribute": ["@svgr/babel-plugin-remove-jsx-attribute@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-BcCkm/STipKvbCl6b7QFrMh/vx00vIP63k2eM66MfHJzPr6O2U0jYEViXkHJWqXqQYjdeA9cuCl5KWmlwjDvbA=="],

    "@svgr/babel-plugin-remove-jsx-empty-expression": ["@svgr/babel-plugin-remove-jsx-empty-expression@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-5BcGCBfBxB5+XSDSWnhTThfI9jcO5f0Ai2V24gZpG+wXF14BzwxxdDb4g6trdOux0rhibGs385BeFMSmxtS3uA=="],

    "@svgr/babel-plugin-replace-jsx-attribute-value": ["@svgr/babel-plugin-replace-jsx-attribute-value@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-KVQ+PtIjb1BuYT3ht8M5KbzWBhdAjjUPdlMtpuw/VjT8coTrItWX6Qafl9+ji831JaJcu6PJNKCV0bp01lBNzQ=="],

    "@svgr/babel-plugin-svg-dynamic-title": ["@svgr/babel-plugin-svg-dynamic-title@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-omNiKqwjNmOQJ2v6ge4SErBbkooV2aAWwaPFs2vUY7p7GhVkzRkJ00kILXQvRhA6miHnNpXv7MRnnSjdRjK8og=="],

    "@svgr/babel-plugin-svg-em-dimensions": ["@svgr/babel-plugin-svg-em-dimensions@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-mURHYnu6Iw3UBTbhGwE/vsngtCIbHE43xCRK7kCw4t01xyGqb2Pd+WXekRRoFOBIY29ZoOhUCTEweDMdrjfi9g=="],

    "@svgr/babel-plugin-transform-react-native-svg": ["@svgr/babel-plugin-transform-react-native-svg@8.1.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-Tx8T58CHo+7nwJ+EhUwx3LfdNSG9R2OKfaIXXs5soiy5HtgoAEkDay9LIimLOcG8dJQH1wPZp/cnAv6S9CrR1Q=="],

    "@svgr/babel-plugin-transform-svg-component": ["@svgr/babel-plugin-transform-svg-component@8.0.0", "", { "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-DFx8xa3cZXTdb/k3kfPeaixecQLgKh5NVBMwD0AQxOzcZawK4oo1Jh9LbrcACUivsCA7TLG8eeWgrDXjTMhRmw=="],

    "@svgr/babel-preset": ["@svgr/babel-preset@8.1.0", "", { "dependencies": { "@svgr/babel-plugin-add-jsx-attribute": "8.0.0", "@svgr/babel-plugin-remove-jsx-attribute": "8.0.0", "@svgr/babel-plugin-remove-jsx-empty-expression": "8.0.0", "@svgr/babel-plugin-replace-jsx-attribute-value": "8.0.0", "@svgr/babel-plugin-svg-dynamic-title": "8.0.0", "@svgr/babel-plugin-svg-em-dimensions": "8.0.0", "@svgr/babel-plugin-transform-react-native-svg": "8.1.0", "@svgr/babel-plugin-transform-svg-component": "8.0.0" }, "peerDependencies": { "@babel/core": "^7.0.0-0" } }, "sha512-7EYDbHE7MxHpv4sxvnVPngw5fuR6pw79SkcrILHJ/iMpuKySNCl5W1qcwPEpU+LgyRXOaAFgH0KhwD18wwg6ug=="],

    "@svgr/core": ["@svgr/core@8.1.0", "", { "dependencies": { "@babel/core": "^7.21.3", "@svgr/babel-preset": "8.1.0", "camelcase": "^6.2.0", "cosmiconfig": "^8.1.3", "snake-case": "^3.0.4" } }, "sha512-8QqtOQT5ACVlmsvKOJNEaWmRPmcojMOzCz4Hs2BGG/toAp/K38LcsMRyLp349glq5AzJbCEeimEoxaX6v/fLrA=="],

    "@svgr/hast-util-to-babel-ast": ["@svgr/hast-util-to-babel-ast@8.0.0", "", { "dependencies": { "@babel/types": "^7.21.3", "entities": "^4.4.0" } }, "sha512-EbDKwO9GpfWP4jN9sGdYwPBU0kdomaPIL2Eu4YwmgP+sJeXT+L7bMwJUBnhzfH8Q2qMBqZ4fJwpCyYsAN3mt2Q=="],

    "@svgr/plugin-jsx": ["@svgr/plugin-jsx@8.1.0", "", { "dependencies": { "@babel/core": "^7.21.3", "@svgr/babel-preset": "8.1.0", "@svgr/hast-util-to-babel-ast": "8.0.0", "svg-parser": "^2.0.4" }, "peerDependencies": { "@svgr/core": "*" } }, "sha512-0xiIyBsLlr8quN+WyuxooNW9RJ0Dpr8uOnH/xrCVO8GLUcwHISwj1AG0k+LFzteTkAA0GbX0kj9q6Dk70PTiPA=="],

    "@tybys/wasm-util": ["@tybys/wasm-util@0.10.4", "", { "dependencies": { "tslib": "^2.4.0" } }, "sha512-W3c4gRigFS0T/Ma4qIYF3GDAc5AQdHb1yL5znJT1Zv1YaD9Kitx656wBjvr19qbiosmZT8lWDM5BEMynUqX65A=="],

    "@types/d3-array": ["@types/d3-array@3.2.2", "", {}, "sha512-hOLWVbm7uRza0BYXpIIW5pxfrKe0W+D5lrFiAEYR+pb6w3N2SwSMaJbXdUfSEv+dT4MfHBLtn5js0LAWaO6otw=="],

    "@types/d3-contour": ["@types/d3-contour@3.0.6", "", { "dependencies": { "@types/d3-array": "*", "@types/geojson": "*" } }, "sha512-BjzLgXGnCWjUSYGfH1cpdo41/hgdWETu4YxpezoztawmqsvCeep+8QGfiY6YbDvfgHz/DkjeIkkZVJavB4a3rg=="],

    "@types/d3-geo": ["@types/d3-geo@3.1.0", "", { "dependencies": { "@types/geojson": "*" } }, "sha512-856sckF0oP/diXtS4jNsiQw/UuK5fQG8l/a9VVLeSouf1/PPbBE1i1W852zVwKwYCBkFJJB7nCFTbk6UMEXBOQ=="],

    "@types/dom-mediacapture-transform": ["@types/dom-mediacapture-transform@0.1.12", "", { "dependencies": { "@types/dom-webcodecs": "*" } }, "sha512-d7/QsLRwF864A5mgIM/YrfiglHoYn7zgCcAoJgW404r+2DwnNr7EBbLnCWpmOMgH8y0te73L1AV6H1bmauaWFw=="],

    "@types/dom-webcodecs": ["@types/dom-webcodecs@0.1.13", "", {}, "sha512-O5hkiFIcjjszPIYyUSyvScyvrBoV3NOEEZx/pMlsu44TKzWNkLVBBxnxJz42in5n3QIolYOcBYFCPZZ0h8SkwQ=="],

    "@types/eslint": ["@types/eslint@9.6.1", "", { "dependencies": { "@types/estree": "*", "@types/json-schema": "*" } }, "sha512-FXx2pKgId/WyYo2jXw63kk7/+TY7u7AziEJxJAnSFzHlqTAS3Ync6SvgYAN/k4/PQpnnVuzoMuVnByKK2qp0ag=="],

    "@types/eslint-scope": ["@types/eslint-scope@3.7.7", "", { "dependencies": { "@types/eslint": "*", "@types/estree": "*" } }, "sha512-MzMFlSLBqNF2gcHWO0G1vP/YQyfvrxZ0bF+u7mzUdZ1/xK4A4sru+nraZz5i3iEIk1l1uyicaDVTB4QbbEkAYg=="],

    "@types/estree": ["@types/estree@1.0.9", "", {}, "sha512-GhdPgy1el4/ImP05X05Uw4cw2/M93BCUmnEvWZNStlCzEKME4Fkk+YpoA5OiHNQmoS7Cafb8Xa3Pya8m1Qrzeg=="],

    "@types/geojson": ["@types/geojson@7946.0.16", "", {}, "sha512-6C8nqWur3j98U6+lXDfTUWIfgvZU+EumvpHKcYjujKH7woYyLj2sUmff0tRhrqM7BohUw7Pz3ZB1jj2gW9Fvmg=="],

    "@types/json-schema": ["@types/json-schema@7.0.15", "", {}, "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA=="],

    "@types/node": ["@types/node@26.6.5", "", { "dependencies": { "undici-types": "~8.9.0" } }, "sha512-uMzsv9stDdofIZBx4UGh4Z9ZgXnGC9seRDscilBcTHAeOFk67MZg/k9bWVfO+bk4qZmG+l52hRnLwUiH2LnJTg=="],

    "@types/react": ["@types/react@19.2.14", "", { "dependencies": { "csstype": "^3.2.2" } }, "sha512-ilcTH/UniCkMdtexkoCN0bI7pMcJDvmQFPvuPvmEaYA/NSfFTAgdUSLAoVjaRJm7+6PvcM+q1zYOwS4wTYMF9w=="],

    "@webassemblyjs/ast": ["@webassemblyjs/ast@1.14.1", "", { "dependencies": { "@webassemblyjs/helper-numbers": "1.13.2", "@webassemblyjs/helper-wasm-bytecode": "1.13.2" } }, "sha512-nuBEDgQfm1ccRp/8bCQrx1frohyufl4JlbMMZ4P1wpeOfDhF6FQkxZJ1b/e+PLwr6X1Nhw6OLme5usuBWYBvuQ=="],

    "@webassemblyjs/floating-point-hex-parser": ["@webassemblyjs/floating-point-hex-parser@1.13.2", "", {}, "sha512-6oXyTOzbKxGH4steLbLNOu71Oj+C8Lg34n6CqRvqfS2O71BxY6ByfMDRhBytzknj9yGUPVJ1qIKhRlAwO1AovA=="],

    "@webassemblyjs/helper-api-error": ["@webassemblyjs/helper-api-error@1.13.2", "", {}, "sha512-U56GMYxy4ZQCbDZd6JuvvNV/WFildOjsaWD3Tzzvmw/mas3cXzRJPMjP83JqEsgSbyrmaGjBfDtV7KDXV9UzFQ=="],

    "@webassemblyjs/helper-buffer": ["@webassemblyjs/helper-buffer@1.14.1", "", {}, "sha512-jyH7wtcHiKssDtFPRB+iQdxlDf96m0E39yb0k5uJVhFGleZFoNw1c4aeIcVUPPbXUVJ94wwnMOAqUHyzoEPVMA=="],

    "@webassemblyjs/helper-numbers": ["@webassemblyjs/helper-numbers@1.13.2", "", { "dependencies": { "@webassemblyjs/floating-point-hex-parser": "1.13.2", "@webassemblyjs/helper-api-error": "1.13.2", "@xtuc/long": "4.2.2" } }, "sha512-FE8aCmS5Q6eQYcV3gI35O4J789wlQA+7JrqTTpJqn5emA4U2hvwJmvFRC0HODS+3Ye6WioDklgd6scJ3+PLnEA=="],

    "@webassemblyjs/helper-wasm-bytecode": ["@webassemblyjs/helper-wasm-bytecode@1.13.2", "", {}, "sha512-3QbLKy93F0EAIXLh0ogEVR6rOubA9AoZ+WRYhNbFyuB70j3dRdwH9g+qXhLAO0kiYGlg3TxDV+I4rQTr/YNXkA=="],

    "@webassemblyjs/helper-wasm-section": ["@webassemblyjs/helper-wasm-section@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/wasm-gen": "1.14.1" } }, "sha512-ds5mXEqTJ6oxRoqjhWDU83OgzAYjwsCV8Lo/N+oRsNDmx/ZDpqalmrtgOMkHwxsG0iI//3BwWAErYRHtgn0dZw=="],

    "@webassemblyjs/ieee754": ["@webassemblyjs/ieee754@1.13.2", "", { "dependencies": { "@xtuc/ieee754": "^1.2.0" } }, "sha512-4LtOzh58S/5lX4ITKxnAK2USuNEvpdVV9AlgGQb8rJDHaLeHciwG4zlGr0j/SNWlr7x3vO1lDEsuePvtcDNCkw=="],

    "@webassemblyjs/leb128": ["@webassemblyjs/leb128@1.13.2", "", { "dependencies": { "@xtuc/long": "4.2.2" } }, "sha512-Lde1oNoIdzVzdkNEAWZ1dZ5orIbff80YPdHx20mrHwHrVNNTjNr8E3xz9BdpcGqRQbAEa+fkrCb+fRFTl/6sQw=="],

    "@webassemblyjs/utf8": ["@webassemblyjs/utf8@1.13.2", "", {}, "sha512-3NQWGjKTASY1xV5m7Hr0iPeXD9+RDobLll3T9d2AO+g3my8xy5peVyjSag4I50mR1bBSN/Ct12lo+R9tJk0NZQ=="],

    "@webassemblyjs/wasm-edit": ["@webassemblyjs/wasm-edit@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/helper-wasm-section": "1.14.1", "@webassemblyjs/wasm-gen": "1.14.1", "@webassemblyjs/wasm-opt": "1.14.1", "@webassemblyjs/wasm-parser": "1.14.1", "@webassemblyjs/wast-printer": "1.14.1" } }, "sha512-RNJUIQH/J8iA/1NzlE4N7KtyZNHi3w7at7hDjvRNm5rcUXa00z1vRz3glZoULfJ5mpvYhLybmVcwcjGrC1pRrQ=="],

    "@webassemblyjs/wasm-gen": ["@webassemblyjs/wasm-gen@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/ieee754": "1.13.2", "@webassemblyjs/leb128": "1.13.2", "@webassemblyjs/utf8": "1.13.2" } }, "sha512-AmomSIjP8ZbfGQhumkNvgC33AY7qtMCXnN6bL2u2Js4gVCg8fp735aEiMSBbDR7UQIj90n4wKAFUSEd0QN2Ukg=="],

    "@webassemblyjs/wasm-opt": ["@webassemblyjs/wasm-opt@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-buffer": "1.14.1", "@webassemblyjs/wasm-gen": "1.14.1", "@webassemblyjs/wasm-parser": "1.14.1" } }, "sha512-PTcKLUNvBqnY2U6E5bdOQcSM+oVP/PmrDY9NzowJjislEjwP/C4an2303MCVS2Mg9d3AJpIGdUFIQQWbPds0Sw=="],

    "@webassemblyjs/wasm-parser": ["@webassemblyjs/wasm-parser@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@webassemblyjs/helper-api-error": "1.13.2", "@webassemblyjs/helper-wasm-bytecode": "1.13.2", "@webassemblyjs/ieee754": "1.13.2", "@webassemblyjs/leb128": "1.13.2", "@webassemblyjs/utf8": "1.13.2" } }, "sha512-JLBl+KZ0R5qB7mCnud/yyX08jWFw5MsoalJ1pQ4EdFlgj9VdXKGuENGsiCIjegI1W7p91rUlcB/LB5yRJKNTcQ=="],

    "@webassemblyjs/wast-printer": ["@webassemblyjs/wast-printer@1.14.1", "", { "dependencies": { "@webassemblyjs/ast": "1.14.1", "@xtuc/long": "4.2.2" } }, "sha512-kPSSXE6De1XOR820C90RIo2ogvZG+c3KiHzqUoO/F34Y2shGzesfqv7o57xrxovZJH/MetF5UjroJ/R/3isoiw=="],

    "@xtuc/ieee754": ["@xtuc/ieee754@1.2.0", "", {}, "sha512-DX8nKgqcGwsc0eJSqYt5lwP4DH5FlHnmuWWBRy7X0NcaGR0ZtuyeESgMwTYVEtxmsNGY+qit4QYT/MIYTOTPeA=="],

    "@xtuc/long": ["@xtuc/long@4.2.2", "", {}, "sha512-NuHqBY1PB/D8xU6s/thBgOAiAP7HOYDQ32+BFZILJ8ivkUkAHQnWfn6WhL79Owj1qmUnoN/YPhktdIoucipkAQ=="],

    "acorn": ["acorn@8.19.0", "", { "bin": { "acorn": "bin/acorn" } }, "sha512-oJlA3XiRm7Cyk6qFD2Jn8ak9B7jSy0qy00ADO3+8dpT0LSjFihQYv4C02LFCSYJV3Q37xYwwRy5m+IpIiUzqWw=="],

    "acorn-import-phases": ["acorn-import-phases@1.0.4", "", { "peerDependencies": { "acorn": "^8.14.0" } }, "sha512-wKmbr/DDiIXzEOiWrTTUcDm24kQ2vGfZQvM2fwg2vXqR5uW6aapr7ObPtj1th32b9u90/Pf4AItvdTh42fBmVQ=="],

    "ajv": ["ajv@8.20.0", "", { "dependencies": { "fast-deep-equal": "^3.1.3", "fast-uri": "^3.0.1", "json-schema-traverse": "^1.0.0", "require-from-string": "^2.0.2" } }, "sha512-Thbli+OlOj+iMPYFBVBfJ3OmCAnaSyNn4M1vz9T6Gka5Jt9ba/HIR56joy65tY6kx/FCF5VXNB819Y7/GUrBGA=="],

    "ajv-formats": ["ajv-formats@3.0.1", "", { "dependencies": { "ajv": "^8.0.0" } }, "sha512-8iUql50EUR+uUcdRQ3HDqa6EVyo3docL8g5WJ3FNcWmu62IbkGUue/pEyLBW8VGKKucTPgqeks4fIU1DA4yowQ=="],

    "ajv-keywords": ["ajv-keywords@5.1.0", "", { "dependencies": { "fast-deep-equal": "^3.1.3" }, "peerDependencies": { "ajv": "^8.8.2" } }, "sha512-YCS/JNFAUyr5vAuhk1DWm1CBxRHW9LbJ2ozWeemrIqpbsqKjHVxYPyi5GC0rjZIT5JxJ3virVTS8wk4i/Z+krw=="],

    "argparse": ["argparse@2.0.1", "", {}, "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q=="],

    "ast-types": ["ast-types@0.16.1", "", { "dependencies": { "tslib": "^2.0.1" } }, "sha512-6t10qk83GOG8p0vKmaCr8eiilZwO171AvbROMtvvNiwrTly62t+7XkA8RdIIVbpMhCASAsxgAzdRSwh6nw/5Dg=="],

    "baseline-browser-mapping": ["baseline-browser-mapping@2.11.28", "", { "bin": { "baseline-browser-mapping": "dist/cli.cjs" } }, "sha512-br0LOmjJqr6Rt4AEkadbcNf67Zpo7EPwKsWbjnRrJIa1QYFHQBqM4C7F2WTbV8ahTEcg1Eo+Y0aWjjORInYFyA=="],

    "browserslist": ["browserslist@4.29.3", "", { "dependencies": { "baseline-browser-mapping": "^2.11.26", "caniuse-lite": "^1.0.30001813", "electron-to-chromium": "^1.5.439", "node-releases": "^2.0.57", "update-browserslist-db": "^1.3.3" }, "bin": { "browserslist": "cli.js" } }, "sha512-1R4kiYKXGViqEN0CnoDrXc1StD9niAwu+j2dukWzrD4bJgsD4lDmEp0CRbc6E/vYJIfTHwPmwyaKtVSudICdPA=="],

    "buffer-from": ["buffer-from@1.1.2", "", {}, "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ=="],

    "callsites": ["callsites@3.1.0", "", {}, "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ=="],

    "camelcase": ["camelcase@6.3.0", "", {}, "sha512-Gmy6FhYlCY7uOElZUSbxo2UCDH8owEk996gkbrpsgGtrJLM3J7jGxl9Ic7Qwwj4ivOE5AWZWRMecDdF7hqGjFA=="],

    "caniuse-lite": ["caniuse-lite@1.0.30001816", "", {}, "sha512-+8Yx7BXCoqk6IF8yTicjfUR6D/ldJzdlsodlEOiOSPmhK844WIgk67/zIQaGAOxNkZyyvBlrRFnLvqKIoqbAFw=="],

    "chrome-trace-event": ["chrome-trace-event@1.0.4", "", {}, "sha512-rNjApaLzuwaOTjCiT8lSDdGN1APCiqkChLMJxJPWLunPAt5fy8xgU9/jNOchV84wfIxrA0lRQB7oCT8jrn/wrQ=="],

    "commander": ["commander@2.20.3", "", {}, "sha512-GpVkmM8vF2vQUkj2LvZmD35JxeJOLCwJ9cUkugyk2nuhbv3+mJvpLYYt+0+USMxE+oj+ey/lJEnhZw75x/OMcQ=="],

    "convert-source-map": ["convert-source-map@2.0.0", "", {}, "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg=="],

    "cosmiconfig": ["cosmiconfig@8.3.6", "", { "dependencies": { "import-fresh": "^3.3.0", "js-yaml": "^4.1.0", "parse-json": "^5.2.0", "path-type": "^4.0.0" }, "peerDependencies": { "typescript": ">=4.9.5" }, "optionalPeers": ["typescript"] }, "sha512-kcZ6+W5QzcJ3P1Mt+83OUv/oHFqZHIx8DuxG6eZ5RGMERoLqp4BuGjhHLYGK+Kf5XVkQvqBSmAy/nGWN3qDgEA=="],

    "cross-spawn": ["cross-spawn@7.0.6", "", { "dependencies": { "path-key": "^3.1.0", "shebang-command": "^2.0.0", "which": "^2.0.1" } }, "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA=="],

    "css-loader": ["css-loader@7.1.4", "", { "dependencies": { "icss-utils": "^5.1.0", "postcss": "^8.4.40", "postcss-modules-extract-imports": "^3.1.0", "postcss-modules-local-by-default": "^4.0.5", "postcss-modules-scope": "^3.2.0", "postcss-modules-values": "^4.0.0", "postcss-value-parser": "^4.2.0", "semver": "^7.6.3" }, "peerDependencies": { "@rspack/core": "0.x || ^1.0.0 || ^2.0.0-0", "webpack": "^5.27.0" }, "optionalPeers": ["@rspack/core", "webpack"] }, "sha512-vv3J9tlOl04WjiMvHQI/9tmIrCxVrj6PFbHemBB1iihpeRbi/I4h033eoFIhwxBBqLhI0KYFS7yvynBFhIZfTw=="],

    "cssesc": ["cssesc@3.0.0", "", { "bin": { "cssesc": "bin/cssesc" } }, "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg=="],

    "csstype": ["csstype@3.2.3", "", {}, "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ=="],

    "d3-array": ["d3-array@3.2.4", "", { "dependencies": { "internmap": "1 - 2" } }, "sha512-tdQAmyA18i4J7wprpYq8ClcxZy3SC31QMeByyCFyRt7BVHdREQZ5lpzoe5mFEYZUWe+oq8HBvk9JjpibyEV4Jg=="],

    "d3-contour": ["d3-contour@4.0.2", "", { "dependencies": { "d3-array": "^3.2.0" } }, "sha512-4EzFTRIikzs47RGmdxbeUvLWtGedDUNkTcmzoeyg4sP/dvCexO47AaQL7VKy/gul85TOxw+IBgA8US2xwbToNA=="],

    "d3-geo": ["d3-geo@3.1.1", "", { "dependencies": { "d3-array": "2.5.0 - 3" } }, "sha512-637ln3gXKXOwhalDzinUgY83KzNWZRKbYubaG+fGVuc/dxO64RRljtCTnf5ecMyE1RIdtqpkVcq0IbtU2S8j2Q=="],

    "debug": ["debug@4.4.3", "", { "dependencies": { "ms": "^2.1.3" }, "peerDependencies": { "supports-color": "*" }, "optionalPeers": ["supports-color"] }, "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA=="],

    "define-lazy-prop": ["define-lazy-prop@2.0.0", "", {}, "sha512-Ds09qNh8yw3khSjiJjiUInaGX9xlqZDY7JVryGxdxV7NPeuqQfplOpQ66yJFZut3jLa5zOwkXw1g9EI2uKh4Og=="],

    "dot-case": ["dot-case@3.0.4", "", { "dependencies": { "no-case": "^3.0.4", "tslib": "^2.0.3" } }, "sha512-Kv5nKlh6yRrdrGvxeJ2e5y2eRUpkUosIW4A2AS38zwSz27zu7ufDwQPi5Jhs3XAlGNetl3bmnGhQsMtkKJnj3w=="],

    "dotenv": ["dotenv@17.3.1", "", {}, "sha512-IO8C/dzEb6O3F9/twg6ZLXz164a2fhTnEWb95H23Dm4OuN+92NmEAlTrupP9VW6Jm3sO26tQlqyvyi4CsnY9GA=="],

    "electron-to-chromium": ["electron-to-chromium@1.5.456", "", {}, "sha512-8hboqI6xesozteFb8aa7OGknvxUtTeRJLz0FoePysUEh/oWbddykIGdgpEJRbPRg/nIMfBf2DFos+H2MtvJl2A=="],

    "enhanced-resolve": ["enhanced-resolve@5.26.0", "", { "dependencies": { "graceful-fs": "^4.2.4", "tapable": "^2.3.3" } }, "sha512-9vhedylFonb2YGogzUKX6+Ja72gOJbN1QHAqdrvqLwhdl/QWbKopzoUC9EbQNVsAns/bx/4uyqalrQAoy1IByw=="],

    "entities": ["entities@4.5.0", "", {}, "sha512-V0hjH4dGPh9Ao5p0MoRY6BVqtwCjhz6vI5LT8AJ55H+4g9/4vbHx1I54fS0XuclLhDHArPQCiMjDxjaL8fPxhw=="],

    "error-ex": ["error-ex@1.3.4", "", { "dependencies": { "is-arrayish": "^0.2.1" } }, "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ=="],

    "error-stack-parser": ["error-stack-parser@2.1.4", "", { "dependencies": { "stackframe": "^1.3.4" } }, "sha512-Sk5V6wVazPhq5MhpO+AUxJn5x7XSXGl1R93Vn7i+zS15KDVxQijejNCrz8340/2bgLBjR9GtEG8ZVKONDjcqGQ=="],

    "es-module-lexer": ["es-module-lexer@2.3.2", "", {}, "sha512-poHGpORABojJJucnV9KbOavETW8lBVnphkW77ER5/BQ5Fz7oXSoCNek7IH3vR5nRjdsEz926ibFYX8KtLQmdyw=="],

    "esbuild": ["esbuild@0.28.1", "", { "optionalDependencies": { "@esbuild/aix-ppc64": "0.28.1", "@esbuild/android-arm": "0.28.1", "@esbuild/android-arm64": "0.28.1", "@esbuild/android-x64": "0.28.1", "@esbuild/darwin-arm64": "0.28.1", "@esbuild/darwin-x64": "0.28.1", "@esbuild/freebsd-arm64": "0.28.1", "@esbuild/freebsd-x64": "0.28.1", "@esbuild/linux-arm": "0.28.1", "@esbuild/linux-arm64": "0.28.1", "@esbuild/linux-ia32": "0.28.1", "@esbuild/linux-loong64": "0.28.1", "@esbuild/linux-mips64el": "0.28.1", "@esbuild/linux-ppc64": "0.28.1", "@esbuild/linux-riscv64": "0.28.1", "@esbuild/linux-s390x": "0.28.1", "@esbuild/linux-x64": "0.28.1", "@esbuild/netbsd-arm64": "0.28.1", "@esbuild/netbsd-x64": "0.28.1", "@esbuild/openbsd-arm64": "0.28.1", "@esbuild/openbsd-x64": "0.28.1", "@esbuild/openharmony-arm64": "0.28.1", "@esbuild/sunos-x64": "0.28.1", "@esbuild/win32-arm64": "0.28.1", "@esbuild/win32-ia32": "0.28.1", "@esbuild/win32-x64": "0.28.1" }, "bin": { "esbuild": "bin/esbuild" } }, "sha512-HrJrvZv5ayxBzPfwphOoNzkzOIIlifzk0KJrGK2c8R4+LKpMtpYLQeUdjnwjWv/LZlkH2laZk+4w78pi99D4Vw=="],

    "escalade": ["escalade@3.2.0", "", {}, "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA=="],

    "eslint-scope": ["eslint-scope@5.1.1", "", { "dependencies": { "esrecurse": "^4.3.0", "estraverse": "^4.1.1" } }, "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw=="],

    "esprima": ["esprima@4.0.1", "", { "bin": { "esparse": "./bin/esparse.js", "esvalidate": "./bin/esvalidate.js" } }, "sha512-eGuFFw7Upda+g4p+QHvnW0RyTX/SVeJBDM/gCtMARO0cLuT2HcEKnTPvhjV6aGeqrCB/sbNop0Kszm0jsaWU4A=="],

    "esrecurse": ["esrecurse@4.3.0", "", { "dependencies": { "estraverse": "^5.2.0" } }, "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag=="],

    "estraverse": ["estraverse@4.3.0", "", {}, "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw=="],

    "events": ["events@3.3.0", "", {}, "sha512-mQw+2fkQbALzQ7V0MY0IqdnXNOeTtP4r0lN9z7AAawCXgqea7bDii20AYrIBrFd/Hx0M2Ocz6S111CaFkUcb0Q=="],

    "execa": ["execa@5.1.1", "", { "dependencies": { "cross-spawn": "^7.0.3", "get-stream": "^6.0.0", "human-signals": "^2.1.0", "is-stream": "^2.0.0", "merge-stream": "^2.0.0", "npm-run-path": "^4.0.1", "onetime": "^5.1.2", "signal-exit": "^3.0.3", "strip-final-newline": "^2.0.0" } }, "sha512-8uSpZZocAZRBAPIEINJj3Lo9HyGitllczc27Eh5YYojjMFMn8yHMDMaUHE2Jqfq05D/wucwI4JGURyXt1vchyg=="],

    "fast-deep-equal": ["fast-deep-equal@3.1.3", "", {}, "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q=="],

    "fast-uri": ["fast-uri@3.1.8", "", {}, "sha512-GZMtZUTNRpOVIECoXwLNZS5xUGE+mVNbTB8h/7Rwh2TFWcBQiPzTgyZi05BF9UMZKkLJv8XBRJTlU7zg8+ZfMg=="],

    "fs-monkey": ["fs-monkey@1.0.3", "", {}, "sha512-cybjIfiiE+pTWicSCLFHSrXZ6EilF30oh91FDP9S2B051prEa7QWfrVTQm10/dDpswBDXZugPa1Ogu8Yh+HV0Q=="],

    "gensync": ["gensync@1.0.0-beta.2", "", {}, "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg=="],

    "get-stream": ["get-stream@6.0.1", "", {}, "sha512-ts6Wi+2j3jQjqi70w5AlN8DFnkSwC+MqmxEzdEALB2qXZYV3X/b1CTfgPLGJNMeAWxdPfU8FO1ms3NUfaHCPYg=="],

    "glob-to-regexp": ["glob-to-regexp@0.4.1", "", {}, "sha512-lkX1HJXwyMcprw/5YUZc2s7DrpAiHB21/V+E1rHUrVNokkvB6bqMzT0VfV6/86ZNabt1k14YOIaT7nDvOX3Iiw=="],

    "graceful-fs": ["graceful-fs@4.2.11", "", {}, "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ=="],

    "has-flag": ["has-flag@4.0.0", "", {}, "sha512-EykJT/Q1KjTWctppgIAgfSO0tKVuZUjhgMr17kqTumMl6Afv3EISleU7qZUzoXDFTAHTDC4NOoG/ZxU3EvlMPQ=="],

    "html-entities": ["html-entities@2.6.0", "", {}, "sha512-kig+rMn/QOVRvr7c86gQ8lWXq+Hkv6CbAH1hLu+RG338StTpE8Z0b44SDVaqVu7HGKf27frdmUYEs9hTUX/cLQ=="],

    "human-signals": ["human-signals@2.1.0", "", {}, "sha512-B4FFZ6q/T2jhhksgkbEW3HBvWIfDW85snkQgawt07S7J5QXTk6BkNV+0yAeZrM5QpMAdYlocGoljn0sJ/WQkFw=="],

    "icss-utils": ["icss-utils@5.1.0", "", { "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-soFhflCVWLfRNOPU3iv5Z9VUdT44xFRbzjLsEzSr5AQmgqPMTHdU3PMT1Cf1ssx8fLNJDA1juftYl+PUcv3MqA=="],

    "import-fresh": ["import-fresh@3.3.1", "", { "dependencies": { "parent-module": "^1.0.0", "resolve-from": "^4.0.0" } }, "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ=="],

    "internmap": ["internmap@2.0.3", "", {}, "sha512-5Hh7Y1wQbvY5ooGgPbDaL5iYLAPzMTUrjMulskHLH6wnv/A+1q5rgEaiuqEjB+oxGXIVZs1FF+R/KPN3ZSQYYg=="],

    "is-arrayish": ["is-arrayish@0.2.1", "", {}, "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg=="],

    "is-docker": ["is-docker@2.2.1", "", { "bin": { "is-docker": "cli.js" } }, "sha512-F+i2BKsFrH66iaUFc0woD8sLy8getkwTwtOBjvs56Cx4CgJDeKQeqfz8wAYiSb8JOprWhHH5p77PbmYCvvUuXQ=="],

    "is-stream": ["is-stream@2.0.1", "", {}, "sha512-hFoiJiTl63nn+kstHGBtewWSKnQLpyb155KHheA1l39uvtO9nWIop1p3udqPcUd/xbF1VLMO4n7OI6p7RbngDg=="],

    "is-wsl": ["is-wsl@2.2.0", "", { "dependencies": { "is-docker": "^2.0.0" } }, "sha512-fKzAra0rGJUUBwGBgNkHZuToZcn+TtXHpeCgmkMJMMYx1sQDYaCSyjJBSCa2nH1DGm7s3n1oBnohoVTBaN7Lww=="],

    "isexe": ["isexe@2.0.0", "", {}, "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw=="],

    "jest-worker": ["jest-worker@27.5.1", "", { "dependencies": { "@types/node": "*", "merge-stream": "^2.0.0", "supports-color": "^8.0.0" } }, "sha512-7vuh85V5cdDofPyxn58nrPjBktZo0u9x1g8WtjQol+jZDaE+fhN+cIvTj11GndBnMnyfrUOG1sZQxCdjKh+DKg=="],

    "js-tokens": ["js-tokens@4.0.0", "", {}, "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ=="],

    "js-yaml": ["js-yaml@4.3.2", "", { "dependencies": { "argparse": "^2.0.1" }, "bin": { "js-yaml": "bin/js-yaml.js" } }, "sha512-SFNOvSJ+Dgf/9An904Yx+CgSlIPCkIpao4qo51lpee25TIRejdH3rhR4EZMGoNx3/TP3O+wzWuiTFl4sqbltzA=="],

    "jsesc": ["jsesc@3.1.0", "", { "bin": { "jsesc": "bin/jsesc" } }, "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA=="],

    "json-parse-even-better-errors": ["json-parse-even-better-errors@2.3.1", "", {}, "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w=="],

    "json-schema-traverse": ["json-schema-traverse@1.0.0", "", {}, "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug=="],

    "json5": ["json5@2.2.3", "", { "bin": { "json5": "lib/cli.js" } }, "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg=="],

    "kiwi-schema": ["kiwi-schema@0.5.0", "", { "bin": { "kiwic": "cli.js" } }, "sha512-X+FpfU0yTEtc6aTHS7VwbOpvQwRt70+pXXWRI5fd6CvWhe7pSVC854TVo4Zo0x5/wwcWj+/9KUlXpdcP0dY9AA=="],

    "kleur": ["kleur@3.0.3", "", {}, "sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w=="],

    "lines-and-columns": ["lines-and-columns@1.2.4", "", {}, "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg=="],

    "loader-runner": ["loader-runner@4.3.2", "", {}, "sha512-DFEqQ3ihfS9blba08cLfYf1NRAIEm+dDjic073DRDc3/JspI/8wYmtDsHwd3+4hwvdxSK7PGaElfTmm0awWJ4w=="],

    "lower-case": ["lower-case@2.0.2", "", { "dependencies": { "tslib": "^2.0.3" } }, "sha512-7fm3l3NAF9WfN6W3JOmf5drwpVqX78JtoGJ3A6W0a6ZnldM41w2fV5D490psKFTpMds8TJse/eHLFFsNHHjHgg=="],

    "lru-cache": ["lru-cache@6.0.0", "", { "dependencies": { "yallist": "^4.0.0" } }, "sha512-Jo6dJ04CmSjuznwJSS3pUeWmd/H0ffTlkXXgwZi+eq1UCmqQwCh+eLsYOYCwY991i2Fah4h1BEMCx4qThGbsiA=="],

    "mediabunny": ["mediabunny@1.50.8", "", { "dependencies": { "@types/dom-mediacapture-transform": "^0.1.11", "@types/dom-webcodecs": "0.1.13" } }, "sha512-LgykLyQzhdpo0V2yw3UXmOpj+b4JAGdpHBwsPE6kjSt8Za0d1VllD+FV7EGHBcdV4+oHUAo+yrqbVAWxNSDCPQ=="],

    "memfs": ["memfs@3.4.3", "", { "dependencies": { "fs-monkey": "1.0.3" } }, "sha512-eivjfi7Ahr6eQTn44nvTnR60e4a1Fs1Via2kCR5lHo/kyNoiMWaXCNJ/GpSd0ilXas2JSOl9B5FTIhflXu0hlg=="],

    "merge-stream": ["merge-stream@2.0.0", "", {}, "sha512-abv/qOcuPfk3URPfDzmZU1LKmuw8kT+0nIHvKrKgFrwifol/doWcdA4ZqsWQ8ENrFKkd67Mfpo/LovbIUsbt3w=="],

    "mime-db": ["mime-db@1.52.0", "", {}, "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg=="],

    "mime-types": ["mime-types@2.1.35", "", { "dependencies": { "mime-db": "1.52.0" } }, "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw=="],

    "mimic-fn": ["mimic-fn@2.1.0", "", {}, "sha512-OqbOk5oEQeAZ8WXWydlu9HJjz9WVdEIvamMCcXmuqUYjTknH/sqsWvhQ3vgwKFRR1HpjvNBKQ37nbJgYzGqGcg=="],

    "minimist": ["minimist@1.2.6", "", {}, "sha512-Jsjnk4bw3YJqYzbdyBiNsPWHPfO++UGG749Cxs6peCu5Xg4nrena6OVxOYxrQTqww0Jmwt+Ref8rggumkTLz9Q=="],

    "ms": ["ms@2.1.3", "", {}, "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA=="],

    "nanoid": ["nanoid@3.3.20", "", { "bin": { "nanoid": "bin/nanoid.cjs" } }, "sha512-uKdg2G3GNCKQn9byYOpxbGqrT2fGO5KRt5J/8b3pok8rT6qxGWF6hxMyJiEYtAf+FVyYuD9hRaDqX5uPFYJ4ZQ=="],

    "neo-async": ["neo-async@2.6.2", "", {}, "sha512-Yd3UES5mWCSqR+qNT93S3UoYUkqAZ9lLg8a7g9rimsWmYGK8cVToA4/sF3RrshdyV3sAGMXVUmpMYOw+dLpOuw=="],

    "no-case": ["no-case@3.0.4", "", { "dependencies": { "lower-case": "^2.0.2", "tslib": "^2.0.3" } }, "sha512-fgAN3jGAh+RoxUGZHTSOLJIqUc2wmoBwGR4tbpNAKmmovFoWq0OdRkb0VkldReO2a2iBT/OEulG9XSUc10r3zg=="],

    "node-releases": ["node-releases@2.0.59", "", {}, "sha512-5qr2okC4ItAI0hG5SaV0HoYMpnM/Y6+Oqr7AmPYy/2uEoGvS+GbSKLeRxSS1uAdu59yz0ouzcuXievSgg///WA=="],

    "npm-run-path": ["npm-run-path@4.0.1", "", { "dependencies": { "path-key": "^3.0.0" } }, "sha512-S48WzZW777zhNIrn7gxOlISNAqi9ZC/uQFnRdbeIHhZhCA6UqpkOT8T1G7BvfdgP4Er8gF4sUbaS0i7QvIfCWw=="],

    "onetime": ["onetime@5.1.2", "", { "dependencies": { "mimic-fn": "^2.1.0" } }, "sha512-kbpaSSGJTWdAY5KPVeMOKXSrPtr8C8C7wodJbcsd51jRnmD+GZu8Y0VoU6Dm5Z4vWr0Ig/1NKuWRKf7j5aaYSg=="],

    "open": ["open@8.4.2", "", { "dependencies": { "define-lazy-prop": "^2.0.0", "is-docker": "^2.1.1", "is-wsl": "^2.2.0" } }, "sha512-7x81NCL719oNbsq/3mh+hVrAWmFuEYUqrq/Iw3kUzH8ReypT9QQ0BLoJS7/G9k6N81XjW4qHWtjWwe/9eLy1EQ=="],

    "parent-module": ["parent-module@1.0.1", "", { "dependencies": { "callsites": "^3.0.0" } }, "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g=="],

    "parse-json": ["parse-json@5.2.0", "", { "dependencies": { "@babel/code-frame": "^7.0.0", "error-ex": "^1.3.1", "json-parse-even-better-errors": "^2.3.0", "lines-and-columns": "^1.1.6" } }, "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg=="],

    "path-key": ["path-key@3.1.1", "", {}, "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q=="],

    "path-type": ["path-type@4.0.0", "", {}, "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw=="],

    "picocolors": ["picocolors@1.1.1", "", {}, "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA=="],

    "postcss": ["postcss@8.5.30", "", { "dependencies": { "nanoid": "^3.3.20", "picocolors": "^1.1.1", "source-map-js": "^1.2.2" } }, "sha512-zkd+e9S1AQHhmaBKye9zlFHWjOwVgqXl1q3ECYy8561K7qxR2cREf/STLskulBFd78k6AOFeA+ff1TtEzk9bAA=="],

    "postcss-modules-extract-imports": ["postcss-modules-extract-imports@3.1.0", "", { "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-k3kNe0aNFQDAZGbin48pL2VNidTF0w4/eASDsxlyspobzU3wZQLOGj7L9gfRe0Jo9/4uud09DsjFNH7winGv8Q=="],

    "postcss-modules-local-by-default": ["postcss-modules-local-by-default@4.2.0", "", { "dependencies": { "icss-utils": "^5.0.0", "postcss-selector-parser": "^7.0.0", "postcss-value-parser": "^4.1.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-5kcJm/zk+GJDSfw+V/42fJ5fhjL5YbFDl8nVdXkJPLLW+Vf9mTD5Xe0wqIaDnLuL2U6cDNpTr+UQ+v2HWIBhzw=="],

    "postcss-modules-scope": ["postcss-modules-scope@3.2.1", "", { "dependencies": { "postcss-selector-parser": "^7.0.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-m9jZstCVaqGjTAuny8MdgE88scJnCiQSlSrOWcTQgM2t32UBe+MUmFSO5t7VMSfAf/FJKImAxBav8ooCHJXCJA=="],

    "postcss-modules-values": ["postcss-modules-values@4.0.0", "", { "dependencies": { "icss-utils": "^5.0.0" }, "peerDependencies": { "postcss": "^8.1.0" } }, "sha512-RDxHkAiEGI78gS2ofyvCsu7iycRv7oqw5xMWn9iMoR0N/7mf9D50ecQqUo5BZ9Zh2vH4bCUR/ktCqbB9m8vJjQ=="],

    "postcss-selector-parser": ["postcss-selector-parser@7.1.6", "", { "dependencies": { "cssesc": "^3.0.0", "util-deprecate": "^1.0.2" } }, "sha512-7qASPzhKF2l2KLboRZux8CCTRMdGiV08vWmyKzPz22qZ7ZjQBOeY7rNzNoCLSUiftJ7HUq0GERHmxw/t0dCdMw=="],

    "postcss-value-parser": ["postcss-value-parser@4.2.0", "", {}, "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ=="],

    "prettier": ["prettier@3.8.1", "", { "bin": { "prettier": "bin/prettier.cjs" } }, "sha512-UOnG6LftzbdaHZcKoPFtOcCKztrQ57WkHDeRD9t/PTQtmT0NHSeWWepj6pS0z/N7+08BHFDQVUrfmfMRcZwbMg=="],

    "prompts": ["prompts@2.4.2", "", { "dependencies": { "kleur": "^3.0.3", "sisteransi": "^1.0.5" } }, "sha512-NxNv/kLguCA7p3jE8oL2aEBsrJWgAakBpgmgK6lpPWV+WuOmY6r2/zbAVnP+T8bQlA0nzHXSJSJW0Hq7ylaD2Q=="],

    "react": ["react@19.2.8", "", {}, "sha512-PWaYA1L/q9u2u7xYQi+Y3L3Yfnie7XyLeaJICV1MGD6LprsBxcAqGjYyr0eY3p+QdsA+x/Irkt4Qif8D63+Sbw=="],

    "react-dom": ["react-dom@19.2.8", "", { "dependencies": { "scheduler": "^0.27.0" }, "peerDependencies": { "react": "^19.2.8" } }, "sha512-rVprimfGBG3DR+Tq0IQG2DT5PxKth1WIGDmj5yPmlzr4YBe7uyE+Du4oVqTDXZSHGGGXRtTJEGSSePyQCMBglQ=="],

    "react-refresh": ["react-refresh@0.18.0", "", {}, "sha512-QgT5//D3jfjJb6Gsjxv0Slpj23ip+HtOpnNgnb2S5zU3CB26G/IDPGoy4RJB42wzFE46DRsstbW6tKHoKbhAxw=="],

    "recast": ["recast@0.23.11", "", { "dependencies": { "ast-types": "^0.16.1", "esprima": "~4.0.0", "source-map": "~0.6.1", "tiny-invariant": "^1.3.3", "tslib": "^2.0.1" } }, "sha512-YTUo+Flmw4ZXiWfQKGcwwc11KnoRAYgzAE2E7mXKCjSviTKShtxBsN6YUUBB2gtaBzKzeKunxhUwNHQuRryhWA=="],

    "remotion": ["remotion@4.0.507", "", { "peerDependencies": { "react": ">=16.8.0", "react-dom": ">=16.8.0" } }, "sha512-g/NrnRZKJyh0isE+/0sIxKlgJl6BH5v/CJ35W4TGYR1obQZf60fHkf9CGxSBHJEw27dG1PJCgKT75YGfoCZ7tg=="],

    "require-from-string": ["require-from-string@2.0.2", "", {}, "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw=="],

    "resolve-from": ["resolve-from@4.0.0", "", {}, "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g=="],

    "scheduler": ["scheduler@0.27.0", "", {}, "sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q=="],

    "schema-utils": ["schema-utils@4.5.0", "", { "dependencies": { "@types/json-schema": "^7.0.15", "ajv": "^8.20.0", "ajv-formats": "^3.0.1", "ajv-keywords": "^5.1.0" } }, "sha512-zJlMCZ0cAR5p/Y4oVpRoqioDMJcGxaXRrQ/4rP4WyR84vc5z/DolXdbvXeDpTwbtocDFr2rhPqHPErDCUtz2kA=="],

    "semver": ["semver@7.5.3", "", { "dependencies": { "lru-cache": "^6.0.0" }, "bin": { "semver": "bin/semver.js" } }, "sha512-QBlUtyVk/5EeHbi7X0fw6liDZc7BBmEaSYn01fMU1OUYbf6GPsbTtd8WmnqbI20SeycoHSeiybkE/q1Q+qlThQ=="],

    "shebang-command": ["shebang-command@2.0.0", "", { "dependencies": { "shebang-regex": "^3.0.0" } }, "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA=="],

    "shebang-regex": ["shebang-regex@3.0.0", "", {}, "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A=="],

    "signal-exit": ["signal-exit@3.0.7", "", {}, "sha512-wnD2ZE+l+SPC/uoS0vXeE9L1+0wuaMqKlfz9AMUo38JsyLSBWSFcHR1Rri62LZc12vLr1gb3jl7iwQhgwpAbGQ=="],

    "sisteransi": ["sisteransi@1.0.5", "", {}, "sha512-bLGGlR1QxBcynn2d5YmDX4MGjlZvy2MRBDRNHLJ8VI6l6+9FUiyTFNJ0IveOSP0bcXgVDPRcfGqA0pjaqUpfVg=="],

    "snake-case": ["snake-case@3.0.4", "", { "dependencies": { "dot-case": "^3.0.4", "tslib": "^2.0.3" } }, "sha512-LAOh4z89bGQvl9pFfNF8V146i7o7/CqFPbqzYgP+yYzDIDeS9HaNFtXABamRW+AQzEVODcvE79ljJ+8a9YSdMg=="],

    "source-map": ["source-map@0.8.0", "", {}, "sha512-d8EqvL+k/SOXCreS/SUzg2ciyHqBBLcN/yuRjFsbvVhHTE2pgei7oAhmPM7kWFbkX6OSMQfUq4KbkF3au9lhYQ=="],

    "source-map-js": ["source-map-js@1.2.2", "", {}, "sha512-KGj/8Y43x35aZVDtt+J4mK1hoLGHULMYfSkODJNQjNDC3oW1PqPoxMwo0pLUsWM/UEGzON/NxeHywEfNXNP3Vw=="],

    "source-map-support": ["source-map-support@0.5.21", "", { "dependencies": { "buffer-from": "^1.0.0", "source-map": "^0.6.0" } }, "sha512-uBHU3L3czsIyYXKX88fdrGovxdSCoTGDRZ6SYXtSRxLZUzHg5P/66Ht6uoUlHu9EZod+inXhKo3qQgwXUT/y1w=="],

    "stackframe": ["stackframe@1.3.4", "", {}, "sha512-oeVtt7eWQS+Na6F//S4kJ2K2VbRlS9D43mAlMyVpVWovy9o+jfgH8O9agzANzaiLjclA0oYzUXEM4PurhSUChw=="],

    "strip-final-newline": ["strip-final-newline@2.0.0", "", {}, "sha512-BrpvfNAE3dcvq7ll3xVumzjKjZQ5tI1sEUIKr3Uoks0XUl45St3FlatVqef9prk4jRDzhW6WZg+3bk93y6pLjA=="],

    "style-loader": ["style-loader@4.0.0", "", { "peerDependencies": { "webpack": "^5.27.0" } }, "sha512-1V4WqhhZZgjVAVJyt7TdDPZoPBPNHbekX4fWnCJL1yQukhCeZhJySUL+gL9y6sNdN95uEOS83Y55SqHcP7MzLA=="],

    "supports-color": ["supports-color@8.1.1", "", { "dependencies": { "has-flag": "^4.0.0" } }, "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q=="],

    "svg-parser": ["svg-parser@2.1.0", "", {}, "sha512-bwLf38YmY+TDYHJw1Ex0Co8c4yeXuJAo8YnXGZrscxrvYoVVIvLeniEkV1Ks/54VteMnL4FtyN1+P+TZJdUPmQ=="],

    "tapable": ["tapable@2.3.3", "", {}, "sha512-uxc/zpqFg6x7C8vOE7lh6Lbda8eEL9zmVm/PLeTPBRhh1xCgdWaQ+J1CUieGpIfm2HdtsUpRv+HshiasBMcc6A=="],

    "terser": ["terser@5.51.2", "", { "dependencies": { "@jridgewell/source-map": "^0.3.3", "acorn": "^8.15.0", "commander": "^2.20.0", "source-map-support": "~0.5.20" }, "bin": { "terser": "bin/terser" } }, "sha512-bWnjSNscmuI+GJze6ZupnHP8G/cTcsJF+bXCeQknk2SHQsgbNJnLrqiH9jZ2W4STPVXH2mDKKRX3iwPhc9Cn/Q=="],

    "terser-webpack-plugin": ["terser-webpack-plugin@5.6.1", "", { "dependencies": { "@jridgewell/trace-mapping": "^0.3.25", "jest-worker": "^27.4.5", "schema-utils": "^4.3.0", "terser": "^5.31.1" }, "peerDependencies": { "@minify-html/node": "*", "@swc/core": "*", "@swc/css": "*", "@swc/html": "*", "clean-css": "*", "cssnano": "*", "csso": "*", "esbuild": "*", "html-minifier-terser": "*", "lightningcss": "*", "postcss": "*", "uglify-js": "*", "webpack": "^5.1.0" }, "optionalPeers": ["@minify-html/node", "@swc/core", "@swc/css", "@swc/html", "clean-css", "cssnano", "csso", "esbuild", "html-minifier-terser", "lightningcss", "postcss", "uglify-js"] }, "sha512-201R5j+sJpK8nFWwKVyNfZot8FaJbLZDq5evriVzbV1wDtSXDjRUDRfJzHpAaxFDMEhsZL1QkeqM61wgsS3KaQ=="],

    "tiny-invariant": ["tiny-invariant@1.3.3", "", {}, "sha512-+FbBPE1o9QAYvviau/qC5SE3caw21q3xkvWKBtja5vgqOWIHHJ3ioaq1VPfn/Szqctz2bU/oYeKd9/z5BL+PVg=="],

    "to-fast-properties": ["to-fast-properties@2.0.0", "", {}, "sha512-/OaKK0xYrs3DmxRYqL/yDc+FxFUVYhDlXMhRmv3z915w2HF1tnN1omB354j8VUGO/hbRzyD6Y3sA7v7GS/ceog=="],

    "tslib": ["tslib@2.8.1", "", {}, "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w=="],

    "typescript": ["typescript@5.9.3", "", { "bin": { "tsc": "bin/tsc", "tsserver": "bin/tsserver" } }, "sha512-jl1vZzPDinLr9eUt3J/t7V6FgNEw9QjvBPdysz9KfQDD41fQrC2Y4vKQdiaUpFT4bXlb1RHhLpp8wtm6M5TgSw=="],

    "undici-types": ["undici-types@8.9.0", "", {}, "sha512-KTDyRTYX8sWmKXAikPHHSyc63CRPETMctyjKFupcC6OBLXT3xsN0e9aF7m+mIXutFWpUXuedtowG7iLOzp0kQg=="],

    "update-browserslist-db": ["update-browserslist-db@1.3.4", "", { "dependencies": { "escalade": "^3.2.0", "picocolors": "^1.1.1" }, "peerDependencies": { "browserslist": ">= 4.21.0" }, "bin": { "update-browserslist-db": "cli.js" } }, "sha512-t8wonIOdQyOjtPd2VktlBu6QjTVTks6v8bSi7kd0r2Vll8TK1JYDZtRRdbmCHOAMphkZgrzK+L+vXK4pyZ8t4A=="],

    "util-deprecate": ["util-deprecate@1.0.2", "", {}, "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw=="],

    "watchpack": ["watchpack@2.6.1", "", { "dependencies": { "graceful-fs": "^4.1.2" } }, "sha512-8mk/LnXpQAiM2xKZhTkxikwly5GhL2Z+DWiLTkMa/E1Nfv9zURhHgiFyWvM4BWqW+LjIgL2AIS7JntEUx6v3vQ=="],

    "webpack": ["webpack@5.105.0", "", { "dependencies": { "@types/eslint-scope": "^3.7.7", "@types/estree": "^1.0.8", "@types/json-schema": "^7.0.15", "@webassemblyjs/ast": "^1.14.1", "@webassemblyjs/wasm-edit": "^1.14.1", "@webassemblyjs/wasm-parser": "^1.14.1", "acorn": "^8.15.0", "acorn-import-phases": "^1.0.3", "browserslist": "^4.28.1", "chrome-trace-event": "^1.0.2", "enhanced-resolve": "^5.19.0", "es-module-lexer": "^2.0.0", "eslint-scope": "5.1.1", "events": "^3.2.0", "glob-to-regexp": "^0.4.1", "graceful-fs": "^4.2.11", "json-parse-even-better-errors": "^2.3.1", "loader-runner": "^4.3.1", "mime-types": "^2.1.27", "neo-async": "^2.6.2", "schema-utils": "^4.3.3", "tapable": "^2.3.0", "terser-webpack-plugin": "^5.3.16", "watchpack": "^2.5.1", "webpack-sources": "^3.3.3" }, "peerDependencies": { "webpack-cli": "*" }, "optionalPeers": ["webpack-cli"], "bin": { "webpack": "bin/webpack.js" } }, "sha512-gX/dMkRQc7QOMzgTe6KsYFM7DxeIONQSui1s0n/0xht36HvrgbxtM1xBlgx596NbpHuQU8P7QpKwrZYwUX48nw=="],

    "webpack-sources": ["webpack-sources@3.6.0", "", {}, "sha512-EIMmPVvNI0CYXyRPp34F2Qk7W37/BZVZIofS6LAUnrNjCVahS+hO4mxwFJDjQjODTGZDtVzLYoN2+1dYkhk9qA=="],

    "which": ["which@2.0.2", "", { "dependencies": { "isexe": "^2.0.0" }, "bin": { "node-which": "./bin/node-which" } }, "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA=="],

    "ws": ["ws@8.21.0", "", { "peerDependencies": { "bufferutil": "^4.0.1", "utf-8-validate": ">=5.0.2" }, "optionalPeers": ["bufferutil", "utf-8-validate"] }, "sha512-Vsp28b7DRcimFQvrqu2Wek3z1iYxDCWqHYB8Qsnk/S4RfaCQzPGPyBNuVjJV3cd6UiKtUtp6sNM77gWvzcCH+g=="],

    "yallist": ["yallist@4.0.0", "", {}, "sha512-3wdGidZyq5PB084XLES5TpOSRA3wjXAlIWMhum2kRcv/41Sn2emQ0dycQW4uZXLejwKvg6EsvbdlVL+FYEct7A=="],

    "zod": ["zod@4.4.3", "", {}, "sha512-ytENFjIJFl2UwYglde2jchW2Hwm4GJFLDiSXWdTrJQBIN9Fcyp7n4DhxJEiWNAJMV1/BqWfW/kkg71UDcHJyTQ=="],

    "@babel/core/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/core/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/core/semver": ["semver@6.3.1", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA=="],

    "@babel/generator/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/generator/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/helper-compilation-targets/lru-cache": ["lru-cache@5.1.1", "", { "dependencies": { "yallist": "^3.0.2" } }, "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w=="],

    "@babel/helper-compilation-targets/semver": ["semver@6.3.1", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA=="],

    "@babel/helper-module-imports/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/helpers/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/template/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/template/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "@babel/traverse/@babel/parser": ["@babel/parser@7.29.9", "", { "dependencies": { "@babel/types": "^7.29.8" }, "bin": "./bin/babel-parser.js" }, "sha512-CjXrNHTnvqBVqHgdBysY3vk2T8tpJHb5/RMeHJBTyVa9xgugCB0CJTx/3oO8RV2QRQP391RWpB7D6hLjm8V9uA=="],

    "@babel/traverse/@babel/types": ["@babel/types@7.29.8", "", { "dependencies": { "@babel/helper-string-parser": "^7.29.7", "@babel/helper-validator-identifier": "^7.29.7" } }, "sha512-Vj1jF3cPfxg7OAfoI7QnVKLoILlm2JF9pnVHrX8qx7AHMiYWT+NDAA7jChlNgRS4WTLc/fD1lXLmPixluj+3Gg=="],

    "css-loader/semver": ["semver@7.8.5", "", { "bin": { "semver": "bin/semver.js" } }, "sha512-Y7/KDsb8LjooZpwaqGyulO6DQlksgCncchHGk+sZIY4SBvUocMBEFH5Ur1fI4dV+Jvl0w6cjvucaIi40puRioA=="],

    "esrecurse/estraverse": ["estraverse@5.3.0", "", {}, "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA=="],

    "recast/ast-types": ["ast-types@0.16.3", "", { "dependencies": { "tslib": "^2.0.1" } }, "sha512-FvWoWYfSCM6kRxCSH+MGLHIKKGRL6A6AW7Zek2O32REPQRdg131428uRTKMBYAeRd3XXAaHDS60Wpri7CdKDrA=="],

    "recast/source-map": ["source-map@0.6.1", "", {}, "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g=="],

    "source-map-support/source-map": ["source-map@0.6.1", "", {}, "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g=="],

    "@babel/helper-compilation-targets/lru-cache/yallist": ["yallist@3.1.1", "", {}, "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g=="],
  }
}
````
