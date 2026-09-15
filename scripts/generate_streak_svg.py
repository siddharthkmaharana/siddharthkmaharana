#!/usr/bin/env python3
"""
generate_streak_svg.py USERNAME OUT.svg

Fetches the user's real GitHub contribution calendar and renders it as a
borderless, transparent, monochrome SVG where each day-cell pops in and
flashes brighter once, staggered left-to-right (oldest -> newest).
"""
import sys
import datetime
from fetch_contributions import fetch, parse

CELL = 11
GAP = 3
RADIUS = 2
BG = "#0d1117"
LEVEL_COLORS = ["#161b22", "#2d3a4f", "#39567a", "#4f7fb3", "#79c0ff"]
STAGGER = 0.012          # seconds between successive week-columns starting
CELL_STAGGER = 0.0025    # extra stagger per row within a column
POP_DUR = 0.5


def build(cells, out_path, username):
    # bucket into weeks (columns), GitHub week starts Sunday
    if not cells:
        raise SystemExit("no contribution cells parsed")

    dated = [
        (datetime.date.fromisoformat(d), lvl) for d, lvl in cells
    ]
    dated.sort(key=lambda x: x[0])

    # find the Sunday on/before the first date to align the grid
    first = dated[0][0]
    start = first - datetime.timedelta(days=(first.weekday() + 1) % 7)

    weeks = {}
    for date, lvl in dated:
        offset_days = (date - start).days
        week_idx = offset_days // 7
        row = offset_days % 7
        weeks.setdefault(week_idx, {})[row] = (date, lvl)

    n_weeks = max(weeks.keys()) + 1
    width = n_weeks * (CELL + GAP) + GAP
    height = 7 * (CELL + GAP) + GAP + 20

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%">')
    style = """
<style>
  .contrib-cell {
    animation: popflash 0.6s cubic-bezier(.34,1.56,.64,1) both;
  }
  @keyframes popflash {
    0%   { transform: scale(0); opacity: 0; }
    55%  { transform: scale(1.35); opacity: 1; filter: brightness(1.8); }
    100% { transform: scale(1); opacity: 1; filter: brightness(1); }
  }
</style>
"""
    svg.append(style)

    total_contrib = sum(lvl_to_count(lvl) for _, lvl in dated)  # rough visual only

    for w in range(n_weeks):
        col = weeks.get(w, {})
        for row in range(7):
            if row not in col:
                continue
            date, lvl = col[row]
            x = GAP + w * (CELL + GAP)
            y = GAP + row * (CELL + GAP) + 14
            color = LEVEL_COLORS[min(lvl, len(LEVEL_COLORS) - 1)]
            delay = w * STAGGER + row * CELL_STAGGER
            svg.append(
                f'<rect class="contrib-cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{color}" '
                f'style="animation-delay:{delay:.3f}s; transform-box: fill-box; transform-origin: 50% 50%;">'
                f'<title>{date.isoformat()} · level {lvl}</title>'
                f'</rect>'
            )

    svg.append("</svg>")
    with open(out_path, "w") as f:
        f.write("\n".join(svg))
    print(f"wrote {out_path}  ({n_weeks} weeks x 7 days, {len(dated)} cells)")


def lvl_to_count(lvl):
    return [0, 1, 3, 6, 10][min(lvl, 4)]


if __name__ == "__main__":
    username = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    html = fetch(username)
    cells = parse(html)
    build(cells, out, username)
