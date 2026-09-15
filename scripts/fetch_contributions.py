#!/usr/bin/env python3
"""
fetch_contributions.py USERNAME [out.json]
Scrapes github.com/users/USERNAME/contributions (the fragment GitHub itself
lazy-loads on profile pages) and writes [{date, level, count_hint}, ...].
"""
import sys
import re
import json
import urllib.request

CELL_RE = re.compile(
    r'data-date="(?P<date>\d{4}-\d{2}-\d{2})"[^>]*data-level="(?P<level>\d)"'
)
# some markup orders attrs the other way around; handle both
CELL_RE_ALT = re.compile(
    r'data-level="(?P<level>\d)"[^>]*data-date="(?P<date>\d{4}-\d{2}-\d{2})"'
)


def fetch(username):
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")


def parse(html):
    cells = []
    for m in CELL_RE.finditer(html):
        cells.append((m.group("date"), int(m.group("level"))))
    if not cells:
        for m in CELL_RE_ALT.finditer(html):
            cells.append((m.group("date"), int(m.group("level"))))
    cells.sort(key=lambda c: c[0])
    return cells


if __name__ == "__main__":
    username = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "contributions.json"
    html = fetch(username)
    cells = parse(html)
    with open(out, "w") as f:
        json.dump(cells, f)
    print(f"parsed {len(cells)} days -> {out}")
