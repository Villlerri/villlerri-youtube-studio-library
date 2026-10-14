"""Build the comparison tables from the tool cards and check the library.

Writes tables/tools.csv (one row per tool) and tables/by-scene.csv
(one row per scene type and tool, without sync-only tools). Prints card fields that break
method.md and relative links that point at missing files.

    python3 docs/visual-production/scripts/build_tables.py
"""
import csv
import re
import sys

from vp_common import ROOT, TABLES, cards

CLASSES = ["2d-code", "motion-design", "web-graphics", "3d", "simulation", "frame-vector-skeletal",
           "whiteboard", "edit-composite", "procedural", "generative", "hybrid", "sync"]
SCENES = ["formula", "graph", "diagram", "mechanism", "field", "micro", "scale", "simulation",
          "character", "drawing", "real-footage", "typography", "map-timeline", "screen"]
MATURITY = ["experimental", "young", "stable", "standard", "declining", "abandoned"]
SCORES = ["quality", "human_difficulty", "agent_difficulty", "automation", "reproducibility"]
COLUMNS = ["id", "name", "class", "kind", "scenes", "quality", "human_difficulty", "agent_difficulty",
           "automation", "reproducibility", "cost", "price", "maturity", "platforms", "export",
           "code_license", "gh_stars", "gh_last_commit", "gh_last_release", "site", "github", "checked", "card"]


def problems(fm):
    out = []
    for key in COLUMNS[:-1]:
        if key.startswith("gh_"):
            continue
        if fm.get(key) in (None, "", []):
            out.append(f"missing {key}")
    out += [f"class {c}?" for c in fm.get("class", []) if c not in CLASSES]
    out += [f"scene {s}?" for s in fm.get("scenes", []) if s not in SCENES]
    if fm.get("maturity") not in MATURITY:
        out.append(f"maturity {fm.get('maturity')}?")
    for key in SCORES:
        if fm.get(key) not in list("12345"):
            out.append(f"{key} {fm.get(key)}?")
    if fm.get("cost") not in list("0123?"):
        out.append(f"cost {fm.get('cost')}?")
    return out


def broken_links():
    out = []
    for path in ROOT.rglob("*.md"):
        if path.parent.name == "templates":
            continue
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                out.append(f"{path.relative_to(ROOT)} -> {target}")
    return out


def main():
    gh = {}
    if (TABLES / "github.csv").exists():
        with (TABLES / "github.csv").open(encoding="utf-8") as f:
            gh = {r["id"]: r for r in csv.DictReader(f)}
    rows, issues = [], []
    for path, fm in cards():
        issues += [f"{path.name}: {p}" for p in problems(fm)]
        g = gh.get(fm.get("id"), {})
        row = {k: "; ".join(v) if isinstance(v, list) else v for k, v in fm.items() if k in COLUMNS}
        row.update({
            "gh_stars": g.get("stars", ""),
            "gh_last_commit": g.get("last_commit", ""),
            "gh_last_release": g.get("last_release", ""),
            "card": f"tools/{path.name}",
        })
        rows.append((fm, row))
    rows.sort(key=lambda r: (CLASSES.index(r[0]["class"][0]) if r[0].get("class") and r[0]["class"][0] in CLASSES else 99, r[1]["id"]))
    TABLES.mkdir(exist_ok=True)
    with (TABLES / "tools.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(r for _, r in rows)
    # Sync-only tools (voice, alignment, subtitles) serve every scene; they stay out of the scene table.
    pairs = [(s, fm, row) for fm, row in rows if set(fm.get("class", [])) != {"sync"}
             for s in fm.get("scenes", []) if s in SCENES]
    pairs.sort(key=lambda p: (SCENES.index(p[0]), -int(p[2]["quality"] or 0), "0123?".find(p[2]["cost"] or "?"), p[2]["id"]))
    with (TABLES / "by-scene.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["scene", "id", "name", "quality", "human_difficulty", "agent_difficulty", "cost", "price", "card"])
        for s, _, r in pairs:
            w.writerow([s, r["id"], r["name"], r["quality"], r["human_difficulty"], r["agent_difficulty"], r["cost"], r["price"], r["card"]])
    issues += [f"broken link {b}" for b in broken_links()]
    print(f"{len(rows)} cards, {len(pairs)} scene rows")
    for line in issues:
        print("ISSUE", line)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
