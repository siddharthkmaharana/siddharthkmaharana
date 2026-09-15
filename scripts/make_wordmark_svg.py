#!/usr/bin/env python3
"""
make_wordmark_svg.py --mode rock --out wordmark.svg

Builds a monochrome "extruded" ASCII-style wordmark: the text is drawn as
stacked layers with a small offset per layer (fake 3D depth), each layer
darker than the one above it, then the whole block gently rocks left/right
using a 3D CSS transform driven by SMIL.
"""
import argparse

# ---------------- [CONFIG] ----------------
TEXT = "SIDDHARTH"
FONT_SIZE = 150
FONT_WEIGHT = 800
DEPTH_LAYERS = 14          # number of extrusion layers
DEPTH_OFFSET = 2.1         # px offset per layer
ROW_MARGIN = 85            # top/bottom margin -> tunes total height to match portrait (~385px target)
ROCK_DEGREES = 10
ROCK_DURATION = 4.2        # seconds for one full left-right-left cycle
TOP_COLOR = (230, 236, 241)     # face color (front-most layer)
DEPTH_COLOR_DARK = (13, 17, 23)  # far extrusion layer color (matches bg)
BG = "#0d1117"
DIM = "#30363d"
USERNAME = "siddharthkmaharana@github"
# -------------------------------------------


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def build_svg(text, out_path, mode="rock"):
    char_w_ratio = 0.62
    text_w = len(text) * FONT_SIZE * char_w_ratio
    pad_x = 40
    extra_depth = DEPTH_LAYERS * DEPTH_OFFSET
    width = text_w + pad_x * 2 + extra_depth
    height = FONT_SIZE + ROW_MARGIN * 2 + extra_depth + 30

    cx = width / 2
    cy = height / 2 + 10

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="100%">')
    svg.append(f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" rx="10" fill="{BG}"/>')
    svg.append(f'<rect x="0.5" y="0.5" width="{width-1:.0f}" height="{height-1:.0f}" rx="10" fill="none" stroke="{DIM}"/>')
    svg.append(
        f'<text x="20" y="24" font-family="Consolas,Menlo,monospace" '
        f'font-size="10" fill="{DIM}">{USERNAME} ~ $ ./whoami.sh</text>'
    )

    anim_id = "rockGroup"
    style = f"""
<style>
  #{anim_id} {{
    transform-box: fill-box;
    transform-origin: 50% 50%;
  }}
  .wordmark-text {{
    font-family: 'Consolas','SF Mono','Menlo',monospace;
    font-weight: {FONT_WEIGHT};
    font-size: {FONT_SIZE}px;
    letter-spacing: 2px;
  }}
</style>
"""
    svg.append(style)

    svg.append(f'<g id="{anim_id}">')
    if mode == "rock":
        svg.append(
            f'<animateTransform attributeName="transform" type="rotate" '
            f'values="-{ROCK_DEGREES} {cx:.1f} {cy:.1f}; {ROCK_DEGREES} {cx:.1f} {cy:.1f}; -{ROCK_DEGREES} {cx:.1f} {cy:.1f}" '
            f'keyTimes="0;0.5;1" dur="{ROCK_DURATION}s" '
            f'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
            f'repeatCount="indefinite"/>'
        )

    text_x = pad_x
    text_y = height / 2 + FONT_SIZE * 0.32

    # extrusion layers, back to front
    for i in range(DEPTH_LAYERS, -1, -1):
        t = i / DEPTH_LAYERS
        color = lerp(TOP_COLOR, DEPTH_COLOR_DARK, t)
        dx = i * DEPTH_OFFSET * 0.72
        dy = i * DEPTH_OFFSET
        svg.append(
            f'<text class="wordmark-text" x="{text_x + dx:.1f}" y="{text_y + dy:.1f}" '
            f'fill="{to_hex(color)}">{text}</text>'
        )

    svg.append("</g>")
    svg.append("</svg>")

    with open(out_path, "w") as f:
        f.write("\n".join(svg))
    print(f"wrote {out_path}  ({width:.0f}x{height:.0f}px, text='{text}')")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="rock", choices=["rock", "static"])
    ap.add_argument("--out", default="wordmark.svg")
    ap.add_argument("--text", default=TEXT)
    args = ap.parse_args()
    build_svg(args.text, args.out, mode=args.mode)
