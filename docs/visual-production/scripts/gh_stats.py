"""Fetch GitHub facts for every card with a `github:` field.

Writes tables/github.csv and fills the gh-stats block of each card.
Uses one GitHub API call per repo (60 an hour without GITHUB_TOKEN);
release and commit dates come from public Atom feeds.
Rows already fetched today are reused unless --force is given.

    python3 docs/visual-production/scripts/gh_stats.py [--force] [id ...]
"""
import csv
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from vp_common import TABLES, cards

TODAY = datetime.date.today().isoformat()
FIELDS = ["repo", "stars", "license", "archived", "pushed", "last_commit", "last_release", "last_release_date", "checked"]
ATOM = "{http://www.w3.org/2005/Atom}"


def get(url, api=False):
    headers = {"User-Agent": "visual-production-library"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
        return resp.read()


def first_entry(repo, feed):
    """Tag (from the entry link) and date of the newest entry of a repo Atom feed, or ('', '')."""
    try:
        root = ET.fromstring(get(f"https://github.com/{repo}/{feed}.atom"))
    except (urllib.error.URLError, ET.ParseError):
        return "", ""
    entry = root.find(ATOM + "entry")
    if entry is None:
        return "", ""
    link = entry.find(ATOM + "link")
    href = link.get("href", "") if link is not None else ""
    name = urllib.parse.unquote(href.rsplit("/", 1)[-1]) if "/releases/tag/" in href else ""
    return name or (entry.findtext(ATOM + "title") or "").strip(), (entry.findtext(ATOM + "updated") or "")[:10]


def fetch(repo, cached=None):
    """API facts (reused from `cached` when given) plus fresh Atom-feed dates."""
    if cached:
        row = dict(cached)
    else:
        meta = json.loads(get(f"https://api.github.com/repos/{repo}", api=True))
        row = {
            "repo": meta["full_name"],
            "stars": meta["stargazers_count"],
            "license": (meta.get("license") or {}).get("spdx_id") or "нет",
            "archived": "да" if meta["archived"] else "нет",
            "pushed": meta["pushed_at"][:10],
            "checked": TODAY,
        }
    row["last_release"], row["last_release_date"] = first_entry(row["repo"], "releases")
    _, row["last_commit"] = first_entry(row["repo"], "commits")
    return row


def block(row):
    lic = row["license"] if row["license"] not in ("NOASSERTION", "нет") else "GitHub не определил, см. «Лицензия и права»"
    release = f"{row['last_release']} ({row['last_release_date']})" if row["last_release"] else "релизов и тегов в ленте нет"
    return "\n".join([
        f"- Звёзды GitHub: {int(row['stars']):,}".replace(",", " "),
        f"- Последний коммит в основной ветке: {row['last_commit'] or 'лента коммитов не получена'}",
        f"- Последний релиз или тег: {release}",
        f"- Лицензия по данным GitHub: {lic}",
        f"- Репозиторий в архиве: {row['archived']}",
        f"- Источник: GitHub API и Atom-ленты репозитория {row['repo']}, получено {row['checked']}.",
    ])


def main():
    force = "--force" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = TABLES / "github.csv"
    rows = {}
    if out.exists():
        with out.open(encoding="utf-8") as f:
            rows = {r["id"]: r for r in csv.DictReader(f)}
    failed = []
    for path, fm in cards():
        if only and fm.get("id") not in only:
            continue
        repo = fm.get("github", "none")
        if repo in ("", "none"):
            rows.pop(fm.get("id"), None)
            continue
        old = rows.get(fm["id"])
        fresh = old and old["checked"] == TODAY and old["repo"].lower() == repo.lower()
        try:
            rows[fm["id"]] = {"id": fm["id"], **fetch(repo, None if force or not fresh else old)}
        except urllib.error.HTTPError as e:
            failed.append(f"{fm['id']} ({repo}): HTTP {e.code}")
            if e.code in (403, 429):
                break
            continue
        text = path.read_text(encoding="utf-8")
        new = re.sub(
            r"(<!-- gh-stats:[^>]*-->)\n.*?(<!-- /gh-stats -->)",
            lambda m: m.group(1) + "\n" + block(rows[fm["id"]]) + "\n" + m.group(2),
            text, flags=re.S)
        if new == text and "<!-- gh-stats:" not in text:
            failed.append(f"{fm['id']}: no gh-stats block")
        path.write_text(new, encoding="utf-8")
    TABLES.mkdir(exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id"] + FIELDS, lineterminator="\n")
        w.writeheader()
        for key in sorted(rows):
            w.writerow(rows[key])
    print(f"{len(rows)} repos in {out}")
    for line in failed:
        print("FAILED", line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
