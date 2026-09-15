#!/usr/bin/env python3
"""
make_ascii_svg.py <input_photo> <output_svg>

Converts a photo into a monochrome ASCII-art portrait rendered as a
self-typing terminal-style animated SVG (rows type in left-to-right,
top-to-bottom, with a blinking terminal cursor at the end).
"""
import os
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

STATIC = os.environ.get("STATIC") == "1"

# ---------------- [CONFIG] ----------------
USERNAME = "siddharthkmaharana@github"
COLS = 92                # ascii grid width (characters)
CHAR_ASPECT = 0.52        # terminal char cell height:width compensation
CONTRAST = 1.55
GAMMA = 0.72
WHITE_FLOOR = 4           # brightness floor (0-255) below which pixels go blank
RAMP = " .:-=+*#%@"       # 10-level brightness ramp
ROW_DUR = 0.028           # seconds "typing" speed per character (approx)
STAGGER = 0.55            # seconds between the start of each row typing
FONT_SIZE = 8
LINE_HEIGHT = FONT_SIZE * 1.02
BG = "#0d1117"
FG = "#c9d1d9"
DIM = "#30363d"
# -------------------------------------------


def load_and_prep(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode == "RGBA"
    alpha = im.split()[3] if has_alpha else None
    rgb = im.convert("RGB")
    gray = ImageOps.grayscale(rgb)
    gray = ImageEnhance.Contrast(gray).enhance(CONTRAST)
    gray = ImageEnhance.Brightness(gray).enhance(1.05)
    gray = gray.filter(ImageFilter.SMOOTH_MORE)
    return gray, alpha


def to_ascii_grid(gray, alpha=None):
    w, h = gray.size
    rows = max(1, round(COLS * (h / w) * CHAR_ASPECT))
    small = gray.resize((COLS, rows), Image.LANCZOS)
    small_alpha = alpha.resize((COLS, rows), Image.LANCZOS) if alpha else None
    pixels = list(small.getdata())
    alpha_px = list(small_alpha.getdata()) if small_alpha else None
    ramp = RAMP
    n = len(ramp) - 1
    grid = []
    for y in range(rows):
        row_chars = []
        for x in range(COLS):
            i = y * COLS + x
            if alpha_px is not None and alpha_px[i] < 100:
                row_chars.append(" ")
                continue
            p = pixels[i]
            p = 255 * ((p / 255) ** GAMMA)
            if p < WHITE_FLOOR:
                row_chars.append(" ")
                continue
            idx = int((p / 255) * n)
            row_chars.append(ramp[idx])
        grid.append("".join(row_chars))
    return grid


def esc(c):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


def build_svg(grid, out_path):
    rows = len(grid)
    cols = COLS
    char_w = FONT_SIZE * 0.6
    pad = 14
    width = cols * char_w + pad * 2
    height = rows * LINE_HEIGHT + pad * 2 + 26

    total_type_time = STAGGER * rows + ROW_DUR * cols + 0.4

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="100%">')
    svg.append(f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" rx="10" fill="{BG}"/>')
    svg.append(f'<rect x="0.5" y="0.5" width="{width-1:.0f}" height="{height-1:.0f}" rx="10" fill="none" stroke="{DIM}"/>')
    svg.append(
        f'<text x="{pad}" y="{pad+10}" font-family="Consolas,Menlo,monospace" '
        f'font-size="10" fill="{DIM}">{esc(USERNAME)} ~ $ ./portrait.sh</text>'
    )

    style = f"""
<style>
  .ascii-row {{
    font-family: 'Consolas','SF Mono','Menlo',monospace;
    font-size: {FONT_SIZE}px;
    fill: {FG};
    white-space: pre;
  }}
  .cursor {{
    fill: {FG};
    animation: blink 1s steps(1) infinite;
    animation-delay: {total_type_time:.2f}s;
    opacity: 0;
  }}
  @keyframes blink {{
    0%   {{ opacity: 1; }}
    50%  {{ opacity: 0; }}
    100% {{ opacity: 1; }}
  }}
</style>
"""
    svg.append(style)

    base_y = pad + 26
    for i, row in enumerate(grid):
        row_start = STAGGER * i
        row_len = max(1, len(row.rstrip()))
        dur = max(0.15, ROW_DUR * row_len)
        y = base_y + i * LINE_HEIGHT
        row_esc = "".join(esc(c) for c in row)
        clip_id = f"clip{i}"
        if STATIC:
            svg.append(
                f'<text class="ascii-row" x="{pad}" y="{y}">{row_esc}</text>'
            )
        else:
            svg.append(
                f'<clipPath id="{clip_id}">'
                f'<rect x="{pad}" y="{y - FONT_SIZE}" width="0" height="{FONT_SIZE+4}">'
                f'<animate attributeName="width" from="0" to="{cols*char_w:.1f}" '
                f'begin="{row_start:.2f}s" dur="{dur:.2f}s" fill="freeze" '
                f'calcMode="spline" keySplines="0.25 0 0.3 1" keyTimes="0;1"/>'
                f'</rect></clipPath>'
            )
            svg.append(
                f'<text class="ascii-row" x="{pad}" y="{y}" clip-path="url(#{clip_id})">{row_esc}</text>'
            )

    last_row = grid[-1].rstrip()
    cursor_x = pad + len(last_row) * char_w
    cursor_y = base_y + (rows - 1) * LINE_HEIGHT
    svg.append(
        f'<rect class="cursor" x="{cursor_x:.1f}" y="{cursor_y-FONT_SIZE+1:.1f}" '
        f'width="{char_w*0.85:.1f}" height="{FONT_SIZE+1}"/>'
    )

    svg.append("</svg>")
    with open(out_path, "w") as f:
        f.write("\n".join(svg))
    print(f"wrote {out_path}  ({cols} x {rows} chars, ~{total_type_time:.1f}s type animation)")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "photo.png"
    dst = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"
    gray, alpha = load_and_prep(src)
    grid = to_ascii_grid(gray, alpha)
    build_svg(grid, dst)
