"""Shared helpers for the visual-production library scripts (stdlib only)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
TABLES = ROOT / "tables"


def front_matter(path):
    """Return the flat key: value front matter of a card; lists become Python lists."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        data[key.strip()] = value
    return data


def cards():
    """Yield (path, front matter) for every tool card."""
    for path in sorted(TOOLS.glob("*.md")):
        yield path, front_matter(path)
